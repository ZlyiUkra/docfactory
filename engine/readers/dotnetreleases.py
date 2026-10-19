"""Читач метаданих випусків .NET: releases-index.json і releases.json кожної лінії dotnet/core.

`dotnet-releases` — `url` — releases-index.json репозиторію dotnet/core
                    (https://raw.githubusercontent.com/dotnet/core/<гілка>/release-notes/releases-index.json):
                    перелік ліній з фазою підтримки, типом (LTS/STS), датою кінця підтримки й
                    останнім випуском. `releases.json` кожної лінії береться з тієї самої гілки поруч
                    («release-notes/8.0/releases.json»), а не з адреси builds.dotnet.microsoft.com, яку
                    називає індекс: файл той самий, а білий список лишається одним репозиторієм.
                    `lines` — перелік ліній, які беруться («10.0» … «1.0»; без поля — усі з індексу);
                    `stable: true` — без передрелізів (preview, rc).

Документи: огляд усіх ліній («overview»), документ на лінію («line-8-0», версія «8.0») — фаза,
тип, кінець підтримки й таблиця всіх її випусків — і документ на випуск («release-8-0-5», версія
«8.0.5»): дата, чи безпековий, CVE з посиланнями, версії runtime, SDK (з версіями C#, F#, VB і
Visual Studio), ASP.NET Core Runtime з модулем IIS, Windows Desktop і посилання на нотатки
випуску. Переліки файлів для завантаження (адреси й хеші) не беруться: це тисячі рядків без
змісту для питань.

Навіщо. Документація каже, що є у версії, але не каже, які лінії ще підтримуються, коли
закінчиться підтримка, який SDK іде з яким runtime і які CVE закрив випуск. Читач лише
переписує факти з офіційних файлів і нічого не виводить сам: дата й фаза — такі, як у файлі.
"""

import json
import re

from engine.readers import Item, _markup, register

_INDEX = re.compile(r"^(https://raw\.githubusercontent\.com/[^/]+/[^/]+/[^/]+/release-notes/)releases-index\.json$")


def _key(v: str) -> tuple:
    nums = re.findall(r"\d+", v.split("-", 1)[0])
    return tuple(int(x) for x in nums) + ((1,) if "-" not in v else (0,))


def _ver(obj) -> str:
    return (obj or {}).get("version-display") or (obj or {}).get("version") or ""


def _json(ctx, url: str):
    try:
        return json.loads(ctx.text(url))
    except ValueError as exc:
        raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")


def _release_body(r: dict, line: dict) -> str:
    # Фаза й кінець підтримки — властивість лінії, а не випуску: повторені в кожному з трьохсот
    # документів випусків, вони забирали всю видачу на запит «end of support» у документа лінії.
    out = [f"Release date: {r.get('release-date', '')}",
           f"Release line: .NET {line.get('channel-version', '')}",
           f"Security release: {'yes' if r.get('security') else 'no'}", ""]
    cves = r.get("cve-list") or []
    if cves:
        out += ["## Security fixes (CVE)", ""]
        out += [f"- {c.get('cve-id', '')}: {c.get('cve-url', '')}" for c in cves]
        out.append("")
    rt = r.get("runtime") or {}
    if rt:
        out += ["## .NET Runtime", "", f"Version: {_ver(rt)}"]
        if rt.get("vs-version"):
            out.append(f"Visual Studio: {rt['vs-version']}")
        if rt.get("vs-mac-version"):
            out.append(f"Visual Studio for Mac: {rt['vs-mac-version']}")
        out.append("")
    sdks = r.get("sdks") or ([r["sdk"]] if r.get("sdk") else [])
    if sdks:
        out += ["## .NET SDK", ""]
        for s in sdks:
            langs = ", ".join(f"{n} {s[k]}" for n, k in (("C#", "csharp-version"), ("F#", "fsharp-version"),
                                                         ("Visual Basic", "vb-version")) if s.get(k))
            row = f"- SDK {_ver(s)}"
            if s.get("runtime-version"):
                row += f" (runtime {s['runtime-version']})"
            if langs:
                row += f"; {langs}"
            vs = s.get("vs-support") or s.get("vs-version")
            if vs:
                row += f"; Visual Studio: {vs}"
            out.append(row)
        out.append("")
    asp = r.get("aspnetcore-runtime") or {}
    if asp:
        out += ["## ASP.NET Core Runtime", "", f"Version: {_ver(asp)}"]
        ancm = asp.get("version-aspnetcoremodule") or []
        if ancm:
            out.append(f"ASP.NET Core Module (IIS): {', '.join(ancm)}")
        if asp.get("vs-version"):
            out.append(f"Visual Studio: {asp['vs-version']}")
        out.append("")
    wd = r.get("windowsdesktop") or {}
    if wd:
        out += ["## Windows Desktop Runtime", "", f"Version: {_ver(wd)}", ""]
    if r.get("release-notes"):
        out += [f"Release notes: {r['release-notes']}", ""]
    return "\n".join(out)


@register("dotnet-releases")
def dotnet_releases(source: dict, ctx) -> list[Item]:
    m = _INDEX.match(source["url"])
    if not m:
        raise SystemExit(f"{source['url']}: очікував releases-index.json на raw.githubusercontent.com "
                         f"(…/release-notes/releases-index.json).")
    base = m.group(1)
    blob = base.replace("https://raw.githubusercontent.com/", "https://github.com/", 1)
    blob = re.sub(r"^(https://github\.com/[^/]+/[^/]+/)", r"\1blob/", blob)
    stable = source.get("stable") is True
    index = _json(ctx, source["url"]).get("releases-index") or []
    wanted = source.get("lines")
    lines = [c for c in index if not wanted or c.get("channel-version") in wanted]
    if not lines:
        raise SystemExit(f"{source['url']}: в індексі немає жодної з ліній {wanted}.")
    data: dict = {}
    for c in lines:
        ch = c["channel-version"]
        url = f"{base}{ch}/releases.json"
        if not ctx.allowed(url):
            raise SystemExit(f"{url}: поза білим списком — додайте префікс у within.")
        d = _json(ctx, url)
        rels = [r for r in d.get("releases") or []
                if not (stable and "-" in (r.get("release-version") or ""))]
        data[ch] = (d, rels)

    def overview():
        out = ["| Line | Type | Support phase | End of support | Latest release | Released | Latest SDK |",
               "|---|---|---|---|---|---|---|"]
        for c in lines:
            d = data[c["channel-version"]][0]
            out.append(f"| .NET {c['channel-version']} | {(c.get('release-type') or '').upper()} | "
                       f"{c.get('support-phase', '')} | {d.get('eol-date') or c.get('eol-date') or ''} | "
                       f"{c.get('latest-release', '')} | {c.get('latest-release-date', '')} | "
                       f"{c.get('latest-sdk', '')} |")
        body = ("Release lines of .NET (formerly .NET Core) with their support status, as published in "
                "the official release metadata.\n\n" + "\n".join(out))
        return _markup.document(".NET release lines and support status", blob + "releases-index.json",
                                ctx.stamp, body)

    items = [Item(id=f"{source['id']}/overview", file=f"{source['id']}--overview.txt",
                  make=overview)]
    for c in lines:
        ch = c["channel-version"]
        d, rels = data[ch]

        def line_doc(ch=ch, d=d, rels=rels):
            kind = (d.get("release-type") or "").upper()
            kind = {"LTS": "long-term support (LTS)", "STS": "standard-term support (STS)"}.get(kind, kind)
            head = [f".NET {ch} release type: {kind}.",
                    f"Support phase: {d.get('support-phase', '')}"]
            if d.get("eol-date"):
                head.append(f"End of support: {d['eol-date']}")
            head += [f"Latest release: {d.get('latest-release', '')} ({d.get('latest-release-date', '')})",
                     f"Latest runtime: {d.get('latest-runtime', '')}",
                     f"Latest SDK: {d.get('latest-sdk', '')}"]
            if d.get("lifecycle-policy"):
                head.append(f"Lifecycle policy: {d['lifecycle-policy']}")
            rows = ["| Version | Date | Security | Runtime | SDK | ASP.NET Core | CVEs |", "|---|---|---|---|---|---|---|"]
            for r in rels:
                sdks = r.get("sdks") or ([r["sdk"]] if r.get("sdk") else [])
                rows.append(f"| {r.get('release-version', '')} | {r.get('release-date', '')} | "
                            f"{'yes' if r.get('security') else 'no'} | {_ver(r.get('runtime'))} | "
                            f"{', '.join(_ver(s) for s in sdks)} | {_ver(r.get('aspnetcore-runtime'))} | "
                            f"{', '.join(x.get('cve-id', '') for x in r.get('cve-list') or [])} |")
            body = "\n".join(head) + "\n\n## Releases\n\n" + "\n".join(rows)
            return _markup.document(f".NET {ch} support phase, end of support and releases",
                                    f"{blob}{ch}/releases.json",
                                    ctx.stamp, body, ch)

        name = f"line-{_markup.slug(ch)}"
        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=line_doc))
        seen = set()
        for r in sorted(rels, key=lambda r: _key(r.get("release-version", "")), reverse=True):
            v = r.get("release-version") or ""
            if not v or v in seen:
                continue
            seen.add(v)

            def rel_doc(r=r, d=d, v=v, ch=ch):
                title = f".NET {v} release ({r.get('release-date', '')})"
                return _markup.document(title, r.get("release-notes") or f"{blob}{ch}/releases.json",
                                        ctx.stamp, _release_body(r, d), v)

            name = f"release-{_markup.slug(v)}"
            items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=rel_doc))
    return items
