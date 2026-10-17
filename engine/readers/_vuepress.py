"""Розмітка сайту VuePress 1 → текст (поле `vuepress` читача `ghdocs-history`).

Сайт ajv.js.org зібрано VuePress із теки `docs/` репозиторію ajv, і в сторінках три вставки,
яких markdown не знає:

- контейнери `::: warning Use single Ajv instance` … `:::` — сорок попереджень, і саме в них
  сказано, чого не робити (ReDoS, `removeAdditional` з `anyOf`, несумісність draft-2020-12).
  Загальний розбір виносок Docusaurus їх не бере: там після `:::` пробілу немає;
- `<code-group>` з `<code-block title="JavaScript">` — той самий приклад для JSON Schema і JTD,
  JavaScript і TypeScript. Без підпису два блоки коду стояли б поспіль без пояснення;
- `<Badge text="JTD only" />` у заголовку опції — до чого опція стосується. Позначка стає окремим
  рядком під заголовком, а не частиною його: у 8.x до «unevaluatedProperties» дописали «NEW: draft
  2019-09», і в заголовку вона дала б розділу інший ключ, ніж у 7.x, — та сама сторінка двох ліній
  не злилася б в один уривок;
- `[[toc]]` — місце змісту сторінки, тексту не несе.

Код між огорожами не чіпається. Огорожа з відступом (приклад усередині пункту списку) закінчується
разом із пунктом: markdown-it закриває її сам, щойно рядок тексту стоїть лівіше за огорожу. У
docs/json-schema.md (опис `items`) після прикладу лишився зайвий рядок «```»; без такого закриття
решта сторінки — заголовки `prefixItems`, `additionalItems`, попередження — читалася б кодом, а
код — текстом.
"""

import re

_FENCE = re.compile(r"^\s*(```|~~~)")
_CONTAINER = re.compile(r"^\s*:::\s*(tip|warning|danger|details|note|info)\b[ \t]*(.*?)\s*$")
_CONTAINER_END = re.compile(r"^\s*:::\s*$")
_CODE_BLOCK = re.compile(r'^\s*<code-block\b[^>]*?\btitle="([^"]*)"[^>]*>\s*$')
_CODE_TAG = re.compile(r"^\s*</?code-(?:group|block)\b[^>]*>\s*$")
_BADGE = re.compile(r'\s*<Badge\b[^>]*?\btext="([^"]*)"[^>]*/>')
_TOC = re.compile(r"^\s*\[\[toc\]\]\s*$")


def expand(text: str) -> str:
    out: list[str] = []
    fence, indent = False, 0
    for line in text.split("\n"):
        width = len(line) - len(line.lstrip())
        if fence and indent and line.strip() and width < indent and not _FENCE.match(line):
            out.append(" " * indent + "```")
            fence = False
        if _FENCE.match(line):
            fence = not fence
            indent = width
            out.append(line)
            continue
        if fence:
            out.append(line)
            continue
        if m := _CONTAINER.match(line):
            label = m.group(1).capitalize()
            out += ["", f"{label}: {m.group(2)}" if m.group(2) else f"{label}:", ""]
        elif (_CONTAINER_END.match(line) or _TOC.match(line)
              or _CODE_TAG.match(line) and not _CODE_BLOCK.match(line)):
            out.append("")
        elif m := _CODE_BLOCK.match(line):
            out += ["", f"{m.group(1)}:", ""]
        elif line.lstrip().startswith("#") and (badges := _BADGE.findall(line)):
            out += [_BADGE.sub("", line).rstrip(), "", "(" + ", ".join(badges) + ")"]
        else:
            out.append(_BADGE.sub(lambda b: f" ({b.group(1)})", line))
    return "\n".join(out)
