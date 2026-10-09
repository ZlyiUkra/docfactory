"""Читач історії файла типів DefinitelyTyped: один документ на кожен текст, що виходив у npm.

`dt-history` — `url` — перелік комітів файла через API
               (https://api.github.com/repos/DefinitelyTyped/DefinitelyTyped/commits?path=
               types/ПАКЕТ/index.d.ts&per_page=100; сторінки гортаються параметром page),
               `versions` — опис пакета @types/ПАКЕТ у реєстрі npm, `label` — назва документа.
               Необов'язкове `skip_versions` — вираз версій, що не беруться (напр. заглушка, яку
               DefinitelyTyped публікує, коли пакет почав нести власні типи).

Навіщо. Типи бібліотеки, що не пише їх сама (react-window 1.x), живуть у DefinitelyTyped, і
коментарі до кожної властивості там — така сама документація, як сторінка сайту: що TypeScript
дозволить передати, які параметри має `children`, що повертає `scrollToItem`. Тегів версій у
DefinitelyTyped немає, а реєстр npm для пакетів @types не пише `gitHead`. Зате публікатор
DefinitelyTyped випускає версію одразу після злиття правки, тож версія несе файл таким, яким він
був у найновішому коміті, не пізнішому за мить її публікації в реєстрі.

Одиниця — коміт, з якого вийшла хоч одна версія: проміжні коміти між публікаціями до npm не
потрапляли і в корпус не йдуть. Версії документа — усі версії, що вийшли з цього коміту.

Текст — файл .d.ts, поділений на розділи за оголошеннями верхнього рівня (`export interface
ListProps`, `export class FixedSizeList` …): розділ — оголошення разом із коментарем JSDoc над
ним, блоком коду. Так уривок про `itemSize` веде в розділ інтерфейсу, де ця властивість стоїть.
"""

import json
import re
from datetime import datetime
from urllib.parse import parse_qs, quote, urlsplit

from engine.readers import Item, _markup, register

_COMMITS = re.compile(r"^/repos/([^/]+)/([^/]+)/commits$")
_STABLE = re.compile(r"^\d+\.\d+\.\d+$")
_DECL = re.compile(r"^(?:export\s+)?(?:declare\s+)?(?:default\s+)?(?:abstract\s+)?"
                   r"(interface|type|class|function|const|let|var|namespace|enum)\s+([\w$]+)")


def _when(stamp: str) -> datetime:
    return datetime.fromisoformat(stamp.replace("Z", "+00:00"))


def _sections(text: str) -> str:
    """Файл .d.ts → markdown: шапка файла (коментарі, імпорти) і розділ на кожне оголошення
    верхнього рівня з коментарем над ним."""
    lines = text.replace("\r\n", "\n").split("\n")
    parts: list = []          # [заголовок, рядки]
    pending: list = []        # коментар і порожні рядки, що чекають свого оголошення
    head: list = []
    current = None
    comment = False
    for line in lines:
        starts = not line[:1].isspace() and line[:1] not in ("}", ")", "]", "")
        if starts and line.startswith(("/**", "/*", "//")) or comment:
            pending.append(line)
            comment = (comment or line.startswith("/*")) and "*/" not in line
            continue
        m = _DECL.match(line) if starts else None
        if m:
            current = [f"{m.group(1)} {m.group(2)}", pending + [line]]
            parts.append(current)
            pending = []
            continue
        if current is None:
            head.extend(pending + [line])
        else:
            current[1].extend(pending + [line])
        pending = []
    if current is None:
        head.extend(pending)
    else:
        current[1].extend(pending)
    out = []
    head_code = "\n".join(head).strip("\n")
    if head_code.strip():
        out.append(f"```ts\n{head_code}\n```")
    for title, body in parts:
        out.append(f"## {title}\n\n```ts\n" + "\n".join(body).strip("\n") + "\n```")
    return "\n\n".join(out)


@register("dt-history")
def dt_history(source: dict, ctx) -> list[Item]:
    parts = urlsplit(source["url"])
    m = _COMMITS.match(parts.path)
    path = (parse_qs(parts.query).get("path") or [""])[0]
    if not m or not path:
        raise SystemExit(f"{source['url']}: очікував перелік комітів файла "
                         f"/repos/ВЛАСНИК/РЕПО/commits?path=ШЛЯХ.")
    owner, repo = m.groups()
    per_page = int((parse_qs(parts.query).get("per_page") or ["30"])[0])
    commits: list = []
    for page in range(1, 101):
        url = source["url"] if page == 1 else f"{source['url']}&page={page}"
        try:
            batch = json.loads(ctx.text(url))
        except ValueError as exc:
            raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
        if not isinstance(batch, list):
            raise SystemExit(f"{url}: очікував список комітів.")
        commits.extend(batch)
        if len(batch) < per_page:
            break
    dated = sorted(((_when(c["commit"]["committer"]["date"]), c["sha"]) for c in commits
                    if isinstance(c, dict) and c.get("sha")), reverse=True)
    if not dated:
        raise SystemExit(f"{source['url']}: жодного коміту файла {path}.")
    try:
        packument = json.loads(ctx.text(source["versions"]))
    except ValueError as exc:
        raise SystemExit(f"{source['versions']}: відповідь не JSON ({exc}).")
    times = packument.get("time") or {}
    skip = re.compile(source["skip_versions"]) if source.get("skip_versions") else None
    # коміт → [версії], від найновішої версії
    by_commit: dict = {}
    for version in sorted((v for v in packument.get("versions") or {} if _STABLE.match(v)
                           and v in times and not (skip and skip.search(v))),
                          key=lambda v: _when(times[v]), reverse=True):
        published = _when(times[version])
        sha = next((s for when, s in dated if when <= published), None)
        if sha:
            by_commit.setdefault(sha, []).append(version)
    label = source.get("label", path)
    items = []
    for sha, versions in by_commit.items():
        raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{sha}/{quote(path)}"
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{sha}/{quote(path)}"
        name = f"{_markup.slug(path)}-{sha[:8]}"

        def make(raw=raw, blob=blob, versions=versions, sha=sha):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            body = (f"Published to npm as version {', '.join(reversed(versions))} "
                    f"from DefinitelyTyped commit {sha[:10]}.\n\n{_sections(text)}")
            _markup.require(label, body, raw, min_chars=1)
            return _markup.document(label, blob, ctx.stamp, body, ", ".join(versions))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодна версія реєстру не зіставилася з комітом.")
    return items
