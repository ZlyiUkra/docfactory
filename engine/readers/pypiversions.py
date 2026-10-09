"""Читач реєстру PyPI: що й коли виходило, з якою вимогою до Python, з якими залежностями й описом.

`pypi-versions` — `url` — опис проєкту в JSON API PyPI (https://pypi.org/pypi/ПРОЄКТ/json);
                  `label` — назва проєкту в заголовках. Поля:
                  `skip_versions` — вираз версій, що не беруться (`[a-z]` — без dev, rc, b);
                  `name_prefix` — рядок перед іменем документа: «overview» і «line-2» кількох
                  проєктів одного примірника інакше мали б спільний ключ розділу;
                  `readme: true` — ще й опис проєкту (те, що PyPI показує на сторінці версії):
                  один документ на кожен неповторний текст, з усіма версіями, де він був таким.

Навіщо. Те саме, що `npm-versions` для пакетів npm: документація каже, як працює інструмент, але
рідко — з якої версії щось є і що треба для встановлення. PyPI знає це точно для кожної версії:
дату публікації, вимогу до Python (`requires_python`), залежності з їхніми межами й умовами
(`requires_dist`: `acme>=5.8.0`, `pywin32>=300; sys_platform == "win32"`, додаткові набори
`extra == "test"`) і позначку yanked (версію відкликано, `pip install` без точного номера її
оминає). Звідси відповіді «яку версію certbot ставити на Python 3.8», «з якої версії плагін
Cloudflare вимагає бібліотеку cloudflare 4».

Звернення. Опис проєкту дає перелік версій, дати й позначку yanked, але залежності й вимога до
Python лежать лише в описі кожної версії (https://pypi.org/pypi/ПРОЄКТ/ВЕРСІЯ/json) — одне
звернення на версію. Опис версії зі старих завантажень буває без `requires_dist` (метадані взято з
архіву sdist): тоді залежності «невідомі», а не «жодної», і зміни відносно сусідніх версій для них
не рахуються — інакше таблиця вигадала б, що всі залежності прибрали й повернули.

Документи:
- огляд проєкту: найновіша версія, лінії з першою й останньою версією та датами, відкликані версії,
  з якої версії діяла кожна вимога до Python;
- по одному документу на мажорну лінію: розділ на кожну мінорну гілку, рядок на кожну версію —
  дата, позначка yanked, і що змінилося відносно попередньої версії у вимозі до Python і
  залежностях;
- з `readme: true` — описи проєкту; reStructuredText (так пише Certbot) розбирається як сторінка
  Sphinx (див. `_sphinx`).
"""

import hashlib
import json
import re

from engine.readers import Item, _markup, register

_NUM = re.compile(r"\d+")
# Вимога PEP 508: ім'я, набори в дужках, межі версій; умова — після «;».
_REQ = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*(\[[^\]]*\])?\s*(?:\(([^)]*)\))?([^;]*)(?:;(.*))?$")
_EXTRA = re.compile(r"""extra\s*==\s*['"]([^'"]+)['"]""")


def _key(v: str) -> tuple:
    return tuple(int(x) for x in _NUM.findall(v))


# Додаткові набори для розробки самого проєкту (`pip install certbot[test]`): користувачеві вони не
# потрібні, а в Certbot їх десятки рядків на кожну версію — таблиця тонула б у pytest і mypy.
_DEV_EXTRAS = {"dev", "dev3", "docs", "test", "lint", "type", "mypy", "all"}


def _deps(requires) -> dict | None:
    """`requires_dist` → {«ім'я [extra X]» → «межі (when умова)»}. None — PyPI залежностей не знає.
    Набори розробки (`_DEV_EXTRAS`) не беруться."""
    if requires is None:
        return None
    out = {}
    for line in requires:
        m = _REQ.match(line)
        if not m:
            out[line.strip()] = ""
            continue
        name = m.group(1).lower().replace("_", "-") + (m.group(2) or "")
        spec = (m.group(3) or m.group(4) or "").strip()
        marker = (m.group(5) or "").strip()
        extra = _EXTRA.search(marker)
        if extra:
            if extra.group(1).lower() in _DEV_EXTRAS:
                continue
            name += f" [extra {extra.group(1)}]"
            marker = _EXTRA.sub("", marker).strip()
            marker = re.sub(r"^(and|or)\s+|\s+(and|or)$", "", marker).strip()
        value = spec or "any version"
        if marker:
            value += f" (when {marker})"
        out[name] = value
    return out


def _diff(old: dict, new: dict) -> list[str]:
    out = []
    for k in sorted(set(old) | set(new)):
        if k not in old:
            out.append(f"dependency added: {k} {new[k]}")
        elif k not in new:
            out.append(f"dependency removed: {k}")
        elif old[k] != new[k]:
            out.append(f"dependency changed: {k} {old[k]} → {new[k]}")
    return out


def _overview(label, cite, stamp, rows, lines) -> str:
    out = [f"Latest version: {rows[-1]['v']} ({rows[-1]['day']}).", "", "## Release lines", ""]
    for ln in lines:
        rs = [r for r in rows if r["v"].split(".")[0] == ln]
        out.append(f"- {ln}.x: {len(rs)} versions; {rs[0]['v']} ({rs[0]['day']}) … "
                   f"{rs[-1]['v']} ({rs[-1]['day']})")
    yanked = [r for r in rows if r["yanked"] is not None]
    if yanked:
        out += ["", "## Yanked versions", "",
                "A yanked version stays downloadable by its exact number, but pip skips it "
                "when resolving a range.", ""]
        out += [f"- {r['v']} ({r['day']})" + (f": {r['yanked']}" if r["yanked"] else "")
                for r in yanked]
    spans: list = []
    for r in rows:
        if spans and spans[-1][0] == r["python"]:
            spans[-1][2] = r
        else:
            spans.append([r["python"], r, r])
    if any(p for p, _, _ in spans):
        out += ["", "## Required Python version", ""]
        out += [f"- {p or 'not declared'}: from {a['v']} ({a['day']}) to {b['v']} ({b['day']})"
                for p, a, b in spans]
    return _markup.document(f"{label} on PyPI: overview of all versions", cite, stamp,
                            "\n".join(out), ", ".join(reversed([r["v"] for r in rows])))


def _line_doc(label, cite, stamp, rows, ln) -> str:
    out: list[str] = []
    prev = None
    minor = None
    for r in rows:
        mm = ".".join(r["v"].split(".")[:2])
        if mm != minor:
            minor = mm
            out += ["", f"## {label} {mm}.x", ""]
        line = f"- {r['v']} — published {r['day']}"
        if r["yanked"] is not None:
            line += ", YANKED" + (f": {' '.join(r['yanked'].split())}" if r["yanked"] else "")
        changes = []
        if prev is None or prev["python"] != r["python"]:
            changes.append(f"requires Python {r['python'] or 'not declared'}")
        if r["deps"] is None:
            changes.append("dependencies not recorded on PyPI")
        elif prev is None or prev["deps"] is None:
            if r["deps"]:
                changes.append("dependencies: " + ", ".join(f"{k} {v}"
                                                            for k, v in r["deps"].items()))
        else:
            changes += _diff(prev["deps"], r["deps"])
        if changes:
            line += "; " + "; ".join(changes)
        out.append(line)
        if r["deps"] is not None or prev is None:
            prev = r
    body = (f"{len(rows)} published versions of line {ln}, oldest first, with what changed "
            f"against the previous version of the line.\n" + "\n".join(out))
    return _markup.document(f"{label} on PyPI: versions {ln}.x", cite, stamp, body,
                            ", ".join(reversed([r["v"] for r in rows])))


def _readme(text: str, kind: str) -> str:
    if "rst" in (kind or "text/x-rst"):
        from engine.readers import _sphinx
        return _sphinx.to_markdown(text)
    return text


@register("pypi-versions")
def pypi_versions(source: dict, ctx) -> list[Item]:
    url = source["url"]
    m = re.match(r"^https://pypi\.org/pypi/([^/]+)/json$", url)
    if not m:
        raise SystemExit(f"{url}: очікував https://pypi.org/pypi/ПРОЄКТ/json.")
    project = m.group(1)
    label = source.get("label") or project
    cite = f"https://pypi.org/project/{project}/"
    skip = re.compile(source["skip_versions"]) if source.get("skip_versions") else None
    try:
        pack = json.loads(ctx.text(url))
    except ValueError as exc:
        raise SystemExit(f"{url}: відповідь не JSON ({exc}).")
    rows = []
    texts: dict = {}
    for v, files in (pack.get("releases") or {}).items():
        # Версія без файлів — номер, чиї архіви видалено: встановити її неможливо.
        if not files or (skip and skip.search(v)):
            continue
        day = min(f.get("upload_time_iso_8601") or f.get("upload_time") or "" for f in files)
        rows.append({"v": v, "day": day[:10]})
    if not rows:
        raise SystemExit(f"{url}: жодної версії.")
    rows.sort(key=lambda r: _key(r["v"]))
    for r in rows:
        vurl = f"https://pypi.org/pypi/{project}/{r['v']}/json"
        try:
            info = json.loads(ctx.text(vurl)).get("info") or {}
        except ValueError as exc:
            raise SystemExit(f"{vurl}: відповідь не JSON ({exc}).")
        r["python"] = (info.get("requires_python") or "").strip()
        r["deps"] = _deps(info.get("requires_dist"))
        r["yanked"] = (info.get("yanked_reason") or "") if info.get("yanked") else None
        if source.get("readme") is True and (info.get("description") or "").strip():
            text = info["description"]
            h = hashlib.sha1(text.encode()).hexdigest()[:8]
            texts.setdefault(h, [text, info.get("description_content_type") or "", []])[2] \
                .append(r["v"])
    lines = sorted({r["v"].split(".")[0] for r in rows}, key=int)
    lead = (re.sub(r"[^\w.-]+", "-", source["name_prefix"]).strip("-") + "-"
            if source.get("name_prefix") else "")
    docs = {"overview": _overview(label, cite, ctx.stamp, rows, lines)}
    for ln in lines:
        docs[f"line-{ln}"] = _line_doc(label, f"{cite}#history", ctx.stamp,
                                       [r for r in rows if r["v"].split(".")[0] == ln], ln)
    for h, (text, kind, versions) in texts.items():
        body = _markup.markdown_body(_readme(text, kind))
        docs[f"readme-{h}"] = _markup.document(
            f"{label}: project description on PyPI", f"{cite}{versions[-1]}/", ctx.stamp, body,
            ", ".join(reversed(versions)))
    return [Item(id=f"{source['id']}/{lead}{name}", file=f"{source['id']}--{lead}{name}.txt",
                 make=lambda text=text: text) for name, text in docs.items()]
