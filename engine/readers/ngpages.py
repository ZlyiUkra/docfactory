"""Читач сторінок-компонентів Angular: документація, що жила в HTML-шаблонах.

`ngpages` — глави сайту, зібраного як застосунок Angular, де кожна глава це пара
файлів у `src/app/homepage/pages/`: шаблон `X.component.html` з текстом і клас
`X.component.ts` з прикладами коду.

Навіщо. До квітня 2018 docs.nestjs.com не мав теки `content/` узагалі: теперішні
читачі markdown там не мають чого читати, і лінії 4 та 5 лишалися в корпусі самими
нотатками релізів. Текст при цьому нікуди не подівся, він просто лежить розміткою.

Чому окремий модуль, а не гілка в наявних читачах: примірники `ecmascript` і
`react` зібрані й звірені, а правка спільного читача — ризик зсуву в готовій
роботі. Хто не назвав ім'я `ngpages` у sources.json, того цей модуль не стосується.

Три особливості цієї розмітки, через які звичайний «зняти теги» не годиться:

1. Прикладів коду в шаблоні немає. Там стоїть підстановка Angular —
   `<pre><code class="language-typescript">{{ catsController }}</code></pre>`, — а
   сам приклад лежить у класі компонента властивістю `get catsController()`.
   Читач, що просто зняв би теги, дав би главу, з якої зник увесь код: не порожню,
   а гіршу — таку, що виглядає повною. Тому шаблон і клас читаються парою.

2. Приклад має два різновиди, TypeScript і JavaScript: два сусідні `<pre>`, з яких
   сайт показує один, дивлячись на перемикач. Обидва лягають в одну огорожу через
   `@@switch` — рівно так, як їх записує markdown пізніших ліній.

3. Ім'я файлу над прикладом теж підстановка — `{{ 'cats.controller' | extension: … }}`.
   Воно стає рядком `@@filename(cats.controller)` всередині огорожі, знову ж як у
   markdown пізніших ліній.

Непевність — відмова, а не здогад. Підстановка, якій не знайшлося властивості в
класі, зупиняє документ: глава з мовчки зниклим прикладом дає хибну відповідь на
питання «як це писалося тоді», а зупинка не псує нічого, бо наявний файл лишається
як був.

Імена документів зводяться до адрес сайту тією ж таблицею маршрутів, що й у
`ghdocs-heading` (поле `route_map`): тека компонента зветься
`fundamentals/dependency-injection`, а сторінка вже тоді жила за адресою
`fundamentals/custom-providers`, під якою лежить і донині.
"""

import html as _html
import json
import re
import sys
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register
from engine.readers.mdheading import _route_map

_TREE = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/([^/]+)$")
_PAGES = "src/app/homepage/pages/"
_PAGE_HTML = re.compile(r"^src/app/homepage/pages/(.+)/[^/]+\.component\.html$")

# get catsController(): string { return `…`; } — приклад коду в класі компонента.
# Крапка з комою після закривної лапки необов'язкова: у частині глав її просто не
# поставили, і вимога її наявності мовчки лишала главу без прикладу.
_GETTER = re.compile(r"\bget\s+(\w+)\s*\(\)\s*(?::\s*string\s*)?\s*\{\s*"
                     r"return\s+`((?:[^`\\]|\\.)*)`\s*;?", re.S)
# Шматки шаблону, що потребують заміни: ім'я файлу над прикладом і сам приклад.
_PIECE = re.compile(
    r"<span\s+class=[\"']filename[\"'][^>]*>(?P<fn>.*?)</span>"
    r"|<pre(?P<attrs>[^>]*)>\s*<code(?P<cattrs>[^>]*)>\s*\{\{\s*(?P<name>\w+)\s*\}\}\s*"
    r"</code>\s*</pre>", re.S)
_EXT = re.compile(r"\{\{\s*'([^']+)'\s*\|\s*extension:[^}]*\}\}")
_LANG = re.compile(r"language-([\w+#-]+)")
# [class.hide]="!xT.isJsActive" — саме цей <pre> сайт показує в режимі JavaScript.
_JS_TWIN = re.compile(r"\[class\.hide\]\s*=\s*[\"']\s*!")
_TABS = re.compile(r"<app-tabs[^>]*>\s*(?:</app-tabs>)?", re.S)
_H3 = re.compile(r"<h3[^>]*>(.*?)</h3>", re.S)
_LEFTOVER = re.compile(r"\{\{(.*?)\}\}", re.S)
_TAG = re.compile(r"</?[A-Za-z][\w.-]*(?:\s[^<>]*)?/?>")


def _samples(ctx, url: str) -> dict:
    """{ім'я властивості: текст прикладу} з класу компонента."""
    return {name: code.replace("\\`", "`").strip("\n")
            for name, code in _GETTER.findall(ctx.text(url))}


def _fence(lang: str, filename: str, ts: str, js: str = "") -> str:
    """Огорожа коду у вигляді, який дає markdown пізніших ліній: ім'я файлу рядком
    `@@filename(…)`, другий різновид після `@@switch`. Екранування обов'язкове:
    у коді трапляється `Array<string>`, і без нього розбирач шаблону прийняв би це
    за тег і мовчки викинув шматок прикладу."""
    body = []
    if filename:
        body.append(f"@@filename({filename})")
    body.append(ts)
    if js:
        body.append("@@switch")
        body.append(js)
    text = _html.escape("\n".join(body))
    return f'<pre class="language-{lang}"><code>{text}</code></pre>'


def _prepare(text: str, samples: dict, where: str) -> str:
    """Шаблон Angular → звичайний HTML, який уже вміє читати `_markup.html_body`.

    Приклади спершу лягають мітками, а справжнім текстом стають в останню чергу.
    Порядок тут не косметичний: у главі про MVC прикладом є шаблон Handlebars, а в
    ньому літерально стоїть `{{ message }}`. Вставивши приклад одразу, читач побачив
    би цей рядок серед підстановок Angular — і або підставив би замість нього чуже
    (спотворивши приклад), або відмовив би цілій справній главі. Поки на місці
    прикладів стоять мітки, перевірка дивиться лише на власні підстановки шаблону.
    """
    if "\x00" in text:
        raise SystemExit(f"Сторінка не схожа на документ ({where}): у шаблоні є нульовий "
                         f"байт, яким читач позначає місця прикладів — документ не записую.")
    fences: list[dict] = []
    out: list[str] = []
    last, pending, open_at = 0, "", -1
    for m in _PIECE.finditer(text):
        gap = text[last:m.start()]
        last = m.end()
        if gap.strip():
            open_at = -1
        out.append(gap)
        if m.group("fn") is not None:
            ext = _EXT.search(m.group("fn"))
            pending = ext.group(1) if ext else _TAG.sub("", m.group("fn")).strip()
            open_at = -1
            continue
        name = m.group("name")
        if name not in samples:
            raise SystemExit(f"Сторінка не схожа на документ ({where}): у класі "
                             f"компонента немає прикладу «{name}», на який посилається "
                             f"шаблон — документ без коду не записую, наявний лишається "
                             f"як був.")
        found = (_LANG.search(m.group("cattrs") or "")
                 or _LANG.search(m.group("attrs") or ""))
        lang = found.group(1) if found else "typescript"
        if open_at >= 0 and _JS_TWIN.search(m.group("attrs") or ""):
            fences[open_at]["js"] = samples[name]
            open_at = -1
            continue
        fences.append({"lang": lang, "filename": pending, "ts": samples[name], "js": ""})
        out.append(f"\x00{len(fences) - 1}\x00")
        open_at, pending = len(fences) - 1, ""
    out.append(text[last:])
    ready = _TABS.sub("", "".join(out))

    # Підстановка трапляється й посеред речення: «…avoid typing
    # <code>{{ apiModelPropertyOptional }}</code>». Це не огорожа, а вставка в рядок,
    # тож переноси в ній згортаються в пробіли. `re.sub` вставленого не перечитує,
    # отже приклад, що сам містить фігурні дужки, не потрапить під другий розбір.
    missing: list[str] = []

    def inline(m):
        name = m.group(1).strip()
        if name in samples:
            return _html.escape(" ".join(samples[name].split()))
        missing.append(name)
        return m.group(0)

    ready = _LEFTOVER.sub(inline, ready)
    if missing:
        raise SystemExit(f"Сторінка не схожа на документ ({where}): у шаблоні лишилися "
                         f"нерозібрані підстановки ({'; '.join(missing[:3])}) — текст був "
                         f"би неповним, документ не записую.")
    return re.sub(r"\x00(\d+)\x00", lambda m: _fence(**fences[int(m.group(1))]), ready)


def _take_title(text: str) -> tuple[str, str]:
    """(назва з першого <h3>, шаблон без того заголовка). Назва вже стоїть у шапці
    документа, тож лишати її вдруге означало б дублювати в кожному фрагменті."""
    m = _H3.search(text)
    if not m:
        return "", text
    return " ".join(_TAG.sub("", m.group(1)).split()), text[:m.start()] + text[m.end():]


def _document(ctx, base: str, path: str, page: str, version: str) -> str:
    raw = ctx.text(base + path)
    ready = _prepare(raw, _samples(ctx, base + path[:-5] + ".ts"), page)
    title, ready = _take_title(ready)
    body = _markup.html_body(ready)
    _markup.require(title, body, page, min_chars=1)
    return _markup.document(title, page, ctx.stamp, body, version)


@register("ngpages")
def ngpages(source: dict, ctx) -> list[Item]:
    m = _TREE.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував адресу дерева коміту "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/КОМІТ.")
    owner, repo, tag = m.groups()
    try:
        tree = json.loads(ctx.text(source["url"]))
    except ValueError as exc:
        raise SystemExit(f"{source['url']}: відповідь не JSON ({exc}) — перелік не складено.")
    if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
        raise SystemExit(f"{source['url']}: у відповіді немає дерева файлів.")
    if tree.get("truncated"):
        raise SystemExit(f"{source['url']}: GitHub обрізав дерево — перелік був би неповним.")
    all_paths = [e.get("path", "") for e in tree["tree"] if e.get("type") == "blob"]
    base = f"https://raw.githubusercontent.com/{owner}/{repo}/{tag}/"
    routes = _route_map(ctx, base, all_paths) if source.get("route_map") is True else {}
    renamed, items = 0, []
    for path in sorted(all_paths):
        page_dir = _PAGE_HTML.match(path)
        if not page_dir or path[:-5] + ".ts" not in all_paths:
            continue
        raw = base + path
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{tag}/{path}"
        stem = page_dir.group(1)
        if stem in routes:
            if routes[stem] != stem:
                renamed += 1
            stem = routes[stem]
        name = _markup.slug(stem)

        def make(raw=raw, path=path, blob=blob):
            return _document(ctx, base, path, blob, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['url']}: у {_PAGES} немає жодної пари "
                         f"«X.component.html + X.component.ts».")
    if routes:
        print(f"  {source['id']}: таблиця маршрутів на {len(routes)} сторінок, "
              f"зведено імен {renamed}", file=sys.stderr)
    return items
