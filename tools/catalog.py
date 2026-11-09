"""Каталог примірників: який сервер підняти під конкретну розробку.

    python3 tools/catalog.py            # звірити порти й записати docs/instances.md
    python3 tools/catalog.py --check    # лише звірити, нічого не записувати

Навіщо. Примірників майже двісті, і вибрати потрібні за назвами неможливо: треба бачити, коли
кожен потрібен, що в ньому є і чого немає. Опис береться з самих примірників (`prompts/loaded.txt`,
README, `config.json`), тому не розходиться з ними. Людиною написано лише те, чого в примірнику
немає: тему й рядок «коли піднімати» у `docs/instance-topics.json`. Примірник без такого рядка
зупиняє запис: інакше новий примірник тихо випав би з вибору.

Порт перевіряється тут же, бо два сервери на одному порту не піднімуться разом, а помилка
з'явилася б лише в ту мить, коли обидва потрібні.
"""

import collections
import json
import os
import pathlib
import posixpath
import re
import sys
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
INSTANCES = ROOT / "instances"
TOPICS = ROOT / "docs" / "instance-topics.json"
OUT = ROOT / "docs" / "instances.md"
WIDTH = 118
# Заголовки README, які допомагають обрати. Решта (установка, збирання, архів) вибору не стосується.
LIMITS = "Межі"
# Відносне посилання README: у каталозі воно мусить вести туди ж, хоч файл лежить в іншій теці.
_LINK = re.compile(r"\]\((?!https?:|#|mailto:)([^)\s]+)\)")
_PLACEHOLDER = re.compile(r"[^.]*\{\w+\}[^.]*\.?\s*")
_OPENING = re.compile(r"^Loaded right now:\s*\{excerpts\} excerpts from \{documents\} documents\s*")


def load() -> dict:
    out = {}
    for path in sorted(INSTANCES.glob("*/config.json")):
        out[path.parent.name] = json.loads(path.read_text(encoding="utf-8"))
    return out


def problems(configs: dict, topics: dict) -> list:
    """Усе, через що сервери не піднімуться разом або вибір буде неповним."""
    found = []
    for field in ("port", "server_name", "collection"):
        groups = collections.defaultdict(list)
        for name, config in configs.items():
            groups[config.get(field)].append(name)
        found += [f"спільне значення {field}={value}: {', '.join(names)}"
                  for value, names in groups.items() if value is None or len(names) > 1]
    ports = {config["server_name"]: config["port"] for config in configs.values()}
    for name, config in configs.items():
        servers = _servers(name)
        if config["server_name"] not in servers:
            found.append(f"{name}: у .mcp.json немає власного сервера {config['server_name']}")
        for server, port in servers.items():
            if server not in ports:
                found.append(f"{name}: .mcp.json називає невідомий сервер {server}")
            elif ports[server] != port:
                found.append(f"{name}: .mcp.json дає {server} порт {port}, а в config.json {ports[server]}")
    named = [name for group in topics.values() for name in group]
    found += [f"{name}: немає рядка в {TOPICS.name}" for name in sorted(set(configs) - set(named))]
    found += [f"{name}: є в {TOPICS.name}, але такого примірника немає"
              for name in sorted(set(named) - set(configs))]
    found += [f"{name}: двічі в {TOPICS.name}"
              for name, count in collections.Counter(named).items() if count > 1]
    return found


def _servers(name: str) -> dict:
    data = json.loads((INSTANCES / name / ".mcp.json").read_text(encoding="utf-8"))
    out = {}
    for server, entry in data.get("mcpServers", {}).items():
        found = re.search(r":(\d+)/", entry.get("url", ""))
        out[server] = int(found.group(1)) if found else None
    return out


def _inside(name: str) -> str:
    """Опис для моделі без чисел під час роботи: їх сервер підставляє сам, тут вони порожні."""
    text = " ".join((INSTANCES / name / "prompts" / "loaded.txt").read_text(encoding="utf-8").split())
    text = _OPENING.sub("Documents ", text)
    return " ".join(_PLACEHOLDER.sub(" ", text).split())


def _relink(text: str, name: str) -> str:
    def fix(found):
        target = posixpath.normpath(posixpath.join("../instances", name, found.group(1)))
        return f"]({target})"
    return _LINK.sub(fix, text)


def _readme(name: str) -> tuple[str, str, list]:
    """(вступ, розділ про межі, назви розділів) README примірника."""
    text = (INSTANCES / name / "README.md").read_text(encoding="utf-8")
    parts = re.split(r"^## ", text, flags=re.M)
    intro = " ".join(parts[0].split("\n", 1)[1].split()) if "\n" in parts[0] else ""
    limits = ""
    for part in parts[1:]:
        if part.startswith(LIMITS):
            limits = part.split("\n", 1)[1].strip() if "\n" in part else ""
            break
    return _relink(intro, name), _relink(limits, name), [p.split("\n", 1)[0].strip() for p in parts[1:]]


def _wrap(text: str) -> str:
    return textwrap.fill(text, WIDTH, break_long_words=False, break_on_hyphens=False)


def _count(name: str) -> tuple[int, object]:
    passport = json.loads((INSTANCES / name / "corpus" / "index.json").read_text(encoding="utf-8"))
    checks = json.loads((INSTANCES / name / "checks.json").read_text(encoding="utf-8"))
    return len(passport.get("documents", ())), checks.get("expected_passages")


def _number(value) -> str:
    return f"{value:,}".replace(",", " ") if isinstance(value, int) else "не записано"


def card(name: str, config: dict, when: str, configs: dict) -> str:
    documents, passages = _count(name)
    intro, limits, sections = _readme(name)
    lines = [f"### {name}", "", f"**Коли піднімати.** {when}", "",
             f"**Порт** {config['port']}, сервер `{config['server_name']}`. "
             f"Підняти: `./df {name} serve`. Адреса: `http://127.0.0.1:{config['port']}/mcp`.", "",
             f"**Обсяг.** Документів: {_number(documents)}, фрагментів: {_number(passages)}.", ""]
    family = {s: p for s, p in _servers(name).items() if s != config["server_name"]}
    if family:
        lines += [_wrap("**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: "
                        + ", ".join(f"`{s}` ({p})" for s, p in sorted(family.items())) + "."), ""]
    if intro:
        lines += ["**Опис.**", "", _wrap(intro), ""]
    inside = _inside(name)
    if inside:
        lines += ["**Склад (так його описано моделі, англійською).**", "", _wrap(inside), ""]
    if limits:
        lines += ["**Межі.**", "", limits, ""]
    lines += [_wrap(f"**Далі в [README](../instances/{name}/README.md):** " + "; ".join(sections) + "."), ""]
    return "\n".join(lines)


def render(configs: dict, topics: dict) -> str:
    ports = sorted(config["port"] for config in configs.values())
    free = sorted(set(range(ports[0], ports[-1] + 1)) - set(ports))
    head = [
        "# Каталог примірників",
        "",
        "Цей файл збирає `python3 tools/catalog.py`, руками його не правлять. Рядки «Коли піднімати» лежать у",
        "`docs/instance-topics.json`, а все інше береться з теки кожного примірника.",
        "",
        f"Примірників: {len(configs)}. Кожен має власний порт, власну назву сервера й власну колекцію Qdrant, тому",
        "їх можна піднімати в будь-якому поєднанні. Скрипт перевіряє це щоразу й без цього файл не запише.",
        f"Зайняті порти: {ports[0]}–{ports[-1]}" + (f", вільний усередині: {', '.join(map(str, free))}" if free else "")
        + f". Наступний новий: {ports[-1] + 1}.",
        "",
        "## Як обирати",
        "",
        "1. Назвіть, що розробляєте. Перегляньте таблиці теми нижче й випишіть примірники, чий рядок підходить.",
        "2. Прочитайте картку кожного кандидата в другій частині файла: там є склад і межі примірника.",
        "3. Кожен сервер запускають окремою командою `./df <примірник> serve` в окремому терміналі. Кілька серверів",
        "   разом піднімає з одного термінала `tools/up.sh <примірник> <примірник> …`: він показує виклики до них",
        "   і після Ctrl+C зупиняє всі. Як ним користуватися — README, розділ «Як підняти локальний MCP-сервер».",
        "4. Якщо в картці є рядок «Родина», підніміть і названі там сервери, інакше частину питань не буде кому",
        "   відповісти.",
        "",
        "Кожен запущений сервер тримає в пам'яті фрагменти свого примірника, тому чим більше число фрагментів, тим",
        "більше пам'яті він забере. Вектори лежать у контейнері Qdrant, і він має працювати для всіх серверів.",
        "",
        "## Вибір за темою",
        "",
    ]
    tables, cards = [], ["## Картки", ""]
    for topic, group in topics.items():
        tables += [f"### {topic}", "", "| Примірник | Порт | Коли піднімати |", "|---|---:|---|"]
        cards += [f"<!-- тема: {topic} -->", ""]
        for name, when in group.items():
            tables.append(f"| [`{name}`](#{name}) | {configs[name]['port']} | {when} |")
            cards.append(card(name, configs[name], when, configs))
        tables.append("")
    return "\n".join(head + tables + cards).rstrip() + "\n"


def main() -> int:
    configs = load()
    topics = json.loads(TOPICS.read_text(encoding="utf-8"))
    found = problems(configs, topics)
    for line in found:
        print(line)
    if found:
        print(f"Проблем: {len(found)}. Каталог не записано.")
        return 1
    print(f"Примірників {len(configs)}: порти, сервери й колекції не повторюються.")
    if "--check" in sys.argv[1:]:
        return 0
    tmp = OUT.with_suffix(".md.new")
    tmp.write_text(render(configs, topics), encoding="utf-8")
    os.replace(tmp, OUT)
    print(f"Записано {OUT.relative_to(ROOT)}: {OUT.stat().st_size // 1024} КБ.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
