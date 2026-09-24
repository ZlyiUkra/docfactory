"""Читач специфікацій налаштувань у форматі configspec (YAML).

`config-spec` — `url` — сирий YAML специфікації (`configspec: '001'`): блок `info`
                з назвою, описом і переліком груп (`tags`) та список `parameters`.
                Документом стає кожна група: «config.toml: Auth», «config.toml:
                Database»…, а кожен параметр у ній — окремий заголовок «## назва»
                з описом, значенням за замовчуванням, обов'язковістю, прикладом і
                посиланнями. Опис самої специфікації — окремий документ «огляд».
                Поле `label` — префікс назв документів (типово — `info.title`),
                поле `page` — людська адреса сторінки, що рендерить цю специфікацію.

Навіщо. Supabase тримає довідники налаштувань — `supabase/config.toml` і змінні
оточення self-hosted Auth, Storage, Realtime, Analytics, Functions — лише як YAML у
`apps/docs/spec/` свого репозиторію. Сайт рендерить із них HTML на пів мегабайта
без markdown-двійника, тож першоджерело тут — сам YAML.

Чому документ на групу, а не на параметр: параметр — два-три рядки, і сто
шістдесят крихітних документів лише розмножили б шапки. Фрагментом пошуку все одно
стає окремий параметр — корпус ділить документ саме по «##».

Бібліотека YAML імпортується всередині читача, а не нагорі модуля. Реєстр
імпортує всі модулі читачів у кожному примірнику, а PyYAML стоїть лише у venv
тих, кому цей читач потрібен; імпорт нагорі зламав би решту примірників.
"""

from engine.readers import Item, _markup, register


def _load(ctx, url: str) -> dict:
    try:
        import yaml
    except ImportError:
        raise SystemExit("Читачеві config-spec потрібен PyYAML: додайте його в "
                         "requirements.txt примірника й поставте у його venv.")
    try:
        spec = yaml.safe_load(ctx.text(url))
    except yaml.YAMLError as e:
        raise SystemExit(f"{url}: YAML не розбирається — {e}")
    if not isinstance(spec, dict) or not isinstance(spec.get("parameters"), list):
        raise SystemExit(f"{url}: не схоже на configspec — немає списку `parameters`.")
    return spec


def _text(value) -> str:
    return "" if value is None else str(value).strip()


def _parameter(p: dict) -> str:
    title = _text(p.get("title")) or _text(p.get("id"))
    lines = [f"## {title}", ""]
    facts = []
    if "required" in p:
        facts.append(f"- Required: {'yes' if p.get('required') else 'no'}")
    if _text(p.get("type")):
        facts.append(f"- Type: `{_text(p['type'])}`")
    if "default" in p:
        facts.append(f"- Default: `{_text(p.get('default'))}`")
    lines += facts + ([""] if facts else [])
    if _text(p.get("description")):
        lines += [_text(p["description"]), ""]
    if _text(p.get("usage")):
        lines += ["Usage:", "", "```toml", _text(p["usage"]), "```", ""]
    links = [l for l in p.get("links") or [] if isinstance(l, dict) and l.get("link")]
    if links:
        lines += ["See also:", ""]
        lines += [f"- {_text(l.get('name')) or 'link'}: {_text(l['link'])}" for l in links]
        lines.append("")
    return "\n".join(lines)


@register("config-spec")
def config_spec(source: dict, ctx) -> list[Item]:
    page = source.get("page", "")
    if not page.startswith("https://"):
        raise SystemExit(f"{source['id']}: читач config-spec вимагає поле `page` — "
                         f"людську https-адресу довідника.")
    spec = _load(ctx, source["url"])
    info = spec.get("info") or {}
    label = source.get("label") or _text(info.get("title")) or source["id"]
    version = source.get("version", "")
    tags = {t["id"]: t for t in info.get("tags") or [] if isinstance(t, dict) and "id" in t}

    # Порядок груп — як в `info.tags`, далі групи, яких там не оголосили.
    groups: dict[str, list] = {tid: [] for tid in tags}
    for p in spec["parameters"]:
        if not isinstance(p, dict):
            continue
        tid = (p.get("tags") or ["general"])[0]
        groups.setdefault(tid, []).append(p)

    items = []
    overview = _text(info.get("description"))
    if overview:
        def make_overview():
            body = _markup.markdown_body(overview)
            return _markup.document(f"{label}: overview", page, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/overview",
                          file=f"{source['id']}--overview.txt", make=make_overview))

    for tid, params in groups.items():
        if not params:
            continue
        tag = tags.get(tid, {})
        title = f"{label}: {_text(tag.get('title')) or tid}"
        name = _markup.slug(tid)

        def make(title=title, tag=tag, params=params):
            intro = _text(tag.get("description"))
            md = "\n".join(([intro, ""] if intro else []) + [_parameter(p) for p in params])
            body = _markup.markdown_body(md)
            _markup.require(title, body, source["url"], min_chars=1)
            return _markup.document(title, page, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
