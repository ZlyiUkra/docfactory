"""Читачі каталогів astro.build: теми, вітрина сайтів, інтеграції.

`astro-catalog`      — посторінковий каталог сайту (`/themes/1/`, `/showcase/`):
                       кожна сторінка переліку стає документом. Перелік сторінок
                       береться з пагінації першої сторінки.
`astro-integrations` — каталог інтеграцій із `integrations.json` репозиторію сайту:
                       один документ на категорію.

Навіщо окремі читачі. Документація Astro лежить markdown-ом у репозиторії, і її
беруть звичайні читачі. Каталоги — ні: теми взагалі не зберігаються в репозиторії,
вони приходять із зовнішнього API під час збірки, тож єдине місце, де їх видно, —
готові сторінки сайту. Вітрина лежить у репозиторії, але трьома тисячами окремих
файлів YAML на три рядки кожен; тягнути три тисячі файлів заради трьох тисяч
назв — не те, за що варто платити годинами звернень до чужого сервера.

Чому сторінки переліку, а не сторінки окремих тем. У каталозі тем 62 сторінки по
18 тем, тобто близько 1100 окремих сторінок. Сторінка переліку вже несе назву,
повний опис, автора й ознаку «Free/Paid» кожної теми — усе, чим відповідають на
питання «які є теми й де їх узяти». Сторінка окремої теми додає до цього знімки
екрана та сторінку купівлі. Тому каталог береться переліками: 62 звернення проти
1100, а відповідь та сама.

Інтеграції, навпаки, мають машинне джерело — `src/content/integrations.json` у
репозиторії сайту, 1776 записів з описом, категоріями, адресами npm і репозиторію
та числом завантажень. Один документ на категорію: тринадцять документів замість
тисячі семисот, і кожен читається як довідка «що є для цієї задачі».
"""

import json
import re

from engine.readers import Item, _markup, register

_PAGE_LINK = re.compile(r'href="(/[a-z-]+/)(\d+)/"')
_MAIN = re.compile(r"<main\b.*?</main>", re.S)


def _page_text(html: str, skip: tuple[str, ...] = ()) -> str:
    """Текст сторінки каталогу: лише <main>, бо шапка й підвал сайту на кожній
    сторінці однакові, і в корпусі вони стали б тисячею копій меню.

    `skip` — назви розділів, які теж повторюються на кожній сторінці каталогу:
    панель фільтрів із переліком усіх категорій і технологій, заклик подати свою
    тему, гасло над переліком. Один раз це зміст, шістдесят два рази — шум, у
    якому запит про Svelte чи Tailwind влучає в бічну панель, а не в тему."""
    m = _MAIN.search(html)
    text = _markup.html_body(m.group(0) if m else html)
    if not skip:
        return text
    out, dropping = [], False
    for line in text.split("\n"):
        head = line.startswith("## ")
        if head:
            dropping = line[3:].strip() in skip
        if not dropping:
            out.append(line)
    return "\n".join(out).strip()


@register("astro-catalog")
def astro_catalog(source: dict, ctx) -> list[Item]:
    first = source["url"]
    html = ctx.text(first)
    # Скільки всього сторінок, каже сама пагінація першої. Межу беремо з неї, а не
    # вгадуємо: каталог росте, і зашите число мовчки обрізало б хвіст.
    base, last = "", 1
    for m in _PAGE_LINK.finditer(html):
        if source.get("path", "") in m.group(1):
            base, last = m.group(1), max(last, int(m.group(2)))
    if not base:
        raise SystemExit(f"{first}: пагінації не видно — сторінка каталогу змінилася, "
                         f"читача треба поправити.")
    limit = int(source.get("max_pages") or 0)
    if limit:
        last = min(last, limit)
    label = source.get("label", "Catalog")
    items = []
    for n in range(1, last + 1):
        # Перша сторінка вітрини живе без номера («/showcase/»), а перша сторінка тем —
        # із номером. Тому адреса першої береться з джерела, як її оголосили.
        url = first if n == 1 else f"https://astro.build{base}{n}/"
        if not ctx.allowed(url):
            continue

        skip = tuple(source.get("skip_sections") or ())

        def make(url=url, n=n, skip=skip):
            body = _page_text(ctx.text(url), skip)
            title = f"{label}, page {n} of {last}"
            _markup.require(title, body, url, min_chars=1)
            return _markup.document(title, url, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/page-{n}",
                          file=f"{source['id']}--page-{n:03d}.txt", make=make))
    return items


@register("astro-integrations")
def astro_integrations(source: dict, ctx) -> list[Item]:
    try:
        data = json.loads(ctx.text(source["url"]))
    except ValueError as exc:
        raise SystemExit(f"{source['url']}: відповідь не JSON ({exc}) — перелік не складено.")
    if not isinstance(data, list) or not data:
        raise SystemExit(f"{source['url']}: очікував непорожній список інтеграцій.")
    groups: dict[str, list] = {}
    for entry in data:
        if not isinstance(entry, dict) or not entry.get("id"):
            continue
        for cat in (entry.get("categories") or ["uncategorized"]):
            groups.setdefault(str(cat), []).append(entry)
    if not groups:
        raise SystemExit(f"{source['url']}: у жодного запису немає категорії.")
    cite = source.get("cite", "https://astro.build/integrations/")
    items = []
    for cat in sorted(groups):
        rows = sorted(groups[cat], key=lambda e: -int(e.get("downloads") or 0))

        def make(cat=cat, rows=rows):
            lines = [f"Astro integrations, category «{cat}»: {len(rows)} packages, "
                     f"most downloaded first.", ""]
            for e in rows:
                lines.append(f"## {e['id']}")
                lines.append("")
                if e.get("description"):
                    lines.append(str(e["description"]).strip())
                    lines.append("")
                where = [f"npm: {e['npmUrl']}" if e.get("npmUrl") else "",
                         f"repository: {e['repoUrl']}" if e.get("repoUrl") else "",
                         f"weekly downloads: {e['downloads']}" if e.get("downloads") else ""]
                tail = ", ".join(x for x in where if x)
                if tail:
                    lines += [tail, ""]
            body = "\n".join(lines).strip()
            title = f"Integrations: {cat}"
            _markup.require(title, body, source["url"], min_chars=1)
            return _markup.document(title, cite, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{_markup.slug(cat)}",
                          file=f"{source['id']}--{_markup.slug(cat)}.txt", make=make))
    return items
