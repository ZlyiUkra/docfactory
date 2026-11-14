"""Читач сайту Sphinx у зібраному HTML: знімок кожної версії, яку сайт публікує окремою текою.

`sphinx-html` — `url` — стартова сторінка версії з `{version}` на місці номера
                (`…/container-toolkit/{version}/index.html`); `versions` — номери тек, які
                публікує сайт, від найновішого. Сторінки версії — стартова й усе, куди з неї
                (і далі зі знайдених сторінок) ведуть посилання `.html` у межах теки цієї ж
                версії та поля `within`. Необов'язкові: `exclude` — вирази адрес, що не
                беруться (пошук, покажчики й службові теки `_static`, `_sources`, `_images`
                не беруться й так); `end` — вирази, на яких текст сторінки закінчується
                (найближчий), типово `</article>`, `<footer`, `rst-footer-buttons`;
                `version_prefix` — рядок перед номером у мітці версії. `min_chars` — найкоротше
                тіло без підзаголовка: сторінка атрибута в довіднику pandas має один рядок опису.
                `version_labels` — об'єкт «тека → номер»: Read the Docs називає теки
                `release_3.3.0` і `stable`, а мітка версії мусить бути номером («3.3», «3.4»).
                Тека без запису в об'єкті дає мітку з власної назви, як і без поля.
                `qualify_titles` — `true`: сторінка класу, що починається сигнатурою «class
                torch.nn.Linear(…», дістає назву «torch.nn.Linear» замість короткої «Linear».
                `name_prefix` — рядок перед іменем кожного документа: у примірнику onnx три сайти
                Sphinx (onnx, onnxruntime, skl2onnx) мають сторінки `index.html` і
                `api_summary.html`, і без префікса вони ділили б один ключ розділу. Без поля імена
                ті самі, що й були.
                `skip_untitled` — `true`: сторінка без `<h1>` не документ, а посилання з неї все
                одно йдуть в обхід. У scikit-learn такі сторінки двох видів: заглушки-переадресації
                на місці перейменованих сторінок (`documentation.html` → `index.html`) і зміст
                посібника старої теми (`user_guide.html` 0.16 — лише toctree). Без поля сторінка
                без `<h1>`, як і раніше, зупиняє перелік.
                `param_types` — `true`: між назвою параметра й типом у довіднику numpydoc
                (`<strong>endog</strong><span class="classifier">array_like</span>`) стає
                « : », як у старій темі. Без цього назва зливається з типом в одне слово
                («seasonal_orderiterable»), і пошук за назвою параметра її не знаходить
                (statsmodels). Без поля текст той самий, що й був.

Навіщо. Документація NVIDIA Container Toolkit на docs.nvidia.com — сайт Sphinx, і кожна версія
лежить своєю текою (`…/1.20.1/`, `…/1.6.0/`), а перелік версій (`versions1.json`) називає лише
вісім найновіших. Мапи сайту немає, набори сторінок різних років різні (старі — overview,
concepts, user-guide; нові — install-guide, docker-specialized, cdi-support), тож перелік —
обхід посилань від стартової сторінки в межах теки версії. `html-pages` бере лише посилання
однієї сторінки-змісту однієї версії і не знає розмітки Sphinx:

- якір заголовка (`<a class="headerlink">#</a>`, у старій темі — значок шрифту U+F0C1) дописувався
  б до кожного заголовка: «## Configuration#» — уже інший ключ розділу й інше слово для пошуку;
- мова блоку коду записана в класі обгортки (`<div class="highlight-console">`), а не `<pre>`;
- вкладки sphinx-tabs старої теми мають назви в `<button>` («CentOS 8», «CentOS 7»), які розбір
  HTML викидає разом з усіма кнопками: команди двох систем злипалися б у безіменний ряд коду;
  вкладки sphinx-design — у `<label>` без жодного розриву перед вмістом;
- заголовок виноски (`<p class="admonition-title">Note</p>`) лишався б окремим словом без двокрапки;
- зміст `toctree` — перелік посилань, який повторює бічне меню: стартова сторінка старої теми
  тільки з нього й складається, і такої сторінки як документа немає (посилання з неї все одно
  ведуть обхід далі).

Документ — неповторний текст сторінки: та сама сторінка кількох версій з дослівно однаковим
текстом — один документ, у версії якого лягають усі ці версії, а адреса — сторінка найновішої з
них; ім'я — «джерело--шлях-сторінки-<8 знаків хеша тексту>», і `revision_suffix` дає редакціям
однієї сторінки спільний ключ. Тексти рахуються ще під час переліку (обхід однаково читає кожну
сторінку), у пам'яті лишається лише текст без HTML.
"""

import hashlib
import re
from urllib.parse import urldefrag, urljoin, urlsplit

from engine.readers import Item, _markup, register

_HREF = re.compile(r'href="([^"]+)"')
_H1 = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.S)
_SKIP = [re.compile(r"/(search|genindex|py-modindex|objects)\.html$"),
         re.compile(r"/_(static|sources|images|downloads)/")]
_ENDS = [r"</article>", r"<footer\b", r"rst-footer-buttons"]
_HEADERLINK = re.compile(r'<a class="headerlink"[^>]*>.*?</a>', re.S)
# Обгортка підсвіченого блоку: мова — у класі обгортки, сам <pre> без класу.
_HIGHLIGHT = re.compile(r'<div class="highlight-([\w+#-]+)[^"]*">\s*<div class="highlight">\s*<pre>')
# sphinx-tabs: назви вкладок — кнопки переліку, панель посилається на свою кнопку.
_TAB_BUTTON = re.compile(r'<button\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</button>', re.S)
_TABLIST = re.compile(r'<div\b[^>]*role="tablist"[^>]*>.*?</div>', re.S)
_TAB_PANEL = re.compile(r'(<div\b[^>]*aria-labelledby="([^"]+)"[^>]*class="sphinx-tabs-panel"[^>]*>)')
# sphinx-design: назва вкладки — <label> перед вмістом, перемикач — <input>.
_SD_LABEL = re.compile(r'<label class="sd-tab-label"[^>]*>(.*?)</label>', re.S)
_ADMONITION_TITLE = re.compile(r'<p class="admonition-title">(.*?)</p>', re.S)
_DIV_TAG = re.compile(r"<(/?)div\b[^>]*>")
# Клітинка таблиці docutils — абзац у <td>: розбір HTML ставив би кожну клітинку окремим абзацом,
# і рядок таблиці розсипався б стовпчиком.
_TABLE = re.compile(r"<table\b.*?</table>", re.S)
_CELL_P = re.compile(r"</?p\b[^>]*>")
# Перший абзац пункту списку (`<li><p>…</p>`): без цього між пунктами стояли б порожні рядки, а
# пункт відривався б від свого маркера.
_LI_P = re.compile(r"(<li\b[^>]*>)\s*<p>(.*?)</p>", re.S)
_TOCTREE = re.compile(r'<div class="toctree-wrapper\b')
# Тип параметра numpydoc новішої теми: окремий <span> одразу за назвою, без розділювача.
_CLASSIFIER = re.compile(r'</strong>\s*<span class="classifier">')
# Мови, які нічого не кажуть: блок без мови — так само простий текст.
_NO_LANG = {"default", "none", "text"}


def _cut_divs(html: str, start: re.Pattern) -> str:
    """Вирізає кожен елемент <div>, що починається збігом `start`, разом із вкладеними <div>:
    зміст toctree — переліки в переліках, і лінивий вираз зупинився б на першому </div>."""
    out, pos = [], 0
    while True:
        m = start.search(html, pos)
        if not m:
            out.append(html[pos:])
            return "".join(out)
        out.append(html[pos:m.start()])
        depth, end = 0, len(html)
        for tag in _DIV_TAG.finditer(html, m.start()):
            depth += -1 if tag.group(1) else 1
            if depth == 0:
                end = tag.end()
                break
        pos = end


def _plain(html: str) -> str:
    return " ".join(_markup.html_body(html).split())


def _label_tabs(html: str) -> str:
    names = {i: _plain(t) for i, t in _TAB_BUTTON.findall(html)}
    html = _TABLIST.sub("", html)
    html = _TAB_PANEL.sub(lambda m: m.group(1) + (f"<p>{names[m.group(2)]}:</p>"
                                                  if names.get(m.group(2)) else ""), html)
    return _SD_LABEL.sub(lambda m: f"<p>{_plain(m.group(1))}:</p>", html)


def page_text(html: str, url: str, ends: list, param_types: bool = False) -> tuple[str, str]:
    """(назва, тіло) сторінки Sphinx; тіло порожнє, коли на сторінці, крім змісту, нічого."""
    m = _H1.search(html)
    if not m:
        raise SystemExit(f"На сторінці немає <h1> ({url}) — документ не записую.")
    title = _plain(_HEADERLINK.sub("", m.group(1))).rstrip("#¶ ")
    stop = min((e.start() for e in (r.search(html, m.end()) for r in ends) if e),
               default=len(html))
    part = _HEADERLINK.sub("", html[m.end():stop])
    part = _cut_divs(part, _TOCTREE)
    if param_types:
        part = _CLASSIFIER.sub('</strong> : <span class="classifier">', part)
    part = _label_tabs(part)
    part = _ADMONITION_TITLE.sub(lambda t: f"<p>{_plain(t.group(1)).rstrip(':')}:</p>", part)
    part = _TABLE.sub(lambda t: _CELL_P.sub(" ", t.group(0)), part)
    part = _LI_P.sub(r"\1\2", part)
    part = _HIGHLIGHT.sub(lambda h: "<pre>" if h.group(1) in _NO_LANG
                          else f'<pre class="language-{h.group(1)}">', part)
    return title, _markup.html_body(part).replace("", "")


# Сигнатура класу на першому рядку сторінки довідника autodoc: «class torch.nn.Linear(…».
_CLASS_SIG = re.compile(r"\s*class\s+([\w.]+)\(")


def _qualified(title: str, body: str) -> str:
    """Повне ім'я класу замість короткого заголовка сторінки (`qualify_titles`).

    PyTorch називає сторінку класу коротким ім'ям («CrossEntropyLoss»), а сторінку функції —
    повним («torch.compile»). Модель питає повним ім'ям класу, а `title_match` свідомо не
    зараховує «CrossEntropyLoss» у «torch.nn.CrossEntropyLoss» (так «toString» не збігається з
    «Object.prototype.toString»), тож сторінка класу програвала сторінкам, де ім'я стоїть у
    тексті. Назва замінюється, лише коли сигнатура закінчується саме коротким заголовком."""
    m = _CLASS_SIG.match(body)
    if m and m.group(1).rsplit(".", 1)[-1] == title and "." in m.group(1):
        return m.group(1)
    return title


@register("sphinx-html")
def sphinx_html(source: dict, ctx) -> list[Item]:
    template = source["url"]
    versions = [str(v) for v in source.get("versions") or ()]
    if "{version}" not in template or not versions:
        raise SystemExit(f"{source['id']}: читач sphinx-html потребує `url` з {{version}} і "
                         f"поля `versions` — переліку тек, які публікує сайт.")
    exclude = _SKIP + [re.compile(r) for r in source.get("exclude") or ()]
    ends = [re.compile(r) for r in source.get("end") or _ENDS]
    vprefix = source.get("version_prefix", "")
    vlabels = source.get("version_labels") or {}
    untitled = bool(source.get("skip_untitled"))
    qualify = bool(source.get("qualify_titles"))
    param_types = bool(source.get("param_types"))

    # Сторінка → {хеш тексту → [назва, тіло, адреса найновішої версії, версії]}; порядок
    # сторінок — порядок обходу найновішої версії, де сторінка з'явилася вперше.
    pages: dict[str, dict] = {}
    for version in versions:
        start = template.replace("{version}", version)
        root = start.rsplit("/", 1)[0] + "/"
        if not ctx.allowed(start):
            raise SystemExit(f"{source['id']}: адреса {start} поза білим списком.")
        queue, seen = [start], {start}
        while queue:
            url = queue.pop(0)
            try:
                html = ctx.text(url)
            except SystemExit as e:
                if url == start:
                    raise
                print(f"  {url}: {e} — сторінку пропускаю", flush=True)
                continue
            for href in _HREF.findall(html):
                link = urldefrag(urljoin(url, href.strip()))[0].split("?", 1)[0]
                if (link not in seen and link.startswith(root) and link.endswith(".html")
                        and ctx.allowed(link) and not any(r.search(link) for r in exclude)):
                    seen.add(link)
                    queue.append(link)
            if untitled and not _H1.search(html):
                continue
            title, body = page_text(html, url, ends, param_types)
            if qualify:
                title = _qualified(title, body)
            if not body.strip():
                continue
            key = _markup.slug(urlsplit(url).path[len(urlsplit(root).path):].rsplit(".", 1)[0])
            digest = hashlib.sha1(f"{title}\n{body}".encode()).hexdigest()[:8]
            entry = pages.setdefault(key, {}).setdefault(digest, [title, body, url, []])
            entry[3].append(version)

    if not pages:
        raise SystemExit(f"{source['id']}: жодної сторінки з текстом у теках {versions} — "
                         f"розмітка сайту змінилася.")
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""
    items = []
    for key, revisions in pages.items():
        for digest, (title, body, url, vers) in revisions.items():
            def make(title=title, body=body, url=url, vers=vers):
                _markup.require(title, body, url,
                                int(source.get("min_chars", _markup.MIN_BODY)))
                return _markup.document(title, url, ctx.stamp, body,
                                        ", ".join(vprefix + vlabels.get(v, v) for v in vers))

            name = f"{lead}{key}-{digest}"
            items.append(Item(id=f"{source['id']}/{name}",
                              file=f"{source['id']}--{name}.txt", make=make))
    return items
