"""Засів сховища сирого примірника з голого клону — для джерел читача `snooty-history`.

    .venvs/gpu/bin/python tools/seed_snooty_store.py --instance mongodb \\
        --clone mongodb/docs=/шлях/до/docs.git --clone 10gen/docs-shared=/шлях/до/docs-shared.git [--dry-run]

Навіщо. Репозиторій документації MongoDB — 60 тисяч файлів у двох десятках гілок; `refresh` тягне їх
мережею по одному (~1,3 файла/с, сім годин), хоча blob, що не мінявся між гілками, той самий. Голий клон
(`git clone --bare https://github.com/mongodb/docs.git`) має всі blob-и локально, а GitHub віддає за адресою
raw.githubusercontent.com байт у байт той самий blob. Інструмент кладе кожен blob у сховище під тією адресою,
за якою його брав би `refresh`, і пише мапу `raw/snooty-blobs.json` «sha → адреса», якою читач бере один
текст для всіх гілок, де він не змінився. Далі `./df <примірник> build` збирає корпус без мережі.

Білий список не слабшає: беруться лише ті гілки й теки, що оголошені у `sources.json` джерелами
`snooty-history` (`refs` × `folders`, спільні вставки `shared_url`/`shared_ref`), і лише з клонів, названих у
`--clone owner/repo=шлях`. Дерева гілок (`git/trees/<sha>?recursive=1`) інструмент не кладе — їх `build`
візьме мережею через API, це кількасот запитів.

Нічого не видаляє й не перезаписує: запис, який у сховищі вже є, лишається.
"""

import argparse
import json
import pathlib
import subprocess
import sys
import time
from urllib.parse import quote

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from engine import rawstore  # noqa: E402

RAW = "https://raw.githubusercontent.com"
# Картинки й двійкові файли читачеві не потрібні — у сховище не йдуть.
SKIP = (".png", ".gif", ".jpg", ".jpeg", ".svg", ".ico", ".pdf", ".webp", ".mp4", ".zip", ".drawio", ".jam",
        ".woff", ".woff2", ".ttf", ".eot")


def _repo_of(api_url: str) -> str:
    """`https://api.github.com/repos/mongodb/docs/git/trees/` → `mongodb/docs`."""
    parts = api_url.split("/repos/", 1)[-1].split("/")
    return "/".join(parts[:2])


def _plan(sources: list[dict]) -> dict[str, list[tuple[str, list[str], str]]]:
    """repo → [(ref, теки, source_dir)]; теки "" — проєкт у корені (беруться лише source/, snooty.toml,
    conf.py), інакше — уся тека проєкту монорепозиторію. Спільні вставки — увесь ref."""
    plan: dict[str, list] = {}
    for src in sources:
        if src.get("reader") != "snooty-history":
            continue
        repo = _repo_of(src["url"])
        folders = src.get("folders") or [""]
        folders = list(folders.keys()) if isinstance(folders, dict) else list(folders)
        refs = src.get("refs") or {}
        refs = list(refs.keys()) if isinstance(refs, dict) else list(refs)
        for ref in refs:
            plan.setdefault(repo, []).append((ref, folders, src.get("source_dir", "source")))
        if src.get("shared_url"):
            plan.setdefault(_repo_of(src["shared_url"]), []).append((src.get("shared_ref", "main"), ["*"], ""))
    return plan


def _ls(clone: pathlib.Path, ref: str, folder: str):
    args = ["git", "-C", str(clone), "ls-tree", "-r", "-l", ref] + (["--", folder] if folder else [])
    out = subprocess.run(args, capture_output=True, text=True, errors="replace")
    if out.returncode:
        raise SystemExit(f"{clone}: git ls-tree {ref} {folder}: {out.stderr.strip()}")
    for ln in out.stdout.splitlines():
        meta, path = ln.split("\t", 1)
        mode, typ, sha, _size = meta.split()
        if typ == "blob":
            yield sha, path


def _wanted(path: str, folder: str, source_dir: str) -> bool:
    if path.lower().endswith(SKIP):
        return False
    if folder in ("", "*"):
        if folder == "*":
            return True
        return path.startswith(source_dir + "/") or path in ("snooty.toml", "conf.py")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--instance", required=True, help="назва примірника (тека в instances/)")
    ap.add_argument("--clone", action="append", default=[], metavar="owner/repo=шлях",
                    help="голий клон репозиторію; повторюваний")
    ap.add_argument("--dry-run", action="store_true", help="лише порахувати, нічого не писати")
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    inst = root / "instances" / args.instance
    if not (inst / "sources.json").exists():
        raise SystemExit(f"{inst}: немає sources.json")
    data = json.loads((inst / "sources.json").read_text(encoding="utf-8"))
    sources = data["sources"] if isinstance(data, dict) else data
    clones = {}
    for item in args.clone:
        repo, _, path = item.partition("=")
        if not path or not pathlib.Path(path).exists():
            raise SystemExit(f"--clone {item}: немає такої теки")
        clones[repo] = pathlib.Path(path)
    plan = _plan(sources)
    if not plan:
        raise SystemExit(f"{inst}: жодного джерела snooty-history")
    missing = [r for r in plan if r not in clones]
    for r in missing:
        # Без клона репозиторій лишається мережі: `refresh`/`build` візьмуть його через API як завжди.
        print(f"  {r}: клона не дано — лишається мережі", flush=True)
        plan.pop(r)
    if not plan:
        raise SystemExit("жодного клона з --clone owner/repo=шлях не збіглося з джерелами")

    store = None if args.dry_run else rawstore.of(inst, time.strftime("%Y-%m-%d"))
    if store is None and not args.dry_run:
        raise SystemExit(f"{inst}: сховище сирого вимкнено (raw_store: false)")
    mappath = (store.root / "snooty-blobs.json") if store else None
    by_sha = json.loads(mappath.read_text(encoding="utf-8")) if mappath and mappath.exists() else {}
    t0 = time.time()
    written = seen = skipped = 0
    for repo, entries in plan.items():
        clone = clones[repo]
        proc = None if args.dry_run else subprocess.Popen(
            ["git", "-C", str(clone), "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        for ref, folders, source_dir in entries:
            for folder in folders:
                for sha, path in _ls(clone, ref, "" if folder == "*" else folder):
                    if not _wanted(path, folder, source_dir):
                        continue
                    seen += 1
                    if sha in by_sha:
                        skipped += 1
                        continue
                    url = f"{RAW}/{repo}/{quote(ref, safe='@')}/{quote(path)}"
                    if args.dry_run:
                        by_sha[sha] = url
                        written += 1
                        continue
                    proc.stdin.write((sha + "\n").encode())
                    proc.stdin.flush()
                    head = proc.stdout.readline().decode().split()
                    if len(head) < 3 or head[1] == "missing":
                        continue
                    n = int(head[2])
                    blob = proc.stdout.read(n)
                    proc.stdout.read(1)
                    if store.meta(url) is None:
                        store.put(url, "", blob, {})
                    by_sha[sha] = url
                    written += 1
                    if written % 5000 == 0:
                        mappath.write_text(json.dumps(by_sha, indent=0), encoding="utf-8")
                        print(f"  {written} записів, {time.time() - t0:.0f} с", flush=True)
        if proc:
            proc.stdin.close()
            proc.wait()
    if mappath:
        mappath.write_text(json.dumps(by_sha, indent=0), encoding="utf-8")
    verb = "порахував би" if args.dry_run else "записано"
    print(f"готово: файлів у плані {seen}, {verb} {written}, повторних хешів {skipped}, мапа {len(by_sha)}, "
          f"{time.time() - t0:.0f} с")
    return 0


if __name__ == "__main__":
    sys.exit(main())
