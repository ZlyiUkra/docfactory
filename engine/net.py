"""Звернення до мережі крізь білий список примірника.

Ніщо в ядрі не звертається до мережі повз цей модуль, і кожен виклик спершу
питає дозвіл (`allow(url)`): адреса поза оголошенням примірника не завантажується,
хоч би хто її підсунув. Той самий дозвіл питається і на кожному переході
редиректу — інакше оголошений хост відповідав би 302 і приводив тіло будь-якої
відхиленої адреси, зокрема й через зміну https на http. Обмеження ті самі, що
були в завантажувачах: лише https (це вже в `allow`), відповідь не більша за
`MAX_BYTES`, між зверненнями пауза, і є умовний запит «чи змінилося після нашої
дати».
"""

import datetime
import email.utils
import os
import pathlib
import urllib.error
import urllib.parse
import urllib.request

MAX_BYTES = 20_000_000
TIMEOUT_SEC = 60
PAUSE_SEC = 1.0
_UA = "agent0826-docfactory/1.0"
# Хост, і тільки він, отримує заголовок авторизації (див. _github_token).
_TOKEN_HOST = "api.github.com"


def _github_token() -> str:
    """Токен GitHub із `.env` того примірника, з яким іде цей запуск, або порожньо.

    Навіщо. Анонімний GitHub API дає 60 звернень на годину, а домен, що збирає
    документацію з вісімдесяти знімків репозиторію, витрачає одне звернення на
    кожен знімок і ще десятки на гортання релізів монорепозиторію. З токеном
    ліміт 5000, і збирання йде одним прогоном замість розкладу по годинних вікнах.

    Чому саме так, а не зі змінної оточення. Токен належить одному примірникові,
    і жоден інший не має права ним скористатися навіть випадково. Тому:

    - читається лише файл `.env` теки примірника, яку назвав `df` через
      DF_INSTANCE_DIR; оточення процесу не дивиться взагалі, тож глобальний
      GITHUB_TOKEN, якщо він колись зʼявиться в системі, нікуди не потрапить;
    - заголовок додається лише зверненням до api.github.com; на
      raw.githubusercontent.com, astro.build чи будь-який інший хост він не йде;
    - немає файла, немає рядка, немає теки примірника — немає й заголовка, і
      поведінка та сама до байта, що й до появи цієї функції. Примірники, у чиїх
      `.env` цього рядка немає, працюють рівно як раніше.

    Значення нікуди не друкується: ні в журнал, ні у звіт, ні в повідомлення збою.
    """
    root = os.environ.get("DF_INSTANCE_DIR", "")
    if not root:
        return ""
    try:
        text = (pathlib.Path(root) / ".env").read_text(encoding="utf-8")
    except OSError:
        return ""
    for line in text.splitlines():
        key, sep, value = line.partition("=")
        if sep and key.strip() == "GITHUB_TOKEN":
            return value.strip().strip('"').strip("'")
    return ""


class Refused(Exception):
    """Адреса не проходить білий список примірника."""


class _GuardedRedirects(urllib.request.HTTPRedirectHandler):
    """Редиректи крізь той самий білий список, що й перша адреса.

    Типовий обробник urllib мовчки йде по 301/302/303/307, тож дозвіл, спитаний
    до запиту, покривав лише перший перехід. Тут кожна нова адреса питає той
    самий `allow`; відмова — Refused, і тіло відхиленої адреси не читається.
    Схему переходу окремо перевіряти не треба: `allow` приймає лише https."""

    def __init__(self, allow):
        self._allow = allow

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not self._allow(newurl):
            raise Refused(
                f"редирект на адресу поза оголошенням примірника: {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def since_header(day: str) -> str:
    """Дата з шапки документа у вигляді, який розуміє If-Modified-Since."""
    when = datetime.datetime.strptime(day, "%Y-%m-%d").replace(
        tzinfo=datetime.timezone.utc)
    return email.utils.format_datetime(when, usegmt=True)


def fetch(url: str, allow, *, since: str = "") -> tuple[str, bytes]:
    """(код, байти). Код: «200», «304» або рядок «збій: …».

    `allow` — функція примірника: недозволена адреса не завантажується взагалі,
    підіймається Refused. `since` вмикає умовний запит: сервер відповість «304»,
    якщо документ не змінювався з тієї дати, і тіла не надішле.
    """
    if not allow(url):
        raise Refused(f"адреса поза оголошенням примірника: {url}")
    headers = {"User-Agent": _UA}
    token = _github_token()
    if token and urllib.parse.urlsplit(url).hostname == _TOKEN_HOST:
        headers["Authorization"] = f"Bearer {token}"
    if since:
        try:
            headers["If-Modified-Since"] = since_header(since)
        except ValueError:
            pass
    req = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener(_GuardedRedirects(allow))
    try:
        with opener.open(req, timeout=TIMEOUT_SEC) as resp:
            data = resp.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            return (f"збій: більше за {MAX_BYTES} байтів", b"")
        return ("200", data)
    except urllib.error.HTTPError as e:
        return ("304", b"") if e.code == 304 else (f"збій: HTTP {e.code}", b"")
    except urllib.error.URLError as e:
        return (f"збій: {e.reason}", b"")
