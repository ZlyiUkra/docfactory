"""Читач тегів образу контейнера з реєстру за протоколом OCI (Docker Registry HTTP API v2).

`registry-tags` — `url` — перелік тегів образу (https://mcr.microsoft.com/v2/mssql/server/tags/list,
                  відповідь `{"name": …, "tags": […]}`); `image` — повна назва образу для команд
                  (`mcr.microsoft.com/mssql/server`); `line` — вираз з групою `v`, що дістає з тега
                  лінію («^(?P<v>20\\d\\d)-» — рік випуску SQL Server); `label` — назва образу в
                  заголовках; `page` — людська сторінка образу (на неї веде шапка документів).
                  Необов'язкове `version_prefix` — рядок перед міткою лінії у версіях документів.

Навіщо. Образ SQL Server на Linux має сотні тегів: кумулятивне оновлення (CU), виправлення
безпеки поверх нього (GDR), збірки на вимогу (OD), передвипуски (CTP, RC) і варіанти під кожну
версію Ubuntu. Документація каже «візьміть 2022-latest», але який тег закріплює CU 15 на Ubuntu
22.04, чи є для 2019 образ на Ubuntu 22.04 і коли зник образ на 16.04 — знає лише сам реєстр.

Документи:
- огляд образу: лінії з кількістю тегів, найновішим CU і плаваючими тегами (`latest`,
  `2022-latest`), і як тег складається з частин;
- по одному документу на лінію (версія документа — лінія, «2022»): плаваючі теги, таблиця
  кумулятивних оновлень (рядок на CU: варіанти GDR/OD і ОС, команда `docker pull` найновішого),
  передвипуски й RTM. Порядок — за номером, а не за абеткою: у реєстрі «CU10» стоїть перед «CU2».
"""

import json
import re

from engine.readers import Item, _markup, register

_PART = re.compile(r"^(?:CU(?P<cu>\d+)|(?P<pre>CTP\d+(?:\.\d+)?|RC\d+|RTM))"
                   r"(?:-(?P<fix>(?:GDR|OD)\d*))?(?:-(?P<os>.+))?$")


def _num(text: str) -> tuple:
    return tuple(int(x) for x in re.findall(r"\d+", text)) or (0,)


@register("registry-tags")
def registry_tags(source: dict, ctx) -> list[Item]:
    try:
        data = json.loads(ctx.text(source["url"]))
    except ValueError as exc:
        raise SystemExit(f"{source['url']}: відповідь не JSON ({exc}) — перелік тегів не складено.")
    tags = [t for t in data.get("tags") or [] if isinstance(t, str)]
    if not tags:
        raise SystemExit(f"{source['url']}: у відповіді немає тегів.")
    image = source.get("image") or data.get("name") or ""
    label = source.get("label") or image
    page = source.get("page") or source["url"]
    line_rx = re.compile(source.get("line") or r"^(?P<v>\d+)-")
    prefix = source.get("version_prefix", "")
    lines: dict = {}
    floating = []
    for tag in tags:
        m = line_rx.match(tag)
        if not m:
            floating.append(tag)
            continue
        lines.setdefault(m.group("v"), []).append(tag)
    order = sorted(lines, key=_num)

    def line_doc(v: str) -> str:
        own = lines[v]
        cus: dict = {}
        pre: dict = {}
        float_ = []
        other = []
        for tag in own:
            rest = tag[len(v) + 1:]
            m = _PART.match(rest)
            if not m:
                float_.append(tag) if "latest" in rest else other.append(tag)
                continue
            if m.group("cu"):
                cus.setdefault(int(m.group("cu")), []).append((m.group("fix") or "", m.group("os") or "", tag))
            else:
                pre.setdefault(m.group("pre"), []).append(tag)
        out = [f"Image `{image}`, SQL Server {v} line: {len(own)} tags in the registry.", ""]
        if float_:
            out += ["## Floating tags", "",
                    "These tags move to the newest build of the line:", ""]
            out += [f"- `{t}` — `docker pull {image}:{t}`" for t in sorted(float_)]
            out.append("")
        if cus:
            newest = max(cus)
            out += ["## Cumulative updates", "",
                    f"Cumulative updates CU{min(cus)}–CU{newest}; the newest is CU{newest}. GDR is a security "
                    f"fix on top of a CU, OD an on-demand build; the suffix names the base OS of the image.", "",
                    "| CU | Tags | Pull the newest |", "|---|---|---|"]
            for cu in sorted(cus):
                rows = sorted(cus[cu], key=lambda r: (_num(r[0]) if r[0] else (-1,), r[1]))
                names = ", ".join(f"`{t}`" for _, _, t in rows)
                last = rows[-1][2]
                out.append(f"| CU{cu} | {names} | `docker pull {image}:{last}` |")
            out.append("")
        if pre:
            out += ["## Previews and release to manufacturing", ""]
            for name in sorted(pre, key=lambda p: (p.startswith("RTM"), p[:2], _num(p))):
                out.append(f"- {name}: " + ", ".join(f"`{t}`" for t in sorted(pre[name])))
            out.append("")
        if other:
            out += ["## Other tags", "", *[f"- `{t}`" for t in sorted(other)], ""]
        return "\n".join(out)

    def overview() -> str:
        out = [f"Image `{image}` in the registry: {len(tags)} tags in {len(order)} lines.", "",
               "A tag is built as `<line>-<build>[-<fix>]-<os>`: the line is the SQL Server release year, "
               "the build is a cumulative update (`CU15`), a preview (`CTP2.0`, `RC1`) or `RTM`, the fix is "
               "a security update (`GDR1`) or an on-demand build (`OD1`), and the OS is the base image "
               "(`ubuntu-22.04`). `<line>-latest` follows the newest build of a line.", "",
               "| Line | Tags | Newest CU | Floating |", "|---|---|---|---|"]
        for v in order:
            cus = [int(m.group("cu")) for t in lines[v] if (m := _PART.match(t[len(v) + 1:])) and m.group("cu")]
            fl = [f"`{t}`" for t in lines[v] if t.endswith("latest")]
            out.append(f"| {v} | {len(lines[v])} | {('CU' + str(max(cus))) if cus else '—'} | "
                       f"{', '.join(fl) or '—'} |")
        if floating:
            out += ["", "## Tags without a line", "",
                    *[f"- `{t}` — `docker pull {image}:{t}`" for t in sorted(floating)]]
        return "\n".join(out)

    slug = _markup.slug(source.get("name_prefix") or label)
    items = []

    def add(name, title, version, build):
        def make():
            body = build()
            _markup.require(title, body, page, min_chars=1)
            return _markup.document(title, page, ctx.stamp, _markup.markdown_body(body), version)
        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))

    add(f"{slug}-tags", f"{label}: image tags", ", ".join(prefix + v for v in order), overview)
    for v in order:
        add(f"{slug}-{_markup.slug(v)}", f"{label} {v}: image tags", prefix + v, lambda v=v: line_doc(v))
    return items
