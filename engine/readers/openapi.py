"""Читач специфікацій HTTP API у форматі OpenAPI 3 (JSON або YAML).

`openapi` — `url` — сира специфікація. Документом стає кожен тег («Auth API: admin»,
            «Storage API: object»…), а кожен ендпоінт у ньому — заголовок
            «## METHOD /шлях» з описом, параметрами, полями тіла запиту й кодами
            відповідей. Опис самої специфікації — окремий документ «огляд». Поле
            `label` — префікс назв документів, поле `page` — людська адреса довідника.

Навіщо. Ендпоінти self-hosted Auth, Storage і Analytics сайт Supabase рендерить з
OpenAPI у HTML без markdown-двійника, а в llms-файлах їх немає зовсім. Для Auth
першоджерело — `openapi.yaml` репозиторію supabase/auth: у репозиторії
документації лежить стара Swagger 2.0 ще від netlify/gotrue на 21 ендпоінт, а
чинна специфікація — на 46 шляхів.

Схеми розкриваються на один рівень: поля тіла запиту з типами й описами, без
вкладених об'єктів. Повна схема відповіді — це десятки полів користувача чи
об'єкта, які в уривку лише заглушили б те, про що питають: що передати й що
означає код відповіді.

PyYAML імпортується лише для YAML і лише всередині читача — з тієї ж причини, що
в `config-spec`.
"""

import json

from engine.readers import Item, _markup, register

_METHODS = ("get", "post", "put", "patch", "delete", "head", "options")


def _text(value) -> str:
    return "" if value is None else str(value).strip()


def _load(ctx, url: str) -> dict:
    raw = ctx.text(url)
    if raw.lstrip().startswith("{"):
        spec = json.loads(raw)
    else:
        try:
            import yaml
        except ImportError:
            raise SystemExit("Читачеві openapi для YAML потрібен PyYAML: додайте його в "
                             "requirements.txt примірника й поставте у його venv.")
        spec = yaml.safe_load(raw)
    if not isinstance(spec, dict) or not isinstance(spec.get("paths"), dict):
        raise SystemExit(f"{url}: не схоже на OpenAPI — немає `paths`.")
    return spec


def _resolve(spec: dict, node, depth: int = 0):
    """Внутрішнє посилання «#/components/…» → сам вузол. Зовнішні не тягнуться."""
    while isinstance(node, dict) and "$ref" in node and depth < 10:
        ref = str(node["$ref"])
        if not ref.startswith("#/"):
            return node
        target = spec
        for part in ref[2:].split("/"):
            target = target.get(part, {}) if isinstance(target, dict) else {}
        node, depth = target, depth + 1
    return node


def _type(spec: dict, schema) -> str:
    schema = _resolve(spec, schema)
    if not isinstance(schema, dict):
        return ""
    kind = _text(schema.get("type"))
    if kind == "array":
        inner = _type(spec, schema.get("items"))
        return f"array of {inner}" if inner else "array"
    if schema.get("enum"):
        return f"{kind or 'string'}, one of {', '.join(map(str, schema['enum']))}"
    return kind or ("object" if schema.get("properties") else "")


def _fields(spec: dict, schema) -> list[str]:
    schema = _resolve(spec, schema)
    if not isinstance(schema, dict):
        return []
    parts = [schema] + [_resolve(spec, s) for s in schema.get("allOf") or []]
    lines = []
    for part in parts:
        if not isinstance(part, dict):
            continue
        need = set(part.get("required") or [])
        for name, prop in (part.get("properties") or {}).items():
            prop = _resolve(spec, prop)
            kind = _type(spec, prop)
            desc = " ".join(_text(prop.get("description") if isinstance(prop, dict)
                                  else "").split())
            lines.append(f"- `{name}`" + (f" `{kind}`" if kind else "")
                         + (", required" if name in need else "")
                         + (f": {desc}" if desc else ""))
    return lines


def _operation(spec: dict, method: str, path: str, op: dict, shared: list) -> str:
    lines = [f"## {method.upper()} {path}", ""]
    if _text(op.get("summary")):
        lines += [_text(op["summary"]), ""]
    if _text(op.get("description")):
        lines += [_text(op["description"]), ""]
    if op.get("deprecated"):
        lines += ["Deprecated.", ""]
    security = [name for item in op.get("security") or [] if isinstance(item, dict)
                for name in item]
    if security:
        lines += [f"Security: {', '.join(security)}", ""]
    params = [_resolve(spec, p) for p in shared + (op.get("parameters") or [])]
    params = [p for p in params if isinstance(p, dict) and p.get("name")]
    if params:
        lines += ["Parameters:", ""]
        for p in params:
            kind = _type(spec, p.get("schema") or p)
            desc = " ".join(_text(p.get("description")).split())
            lines.append(f"- `{p['name']}` ({_text(p.get('in'))}"
                         + (", required" if p.get("required") else "") + ")"
                         + (f" `{kind}`" if kind else "") + (f": {desc}" if desc else ""))
        lines.append("")
    body = _resolve(spec, op.get("requestBody"))
    if isinstance(body, dict):
        for ctype, media in (body.get("content") or {}).items():
            fields = _fields(spec, (media or {}).get("schema"))
            lines += [f"Request body ({ctype}):", ""] + (fields or ["- (no fields listed)"])
            lines.append("")
    responses = op.get("responses") or {}
    if responses:
        lines += ["Responses:", ""]
        for code, resp in responses.items():
            resp = _resolve(spec, resp)
            desc = " ".join(_text(resp.get("description") if isinstance(resp, dict)
                                  else "").split())
            lines.append(f"- `{code}`" + (f": {desc}" if desc else ""))
        lines.append("")
    return "\n".join(lines)


@register("openapi")
def openapi(source: dict, ctx) -> list[Item]:
    page = source.get("page", "")
    if not page.startswith("https://"):
        raise SystemExit(f"{source['id']}: читач openapi вимагає поле `page` — людську "
                         f"https-адресу довідника.")
    spec = _load(ctx, source["url"])
    info = spec.get("info") or {}
    label = source.get("label") or _text(info.get("title")) or source["id"]
    version = source.get("version", "")
    prefix = _markup.slug(label)
    described = {t.get("name"): _text(t.get("description"))
                 for t in spec.get("tags") or [] if isinstance(t, dict)}

    groups: dict[str, list] = {}
    for path, item in spec["paths"].items():
        if not isinstance(item, dict):
            continue
        shared = item.get("parameters") or []
        for method in _METHODS:
            op = item.get(method)
            if isinstance(op, dict):
                tag = (op.get("tags") or ["general"])[0]
                groups.setdefault(tag, []).append((method, path, op, shared))

    items = []
    overview = _text(info.get("description"))
    if overview:
        def make_overview():
            body = _markup.markdown_body(overview)
            return _markup.document(f"{label}: overview", page, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{prefix}-overview",
                          file=f"{source['id']}--{prefix}-overview.txt", make=make_overview))

    for tag, ops in groups.items():
        title = f"{label}: {tag}"
        name = f"{prefix}-{_markup.slug(tag)}"

        def make(title=title, tag=tag, ops=ops):
            intro = described.get(tag, "")
            md = "\n".join(([intro, ""] if intro else [])
                           + [_operation(spec, m, p, o, s) for m, p, o, s in ops])
            body = _markup.markdown_body(md)
            _markup.require(title, body, source["url"], min_chars=1)
            return _markup.document(title, page, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
