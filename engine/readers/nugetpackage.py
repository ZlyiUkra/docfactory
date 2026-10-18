"""Читач NuGet: пакети — їх версії, описи, залежності й README.

`nuget-package` — `packages` — перелік ідентифікаторів пакетів NuGet. Для кожного пакета
реєстр (api.nuget.org/v3/registration5-semver1/ПАКЕТ/index.json) дає всі опубліковані
версії з датою, описом, цільовими платформами й залежностями. З цього складаються:

- огляд пакета («<пакет>-versions»): опис, проєкт, ліцензія і таблиця всіх стабільних
  версій з датою випуску — по лініях «мажор.мінор»;
- документ на кожну лінію («<пакет>-<лінія>»): версії лінії, платформи й залежності
  найновішої версії лінії, зміни опису та залежностей між версіями;
- README — для версій, що його несуть (у пакетах ASP.NET Core — з 9.0): найновіша
  версія кожної лінії, однакові тексти — один документ з усіма версіями
  («<пакет>-readme-<хеш>»), як у `npm-readme`.

Попередні випуски (`-preview`, `-rc`) не беруться: корпус — про стабільні версії. Поле
`version_prefix` стає перед версією в шапці — для пакетів, чия нумерація не збігається з
нумерацією продукту (класичний ASP.NET: «mvc-5.2.9»); `version_prefixes` — те саме
перелік пар [вираз імені пакета, префікс], коли в одному джерелі пакети різних продуктів.
"""

import hashlib
import json
import re

from engine.readers import Item, _markup, register

_REG = "https://api.nuget.org/v3/registration5-semver1/"
_FLAT = "https://api.nuget.org/v3-flatcontainer/"
_STABLE = re.compile(r"^\d+(?:\.\d+){1,3}$")
_BUILT_FROM = re.compile(r"\s*This package was built from the source code at \S+")


def _key(v: str) -> tuple:
    return tuple(int(x) for x in v.split("."))


def _line(v: str) -> str:
    return ".".join(v.split(".")[:2])


def _entries(pkg: str, ctx) -> list[dict]:
    """Записи catalogEntry усіх версій пакета. Реєстр великого пакета ділить версії на
    сторінки, і сторінка без `items` — посилання, яке треба дочитати окремо."""
    url = f"{_REG}{pkg.lower()}/index.json"
    try:
        data = json.loads(ctx.text(url))
    except ValueError as exc:
        raise SystemExit(f"{url}: відповідь не JSON ({exc}).")
    out = []
    for page in data.get("items", []):
        items = page.get("items")
        if items is None:
            try:
                items = json.loads(ctx.text(page["@id"])).get("items", [])
            except ValueError as exc:
                raise SystemExit(f"{page['@id']}: відповідь не JSON ({exc}).")
        out.extend(i["catalogEntry"] for i in items if "catalogEntry" in i)
    return out


def _deps(entry: dict) -> list[str]:
    rows = []
    for g in entry.get("dependencyGroups") or []:
        fw = g.get("targetFramework") or "any"
        deps = ", ".join(f"{d.get('id')} {d.get('range', '')}".strip()
                         for d in g.get("dependencies") or [])
        rows.append(f"- {fw}: {deps or '(no dependencies)'}")
    return rows


@register("nuget-package")
def nuget_package(source: dict, ctx) -> list[Item]:
    prefixes = [(re.compile(a), b) for a, b in source.get("version_prefixes") or []]
    items = []
    for pkg in source["packages"]:
        vp = next((b for a, b in prefixes if a.search(pkg)), source.get("version_prefix", ""))
        url_reg = f"{_REG}{pkg.lower()}/index.json"
        if not ctx.allowed(url_reg):
            continue
        entries = [e for e in _entries(pkg, ctx) if _STABLE.match(e.get("version", ""))
                   and e.get("listed", True) is not False]
        if not entries:
            continue
        entries.sort(key=lambda e: _key(e["version"]))
        name = _markup.slug(pkg)
        cite = f"https://www.nuget.org/packages/{pkg}"
        lines: dict = {}
        for e in entries:
            lines.setdefault(_line(e["version"]), []).append(e)

        def overview(pkg=pkg, entries=entries, lines=lines, cite=cite):
            last = entries[-1]
            body = [f"Package: {pkg}", ""]
            if last.get("description"):
                body += [last["description"].strip(), ""]
            for k, label in (("projectUrl", "Project"), ("licenseExpression", "License"),
                             ("authors", "Authors")):
                if last.get(k):
                    body.append(f"{label}: {last[k]}")
            if last.get("tags"):
                body.append("Tags: " + ", ".join(last["tags"]) if isinstance(last["tags"], list)
                            else f"Tags: {last['tags']}")
            body += ["", f"Stable versions: {len(entries)}, from {entries[0]['version']} "
                         f"({entries[0].get('published', '')[:10]}) to {last['version']} "
                         f"({last.get('published', '')[:10]}).", ""]
            for ln, rows in lines.items():
                body += [f"## {pkg} {ln}", ""]
                body += [f"- {r['version']} — {r.get('published', '')[:10]}" for r in rows]
                body.append("")
            return _markup.document(f"{pkg} — NuGet package versions", cite, ctx.stamp,
                                    _markup.tidy("\n".join(body), strip=False))

        items.append(Item(id=f"{source['id']}/{name}-versions",
                          file=f"{source['id']}--{name}-versions.txt", make=overview))

        for ln, rows in lines.items():
            def line_doc(pkg=pkg, ln=ln, rows=rows, cite=cite, vp=vp):
                last = rows[-1]
                body = [f"Package: {pkg}, line {ln}: versions "
                        + ", ".join(r["version"] for r in rows) + ".", ""]
                if last.get("description"):
                    body += ["Description:", "", last["description"].strip(), ""]
                deps = _deps(last)
                if deps:
                    body += [f"## Dependencies of {pkg} {last['version']}", "", *deps, ""]
                prev = None
                changes = []
                for r in rows:
                    # Опис пакетів ASP.NET Core 3.0+ закінчується комітом збирання — він
                    # різний у кожній версії і змінами опису не є.
                    d = _BUILT_FROM.sub("", (r.get("description") or "")).strip()
                    if prev is not None and d != prev:
                        changes.append(f"- {r['version']}: description changed to: {d}")
                    prev = d
                if changes:
                    body += ["## Description changes", "", *changes, ""]
                return _markup.document(f"{pkg} {ln} — NuGet package", f"{cite}/{last['version']}",
                                        ctx.stamp, _markup.tidy("\n".join(body), strip=False),
                                        vp + last["version"])

            items.append(Item(id=f"{source['id']}/{name}-{_markup.slug(ln)}",
                              file=f"{source['id']}--{name}-{_markup.slug(ln)}.txt",
                              make=line_doc))

        # README: найновіша версія кожної лінії, однакові тексти — один документ.
        if not source.get("readme", True):
            continue
        seen: dict = {}
        for ln, rows in lines.items():
            v = rows[-1]["version"]
            url = f"{_FLAT}{pkg.lower()}/{v.lower()}/readme"
            if not ctx.allowed(url) or (source.get("readme_from") and
                                        _key(v) < _key(source["readme_from"])):
                continue
            code, data = ctx.fetch(url)
            if code != "200" or not data.strip():
                continue
            h = hashlib.sha256(data).hexdigest()[:8]
            seen.setdefault(h, (url, []))[1].append(v)
        for h, (url, versions) in seen.items():
            def readme(url=url, versions=versions, pkg=pkg, vp=vp):
                text = ctx.text(url)
                meta, rest = _markup.front_matter(text)
                body = _markup.markdown_body(rest)
                body = f"README of the NuGet package {pkg}, versions {', '.join(versions)}.\n\n{body}"
                return _markup.document(f"{pkg} README", f"https://www.nuget.org/packages/{pkg}/"
                                        f"{versions[-1]}#readme-body-tab", ctx.stamp, body,
                                        vp + versions[-1])

            items.append(Item(id=f"{source['id']}/{name}-readme-{h}",
                              file=f"{source['id']}--{name}-readme-{h}.txt", make=readme))
    if not items:
        raise SystemExit(f"{source['id']}: жодного пакета з дозволеного переліку.")
    return items
