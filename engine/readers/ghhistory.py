"""Читач історії документації репозиторію: один документ на кожен неповторний текст файла.

`ghdocs-history` — markdown-документація з багатьох тегів одного репозиторію разом.
                   `url` — префікс дерев через API
                   (…/repos/ВЛАСНИК/РЕПО/git/trees/), поле `tags` — об'єкт «тег →
                   версія», від найновішого. `folders` — теки, .md-файли яких
                   беруться (з `recursive: true` — і з вкладених тек), `files` —
                   окремі файли поза ними (напр. кореневий FAQ.md).
                   Необов'язкові: `extensions` — розширення файлів документації (типово
                   лише `.md`; сайт на MDX додає `.mdx`), `exclude` — вирази шляхів, що не
                   беруться (переклади, службові файли теки), `title_prefix` — об'єкт
                   «початок шляху → назва» (тека пишеться з «/» у кінці, окремий файл —
                   повним шляхом): такий документ дістає назву «Назва: заголовок», якщо
                   заголовок цієї назви ще не містить; `name_prefix` — рядок, що стає
                   перед іменем документа («helmet» → «helmet-changelog-290249f0»);
                   `mdx: true` — і файли `.md` читаються як MDX: без `import`/`export`
                   верхнього рівня (Docusaurus так і збирає `.md`, тож сторінки socket.io
                   з вкладками починаються з `import Tabs from '@theme/Tabs'`);
                   `site` — об'єкт «вираз шляху → адреса сторінки сайту» (`\\1` — група
                   виразу): документ, чий шлях цілком збігся з виразом, дістає в шапку
                   адресу сайту, решта — blob на GitHub. Сайт не читається: текст і далі
                   береться з raw.githubusercontent.com, адреса лише цитується. `{version}`
                   в адресі — мітка найновішого тегу, де файл такий був (сайт Node.js
                   тримає документацію кожного мажору за своєю адресою);
                   `yaml_history: true` — блоки `<!-- YAML … -->` (так документація API
                   Node.js записує, з якої версії функція є, коли застаріла і що в ній
                   мінялося) стають видимим текстом «Added in / History»; інакше разом з
                   іншими коментарями HTML вони зникали б, і примірник не знав би версій;
                   `jsx_props: true` — компоненти, чий зміст лежить у властивостях
                   (`<APIMethod path method>`, `<TypeTable type>`, `<DatabaseTable fields>`
                   документації Better Auth), стають текстом: рядком ендпоінта і списками
                   опцій та полів таблиць; `component_labels` — об'єкт «тег → підпис»:
                   рядок-тег вкладки (`<Code.Next>`) стає підписом («Next.js:»);
                   `admonitions: true` — виноски Docusaurus (`:::tip Назва` … `:::`) стають
                   підписом «Tip: Назва» замість рядків із двокрапками;
                   `nginx_xml: true` — файли `.xml` (документація nginx.org у власному словнику
                   XML) перед розбором стають markdown (див. `_nginxxml`): директиви з рядками
                   «Syntax / Default / Context», приклади — блоками коду;
                   `hugo` — об'єкт `{"includes": тека, "shortcodes": тека}`: вставки Hugo сайту
                   (docs.nginx.com) розгортаються — `include` спільних шматків, `ghcode`
                   прикладів, номери версій із файлів шаблонів, підписи виносок і вкладок;
                   `base_ui: true` — вставки сторінок Base UI (демо, таблиці API з `types.md` чи
                   довідки JSON) стають кодом і списками (див. `_baseui`);
                   `react_spectrum: true` — службове зі сторінок репозиторію React Aria знімається:
                   коментар ліцензії, шапка YAML після імпортів, вирази `{docs.exports.….description}`
                   і позначки підсвічування `/*- begin highlight -*/` у коді.

Навіщо `name_prefix`. Ключ розділу будується з імені документа, а ім'я — зі шляху файла.
Журнали змін кількох репозиторіїв в одному примірнику (HISTORY.md body-parser, cors,
express-session…) мали б усі ім'я «history», і розділ «1.19.0» одного пакета пошук згортав
би як повтор того самого розділу іншого. Без поля ім'я те саме, що й було.

Навіщо `title_prefix`. Сайт, що описує кілька обгорток однієї бібліотеки, дає сторінкам
кожної обгортки ті самі заголовки: у Testing Library «API», «Setup», «Example» є і в
React, і у Vue, і у Svelte — тридцять дві сторінки «API». На сайті їх розрізняє бічне
меню, у корпусі — нічого, а назва документа йде в контекст кожного його фрагмента.

Навіщо. `ghdocs` дає знімок на тег: кожен тег — повна копія теки документації. У
React Router 820 тегів, у кожному 100–200 файлів, разом 88 тисяч файлів, а різних
текстів серед них лише 2 855: між сусідніми тегами змінюється один-два файли або
жодного. Знімки на тег означали б 88 тисяч завантажень і корпус, у якому 97% —
дослівні повтори, які злиття однаково зводить в один фрагмент.

Тут одиниця — пара «шлях, вміст» (вміст упізнається хешем blob із дерева тегу). Така
пара стає одним документом, а в його версії лягають усі теги, де цей файл лежав
саме таким. Фільтр `version: "6.4"` знаходить рівно ті тексти, що знайшов би серед
знімків, бо текст той самий, — різниця лише в тому, що кожен тягнеться й лежить
один раз. Адреса в шапці — blob на першому з тегів переліку, де файл такий був,
тобто на найновішому.

Версія — рядок із `tags`, а не номер, вирізаний із тегу. Так збірки, чий номер
нічого не каже (`v0.0.0-experimental-004e483a8`), дістають мітку `experimental`
і не змішуються з лінією 0.x, у якої номер той самий.

Назва документа — поле `title` шапки YAML; без шапки — заголовок, що стоїть першим
рядком; інакше — ім'я файла. Саме так і в 0.x: сторінка «Route.md» починається
одразу текстом, а перший заголовок у ній — підрозділ «Props», не назва. Стара документація (до v4) пише заголовки
підкресленням («Назва» і рядок «===» під нею), і `_markup` їх не знає: тут вони
стають «#»/«##» до розбору, інакше документ не ділився б на розділи.

Чому окремий модуль, а не поле в `ghdocs`: примірники, зібрані знімками на тег,
звірені, а правка спільного читача — ризик зсуву в готовій роботі.
"""

import json
import re
from html import unescape
from urllib.parse import quote, urlsplit

from engine.readers import Item, _baseui, _markup, _nginxxml, register

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
_LOCALE = re.compile(r"\.[a-z]{2}-[A-Z]{2}\.md$")
_FENCE = re.compile(r"^\s*(```|~~~)")
_ATX = re.compile(r"^(#{1,6})[ \t]+(\S.*?)[ \t]*#*[ \t]*$")
_SETEXT = re.compile(r"^(=+|-+)[ \t]*$")
# Рядок, що підкресленням заголовка бути не може: пункт списку, цитата, таблиця,
# інший заголовок. Інакше «---» під пунктом списку став би заголовком із пункту.
_NOT_TITLE = re.compile(r"^\s*([-*+>|#]|\d+[.)]\s|```|~~~)")
_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_ATTRS = re.compile(r"\{:[^}]*\}")
_YAML_BLOCK = re.compile(r"<!--\s*YAML\s*\n(.*?)-->", re.S)
# Рядок із самою картинкою: markdown (`![logo](…){: …}`) або тег HTML (`<img align="right" …/>` —
# так іконка адаптера стоїть над заголовком кожної сторінки authjs.dev).
# Сторінки React Aria в репозиторії: шапка YAML стоїть після імпортів, перед нею — коментар
# ліцензії, а опис компонента — вираз, який сайт підставляв із коду TypeScript.
_RS_COMMENT = re.compile(r"^\{/\*.*?\*/\}[ \t]*$\n?", re.M | re.S)
_RS_FRONT = re.compile(r"^---[ \t]*\n(?:[A-Za-z_]+:.*\n)+---[ \t]*$\n?", re.M)
_RS_EXPR = re.compile(r"^[ \t]*(?:<PageDescription>)?\{docs\.exports\.[\w.]+\}"
                      r"(?:</PageDescription>)?[ \t]*$\n?", re.M)
_RS_HIGHLIGHT = re.compile(r"^[ \t]*\{?/\*- (?:begin|end) highlight -\*/\}?[ \t]*\n"
                           r"|\{?/\*- (?:begin|end) highlight -\*/\}?", re.M)
_IMAGE_LINE = re.compile(r"^[ \t]*(?:!\[[^\]]*\]\([^)]*\)[ \t]*(\{:[^}]*\})?|<img\b[^<>]*>)[ \t]*$", re.M)


def _versions(value) -> str:
    return ", ".join(str(v) for v in value) if isinstance(value, list) else str(value)


def _yaml_history(text: str) -> str:
    """Блоки `<!-- YAML … -->` документації Node.js → рядки тексту. Блок, який не
    розбирається як YAML, лишається як був (і зникне разом з коментарями): вигадувати
    версій читач не стане."""
    import yaml

    def render(m):
        try:
            meta = yaml.safe_load(m.group(1))
        except yaml.YAMLError:
            return m.group(0)
        if not isinstance(meta, dict):
            return m.group(0)
        lines = []
        for key, label in (("added", "Added in"), ("deprecated", "Deprecated since"),
                           ("removed", "Removed in"), ("napiVersion", "N-API version")):
            if meta.get(key) is not None:
                lines.append(f"{label}: {_versions(meta[key])}.")
        changes = [c for c in meta.get("changes") or () if isinstance(c, dict)]
        if changes:
            lines.append("History:")
            for c in changes:
                what = " ".join(str(c.get("description", "")).split())
                lines.append(f"- {_versions(c.get('version', ''))}: {what}")
        return "\n".join(lines) + "\n" if lines else ""

    return _YAML_BLOCK.sub(render, text)


def _atx(text: str) -> str:
    """Заголовки-підкреслення → «#»/«##». Код і вже звичайні заголовки не
    чіпаються."""
    lines = text.split("\n")
    out: list[str] = []
    fence = False
    for ln in lines:
        if _FENCE.match(ln):
            fence = not fence
        elif (not fence and _SETEXT.match(ln) and out and out[-1].strip()
              and not _NOT_TITLE.match(out[-1])
              and (len(out) < 2 or not out[-2].strip())):
            out[-1] = ("# " if ln.lstrip()[0] == "=" else "## ") + out[-1].strip()
            continue
        out.append(ln)
    return "\n".join(out)


_JS_NAME = re.compile(r"[A-Za-z_$][\w$]*")
_JS_NUMBER = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?")
_JS_EXPORT = re.compile(r"^export\s+const\s+([A-Za-z_$][\w$]*)\s*=\s*", re.M)
_PROP_TABLE = re.compile(r"<(TypeTable|DatabaseTable|PropsTable|DataAttributesTable|KeyboardTable"
                         r"|CssVariablesTable|Highlights|PropsReferenceTable)\b")
_TABLE_PROP = {"TypeTable": "type", "DatabaseTable": "fields", "Highlights": "features"}
_PACKAGE_RELEASE = re.compile(r'^[ \t]*<PackageRelease\s+name="([^"]+)"\s+version="([^"]+)"'
                              r'\s*/>[ \t]*$', re.M)
_PR_LINK = re.compile(r"<PRLink\s+id=\{(\d+)\}\s*/>")
_CODE_TAG = re.compile(r"<Code>([^<>{}]*)</Code>")
_HERO = re.compile(r"^[ \t]*<HeroContainer>.*?</HeroContainer>[ \t]*$"
                   r"|^[ \t]*<(?:HeroCodeBlock|ThemesPropsTable)\b[^>]*/>[ \t]*$", re.M | re.S)
_API_METHOD = re.compile(r"^[ \t]*<APIMethod\b((?:[^<>\"{}]|\"[^\"]*\"|\{[^{}]*\})*)>[ \t]*$", re.M)
_JSX_ATTR = re.compile(r"(\w+)(?:\s*=\s*(?:\"([^\"]*)\"|\{([^{}]*)\}))?")
_JSX_SPACE = re.compile(r"\{\s*([\"'])\s*\1\s*\}")
_SHIKI_MARK = re.compile(r"[ \t]*(?://|#)?[ \t]*\[!code [^\]]*\]")
_ADMONITION = re.compile(r"^:::(\w+)(?:\[([^\]]*)\]|[ \t]+(.+?))?[ \t]*$")
_ADMONITION_END = re.compile(r"^:::[ \t]*$")
_DB_FLAGS = (("isPrimaryKey", "primary key"), ("isForeignKey", "foreign key"),
             ("isUnique", "unique"), ("isOptional", "optional"), ("isRequired", "required"))


class _NotLiteral(ValueError):
    """Значення JS — не дані (функція, JSX, виклик): таблицю не відтворити."""


def _js_skip(s: str, i: int) -> int:
    while i < len(s):
        if s[i].isspace():
            i += 1
        elif s.startswith("//", i):
            j = s.find("\n", i)
            i = len(s) if j < 0 else j
        elif s.startswith("/*", i):
            j = s.find("*/", i)
            i = len(s) if j < 0 else j + 2
        else:
            break
    return i


def _js_string(s: str, i: int) -> tuple[str, int]:
    quote_, out, i = s[i], [], i + 1
    while i < len(s) and s[i] != quote_:
        if s[i] == "\\" and i + 1 < len(s):
            i += 1
            out.append({"n": "\n", "t": "\t"}.get(s[i], s[i]))
        else:
            out.append(s[i])
        i += 1
    if i >= len(s):
        raise _NotLiteral
    return "".join(out), i + 1


_JSX_OPEN = re.compile(r"<([A-Za-z][\w.]*)?((?:[^<>\"'{}]|\"[^\"]*\"|'[^']*'|\{[^{}]*\})*?)(/?)>")
_JSX_CLOSE = re.compile(r"</([A-Za-z][\w.]*)?\s*>")


def _jsx_text(s: str, i: int) -> tuple[str, int]:
    """(текст, позиція після елемента) для елемента JSX у значенні властивості: так Radix
    пише опис пропса — `description: (<span>Must be used with <Code>onOpenChange</Code>.</span>)`.
    `<Code>` стає `кодом`, `<br />` — пробілом, решта тегів знімається, а з виразів `{…}`
    лишаються лише рядки (`{" "}`, `{"…"}`)."""
    # Стек відкритих тегів і буфер кожного: вміст `<Code>` збирається окремо, щоб стати
    # `кодом` без пробілів усередині лапок.
    stack: list[tuple[str, list[str]]] = [("", [])]
    while i < len(s):
        if s[i] == "<":
            m = _JSX_CLOSE.match(s, i)
            if m:
                if len(stack) < 2:
                    raise _NotLiteral
                tag, buf = stack.pop()
                inner = " ".join("".join(buf).split())
                stack[-1][1].append(f"`{inner}`" if tag == "Code" and inner else inner)
                i = m.end()
                if len(stack) == 1:
                    break
                continue
            m = _JSX_OPEN.match(s, i)
            if not m:
                raise _NotLiteral
            i = m.end()
            if m.group(3):
                stack[-1][1].append(" " if m.group(1) == "br" else "")
                if len(stack) == 1:
                    break
            else:
                stack.append((m.group(1) or "", []))
        elif s[i] == "{":
            j = _js_skip(s, i + 1)
            if s[j:j + 1] in ("'", '"', "`"):
                text, j = _js_string(s, j)
                stack[-1][1].append(text)
                j = _js_skip(s, j)
            close = s.find("}", j)
            if close < 0:
                raise _NotLiteral
            i = close + 1
        else:
            stack[-1][1].append(s[i])
            i += 1
    if len(stack) != 1:
        raise _NotLiteral
    return " ".join("".join(stack[0][1]).split()), i


def _js_value(s: str, i: int):
    """(значення, позиція після нього) для літерала JS: об'єкт, масив, рядок, число, ім'я,
    а також елемент JSX (його текст, див. `_jsx_text`), зокрема в дужках. Скаляри лишаються
    рядками так, як записані («false», «128»): у таблицю вони й ідуть текстом."""
    i = _js_skip(s, i)
    if i >= len(s):
        raise _NotLiteral
    c = s[i]
    if c == "<":
        return _jsx_text(s, i)
    if c == "(":
        value, i = _js_value(s, i + 1)
        i = _js_skip(s, i)
        if s[i:i + 1] != ")":
            raise _NotLiteral
        return value, i + 1
    if c == "{":
        out: dict = {}
        i = _js_skip(s, i + 1)
        while s[i:i + 1] != "}":
            if s[i:i + 1] in ("'", '"'):
                key, i = _js_string(s, i)
            else:
                m = _JS_NAME.match(s, i)
                if not m:
                    raise _NotLiteral
                key, i = m.group(0), m.end()
            i = _js_skip(s, i)
            if s[i:i + 1] == ":":
                out[key], i = _js_value(s, i + 1)
            else:
                out[key] = key
            i = _js_skip(s, i)
            if s[i:i + 1] == ",":
                i = _js_skip(s, i + 1)
            elif s[i:i + 1] != "}":
                raise _NotLiteral
        return out, i + 1
    if c == "[":
        items: list = []
        i = _js_skip(s, i + 1)
        while s[i:i + 1] != "]":
            value, i = _js_value(s, i)
            items.append(value)
            i = _js_skip(s, i)
            if s[i:i + 1] == ",":
                i = _js_skip(s, i + 1)
            elif s[i:i + 1] != "]":
                raise _NotLiteral
        return items, i + 1
    if c in "\"'`":
        text, i = _js_string(s, i)
        j = _js_skip(s, i)
        # «"довгий опис " + "продовження"» — так у джерелі розривають довгі рядки.
        while s[j:j + 1] == "+":
            more, i = _js_value(s, j + 1)
            if not isinstance(more, str):
                raise _NotLiteral
            text += more
            j = _js_skip(s, i)
        return text, i
    m = _JS_NUMBER.match(s, i) or _JS_NAME.match(s, i)
    if not m:
        raise _NotLiteral
    after = _js_skip(s, m.end())
    if s[after:after + 1] in ("(", ".") or s.startswith("=>", after):
        raise _NotLiteral
    return m.group(0), m.end()


def _type_rows(table: dict, depth: int = 0) -> list[str]:
    rows = []
    for key, spec in table.items():
        if not isinstance(spec, dict):
            continue
        bits = [str(spec["type"])] if isinstance(spec.get("type"), str) and spec["type"] else []
        if spec.get("required") == "true":
            bits.append("required")
        if isinstance(spec.get("default"), str) and spec["default"] not in ("", "undefined"):
            bits.append(f"default: {spec['default']}")
        if spec.get("deprecated") == "true":
            bits.append("deprecated")
        desc = " ".join(str(spec.get("description") or "").split())
        head = f"{'  ' * depth}- `{key}`" + (f" ({', '.join(bits)})" if bits else "")
        rows.append(head + (f" — {desc}" if desc else ""))
        if isinstance(spec.get("properties"), dict):
            rows += _type_rows(spec["properties"], depth + 1)
    return rows


def _reference_rows(table: dict) -> list[str]:
    """`<PropsReferenceTable data={{…}}>` Base UI: параметри й значення хуків та утиліт. Тип і
    типове значення — кодом: `RenderProp<State>` без лапок розмітка прийняла б за тег."""
    rows = []
    for key, spec in table.items():
        if not isinstance(spec, dict):
            continue
        bits = [f"`{' '.join(str(spec['type']).split())}`"] if spec.get("type") else []
        if isinstance(spec.get("default"), str) and spec["default"] not in ("", "undefined"):
            bits.append(f"default: `{spec['default']}`")
        desc = " ".join(str(spec.get("description") or "").split())
        rows.append(f"- `{key}`" + (f" ({', '.join(bits)})" if bits else "")
                    + (f" — {desc}" if desc else ""))
    return rows


def _db_rows(fields: list) -> list[str]:
    rows = []
    for f in fields:
        if not isinstance(f, dict) or not f.get("name"):
            continue
        bits = [str(f["type"])] if isinstance(f.get("type"), str) and f["type"] else []
        bits += [label for key, label in _DB_FLAGS if f.get(key) == "true"]
        ref = f.get("references")
        if isinstance(ref, dict) and ref.get("model"):
            bits.append(f"references `{ref['model']}.{ref.get('field', 'id')}`")
        if isinstance(f.get("defaultValue"), str):
            bits.append(f"default: {f['defaultValue']}")
        desc = " ".join(str(f.get("description") or "").split())
        rows.append(f"- `{f['name']}`" + (f" ({', '.join(bits)})" if bits else "")
                    + (f" — {desc}" if desc else ""))
    return rows


def _radix_rows(kind: str, data: list) -> list[str]:
    """Рядки таблиць Radix: пропси, атрибути `data-*`, клавіші, змінні CSS, можливості."""
    if kind == "Highlights":
        return ["Features:", ""] + [f"- {' '.join(str(f).split())}" for f in data if str(f).strip()]
    head = {"PropsTable": "Props:", "DataAttributesTable": "Data attributes:",
            "KeyboardTable": "Keyboard interactions:", "CssVariablesTable": "CSS variables:"}[kind]
    rows = [head, ""]
    for row in data:
        if not isinstance(row, dict):
            continue
        desc = " ".join(str(row.get("description") or "").split())
        if kind == "PropsTable" and row.get("name"):
            bits = [str(row["type"])] if isinstance(row.get("type"), str) and row["type"] else []
            if row.get("required") == "true":
                bits.append("required")
            if isinstance(row.get("default"), str) and row["default"] not in ("", "undefined"):
                bits.append(f"default: {row['default']}")
            rows.append(f"- `{row['name']}`" + (f" ({', '.join(bits)})" if bits else "")
                        + (f" — {desc}" if desc else ""))
        elif kind == "DataAttributesTable" and row.get("attribute"):
            values = row.get("values")
            values = " | ".join(f"`{v}`" for v in values) if isinstance(values, list) else values
            rows.append(f"- `{row['attribute']}`" + (f": {values}" if values else ""))
        elif kind == "KeyboardTable" and row.get("keys"):
            keys = row["keys"] if isinstance(row["keys"], list) else [row["keys"]]
            rows.append(f"- {' + '.join(str(k) for k in keys)}" + (f" — {desc}" if desc else ""))
        elif kind == "CssVariablesTable" and row.get("cssVariable"):
            rows.append(f"- `{row['cssVariable']}`" + (f" — {desc}" if desc else ""))
    return rows if len(rows) > 2 else []


def _jsx_props(text: str) -> str:
    """Компоненти, чий зміст лежить у властивостях, а не між тегами, → текст.

    Так пише Better Auth: метод і шлях ендпоінта — атрибути `<APIMethod path="/sign-in/email"
    method="POST">`, опції — об'єкт `export const …Type = {…}` для `<TypeTable type={…} />`, поля
    таблиць бази — масив для `<DatabaseTable fields={…} />`. Розмітка `_markup` бере лише текст між
    тегами, а рядки `export` MDX викидаються як код сторінки, тож без цього в корпус не дійшли б
    ні адреси ендпоінтів, ні жодна опція, ні жодна схема таблиці. Значення, що не є даними
    (функція, виклик), таблицю не відтворює — тоді вона випадає, як і без цього поля.

    Так само пише Radix: пропси частини компонента — масив `<PropsTable data={[…]} />` з описом
    у JSX, атрибути стану — `<DataAttributesTable>`, клавіші — `<KeyboardTable>`, змінні CSS —
    `<CssVariablesTable>`, можливості — `<Highlights features={[…]} />`; у журналі випусків пакет
    і версія — `<PackageRelease name version />` (стає підзаголовком), номер PR — `<PRLink id>`.
    Демо (`<HeroContainer>`, `<HeroCodeBlock>`) знімається: це живий компонент сайту, а не
    текст; `<ThemesPropsTable defs>` теж — його дані лежать у коді Radix Themes, не на сторінці.
    Заодно: `{" "}` — пробіл JSX, а `[!code highlight]` (після `//`, `#` або коментаря) — позначка
    підсвічування рядка коду."""
    # Розібраний експорт вирізається цілком: `mdx_statements_out` знімає лише його перший
    # рядок, і решта масиву лишалася б у тексті сирим кодом.
    names: dict = {}
    kept, i = [], 0
    for m in _JS_EXPORT.finditer(text):
        if m.start() < i:
            continue
        try:
            names[m.group(1)], end = _js_value(text, m.end())
        except _NotLiteral:
            continue
        end = _js_skip(text, end)
        kept.append(text[i:m.start()])
        i = end + 1 if text[end:end + 1] == ";" else end
    text = "".join(kept) + text[i:]

    def api(m):
        attrs = {k: (a if a is not None else b if b is not None else "true")
                 for k, a, b in _JSX_ATTR.findall(m.group(1))}
        if not attrs.get("path"):
            return m.group(0)
        line = f"Endpoint: `{attrs.get('method', 'GET').upper()} {attrs['path']}`"
        flags = [label for key, label in (("requireSession", "requires a session"),
                                          ("requireHeaders", "requires request headers"),
                                          ("isServerOnly", "server only"),
                                          ("isClientOnly", "client only")) if key in attrs]
        notes = [" ".join(attrs[k].split()) for k in ("note", "serverOnlyNote", "clientOnlyNote")
                 if attrs.get(k) and attrs[k] != "true"]
        return "\n".join([line + (f" ({', '.join(flags)})" if flags else "") + ".", ""]
                         + [n + "\n" for n in notes])

    out, i = [], 0
    for m in _PROP_TABLE.finditer(text):
        if m.start() < i:
            continue
        kind = m.group(1)
        prop = _TABLE_PROP.get(kind, "data")
        end = text.find("/>", m.end())
        attr = re.compile(rf"\b{prop}\s*=\s*\{{").search(text, m.end(), end if end > 0 else None)
        if not attr:
            continue
        try:
            value, j = _js_value(text, attr.end())
            j = _js_skip(text, j)
            if text[j:j + 1] != "}":
                raise _NotLiteral
            close = text.index("/>", j)
        except (_NotLiteral, ValueError):
            continue
        if isinstance(value, str):
            value = names.get(value)
        named = re.search(r'\bname\s*=\s*"([^"]+)"', text[m.end():close])
        if kind == "TypeTable" and isinstance(value, dict):
            rows = _type_rows(value)
        elif kind == "DatabaseTable" and isinstance(value, list):
            rows = ([f"Table `{named.group(1)}`:", ""] if named else []) + _db_rows(value)
        elif kind == "PropsReferenceTable" and isinstance(value, dict):
            rows = _reference_rows(value)
        elif kind not in ("TypeTable", "DatabaseTable") and isinstance(value, list):
            rows = _radix_rows(kind, value)
        else:
            continue
        out += [text[i:m.start()], "\n".join(rows) + "\n"]
        i = close + 2
    text = "".join(out) + text[i:]
    text = _HERO.sub("", text)
    text = _PACKAGE_RELEASE.sub(lambda m: f"### {m.group(1)} {m.group(2)}", text)
    text = _PR_LINK.sub(lambda m: f"(#{m.group(1)})", text)
    text = _CODE_TAG.sub(lambda m: f"`{m.group(1).strip()}`", text)
    text = _API_METHOD.sub(api, text)
    text = _JSX_SPACE.sub(" ", text)
    return _SHIKI_MARK.sub("", text)


def _component_labels(text: str, labels: dict) -> str:
    """Рядок-тег вкладки (`<Code.Next>`) → підпис «Next.js:». Auth.js показує той самий
    приклад для кожного фреймворку окремою вкладкою; без підпису в тексті лишалися б
    чотири блоки коду поспіль, і відповідь про Next.js могла б процитувати SvelteKit."""
    tags = re.compile(r"^[ \t]*<(" + "|".join(re.escape(t) for t in labels) + r")>[ \t]*$", re.M)
    return tags.sub(lambda m: f"\n{labels[m.group(1)]}:\n", text)


def _admonitions(text: str) -> str:
    """Виноски Docusaurus (`:::tip Назва` … `:::`) → підпис «Tip: Назва» і абзаци. Інакше
    двокрапки лишалися б у тексті окремими рядками. Код не чіпається."""
    out, fence = [], False
    for line in text.split("\n"):
        if _FENCE.match(line):
            fence = not fence
        elif not fence and (m := _ADMONITION.match(line.strip())):
            label = m.group(1).capitalize()
            title = (m.group(2) or m.group(3) or "").strip()
            out += ["", f"{label}: {title}" if title else f"{label}:", ""]
            continue
        elif not fence and _ADMONITION_END.match(line.strip()):
            out.append("")
            continue
        out.append(line)
    return "\n".join(out)


_HUGO_INCLUDE = re.compile(r'\{\{<\s*include\s+"([^"]+)"\s*>\}\}')
_HUGO_GHCODE = re.compile(r'\{\{<\s*ghcode\s+"([^"]+)"[^}]*>\}\}')
_HUGO_CALLOUT = re.compile(r'\{\{<\s*call-out\b([^}]*)>\}\}')
_HUGO_LABEL = re.compile(r'\{\{[<%]\s*(?:tab\s+name|details\s+summary)="([^"]*)"[^}]*[>%]\}\}')
_HUGO_BARE = re.compile(r"\{\{<\s*([a-z][\w-]*)\s*/?>\}\}")
_HUGO_ANY = re.compile(r"\{\{[<%].*?[>%]\}\}")


def _hugo(text: str, ctx, base: str, conf: dict, depth: int = 0) -> str:
    """Вставки Hugo сайту docs.nginx.com → текст.

    `{{< include "nic/…md" >}}` — шматок спільної теки (`conf["includes"]`), що стоїть на
    місці вставки: без нього кроки встановлення й цілі абзаци застережень зникали б.
    `{{< ghcode "https://raw…" >}}` — приклад коду з іншого репозиторію, якщо адреса є в
    білому списку. Виноски `call-out` — підпис «Note:», вкладки й розгортки — підпис зі своєю
    назвою. Порожня вставка на кшталт `{{< nic-version >}}` — номер поточного випуску: файл
    шаблону (`conf["shortcodes"]`) у цьому сайті — сам номер, і він стає на її місце. Решта
    вставок (`ref`, `nb`, `table`, `icon`, `img`) знімаються, а текст між ними лишається.
    Вставка, якої не вдалося прочитати, просто випадає: ціле завантаження через неї не
    обривається."""
    def fetch(url: str) -> str:
        if not ctx.allowed(url):
            return ""
        code, data = ctx.fetch(url)
        return data.decode("utf-8", errors="replace") if code == "200" else ""

    def include(m):
        path = m.group(1) if m.group(1).endswith(".md") else m.group(1) + ".md"
        piece = fetch(f"{base}{conf.get('includes', 'content/includes')}/{path}")
        if not piece or depth >= 3:
            return ""
        return "\n" + _hugo(_markup.front_matter(piece)[1], ctx, base, conf, depth + 1) + "\n"

    def ghcode(m):
        code = fetch(m.group(1))
        return f"\n```\n{code.strip()}\n```\n" if code else ""

    def callout(m):
        args = re.findall(r'"([^"]*)"', m.group(1))
        kind = (re.search(r'class="([^"]*)"', m.group(1)) or [None, args[0] if args else "note"])[1]
        title = re.search(r'title="([^"]*)"', m.group(1))
        label = kind.split()[0].capitalize() if kind else "Note"
        rest = title.group(1) if title else (args[1] if len(args) > 1 and "class=" not in m.group(1) else "")
        return f"\n\n{label}: {rest}".rstrip() + "\n\n"

    def bare(m):
        if m.group(1) not in cache:
            value = fetch(f"{base}{conf.get('shortcodes', 'layouts/shortcodes')}/{m.group(1)}.html").strip()
            cache[m.group(1)] = value if value and len(value) <= 40 and "{{" not in value and "<" not in value else ""
        return cache[m.group(1)]

    cache: dict = conf.setdefault("_cache", {})
    text = _HUGO_INCLUDE.sub(include, text)
    text = _HUGO_GHCODE.sub(ghcode, text)
    text = _HUGO_CALLOUT.sub(callout, text)
    text = _HUGO_LABEL.sub(lambda m: f"\n\n{m.group(1)}:\n\n", text)
    text = _HUGO_BARE.sub(bare, text)
    return _HUGO_ANY.sub("", text)


_SOURCE_TAG = re.compile(r"<(ComponentPreview|ComponentExample|ComponentSource)\b"
                         r"((?:[^<>\"{}]|\"[^\"]*\"|\{[^{}]*\})*?)/?>")
_SOURCE_KIND = {"ComponentPreview": "example", "ComponentExample": "example",
                "ComponentSource": "source"}
_BASES = ("radix", "base", "aria")


def _template_rx(template: str) -> re.Pattern:
    """Шаблон шляху (`{root}/examples/{base}/{name}.tsx`) → вираз, яким тека тегу
    відбирає файли, що можуть знадобитися: усіх файлів дерева в пам'яті не тримаємо."""
    parts = re.split(r"(\{root\}|\{base\}|\{name\})", template)
    slots = {"{root}": ".+?", "{base}": "[^/]+", "{name}": ".+"}
    return re.compile("^" + "".join(slots.get(p, re.escape(p)) for p in parts) + "$")


def _sources(text: str, meta: dict, path: str, files: dict, conf: dict, fetch) -> str:
    """Вставки коду shadcn/ui → блоки коду. Сторінка компонента показує приклади тегом
    `<ComponentPreview name="dialog-demo" />`, а сам компонент —
    `<ComponentSource name="dialog" />`; код лежить у файлах реєстру того самого тегу
    (`apps/v4/examples/radix/dialog-demo.tsx`, `apps/www/registry/new-york/ui/dialog.tsx`).
    Без нього на сторінці лишався б заголовок «Custom Close Button» без жодного рядка коду.
    Шлях — перший із шаблонів `conf`, що є в дереві тегу; `{root}` — тека сайту (частина
    шляху до `/content/`), `{base}` — бібліотека примітивів сторінки (`radix`, `base`,
    `aria`: префікс `styleName` або поле `base` шапки). Вставка, якої не знайдено, лишає
    назву прикладу текстом."""
    root = path.split("/content/", 1)[0]

    def put(m):
        attrs = {k: (a if a is not None else b if b is not None else "true")
                 for k, a, b in _JSX_ATTR.findall(m.group(2))}
        kind = _SOURCE_KIND[m.group(1)]
        name = (attrs.get("fileName") if kind == "source" and attrs.get("fileName")
                else attrs.get("name", ""))
        style = attrs.get("styleName", "").split("-", 1)[0]
        base = (style if style in _BASES
                else meta.get("base") if meta.get("base") in _BASES else "radix")
        if attrs.get("src"):
            candidates = [f"{root}/{attrs['src'].lstrip('/')}"]
            name = name or re.sub(r"\.tsx?$", "", "/".join(attrs["src"].rsplit("/", 2)[-2:]))
        else:
            candidates = [t.format(root=root, base=base, name=name) for t in conf.get(kind) or ()]
        found = next((c for c in candidates if c in files), "")
        code = fetch(found, files[found]) if found else ""
        label = attrs.get("title") or name
        desc = attrs.get("description", "").rstrip(".")
        head = (f"Example `{name}`" + (f" — {desc}" if desc else "") if kind == "example"
                else f"`{label}`")
        if not code:
            return f"\n\n{head}.\n\n" if name else ""
        return f"\n\n{head}:\n\n```tsx\n{code.strip()}\n```\n\n"

    return _SOURCE_TAG.sub(put, text)


def _split_title(text: str) -> tuple[str, str]:
    """(назва з заголовка першого непорожнього рядка, текст без нього). Заголовок
    далі в тексті — підрозділ, а не назва."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        m = _ATX.match(line)
        if m:
            return m.group(2), "\n".join(lines[:i] + lines[i + 1:])
        break
    return "", text


@register("ghdocs-history")
def ghdocs_history(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/.")
    owner, repo = m.groups()
    tags = source.get("tags")
    if not isinstance(tags, dict) or not tags:
        raise SystemExit(f"{source['id']}: читач ghdocs-history потребує поля tags — "
                         f"об'єкта «тег → версія».")
    folders = [f.strip("/") for f in source.get("folders") or ["docs"]]
    files = {f.strip("/") for f in source.get("files") or ()}
    recursive = source.get("recursive") is True
    exts = tuple(source.get("extensions") or (".md",))
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    prefixes = dict(source.get("title_prefix") or {})
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""
    sites = [(re.compile(k), v) for k, v in (source.get("site") or {}).items()]
    labels = dict(source.get("component_labels") or {})
    nginx_xml = source.get("nginx_xml") is True
    hugo = dict(source["hugo"]) if isinstance(source.get("hugo"), dict) else None
    path_version = [(re.compile(a), b) for a, b in source.get("path_version") or ()]
    sources = dict(source["jsx_sources"]) if isinstance(source.get("jsx_sources"), dict) else None
    wanted = [_template_rx(t) for k in ("example", "source") for t in (sources or {}).get(k) or ()]
    base_ui = source.get("base_ui") is True
    if base_ui:
        wanted += _baseui.WANTED
    # тег → {шлях файла реєстру: sha}; вміст за sha — один раз на весь прогін
    registry: dict = {}
    code_cache: dict = {}

    # ім'я документа → [шлях, [теги]]; порядок ключів — порядок першої появи, тобто
    # від найновішого тегу, бо `tags` оголошено від найновішого. Ключ — ім'я, а не
    # шлях: у 2.x той самий файл лежав то як «Testing.md», то як «testing.md», і
    # дві такі пари з одним вмістом дали б одне ім'я файла — друга затерла б першій
    # перелік версій. Тут вони — один документ з версіями обох.
    seen: dict = {}
    for tag in tags:
        url = f"{source['url']}{tag}?recursive=1"
        try:
            tree = json.loads(ctx.text(url))
        except ValueError as exc:
            raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
        if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
            raise SystemExit(f"{url}: у відповіді немає дерева файлів.")
        if tree.get("truncated"):
            raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
        if wanted:
            registry[tag] = {e["path"]: e["sha"] for e in tree["tree"] if e.get("type") == "blob"
                             and any(r.match(e.get("path", "")) for r in wanted)}
        for entry in tree["tree"]:
            path = entry.get("path", "")
            folder, _, leaf = path.rpartition("/")
            inside = path in files or (
                folder in folders if not recursive else
                any(folder == f or folder.startswith(f + "/") for f in folders))
            # Порожній файл — не документ і не історія: з нього нема чого читати.
            if (entry.get("type") == "blob" and inside and leaf.endswith(exts)
                    and not _LOCALE.search(leaf) and entry.get("size", 1) > 0
                    and not any(r.search(path) for r in exclude)):
                stem = re.sub(r"\.mdx?$", "", path)
                sha = entry["sha"]
                if base_ui:
                    sha = _baseui.revision(path, sha, registry[tag])
                name = f"{lead}{_markup.slug(stem)}-{sha[:8]}"
                seen.setdefault(name, [path, []])[1].append(tag)

    order = {t: i for i, t in enumerate(tags)}
    items = []
    for name, (path, found) in seen.items():
        found = sorted(set(found), key=order.get)
        tag = found[0]
        # У шляхах 0.x бувають пробіли («doc/04 Locations/…»): без екранування
        # такої адреси urllib не відправить зовсім.
        where = f"{owner}/{repo}/{quote(tag, safe='@')}/{quote(path)}"
        raw = f"https://raw.githubusercontent.com/{where}"
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{where.split('/', 2)[2]}"
        # Відповідь має вести туди, де людина читає документ, — на сайт, а не в репозиторій.
        hit = next((m.expand(v) for r, v in sites if (m := r.fullmatch(path))), "")
        blob = hit.replace("{version}", str(tags[tag])) or blob
        # Кілька тегів з однією міткою (усі experimental-збірки) — одна версія.
        version = ", ".join(dict.fromkeys(tags[t] for t in found))
        # Сайт, що тримав окремий файл на кожну версію (`components/dialog/1.1.2.mdx`), — версія
        # в імені файла, а не в тезі, на якому файл знайшовся.
        version = next((m.expand(v) for r, v in path_version if (m := r.search(path))), version)

        def make(raw=raw, blob=blob, path=path, version=version, tag=tag):
            text = ctx.text(raw)
            if nginx_xml and path.endswith(".xml"):
                # XML nginx.org буває, що починається з `<!DOCTYPE module`, — це не сторінка
                # помилки, тож перевірку на HTML робить уже перетворений текст.
                text = _nginxxml.to_markdown(text)
            _markup.refuse_html(text, raw)
            meta, rest = _markup.front_matter(text)
            if hugo:
                rest = _hugo(rest, ctx, f"https://raw.githubusercontent.com/{owner}/{repo}/"
                                        f"{quote(tag, safe='@')}/", hugo)
            def fetch(where, sha, tag=tag):
                if sha not in code_cache:
                    url = (f"https://raw.githubusercontent.com/{owner}/{repo}/"
                           f"{quote(tag, safe='@')}/{quote(where)}")
                    code, data = ctx.fetch(url) if ctx.allowed(url) else ("", b"")
                    code_cache[sha] = (data.decode("utf-8", errors="replace")
                                       if code == "200" else "")
                return code_cache[sha]

            if sources is not None:
                rest = _sources(rest, meta or {}, path, registry.get(tag, {}), sources, fetch)
            # До викидання `import`: саме з них видно, який файл стоїть за тегом вставки.
            if base_ui:
                rest = _baseui.expand(rest, path, registry.get(tag, {}), fetch)
            # Обидва — до викидання `export`: таблиці беруть дані саме з них.
            if source.get("jsx_props") is True:
                rest = _jsx_props(rest)
            if labels:
                rest = _component_labels(rest, labels)
            if source.get("admonitions") is True:
                rest = _admonitions(rest)
            if path.endswith(".mdx") or source.get("mdx") is True:
                # Імпорти й експорти MDX — код сторінки, а не її текст.
                rest = _markup.mdx_statements_out(rest)
            if source.get("react_spectrum") is True:
                rest = _RS_HIGHLIGHT.sub("", _RS_EXPR.sub("", _RS_FRONT.sub(
                    "", _RS_COMMENT.sub("", rest), count=1)))
            # Рядок із самою картинкою (логотип над заголовком) тексту не несе, а стоячи
            # першим, ховав від _split_title справжню назву сторінки.
            if source.get("yaml_history") is True:
                rest = _yaml_history(rest)
            rest = _atx(_IMAGE_LINE.sub("", rest))
            title = meta.get("title", "") if meta else ""
            if not title:
                title, rest = _split_title(rest)
            # Картинка в заголовку — шапка чи іконка сторінки («# ![OWASPHeader](…)», «# A01:2025
            # … ![icon](…){: style=…}»), а не слова назви: інакше назвою ставала розмітка.
            title = _ATTRS.sub("", _IMAGE.sub("", title)).strip()
            if not title:
                title = re.sub(r"\.mdx?$", "", path.rsplit("/", 1)[-1])
            # У 4.x–5.x назва пишеться «# &lt;Route>»: на сайті це «<Route>».
            title = unescape(title)
            # Найдовший початок виграє: вкладена тека може належати іншій обгортці.
            owner_name = max(((k, v) for k, v in prefixes.items() if path.startswith(k)),
                             key=lambda kv: len(kv[0]), default=("", ""))[1]
            if owner_name and owner_name.lower() not in title.lower():
                title = f"{owner_name}: {title}"
            body = _markup.markdown_body(rest)
            # Файл на закріпленому тезі — не сторінка помилки (від HTML захищає
            # refuse_html), тож і коротке тіло («сторінку перенесено»), і порожнє —
            # теж історія. Порожнє буває двох видів: рубрика меню сайту з самою
            # шапкою («title: Guides») і заготовка старих версій з самим заголовком
            # («# IndexLink»). Фрагментів такий документ не дасть, бо порожнього
            # тексту корпус не ділить, але те, що сторінка була, лишається.
            if body.strip():
                _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: у теках {', '.join(folders)} жодного "
                         f"дозволеного .md на жодному з {len(tags)} тегів.")
    return items
