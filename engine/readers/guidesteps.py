"""Читач посібника-кроків, що лежить у коді сайту масивом `steps`, з усіма вкладками.

`guide-steps` — `url` — сира тека з файлами JS, `files` — імена посібників (файл — ім'я з
                «.js»), `page` — шаблон адреси сторінки на сайті з `{name}`;
                `version` — версія всіх документів джерела.

Навіщо. Посібники v3 «Install Tailwind CSS with …» (tailwindcss.com, гілка v3) — не
MDX, а модулі JS: масив кроків `{ title, body: () => (<p>…</p>), code: { name, lang,
code } }`, а в посібниках з кількома шляхами — масив вкладок `{ name: 'Using Vue',
steps: […] }`. Зібраний сайт показує лише першу вкладку: Vue і Svelte у посібнику Vite,
Laravel Mix у посібнику Laravel в HTML не потрапляють. Тут вкладка стає розділом, крок —
підрозділом, код — огородженим блоком з ім'ям файла.

Код кроку в v3 позначає рядки першим символом: «>» — доданий рядок, «<» — прибраний,
пробіл — незмінний. Позначки знімаються, прибраний рядок пропускається: у тексті лишається
той вміст файла, який посібник велить отримати.

Розбір — виразами по сталій формі цих файлів, без повного розбору JS. Тіло кроку (JSX)
перетворюється на текст через `_jsx`. Файл, у якому не знайдено жодного кроку, — не
документ: форма змінилася, і мовчки записати порожнечу гірше, ніж зупинитися.
"""

import re

from engine.readers import Item, _jsx, _markup, register

_TAB = re.compile(r"\bname:\s*(['\"])(Using [^'\"]+)\1")
# Тіло кроку закінчується там, де починається його код або закривається сам крок.
_STEP = re.compile(
    r"\btitle:\s*(['\"])((?:\\.|(?!\1).)*)\1,\s*"
    r"body:\s*\(\)\s*=>\s*(.*?),?\s*\n\s*(?:code:\s*\{|\},?\s*\n)", re.S)
# Поля коду читаються одне за одним від «code: {»: сам код (конфіг з «theme: {}») має
# власні дужки, і пошук кінця об'єкта різав би його на першій із них.
_FIELD = re.compile(r"\s*(name|lang|code):\s*(?:(['\"])((?:\\.|(?!\2).)*)\2|"
                    r"`((?:\\.|[^`\\])*)`)\s*,?", re.S)
_LAYOUT = re.compile(r"<FrameworkGuideLayout\s+title=\"([^\"]+)\"\s+description=\"([^\"]*)\"")
_MARK = re.compile(r"^(?:  |> |< |>$|<$|$)")


def _unescape(s: str) -> str:
    return re.sub(r"\\(.)", lambda m: "\n" if m.group(1) == "n" else m.group(1), s)


def _code(lines: str) -> str:
    rows = lines.split("\n")
    if all(_MARK.match(r) for r in rows):
        rows = [r[2:] for r in rows if not r.startswith("<")]
    return "\n".join(rows).strip("\n")


def _page(text: str, url: str) -> tuple[str, str]:
    m = _LAYOUT.search(text)
    if not m:
        raise SystemExit(f"{url}: немає <FrameworkGuideLayout title=…> — форма змінилася.")
    tabs = [(t.start(), t.group(2)) for t in _TAB.finditer(text)]
    out = [m.group(2), ""]
    tab = None
    found = 0
    for s in _STEP.finditer(text):
        here = [name for pos, name in tabs if pos < s.start()]
        if here and here[-1] != tab:
            tab = here[-1]
            out += [f"## {tab}", ""]
        body = _jsx.text_of(s.group(3)).strip()
        fields = {}
        pos = s.end()
        while s.group(0).rstrip().endswith("{") and (f := _FIELD.match(text, pos)):
            fields[f.group(1)] = _unescape(f.group(3) if f.group(3) is not None
                                           else f.group(4))
            pos = f.end()
        out += [f"{'###' if tab else '##'} {_unescape(s.group(2))}", "", body, ""]
        if fields.get("code"):
            if fields.get("name"):
                out += [fields["name"], ""]
            out += [f"```{fields.get('lang', '')}", _code(fields["code"]), "```", ""]
        found += 1
    if not found:
        raise SystemExit(f"{url}: жодного кроку title/body/code — форма змінилася.")
    return m.group(1), "\n".join(out)


@register("guide-steps")
def guide_steps(source: dict, ctx) -> list[Item]:
    files = source.get("files")
    page_of = source.get("page") or ""
    if not isinstance(files, list) or not files or "{name}" not in page_of:
        raise SystemExit(f"{source['id']}: читач guide-steps потребує полів files — "
                         f"списку імен — і page — шаблону адреси з {{name}}.")
    items = []
    for name in files:
        raw = f"{source['url'].rstrip('/')}/{name}.js"
        page = page_of.format(name=name)
        if not ctx.allowed(raw):
            continue

        def make(raw=raw, page=page):
            title, body = _page(ctx.text(raw), raw)
            body = _markup.markdown_body(body)
            _markup.require(title, body, raw)
            return _markup.document(title, page, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
