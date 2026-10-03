"""Читач `cncf-curriculum` — програми сертифікаційних іспитів CNCF (github.com/cncf/curriculum).

`url` — дерево гілки через API (…/repos/ВЛАСНИК/РЕПО/git/trees/ГІЛКА?recursive=1), `within` —
тека raw.githubusercontent.com тієї ж гілки. Документом стає кожен PDF дерева, що лежить у
білому списку; файли однакового вмісту (той самий хеш блоба — побайтово однакові) дають один
документ, і в ньому перелічено всі їхні шляхи. Назва — «<Іспит> Curriculum» і номери з імен
файлів; версії Kubernetes з імен (CKA_Curriculum_v1.35, CKAD_Curriculum_V1.12.0) лягають у
рядок «версія» шапки — усі, під якими цей вміст лежить. Файл без номера версії її не має.

Навіщо окремий читач. Програми видаються лише як PDF, і `pdf` їх не прочитає: той шукає
розділ «1 Scope» стандарту Ecma і читає сторінку рядками, як її віддає pypdf. А тут:

1. Дві колонки. Ліва — «10% - Storage» і пункти під ним, права — «30% - Troubleshooting» і
   свої пункти; pypdf віддає їх упереміш. Читач бере позиції фрагментів (visitor pypdf),
   складає рядки за висотою і ділить рядок навпіл за серединою сторінки, а колонки читає
   по черзі: розділ лишається зі своїми пунктами.
2. Старі програми CKA/CKAD 1.12–1.15 набрано по літері: кожна гліфа — окремий фрагмент, і
   звичайне видобування дає літеру на рядок. Складання рядків за позицією зшиває їх назад.
3. Лігатури (ﬁ, ﬂ) — звичайними літерами, інакше «Conﬁgure» не знаходиться словом «configure».
4. Чотири програми (CAPA, CCA, CGOA, стара ICA) — картинки без текстового шару. Такі
   сторінки розпізнаються (OCR): pypdfium2 малює сторінку, rapidocr-onnxruntime читає. Обидва
   ставляться лише в примірник, якому це треба, і імпортуються тут же, коли до них дійшло:
   інші примірники без цих пакетів працюють як раніше. Документ з розпізнаним текстом
   позначено — у ньому можливі помилки.

Розділ «NN% - Назва» стає заголовком `## NN% - Назва`, кожен пункт — рядком «- …».
"""

import collections
import io
import json
import re
from urllib.parse import quote, unquote, urlsplit

from engine.readers import Item, _markup, register

_TREE = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/([^/]+)$")

_LIGATURES = {"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "st",
              "ﬆ": "st", "\u00a0": " ", "\u00ad": ""}
# Позначка пункту: крапка, квадратик, а в старих файлах — гліфа шрифту Symbol, що pypdf
# віддає як «\x87» чи символ приватної зони Unicode.
_BULLET = re.compile(r"^\s*[•●▪■◦‣∙·\x87\uf0a7\uf0b7\uf076\uf0d8]\s*")
# Розпізнавання бачить позначку пункту то двокрапкою, то крапкою, то чимось нечитним:
# поодинокий не-буквений знак перед словом — це вона.
_OCR_BULLET = re.compile(r"^\s*[^\w\s(\"'“‘]\s*(?=\w)")
_DOMAIN = re.compile(r"^(\d{1,3})\s*%\s*(?:[-–—:]\s*)?(\S.*)$")
_TRAILING_BULLET = re.compile(r"^\s*(\w.*?)\s*•\s*$")
_SECOND_DOMAIN = re.compile(r"\S\s+(\d{1,3}\s?%\s?[-–—]\s)")
_PAGE_NUMBER = re.compile(r"^\d{1,3}$")
_VERSION = re.compile(r"(?i)(?<![A-Za-z0-9.])v\s?(\d+)\.(\d+)((?:\.\d+)?)(?![\d.])")
# Довгі імена найперших файлів (2017–2018), де абревіатури іспиту немає.
_LONG_NAMES = (("certified_kubernetes_administrator", "CKA"),
               ("certified_kubernetes_application_developer", "CKAD"),
               ("certified_kubernetes_developer", "CKAD"))
_EXAM = re.compile(r"(?i)([a-z]+)(?:-\d{4})?[ _-]+curriculum")
# Найменша мінорна версія, яку номер у імені файла може означати як Kubernetes: перший CKA
# (2017) — на 1.6–1.7. Номери нижче (v0.9 чернетки CKA, v1.0 першого CKAD) — редакції самого
# документа, а не версії Kubernetes, і міткою версії не стають.
_MIN_MINOR = 6
# Сторінка, де літер менше, — картинка без текстового шару (на ній лишаються хіба позначки
# пунктів), її текст дає лише розпізнавання.
_MIN_LETTERS = 20
# Роздільність малювання для розпізнавання: за 200 точок на дюйм дрібний шрифт пунктів
# (10–11 пт) читається впевнено, а сторінка ще не займає сотні мегабайт.
_OCR_DPI = 200
# Нижче цієї впевненості розпізнаний шматок — шум (логотипи, візерунки фону).
_OCR_MIN_SCORE = 0.5
OCR_NOTE = "Увага: текст розпізнано з зображення (OCR), можливі помилки."

# Гліфа з пробілом-здогадкою попереду, як її віддає pypdf 6.
_GLYPH = re.compile(r"\s+(\S)")

Frag = collections.namedtuple("Frag", "x y size text")
Row = collections.namedtuple("Row", "x y size text column")


def clean(text: str) -> str:
    """Лігатури — звичайними літерами, пробіли — по одному."""
    for lig, plain in _LIGATURES.items():
        text = text.replace(lig, plain)
    return " ".join(text.split())


# ── фрагменти сторінки ─────────────────────────────────────────────────────


def _identity(cm, tm) -> bool:
    return list(tm) == [1, 0, 0, 1, 0, 0] and not cm[4] and not cm[5]


def text_fragments(page) -> list:
    """Фрагменти текстового шару з позиціями: (x, y, кегль, текст) у пунктах сторінки.

    pypdf віддає текст із форм (XObject) двічі: зсередини форми — з позицією, а потім
    ще раз увесь разом, з одиничною матрицею. А буває й навпаки: фрагмент приходить з
    одиничною матрицею, а його позиція — у наступному, порожньому виклику. Тож фрагмент
    без позиції бере позицію в сусіда, а коли й там її немає — це повтор, і він відкидається.
    """
    calls = []
    page.extract_text(visitor_text=lambda t, cm, tm, fd, fs: calls.append(
        (t, list(cm), list(tm), fs)))
    out = []
    for i, (text, cm, tm, fs) in enumerate(calls):
        text = text.replace("\n", "")
        if not text:
            continue
        if _identity(cm, tm):
            nxt = calls[i + 1] if i + 1 < len(calls) else None
            if nxt is None or nxt[0].strip() or _identity(nxt[1], nxt[2]):
                continue
            cm, tm = nxt[1], nxt[2]
        # pypdf 6 ставить перед кожною гліфою файла, набраного по гліфі, власний
        # пробіл-здогадку («C», « e», « r»…). Пробіли між словами такі файли несуть
        # окремими гліфами, тож здогадка лише розриває слова — її прибрано.
        glyph = _GLYPH.fullmatch(text)
        if glyph:
            text = glyph.group(1)
        x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
        y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
        size = abs(tm[3] * cm[3]) * fs or 1.0
        out.append(Frag(x, y, size, text))
    # Сусідні в потоці сторінки гліфи, що стоять упритул по горизонталі, — один рядок.
    # pypdf 6 подекуди віддає першу гліфу рядка на ~0,8 кегля вище («1» у «18%» над
    # «8%»), і без цього вона відходила б в інший рядок або губилася.
    for i in range(len(out) - 1):
        a, b = out[i], out[i + 1]
        if (len(a.text) == 1 and len(b.text.strip()) == 1 and a.y != b.y
                and 0 < b.x - a.x <= 1.5 * max(a.size, b.size)
                and abs(a.y - b.y) <= max(a.size, b.size)):
            out[i] = a._replace(y=b.y)
    return out


_OCR_ENGINE = []


def _ocr_engine():
    """Рушій розпізнавання — один на прогін: модель вантажиться секунди і сотню мегабайт."""
    if not _OCR_ENGINE:
        try:
            from rapidocr_onnxruntime import RapidOCR
        except ImportError:
            raise SystemExit("Для PDF без текстового шару потрібен rapidocr-onnxruntime: "
                             ".venv/bin/pip install -r requirements.txt")
        _OCR_ENGINE.append(RapidOCR())
    return _OCR_ENGINE[0]


def ocr_fragments(data: bytes, index: int) -> list:
    """Фрагменти сторінки `index`, розпізнані з картинки, у тих самих пунктах, що й текст."""
    try:
        import numpy
        import pypdfium2
    except ImportError:
        raise SystemExit("Для PDF без текстового шару потрібен pypdfium2: "
                         ".venv/bin/pip install -r requirements.txt")
    doc = pypdfium2.PdfDocument(data)
    try:
        page = doc[index]
        height = page.get_height()
        image = numpy.asarray(page.render(scale=_OCR_DPI / 72).to_pil())
    finally:
        doc.close()
    found, _ = _ocr_engine()(image)
    k = 72 / _OCR_DPI
    out = []
    for box, text, score in found or ():
        if float(score) < _OCR_MIN_SCORE:
            continue
        top = min(p[1] for p in box)
        bottom = max(p[1] for p in box)
        left = min(p[0] for p in box)
        out.append(Frag(left * k, height - (top + bottom) / 2 * k, (bottom - top) * k, text))
    return out


# ── рядки й колонки ────────────────────────────────────────────────────────


def rows(frags: list, width: float, page_no: int = 0) -> list:
    """Рядки сторінки: фрагменти однієї висоти, кожна колонка окремо, колонки по черзі.

    Рядок ділиться на середині сторінки. Виняток — літера, що стоїть впритул до попередньої
    літери: це файл, набраний по гліфі, і рядок просто перетинає середину. Такі файли ще й
    друкують частину гліф двічі в тій самій точці (жирність накладанням) — повтор
    відкидається, інакше виходить «ttoo uussee tthheemm».

    Буває, що заголовки обох колонок набрано одним шматком тексту («44% - Kubernetes
    Fundamentals 16% - Cloud Native»): другий заголовок відрізається й стає на початок
    правої колонки, де під ним його продовження й пункти.
    """
    mid = width / 2
    split = []
    for f in frags:
        # Перший CKAD (v1.0) пише позначку пункту в кінці рядка: «Understand ConfigMaps•».
        tail = _TRAILING_BULLET.match(f.text)
        if tail:
            f = f._replace(text=f"• {tail.group(1)}")
        m = _SECOND_DOMAIN.search(f.text)
        if m and f.x < mid:
            split += [f._replace(text=f.text[:m.start(1)]),
                      f._replace(x=mid, text=f.text[m.start(1):])]
        else:
            split.append(f)
    frags = split
    order = sorted(range(len(frags)), key=lambda i: (-frags[i].y, frags[i].x, i))
    lines: list = []
    seen = set()
    for i in order:
        f = frags[i]
        key = (f.text, round(f.x, 1), round(f.y, 1))
        if key in seen:
            continue
        seen.add(key)
        if lines and abs(lines[-1][0] - f.y) <= max(2.0, 0.3 * f.size):
            lines[-1][1].append(i)
        else:
            lines.append((f.y, [i]))
    out = {0: [], 1: []}
    for y, members in lines:
        members.sort(key=lambda i: (frags[i].x, i))
        side, parts = 0, {0: [], 1: []}
        prev = None          # остання непорожня гліфа: пробіли бувають і відступом до колонки
        for i in members:
            f = frags[i]
            if side == 0 and f.x >= mid:
                glued = (prev is not None and len(prev.text) == 1
                         and f.x - prev.x <= 1.5 * max(prev.size, f.size))
                if not glued:
                    side = 1
            parts[side].append(f)
            if f.text.strip():
                prev = f
        for side, part in parts.items():
            if not part:
                continue
            text = "".join(p.text for p in part)
            if not text.strip():
                continue
            words = [p for p in part if p.text.strip() and not _BULLET.fullmatch(p.text)]
            size = max((p.size for p in words), default=part[0].size)
            out[side].append(Row(part[0].x, y, size, text, (page_no, side)))
    return out[0] + out[1]


# ── розмітка ───────────────────────────────────────────────────────────────


def _join(head: str, tail: str) -> str:
    """Продовження на наступному рядку. Перенос «deploy-/ments» зшивається в слово, а
    «Self-/Service» — у слово з дефісом."""
    if re.search(r"[a-z]-$", head) and tail[:1].islower():
        return head[:-1] + tail
    if re.search(r"\w-$", head):
        return head + tail
    return f"{head} {tail}"


def layout(rows_: list, ocr: bool = False) -> str:
    """Рядки сторінок → markdown: розділ «NN% - …» заголовком, пункт — рядком «- …»,
    решта — абзацами. Повтори (колонтитул з назвою на кожній сторінці) відкидаються."""
    blocks: list = []        # [вид, текст, кегль]: «h» розділ, «b» пункт, «p» абзац
    last = None              # попередній рядок тієї ж колонки
    bullet_x = None
    for row in rows_:
        text = clean(row.text)
        if not text or _PAGE_NUMBER.match(text):
            continue
        if last is not None and last.column != row.column:
            last = None
        near = last is not None and last.y - row.y <= 2.2 * max(row.size, last.size)
        cur = blocks[-1] if blocks and last is not None else None
        marker = _BULLET.match(text) or (ocr and _OCR_BULLET.match(text))
        domain = _DOMAIN.match(text)
        if domain and not marker:
            blocks.append(["h", f"{domain.group(1)}% - {domain.group(2).strip(' :')}", row.size])
        elif marker:
            blocks.append(["b", text[marker.end():], row.size])
            bullet_x = row.x
        elif cur and cur[0] == "h" and near and row.size >= 0.85 * cur[2] and not (
                ocr and last.y - row.y > 1.6 * max(row.size, last.size)):
            # Продовження заголовка — тим самим кеглем. Висоти розпізнаних рамок гуляють, і
            # пункт під заголовком у картинці буває лише на десяту частину нижчий, тож там
            # рішення за відстанню: другий рядок заголовка стоїть щільно, пункти — нижче.
            cur[1] = _join(cur[1], text).strip(" :")
        elif cur and cur[0] == "b" and near and row.size <= 1.2 * cur[2] and not (
                ocr and bullet_x is not None and row.x <= bullet_x + 0.5 * row.size):
            cur[1] = _join(cur[1], text)
        elif cur and cur[0] == "b" and near and ocr:
            # Розпізнавання загубило позначку, але рядок стоїть там, де починаються пункти.
            blocks.append(["b", text, row.size])
        elif (ocr and cur and cur[0] == "h" and row.size < 1.15 * cur[2]
              and last.y - row.y <= 4 * cur[2]):
            # Перший рядок під розділом у картинці — пункт, що загубив позначку. Позначка
            # стояла б на кегль лівіше, тож продовження з тим самим відступом — продовження.
            blocks.append(["b", text, row.size])
            bullet_x = row.x - row.size
        elif cur and cur[0] == "p" and near and abs(row.size - cur[2]) <= 0.15 * cur[2]:
            cur[1] = _join(cur[1], text)
        else:
            blocks.append(["p", text, row.size])
        last = row
    out, seen = [], set()
    for kind, text, _ in blocks:
        text = text.strip()
        if not text:
            continue
        if kind == "h":
            out.append(f"\n## {text}\n")
        elif kind == "b":
            out.append(f"- {text}")
        elif text not in seen:
            seen.add(text)
            out.append(f"\n{text}\n")
    body = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", body).strip("\n")


def curriculum_text(data: bytes) -> tuple[str, bool]:
    """Текст програми з PDF і чи довелося розпізнавати бодай одну сторінку."""
    try:
        import pypdf
    except ImportError:
        raise SystemExit("Потрібен pypdf: .venv/bin/pip install -r requirements.txt")
    reader = pypdf.PdfReader(io.BytesIO(data))
    all_rows, ocr = [], False
    for n, page in enumerate(reader.pages):
        frags = text_fragments(page)
        letters = sum(ch.isalpha() for f in frags for ch in f.text)
        if letters < _MIN_LETTERS:
            frags = ocr_fragments(data, n)
            ocr = True
        all_rows.extend(rows(frags, float(page.mediabox.width), n))
    return layout(all_rows, ocr), ocr


# ── імена файлів ───────────────────────────────────────────────────────────


def _stem(path: str) -> str:
    return unquote(path.rsplit("/", 1)[-1]).removesuffix(".pdf")


def name_versions(path: str) -> list:
    """Номери з імені файла як написано («v1.35», «v1.12.0»)."""
    return [f"v{a}.{b}{c}" for a, b, c in _VERSION.findall(_stem(path))]


def k8s_versions(path: str) -> list:
    """Версії Kubernetes з імені файла: «1.35», «1.12» (з V1.12.0); редакції документа
    (v0.9, v1.0) — ні."""
    return [f"{a}.{b}" for a, b, _ in _VERSION.findall(_stem(path))
            if a == "1" and int(b) >= _MIN_MINOR]


def _vkey(label: str) -> tuple:
    return tuple(int(p) for p in re.findall(r"\d+", label))


def exam_title(path: str) -> str:
    """«CKA Curriculum», а слова імені поза іспитом і номером — у дужках («Coming Q3 2021»)."""
    stem = _stem(path)
    rest = _VERSION.sub(" ", stem)
    exam = next((short for long, short in _LONG_NAMES if long in stem.lower()), "")
    if exam:
        rest = ""
    else:
        m = _EXAM.search(rest)
        if m:
            word = m.group(1)
            exam = word.upper() if len(word) <= 5 else word.capitalize()
            rest = rest[:m.start()] + " " + rest[m.end():]
        else:
            exam, rest = stem, ""
    extra = [w for w in re.split(r"[\s_-]+", rest) if w and w.lower() != "copy"]
    return f"{exam} Curriculum" + (f" ({' '.join(extra)})" if extra else "")


def _primary(paths: list) -> str:
    """Шлях, за яким документ названо: чинний файл з кореня, коли він є серед однакових,
    інакше — з найбільшим номером. Однакові CKS 1.19–1.23 інакше звалися б першим іменем,
    «… v1.19 Coming Soon November 2020», хоч вміст давно не анонс."""
    def key(p):
        top = max((_vkey(v) for v in name_versions(p)), default=())
        return ("/" in p, tuple(-n for n in top), p)
    return sorted(paths, key=key)[0]


def document(paths: list, data: bytes, blob_base: str, stamp: str) -> str:
    primary = _primary(paths)
    numbers = sorted({v for p in paths for v in name_versions(p)}, key=_vkey)
    title = exam_title(primary) + (f" {', '.join(numbers)}" if numbers else "")
    labels = sorted({v for p in paths for v in k8s_versions(p)}, key=_vkey)
    text, ocr = curriculum_text(data)
    head = "Файли в репозиторії: " + ", ".join(sorted(paths, key=lambda p: ("/" in p, p)))
    if ocr:
        head += "\n\n" + OCR_NOTE
    body = f"{head}\n\n{text}"
    if not text.strip():
        raise SystemExit(f"{primary}: тексту не видобуто — документ не записую.")
    return _markup.document(title, blob_base + quote(primary), stamp, body, ", ".join(labels))


@register("cncf-curriculum")
def cncf_curriculum(source: dict, ctx) -> list[Item]:
    url = source["url"]
    m = _TREE.match(urlsplit(url).path)
    if not m:
        raise SystemExit(f"{url}: очікував адресу дерева /repos/ВЛАСНИК/РЕПО/git/trees/ГІЛКА.")
    owner, repo, ref = m.groups()
    try:
        tree = json.loads(ctx.text(url))
    except ValueError as exc:
        raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
    if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
        raise SystemExit(f"{url}: у відповіді немає дерева файлів.")
    if tree.get("truncated"):
        raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
    raw_base = f"https://raw.githubusercontent.com/{owner}/{repo}/{quote(ref)}/"
    blob_base = f"https://github.com/{owner}/{repo}/blob/{quote(ref)}/"
    groups: dict = {}
    for entry in tree["tree"]:
        path = entry.get("path", "")
        if entry.get("type") != "blob" or not path.lower().endswith(".pdf"):
            continue
        if not ctx.allowed(raw_base + quote(path)):
            continue
        groups.setdefault(entry.get("sha") or path, []).append(path)
    items = []
    for paths in groups.values():
        primary = _primary(paths)
        name = _markup.slug(primary.removesuffix(".pdf"))

        def make(paths=paths, primary=primary):
            data = ctx.bytes(raw_base + quote(primary))
            return document(paths, data, blob_base, ctx.stamp)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    if not items:
        raise SystemExit(f"{url}: у дереві немає жодного дозволеного PDF.")
    return items
