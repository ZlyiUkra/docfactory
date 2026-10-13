"""Читач історії сайту nuqs.dev у репозиторії: як `ghdocs-history`, але з розбором компонентів MDX сайту.

`ghdocs-history-nuqs` — markdown і MDX сайту з багатьох тегів одного репозиторію разом. Поля ті самі,
                        що в `ghdocs-history` (`url`, `tags`, `folders`, `recursive`, `extensions`,
                        `exclude`, `name_prefix` …). Текст кожного файла `.mdx` перед звичайним розбором
                        проходить п'ять замін, описаних нижче (п'ята — багаторядкові імпорти, див. `_imports_out`).

Навіщо. Сайт nuqs (Fumadocs) пише сторінки для двох читачів одразу: `<HumanContent>` — для людей
(з іконками фреймворків і живими демо), `<LLMContent>` — те саме простим текстом для мовних
моделей. Розмітка `_markup` бере текст між тегами, тож обидві версії лягали б у документ поруч,
і перелік адаптерів чи приклад стояв би на сторінці двічі. Тут пара «HumanContent, а впритул за
ним LLMContent» (чи навпаки) лишає тільки LLMContent; самотній блок будь-якого з двох лишається
своїм текстом.

`<FeatureSupportMatrix introducedInVersion='2.5.0' />` — плашка «з якої версії є можливість»; без
заміни вона зникала б разом з тегом, а це саме те, про що питають. Тут вона стає реченням
«Introduced in nuqs 2.5.0.».

Позначки підсвічування rehype-pretty-code: мова в інлайн-коді (`` `useQueryState{:ts}` ``) і
коментарі shiki в блоках коду (`// [!code word:NuqsAdapter]`, `// [!code highlight]`) — не текст
документації, а розмітка сайту.

Чому окремий модуль, а не поле в `ghdocs-history`: спільний читач звірено в багатьох готових
примірниках, а тут досить підмінити текст файла, перш ніж читач його розбере.
"""

import re

from engine.readers import register
from engine.readers.ghhistory import ghdocs_history

# Вміст блоку — без інших тегів HumanContent/LLMContent: інакше лінивий збіг, не знайшовши пари
# одразу за першим блоком, розтягувався до наступного й ковтав усе між ними.
_INSIDE = r"((?:(?!</?(?:HumanContent|LLMContent)>).)*)"
_PAIR = re.compile(rf"<(HumanContent|LLMContent)>{_INSIDE}</\1>\s*"
                   rf"<(HumanContent|LLMContent)>{_INSIDE}</\3>", re.S)
# Обгортка демо: `fallback={<DemoFallback />}` має `>` усередині, і розмітка тег не впізнавала.
_SUSPENSE = re.compile(r"</?Suspense\b(?:[^<>]|<[^<>]*>)*>")
_SOLO = re.compile(r"</?(?:HumanContent|LLMContent)>")
_SINCE = re.compile(r"<FeatureSupportMatrix\b[^>]*?\bintroducedInVersion\s*=\s*['\"]([^'\"]+)['\"]"
                    r"[^>]*?/>")
_INLINE_LANG = re.compile(r"(`[^`\n]*?)\{:[\w-]+\}`")
_SHIKI_LINE = re.compile(r"^[ \t]*(?://|#|\{/\*)[ \t]*\[!code [^\]]*\](?:[ \t]*\*/\})?[ \t]*\n", re.M)
_SHIKI_TAIL = re.compile(r"[ \t]*(?://|#)[ \t]*\[!code [^\]]*\]")
_FENCE = re.compile(r"^[ \t]*(```|~~~)")
# Оператор import, а не речення, що починається словом «import» («import the parsers from
# `nuqs/parsers`»): таке речення поглинало б текст аж до наступного рядка з `from '…'`.
_IMPORT = re.compile(r"^import\s+(?:['\"]|(?:type\s+)?(?:\{|\*\s+as\s|[\w$]+\s*(?:,|\s+from\b|$)))")
_WORD_IMPORT = re.compile(r"^(?:import|export)\s")
_FROM = re.compile(r"\bfrom\s+['\"][^'\"]+['\"];?\s*$|^import\s+['\"][^'\"]+['\"];?\s*$")


def _imports_out(text: str) -> str:
    """Імпорти MDX верхнього рівня, і багаторядкові теж; код у блоках не чіпається.

    `mdx_statements_out` знімає рядок, що починається з `import`, а імпорт на кількох рядках
    («import {», далі по імені в рядку, «} from '@/src/components/frameworks'») лишав у тексті
    сирий перелік компонентів."""
    out, fence, open_import = [], "", False
    for line in text.split("\n"):
        f = _FENCE.match(line)
        if fence:
            if f and f.group(1) == fence:
                fence = ""
            out.append(line)
            continue
        if open_import:
            open_import = not _FROM.search(line)
            continue
        if _IMPORT.match(line):
            open_import = not _FROM.search(line)
            continue
        if _WORD_IMPORT.match(line) and out and out[-1].strip():
            # Речення абзацу, що почалося словом «import» з нового рядка: спільний
            # `mdx_statements_out` викинув би його як оператор, тож воно приєднується до
            # попереднього рядка того самого абзацу.
            out[-1] += " " + line
            continue
        if f:
            fence = f.group(1)
        out.append(line)
    return "\n".join(out)


def _rework(text: str) -> str:
    """Текст MDX сайту nuqs без дублів для двох читачів і без розмітки підсвічування."""
    text = _imports_out(text)
    def pair(m):
        if m.group(1) == m.group(3):
            return m.group(0)
        return m.group(2) if m.group(1) == "LLMContent" else m.group(4)
    text = _PAIR.sub(pair, text)
    text = _SOLO.sub("", _SUSPENSE.sub("", text))
    text = _SINCE.sub(lambda m: f"Introduced in nuqs {m.group(1)}.", text)
    text = _INLINE_LANG.sub(r"\1`", text)
    text = _SHIKI_LINE.sub("", text)
    return _SHIKI_TAIL.sub("", text)


class _Ctx:
    """Той самий контекст завантаження, лише текст файлів `.mdx` проходить `_rework`."""

    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        return _rework(text) if url.split("?", 1)[0].endswith(".mdx") else text


@register("ghdocs-history-nuqs")
def ghdocs_history_nuqs(source: dict, ctx):
    return ghdocs_history(source, _Ctx(ctx))
