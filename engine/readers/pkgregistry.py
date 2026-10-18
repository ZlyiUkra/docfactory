"""Читач таблиць версій пакета з реєстрів інших мов: RubyGems, Packagist, NuGet, Maven, CocoaPods.

`pkg-registry` — `kind` — реєстр (`rubygems`, `packagist`, `nuget`, `maven`, `cocoapods`), `url` — його
                 відповідь про пакет:
                 - rubygems: `https://rubygems.org/api/v1/versions/<gem>.json`;
                 - packagist: `https://repo.packagist.org/p2/<vendor>/<package>.json`;
                 - nuget: `https://api.nuget.org/v3/registration5-semver1/<id>/index.json` (сторінки
                   реєстрації дочитуються за їхніми адресами, тож вони мають бути в `within`);
                 - maven: `https://repo1.maven.org/maven2/<group>/<artifact>/maven-metadata.xml`;
                 - cocoapods: `https://trunk.cocoapods.org/api/v1/pods/<Pod>`.
                 Документ один на пакет: огляд (найновіша стабільна, скільки версій у кожній мажорній
                 лінії, перша й остання з датами) і розділ на мажорну лінію з кожною стабільною
                 версією, датою й вимогами (Ruby, PHP і розширення, цільові платформи .NET).
                 Передрелізи (`beta`, `alpha`, `rc`, `pre`) лише рахуються. `label` — назва пакета в
                 заголовку, `version_prefix` — мітка версій («ruby-»), `page` — людська сторінка.

Навіщо. Для SDK Stripe інших мов реєстри кажуть те, чого немає в репозиторії: коли версію
опубліковано і яку версію мови чи .NET вона вимагає. README у цих реєстрах — той самий, що на
GitHub, тож його не беремо.
"""

import json
import re
from xml.etree import ElementTree

from engine.readers import Item, _markup, register

_STABLE = re.compile(r"^v?\d+(\.\d+)*$")


def _rows_rubygems(ctx, source):
    for v in json.loads(ctx.text(source["url"])):
        yield v.get("number", ""), str(v.get("created_at", ""))[:10], \
            f"Ruby {v['ruby_version']}" if v.get("ruby_version") else ""


def _rows_packagist(ctx, source):
    data = json.loads(ctx.text(source["url"]))["packages"]
    req: dict = {}
    for v in next(iter(data.values())):
        # Packagist p2 стискає перелік: поле, однакове з попередньою версією, пропускає.
        if isinstance(v.get("require"), dict):
            req = v["require"]
        need = ", ".join(f"{k} {c}" for k, c in req.items())
        yield v.get("version", ""), str(v.get("time", ""))[:10], need


def _rows_nuget(ctx, source):
    index = json.loads(ctx.text(source["url"]))
    for page in index.get("items", []):
        leaves = page.get("items")
        if leaves is None:
            if not ctx.allowed(page["@id"]):
                continue
            leaves = json.loads(ctx.text(page["@id"])).get("items", [])
        for leaf in leaves:
            entry = leaf.get("catalogEntry") or {}
            fws = [g.get("targetFramework", "") for g in entry.get("dependencyGroups") or []]
            yield entry.get("version", ""), str(entry.get("published", ""))[:10], \
                ("targets " + ", ".join(f for f in fws if f)) if any(fws) else ""


def _rows_maven(ctx, source):
    root = ElementTree.fromstring(ctx.text(source["url"]))
    for v in root.iter("version"):
        yield (v.text or "").strip(), "", ""


def _rows_cocoapods(ctx, source):
    for v in json.loads(ctx.text(source["url"])).get("versions", []):
        yield v.get("name", ""), str(v.get("created_at", ""))[:10], ""


_KINDS = {"rubygems": _rows_rubygems, "packagist": _rows_packagist, "nuget": _rows_nuget,
          "maven": _rows_maven, "cocoapods": _rows_cocoapods}


def _key(v: str):
    return tuple(int(x) for x in re.findall(r"\d+", v)[:4])


@register("pkg-registry")
def pkg_registry(source: dict, ctx) -> list[Item]:
    kind = source.get("kind")
    if kind not in _KINDS:
        raise SystemExit(f"{source['id']}: поле kind — одне з {', '.join(_KINDS)}.")
    label = source.get("label") or source["id"]
    prefix = source.get("version_prefix", "")
    name = _markup.slug(source.get("name_prefix") or label)

    def make():
        rows = [(v.lstrip("v"), d, need) for v, d, need in _KINDS[kind](ctx, source) if v]
        stable = sorted({r[0]: r for r in rows if _STABLE.match(r[0])}.values(),
                        key=lambda r: _key(r[0]), reverse=True)
        pre = len(rows) - len(stable)
        if not stable:
            raise SystemExit(f"{source['url']}: жодної стабільної версії.")
        lines: dict[str, list] = {}
        for r in stable:
            lines.setdefault(r[0].split(".")[0], []).append(r)
        out = ["## Overview", "",
               f"Latest stable: {stable[0][0]}" + (f" ({stable[0][1]})" if stable[0][1] else "") + ".",
               f"Stable versions: {len(stable)}; pre-releases (alpha, beta, rc): {pre}.", ""]
        for major, rs in lines.items():
            first, last = rs[-1], rs[0]
            out.append(f"- {major}.x: {len(rs)} versions, {first[0]}"
                       + (f" ({first[1]})" if first[1] else "") + f" … {last[0]}"
                       + (f" ({last[1]})" if last[1] else ""))
        for major, rs in lines.items():
            out += ["", f"## {label} {major}.x", ""]
            for v, d, need in rs:
                out.append(f"- {v}" + (f" — {d}" if d else "") + (f"; requires {need}" if need else ""))
        versions = ", ".join(prefix + r[0] for r in stable)
        return _markup.document(f"{label}: all versions ({kind})", source.get("page") or source["url"],
                                ctx.stamp, "\n".join(out), versions)

    return [Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make)]
