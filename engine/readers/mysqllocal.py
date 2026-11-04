"""Читачі посібників MySQL, які користувач завантажив сам: Info-архів і PDF на цій машині.

`mysql-info` — `file` — абсолютний шлях ZIP із файлом info; `url` — зміст посібника на dev.mysql.com,
               лише для адрес у шапках документів; `version` — лінія («8.4»).
`mysql-pdf`  — `file` — абсолютний шлях PDF; `url` — зміст посібника; необов'язкові `version` і
               `label` (рядок перед назвою сторінки, бо заголовки різних посібників збігаються).

Навіщо локальні файли. dev.mysql.com і downloads.mysql.com відповідають 403 на назву клієнта
завантажувача, а обходити цей фільтр підміною назви проєкт не буде. Умови Oracle дозволяють
особисте використання й перетворення формату без зміни змісту, але не поширення, тому корпус та
індекс цього примірника лишаються поза git. Читачі до мережі не звертаються: білий список тут —
сам шлях, оголошений у `sources.json`.

Вузол info має те саме ім'я, що й сторінка сайту (`select` → `select.html`), тож один вузол —
один документ зі справжньою адресою, а однакові імена дають спільний ключ для родини версій. У PDF
документ — пункт закладок: текст від його заголовка до заголовка наступного пункту.
"""

import re
import zipfile
from pathlib import Path

from engine.readers import Item, _markup, register
from engine.readers.gnuinfo import info_to_markdown

# Покажчики — лише посилання; у preface стоїть правова примітка, а не зміст посібника.
_SKIP = re.compile(r"^(top|preface|index|dynindex-.*|.*-index|ix\d+)$", re.I)
_HEAD = re.compile(r"^#+ (.+)$", re.M)
_NODE = re.compile(r"Node:\s*([^,\n]+)")
_MIN_CHARS = 40
# Меню вузла: у спільному info_to_markdown воно забирає й відступлений блок коду після себе, а в
# посібниках MySQL саме там стоїть синтаксис інструкції. Тому меню знімається тут, лише його рядки.
_MENU = re.compile(r"^\* Menu:\n\n?(?:\* .*\n(?: +\S.*\n)*)+", re.M)
# Посилання «*note 'SELECT': select.» читач бачить як SELECT; крапка тут — синтаксис info.
_XREF = re.compile(r"\*[Nn]ote\s+([^:]+?)(?:::|:\s*[\w.-]*\w\.?)", re.S)


def _xref(m: re.Match) -> str:
    return " ".join(m.group(1).split()).strip("'")


def _local(source: dict) -> Path:
    path = Path(source["file"]).expanduser()
    if not path.is_file():
        raise SystemExit(f"{source['id']}: немає файлу {path} — поверніть його з архіву примірника.")
    return path


def _titled(source: dict, title: str) -> str:
    return f"{source['label']}: {title}" if source.get("label") else title


@register("mysql-info")
def mysql_info(source: dict, ctx) -> list[Item]:
    with zipfile.ZipFile(_local(source)) as archive:
        member = next((n for n in archive.namelist() if n.endswith(".info")), None)
        if not member:
            raise SystemExit(f"{source['id']}: в архіві немає файлу .info.")
        text = archive.read(member).decode("utf-8", errors="replace")
    root = source["url"]
    items = []
    for node in text.split("\x1f"):
        node = node.lstrip("\n")
        name = _NODE.search(node[:200]) if node.startswith("File:") else None
        if not name or _SKIP.match(name.group(1).strip()):
            continue
        name = name.group(1).strip()
        body = info_to_markdown("\x1f" + _XREF.sub(_xref, _MENU.sub("", node)))
        head = _HEAD.search(body)
        if not head or len(body) - head.end() < _MIN_CHARS:
            continue    # Вузол лише з меню підрозділів: тексту в ньому немає.
        title, rest = head.group(1).strip(), body[head.end():].strip()
        slug = _markup.slug(name)

        def make(title=title, rest=rest, name=name):
            return _markup.document(_titled(source, title), f"{root}{name}.html", ctx.stamp, rest,
                                    source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{slug}", file=f"{source['id']}--{slug}.txt",
                          make=make))
    if not items:
        raise SystemExit(f"{source['id']}: у файлі info не знайдено вузлів — формат змінився.")
    return items


def _outline(reader, entries, out):
    for entry in entries:
        if isinstance(entry, list):
            _outline(reader, entry, out)
            continue
        page = reader.get_destination_page_number(entry)
        if page is not None:
            out.append((str(entry.title).strip(), page))
    return out


@register("mysql-pdf")
def mysql_pdf(source: dict, ctx) -> list[Item]:
    import pypdf
    reader = pypdf.PdfReader(str(_local(source)))
    marks = _outline(reader, reader.outline, [])
    if not marks:
        raise SystemExit(f"{source['id']}: у PDF немає закладок — документи не виділити.")
    pages: dict[int, list[str]] = {}

    def lines_of(number: int) -> list[str]:
        # Перший рядок сторінки — колонтитул із назвою посібника, останній — її номер.
        if number not in pages:
            lines = (reader.pages[number].extract_text() or "").splitlines()
            pages[number] = lines[1:-1] if len(lines) > 2 else lines
        return pages[number]

    def at(number: int, title: str) -> int:
        key = re.sub(r"\s+", "", title)
        for i, line in enumerate(lines_of(number)):
            if re.sub(r"\s+", "", line).startswith(key[:40]):
                return i
        return 0

    items, names = [], set()
    for k, (title, page) in enumerate(marks):
        if _SKIP.match(title) or re.match(r"^(Preface|Legal Notices|Index)\b", title):
            continue
        end = marks[k + 1][1] if k + 1 < len(marks) else len(reader.pages) - 1
        slug = _markup.slug(re.sub(r"^[\dA-Z]+(?:\.\d+)*\s+", "", title)) or f"section-{k}"
        if slug in names:
            slug = f"{slug}-{k}"
        names.add(slug)

        start = at(page, title) + 1
        if end == page:
            stop = at(end, marks[k + 1][0]) if k + 1 < len(marks) else None
            chunk = lines_of(page)[start:stop]
        else:
            chunk = list(lines_of(page)[start:])
            for n in range(page + 1, end):
                chunk += lines_of(n)
            if k + 1 < len(marks):
                chunk += lines_of(end)[:at(end, marks[k + 1][0])]
        text = "\n".join(chunk).strip()
        if len(text) < _MIN_CHARS:
            continue    # Пункт закладок лише з підрозділами: тексту в ньому немає.

        def make(title=title, text=text):
            return _markup.document(_titled(source, title), source["url"], ctx.stamp, text,
                                    source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{slug}", file=f"{source['id']}--{slug}.txt", make=make))
    return items
