"""Читач історії файлів Protocol Buffers: як `ghcode-history-ts`, але розділи — повідомлення протоколу.

`ghcode-history-proto` — файли `.proto` з багатьох тегів (чи комітів) одного репозиторію разом. Поля ті
                         самі, що в `ghcode-history-ts`: `url` — префікс дерев через API
                         (…/repos/ВЛАСНИК/РЕПО/git/trees/), `tags` — об'єкт «тег або коміт → версія»
                         від найновішого, `include` — вирази шляхів, що беруться; необов'язкові
                         `exclude` і `name_prefix`.

Навіщо окремий читач. OTLP описано не текстом, а файлами `.proto`: що означає поле
`Span.start_time_unix_nano`, коли `Exemplar` має `span_id`, які значення в `StatusCode` — усе це
коментарі над повідомленнями й полями. Цілий `metrics.proto` (понад 30 тисяч символів) одним блоком
коду — один фрагмент, і вектор бачить лише його початок. Тут кожне `message`, `enum`, `service` (і
вкладене повідомлення) стає розділом з коментарем, що стоїть над ним, тож «HistogramDataPoint» —
окремий розділ зі своїм описом полів, а злиття однакових фрагментів між редакціями
(`revision_suffix`) лишає кожному повідомленню версії, у яких воно було таким.

Документ — неповторна пара «шлях, вміст» (хеш blob із дерева), у версії лягають усі теги, де файл
лежав саме таким; адреса в шапці — blob на найновішому з них.
"""

import json
import re
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
_MAX_FILE = 200_000
_DECL = re.compile(r"^( *)(message|enum|service|extend)\s+([\w.]+)\s*\{")
_COMMENT = re.compile(r"^\s*(?://|/\*|\*)")


def _outline(text: str) -> str:
    """Тіло з розділами: заголовок на кожному повідомленні, під ним — блок коду до наступного.
    Коментар упритул над оголошенням іде в його розділ."""
    lines = text.rstrip().split("\n")
    parts: list = [["", []]]
    pending: list = []
    for line in lines:
        m = _DECL.match(line)
        if m and len(m[1]) <= 6:
            parts.append([f"{'#' * min(2 + len(m[1]) // 2, 6)} {m[2]} {m[3]}", pending + [line]])
            pending = []
            continue
        if _COMMENT.match(line):
            pending.append(line)
            continue
        if pending:
            parts[-1][1].extend(pending)
            pending = []
        parts[-1][1].append(line)
    parts[-1][1].extend(pending)
    out = []
    for heading, body in parts:
        code = "\n".join(body).strip("\n")
        if not code.strip():
            continue
        if heading:
            out.append(heading)
        out.append(f"```protobuf\n{code}\n```")
    return "\n\n".join(out)


@register("ghcode-history-proto")
def ghcode_history_proto(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/.")
    owner, repo = m.groups()
    tags = source.get("tags")
    if not isinstance(tags, dict) or not tags:
        raise SystemExit(f"{source['id']}: поле `tags` — об'єкт «тег → версія».")
    include = [re.compile(x) for x in source.get("include") or ()]
    if not include:
        raise SystemExit(f"{source['id']}: поле `include` — вирази шляхів, що беруться.")
    exclude = [re.compile(x) for x in source.get("exclude") or ()]
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""

    seen: dict = {}
    for tag in tags:
        url = f"{source['url']}{quote(tag, safe='@')}?recursive=1"
        try:
            tree = json.loads(ctx.text(url))
        except ValueError as exc:
            raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
        if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
            raise SystemExit(f"{url}: у відповіді немає дерева файлів.")
        if tree.get("truncated"):
            raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
        for entry in tree["tree"]:
            path = entry.get("path", "")
            if (entry.get("type") == "blob" and 0 < entry.get("size", 1) <= _MAX_FILE
                    and any(r.search(path) for r in include)
                    and not any(r.search(path) for r in exclude)):
                name = f"{lead}{_markup.slug(path)}-{entry['sha'][:8]}"
                seen.setdefault(name, [path, []])[1].append(tag)

    order = {t: i for i, t in enumerate(tags)}
    items = []
    for name, (path, found) in seen.items():
        found = sorted(set(found), key=order.get)
        where = f"{owner}/{repo}/{quote(found[0], safe='@')}/{quote(path)}"
        raw = f"https://raw.githubusercontent.com/{where}"
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{where.split('/', 2)[2]}"
        version = ", ".join(dict.fromkeys(tags[t] for t in found))

        def make(path=path, raw=raw, blob=blob, version=version):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            title = f"{repo}: {path}"
            body = _outline(text)
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодного файла за `include` на жодному з "
                         f"{len(tags)} тегів.")
    return items
