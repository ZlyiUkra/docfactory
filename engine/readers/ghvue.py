"""Читачі сайтів документації Vue: як `ghsite-dated`, `ghdocs-history`, `ghdocs`, з розбором розмітки.

`ghsite-dated-vue`   — те саме, що `ghsite-dated` (знімок репозиторію сайту на кожну версію
                       пакета npm): vuejs.org і давній vuejs.org (v2.vuejs.org), де тегів немає.
`ghdocs-history-vue` — те саме, що `ghdocs-history` (документація з тегів одного репозиторію):
                       Vue Router, Pinia, Vuex, Vue Test Utils.
`ghdocs-vue`         — те саме, що `ghdocs` (одне дерево): посібник переходу на Vue 3, блог, RFC.

Поля ті самі, що в цих читачів. Текст кожного файла `.md` перед звичайним розбором проходить
заміни, описані нижче; код прикладів у огорожах лишається як є.

Навіщо. Сайти Vue пишуть розмітку, яку спільний розбір губить або перетворює на шум:
- **Стиль API.** vuejs.org з 2022 року тримає на одній сторінці два тексти — для Options API і для
  Composition API (`<div class="options-api">` / `<div class="composition-api">`), а читач сайту
  перемикач бачить лише один. Без підпису обидва тексти стоять поруч, і розділ «Declaring
  Reactive State» трапляється двічі з тим самим заголовком. Тут блок дістає підпис «Options API:»
  чи «Composition API:», а заголовки в ньому — той самий підпис у дужках замість позначок ` \\*`
  і ` \\*\\*`, тож ключі розділів різні й пошук знає, котрий стиль описано. Рядкові
  `<span class="options-api">` стають «(Options API: …)».
- **Позначки версій у заголовку** (`## defineModel() <sup class="vt-badge" data-text="3.4+" />`,
  у VuePress — `<Badge text="3.2+" />`) стають рядком під заголовком: з позначкою в самому
  заголовку випуск, що її додав, давав би розділу новий ключ, і редакції перестали б зливатися.
  Поза заголовком позначка версії стає текстом «(3.4+)», позначка TypeScript знімається.
- **Контейнери VitePress і VuePress** (`::: tip`, `::: details`, `::: code-group`), підписи блоків
  коду й позначки підсвічування — як у `_vitepress`: «Tip: …» замість рядків із двокрапками;
  `{{ $frontmatter.title }}` у заголовку сторінок VuePress стає назвою з шапки.
- **Розмітка Hexo давнього сайту** (`{% raw %}`, `{% codeblock lang:js %}`, `<p class="tip">`):
  обгортки знімаються, блок коду стає огорожею, порада — рядком «Tip: …». Блок `{% raw %}` на
  власних рядках — це живий приклад (HTML і `<script>` демо на сторінці), він знімається цілим.
- **Позначки посібника переходу** (шапка `badges: [breaking]` і `<MigrationBadges … />` у заголовку)
  стають рядком «Badges: breaking.» під заголовком: інакше шапка з одним полем ставала назвою
  документа, а компонент у заголовку — шумом.
- **Живі приклади й банери** (`<script>`/`<style>` верхнього рівня, `<VueSchoolLink>`,
  `<ScrimbaLink>`) знімаються: від них розбір лишав код демо посеред тексту чи назву відеоуроку.

Чому окремий модуль, а не поля в спільних читачах: їх звірено в багатьох готових примірниках, а
тут досить підмінити текст файла, перш ніж читач його розбере.
"""

import re

from engine.readers import _markup, _vitepress, register
from engine.readers.ghdated import ghsite_dated
from engine.readers.ghhistory import ghdocs_history
from engine.readers.github import ghdocs

_FENCE = re.compile(r"^([ \t]*)(```+|~~~+)(.*)$")
_FRONT = re.compile(r"\A---[ \t]*\n.*?\n---[ \t]*(?:\n|\Z)", re.S)
_HEADING = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*$")
_ANCHOR = re.compile(r"[ \t]*(\{#[^}]*\})[ \t]*$")
_STAR = re.compile(r"[ \t]*(?:\\\*)+[ \t]*$")
_API_OPEN = re.compile(r"^[ \t]*<div\s+class=\"(options|composition)-api\"\s*>[ \t]*$")
_DIV_OPEN = re.compile(r"^[ \t]*<div\b[^>]*>[ \t]*$")
_DIV_CLOSE = re.compile(r"^[ \t]*</div>[ \t]*$")
_API_SPAN = re.compile(r"<span\s+class=\"(options|composition)-api\"\s*>(.*?)</span>", re.S)
_BADGE = re.compile(r"[ \t]*<(?:sup\s+class=\"vt-badge(?P<ts>\s+ts)?\""
                    r"(?:\s+data-text=\"(?P<vt>[^\"]*)\")?"
                    r"|Badge\b[^>]*?\btext=\"(?P<b>[^\"]*)\")[^>]*?/?>(?:</(?:sup|Badge)>)?")
_TIP = re.compile(r"<p\s+class=\"tip\"\s*>\s*")
_HEXO_CODE = re.compile(r"^[ \t]*\{%\s*codeblock(?:\s+lang:(\S+))?[^%]*%\}[ \t]*$")
_HEXO_CODE_END = re.compile(r"^[ \t]*\{%\s*endcodeblock\s*%\}[ \t]*$")
_HEXO_RAW = re.compile(r"\{%\s*(?:end)?raw\s*%\}")
_HEXO_DEMO = re.compile(r"^[ \t]*\{%\s*raw\s*%\}[ \t]*\n.*?^[ \t]*\{%\s*endraw\s*%\}[ \t]*$",
                        re.S | re.M)
_BANNER = re.compile(r"<(VueSchoolLink|ScrimbaLink|VueMasteryLogoLink)\b(?:[^<>]|\{[^{}]*\})*?"
                     r"(?:/>|>.*?</\1>)", re.S)
_STYLE = {"options": "Options API", "composition": "Composition API"}
_COMPONENT = re.compile(r"[ \t]*<[A-Z][\w.]*\b[^<>]*/>")
_BADGES = re.compile(r"^badges:[ \t]*\n((?:[ \t]+-[ \t]*\S.*\n?)+)", re.M)


def _heading(line: str, style: str) -> list[str]:
    """Заголовок без позначок версії в тексті: позначка — окремим рядком під ним; у блоці
    стилю API — з підписом стилю."""
    m = _HEADING.match(line)
    if not m:
        return [line]
    hashes, text = m.groups()
    notes = []
    for b in _BADGE.finditer(text):
        if b.group("ts"):
            notes.append("TypeScript-specific.")
        elif b.group("vt") or b.group("b"):
            notes.append(f"Version: {b.group('vt') or b.group('b')}")
    text = _COMPONENT.sub("", _BADGE.sub("", text))
    anchor = _ANCHOR.search(text)
    tail = ""
    if anchor:
        tail = " " + anchor.group(1)
        text = text[:anchor.start()]
    if style:
        text = _STAR.sub("", text) + f" ({style})"
    out = [f"{hashes} {text.rstrip()}{tail}"]
    if notes:
        out += ["", *notes]
    return out


def _prose(text: str) -> str:
    """Заміни для тексту поза блоками коду."""
    text = _BANNER.sub("", text)
    text = _HEXO_DEMO.sub("", text)
    text = _HEXO_RAW.sub("", text)
    text = _BADGE.sub(lambda b: "" if b.group("ts") or not (b.group("vt") or b.group("b"))
                      else f" ({b.group('vt') or b.group('b')})", text)
    text = _TIP.sub("\n\nTip: ", text)
    return _API_SPAN.sub(lambda m: f"({_STYLE[m.group(1)]}: {m.group(2).strip()})", text)


def _rework(text: str) -> str:
    front = _FRONT.match(text)
    head, body = (text[:front.end()], text[front.end():]) if front else ("", text)
    badges = _BADGES.search(head)
    if badges:
        names = [b.strip().lstrip("-").strip() for b in badges.group(1).splitlines() if b.strip()]
        head = head[:badges.start()] + head[badges.end():]
        if re.fullmatch(r"---[ \t]*\n---[ \t]*\n?", head):
            head = ""
        body = re.sub(r"^(# .*)$", lambda m: f"{m.group(1)}\n\nBadges: {', '.join(names)}.", body,
                      count=1, flags=re.M)
    body, _scripts = _vitepress._blocks_out(body)
    out, prose, fence = [], [], ""
    divs: list = []  # стек відкритих <div> на окремих рядках: стиль API або "" для інших

    def flush():
        if prose:
            out.extend(_prose("\n".join(prose)).split("\n"))
            prose.clear()

    for line in body.split("\n"):
        if fence:
            out.append(line)
            m = _FENCE.match(line)
            if (m and m.group(2).startswith(fence) and not m.group(3).strip()) \
                    or (fence == "hexo" and _HEXO_CODE_END.match(line)):
                if fence == "hexo":
                    out[-1] = "```"
                fence = ""
            continue
        m = _FENCE.match(line)
        if m:
            flush()
            fence = m.group(2)
            out.append(line)
            continue
        h = _HEXO_CODE.match(line)
        if h:
            flush()
            fence = "hexo"
            out.append(f"```{h.group(1) or ''}")
            continue
        a = _API_OPEN.match(line)
        if a:
            divs.append(_STYLE[a.group(1)])
            prose += ["", f"{_STYLE[a.group(1)]}:", ""]
            continue
        if _DIV_OPEN.match(line):
            divs.append("")
            prose.append(line)
            continue
        if _DIV_CLOSE.match(line) and divs:
            if divs.pop():
                prose.append("")
                continue
            prose.append(line)
            continue
        style = next((s for s in reversed(divs) if s), "")
        prose.extend(_heading(line, style))
    flush()
    meta = _markup.front_matter(head + "\n")[0] if head else {}
    return head + _vitepress._markup("\n".join(out), {"$frontmatter": meta or {}})


class _Ctx:
    """Той самий контекст завантаження, лише текст файлів `.md` проходить `_rework`."""

    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        return _rework(text) if re.search(r"\.md$", url.split("?", 1)[0]) else text


@register("ghsite-dated-vue")
def ghsite_dated_vue(source: dict, ctx):
    return ghsite_dated(source, _Ctx(ctx))


@register("ghdocs-history-vue")
def ghdocs_history_vue(source: dict, ctx):
    return ghdocs_history(source, _Ctx(ctx))


@register("ghdocs-vue")
def ghdocs_vue(source: dict, ctx):
    return ghdocs(source, _Ctx(ctx))
