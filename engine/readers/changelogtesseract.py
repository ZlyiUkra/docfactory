"""Читач журналу ChangeLog Tesseract, де заголовок версії — «2024-11-10 - V5.5.0» (дата, тире, «V» і номер).

`changelog-tesseract` — те саме, що `changelog`: файл, поділений на версії, одна версія — один документ, версією
                        документа стає номер із заголовка. Поле `skip` — вираз для версій, яких не брати
                        (передрелізи: «5.4.0-rc2», «3.03(rc1)»).

Навіщо. Tesseract пише журнал із 2006 року одним текстовим файлом: «2024-11-10 - V5.5.0», далі пункти «*». Старі
записи несуть хвости: «V2.02 (again)» (повторний випуск), «V1.01.», «V1.0 of open source Tesseract checked-in.».
Жоден спільний читач такого заголовка не впізнає. З 5.5.1 у теці лишилася заглушка з посиланням на останній
коміт повного журналу, тож джерело бере файл із того коміту.

Чому окремий модуль: спільні читачі вже звірено в готових примірниках, правка виразу в них — ризик зсуву; новий
домен додає свого читача.
"""

import re

from engine.readers import Item, _markup, register

_VERSION_HEAD = re.compile(r"^(\d{4}-\d{2}-\d{2})[ \t]+-[ \t]+V(\d+(?:\.\d+)*)([^\n]*)$", re.M)


@register("changelog-tesseract")
def changelog_tesseract(source: dict, ctx) -> list[Item]:
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    heads = list(_VERSION_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка версії «дата - VX.Y» — "
                         f"формат змінився, читача треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "ChangeLog")
    skip = re.compile(source["skip"]) if source.get("skip") else None
    # Повторний випуск під тим самим номером («V2.02 (again)») зливається з першим записом: окремими
    # документами з одним ім'ям файла другий затер би перший.
    entries: dict = {}
    for i, head in enumerate(heads):
        version, tail = head.group(2), head.group(3).strip()
        if skip and skip.search(version + tail):
            continue
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        note = tail.rstrip(".").strip()
        entries.setdefault(version, []).append((head.group(1), note, chunk))
    items = []
    for version, parts in entries.items():
        name = re.sub(r"[^\w.-]+", "-", version)

        def make(parts=parts, version=version):
            bodies = []
            for day, note, chunk in parts:
                lead = f"Released {day}" + (f" ({note})" if note else "") + "."
                bodies.append(f"{lead}\n\n{_markup.markdown_body(chunk)}")
            return _markup.document(f"{label}: {version}", cite, ctx.stamp, "\n\n".join(bodies), version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    return items
