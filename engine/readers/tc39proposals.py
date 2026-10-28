"""Читач `tc39-finished` — таблиця завершених пропозицій TC39 (tc39/proposals,
finished-proposals.md і ecma402/finished-proposals.md).

Пропозиція, що дійшла до stage 4, входить у редакцію року, названого в стовпці
«Expected Publication Year». Таблиця — пряма відповідь на питання «з якої редакції
це є», якої текст самої специфікації не дає: розділ кожної редакції каже, що в ній
є, а не з якого року.

Документ ділиться за роками («## ECMAScript 2016»), а в межах року кожна пропозиція —
окремим заголовком: пошук за назвою пропозиції знаходить саме її рядок. Посилання
таблиці (за посиланням-міткою «[text][ref]») стають адресою репозиторію пропозиції;
стовпець нотаток зустрічей зводиться до дат зустрічей.
"""

import html as html_lib
import re

from engine.readers import Item, register

_REF_DEF = re.compile(r"^\[([^\]]+)\]:\s*(\S+)", re.M)
_REF_LINK = re.compile(r"\[([^\]]*)\]\[([^\]]*)\]")
_INLINE_LINK = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")


def _cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def _plain(cell: str) -> str:
    """Текст клітинки: посилання — своїм текстом, теги — геть, <br> — кома."""
    cell = re.sub(r"<br\s*/?>", ", ", cell)
    cell = _REF_LINK.sub(r"\1", cell)
    cell = _INLINE_LINK.sub(r"\1", cell)
    cell = re.sub(r"<[^>]+>", " ", cell)
    cell = html_lib.unescape(cell).replace("‑", "-").replace("`", "")
    cell = re.sub(r"\s*,\s*(,\s*)*", ", ", cell)
    return " ".join(cell.split()).strip(" ,-")


def _render(text: str, edition: str) -> str:
    refs = {k.lower(): v for k, v in _REF_DEF.findall(text)}
    rows = [ln for ln in text.splitlines() if ln.startswith("|")]
    if len(rows) < 3:
        raise SystemExit("У finished-proposals.md не знайдено таблиці — розмітка змінилася, "
                         "читача треба поправити.")
    head = [_plain(c).lower() for c in _cells(rows[0])]

    def col(name: str) -> int:
        for i, h in enumerate(head):
            if h.startswith(name):
                return i
        raise SystemExit(f"У таблиці немає стовпця «{name}» — розмітка змінилася.")

    c_name, c_author, c_champ = col("proposal"), col("author"), col("champion")
    c_notes, c_year = col("meeting notes"), col("expected publication year")
    by_year: dict[str, list[str]] = {}
    for row in rows[2:]:
        cells = _cells(row)
        if len(cells) < len(head):
            continue
        raw_name = cells[c_name]
        link = _REF_LINK.search(raw_name)
        url = refs.get(link.group(2).lower(), "") if link else ""
        name = _plain(raw_name)
        year = _plain(cells[c_year]) or "year not set"
        dates = list(dict.fromkeys(re.findall(r"\d{4}-\d{2}", _plain(cells[c_notes]))))
        lines = [f"### {name}", "",
                 f"{name} is a finished (stage 4) proposal included in {edition} {year}."]
        lines.append(f"Author: {_plain(cells[c_author])}. "
                     f"Champion(s): {_plain(cells[c_champ])}.")
        if url:
            lines.append(f"Proposal repository: {url}")
        if dates:
            lines.append(f"TC39 meetings: {', '.join(dates)}.")
        by_year.setdefault(year, []).append("\n".join(lines))
    out = []
    for year in sorted(by_year, reverse=True):
        out.append(f"## {edition} {year}")
        out.extend(by_year[year])
    return "\n\n".join(out)


@register("tc39-finished")
def tc39_finished(source: dict, ctx) -> list[Item]:
    """Поля: `url` — сирий finished-proposals.md; `edition` — як таблиця називає
    редакцію («ECMAScript», «ECMAScript Internationalization API»)."""
    url = source["url"]
    title = source.get("title", source["id"])
    edition = source.get("edition") or "ECMAScript"

    def make():
        body = _render(ctx.text(url), edition)
        return f"# {title}\n# джерело: {url}\n# отримано: {ctx.stamp}\n\n{body}\n"

    return [Item(id=source["id"], file=f"{source['id']}.txt", make=make)]
