"""Читач тегів образу з API Docker Hub: огляд образу й документ на кожну лінію версій.

`dockerhub-tags` — `url` — перша сторінка переліку тегів
                   (https://hub.docker.com/v2/namespaces/ВЛАСНИК/repositories/ОБРАЗ/tags?page_size=100);
                   наступні сторінки — з поля `next` відповіді, і кожна мусить лежати в `within`.
                   `image` — назва образу для команд (`oven/bun`), `label` — назва в заголовках, `page` —
                   людська сторінка образу (на неї веде шапка документів). Необов'язкові: `line` — вираз
                   з групою `v`, що дістає лінію з номера версії (типово дві перші цифри: «1.4»),
                   `version_prefix` — рядок перед міткою лінії, `name_prefix` — початок імені документів.

Навіщо. Образ Bun на Docker Hub має сотні тегів: кожна версія в п'яти варіантах (без суфікса,
`-slim`, `-debian`, `-alpine`, `-distroless`) і плаваючі теги (`latest`, `1`, `1.4`, `canary`,
`alpine`), що щоразу переїжджають на новішу збірку. Котру версію зараз дає `1.4-alpine`, з якої
версії є варіант `distroless`, для яких архітектур зібрано образ — знає лише реєстр. `registry-tags`
читає протокол OCI, але реєстр Docker Hub без токена його не віддає (401), а дзеркало mirror.gcr.io
тримає лише частину тегів. API самого Docker Hub відкритий і дає більше: дату останньої публікації,
дайджест і архітектури кожного тега.

Тег, де за номером «1.2.3» стоїть суфікс, — версія у варіанті; тег без повного номера —
плаваючий: на що він указує, видно з дайджесту — у нього той самий, що й у тега повної версії
того ж варіанта. Порядок версій — за номером, а не за абеткою.
"""

import json
import re

from engine.readers import Item, _markup, register

_VERSION = re.compile(r"^(?P<num>\d+\.\d+\.\d+)(?:-(?P<variant>[a-z][\w.-]*))?$")


def _num(text: str) -> tuple:
    return tuple(int(x) for x in re.findall(r"\d+", text)) or (0,)


def _archs(entry: dict) -> str:
    seen = []
    for img in entry.get("images") or []:
        arch = "/".join(x for x in (img.get("architecture"), img.get("variant")) if x)
        if arch and arch not in seen and arch != "unknown":
            seen.append(arch)
    return ", ".join(sorted(seen)) or "—"


@register("dockerhub-tags")
def dockerhub_tags(source: dict, ctx) -> list[Item]:
    entries: dict = {}
    url = source["url"]
    while url:
        if not ctx.allowed(url):
            raise SystemExit(f"{url}: наступна сторінка тегів поза `within` — перелік був би неповним.")
        try:
            data = json.loads(ctx.text(url))
        except ValueError as exc:
            raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік тегів не складено.")
        for entry in data.get("results") or []:
            if isinstance(entry, dict) and entry.get("name"):
                entries[entry["name"]] = entry
        url = data.get("next")
    if not entries:
        raise SystemExit(f"{source['url']}: у відповіді немає тегів.")
    image = source.get("image") or ""
    label = source.get("label") or image
    page = source.get("page") or source["url"]
    line_rx = re.compile(source.get("line") or r"^(?P<v>\d+\.\d+)\.")
    prefix = source.get("version_prefix", "")

    # версія → варіант → запис тега; плаваючі — окремо
    versions: dict = {}
    floating = []
    for name, entry in entries.items():
        m = _VERSION.match(name)
        if m:
            versions.setdefault(m["num"], {})[m["variant"] or ""] = entry
        else:
            floating.append(name)
    lines: dict = {}
    for num in versions:
        m = line_rx.match(num)
        lines.setdefault(m["v"] if m else num, []).append(num)
    order = sorted(lines, key=_num)
    by_digest = {}
    for num in sorted(versions, key=_num):
        for variant, entry in versions[num].items():
            if entry.get("digest"):
                by_digest[entry["digest"]] = num + (f"-{variant}" if variant else "")

    def pushed(entry: dict) -> str:
        return (entry.get("tag_last_pushed") or entry.get("last_updated") or "")[:10] or "—"

    def variant_name(v: str) -> str:
        return f"`-{v}`" if v else "none (`<version>`)"

    def overview() -> str:
        variants = {}
        for num in versions:
            for v in versions[num]:
                variants.setdefault(v, []).append(num)
        out = [f"Image `{image}` on Docker Hub: {len(entries)} tags — {len(versions)} versions in "
               f"{len(order)} lines and {len(floating)} floating tags.", "",
               "A version tag is `<version>` or `<version>-<variant>`; a floating tag has no full version "
               "number and moves to a newer build with every release.", "",
               "## Variants", "", "| Variant | Versions | Oldest | Newest |", "|---|---|---|---|"]
        for v in sorted(variants, key=lambda x: (x != "", x)):
            nums = sorted(variants[v], key=_num)
            out.append(f"| {variant_name(v)} | {len(nums)} | {nums[0]} | {nums[-1]} |")
        out += ["", "## Floating tags", "",
                "| Tag | Points to | Last pushed | Architectures |", "|---|---|---|---|"]
        for name in sorted(floating, key=lambda t: (_num(t), t)):
            entry = entries[name]
            target = by_digest.get(entry.get("digest") or "", "—")
            out.append(f"| `{name}` | {('`' + target + '`') if target != '—' else '—'} | {pushed(entry)} | "
                       f"{_archs(entry)} |")
        out += ["", "## Lines", "", "| Line | Versions | Oldest | Newest | First pushed | Last pushed |",
                "|---|---|---|---|---|---|"]
        for v in order:
            nums = sorted(lines[v], key=_num)
            dates = sorted(pushed(e) for n in nums for e in versions[n].values() if pushed(e) != "—")
            out.append(f"| {v} | {len(nums)} | {nums[0]} | {nums[-1]} | {dates[0] if dates else '—'} | "
                       f"{dates[-1] if dates else '—'} |")
        return "\n".join(out)

    def line_doc(v: str) -> str:
        nums = sorted(lines[v], key=_num, reverse=True)
        out = [f"Image `{image}`, line {v}: {len(nums)} versions, {nums[-1]}–{nums[0]}.", "",
               f"Pull a version: `docker pull {image}:{nums[0]}`; a variant: "
               f"`docker pull {image}:{nums[0]}-<variant>`.", "",
               "| Version | Variants | Last pushed | Architectures |", "|---|---|---|---|"]
        for num in nums:
            own = versions[num]
            names = ", ".join(f"`{num}{('-' + x) if x else ''}`" for x in sorted(own, key=lambda x: (x != "", x)))
            base = own.get("") or next(iter(own.values()))
            out.append(f"| {num} | {names} | {pushed(base)} | {_archs(base)} |")
        moving = [n for n in floating if by_digest.get(entries[n].get("digest") or "", "").split("-")[0] in nums]
        if moving:
            out += ["", "## Floating tags pointing into this line", ""]
            out += [f"- `{n}` → `{by_digest[entries[n]['digest']]}`" for n in sorted(moving)]
        return "\n".join(out)

    slug = _markup.slug(source.get("name_prefix") or label)
    items = []

    def add(name, title, version, build):
        def make():
            body = build()
            _markup.require(title, body, page, min_chars=1)
            return _markup.document(title, page, ctx.stamp, _markup.markdown_body(body), version)
        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))

    add(f"{slug}-tags", f"{label}: Docker image tags", ", ".join(prefix + v for v in reversed(order)), overview)
    for v in order:
        add(f"{slug}-{_markup.slug(v)}", f"{label} {v}: Docker image tags", prefix + v, lambda v=v: line_doc(v))
    return items
