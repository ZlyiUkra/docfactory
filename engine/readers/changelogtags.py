"""Читач простого текстового журналу змін на тегах гілок випусків: «version 7.1.5:».

`changelog-tags` — `raw`      — корінь сирих файлів (https://raw.githubusercontent.com/ВЛАСНИК/РЕПО/);
                   `blob`     — корінь людських адрес (https://github.com/ВЛАСНИК/РЕПО/blob/);
                   `file`     — шлях журналу в репозиторії («Changelog»);
                   `versions` — теги, з яких читається журнал, від найновішого;
                   `tag_prefix` — що зрізати з тегу, щоб лишилась версія («n»);
                   `label`    — підпис у назві документа («FFmpeg»).

Навіщо. FFmpeg пише журнал без markdown: рядок «version 7.1.5:», під ним перелік. Записи
точкових випусків (7.1.1…7.1.5 — назви комітів-виправлень) є лише в журналі своєї гілки
випусків: гілка 8.0 не знає про 7.1.5. Тому журнал читається з останнього тегу кожної
гілки, а запис мажорного випуску («version 7.1:» — нові можливості) повторюється в
журналах усіх пізніших гілок.

Одиниця — запис однієї версії. Запис береться з першого журналу, де він трапився, якщо
йти від найстарішого тегу: запис з'являється вперше у власній гілці, тож береться саме
звідти, а повтори в пізніших журналах відкидаються. Беруться лише сталі номери — цифри
через крапку: «version 0.4.9-pre1:» і «version <next>:» (заготовка гілки розробки) — ні.

Запис починається заголовком «## version 7.1», як рядок журналу: без заголовка документ не
має жодного розділу, і ні пошук, ні замір не можуть назвати його розділом. Рядки запису
стають пунктами, і кожні 15 пунктів відділяються порожнім рядком: запис точкового випуску
буває на сотні комітів, а фрагмент ріже текст лише по порожніх рядках.
Перелік читає журнал кожного тегу одразу (версії видно тільки з тексту), але в пам'яті
лишаються тільки тег і версії: текст читається вдруге під час запису.
"""

import re

from engine.readers import Item, _markup, register

_VERSION = re.compile(r"^version\s+(\S+?):?\s*$", re.M)
_STABLE = re.compile(r"^\d+(?:\.\d+)+$")


def entries(text: str) -> dict[str, str]:
    """Версія → рядки її запису (лише сталі номери)."""
    text = text.replace("\r\n", "\n")
    marks = list(_VERSION.finditer(text))
    out = {}
    for k, m in enumerate(marks):
        end = marks[k + 1].start() if k + 1 < len(marks) else len(text)
        version = m.group(1).rstrip(":")
        if _STABLE.match(version) and version not in out:
            out[version] = text[m.end():end].strip("\n")
    return out


def _body(lines: str) -> str:
    items, out = [], []
    for ln in lines.split("\n"):
        if not ln.strip():
            continue
        if ln.startswith((" ", "\t")) and items and not ln.lstrip().startswith("-") \
                and items[-1].startswith("-") and ln.startswith("  "):
            items[-1] += " " + ln.strip()          # продовження пункту «- …» з відступом
            continue
        stripped = ln.strip()
        items.append(stripped if stripped.startswith("-") else f"- {stripped}")
    for k in range(0, len(items), 15):
        out.append("\n".join(items[k:k + 15]))
    return "\n\n".join(out)


@register("changelog-tags")
def changelog_tags(source: dict, ctx) -> list[Item]:
    need = ("raw", "blob", "file", "versions")
    if any(not source.get(k) for k in need):
        raise SystemExit(f"{source['id']}: читач changelog-tags потребує полів {', '.join(need)}.")
    raw_base, blob_base = source["raw"].rstrip("/") + "/", source["blob"].rstrip("/") + "/"
    path, prefix, label = source["file"].strip("/"), source.get("tag_prefix", ""), \
        source.get("label", "")
    owner: dict[str, str] = {}                      # версія → тег, з журналу якого її брати
    for tag in reversed(source["versions"]):
        url = f"{raw_base}{tag}/{path}"
        if not ctx.allowed(url):
            raise SystemExit(f"{url}: поза білим списком.")
        for version in entries(ctx.text(url)):
            owner.setdefault(version, tag)
    if not owner:
        raise SystemExit(f"{source['id']}: у журналах жодного запису «version X.Y:».")
    items = []
    for version, tag in owner.items():
        def make(version=version, tag=tag):
            text = entries(ctx.text(f"{raw_base}{tag}/{path}")).get(version)
            if text is None:
                raise SystemExit(f"{tag}/{path}: запису {version} вже немає — не записую.")
            body = _body(text) or "No entries."
            tagged = tag[len(prefix):] if prefix and tag.startswith(prefix) else tag
            head = f"## version {version}\n\nFrom the {path} of the {tagged} release."
            title = f"{label} {path}: version {version}".strip()
            return _markup.document(title, f"{blob_base}{tag}/{path}", ctx.stamp,
                                    f"{head}\n\n{body}", version)

        name = f"changelog-{version}"
        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    return items
