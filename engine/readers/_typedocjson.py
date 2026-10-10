"""Довідник API з JSON, який видає TypeDoc (`typedoc --json`), — у markdown.

Сайт docs.expo.dev не пише API модулів руками: сторінка ставить `<APISection
packageName="expo-camera" />`, а сайт малює розділ з JSON, згенерованого TypeDoc із
коду пакета (`docs/public/static/data/v57.0.0/expo-camera.json`). У самій сторінці
жодного методу, пропса чи типу немає, тож без цього перетворення корпус знав би про
`expo-camera` лише вступ і приклад.

Що стає текстом: кожна сутність верхнього рівня — підзаголовок `### Назва` з видом
(Component, Hook, Method, Class, Interface, Type, Enum, Constant), описом і тегами
(`@platform`, `@default`, `@deprecated`, `@example`, `@returns`); сигнатури — блоком коду
TypeScript і переліком параметрів; члени класів, інтерфейсів і об'єктних типів —
списком із типом і описом; члени enum — зі значеннями. Приватні члени (`_ім'я`,
`isPrivate`, `isProtected`) і успадковані від зовнішніх пакетів (EventEmitter,
React.Component) не беруться: їх сайт теж не показує.

Формат JSON мінявся разом із TypeDoc: старі файли пишуть опис у `comment.shortText`
і `comment.text`, а теги — у `comment.tags`; нові — у `comment.summary` і
`comment.blockTags`. Тут читаються обидва.
"""

import json

_KIND = {8: "Enum", 32: "Constant", 64: "Method", 128: "Class", 256: "Interface",
         2097152: "Type", 4194304: "Reference", 4: "Namespace", 2: "Module"}
_MEMBER = {1024: "Property", 2048: "Method", 262144: "Property", 512: "Constructor"}
_MAX_TYPE = 400


def _parts(parts) -> str:
    return "".join(p.get("text", "") for p in parts or () if isinstance(p, dict))


def comment(c) -> tuple[str, list]:
    """(опис, [(тег, текст)]) з коментаря будь-якого з двох форматів."""
    if not isinstance(c, dict):
        return "", []
    if "summary" in c or "blockTags" in c:
        text = _parts(c.get("summary"))
        tags = [(t.get("tag", "").lstrip("@"), _parts(t.get("content")))
                for t in c.get("blockTags") or ()]
    else:
        text = "\n\n".join(x for x in (c.get("shortText", ""), c.get("text", "")) if x)
        tags = [(t.get("tag", "").lstrip("@"), t.get("text", "")) for t in c.get("tags") or ()]
    return text.strip(), [(k, v.strip()) for k, v in tags]


def type_text(t, depth: int = 0) -> str:
    out = _type(t, depth)
    return out if len(out) <= _MAX_TYPE else out[:_MAX_TYPE] + "…"


def _type(t, depth: int = 0) -> str:
    if not isinstance(t, dict) or depth > 6:
        return ""
    kind = t.get("type")
    d = depth + 1
    if kind == "intrinsic":
        return t.get("name", "")
    if kind == "reference":
        name = t.get("name") or (t.get("target") or {}).get("qualifiedName", "") \
            if isinstance(t.get("target"), dict) else t.get("name", "")
        args = t.get("typeArguments") or ()
        return f"{name}<{', '.join(_type(a, d) for a in args)}>" if args else str(name)
    if kind == "literal":
        v = t.get("value")
        if isinstance(v, dict) and "value" in v:  # bigint
            return f"{'-' if v.get('negative') else ''}{v['value']}n"
        return json.dumps(v) if isinstance(v, str) else "null" if v is None else str(v).lower() \
            if isinstance(v, bool) else str(v)
    if kind in ("union", "intersection"):
        sep = " | " if kind == "union" else " & "
        return sep.join(_type(x, d) for x in t.get("types") or ())
    if kind == "array":
        inner = _type(t.get("elementType"), d)
        return f"({inner})[]" if " " in inner else f"{inner}[]"
    if kind == "tuple":
        return "[" + ", ".join(_type(x, d) for x in t.get("elements") or ()) + "]"
    if kind == "named-tuple-member":
        return f"{t.get('name', '')}{'?' if t.get('isOptional') else ''}: " \
               f"{_type(t.get('element'), d)}"
    if kind == "optional":
        return _type(t.get("elementType"), d) + "?"
    if kind == "rest":
        return "..." + _type(t.get("elementType"), d)
    if kind == "typeOperator":
        return f"{t.get('operator', '')} {_type(t.get('target'), d)}"
    if kind == "query":
        return f"typeof {_type(t.get('queryType'), d)}"
    if kind == "indexedAccess":
        return f"{_type(t.get('objectType'), d)}[{_type(t.get('indexType'), d)}]"
    if kind == "conditional":
        return (f"{_type(t.get('checkType'), d)} extends {_type(t.get('extendsType'), d)} ? "
                f"{_type(t.get('trueType'), d)} : {_type(t.get('falseType'), d)}")
    if kind == "predicate":
        return f"{t.get('name', '')} is {_type(t.get('targetType'), d)}"
    if kind == "templateLiteral":
        tail = "".join("${" + _type(a, d) + "}" + str(b) for a, b in t.get("tail") or ())
        return f"`{t.get('head', '')}{tail}`"
    if kind == "mapped":
        return (f"{{ [{t.get('parameter', 'K')} in {_type(t.get('parameterType'), d)}]: "
                f"{_type(t.get('templateType'), d)} }}")
    if kind == "reflection":
        decl = t.get("declaration") or {}
        sigs = decl.get("signatures") or ()
        if sigs:
            return " | ".join(_signature_type(s, d) for s in sigs)
        kids = decl.get("children") or ()
        if kids:
            fields = [f"{k.get('name')}{'?' if (k.get('flags') or {}).get('isOptional') else ''}: "
                      f"{_type(k.get('type'), d)}" for k in kids]
            return "{ " + "; ".join(fields) + " }"
        index = decl.get("indexSignatures") or decl.get("indexSignature")
        if index:
            index = index[0] if isinstance(index, list) else index
            p = (index.get("parameters") or [{}])[0]
            return f"{{ [{p.get('name', 'key')}: {_type(p.get('type'), d)}]: " \
                   f"{_type(index.get('type'), d)} }}"
        return "object"
    return t.get("name", "") or kind or ""


def _params(sig, depth: int = 0) -> str:
    out = []
    for p in sig.get("parameters") or ():
        flags = p.get("flags") or {}
        rest = "..." if flags.get("isRest") else ""
        opt = "?" if flags.get("isOptional") or "defaultValue" in p else ""
        out.append(f"{rest}{p.get('name', '')}{opt}: {_type(p.get('type'), depth)}")
    return ", ".join(out)


def _signature_type(sig, depth: int = 0) -> str:
    return f"({_params(sig, depth)}) => {_type(sig.get('type'), depth)}"


def _tags_lines(tags: list) -> list[str]:
    lines = []
    platforms = [v for k, v in tags if k == "platform" and v]
    if platforms:
        lines.append(f"Platforms: {', '.join(platforms)}.")
    for k, v in tags:
        if k == "platform" or not v and k not in ("deprecated", "experimental"):
            continue
        if k == "example":
            lines += ["Example:", "", v if v.lstrip().startswith("```") else f"```ts\n{v}\n```"]
        elif k in ("returns", "return"):
            lines.append(f"Returns: {v}")
        elif k == "default":
            lines.append(f"Default: {v.strip('`') and v}")
        elif k == "deprecated":
            lines.append(f"Deprecated{': ' + v if v else '.'}")
        elif k == "see":
            lines.append(f"See: {v}")
        elif k in ("experimental", "alpha", "beta"):
            lines.append(f"{k.capitalize()}{': ' + v if v else '.'}")
        elif k in ("header", "hidden", "internal", "private", "docsMissing"):
            continue
        else:
            lines.append(f"{k.capitalize()}: {v}")
    return lines


def _skip(node) -> bool:
    flags = node.get("flags") or {}
    name = str(node.get("name", ""))
    if name.startswith("_") or flags.get("isPrivate") or flags.get("isProtected"):
        return True
    if flags.get("isExternal"):
        return True
    _, tags = comment(node.get("comment"))
    if any(k in ("hidden", "private", "internal") for k, _v in tags):
        return True
    return False


def _inherited_external(node) -> bool:
    """Член, успадкований від зовнішнього пакета: EventEmitter, React.Component, NativeModule."""
    src = node.get("inheritedFrom")
    if not isinstance(src, dict):
        return False
    target = src.get("target")
    return isinstance(target, dict) or (isinstance(target, int) and target < 0)


def _signature_block(name: str, sig) -> list[str]:
    lines = ["```ts", f"{name}({_params(sig)}): {type_text(sig.get('type'))}", "```", ""]
    text, tags = comment(sig.get("comment"))
    if text:
        lines += [text, ""]
    params = []
    for p in sig.get("parameters") or ():
        ptext, ptags = comment(p.get("comment"))
        flags = p.get("flags") or {}
        bits = [f"`{type_text(p.get('type'))}`"]
        if flags.get("isOptional") or "defaultValue" in p:
            bits.append("optional")
        if p.get("defaultValue") not in (None, "..."):
            bits.append(f"default: `{p['defaultValue']}`")
        line = f"- `{p.get('name', '')}` ({', '.join(bits)})"
        params.append(line + (f" — {' '.join(ptext.split())}" if ptext else ""))
    if params:
        lines += ["Parameters:", ""] + params + [""]
    lines += _tags_lines(tags)
    return lines


def _member_lines(member, depth: int = 0) -> list[str]:
    name = member.get("name", "")
    flags = member.get("flags") or {}
    text, tags = comment(member.get("comment"))
    sigs = member.get("signatures") or ()
    if not sigs and member.get("getSignature"):
        sigs = ()
        member = dict(member, type=(member.get("getSignature") or {}).get("type"))
    pad = "  " * depth
    if sigs:
        sig = sigs[0]
        stext, stags = comment(sig.get("comment"))
        text, tags = text or stext, tags or stags
        head = f"{pad}- `{name}({_params(sig)})`: `{type_text(sig.get('type'))}`"
    else:
        opt = "?" if flags.get("isOptional") else ""
        head = f"{pad}- `{name}{opt}`: `{type_text(member.get('type'))}`"
        if member.get("defaultValue") not in (None, "...", ""):
            head += f" = `{member['defaultValue']}`"
    tail = [" ".join(x.split()) for x in _tags_lines(tags) if not x.startswith(("Example", "```"))]
    desc = " ".join(text.split())
    return [head + (f" — {desc}" if desc else "") + (f" ({' '.join(tail)})" if tail else "")]


def _members(node, depth: int = 0) -> list[str]:
    out = []
    for m in node.get("children") or ():
        if _skip(m) or _inherited_external(m):
            continue
        out += _member_lines(m, depth)
    return out


def _object_members(t) -> list:
    """Члени об'єктного типу: `{…}` або перетин `ViewProps & {…}` — лише власні поля."""
    if not isinstance(t, dict):
        return []
    if t.get("type") == "reflection":
        return list((t.get("declaration") or {}).get("children") or ())
    if t.get("type") == "intersection":
        out = []
        for x in t.get("types") or ():
            out += _object_members(x)
        return out
    return []


def _kind_label(node) -> str:
    kind = node.get("kind")
    name = str(node.get("name", ""))
    if kind == 32 and name.startswith("use"):
        return "Hook"
    if kind == 64 and name.startswith("use"):
        return "Hook"
    if kind == 128 and any(
            "Component" in str((e or {}).get("name", "")) for e in node.get("extendedTypes") or ()):
        return "Component"
    return _KIND.get(kind, "")


def entity(node) -> list[str]:
    """Сутність верхнього рівня → рядки markdown."""
    name = node.get("name", "")
    kind = node.get("kind")
    label = _kind_label(node)
    lines = [f"### {name}", ""]
    text, tags = comment(node.get("comment"))
    sigs = list(node.get("signatures") or ())
    if kind == 32 and not sigs:
        decl = (node.get("type") or {}).get("declaration") or {}
        sigs = list(decl.get("signatures") or ())
    if label:
        lines += [f"Type: {label}.", ""]
    if text:
        lines += [text, ""]
    lines += _tags_lines(tags)
    if lines[-1:] != [""]:
        lines.append("")
    if sigs:
        for sig in sigs:
            lines += _signature_block(name, sig) + [""]
    elif kind == 8:
        members = []
        for m in node.get("children") or ():
            mtext, _ = comment(m.get("comment"))
            value = type_text(m.get("type")) or str(m.get("defaultValue", ""))
            members.append(f"- `{m.get('name', '')}`" + (f" = `{value}`" if value else "")
                           + (f" — {' '.join(mtext.split())}" if mtext else ""))
        lines += ["Members:", ""] + members + [""]
    elif kind in (128, 256):
        ctor = [c for c in node.get("children") or () if c.get("kind") == 512]
        members = _members(node)
        if node.get("extendedTypes"):
            lines += ["Extends: " + ", ".join(f"`{type_text(e)}`" for e in node["extendedTypes"]),
                      ""]
        if members:
            lines += ["Members:", ""] + members + [""]
        del ctor
    elif kind == 2097152:
        kids = [k for k in _object_members(node.get("type")) if not _skip(k)]
        others = [x for x in ((node.get("type") or {}).get("types") or ())
                  if x.get("type") != "reflection"] if (node.get("type") or {}).get(
            "type") == "intersection" else []
        if kids:
            if others:
                lines += ["Extends: " + ", ".join(f"`{type_text(o)}`" for o in others), ""]
            lines += ["Properties:", ""]
            for k in kids:
                lines += _member_lines(k)
            lines.append("")
        else:
            lines += ["```ts", f"type {name} = {type_text(node.get('type'))}", "```", ""]
    elif kind == 32:
        lines += ["```ts", f"const {name}: {type_text(node.get('type'))}", "```", ""]
    return lines


def render(data: dict, api_name: str = "") -> str:
    """Увесь JSON пакета → markdown розділу API. Порожній рядок — нема чого показати."""
    if not isinstance(data, dict):
        return ""
    nodes = list(data.get("children") or ())
    # Пакет із підмодулями (`expo-sqlite` з `next`): діти модуля — ті самі сутності.
    flat = []
    for n in nodes:
        if n.get("kind") in (2, 4) and n.get("children"):
            flat += n["children"]
        else:
            flat.append(n)
    out: list[str] = []
    for n in flat:
        if _skip(n) or n.get("kind") == 4194304:
            continue
        out += entity(n)
    return "\n".join(out).strip()
