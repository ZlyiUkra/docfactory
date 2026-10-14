"""Читачі релізів Node.js: розклад ліній і склад кожного релізу, журнал змін кожної версії.

`node-releases` — `url` — перелік усіх релізів (https://nodejs.org/dist/index.json: версія, дата, LTS-ім'я,
                  позначка безпекового релізу, версії npm, V8, libuv, OpenSSL, zlib, ABI модулів), `schedule` —
                  розклад ліній робочої групи релізів (schedule.json репозиторію nodejs/Release: початок,
                  Active LTS, Maintenance, End-of-life, кодове ім'я), `cite` — адреса для людей. Документи:
                  огляд усіх ліній («releases») і по документу на лінію (версія документа — мажор, «24»; у
                  0.x — «0.12»), де фази лінії стоять над переліком її релізів.

`changelog-node` — журнали змін `doc/changelogs/CHANGELOG_V<мажор>.md` репозиторію nodejs/node: `url` —
                   шаблон адреси з `{major}`, `majors` — перелік мажорів, `cite` — шаблон адреси для людей.
                   Один документ на версію: заголовок «2025-06-24, Version 24.3.0 (Current), @автор» і все до
                   розділу «### Commits» — Notable Changes, а в безпекових релізах — перелік CVE і вражених
                   ліній. Перелік комітів не береться: це тисячі рядків на версію без пояснень.

Навіщо. Довідник API каже, що є в кожній версії, але не каже, які лінії ще підтримуються, коли закінчиться
підтримка, що нового в релізі й який npm іде з якою версією Node — а з цього й починається вибір версії.
Розклад і перелік релізів — JSON, і спільні читачі markdown їх не беруть.
"""

import json
import re

from engine.readers import Item, _markup, register


def _line(version: str) -> str:
    """Лінія релізу: «v24.3.0» → «24», «v0.12.18» → «0.12»."""
    parts = version.lstrip("v").split(".")
    return ".".join(parts[:2]) if parts[0] == "0" else parts[0]


def _line_key(line: str) -> tuple:
    return tuple(int(x) for x in line.split("."))


def _phases(line: str, sched: dict) -> list[str]:
    """Рядки фаз лінії з розкладу; порожній перелік, коли лінії в розкладі немає."""
    s = sched.get(f"v{line}")
    if not s:
        return []
    rows = []
    if s.get("codename"):
        rows.append(f"- Codename: {s['codename']}")
    names = (("alpha", "Alpha"), ("start", "Initial release (Current)"), ("lts", "Active LTS start"),
             ("maintenance", "Maintenance LTS start"), ("end", "End-of-life"))
    for key, name in names:
        if s.get(key):
            rows.append(f"- {name}: {s[key]}")
    return rows


def _release_row(r: dict) -> str:
    kind = f"LTS '{r['lts']}'" if r.get("lts") else "Current"
    sec = ", security release" if r.get("security") else ""
    parts = [f"npm {r['npm']}" if r.get("npm") else "", f"V8 {r['v8']}" if r.get("v8") else "",
             f"libuv {r['uv']}" if r.get("uv") else "",
             f"OpenSSL {r['openssl']}" if r.get("openssl") else "",
             f"zlib {r['zlib']}" if r.get("zlib") else "",
             f"modules ABI {r['modules']}" if r.get("modules") else ""]
    return f"- {r['version']} — {r['date']} — {kind}{sec}; " + ", ".join(p for p in parts if p)


@register("node-releases")
def node_releases(source: dict, ctx) -> list[Item]:
    cite = source.get("cite", source["url"])
    state = {}

    def load():
        if not state:
            state["rel"] = json.loads(ctx.text(source["url"]))
            state["sched"] = json.loads(ctx.text(source["schedule"]))
        return state["rel"], state["sched"]

    rel, sched = load()
    lines: dict[str, list] = {}
    for r in rel:
        lines.setdefault(_line(r["version"]), []).append(r)
    order = sorted(set(lines) | {k[1:] for k in sched}, key=_line_key, reverse=True)

    def overview():
        rel, sched = load()
        out = ["Every Node.js release line: its phases from the Release Working Group schedule "
               "(dates are subject to change; the rules of the phases are in the Release Working Group "
               "README) and its newest release.", ""]
        for line in order:
            rs = lines.get(line, [])
            out += [f"## Node.js {line}.x", ""] + _phases(line, sched)
            if rs:
                newest, first = rs[0], rs[-1]
                out.append(f"- Releases: {len(rs)}, from {first['version']} ({first['date']}) "
                           f"to {newest['version']} ({newest['date']})")
            out.append("")
        body = _markup.markdown_body("\n".join(out))
        return _markup.document("Node.js release lines: schedule, LTS and end-of-life", cite,
                                ctx.stamp, body, "releases")

    items = [Item(id=f"{source['id']}/overview", file=f"{source['id']}--overview.txt",
                  make=overview)]
    for line in order:
        if line not in lines:
            continue

        def make(line=line):
            rel, sched = load()
            rs = [r for r in rel if _line(r["version"]) == line]
            out = [f"Phases of the Node.js {line}.x line and every release of it, newest first, with "
                   "the versions of npm, V8, libuv, OpenSSL and zlib it ships.", ""]
            phases = _phases(line, sched)
            if phases:
                out += ["## Schedule", ""] + phases + [""]
            out += ["## Releases", ""] + [_release_row(r) for r in rs]
            body = _markup.markdown_body("\n".join(out))
            return _markup.document(f"Node.js {line}.x releases", cite, ctx.stamp, body, line)

        name = f"line-{line}"
        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    return items


_ANCHOR = re.compile(r'^<a id="(?P<v>\d+\.\d+\.\d+)"></a>\s*$', re.M)
_HEAD = re.compile(r"^## (?P<date>\d{4}-\d\d-\d\d), Version (?P<v>\d+\.\d+\.\d+)(?P<rest>.*)$", re.M)
_COMMITS = re.compile(r"^###\s+(?:Semver-\w+\s+)?Commits\s*$", re.M)


@register("changelog-node")
def changelog_node(source: dict, ctx) -> list[Item]:
    items = []
    for major in source["majors"]:
        url = source["url"].format(major=major)
        cite = source.get("cite", source["url"]).format(major=major)
        text = ctx.text(url).replace("\r\n", "\n")
        _markup.refuse_html(text, url)
        heads = list(_HEAD.finditer(text))
        if not heads:
            raise SystemExit(f"{url}: жодного заголовка «## дата, Version X.Y.Z» — формат змінився, "
                             f"читача треба поправити.")
        for i, head in enumerate(heads):
            end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
            chunk = text[head.end():end]
            cut = _COMMITS.search(chunk)
            chunk = _ANCHOR.sub("", chunk[:cut.start()] if cut else chunk)
            if not chunk.strip():
                continue
            version = head.group("v")
            # «'Jod' (LTS), @aduh95» → «'Jod' (LTS)»: хто випускав, для відповіді не важить.
            rest = re.sub(r",\s*@[\w-]+.*$", "", head.group("rest")).strip(" ,")
            title = f"Node.js {version} {rest} — {head.group('date')}".replace("  ", " ")

            def make(chunk=chunk, title=title, version=version, cite=cite):
                body = _markup.markdown_body(chunk)
                _markup.require(title, body, f"{cite}#{version}", min_chars=1)
                return _markup.document(title, f"{cite}#{version}", ctx.stamp, body, version)

            name = f"{source.get('name_prefix', 'node-changelog')}-{version}"
            items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                              make=make))
    return items
