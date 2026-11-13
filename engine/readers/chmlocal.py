"""Читач довідки CHM, розпакованої в теку на цій машині: тема змісту — документ.

`chm-local` — `folder` — абсолютний шлях теки, куди розпаковано файл `.chm` (7-Zip: `7z x файл.chm
              -oтека`); `url` — сторінка довідки на сайті видавця, стоїть у шапці кожного документа й
              сама не читається; `title` — назва довідки, вона стоїть перед назвою кожного документа.
              Необов'язкові: `hhc` — ім'я файла змісту (типово єдиний `*.hhc` теки); `name_prefix` —
              початок імені кожного документа; `version` — мітка версії; `code_lang` — мова блоків коду;
              `skip` — вираз назв тем, що не беруться; `min_chars` — найкоротше тіло.

Навіщо. Довідку терміналу MetaTrader 5 (торгівля, графіки, тестер стратегій, вбудовані індикатори з
формулами) і довідник MQL4 MetaQuotes дає лише файлами CHM, а умови mql5.com забороняють збирати сайт
програмами. Файл кладе людина (або його ставить сам термінал), розпаковує 7-Zip-ом, і читач до мережі
не звертається: білий список тут — сам шлях, оголошений у `sources.json`.

Що робить. CHM — це архів сторінок HTML і файла змісту `.hhc`. Зміст — вкладені `<UL>` з об'єктами
`text/sitemap`, у кожного назва (`Name`) і сторінка (`Local`). Читач іде змістом по порядку; сторінка,
яку зміст називає вдруге, не повторюється. Першим рядком тіла стоїть шлях розділів («Section: Algorithmic
Trading › Strategy Tester»), як у читачі `helpmanual-pdf`: назва теми часто загальна («Settings»), і
без шляху не видно, про що вона.

Сторінки, зібрані Help+Manual, не мають тегів заголовків: підзаголовок — абзац із класом `p_H2`
чи `p_H3`, а приклад коду — абзац `p_CodeExample` з рядками через `<br>`, загорнутий у таблицю з однієї
клітинки. Без заміни підзаголовки злилися б із текстом, а код став би рядком таблиці. Тому перед
розбором `p_H2`/`p_H3` стають `<h2>`/`<h3>`, абзац коду — `<pre>`, а таблиця, де лише код, знімається.
Назва теми (`p_H1`) прибирається з тіла: вона вже стоїть у назві документа. Кодування сторінки
береться з її `<meta charset>` (Help+Manual пише Windows-1252).
"""

import os
import re

from engine.readers import Item, _markup, register

_ENTRY = re.compile(r"<UL>|</UL>|<OBJECT\s+type=\"text/sitemap\">(.*?)</OBJECT>", re.S | re.I)
_PARAM = re.compile(r'<param\s+name="(\w+)"\s+value="([^"]*)"', re.I)
_CHARSET = re.compile(rb"charset=[\"']?([\w-]+)", re.I)
_HELP = re.compile(r'<div id="help">(.*)</div>', re.S | re.I)
_BODY = re.compile(r"<body\b[^>]*>(.*)</body>", re.S | re.I)
_H1 = re.compile(r'<p class="p_H1"[^>]*>.*?</p>', re.S)
_HEAD = re.compile(r'<p class="p_(?:table_)?H([23])"[^>]*>(.*?)</p>', re.S)
_CODE = re.compile(r'<p class="p_CodeExample\w*"[^>]*>(.*?)</p>', re.S)
_CODE_TABLE = re.compile(r"<table\b[^>]*>\s*<tr\b[^>]*>\s*<td\b[^>]*>\s*(<pre\b.*?</pre>)\s*</td>\s*"
                         r"</tr>\s*</table>", re.S | re.I)


def _decode(raw: bytes) -> str:
    m = _CHARSET.search(raw[:2048])
    for enc in ([m.group(1).decode()] if m else []) + ["utf-8", "cp1252"]:
        try:
            return raw.decode(enc)
        except (LookupError, UnicodeDecodeError):
            continue
    return raw.decode("utf-8", "replace")


def _toc(text: str) -> list[tuple[list[str], str]]:
    """(шлях назв від кореня, сторінка) кожного пункту змісту по порядку."""
    out, stack, depth = [], [], 0
    for m in _ENTRY.finditer(text):
        token = m.group(0)[:4].upper()
        if token == "<UL>":
            depth += 1
        elif token == "</UL":
            depth = max(0, depth - 1)
            del stack[depth:]
        else:
            params = {k.lower(): v for k, v in _PARAM.findall(m.group(1))}
            name = " ".join(params.get("name", "").split())
            del stack[max(0, depth - 1):]
            stack.append(name)
            local = params.get("local", "").split("#", 1)[0]
            if local:
                out.append((list(stack), local))
    return out


def _body(html: str, code_lang: str) -> str:
    m = _HELP.search(html) or _BODY.search(html)
    part = m.group(1) if m else html
    part = part.replace("&nbsp;", " ")
    part = _H1.sub("", part, count=1)
    part = _HEAD.sub(lambda h: f"<h{h.group(1)}>{h.group(2)}</h{h.group(1)}>", part)
    lang = f' class="language-{code_lang}"' if code_lang else ""
    part = _CODE.sub(lambda c: f"<pre{lang}>{c.group(1)}</pre>", part)
    part = _CODE_TABLE.sub(r"\1", part)
    return _markup.html_body(part).strip()


@register("chm-local")
def chm_local(source: dict, ctx) -> list[Item]:
    folder = source.get("folder")
    if not folder or not os.path.isdir(folder):
        raise SystemExit(f"{source['id']}: читач chm-local потребує поля folder — теки, куди "
                         f"розпаковано CHM; {folder!r} не тека.")
    files = {name.lower(): name for name in os.listdir(folder)}
    hhc = source.get("hhc") or next((files[n] for n in sorted(files) if n.endswith(".hhc")), "")
    if not hhc or hhc.lower() not in files:
        raise SystemExit(f"{source['id']}: у {folder} немає файла змісту .hhc.")
    with open(os.path.join(folder, files[hhc.lower()]), "rb") as fh:
        toc = _toc(_decode(fh.read()))
    label = source.get("title") or source["id"]
    page_url = source.get("url", "")
    lead = f"{_markup.slug(source.get('name_prefix') or source['id'])}-"
    skip = re.compile(source["skip"]) if source.get("skip") else None
    min_chars = int(source.get("min_chars", 80))
    code_lang = source.get("code_lang", "")
    items, seen, short = [], set(), 0
    for path, local in toc:
        key = local.replace("\\", "/").lower()
        if key in seen or key not in files or (skip and skip.search(path[-1])):
            continue
        seen.add(key)
        with open(os.path.join(folder, files[key]), "rb") as fh:
            body = _body(_decode(fh.read()), code_lang)
        if len(body) < min_chars:
            short += 1
            continue
        if len(path) > 1:
            body = f"Section: {' › '.join(path[:-1])}\n\n{body}"
        title = f"{label}: {path[-1]}"
        slug = lead + _markup.slug(os.path.splitext(local)[0])

        def make(title=title, body=body):
            _markup.require(title, body, page_url, min_chars)
            return _markup.document(title, page_url, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{slug}", file=f"{source['id']}--{slug}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: зміст {hhc} не назвав жодної сторінки з текстом.")
    print(f"  {label}: документів {len(items)}, коротких пропущено {short}", flush=True)
    return items
