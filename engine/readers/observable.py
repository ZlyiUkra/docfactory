"""Читач зошитів Observable: збірки власника і зошити в них, через відкритий API сайту.

`observable-collections` — `url` — перелік збірок власника
                           (https://api.observablehq.com/collections/@ВЛАСНИК). Кожна збірка
                           (…/collection/@ВЛАСНИК/СЛАГ) дає свої зошити, а кожен зошит
                           (…/document/@ВЛАСНИК/СЛАГ) стає документом. Необов'язкові:
                           `label` — підпис перед назвою («D3 notebook» → «D3 notebook: Bar
                           Chart»), `notebooks` — шляхи зошитів поза збірками («@d3/d3-fcumsum»),
                           на які посилається документація, `skip` — вираз шляхів, що не беруться.

Навіщо. Приклади D3 — галерея графіків, підручник «Learn D3», приклад до кожної функції
довідника — живуть не в репозиторії, а в зошитах Observable: d3js.org посилається на них
рядком «Examples» біля кожного методу. Зошит — це послідовність комірок: текст markdown і
код JavaScript, який малює графік. Сайт показує результат, а API віддає самі комірки (JSON):
їх і бере читач. Комірка тексту лишається markdown, комірка коду стає огорожею ```js, тож
пошук бачить і пояснення, і повний код прикладу.

Що прибирається з тексту комірок: блоки `<style>` (оформлення сторінки зошита) і багаторядкові
вставки `${…}` — у тексті зошита це код, що малює прев'ю чи віджет (галерея вставляє так
сотні рядків опису мініатюр). Однорядкові вставки (`${tex`…`}`, `${count}`) лишаються: вони
коротко кажуть, що там стоїть.

Документ без номера версії: зошит не прив'язаний до релізу D3, а версію бібліотеки, з якою
він працює, видно з його коду (`d3 = require("d3@7")`) або це поточна. Рядок «Collections:»
на початку називає збірки, куди зошит входить (d3-shape, Gallery…), а «Updated:» — день
останньої публікації.

Чому окремий модуль: інших читачів цього сайту немає, а спільні вже звірено в готових
примірниках.
"""

import json
import re
from urllib.parse import quote

from engine.readers import Item, _markup, register

_API = "https://api.observablehq.com"
_SITE = "https://observablehq.com"
_STYLE = re.compile(r"<style\b.*?</style>", re.S | re.I)
_MD_TAG = re.compile(r"md`(.*)`", re.S)


def _interpolations_out(text: str) -> str:
    """Багаторядкові `${…}` геть; дужки рахуються, бо в коді вставки є свої `{}`."""
    out, i = [], 0
    while True:
        j = text.find("${", i)
        if j < 0:
            out.append(text[i:])
            return "".join(out)
        depth, k = 0, j + 1
        while k < len(text):
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        chunk = text[j:k + 1]
        out.append(text[i:j])
        if "\n" not in chunk:
            out.append(chunk)
        i = k + 1


def _body(doc: dict, collections: list) -> str:
    parts = []
    if collections:
        parts.append(f"Collections: {', '.join(collections)}.")
    day = (doc.get("publish_time") or doc.get("update_time") or "")[:10]
    if day:
        parts.append(f"Updated: {day}.")
    for node in doc.get("nodes") or []:
        value = (node.get("value") or "").strip()
        if not value:
            continue
        mode = node.get("mode") or "js"
        # Старі зошити (до 2021 року) пишуть текст комірками коду md`…`: це той самий markdown.
        tagged = _MD_TAG.fullmatch(value) if mode == "js" else None
        if tagged:
            mode, value = "md", tagged.group(1).replace("\\`", "`")
        if mode == "md":
            text = _interpolations_out(_STYLE.sub("", value)).strip()
            if text:
                parts.append(_markup.markdown_body(text))
        else:
            fence = "```" + ("js" if mode == "js" else mode)
            parts.append(f"{fence}\n{value}\n```")
    return "\n\n".join(p for p in parts if p.strip())


@register("observable-collections")
def observable_collections(source: dict, ctx) -> list[Item]:
    m = re.fullmatch(re.escape(_API) + r"/collections/@([\w-]+)", source["url"])
    if not m:
        raise SystemExit(f"{source['id']}: читач observable-collections чекає адресу "
                         f"{_API}/collections/@ВЛАСНИК.")
    owner = m.group(1)
    skip = re.compile(source["skip"]) if source.get("skip") else None
    # Шлях зошита → назви збірок, де він стоїть; порядок — як у збірках.
    found: dict[str, list] = {}
    for col in json.loads(ctx.text(source["url"])):
        url = f"{_API}/collection/@{owner}/{quote(col['slug'])}"
        if not ctx.allowed(url):
            continue
        for entry in json.loads(ctx.text(url)).get("listings") or []:
            if entry.get("listing_type") != "notebook":
                continue
            path = f"@{entry['owner']['login']}/{entry['slug']}"
            found.setdefault(path, []).append(col.get("title") or col["slug"])
    for path in source.get("notebooks") or []:
        found.setdefault(path, [])
    items = []
    for path, cols in found.items():
        url = f"{_API}/document/{path}"
        if (skip and skip.search(path)) or not ctx.allowed(url):
            continue
        name = _markup.slug(path.split("/", 1)[1])

        def make(url=url, path=path, cols=cols):
            doc = json.loads(ctx.text(url))
            if doc.get("trashed"):
                raise SystemExit(f"{url}: зошит у кошику")
            title = " ".join((doc.get("title") or "").split())
            if source.get("label") and title:
                title = f"{source['label']}: {title}"
            body = _body(doc, cols)
            _markup.require(title, body, url)
            return _markup.document(title, f"{_SITE}/{path}", ctx.stamp, body)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    if not items:
        raise SystemExit(f"{source['url']}: у збірках не знайдено жодного дозволеного зошита.")
    return items
