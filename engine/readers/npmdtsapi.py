"""Читач довідника API пакета npm з файлів типів тарбола: символ публічного API — документ.

`npm-dts-api` — `url` — опис пакета в реєстрі (https://registry.npmjs.org/@angular/material), `versions`
                — об'єкт «версія npm → мітка версії документа» від найновішої. `scope` — ім'я пакета в
                назвах і точках входу (`@angular/material`); `name_prefix` — початок імені документа
                («material-api»).

Навіщо. Довідник API Angular Material і CDK 6.0–6.3 ніде не лежить готовим: сайт material.angular.io
тих ліній збирався з репозиторію `material2-docs-content`, а стабільних знімків 6.0–6.3 там немає (є
лише бети 6.0.0-beta). Те саме, з чого генерувалися сторінки, є в пакеті npm кожної версії: файли
типів `.d.ts` з коментарями JSDoc і `index.metadata.json` з декораторами (селектор, `exportAs`, входи
й виходи). Це і є сторінка довідника: що за символ, де його імпортувати, опис, оголошення з членами і
опис кожного члена.

Перелік символів — те, що справді експортує точка входу пакета: `<точка>/index.d.ts` →
`typings/index.d.ts` → `public-api.d.ts` → `export * from './…'` і `export { A as B } from './…'` до
самих оголошень. Корінь пакета (`@angular/material` у 6.x — збірка з усіх точок входу) окремо не
береться: кожен символ і так є у своїй точці входу. Імена з `ɵ` чи `_` і символи з позначкою
`@docs-private` — службові й не беруться, як не показував їх і сайт; так само в оголошенні класу
пропускаються члени `private` і з `_`.

Документ — неповторний текст символу точки входу; у його версії лягають усі версії, де текст був
саме таким. Ім'я — «<name_prefix>-<точка входу>-<символ>-<хеш>», як у `ng-api-history`: `revision_suffix`
зрізає хеш, і редакції одного символу 6.0–6.3 зливаються.

Чому окремий читач, а не поле `ng-api-history`: там перелік символів — золоті файли репозиторію на
тегах, а для Material 6.x таких немає; тарбол тут — і перелік, і опис.
"""

import hashlib
import io
import json
import posixpath
import re
import tarfile
import zlib

from engine.readers import Item, _markup, register
from engine.readers.ngapi import _body_of, _jsdoc, _source_docs

_STAR = re.compile(r"""^export \* from ['"]([^'"]+)['"];?""", re.M)
_NAMED = re.compile(r"""^export \{([^}]*)\} from ['"]([^'"]+)['"];?""", re.M)
_LOCAL = re.compile(r"^export\s+(?:declare\s+)?(?:abstract\s+)?(class|interface|function|const|let|var|type|enum)"
                    r"\s+([\w$]+)", re.M)
_COMMENT = re.compile(r"/\*.*?\*/|^\s*//[^\n]*\n", re.S | re.M)
# Службовий член класу — рядок на відступі члена (чотири пробіли); глибші рядки — продовження
# сигнатури (параметри конструктора), їх не чіпаємо.
_PRIVATE = re.compile(r"^ {4}(?:private\s|protected\s|(?:readonly\s+|static\s+)*_)")


def _resolve(files: dict, path: str, seen=None) -> dict:
    """{ім'я, що експортує файл: (файл оголошення, ім'я там)} — з `export *` і `export { … }`."""
    seen = seen if seen is not None else set()
    if path in seen or path not in files:
        return {}
    seen.add(path)
    text, out = files[path], {}

    def target(spec):
        base = posixpath.normpath(posixpath.join(posixpath.dirname(path), spec))
        for cand in (base + ".d.ts", base + "/index.d.ts"):
            if cand in files:
                return cand
        return ""
    for m in _LOCAL.finditer(text):
        out.setdefault(m.group(2), (path, m.group(2)))
    for m in _NAMED.finditer(text):
        t = target(m.group(2))
        names = _resolve(files, t, seen) if t else {}
        for part in m.group(1).split(","):
            bits = part.strip().split(" as ")
            if bits[0].strip() and bits[0].strip() in names:
                out.setdefault(bits[-1].strip(), names[bits[0].strip()])
    for m in _STAR.finditer(text):
        t = target(m.group(1))
        for k, v in (_resolve(files, t, seen) if t else {}).items():
            out.setdefault(k, v)
    return out


def _declaration(text: str, name: str) -> tuple[str, str]:
    """(вид, оголошення без коментарів і службових членів) символу у файлі типів."""
    m = re.search(rf"^export\s+(?:declare\s+)?(?:abstract\s+)?(class|interface|function|const|let|var|type|enum)"
                  rf"\s+{re.escape(name)}\b", text, re.M)
    if not m:
        return "", ""
    kind = m.group(1)
    if kind in ("class", "interface", "enum"):
        body = _body_of(text, m.end())
        head = text[m.start():text.find("{", m.end())].strip()
        rows = [ln for ln in _COMMENT.sub("", body).split("\n") if ln.strip() and not _PRIVATE.match(ln)]
        code = head + " {\n" + "\n".join(rows) + "\n}"
    else:
        end = text.find(";", m.end())
        code = text[m.start():end + 1 if end > 0 else len(text)]
        code = _COMMENT.sub("", code)
    return kind, re.sub(r"\n{2,}", "\n", code).strip()


def _meta_line(meta: dict) -> list[str]:
    """Рядки про декоратор з `index.metadata.json`: вид, селектор, `exportAs`, входи й виходи."""
    out = []
    for dec in meta.get("decorators") or ():
        if not isinstance(dec, dict) or not isinstance(dec.get("expression"), dict):
            continue
        name = dec["expression"].get("name", "")
        if name not in ("Component", "Directive", "NgModule", "Injectable", "Pipe"):
            continue
        args = (dec.get("arguments") or [{}])[0]
        args = args if isinstance(args, dict) else {}
        out.append(f"Angular kind: {name.lower()}")
        if isinstance(args.get("selector"), str):
            out.append(f"Selector: `{' '.join(args['selector'].split())}`")
        if isinstance(args.get("exportAs"), str):
            out.append(f"Exported as: `{args['exportAs']}`")
        if isinstance(args.get("name"), str) and name == "Pipe":
            out.append(f"Pipe name: `{args['name']}`")
        ins = [x for x in args.get("inputs") or () if isinstance(x, str)]
        outs = [x for x in args.get("outputs") or () if isinstance(x, str)]
        members = meta.get("members") if isinstance(meta.get("members"), dict) else {}
        for member, decls in members.items():
            for d in decls if isinstance(decls, list) else ():
                for md in (d.get("decorators") or ()) if isinstance(d, dict) else ():
                    n = (md.get("expression") or {}).get("name") if isinstance(md, dict) else None
                    if n == "Input":
                        ins.append(member)
                    elif n == "Output":
                        outs.append(member)
        if ins:
            out.append("Inputs: " + ", ".join(f"`{x}`" for x in dict.fromkeys(ins)))
        if outs:
            out.append("Outputs: " + ", ".join(f"`{x}`" for x in dict.fromkeys(outs)))
        break
    return out


@register("npm-dts-api")
def npm_dts_api(source: dict, ctx) -> list[Item]:
    versions = source.get("versions")
    if not isinstance(versions, dict) or not versions:
        raise SystemExit(f"{source['id']}: читач npm-dts-api потребує поля versions.")
    scope = str(source.get("scope") or source["url"].split("registry.npmjs.org/", 1)[-1])
    lead = _markup.slug(source.get("name_prefix") or scope)
    meta_all = json.loads(ctx.text(source["url"], gzip=True))
    found: dict = {}
    texts: dict = {}
    for version, label in versions.items():
        url = (((meta_all.get("versions") or {}).get(version) or {}).get("dist") or {}).get("tarball", "")
        if not url or not ctx.allowed(url):
            print(f"  {source['id']}: тарбола {version} немає чи він поза білим списком", flush=True)
            continue
        files, metas = {}, {}
        with tarfile.open(fileobj=io.BytesIO(ctx.bytes(url)), mode="r:*") as tar:
            for m in tar:
                if not m.isfile():
                    continue
                path = m.name.split("/", 1)[-1]
                if path.endswith(".d.ts"):
                    files[path] = tar.extractfile(m).read().decode("utf-8", errors="replace")
                elif path.endswith("index.metadata.json"):
                    try:
                        data = json.loads(tar.extractfile(m).read())
                    except ValueError:
                        continue
                    for block in data if isinstance(data, list) else [data]:
                        metas.setdefault(posixpath.dirname(path).split("/typings")[0], {}).update(
                            (block or {}).get("metadata") or {})
        entries = sorted(p.rsplit("/", 1)[0] for p in files
                         if p.endswith("/index.d.ts") and "/typings/" not in p and p.count("/") <= 2
                         and not p.startswith(("schematics/", "esm", "bundles/")))
        for entry in entries:
            names = _resolve(files, f"{entry}/index.d.ts")
            docs_cache: dict = {}
            for name, (where, orig) in sorted(names.items()):
                if name.startswith(("ɵ", "_")):
                    continue
                if where not in docs_cache:
                    docs_cache[where] = _source_docs(files[where])
                decl_docs = docs_cache[where].get(orig, [])
                if any("@docs-private" in d for _, d, _ in decl_docs):
                    continue
                kind, code = _declaration(files[where], orig)
                if not code:
                    continue
                full = f"{scope}/{entry}"
                parts = [f"Entry point: `{full}`", f"Kind: {kind}"]
                meta = metas.get(entry, {}).get(orig)
                parts += _meta_line(meta if isinstance(meta, dict) else {})
                body = ["  \n".join(parts)]
                for _, doc, _ in decl_docs:
                    rendered = _jsdoc(doc)
                    if rendered and rendered not in body:
                        body.append(rendered)
                body.append(f"```ts\n{code}\n```")
                members = {}
                for _, _, mem in decl_docs:
                    for k, v in mem.items():
                        members.setdefault(k, v)
                for member, doc in members.items():
                    if member.startswith("_") or not re.search(rf"\b{re.escape(member)}\b", code):
                        continue
                    text = _jsdoc(doc)
                    if text:
                        body.append(f"## {member}\n\n{text}")
                text = "\n\n".join(body)
                digest = hashlib.sha1(f"{full}\n{name}\n{text}".encode()).hexdigest()
                found.setdefault((entry, name, kind), {}).setdefault(digest, []).append(str(label))
                if digest not in texts:
                    texts[digest] = (zlib.compress(text.encode(), 6), url)
    if not found:
        raise SystemExit(f"{source['id']}: у жодному тарболі не знайдено точок входу з типами.")
    items = []
    for (entry, name, kind), revs in found.items():
        tail = _markup.slug(name) + (f"-{kind}" if name[:1].islower() else "")
        for digest, labels in revs.items():
            doc = f"{lead}-{_markup.slug(entry)}-{tail}-{digest[:8]}"

            def make(digest=digest, labels=labels, entry=entry, name=name):
                blob, url = texts[digest]
                return _markup.document(f"{name} ({scope}/{entry})", url, ctx.stamp,
                                        zlib.decompress(blob).decode(), ", ".join(dict.fromkeys(labels)))

            items.append(Item(id=f"{source['id']}/{doc}", file=f"{source['id']}--{doc}.txt", make=make))
    return items
