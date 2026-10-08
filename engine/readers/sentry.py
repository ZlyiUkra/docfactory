"""Читачі документації Sentry: сайт docs.sentry.io, журнал змін sentry-cli, README плагінів збирачів.

`sentry-md`         — те саме, що `sitemap-md`: `url` — sitemap.xml сайту, документом стає кожна
                      адреса всередині `within`, текст — її markdown-двійник із «.md», назва — перший
                      заголовок. Різниця — версія. Сторінка зі суфіксом «__v10.x» чи «__v10.7.0»
                      в адресі — це та сама сторінка для старшої лінії SDK, і версією стає число
                      з суфікса («10», «10.7.0»); решта сторінок несе `version` джерела. І ще
                      імена двох сторінок, що різняться лише регістром адреси, — див. у коді.
`sentry-changelog`  — те саме, що `changelog`: CHANGELOG.md, поділений на версії, одна версія — один
                      документ. Заголовок версії може нести назву продукту: «## sentry-cli 1.68.0»
                      поруч із «## 3.8.0». `name_prefix` — рядок перед іменем документа: журнали
                      плагінів, CLI і SDK мають ті самі номери («2.0.0»), і без нього однаковий запис
                      двох журналів злився б в один фрагмент.
`npm-readme-latest` — README найновішої версії пакета з опису в реєстрі npm (`url` —
                      https://registry.npmjs.org/ПАКЕТ, поле `readme`); версія документа — мітка
                      `latest`.

Навіщо. Сайт тримає поточну лінію SDK за звичайною адресою, а сторінки, що для старшої лінії
відрізняються, — поруч, зі суфіксом версії: «…/tracing/streamed-spans__v10.x». `sitemap-md` дав
би обом ту саму версію джерела, і сторінка лінії 10 лежала б у корпусі як поточна. Журнал
sentry-cli до 1.69.0 підписував версії назвою програми, і `changelog` такого заголовка не
впізнає: понад сотня записів 1.x злиплася б в один документ 1.69.0. README плагінів Vite,
webpack, Rollup та esbuild з усіма опціями збирається з шаблону під час публікації — у
репозиторії лежить лише шаблон, а повний текст є тільки в реєстрі npm. `npm-readme` читає README
з репозиторію на коміті кожної версії, тож тут не годиться.

Чому окремий модуль, а не поля в наявних читачах: інші примірники зібрані й звірені, а правка
спільного читача — ризик зсуву в готовій роботі. Цей модуль лише реєструє нові імена й
перевикористовує помічники, нічого в них не змінюючи.
"""

import collections
import json
import re
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register
from engine.readers.ghhistory import _atx
from engine.readers.mdheading import _document, _split_title
from engine.readers.sitemap import _LOC, _inside

_SDK_LINE = re.compile(r"__v(\d+(?:\.\d+)*)(?:\.x)?$")
_CAMEL = re.compile(r"([a-z0-9])([A-Z])")
_NAMED_HEAD = re.compile(
    r"^## +(?:[A-Za-z][\w-]* +)?v?(\d+\.\d+[\w.-]*)[ \t]*(\([^)\n]*\))?[ \t]*$", re.M)


@register("sentry-md")
def sentry_md(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач sentry-md вимагає поле `within` — "
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
    # Ім'я документа — шлях у нижньому регістрі, але сайт має пари сторінок, що
    # різняться лише регістром: в Electron «…/integrations/childprocess» (ChildProcess)
    # і «…/integrations/childProcess» (Child Process Integration) — різні тексти.
    # Зі спільним ім'ям друга затирала б першу; сторінка з великими літерами в такій
    # парі дістає ім'я зі словами, розділеними на межі регістру («child-process»).
    # Решта імен ті самі, що дав би sitemap-md.
    taken = collections.Counter(_markup.slug(urlsplit(p).path) for p in pages)
    items = []
    for page in pages:
        path = urlsplit(page).path
        name = _markup.slug(path)
        if taken[name] > 1 and path != path.lower():
            name = _markup.slug(_CAMEL.sub(r"\1-\2", path))
        line = _SDK_LINE.search(page)
        version = line.group(1) if line else source.get("version", "")

        def make(page=page, version=version):
            return _document(ctx, page + ".md", page, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items


@register("sentry-changelog")
def sentry_changelog(source: dict, ctx) -> list[Item]:
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    heads = list(_NAMED_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка версії «## X.Y.Z» — "
                         f"формат змінився, читача треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Changelog")
    lead = (re.sub(r"[^\w.-]+", "-", source["name_prefix"]).strip("-") + "-"
            if source.get("name_prefix") else "")
    items = []
    for i, head in enumerate(heads):
        version = head.group(1)
        heading = f"{version} {head.group(2) or ''}".strip()
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        name = lead + re.sub(r"[^\w.-]+", "-", version)
        # Якір — від заголовка, як його написано в журналі: GitHub ставить його й
        # назві продукту («sentry-cli-1680»), і без неї посилання вело б у нікуди.
        anchor = _markup.github_anchor(head.group(0).lstrip("#"))

        def make(chunk=chunk, heading=heading, version=version, anchor=anchor):
            body = _markup.markdown_body(chunk)
            _markup.require(heading, body, f"{source['url']} {heading}", min_chars=1)
            return _markup.document(f"{label}: {heading}", f"{cite}#{anchor}", ctx.stamp,
                                    body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items


@register("npm-readme-latest")
def npm_readme_latest(source: dict, ctx) -> list[Item]:
    package = (source["url"].split("registry.npmjs.org/", 1)[-1]
               .replace("%2F", "/").replace("%2f", "/"))
    name = re.sub(r"[^\w.-]+", "-", package).strip("-")

    def make():
        try:
            packument = json.loads(ctx.text(source["url"]))
        except ValueError as exc:
            raise SystemExit(f"{source['url']}: відповідь не JSON ({exc}).")
        version = str((packument.get("dist-tags") or {}).get("latest") or "")
        text = str(packument.get("readme") or "").replace("\r\n", "\n")
        if not version or not text.strip():
            raise SystemExit(f"{source['url']}: у реєстрі немає мітки latest або README — "
                             f"документ не записую.")
        _, rest = _markup.front_matter(text)
        title, rest = _split_title(_atx(rest))
        body = _markup.markdown_body(rest)
        title = title or package
        _markup.require(title, body, source["url"])
        page = source.get("page") or f"https://www.npmjs.com/package/{package}"
        label = source.get("label", "README")
        return _markup.document(f"{label} {version}: {title}", page, ctx.stamp, body, version)

    return [Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make)]
