"""Читач сайтів на Mintlify (docs.kraken.com).

`sitemap-mintlify` — `url` — sitemap.xml сайту; документом стає кожна адреса з нього,
                     що лежить усередині поля `within` цього ж джерела, а текст
                     береться з її markdown-двійника — тієї ж адреси з «.md». Назва —
                     перший заголовок сторінки; поле `label` ставить перед нею
                     префікс («WebSocket v2: Ticker»).

Навіщо окремий читач. Двійник Mintlify — це не чистий markdown, а MDX сайту, лише
з розгорнутими вставками, і `sitemap-md` дав би з нього хибний текст:

- кожна сторінка починається тим самим блоком-цитатою «Documentation Index … llms.txt»
  — це сто з гаком однакових фрагментів без змісту;
- поля повідомлень WebSocket описано компонентами `<ResponseField name="symbol"
  type="string[]" required>`, а `markdown_body` від рядка-компонента лишає тільки
  `title` — тобто саме ім'я поля, його тип і обов'язковість зникали б;
- сторінка ендпойнта REST — це шматок OpenAPI у блоці ````yaml: та сама шапка
  специфікації в кожному (info, servers, теги з довгим описом Earn), а далі схема з
  прикладами — до ста з гаком тисяч символів. Огорожу коду рушій на уривки не ріже,
  тож такий блок став би одним уривком, з якого модель векторів бачить лише початок.
  Блок розбирається (PyYAML) і стає розділами «Request» і «Response»: метод і повна
  адреса, чи потрібен ключ, параметри, поля тіла й відповіді списком з описами,
  переліками значень і короткими прикладами JSON.

Решта компонентів (Tabs, Accordion, Card, Steps, Note…) стає звичайним текстом:
заголовки вкладок і карток — рядком **жирним**, рамки — нічим. Код між огорожами
не чіпається, лише знімається відступ, яким MDX вкладає його в компонент.
"""

import json
import re
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register
from engine.readers.mdheading import _split_title
from engine.readers.sitemap import _LOC, _inside

# Блок-цитата, якою Mintlify відкриває кожен двійник: «> ## Documentation Index» і
# два-три рядки «> …» під ним.
_INDEX = re.compile(r"\A\s*> ## Documentation [Ii]ndex\n(?:>[^\n]*\n)*")
_OPENAPI = re.compile(r"^(?:## OpenAPI\n+)?(`{3,})yaml (\S+) (get|post|put|patch|delete) (\S+)\n"
                      r"(.*?)^\1[ \t]*$", re.M | re.S)
# Найдовший приклад JSON, що лишається в тексті.
_EXAMPLE_MAX = 1500
_FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})")
_OPEN = re.compile(r"^\s*<([A-Z][A-Za-z]*)\b([^>]*?)(/?)>\s*$")
_CLOSE = re.compile(r"^\s*</([A-Z][A-Za-z]*)>\s*$")
_INLINE = re.compile(r"^\s*<([A-Z][A-Za-z]*)\b([^>]*)>(.*)</\1>\s*$")
_ATTR = re.compile(r'\b(\w+)="([^"]*)"')
_FLAG = re.compile(r"\s(required|deprecated)\b")
_BANNER = re.compile(r'<div className="api-banner">(.*?)</div>', re.S)
_SPAN = re.compile(r"<span[^>]*>([^<]*)</span>")

# Компоненти, від яких не лишається нічого: рамки й групи.
_FRAMES = {"Tabs", "CodeGroup", "CardGroup", "AccordionGroup", "Steps", "Panel",
           "Expandable", "Frame", "Columns"}
# Підписи врізок — як у LABELS спільного `_markup`.
_CALLOUTS = {"Note": "Note:", "Warning": "Warning:", "Tip": "Tip:", "Info": "Info:",
             "Check": "Check:", "Danger": "Danger:"}


def _resolve(spec: dict, node, seen: tuple = ()):
    """Внутрішнє посилання «#/components/…» → (сам вузол, ланцюжок пройдених
    посилань). Схема, що посилається сама на себе, обривається на другому колі."""
    while isinstance(node, dict) and "$ref" in node:
        ref = str(node["$ref"])
        if not ref.startswith("#/") or ref in seen:
            return {}, seen
        target = spec
        for part in ref[2:].split("/"):
            target = target.get(part, {}) if isinstance(target, dict) else {}
        node, seen = target, seen + (ref,)
    return (node if isinstance(node, dict) else {}), seen


def _code(value) -> str:
    return f"`{json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value}`"


def _kind(spec: dict, sch: dict, seen: tuple) -> str:
    """Тип поля словами: «string», «array of object», «object»."""
    t = sch.get("type") or ("object" if "properties" in sch else "")
    if t == "array":
        items, _ = _resolve(spec, sch.get("items") or {}, seen)
        inner = items.get("type") or ("object" if "properties" in items else "")
        return f"array of {inner}" if inner else "array"
    return str(t)


def _notes(spec: dict, sch: dict, seen: tuple, required: bool, where: str = "") -> str:
    notes = [n for n in (where, _kind(spec, sch, seen), sch.get("format")) if n]
    if required:
        notes.append("required")
    if sch.get("nullable"):
        notes.append("nullable")
    if sch.get("deprecated"):
        notes.append("deprecated")
    return f" ({', '.join(notes)})" if notes else ""


def _facts(sch: dict) -> list[str]:
    """Перелік значень, типове значення, межі й приклад — тим самим ладом, яким сайт
    пише їх у полях WebSocket («One of: …», «Default: …»)."""
    out = []
    if sch.get("enum"):
        out.append("One of: " + ", ".join(_code(v) for v in sch["enum"]))
    if "default" in sch:
        out.append("Default: " + _code(sch["default"]))
    for key, word in (("minimum", "Minimum"), ("maximum", "Maximum"),
                      ("minItems", "Min items"), ("maxItems", "Max items")):
        if key in sch:
            out.append(f"{word}: {_code(sch[key])}")
    if "example" in sch and not isinstance(sch["example"], (dict, list)):
        out.append("Example: " + _code(sch["example"]))
    return out


def _text_lines(text, pad: str) -> list[str]:
    return [pad + ln.strip() if ln.strip() else "" for ln in str(text or "").strip().split("\n")]


def _fields(spec: dict, sch, depth: int, seen: tuple, out: list[str]) -> None:
    """Поля схеми пунктами списку, вкладені поля — з відступом, як у сторінках WebSocket."""
    sch, seen = _resolve(spec, sch, seen)
    if depth > 8:
        return
    for sub in sch.get("allOf") or []:
        _fields(spec, sub, depth, seen, out)
    pad = "  " * depth
    for key in ("oneOf", "anyOf"):
        for i, sub in enumerate(sch.get(key) or [], 1):
            var, vseen = _resolve(spec, sub, seen)
            label = var.get("title") or f"variant {i}"
            out += ["", f"{pad}- One of the forms, {i}: {label}{_notes(spec, var, vseen, False)}"]
            out += _text_lines(var.get("description"), pad + "  ")
            _children(spec, var, depth + 1, vseen, out)
    required = set(sch.get("required") or [])
    for name, sub in (sch.get("properties") or {}).items():
        field, fseen = _resolve(spec, sub, seen)
        out += ["", f"{pad}- `{name}`{_notes(spec, field, fseen, name in required)}"]
        out += _text_lines(field.get("description") or field.get("title"), pad + "  ")
        out += [pad + "  " + f for f in _facts(field)]
        _children(spec, field, depth + 1, fseen, out)
    extra = sch.get("additionalProperties")
    if isinstance(extra, dict):
        field, fseen = _resolve(spec, extra, seen)
        name = extra.get("x-additionalPropertiesName") or field.get("x-additionalPropertiesName") \
            or "key"
        out += ["", f"{pad}- `<{name}>`{_notes(spec, field, fseen, False)}"]
        out += _text_lines(field.get("description") or field.get("title"), pad + "  ")
        _children(spec, field, depth + 1, fseen, out)


def _children(spec: dict, sch: dict, depth: int, seen: tuple, out: list[str]) -> None:
    """Вкладене: поля об'єкта, поля елемента масиву, варіанти oneOf."""
    if sch.get("type") == "array":
        items, iseen = _resolve(spec, sch.get("items") or {}, seen)
        _fields(spec, items, depth, iseen, out)
    else:
        _fields(spec, sch, depth, seen, out)


def _example(value, out: list[str], title: str = "") -> None:
    """Приклад JSON — лише короткий: огорожу коду рушій не ріже, і довгий приклад
    став би одним уривком на десятки тисяч символів."""
    text = json.dumps(value, ensure_ascii=False, indent=2)
    if len(text) > _EXAMPLE_MAX:
        return
    out += ["", f"Example{': ' + title if title else ''}:", "", "```json", text, "```"]


def _openapi(m: re.Match) -> str:
    """Блок OpenAPI ендпойнта → розділи «Request» і «Response» з полями списком.

    Сирий YAML тут не годиться: огорожу коду рушій не ріже на уривки, а схема з
    прикладами доходить до ста з гаком тисяч символів одним шматком. Тож від
    специфікації лишається те, що в ній читає людина: адреса й метод, чи потрібен
    ключ, параметри, поля тіла запиту й відповіді з описами, короткі приклади."""
    try:
        import yaml
    except ImportError:
        raise SystemExit("Читачеві sitemap-mintlify потрібен PyYAML: він приходить разом "
                         "із fastembed (через huggingface_hub).")
    method, path = m.group(3), m.group(4)
    spec = yaml.safe_load(m.group(5)) or {}
    op = ((spec.get("paths") or {}).get(path) or {}).get(method) or {}
    servers = op.get("servers") or spec.get("servers") or [{}]
    out = ["## Request", "", f"`{method.upper()} {servers[0].get('url', '')}{path}`", ""]
    security = op.get("security", spec.get("security"))
    out.append("Authentication: " + (
        "none (public endpoint)." if security == [] else
        ", ".join(f"`{k}`" for s in security or [] for k in s) + " headers." if security else
        "not stated."))
    if op.get("deprecated"):
        out += ["", "Deprecated."]
    params = [_resolve(spec, p)[0] for p in op.get("parameters") or []]
    if params:
        out += ["", "**Parameters**"]
        for p in params:
            sch, seen = _resolve(spec, p.get("schema") or {})
            out += ["", f"- `{p.get('name', '')}`"
                        f"{_notes(spec, sch, seen, bool(p.get('required')), p.get('in', ''))}"]
            out += _text_lines(p.get("description"), "  ")
            out += ["  " + f for f in _facts(sch | ({"example": p["example"]}
                                                    if "example" in p else {}))]
    body = (_resolve(spec, op.get("requestBody") or {})[0].get("content") or {})
    for mime, media in body.items():
        out += ["", f"**Request body** (`{mime}`)"]
        _fields(spec, media.get("schema") or {}, 0, (), out)
        if "example" in media:
            _example(media["example"], out)
    out += ["", "## Response"]
    for code, resp in (op.get("responses") or {}).items():
        resp, _ = _resolve(spec, resp)
        out += ["", f"**{code}** — {str(resp.get('description') or '').strip()}"]
        for mime, media in (resp.get("content") or {}).items():
            sch, seen = _resolve(spec, media.get("schema") or {})
            if mime != "application/json":
                out += ["", f"Content type: `{mime}`"]
            _fields(spec, sch, 0, seen, out)
            if "example" in media:
                _example(media["example"], out)
            elif "example" in sch:
                _example(sch["example"], out)
            for title, ex in (media.get("examples") or {}).items():
                if isinstance(ex, dict) and "value" in ex:
                    _example(ex["value"], out, title)
    return "\n".join(out)


def _field(attrs: str) -> str:
    """`<ResponseField name="x" type="t" required>` → «`x` (t, required)»."""
    a = dict(_ATTR.findall(attrs))
    notes = [a["type"]] if a.get("type") else []
    notes += _FLAG.findall(" " + _ATTR.sub("", attrs))
    if a.get("default"):
        notes.append(f"default `{a['default']}`")
    name = f"`{a['name']}`" if a.get("name") else ""
    return name + (f" ({', '.join(notes)})" if notes else "")


def _mdx(text: str) -> str:
    """MDX двійника → markdown, який далі розбирає `_markup.markdown_body`."""
    text = _BANNER.sub(lambda m: " ".join(_SPAN.findall(m.group(1))), text)
    out: list[str] = []
    fence, cut, depth = "", 0, 0
    for ln in text.split("\n"):
        if fence:
            out.append(ln[cut:] if ln[:cut].strip() == "" else ln.lstrip())
            if ln.strip().startswith(fence) and set(ln.strip()) == {fence[0]}:
                fence = ""
            continue
        m = _FENCE.match(ln)
        if m:
            fence, cut = m.group(2), len(m.group(1))
            out.append(ln[cut:])
            continue
        m = _INLINE.match(ln)
        if m:
            # Компонент в один рядок: «<ResponseField name="ask" type="float">Best ask
            # price.</ResponseField>», «<Note>…</Note>».
            tag, attrs, inner = m.groups()
            if tag in ("ResponseField", "ParamField"):
                out += ["", "  " * depth + "- " + _field(attrs) + " — " + inner.strip()]
            else:
                out += ["", (_CALLOUTS.get(tag, "") + " " + inner.strip()).strip()]
            continue
        m = _CLOSE.match(ln)
        if m:
            if m.group(1) == "ResponseField":
                depth = max(0, depth - 1)
            continue
        m = _OPEN.match(ln)
        if m:
            tag, attrs, closed = m.groups()
            if tag == "ResponseField" or tag == "ParamField":
                out += ["", "  " * depth + "- " + _field(attrs)]
                if not closed:
                    depth += 1
            elif tag in _CALLOUTS:
                out += ["", _CALLOUTS[tag]]
            elif tag not in _FRAMES:
                title = dict(_ATTR.findall(attrs)).get("title")
                if title:
                    out += ["", f"**{title}**", ""]
            continue
        # Відступ MDX — це вкладеність компонентів, а не код: знімається; текст поля
        # лишається під своїм пунктом.
        s = ln.strip()
        if depth and s:
            out.append("  " * depth + s)
        else:
            out.append(s if ln[:1] in (" ", "\t") else ln)
    return "\n".join(out)


def _document(ctx, source: dict, md_url: str, page: str) -> str:
    text = ctx.text(md_url)
    _markup.refuse_html(text, md_url)
    text = _INDEX.sub("", text.replace("\r\n", "\n"))
    title, rest = _split_title(text)
    # Спершу MDX, потім OpenAPI: _mdx знімає відступи, а у списку полів відповіді
    # відступ — це вкладеність поля.
    rest = _OPENAPI.sub(_openapi, _mdx(rest))
    body = _markup.markdown_body(rest)
    _markup.require(title, body, md_url, min_chars=1)
    if source.get("label"):
        title = f"{source['label']}: {title}"
    return _markup.document(title, page, ctx.stamp, body, source.get("version", ""))


@register("sitemap-mintlify")
def sitemap_mintlify(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач sitemap-mintlify вимагає поле `within` — "
                         f"інакше сайтмап потягнув би весь сайт.")
    pages: list[str] = []
    for loc in _LOC.findall(ctx.text(source["url"])):
        page = loc.rstrip("/")
        md = page + ".md"
        if page not in pages and _inside(md, within) and ctx.allowed(md):
            pages.append(page)
    if not pages:
        raise SystemExit(f"У сайтмапі {source['url']} не знайдено жодної дозволеної "
                         f"сторінки — розмітка змінилася або `within` не той.")
    items = []
    for page in pages:
        name = _markup.slug(urlsplit(page).path)

        def make(page=page):
            return _document(ctx, source, page + ".md", page)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
