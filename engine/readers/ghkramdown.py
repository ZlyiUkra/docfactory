"""Читач історії документації .NET-репозиторіїв, яку збирають Jekyll (kramdown) чи DocFX.

`ghdocs-history-kramdown` — те саме, що `ghdocs-history` (усі його поля), плюс перед розбором
                            кожна сторінка `.md`/`.markdown` проходить кілька замін поза
                            блоками коду:
                            - списки атрибутів kramdown (`{: .issue-link }`, `{:.no_toc}`) і
                              якорі заголовків (`## Class Fixtures{ #class-fixture }`)
                              зникають — сайт робить з них класи CSS і якорі, а не текст; зміст
                              сторінки («* TOC» над `{:toc}`) теж;
                            - блок `{% examplecode csharp %}` … `{% endexamplecode %}` стає
                              блоком коду цієї мови, а прихований код-заготовка
                              `{% requiredcode %}` … `{% endrequiredcode %}` зникає разом зі
                              змістом (так сайт NSubstitute 1.x–2.x перевіряв приклади й не
                              показував заготовку); позначки `{% raw %}`/`{% endraw %}` зникають;
                            - виноска `> [!NOTE]` (DocFX, GitHub) стає `> Note:`;
                            - службові рядки mdsnippets навколо вставленого прикладу
                              (`<a id='snippet-…'></a>` і `<sup>…snippet source…</sup>`) зникають;
                            - `jekyll_data` — тека даних сайту Jekyll у репозиторії («docs/_data»):
                              вставка `{% include assertion-comparison.html … caption="…"
                              examples=site.data.tips.collections %}` (сторінка порад
                              fluentassertions.com) стає розділом «### Назва» з кожним прикладом —
                              код «як було» і «як краще» та обидва повідомлення про збій — з файла
                              `docs/_data/tips/collections.yml` того самого тегу.

Навіщо. Сайти бібліотек тестування .NET живуть markdown-ом у репозиторіях, але кожен зі своїм
генератором: xunit.net (DocFX) ставить після посилань на задачі `{: .issue-link }` — 244 рази в
нотатках випусків; сторінки NSubstitute 1.x–2.x загортають кожен приклад у тег Liquid
`examplecode`, і без заміни код ставав звичайним абзацом; документація Shouldly — вставки
mdsnippets, де під кожним прикладом стоїть рядок «snippet source | anchor». Сторінка порад
FluentAssertions — лише вісім рядків-вставок, а самі поради (понад сотню пар «як було — як
краще») лежать у YAML; без розгортання сторінка в корпусі була б порожньою.

Редакція сторінки — як у `ghdocs-history`: пара «шлях, вміст» самої сторінки. Дані вставки
беруться з того тегу, з якого береться сторінка (найновішого, де вона була саме такою).

Чому окремий модуль, а не поле в `ghdocs-history`: примірники з тим читачем зібрані й звірені,
а правка спільного читача — ризик зсуву в готовій роботі. Розбір той самий — його й викликано;
заміни робить обгортка контексту, через яку читач бере текст сторінки (як `ghdocs-history-jekyll`).
"""

import re

from engine.readers import register
from engine.readers.docfx import yaml_load
from engine.readers.ghhistory import ghdocs_history

_RAW_PAGE = re.compile(r"^https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)/(.+\.(?:md|markdown))$")
_FENCE = re.compile(r"^\s*(```+|~~~+)")
_IAL = re.compile(r"[ \t]*\{:[^}\n]*\}")
# Атрибути заголовка markdig/kramdown у кінці рядка «## Class Fixtures{ #class-fixture }» — якір, а не назва.
_HEADING_ID = re.compile(r"^(#{1,6}[ \t]+.*?)[ \t]*\{[ \t]*#[\w.:-]+(?:[ \t]+[.#][\w.:-]+)*[ \t]*\}[ \t]*$")
_EXAMPLE = re.compile(r"^\s*\{%\s*examplecode\s+([\w+#-]+)\s*%\}\s*$")
_EXAMPLE_END = re.compile(r"^\s*\{%\s*endexamplecode\s*%\}\s*$")
_REQUIRED = re.compile(r"\{%\s*requiredcode\s*%\}.*?\{%\s*endrequiredcode\s*%\}[ \t]*\n?", re.S)
_RAW_TAG = re.compile(r"\{%\s*(?:raw|endraw)\s*%\}")
# Зміст сторінки kramdown: пункт «* TOC» з атрибутом `{:toc}` під ним — місце, куди сайт ставить
# перелік заголовків; у тексті він став би пунктом списку «TOC».
_TOC = re.compile(r"^[ \t]*[*-][ \t]+TOC[ \t]*\n[ \t]*\{:toc\}[ \t]*$\n?", re.M)
_ALERT = re.compile(r"^(\s*>\s*)\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]", re.I)
_SNIPPET_ANCHOR = re.compile(r"^\s*<a id='snippet-[^']*'></a>\s*$")
_SNIPPET_SOURCE = re.compile(r"^\s*<sup>.*snippet source.*</sup>\s*$", re.I)
_INCLUDE = re.compile(r"^\s*\{%\s*include\s+assertion-comparison\.html\b(.*?)%\}\s*$", re.M)
_ATTR = re.compile(r'([\w-]+)=(?:"([^"]*)"|(\S+))')


def _clean(text: str) -> str:
    text = _TOC.sub("", _REQUIRED.sub("", text.replace("\r\n", "\n")))
    out, fence = [], ""
    for ln in text.split("\n"):
        m = _FENCE.match(ln)
        if fence:
            out.append(ln)
            if m and ln.strip().startswith(fence[0] * len(fence)) and not ln.strip().strip(fence[0]):
                fence = ""
            continue
        if m:
            fence = m.group(1)
            out.append(ln)
            continue
        em = _EXAMPLE.match(ln)
        if em:
            out.append("```" + em.group(1))
            continue
        if _EXAMPLE_END.match(ln):
            out.append("```")
            continue
        if _SNIPPET_ANCHOR.match(ln) or _SNIPPET_SOURCE.match(ln):
            continue
        ln = _HEADING_ID.sub(r"\1", ln)
        ln = _ALERT.sub(lambda am: f"{am.group(1)}{am.group(2).capitalize()}:", ln)
        stripped = _IAL.sub("", ln)
        # Рядок, що весь був списком атрибутів, зникає зовсім, а не лишає порожнього рядка
        # посеред абзацу.
        if stripped.strip() or not ln.strip():
            out.append(stripped)
    return _RAW_TAG.sub("", "\n".join(out))


def _block(label: str, lang: str, code) -> list[str]:
    code = str(code or "").strip("\n")
    return [f"{label}:", "", f"```{lang}", code, "```", ""] if code.strip() else []


class _Kramdown:
    """Обгортка контексту: сторінки віддає вже очищеними, усе інше (дерева тегів) — як є."""

    def __init__(self, ctx, data_root: str):
        self._ctx = ctx
        self._data = data_root.strip("/")

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def _expand(self, text: str, base: str) -> str:
        def include(m):
            attrs = {a: b or c for a, b, c in _ATTR.findall(m.group(1))}
            data = attrs.get("examples", "")
            if not data.startswith("site.data."):
                return ""
            url = f"{base}{self._data}/{data[len('site.data.'):].replace('.', '/')}.yml"
            if not self._ctx.allowed(url):
                return ""
            # Сторінка буває, що називає файл даних, якого в цьому тезі ще немає (поради FluentAssertions 5.x–6.x
            # вставляють `tips.datetimes` раніше, ніж з'явився datetimes.yml): Jekyll тоді не малює нічого, і тут
            # вставка теж зникає, а не валить сторінку.
            code, data = self._ctx.fetch(url)
            if code != "200":
                return ""
            rows = yaml_load(data.decode("utf-8", errors="replace"))
            if not isinstance(rows, list):
                return ""
            left, right = attrs.get("header1", "Before"), attrs.get("header2", "After")
            lines = [f"### {attrs.get('caption', '')}".rstrip(), ""]
            for row in rows:
                if not isinstance(row, dict):
                    continue
                lines += _block(left, "csharp", row.get("old"))
                lines += _block(right, "csharp", row.get("new"))
                lines += _block(f"{left} failure message", "text", row.get("old-message"))
                lines += _block(f"{right} failure message", "text", row.get("new-message"))
            return "\n".join(lines)

        return _INCLUDE.sub(include, text)

    def text(self, url: str, gzip: bool = False, accept: str = "") -> str:
        text = self._ctx.text(url, gzip, accept)
        m = _RAW_PAGE.match(url)
        if not m:
            return text
        if self._data:
            owner, repo, tag, _ = m.groups()
            text = self._expand(text, f"https://raw.githubusercontent.com/{owner}/{repo}/{tag}/")
        return _clean(text)


@register("ghdocs-history-kramdown")
def ghdocs_history_kramdown(source: dict, ctx) -> list:
    return ghdocs_history(source, _Kramdown(ctx, str(source.get("jekyll_data") or "")))
