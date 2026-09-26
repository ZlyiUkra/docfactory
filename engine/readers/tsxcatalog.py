"""Читач каталогу посилань, що лежить у коді сайту об'єктом даних.

`tsx-catalog` — `url` — сирий файл (TS/JS), чий `export default` — об'єкт груп:
                `{ article: [ {title, url, author, description, …}, … ], video: […] }`.
                `groups` — «ключ групи → [назва документа, адреса сторінки групи]»;
                одна група — один документ, і джерелом у шапці стоїть сторінка групи.

Навіщо. Розділ «Resources» сайту react-hook-form.com (статті, відео, розсилки, обгортки для
бібліотек компонентів) — не сторінки з текстом, а перелік чужих матеріалів з анотаціями.
Самих статей тут немає, лише те, що про них каже сайт: назва, автор, адреса, опис. Цього
досить, щоб на питання «де почитати про RHF з Zod» відповісти посиланням.

Розбір навмисно вузький: у кожному записі беруться лише поля-рядки в лапках. Запис, у
якому немає ні назви, ні адреси, пропускається, а не ламає документ.
"""

import re

from engine.readers import Item, _markup, register

_FIELD = re.compile(r"\b(\w+)\s*:\s*(?:\n\s*)?([\"'`])((?:\\.|(?!\2).)*)\2", re.S)


def _group(text: str, key: str) -> list[str]:
    """Тексти об'єктів `{…}` масиву під ключем key."""
    m = re.search(rf"^\s*{re.escape(key)}\s*:\s*\[", text, re.M)
    if not m:
        return []
    out, depth, start = [], 0, 0
    i = m.end()
    quote = ""
    while i < len(text):
        c = text[i]
        if quote:
            if c == "\\":
                i += 2
                continue
            if c == quote:
                quote = ""
        elif c in "\"'`":
            quote = c
        elif c == "{":
            if depth == 0:
                start = i
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                out.append(text[start:i + 1])
        elif c == "]" and depth == 0:
            break
        i += 1
    return out


@register("tsx-catalog")
def tsx_catalog(source: dict, ctx) -> list[Item]:
    groups = source.get("groups")
    if not isinstance(groups, dict) or not groups:
        raise SystemExit(f"{source['id']}: читач tsx-catalog потребує поля groups.")
    items = []
    for key, (title, cite) in groups.items():

        def make(key=key, title=title, cite=cite):
            text = ctx.text(source["url"]).replace("\r\n", "\n")
            entries = []
            for obj in _group(text, key):
                f = {k: " ".join(v.replace("\\'", "'").replace('\\"', '"').split())
                     for k, _q, v in _FIELD.findall(obj)}
                if not (f.get("title") or f.get("url")):
                    continue
                lines = [f"## {f.get('title') or f['url']}", ""]
                who = f.get("author", "")
                if who:
                    lines.append(f"Author: {who}" + (f" ({f['authorUrl']})"
                                                    if f.get("authorUrl") else ""))
                if f.get("url"):
                    lines.append(f"Link: {f['url']}")
                if f.get("version"):
                    lines.append(f"React Hook Form version: {f['version']}")
                if f.get("description"):
                    lines += ["", f["description"]]
                entries.append("\n".join(lines))
            if not entries:
                raise SystemExit(f"{source['url']}: у групі «{key}» жодного запису — "
                                 f"формат змінився, читача треба поправити.")
            body = f"{len(entries)} entries.\n\n" + "\n\n".join(entries)
            return _markup.document(title, cite, ctx.stamp, body)

        items.append(Item(id=f"{source['id']}/{key}",
                          file=f"{source['id']}--{key}.txt", make=make))
    return items
