"""Читач журналу змін будь-якого формату: заголовок запису задає вираз із джерела.

`changelog-regex` — `url`     — сирий файл журналу; `cite` — адреса для людей;
                    `heading` — вираз рядка, з якого починається запис (багаторядковий режим), з групою
                                `v` — номер версії, і необов'язковою `d` — датою;
                    `label`   — підпис у назві документа («poppler NEWS»).
                    Необов'язкові: `markdown: true` — запис уже markdown і розбирається як markdown, інакше
                    це простий текст (див. нижче); `skip` — вираз версій, що не беруться (передвипуски);
                    `name_prefix` — рядок перед номером в імені документа; `version_prefix` — рядок перед
                    номером у мітці версії («poppler-»), щоб версії кількох продуктів одного примірника не
                    збігалися.

Навіщо. У примірнику файлових інструментів десяток журналів, і кожен пише запис по-своєму: poppler —
«Release 26.10.0:» з відступами табуляцією, file — «* release 5.46» усередині датованих записів ChangeLog,
ExifTool — «Oct. 10, 2026 - Version 13.40», ImageMagick — «# 7.1.2-34 - 2026-…», qpdf — дата й автор над
записом. Окремий читач на кожен формат — десяток майже однакових модулів; тут формат — лише вираз у
`sources.json`, а поділ і запис документа — спільні.

Простий текст стає markdown так: спільний відступ знімається, пункти «*», «-», «+», «o» стають «- », рядок із
більшим відступом під пунктом — його продовженням, рядок «core:» над переліком — підписом. Без цього відступ
у вісім пробілів markdown прочитав би як блок коду, і весь запис став би одним кодом.
"""

import re
import textwrap

from engine.readers import Item, _markup, register

_BULLET = re.compile(r"^(?:[*+\-]|o)\s+")


def _plain(chunk: str) -> str:
    lines = textwrap.dedent(chunk.expandtabs(8).strip("\n")).split("\n")
    out: list[str] = []
    bullet_indent = -1
    for ln in lines:
        if not ln.strip():
            out.append("")
            bullet_indent = -1
            continue
        indent = len(ln) - len(ln.lstrip())
        text = ln.strip()
        if _BULLET.match(text):
            out.append("- " + _BULLET.sub("", text))
            bullet_indent = indent
        elif bullet_indent >= 0 and indent > bullet_indent and out and out[-1].startswith("- "):
            out[-1] += " " + text
        elif text.endswith(":") and len(text) < 60:
            out.append(f"**{text}**")
            bullet_indent = -1
        else:
            out.append(text)
            bullet_indent = -1
    body = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", body).strip()


@register("changelog-regex")
def changelog_regex(source: dict, ctx) -> list[Item]:
    if not source.get("heading"):
        raise SystemExit(f"{source['id']}: читач changelog-regex потребує поля heading.")
    head_rx = re.compile(source["heading"], re.M)
    skip = re.compile(source["skip"]) if source.get("skip") else None
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    _markup.refuse_html(text, source["url"])
    heads = list(head_rx.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка запису за виразом heading — "
                         f"формат змінився, вираз треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Changelog")
    lead = (re.sub(r"[^\w.-]+", "-", source["name_prefix"]).strip("-") + "-"
            if source.get("name_prefix") else "")
    vprefix = source.get("version_prefix", "")
    markdown = source.get("markdown") is True
    items, taken = [], set()
    for i, head in enumerate(heads):
        version = head.group("v").strip()
        if version in taken or (skip and skip.search(version)):
            continue
        taken.add(version)
        date = (head.groupdict().get("d") or "").strip()
        heading = f"{version} ({date})" if date else version
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        name = lead + re.sub(r"[^\w.-]+", "-", version)

        # Рядок заголовка без підкреслення reStructuredText («Version 2.63.3» над «=====»).
        def make(chunk=chunk, heading=heading, version=version,
                 line=head.group(0).strip().split("\n")[0].strip()):
            body = _markup.markdown_body(chunk) if markdown else _plain(chunk)
            body = f"{line}\n\n{body}" if not markdown else body
            _markup.require(heading, body, f"{source['url']} {heading}", min_chars=1)
            return _markup.document(f"{label}: {heading}", cite, ctx.stamp, body,
                                    f"{vprefix}{version}")

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
