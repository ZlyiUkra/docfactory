"""Читач книжки, розпізнаної зі скану заздалегідь: одна сторінка — один файл JSON з рамками рядків.

`ocr-pages` — `folder` — абсолютний шлях до теки зі сторінками `0001.json`, `0002.json`… (кожен файл:
              `{"page": N, "items": [[рамка, текст, впевненість], …]}`, як їх пише rapidocr); `title` —
              назва книжки, вона стоїть перед назвою кожного документа; `url` — людська адреса книжки
              для шапки. `page_titles` — об'єкт «номер сторінки скану → назва розділу»: кожна названа
              сторінка починає документ, що триває до наступної названої; сторінки перед першою
              назвою не беруться. Необов'язкові: `page_offset` — на скільки номер сторінки скану
              більший за номер у книжці (для рядка «сторінки книжки N–M»); `skip_lines` — вирази
              рядків, що випадають (колонтитули); `min_score` — найнижча впевненість розпізнавання
              (типово 0.5); `name_prefix` — початок імені кожного документа (типово id джерела);
              `version` — мітка версії.

Навіщо. Деякі книжки існують лише сканом без текстового шару, як-от DjVu «Beyond Cracking the Coding
Interview». Розпізнавання 646 сторінок займає годину процесора, тож воно робиться один раз окремо,
а читач лише складає рядки з готових рамок. Правка поділу на розділи чи колонтитулів тоді коштує
секунди, а не нове розпізнавання.

Рядок складається з рамок, чиї середини по вертикалі ближчі за половину звичайної висоти рамки;
усередині рядка рамки йдуть зліва направо. Дві колонки коду поруч (книжка порівнює два розв'язки)
так зливаються в спільні рядки: читач цього не лагодить, бо не може надійно вгадати межу колонок.
Рядок лише з великих літер стає підзаголовком `## …`. Документ починається позначкою, що текст
розпізнано і що цитату треба звіряти зі сторінкою скану.
"""

import json
import os
import re
import statistics

from engine.readers import Item, _markup, register
from engine.readers.cncfcurriculum import OCR_NOTE
from engine.readers.pdfoutline import _paragraphs

_NUMBER = re.compile(r"^\s*[\divxlcIVXLC]+\s*$")
_CAPS = re.compile(r"^[^a-z]*[A-Z]{3}[^a-z]*$")


def _rows(items: list, min_score: float) -> list[str]:
    boxes = [(box, text) for box, text, score in items if float(score) >= min_score and text.strip()]
    if not boxes:
        return []
    height = statistics.median(b[2][1] - b[0][1] for b, _ in boxes) or 1
    rows: list[list] = []
    for box, text in sorted(boxes, key=lambda b: (b[0][0][1] + b[0][2][1]) / 2):
        y = (box[0][1] + box[2][1]) / 2
        if rows and abs(rows[-1][0] - y) < height / 2:
            rows[-1][1].append((box[0][0], text))
        else:
            rows.append([y, [(box[0][0], text)]])
    return [" ".join(" ".join(t for _x, t in sorted(row[1])).split()) for row in rows]


def _body(lines: list[str]) -> str:
    blocks, run = [], []
    for line in lines:
        if _CAPS.match(line) and len(line) <= 90:
            if run:
                blocks.append(_paragraphs(run))
                run = []
            blocks.append(f"## {line}")
        else:
            run.append(line)
    if run:
        blocks.append(_paragraphs(run))
    return "\n\n".join(b for b in blocks if b.strip())


@register("ocr-pages")
def ocr_pages(source: dict, ctx) -> list[Item]:
    folder = source["folder"]
    try:
        files = sorted(f for f in os.listdir(folder) if re.fullmatch(r"\d{4}\.json", f))
    except OSError as exc:
        raise SystemExit(f"{source['id']}: не відкрив {folder}: {exc}")
    total = len(files)
    titles = {int(k): v for k, v in (source.get("page_titles") or {}).items()}
    if not titles:
        raise SystemExit(f"{source['id']}: читач ocr-pages потребує поля page_titles.")
    label = source.get("title") or source["id"]
    url = source.get("url") or ""
    offset = int(source.get("page_offset", 0))
    min_score = float(source.get("min_score", 0.5))
    skip = [re.compile(r) for r in source.get("skip_lines") or ()]
    lead = f"{_markup.slug(source.get('name_prefix') or source['id'])}-"
    starts = sorted(titles)

    def page_lines(n: int) -> list[str]:
        with open(os.path.join(folder, f"{n:04d}.json"), encoding="utf-8") as fh:
            rows = _rows(json.load(fh)["items"], min_score)
        return [r for r in rows if not _NUMBER.match(r) and not any(s.search(r) for s in skip)]

    items, names = [], set()
    for i, first in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else total + 1
        lines = []
        for n in range(first, end):
            lines += page_lines(n) + [""]
        title = titles[first]
        where = f"сторінки книжки {first - offset}–{end - 1 - offset}, сторінки скану {first}–{end - 1}"
        body = f"{OCR_NOTE} Цитату звіряти зі сканом: {where}.\n\n{_body(lines)}"
        full = f"{label}: {title}"
        slug = lead + _markup.slug(title)
        if slug in names:
            raise SystemExit(f"{source['id']}: дві назви дають одне ім'я {slug}.")
        names.add(slug)

        def make(full=full, body=body):
            _markup.require(full, body, url)
            return _markup.document(full, url, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{slug}", file=f"{source['id']}--{slug}.txt", make=make))
    print(f"  {label}: сторінок {total}, документів {len(items)}", flush=True)
    return items
