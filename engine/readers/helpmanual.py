"""Читач книжки PDF, зібраної програмою Help+Manual: тема закладок — документ.

`helpmanual-pdf` — `file` — абсолютний шлях PDF на цій машині; `url` — сторінка книжки на сайті видавця,
                   стоїть у шапці кожного документа й сама не читається. Необов'язкові: `name_prefix` —
                   початок імені кожного документа (кілька книжок в одному примірнику); `version` —
                   мітка версії; `code_lang` — мова блоків коду (типово `mql5`); `subheads` — назви
                   підзаголовків теми (типово «Parameters», «Return Value», «Note», «Example» та інші
                   з `_SUBHEADS`); `skip` — вираз назв тем, що не беруться; `min_chars` — найкоротше
                   тіло; `title_size` — найменший кегль назви теми (типово 18: у довіднику 21, у
                   книжках 16); `furniture_after` — скільки рядків колонтитула стоїть після номера
                   сторінки (у довіднику 0, у книжках 1 — назва розділу).

Навіщо. Довідник MQL5 і обидві книжки MetaQuotes («MQL5 Programming for Traders», «Neural Networks for
Algorithmic Trading with MQL5») видавець дає PDF-файлами, а умови mql5.com забороняють збирати сайт
програмами й копіювати його вміст. Тому файли завантажує людина браузером, а читач до мережі не
звертається: білий список тут — сам шлях, оголошений у `sources.json`.

Що робить. Help+Manual починає кожну тему з нової сторінки й ставить її назву кеглем 21, а вгорі кожної
сторінки — три рядки колонтитула: назву розділу, «© 2000-2026, MetaQuotes Ltd.» і номер сторінки. Пункт
закладок будь-якої глибини — документ: текст від назви теми до назви наступної. Простий витяг тексту
губить, де код: шрифт кожного символу береться з `visitor_text` pypdf, чий потік збігається з
`extract_text` до символу. Рядок, увесь набраний Courier New дрібного кегля, — рядок коду з відступами
як є; одне слово тим самим шрифтом більшого кегля — назва параметра. Підзаголовки теми набрано тим
самим шрифтом, що й текст, тож вони впізнаються за назвою. Посилання в тексті pypdf виносить на новий
рядок, що починається пробілом чи розділовим знаком («The NULL» + « value means»): такий рядок
приклеюється до попереднього.
"""

import collections
import re

from engine.readers import Item, _markup, register

_MONO = re.compile(r"Courier|Code|Mono", re.I)
_TITLE_SIZE = 18.0
_CODE_MAX = 12.5
_SUBHEADS = ("Parameters", "Return Value", "Returned value", "Return value", "Note", "Notes", "Example",
             "Examples", "Example:", "See also", "See Also", "Description", "Remark", "Remarks")
_BULLET = re.compile(r"^[·•]\s*")
# Назва — це слова: значки «+», «-», «●» у таблицях книжок набрано тим самим великим кеглем.
_WORDY = re.compile(r"[A-Za-z]{2}")
_PAGE_NO = re.compile(r"^\d[\d ]*$")


def _page_lines(page, title_size: float = _TITLE_SIZE, after: int = 0) -> list[tuple[str, str]]:
    """(текст рядка, вид) сторінки без колонтитула. Вид: title, code, param, text."""
    parts = []

    def visit(text, cm, tm, font, size):
        name = (font or {}).get("/BaseFont", "") if hasattr(font, "get") else ""
        parts.append((text, str(name), (size or 0) * (tm[0] or 1)))

    page.extract_text(visitor_text=visit)
    lines, cur, kinds = [], [], collections.Counter()
    for text, font, size in parts:
        for n, piece in enumerate(text.split("\n")):
            if n:
                lines.append(("".join(cur), kinds))
                cur, kinds = [], collections.Counter()
            cur.append(piece)
            if piece.strip():
                kinds[_kind(font, size, title_size)] += len(piece.strip())
    lines.append(("".join(cur), kinds))
    return _classify(lines, after)


def _kind(font: str, size: float, title_size: float) -> str:
    mono = bool(_MONO.search(font))
    return ("title" if size >= title_size and not mono else
            "code" if mono and size <= _CODE_MAX else
            "param" if mono else "text")


def _pdfium_lines(document, n: int, title_size: float, after: int) -> list[tuple[str, str]]:
    """Те саме, що _page_lines, але через PDFium (pypdfium2) — для сторінки, на якій pypdf падає.

    pypdf не розкодовує шрифт із кодуванням KSCms-UHC-H (сторінка 427 книжки MQL5 Programming for
    Traders: журнал скрипту з текстом у різних кодуваннях), а PDFium читає її повністю, зі шрифтом і
    кеглем кожного символу. Відступи рядків коду PDFium стискає до одного пробілу, тож відступ
    відновлюється з координати першого знака: відстань від лівого краю коду сторінки в ширинах знака
    моноширинного шрифту (0,6 кегля)."""
    import ctypes
    import pypdfium2.raw as raw

    page = document[n]
    text_page = page.get_textpage()
    handle = text_page.raw
    buf = ctypes.create_string_buffer(128)
    flags = ctypes.c_int()
    left, right, bottom, top = (ctypes.c_double() for _ in range(4))
    rows = []    # [текст, види, x першого знака, кегль першого знака]
    row = ["", collections.Counter(), None, 0.0]
    for i in range(raw.FPDFText_CountChars(handle)):
        char = chr(raw.FPDFText_GetUnicode(handle, i))
        if char == "\r":
            continue
        if char == "\n":
            rows.append(row)
            row = ["", collections.Counter(), None, 0.0]
            continue
        row[0] += char
        if char.strip():
            raw.FPDFText_GetFontInfo(handle, i, buf, len(buf), ctypes.byref(flags))
            size = raw.FPDFText_GetFontSize(handle, i)
            row[1][_kind(buf.value.decode("latin-1"), size, title_size)] += 1
            if row[2] is None:
                raw.FPDFText_GetCharBox(handle, i, ctypes.byref(left), ctypes.byref(right),
                                        ctypes.byref(bottom), ctypes.byref(top))
                row[2], row[3] = left.value, size
    rows.append(row)
    text_page.close()
    page.close()
    code_x = [r[2] for r in rows if r[2] is not None and r[1] and r[1].most_common(1)[0][0] == "code"]
    edge = min(code_x) if code_x else 0.0
    lines = []
    for text, kinds, x, size in rows:
        if kinds and kinds.most_common(1)[0][0] == "code" and x is not None and size:
            text = " " * max(0, round((x - edge) / (0.6 * size))) + text.strip()
        lines.append((text, kinds))
    return _classify(lines, after)


def _classify(lines: list, after: int) -> list[tuple[str, str]]:
    # Колонтитул — у перших чотирьох рядках, до номера сторінки включно, і ще `after` рядків після
    # нього: у довіднику це назва розділу, «© …» і номер, у книжках — назва частини, номер (pypdf
    # подекуди розриває його: «1 01») і назва розділу.
    for i, (text, _) in enumerate(lines[:4]):
        if _PAGE_NO.match(text.strip()):
            lines = lines[i + 1 + after:]
            break
    out = []
    for text, kinds in lines:
        if not text.strip():
            continue
        kind = kinds.most_common(1)[0][0] if kinds else "text"
        # Рядок коду — лише коли код майже весь: моноширинне слово серед тексту — назва, а не код.
        # Майже, бо в книжках окремі знаки коду («<», «,») набрано звичайним шрифтом.
        if kind == "code" and kinds["code"] < 0.8 * sum(kinds.values()):
            kind = "text"
        if kind == "title" and not _WORDY.search(text):
            kind = "text"
        out.append((text.replace("\xa0", " ").rstrip(), kind))
    return out


def _markdown(lines: list[tuple[str, str]], subheads: set, lang: str) -> str:
    blocks: list[str] = []
    para: list[str] = []
    code: list[str] = []

    def flush_para():
        if para:
            blocks.append(" ".join(para))
            para.clear()

    def flush_code():
        if code:
            blocks.append(f"```{lang}\n" + "\n".join(code) + "\n```")
            code.clear()

    for text, kind in lines:
        if kind == "code":
            flush_para()
            code.append(text)
            continue
        flush_code()
        stripped = text.strip()
        if kind == "title":
            flush_para()
            blocks.append(f"## {stripped}")
        elif stripped.rstrip(":") in subheads or stripped in subheads:
            flush_para()
            blocks.append(f"## {stripped.rstrip(':')}")
        elif kind == "param":
            flush_para()
            blocks.append(f"`{stripped}`")
        elif _BULLET.match(stripped):
            flush_para()
            para.append("- " + _BULLET.sub("", stripped))
        elif para and (text[:1] == " " or stripped[:1] in ",.;:)]"):
            # Посилання pypdf виносить на окремий рядок: «The NULL» + « value means».
            para[-1] += text
        else:
            para.append(stripped)
    flush_para()
    flush_code()
    return "\n\n".join(blocks)


def _outline(reader, entries, out, depth=0):
    for entry in entries:
        if isinstance(entry, list):
            _outline(reader, entry, out, depth + 1)
            continue
        page = reader.get_destination_page_number(entry)
        if page is not None:
            out.append((" ".join(str(entry.title).split()), page, depth))
    return out


@register("helpmanual-pdf")
def helpmanual_pdf(source: dict, ctx) -> list[Item]:
    import pypdf

    path = source.get("file")
    if not path or not source.get("url"):
        raise SystemExit(f"{source['id']}: читач helpmanual-pdf потребує полів file і url.")
    try:
        reader = pypdf.PdfReader(path)
    except OSError as exc:
        raise SystemExit(f"{source['id']}: не відкрив {path}: {exc}")
    marks = _outline(reader, reader.outline, [])
    if not marks:
        raise SystemExit(f"{source['id']}: у {path} немає закладок — теми не виділити.")
    # Порожній перелік вимикає підзаголовки за назвою: у книжках їх набрано кеглем назви, а слово
    # «Description» там — шапка таблиці.
    subheads = set(source.get("subheads", _SUBHEADS))
    lang = source.get("code_lang", "mql5")
    skip = re.compile(source["skip"]) if source.get("skip") else None
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""
    min_chars = int(source.get("min_chars", 40))
    title_size = float(source.get("title_size", _TITLE_SIZE))
    after = int(source.get("furniture_after", 0))

    cache: dict[int, list] = {}
    fallback: dict = {}

    def lines_of(n: int) -> list:
        if n not in cache:
            if len(cache) > 64:
                cache.clear()
            try:
                cache[n] = _page_lines(reader.pages[n], title_size, after)
            except (UnicodeDecodeError, ValueError, KeyError) as exc:
                # pypdf не декодує подекуди шрифт з кодуванням KSCms-UHC-H (книжка MQL5 Programming
                # for Traders), і таку сторінку читає PDFium.
                import pypdfium2
                if "pdfium" not in fallback:
                    fallback["pdfium"] = pypdfium2.PdfDocument(path)
                cache[n] = _pdfium_lines(fallback["pdfium"], n, title_size, after)
                print(f"  {path}: сторінку {n + 1} pypdf не прочитав ({type(exc).__name__}), "
                      f"прочитано через PDFium: рядків {len(cache[n])}", flush=True)
        return cache[n]

    def key(text: str) -> str:
        return re.sub(r"\s+", "", text)[:30]

    items, names = [], collections.Counter()
    # Шлях закладок: назва теми «Parameters» трапляється в багатьох розділах, а з батьківськими
    # назвами ім'я документа неповторне й каже, де тема стоїть.
    trail: list[str] = []
    for k, (title, page, depth) in enumerate(marks):
        trail[depth:] = [title]
        end = marks[k + 1][1] if k + 1 < len(marks) else len(reader.pages)
        if skip and skip.search(title):
            continue
        lines = []
        for n in range(page, max(end, page + 1)):
            lines += lines_of(n)
        # Назва теми — рядок кеглем назви з її текстом; усе до нього — хвіст попередньої теми, що
        # закінчилася на тій самій сторінці. Довга назва переноситься на другий рядок того ж кегля.
        titles = [i for i, (t, kind) in enumerate(lines) if kind == "title"]
        start = next((i for i in titles if key(lines[i][0]) == key(title)[:len(key(lines[i][0]))]),
                     titles[0] if titles else -1)
        while start + 1 < len(lines) and lines[start + 1][1] == "title":
            start += 1
        body_lines = lines[start + 1:]
        # Якщо наступна тема почалася на тій самій сторінці, текст закінчується на її назві.
        if k + 1 < len(marks) and marks[k + 1][1] == page:
            stop = next((i for i, (t, kind) in enumerate(body_lines) if kind == "title"), None)
            body_lines = body_lines[:stop]
        body = _markdown(body_lines, subheads, lang)
        if len(body) < min_chars:
            continue    # Тема лише з переліком підтем: тексту в ній немає.
        slug = lead + _markup.slug(" ".join(trail[-2:]) if depth > 1 else title)
        names[slug] += 1
        if names[slug] > 1:
            slug = f"{slug}-{names[slug]}"
        # Назва документа — сама тема («iMA»): так її ставить першою title_match. Де тема стоїть у
        # книжці, каже перший рядок тексту.
        where = " › ".join(trail[1:-1])
        if where:
            body = f"Section: {where}\n\n{body}"

        def make(title=title, body=body):
            _markup.require(title, body, source["url"], min_chars)
            return _markup.document(title, source["url"], ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{slug}", file=f"{source['id']}--{slug}.txt", make=make))
        if k % 500 == 0:
            print(f"  {path}: тем {k} із {len(marks)}", flush=True)
    if not items:
        raise SystemExit(f"{source['id']}: у {path} не знайдено жодної теми з текстом.")
    return items
