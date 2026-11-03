"""Читачі права про захист даних: акти ЄС, закони Португалії, рішення CNPD і PDF-настанови.

`eu-act`        — `url` — XHTML акта у сховищі Бюро публікацій ЄС (publications.europa.eu/resource/
                  cellar/…/DOC_n: за цією адресою текст однієї мови); `title` — назва документа;
                  `part` — `articles` (типово) чи `recitals`; `recital` — слово заголовка вступного
                  пункту («Considerando»); `page` — людська адреса для шапки, змовчання — `url`.
                  Один документ: кожна стаття чи вступний пункт — розділ `## …`.
`pgdl-law`      — `url` — lei_mostra_articulado.php сайту pgdlisboa.pt (чинна редакція закону);
                  `title` — назва. Один документ: кожна стаття — розділ `## Artigo … — Назва`.
                  Позначки змін під статтею лишаються: з них видно, котрий закон вніс редакцію.
`cnpd-decisions` — `url` — сторінка «Histórico de decisões» cnpd.pt; `types` — об'єкт «номер типу →
                  слово в імені файла» (`{"5": "diretriz"}`); `since` — перший рік. Кожна картка
                  (номер, адресат, предмет) стає документом з PDF-а, на який вона веде.
`pdf-list`      — `pdfs` — перелік `{url, title, name}` (`name` необов'язкове); `index` — сторінки,
                  де посилання на PDF збігаються з виразом `match`: назвою стає текст посилання.
                  `url` — адреса першої сторінки чи першого PDF, для перевірки оголошення.

Спільні поля PDF: `skip_lines` — вирази рядків, що випадають (колонтитули); `headings` — вирази
рядка-заголовка розділу.

Навіщо окремий модуль. EUR-Lex не віддає текст автоматичним запитам, а той самий текст лежить у
сховищі Бюро публікацій, але без спільного читача: розмітка своя в акта ОВ («oj-ti-art») і у
зведеної редакції («title-article-norm»). Зведена редакція містить виправлення, але без вступних
пунктів, тому RGPD береться двома джерелами. pgdlisboa.pt — єдине з посилань CNPD на чинну
редакцію законів, що віддає текст простим запитом (сайт Diário da República малює його скриптом),
і кодує сторінку в ISO-8859-1.

Рішення CNPD до 2020 року — переважно скани без текстового шару. Такий PDF розпізнається тим самим
рушієм, що й у cncf-curriculum, а той не знає португальських наголосів: «comunicações» виходить як
«comunicacoes». Тому примірник вмикає `fold_accents` (common/lexical.py), а документ зі сканів
позначено: цитувати його можна лише звіривши з PDF.
"""

import hashlib
import html
import io
import json
import os
import pathlib
import re
from urllib.parse import urljoin, urlsplit

from engine.readers import Item, _markup, register
from engine.readers.cncfcurriculum import _OCR_DPI, OCR_NOTE, _ocr_engine

# ── спільне ─────────────────

_BLOCK_END = re.compile(r"</(?:p|div|tr|li|h[1-6])>|<br\s*/?>|<hr[^>]*>", re.I)
_TAG = re.compile(r"<[^>]+>")
# Позначка пункту, що в розмітці стоїть окремо від тексту: «1.», «a)», «(a)».
_MARK = re.compile(r"^(?:\d+\.|\(?[a-z0-9]{1,4}\))$")
# Менше символів на сторінку, ніж у самому колонтитулі: текстового шару немає.
_SCAN_CHARS = 100
# Два фрагменти одного рядка скану: центри по висоті ближче, ніж півтора кегля цього розміру.
_OCR_ROW = 14


def _flat(fragment: str) -> str:
    """Текст фрагмента HTML: блоки — рядками, позначка пункту — на одному рядку з текстом."""
    text = html.unescape(_TAG.sub("", _BLOCK_END.sub("\n", fragment)))
    lines = [" ".join(line.split()) for line in text.splitlines()]
    out: list[str] = []
    for line in filter(None, lines):
        if out and _MARK.match(out[-1]):
            out[-1] += " " + line
        else:
            out.append(line)
    return "\n\n".join(out)


def _ordinal(fragment: str) -> str:
    """Надрядкове «o» актів ЄС стає «º»: «artigo 6.º», як пишуть закони й запити."""
    return re.sub(r'<span class="(?:oj-)?super(?:script)?">\s*(o|a)\s*</span>',
                  lambda m: "º" if m.group(1) == "o" else "ª", fragment)


# ── eu-act ─────────────────

_EU_PIECE = re.compile(r'<div class="eli-subdivision" id="(art_\d+|rct_\d+)"')
# Старіші зведені редакції не ділять статті на блоки: межа статті там лише її заголовок.
_EU_PLAIN = re.compile(r'<p[^>]*class="title-article-norm"')
_EU_CUT = re.compile(r'id="cpt_|class="(?:oj-)?(?:final|footnote|signatory)"|<hr class="(?:oj-)?(?:note|separator-short)"')
_EU_NOTE = re.compile(r'<a href="#[^"]*"[^>]*>.*?</a>', re.S)
_EU_MODREF = re.compile(r'<p class="modref">.*?</p>', re.S)
_EU_ARTICLE = re.compile(r'<p[^>]*class="(?:oj-ti-art|title-article-norm)"[^>]*>(.*?)</p>', re.S)
_EU_TITLE = re.compile(r'<p[^>]*class="(?:oj-sti-art|stitle-article-norm)"[^>]*>(.*?)</p>', re.S)


def _eu_body(page: str, part: str, recital: str) -> str:
    page = _ordinal(_EU_MODREF.sub("", page))
    prefix = "rct" if part == "recitals" else "art"
    marks = [m for m in _EU_PIECE.finditer(page) if m.group(1).startswith(prefix)]
    if not marks and part != "recitals":
        marks = list(_EU_PLAIN.finditer(page))
    sections = []
    for i, mark in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(page)
        block = page[mark.start():end]
        cut = _EU_CUT.search(block)
        block = _EU_NOTE.sub("", block[:cut.start()] if cut else block)
        if part == "recitals":
            number = mark.group(1).split("_")[1]
            text = _flat(block)
            text = re.sub(rf"^\({number}\)\s*", "", text)
            sections.append(f"## {recital} ({number})\n\n{text}")
            continue
        article, title = _EU_ARTICLE.search(block), _EU_TITLE.search(block)
        if not article:
            raise SystemExit(f"Стаття {mark.group(0)} без заголовка: розмітка акта змінилась.")
        head = _flat(article.group(1))
        if title:
            head += " — " + _flat(title.group(1))
            block = block[:title.start()] + block[title.end():]
        block = block[:article.start()] + block[article.end():]
        sections.append(f"## {head}\n\n{_flat(block)}")
    return "\n\n".join(sections)


@register("eu-act")
def eu_act(source: dict, ctx) -> list[Item]:
    part = source.get("part", "articles")

    def make():
        body = _eu_body(ctx.bytes(source["url"]).decode("utf-8"), part, source.get("recital", "Recital"))
        _markup.require(source["title"], body, source["url"])
        return _markup.document(source["title"], source.get("page", source["url"]), ctx.stamp, body,
                                source.get("version", ""))

    return [Item(id=source["id"], file=f"{source['id']}.txt", make=make)]


# ── pgdl-law ─────────────────

_PGDL_OPTION = re.compile(r'<option value="\d+A[^"]+">')
_PGDL_HEAD = re.compile(r"color:#d74600[^>]*>(.*?)</td>", re.S)
_PGDL_TEXT = re.compile(r'colspan=4 class=txt_base_n_l>(.*?)<!-- IN[IÍ]CIO DAS ANOTA', re.S)
_PGDL_NOTE = re.compile(r"-->(.*?)<DIV id=\"div_cria_anotacao", re.S)
_PGDL_INTRO = re.compile(r"<td class=txt_base_n_l colspan=3>(.*?)</td>", re.S)


def _pgdl_body(page: str, url: str) -> str:
    heads = list(_PGDL_HEAD.finditer(page))
    # Додаток має заголовок, але не має рядка у змісті статей: Lei 58/2019 несе ANEXO.
    articles = [h for h in heads if "Artigo" in h.group(1)]
    if len(articles) != len(_PGDL_OPTION.findall(page)):
        raise SystemExit(f"{url}: у змісті {len(_PGDL_OPTION.findall(page))} статей, а на сторінці "
                         f"{len(articles)} — закон показано не цілком, документ не записую.")
    intro = _PGDL_INTRO.search(page)
    sections = [_flat(intro.group(1))] if intro else []
    for i, head in enumerate(heads):
        block = page[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(page)]
        text = _PGDL_TEXT.search(block)
        if not text:
            raise SystemExit(f"{url}: стаття без тексту — розмітка сторінки змінилась.")
        name = [" ".join(p.split()) for p in re.split(r"<br\s*/?>", head.group(1), flags=re.I)]
        name = [html.unescape(_TAG.sub("", p)).strip() for p in name]
        note = _PGDL_NOTE.search(block, text.end() - 8)
        extra = _flat(note.group(1)) if note else ""
        title = " — ".join(p for p in name if p)
        sections.append(f"## {title}\n\n{_flat(text.group(1))}" + (f"\n\n{extra}" if extra else ""))
    return "\n\n".join(sections)


@register("pgdl-law")
def pgdl_law(source: dict, ctx) -> list[Item]:
    def make():
        page = ctx.bytes(source["url"]).decode("cp1252", "replace")
        # Сайт зберігає знак відсотка службовим словом: «60 /prct. para o Estado».
        body = _pgdl_body(page.replace(" /prct.", " %"), source["url"])
        _markup.require(source["title"], body, source["url"])
        return _markup.document(source["title"], source["url"], ctx.stamp, body, source.get("version", ""))

    return [Item(id=source["id"], file=f"{source['id']}.txt", make=make)]


# ── PDF ─────────────────


def _ocr_cached(data: bytes, index: int) -> list[str]:
    """Розпізнана сторінка лежить в out/ocr примірника: 480 сторінок сканів — це півгодини
    процесора, а правка заголовків і колонтитулів міняє лише те, що робиться з рядками далі."""
    folder = pathlib.Path(os.environ["DF_INSTANCE_DIR"]) / "out" / "ocr"
    path = folder / f"{hashlib.sha256(data).hexdigest()[:24]}-{index}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    lines = _ocr_lines(data, index)
    folder.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(lines, ensure_ascii=False), encoding="utf-8")
    return lines


def _ocr_lines(data: bytes, index: int) -> list[str]:
    import numpy
    import pypdfium2
    doc = pypdfium2.PdfDocument(data)
    try:
        image = numpy.asarray(doc[index].render(scale=_OCR_DPI / 72).to_pil())
    finally:
        doc.close()
    found, _ = _ocr_engine()(image)
    rows: list[list] = []
    for box, text, _score in sorted(found or (), key=lambda f: f[0][0][1]):
        y = (box[0][1] + box[2][1]) / 2
        if rows and abs(rows[-1][0] - y) < _OCR_ROW:
            rows[-1][1].append((box[0][0], text))
        else:
            rows.append([y, [(box[0][0], text)]])
    return [" ".join(t for _x, t in sorted(row[1])) for row in rows]


def _paragraphs(lines: list[str], headings: list) -> str:
    """Рядки сторінок стають абзацами: абзац кінчається там, де рядок закінчив речення, а
    наступний починається з великої літери чи номера. Рядок-заголовок стає `## …`."""
    out: list[str] = []
    for line in lines:
        if any(r.match(line) for r in headings):
            out.append("## " + line)
        elif out and not out[-1].startswith("## ") and not re.search(r"[.:;!?»)]$", out[-1]):
            if out[-1].endswith("-") and line[:1].islower():
                out[-1] = out[-1][:-1] + line
            else:
                out[-1] += " " + line
        elif out and not out[-1].startswith("## ") and line[:1].islower():
            out[-1] += " " + line
        else:
            out.append(line)
    return "\n\n".join(out)


def _pdf_body(data: bytes, source: dict) -> str:
    from pypdf import PdfReader
    skip = [re.compile(r) for r in source.get("skip_lines") or ()]
    heads = [re.compile(r) for r in source.get("headings") or ()]
    reader = PdfReader(io.BytesIO(data))
    lines: list[str] = []
    scanned = False
    for index, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if len(text.strip()) < _SCAN_CHARS:
            scanned = True
            found = _ocr_cached(data, index)
        else:
            found = text.splitlines()
        for line in found:
            line = " ".join(line.split())
            if line and not any(r.search(line) for r in skip):
                lines.append(line)
    body = _paragraphs(lines, heads)
    return f"{OCR_NOTE} Цитату звіряти з PDF за адресою джерела.\n\n{body}" if scanned else body


def _pdf_item(source: dict, ctx, url: str, title: str, name: str) -> Item:
    def make():
        body = _pdf_body(ctx.bytes(url), source)
        _markup.require(title, body, url)
        return _markup.document(title, url, ctx.stamp, body, source.get("version", ""))

    return Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make)


# ── cnpd-decisions ─────────────────

_CNPD_CARD = re.compile(r'<a href="(/umbraco/surface/cnpdDecision/download/\d+)"[^>]*>(.*?)</a>', re.S)
_CNPD_FIELD = re.compile(r'<div class="c-card-[a-z-]+">(.*?)</div>', re.S)
_CNPD_COUNT = re.compile(r"(\d+) registos? encontrados?")


@register("cnpd-decisions")
def cnpd_decisions(source: dict, ctx) -> list[Item]:
    base = source["url"]
    last = int(ctx.stamp[:4])
    items = []
    for kind, word in source["types"].items():
        for year in range(int(source["since"]), last + 1):
            page = ctx.text(f"{base}?year={year}&type={kind}")
            cards = _CNPD_CARD.findall(page)
            count = _CNPD_COUNT.search(page)
            # Сайт показує до 50 карток на рік, а гортання не має адреси: неповний перелік — відмова.
            if count and int(count.group(1)) != len(cards):
                raise SystemExit(f"{base}: {year}, тип {kind}: {count.group(1)} записів, а на сторінці "
                                 f"{len(cards)} — перелік неповний.")
            for href, card in cards:
                fields = [" ".join(html.unescape(_TAG.sub(" ", f)).split()) for f in _CNPD_FIELD.findall(card)]
                number = re.search(r"(\d+)/(\d{4})", fields[0]) if fields else None
                if not number:
                    raise SystemExit(f"{base}: картка без номера ({fields}).")
                name = f"{word}-{number.group(2)}-{number.group(1)}"
                items.append(_pdf_item(source, ctx, urljoin(base, href), " — ".join(fields), name))
    return items


# ── pdf-list ─────────────────


@register("pdf-list")
def pdf_list(source: dict, ctx) -> list[Item]:
    entries = [(p["url"], p["title"], p.get("name", "")) for p in source.get("pdfs") or ()]
    match = re.compile(source.get("match", r"\.pdf$"))
    for index in source.get("index") or ():
        page = ctx.text(index)
        for href, text in re.findall(r'<a [^>]*?href="([^"]+)"[^>]*>(.*?)</a>', page, flags=re.S):
            url = urljoin(index, html.unescape(href))
            title = " ".join(html.unescape(_TAG.sub(" ", text)).split())
            if match.search(url) and ctx.allowed(url) and title:
                entries.append((url, title, ""))
    items, names = [], set()
    for url, title, name in entries:
        name = name or _markup.slug(urlsplit(url).path.rsplit("/", 1)[-1].rsplit(".", 1)[0])
        if name not in names:
            names.add(name)
            items.append(_pdf_item(source, ctx, url, title, name))
    if not items:
        raise SystemExit(f"{source['id']}: не знайдено жодного PDF — розмітка змінилась.")
    return items
