"""Перетворювач сторінок man у розмітці mdoc (BSD) на markdown: file(1), magic(5), libmagic(3).

Навіщо. Сторінки file пишуться в mdoc — семантичній розмітці BSD (`.Nm`, `.Fl`, `.Bl -tag`, `.It`), а не в man(7),
яку розбирає `manpages.to_markdown`: той лишив би макроси як є, і опис кожної опції злипся б із назвами макросів.
Тут — підмножина mdoc, що трапляється в сторінках файлових інструментів: розділи, списки (`-tag`, `-bullet`,
`-enum`, `-column`), блоки (`.Bd -literal`), вбудовані макроси опцій, аргументів, посилань і лапок. Пункт списку
стає рядком «- `MAGIC_MIME_TYPE` — опис»: назва й опис лежать поруч, і пошук знаходить їх разом; опція розділу
OPTIONS — власним підрозділом «### `-i`, `--mime`», бо сорок опцій одним фрагментом пошук не розрізняє.

`is_mdoc` упізнає таку сторінку за `.Dd`/`.Sh` без `.TH` — останній має лише man(7).
"""

import re

from engine.readers.manpages import _args, inline

_DELIM_AFTER = {".", ",", ":", ";", ")", "]", "?", "!"}
_DELIM_BEFORE = {"(", "["}
_ENCLOSE = {"Dq": ("“", "”"), "Sq": ("‘", "’"), "Pq": ("(", ")"), "Bq": ("[", "]"),
            "Brq": ("{", "}"), "Aq": ("<", ">"), "Op": ("[", "]"), "Qq": ('"', '"'),
            "Do": ("“", ""), "Dc": ("", "”"), "So": ("‘", ""), "Sc": ("", "’"), "Po": ("(", ""),
            "Pc": ("", ")"), "Bo": ("[", ""), "Bc": ("", "]"), "Oo": ("[", ""), "Oc": ("", "]"),
            "Ao": ("<", ""), "Ac": ("", ">"), "Qo": ('"', ""), "Qc": ("", '"')}
_CODE = {"Fl", "Cm", "Ic", "Li", "Ql", "Pa", "Ev", "Dv", "Er", "Ft", "Vt", "Fn", "Fo", "Ms"}
_ITALIC = {"Ar", "Va", "Fa", "Em"}
_PLAIN = {"No", "Tn", "Sx", "Nm", "An", "Pf", "Ns", "Ta", "Sy", "Xr", "In", "Lk", "Mt", "St",
          "Bx", "Ux", "Nx", "Fx", "Ox", "Bsx", "Dx", "At", "Ex", "Rv", "Xo", "Xc", "Ap", "Ot", "Es",
          "En", "Eo", "Ec", "Lb", "Cd", "Dt", "Ad", "Fr", "Ef", "Bf", "%A", "%B", "%D", "%I",
          "%J", "%N", "%O", "%P", "%Q", "%R", "%T", "%U", "%V"}
_MACROS = set(_ENCLOSE) | _CODE | _ITALIC | _PLAIN
_BSD = {"Bx": "BSD", "Ux": "UNIX", "Nx": "NetBSD", "Fx": "FreeBSD", "Ox": "OpenBSD", "Bsx": "BSD/OS",
        "Dx": "DragonFly", "At": "AT&T UNIX"}
_STD = {"-p1003.1": "IEEE Std 1003.1 (“POSIX.1”)", "-p1003.1-2001": "IEEE Std 1003.1-2001 (“POSIX.1”)",
        "-p1003.1-2008": "IEEE Std 1003.1-2008 (“POSIX.1”)", "-p1003.2": "IEEE Std 1003.2 (“POSIX.2”)",
        "-isoC": "ISO/IEC 9899:1990 (“ISO C90”)", "-isoC-99": "ISO/IEC 9899:1999 (“ISO C99”)",
        "-ansiC": "ANSI X3.159-1989 (“ANSI C89”)", "-susv2": "Version 2 of the Single UNIX Specification",
        "-svid4": "System V Interface Definition, Fourth Edition (“SVID4”)"}


def is_mdoc(src: str) -> bool:
    return bool(re.search(r"^\.(Dd|Sh)\b", src, re.M)) and not re.search(r"^\.TH\b", src, re.M)


class _Page:
    def __init__(self):
        self.name = ""                # перше .Nm — ним стає порожнє .Nm далі
        self.fo: list[str] | None = None

    def phrase(self, tokens: list[str]) -> str:
        """Аргументи рядка-макроса → текст. Макрос діє на слова до наступного макроса."""
        parts: list[tuple[str, bool]] = []   # (текст, пробіл перед ним)
        i, glue = 0, False

        def put(text: str, space: bool = True) -> None:
            nonlocal glue
            if text == "":
                return
            parts.append((text, space and not glue))
            glue = False

        while i < len(tokens):
            t = tokens[i]
            if t in _ENCLOSE:
                op, cl = _ENCLOSE[t]
                if t in ("Dq", "Sq", "Pq", "Bq", "Brq", "Aq", "Op", "Qq"):
                    rest = tokens[i + 1:]
                    tail = []
                    while rest and rest[-1] in _DELIM_AFTER:
                        tail.insert(0, rest.pop())
                    put(op + self.phrase(rest) + cl)
                    for d in tail:
                        put(d, False)
                    return self._join(parts)
                if op:
                    put(op)
                    glue = True
                else:
                    parts.append((cl, False))
                i += 1
                continue
            if t in ("Ns", "Ap"):
                glue = True
                if t == "Ap":
                    parts.append(("'", False))
                    glue = True
                i += 1
                continue
            if t == "Pf":
                # Префікс приліплюється до наступного слова без пробілу: «Pf ( Fl x» → «(-x».
                if i + 1 < len(tokens):
                    put(inline(tokens[i + 1]))
                    glue = True
                i += 2
                continue
            if t == "Fl":
                # «Fl Fl brief» — перше Fl без слова дає риску перед наступним: «--brief».
                n = 0
                while i < len(tokens) and tokens[i] == "Fl":
                    n, i = n + 1, i + 1
                words = []
                while i < len(tokens) and tokens[i] not in _MACROS:
                    words.append(tokens[i])
                    i += 1
                trail = []
                while words and words[-1] in _DELIM_AFTER:
                    trail.insert(0, words.pop())
                if not words:
                    put(f"`{'-' * n}`")
                for k, x in enumerate(words):
                    x = inline(x)
                    put(x if x == "|" else f"`{'-' * (n if k == 0 else 1)}{x}`")
                for d in trail:
                    put(d, False)
                continue
            if t in _MACROS:
                words = []
                j = i + 1
                while j < len(tokens) and tokens[j] not in _MACROS:
                    words.append(tokens[j])
                    j += 1
                trail = []
                while words and words[-1] in _DELIM_AFTER:
                    trail.insert(0, words.pop())
                self._macro(t, words, put, tokens[j] if j < len(tokens) else "")
                for d in trail:
                    put(d, False)
                i = j
                continue
            if t in _DELIM_AFTER:
                put(inline(t), False)
            elif t in _DELIM_BEFORE:
                put(t)
                glue = True
            else:
                put(inline(t))
            i += 1
        return self._join(parts)

    @staticmethod
    def _join(parts) -> str:
        out = ""
        for text, space in parts:
            out += (" " if space and out else "") + text
        return out

    def _macro(self, m: str, words: list[str], put, nxt: str) -> None:
        w = [inline(x) for x in words]
        if m == "Nm":
            if w and not self.name:
                self.name = w[0]
            put(f"**{' '.join(w) or self.name}**")
            return
        if m == "Xr":
            put(f"{w[0]}({w[1]})" if len(w) > 1 else " ".join(w))
            for x in w[2:]:
                put(x)
            return
        if m == "Fn":
            if w:
                put(f"`{w[0]}({', '.join(w[1:])})`")
            return
        if m == "Fo":
            self.fo = [w[0] if w else ""]
            return
        if m == "Fa" and self.fo is not None:
            self.fo.extend(w)
            return
        if m == "In":
            put(f"`#include <{' '.join(w)}>`")
            return
        if m == "Lk":
            put(f"{' '.join(w[1:])} ({w[0]})" if len(w) > 1 else (w[0] if w else ""))
            return
        if m == "Mt":
            put(" ".join(w))
            return
        if m == "St":
            put(_STD.get(w[0], w[0]) if w else "")
            for x in w[1:]:
                put(x)
            return
        if m in _BSD:
            put(_BSD[m] + (" " + " ".join(w) if w else ""))
            return
        if m == "Ex":
            names = [x for x in w if x != "-std"] or [self.name]
            put(f"The {', '.join(names)} utility exits 0 on success, and >0 if an error occurs.")
            return
        if m == "Rv":
            names = [x for x in w if x != "-std"] or [self.name]
            put(f"The {', '.join(n + '()' for n in names)} function returns the value 0 if "
                f"successful; otherwise the value -1 is returned and the global variable errno is "
                f"set to indicate the error.")
            return
        if m == "Sy":
            put(f"**{' '.join(w)}**" if w else "")
            return
        if m in _CODE or m in _ITALIC:
            # Слова одного виклику — одним шматком: «.Ft const char *» — це один тип.
            mark = "`" if m in _CODE else "*"
            chunk: list[str] = []
            for x in w:
                if x in ("|", "..."):
                    if chunk:
                        put(mark + " ".join(chunk) + mark)
                        chunk = []
                    put(x)
                else:
                    chunk.append(x)
            if chunk:
                put(mark + " ".join(chunk) + mark)
            return
        for x in w:
            put(x)


def to_markdown(src: str) -> tuple[str, str]:
    """Сторінка mdoc → (назва «ім'я(розділ) — опис», markdown)."""
    page = _Page()
    out: list[str] = []
    para: list[str] = []
    lists: list[str] = []            # типи вкладених .Bl
    head = None                      # пункт списку, що чекає на свій опис
    literal = False
    xo = False
    dt, nd, section = ("", ""), "", ""
    refs: list[str] = []

    def indent() -> str:
        return "  " * max(0, len(lists) - 1)

    def flush() -> None:
        nonlocal para, head
        text = " ".join(x for x in para if x).strip()
        para = []
        if head is not None and head.startswith("### "):
            out.append(head)
            if text:
                out.append(text)
            head = None
        elif head is not None:
            out.append(head + (" — " + text if text and not head.endswith("- ") else text))
            head = None
        elif text:
            out.append(indent() + text if lists else text)

    for raw in src.replace("\r\n", "\n").split("\n"):
        if raw.startswith(('.\\"', "'", '.\\\\"')) or raw.strip() in (".", ""):
            if not raw.strip() and not literal:
                flush()
            elif literal and not raw.strip():
                out.append("")
            continue
        if literal and not raw.startswith("."):
            out.append(inline(raw))
            continue
        if not raw.startswith("."):
            para.append(inline(raw))
            continue
        tokens = _args(raw[1:].strip())
        if not tokens:
            continue
        mac, args = tokens[0], tokens[1:]
        if mac == "Dd":
            continue
        if mac == "Dt":
            dt = (args[0] if args else "", args[1] if len(args) > 1 else "")
            continue
        if mac == "Os":
            continue
        if mac in ("Sh", "Ss"):
            flush()
            while lists:
                lists.pop()
            section = " ".join(inline(a) for a in args)
            out.append(("## " if mac == "Sh" else "### ") + section)
            continue
        if mac in ("Pp", "Lp", "sp", "PP", "LP"):
            flush()
            continue
        if mac == "br":
            flush()
            continue
        if mac == "Nd":
            nd = page.phrase(args)
            para.append("— " + nd)
            continue
        if mac == "Bl":
            flush()
            kind = next((a for a in args if a in ("-tag", "-bullet", "-enum", "-dash", "-hyphen",
                                                   "-item", "-column", "-hang", "-ohang", "-inset",
                                                   "-diag")), "-tag")
            lists.append(kind)
            continue
        if mac == "El":
            flush()
            if lists:
                lists.pop()
            continue
        if mac == "It":
            flush()
            kind = lists[-1] if lists else "-tag"
            if kind == "-column":
                cells, cur = [], []
                for a in args:
                    if a == "Ta":
                        cells.append(cur)
                        cur = []
                    else:
                        cur.append(a)
                cells.append(cur)
                out.append(indent() + " | ".join(page.phrase(c) for c in cells))
                continue
            if kind in ("-bullet", "-dash", "-hyphen", "-item"):
                head = indent() + "- "
                if args:
                    para.append(page.phrase(args))
                continue
            if kind == "-enum":
                head = indent() + "1. "
                continue
            if "Xo" in args:
                xo = True
                args = [a for a in args if a != "Xo"]
            if len(lists) == 1 and section.upper() == "OPTIONS":
                # Опція верхнього рівня — власний підрозділ («### `-i`, `--mime`»): розділ OPTIONS file(1) —
                # шість тисяч символів сорока опцій, і цілим фрагментом пошук не підіймав жодну з них.
                head = "### " + page.phrase(args)
            else:
                head = indent() + "- " + page.phrase(args)
            continue
        if mac == "Xc":
            xo = False
            continue
        if xo and head is not None:
            head += " " + page.phrase(tokens)
            continue
        if mac == "Bd":
            flush()
            if any(a in ("-literal", "-unfilled") for a in args):
                out.append("```")
                literal = True
            continue
        if mac == "Ed":
            if literal:
                out.append("```")
                literal = False
            flush()
            continue
        if mac in ("D1", "Dl"):
            flush()
            line = page.phrase(args)
            out.append(f"    {line}" if mac == "Dl" else line)
            continue
        if mac == "Rs":
            flush()
            refs = []
            continue
        if mac.startswith("%"):
            refs.append(page.phrase(args))
            continue
        if mac == "Re":
            out.append(", ".join(refs))
            refs = []
            continue
        if mac == "Fc":
            if page.fo is not None:
                name, *fa = page.fo
                para.append(f"`{name}({', '.join(fa)})`")
                page.fo = None
            continue
        if mac in ("Ft", "In") and section.upper() == "SYNOPSIS":
            # Рядок синопсиса — тип і функція разом: «const char * magic_error(magic_t cookie)».
            flush()
        if mac == "Nm" and section.upper() == "SYNOPSIS":
            flush()
        if mac in _MACROS:
            text = page.phrase(tokens)
            if literal:
                out.append(text)
            elif text:
                para.append(text)
            continue
        # Решта — запити roff (.ds, .de, .if, .nr, .ad, .na, .ft, .in, .ti, .TS…): тексту не несуть.
    flush()
    if literal:
        out.append("```")
    body = "\n\n".join(x for x in _merge_lists(out) if x is not None)
    name = dt[0].lower() or page.name
    title = f"{name}({dt[1]})" if dt[1] else name
    if nd:
        title = f"{title} — {nd}"
    return title, body


def _merge_lists(lines: list[str]) -> list[str]:
    """Сусідні пункти одного списку — одним блоком, рядок під рядком; огорожа коду — теж одним
    блоком, без порожніх рядків між її рядками."""
    out: list[str] = []
    block: list[str] = []
    fenced = False
    for ln in lines:
        if ln == "```":
            if not fenced:
                if block:
                    out.append("\n".join(block))
                block = ["```"]
                fenced = True
            else:
                block.append("```")
                out.append("\n".join(block))
                block, fenced = [], False
            continue
        if fenced:
            block.append(ln)
            continue
        is_item = ln.lstrip().startswith(("- ", "1. ")) or " | " in ln
        if is_item and block and (block[-1].lstrip().startswith(("- ", "1. ")) or " | " in block[-1]):
            block.append(ln)
            continue
        if block:
            out.append("\n".join(block))
        block = [ln]
    if block:
        out.append("\n".join(block))
    return out
