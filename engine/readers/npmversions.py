"""Читач реєстру версій npm: що й коли виходило, з якими мітками, точками входу й залежностями.

`npm-versions` — `url` — опис пакета в реєстрі (https://registry.npmjs.org/ПАКЕТ); `label` — назва
                 пакета в заголовках. Одне звернення: опис пакета вже містить усі версії.

Навіщо. Документація каже, як працює API, але рідко — з якої версії він є і як перейти з однієї
версії на іншу. Реєстр npm знає це точно для кожної версії, яку можна встановити, зокрема canary,
alpha, beta й next: дату публікації, мітку поширення (`latest`, `beta`…), позначку deprecated,
точки входу пакета (`exports`: з якої версії імпортується `zod/v4` чи `zod/mini`), залежності,
peer-залежності й вимоги до Node. Тому реєстр — база для питань «з якої версії», «що
змінилося», «що встановити», і з нього читаються всі версії без відсіву.

Документи:
- огляд пакета: поточні мітки, перелік ліній з першою й останньою версією та датами, і для кожної
  точки входу — перша й остання версія, де вона була;
- по одному документу на мажорну лінію: розділ на кожну мінорну гілку, рядок на кожну версію —
  дата, вид (стабільна, canary, beta…), мітки, і що змінилося відносно попередньої версії лінії в
  точках входу, залежностях і вимогах. Саме ці зміни — канва для переходу з версії на версію.

Версії документа лінії — усі її версії, тож фільтр `version: "4"` знаходить таблицю лінії 4.
"""

import json
import re

from engine.readers import Item, _markup, register

_SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?")


def _kind(v: str) -> str:
    m = _SEMVER.match(v)
    if not m or not m.group(4):
        return "stable"
    word = re.match(r"[A-Za-z]+", m.group(4))
    return word.group(0).lower() if word else "prerelease"


def _entries(meta: dict) -> list[str]:
    """Точки входу пакета: ключі `exports`, а без них — `main`/`module`."""
    exp = meta.get("exports")
    if isinstance(exp, dict):
        keys = [k for k in exp if k.startswith(".")]
        if keys:
            return sorted(keys)
        return ["."]
    if isinstance(exp, str):
        return ["."]
    return ["."] if (meta.get("main") or meta.get("module")) else []


def _deps(meta: dict, field: str) -> dict:
    d = meta.get(field)
    return {k: str(v) for k, v in d.items()} if isinstance(d, dict) else {}


def _diff(old: dict, new: dict, what: str) -> list[str]:
    out = []
    for k in sorted(set(old) | set(new)):
        if k not in old:
            out.append(f"{what} added: {k} {new[k]}")
        elif k not in new:
            out.append(f"{what} removed: {k}")
        elif old[k] != new[k]:
            out.append(f"{what} changed: {k} {old[k]} → {new[k]}")
    return out


@register("npm-versions")
def npm_versions(source: dict, ctx) -> list[Item]:
    url = source["url"]
    label = source.get("label") or url.rstrip("/").rsplit("/", 1)[-1]
    cite = f"https://www.npmjs.com/package/{url.split('registry.npmjs.org/', 1)[-1]}?activeTab=versions"

    def load() -> dict:
        try:
            pack = json.loads(ctx.text(url))
        except ValueError as exc:
            raise SystemExit(f"{url}: відповідь не JSON ({exc}).")
        times = pack.get("time") or {}
        versions = sorted((v for v in pack.get("versions") or {} if v in times),
                          key=lambda v: times[v])
        if not versions:
            raise SystemExit(f"{url}: жодної версії.")
        tags: dict = {}
        for t, v in (pack.get("dist-tags") or {}).items():
            tags.setdefault(v, []).append(t)
        # Лише потрібне з кожної версії: опис пакета великий, а в пам'яті його не тримаємо.
        rows = []
        for v in versions:
            meta = pack["versions"][v] or {}
            rows.append({
                "v": v, "day": times[v][:10], "kind": _kind(v), "tags": tags.get(v, []),
                "deprecated": str(meta.get("deprecated") or ""),
                "entries": _entries(meta),
                "deps": _deps(meta, "dependencies"),
                "peer": _deps(meta, "peerDependencies"),
                "engines": _deps(meta, "engines"),
            })
        return {"rows": rows, "dist_tags": pack.get("dist-tags") or {}}

    # Перелік ліній потрібен уже для переліку документів, тож опис читається тут; для запису
    # кожен документ читає його ще раз — у пам'яті між ними нічого не лишається.
    first = load()
    lines = sorted({r["v"].split(".")[0] for r in first["rows"]}, key=lambda x: (len(x), x))
    line_versions = {ln: [r["v"] for r in first["rows"] if r["v"].split(".")[0] == ln]
                     for ln in lines}
    del first

    items = []

    def make_overview():
        data = load()
        rows = data["rows"]
        out = ["## Current dist-tags", ""]
        out += [f"- `{t}` → {v}" for t, v in data["dist_tags"].items()]
        out += ["", "## Release lines", ""]
        for ln in lines:
            rs = [r for r in rows if r["v"].split(".")[0] == ln]
            st = [r for r in rs if r["kind"] == "stable"]
            kinds = {}
            for r in rs:
                kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
            span = (f"stable {st[0]['v']} ({st[0]['day']}) … {st[-1]['v']} ({st[-1]['day']})"
                    if st else "no stable release")
            out.append(f"- {ln}.x: {len(rs)} versions ("
                       + ", ".join(f"{k} {n}" for k, n in sorted(kinds.items()))
                       + f"); {span}")
        seen: dict = {}
        for r in rows:
            for e in r["entries"]:
                seen.setdefault(e, [r, r])[1] = r
        if seen:
            out += ["", "## Entry points (package exports)", "",
                    "First and last published version that had each import path:", ""]
            for e, (a, b) in sorted(seen.items(), key=lambda kv: kv[1][0]["day"]):
                path = label if e == "." else f"{label}/{e[2:]}"
                out.append(f"- `{path}`: from {a['v']} ({a['day']}) to {b['v']} ({b['day']})")
        body = "\n".join(out)
        return _markup.document(f"{label} npm registry: overview of all versions", cite,
                                ctx.stamp, body)

    items.append(Item(id=f"{source['id']}/overview", file=f"{source['id']}--overview.txt",
                      make=make_overview))

    for ln in lines:

        def make(ln=ln):
            rows = [r for r in load()["rows"] if r["v"].split(".")[0] == ln]
            out: list[str] = []
            prev = None
            minor = None
            for r in rows:
                m = _SEMVER.match(r["v"])
                mm = f"{m.group(1)}.{m.group(2)}" if m else r["v"]
                if mm != minor:
                    minor = mm
                    out += ["", f"## {label} {mm}.x", ""]
                line = f"- {r['v']} — published {r['day']}, {r['kind']}"
                if r["tags"]:
                    line += f", dist-tag {', '.join(r['tags'])}"
                if r["deprecated"]:
                    line += f", DEPRECATED: {' '.join(r['deprecated'].split())}"
                changes = []
                if prev is not None:
                    new_e = [e for e in r["entries"] if e not in prev["entries"]]
                    gone_e = [e for e in prev["entries"] if e not in r["entries"]]
                    if new_e:
                        changes.append("new import paths: " + ", ".join(
                            label if e == "." else f"{label}/{e[2:]}" for e in new_e))
                    if gone_e:
                        changes.append("removed import paths: " + ", ".join(
                            label if e == "." else f"{label}/{e[2:]}" for e in gone_e))
                    changes += _diff(prev["deps"], r["deps"], "dependency")
                    changes += _diff(prev["peer"], r["peer"], "peer dependency")
                    changes += _diff(prev["engines"], r["engines"], "engine")
                else:
                    if r["entries"]:
                        changes.append("import paths: " + ", ".join(
                            label if e == "." else f"{label}/{e[2:]}" for e in r["entries"]))
                    for what, d in (("dependencies", r["deps"]), ("peer dependencies",
                                    r["peer"]), ("engines", r["engines"])):
                        if d:
                            changes.append(f"{what}: " + ", ".join(f"{k} {v}"
                                                                   for k, v in d.items()))
                if changes:
                    line += "; " + "; ".join(changes)
                out.append(line)
                prev = r
            body = (f"{len(rows)} published versions of line {ln}, oldest first, with what "
                    f"changed against the previous version of the line.\n" + "\n".join(out))
            return _markup.document(f"{label} npm registry: versions {ln}.x", cite, ctx.stamp,
                                    body, ", ".join(reversed([r["v"] for r in rows])))

        items.append(Item(id=f"{source['id']}/line-{ln}",
                          file=f"{source['id']}--line-{ln}.txt", make=make))
    return items
