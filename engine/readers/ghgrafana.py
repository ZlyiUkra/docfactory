"""Читач історії документації Grafana: сторінки `docs/sources` з вставками Hugo сайту grafana.com.

`ghdocs-history-grafana` — те саме, що `ghdocs-history` (усі його поля), плюс перед розбором
                           кожна сторінка `.md` проходить заміни:
                           - шапка TOML (`+++` … `+++`, документація 2.x–6.x) стає шапкою YAML;
                           - `{{< docs/shared lookup="x.md" source="grafana" >}}` — шматок теки
                             `docs/sources/shared` того самого тегу стає на місце вставки;
                             шматки інших продуктів (`source="alloy"`) лежать поза білим
                             списком і випадають;
                           - `{{< admonition type="note" >}}` стає підписом «Note:», вкладки
                             (`tab-content name`), розгортки (`collapse title`) і питання
                             (`qa question`) — підписом зі своєю назвою;
                           - блоки `{{% docs/reference %}}` (визначення посилань для сайту)
                             знімаються цілком, решта вставок — лише самі дужки.

Навіщо. Сторінка в репозиторії — не те, що бачить людина на grafana.com: спільні шматки
(кроки налаштування джерел даних, застарілі API, вимоги до SSO) записані вставкою, і без неї
на сторінці лишався б заголовок без жодного рядка. Без підпису виноски застереження «не
вмикайте це в продукції» зливалося б із сусіднім абзацом. Документація до 7.0 писала шапку в
TOML, і назвою ставало ім'я файла, а рядки `title = …` лягали першим абзацом.

Шматки беруться з того самого тегу, що й сторінка, а вміст тягнеться один раз на хеш blob:
дерево тегу читач однаково завантажує, обгортка лише запам'ятовує з нього хеші теки
`shared`. Чому окремий модуль, а не поле в `ghdocs-history`, — див. `ghtoml`.
"""

import json
import re

from engine.readers import _markup, register
from engine.readers.ghhistory import ghdocs_history
from engine.readers.ghtoml import _yaml_front

SHARED = "docs/sources/shared/"

_RAW_PAGE = re.compile(r"^https://raw\.githubusercontent\.com/[^/]+/[^/]+/([^/]+)/(.+)$")
_TREE = re.compile(r"/git/trees/([^/?]+)")
_SC_SHARED = re.compile(r"\{\{[<%]\s*docs/shared\b(.*?)[>%]\}\}", re.S)
_SC_ADMONITION = re.compile(r"\{\{[<%]\s*admonition\b(.*?)[>%]\}\}", re.S)
_SC_LABEL = re.compile(r'\{\{[<%]\s*(?:tab-content\s+name|collapse\s+title|qa\s+question)'
                       r'="([^"]*)"[^}]*[>%]\}\}')
_SC_REFERENCE = re.compile(r"\{\{[<%]\s*docs/reference\s*[>%]\}\}.*?"
                           r"\{\{[<%]\s*/docs/reference\s*[>%]\}\}", re.S)
_SC_IN_LINK = re.compile(r"\]\(\s*\{\{[<%].*?[>%]\}\}\s*\)")
_SC_ANY = re.compile(r"\{\{[<%].*?[>%]\}\}", re.S)
_ARG = re.compile(r'(?:(\w+)=)?"([^"]*)"')


class _Grafana:
    """Обгортка контексту: сторінки `.md` віддає вже з розкритими вставками, усе інше
    (дерева тегів) — як є, лише запам'ятавши хеші шматків `shared` кожного тегу."""

    def __init__(self, ctx):
        self._ctx = ctx
        self._shared: dict = {}
        self._pieces: dict = {}

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def _piece(self, owner_repo: str, tag: str, path: str) -> str:
        sha = self._shared.get(tag, {}).get(path)
        key = sha or (tag, path)
        if key not in self._pieces:
            url = f"https://raw.githubusercontent.com/{owner_repo}/{tag}/{path}"
            text = ""
            if self._ctx.allowed(url):
                code, data = self._ctx.fetch(url)
                text = data.decode("utf-8", errors="replace") if code == "200" else ""
            self._pieces[key] = _markup.front_matter(_yaml_front(text.replace("\r\n", "\n")))[1]
        return self._pieces[key]

    def _expand(self, text: str, owner_repo: str, tag: str, depth: int = 0) -> str:
        def shared(m):
            args = {k or "": v for k, v in _ARG.findall(m.group(1))}
            path = (args.get("lookup") or args.get("") or "").lstrip("/")
            if not path or args.get("source", "grafana") != "grafana" or depth >= 3:
                return ""
            piece = self._piece(owner_repo, tag, SHARED + path)
            return "\n" + self._expand(piece, owner_repo, tag, depth + 1) + "\n" if piece else ""

        def admonition(m):
            kind = re.search(r'type="(\w+)"', m.group(1))
            return f"{kind.group(1).capitalize() if kind else 'Note'}:"

        text = _SC_REFERENCE.sub("", text)
        text = _SC_SHARED.sub(shared, text)
        text = _SC_ADMONITION.sub(admonition, text)
        text = _SC_LABEL.sub(lambda m: f"\n\n{m.group(1)}:\n\n", text)
        text = _SC_IN_LINK.sub("](#)", text)
        return _SC_ANY.sub("", text)

    def text(self, url: str, gzip: bool = False, accept: str = "") -> str:
        text = self._ctx.text(url, gzip, accept)
        tree = _TREE.search(url)
        if tree and "api.github.com" in url:
            try:
                entries = json.loads(text).get("tree", [])
            except ValueError:
                entries = []
            self._shared[tree.group(1)] = {e["path"]: e["sha"] for e in entries
                                           if e.get("path", "").startswith(SHARED)}
            return text
        page = _RAW_PAGE.match(url)
        if not page or not page.group(2).endswith(".md"):
            return text
        owner_repo = "/".join(url.split("/")[3:5])
        meta_text = _yaml_front(text.replace("\r\n", "\n"))
        return self._expand(meta_text, owner_repo, page.group(1))


@register("ghdocs-history-grafana")
def ghdocs_history_grafana(source: dict, ctx) -> list:
    return ghdocs_history(source, _Grafana(ctx))
