"""ПРАКТИКА М5 · MCP-сервер над пошуком по корпусу документів примірника.

Своє API тут — шар пошуку з практик модулів 2–4: документи, поділені на фрагменти,
і пошук по словах BM25 над ними. Агент курсу возить цей пошук усередині свого
процесу; тут той самий пошук виставлений назовні двома інструментами, і його бачить
будь-який MCP-клієнт — Inspector, Claude Code, Cursor.

Завантажується весь корпус примірника: у ecmascript — уся ECMA-262 плюс ECMA-402,
ECMA-404, ECMA-414 і вільні документи, на які спирається 402, у react — документація
React усіх версій. Що саме завантажено, сервер пише в stderr на старті і дописує
окремим реченням до опису обох інструментів. Самі описи, ім'я сервера й імена
інструментів — дані домену: лежать у теці примірника (prompts/, config.json) і
читаються через common/profile.py, бо слова, якими сервер говорить з моделлю, у
кожного домену свої.

Шукає сервер двома способами. По словах — завжди: індекс BM25 будується з тих
самих файлів при завантаженні модуля і нічого більше не потребує. За змістом —
коли власник погодився на це при підготовці (server/setup.py): тоді поруч
працює Qdrant, а близькість рахує модель bge-small через ONNX. Обидва списки
зливаються за взаємним рангом, і відповідь пошуку каже полем `search`, який із
двох способів її дав.

Другий спосіб ніде не стоїть на критичному шляху. Контейнер піднімається, а
модель прогрівається в окремій нитці, тож на перший запит сервер відповідає
одразу, поки що по словах. Якщо Qdrant не піднявся або колекція порожня, сервер
не падає: пише причину в stderr і працює по словах далі.

Ключі серверу не потрібні: він не звертається ні до Anthropic, ні в мережу —
читає теки docs*/, говорить із Qdrant на localhost і більше нічого.

Запуск на stdio (сам по собі мовчки чекає клієнта — це не зависання): клієнт,
чи то Mode A, чи то Inspector, сам запускає цей процес і говорить у труби.

    .venv/bin/python server/spec_mcp.py

Запуск HTTP-сервером для Claude Code: довгий процес тримає порт примірника з
config.json, а Claude Code під'єднується за адресою (див. .mcp.json).

    .venv/bin/python server/spec_mcp.py --serve

Перевірки:

    .venv/bin/python -m server.smoke     функції напряму, повз протокол
    .venv/bin/python -m server.check     справжній stdio-клієнт
    npx -y @modelcontextprotocol/inspector .venv/bin/python server/spec_mcp.py
"""

import datetime
import os
import pathlib
import re
import sys
import threading

# Сервер запускають файлом («python server/spec_mcp.py»), і клієнт (Mode A,
# Inspector) робить це зі своєї поточної теки. Тому корінь коду фабрики
# (docfactory/, на рівень вище за server/) додаємо в шлях самі, інакше
# «import common» і «import server» не знайдуться.
_CODE_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(_CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(_CODE_ROOT))

# MCP SDK 1.x називав це FastMCP, у 2.0 — MCPServer; API той самий.
# Той самий подвійний імпорт, що в курсовому tracking_mcp.py.
try:
    from mcp.server import MCPServer as _Server          # SDK >= 2.0
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP as _Server  # SDK 1.x
    except ImportError:
        raise SystemExit("Потрібен MCP SDK:  pip install 'mcp[cli]'")

from common import instance
from common import nform
from common import profile
from common.corpus import (DOC_SET, Passage, corpus_archived, section_map,
                           used_cache, version_key, version_line, version_within)
from common.idmap import assign_ids
from common import mode
from common.lexical import LexicalIndex, tokenize

# Тека даних цього примірника: corpus/ уже прочитано через common, тут потрібні
# out/ для журналу викликів і config.json для порту HTTP-сервера. Її каже
# DF_INSTANCE_DIR, а не розташування коду — код спільний на всі домени.
_INSTANCE = instance.root()

# Скільки символів фрагмента віддавати у відповіді пошуку. Фрагменти бувають до
# півтори тисячі символів, і три таких у відповіді — це вже стіна тексту в
# контексті клієнта. Хто хоче повний текст, кличе read_section за ідентифікатором.
PREVIEW_CHARS = 600

# Межі k. Менше одного — безглуздо, більше десяти — це вже добрих кілька тисяч
# слів в одній відповіді, і клієнт платить за них своїми токенами.
K_MIN, K_MAX = 1, 10

# Найдовший рядок версії, який пошук приймає: «16.0.0-alpha.4» — чотирнадцять
# символів, а довше за сорок — уже не версія, а текст не в тому полі.
VERSION_MAX = 40

# Індекс будується один раз при завантаженні модуля, а не на кожен виклик:
# уся ECMA-262 читається з файлів і індексується приблизно за секунду, але
# робити це щоразу означало б платити цією секундою за кожен запит.
_INDEX = LexicalIndex()

# Ідентифікатори роздає common/idmap.py, а не сам Passage.pid: на повній
# специфікації два фрагменти можуть дістати однаковий pid, і один із них став би
# недосяжним. Те саме місце використовує заливання в Qdrant, тож ідентифікатор у
# відповіді пошуку і ідентифікатор у базі — той самий рядок.
_BY_ID, _UID = assign_ids(_INDEX.passages)

# Порожній індекс — завжди помилка даних, і сказати про неї треба словами ще
# тут: нижче код бере з індексу приклад ідентифікатора, і на порожньому словнику
# це падало б голим StopIteration без жодного натяку на причину. Порожнім індекс
# буває у свіжого домену, де corpus/ ще не наповнений.
if not _BY_ID:
    raise SystemExit(
        "spec_mcp: індекс порожній — жоден документ у corpus/ не дав фрагмента з "
        "текстом. Наповніть корпус (./df <домен> refresh) і підніміть сервер знову.")

_COUNT = len(_INDEX.passages)
_DOCS = len({p.doc_id for p in _INDEX.passages})

# Версії, які несуть документи, від найновішої. Порожньо — корпус версій не має.
_VERSIONS = sorted({v for p in _INDEX.passages for v in p.versions},
                   key=version_key, reverse=True)
_LINES = sorted({version_line(v) for v in _VERSIONS}, key=version_key, reverse=True)

# Що саме зараз завантажено — одним реченням для моделі. Це не можна написати в
# описі наперед: набір обирає той, хто запускає сервер, і лише сам сервер знає,
# що з цього вийшло. Модель, яка не знає меж того, що їй доступно, вигадує
# відповіді про розділи, яких тут немає. Речення — у prompts/loaded.txt
# примірника; числа й лінії версій підставляє сервер.
_LOADED = (profile.text("loaded")
           .replace("{excerpts}", str(_COUNT))
           .replace("{documents}", str(_DOCS))
           .replace("{versions}", ", ".join(_LINES)))

# Рядок діагностики — у stderr. У stdout не можна нічого: там ходять кадри
# JSON-RPC, і будь-який print ламає клієнтові розбір відповіді.
print(f"spec_mcp: набір «{DOC_SET}», проіндексовано {_COUNT} "
      f"{nform(_COUNT, 'фрагмент', 'фрагменти', 'фрагментів')} "
      f"з {_DOCS} {nform(_DOCS, 'розділу', 'розділів', 'розділів')}"
      f"{' (з кешу)' if used_cache() else ''}",
      file=sys.stderr)

# Звірка з документами: кожен розділ, у якого є власний текст, мусить бути в
# індексі. Мовчазна втрата вже траплялася — відбір за довжиною в corpus.py
# прибирав 368 коротких розділів, і пошук відповідав за них сусідніми номерами.
# Тепер втрата — не тихий мінус у числі фрагментів, а рядок з іменами при
# кожному старті, поруч із рештою чисел.
# В архівному режимі звіряти індекс нема з чим: документів у теці немає, і
# єдине джерело — той самий кеш, з якого індекс і зібрано. Мовчазного «усі
# розділи на місці» тут бути не повинно, тому сказано прямо.
if corpus_archived():
    # Перелік рубрик без власного тексту дають самі документи, тож в архіві
    # його нізвідки взяти: рубрика тим і відрізняється, що в індексі її немає.
    # read_section тоді на голий номер розділу відповість звичайним «такого id
    # немає» замість докладнішого «це рубрика, дивіться підрозділи».
    _SECTIONS: dict[str, bool] = {}
    print("spec_mcp: корпус в архіві — індекс із кешу, звірка з документами "
          "пропущена; щоб оновлювати корпус, поверніть тексти в corpus/",
          file=sys.stderr)
else:
    _SECTIONS = section_map()
    _WITH_TEXT = {s for s, has in _SECTIONS.items() if has}
    _LOST = _WITH_TEXT - {p.anchor for p in _INDEX.passages if p.section}
    if _LOST:
        print(f"spec_mcp: УВАГА: {len(_LOST)} "
              f"{nform(len(_LOST), 'розділ', 'розділи', 'розділів')} із власним "
              f"текстом немає в індексі: {', '.join(sorted(_LOST)[:5])}"
              f"{'…' if len(_LOST) > 5 else ''} — пошук відповідатиме сусідніми",
              file=sys.stderr)
    else:
        print(f"spec_mcp: усі {len(_WITH_TEXT)} розділів із власним текстом в "
              f"індексі; рубрик без тексту {len(_SECTIONS) - len(_WITH_TEXT)}",
              file=sys.stderr)

# Пошук за змістом: чи його просили, і чи він уже готовий.
#
# Рішення ухвалене один раз при підготовці (server/setup.py) і лежить у
# out/mode.json; тут його лише читають. Якщо просили — усе довге робиться в
# окремій нитці: підняти контейнер Qdrant, звірити колекцію, прогріти модель.
# На критичному шляху не стоїть нічого: сервер відповідає клієнтові одразу, а
# поки нитка не впоралася, пошук іде по словах. Так само він поводиться, коли
# Qdrant лежить і підняти його не вдалося.
_MODE = mode.read()
_VECTORS_ASKED = _MODE.get("search") == "vectors"
_VECTORS_READY = False
_VECTORS_WHY = "" if _VECTORS_ASKED else "не просили при підготовці"


def _prepare_vectors() -> None:
    global _VECTORS_READY, _VECTORS_WHY
    try:
        from common import embed, vectorstore
        if not vectorstore.ensure_running():
            _VECTORS_WHY = "Qdrant не відповідає і контейнер не піднявся"
        elif vectorstore.count() == 0:
            _VECTORS_WHY = (f"колекція {vectorstore.COLLECTION} порожня — "
                            f"запустіть python -m server.setup --vectors")
        else:
            embed.model()          # прогрів: перший запит не має платити за це
            _VECTORS_READY = True
            have = vectorstore.count()
            print(f"spec_mcp: пошук за змістом готовий, "
                  f"{have} точок у {vectorstore.COLLECTION}", file=sys.stderr)
            # Недолита колекція — не привід відмовлятися від неї: три з половиною
            # тисячі фрагментів шукають краще, ніж жодного. Але й мовчати про це
            # не можна: заливання переривається легко, а зовні недостача видно
            # тільки як «чомусь не знайшлося».
            if have < _COUNT:
                print(f"spec_mcp: у колекції {have} точок замість {_COUNT} — "
                      f"частина фрагментів шукається лише по словах; "
                      f"дорахувати: python -m server.setup --vectors",
                      file=sys.stderr)
            elif have > _COUNT:
                print(f"spec_mcp: у колекції {have} точок, а фрагментів {_COUNT} — "
                      f"колекція від іншого видання набору, і частина її точок "
                      f"описує текст, якого в документах уже немає; "
                      f"що з цим робити: python -m server.setup --vectors",
                      file=sys.stderr)
            return
    except Exception as exc:                      # noqa: BLE001 - причина в stderr
        _VECTORS_WHY = f"{type(exc).__name__}: {exc}"
    print(f"spec_mcp: пошук за змістом недоступний ({_VECTORS_WHY}); "
          f"працюю по словах", file=sys.stderr)


if _VECTORS_ASKED:
    # Нитка правильна для роботи: клієнт дістає відповідь одразу, поки що по
    # словах, а пошук за змістом підхоплюється секунд через десять. Для виміру
    # якості це не годиться — перші питання прогону шукали б по словах, пізніші
    # за змістом, і число залежало б від того, що встигло раніше. DF_VECTORS_WAIT
    # робить прогрів синхронним: сервер відповідає лише коли вектори готові.
    if os.getenv("DF_VECTORS_WAIT"):
        _prepare_vectors()
    else:
        threading.Thread(target=_prepare_vectors, name="vectors",
                         daemon=True).start()


# Журнал викликів: хто що питав.
#
# Кожен клієнт запускає власну копію цього сервера, тому в Inspector видно лише
# те, що питав Inspector, а в Claude Code — лише те, що питав Claude Code.
# Рядок нижче йде у два місця. У stderr — бо там його одразу показує Inspector
# (вкладка Console) і Claude Code із прапорцем --debug; це те саме stderr, куди
# картка велить складати всю діагностику, аби не зачепити stdout, де ходить
# протокол. У файл — бо stderr живе рівно стільки, скільки процес, а щоб
# порівняти виклики з різних клієнтів, запис має пережити їх усі.
#
# Файл тільки дописується. Ніщо в цьому коді його не читає, не чистить і не
# перезаписує; коли він набридне, власник прибирає його сам. Дві межі бережуть
# його від переповнення без жодного видалення:
# - поле запиту ріжеться тут, в одному місці, а не по місцях виклику — інакше
#   довжину рядка обирає той, хто кличе інструмент: запит на 50 000 символів
#   із хибним k колись лягав у файл цілим саме на тому шляху, що його відхиляв,
#   і модель, зациклена на незрозумілій їй помилці, заповнювала диск;
# - сягнувши стелі, файл більше не дописується — про це кажеться раз у stderr,
#   а сам stderr пишеться далі, тож Inspector і --debug нічого не втрачають.
#   Ротації навмисно немає: вона видаляла б журнал сама, без відома власника.
LOG_PATH = _INSTANCE / "out" / "calls.log"
LOG_FIELD_CHARS = 120
LOG_MAX_BYTES = 16 * 1024 * 1024
_PID = os.getpid()
_LOG_FULL = False


def _log(tool: str, request: str, outcome: str) -> None:
    global _LOG_FULL
    if len(request) > LOG_FIELD_CHARS:
        request = (f"{request[:LOG_FIELD_CHARS]}… "
                   f"(+{len(request) - LOG_FIELD_CHARS} симв.)")
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{stamp} pid={_PID} {tool} {request} -> {outcome}"
    print(line, file=sys.stderr)
    if _LOG_FULL:
        return
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        if LOG_PATH.exists() and LOG_PATH.stat().st_size >= LOG_MAX_BYTES:
            _LOG_FULL = True
            print(f"spec_mcp: журнал {LOG_PATH} сягнув "
                  f"{LOG_MAX_BYTES // (1024 * 1024)} МБ — у файл більше не пишу, "
                  f"stderr пишеться далі; приберіть або перейменуйте файл самі",
                  file=sys.stderr)
            return
        with LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except OSError as exc:
        # Журнал не має права зіпсувати відповідь клієнтові: якщо теки немає або
        # диск не пише, скаржимося в stderr і працюємо далі.
        print(f"spec_mcp: журнал не записався ({exc})", file=sys.stderr)


mcp = _Server(profile.SERVER_NAME)


def _preview(text: str) -> str:
    """Текст фрагмента для відповіді пошуку: обрізаний, з видимою позначкою обрізки."""
    if len(text) <= PREVIEW_CHARS:
        return text
    return text[:PREVIEW_CHARS] + "..."


# Санітар видачі — серверна оборона для клієнта, якого ми не контролюємо (Claude
# Code, Inspector). Це розтяжка на очевидні формулювання вшитих указівок, а не
# класифікатор: регулярний вираз не впізнає вказівку природною мовою, тож ключі
# нижче чіпляють лише типові звороти, і вказівка, сказана іншими словами,
# пройде повз. Зате спрацювання гучне: зачеплений фрагмент вилучається з
# відповіді цілком (див. _sanitize). Корпус тут чистий, тож у нормі розтяжка
# мовчить; чесні межі захисту названі в README.
_INJECTION = re.compile(
    r"ignore\s+(all\s+)?previous|disregard\s+(the\s+)?(above|previous)|"
    r"system\s+prompt|reveal\s+your|call\s+the\s+tool|fetch_url|"
    r"append\s+.{0,40}https?://|EDITORIAL\s+NOTE", re.I)


def _sanitize(passage: Passage) -> tuple[str, bool]:
    """Текст фрагмента для відповіді, або відмова замість нього. Повертає
    (текст, чи спрацювала розтяжка).

    Раніше вирізалися лише збіглі слова — а це гірше, ніж нічого: вказівка
    лишалася читною, маркер же створював враження, що її знешкоджено. Фрагмент,
    який зачепив розтяжку, не можна читати по шматках: замість тексту клієнт
    дістає відмову з номером розділу, а спрацювання лягає в out/calls.log."""
    if _INJECTION.search(passage.text):
        return (f"[{passage.label}: текст вилучено політикою сервера — у "
                f"фрагменті знайдено вбудовану вказівку для моделі, тож його "
                f"не видано ані цілим, ані частинами.]"), True
    return passage.text, False


def _degraded() -> str:
    """Чому видача врізана, англійською для моделі — або порожньо, коли все гаразд.

    Кричати в stderr мало: його бачить тільки той, хто сам підняв serve у своєму
    терміналі. Клієнт, що прийшов по HTTP, досі мав єдиний натяк — поле `search`
    зі значенням «words», — і відрізнити «документація мовчить» від «половина
    пошуку лежить» не міг. Тепер причина їде у відповіді.
    """
    if not _VECTORS_ASKED or _VECTORS_READY:
        return ""
    # Порожня причина означає, що нитка прогріву ще не дійшла до висновку:
    # перші секунди після старту сервер працює по словах не через поломку.
    why = _VECTORS_WHY or "still warming up, ask again in a few seconds"
    return (f"Meaning search is not available for this query ({why}), so this is a "
            f"word search only: a miss may mean the wording differs, not that the "
            f"documentation is silent.")


def _format_hits(passages: list[Passage], how: str) -> dict:
    """Відповідь пошуку. Формат той самий, що в common/search.py практики модуля 4,
    плюс поле `search` і обрізаний текст.

    Поле `search` каже моделі, як саме знайдено: «words» — лише по словах,
    «meaning+words» — обидва способи разом. Це не прикраса: коли пошук за змістом
    лежить, порожня відповідь означає інше, ніж коли він працює, і модель має
    змогу це врахувати.

    Поле `versions` є лише в корпусі з версіями: усі версії, в документах яких
    цей текст стоїть дослівно, від найновішої."""
    why = _degraded()
    if not passages:
        note = "Nothing in the available excerpts matches this query."
        return {"found": 0, "search": how,
                "note": f"{note} {why}".strip()}
    items = []
    for p in passages:
        clean, flagged = _sanitize(p)
        if flagged:
            _log("sanitize", f"id={_UID[p]}",
                 f"фрагмент вилучено з видачі {profile.SEARCH_TOOL}: розтяжка санітара")
        item = {"id": _UID[p], "section": p.label,
                "document": p.doc_title, "text": _preview(clean)}
        if p.versions:
            item["versions"] = list(p.versions)
        items.append(item)
    out = {"found": len(passages), "search": how, "passages": items}
    if why:
        out["note"] = why
    return out


def _rrf(rankings: list[list[Passage]], k: int, const: int = 60) -> list[Passage]:
    """Злиття двох списків за взаємним рангом (RRF).

    Пошук по словах і пошук за змістом дають оцінки в різних шкалах, і порівнювати
    їх безпосередньо не можна. RRF порівнює не оцінки, а місця: фрагмент, що
    трапився високо в обох списках, підіймається вище за той, що виграв лише в
    одному. Стала 60 — та, з якою цей спосіб опублікували; вона згладжує різницю
    між першим і другим місцем.
    """
    score: dict[Passage, float] = {}
    for ranking in rankings:
        for place, passage in enumerate(ranking):
            score[passage] = score.get(passage, 0.0) + 1.0 / (const + place + 1)
    return sorted(score, key=lambda p: -score[p])[:k]


# У скільки разів глибше просять кожен спосіб, перш ніж згорнути повтори розділу.
# Шість — з заміру server.quality: на його десятці цього запасу вистачає, щоб після
# згортання всі k місць були зайняті різними розділами.
DEPTH = 6


# Варіанти тієї самої сторінки для різних SDK — поле variant_pattern у config.json.
# У clerk сторінка Core 3 лежить у 10–12 варіантах (/docs/nextjs/…, /docs/astro/…),
# що різняться лише кодом; оцінки в них майже однакові, і п'ять місць видачі
# займала одна сторінка, а правильний SDK з них ще й випадав. Без поля _VARIANT —
# None, ключ розділу той самий, що й був, і видача не змінюється ні на місце.
_VARIANT = re.compile(profile.VARIANT_PATTERN) if profile.VARIANT_PATTERN else None


def _page_key(p: Passage) -> tuple[str, int]:
    """Ключ згортання: розділ разом із номером частини, а ім'я варіанта в ньому
    заміняється «*». Саме заміняється, а не вирізається: інакше
    docs-astro-reference-hooks-use-auth збігся б із reference-hooks-use-auth —
    сторінкою іншої лінії, яка мусить лишитися у видачі окремо."""
    m = _VARIANT.match(p.anchor) if _VARIANT else None
    if not m:
        return p.anchor, p.part
    return p.anchor[:m.start(1)] + "*" + p.anchor[m.end(1):], p.part


# Сторінка → {варіант: фрагмент}: щоб на запит, що називає SDK, віддати саме його
# варіант, навіть якщо пошук приніс інший.
_TWINS: dict[tuple[str, int], dict[str, Passage]] = {}
if _VARIANT:
    for _p in _INDEX.passages:
        _m = _VARIANT.match(_p.anchor)
        if _m:
            _TWINS.setdefault(_page_key(_p), {}).setdefault(_m.group(1), _p)
_ALIASES = sorted(
    ((a.lower(), name) for name in {v for twins in _TWINS.values() for v in twins}
     for a in (profile.VARIANT_ALIASES.get(name) or [name.replace("-", " ")])),
    key=lambda pair: -len(pair[0]))


def _wanted_variant(query: str) -> str:
    """Варіант, який називає запит («…in Next.js» → nextjs), або порожньо. Довша назва
    перемагає: «React Router» — це react-router, а не react."""
    if not _ALIASES:
        return ""
    q = " " + re.sub(r"\.(?=\s|$)", "", re.sub(r"[^a-z0-9.]+", " ", query.lower())) + " "
    return next((name for alias, name in _ALIASES if f" {alias} " in q), "")


def _only_wanted(query: str, keep=None):
    """Фільтр для variant_strict: коли запит називає варіант, фрагменти інших
    варіантів відсіюються разом із фільтром версії `keep`.

    Згортання тут не рятує: у tanstack-query довідник API кожного фреймворку має
    свої імена сторінок (injectQuery в Angular, createQuery у Solid), тож двійників
    у React вони не мають і, щільні на назви опцій, відтісняють гайди. Відсів іде
    до відбору місць, а не після, — інакше видача коротшала б. Варіант, у сторінки
    якого є двійник названого, лишається: часто саме він тягне сторінку вгору, а
    _dedup потім віддає місце двійникові. Сторінки поза виразом варіантів (README,
    приклади, журнали змін) проходять. Без поля чи без названого варіанта
    повертається сам `keep`, і видача та сама, що й була."""
    want = _wanted_variant(query) if profile.VARIANT_STRICT and _VARIANT else ""
    if not want:
        return keep

    def only(p: Passage) -> bool:
        m = _VARIANT.match(p.anchor)
        return ((not m or m.group(1) == want or want in _TWINS.get(_page_key(p), {}))
                and (keep is None or keep(p)))
    return only


def _dedup(passages: list[Passage], k: int, query: str = "") -> list[Passage]:
    """Одне місце у видачі — один розділ.

    Документація сусідніх версій описує той самий розділ майже однаково. Дослівні
    повтори злиті ще при побудові корпусу, але ті, що різняться парою слів,
    лишаються окремими фрагментами — і на запит про портали всі п'ять місць
    займав той самий розділ у п'яти редакціях. Тут лишається одна, найвища за
    рангом; решта поступається місцем іншим розділам.

    Ключ — розділ разом із номером частини: частини довгого розділу несуть різний
    текст, і згортати їх в одну не можна. З variant_pattern варіанти однієї
    сторінки для різних SDK — теж один розділ, і якщо запит називає SDK, місце
    дістається його варіантові.
    """
    want = _wanted_variant(query)
    seen, out = set(), []
    for p in passages:
        key = _page_key(p)
        if key in seen:
            continue
        seen.add(key)
        if want:
            p = _TWINS.get(key, {}).get(want, p)
        out.append(p)
        if len(out) == k:
            break
    return out


def _find(query: str, k: int, keep=None) -> tuple[list[Passage], str]:
    """Пошук по словах, а якщо готовий — разом із пошуком за змістом.

    Кожен спосіб просять углиб у DEPTH разів більше за k, і аж потім згортають
    повтори розділу: заміну витісненій редакції взяти більше нізвідки, а без
    запасу згортання лишило б видачу коротшою за k.

    `keep` — фільтр версії. Qdrant його не знає (версії фрагмента дописуються при
    злитті повторів і в payload точки могли б застаріти), тож за змістом береться
    ширший список, а відбір робиться тут, по фрагментах поточного корпусу.

    Злиття бачить по `fuse` місць кожного способу. Без поля `fusion_depth` у
    config.json це k — і тоді розділ, п'ятий по словах і четвертий за змістом, зі
    злиття по п'ять місць випадає, хоч обидва способи його знайшли. Примірник, якому
    це важливо, задає глибину сам; решта дістає рівно ту видачу, що й раніше."""
    keep = _only_wanted(query, keep)
    fuse = profile.FUSION_DEPTH or k
    deep = max(k * DEPTH, fuse)
    words = _dedup(_INDEX.retrieve(query, deep, keep), fuse, query)
    if not _VECTORS_READY:
        return words[:k], "words"
    try:
        from common import embed, vectorstore
        limit = deep if keep is None else max(50, deep * 2)
        hits = vectorstore.search(embed.embed_query(query), limit)
        meaning = [_BY_ID[h["uid"]] for h in hits if h.get("uid") in _BY_ID]
        if keep is not None:
            meaning = [p for p in meaning if keep(p)]
        meaning = _dedup(meaning, fuse, query)
    except Exception as exc:                      # noqa: BLE001 - причина в stderr
        print(f"spec_mcp: пошук за змістом не відповів ({exc}); "
              f"віддаю знайдене по словах", file=sys.stderr)
        return words[:k], "words"
    if not meaning:
        return words[:k], "words"
    return _dedup(_rrf([words, meaning], k * 2), k, query), "meaning+words"


def _search(query: str, k: int, version: str | None = None) -> dict:
    """Пошук, спільний для обох форм інструмента. Опис для моделі — не тут, а в
    prompts/search.txt примірника: що шукати і коли не кликати, у кожного домену
    своє."""
    tool = profile.SEARCH_TOOL
    tail = f" version={version!r}" if version else ""
    if not isinstance(k, int) or k < K_MIN or k > K_MAX:
        _log(tool, f"query={query!r} k={k!r}{tail}", "помилка: k поза межами")
        return {"error": f"k має бути від {K_MIN} до {K_MAX}"}

    keep = None
    if version is not None:
        if not isinstance(version, str) or len(version) > VERSION_MAX:
            _log(tool, f"query={query!r} k={k}{tail}", "помилка: версія не рядок чи задовга")
            return {"error": f"version має бути рядком до {VERSION_MAX} символів, "
                             f"напр. \"18\" або \"16.8\""}
        want = version.strip().removeprefix("v")
        if want:
            if not any(version_within(v, want) for v in _VERSIONS):
                _log(tool, f"query={query!r} k={k}{tail}", "такої версії немає")
                return {"found": 0, "search": "words",
                        "note": f"Nothing here is marked with version {want!r}. "
                                f"Release lines held here: {', '.join(_LINES)}. Pass one "
                                f"of them or a longer version within it (\"18\" matches "
                                f"every 18.x, \"16.8\" every 16.8.x), or leave version "
                                f"empty to search everything."}

            def keep(p: Passage) -> bool:
                return any(version_within(v, want) for v in p.versions)

    # Запит без жодного латинського слова далі не йде — ані в пошук по словах,
    # ані в пошук за змістом. По словах він і так дав би нуль: токенізатор бачить
    # тільки [a-z0-9_]+. А от пошук за змістом дав би відповідь, і в цьому вся
    # біда: модель векторів англійська, кирилицю вона зводить до чисел, які нічого
    # не означають, але найближчі сусіди в них знайдуться завжди. Клієнт дістав би
    # три впевнені номери розділів навмання — саме та помилка, проти якої написано
    # абзац «коли не кликати». Тому тут відповідь чесна: шукати не було чого.
    if not tokenize(query):
        _log(tool, f"query={query!r} k={k}{tail}", "нуль латинських слів у запиті")
        return {"found": 0, "search": "words",
                "note": "The query has no latin words, and everything held here "
                        "is English -- both the word index and the meaning index. "
                        "Translate the question into the terms the specification "
                        "uses, then search again."}

    hits, how = _find(query, k, keep)
    _log(tool, f"query={query!r} k={k}{tail}", f"знайдено {len(hits)} ({how})")
    return _format_hits(hits, how)


def search_spec(query: str, k: int = 3) -> dict:
    """Пошук без фільтра версії — для корпусу, де документи версій не мають."""
    return _search(query, k)


def search_versioned(query: str, k: int = 3, version: str = "") -> dict:
    """Пошук з фільтром версії: "18" лишає 18.x, "0.14" — 0.14.x, порожньо — усе."""
    return _search(query, k, version)


def read_section(id: str) -> dict:
    """Повний текст одного фрагмента за ідентифікатором з видачі пошуку. Опис для
    моделі — prompts/read.txt примірника."""
    tool = profile.READ_TOOL
    passage = _BY_ID.get(id)
    if passage is None:
        # Голий номер розділу — найчастіша вгадка моделі. Якщо документи такий
        # розділ справді називають, відповідь мусить сказати, що з ним:
        # рубрика без власного тексту — це межа корпусу, а не помилка виклику,
        # і мовчати про неї означає вчити модель гадати номери далі.
        sec = id.strip()
        if sec in _SECTIONS and not _SECTIONS[sec]:
            _log(tool, f"id={id!r}", "рубрика без власного тексту")
            return {"error": f"розділ {sec} існує, але власного тексту не має — "
                             f"його вміст лежить у підрозділах",
                    "hint": f"знайдіть підрозділи через {profile.SEARCH_TOOL} і читайте "
                            f"їх за id з видачі"}
        if sec in _SECTIONS:
            _log(tool, f"id={id!r}", "номер розділу замість id")
            return {"error": f"розділ {sec} в індексі є, але читається він за "
                             f"повним id, а не голим номером",
                    "hint": f"id береться з поля id у відповіді {profile.SEARCH_TOOL}, "
                            f'напр. "{_EXAMPLE_ID}"'}
        _log(tool, f"id={id!r}", "помилка: такого id немає")
        return {"error": "фрагмента з таким id немає",
                "hint": f"id береться з поля id у відповіді {profile.SEARCH_TOOL}"}
    clean, flagged = _sanitize(passage)
    if flagged:
        _log(tool, f"id={id!r}", "фрагмент вилучено з відповіді: розтяжка санітара")
    else:
        _log(tool, f"id={id!r}", f"{len(passage.text)} символів")
    answer = {"id": _UID[passage],
              "section": passage.label,
              "document": passage.doc_title,
              "url": passage.url,
              "fetched": passage.fetched,
              "text": clean}
    if passage.versions:
        answer["versions"] = list(passage.versions)
    return answer


# Реєстрація. Обидва інструменти могли б висіти на звичайному @mcp.tool(), і тоді
# описом ставав би самий докстрінг — так зроблено в курсовому tracking_mcp.py.
# Тут описом стає текст із prompts/ примірника ПЛЮС рядок про завантажений набір:
# інакше модель не знає, де межа того, що їй доступно, а заготовлений текст цієї
# межі знати не може, бо її обирають при запуску.
#
# Так само дописується приклад ідентифікатора для read_section. У заготовці його
# теж не напишеш наперед: ідентифікатор починається з імені файла, а те саме
# місце специфікації лежить у різних наборах у файлах із різними іменами —
# «14-object-objects#20.1.3.6/2» у наборі core і «20-fundamental-objects#20.1.3.6/2»
# у full та suite. Приклад модель копіює дослівно, тож він мусить бути з того
# індексу, який справді завантажений.
_EXAMPLE_ID = next(
    (uid for uid, p in _BY_ID.items()
     if profile.EXAMPLE_LABEL and profile.EXAMPLE_LABEL in p.label),
    next(iter(_BY_ID)))

# Форма пошуку — з фільтром версії чи без — задана профілем: схема інструмента
# без поля version для корпусу, де версій немає, не пропонує моделі аргумент,
# якого сервер не зміг би виконати.
SEARCH = search_versioned if profile.VERSIONS else search_spec
READ = read_section

_EXTRA = {
    "search": _LOADED,
    "read": f'Example identifier: "{_EXAMPLE_ID}".\n\n{_LOADED}',
}

TOOL_DESCRIPTIONS: dict[str, str] = {}

for _name, _fn, _key in ((profile.SEARCH_TOOL, SEARCH, "search"),
                         (profile.READ_TOOL, READ, "read")):
    TOOL_DESCRIPTIONS[_name] = profile.text(_key) + "\n\n" + _EXTRA[_key]
    mcp.tool(name=_name, description=TOOL_DESCRIPTIONS[_name])(_fn)


def _serve_port() -> int:
    """Порт HTTP-сервера: змінна DF_PORT як явне перекриття, інакше поле port
    із config.json примірника (його читає й перевіряє common/instance.py), як
    останній засіб — 8000. Так один і той самий примірник завжди на своєму
    порту, а різні примірники фабрики не б'ються за один."""
    env = os.environ.get("DF_PORT")
    if env and env.isdigit():
        return int(env)
    port = instance.config().get("port")
    return port if isinstance(port, int) else 8000


if __name__ == "__main__":
    # Без аргументів — stdio: клієнт (Mode A, Inspector) сам запускає цей процес
    # і говорить у труби. З --serve — довгий HTTP-сервер на порту примірника, до
    # якого Claude Code під'єднується за адресою. Захист однаковий в обох
    # транспортах: санітар видачі й вузький перелік інструментів живуть на
    # сервері, тож клієнт, який ми не контролюємо, дістає вже очищену відповідь.
    if "--serve" in sys.argv[1:]:
        _port = _serve_port()
        print(f"spec_mcp: HTTP-сервер на http://127.0.0.1:{_port}/mcp "
              f"(Ctrl+C спиняє)", file=sys.stderr)
        try:
            mcp.run(transport="streamable-http", host="127.0.0.1", port=_port)
        except KeyboardInterrupt:
            # Ctrl+C — штатна зупинка: uvicorn уже закрив сесії, тож traceback,
            # який anyio підіймає слідом, нічого не каже, окрім «зупинили».
            print("spec_mcp: сервер зупинено", file=sys.stderr)
    else:
        mcp.run()      # stdio: клієнт сам запускає цей процес і говорить у труби
