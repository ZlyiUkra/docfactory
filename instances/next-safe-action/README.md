# next-safe-action — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про next-safe-action — бібліотеку типобезпечних перевірених Server
Actions для Next.js (сайт next-safe-action.dev, репозиторій next-safe-action/next-safe-action, реєстр npm). Код спільний і
лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики —
у [../../README.md](../../README.md).

## Навіщо окремий примірник

Server Action у Next.js приймає що завгодно з браузера, і перевірку вводу, авторизацію та форму помилок кожна дія
пише сама. next-safe-action збирає це в клієнт дій (`createSafeActionClient`): схема вводу через Standard Schema (Zod,
Valibot та інші), middleware з контекстом (`use`, `next`, `ctx`), єдиний результат (`data`, `serverError`,
`validationErrors`) і хуки для клієнтських компонентів (`useAction`, `useOptimisticAction`). У плані Next.js
(фулстек-родина) — у розділі «знати, що існує», поряд із tRPC.

## Скільки цього

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| Сайт, README, адаптери | 359 | 43 | репозиторій, останній тег кожної мінорної 1.0–8.7 |
| Релізи GitHub | 203 | 196 | стабільні релізи пакета й адаптерів |
| Реєстр npm | 15 | — | чотири пакети |

Разом 577 записів паспорта; в індексі 522 документи й 1955 фрагментів (`expected_passages` у `checks.json`): однаковий
текст різних версій — один уривок із переліком версій. Замір `quality`: по словах 8 із 10, за змістом 7, разом 8, «як
модель» 10 із 10 з першого заміру.

Чому сайт береться з репозиторію. Сайт next-safe-action.dev зібрано з теки репозиторію, і кожен тег тримає сайт тієї
версії: з 4.0 — `packages/website/docs`, з 5.0 — `website/docs` (Docusaurus), з 8.3 — `apps/docs/content` (Fumadocs).
Береться останній тег кожної мінорної (43 теги 1.0–8.7); версії 1.0–3.4 сайту не мали, лише README (і `README_v2.md`,
`README_v3.md` у пакеті). Одне джерело з усіма тегами: однаковий файл різних тегів тягнеться й лежить один раз, а в
його версії лягають усі теги, де він був таким.

Чого немає. Код і тести пакета, застосунок playground, навички агентів `.agents/skills` (чужі: React, Next.js,
Turborepo), пререлізи (`-beta`, `-next`, `-alpha`, `-experimental`), Next.js, React, Zod, React Hook Form, TanStack Query
і Better Auth як окремі проєкти.

## Що в цій теці

- `corpus/` — паспорт `index.json`, тобто опис копії: адреса, дата завантаження й сума тексту кожного документа. Самих
  текстів тут немає: корпус в архіві (розділ «Архівний режим» нижче).
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`, розпакований
  `passages.json` лежить поруч і в git не потрапляє.
- `sources.json` — звідки корпус будується, і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.mcp.json` — запис HTTP-сервера для Claude Code. `ANTHROPIC_API_KEY` (лише для кроку `ask`) і `GITHUB_TOKEN` (лише
  для завантаження корпусу) беруться з кореневого `.env`.

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df next-safe-action <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сайт, README, адаптери | дерева 43 тегів (`vX.Y.Z`, з 8.x — `next-safe-action@X.Y.Z`): `apps/docs/content`, `website/docs`, `packages/website/docs`, README і журнали адаптерів | `ghdocs-history` |
| релізи | api.github.com, `/repos/next-safe-action/next-safe-action/releases`, без передрелізів | `ghreleases` |
| реєстр npm | `next-safe-action`, `@next-safe-action/adapter-react-hook-form`, `adapter-tanstack-query`, `adapter-better-auth` | `npm-versions` |

Нових читачів і полів не знадобилося. Репозиторій переїхав із `TheEdoRan/next-safe-action` до
`next-safe-action/next-safe-action`: стара адреса API відповідає редиректом на `repositories/<id>`, який білий список не
пропускає, тож у `sources.json` стоїть нова. Сторінки нинішнього сайту (`apps/docs/content/docs`) цитуються адресами
next-safe-action.dev (поле `site`), старші — файлами на GitHub. Релізам задано `skip: "\\d-(alpha|beta|next|rc|experimental)"`:
передрелізи без позначки на GitHub `stable: true` не відсіює, а простий `"-"` відкинув би й релізи адаптерів
(`@next-safe-action/adapter-react-hook-form@2.1.0`).

## Версії

Сторінки сайту, README й журнали несуть версію тегу, з якого взяті (`8.7.3`), релізи — версію релізу, реєстр — версію
пакета; фільтр `version` бере мажор (`"8"`), мінор (`"7.10"`) або точну версію (`"7.10.8"`). Адаптери мають свою
нумерацію (`adapter-react-hook-form` 1.x і 2.x). За завантаженнями `next-safe-action` у npm за тиждень до 26.10.2026 лінія
8 тримає 80 %, лінія 7 — 19 %, старші — 1 %, тож промпт відповідає для 8.x, а для коду на v7 чи старшій каже, що
змінилося.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку: у `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/next-safe-action-corpus-2026-10-26.tar.gz` (577 текстів, паспорт і сховище сирого
`raw/`; перед видаленням текстів розпакований окремо й звірений із диском) і в копії на Windows-диску
`C:\Distr\next-safe-action-corpus-2026-10-26.tar.gz` (звірено за SHA-256). В історії git текстів немає ніде.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/next-safe-action/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/next-safe-action-corpus-РРРР-ММ-ДД.tar.gz -C instances/next-safe-action corpus raw
find instances/next-safe-action/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/next-safe-action/raw
gzip -9 -c instances/next-safe-action/index/passages.json > instances/next-safe-action/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти й сховище — лише після того, як
архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із ними повертається й сховище `raw/`:

```
tar -xzf ~/archives/docfactory/next-safe-action-corpus-2026-10-26.tar.gz -C instances/next-safe-action
./df next-safe-action smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Дві
перевірки `smoke` чесно пропускаються («корпус в архіві»).

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/next-safe-action/index/passages.json.gz`,
далі `./df next-safe-action vectors` заллє колекцію Qdrant (секунди на відеокарті, кілька хвилин на процесорі).

## Установка venv

Власний venv цьому примірнику не потрібен: `./df next-safe-action …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md, розділ
«Спільне середовище».

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df next-safe-action sources --why   # перелік джерел і білий список
./df next-safe-action refresh         # завантажити все задеклароване (близько 6 хвилин)
./df next-safe-action manifest        # оновити паспорт
./df next-safe-action setup           # Qdrant чи пошук лише по словах
./df next-safe-action vectors         # залити корпус у docs-next-safe-action
./df next-safe-action smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df next-safe-action serve          # порт 8905
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8905/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user next-safe-action-docs http://127.0.0.1:8905/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `next-safe-action-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у [README
примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
