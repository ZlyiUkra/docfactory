# Creating a new documentation instance · Новий примірник документації · Criando uma nova instância

Three complete versions of the same guide. Pick your language:

- [English](#english)
- [Українська](#українська)
- [Português](#português)

---

<a name="english"></a>

# English

## What you end up with

A protected MCP server that answers questions about one body of documentation, from a local corpus, with four
protection layers. The shared code is never touched: a new domain adds one data folder under `instances/` and, only
if the target site needs it, one new reader under `engine/readers/`.

## Before you start

| Requirement | Why | Optional? |
|-------------|-----|-----------|
| bash (Linux, macOS or WSL on Windows) | `df` calls the Linux `.venv/bin/python`; a native Windows shell cannot run it | no |
| Python 3.10 or newer | the whole engine | no |
| Docker | meaning search (Qdrant); without it the server searches by words only | yes |
| Anthropic API key | only the `ask` step, the project's own agent | yes |

Everything except the first step runs from the repository root `docfactory/` as `./df <instance> <step>`.

## Anatomy of an instance

Fourteen files, identical in shape across `ecmascript` and `react`, plus three folders that create themselves.

| Path | What it holds | Who writes it |
|------|---------------|---------------|
| `config.json` | port, collection, embedding model, domain profile | you |
| `sources.json` | where to fetch from, and the whitelist that bounds the fetcher | **you, the main work** |
| `prompts/search.txt` | tool description the model reads before calling search | you |
| `prompts/read.txt` | tool description for reading one excerpt | you |
| `prompts/loaded.txt` | one line saying what is loaded; `{excerpts}`, `{documents}`, `{versions}` are filled in | you |
| `prompts/agent.txt` | system prompt for the project's own agent (`ask`) | you |
| `prompts/refusal.txt` | the text layer 1 returns when it blocks a request | you |
| `checks.json` | queries and expectations for `smoke`, `check`, `raw` and `quality` | you, after the first corpus |
| `requirements.txt` | the instance venv contents | copy, then trim |
| `.env.example` | key placeholder; never commit a real `.env` | copy |
| `.gitignore` | `.env`, `__pycache__/`, `*.pyc`, `.venv/`, `out/` | copy |
| `.mcp.json` | HTTP server record for Claude Code | copy, change the port |
| `README.md` | what this domain is and where its docs come from | you |
| `UPDATE.md` | how to refresh this corpus when upstream changes | you |
| `corpus/` | the downloaded documents plus `index.json`, the passport | `refresh`, `manifest` |
| `out/` | the search-mode decision, logs | `setup`, `serve` |
| `.venv/` | the instance's own virtual environment | step 1 |

## Step 1 · Folder and virtual environment

This is the only step performed from inside the instance folder. You never activate the venv: `df` calls the right
instance's `.venv/bin/python` itself.

```
mkdir -p instances/<domain>/prompts
cp instances/react/requirements.txt instances/react/.gitignore instances/react/.env.example instances/<domain>/
cd instances/<domain>
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cd ../..
```

**Known trap.** On some systems the packaged `python3` ships without the `venv` module. Use a Python that has it,
for example a conda interpreter: `/path/to/miniconda3/bin/python3 -m venv .venv`. Everything afterwards is
unaffected, because the venv is self-contained.

Trim `requirements.txt` to what the domain actually needs. `pypdf` belongs there only if some source is a PDF;
`fastembed` only if you want meaning search.

## Step 2 · `config.json`

```json
{
  "instance": "<domain>",
  "port": 8762,
  "collection": "docs-<domain>",
  "embed_model": "bge-small",
  "pause_sec": 5,
  "server_name": "<domain>-docs",
  "doc_set": "<domain>",
  "sections": "markdown",
  "versions": true,
  "tools": {"search": "search_docs", "read": "read_section"},
  "answer_hosts": ["example.com"],
  "example_label": "<a section name from your corpus>"
}
```

| Field | Meaning | Default if omitted |
|-------|---------|--------------------|
| `instance` | the folder name, for diagnostics | — |
| `port` | HTTP port of this server; integer 1–65535 | — |
| `collection` | Qdrant collection name | — |
| `embed_model` | embedding model key | — |
| `pause_sec` | seconds between requests to the same site while fetching | — |
| `server_name` | the name the MCP client shows | `<folder>-docs` |
| `doc_set` | set label in diagnostics and in the Qdrant collection name | `suite` |
| `sections` | `numbered` for documents with section numbers, `markdown` for `## Heading` sites | `numbered` |
| `versions` | whether documents carry a version and search accepts a version filter | `false` |
| `tools` | the two tool names the model sees | `search_spec`, `read_section` |
| `answer_hosts` | hosts whose links layer 4 leaves intact in an answer | empty |
| `example_label` | a word from a section name, used to build the example identifier | — |

**Ports in use today:** 8760 `ecmascript`, 8761 `react`. Take the next free one.

## Step 3 · `sources.json`

This is not a step, it is the work. Everything else is mechanical.

Find out how the target site serves its documentation, then decide whether one of the sixteen existing readers fits.
The whitelist principle is absolute: the updater fetches only what `sources.json` declares, and nothing else, ever.

```json
{
  "instance": "<domain>",
  "sources": [
    {
      "id": "docs-current",
      "url": "https://example.com/llms.txt",
      "reader": "llms",
      "version": "1.4",
      "within": ["https://example.com/docs/"],
      "title": "Example 1.4 documentation",
      "added": "2026-09-21",
      "note": "Why this source exists and what it covers."
    }
  ]
}
```

**Required fields:** `id`, `url`, `reader`. The URL must be `https`. Duplicate ids are rejected.

**Common optional fields**

| Field | Purpose |
|-------|---------|
| `within` | the only URL prefixes this source may reach; links outside it are skipped, not fetched |
| `version` | version carried into every document of this source; several may be given comma-separated |
| `frozen` | `true` means a snapshot that must never change; `check` reports any drift as an error |
| `title`, `label`, `note`, `added` | human metadata; `note` explains why the source exists |
| `pages` | extra page URLs alive on the site but missing from its menu |
| `index` | extra table-of-contents pages to harvest links from |
| `folders`, `root`, `recursive`, `files` | repository readers: which folders to take, what prefix to strip |
| `before` | blog readers: keep only posts older than this date |
| `keep_links` | keep URLs in the text; for a sitemap page where the links are the content |
| `expand`, `children`, `alt`, `meta` | specification readers: sub-page expansion and alternate titles |

### The sixteen readers

| Reader | Source shape |
|--------|--------------|
| `toc` | multi-page ecmarkup edition; chapter URLs taken from the table of contents |
| `page` | one ecmarkup page split into top-level sections |
| `pdf` | standards published only as PDF |
| `rfc` | RFC plain text; page furniture and the index are stripped |
| `report` | Unicode report HTML (UAX/UTS) with numbered headings |
| `ldml` | UTS #35 parts where the markup carries no section numbers |
| `llms` | `llms.txt` page list; each page fetched as its `.md` twin |
| `mdblog` | blog index HTML; posts fetched as markdown |
| `mdpage` | a single markdown page |
| `nextdata` | Next.js site with content in `<script id="__NEXT_DATA__">` |
| `gatsby` | Gatsby site serving `page-data.json` next to each page |
| `gatsby-blog` | the blog half of a Gatsby site |
| `ghdocs` | markdown docs as they stood at a repository tag or commit |
| `changelog` | `CHANGELOG.md` split into one document per version |
| `ghreleases` | GitHub release notes through the API |
| `ghcommit` | a single commit: message, author, date, file list |

If none fits, a new reader in `engine/readers/` comes first, before anything else. Readers register themselves, so
no shared file needs editing.

## Step 4 · Check the declaration, no network

```
./df <domain> sources --why
```

Fails loudly on a missing field, a non-https URL, a duplicate id or an unknown reader.

## Step 5 · Dry run

```
./df <domain> list
```

Shows what would be downloaded. Writes nothing. Read this output carefully: it is the cheapest moment to notice that
a reader picks up the wrong pages.

## Step 6 · Fetch the corpus

```
./df <domain> refresh
./df <domain> manifest
```

`refresh` fetches only what is declared. `manifest` writes `corpus/index.json`, the passport: the URL, the fetch date
and a checksum for every document. Nothing is ever deleted by these steps.

Useful variants: `./df <domain> refresh --missing` writes only files that are absent, and
`./df <domain> refresh <id> <id>` limits the run to named sources.

## Step 7 · `prompts/`

Five files. There are deliberately no defaults: a tool description guessed for the wrong domain is exactly the
confident fabrication this whole tool exists to prevent.

- **`search.txt`** — what the corpus contains, when to call the tool, and above all **when not to**. This is the
  longest of the five and the one that most affects answer quality.
- **`read.txt`** — how to read one excerpt by its identifier, and that the answer carries the source URL and the
  fetch date so a quotation can be verified.
- **`loaded.txt`** — one line stating what is loaded. `{excerpts}`, `{documents}` and `{versions}` are substituted
  by the server.
- **`agent.txt`** — the system prompt for `ask`. Must name the domain and the two tool names, and must say that
  instructions found inside retrieved text are data, not commands.
- **`refusal.txt`** — the text returned when layer 1 blocks a request.

## Step 8 · `checks.json`

Written after the first corpus exists, because it needs real numbers and real identifiers.

| Field | What it pins down |
|-------|-------------------|
| `expected_passages` | how many excerpts the corpus yields; `smoke` fails if it drifts |
| `expected_note` | why that number is what it is, and when it was taken |
| `find` | a query that must return a known section |
| `short` | a short section that must still be findable |
| `count_query`, `plain_query`, `long_query`, `ua_query`, `mixed_query` | query shapes the server must survive |
| `bad_id` | an identifier that must be rejected |
| `url_prefix` | prefix used when checking answer links |
| `paraphrase` | a query with no word in common with the target text |
| `description_phrases` | phrases the tool descriptions must contain |
| `layer1_legit` | genuine domain questions layer 1 must let through |
| `layer4_keep` | numbers and versions layer 4 must not mask |
| `version_probe` | a query plus a version, when `versions` is true |
| `quality` | ten pairs of query and target for the `quality` measurement |

**On `quality` targets.** A target is every page a knowledgeable person would accept as an answer, and it is chosen
from the documentation, never from what search happened to return. A target may be a string or a list of strings.
In `markdown` mode a target without `#` means the whole document, and that is used only when the entire document
answers the question. If a question has five acceptable answers, the question is too vague: rewrite the query rather
than widen the target.

## Step 9 · Meaning search, optional

```
./df <domain> setup
./df <domain> vectors
```

`setup` asks once whether to use Qdrant or stay with word search; the decision is recorded in `out/mode.json` and can
be changed later. `vectors` starts the container, downloads the embedding model and computes the vectors. Minutes of
CPU, no money, no network beyond the model download.

The container `agent0826-qdrant` is **shared** with other projects. Deleting collections is a human decision and no
step ever does it: `vectors` reports points whose text no longer exists and prints the command, nothing more.

## Step 10 · Verify

```
./df <domain> smoke       # checks past the protocol
./df <domain> protocol    # a dialogue over the protocol, foreign client
./df <domain> raw         # raw JSON-RPC frames, no library
./df <domain> tools       # MCP handshake, tool listing
./df <domain> quality     # measurement: what meaning search adds
```

`quality` is a measurement, not a check: it never fails. The absolute score is meaningless on its own; only the
comparison between the three columns on the same ten queries carries information.

## Step 11 · Serve and connect

```
./df <domain> serve
```

Leave it running in its own terminal. Then, once:

```
claude mcp add --transport http --scope user <server_name> http://127.0.0.1:<port>/mcp
```

In a Claude Code session, `/mcp` must list the server with its two tools.

## Step 12 · Document it

Write the instance `README.md` and `UPDATE.md`, then add the domain to the instance list in the root `README.md`.
`UPDATE.md` matters more than it looks: it is where you record how to take a snapshot before a version bump, and
what must never be deleted.

The instance `README.md` must spell out how to raise this very server — that is the point of the whole instance,
and it is the first thing looked up: the venv, `./df <domain> serve` with its port, both ways of registering it
in Claude Code (`.mcp.json` of this folder, or `claude mcp add --transport http --scope user`), the `/mcp` check,
and what a taken port and a failed connection look like. A domain list in the root README does not replace it.

## Final checklist

```
[ ] .venv built, dependencies installed
[ ] config.json: free port, own collection, profile filled in
[ ] sources.json: every source declared, whitelist bounded by `within`
[ ] ./df <domain> sources --why  passes
[ ] ./df <domain> list           looks right
[ ] corpus fetched, manifest written
[ ] prompts/: all five, none carrying another domain's words
[ ] checks.json: real numbers, targets chosen from documentation
[ ] smoke, protocol, raw, tools all green
[ ] README.md says how to raise the server and register it in Claude Code
[ ] README.md and UPDATE.md written; root README lists the domain
```

---

<a name="українська"></a>

# Українська

## Що виходить у кінці

Захищений MCP-сервер, який відповідає на питання про один корпус документації, з локальних файлів, за чотирма
шарами захисту. Спільний код при цьому не чіпається: новий домен додає одну теку даних в `instances/` і, лише якщо
цього вимагає цільовий сайт, один новий читач в `engine/readers/`.

## Передумови

| Потрібно | Навіщо | Обов'язково? |
|----------|--------|--------------|
| bash (Linux, macOS або WSL на Windows) | `df` кличе лінуксовий `.venv/bin/python`; з нативного Windows-шелу не піде | так |
| Python 3.10 або новіший | увесь рушій | так |
| Docker | пошук за змістом (Qdrant); без нього сервер шукає лише по словах | ні |
| Ключ Anthropic | лише крок `ask`, власний агент проєкту | ні |

Усе, крім першого кроку, біжить із кореня `docfactory/` через `./df <примірник> <крок>`.

## З чого складається примірник

Чотирнадцять файлів, однакових за складом у `ecmascript` і `react`, плюс три теки, що створюються самі.

| Шлях | Що тримає | Хто пише |
|------|-----------|----------|
| `config.json` | порт, колекція, модель векторів, профіль домену | ви |
| `sources.json` | звідки тягнути, і водночас білий список для оновлювача | **ви, головна робота** |
| `prompts/search.txt` | опис інструмента пошуку, який читає модель | ви |
| `prompts/read.txt` | опис інструмента читання одного фрагмента | ви |
| `prompts/loaded.txt` | рядок про те, що завантажено; `{excerpts}`, `{documents}`, `{versions}` підставляє сервер | ви |
| `prompts/agent.txt` | системний промпт власного агента (`ask`) | ви |
| `prompts/refusal.txt` | текст, який шар 1 повертає, коли блокує запит | ви |
| `checks.json` | запити й очікування для `smoke`, `check`, `raw` і `quality` | ви, після першого корпусу |
| `requirements.txt` | склад venv примірника | копія, потім підрізати |
| `.env.example` | заготовка для ключа; справжній `.env` у git не потрапляє ніколи | копія |
| `.gitignore` | `.env`, `__pycache__/`, `*.pyc`, `.venv/`, `out/` | копія |
| `.mcp.json` | запис HTTP-сервера для Claude Code | копія, змінити порт |
| `README.md` | що це за домен і звідки береться його документація | ви |
| `UPDATE.md` | як оновлювати корпус, коли нагорі щось змінилося | ви |
| `corpus/` | завантажені документи плюс `index.json`, паспорт | `refresh`, `manifest` |
| `out/` | рішення про спосіб пошуку, журнали | `setup`, `serve` |
| `.venv/` | власне віртуальне середовище примірника | крок 1 |

## Крок 1 · Тека і venv

Це єдиний крок, що робиться зсередини теки примірника. Venv активувати не треба ніколи: `df` сам викликає
`.venv/bin/python` потрібного примірника.

```
mkdir -p instances/<домен>/prompts
cp instances/react/requirements.txt instances/react/.gitignore instances/react/.env.example instances/<домен>/
cd instances/<домен>
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cd ../..
```

**Відома пастка.** На деяких системах пакетний `python3` іде без модуля `venv`. Тоді беріть інтерпретатор, у якого
він є, наприклад conda: `/шлях/до/miniconda3/bin/python3 -m venv .venv`. На все подальше це не впливає, бо venv
самодостатній.

`requirements.txt` підріжте під домен. `pypdf` потрібен, лише якщо якесь джерело видається PDF-ом; `fastembed` —
лише якщо потрібен пошук за змістом.

## Крок 2 · `config.json`

```json
{
  "instance": "<домен>",
  "port": 8762,
  "collection": "docs-<домен>",
  "embed_model": "bge-small",
  "pause_sec": 5,
  "server_name": "<домен>-docs",
  "doc_set": "<домен>",
  "sections": "markdown",
  "versions": true,
  "tools": {"search": "search_docs", "read": "read_section"},
  "answer_hosts": ["example.com"],
  "example_label": "<слово з назви розділу вашого корпусу>"
}
```

| Поле | Що означає | Змовчання |
|------|------------|-----------|
| `instance` | ім'я теки, для діагностики | — |
| `port` | HTTP-порт цього сервера; ціле 1–65535 | — |
| `collection` | ім'я колекції Qdrant | — |
| `embed_model` | ключ моделі векторів | — |
| `pause_sec` | пауза в секундах між зверненнями до того самого сайту | — |
| `server_name` | ім'я, яке бачить MCP-клієнт | `<тека>-docs` |
| `doc_set` | мітка набору в діагностиці й в імені колекції | `suite` |
| `sections` | `numbered` для документів із номерами розділів, `markdown` для сайтів із `## Заголовок` | `numbered` |
| `versions` | чи несуть документи версію і чи приймає пошук фільтр версії | `false` |
| `tools` | два імені інструментів, які бачить модель | `search_spec`, `read_section` |
| `answer_hosts` | домени, посилання на які шар 4 лишає у відповіді | порожньо |
| `example_label` | слово з назви розділу, з якого будується приклад ідентифікатора | — |

**Зайняті порти:** 8760 `ecmascript`, 8761 `react`. Беріть наступний вільний.

## Крок 3 · `sources.json`

Це не крок, це робота. Усе інше механічне.

Треба з'ясувати, як цільовий сайт віддає документацію, і вирішити, чи підходить котрийсь із шістнадцяти наявних
читачів. Принцип білого списку непорушний: оновлювач тягне рівно те, що оголошено в `sources.json`, і нічого більше.

```json
{
  "instance": "<домен>",
  "sources": [
    {
      "id": "docs-current",
      "url": "https://example.com/llms.txt",
      "reader": "llms",
      "version": "1.4",
      "within": ["https://example.com/docs/"],
      "title": "Документація Example 1.4",
      "added": "2026-09-21",
      "note": "Навіщо це джерело і що воно покриває."
    }
  ]
}
```

**Обов'язкові поля:** `id`, `url`, `reader`. Адреса мусить бути `https`. Повторений `id` відхиляється.

**Поширені необов'язкові поля**

| Поле | Навіщо |
|------|--------|
| `within` | єдині префікси адрес, куди цьому джерелу можна; посилання поза ними пропускаються, а не тягнуться |
| `version` | версія, яку несе кожен документ джерела; кілька — через кому |
| `frozen` | `true` означає знімок, який не має мінятися; `check` рахує будь-який зсув помилкою |
| `title`, `label`, `note`, `added` | людські дані; `note` пояснює, навіщо джерело існує |
| `pages` | адреси сторінок, живих на сайті, але прибраних із меню |
| `index` | додаткові сторінки-змісти, з яких беруться посилання |
| `folders`, `root`, `recursive`, `files` | читачі репозиторію: які теки брати, який префікс знімати |
| `before` | читачі блогу: лишити лише записи, старші за цю дату |
| `keep_links` | лишити адреси в тексті; для сторінки-мапи, де посилання і є змістом |
| `expand`, `children`, `alt`, `meta` | читачі специфікацій: розгортання підсторінок і запасні назви |

### Шістнадцять читачів

| Читач | Форма джерела |
|-------|---------------|
| `toc` | багатосторінкове видання ecmarkup; адреси глав беруться зі змісту |
| `page` | одна сторінка ecmarkup, поділена на верхні розділи |
| `pdf` | стандарти, які видають лише PDF-ом |
| `rfc` | текст RFC; колонтитули й кінцевий покажчик прибираються |
| `report` | HTML звіту Unicode (UAX/UTS) з номерами в заголовках |
| `ldml` | частини UTS #35, де в розмітці номерів розділів немає |
| `llms` | перелік сторінок у форматі `llms.txt`; текст кожної — її markdown-двійник |
| `mdblog` | сторінка-перелік блогу; записи беруться markdown-ом |
| `mdpage` | одна markdown-сторінка |
| `nextdata` | сайт на Next.js, де вміст лежить у `<script id="__NEXT_DATA__">` |
| `gatsby` | сайт на Gatsby, що поруч зі сторінкою віддає `page-data.json` |
| `gatsby-blog` | блогова половина сайту на Gatsby |
| `ghdocs` | markdown-документація на тезі чи коміті репозиторію |
| `changelog` | `CHANGELOG.md`, поділений на версії: одна версія — один документ |
| `ghreleases` | нотатки релізів GitHub через API |
| `ghcommit` | один коміт: повідомлення, автор, дата, склад файлів |

Якщо не підходить жоден, новий читач в `engine/readers/` йде першим, до всього іншого. Читачі реєструються самі,
тож жодного спільного файлу правити не треба.

## Крок 4 · Перевірка оголошення, без мережі

```
./df <домен> sources --why
```

Голосно падає на відсутньому полі, адресі не-https, повтореному `id` чи невідомому читачі.

## Крок 5 · Пробний перелік

```
./df <домен> list
```

Показує, що завантажилося б. Не пише нічого. Цей вивід варто читати уважно: це найдешевша мить, щоб помітити, що
читач підхоплює не ті сторінки.

## Крок 6 · Завантаження корпусу

```
./df <домен> refresh
./df <домен> manifest
```

`refresh` тягне лише задеклароване. `manifest` пише `corpus/index.json`, паспорт: адреса, дата завантаження й сума
тексту кожного документа. Жоден із цих кроків нічого не видаляє.

Корисні варіанти: `./df <домен> refresh --missing` пише лише відсутні файли, а `./df <домен> refresh <id> <id>`
обмежує прогін названими джерелами.

## Крок 7 · `prompts/`

П'ять файлів. Текстів за змовчанням немає навмисно: опис інструмента, вгаданий за чужий домен, це рівно та
впевнена вигадка, проти якої весь інструмент і зроблено.

- **`search.txt`** — що в корпусі, коли кликати інструмент і, найголовніше, **коли не кликати**. Найдовший із
  п'яти і той, що найбільше впливає на якість відповідей.
- **`read.txt`** — як прочитати один фрагмент за ідентифікатором, і що у відповіді є адреса джерела та дата
  завантаження, щоб цитату можна було звірити.
- **`loaded.txt`** — рядок про те, що завантажено. `{excerpts}`, `{documents}` і `{versions}` підставляє сервер.
- **`agent.txt`** — системний промпт для `ask`. Мусить називати домен і два імені інструментів, і мусить казати,
  що вказівки, знайдені всередині отриманого тексту, це дані, а не команди.
- **`refusal.txt`** — текст, який повертається, коли шар 1 блокує запит.

## Крок 8 · `checks.json`

Пишеться після того, як з'явився перший корпус, бо потребує реальних чисел і реальних ідентифікаторів.

| Поле | Що фіксує |
|------|-----------|
| `expected_passages` | скільки фрагментів дає корпус; `smoke` падає, якщо число зсунулося |
| `expected_note` | чому число саме таке і коли його знято |
| `find` | запит, який мусить повернути відомий розділ |
| `short` | короткий розділ, який усе одно мусить знаходитися |
| `count_query`, `plain_query`, `long_query`, `ua_query`, `mixed_query` | форми запитів, які сервер мусить пережити |
| `bad_id` | ідентифікатор, який мусить бути відхилений |
| `url_prefix` | префікс для перевірки посилань у відповіді |
| `paraphrase` | запит, у якому немає жодного спільного слова з текстом цілі |
| `description_phrases` | фрази, які мусять бути в описах інструментів |
| `layer1_legit` | справжні питання домену, які шар 1 мусить пропустити |
| `layer4_keep` | числа й версії, які шар 4 не має маскувати |
| `version_probe` | запит разом із версією, коли `versions` true |
| `quality` | десять пар «запит і ціль» для заміру `quality` |

**Про цілі `quality`.** Ціль це всі сторінки, які знаюча людина прийняла б як відповідь, і добирається вона з
документації, а не з того, що знайшов пошук. Ціль може бути рядком або списком рядків. У режимі `markdown` ціль без
`#` означає документ цілком, і так називають лише документ, що весь про це питання. Якщо у питання виходить п'ять
правильних відповідей, розмите питання: переписують запит, а не розширюють ціль.

## Крок 9 · Пошук за змістом, необов'язково

```
./df <домен> setup
./df <домен> vectors
```

`setup` питає один раз, брати Qdrant чи лишитися на пошуку по словах; рішення пишеться в `out/mode.json` і його
можна передумати. `vectors` підіймає контейнер, довантажує модель і рахує вектори. Хвилини процесора, без грошей і
без мережі, окрім завантаження самої моделі.

Контейнер `agent0826-qdrant` **спільний** з іншими проєктами. Видалення колекцій це рішення людини, і жоден крок
його не робить: `vectors` повідомляє про точки, чий текст уже зник, і друкує команду, не більше.

## Крок 10 · Перевірки

```
./df <домен> smoke       # перевірки повз протокол
./df <домен> protocol    # діалог по протоколу, чужим клієнтом
./df <домен> raw         # сирі кадри JSON-RPC, без бібліотеки
./df <домен> tools       # рукостискання MCP, перелік інструментів
./df <домен> quality     # замір: що додає пошук за змістом
```

`quality` це замір, а не перевірка: він ніколи не падає. Абсолютне число саме по собі нічого не означає; сенс має
лише порівняння трьох стовпців на одній і тій самій десятці запитів.

## Крок 11 · Підняти сервер і під'єднати

```
./df <домен> serve
```

Лишіть жити в окремому терміналі. Далі, один раз:

```
claude mcp add --transport http --scope user <server_name> http://127.0.0.1:<порт>/mcp
```

У сесії Claude Code команда `/mcp` має показати сервер із двома інструментами.

## Крок 12 · Описати

Напишіть `README.md` і `UPDATE.md` примірника, далі додайте домен у перелік примірників кореневого `README.md`.
`UPDATE.md` важливіший, ніж здається: саме там записується, як зробити знімок перед підняттям версії і що не можна
видаляти ніколи.

У `README.md` примірника **обов'язково** має бути, як підняти саме цей сервер: заради нього примірник і робиться,
і шукають це першим. Тобто venv, `./df <домен> serve` із номером порту, обидва способи запису в Claude Code
(`.mcp.json` цієї теки або `claude mcp add --transport http --scope user`), перевірка через `/mcp` і те, який
вигляд має зайнятий порт і невдале під'єднання. Перелік доменів у кореневому README цього не замінює: там опис
фабрики, а не інструкція.

## Підсумковий список

```
[ ] .venv піднято, залежності встановлено
[ ] config.json: вільний порт, власна колекція, профіль заповнено
[ ] sources.json: усі джерела оголошено, білий список обмежено через `within`
[ ] ./df <домен> sources --why  проходить
[ ] ./df <домен> list           виглядає правильно
[ ] корпус завантажено, паспорт записано
[ ] prompts/: усі п'ять, у жодному немає слів чужого домену
[ ] checks.json: справжні числа, цілі дібрані з документації
[ ] smoke, protocol, raw, tools зелені
[ ] README.md каже, як підняти сервер і записати його в Claude Code
[ ] README.md і UPDATE.md написані; кореневий README називає домен
```

---

<a name="português"></a>

# Português

## O que você obtém no final

Um servidor MCP protegido que responde perguntas sobre um corpo de documentação, a partir de um corpus local, com
quatro camadas de proteção. O código compartilhado nunca é alterado: um novo domínio acrescenta uma pasta de dados
em `instances/` e, somente se o site de destino exigir, um novo leitor em `engine/readers/`.

## Pré-requisitos

| Necessário | Para quê | Obrigatório? |
|------------|----------|--------------|
| bash (Linux, macOS ou WSL no Windows) | `df` chama o `.venv/bin/python` do Linux; um shell nativo do Windows não roda | sim |
| Python 3.10 ou mais recente | todo o motor | sim |
| Docker | busca por significado (Qdrant); sem ele o servidor busca apenas por palavras | não |
| Chave da Anthropic | apenas o passo `ask`, o agente próprio do projeto | não |

Tudo, exceto o primeiro passo, roda a partir da raiz `docfactory/` como `./df <instância> <passo>`.

## Anatomia de uma instância

Quatorze arquivos, com a mesma composição em `ecmascript` e `react`, mais três pastas que se criam sozinhas.

| Caminho | O que contém | Quem escreve |
|---------|--------------|--------------|
| `config.json` | porta, coleção, modelo de vetores, perfil do domínio | você |
| `sources.json` | de onde buscar, e ao mesmo tempo a lista branca do atualizador | **você, o trabalho principal** |
| `prompts/search.txt` | descrição da ferramenta de busca que o modelo lê | você |
| `prompts/read.txt` | descrição da ferramenta que lê um trecho | você |
| `prompts/loaded.txt` | uma linha dizendo o que está carregado; `{excerpts}`, `{documents}`, `{versions}` são preenchidos | você |
| `prompts/agent.txt` | prompt de sistema do agente próprio (`ask`) | você |
| `prompts/refusal.txt` | texto que a camada 1 devolve ao bloquear um pedido | você |
| `checks.json` | consultas e expectativas de `smoke`, `check`, `raw` e `quality` | você, após o primeiro corpus |
| `requirements.txt` | conteúdo do venv da instância | copiar e depois enxugar |
| `.env.example` | modelo para a chave; um `.env` real nunca vai para o git | cópia |
| `.gitignore` | `.env`, `__pycache__/`, `*.pyc`, `.venv/`, `out/` | cópia |
| `.mcp.json` | registro do servidor HTTP para o Claude Code | cópia, trocar a porta |
| `README.md` | o que é este domínio e de onde vem sua documentação | você |
| `UPDATE.md` | como atualizar o corpus quando a origem mudar | você |
| `corpus/` | documentos baixados mais `index.json`, o passaporte | `refresh`, `manifest` |
| `out/` | a decisão sobre o modo de busca, logs | `setup`, `serve` |
| `.venv/` | ambiente virtual próprio da instância | passo 1 |

## Passo 1 · Pasta e ambiente virtual

É o único passo executado de dentro da pasta da instância. Nunca é preciso ativar o venv: o `df` chama sozinho o
`.venv/bin/python` da instância certa.

```
mkdir -p instances/<domínio>/prompts
cp instances/react/requirements.txt instances/react/.gitignore instances/react/.env.example instances/<domínio>/
cd instances/<domínio>
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cd ../..
```

**Armadilha conhecida.** Em alguns sistemas o `python3` do pacote vem sem o módulo `venv`. Use um interpretador que
o tenha, por exemplo o do conda: `/caminho/para/miniconda3/bin/python3 -m venv .venv`. Isso não afeta nada depois,
porque o venv é autocontido.

Enxugue o `requirements.txt` conforme o domínio. `pypdf` só é necessário se alguma fonte for PDF; `fastembed` só se
você quiser busca por significado.

## Passo 2 · `config.json`

```json
{
  "instance": "<domínio>",
  "port": 8762,
  "collection": "docs-<domínio>",
  "embed_model": "bge-small",
  "pause_sec": 5,
  "server_name": "<domínio>-docs",
  "doc_set": "<domínio>",
  "sections": "markdown",
  "versions": true,
  "tools": {"search": "search_docs", "read": "read_section"},
  "answer_hosts": ["example.com"],
  "example_label": "<uma palavra do nome de uma seção do seu corpus>"
}
```

| Campo | Significado | Padrão se omitido |
|-------|-------------|-------------------|
| `instance` | nome da pasta, para diagnóstico | — |
| `port` | porta HTTP deste servidor; inteiro de 1 a 65535 | — |
| `collection` | nome da coleção no Qdrant | — |
| `embed_model` | chave do modelo de vetores | — |
| `pause_sec` | pausa em segundos entre requisições ao mesmo site | — |
| `server_name` | nome que o cliente MCP exibe | `<pasta>-docs` |
| `doc_set` | rótulo do conjunto no diagnóstico e no nome da coleção | `suite` |
| `sections` | `numbered` para documentos com seções numeradas, `markdown` para sites com `## Título` | `numbered` |
| `versions` | se os documentos carregam versão e se a busca aceita filtro de versão | `false` |
| `tools` | os dois nomes de ferramentas que o modelo vê | `search_spec`, `read_section` |
| `answer_hosts` | domínios cujos links a camada 4 mantém na resposta | vazio |
| `example_label` | palavra do nome de uma seção, usada para montar o identificador de exemplo | — |

**Portas já usadas:** 8760 `ecmascript`, 8761 `react`. Pegue a próxima livre.

## Passo 3 · `sources.json`

Isto não é um passo, é o trabalho. Todo o resto é mecânico.

É preciso descobrir como o site de destino entrega a documentação e decidir se algum dos dezesseis leitores
existentes serve. O princípio da lista branca é inviolável: o atualizador busca exatamente o que está declarado em
`sources.json`, e nada mais.

```json
{
  "instance": "<domínio>",
  "sources": [
    {
      "id": "docs-current",
      "url": "https://example.com/llms.txt",
      "reader": "llms",
      "version": "1.4",
      "within": ["https://example.com/docs/"],
      "title": "Documentação Example 1.4",
      "added": "2026-09-21",
      "note": "Por que esta fonte existe e o que ela cobre."
    }
  ]
}
```

**Campos obrigatórios:** `id`, `url`, `reader`. O endereço precisa ser `https`. `id` repetido é rejeitado.

**Campos opcionais mais usados**

| Campo | Para quê |
|-------|----------|
| `within` | os únicos prefixos de endereço que esta fonte pode alcançar; links fora deles são ignorados, não baixados |
| `version` | versão que cada documento da fonte carrega; várias, separadas por vírgula |
| `frozen` | `true` indica um instantâneo que não deve mudar; `check` trata qualquer desvio como erro |
| `title`, `label`, `note`, `added` | dados para humanos; `note` explica por que a fonte existe |
| `pages` | endereços de páginas vivas no site, porém removidas do menu |
| `index` | páginas de sumário adicionais das quais extrair links |
| `folders`, `root`, `recursive`, `files` | leitores de repositório: quais pastas pegar, qual prefixo remover |
| `before` | leitores de blog: manter apenas posts anteriores a esta data |
| `keep_links` | manter endereços no texto; para uma página-mapa em que os links são o conteúdo |
| `expand`, `children`, `alt`, `meta` | leitores de especificação: expansão de subpáginas e títulos alternativos |

### Os dezesseis leitores

| Leitor | Formato da fonte |
|--------|------------------|
| `toc` | edição ecmarkup em várias páginas; endereços dos capítulos vêm do sumário |
| `page` | uma página ecmarkup dividida em seções de primeiro nível |
| `pdf` | normas publicadas apenas em PDF |
| `rfc` | texto puro de RFC; cabeçalhos de página e índice final são removidos |
| `report` | HTML de relatório Unicode (UAX/UTS) com números nos títulos |
| `ldml` | partes do UTS #35 em que a marcação não traz números de seção |
| `llms` | lista de páginas no formato `llms.txt`; cada página vem do seu gêmeo `.md` |
| `mdblog` | página-índice de blog; os posts vêm em markdown |
| `mdpage` | uma única página markdown |
| `nextdata` | site Next.js com o conteúdo em `<script id="__NEXT_DATA__">` |
| `gatsby` | site Gatsby que serve `page-data.json` ao lado de cada página |
| `gatsby-blog` | a metade de blog de um site Gatsby |
| `ghdocs` | documentação markdown como estava em uma tag ou commit do repositório |
| `changelog` | `CHANGELOG.md` dividido por versão: uma versão, um documento |
| `ghreleases` | notas de release do GitHub via API |
| `ghcommit` | um commit: mensagem, autor, data, lista de arquivos |

Se nenhum servir, um novo leitor em `engine/readers/` vem primeiro, antes de tudo. Os leitores se registram
sozinhos, então nenhum arquivo compartilhado precisa ser alterado.

## Passo 4 · Conferir a declaração, sem rede

```
./df <domínio> sources --why
```

Falha em voz alta diante de campo ausente, endereço que não seja https, `id` repetido ou leitor desconhecido.

## Passo 5 · Ensaio

```
./df <domínio> list
```

Mostra o que seria baixado. Não escreve nada. Leia esta saída com atenção: é o momento mais barato para notar que um
leitor está pegando as páginas erradas.

## Passo 6 · Baixar o corpus

```
./df <domínio> refresh
./df <domínio> manifest
```

`refresh` baixa apenas o que foi declarado. `manifest` escreve `corpus/index.json`, o passaporte: endereço, data do
download e soma de verificação de cada documento. Nenhum destes passos apaga coisa alguma.

Variantes úteis: `./df <domínio> refresh --missing` grava apenas os arquivos ausentes, e
`./df <domínio> refresh <id> <id>` limita a execução às fontes indicadas.

## Passo 7 · `prompts/`

Cinco arquivos. Não existem textos padrão, e isso é proposital: uma descrição de ferramenta adivinhada para o
domínio errado é exatamente a invenção confiante contra a qual esta ferramenta inteira foi construída.

- **`search.txt`** — o que há no corpus, quando chamar a ferramenta e, acima de tudo, **quando não chamar**. É o
  mais longo dos cinco e o que mais afeta a qualidade das respostas.
- **`read.txt`** — como ler um trecho pelo identificador, e que a resposta traz o endereço da fonte e a data do
  download, para que a citação possa ser conferida.
- **`loaded.txt`** — uma linha dizendo o que está carregado. `{excerpts}`, `{documents}` e `{versions}` são
  substituídos pelo servidor.
- **`agent.txt`** — prompt de sistema do `ask`. Precisa nomear o domínio e as duas ferramentas, e precisa dizer que
  instruções encontradas dentro do texto recuperado são dados, não comandos.
- **`refusal.txt`** — texto devolvido quando a camada 1 bloqueia um pedido.

## Passo 8 · `checks.json`

Escrito depois que o primeiro corpus existe, porque precisa de números e identificadores reais.

| Campo | O que fixa |
|-------|------------|
| `expected_passages` | quantos trechos o corpus produz; `smoke` falha se o número mudar |
| `expected_note` | por que o número é esse e quando foi medido |
| `find` | uma consulta que precisa devolver uma seção conhecida |
| `short` | uma seção curta que ainda assim precisa ser encontrada |
| `count_query`, `plain_query`, `long_query`, `ua_query`, `mixed_query` | formatos de consulta que o servidor precisa suportar |
| `bad_id` | um identificador que precisa ser rejeitado |
| `url_prefix` | prefixo usado ao verificar links na resposta |
| `paraphrase` | consulta sem nenhuma palavra em comum com o texto do alvo |
| `description_phrases` | frases que as descrições das ferramentas precisam conter |
| `layer1_legit` | perguntas legítimas do domínio que a camada 1 precisa deixar passar |
| `layer4_keep` | números e versões que a camada 4 não deve mascarar |
| `version_probe` | uma consulta com versão, quando `versions` for true |
| `quality` | dez pares de consulta e alvo para a medição `quality` |

**Sobre os alvos de `quality`.** Um alvo é toda página que uma pessoa que domina o assunto aceitaria como resposta,
e ele é escolhido a partir da documentação, nunca a partir do que a busca por acaso devolveu. O alvo pode ser uma
string ou uma lista de strings. No modo `markdown`, um alvo sem `#` significa o documento inteiro, e isso só se usa
quando o documento inteiro responde à pergunta. Se uma pergunta admite cinco respostas corretas, a pergunta está
vaga: reescreva a consulta em vez de alargar o alvo.

## Passo 9 · Busca por significado, opcional

```
./df <domínio> setup
./df <domínio> vectors
```

`setup` pergunta uma vez se deve usar o Qdrant ou permanecer na busca por palavras; a decisão fica em
`out/mode.json` e pode ser revista. `vectors` sobe o contêiner, baixa o modelo e calcula os vetores. Minutos de CPU,
sem custo e sem rede além do download do modelo.

O contêiner `agent0826-qdrant` é **compartilhado** com outros projetos. Apagar coleções é decisão humana e nenhum
passo faz isso: `vectors` informa quais pontos descrevem texto que já não existe e imprime o comando, nada além.

## Passo 10 · Verificar

```
./df <domínio> smoke       # verificações fora do protocolo
./df <domínio> protocol    # diálogo pelo protocolo, cliente externo
./df <domínio> raw         # quadros JSON-RPC crus, sem biblioteca
./df <domínio> tools       # handshake MCP, listagem de ferramentas
./df <domínio> quality     # medição: o que a busca por significado acrescenta
```

`quality` é uma medição, não uma verificação: nunca falha. O número absoluto nada significa sozinho; só a comparação
entre as três colunas sobre as mesmas dez consultas carrega informação.

## Passo 11 · Subir e conectar

```
./df <domínio> serve
```

Deixe rodando em um terminal próprio. Depois, uma única vez:

```
claude mcp add --transport http --scope user <server_name> http://127.0.0.1:<porta>/mcp
```

Em uma sessão do Claude Code, `/mcp` precisa listar o servidor com suas duas ferramentas.

## Passo 12 · Documentar

Escreva o `README.md` e o `UPDATE.md` da instância e acrescente o domínio à lista de instâncias do `README.md` da
raiz. O `UPDATE.md` importa mais do que parece: é nele que se registra como tirar um instantâneo antes de subir uma
versão e o que nunca deve ser apagado.

O `README.md` da instância precisa dizer como subir este servidor — é para isso que a instância existe, e é a
primeira coisa que se procura: o venv, `./df <domínio> serve` com a porta, as duas formas de registrá-lo no Claude
Code (o `.mcp.json` desta pasta ou `claude mcp add --transport http --scope user`), a conferência pelo `/mcp` e o
que aparece quando a porta está ocupada ou a conexão falha. A lista de domínios no README da raiz não substitui
isso.

## Lista final de conferência

```
[ ] .venv criado, dependências instaladas
[ ] config.json: porta livre, coleção própria, perfil preenchido
[ ] sources.json: todas as fontes declaradas, lista branca limitada por `within`
[ ] ./df <domínio> sources --why  passa
[ ] ./df <domínio> list           parece correto
[ ] corpus baixado, passaporte escrito
[ ] prompts/: todos os cinco, nenhum com palavras de outro domínio
[ ] checks.json: números reais, alvos escolhidos a partir da documentação
[ ] smoke, protocol, raw, tools todos verdes
[ ] README.md diz como subir o servidor e registrá-lo no Claude Code
[ ] README.md e UPDATE.md escritos; o README da raiz cita o domínio
```
