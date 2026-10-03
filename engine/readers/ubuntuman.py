"""Читач man-сторінок Ubuntu з manpages.ubuntu.com: сторінка команди на кожному випуску.

`ubuntu-man` — `url`      — мапа сайту (…/sitemaps/sitemap-index.xml);
               `releases` — об'єкт «кодова назва випуску → версія Ubuntu», від найновішого
                            («resolute» → «26.04»);
               `pages`    — явний перелік сторінок «ім'я.розділ» («ip.8», «sshd_config.5»);
               `label`    — префікс назви документа.

Навіщо. Команди, якими адміністратор працює щодня (ip, ss, ssh, useradd, lvcreate,
systemctl, apt), документуються в десятку різних проєктів, і кожен пише man-сторінки своєю
розміткою: groff, mdoc, AsciiDoc, DocBook, POD. Ubuntu збирає їх усі однаково — mandoc
віддає готовий HTML, — і під кожною сторінкою пише пакет і його версію в цьому випуску. Тож
один читач дає те, що інакше вимагало б п'яти. Сторінок на сайті десятки тисяч, тому
перелік явний: лише те, що потрібно адміністраторові.

Які сторінки є у випуску, читач дізнається з мапи сайту (кілька файлів на випуск), а не
питаючи кожну адресу: сторінки, якої у випуску немає, у переліку просто не буде.

Одиниця — сторінка у випуску. Ім'я документа — сторінка й хеш випуску, тож однаковий
розділ кількох випусків зливається в корпусі в один фрагмент з усіма версіями
(`revision_suffix` у config.json).
"""

import hashlib
import re

from engine.readers import Item, _markup, register

_LOC = re.compile(r"<loc>([^<]+)</loc>")
_H1 = re.compile(r"<h1>(.*?)</h1>", re.S)
_LEAD = re.compile(r'<p class="p-heading--4">(.*?)</p>', re.S)
_PROVIDED = re.compile(r"Provided by:\s*<a[^>]*>([^<]+)</a>", re.S)
_BODY = re.compile(r'id="manpage-content"[^>]*>(.*?)</main>', re.S)


@register("ubuntu-man")
def ubuntu_man(source: dict, ctx) -> list[Item]:
    releases = source.get("releases")
    pages = source.get("pages")
    if not isinstance(releases, dict) or not releases or not pages:
        raise SystemExit(f"{source['id']}: читач ubuntu-man потребує полів releases "
                         f"(«випуск → версія») і pages («ім'я.розділ»).")
    wanted = {}
    for p in pages:
        name, _, sec = p.rpartition(".")
        if not name or not sec:
            raise SystemExit(f"{source['id']}: сторінка «{p}» — не «ім'я.розділ».")
        wanted[(name, sec)] = p
    label = source.get("label", "")
    maps = _LOC.findall(ctx.text(source["url"]))

    items = []
    for release, version in releases.items():
        sections = sorted({sec for _, sec in wanted})
        found: dict = {}
        for sec in sections:
            pattern = re.compile(rf"/sitemap-{re.escape(release)}-man{re.escape(sec[0])}"
                                 rf"(-\d+)?\.xml$")
            for m in (u for u in maps if pattern.search(u)):
                if not ctx.allowed(m):
                    continue
                for url in _LOC.findall(ctx.text(m)):
                    hit = re.search(rf"/manpages/{re.escape(release)}/man\w+/(.+)\.(\w+)\.html$",
                                    url)
                    if hit and (hit.group(1), hit.group(2)) in wanted:
                        found[(hit.group(1), hit.group(2))] = url
        stamp = hashlib.sha1(release.encode()).hexdigest()[:8]
        for (name, sec), url in sorted(found.items()):
            if not ctx.allowed(url):
                continue
            doc = f"{_markup.slug(f'{name}-{sec}')}-{stamp}"

            def make(url=url, name=name, sec=sec, version=version, release=release):
                html = ctx.text(url)
                body = _BODY.search(html)
                head = _H1.search(html)
                if not body or not head:
                    raise SystemExit(f"Сторінка не схожа на man-сторінку ({url}) — "
                                     f"документ не записую.")
                lead = _LEAD.search(html)
                lead = _markup.html_body(lead.group(1)).strip() if lead else ""
                title = f"{name}({sec})" + (f" — {lead}" if lead else "")
                if label:
                    title = f"{label}: {title}"
                pkg = _PROVIDED.search(html)
                text = _markup.html_body(body.group(1))
                if pkg:
                    text = (f"Ubuntu {version} ({release}), package "
                            f"{' '.join(pkg.group(1).split())}.\n\n{text}")
                _markup.require(title, text, url)
                return _markup.document(title, url, ctx.stamp, text, version)

            items.append(Item(id=f"{source['id']}/{doc}",
                              file=f"{source['id']}--{doc}.txt", make=make))
    return items
