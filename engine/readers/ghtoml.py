"""Читач історії документації сайту Hugo, чиї сторінки мають шапку TOML (`+++`).

`ghdocs-history-toml` — те саме, що `ghdocs-history` (усі його поля), плюс перед розбором
                        кожна сторінка проходить три заміни:
                        - шапка TOML на початку файла (`+++` … `+++`, рядки `ключ = значення`)
                          стає шапкою YAML (`---`, `ключ: значення`);
                        - вставка `{{< ім'я >}}`, чий шаблон у `layouts/shortcodes/ім'я.html` —
                          рівно `{{ .Site.Params.vars.ім'я }}`, стає значенням із таблиці
                          `[params.vars]` файла `config.toml` того самого знімка;
                        - вставка графіка `{{< graph … title="…" >}}` стає рядком «Graph: …».

Навіщо. Архівний сайт gvisor.dev 2019–2020 (репозиторій google/gvisor-website, Hugo з темою
Docsy) пише шапку сторінки в TOML: `+++ / title = "Installation" / weight = 20 / +++`.
`ghdocs-history` знає лише YAML-шапку, тож назвою ставало ім'я файла («install»), а рядки
`title = …` і `weight = …` лягали першим абзацом тексту. Вимога до ядра Linux на сторінках
встановлення й FAQ записана вставкою `{{< required_linux >}}`, значення якої живе в
конфігурації сайту, а не в шаблоні: без підстановки речення «requires Linux 4.14.77+»
втрачало саме номер. Графіки сторінки продуктивності — дані з CSV, у тексті від них лишається
підпис: назва бенчмарка й прапорці запуску.

Чому окремий модуль, а не поле в `ghdocs-history`: примірники з тим читачем зібрані й
звірені, а правка спільного читача — ризик зсуву в готовій роботі. Розбір той самий — його й
викликано; заміни робить обгортка контексту, через яку читач бере текст сторінки.
"""

import re

from engine.readers import register
from engine.readers.ghhistory import ghdocs_history

_TOML_FRONT = re.compile(r"\A﻿?\+\+\+[ \t]*\n(.*?)\n\+\+\+[ \t]*(?:\n|\Z)", re.S)
_TOML_PAIR = re.compile(r"^([A-Za-z_][\w-]*)\s*=\s*(.*?)\s*$")
_RAW_PAGE = re.compile(r"^(https://raw\.githubusercontent\.com/[^/]+/[^/]+/[^/]+/)(.+)$")
_BARE = re.compile(r"\{\{<\s*([a-z][\w-]*)\s*/?>\}\}")
_GRAPH = re.compile(r"\{\{<\s*graph\b([^}]*)>\}\}")
_VAR_TEMPLATE = re.compile(r"\A\s*\{\{\s*\.Site\.Params\.vars\.([\w-]+)\s*\}\}\s*\Z")


def _yaml_front(text: str) -> str:
    """Шапка TOML → шапка YAML. Беруться лише прості пари: таблиці (`[menu.main]`) і масиви
    на кілька рядків читачеві не потрібні, а розбирач шапки ядра їх однаково не знає."""
    m = _TOML_FRONT.match(text)
    if not m:
        return text
    pairs = []
    for line in m.group(1).splitlines():
        p = _TOML_PAIR.match(line)
        if p:
            pairs.append(f"{p.group(1)}: {p.group(2)}")
    return "---\n" + "\n".join(pairs) + "\n---\n" + text[m.end():]


def _vars(config: str) -> dict:
    """Пари таблиці `[params.vars]` файла config.toml: ім'я → значення без лапок."""
    out, inside = {}, False
    for line in config.splitlines():
        s = line.strip()
        if s.startswith("["):
            inside = s == "[params.vars]"
            continue
        p = _TOML_PAIR.match(s) if inside else None
        if p:
            out[p.group(1)] = p.group(2).strip('"').strip("'")
    return out


class _Hugo:
    """Обгортка контексту: сторінки `.md` віддає вже з шапкою YAML і розкритими вставками,
    усе інше (дерева тегів, шаблони, config.toml) — як є."""

    def __init__(self, ctx):
        self._ctx = ctx
        self._config: dict = {}
        self._templates: dict = {}

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def _fetch(self, url: str) -> str:
        if not self._ctx.allowed(url):
            return ""
        code, data = self._ctx.fetch(url)
        return data.decode("utf-8", errors="replace") if code == "200" else ""

    def _value(self, base: str, name: str) -> str | None:
        key = (base, name)
        if key not in self._templates:
            m = _VAR_TEMPLATE.match(self._fetch(f"{base}layouts/shortcodes/{name}.html"))
            if m and base not in self._config:
                self._config[base] = _vars(self._fetch(f"{base}config.toml"))
            self._templates[key] = self._config.get(base, {}).get(m.group(1)) if m else None
        return self._templates[key]

    def text(self, url: str, gzip: bool = False, accept: str = "") -> str:
        text = self._ctx.text(url, gzip, accept)
        page = _RAW_PAGE.match(url)
        if not page or not page.group(2).endswith(".md"):
            return text
        base = page.group(1)
        text = _yaml_front(text.replace("\r\n", "\n"))

        def graph(m):
            title = re.search(r'title="([^"]*)"', m.group(1))
            return f"Graph: {title.group(1)}" if title else ""

        def bare(m):
            value = self._value(base, m.group(1))
            return m.group(0) if value is None else value

        return _BARE.sub(bare, _GRAPH.sub(graph, text))


@register("ghdocs-history-toml")
def ghdocs_history_toml(source: dict, ctx) -> list:
    return ghdocs_history(source, _Hugo(ctx))
