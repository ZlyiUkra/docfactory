"""Читач журналу змін nginx (nginx.org/en/CHANGES): одна версія — один документ.

`nginx-changes` — `url` і `files` — адреси текстових журналів (`text/en/CHANGES`,
                  `text/en/CHANGES-1.30` …) у репозиторії nginx.org; документом стає
                  кожна версія («Changes with nginx 1.31.6   15 Sep 2026»), версією
                  документа — її номер. `site` — префікс адреси журналу на сайті:
                  до нього дописується ім'я файла (`https://nginx.org/en/` + `CHANGES-1.30`).

Навіщо. Документація nginx.org — одна, поточна: при директиві сказано, з якої версії вона
є, але не що змінилося в кожному випуску — виправлення, зміни поведінки, вразливості.
Це пише лише журнал. Він простим текстом, не markdown: заголовок версії — рядок «Changes
with nginx», записи — «*) Feature: …» з відступом, тож жоден наявний читач журналу його
не ділить.

Головний журнал (`CHANGES`) тримає всю історію основної гілки, а виправлення стабільних
гілок (1.30.1 … 1.30.5) є лише в журналі своєї гілки (`CHANGES-1.30`). Версія, що є в
кількох файлах, стає одним документом: береться з першого файла переліку, де вона є.
"""

import re

from engine.readers import Item, _markup, register

_HEAD = re.compile(r"^Changes with nginx (\d+\.\d+\.\d+)[ \t]+(\d{1,2} \w{3} \d{4})[ \t]*$", re.M)
_ITEM = re.compile(r"^[ \t]*\*\)[ \t]+")


def _body(chunk: str) -> str:
    """Записи «*) Feature: …» з переносами всередині → пункти списку одним рядком."""
    items: list[str] = []
    for line in chunk.split("\n"):
        if _ITEM.match(line):
            items.append(_ITEM.sub("", line).strip())
        elif line.strip() and items:
            items[-1] += " " + line.strip()
    return "\n".join(f"- {i}" for i in items)


@register("nginx-changes")
def nginx_changes(source: dict, ctx) -> list[Item]:
    files = [source["url"]] + [f for f in source.get("files") or () if f != source["url"]]
    site = source.get("site", "")
    seen: dict = {}
    for url in files:
        if not ctx.allowed(url):
            raise SystemExit(f"{source['id']}: адреса {url} поза білим списком — допишіть її в "
                             f"`within`.")
        text = ctx.text(url).replace("\r\n", "\n")
        heads = list(_HEAD.finditer(text))
        if not heads:
            raise SystemExit(f"{url}: жодного рядка «Changes with nginx X.Y.Z  дата» — формат "
                             f"змінився, читача треба поправити.")
        cite = f"{site}{url.rsplit('/', 1)[-1]}" if site else url
        for i, head in enumerate(heads):
            end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
            seen.setdefault(head.group(1), (head.group(2), _body(text[head.end():end]), cite))
    items = []
    for version, (day, body, cite) in seen.items():
        def make(version=version, day=day, body=body, cite=cite):
            return _markup.document(f"Changes with nginx {version}", cite, ctx.stamp,
                                    f"Released {day}.\n\n{body}", version)

        items.append(Item(id=f"{source['id']}/{version}",
                          file=f"{source['id']}--{version}.txt", make=make))
    return items
