"""Читач індексу APT, що тримає всі випущені версії пакетів: документ на пакет із переліком версій.

`apt-packages-versions` — `url` — індекс `Packages` репозиторію Debian; `pages` — індекси тих
                          самих пакетів для інших архітектур. `packages` — імена пакетів, що
                          беруться (без поля — усі). Документ — пакет: назва «<пакет> <найновіша
                          версія> (APT)», першим абзацом — опис пакета, далі розділ найновішої
                          версії на кожну архітектуру з полями керування (Depends, Breaks, Replaces,
                          Size, Filename, SHA256…) і розділ «Versions» — кожна версія індексу від
                          найновішої з її залежностями, розміром і файлом .deb. Мітки версій документа
                          — номери без ревізії Debian («1.20.1-1» → «1.20.1»). Необов'язкові:
                          `version_prefix` — рядок перед номером у мітці, або об'єкт «пакет →
                          рядок» (архівні пакети з власною нумерацією); `name_prefix` — рядок перед
                          іменем документа; `label` — підпис у назві замість «APT».

Навіщо. Репозиторій libnvidia-container (nvidia.github.io/libnvidia-container/stable/deb) тримає не
останню версію, як репозиторій gVisor, а всі: 28 версій кожного пакета від 1.14.0 до 1.20.1, і
впорядковані вони від найстарішої. `apt-packages` бере назву з першого запису, тож документ казав
би «nvidia-container-toolkit 1.14.0-1» — найстарішу версію за ту, що ставить `apt-get install`, а
28 однакових розділів «amd64» різнилися б лише полями, без номера в заголовку. Тут найновіша версія
— за номером, а не за місцем в індексі, і перелік версій з їхніми залежностями — одним розділом:
«яка версія `libnvidia-container-tools` потрібна toolkit 1.17.8» видно в одному рядку.

Чому окремий модуль: `apt-packages` звірено в gvisor, а правка спільного читача — ризик зсуву в
готовій роботі. Розбір індексу й опису той самий — його й викликано.
"""

import re

from engine.readers import Item, _markup, register
from engine.readers.aptpackages import _ARCH, _SKIP, _description, _stanzas

# Поля рядка версії в переліку: що змінюється від версії до версії. Контрольні суми й Breaks/Replaces
# стоять у розділі найновішої версії: у кожному з 28 рядків вони роздули б перелік учетверо.
_BRIEF = ("Depends", "Size", "Filename")
_REVISION = re.compile(r"-[^-]+$")


def _key(version: str) -> tuple:
    """Ключ порівняння версії Debian за числами: «1.20.0-1» > «1.9.0-1», а «1.17.10» > «1.17.9»."""
    return tuple(int(n) for n in re.findall(r"\d+", version.split(":")[-1]))


@register("apt-packages-versions")
def apt_packages_versions(source: dict, ctx) -> list[Item]:
    indexes = [source["url"]] + list(source.get("pages") or ())
    for url in indexes:
        if not ctx.allowed(url):
            raise SystemExit(f"{source['id']}: адреса {url} поза білим списком — "
                             f"допишіть її в `within`.")
    label = source.get("label", "APT")
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""
    wanted = list(source.get("packages") or ())
    prefixes = source.get("version_prefix") or ""
    texts = {url: ctx.text(url) for url in indexes}
    names: list[str] = []
    for url in indexes:
        for st in _stanzas(texts[url]):
            name = st.get("Package")
            if name and name not in names and (not wanted or name in wanted):
                names.append(name)
    missing = [n for n in wanted if n not in names]
    if missing or not names:
        raise SystemExit(f"{source['url']}: в індексі немає пакетів {missing or wanted} — "
                         f"формат чи склад репозиторію змінився.")

    items = []
    for name in names:
        prefix = prefixes.get(name, "") if isinstance(prefixes, dict) else prefixes

        def make(name=name, prefix=prefix):
            entries = [(url, st) for url in indexes for st in _stanzas(texts[url])
                       if st.get("Package") == name]
            entries.sort(key=lambda e: _key(e[1].get("Version", "")), reverse=True)
            versions = list(dict.fromkeys(st.get("Version", "") for _, st in entries
                                          if st.get("Version")))
            newest = versions[0] if versions else ""
            parts = []
            first = next((st for _, st in entries if st.get("Description")), None)
            if first:
                parts.append(_description(first["Description"]))
            for url, st in entries:
                if st.get("Version", "") != newest:
                    continue
                arch = st.get("Architecture") or (_ARCH.search(url) or [None, "?"])[1]
                fields = "\n".join(f"- {k}: {' '.join(v.split())}" for k, v in st.items()
                                   if k not in _SKIP)
                # Без номера в заголовку: ключ розділу лишається тим самим від версії до версії.
                parts.append(f"## {arch}\n\nIndex: {url}\n\n{fields}")
            lines = []
            for url, st in entries:
                brief = "; ".join(f"{k}: {' '.join(st[k].split())}" for k in _BRIEF if st.get(k))
                lines.append(f"- {st.get('Version', '?')} — {brief}")
            parts.append("## Versions\n\nEvery version this repository index holds, newest "
                         "first:\n\n" + "\n".join(lines))
            body = "\n\n".join(parts)
            title = f"{name} {newest} ({label})" if newest else f"{name} ({label})"
            _markup.require(title, body, source["url"])
            labels = list(dict.fromkeys(prefix + _REVISION.sub("", v) for v in versions))
            return _markup.document(title, source["url"], ctx.stamp, body, ", ".join(labels))

        slug = _markup.slug(name)
        items.append(Item(id=f"{source['id']}/{lead}{slug}",
                          file=f"{source['id']}--{lead}{slug}.txt", make=make))
    return items
