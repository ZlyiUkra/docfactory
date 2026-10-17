"""Читач індексу пакетів репозиторію APT: один документ на ім'я пакета.

`apt-packages` — `url` — індекс `Packages` репозиторію Debian (…/dists/<набір>/<компонент>/
                 binary-<архітектура>/Packages), необов'язкове `pages` — індекси тих самих
                 пакетів для інших архітектур. Документом стає кожне ім'я пакета: назва
                 «<пакет> <версія> (APT)», версія — поле Version, у тексті — розділ на кожну
                 архітектуру з полями керування (Version, Architecture, Depends, Size, Filename,
                 SHA256…) і довгий опис пакета текстом. `name_prefix` — рядок перед іменем
                 документа; `label` — підпис у назві замість «APT».

Навіщо. Офіційний репозиторій APT gVisor (storage.googleapis.com/gvisor/releases) тримає лише
останню версію `runsc`: що саме ставить `apt-get install runsc` сьогодні — номер, розмір, шлях
до .deb, контрольні суми для amd64 і arm64 — видно тільки з самого індексу. Це власний опис
пакета менеджером пакетів, не переказ: документація лише показує команди встановлення, а
номера версії, яку вони поставлять, не знає.

Формат індексу — абзаци «Поле: значення», розділені порожнім рядком (Debian Policy, розділ
5.1). Рядок, що починається пробілом, продовжує попереднє поле; у довгому описі рядок « .»
— розрив абзацу, а перший рядок поля Description — короткий опис, тож він стає першим
абзацом окремо.
"""

import re

from engine.readers import Item, _markup, register

# Поля, які показуються списком; решта (Description) — текстом під ними. MD5sum і SHA1 —
# застарілі суми, але індекс їх дає, а людина звіряє саме те, що надрукував її apt.
_SKIP = {"Package", "Description"}
_ARCH = re.compile(r"/binary-([\w-]+)/")


def _stanzas(text: str) -> list[dict]:
    """Абзаци індексу → словники полів. Рядки продовження лишаються при полі як є (з
    відступом), бо в Description відступ і « .» мають значення."""
    out, cur, last = [], {}, ""
    for line in text.replace("\r\n", "\n").split("\n"):
        if not line.strip():
            if cur:
                out.append(cur)
            cur, last = {}, ""
            continue
        if line[:1] in (" ", "\t") and last:
            cur[last] += "\n" + line
            continue
        key, sep, value = line.partition(":")
        if sep and key and " " not in key:
            last = key.strip()
            cur[last] = value.strip()
    if cur:
        out.append(cur)
    return out


def _description(value: str) -> str:
    """Поле Description → текст: перший рядок — короткий опис, далі абзаци довгого опису.
    « .» — порожній рядок між абзацами; рядок із двома пробілами на початку — дослівний
    (Debian Policy 5.6.13), тож такі рядки лягають блоком коду."""
    first, _, rest = value.partition("\n")
    parts, verbatim, para = [first.strip()], [], []

    def flush_para():
        if para:
            parts.append(" ".join(para))
            para.clear()

    def flush_verbatim():
        if verbatim:
            parts.append("```\n" + "\n".join(verbatim) + "\n```")
            verbatim.clear()

    for line in rest.split("\n") if rest else ():
        body = line[1:] if line[:1] in (" ", "\t") else line
        if body.strip() == ".":
            flush_para()
            flush_verbatim()
        elif body.startswith(" "):
            flush_para()
            verbatim.append(body[1:])
        elif body.strip():
            flush_verbatim()
            para.append(body.strip())
    flush_para()
    flush_verbatim()
    return "\n\n".join(p for p in parts if p)


@register("apt-packages")
def apt_packages(source: dict, ctx) -> list[Item]:
    indexes = [source["url"]] + list(source.get("pages") or ())
    for url in indexes:
        if not ctx.allowed(url):
            raise SystemExit(f"{source['id']}: адреса {url} поза білим списком — "
                             f"допишіть її в `within`.")
    label = source.get("label", "APT")
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""
    # Перелік — з першого індексу: ім'я пакета, якого немає в головній архітектурі, однаково
    # потрапить, бо решта індексів читається тут же; тексти лишаються до `make`.
    texts = {url: ctx.text(url) for url in indexes}
    names: list[str] = []
    for url in indexes:
        for st in _stanzas(texts[url]):
            if st.get("Package") and st["Package"] not in names:
                names.append(st["Package"])
    if not names:
        raise SystemExit(f"{source['url']}: в індексі жодного пакета — формат змінився.")

    items = []
    for name in names:

        def make(name=name):
            entries = []
            for url in indexes:
                for st in _stanzas(texts[url]):
                    if st.get("Package") == name:
                        entries.append((url, st))
            # Новіша версія першою: індекс може тримати кілька версій одного пакета.
            versions = list(dict.fromkeys(st.get("Version", "") for _, st in entries))
            sections = []
            for url, st in entries:
                arch = st.get("Architecture") or (_ARCH.search(url) or [None, "?"])[1]
                fields = "\n".join(f"- {k}: {' '.join(v.split())}" for k, v in st.items()
                                   if k not in _SKIP)
                # Без номера в заголовку: ключ розділу лишається тим самим від версії до
                # версії, а номер і так стоїть у полях.
                text = [f"## {arch}", f"Index: {url}", fields]
                if st.get("Description"):
                    text.append(_description(st["Description"]))
                sections.append("\n\n".join(text))
            body = "\n\n".join(sections)
            title = f"{name} {versions[0]} ({label})" if versions and versions[0] else name
            _markup.require(title, body, source["url"])
            return _markup.document(title, source["url"], ctx.stamp, body,
                                    ", ".join(v for v in versions if v))

        slug = _markup.slug(name)
        items.append(Item(id=f"{source['id']}/{lead}{slug}",
                          file=f"{source['id']}--{lead}{slug}.txt", make=make))
    return items
