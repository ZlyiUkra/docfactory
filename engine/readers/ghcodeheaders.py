"""Читач історії заголовкових файлів C: як `ghcode-history`, але розділ — кожна група оголошень зі своїм коментарем.

`ghcode-history-ch` — файли `.h` з багатьох тегів одного репозиторію разом. Поля ті самі, що в `ghcode-history`:
                      `url` — префікс дерев через API (…/repos/ВЛАСНИК/РЕПО/git/trees/), `tags` — об'єкт
                      «тег → версія» від найновішого, `include` — вирази шляхів, що беруться; необов'язкові
                      `exclude`, `name_prefix` і `max_file` — межа розміру файла в байтах (типово 300 000).
                      Поля `outline` немає: заголовок ділиться на розділи завжди.

Навіщо. Довідник C API бібліотеки MuPDF — це її заголовкові файли: сторінки документації описують лише частину
функцій, а опис кожної стоїть коментарем над її оголошенням у `include/mupdf/fitz/*.h` і `include/mupdf/pdf/*.h`.
`ghcode-history` з `outline: true` ділить заголовок лише за коментарями Doxygen «/** … */» (так написано ICU).
У MuPDF так оформлено тільки частину файлів нових версій: `pdf/annot.h` і `pdf/object.h`, як і всі заголовки до
1.17, мають звичайні коментарі «/* … */» — і кожен такий файл на 20–35 тисяч символів лишався одним розділом без
жодної назви функції. Тип-функція (`typedef void (fz_document_drop_fn)(…)`) діставала там назву «void()».

Розділи. Заголовок читається як перелік груп, розділених порожнім рядком поза оголошеннями. Група — це коментар
(«/** … */» чи «/* … */» з першої колонки), якщо він є, і оголошення під ним: прототипи функцій, типи, структури,
переліки, макроси. Група з коментарем — завжди окремий розділ. Група без коментаря коротша за 200 символів
приклеюється до попереднього розділу, довша — стає окремим. Назва розділу — імена того, що група оголошує: до
трьох імен через кому, далі «…»; функція — з дужками («fz_open_document()»), тип-функція, тип і макрос — саме
ім'я, структура чи перелік з іменем — «struct fz_document». Тому функцію без власного коментаря теж видно: або
в назві розділу, або в коді під коментарем, що описує її разом із сусідніми («Get/set the annotation flags» над
`pdf_annot_flags` і `pdf_set_annot_flags`).

Текст розділу. Коментар групи лягає звичайним текстом, без «/*» і відступу, — це й є опис функції; оголошення
під ним — блоком коду. Коментарі всередині структур і між рядками оголошень лишаються в коді. Рядки ліцензії
«// Copyright …» на початку файла знімаються: вони однакові в усіх файлах усіх версій.

Далі все як у `ghcode-history`: документ — неповторна пара «шлях, вміст» (хеш blob із дерева), у версії лягають
усі теги, де файл лежав саме таким; адреса в шапці — blob на найновішому з них.
"""

import json
import re
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register

_MAX_FILE = 300_000
_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
# Розділ без коментаря, коротший за це, приклеюється до попереднього (той самий поріг, що й у фрагментів).
_MIN_PART = 200
_MAX_NAMES = 3

_COMMENTS = re.compile(r"/\*.*?\*/|//[^\n]*", re.S)
_DEFINE = re.compile(r"#\s*define\s+([A-Za-z_]\w*)(\()?")
_FN_TYPE = re.compile(r"\(\s*\*?\s*([A-Za-z_]\w*)\s*\)\s*\(")
_LAST = re.compile(r"([A-Za-z_]\w*)\s*(?:\[[^\]]*\]\s*)*(?:=[^;]*)?;\s*$")
_TAGGED = re.compile(r"(struct|union|enum)\s+([A-Za-z_]\w*)\s*(?:\{|;|$)")
_CALL = re.compile(r"([A-Za-z_]\w*)\s*\(")
# Слова перед дужкою, що іменем функції не бувають: позначки компілятора й макроси-атрибути MuPDF.
_NOT_NAME = re.compile(r"^(?:__\w+|FZ_[A-Z_]+|if|while|for|switch|sizeof|return|defined|struct|union|enum)$")


def _name(decl: str) -> str:
    """Що оголошує оголошення: «fz_open_document()», «fz_document_drop_fn», «struct fz_page», «FZ_VERSION»."""
    text = " ".join(_COMMENTS.sub(" ", decl).split())
    if m := _DEFINE.match(text):
        # Макрос-запобіжник від повторного включення (`MUPDF_FITZ_DOCUMENT_H`) нічого не оголошує.
        return "" if m[1].endswith("_H") and not m[2] else m[1] + ("()" if m[2] else "")
    if not text or text.startswith("#"):
        return ""
    if text.startswith("typedef"):
        head = text.split("{", 1)[0]
        if "{" not in text and (m := _FN_TYPE.search(text)):
            return m[1]
        # Ім'я типу стоїть після тіла структури чи переліку: «typedef enum { … } fz_permission;».
        if m := _LAST.search(re.sub(r"\{.*\}", "{}", text)):
            return m[1]
        return (m[2] if (m := _TAGGED.search(head)) else "")
    if (m := _TAGGED.match(text)) and "(" not in text.split("{", 1)[0]:
        return f"{m[1]} {m[2]}"
    if m := re.match(r"enum\s*\{\s*([A-Za-z_]\w*)", text):
        return f"enum {m[1]}"
    for m in _CALL.finditer(text.split("{", 1)[0]):
        if not _NOT_NAME.match(m[1]):
            return m[1] + "()"
    if m := _LAST.search(text):
        return m[1]
    return ""


def _prose(comment: list[str]) -> str:
    """Коментар групи звичайним текстом: без «/*», «*/», зірочок на початку рядків і спільного відступу."""
    text = "\n".join(comment).strip()
    text = re.sub(r"^/\*+!?<?", "", text)
    text = re.sub(r"\*+/$", "", text)
    lines = [re.sub(r"^\s*\*(?:\s|$)", "", ln.replace("\t", "    ")).rstrip() for ln in text.split("\n")]
    cut = min((len(ln) - len(ln.lstrip()) for ln in lines if ln.strip()), default=0)
    lines = [ln[cut:] if ln.strip() else "" for ln in lines]
    # «#» чи «=» на початку рядка markdown прочитав би як заголовок, тому такий рядок екранується.
    lines = ["\\" + ln if re.match(r"#|={3,}|-{3,}", ln) else ln for ln in lines]
    return "\n".join(lines).strip()


def _groups(text: str) -> list[dict]:
    """Заголовок як перелік груп: `comment` — рядки коментаря над групою, `code` — рядки оголошень, `names`."""
    lines = text.replace("\r\n", "\n").rstrip().split("\n")
    i = 0
    # Ліцензія рядками «//» на початку файла — та сама в усіх файлах.
    while i < len(lines) and (lines[i].startswith("//") or not lines[i].strip()):
        i += 1
    groups: list[dict] = []
    cur = {"comment": [], "code": [], "names": []}

    def close():
        nonlocal cur
        if cur["comment"] or any(x.strip() for x in cur["code"]):
            groups.append(cur)
        cur = {"comment": [], "code": [], "names": []}

    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            close()
            i += 1
            continue
        if line.startswith("/*"):
            j = i
            while j < n and "*/" not in lines[j][2 if j == i else 0:]:
                j += 1
            block = lines[i:j + 1]
            # Коментар посеред групи (другий опис без порожнього рядка) починає нову групу.
            if cur["code"] or cur["comment"]:
                close()
            cur["comment"] = block
            i = j + 1
            continue
        if line.lstrip().startswith("#"):
            j = i
            while j < n - 1 and lines[j].rstrip().endswith("\\"):
                j += 1
            block = lines[i:j + 1]
            if name := _name(" ".join(x.rstrip("\\") for x in block)):
                cur["names"].append(name)
            cur["code"] += block
            i = j + 1
            continue
        if re.match(r'extern\s+"C"|\}\s*$', line):
            cur["code"].append(line)
            i += 1
            continue
        # Оголошення: до «;» на нульовій глибині дужок, а тіло вбудованої функції — до її «}».
        j, depth, opened = i, 0, False
        needs_semicolon = bool(re.match(r"(?:typedef|struct|union|enum)\b", line))
        while j < n:
            code = _COMMENTS.sub(" ", lines[j])
            depth += code.count("{") - code.count("}")
            opened = opened or "{" in code
            stripped = code.rstrip()
            if depth <= 0 and (stripped.endswith(";") or (opened and not needs_semicolon and stripped.endswith("}"))):
                break
            # Порожній рядок поза дужками — оголошення без «;» (макрос-обгортка): далі вже інша група.
            if depth <= 0 and not opened and j + 1 < n and not lines[j + 1].strip():
                break
            j += 1
        block = lines[i:j + 1]
        if name := _name("\n".join(block)):
            cur["names"].append(name)
        cur["code"] += block
        i = j + 1
    close()
    return groups


def _outline(text: str) -> str:
    """Тіло документа: розділ на групу оголошень — назва, опис із коментаря, код."""
    parts: list = []          # [імена, опис, код]
    pending: list[str] = []   # коментар без оголошень під ним — переходить до наступної групи
    for g in _groups(text):
        comment, code, names = g["comment"], "\n".join(g["code"]).strip("\n"), g["names"]
        if not code.strip():
            pending += comment + [""]
            continue
        comment, pending = pending + comment, []
        if not names or (not comment and parts and len(code) < _MIN_PART):
            if parts:
                parts[-1][0] += names
                parts[-1][2] += "\n\n" + ("\n".join(comment) + "\n" if comment else "") + code
            else:
                parts.append([names, "", ("\n".join(comment) + "\n" if comment else "") + code])
            continue
        parts.append([list(names), _prose(comment) if comment else "", code])
    out, used = [], {}
    for names, prose, code in parts:
        names = list(dict.fromkeys(names))
        heading = ", ".join(names[:_MAX_NAMES]) + (" …" if len(names) > _MAX_NAMES else "")
        if heading:
            used[heading] = used.get(heading, 0) + 1
            if used[heading] > 1:
                heading = f"{heading} ({used[heading]})"
        chunk = [f"## {heading}"] if heading else []
        if prose:
            chunk.append(prose)
        chunk.append(f"```c\n{code}\n```")
        out.append("\n\n".join(chunk))
    return "\n\n".join(out)


@register("ghcode-history-ch")
def ghcode_history_ch(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев /repos/ВЛАСНИК/РЕПО/git/trees/.")
    owner, repo = m.groups()
    tags = source.get("tags")
    if not isinstance(tags, dict) or not tags:
        raise SystemExit(f"{source['id']}: поле `tags` — об'єкт «тег → версія».")
    include = [re.compile(x) for x in source.get("include") or ()]
    if not include:
        raise SystemExit(f"{source['id']}: поле `include` — вирази шляхів, що беруться.")
    exclude = [re.compile(x) for x in source.get("exclude") or ()]
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""
    limit = int(source.get("max_file") or _MAX_FILE)

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
            if (entry.get("type") == "blob" and 0 < entry.get("size", 1) <= limit
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
            body = _outline(text)
            title = f"{repo}: {path}"
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодного файла за `include` на жодному з {len(tags)} тегів.")
    return items
