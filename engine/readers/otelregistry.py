"""Читач реєстру OpenTelemetry: data/registry/*.yml сайту opentelemetry.io.

`otel-registry` — записи реєстру (opentelemetry.io/ecosystem/registry) одного коміту сайту. `url` — дерево
                  коміту через API (…/repos/ВЛАСНИК/РЕПО/git/trees/<sha>?recursive=1), `ref` — той
                  самий коміт: з нього тягнеться кожен файл запису. Документ — тип запису й мова
                  (за іменем файла «instrumentation-js-express.yml»: тип «instrumentation», мова «js»),
                  розділ — один запис: назва, опис, пакет із версією, ліцензія, посилання, автори.

Навіщо. Сторінка реєстру на сайті — поле пошуку, яке скрипт заповнює з цих файлів: у тексті сайту
жодного запису немає. А саме реєстр відповідає на «чи є інструментація для mongoose», «який
експортер Collector пише в Loki», «як називається пакет для Kafka в Go». Тисяча з гаком записів
окремими документами розсипалися б на фрагменти з трьох рядків; групою за типом і мовою вони —
перелік, у якому кожен запис — свій розділ.
"""

import collections
import json
import re
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register
from engine.readers._otelhugo import yaml_subset

_TREE = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/([0-9a-f]{7,40})$")
_FILE = re.compile(r"^data/registry/([a-z0-9]+)-([a-z0-9]+)-[^/]+\.ya?ml$")
_LANGS = {"js": "JavaScript", "go": "Go", "java": "Java", "python": "Python", "dotnet": ".NET",
          "ruby": "Ruby", "php": "PHP", "rust": "Rust", "cpp": "C++", "erlang": "Erlang/Elixir",
          "swift": "Swift", "kotlin": "Kotlin", "collector": "Collector", "elixir": "Elixir"}


def _entry(data: dict) -> str:
    title = str(data.get("title") or "").strip() or "(no title)"
    lines = [f"## {title}", ""]
    facts = []
    for key, name in (("registryType", "Type"), ("language", "Language"), ("license", "License")):
        if data.get(key):
            facts.append(f"{name}: {data[key]}")
    pkg = data.get("package") if isinstance(data.get("package"), dict) else {}
    if pkg.get("name"):
        facts.append(f"Package: {pkg.get('registry', '')} `{pkg['name']}`"
                     + (f" {pkg['version']}" if pkg.get("version") else ""))
    if "isFirstParty" in data:
        facts.append("First party: " + ("yes" if str(data["isFirstParty"]).lower() == "true" else "no"))
    if data.get("isNative"):
        facts.append("Native: " + str(data["isNative"]))
    if facts:
        lines += [" · ".join(facts), ""]
    if data.get("description"):
        lines += [str(data["description"]).strip(), ""]
    urls = data.get("urls") if isinstance(data.get("urls"), dict) else {}
    if urls:
        lines += ["Links: " + "; ".join(f"{k}: {v}" for k, v in urls.items()), ""]
    authors = data.get("authors")
    if isinstance(authors, list) and authors:
        names = [a.get("name", "") if isinstance(a, dict) else str(a) for a in authors]
        lines += ["Authors: " + ", ".join(n for n in names if n), ""]
    if isinstance(data.get("tags"), list) and data["tags"]:
        lines += ["Tags: " + ", ".join(str(t) for t in data["tags"]), ""]
    if data.get("createdAt"):
        lines += [f"Added to the registry: {data['createdAt']}", ""]
    return "\n".join(lines).rstrip()


@register("otel-registry")
def otel_registry(source: dict, ctx) -> list[Item]:
    m = _TREE.match(urlsplit(source["url"]).path)
    if not m or not source.get("ref"):
        raise SystemExit(f"{source['id']}: `url` — дерево коміту (…/git/trees/<sha>?recursive=1), "
                         f"`ref` — той самий коміт.")
    owner, repo, _ = m.groups()
    ref = source["ref"]
    try:
        tree = json.loads(ctx.text(source["url"]))
    except ValueError as exc:
        raise SystemExit(f"{source['url']}: відповідь не JSON ({exc}).")
    if tree.get("truncated"):
        raise SystemExit(f"{source['url']}: GitHub обрізав дерево — перелік був би неповним.")
    groups = collections.defaultdict(list)
    for e in tree.get("tree", []):
        hit = _FILE.match(e.get("path", ""))
        if e.get("type") == "blob" and hit:
            groups[(hit.group(1), hit.group(2))].append(e["path"])
    items = []
    for (kind, lang), paths in sorted(groups.items()):
        name = f"registry-{kind}-{lang}"
        urls = [f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{quote(p)}" for p in sorted(paths)]
        urls = [u for u in urls if ctx.allowed(u)]
        if not urls:
            continue
        page = (f"https://opentelemetry.io/ecosystem/registry/?component={quote(kind)}"
                f"&language={quote(lang)}")

        def make(urls=urls, kind=kind, lang=lang, page=page):
            entries = []
            for u in urls:
                data = yaml_subset(ctx.text(u))
                if isinstance(data, dict) and data.get("title"):
                    entries.append((str(data["title"]).lower(), _entry(data)))
            body = "\n\n".join(e for _, e in sorted(entries))
            title = f"OpenTelemetry Registry: {kind} — {_LANGS.get(lang, lang)}"
            _markup.require(title, body, page, min_chars=1)
            return _markup.document(title, page, ctx.stamp, body, "")

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: у дереві немає жодного data/registry/*.yml.")
    return items
