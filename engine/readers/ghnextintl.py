"""Читач історії сайту next-intl.dev у репозиторії: як `ghdocs-history`, але з розбором компонентів сайту.

`ghdocs-history-nextintl` — markdown і MDX сайту з багатьох тегів одного репозиторію разом. Поля ті
                           самі, що в `ghdocs-history` (`url`, `tags`, `folders`, `recursive`,
                           `extensions`, `exclude`, `name_prefix` …). Текст кожного файла `.md`/`.mdx`
                           перед звичайним розбором проходить заміни, описані нижче.

Навіщо. Сайт next-intl (Nextra) пише сторінки з компонентами, які спільний розбір губить або
перетворює на шум:

- **Назва файла блоку коду** (```` ```tsx filename="src/i18n/request.ts" ````) — саме з неї видно,
  куди класти код, а розбір лишає від рядка відкриття лише мову. Тут вона стає рядком
  «File `src/i18n/request.ts`:» перед блоком, як у сайті Prisma (`_prismamdx`).
- **Вкладки** `<Tabs items={['i18n/request.ts', 'Provider']}>` з `<Tabs.Tab>` (у 2.x — `<Tab>`):
  без підписів дві версії коду (з маршрутизацією за мовою і без неї, сервер і клієнт) стояли б
  поруч без пояснення, котра є котрою. Кожна вкладка дістає підпис зі свого місця в `items`.
- **Питання `<details>`/`<Details>`** — `<summary>Питання?</summary>` стає рядком `**Питання?**`,
  а не загубленим серед абзаців реченням.
- **Банери курсу й партнерів** (`<CourseVideoBanner title=…/>`, «Prefer to watch a video?»,
  `<StayUpdated />`, відео в блозі) і коментарі JSX `{/* … */}` поза кодом знімаються: від банера розбір лишав би
  назву відеоуроку окремим рядком.

Чому окремий модуль, а не поля в `ghdocs-history`: спільний читач звірено в багатьох готових
примірниках, а тут досить підмінити текст файла, перш ніж читач його розбере.
"""

import re

from engine.readers import register
from engine.readers.ghhistory import ghdocs_history

_FENCE = re.compile(r"^([ \t]*)(```+|~~~+)(.*)$")
_FILENAME = re.compile(r"\bfilename\s*=\s*\"([^\"]+)\"")
_TABS = re.compile(r"^\s*<Tabs\b[^>]*\bitems\s*=\s*\{\s*\[(.*?)\]\s*\}[^>]*>\s*$")
_TAB = re.compile(r"^\s*<(?:Tabs\.Tab|Tab)\b[^>]*>\s*$")
_TABS_END = re.compile(r"^\s*</Tabs>\s*$")
_STRINGS = re.compile(r"'([^']*)'|\"([^\"]*)\"")
_SUMMARY = re.compile(r"<summary>\s*(.*?)\s*</summary>", re.S)
_BANNER = re.compile(r"<(?:CourseVideoBanner|CourseBanner|PartnerBanner|StayUpdated|BlogVideo"
                     r"|BlogVimeoVideo)\b"
                     r"(?:[^<>]|\{[^{}]*\})*/>", re.S)
_WATCH = re.compile(r"^[ \t]*(?:<summary>)?Prefer to watch a video\?(?:</summary>)?[ \t]*\n", re.M)
_JSX_COMMENT = re.compile(r"\{/\*.*?\*/\}", re.S)


def _prose(text: str) -> str:
    """Заміни для тексту поза блоками коду."""
    text = _BANNER.sub("", text)
    text = _WATCH.sub("", text)
    text = _JSX_COMMENT.sub("", text)
    return _SUMMARY.sub(lambda m: f"**{' '.join(m.group(1).split())}**", text)


def _rework(text: str) -> str:
    """Текст сторінки сайту next-intl з підписами вкладок і назвами файлів коду, без банерів."""
    out, prose, fence, tabs = [], [], "", []

    def flush():
        if prose:
            out.extend(_prose("\n".join(prose)).split("\n"))
            prose.clear()

    for line in text.split("\n"):
        m = _FENCE.match(line)
        if fence:
            out.append(line)
            if m and m.group(2).startswith(fence) and not m.group(3).strip():
                fence = ""
            continue
        if m:
            flush()
            name = _FILENAME.search(m.group(3))
            if name:
                out += ["", f"File `{name.group(1)}`:", ""]
            fence = m.group(2)
            out.append(line)
            continue
        t = _TABS.match(line)
        if t:
            tabs.append([[a or b for a, b in _STRINGS.findall(t.group(1))], 0])
            prose.append("")
            continue
        if _TAB.match(line) and tabs:
            items, i = tabs[-1]
            tabs[-1][1] += 1
            prose += ["", f"{items[i]}:" if i < len(items) else "", ""]
            continue
        if _TABS_END.match(line) and tabs:
            tabs.pop()
            prose.append("")
            continue
        prose.append(line)
    flush()
    return "\n".join(out)


class _Ctx:
    """Той самий контекст завантаження, лише текст файлів `.md`/`.mdx` проходить `_rework`."""

    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        return _rework(text) if re.search(r"\.mdx?$", url.split("?", 1)[0]) else text


@register("ghdocs-history-nextintl")
def ghdocs_history_nextintl(source: dict, ctx):
    return ghdocs_history(source, _Ctx(ctx))
