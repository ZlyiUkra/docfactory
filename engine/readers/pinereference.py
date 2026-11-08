"""Читач довідника мови Pine Script, збереженого браузером: запис на кожну функцію, змінну, константу.

`pine-reference-local` — `files` — об'єкт «мітка версії → абсолютний шлях HTML»
                         (`{"pine-v6": "/…/raw/local/pine-reference-v6.html"}`), від найновішої;
                         `url` — адреса довідника з `{version}` на місці номера версії мови
                         (`https://www.tradingview.com/pine-script-reference/{version}/`); `{version}`
                         заміняється тим, що стоїть у мітці після останнього дефіса («v6»).
                         Необов'язкове `min_chars` — найкоротше тіло запису.

Навіщо. Довідник Pine Script (кожна вбудована функція, змінна й константа з аргументами, типами
й прикладами) сайт TradingView збирає в браузері з бандлів JavaScript: у HTML, який віддає сервер,
жодного запису немає. Умови TradingView забороняють збирати їхній вміст програмами, тож сторінки
кожної версії мови користувач зберіг сам браузером («Веб-сторінка повністю»), уже відмальованими,
і примірник живе лише на його машині. Звернень у мережу читач не робить.

Будова запису: `<div id="fun_ta.sma" class="tv-pine-reference-item …">` з назвою в `<h3>`, далі
текст, підзаголовки («Syntax», «Arguments», «Example», «Returns», «Remarks», «See also») як `<div>`,
синтаксис — `<pre>`, тип аргументу — `<span>` перед описом, а приклад — `<pre>`, де кожен рядок —
група `<span>` підсвітки, рядки розділено `<br>`, а пробіли записано `&nbsp;`. Без перетворення
приклад склеївся б в один рядок, підзаголовки стали б простими абзацами, а тип аргументу злипся б з
його описом, а посилання «See also» — одне з одним. Однаковий запис кількох версій — один документ із переліком версій, адреса — якір
найновішої.
"""

import hashlib
import html as _html
import pathlib
import re

from engine.readers import Item, _markup, register

_ITEM = re.compile(r'<div id="([^"]+)" data-legacy-id="[^"]*" '
                   r'class="tv-pine-reference-item tv-pine-reference-item--scroll-aligner"')
_H3 = re.compile(r'<h3 class="tv-pine-reference-item__header">(.*?)</h3>', re.S)
_BUTTON = re.compile(r'<button\b.*?</button>', re.S)
_SUB = re.compile(r'<div class="tv-pine-reference-item__sub-header[^"]*">(.*?)</div>', re.S)
_SYNTAX = re.compile(r'<pre class="tv-pine-reference-item__syntax[^"]*">(.*?)</pre>', re.S)
_EXAMPLE = re.compile(r'<pre class="tv-pine-reference-item__example[^"]*">(.*?)</pre>', re.S)
_ARG = re.compile(r'<span class="tv-pine-reference-item__arg-type">(.*?)</span>', re.S)
_LEARN = re.compile(r'<a href="([^"]+)"[^>]*class="tv-pine-reference-item__learn-more-link"[^>]*>.*?</a>',
                    re.S)
_TAG = re.compile(r"<[^>]+>")
# Посилання «See also» стоять упритул одне до одного: без коми «ta.emata.rmata.wma».
_ADJACENT = re.compile(r"</a>\s*<a\b")


def _code(inner: str) -> str:
    text = _TAG.sub("", re.sub(r"<br\s*/?>", "\n", inner))
    return _html.escape(_html.unescape(text).replace("\xa0", " "), quote=False)


def _sub_header(h: re.Match) -> str:
    # «See also» — лише перелік імен. Окремим розділом він ставав крихітним фрагментом, який на
    # запит з іменем («ta.sma») виходив вище за сам запис: пів видачі займали «See also» чужих
    # записів. Абзацом наприкінці попереднього розділу перелік лишається в тексті запису.
    name = _markup.html_body(h.group(1)).strip()
    return f"<p><strong>{name}:</strong></p>" if name.lower() == "see also" else f"<h2>{name}</h2>"


def _item_html(part: str) -> tuple[str, str]:
    m = _H3.search(part)
    # «ta.sma()» → «ta.sma»: з дужками назва не схожа на ідентифікатор, і title_match не ставив
    # запис першим на запит з його іменем — нагорі були «See also» чужих записів.
    title = _markup.html_body(m.group(1)).strip().removesuffix("()") if m else ""
    body = part[m.end():] if m else part
    body = _BUTTON.sub("", body)
    body = _LEARN.sub(lambda a: f"<p>Learn more: {a.group(1)}</p>", body)
    body = _EXAMPLE.sub(lambda e: f'<pre class="language-pine"><code>{_code(e.group(1))}</code></pre>', body)
    body = _SYNTAX.sub(lambda s: f'<pre class="language-pine"><code>{_code(s.group(1))}</code></pre>', body)
    body = _SUB.sub(_sub_header, body)
    body = _ADJACENT.sub("</a>, <a", body)
    body = _ARG.sub(lambda a: f"<strong>{a.group(1).strip()}</strong> — ", body)
    return title, body


@register("pine-reference-local")
def pine_reference_local(source: dict, ctx) -> list[Item]:
    files = source.get("files") or {}
    template = source.get("url", "")
    if not files or "{version}" not in template:
        raise SystemExit(f"{source['id']}: читач pine-reference-local потребує `files` "
                         f"(мітка → шлях) і `url` з {{version}}.")
    # ключ запису → {хеш тексту → [назва, тіло, адреса найновішої версії, версії]}
    entries: dict[str, dict] = {}
    for label, path in files.items():
        page = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
        base = template.replace("{version}", label.rsplit("-", 1)[-1])
        starts = [m for m in _ITEM.finditer(page)]
        if not starts:
            raise SystemExit(f"{source['id']}: у {path} немає жодного запису довідника — сторінку "
                             f"збережено до того, як браузер її відмалював?")
        for n, m in enumerate(starts):
            stop = starts[n + 1].start() if n + 1 < len(starts) else page.find("</main>", m.end())
            title, body = _item_html(page[m.end():stop if stop > 0 else len(page)])
            text = _markup.html_body(body).strip()
            if not title or not text:
                continue
            digest = hashlib.sha1(f"{title}\n{text}".encode()).hexdigest()[:8]
            entry = entries.setdefault(m.group(1), {}).setdefault(
                digest, [title, text, f"{base}#{m.group(1)}", []])
            entry[3].append(label)
        print(f"  {path}: записів {len(starts)}", flush=True)

    items = []
    for key, revisions in entries.items():
        for digest, (title, text, url, labels) in revisions.items():
            def make(title=title, text=text, url=url, labels=labels):
                _markup.require(title, text, url, int(source.get("min_chars", 20)))
                return _markup.document(title, url, ctx.stamp, text, ", ".join(labels))

            name = f"{_markup.slug(key)}-{digest}"
            items.append(Item(id=f"{source['id']}/{name}",
                              file=f"{source['id']}--{name}.txt", make=make))
    return items
