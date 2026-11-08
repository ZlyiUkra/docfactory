"""Читач книжки чи статті PDF за закладками: пункт закладок до заданої глибини — документ.

`pdf-outline` — PDF береться з `file` (абсолютний шлях на цій машині: файл завантажила людина) або з
                `url` (звернення крізь білий список примірника). `title` — назва книжки чи статті: вона
                стоїть перед назвою кожного документа («Louppe, Understanding Random Forests: 3.2 …»);
                `page` — людська адреса для шапки, змовчання — `url`. Необов'язкові: `depth` — найглибший
                рівень закладок, що стає окремим документом (типово 1: глави й розділи); глибші пункти
                стають підзаголовками всередині документа; `skip` — вираз назв пунктів, що не беруться
                (зміст, покажчик, список літератури); `name_prefix` — початок імені кожного документа (типово id джерела);
                `version` — мітка версії; `min_chars` — найкоротше тіло. PDF без закладок — один
                документ на кожні `chunk_pages` сторінок (типово 4) з назвою «назва, с. N–M».

Навіщо. Книжки й статті про дерева рішень лежать PDF-файлами, зверстаними щоразу інакше (LaTeX,
Springer, CRC, Packt, O'Reilly), і підлаштовувати під кожну розбір шрифтів, як у `pdf-book`, означало б
дев'ять різних настроювань. Закладки ж мають майже всі: автор чи видавець ставить їх на кожну главу й
розділ, і межі документа беруться звідти. Текст — простий витяг pypdf, а сторінку, на якій pypdf
падає, читач бере через PDFium (pypdfium2).

Що прибирається. Колонтитули — рядки з двох перших і двох останніх місць сторінки, що з цифрами,
заміненими на «#», повторюються щонайменше на п'ятій частині сторінок (назва глави, номер сторінки,
назва книжки); окремий рядок з одного лише числа. Перенос слова в кінці рядка («deci-» + «sion»)
зливається, коли далі мала літера. Рядки абзацу склеюються, а абзац закінчується на рядку, що
завершується крапкою, двокрапкою чи знаком питання і помітно коротший за звичайний.
"""

import collections
import io
import re

from engine.readers import Item, _markup, register

_SKIP = (r"^(Contents|Table of Contents|Index|Subject Index|Author Index|Bibliography|References|"
         r"Cover|Half[ -]?Title|Title Page|Series Page|Copyright.*|Dedication|Epigraph|About Packt|"
         r"Other Books You May Enjoy|Humble Bundle|Colophon|About the Authors?|Contributors|"
         r"Leave a review.*|Why subscribe\?)$")
_NUMBER = re.compile(r"^\s*[\divxlcIVXLC]+\s*$")
_DIGITS = re.compile(r"\d+")
_END = re.compile(r"[.:?!]\s*$")


def _outline(reader, entries, out, depth=0):
    for entry in entries:
        if isinstance(entry, list):
            _outline(reader, entry, out, depth + 1)
            continue
        try:
            page = reader.get_destination_page_number(entry)
        except Exception:
            page = None
        if page is not None:
            out.append((" ".join(str(entry.title).split()), page, depth))
    return out


def _key(text: str) -> str:
    return re.sub(r"\W+", "", text).lower()[:40]


class _Pages:
    """Рядки сторінок без колонтитулів; сторінку, на якій pypdf падає, читає PDFium."""

    def __init__(self, reader, data, label):
        self.reader, self.data, self.label = reader, data, label
        self.raw: dict[int, list[str]] = {}
        self.pdfium = None
        self.furniture: set[str] = set()

    def lines(self, n: int) -> list[str]:
        if n not in self.raw:
            try:
                text = self.reader.pages[n].extract_text() or ""
            except Exception as exc:  # pypdf падає на окремих шрифтах
                import pypdfium2
                if self.pdfium is None:
                    self.pdfium = pypdfium2.PdfDocument(self.data)
                page = self.pdfium[n]
                text_page = page.get_textpage()
                text = text_page.get_text_range().replace("\r", "")
                text_page.close()
                page.close()
                print(f"  {self.label}: сторінку {n + 1} pypdf не прочитав ({type(exc).__name__}), "
                      f"прочитано через PDFium", flush=True)
            # Математичні знаки поза основною площиною Юнікоду pypdf подекуди віддає парою чи й
            # одиноким сурогатом («\ud835»), а такий рядок не записати в UTF-8: пара зливається в
            # знак, одинокий стає «�».
            text = text.encode("utf-16", "surrogatepass").decode("utf-16", "replace")
            self.raw[n] = [line.rstrip() for line in text.splitlines()]
        return self.raw[n]

    def learn_furniture(self, total: int) -> None:
        """Колонтитул — крайній рядок сторінки, що повторюється: з номером сторінки на краю рядка
        («62 Chapter 3. Bagging») — щонайменше на трьох сторінках, бо назва глави в колонтитулі
        тримається лише в межах глави; без номера (назва книжки) — на п'ятій частині сторінок."""
        seen = collections.Counter()
        for n in range(total):
            lines = [line for line in self.lines(n) if line.strip()]
            for line in set(lines[:2] + lines[-2:]):
                seen[_DIGITS.sub("#", line.strip())] += 1
            if len(self.raw) > 32:
                self.raw.clear()
        numbered = re.compile(r"^#|#$")
        self.furniture = {k for k, c in seen.items()
                          if (c >= 3 and numbered.search(k)) or c >= max(3, total // 5)}
        self.raw.clear()

    def clean(self, n: int) -> list[str]:
        lines = self.lines(n)
        out = []
        for i, line in enumerate(lines):
            edge = i < 3 or i >= len(lines) - 3
            if edge and (_NUMBER.match(line) or _DIGITS.sub("#", line.strip()) in self.furniture):
                continue
            out.append(line)
        if len(self.raw) > 32:
            self.raw.clear()
        return out


def _paragraphs(lines: list[str]) -> str:
    widths = sorted(len(x) for x in lines if x.strip())
    full = widths[int(len(widths) * 0.8)] if widths else 80
    paras: list[str] = []
    cur = ""
    for line in lines:
        text = line.strip()
        if not text:
            if cur:
                paras.append(cur)
                cur = ""
            continue
        if cur.endswith("-") and text[:1].islower():
            cur = cur[:-1] + text
        else:
            cur = f"{cur} {text}" if cur else text
        if _END.search(text) and len(text) < 0.8 * full:
            paras.append(cur)
            cur = ""
    if cur:
        paras.append(cur)
    return "\n\n".join(paras)


@register("pdf-outline")
def pdf_outline(source: dict, ctx) -> list[Item]:
    import pypdf

    label = source.get("title") or source["id"]
    if source.get("file"):
        try:
            data = open(source["file"], "rb").read()
        except OSError as exc:
            raise SystemExit(f"{source['id']}: не відкрив {source['file']}: {exc}")
    elif source.get("url"):
        if not ctx.allowed(source["url"]):
            raise SystemExit(f"{source['id']}: адреса {source['url']} поза білим списком.")
        data = ctx.bytes(source["url"])
    else:
        raise SystemExit(f"{source['id']}: читач pdf-outline потребує поля file або url.")
    reader = pypdf.PdfReader(io.BytesIO(data))
    total = len(reader.pages)
    pages = _Pages(reader, data, label)
    pages.learn_furniture(total)
    page_url = source.get("page") or source.get("url") or ""
    depth_max = int(source.get("depth", 1))
    skip = re.compile(source.get("skip") or _SKIP, re.I)
    # Ім'я документа починається з id джерела: «algorithm», «pp-1-4» чи «8-5-random-forests» є в кількох
    # книжках і статтях одного примірника, і без префікса їхні розділи злилися б в один ключ.
    lead = f"{_markup.slug(source.get('name_prefix') or source['id'])}-"
    min_chars = int(source.get("min_chars", 200))

    marks = _outline(reader, reader.outline, []) if reader.outline else []
    marks.sort(key=lambda m: m[1])
    spans = []    # (назва, перша сторінка, остання сторінка не включно, назви глибших пунктів)
    if marks:
        tops = [m for m in marks if m[2] <= depth_max]
        for i, (title, page, depth) in enumerate(tops):
            end = tops[i + 1][1] if i + 1 < len(tops) else total
            if skip.search(title):
                continue
            inner = [m[0] for m in marks if m[2] > depth_max and page <= m[1] < max(end, page + 1)]
            nxt = tops[i + 1][0] if i + 1 < len(tops) and tops[i + 1][1] == end else None
            spans.append((title, page, max(end, page + 1), inner, nxt))
    else:
        size = int(source.get("chunk_pages", 4))
        for a in range(0, total, size):
            spans.append((f"pp. {a + 1}–{min(total, a + size)}", a, min(total, a + size), [], None))

    items, names = [], collections.Counter()
    for title, first, end, inner, nxt in spans:
        lines = []
        for n in range(first, end):
            lines += pages.clean(n)
        # Початок — рядок із назвою пункту на першій сторінці; кінець — назва наступного пункту на
        # останній сторінці, коли наступний починається посеред неї.
        first_page = len(pages.clean(first))
        head = next((i for i, line in enumerate(lines[:first_page]) if _key(line) and _key(title).startswith(_key(line)[:20])
                     and len(_key(line)) >= min(12, len(_key(title)))), None)
        if head is not None:
            lines = lines[head + 1:]
        if nxt:
            tail = [i for i, line in enumerate(lines) if _key(line) and _key(nxt).startswith(_key(line)[:20])
                    and len(_key(line)) >= min(12, len(_key(nxt)))]
            if tail:
                lines = lines[:tail[-1]]
        # Глибші пункти закладок — підзаголовки: рядок, що збігається з назвою пункту, стає «## …».
        wanted = {_key(t): t for t in inner if _key(t)}
        blocks, run = [], []
        for line in lines:
            k = _key(line.replace("\x00", ""))
            if k in wanted and len(line.strip()) <= len(wanted[k]) + 10:
                if run:
                    blocks.append(_paragraphs(run))
                    run = []
                blocks.append(f"## {wanted.pop(k)}")
            else:
                run.append(line.replace("\x00", ""))
        if run:
            blocks.append(_paragraphs(run))
        body = "\n\n".join(b for b in blocks if b.strip())
        if len(body) < min_chars:
            continue
        full = f"{label}: {title}"
        slug = lead + _markup.slug(title)
        names[slug] += 1
        if names[slug] > 1:
            slug = f"{slug}-{names[slug]}"

        def make(full=full, body=body):
            _markup.require(full, body, page_url, min_chars)
            return _markup.document(full, page_url, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{slug}", file=f"{source['id']}--{slug}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: у PDF не знайдено жодного розділу з текстом.")
    print(f"  {label}: сторінок {total}, документів {len(items)}", flush=True)
    return items
