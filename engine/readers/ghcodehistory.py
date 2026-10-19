"""Читач історії коду репозиторію: один документ на кожен неповторний вміст файла з багатьох тегів.

`ghcode-history` — файли коду (не markdown) з багатьох тегів одного репозиторію разом.
                   `url` — префікс дерев через API (…/repos/ВЛАСНИК/РЕПО/git/trees/), поле
                   `tags` — об'єкт «тег → версія», від найновішого; `include` — вирази шляхів,
                   що беруться. Необов'язкові: `exclude` — вирази шляхів, що не беруться,
                   `name_prefix` — рядок перед іменем документа; `outline: true` — файл
                   JavaScript ділиться на розділи (див. `_outline`), файл Solidity — так само
                   (див. `_outline_sol`); `outline` переліком мов (`["go"]`, `["python"]`,
                   `["csharp"]`) — на розділи ділиться лише код цих мов (див. `_outline_go`,
                   `_outline_py`, `_outline_cs`);
                   `max_file` — межа розміру файла в байтах замість спільної (40 000);
                   `outline_indent: "auto"` — відступ членів типу C# береться з першого рядка
                   його тіла, а не як відступ типу плюс чотири пробіли. Testcontainers for .NET
                   пише код з відступом у два пробіли (простір імен блоком, тип на 2, члени на
                   4), а тести — на чотири (простір імен рядком), і під правилом «плюс чотири»
                   весь клас ContainerBuilder на 28 тисяч символів лишався одним розділом. Без
                   поля поділ той самий, що й був.

Навіщо. `ghcode` бере дерево одного тегу, а `ghdocs-history` бере багато тегів, але читає
кожен файл як markdown. CSP-збірка Alpine.js описана на сайті однією сторінкою, і та
відстає від коду: що саме приймає розбирач виразів і з якої версії, видно лише з
`packages/csp/src` і тестів розбирача. Знімок на одному тезі не відповідає на «чи працює
це в 3.15.2», а знімок на кожному з сотні тегів — сотня дослівних повторів.

Тут, як і в `ghdocs-history`, одиниця — пара «шлях, вміст» (вміст упізнається хешем blob
із дерева тегу): така пара стає одним документом, а в його версії лягають усі теги, де
файл лежав саме таким. Фільтр `version: "3.15"` знаходить рівно ту редакцію коду, що
стояла в лінії. Адреса в шапці — blob на найновішому з цих тегів. Текст лягає блоком коду
з мовою за розширенням, як у `ghcode`; файли понад той самий поріг не беруться.

Навіщо `outline`. Цілий файл — один фрагмент: тести розбирача CSP — 32 тисячі символів, і
вектор бачить лише їхній початок, а `read_section` віддає все разом. Поділені на розділи
`describe`/`it`/`test`, тести стають переліком «що підтримується» з назвою кожного випадку,
а злиття однакових фрагментів між редакціями (`revision_suffix`) лишає кожному тестові
версії, у яких він був, — тобто з якої версії збірка це вміє. Код ділиться так само за
оголошеннями верхнього рівня й методами класів.

Навіщо перелік мов. `api/types.go` Ollama — 44 тисячі символів: структура Options з
`num_ctx` і `num_predict`, запити й відповіді всіх ендпоінтів; `ollama/_client.py` клієнта
Python — 41 тисяча. Цілим фрагментом вектор бачив би лише імпорти. Але `outline: true` уже
стоїть у джерелі redis, що бере й файли `.py`: поділ Python під тим самим `true` змінив би
звірений примірник. Перелік вмикає нові мови лише там, де їх назвали.
"""

import json
import re
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register
from engine.readers.ghcode import _MAX_FILE, _lang

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")

# Межі розділів: виклик набору тестів чи тесту з назвою-рядком (рівень — за відступом),
# оголошення верхнього рівня і метод класу на відступі в чотири пробіли.
_TEST = re.compile(r"""^( *)(?:describe|it|test)(?:\.\w+)?\(\s*(['"`])(.+?)\2""")
_DECL = re.compile(r"^(?:export\s+(?:default\s+)?)?(?:async\s+)?(class|function)\s+([A-Za-z_$][\w$]*)")
_METHOD = re.compile(r"^    (?:static\s+|async\s+|get\s+|set\s+)*([A-Za-z_$][\w$]*)\s*\([^)]*\)\s*\{\s*$")
_NOT_METHOD = {"if", "for", "while", "switch", "catch", "function", "return"}


def _outline(text: str, lang: str) -> str:
    """Тіло з розділами: заголовок markdown на кожній межі, під ним — блок коду до наступної."""
    parts: list = [["", []]]
    owner = ""
    for line in text.rstrip().split("\n"):
        heading = ""
        if m := _TEST.match(line):
            heading = f"{'#' * min(2 + len(m[1]) // 4, 6)} {m[3]}"
        elif m := _DECL.match(line):
            owner = m[2] if m[1] == "class" else ""
            heading = f"## {m[1]} {m[2]}"
        elif owner and (m := _METHOD.match(line)) and m[1] not in _NOT_METHOD:
            heading = f"### {owner}.{m[1]}()"
        if heading:
            parts.append([heading, []])
        parts[-1][1].append(line)
    out = []
    for heading, lines in parts:
        code = "\n".join(lines).strip("\n")
        if not code.strip():
            continue
        out.append(f"{heading}\n\n```{lang}\n{code}\n```" if heading else f"```{lang}\n{code}\n```")
    return "\n\n".join(out)


# Solidity: контракт, інтерфейс чи бібліотека верхнього рівня; рядок-банер групи
# («// ======== Environment ========», так Vm.sol ділить читкоди); член на відступі в чотири
# пробіли; рядок NatSpec, що стоїть над членом і належить йому.
_SOL_UNIT = re.compile(r"^(?:abstract\s+)?(contract|interface|library)\s+([A-Za-z_]\w*)")
_SOL_BANNER = re.compile(r"^[ \t]*//[ \t]*={3,}[ \t]*(\S.*?)[ \t]*={3,}[ \t]*$")
_SOL_MEMBER = re.compile(r"^ {4}(?:function\s+([A-Za-z_]\w*)|(?:modifier|event|error|struct|enum)\s+"
                         r"([A-Za-z_]\w*))")
_SOL_DOC = re.compile(r"^[ \t]*(?:///|/\*\*|\*(?!/)|\*/)")


def _outline_sol(text: str) -> str:
    """Файл Solidity з розділами: контракт, група банера, член разом із NatSpec над ним.

    Навіщо. `Vm.sol` forge-std — 160 тисяч символів, інтерфейс сотень читкодів, кожен з описом
    NatSpec. Цілим файлом він або не береться зовсім (межа розміру), або ріжеться на шматки
    посеред опису. Розділ на член дає фрагменту назву читкоду, а злиття однакових фрагментів
    між редакціями лишає кожному члену версії, у яких він був такий. Перевантаження, що йдуть
    поспіль, — один розділ: це той самий читкод."""
    parts: list = [["", []]]
    unit, last, used = "", "", {}
    for line in text.rstrip().split("\n"):
        heading = ""
        if m := _SOL_UNIT.match(line):
            unit, last = m[2], ""
            heading = f"## {m[1]} {m[2]}"
        elif unit and (m := _SOL_BANNER.match(line)):
            last = ""
            heading = f"### {unit}: {m[1]}"
        elif unit and (m := _SOL_MEMBER.match(line)):
            name = m[1] or m[2]
            if name != last:
                heading = f"#### {unit}.{name}" + ("()" if m[1] else "")
            last = name
        if heading:
            # Той самий заголовок удруге (перевантаження далі у файлі) дав би розділ з тим
            # самим ключем — номер його розводить.
            used[heading] = used.get(heading, 0) + 1
            if used[heading] > 1:
                heading = f"{heading} ({used[heading]})"
            lines, doc = parts[-1][1], []
            while lines and _SOL_DOC.match(lines[-1]):
                doc.insert(0, lines.pop())
            parts.append([heading, doc])
        parts[-1][1].append(line)
    out = []
    for heading, lines in parts:
        code = "\n".join(lines).strip("\n")
        if not code.strip():
            continue
        out.append(f"{heading}\n\n```solidity\n{code}\n```" if heading
                   else f"```solidity\n{code}\n```")
    return "\n\n".join(out)


# Заголовки C/C++ з коментарями Doxygen (ICU): розділ починається коментарем «/** … */» і
# триває до наступного такого коментаря; назва розділу — те, що оголошує перше оголошення
# під ним. Макроси на кшталт U_CAPI, U_EXPORT2 назвою не бувають.
_C_KIND = re.compile(r"\b(class|struct|union|enum(?:\s+class)?|namespace)\s+(?:U_\w+\s+)*([A-Za-z_]\w*)")
_C_CALL = re.compile(r"([A-Za-z_~][\w:~]*)\s*\(")
_C_LAST = re.compile(r"([A-Za-z_]\w*)\s*(?:\[[^\]]*\])?\s*(?:=[^;]*)?;")
_C_MACRO = re.compile(r"^(?:U_[A-Z0-9_]+|if|while|for|switch|sizeof|return)$")


def _c_heading(comment: list, decl: list) -> str:
    """Назва розділу за коментарем і першим оголошенням під ним."""
    for line in comment:
        if m := re.search(r"[@\\]file\s+(\S+)", line):
            return f"## File {m[1]}"
    text = " ".join(x.strip() for x in decl).strip()
    if m := re.match(r"#\s*define\s+([A-Za-z_]\w*)", text):
        return f"## {m[1]}"
    if (m := _C_KIND.search(text)) and "(" not in text.split(m[0])[0]:
        return f"## {m[1].split()[0]} {m[2]}"
    for m in _C_CALL.finditer(text):
        if not _C_MACRO.match(m[1]):
            return f"## {m[1]}()"
    if m := _C_LAST.search(text):
        return f"## {m[1]}"
    return ""


def _outline_c(text: str) -> str:
    """Заголовок C/C++ з розділами: коментар Doxygen разом з оголошенням, що йде під ним."""
    lines = text.rstrip().split("\n")
    parts: list = [["", []]]
    used: dict = {}
    i, n = 0, len(lines)
    while i < n:
        if re.match(r"^\s*/\*\*", lines[i]):
            j = i
            while j < n and "*/" not in lines[j]:
                j += 1
            comment = lines[i:j + 1]
            k, decl = j + 1, []
            while k < n and len(decl) < 14 and not re.match(r"^\s*/\*\*", lines[k]):
                decl.append(lines[k])
                if re.search(r"[;{]\s*(?://.*)?$", lines[k]) or lines[k].lstrip().startswith("#"):
                    break
                k += 1
            heading = _c_heading(comment, decl)
            if heading:
                used[heading] = used.get(heading, 0) + 1
                if used[heading] > 1:
                    heading = f"{heading} ({used[heading]})"
            parts.append([heading, []])
            parts[-1][1].extend(comment)
            i = j + 1
            continue
        parts[-1][1].append(lines[i])
        i += 1
    out = []
    for heading, body in parts:
        code = "\n".join(body).strip("\n")
        if not code.strip():
            continue
        out.append(f"{heading}\n\n```c\n{code}\n```" if heading else f"```c\n{code}\n```")
    return "\n\n".join(out)


# Go: оголошення верхнього рівня — функція чи метод (отримувач стає власником), тип, змінна,
# константа; коментар упритул над оголошенням належить йому.
_GO_FUNC = re.compile(r"^func\s+(?:\(\s*\w*\s*\*?\s*([A-Za-z_]\w*)(?:\[[^\]]*\])?\s*\)\s*)?"
                      r"([A-Za-z_]\w*)")
_GO_DECL = re.compile(r"^(type|var|const)\s+(?:(\()|([A-Za-z_]\w*))")
_GO_ITEM = re.compile(r"^\t([A-Za-z_]\w*)\b")
# Розділ коротший за це приклеюється до попереднього (той самий поріг, що в `ghcode-history-ts`).
_MIN_PART = 200


def _go_heading(line: str, following: list) -> str:
    if m := _GO_FUNC.match(line):
        return f"## {m[1]}.{m[2]}()" if m[1] else f"## {m[2]}()"
    m = _GO_DECL.match(line)
    if not m:
        return ""
    if m[3]:
        return f"## {m[1]} {m[3]}"
    names = []
    for item in following:
        if item.startswith(")"):
            break
        if (n := _GO_ITEM.match(item)) and n[1] not in names:
            names.append(n[1])
    shown = ", ".join(names[:8]) + (", …" if len(names) > 8 else "")
    return f"## {m[1]} {shown}" if shown else ""


def _outline_go(text: str) -> str:
    """Файл Go з розділами: заголовок на кожне оголошення верхнього рівня разом з його коментарем."""
    lines = text.rstrip().split("\n")
    parts: list = [["", []]]
    raw_string = False
    for i, line in enumerate(lines):
        heading = "" if raw_string else _go_heading(line, lines[i + 1:])
        if not line.lstrip().startswith("//") and line.count("`") % 2:
            raw_string = not raw_string
        if heading:
            prev = parts[-1][1]
            lead = []
            while prev and prev[-1].startswith("//"):
                lead.insert(0, prev.pop())
            parts.append([heading, lead])
        parts[-1][1].append(line)
    return _join(parts, "go", glue=lambda heading: True)


# Python: клас, функція чи метод (на відступі тіла класу — ollama-python пише двома пробілами,
# більшість коду чотирма); декоратори й коментарі впритул над оголошенням належать йому,
# перевантаження (`@overload`) одного методу — один розділ.
_PY_DEF = re.compile(r"^( *)(?:async\s+)?(def|class)\s+([A-Za-z_]\w*)")
_PY_LEAD = re.compile(r"^ *(?:@|#)")


def _outline_py(text: str) -> str:
    """Файл Python з розділами: класи, функції й методи класів верхнього рівня."""
    lines = text.rstrip().split("\n")
    parts: list = [["", []]]
    owner, body = "", ""
    in_string = False
    for line in lines:
        heading = ""
        if owner and not body and line.strip() and line[0] == " ":
            body = line[:len(line) - len(line.lstrip(" "))]
        if not in_string and (m := _PY_DEF.match(line)):
            if not m[1]:
                owner, body = (m[3] if m[2] == "class" else ""), ""
                heading = f"## {m[2]} {m[3]}" if m[2] == "class" else f"## {m[3]}()"
            elif owner and m[1] == body and m[2] == "def":
                heading = f"### {owner}.{m[3]}()"
        elif not in_string and line and not line[0].isspace() and not _PY_LEAD.match(line):
            owner, body = "", ""
        if line.count('"""') % 2 or line.count("'''") % 2:
            in_string = not in_string
        if heading:
            prev = parts[-1][1]
            lead = []
            while prev and prev[-1].strip() and _PY_LEAD.match(prev[-1]):
                lead.insert(0, prev.pop())
            if heading == parts[-1][0]:
                parts[-1][1].extend(lead)
            else:
                parts.append([heading, lead])
        parts[-1][1].append(line)
    return _join(parts, "python", glue=lambda heading: not heading.startswith("## "))


# C#: оголошення типу (клас, структура, інтерфейс, запис, перелік) і член типу на відступі його
# тіла (тип + чотири пробіли — так пишуть dotnet/efcore і dotnet/ef6, і з простором імен-блоком,
# і з простором імен на файл); коментар документації «///» і атрибути «[…]» впритул над членом
# належать йому. Рядок, що продовжує попередній (перелік базових типів, «=> …», «: base(…)»,
# «where T : …», аргументи атрибута), членом не стає.
_CS_TYPE = re.compile(r"^( *)(?:(?:public|internal|private|protected|static|sealed|abstract|partial|"
                      r"readonly|unsafe|new|file|ref)\s+)*(class|struct|interface|enum|record(?:\s+struct|"
                      r"\s+class)?)\s+([A-Za-z_@]\w*(?:<[^>{(]*>)?)")
_CS_NAME = re.compile(r"(?:\boperator\s*(\S+?)\s*\(|\bthis\s*\[|([A-Za-z_@]\w*)"
                      r"(?:<(?:[^<>()]|<[^<>()]*>)*>)?\s*\()")
_CS_PLAIN = re.compile(r"([A-Za-z_@]\w*)\s*(?:\{|=>|=|;|$)")
_CS_NOT_START = re.compile(r"^(?:\{|\}|//|/\*|\*|\[|#|\)|=>|=|:|\.|\+|-|\?|&&|\|\||,|\"|where\b)")


def _cs_state(line: str, state: str) -> str:
    """Стан після рядка: "" — код, "raw" — усередині «\"\"\"…», "verbatim" — усередині «@\"…»,
    "comment" — усередині «/* … */». Навіщо: тести EF Core тримають очікуваний SQL у
    багаторядкових рядках, і рядок SQL з відступом члена не мусить ставати членом."""
    i, n = 0, len(line)
    while i < n:
        if state == "comment":
            j = line.find("*/", i)
            if j < 0:
                return state
            state, i = "", j + 2
        elif state == "raw":
            j = line.find('"""', i)
            if j < 0:
                return state
            state, i = "", j + 3
            while i < n and line[i] == '"':
                i += 1
        elif state == "verbatim":
            j = line.find('"', i)
            if j < 0:
                return state
            if line[j + 1:j + 2] == '"':
                i = j + 2
                continue
            state, i = "", j + 1
        elif line.startswith("//", i):
            return state
        elif line.startswith("/*", i):
            state, i = "comment", i + 2
        elif line.startswith('"""', i):
            state, i = "raw", i + 3
            while i < n and line[i] == '"':
                i += 1
        elif line[i] == '"' and (line[i - 1:i] == "@" or line[max(0, i - 2):i] == "$@"):
            state, i = "verbatim", i + 1
        elif line[i] == '"':
            i += 1
            while i < n and line[i] != '"':
                i += 2 if line[i] == "\\" else 1
            i += 1
        elif line[i] == "'":
            m = re.match(r"'(?:\\.[^']*|[^'\\])'", line[i:])
            i += len(m.group(0)) if m else 1
        else:
            i += 1
    return state


def _cs_member(line: str) -> str:
    """Ім'я члена з рядка оголошення: метод і конструктор — «Ім'я()», індексатор — «this[]»,
    оператор — «operator ==», властивість, поле, подія — саме ім'я."""
    code = re.sub(r"\[[^\]]*\]", "", line.split("//", 1)[0]).strip()
    m = _CS_NAME.search(code)
    arrow = code.find("=>")
    assign = code.replace("=>", "  ").find("=")
    if m and (arrow < 0 or m.start() < arrow) and (assign < 0 or m.start() < assign):
        if m.group(1):
            return f"operator {m.group(1)}"
        if m.group(0).lstrip().startswith("this"):
            return "this[]"
        return f"{m.group(2)}()"
    m = _CS_PLAIN.search(code)
    return m.group(1) if m else ""


def _outline_cs(text: str, auto: bool = False) -> str:
    """Файл C# з розділами: тип — «## class DbContext», член — «### DbContext.SaveChanges()»
    разом з його «///» і атрибутами; перевантаження, що йдуть поспіль, — один розділ, той
    самий заголовок далі у файлі дістає номер. Шапка файла (ліцензія, using, простір імен)
    входить у розділ першого типу.

    Навіщо. Код і тести EF Core чотирнадцяти ліній — тридцять тисяч редакцій файлів: DbContext.cs
    — 113 тисяч символів, тести перекладу запитів — сотні методів з очікуваним SQL кожен. Поділені
    за довжиною, вони давали б фрагменти посеред методу, і зміна одного рядка зсувала б усі
    наступні. Розділ на член дає фрагментові ім'я методу, а незмінний член сусідніх версій
    зливається в один фрагмент з усіма ними (`revision_suffix`)."""
    parts: list = [["", []]]
    state = ""
    types: list = []      # [[відступ, ім'я, відступ членів]] — тип і вкладені в нього
    used: dict = {}
    lead_from = None      # з якого рядка поточної частини почалися «///» і атрибути члена
    awaiting = False      # між оголошенням типу і його «{»: базові типи, where
    for line in text.replace("\r\n", "\n").rstrip().split("\n"):
        inside, state = state, _cs_state(line, state)
        heading = ""
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))
        if not inside and stripped:
            if awaiting:
                awaiting = not ("{" in stripped or stripped.endswith(";"))
            elif stripped[0] not in "{}":
                while types and indent <= types[-1][0]:
                    types.pop()
                m = _CS_TYPE.match(line)
                if auto and types and types[-1][2] is None and indent > types[-1][0] \
                        and not stripped.startswith("#"):
                    types[-1][2] = indent  # перший рядок тіла типу задає відступ членів
                member = (types[-1][2] or types[-1][0] + 4) if types else None
                if m and (member is None or indent < member):
                    types.append([indent, re.sub(r"<.*", "", m.group(3)),
                                  None if auto else indent + 4])
                    heading = f"## {m.group(2).split()[0]} {m.group(3)}"
                    awaiting = "{" not in stripped and not stripped.endswith(";")
                elif member is not None and indent == member:
                    if stripped.startswith(("///", "[")):
                        if lead_from is None:
                            lead_from = len(parts[-1][1])
                    elif not _CS_NOT_START.match(stripped):
                        owner = types[-1][1]
                        if m:
                            heading = f"### {m.group(2).split()[0]} {owner}.{m.group(3)}"
                            types.append([indent, re.sub(r"<.*", "", m.group(3)),
                                          None if auto else indent + 4])
                            awaiting = "{" not in stripped and not stripped.endswith(";")
                        elif name := _cs_member(stripped):
                            heading = f"### {owner}.{name}"
                        if not heading:
                            lead_from = None
                    else:
                        lead_from = None
        if heading:
            prev = parts[-1][1]
            lead = prev[lead_from:] if lead_from is not None else []
            if lead_from is not None:
                del prev[lead_from:]
            lead_from = None
            if heading == parts[-1][0]:
                prev.extend(lead)
            elif heading.startswith("## ") and len(parts) == 1:
                parts[0] = [heading, prev + lead]
            else:
                used[heading] = used.get(heading, 0) + 1
                n = used[heading]
                parts.append([heading if n == 1 else f"{heading} ({n})", lead])
        parts[-1][1].append(line)
    return _join(parts, "csharp", glue=lambda heading: heading.startswith("### "))


def _join(parts: list, lang: str, glue) -> str:
    """Розділи в текст; куций розділ, якому `glue` дозволяє, приклеюється до попереднього."""
    merged: list = []
    for heading, body in parts:
        code = "\n".join(body).strip("\n")
        if not code.strip():
            continue
        if merged and heading and len(code) < _MIN_PART and glue(heading):
            merged[-1][1] += "\n\n" + code
            continue
        merged.append([heading, code])
    return "\n\n".join(f"{h}\n\n```{lang}\n{c}\n```" if h else f"```{lang}\n{c}\n```"
                       for h, c in merged)


@register("ghcode-history")
def ghcode_history(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/.")
    owner, repo = m.groups()
    tags = source.get("tags")
    if not isinstance(tags, dict) or not tags:
        raise SystemExit(f"{source['id']}: поле `tags` — об'єкт «тег → версія».")
    include = [re.compile(x) for x in source.get("include") or ()]
    if not include:
        raise SystemExit(f"{source['id']}: поле `include` — вирази шляхів, що беруться.")
    exclude = [re.compile(x) for x in source.get("exclude") or ()]
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""
    outline = source.get("outline") is True
    langs = source.get("outline") if isinstance(source.get("outline"), list) else []
    if set(langs) - {"go", "python", "csharp"}:
        raise SystemExit(f"{source['id']}: `outline` переліком знає лише мови «go», «python» "
                         f"і «csharp».")
    max_file = int(source.get("max_file") or _MAX_FILE)

    # ім'я документа → [шлях, [теги]]; порядок — від найновішого тегу, як оголошено в `tags`
    seen: dict = {}
    for tag in tags:
        url = f"{source['url']}{quote(tag, safe='@')}?recursive=1"
        try:
            tree = json.loads(ctx.text(url))
        except ValueError as exc:
            raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
        if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
            raise SystemExit(f"{url}: у відповіді немає дерева файлів.")
        if tree.get("truncated"):
            raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
        for entry in tree["tree"]:
            path = entry.get("path", "")
            if (entry.get("type") == "blob" and 0 < entry.get("size", 1) <= max_file
                    and any(r.search(path) for r in include)
                    and not any(r.search(path) for r in exclude)):
                name = f"{lead}{_markup.slug(path)}-{entry['sha'][:8]}"
                seen.setdefault(name, [path, []])[1].append(tag)

    order = {t: i for i, t in enumerate(tags)}
    items = []
    for name, (path, found) in seen.items():
        found = sorted(set(found), key=order.get)
        where = f"{owner}/{repo}/{quote(found[0], safe='@')}/{quote(path)}"
        raw = f"https://raw.githubusercontent.com/{where}"
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{where.split('/', 2)[2]}"
        version = ", ".join(dict.fromkeys(tags[t] for t in found))

        def make(path=path, raw=raw, blob=blob, version=version):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            lang = "solidity" if path.endswith(".sol") else _lang(path)
            if "go" in langs and path.endswith(".go"):
                body = _outline_go(text)
            elif "python" in langs and lang == "python":
                body = _outline_py(text)
            elif "csharp" in langs and path.endswith(".cs"):
                body = _outline_cs(text, source.get("outline_indent") == "auto")
            elif outline and lang in ("js", "ts"):
                body = _outline(text, lang)
            elif outline and lang == "solidity":
                body = _outline_sol(text)
            elif outline and path.endswith(".h"):
                body = _outline_c(text)
            else:
                body = f"```{lang}\n{text.rstrip()}\n```"
            title = f"{repo}: {path}"
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодного файла за `include` на жодному з "
                         f"{len(tags)} тегів.")
    return items
