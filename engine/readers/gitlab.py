"""Читач історії документації проєкту на GitLab: один документ на кожен неповторний текст файла з багатьох тегів.

`gitlab-history` — `url`     — API проєкту GitLab за числовим id (…/api/v4/projects/14/): у формі
                               ВЛАСНИК%2FРЕПО білий список розкодовує %2F і адреси не впізнає;
                   `raw`     — префікс сирих файлів (…/ВЛАСНИК/РЕПО/-/raw/);
                   `blob`    — префікс людських адрес (…/ВЛАСНИК/РЕПО/-/blob/);
                   `tags`    — об'єкт «тег → версія», від найновішого;
                   `folders` — теки, файли яких беруться, без вкладених («utils», «» — корінь);
                   `match`   — вираз імен файлів (типово markdown і сторінки man `.1`–`.8`).
                   Необов'язкові: `exclude` — вирази шляхів, що не беруться; `name_prefix` — рядок перед
                   іменем документа; `label` — підпис перед назвою документа; `roff_match` і `substitute` —
                   як у `ghdocs-history-roff`.

Навіщо. Poppler живе на gitlab.freedesktop.org, і дзеркала на GitHub у нього немає, а спільні читачі історії
тегів (`ghdocs-history` і його обгортки) знають лише дерева й сирі файли GitHub. Сторінки man утиліт
(`utils/pdftoppm.1`, `pdftotext.1`, `pdfinfo.1` …) лежать у репозиторії файлами roff, і саме вони — повний опис
параметрів кожного випуску.

Одиниця та сама, що в `ghdocs-history`: пара «шлях, вміст» (вміст упізнається id blob з дерева тегу) стає одним
документом, а в його версії лягають усі теги, де файл був саме таким. Тягнеться кожен текст один раз — з
найновішого тегу, де він такий. Дерево береться лише з названих тек і без вкладених: повне рекурсивне дерево
GitLab віддає сторінками по сотні записів, і на кожен тег це були б десятки запитів.
"""

import json
import re
from urllib.parse import quote

from engine.readers import Item, _markup, _mdoc, register
from engine.readers.ghhistory import _split_title
from engine.readers.manpages import to_markdown

_ROFF = re.compile(r"\.[1-8][a-z]?$")
_MATCH = r"\.(md|[1-8])$"


def _tree(ctx, api: str, folder: str, ref: str) -> list[dict]:
    out, page = [], 1
    while True:
        url = (f"{api}repository/tree?path={quote(folder, safe='')}&ref={quote(ref, safe='')}"
               f"&per_page=100&page={page}")
        code, data = ctx.fetch(url)
        if code.endswith("404"):
            # Теки в цьому тезі ще немає (utils/ з'явилася в poppler 0.5): тег просто нічого не дає.
            return out
        if code != "200":
            raise SystemExit(f"{url}: HTTP {code} — перелік не складено.")
        try:
            batch = json.loads(data.decode("utf-8"))
        except ValueError as exc:
            raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
        if not isinstance(batch, list):
            raise SystemExit(f"{url}: у відповіді немає переліку файлів.")
        out += batch
        if len(batch) < 100:
            return out
        page += 1


@register("gitlab-history")
def gitlab_history(source: dict, ctx) -> list[Item]:
    need = ("raw", "blob", "tags", "folders")
    if any(not source.get(k) and source.get(k) != [""] for k in need):
        raise SystemExit(f"{source['id']}: читач gitlab-history потребує полів {', '.join(need)}.")
    api = source["url"].rstrip("/") + "/"
    raw, blob = source["raw"].rstrip("/") + "/", source["blob"].rstrip("/") + "/"
    tags = source["tags"]
    match = re.compile(source.get("match") or _MATCH)
    roff = re.compile(source["roff_match"]) if source.get("roff_match") else _ROFF
    subst = [tuple(p) for p in source.get("substitute") or ()]
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""
    label = source.get("label", "")

    # ім'я документа → [шлях, [теги]]; порядок — від найновішого тегу
    seen: dict = {}
    for tag in tags:
        for folder in source["folders"]:
            for e in _tree(ctx, api, folder.strip("/"), tag):
                path = e.get("path", "")
                if (e.get("type") != "blob" or not match.search(e.get("name", ""))
                        or any(r.search(path) for r in exclude)):
                    continue
                stem = re.sub(r"\.md$", "", path)
                name = f"{lead}{_markup.slug(stem)}-{e['id'][:8]}"
                seen.setdefault(name, [path, []])[1].append(tag)
    if not seen:
        raise SystemExit(f"{source['id']}: у теках {', '.join(source['folders'])} жодного файла "
                         f"на жодному з {len(tags)} тегів.")

    items = []
    for name, (path, found) in seen.items():
        tag = found[0]
        url = f"{raw}{quote(tag, safe='')}/{quote(path)}"
        if not ctx.allowed(url):
            continue
        cite = f"{blob}{quote(tag, safe='')}/{quote(path)}"
        version = ", ".join(dict.fromkeys(str(tags[t]) for t in found))

        def make(url=url, cite=cite, path=path, version=version):
            text = ctx.text(url)
            _markup.refuse_html(text, url)
            if roff.search(path):
                for old, new in subst:
                    text = text.replace(old, new)
                title, body = (_mdoc.to_markdown if _mdoc.is_mdoc(text) else to_markdown)(text)
            elif path.endswith(".md"):
                meta, rest = _markup.front_matter(text)
                title = (meta or {}).get("title", "")
                if not title:
                    title, rest = _split_title(rest)
                body = _markup.markdown_body(rest)
            else:
                title = path.rsplit("/", 1)[-1]
                body = "```\n" + text.strip("\n") + "\n```"
            title = title or path.rsplit("/", 1)[-1]
            if label and label.lower() not in title.lower():
                title = f"{label}: {title}"
            _markup.require(title, body, url)
            return _markup.document(title, cite, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    return items
