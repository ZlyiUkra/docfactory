# github-actions — примірник фабрики docfactory

Тридцять четвертий примірник фабрики: захищений MCP-сервер, що відповідає на питання про GitHub Actions — CI/CD на
GitHub: синтаксис workflow, події, контексти й вирази, змінні й секрети, раннери, кеш і артефакти, environments і
деплой, OIDC, перевикористовувані workflow, власні дії, безпека. Поруч — GitHub Pages, GitHub Packages з Container
registry (ghcr.io), Dependabot для оновлення дій і ціни хвилин, а також README кожного мажору й нотатки релізів
офіційних дій і раннера. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає
самі дані домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо

CI стоїть у планах React, NestJS, Next.js і Docker: тести на кожен push, збирання образу, публікація в ghcr.io, деплой
у кластер. GitHub змінює Actions щороку: нові ключі синтаксису, права `GITHUB_TOKEN`, середовище виконання дій (Node 20
→ 24), а офіційні дії міняють мажори й параметри (`actions/checkout` уже v7, `upload-artifact` у v4 зламав спільні
артефакти). Відповідь з пам'яті тут застаріває найшвидше.

У яких фазах і днях планів навчання він потрібен — див. [../../docs/learning-map.md](../../docs/learning-map.md).

## Скільки цього

| Шар | Документів | Звідки |
|-----|-----------:|--------|
| GitHub Docs, розділ Actions: Get started, Concepts, How-tos, Tutorials, Reference | 245 | `content/actions` github/docs |
| GitHub Docs, розділ Pages | 28 | `content/pages` |
| GitHub Docs, розділ Packages з Container registry | 24 | `content/packages` |
| Dependabot: dependabot.yml, оновлення версій і дій, автоматизація з workflow | 14 | `content/code-security` |
| Ціни хвилин і раннерів; запити від імені GitHub App з workflow | 3 | `content/billing`, `content/apps` |
| README кожного мажору 21 дії (з теками `docs/`: advanced usage, міграції) | 131 | тег `v1`…`v9` кожної дії |
| Журнал змін `actions/checkout` | 1 | `CHANGELOG.md` |
| Нотатки релізів 21 дії | 946 | GitHub API |
| Нотатки релізів раннера `actions/runner` | 146 | GitHub API |

Дії: `actions/checkout`, `setup-node`, `setup-python`, `setup-go`, `setup-java`, `cache`, `upload-artifact`,
`download-artifact`, `github-script`, `configure-pages`, `upload-pages-artifact`, `deploy-pages`, `jekyll-build-pages`,
`attest-build-provenance`, `pnpm/action-setup`, `docker/login-action`, `build-push-action`, `setup-buildx-action`,
`setup-qemu-action`, `metadata-action`, `scout-action`.

Разом 1 538 документів; фрагментів в індексі — 8 362 (`expected_passages` у `checks.json`). Фрагменти — це шматки
документів між заголовками, по яких іде пошук; однаковий текст різних версій зливається в один з усіма версіями.

Замір `quality` на першому корпусі: перша десятка (питання своїми словами) — по словах 8 із 10, за змістом 8, разом 8;
друга, «як модель» (назви ключів і подій), — 10 із 10. `max_per_doc` заміряно з 0, 1, 2 і 3: найкраще 1, воно й стоїть.

**Версія у відповіді.** Сторінки GitHub Docs мають мітку «docs»: вони описують github.com як він є зараз, версій у них
немає. README дії несе номер мажору («4», «5», «7»), нотатки релізів — точну версію дії чи раннера («4.2.1»,
«2.328.0»), журнал змін — «changelog». Номери різних дій перетинаються, тож з фільтром версії дію треба називати й у
запиті. Без названого мажору відповідь — для найновішого README дії, із тим, з якого мажору щось змінилося.

## Що в цій теці

- `corpus/` — лише паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа (тексти — в архіві,
  див. нижче).
- `index/passages.json.gz` — стиснений кеш фрагментів, з якого підіймається сервер.
- `sources.json` — звідки корпус будується, і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — ключ Anthropic (лише для кроку `ask`) і токен GitHub (лише для завантаження); `.mcp.json` — запис
  HTTP-сервера для Claude Code.
- `.venv/` — власний venv примірника; `requirements.txt` — його склад.

Кроки нижче, окрім установки venv, запускаються з кореня фабрики (`docfactory/`) через `./df github-actions <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сторінки GitHub Docs | github/docs, гілка main | `github-docs` |
| README мажорів і журнал змін дій | репозиторії дій, теги `v1`…`v9` | `ghdocs-history` |
| нотатки релізів дій і раннера | GitHub API | `ghreleases` |

Білий список — два хости: `api.github.com` і `raw.githubusercontent.com`. Сам docs.github.com не читається: сайт
збирається з репозиторію github/docs. Посилання у відповідях ведуть на сайт.

Особливості, які варто знати:

- **Новий читач `github-docs`.** Сторінки GitHub Docs — шаблони Liquid: спільні абзаци (`{% data reusables… %}`),
  назви продуктів (`{% data variables… %}`), гілки для github.com і для GitHub Enterprise Server (`{% ifversion %}`),
  посилання `[AUTOTITLE](/шлях)`. Читач підставляє абзаци й назви, лишає гілку github.com, ставить назви сторінок у
  посилання, а приклади з `${{ … }}` у `{% raw %}` лишає як є. Сторінки, яких сайт для github.com не показує, не
  беруться (таких три). Сторінка-зміст без власного тексту дістає перелік назв дочірніх сторінок. Шапки й змінні — YAML,
  його розбирає PyYAML, що приходить разом із fastembed.
- **Теки `docs/` дій** беруться разом із README: `advanced-usage.md` у `setup-*` — це справжня документація кешу,
  приватних реєстрів і matrix версій. Службові `contributors.md`, `contributing.md`, `development.md` виключено.
- **Теги-мажори.** Дії тегують і точні версії (`v4.2.1`), і рухомий мажор (`v4`); README читається на мажорі — так
  дію й підключають. Читач `ghreleases` бере версію і з голого мажору (`v8` у `github-script`). Беты й тестові релізи
  (`v2-beta`, «Sample Release») пропускаються полем `skip`.

## Межі, про які треба пам'ятати

Тут немає GitHub Enterprise Server, REST і GraphQL API GitHub, самого Git, сторонніх дій поза списком, інших CI (GitLab
CI, Jenkins), а також Docker і Kubernetes як таких (окремі примірники `docker` і `kubernetes`). Розділи GitHub Docs
поза Actions, Pages, Packages і Dependabot (Codespaces, Copilot, організації) не взято.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку, як у express: у `corpus/` лежить лише паспорт `index.json`, а сервер
підіймається з кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає
повний текст кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/github-actions-corpus-2026-10-06.tar.gz` (1,1 МБ, 1 538 текстів і
паспорт; перед видаленням розпакований окремо й звірений із диском — нуль розбіжностей). В історії git текстів немає
ніде. Архів лежить лише на цій машині.

**Зайві точки — прибрати на першому ж оновленні.** У колекції `docs-github-actions` 8 455 точок на 8 362 фрагменти:
93 лишилися від службових файлів дій і бет, виключених уже після першої заливки. Пошук їх не показує, на відповіді
вони не впливають. Прибрати їх можна лише знесенням колекції й новим `vectors` (близько 20 хвилин) — разом із першим
оновленням документації.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/github-actions/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/github-actions-corpus-РРРР-ММ-ДД.tar.gz -C instances/github-actions corpus
find instances/github-actions/corpus -maxdepth 1 -name '*.txt' -delete
gzip -9 -c instances/github-actions/index/passages.json > instances/github-actions/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти — лише після того, як архів
звірено з диском.

**Як повернути тексти** — перед будь-яким оновленням корпусу:

```
tar -xzf ~/archives/docfactory/github-actions-corpus-РРРР-ММ-ДД.tar.gz -C instances/github-actions
./df github-actions smoke
```

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/github-actions/index/passages.json.gz`,
далі `./df github-actions vectors` заллє колекцію Qdrant (близько 20 хвилин).

## Установка venv

```
cd instances/github-actions
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

```
./df github-actions sources --why   # перелік джерел і білий список
./df github-actions refresh         # завантажити все задеклароване (~30 хвилин)
./df github-actions manifest        # оновити паспорт
./df github-actions setup           # Qdrant чи пошук лише по словах
./df github-actions vectors         # залити корпус у docs-github-actions (~20 хвилин)
./df github-actions smoke           # перевірки
```

Найдовша частина `refresh` — GitHub Docs: щоб знати, чи показує сайт сторінку на github.com, читач відкриває кожну
сторінку ще під час переліку, а потім дотягує спільні абзаци й змінні — сотні звернень з паузою в секунду. Без
`GITHUB_TOKEN` у `.env` анонімного ліміту GitHub API (60 звернень на годину) не вистачить на релізи. Обірваний
`refresh` продовжується з `--missing`.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd /mnt/c/Projects/fwdays/docfactory
./df github-actions serve           # порт 8794
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8794/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user github-actions-docs http://127.0.0.1:8794/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `github-actions-docs` і два інструменти `search_docs`, `read_section`. Якщо сесію
Claude Code відкрито раніше, ніж піднято сервер, вона покаже його як недоступний: у `/mcp` виберіть сервер і
«Reconnect».

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
