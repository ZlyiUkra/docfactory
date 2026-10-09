"""Читач історії файлів репозиторію за комітами: один документ на кожен неповторний вміст файла.

`ghfile-history` — файли, що живуть у репозиторії без версійних тегів, а змінюються самі:
                   Dockerfile образу, скрипт входу, README, шаблони. `url` — перелік комітів
                   гілки через API (…/repos/ВЛАСНИК/РЕПО/commits?sha=ГІЛКА&per_page=100,
                   можна з `&path=тека`); дерева комітів читаються з тієї ж пари
                   ВЛАСНИК/РЕПО (…/git/trees/).

Поля джерела:
- `include` — вирази шляхів (відносно `root`), що беруться; `exclude` — що ні;
- `root` — тека репозиторію, від якої рахуються шляхи (дерево `коміт:тека`); без неї — корінь;
- `code` — мови блоків коду: об'єкт «вираз шляху → мова»; файл, що не збігся ні з одним
  виразом, читається як markdown;
- `major` — вираз шляху з однією групою: мажорна версія, з якої файл (`^(\\d+(?:\\.\\d+)?)/`);
- `version_files` — вираз шляхів файлів, з вмісту яких береться точна версія, і
  `content_version` — вираз з однією групою, що її вибирає (`^ENV PG_VERSION[ =]+(\\S+)`).
  Версія `19beta4` чи `12rc1` не стабільна: такі редакції в корпус не потрапляють, а мажор
  без жодної стабільної редакції в цьому коміті вважається ще не випущеним;
- `text_versions` — для markdown: `{"scope": вираз ділянки, "token": вираз з однією групою}`,
  версії документа — усі збіги `token` у ділянці (так у README образу видно, які теги
  підтримувалися в цій редакції).

Навіщо. `ghdocs-history` бере знімки на теги, а репозиторій образу `docker-library/postgres`
тегів не має: образ — це Dockerfile у теці мажору (`14/bookworm/Dockerfile`), що змінюється
з кожним мінорним випуском PostgreSQL. Різних вмістів за 986 комітів — кілька тисяч, а
пар «шлях, вміст» у переліку було б у кілька разів більше, якби брати знімок на коміт.
Тут одиниця — пара «шлях, вміст» (вміст упізнається хешем blob із дерева коміту): така пара
стає одним документом, а в шапку лягає найновіший коміт, де файл був саме таким.

Версія. Dockerfile — точна версія PostgreSQL з його вмісту (`14.24`): фільтр `version: "14"`
знаходить усі редакції лінії. Інший файл мажорної теки (скрипт входу) — мажор зі шляху.
Файл без мажора в шляху (спільний скрипт, шаблон) — перелік стабільних мажорів, що були в
деревах, де цей вміст лежав.

Редакція чинна з першого до останнього коміту, де вміст лежав таким: ці дати стоять
першим рядком тіла, щоб у відповіді було видно, коли саме це було правдою.
"""

import json
import re
from urllib.parse import parse_qs, quote, urlsplit

from engine.readers import Item, _markup, register

_COMMITS = re.compile(r"^/repos/([^/]+)/([^/]+)/commits$")
_STABLE = re.compile(r"^(\d+(?:\.\d+)*)(?:-.*)?$")
_NUM = re.compile(r"\d+")


def _order(value: str) -> tuple:
    """Ключ порядку версій: «9.6» < «10» < «14.2», а не за абеткою."""
    return tuple(int(n) for n in _NUM.findall(value))


def _join(values) -> str:
    return ", ".join(sorted(dict.fromkeys(values), key=_order))


@register("ghfile-history")
def ghfile_history(source: dict, ctx) -> list[Item]:
    parts = urlsplit(source["url"])
    m = _COMMITS.match(parts.path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував перелік комітів "
                         f"/repos/ВЛАСНИК/РЕПО/commits?sha=ГІЛКА&per_page=100.")
    owner, repo = m.groups()
    include = [re.compile(x) for x in source.get("include") or ()]
    if not include:
        raise SystemExit(f"{source['id']}: читач ghfile-history потребує поля include.")
    exclude = [re.compile(x) for x in source.get("exclude") or ()]
    code = [(re.compile(k), v) for k, v in (source.get("code") or {}).items()]
    major = re.compile(source["major"]) if source.get("major") else None
    vfiles = re.compile(source["version_files"]) if source.get("version_files") else None
    cver = re.compile(source["content_version"], re.M) if source.get("content_version") else None
    tv = source.get("text_versions") or {}
    tv_scope = re.compile(tv["scope"]) if tv.get("scope") else None
    tv_token = re.compile(tv["token"]) if tv.get("token") else None
    root = (source.get("root") or "").strip("/")
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""
    per_page = int((parse_qs(parts.query).get("per_page") or ["30"])[0])

    commits: list = []                                   # від найновішого
    for page in range(1, 301):
        url = source["url"] if page == 1 else f"{source['url']}&page={page}"
        try:
            batch = json.loads(ctx.text(url))
        except ValueError as exc:
            raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
        if not isinstance(batch, list):
            raise SystemExit(f"{url}: у відповіді немає переліку комітів.")
        commits += [(c["sha"], c["commit"]["committer"]["date"][:10]) for c in batch]
        if len(batch) < per_page:
            break
    if not commits:
        raise SystemExit(f"{source['id']}: у гілці немає комітів.")

    trees = f"https://api.github.com/repos/{owner}/{repo}/git/trees/"
    raw_base = f"https://raw.githubusercontent.com/{owner}/{repo}/"
    texts: dict = {}                                     # sha blob → текст (лише для version_files)

    def text_of(sha: str, commit: str, path: str) -> str:
        if sha not in texts:
            texts[sha] = ctx.text(f"{raw_base}{commit}/{quote(root + '/' if root else '')}{quote(path)}")
        return texts[sha]

    def exact(sha: str, commit: str, path: str) -> str:
        """Точна версія з вмісту: '14.24'; '' — вираз не знайшов; 'unstable' — бета чи rc."""
        found = cver.search(text_of(sha, commit, path))
        if not found:
            return ""
        # «14.24-1.pgdg13+1» → «14.24»: суфікс збірки пакета Debian версією не є.
        number = _STABLE.match(found.group(1))
        return number.group(1) if number else "unstable"

    # (шлях, sha) → {перша: найновіший коміт, дати, мажори стабільних випусків}
    seen: dict = {}
    for commit, day in commits:
        ref = f"{commit}:{root}" if root else commit
        url = f"{trees}{ref}?recursive=1"
        code_, data = ctx.fetch(url)
        if code_ == "404":                               # теки ще (чи вже) не було
            continue
        if code_ != "200":
            raise SystemExit(f"{url}: відповідь {code_} — перелік не складено.")
        try:
            tree = json.loads(data.decode("utf-8", errors="replace"))
        except ValueError as exc:
            raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
        if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
            raise SystemExit(f"{url}: у відповіді немає дерева файлів.")
        if tree.get("truncated"):
            raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
        entries = [e for e in tree["tree"] if e.get("type") == "blob" and e.get("size", 1) > 0
                   and any(r.search(e["path"]) for r in include)
                   and not any(r.search(e["path"]) for r in exclude)]
        stable: set = set()                              # мажори зі стабільним Dockerfile
        labels: dict = {}
        for e in entries:
            if vfiles and cver and vfiles.search(e["path"]):
                label = exact(e["sha"], commit, e["path"])
                labels[e["path"]] = label
                mm = major.match(e["path"]) if major else None
                if mm and label != "unstable":
                    stable.add(mm.group(1))
        for e in entries:
            path, sha = e["path"], e["sha"]
            mm = major.match(path) if major else None
            if mm and mm.group(1) not in stable and vfiles:
                continue                                 # мажор ще не випущено
            if labels.get(path) == "unstable":
                continue
            rec = seen.setdefault((path, sha), {"commit": commit, "last": day, "first": day,
                                                "label": labels.get(path, ""), "majors": set()})
            rec["first"] = day                           # коміти йдуть від новіших до старіших
            rec["majors"] |= stable
            if mm:
                rec["major"] = mm.group(1)

    items = []
    for (path, sha), rec in seen.items():
        where = f"{owner}/{repo}/{rec['commit']}/{quote(root + '/' if root else '')}{quote(path)}"
        raw = f"https://raw.githubusercontent.com/{where}"
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{where.split('/', 2)[2]}"
        name = f"{lead}{_markup.slug(re.sub(r'[.](md|mdx)$', '', path))}-{sha[:8]}"
        # Мажор файла в теці мажору, інакше мажори стабільних випусків із дерев, де він був.
        version = rec["label"] or rec.get("major") or _join(rec["majors"])
        since, until = rec["first"], rec["last"]
        span = (f"Revision in force from {since} to {until} (dates of commits in "
                f"{owner}/{repo}).")

        def make(raw=raw, blob=blob, path=path, version=version, sha=sha, commit=rec["commit"],
                 span=span, rec=rec):
            text = texts.get(sha)
            if text is None:
                text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            lang = next((v for r, v in code if r.search(path)), None)
            if lang is None:
                _, rest = _markup.front_matter(text)
                body = _markup.markdown_body(rest).strip()
                title = next((ln.lstrip("# ").strip() for ln in rest.splitlines()
                              if ln.startswith("# ")), "") or path.rsplit("/", 1)[-1]
                title = f"{repo}: {title}" if repo not in title else title
                ver = version
                if tv_scope and tv_token:
                    scope = tv_scope.search(rest)
                    ver = _join(tv_token.findall(scope.group(0))) if scope else ""
                body = f"{span}\n\n{body}"
                _markup.require(title, body, raw, min_chars=1)
                return _markup.document(title, blob, ctx.stamp, body, ver)
            body = f"{span}\n\n```{lang}\n{text.rstrip()}\n```"
            title = f"{repo}: {path}"
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    if not items:
        raise SystemExit(f"{source['id']}: на жодному з {len(commits)} комітів немає файлів "
                         f"за include.")
    return items
