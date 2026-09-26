"""
СПІЛЬНЕ · профіль домену: усе, чим сервер одного домену відрізняється від сервера іншого.

Код сервера, агента й шарів спільний, а слова, якими він говорить з моделлю, — ні:
опис інструментів ECMAScript велить цитувати номер розділу специфікації, опис React —
казати, з якої версії щось з'явилося. Раніше ці слова стояли в коді, і другий домен
отримав би опис першого. Тепер вони лежать у теці примірника:

  config.json   server_name   ім'я MCP-сервера для клієнта
                doc_set       мітка набору в діагностиці
                sections      як ділити документ: "numbered" — рядки «20.1.3 Назва»
                              специфікації, "markdown" — заголовки «## Назва»
                versions      чи несуть документи версію і чи шукає пошук з фільтром
                tools         {"search": …, "read": …} — імена двох інструментів
                answer_hosts  домени, посилання на які шар 4 лишає у відповіді
                example_label слово з назви розділу, з якого береться приклад id
                fusion_depth  скільки місць кожного способу бачить злиття пошуку по
                              словах і за змістом; без поля — k виклику, як і було
  prompts/     search.txt, read.txt — описи інструментів; loaded.txt — що
                завантажено ({excerpts}, {documents}, {versions} підставляє
                сервер); agent.txt — системний промпт Mode A; refusal.txt — відмова
  checks.json   запити й очікування, якими smoke, check, raw і quality перевіряють
                саме цей корпус

Змовчання полів — ті, з якими сервер жив до появи профілю, тож примірник без поля
поводиться як раніше. Текстів за змовчанням немає навмисно: опис інструмента,
вгаданий за чужий домен, — рівно та впевнена вигадка, проти якої все зроблено.
"""

import json

from . import instance

_CONF = instance.config()
_TOOLS = _CONF.get("tools") or {}

SERVER_NAME = _CONF.get("server_name") or f"{instance.root().name}-docs"
SECTIONS = _CONF.get("sections") or "numbered"
VERSIONS = bool(_CONF.get("versions"))
SEARCH_TOOL = _TOOLS.get("search") or "search_spec"
READ_TOOL = _TOOLS.get("read") or "read_section"
ANSWER_HOSTS = tuple(_CONF.get("answer_hosts") or ())
EXAMPLE_LABEL = _CONF.get("example_label") or ""
# 0 означає «глибина = k», тобто поведінку до появи поля. Число вибирають за
# виміром quality примірника: у supabase плато 8–10 дає влучання і при k=5, і при
# k=3, а від 12 злиття вже губить розділ, перший в одному зі способів, — його
# перемагають сторінки, що є в обох списках хоч і далеко.
FUSION_DEPTH = int(_CONF.get("fusion_depth") or 0)
# Варіанти тієї самої сторінки для різних SDK (clerk: /docs/nextjs/…, /docs/vue/…).
# Вираз з однією групою — ім'я варіанта на початку імені документа; без поля
# варіантів немає, і видача та сама, що до його появи. Синоніми — як варіант
# називають у запиті («next.js» для nextjs); без них — саме ім'я, «-» як пробіл.
VARIANT_PATTERN = _CONF.get("variant_pattern") or ""
VARIANT_ALIASES = _CONF.get("variant_aliases") or {}
# Суворий відбір варіантів: коли запит називає варіант, фрагменти інших варіантів до
# видачі не допускаються зовсім. Без поля — лише згортання, як і раніше.
VARIANT_STRICT = bool(_CONF.get("variant_strict"))
# Розділ, чию назву-ідентифікатор (Object.freeze, SameValue, [[Get]]) запит містить
# дослівно, стає першим. Без поля — видача та сама, що й була.
TITLE_MATCH = bool(_CONF.get("title_match"))


def text(name: str) -> str:
    """Текст із prompts/<name>.txt примірника, без крайових пробілів."""
    path = instance.root() / "prompts" / f"{name}.txt"
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise SystemExit(f"Немає {path} ({exc}) — описи й промпти домену лежать у "
                         f"теці примірника, спільний код своїх не має.")


def checks() -> dict:
    """checks.json примірника: чим перевіряти саме цей корпус."""
    path = instance.root() / "checks.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SystemExit(f"{path}: не читається ({exc}) — перевірки корпусу домену "
                         f"лежать у теці примірника.")
