"""Читачі вмісту пакета npm: файли з tarball версії і файли репозиторію на коміті версії.

`npm-tarball-files` — один файл із tarball кожної версії пакета. `url` — опис пакета в реєстрі
                      (https://registry.npmjs.org/ПАКЕТ), `match` — вираз шляху файла в пакеті без
                      кореневої теки («package/»), `kind` — `markdown` (README) або `types`
                      (файл .d.ts, поділений на розділи за оголошеннями). Необов'язкові: `label` —
                      назва документа, `skip_versions` — вираз версій, що не беруться.
`npm-githead-files` — файли дерева репозиторію на коміті `gitHead` кожної версії. `url` — опис
                      пакета, `repo` — «власник/репозиторій», `include` — вираз шляхів, що беруться
                      (напр. `^examples/.*\\.js$`), `label`, `skip_versions` — як вище.

Навіщо. README пакета з найстаріших версій (0.0.1–0.2.0 у postgrator) не лежить ніде, крім
самого tarball: git-тегів у тих версій немає, а реєстр не записав `gitHead`. Типи `.d.ts` теж
живуть у пакеті версії, і tarball — єдине, що точно відповідає тому, що отримує `npm install`
(`npm-readme` бере README кореня репозиторію на коміті, що майже те саме, але не для версій
без коміту). Приклади ж у пакет не потрапляють (.npmignore), тож їх беруть із репозиторію.

Одиниця — неповторний текст (хеш) файла; версії документа — усі, у яких файл був саме таким.
Перелік складається одразу, але в пам'яті лишаються хеш, адреса й версії: сам текст читається
вдруге під час запису, як у `npm-readme`. Приклади впізнаються за хешем блоба з дерева GitHub,
тож вони не читаються двічі.
"""

import gzip
import hashlib
import io
import json
import re
import tarfile
from urllib.parse import quote

from engine.readers import Item, _markup, register
from engine.readers.dthistory import _sections
from engine.readers.ghhistory import _atx, _split_title


def _packument(source: dict, ctx) -> tuple[dict, list]:
    try:
        packument = json.loads(ctx.text(source["url"]))
    except ValueError as exc:
        raise SystemExit(f"{source['url']}: відповідь не JSON ({exc}).")
    times = packument.get("time") or {}
    skip = re.compile(source["skip_versions"]) if source.get("skip_versions") else None
    versions = sorted((v for v in packument.get("versions") or {}
                       if v in times and not (skip and skip.search(v))),
                      key=lambda v: times[v], reverse=True)
    if not versions:
        raise SystemExit(f"{source['url']}: жодної версії.")
    return packument, versions


def _package_name(source: dict) -> str:
    return re.sub(r"[^\w.-]+", "-", source["url"].split("registry.npmjs.org/", 1)[-1]
                  .replace("%2F", "/").replace("%2f", "/")).strip("-")


def _read_tarball(url: str, match, ctx) -> tuple[str, str]:
    """(шлях, текст) першого файла пакета, що збігся з виразом; ("", "") — такого файла немає."""
    data = ctx.bytes(url)
    if data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        for member in tar:
            if not member.isfile():
                continue
            path = member.name.split("/", 1)[-1]
            if match.search(path):
                return path, tar.extractfile(member).read().decode("utf-8", errors="replace")
    return "", ""


@register("npm-tarball-files")
def npm_tarball_files(source: dict, ctx) -> list[Item]:
    kind = source.get("kind", "markdown")
    if kind not in ("markdown", "types") or not source.get("match"):
        raise SystemExit(f"{source['id']}: читач npm-tarball-files потребує полів match і "
                         f"kind (markdown або types).")
    match = re.compile(source["match"])
    packument, versions = _packument(source, ctx)
    seen: dict = {}      # хеш тексту → [адреса tarball найновішої версії, [версії]]
    missing = []
    for v in versions:
        url = ((packument["versions"][v] or {}).get("dist") or {}).get("tarball", "")
        if not url or not ctx.allowed(url):
            missing.append(v)
            continue
        _, text = _read_tarball(url, match, ctx)
        text = text.replace("\r\n", "\n")
        if not text.strip():
            missing.append(v)
            continue
        key = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
        seen.setdefault(key, [url, []])[1].append(v)
        del text
    if missing:
        print(f"  {source['id']}: без файла {len(missing)} версій: {', '.join(missing[:12])}"
              f"{' …' if len(missing) > 12 else ''}")

    label = source.get("label", "README" if kind == "markdown" else "Types")
    package = _package_name(source)
    items = []
    for key, (url, found) in seen.items():
        name = f"{package}-{kind}-{key[:8]}"

        def make(url=url, found=found):
            _, text = _read_tarball(url, match, ctx)
            text = text.replace("\r\n", "\n")
            span = found[-1] if len(found) == 1 else f"{found[-1]} … {found[0]}"
            if kind == "markdown":
                meta, rest = _markup.front_matter(text)
                title, rest = _split_title(_atx(rest))
                body = _markup.markdown_body(rest)
                full = f"{label} {span}" + (f": {title}" if title else "")
            else:
                body = (f"Shipped in the npm package, version {', '.join(reversed(found))}.\n\n"
                        f"{_sections(text)}")
                full = f"{label} {span}"
            _markup.require(full, body, url, min_chars=1)
            return _markup.document(full, url, ctx.stamp, body, ", ".join(found))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодного файла за виразом {source['match']!r}.")
    return items


@register("npm-githead-files")
def npm_githead_files(source: dict, ctx) -> list[Item]:
    repo = source.get("repo", "")
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", repo) or not source.get("include"):
        raise SystemExit(f"{source['id']}: читач npm-githead-files потребує полів repo "
                         f"(власник/репозиторій) і include.")
    include = re.compile(source["include"])
    packument, versions = _packument(source, ctx)
    label = source.get("label", repo.split("/", 1)[1])
    package = _package_name(source)
    seen: dict = {}      # (шлях, sha блоба) → [sha коміту найновішої версії, [версії]]
    for v in versions:
        head = str((packument["versions"][v] or {}).get("gitHead") or "")
        if not head:
            continue
        url = f"https://api.github.com/repos/{repo}/git/trees/{head}?recursive=1"
        if not ctx.allowed(url):
            continue
        try:
            tree = json.loads(ctx.text(url))
        except SystemExit as exc:
            # Коміт версії міг зникнути з репозиторію (force-push): GitHub тоді дає 422.
            if "404" not in str(exc) and "422" not in str(exc):
                raise
            print(f"  {source['id']}: коміту {head[:8]} версії {v} немає в репозиторії — пропущено")
            continue
        if tree.get("truncated"):
            raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
        for entry in tree.get("tree") or []:
            path = entry.get("path", "")
            if entry.get("type") == "blob" and include.search(path):
                seen.setdefault((path, entry["sha"]), [head, []])[1].append(v)
    items = []
    for (path, blob_sha), (head, found) in seen.items():
        raw = f"https://raw.githubusercontent.com/{repo}/{head}/{quote(path)}"
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{repo}/blob/{head}/{quote(path)}"
        name = f"{package}-{_markup.slug(path)}-{blob_sha[:8]}"

        def make(path=path, raw=raw, blob=blob, found=found):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            ext = path.rsplit(".", 1)[-1] if "." in path else ""
            body = (f"File {path} in the repository, as it was in version "
                    f"{', '.join(reversed(found))}.\n\n```{ext}\n{text.rstrip()}\n```")
            title = f"{label}: {path}"
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, ", ".join(found))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодного файла за виразом {source['include']!r}.")
    return items
