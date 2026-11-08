"""Читач сайту Sphinx, який проєкт публікує цілим архівом HTML на кожну версію.

`sphinx-zip` — `url` — адреса архіву з `{version}` на місці номера
               (`https://numpy.org/doc/{version}/numpy-html.zip`); `versions` — номери, для яких
               архів є, від найновішого; `site` — адреса сторінки для людей з `{version}` і `{path}`
               (шлях усередині архіву): текст береться з архіву, адреса лише цитується.
               Необов'язкові: `archives` — об'єкт «номер → {"url": адреса архіву, "site": адреса
               сторінки з `{path}`}» для версій, чий архів названо інакше чи лежить деінде (старі
               лінії NumPy — на docs.scipy.org: `numpy-1.15.4/numpy-html-1.15.4.zip`); ці версії
               йдуть після `versions`, у порядку об'єкта; `exclude` — вирази шляхів усередині
               архіву, що не беруться; `end` — вирази, на яких текст сторінки закінчується;
               `version_prefix` — рядок перед номером у мітці версії; `min_chars` — найкоротше тіло
               без підзаголовка.

Навіщо. numpy.org публікує для кожної лінії 1.16–2.5 повний сайт одним `numpy-html.zip`, а
docs.scipy.org — для ліній 1.3–1.15: близько 2 700 сторінок, з них понад 2 000 — довідник API,
згенерований з коду, якого в репозиторії немає. Обхід сайту — тисячі звернень на версію (сайт
віддає близько 20 сторінок на хвилину), а архів — одне. Сторінку розбирає `page_text` читача
`sphinx-html`; перед тим тут виправляються три місця, які той розбирає погано, а міняти спільний
розбір означало б зсунути вже зібрані примірники:

- тип параметра в новій темі стоїть окремим `<span class="classifier">` упритул до назви:
  «aarray_like» замість «a : array_like»;
- стара тема (1.13–1.x) пише сигнатуру двома `<code>`: «`numpy.``argsort`»;
- посилання «[source]» і нижній колонтитул старих тем з датою збирання («Last updated on …»):
  дата різна в кожній версії, і однакова сторінка двох версій ставала двома документами; у класичній
  темі (1.3–1.x) перед колонтитулом ще й нижня навігація.

Документ — неповторний текст сторінки, як у `sphinx-html`: однакова сторінка кількох версій — один
документ із переліком версій. Тексти в пам'яті лежать стиснені, бо сторінок десятки тисяч.
"""

import hashlib
import re
import zipfile
import zlib
import io

from engine.readers import Item, _markup, register
from engine.readers.sphinxhtml import _ENDS, page_text

_SKIP = [re.compile(r"(^|/)(search|genindex|py-modindex|objects)\.html$"),
         re.compile(r"(^|/)_(static|sources|images|downloads)/")]
_CLASSIFIER = re.compile(r'(</strong>)\s*(<span class="classifier">)')
_OLD_SIG = re.compile(r'<code class="descclassname">(.*?)</code><code class="descname">(.*?)</code>',
                      re.S)
_SOURCE_LINK = re.compile(r'<a class="reference (?:external|internal)"[^>]*>\s*'
                          r'<span class="viewcode-link">.*?</span>\s*</a>', re.S)
_OLD_FOOTER = r'<div class="container container-navbar-bottom">'
# Класична тема Sphinx (NumPy 1.3–1.x): після тексту — нижня навігація й бічна панель.
_CLASSIC_ENDS = [r'<div class="related"', r'<div class="sphinxsidebar"']


def _fix(html: str) -> str:
    html = _CLASSIFIER.sub(r"\1 : \2", html)
    html = _OLD_SIG.sub(r"\1\2", html)
    return _SOURCE_LINK.sub("", html)


@register("sphinx-zip")
def sphinx_zip(source: dict, ctx) -> list[Item]:
    template, site = source.get("url", ""), source.get("site", "")
    plan = [(str(v), template.replace("{version}", str(v)), site.replace("{version}", str(v)))
            for v in source.get("versions") or ()]
    if plan and ("{version}" not in template or "{path}" not in site):
        raise SystemExit(f"{source['id']}: читач sphinx-zip потребує `url` з {{version}} і `site` з "
                         f"{{version}} і {{path}}.")
    for v, arch in (source.get("archives") or {}).items():
        if "{path}" not in arch.get("site", "") or not arch.get("url"):
            raise SystemExit(f"{source['id']}: запис `archives` «{v}» потребує `url` і `site` з {{path}}.")
        plan.append((str(v), arch["url"], arch["site"]))
    if not plan:
        raise SystemExit(f"{source['id']}: читач sphinx-zip потребує поля `versions` чи `archives`.")
    exclude = _SKIP + [re.compile(r) for r in source.get("exclude") or ()]
    ends = [re.compile(r) for r in source.get("end") or (_ENDS + [_OLD_FOOTER] + _CLASSIC_ENDS)]
    vprefix = source.get("version_prefix", "")

    # Сторінка → {хеш тексту → [назва, стиснене тіло, адреса найновішої версії, версії]}.
    pages: dict[str, dict] = {}

    def take(path: str, html: str, url: str, version: str) -> None:
        try:
            title, body = page_text(_fix(html), url, ends)
        except SystemExit:
            return  # сторінка без <h1>: службова, тексту в ній немає
        if not body.strip():
            return
        key = _markup.slug(path.rsplit(".", 1)[0])
        digest = hashlib.sha1(f"{title}\n{body}".encode()).hexdigest()[:8]
        entry = pages.setdefault(key, {}).setdefault(
            digest, [title, zlib.compress(body.encode()), url, []])
        entry[3].append(version)

    for version, zurl, vsite in plan:
        if not ctx.allowed(zurl):
            raise SystemExit(f"{source['id']}: адреса {zurl} поза білим списком.")
        with zipfile.ZipFile(io.BytesIO(ctx.bytes(zurl))) as z:
            for path in z.namelist():
                if not path.endswith(".html") or any(r.search(path) for r in exclude):
                    continue
                html = z.read(path).decode("utf-8", "replace")
                take(path, html, vsite.replace("{path}", path), version)
        print(f"  {zurl}: сторінок усього {sum(len(r) for r in pages.values())}", flush=True)

    if not pages:
        raise SystemExit(f"{source['id']}: жодної сторінки з текстом — розмітка сайту змінилася.")
    items = []
    for key, revisions in pages.items():
        for digest, (title, packed, url, vers) in revisions.items():
            def make(title=title, packed=packed, url=url, vers=vers):
                body = zlib.decompress(packed).decode()
                _markup.require(title, body, url, int(source.get("min_chars", _markup.MIN_BODY)))
                return _markup.document(title, url, ctx.stamp, body,
                                        ", ".join(vprefix + v for v in vers))

            name = f"{key}-{digest}"
            items.append(Item(id=f"{source['id']}/{name}",
                              file=f"{source['id']}--{name}.txt", make=make))
    return items
