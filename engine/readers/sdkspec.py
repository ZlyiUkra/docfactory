"""Читач специфікацій клієнтських бібліотек у форматі openref (YAML).

`sdk-spec` — `url` — сирий YAML (`openref: 0.1`) зі списком `functions`: кожна
             функція — назва, опис, нотатки, параметри й приклади (код, дані для
             прикладу, відповідь). Увесь референс однієї версії бібліотеки стає
             одним документом, кожна функція — заголовком «## назва», приклад —
             «### Example: …», тож фрагментом пошуку стає метод або приклад, як і в
             поточному референсі з `llms/<мова>.txt`. Поле `label` — назва
             документа, поле `page` — людська адреса цієї версії референсу.

Навіщо. `llms/<мова>.txt` несе лише поточну мажорну версію кожної бібліотеки, а
сайт показує й старі — supabase-js v1, Kotlin v1 і v2, Dart v1, Swift v1, C# v0 і
v1 — лише HTML-ом. Першоджерело всіх них — YAML у `apps/docs/spec/` репозиторію
документації, і саме його сайт рендерить.

Описи частини функцій у YAML немає: там стоїть `$ref` на згенеровану з коду
довідку TypeScript. Її тут не підтягнуто навмисно — функція лишається з назвою,
нотатками й прикладами, а приклади для старого коду важать найбільше.

Бібліотека YAML імпортується всередині читача з тієї ж причини, що в
`config-spec`: реєстр імпортує всі модулі читачів у кожному примірнику.
"""

from engine.readers import Item, _markup, register


def _text(value) -> str:
    return "" if value is None else str(value).strip()


def _params(params, depth: int = 0) -> list[str]:
    lines = []
    for p in params or []:
        if not isinstance(p, dict):
            continue
        kind = f" `{_text(p['type'])}`" if _text(p.get("type")) else ""
        need = ", optional" if p.get("isOptional") else ""
        desc = " ".join(_text(p.get("description")).split())
        lines.append(f"{'  ' * depth}- `{_text(p.get('name'))}`{kind}{need}"
                     + (f": {desc}" if desc else ""))
        lines += _params(p.get("subContent"), depth + 1)
    return lines


def _example(ex: dict) -> list[str]:
    lines = [f"### Example: {_text(ex.get('name')) or _text(ex.get('id'))}", ""]
    for key in ("description", "note", "notes"):
        if _text(ex.get(key)):
            lines += [_text(ex[key]), ""]
    data = ex.get("data")
    if isinstance(data, dict) and _text(data.get("sql")):
        lines += ["Data source:", "", _text(data["sql"]), ""]
    if _text(ex.get("code")):
        lines += [_text(ex["code"]), ""]
    if _text(ex.get("response")):
        lines += ["Response:", "", _text(ex["response"]), ""]
    return lines


def _function(fn: dict) -> str:
    lines = [f"## {_text(fn.get('title')) or _text(fn.get('id'))}", ""]
    for key in ("description", "notes"):
        if _text(fn.get(key)):
            lines += [_text(fn[key]), ""]
    params = _params(fn.get("params"))
    if params:
        lines += ["Parameters:", ""] + params + [""]
    for ex in fn.get("examples") or []:
        if isinstance(ex, dict):
            lines += _example(ex)
    return "\n".join(lines)


@register("sdk-spec")
def sdk_spec(source: dict, ctx) -> list[Item]:
    page = source.get("page", "")
    label = source.get("label", "")
    if not page.startswith("https://") or not label:
        raise SystemExit(f"{source['id']}: читач sdk-spec вимагає поля `label` і `page` — "
                         f"назву документа й людську https-адресу референсу.")
    name = _markup.slug(label)

    def make():
        try:
            import yaml
        except ImportError:
            raise SystemExit("Читачеві sdk-spec потрібен PyYAML: додайте його в "
                             "requirements.txt примірника й поставте у його venv.")
        try:
            spec = yaml.safe_load(ctx.text(source["url"]))
        except yaml.YAMLError as e:
            raise SystemExit(f"{source['url']}: YAML не розбирається — {e}")
        if not isinstance(spec, dict) or not isinstance(spec.get("functions"), list):
            raise SystemExit(f"{source['url']}: не схоже на openref — немає `functions`.")
        md = "\n".join(_function(fn) for fn in spec["functions"] if isinstance(fn, dict))
        body = _markup.markdown_body(md)
        _markup.require(label, body, source["url"])
        return _markup.document(label, page, ctx.stamp, body, source.get("version", ""))

    return [Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make)]
