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
  prompts/      search.txt, read.txt — описи інструментів; loaded.txt — що
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
