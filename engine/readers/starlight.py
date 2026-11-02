"""Читач сайтів Astro Starlight, де приклади коду зібрано Expressive Code, а пошту ховає Cloudflare.

`sitemap-starlight` — те саме, що `sitemap-html` (поля `within`, `match`, `exclude`, `end`, `drop`,
                      `start`, `doc_title`, `min_chars`, `inline_titles`, `version`), але перед
                      розбором сторінка очищується від трьох особливостей розмітки, а адреса,
                      що збігається з `within`, лишається з завершальною рискою.

Навіщо. api.sender.net і центр допомоги sender.net зібрано Starlight, і спільний розбір псує на
них три речі:
- Expressive Code кладе кожен рядок коду в окремий `<div class="ec-line">` без переносу між ними,
  тож рядки злипалися: `import requestsimport json`. Запит із такого прикладу не прочитати;
- посилання-якір біля заголовка несе прихований текст, і під кожним заголовком з'являвся рядок
  «Section titled “Endpoint”», який нічого не каже, зате потрапляє в пошук;
- Cloudflare замінює адреси пошти на «[email protected]», а справжню адресу тримає в атрибуті
  `data-cfemail`. Адреса служби підтримки чи поле `from` у прикладі зникали, хоч вони є в сторінці.

Завершальна риска. `sitemap-html` зрізає її в кожної адреси, а тоді головна сторінка довідки
(`https://api.sender.net/`, а там базова адреса й огляд API) опиняється поза `within` і тихо випадає.

Чому окремий модуль, а не поля в `sitemap-html`: інші примірники зібрані й звірені, а правка
спільного читача — ризик зсуву в готовій роботі. Сама сторінка очищується обгорткою над `ctx`, тож
сховище сирого лишає відповідь сайту такою, як вона прийшла, і `build` очищує її так само.
"""

import re

from engine.readers import register
from engine.readers.sitemap import _LOC, _inside
from engine.readers.sitemaphtml import _fields, _items

_PRE = re.compile(r'<pre\b([^>]*)>\s*<code>(.*?)</code>\s*</pre>', re.S)
_LANG = re.compile(r'\bdata-language="([\w+#-]+)"')
_LINE = re.compile(r'<div class="ec-line[^"]*"[^>]*><div class="code">(.*?)</div></div>', re.S)
_ANCHOR = re.compile(r'<a\b[^>]*\bclass="sl-anchor-link[^"]*"[^>]*>.*?</a>', re.S)
_EMAIL = re.compile(r'<(a|span)\b[^>]*\bdata-cfemail="([0-9a-fA-F]+)"[^>]*>.*?</\1>', re.S)
# Підпис рамки коду («Terminal window») — лише назва оформлення, а не текст сторінки.
_CAPTION = re.compile(r'<figcaption\b[^>]*>.*?</figcaption>', re.S)


def _email(m: re.Match) -> str:
    """Перший байт `data-cfemail` — ключ, решта — адреса, де кожен байт змішано з ключем через XOR."""
    data = bytes.fromhex(m.group(2))
    return bytes(b ^ data[0] for b in data[1:]).decode("utf-8", "replace")


def _code(m: re.Match) -> str:
    lines = _LINE.findall(m.group(2))
    if not lines:
        return m.group(0)
    # Порожній рядок коду сайт записує переносом усередині блоку, тож перенос тут ставимо лише сами.
    code = "\n".join(line.replace("\n", "") for line in lines)
    found = _LANG.search(m.group(1))
    lang = f' lang="{found.group(1)}"' if found else ""
    return f"<pre{lang}><code>{code}</code></pre>"


def clean(html: str) -> str:
    html = _ANCHOR.sub("", html)
    html = _EMAIL.sub(_email, html)
    html = _CAPTION.sub("", html)
    return _PRE.sub(_code, html)


class _Clean:
    """Той самий `ctx`, але сторінки віддає очищеними: розбір спільний, і він цього не помічає."""

    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url, *args, **kwargs):
        return clean(self._ctx.text(url, *args, **kwargs))


@register("sitemap-starlight")
def sitemap_starlight(source: dict, ctx) -> list:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач sitemap-starlight вимагає поле `within` — "
                         f"інакше сайтмап потягнув би весь сайт.")
    match = re.compile(source["match"]) if source.get("match") else None
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    pages: list[str] = []
    for loc in _LOC.findall(ctx.text(source["url"])):
        page = loc.rstrip("/")
        if page + "/" in within:
            page += "/"
        if (page not in pages and _inside(page, within) and ctx.allowed(page)
                and (not match or match.search(page))
                and not any(r.search(page) for r in exclude)):
            pages.append(page)
    if not pages:
        raise SystemExit(f"У сайтмапі {source['url']} не знайдено жодної дозволеної "
                         f"сторінки — розмітка змінилася або `within` не той.")
    return _items(source, _Clean(ctx), pages, *_fields(source))
