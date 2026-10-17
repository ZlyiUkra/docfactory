"""Читач офіційного набору тестів JSON Schema: один файл тестів — один документ з розділом на групу.

`json-test-suite` — `url` — дерево коміту репозиторію json-schema-org/JSON-Schema-Test-Suite через
                    API (…/repos/ВЛАСНИК/РЕПО/git/trees/SHA?recursive=1). `folders` — об'єкт
                    «тека → версія» (`{"tests/draft2020-12": "2020-12"}`): беруться всі `.json`
                    теки разом із вкладеними (`optional/format/…`), версія — з теки.

Навіщо. Тести — найточніша відповідь на «як поводиться ключове слово»: кожна група — схема і
перелік екземплярів з позначкою, проходять вони перевірку чи ні, і описи груп названо так, як
питають («unevaluatedProperties with adjacent properties», «$ref to $dynamicRef finds detached
$dynamicAnchor»). Але файл тестів — масив JSON на десятки кілобайт. Узятий кодом, він різався б
на шматки за довжиною, посеред схеми, і пошук не мав би за що вхопитися. Тут кожна група стає
розділом з назвою-описом: під нею схема і рядки «valid — опис: дані». Версія лежить у теці, а не
в тегу: теги репозиторію — версії модуля Perl, що їх публікує, а не випуски специфікації.
"""

import json
import re
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/([0-9a-f]{40})$")
# Дані, коротші за цю межу, стоять у рядку тесту; довші — окремим блоком коду.
_INLINE = 80


def _data(value) -> str:
    return json.dumps(value, ensure_ascii=False)


def _group(group: dict, seen: dict) -> list[str]:
    title = " ".join(str(group.get("description") or "group").split())
    seen[title] = seen.get(title, 0) + 1
    if seen[title] > 1:
        title = f"{title} ({seen[title]})"
    out = ["", f"## {title}", ""]
    if group.get("comment"):
        out += [str(group["comment"]), ""]
    out += ["Schema:", "", "```json", json.dumps(group.get("schema"), indent=2,
                                                ensure_ascii=False), "```", "", "Tests:", ""]
    for test in group.get("tests") or ():
        verdict = "valid" if test.get("valid") else "invalid"
        desc = " ".join(str(test.get("description") or "").split())
        data = _data(test.get("data"))
        if len(data) <= _INLINE:
            out.append(f"- {verdict} — {desc}: `{data}`")
        else:
            out += [f"- {verdict} — {desc}:", "", "```json",
                    json.dumps(test.get("data"), indent=2, ensure_ascii=False), "```", ""]
        if test.get("comment"):
            out.append(f"  ({' '.join(str(test['comment']).split())})")
    return out


@register("json-test-suite")
def json_test_suite(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував дерево коміту "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/SHA.")
    owner, repo, sha = m.groups()
    folders = source.get("folders")
    if not isinstance(folders, dict) or not folders:
        raise SystemExit(f"{source['id']}: поле `folders` — об'єкт «тека → версія».")
    try:
        tree = json.loads(ctx.text(source["url"]))
    except ValueError as exc:
        raise SystemExit(f"{source['url']}: відповідь не JSON ({exc}) — перелік не складено.")
    if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
        raise SystemExit(f"{source['url']}: у відповіді немає дерева файлів.")
    if tree.get("truncated"):
        raise SystemExit(f"{source['url']}: GitHub обрізав дерево — перелік був би неповним.")

    items = []
    for entry in tree["tree"]:
        path = entry.get("path", "")
        folder = next((f for f in folders if path.startswith(f.rstrip("/") + "/")), None)
        # `tests/latest` — посилання на теку, а не файл тестів.
        if entry.get("type") != "blob" or folder is None or not path.endswith(".json"):
            continue
        raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{sha}/{quote(path)}"
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{sha}/{quote(path)}"
        inner = path[len(folder.rstrip("/")) + 1:-len(".json")]
        label = folder.rstrip("/").rsplit("/", 1)[-1]
        name = _markup.slug(f"{label} {inner}")
        version = str(folders[folder])

        def make(raw=raw, blob=blob, inner=inner, label=label, version=version):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            try:
                groups = json.loads(text)
            except ValueError as exc:
                raise SystemExit(f"{raw}: файл тестів не JSON ({exc}) — документ не записую.")
            if not isinstance(groups, list):
                raise SystemExit(f"{raw}: файл тестів не масив груп — документ не записую.")
            seen: dict = {}
            lines: list[str] = []
            for group in groups:
                if isinstance(group, dict):
                    lines += _group(group, seen)
            title = f"JSON Schema Test Suite ({label}): {inner}"
            body = "\n".join(lines).strip("\n")
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: у теках {', '.join(folders)} жодного файла тестів.")
    return items
