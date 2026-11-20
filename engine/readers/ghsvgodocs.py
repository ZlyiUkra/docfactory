"""Читач документації SVGO: параметри плагіна з шапки YAML сторінки стають текстом.

`ghdocs-history-svgo` — те саме, що `ghdocs-history` (поля `url`, `tags`, `folders`, `recursive`,
                        `extensions`, `site`, `mdx`, `admonitions`, `docusaurus_tabs`, `name_prefix` …), і
                        одна різниця: у файлі `.mdx` з raw.githubusercontent.com блок `svgo:` шапки YAML
                        перед розбором переноситься в текст сторінки.

Навіщо. Сторінка плагіна на svgo.dev — це два абзаци опису, а найважливіше лежить у шапці файла:

    svgo:
      pluginId: cleanupIds
      defaultPlugin: true
      parameters:
        remove:
          description: If to remove all unreferenced IDs.
          default: true

Сайт малює з цього таблицю параметрів і позначку «входить у preset-default». Спільний читач шапку
знімає й бере з неї лише назву, тож сторінка `cleanupIds` лишалася б без жодного параметра, а саме про
параметри плагінів і питають найчастіше.

Що стає текстом: під назвою — рядок з ідентифікатором плагіна і, коли в шапці стоїть
`defaultPlugin: true`, реченням про те, що плагін увімкнено у `preset-default`; наприкінці — розділ
«Parameters» з рядком на параметр: ім'я, опис, тип і типове значення. Типове значення, записане
переліком YAML (`sortAttrs`: порядок атрибутів), зводиться в один рядок у квадратних дужках.

Розбір шапки власний і вузький: бібліотеки YAML у проєкті немає, а блок `svgo:` має одну форму —
ключі на відступах 2, 4 і 6 пробілів і перелік глибше. Рядок, що в цю форму не вкладається, зупиняє
читача з помилкою, а не пропускається мовчки: пропущений параметр у довіднику гірший за зупинку.

Чому обгортка, а не поле в `ghdocs-history`: перелік тегів, імена документів і версії той читач
складає сам і звірений у десятках примірників. Тут лише текст файла міняється дорогою.
"""

import re
from urllib.parse import urlsplit

from engine.readers import register
from engine.readers.ghhistory import ghdocs_history

_FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)
_KEY = re.compile(r"^( *)([A-Za-z_][\w-]*):(?: (.*))?$")
_ITEM = re.compile(r"^ +- (.*)$")


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def _svgo_block(lines: list, where: str) -> tuple[dict, list]:
    """(поля плагіна, параметри) з рядків блоку `svgo:`; параметр — [ім'я, {ключ: значення чи перелік}]."""
    plugin: dict = {}
    params: list = []
    last = None            # (словник, ключ), куди лягають пункти переліку
    for ln in lines:
        if not ln.strip():
            continue
        item = _ITEM.match(ln)
        if item and last:
            box, key = last
            if not isinstance(box.get(key), list):
                box[key] = []
            box[key].append(item.group(1).strip())
            continue
        m = _KEY.match(ln)
        if not m:
            raise SystemExit(f"{where}: рядок шапки `svgo:` не розібрано — {ln!r}.")
        depth, key, value = len(m.group(1)), m.group(2), (m.group(3) or "").strip()
        if depth == 2:
            plugin[key] = value
            last = None
        elif depth == 4:
            params.append([key, {}])
            last = None
        elif depth == 6 and params:
            params[-1][1][key] = value
            last = (params[-1][1], key)
        else:
            raise SystemExit(f"{where}: несподіваний відступ у шапці `svgo:` — {ln!r}.")
    return plugin, params


def _value(value) -> str:
    if isinstance(value, list):
        return "[" + ", ".join(value) + "]"
    return value


def svgo_page(text: str, where: str = "") -> str:
    """Сторінка `.mdx` з блоком `svgo:` у шапці → та сама сторінка з параметрами в тексті."""
    text = text.replace("\r\n", "\n")
    m = _FRONT.match(text)
    if not m or "\nsvgo:" not in "\n" + m.group(1):
        return text
    head, block, inside = [], [], False
    for ln in m.group(1).split("\n"):
        if ln.startswith("svgo:"):
            inside = True
        elif inside and (ln.startswith(" ") or not ln.strip()):
            block.append(ln)
        else:
            inside = False
            head.append(ln)
    plugin, params = _svgo_block(block, where)
    lead = []
    if plugin.get("pluginId"):
        lead.append(f"Plugin ID: `{_unquote(plugin['pluginId'])}`.")
    if plugin.get("defaultPlugin") == "true":
        lead.append("This plugin is enabled by default: it is part of `preset-default`.")
    tail = []
    for name, fields in params:
        parts = [f"- `{name}`"]
        if fields.get("description"):
            parts.append(f" — {_unquote(_value(fields['description']))}")
        extra = []
        if fields.get("type"):
            extra.append(f"Type: `{_unquote(_value(fields['type']))}`.")
        if "default" in fields and _value(fields["default"]) != "":
            extra.append(f"Default: `{_value(fields['default'])}`.")
        tail.append("".join(parts) + (" " + " ".join(extra) if extra else ""))
    body = text[m.end():].strip("\n")
    out = ["---", *head, "---", ""]
    if lead:
        out += [" ".join(lead), ""]
    out.append(body)
    if tail:
        out += ["", "## Parameters", "", *tail]
    return "\n".join(out) + "\n"


class _SvgoCtx:
    """`ctx`, що віддає сторінки плагінів SVGO з параметрами в тексті; решта звернень — до справжнього."""

    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        parts = urlsplit(url)
        if parts.netloc == "raw.githubusercontent.com" and parts.path.endswith((".mdx", ".md")):
            return svgo_page(text, url)
        return text


@register("ghdocs-history-svgo")
def ghdocs_history_svgo(source: dict, ctx) -> list:
    return ghdocs_history(source, _SvgoCtx(ctx))
