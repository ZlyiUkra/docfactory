"""Читач `pdf-paper` — стаття, що існує лише PDF-ом.

`pdf-paper` — `url` — сам PDF; `title` — назва документа (у тексті скану її надійно
              не видно); `page` — людська адреса для шапки, змовчання — `url`.
              `skip_lines` — вирази рядків, що викидаються: колонтитули, номери
              сторінок. `version` — версія документа. Далі одна з двох форм:
              `heading` — вираз рядка-заголовка розділу (скан, текст суцільними
              рядками); типово — номер і слова великими літерами («3 MODEL OF
              COMPUTATION»). `layout: true` — текст із розкладкою сторінки: заголовок
              — короткий рядок з першої колонки між порожніми рядками.

Навіщо. Читач `pdf` розрахований на стандарти Ecma і без розділу «1 Scope»
відмовляє. Стаття — інша форма: заголовки розділів, колонтитули журналу з номером
сторінки, переноси слів у кінці рядка.

Скан (Liskov & Wing, 1994) несе помилки розпізнавання («supert ype», «Llskov») і
зіпсовані формули; читач їх не лагодить, щоб не вигадувати слова. Абзацом там
вважається рядок, що закінчується крапкою і помітно коротший за повний рядок.

Статті з цифровим текстом (колонки Мартіна в The C++ Report) звичайним видобуванням
розсипаються: кожне слово курсивом чи капітеллю стає окремим рядком. Видобування з
розкладкою тримає рядок цілим і порожній рядок між абзацами, а відступ розводить
заголовки (перша колонка) і підписи на рисунках (відцентровані). Вирівнювання за
шириною дає в рядку десятки пробілів — вони стискаються до одного, окрім відступу
на початку рядка: у лістингах коду він і є структурою.
"""

import io
import re

from engine.readers import Item, _markup, register
from engine.readers.pdf import _pdf_text

_HEADING = r"^\d+\.?\s+[A-Z][A-Z ,'’-]{3,}$"
# Рядок, коротший за цю частку найдовших рядків тексту, — кінець абзацу.
_SHORT = 0.75
# Підписи, що стоять у першій колонці, як заголовки, але ними не є.
_CAPTION = re.compile(r"^(Figure|Listing|Table)\b")


def _layout_text(data: bytes) -> list[str]:
    try:
        import pypdf
    except ImportError:
        raise SystemExit("Потрібен pypdf: .venv/bin/pip install pypdf")
    reader = pypdf.PdfReader(io.BytesIO(data))
    lines = []
    for page in reader.pages:
        lines.extend((page.extract_text(extraction_mode="layout") or "").splitlines())
    return lines


def _paper(lines: list[str], heading, skips: list) -> str:
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in lines]
    lines = [ln for ln in lines if ln and not any(r.search(ln) for r in skips)]
    widths = sorted(len(ln) for ln in lines)
    full = widths[int(len(widths) * 0.9)] if widths else 0
    out: list[str] = []
    para = ""
    for ln in lines:
        if heading.match(ln):
            if para:
                out.append(para)
                para = ""
            out.append("## " + ln)
            continue
        if para.endswith("-") and ln[:1].islower():
            para = para[:-1] + ln
        else:
            para = f"{para} {ln}" if para else ln
        if ln.endswith(".") and len(ln) < full * _SHORT:
            out.append(para)
            para = ""
    if para:
        out.append(para)
    return "\n\n".join(out)


def _layout(lines: list[str], skips: list) -> str:
    rows = []
    for ln in lines:
        ln = ln.rstrip()
        indent = len(ln) - len(ln.lstrip())
        body = re.sub(r" {2,}", " ", ln.lstrip())
        if body and any(r.search(body) for r in skips):
            continue
        rows.append((indent, body))
    out: list[str] = []
    last = ""
    for i, (indent, text) in enumerate(rows):
        prev_blank = i == 0 or not rows[i - 1][1]
        next_blank = i + 1 == len(rows) or not rows[i + 1][1]
        if (text and indent == 0 and prev_blank and next_blank and len(text) < 70
                and text[0].isupper() and not re.search(r"[.:,;]$", text)
                and not _CAPTION.match(text)):
            # Число в кінці заголовка — знак виноски, а не частина назви. Той самий
            # заголовок удруге — колонтитул сторінки з назвою поточного розділу.
            title = "## " + re.sub(r" \d+$", "", text)
            if title != last:
                out.append(title)
                last = title
            continue
        if text and out and out[-1].endswith("-") and text[:1].islower():
            out[-1] = out[-1][:-1] + text
            continue
        out.append(" " * indent + text if text else "")
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip("\n")


@register("pdf-paper")
def pdf_paper(source: dict, ctx) -> list[Item]:
    url = source["url"]
    page = source.get("page") or url
    title = source.get("title") or source["id"]
    heading = re.compile(source.get("heading") or _HEADING)
    skips = [re.compile(r) for r in source.get("skip_lines") or ()]

    def make():
        data = ctx.bytes(url)
        if source.get("layout"):
            body = _layout(_layout_text(data), skips)
        else:
            body = _paper(_pdf_text(data), heading, skips)
        _markup.require(title, body, url)
        return _markup.document(title, page, ctx.stamp, body, source.get("version", ""))

    return [Item(id=source["id"], file=f"{source['id']}.txt", make=make)]
