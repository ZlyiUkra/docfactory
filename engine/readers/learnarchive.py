"""Читач архіву learn.microsoft.com «previous-versions»: старі версії документації, що
лишилися на сайті лише сторінками.

`learn-archive` — `url` — коренева сторінка набору: для архіву MSDN — «Books Online»
                  (…/sql/sql-server-2012/ms130214(v=sql.110)), для архіву docs — тека набору
                  (…/sql/2014/). `within` — тека набору: документом стає кожна знайдена
                  сторінка всередині неї. `query` — рядок запиту до кожної адреси набору
                  («view=sql-server-2014»: без нього сайт відповідає перенаправленням).
                  `title_suffix` — вираз хвоста назви, який сайт дописує сам
                  (« - SQL Server 2014», « - SQL Server 2014 Integration Services»).
                  `exclude` — вирази адрес, що не беруться;
                  `skip_meta` — {поле шапки: вираз}: сторінка, чия шапка під нього
                  підпадає, не береться і не розгортається далі.
                  `version` — версія всіх документів джерела.
                  `workers` — скільки звернень іти разом (типово одне): з черги береться хвиля
                  з N адрес, сторінки й змісти тягнуться паралельно, а розбираються по черзі,
                  тож перелік, імена й тексти ті самі, що й в одному потоці (archive-2014:
                  8 220 документів однакові до байта); 429 і 503 так само чекають і повторюють.
                  `trust_store` — день «РРРР-ММ-ДД»: відповідь 200, що лежить у сховищі сирого з
                  цього дня чи пізніше, береться звідти без звернення. Лише на перезапуск
                  перерваного обходу; лишене в оголошенні, поле не дасть оновленню побачити
                  зміни сайту.

Навіщо окремий читач. Набори зібрано з приватних репозиторіїв: мета-поле
`original_content_git_url` веде в Azure DevOps (docs-archive-project) чи в закритий
MicrosoftDocs/sql-docs-archive-pr, тож markdown-джерела немає ніде, крім самого сайту. Сайт
же віддає кожну сторінку ще й markdown-ом — на заголовок «Accept: text/markdown»: це його
власне зведення HTML з шапкою YAML, таблицями рядками «| … |» і кодом в огорожах. Ним читач і
користується: у HTML тих самих сторінок кожна клітинка таблиці розбита на абзаци.

Перелік. Мапа сайту (_sitemaps/previous-versions_en-us_N.xml) неповна: у ній лише частина
сторінок довідника класів, жодної з 116 адрес кореневого змісту SQL Server 2012, а набору
2014 немає зовсім (сторінки NOINDEX,NOFOLLOW). Тому перелік — обхід від кореня: читач бере
сторінку, з її шапки — `toc_rel` (зміст, до якого вона належить), зі змісту — усі адреси в
межах набору, з тіла — посилання в межах набору, і так далі, кожну адресу раз.
- Архів MSDN (2012, 2008 R2, 2008, 2005): зміст розбито по вузлах — <сторінка>/toc.json є
  лише в сторінки з дітьми і показує шлях від кореня, її дітей і розгорнуті вузли-контейнери
  без адреси. Лист посилається на зміст батька, тож зайвих звернень немає.
- Архів docs (2014): зміст — toc.json теки, і кореневий зміст називає лише частину тек
  (in-memory-oltp, backup-restore, service-broker… — ні). Їхні сторінки знаходяться
  посиланнями з тіла, а з першої ж такої сторінки — і зміст теки.
Сторінки читаються вже під час переліку — інакше не знайти ні посилань, ні змісту; зі
сховищем сирого `make` бере ту саму відповідь звідти, без другого звернення. Тексти в пам'яті
не тримаються: лише множина адрес.

`skip_meta` відсікає сторінку за полем шапки: згенерований довідник класів .NET (SMO, AMO, RMO,
Report Builder…) — це десятки тисяч сторінок «Namespace / Class / Method / Property» з
ідентифікатором `ms:assetid` виду «M:Microsoft.SqlServer.Management.Smo.Server.Alter»,
«T:…», «Methods.T:…». Така сторінка читається (інакше її не впізнати), але не потрапляє в
перелік, і ні її зміст, ні посилання далі не розгортаються: простір імен коштує одне
звернення, а не тисячі.

Ім'я документа. В архіві MSDN — ідентифікатор статті без версії: «ms174979(v=sql.110)» →
«ms174979». Ідентифікатор той самий в усіх версіях (CREATE TABLE — ms174979 і в 2005, і в
2012), тож незмінні розділи сусідніх версій однієї родини (families) зливаються. В архіві
docs — шлях сторінки від теки набору, як у читача docfx («relational-databases/backup-
restore/full-file-backups-sql-server» → «relational-databases-backup-restore-full-file-
backups-sql-server»): набір 2014 відгалузився від того самого дерева sql-docs, і ключ
збігається з ключем тієї ж сторінки новіших версій.

Текст. Шапка YAML і перший заголовок знімаються; назва — з цього заголовка (а без нього — з
поля `title`) без «| Microsoft Learn» і `title_suffix`. Екранування markdown («database\\_name»)
знімається поза кодом; «<br>» у клітинці таблиці стає «; » між пунктами чи пробілом після
речення (рядок таблиці лишається одним рядком); зображення випадають (піктограми «Topic link
icon», «Small File Folder Icon» — шум); рядок-підпис «Note» / «Important» / «Caution» стає
«Note:»; кнопки «Ask a question in the … Forums» і «Send Feedback» технічних статей MSDN
знімаються. Посилання — своїм текстом, як в інших читачів. Адреса документа — жива сторінка
(`canonicalUrl` шапки).
"""

import collections
import html as html_lib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote, urljoin, urlsplit

from engine import net
from engine.readers import Item, _markup, register

_ACCEPT = "text/markdown"
_GONE = ("збій: HTTP 404", "збій: HTTP 410")
# Посилання markdown з адресою, де трапляються дужки одного рівня («ms175874(v=sql.105)»),
# і посилання HTML, що лишилися в тексті сирими.
_LINK = re.compile(r"\]\(\s*<?((?:[^()\s<>]|\([^()\s]*\))+)>?(?:\s+\"[^\"]*\")?\s*\)")
_HREF = re.compile(r'\bhref="([^"]+)"')
_MSID = re.compile(r"^(.+?)\((v=[^()]+)\)$")
_VER = re.compile(r"\(v=[^()]+\)$")
# Файл, а не сторінка: зображення, архіви прикладів, документи.
_FILE = re.compile(r"\.(?:gif|png|jpe?g|svg|bmp|ico|zip|exe|msi|cab|pdf|xps|docx?|xlsx?|"
                   r"pptx?|vsd|txt|xml|xsd|json|ya?ml|css|js|mp4|wmv)$", re.I)
_FENCE = re.compile(r"^\s*(```+|~~~+)")
_IMG = re.compile(r"!\[[^\]]*\]\((?:[^()]|\([^()]*\))*\)")
_BR = re.compile(r"(?:\s*<br\s*/?>\s*)+", re.I)
_ESC = re.compile(r"\\([\\`*_{}\[\]()#+\-.!<>~])")
_CODE_SPAN = re.compile(r"(`+)(.+?)\1")
_LABEL = re.compile(r"^(\s*)(Note|Notes|Important|Caution|Tip|Warning|Security Note)\s*$")
_H1 = re.compile(r"\A\s*# (.+?)\s*$", re.M)
_FRONT_RE = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.S)
_LEARN = re.compile(r"\s*\|\s*Microsoft Learn\s*$")
# Хвіст старих сторінок MSDN (технічні статті): кнопки форуму й відгуку, а не текст.
_NOISE = re.compile(r"^\s*(?:- )?(?:(?:\*\*)?Ask a question(?:\*\*)? in the [\w .]*Forums?)?\s*"
                    r"(?:Send Feedback(?: on the [\w ]+)?)?\s*$")
# Кожні стільки сторінок обхід каже, де він: перелік великого набору — години звернень.
REPORT_EVERY = 500


def _front(text: str) -> tuple[dict, str]:
    """(поля шапки YAML, решта). Не _markup.front_matter: ключі тут бувають з двокрапкою
    («ms:assetid: M:Microsoft…»), і ключ відділяється лише «: » з пробілом."""
    m = _FRONT_RE.match(text)
    if not m:
        return {}, text
    meta = {}
    for ln in m.group(1).split("\n"):
        key, sep, value = ln.partition(": ")
        if sep and not ln[:1].isspace() and not ln.startswith("-"):
            meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, text[m.end():]


def _with_query(url: str, query: str) -> str:
    return f"{url}{'&' if '?' in url else '?'}{query}" if query else url


def _unescape(line: str) -> str:
    """Рядок без екранування markdown поза `кодом`: у коді зворотна похила — своя."""
    parts, pos = [], 0
    for m in _CODE_SPAN.finditer(line):
        parts.append(_ESC.sub(r"\1", line[pos:m.start()]))
        parts.append(m.group(0))
        pos = m.end()
    parts.append(_ESC.sub(r"\1", line[pos:]))
    return "".join(parts)


def _br(m) -> str:
    """Перенос рядка всередині клітинки таблиці: між пунктами переліку («sp_addserver<br>
    sp_dropremotelogin») — «; », після кінця речення чи перед пунктом «- » — пробіл."""
    before = m.string[:m.start()].rstrip()[-1:]
    after = m.string[m.end():m.end() + 2]
    return " " if not before or before in ".:;!?|" or after == "- " else "; "


def _clean(text: str) -> str:
    """Markdown сайту → markdown, який далі розбирає _markup.markdown_body."""
    out, fence = [], ""
    for ln in text.split("\n"):
        fm = _FENCE.match(ln)
        if fence:
            out.append(ln)
            if fm and ln.strip().startswith(fence) and not ln.strip()[len(fence):].strip():
                fence = ""
            continue
        if fm:
            fence = fm.group(1)
            out.append(ln)
            continue
        ln = _BR.sub(_br, _IMG.sub("", ln))
        ln = _unescape(ln)
        lm = _LABEL.match(ln)
        if lm:
            ln = f"{lm.group(1)}{lm.group(2)}:"
        out.append(ln)
    return "\n".join(out)


def _quiet(body: str) -> str:
    """Тіло без кнопок форуму й відгуку. Вони — посилання, тож упізнаються вже текстом,
    після _markup.markdown_body; код не чіпається."""
    out, fence = [], False
    for ln in body.split("\n"):
        if ln.startswith("```"):
            fence = not fence
        elif not fence and ln.strip() and _NOISE.match(ln):
            continue
        out.append(ln)
    return _markup.tidy("\n".join(out), strip=False)


def _title(meta: dict, rest: str, suffix) -> tuple[str, str]:
    """(назва, тіло без першого заголовка)."""
    m = _H1.match(rest)
    title = m.group(1) if m else meta.get("title", "")
    if m:
        rest = rest[m.end():]
    title = _LEARN.sub("", html_lib.unescape(_unescape(title.replace("''", "'"))))
    if suffix is not None:
        title = suffix.sub("", title)
    return " ".join(title.split()), rest


def _links(text: str):
    """Адреси посилань тіла поза огорожами коду."""
    fence = ""
    for ln in text.split("\n"):
        fm = _FENCE.match(ln)
        if fence:
            if fm and ln.strip().startswith(fence) and not ln.strip()[len(fence):].strip():
                fence = ""
            continue
        if fm:
            fence = fm.group(1)
            continue
        yield from _LINK.findall(ln)
        yield from _HREF.findall(ln)


@register("learn-archive")
def learn_archive(source: dict, ctx) -> list[Item]:
    within = [w for w in source.get("within") or [] if w.endswith("/")]
    if not within:
        raise SystemExit(f"{source['id']}: читач learn-archive вимагає поля `within` — "
                         f"теки набору з косою рискою в кінці.")
    query = source.get("query", "")
    suffix = re.compile(f"(?:{source['title_suffix']})$") if source.get("title_suffix") else None
    exclude = [re.compile(x) for x in source.get("exclude") or ()]
    skip = {k: re.compile(v) for k, v in (source.get("skip_meta") or {}).items()}
    host = urlsplit(within[0]).hostname

    def norm(link: str, base: str) -> str | None:
        """Адреса сторінки набору за посиланням, або None — поза набором чи не сторінка."""
        if not link or link.startswith(("#", "mailto:", "javascript:")) or "[" in link:
            return None
        parts = urlsplit(urljoin(base, link))
        if parts.scheme != "https" or parts.hostname != host:
            return None
        path = unquote(parts.path)
        if ".." in path.split("/") or _FILE.search(path) or path.endswith("/toc.json"):
            return None
        path = _VER.sub(lambda m: m.group(0).lower(), path)
        url = f"https://{host}{path}"
        if not any(url.startswith(w) for w in within) or not ctx.allowed(url):
            return None
        if any(x.search(url) for x in exclude):
            return None
        return url

    def skipped(meta: dict) -> bool:
        return any(x.search(meta.get(k, "")) for k, x in skip.items())

    def names_of(url: str) -> list[str]:
        """Ім'я документа і запасне — для збігу (стаття двох версій в одній теці MSDN,
        «ms123456(v=sql.110)» і «ms123456(v=msdn.10)»)."""
        base = next(w for w in within if url.startswith(w))
        rel = url[len(base):].strip("/")
        m = _MSID.match(rel)
        if m and "/" not in rel:
            return [_markup.slug(m.group(1)), _markup.slug(rel)]
        return [_markup.slug(re.sub(r"(^|/)index$", "", rel) or "index"), _markup.slug(rel)]

    start = norm(source["url"], source["url"])
    if start is None:
        raise SystemExit(f"{source['id']}: корінь {source['url']} поза полем `within`.")
    queue = collections.deque([start])
    seen, tocs = {start}, set()
    pages: list[tuple[str, str]] = []
    canon: set = set()

    def add(url: str | None) -> None:
        if url and url not in seen:
            seen.add(url)
            queue.append(url)

    workers = max(1, int(source.get("workers") or 1))
    trust = str(source.get("trust_store") or "")

    def fetch(url: str, accept: str = "") -> tuple[str, bytes, str]:
        """(код, тіло, день із сховища) однієї адреси. З `trust_store` відповідь 200, що вже
        лежить у сховищі сирого з дня не раніше названого, береться звідти без звернення:
        перезапуск обходу після збою не мусить заново питати тисячі сторінок. Адреса, яку
        білий список не пускає (переадресація на чинний сайт), — код «refused»."""
        if trust and ctx.store is not None and ctx.allowed(url):
            got = ctx.store.get(url, accept)
            if (got is not None and got[0].get("code", "200") == "200"
                    and got[0].get("day", "") >= trust):
                return "200", got[1], got[0].get("day", "")
        try:
            code, data = ctx.fetch(url, accept=accept) if accept else ctx.fetch(url)
        except net.Refused as exc:
            return "refused", str(exc).encode("utf-8"), ""
        return code, data, ""

    def toc_of(url: str, text: str) -> str:
        meta, _ = _front(text)
        if skipped(meta):
            return ""
        rel = meta.get("toc_rel", "")
        toc = urljoin(url, rel) if rel else ""
        if toc and toc not in tocs and any(toc.startswith(w) for w in within) and ctx.allowed(toc):
            return toc
        return ""

    def decoded(data: bytes) -> str:
        return data.decode("utf-8", errors="replace").replace("\r\n", "\n").lstrip("\ufeff")

    # `workers` > 1 — кілька звернень разом: з черги береться хвиля з N адрес, сторінки (а
    # потім і їхні змісти) тягнуться паралельно, а розбираються по черзі, як в одному потоці.
    # Хвиля — це рівно ті адреси, що стояли першими в черзі, тож черга, імена й документи ті
    # самі, що й без поля. Пауза між зверненнями лишається спільною на контекст.
    pool = ThreadPoolExecutor(workers) if workers > 1 else None
    while queue:
        wave = [queue.popleft() for _ in range(min(workers, len(queue)))]
        if pool is None:
            got = [fetch(_with_query(wave[0], query), _ACCEPT)]
        else:
            got = list(pool.map(lambda u: fetch(_with_query(u, query), _ACCEPT), wave))
        ahead: dict = {}
        if pool is not None:
            want = list(dict.fromkeys(
                t for (code, data, _), u in zip(got, wave) if code == "200"
                for t in [toc_of(u, decoded(data))] if t))
            for toc, res in zip(want, pool.map(lambda t: fetch(_with_query(t, query)), want)):
                ahead[toc] = res
        for url, (code, data, _day) in zip(wave, got):
            if code == "refused":
                # Архівна адреса, що переадресовує на чинний сайт (/sql/…?view=sql-server-2014), —
                # уже не сторінка архіву; білий список її не пускає, і падати мусить вона одна, а
                # не весь перелік.
                print(f"  {url}: {data.decode('utf-8', errors='replace')} — пропускаю", flush=True)
                continue
            if code in _GONE:
                continue
            if code != "200":
                # Збій зв'язку — не відповідь: сторінка лишається в переліку, і `make` спробує
                # ще раз; лише її посилання цього разу не знайдено.
                print(f"  {url}: {code} — посилань і змісту сторінки не знайдено", flush=True)
                pages.append((url, url))
                continue
            text = decoded(data)
            if text.lstrip()[:15].lower().startswith(("<!doctype html", "<html")):
                pages.append((url, url))
                continue
            meta, rest = _front(text)
            if skipped(meta):
                continue
            # Та сама сторінка під двома адресами (регістр, перенаправлення) — один документ.
            real = norm(meta.get("canonicalUrl", "").split("?")[0], url) or url
            if real in canon:
                continue
            canon.add(real)
            seen.add(real)
            pages.append((url, real))
            for link in _links(rest):
                add(norm(link, url))
            rel = meta.get("toc_rel", "")
            toc = urljoin(url, rel) if rel else ""
            if toc and toc not in tocs and any(toc.startswith(w) for w in within) and ctx.allowed(toc):
                tocs.add(toc)
                tcode, tdata, _ = ahead[toc] if toc in ahead else fetch(_with_query(toc, query))
                if tcode == "200":
                    try:
                        items = json.loads(tdata).get("items") or []
                    except ValueError:
                        items = []
                    stack = list(items)
                    while stack:
                        it = stack.pop()
                        if it.get("href"):
                            add(norm(it["href"], toc))
                        stack.extend(it.get("children") or [])
            if len(pages) % REPORT_EVERY == 0:
                print(f"  {source['id']}: перелік — {len(pages)} сторінок, у черзі {len(queue)}",
                      flush=True)
    if pool is not None:
        pool.shutdown()

    items, used = [], set()
    for url, real in pages:
        name, spare = names_of(real)
        if name in used:
            name, n = spare, 2
            while name in used:
                name, n = f"{spare}-{n}", n + 1
        used.add(name)

        def make(url=url, real=real):
            day = ""
            if trust:
                code, data, day = fetch(_with_query(url, query), _ACCEPT)
                if code != "200":
                    raise SystemExit(f"{url}: {code}")
                text = data.decode("utf-8", errors="replace")
            else:
                text = ctx.text(_with_query(url, query), accept=_ACCEPT)
            _markup.refuse_html(text, url)
            meta, rest = _front(text.replace("\r\n", "\n").lstrip("﻿"))
            title, rest = _title(meta, rest, suffix)
            body = _quiet(_markup.markdown_body(_clean(rest)))
            _markup.require(title, body, url, min_chars=1)
            live = meta.get("canonicalUrl", "")
            if not live.startswith(f"https://{host}/"):
                live = _with_query(real, query)
            return _markup.document(title, live, day or ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    if not items:
        raise SystemExit(f"{source['url']}: обхід не знайшов жодної сторінки — розмітка "
                         f"сайту змінилася.")
    return items
