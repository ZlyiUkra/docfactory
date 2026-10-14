"""Читач CHANGES і NEWS OpenSSL: «Changes between 3.5.3 and 3.5.4 [30 Sep 2025]» і текст до наступного заголовка.

`changelog-openssl` — один документ на запис. `url` — файл (`CHANGES.md` чи `NEWS.md` з одного тега: файл містить
                     усю історію від 0.9.0), `cite` — адреса для людей, `label` — підпис у назві («Changes»,
                     «Major changes»), `name_prefix` — рядок перед версією в імені документа. Заголовок — «Changes
                     between A and B [дата]» чи «Major changes between OpenSSL A and OpenSSL B [дата]»; у старих
                     випусках без «#» і з відступом. Запис гілки без дати («[xx XXX xxxx]» — шаблон наступного
                     випуску, що так і не вийшов) пропускається.

Навіщо. Сторінки man кажуть, що є в версії, але не що змінилося між випусками: які CVE закрито, що з'явилося й що
зникло. Це й дають CHANGES (усе) і NEWS (головне). Спільні читачі журналів чекають номер у заголовку без слів
«between … and», тож тут свій розбір.
"""

import re

from engine.readers import Item, _markup, register

_HEAD = re.compile(r"^[ \t]*#{0,4}[ \t]*(?:Major )?[Cc]hanges between (?:OpenSSL )?(?P<a>\S+) and "
                   r"(?:OpenSSL )?(?P<b>\S+?)[ \t]*\[(?P<date>[^\]\n]*)\][ \t]*$", re.M)


@register("changelog-openssl")
def changelog_openssl(source: dict, ctx) -> list[Item]:
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    heads = list(_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка «Changes between A and B» — "
                         f"формат змінився, читача треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Changes")
    prefix = source.get("name_prefix", "changes")
    items, seen = [], {}
    for i, head in enumerate(heads):
        date = head.group("date").strip()
        if "xx" in date.lower():
            continue
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        chunk = text[head.end():end].strip("\n")
        if not chunk.strip():
            continue
        a, b = head.group("a"), head.group("b")
        n = seen.get(b, 0) + 1
        seen[b] = n
        name = f"{prefix}-{b}" + (f"-{n}" if n > 1 else "")
        title = f"OpenSSL {label}: {a} to {b} — {date}"

        # Версія з літерою («1.1.1w») у фільтрі пишеться з крапкою («1.1.1.w»), як у тегів сторінок man.
        label_v = re.sub(r"^(\d+\.\d+(?:\.\d+)?)([a-z]+)$", r"\1.\2", b)

        def make(chunk=chunk, title=title, b=b, cite=cite, label_v=label_v):
            body = _markup.markdown_body(chunk)
            _markup.require(title, body, f"{cite}#{b}", min_chars=1)
            return _markup.document(title, f"{cite}#{b}", ctx.stamp, body, label_v)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    return items
