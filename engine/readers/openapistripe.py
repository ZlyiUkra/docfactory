"""Читач специфікації OpenAPI Stripe (stripe/openapi): ендпоінти за ресурсами й схеми об'єктів.

`openapi-stripe` — `url` — `openapi.spec3.json`. Документом стає:
                   - кожен ресурс API — шлях до першої змінної частини (`/v1/charges`,
                     `/v2/core/accounts`): розділ «## METHOD /шлях» на кожну операцію з описом,
                     параметрами шляху й запиту, полями тіла форми (тип, обов'язковість, значення
                     enum, опис, вкладені поля на один рівень) і тим, що повертає;
                   - кожна схема з `components.schemas` — «Object: charge»: опис, розділ «Fields» з
                     кожним полем, його типом (nullable, enum, посилання на інший об'єкт, anyOf)
                     і описом, і перелік розгортуваних полів (`x-expandableFields`).
                   Версія всіх документів — версія API специфікації («api-2026-09-30.endive»).

Навіщо. Спільний читач `openapi` групує операції за тегами, а Stripe тегів не ставить: усі
644 операції лягли б в один документ. І головне в специфікації Stripe — схеми: точні типи, nullable
і повні переліки значень enum, яких на сторінках сайту видно не завжди.
"""

import json
import re

from engine.readers import Item, _markup, register

_METHODS = ("get", "post", "put", "patch", "delete")


def _t(v) -> str:
    return "" if v is None else " ".join(str(v).split())


def _ref(r: str) -> str:
    return r.rsplit("/", 1)[-1]


def _type(s: dict, depth: int = 0) -> str:
    """Тип поля одним рядком: `string`, `integer`, `charge`, `enum: a | b`, `anyOf: …`, `array of …`."""
    if not isinstance(s, dict):
        return ""
    if "$ref" in s:
        return _ref(s["$ref"])
    for key in ("anyOf", "oneOf", "allOf"):
        if key in s and depth < 3:
            parts = [p for p in (_type(x, depth + 1) for x in s[key]) if p]
            return " | ".join(dict.fromkeys(parts))
    kind = s.get("type", "")
    if kind == "array":
        return f"array of {_type(s.get('items') or {}, depth + 1) or 'object'}"
    if "enum" in s:
        vals = [str(v) for v in s["enum"] if v not in (None, "")]
        return (kind + ", one of: " if kind else "one of: ") + ", ".join(f"`{v}`" for v in vals)
    if kind == "object" and s.get("title"):
        return f"object ({s['title']})"
    return kind or "object"


def _field(name: str, s: dict, required: bool, depth: int, out: list[str]) -> None:
    flags = [_type(s)]
    if s.get("nullable"):
        flags.append("nullable")
    if required:
        flags.append("required")
    if s.get("maxLength"):
        flags.append(f"max length {s['maxLength']}")
    out.append("  " * depth + f"- `{name}` ({', '.join(f for f in flags if f)})")
    desc = _t(_markup.markdown_body(str(s.get("description") or "")))
    if desc:
        out.append("  " * depth + f"  {desc}")
    # Вкладені поля тіла запиту — на один рівень: `metadata`, `payment_method_data[...]`.
    if depth == 0:
        inner = s
        for key in ("anyOf", "oneOf"):
            objs = [x for x in s.get(key, []) if isinstance(x, dict) and x.get("properties")]
            if objs:
                inner = objs[0]
        if inner.get("type") == "array":
            inner = inner.get("items") or {}
        props = inner.get("properties") if isinstance(inner, dict) else None
        if props and len(props) <= 60:
            req = set(inner.get("required") or [])
            for k, v in props.items():
                _field(k, v, k in req, 1, out)


def _operation(method: str, path: str, op: dict) -> list[str]:
    out = [f"## {method.upper()} {path}", ""]
    if op.get("summary"):
        out += [_t(op["summary"]), ""]
    if op.get("description"):
        out += [_markup.markdown_body(str(op["description"])), ""]
    params = [p for p in op.get("parameters") or [] if isinstance(p, dict)]
    for where in ("path", "query", "header"):
        group = [p for p in params if p.get("in") == where]
        if group:
            out += [f"{where.capitalize()} parameters:", ""]
            for p in group:
                _field(p.get("name", ""), dict(p.get("schema") or {}, description=p.get("description")),
                       bool(p.get("required")), 0, out)
            out.append("")
    body = (op.get("requestBody") or {}).get("content") or {}
    for ctype, media in body.items():
        schema = media.get("schema") or {}
        props = schema.get("properties") or {}
        if props:
            req = set(schema.get("required") or [])
            out += [f"Body ({ctype}):", ""]
            for k, v in props.items():
                if k == "expand":
                    continue
                _field(k, v, k in req, 0, out)
            out.append("")
        break
    ok = (op.get("responses") or {}).get("200") or {}
    for media in (ok.get("content") or {}).values():
        ret = _type(media.get("schema") or {})
        if ret:
            out += [f"Returns: {ret}", ""]
        break
    return out


def _resource(path: str) -> str:
    """Шлях до першої змінної частини: /v1/charges/{charge}/capture → /v1/charges."""
    keep = []
    for part in path.strip("/").split("/"):
        if part.startswith("{"):
            break
        keep.append(part)
    depth = 3 if keep[:1] == ["v2"] else 2
    return "/" + "/".join(keep[:depth])


@register("openapi-stripe")
def openapi_stripe(source: dict, ctx) -> list[Item]:
    url = source["url"]
    spec = json.loads(ctx.text(url))
    version = f"api-{spec.get('info', {}).get('version', '')}".rstrip("-")
    page = source.get("page") or url
    groups: dict[str, list] = {}
    for path, item in (spec.get("paths") or {}).items():
        for method in _METHODS:
            if isinstance(item.get(method), dict):
                groups.setdefault(_resource(path), []).append((method, path, item[method]))
    items: list[Item] = []
    for res, ops in groups.items():
        name = _markup.slug("openapi" + res)

        def make(res=res, ops=ops):
            body: list[str] = []
            for method, path, op in ops:
                body += _operation(method, path, op)
            return _markup.document(f"Stripe API {res} (OpenAPI)", page, ctx.stamp,
                                    _markup.tidy("\n".join(body), strip=False), version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    for key, schema in (spec.get("components", {}).get("schemas") or {}).items():
        if not isinstance(schema, dict):
            continue
        name = _markup.slug("object-" + key)

        def make(key=key, schema=schema):
            out = []
            if schema.get("description"):
                out += [_markup.markdown_body(str(schema["description"])), ""]
            props = schema.get("properties") or {}
            req = set(schema.get("required") or [])
            # Поля — одним розділом: розділ на поле дав би десятки тисяч фрагментів з одного рядка.
            if props:
                out += ["", "## Fields", ""]
                for k, v in props.items():
                    _field(k, v, k in req, 1, out)
            if schema.get("x-expandableFields"):
                out += ["", "## Expandable fields", "",
                        ", ".join(f"`{f}`" for f in schema["x-expandableFields"])]
            if not out:
                out = [f"Type: {_type(schema)}"]
            return _markup.document(f"Object: {key} (OpenAPI)", page, ctx.stamp,
                                    _markup.tidy("\n".join(out), strip=False), version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    if not items:
        raise SystemExit(f"{url}: у специфікації немає ні шляхів, ні схем.")
    return items
