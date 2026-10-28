"""Читач `pdf` — стандарти, які Ecma видає лише як PDF (ECMA-404, ECMA-414).

Текст дістає pypdf. У витягнутому тексті трапляються розриви слів («inter change»,
«abou t») — так розкладено літери у самому файлі, і читач цього не лагодить, щоб
не вигадувати слова. Колонтитули, номери сторінок, зміст із крапками і сторінка з
ліцензією прибираються; вступ лишається перед першим розділом. Код перенесено з
колишнього завантажувача практики без змін по суті.

Поле `headings: "markdown"` — для примірника з `sections: "markdown"`: нумерований заголовок
(«8.6 Statements») стає заголовком markdown («### 8.6 Statements», глибина — за номером), а номер
глави з крапкою, як у старих виданнях ECMA-334 2002–2006 («1. Scope», «8. Language overview»),
теж вважається заголовком. Без поля — усе, як було.

Поле `version` — мітка редакції: стає рядком «версія:» у шапці документа (редакції ECMA-262
1997–2009). Без поля — усе, як було.

Поле `line_numbers: true` — PDF друкує на полі номер кожного рядка (1-ше видання ECMA-334, 2001), і
pypdf приклеює його до кінця рядка («8.6 Statements7», «is 1 9»). Номери на сторінці йдуть підряд
від 1, тож знімається лише число, що дорівнює наступному очікуваному; саме число в тексті
(«is 1») лишається. Без поля — усе, як було.
"""

import io
import re

from engine.readers import Item, register

_HEADING = re.compile(r"^\d+(?:\.\d+)*\s+\S")
# Старі видання ECMA-334 пишуть номер глави з крапкою: «1. Scope», «8. Language overview».
_HEADING_DOTTED = re.compile(r"^\d+(?:\.\d+)*\.?\s+\S")
_PAGE_NUMBER = re.compile(r"^\s*(\d+|[ivx]+)\s*$")


def _pdf_text(data: bytes, line_numbers: bool = False) -> list[str]:
    try:
        import pypdf
    except ImportError:
        raise SystemExit("Потрібен pypdf: він є в спільних наборах (requirements/cpu.txt, "
                         "requirements/gpu.txt); запускайте через ./df <примірник> <крок>")
    reader = pypdf.PdfReader(io.BytesIO(data))
    lines = []
    for page in reader.pages:
        page_lines = (page.extract_text() or "").splitlines()
        if line_numbers:
            page_lines = _strip_line_numbers(page_lines)
        lines.extend(page_lines)
    return lines


def _strip_line_numbers(lines: list[str]) -> list[str]:
    """Номер рядка на полі сторінки, приклеєний до кінця рядка: знімається лише той, що
    дорівнює наступному очікуваному (вони йдуть підряд від 1)."""
    out, expected = [], 1
    for i, ln in enumerate(lines):
        m = re.search(r"\s*(\d+)$", ln)
        if m and int(m.group(1)) == expected:
            # Рядок із самого числа перед першим нумерованим — номер сторінки (на сторінці 1
            # він збігається з очікуваним); порожній нумерований рядок наступного числа не має.
            if m.start() == 0 and i + 1 < len(lines) and re.search(rf"\s*{expected}$", lines[i + 1]):
                out.append(ln)
                continue
            ln = ln[:m.start()]
            expected += 1
        out.append(ln)
    return out


def _keep(line: str) -> bool:
    s = line.strip()
    if not s or "Ecma International" in s and ("©" in s or "©" in line):
        return False
    if _PAGE_NUMBER.match(s) or "......" in s:
        return False
    return True


# Заголовок, набраний у PDF розрядкою: «1S c o p e», «8T y p e s» (ECMA-262 1997–1999).
_SPACED = re.compile(r"^(\d+(?:\.\d+)*)\s*([A-Z](?: [a-z])+)((?: \d+)?)$")


def _unspace(line: str) -> str:
    m = _SPACED.match(line)
    return f"{m.group(1)} {m.group(2).replace(' ', '')}{m.group(3)}" if m else line


def _clean_pdf(lines: list[str], markdown: bool = False) -> str:
    """Вступ плюс тіло від останнього «1 Scope»; колонтитули і зміст геть."""
    lines = [_unspace(re.sub(r"[ \t]+", " ", ln).rstrip()) for ln in lines]
    heading = _HEADING_DOTTED if markdown else _HEADING
    scope = r"^1\.? Scope\s*$" if markdown else r"^1 Scope\s*$"
    starts = [i for i, ln in enumerate(lines) if re.match(scope, ln)]
    if not starts:
        raise SystemExit("У PDF не знайдено розділу «1 Scope» — текст видобуто не так, як очікувалося.")
    body = lines[starts[-1]:]
    intro = []
    intro_at = [i for i, ln in enumerate(lines[:starts[-1]]) if ln.strip() == "Introduction"]
    if intro_at:
        for ln in lines[intro_at[0] + 1:starts[-1]]:
            if ln.strip().upper().startswith("COPYRIGHT") or ln.lstrip().startswith("©") \
                    or "......" in ln or ln.strip() == "Contents":
                break
            intro.append(ln)
    out = []
    for ln in intro + body:
        if not _keep(ln):
            continue
        s = ln.strip()
        if heading.match(s):
            if markdown:
                depth = s.split()[0].rstrip(".").count(".") + 1
                s = "#" * min(depth + 1, 6) + " " + s
            out.append("")
            out.append(s)
            out.append("")
            continue
        # Кінець речення і наступний рядок з великої літери — межа абзацу.
        if out and out[-1] and re.search(r"[.:;]$", out[-1]) and s[:1].isupper():
            out.append("")
        out.append(s)
    text = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", text).strip("\n")


def _document_pdf(data: bytes, title: str, url: str, stamp: str, markdown: bool = False,
                  line_numbers: bool = False, version: str = "") -> str:
    body = _clean_pdf(_pdf_text(data, line_numbers), markdown)
    head = f"# {title}\n# джерело: {url}\n# отримано: {stamp}\n"
    if version:
        head += f"# версія: {version}\n"
    return f"{head}\n{body}\n"


@register("pdf")
def pdf(source: dict, ctx) -> list[Item]:
    url = source["url"]
    title = source.get("title", source["id"])
    markdown = source.get("headings") == "markdown"
    line_numbers = bool(source.get("line_numbers"))

    def make():
        return _document_pdf(ctx.bytes(url), title, url, ctx.stamp, markdown, line_numbers,
                             str(source.get("version") or ""))

    return [Item(id=source["id"], file=f"{source['id']}.txt", make=make)]
