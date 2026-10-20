"""Читач browser-compat-data: дані сумісності браузерів з npm-пакета @mdn/browser-compat-data.

`npm-bcd` — `url` — опис пакета в реєстрі (https://registry.npmjs.org/@mdn%2Fbrowser-compat-data).
            З кожної мажорної лінії береться найновіший стабільний випуск (x.y.z без «-»);
            мінорні й патч-випуски всередині лінії пропускаються. Документ — одна ознака
            платформи («api.structuredClone», «css.properties.grid-template-columns.subgrid»):
            посилання на сторінку MDN і специфікацію, статус і перша версія кожного браузера,
            що підтримує ознаку, з примітками, префіксами, прапорцями й частковою підтримкою.

Навіщо. Сторінка MDN несе лише підсумок Baseline: чи можливість широко доступна і з якої версії
чотирьох основних рушіїв. Таблицю по кожному методу, параметру й значенню на сайті браузер
дотягує окремо з цього пакета, тож у зібраному тексті сторінки її немає — а саме вона відповідає
на «з якої версії Node підтримує structuredClone», «чи працює в Safari опція», «який прапорець
вмикає». Пакет — один JSON (data.json, ~20 МБ), тож ознака не може бути окремою сторінкою
сайту: читач сам ріже файл на ознаки.

Одиниця — неповторний текст ознаки. Однаковий у кількох лініях текст — один документ, у шапці
якого всі ці версії; змінений — окремий документ з тим самим іменем без хеша: у `slug_rewrite`
примірника суфікс «-<8 знаків хеша>» зрізається, і редакції однієї ознаки зливаються за
версіями, як сторінки сусідніх версій у інших примірників.
"""

import collections
import gzip
import hashlib
import html
import io
import json
import re
import tarfile

from engine.readers import Item, _markup, register

_STABLE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
_NOT_FEATURES = {"browsers", "__meta"}
_NOT_TREE = {"browsers", "scripts"}     # теки пакета 2.x, де лежать не ознаки
_NAME_MAX = 100     # довші ключі ріжуться, а до імені додається хеш ключа

# Порядок і назви — як у підсумку Baseline на сайті, далі решта рушіїв за абеткою ключа.
_ORDER = ("chrome", "chrome_android", "edge", "firefox", "firefox_android", "safari", "safari_ios")
_BROWSERS = {
    "chrome": "Chrome", "chrome_android": "Chrome Android", "edge": "Edge", "firefox": "Firefox",
    "firefox_android": "Firefox for Android", "safari": "Safari", "safari_ios": "Safari on iOS",
    "opera": "Opera", "opera_android": "Opera Android", "samsunginternet_android": "Samsung Internet",
    "webview_android": "WebView Android", "webview_ios": "WebView on iOS", "ie": "Internet Explorer",
    "nodejs": "Node.js", "deno": "Deno", "bun": "Bun", "oculus": "Oculus Browser",
}


def _releases(source: dict, ctx) -> list[tuple[str, str]]:
    """(версія, адреса tarball) найновішого стабільного випуску кожної мажорної лінії;
    найновіша лінія першою."""
    try:
        packument = json.loads(ctx.text(source["url"]))
    except ValueError as exc:
        raise SystemExit(f"{source['url']}: відповідь не JSON ({exc}).")
    newest: dict = {}
    for version, meta in (packument.get("versions") or {}).items():
        m = _STABLE.match(version)
        if not m:
            continue
        number = tuple(int(x) for x in m.groups())
        if number[0] not in newest or number > newest[number[0]][0]:
            newest[number[0]] = (number, version, ((meta or {}).get("dist") or {}).get("tarball", ""))
    if not newest:
        raise SystemExit(f"{source['url']}: жодного стабільного випуску.")
    out = []
    for number, version, url in sorted(newest.values(), reverse=True):
        if not url or not ctx.allowed(url):
            raise SystemExit(f"{source['id']}: у випуску {version} немає дозволеної адреси tarball.")
        out.append((version, url))
    return out


def _merge(into: dict, part: dict) -> None:
    for name, value in part.items():
        if isinstance(value, dict) and isinstance(into.get(name), dict):
            _merge(into[name], value)
        else:
            into[name] = value


def _data(url: str, ctx) -> dict:
    """Дані одного випуску: data.json, а в пакетів 2.x, де його ще не було, — усі файли
    ознак теками (api/AbortController.json…), зведені в одне дерево, як це робить їхній index.js."""
    raw = ctx.bytes(url)
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    tree: dict = {}
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        for member in tar:
            if not member.isfile():
                continue
            path = member.name.split("/", 1)[-1]
            top, _, rest = path.partition("/")
            if path == "data.json":
                return json.loads(tar.extractfile(member).read().decode("utf-8"))
            if rest.endswith(".json") and top not in _NOT_TREE:
                _merge(tree, json.loads(tar.extractfile(member).read().decode("utf-8")))
    return tree


def _walk(node: dict, key: str, page: str, out: list) -> None:
    """Усі вузли з __compat: (ключ, __compat, сторінка MDN). Вузол без власної сторінки
    (параметр, значення) успадковує сторінку найближчої ознаки вище."""
    compat = node.get("__compat")
    if isinstance(compat, dict):
        page = compat.get("mdn_url") or page
        out.append((key, compat, page))
    for name, child in node.items():
        if name != "__compat" and isinstance(child, dict):
            _walk(child, f"{key}.{name}" if key else name, page, out)


def _plain(text) -> str:
    """Примітки BCD — шматки HTML: <code>, <a>, інколи <em>."""
    text = re.sub(r"<code>(.*?)</code>", r"`\1`", str(text), flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    return " ".join(html.unescape(text).split())


def _version(v) -> str:
    if v is False:
        return "not supported"
    if v is True:
        return "supported (first version not recorded)"
    if v is None:
        return "support unknown"
    v = str(v)
    if v == "preview":
        return "preview versions only"
    return f"{v[1:]} or earlier" if v.startswith("≤") else v


def _entry(e: dict) -> str:
    parts = [_version(e.get("version_added"))]
    removed = e.get("version_removed")
    if removed:
        parts.append("removed in " + (_version(removed) if removed is not True else "a later version"))
    if e.get("prefix"):
        parts.append(f"with the prefix {e['prefix']}")
    if e.get("alternative_name"):
        parts.append(f"under the name {e['alternative_name']}")
    if e.get("flags"):
        flags = ", ".join(f"{f.get('type', 'flag')} {f.get('name', '')}"
                          + (f" set to {f['value_to_set']}" if f.get("value_to_set") else "")
                          for f in e["flags"])
        parts.append(f"only behind a flag ({flags})")
    if e.get("partial_implementation"):
        parts.append("partial implementation")
    notes = e.get("notes")
    if notes:
        notes = notes if isinstance(notes, list) else [notes]
        parts.append("note: " + " ".join(_plain(n) for n in notes))
    return "; ".join(parts)


def _body(key: str, c: dict, page: str) -> str:
    lines = [f"Browser compatibility data (browser-compat-data) for `{key}`.", ""]
    if c.get("description"):
        lines.append(f"Description: {_plain(c['description'])}")
    if page:
        lines.append(f"Documentation: {page}")
    spec = c.get("spec_url")
    if spec:
        lines.append("Specification: " + (spec if isinstance(spec, str) else " ".join(spec)))
    status = c.get("status")
    if isinstance(status, dict) and status:
        lines.append("Status: " + ", ".join([
            "on the standards track" if status.get("standard_track") else "not on the standards track",
            "deprecated" if status.get("deprecated") else "not deprecated",
            "experimental" if status.get("experimental") else "not experimental"]))
    lines += ["", "First version that supports it, per browser:", ""]
    support = c.get("support") or {}
    for browser in sorted(support, key=lambda b: (_ORDER.index(b) if b in _ORDER else len(_ORDER), b)):
        entries = support[browser] if isinstance(support[browser], list) else [support[browser]]
        entries = [e for e in entries if isinstance(e, dict)]
        if not entries:
            continue
        name = _BROWSERS.get(browser, browser.replace("_", " ").title())
        lines.append(f"- {name}: {_entry(entries[0])}")
        lines += [f"  - earlier entry: {_entry(e)}" for e in entries[1:]]
    return "\n".join(lines)


@register("npm-bcd")
def npm_bcd(source: dict, ctx) -> list[Item]:
    variants: dict = collections.defaultdict(dict)   # ключ ознаки → хеш тексту → запис
    for version, url in _releases(source, ctx):
        try:
            data = _data(url, ctx)
        except ValueError as exc:
            raise SystemExit(f"{source['id']}: дані випуску {version} не JSON ({exc}).")
        if not data:
            raise SystemExit(f"{source['id']}: у випуску {version} немає даних.")
        found: list = []
        for category, node in data.items():
            if category not in _NOT_FEATURES and isinstance(node, dict):
                _walk(node, category, "", found)
        del data
        for key, compat, page in found:
            body = _body(key, compat, page)
            digest = hashlib.sha1(body.encode("utf-8")).hexdigest()[:8]
            rec = variants[key].setdefault(digest, {"body": body, "page": page, "versions": []})
            rec["versions"].append(version)
        print(f"  {source['id']}: випуск {version} — {len(found)} ознак", flush=True)

    slugs = {key: _markup.slug(key) for key in variants}
    taken = collections.Counter(slugs.values())
    items, files = [], {}
    for key in sorted(variants):
        slug = slugs[key]
        if taken[slug] > 1 or len(slug) > _NAME_MAX:
            tag = hashlib.sha1(key.encode("utf-8")).hexdigest()[:6]
            slug = f"{slug[:_NAME_MAX].rstrip('-')}-{tag}"
        for digest, rec in variants[key].items():
            name = f"bcd-{slug}-{digest}"
            file = f"{source['id']}--{name}.txt"
            if file in files:
                raise SystemExit(f"{source['id']}: ключі «{files[file]}» і «{key}» дали одне ім'я "
                                 f"{file} — джерело не записую.")
            files[file] = key

            def make(key=key, rec=rec):
                newest = rec["versions"][0]
                url = (rec["page"] + "#browser_compatibility" if rec["page"] else
                       f"https://www.npmjs.com/package/@mdn/browser-compat-data/v/{newest}")
                title = f"Browser compatibility: {key}"
                _markup.require(title, rec["body"], url, min_chars=1)
                return _markup.document(title, url, ctx.stamp, rec["body"],
                                        ", ".join(rec["versions"]))

            items.append(Item(id=f"{source['id']}/{name}", file=file, make=make))
    return items
