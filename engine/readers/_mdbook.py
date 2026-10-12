"""Сторінка книжки mdBook із репозиторію → markdown, яким її бачить читач сайту.

Foundry Book до травня 2025 збирався mdBook із теки `src/`, і частина тексту сторінки лежить в інших
файлах:
- `{{#include common-options.md}}` — спільний шматок довідника CLI (опції, однакові для десятків команд);
- `{{#include ../../projects/writing_tests/test/Basic.t.sol:all}}` — код прикладу, з `:назва` — лише область
  між рядками `ANCHOR: назва` і `ANCHOR_END: назва`;
- `{{#include ../output/hello_foundry/forge-test:all}}` — записаний вивід команди.

mdBook розкриває вставки до розбору markdown, тож вони стоять і в тексті, і всередині блоків коду. Номери рядків
теж бувають: `:2` — лише другий рядок, `:2:10` — з другого по десятий, `::10` — до десятого, `:2:` — від другого.
Рядки з позначками `ANCHOR`/`ANCHOR_END` у вставленому тексті mdBook прибирає завжди.

Без цього сторінка команди мала б замість опцій рядок `{{#include …}}`, а посібник — порожні блоки коду. Шматок
опцій міняється частіше за сторінку, що його вставляє, тож редакція сторінки рахується разом із її вставками.

`files` — {шлях: sha} файлів тегу, які сторінка може взяти (див. `wanted`), `fetch(шлях, sha)` — вміст файла.
Вставка, файла якої на тезі немає, просто зникає.
"""

import hashlib
import posixpath
import re

_INCLUDE = re.compile(r"(?<!\\)\{\{#include\s+([^}\s:]+)(?::([^}]*?))?\s*\}\}")
_ANCHOR = re.compile(r"\b(?:ANCHOR|ANCHOR_END):\s*[\w-]+")
_LINES = re.compile(r"^(\d*)(?::(\d*))?$")
# Записаний вивід команд може нести кольори терміналу — керівні послідовності, а не текст.
_ANSI = re.compile(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)|\x1b\[[0-9;?]*[A-Za-z]")
_DEPTH = 10


def wanted() -> list:
    """Файли тегу, які сторінки можуть узяти: шматки книжки, проєкти прикладів і записаний вивід."""
    return [re.compile(r"^(?:src|projects)/(?!.*\.(?:png|jpe?g|gif|svg|ico|webp|woff2?)$).+")]


def _resolve(target: str, page: str) -> str:
    return posixpath.normpath(posixpath.join(posixpath.dirname(page), target))


def _deps(text: str, path: str, files: dict, read, depth: int = 0) -> list[str]:
    """Шляхи файлів, які сторінка тягне вставками, разом із вкладеними."""
    out: list = []
    if depth >= _DEPTH:
        return out
    for m in _INCLUDE.finditer(text):
        where = _resolve(m.group(1), path)
        if where in files and where not in out:
            out.append(where)
            if where.endswith(".md"):
                out += [p for p in _deps(read(where), where, files, read, depth + 1) if p not in out]
    return out


def revision(path: str, sha: str, files: dict, fetch) -> str:
    """Відбиток редакції сторінки разом із тим, що вона вставляє: незмінна сторінка з
    оновленим шматком опцій — уже інша редакція для читача."""
    def read(where):
        return fetch(where, files[where])

    deps = _deps(read(path), path, files, read)
    if not deps:
        return sha
    near = sorted(f"{p}:{files[p]}" for p in deps)
    return hashlib.sha1("\n".join([sha] + near).encode()).hexdigest()


def _part(text: str, spec: str | None) -> str:
    """Частина вставки за назвою області або номерами рядків; без уточнення — весь файл."""
    lines = text.split("\n")
    if text.endswith("\n"):
        lines = lines[:-1]
    if spec:
        spec = spec.strip()
        m = _LINES.match(spec)
        if m and (m.group(1) or m.group(2)):
            first = int(m.group(1)) if m.group(1) else 1
            if m.group(2) is None:
                lines = lines[first - 1:first]
            else:
                last = int(m.group(2)) if m.group(2) else len(lines)
                lines = lines[first - 1:last]
        else:
            start = re.compile(rf"\bANCHOR:\s*{re.escape(spec)}\b")
            end = re.compile(rf"\bANCHOR_END:\s*{re.escape(spec)}\b")
            inside, picked = False, []
            for line in lines:
                if not inside and start.search(line):
                    inside = True
                elif inside and end.search(line):
                    break
                elif inside:
                    picked.append(line)
            lines = picked
    return "\n".join(line for line in lines if not _ANCHOR.search(line))


def expand(text: str, path: str, files: dict, fetch, depth: int = 0) -> str:
    """Текст сторінки з розкритими вставками; рядок `\\{{#include}}` mdBook показує як є."""
    def sub(m):
        where = _resolve(m.group(1), path)
        if where not in files or depth >= _DEPTH:
            return ""
        body = _ANSI.sub("", fetch(where, files[where]))
        if where.endswith(".md"):
            body = expand(body, where, files, fetch, depth + 1)
        return _part(body, m.group(2))

    return _INCLUDE.sub(sub, text).replace("\\{{#include", "{{#include")
