"""Читач довідника API Ember з даних api.emberjs.com: документ на клас, простір імен чи модуль кожної версії.

`ember-api-json` — `url` — префікс дерев через API (…/repos/ember-learn/ember-api-docs-data/git/trees/), `tags` —
                   об'єкт з одним комітом репозиторію («SHA → ""»), `project` — тека проєкту в `json-docs/`
                   (`ember`, `ember-data`), `label` — назва проєкту в заголовках («Ember», «Ember Data»).
                   Необов'язкові: `version_prefix` — рядок перед міткою версії (Ember Data нумерується
                   окремо: «ember-data-5.4»), `name_prefix` — початок імені документів, `site` — адреса
                   проєкту на api.emberjs.com (`https://api.emberjs.com/ember`), `skip` — вираз тек версій,
                   що не беруться.

Навіщо. api.emberjs.com — застосунок, що читає JSON з репозиторію `ember-api-docs-data`: тека на кожну
версію (`json-docs/ember/6.4.0/`), у ній `classes/`, `namespaces/`, `modules/` — вивід YUIDoc у форматі
JSON:API. Готового тексту сторінки немає ніде, лише ці записи: опис класу, його методи, властивості й
події з параметрами, типами, `since` і позначкою `deprecated`.

Документ. Клас (простір імен) — шапка (модуль, батьківський клас, домішки, файл), опис, далі розділи
«Methods», «Properties», «Events» з підрозділом на кожен власний член класу: сигнатура з параметрами,
з якої версії є, чи застарілий, опис, параметри, що повертає. Успадковане від батьків і домішок — лише
перелік імен під назвою джерела (`inheritedFrom`): інакше методи `Observable` повторювалися б у кожному класі. Члени з
`access: private` не беруться — сайт їх теж ховає за замовчуванням. Модуль — опис і перелік класів.

Версія документа — лінія з імені теки («6.4.0» → «6.4»). Ім'я документа закінчується хешем версії, тож
`revision_suffix` зрізає його, і однакові розділи сусідніх версій зливаються в один фрагмент з усіма
версіями — як у читачах історії репозиторіїв.
"""

import hashlib
import json
import re
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
_VERSION_DIR = re.compile(r"^\d+\.\d+\.\d+$")
_KINDS = {"classes": "class", "namespaces": "namespace", "modules": "module"}


def _num(text: str) -> tuple:
    return tuple(int(x) for x in re.findall(r"\d+", text)) or (0,)


def _line(item: dict) -> str:
    """Рядок ознак члена класу: доступ, статичність, з якої версії, застарілість."""
    marks = []
    if item.get("access") and item["access"] != "public":
        marks.append(item["access"].capitalize())
    if item.get("static"):
        marks.append("Static")
    if item.get("since"):
        marks.append(f"Since {item['since']}")
    if item.get("deprecated"):
        why = (item.get("deprecationMessage") or "").strip()
        marks.append("Deprecated" + (f": {why}" if why else ""))
    return ". ".join(marks) + ("." if marks else "")


def _params(item: dict) -> list:
    out = []
    for p in item.get("params") or []:
        name = p.get("name", "")
        if p.get("optional"):
            name = f"[{name}" + (f"={p['optdefault']}" if p.get("optdefault") else "") + "]"
        typ = f" *{p['type']}*" if p.get("type") else ""
        desc = (p.get("description") or "").strip().replace("\n", " ")
        out.append(f"- `{name}`{typ}" + (f": {desc}" if desc else ""))
        for sub in p.get("props") or []:
            sdesc = (sub.get("description") or "").strip().replace("\n", " ")
            out.append(f"  - `{sub.get('name', '')}`" + (f" *{sub['type']}*" if sub.get("type") else "")
                       + (f": {sdesc}" if sdesc else ""))
    return out


def _member(item: dict, owner: str) -> str:
    kind = item.get("itemtype")
    name = item.get("name", "")
    if kind == "method":
        args = ", ".join(p.get("name", "") for p in item.get("params") or [])
        head = f"### {owner}.{name}({args})"
    else:
        head = f"### {owner}.{name}"
    out = [head, ""]
    if (marks := _line(item)):
        out += [marks, ""]
    if kind == "property":
        facts = []
        if item.get("type"):
            facts.append(f"Type: `{item['type']}`")
        if item.get("default") not in (None, ""):
            facts.append(f"Default: `{item['default']}`")
        if facts:
            out += [". ".join(facts) + ".", ""]
    if (desc := (item.get("description") or "").strip()):
        out += [desc, ""]
    if (params := _params(item)):
        out += ["Parameters:", "", *params, ""]
    ret = item.get("return") or {}
    if ret.get("type") or ret.get("description"):
        rdesc = (ret.get("description") or "").strip().replace("\n", " ")
        out += ["Returns: " + (f"*{ret['type']}*" if ret.get("type") else "") + (f" {rdesc}" if rdesc else ""), ""]
    return "\n".join(out).rstrip()


def _render(kind: str, attrs: dict, label: str) -> tuple[str, str]:
    """Назва й тіло документа markdown з атрибутів запису YUIDoc."""
    name = attrs.get("name") or attrs.get("shortname") or "?"
    title = f"{label} API: {name}" + ("" if kind == "class" else f" ({kind})")
    head = []
    if attrs.get("module") and kind != "module":
        head.append(f"Module: `{attrs['module']}`")
    if attrs.get("extends"):
        head.append(f"Extends: `{attrs['extends']}`")
    if attrs.get("uses"):
        head.append("Uses: " + ", ".join(f"`{u}`" for u in attrs["uses"]))
    if attrs.get("file"):
        head.append(f"Defined in `{attrs['file']}`" + (f":{attrs['line']}" if attrs.get("line") else ""))
    out = [" · ".join(head), ""] if head else []
    if (marks := _line(attrs)):
        out += [marks, ""]
    if (desc := (attrs.get("description") or "").strip()):
        out += [desc, ""]
    if kind == "module":
        for key, word in (("classes", "Classes"), ("namespaces", "Namespaces"), ("submodules", "Submodules")):
            names = attrs.get(key) or {}
            names = sorted(names) if isinstance(names, dict) else sorted(str(x) for x in names)
            if names:
                out += [f"## {word}", "", ", ".join(f"`{n}`" for n in names), ""]
        return title, "\n".join(out).strip()
    owner = name
    for key, word in (("methods", "Methods"), ("properties", "Properties"), ("events", "Events")):
        own, inherited = [], {}
        for item in attrs.get(key) or []:
            if not isinstance(item, dict) or item.get("access") == "private":
                continue
            src = item.get("inheritedFrom") or (item.get("class") if item.get("class") not in (None, "", name) else "")
            if item.get("inherited") or src:
                inherited.setdefault(src or "?", []).append(item.get("name", ""))
            else:
                own.append(item)
        if not own and not inherited:
            continue
        out += [f"## {word}", ""]
        for item in sorted(own, key=lambda x: x.get("name", "")):
            out += [_member(item, owner), ""]
        if inherited:
            out += [f"### Inherited {word.lower()}", ""]
            out += [f"- from `{src}`: " + ", ".join(f"`{n}`" for n in sorted(set(names)))
                    for src, names in sorted(inherited.items())]
            out.append("")
    return title, "\n".join(out).strip()


@register("ember-api-json")
def ember_api_json(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев /repos/ВЛАСНИК/РЕПО/git/trees/.")
    owner, repo = m.groups()
    tags = source.get("tags")
    if not isinstance(tags, dict) or len(tags) != 1:
        raise SystemExit(f"{source['id']}: поле `tags` — один коміт («SHA → \"\"»).")
    commit = next(iter(tags))
    project = source["project"]
    label = source.get("label") or project
    prefix = source.get("version_prefix", "")
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""
    site = (source.get("site") or "").rstrip("/")
    skip = re.compile(source["skip"]) if source.get("skip") else None
    url = f"{source['url']}{quote(commit, safe='')}?recursive=1"
    try:
        tree = json.loads(ctx.text(url))
    except ValueError as exc:
        raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
    if tree.get("truncated"):
        raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
    root = f"json-docs/{project}/"
    found = []
    for entry in tree.get("tree") or []:
        path = entry.get("path", "")
        if entry.get("type") != "blob" or not path.startswith(root) or not path.endswith(".json"):
            continue
        parts = path[len(root):].split("/")
        if len(parts) < 3 or not _VERSION_DIR.match(parts[0]) or parts[1] not in _KINDS:
            continue
        ver = parts[0]
        if skip and skip.search(ver):
            continue
        entity = "/".join(parts[2:])[:-len(".json")]
        entity = re.sub(rf"^{re.escape(project)}-{re.escape(ver)}-", "", entity)
        found.append((path, parts, ver, entity))
    # `@ember/test` і `Ember.Test` (`@ember/routing` і `ember/routing`) — різні записи однієї версії з
    # однаковим слагом: без розрізнення другий файл затирав би перший. При збігу запис з «@» дістає «at-».
    taken: dict = {}
    for _, parts, ver, entity in found:
        taken.setdefault((ver, parts[1], _markup.slug(entity)), set()).add(entity)
    items = []
    for path, parts, ver, entity in found:
        kind = _KINDS[parts[1]]
        line = ".".join(ver.split(".")[:2])
        mark = hashlib.sha1(ver.encode()).hexdigest()[:8]
        stem = _markup.slug(entity)
        if entity.startswith("@") and len(taken[(ver, parts[1], stem)]) > 1:
            stem = f"at-{stem}"
        name = f"{lead}{kind}-{stem}-{mark}"
        raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{commit}/{quote(path)}"
        if not ctx.allowed(raw):
            continue
        page = f"{site}/{line}/{parts[1]}/{quote(entity)}" if site else raw

        def make(raw=raw, page=page, kind=kind, version=prefix + line):
            text = ctx.text(raw)
            try:
                data = json.loads(text)
            except ValueError as exc:
                raise SystemExit(f"{raw}: відповідь не JSON ({exc}).")
            attrs = (data.get("data") or {}).get("attributes") or {}
            title, body = _render(kind, attrs, label)
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, page, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: у json-docs/{project}/ немає жодного запису.")
    return items
