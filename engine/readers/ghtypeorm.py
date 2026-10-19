"""Читач історії документації TypeORM: плоскі сторінки docs/*.md і сайт Docusaurus з власними вкладками.

`ghdocs-history-typeorm` — те саме, що `ghdocs-history` (усі його поля), плюс перед розбором кожна
                           сторінка `.md`/`.mdx` проходить заміни:
                           - імпорт MDX на кількох рядках (`import {` … `} from "@site/…"`) стає одним
                             рядком, і його знімають так само, як однорядковий;
                           - `custom_tabs` — `{"container": "DatabaseTabs", "item": "DatabaseTab",
                             "labels": {значення → підпис}}`: рядки `<DatabaseTabs>` і `</DatabaseTabs>`
                             стають `<Tabs>` і `</Tabs>`, `<DatabaseTab value="postgres">` —
                             `<TabItem value="postgres" label="PostgreSQL">`, `</DatabaseTab>` —
                             `</TabItem>`; підписи далі ставить звичне поле `docusaurus_tabs: true`;
                           - `drop_toc: true` — зміст сторінки (перелік посилань на її ж якорі одразу
                             під назвою, `* [Entity columns](#entity-columns)`) знімається.

Навіщо. Сайт typeorm.io з 1.0 показує те, що в кожної бази даних своє (рівні ізоляції транзакцій,
план запиту, індекси), вкладками власного компонента `<DatabaseTabs>`: назва бази — картинка, а
підпис береться з `docs/src/constants/databases.ts`. `docusaurus_tabs` знає лише `<Tabs>` і
`<TabItem>`, тож без заміни теги зникали б разом з назвою бази, і рівні ізоляції CockroachDB,
MySQL і SQLite стояли б в одному розділі підряд без жодного слова, чиї вони. Ті самі сторінки
імпортують компонент на чотирьох рядках: `_markup` знімає лише однорядковий імпорт, і хвіст
ставав першим рядком тексту, справжній заголовок — розділом, а назвою документа — ім'я файла.

Плоскі сторінки 0.1–0.3.24 починаються змістом — переліком посилань на свої ж розділи (у
`entities.md` 0.3.24 — 25 пунктів). Сайт Docusaurus будує зміст сам, збоку, а в корпусі такий
перелік ставав вступом документа: короткий фрагмент з назвами всіх розділів сторінки, який пошук
по словах ставив вище за самі розділи. Посилання на якорі деінде на сторінці (не одразу під
назвою) лишаються: там вони частина тексту.

Чому окремий модуль, а не поле в `ghdocs-history`: примірники з тим читачем зібрані й звірені, а
правка спільного читача — ризик зсуву в готовій роботі. Розбір той самий — його й викликано;
заміни робить обгортка контексту, через яку читач бере текст сторінки.
"""

import re

from engine.readers import register
from engine.readers.ghhistory import ghdocs_history

_RAW_PAGE = re.compile(r"^https://raw\.githubusercontent\.com/[^/]+/[^/]+/[^/]+/.+\.mdx?$")
_FENCE = re.compile(r"^\s*(```|~~~)")
_IMPORT_OPEN = re.compile(r"^import\s*\{[^}]*$")
_IMPORT_CLOSE = re.compile(r"^\s*\}\s*from\s*[\"'][^\"']+[\"']\s*;?\s*$")
_TITLE = re.compile(r"^#\s+\S")
_TOC_ITEM = re.compile(r"^\s*[-*+]\s+\[[^\]]*\]\(#[^)]*\)\s*$")


def _join_imports(text: str) -> str:
    """Імпорт верхнього рівня на кількох рядках → один рядок; код у блоках не чіпається."""
    out: list = []
    fence, pending = False, []
    for line in text.split("\n"):
        if pending:
            pending.append(line.strip())
            if _IMPORT_CLOSE.match(line):
                out.append(" ".join(pending))
                pending = []
            continue
        if _FENCE.match(line):
            fence = not fence
        elif not fence and _IMPORT_OPEN.match(line):
            pending = [line.strip()]
            continue
        out.append(line)
    return "\n".join(out + pending)


def _drop_toc(text: str) -> str:
    """Перелік посилань на якорі сторінки одразу під її назвою «# …» → нічого."""
    lines = text.split("\n")
    title = next((i for i, ln in enumerate(lines) if _TITLE.match(ln)), None)
    if title is None:
        return text
    start = title + 1
    while start < len(lines) and not lines[start].strip():
        start += 1
    end = start
    while end < len(lines) and _TOC_ITEM.match(lines[end]):
        end += 1
    return "\n".join(lines[:start] + lines[end:]) if end > start else text


def _tab_rules(spec: dict) -> list:
    container, item = re.escape(spec["container"]), re.escape(spec["item"])
    labels = dict(spec.get("labels") or {})

    def open_item(m):
        label = labels.get(m.group(2), m.group(2)).replace('"', "'")
        return f'{m.group(1)}<TabItem value="{m.group(2)}" label="{label}">'

    return [
        (re.compile(rf"^([ \t]*)<{container}>[ \t]*$", re.M), r"\1<Tabs>"),
        (re.compile(rf"^([ \t]*)</{container}>[ \t]*$", re.M), r"\1</Tabs>"),
        (re.compile(rf"^([ \t]*)<{item}\s+value=[\"']([^\"']+)[\"']\s*>[ \t]*$", re.M), open_item),
        (re.compile(rf"^([ \t]*)</{item}>[ \t]*$", re.M), r"\1</TabItem>"),
    ]


class _TypeORM:
    """Обгортка контексту: сторінки віддає вже після замін, усе інше (дерева тегів) — як є."""

    def __init__(self, ctx, rules: list, toc: bool):
        self._ctx = ctx
        self._rules = rules
        self._toc = toc

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, gzip: bool = False, accept: str = "") -> str:
        text = self._ctx.text(url, gzip, accept)
        if not _RAW_PAGE.match(url):
            return text
        text = _join_imports(text.replace("\r\n", "\n"))
        for rx, repl in self._rules:
            text = rx.sub(repl, text)
        return _drop_toc(text) if self._toc else text


@register("ghdocs-history-typeorm")
def ghdocs_history_typeorm(source: dict, ctx) -> list:
    spec = source.get("custom_tabs")
    if spec is not None and (not isinstance(spec, dict) or not spec.get("container")
                             or not spec.get("item")):
        raise SystemExit(f"{source['id']}: поле custom_tabs — {{\"container\": …, \"item\": …, "
                         f"\"labels\": {{…}}}}.")
    rules = _tab_rules(spec) if spec else []
    return ghdocs_history(source, _TypeORM(ctx, rules, source.get("drop_toc") is True))
