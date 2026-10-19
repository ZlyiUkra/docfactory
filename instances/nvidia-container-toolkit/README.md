# nvidia-container-toolkit — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про NVIDIA Container Toolkit — набір, який дає контейнерам доступ до GPU
NVIDIA: середовище виконання `nvidia-container-runtime` (обгортка над `runc`, що дописує в специфікацію OCI пристрої,
бібліотеки драйвера й хуки), хук `nvidia-container-runtime-hook`, CLI `nvidia-ctk` (налаштування Docker, containerd,
CRI-O і Podman, генерація специфікацій CDI), хуки `nvidia-cdi-hook`, встановлювач `nvidia-ctk-installer` (образ, яким
користується GPU Operator) і під ними бібліотека libnvidia-container з CLI `nvidia-container-cli`. Документація —
сайт docs.nvidia.com кожної опублікованої версії 1.6.0–1.20.1; документи, журнал змін і нотатки релізів репозиторію
NVIDIA/nvidia-container-toolkit; код команд із прапорцями кожного сталого тегу v1.0.5–v1.20.1; код і тести v1.20.1;
README, журнал і релізи libnvidia-container; архівні nvidia-docker і nvidia-container-runtime; специфікація Container
Device Interface; пакети офіційного репозиторію APT і довідник публічних пакетів Go на pkg.go.dev. Код спільний і
лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики
— у [../../README.md](../../README.md).

Слова, що трапляються нижче:

- **середовище виконання** (runtime) — програма, яку Docker чи containerd викликають, щоб створити контейнер за
  специфікацією OCI; звичайне — `runc`, тут — `nvidia-container-runtime` поверх нього;
- **хук** — програма, яку середовище виконання запускає на певному кроці створення контейнера (`createContainer`,
  `prestart`): так у контейнер потрапляють пристрої й бібліотеки драйвера;
- **CDI** (Container Device Interface) — відкрита специфікація CNCF: файл YAML чи JSON у `/etc/cdi` або `/var/run/cdi`
  описує пристрій (`nvidia.com/gpu=0`) і зміни, які треба внести в контейнер (`containerEdits`: змінні, вузли
  пристроїв, монтування, хуки), а рушій (containerd, CRI-O, Docker, Podman) вносить їх сам;
- **режими** `nvidia-container-runtime`: `legacy` (усе робить хук через `nvidia-container-cli`), `cdi` (зміни зі
  специфікації CDI), `csv` (Jetson, перелік файлів у CSV), `auto` (вибирає сам);
- **unified release** — з 1.13 libnvidia-container і nvidia-container-toolkit випускаються разом під одним номером.

## Навіщо окремий примірник

Як GPU потрапляє в контейнер, мінялося з кожним поколінням: nvidia-docker 1.0 (обгортка й плагін томів), nvidia-docker2
і окремий пакет nvidia-container-runtime (runtime `nvidia` в `daemon.json`), з 1.6 — усе в nvidia-container-toolkit, з
1.12 — CDI, з 1.18 — служба `nvidia-cdi-refresh`, що сама генерує специфікацію. На машинах стоять дуже різні версії, а
сайт показує свою теку кожної версії. Прапорці `nvidia-ctk` і хуків окремої довідки не мають: їх описано лише в коді
команд (визначення urfave/cli з назвою, підказкою й типовим значенням), і між випусками вони з'являються, міняють
типові значення й переїжджають (`nvidia-ctk hook` → `nvidia-cdi-hook`, `tools/container` → `nvidia-ctk-installer`).
Тож відповідь «що робить `--config-mode` у 1.17.8» береться з коду й сторінок саме тієї версії, а не з пам'яті. Docker,
Kubernetes і gVisor мають власні примірники (`docker`, `kubernetes`, `gvisor`); тут — те, як NVIDIA Container Toolkit
дає їм GPU.

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| Сайт: огляд, встановлення й налаштування рушіїв, спеціалізовані налаштування Docker і змінні середовища, CDI, архітектура, платформи, приклад навантаження, усунення несправностей, нотатки випусків; у старих версіях — поняття, посібник користувача, перехід з nvidia-docker 1.0 | 100 | 550 | docs.nvidia.com, 35 тек версій 1.6.0–1.20.1 |
| README, CONTRIBUTING, DEVELOPMENT, RELEASE; README `nvidia-ctk`, `nvidia-container-runtime`, `nvidia-cdi-hook`, образу встановлювача й образу контейнера | 28 | 78 | `NVIDIA/nvidia-container-toolkit`, 55 тегів v1.0.5–v1.20.1 |
| CHANGELOG: запис на кожен сталий випуск разом із його `-rc` | 35 | 107 | тег v1.20.1 |
| Нотатки релізів | 55 | 217 | GitHub Releases, лише сталі |
| Код команд: `cmd/` (`nvidia-ctk`, `nvidia-cdi-hook`, `nvidia-ctk-installer`, `nvidia-container-runtime`, `nvidia-container-runtime-hook`), старіші `tools/container`, `pkg/` і `nvidia-container-toolkit/` | 408 | 1 468 | ті самі 55 тегів |
| Код Go і тести без `vendor` (бібліотеки `pkg/`, `internal/`, `api/`; тести, зокрема команд) | 329 | 1 364 | тег v1.20.1 |
| README libnvidia-container (`nvidia-container-cli`) | 8 | 14 | `NVIDIA/libnvidia-container`, 61 тег v1.0.0–v1.20.1 |
| CHANGELOG libnvidia-container | 2 | 5 | тег v1.20.1 |
| Нотатки релізів libnvidia-container | 61 | 131 | GitHub Releases, лише сталі |
| Архівний nvidia-docker: README, CONTRIBUTING | 12 | 50 | `NVIDIA/nvidia-docker`, 22 теги v1.0.0–v2.14.0 |
| Архівний nvidia-container-runtime: README, CONTRIBUTING, `testing/README.md` | 9 | 39 | `NVIDIA/nvidia-container-runtime`, 23 теги v3.0.0–v3.14.0 |
| Специфікація CDI: SPEC.md, README, TUTORIAL | 21 | 99 | `cncf-tags/container-device-interface`, 21 тег v0.3.0–v1.1.1 |
| Пакети APT: опис, залежності, усі версії | 7 | 26 | індекс `Packages` репозиторію nvidia.github.io/libnvidia-container (stable, amd64) |
| Публічні пакети Go: `pkg/nvcdi`, `pkg/config` з рушіями, `pkg/lookup`, `pkg/system`, `api/config/v1` | 17 | 291 | pkg.go.dev, версія модуля 1.20.1 |

Разом 1 092 документи (близько 6,6 МБ тексту) і 4 439 фрагментів після злиття однакових текстів
(`expected_passages` у `checks.json`); провалів завантаження — нуль. Зібрано 18.10.2026. Замір `quality` (10 запитів
назвами документації: встановлення через apt, `nvidia-ctk runtime configure` для containerd, `nvidia-ctk cdi generate`,
`NVIDIA_DRIVER_CAPABILITIES`, `nvidia-cdi-hook create-symlinks`, помилка «Failed to initialize NVML» після
`systemctl daemon-reload`, `containerEdits` у специфікації CDI, пакет `nvidia-container-toolkit-base` в APT,
`nvidia-container-cli`, служба `nvidia-cdi-refresh` у 1.18.0): по словах 10, за змістом 8 (повз пройшли
`nvidia-container-cli` і `nvidia-cdi-refresh` з версією), разом 10. `max_per_doc` і `fusion_depth` не міряно: замір
одразу дав 10 з 10.

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут немає:
  корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `sources.json` — звідки корпус будується (14 джерел), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — запис HTTP-сервера для Claude Code.

Кроки нижче запускаються з кореня фабрики через `./df nvidia-container-toolkit <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| сайт docs.nvidia.com, теки 35 версій | `sphinx-html` (новий) |
| документи репозиторіїв toolkit, libnvidia-container, nvidia-docker, nvidia-container-runtime і CDI кожного тегу | `ghdocs-history` |
| CHANGELOG toolkit і libnvidia-container | `changelog-prerelease` (новий) |
| код команд кожного тегу, код і тести v1.20.1 | `ghcode-history` (`outline: ["go"]`) |
| нотатки релізів | `ghreleases-stable` |
| пакети APT | `apt-packages-versions` (новий) |
| пакети Go на pkg.go.dev | `pkgsite` |

Особливості:

- **Сайт Sphinx по теках версій.** Кожна версія лежить своєю текою (`…/container-toolkit/1.20.1/`), а перелік версій
  `latest/versions1.json` називає лише вісім найновіших; решту 27 знайдено перебором номерів тегів (тек 1.17.1, 1.17.2,
  1.16.1, 1.13.0, 1.13.2–1.13.4 і старших за 1.6.0 на сайті немає). Мапи сайту немає, тож `sphinx-html` обходить
  посилання від `index.html` у межах теки версії. Він знімає якорі заголовків (`#`, у старій темі — значок шрифту
  U+F0C1), бере мову блоку коду з класу обгортки (`highlight-console`), підписує вкладки старої теми (sphinx-tabs:
  «CentOS 8:», «CentOS 7:» — без цього команди двох систем злипалися б у безіменний ряд коду), кладе клітинки таблиць
  рядком і викидає зміст `toctree`: стартова сторінка старої теми лише з нього й складається і документом не стає.
- **Злиття версій сайту.** Однаковий текст сторінки кількох версій — один документ, у шапці якого всі ці версії; адреса
  — сторінка найновішої з них. 35 версій дали 100 неповторних сторінок: `install-guide` — 19 редакцій, `release-notes`
  — 30, `arch-overview` — 8. Версії видно в кожному фрагменті. Сторінку «Overview» нових версій (`index.html`) і старих
  (`overview.html`) зведено до одного ключа (`slug_rewrite`).
- **Журнал зі змінами під передрелізами.** NVIDIA пише CHANGELOG так: «## v1.19.0» — один рядок «Promote v1.19.0-rc.7
  to v1.19.0», а зміни — під «## v1.19.0-rc.1» … «## v1.19.0-rc.7». `changelog-prerelease` робить документ на кожен
  сталий випуск, а записи його передрелізів кладе в нього розділами. Журнал береться один раз із тегу v1.20.1: кожен тег
  несе весь попередній журнал.
- **Прапорці в коді.** `ghcode-history` з `outline: ["go"]` ділить файл Go за оголошеннями верхнього рівня разом із
  коментарем над ними: `command.build()` — це `cli.Command` з назвою, підказкою й переліком `Flags` (назва, псевдоніми,
  підказка, типове значення, змінні середовища), а типові значення-константи лежать окремим розділом `const` того
  самого файла. Тести й згенеровані моки не взято. У тегах v1.0.5–v1.5.1 у репозиторії був лише хук
  (`nvidia-container-toolkit/`, потім `pkg/`) на пакеті `flag`.
- **Код і тести v1.20.1** — усе, крім `vendor` і моків; код самих команд `cmd/` бере джерело `cli` (там він з усіма
  тегами), тож один файл не лежить двічі.
- **README, що переїхали.** `build/container/README.md` став `deployments/container/README.md`, а
  `tools/container/README.md` — `cmd/nvidia-ctk-installer/container/README.md`; `slug_rewrite` дає їм спільні ключі.
- **APT з усіма версіями.** Репозиторій nvidia.github.io/libnvidia-container тримає не лише останню версію, а всі від
  1.14.0, і впорядковані вони від найстарішої. `apt-packages-versions` бере назву з найновішої за номером, розділ
  найновішої версії — з полями керування й контрольними сумами, а розділ «Versions» — кожна версія з її залежностями,
  розміром і файлом `.deb`. Репозиторій RPM дає ті самі версії й не береться, як і пакет символів `-dbg`.
- **pkg.go.dev.** Модуль `github.com/NVIDIA/nvidia-container-toolkit` пакета в корені не має, тож коренем джерела
  стоїть `pkg/nvcdi` (з підпакетами `spec` і `transform`), а решта публічних пакетів перелічена в `pages`. Без
  `internal` і команд `cmd` — їхній код дають `cli` і `code`. Пауза між зверненнями — 1,5 с.
- **Мітки версій.** Toolkit і libnvidia-container — спільна нумерація: `1.20.1`; лінія — два числа
  (`version_line_depth: 2`), тобто `version: "1.17"` бере всі 1.17.x. Продукти з власною нумерацією позначено:
  `nvidia-docker-2.14.0` (архівний nvidia-docker і пакет `nvidia-docker2`), `nvidia-container-runtime-3.14.0`
  (архівний runtime і його пакет), `cdi-1.1.1` (теги репозиторію специфікації CDI; версія самої специфікації,
  `cdiVersion`, — у тексті). Документів без версії немає. Без названої версії — найновіша, 1.20.1.
- **Що не береться.** Передрелізи `-rc` усіх репозиторіїв; теги libnvidia-container `v0.10.0+jetpack` (без релізу) і
  `v0.11.0+jetpack` (передреліз); теги nvidia-docker `-rc`, `-beta`, `v0.0.0-poc`; дублікати тегів
  nvidia-container-runtime без «v» (`3.0.0`, `3.0.1`, `3.1.0`); теги модуля CDI `specs-go/…` (ті самі коміти).

## Межі, про які треба пам'ятати

- Старі теки сайту — не точні знімки своїх версій: 1.6.0, 1.7.0, 1.8.0 і 1.8.1 тримають ту саму документацію з
  нотатками випусків аж до 1.8.1, так само 1.10.0 з 1.11.0, 1.12.0 з 1.12.1, 1.13.1 з 1.13.5 — їх викладено пізніше
  одним станом. Номер теки — це те, що каже сайт.
- `command.build()` з довгим переліком прапорців поділено за довжиною, а типове значення часто — константа з розділу
  `const` того самого файла: перш ніж називати значення, варто дочитати обидва розділи через `read_section`.
- CHANGELOG libnvidia-container у репозиторії ведуть лише для 1.14 (1.14.0 і 1.14.1); решта історії бібліотеки — у
  нотатках релізів, а з 1.13 вони здебільшого відсилають до спільного релізу toolkit.
- APT — лише amd64 і лише версії 1.14.0–1.20.1, які репозиторій ще тримає; pkg.go.dev — лише версія модуля 1.20.1;
  повний код і тести — лише 1.20.1 (для старших тегів — тільки код команд).
- Вікі архівного nvidia-docker на GitHub (стара документація встановлення й FAQ) у корпус не входить: джерела — сайт і
  файли репозиторіїв.
- Документації Docker, containerd, Kubernetes, NVIDIA GPU Operator, device plugin і самого драйвера тут немає: Docker —
  у примірнику `docker`, Kubernetes і containerd у кластері — у `kubernetes`, GPU у пісочниці gVisor (nvproxy) — у
  `gvisor`.

## Архівний режим: сервер без корпусу

Корпус в архіві від самого початку: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа. `smoke` дав 226 пройдених перевірок з корпусом і 224 в архівному
режимі (дві звірки з файлами пропускаються), провалів — нуль.

**Де тексти.** В архіві `~/archives/docfactory/nvidia-container-toolkit-corpus-2026-10-18.tar.gz` (9,5 МБ: 1 092
тексти, паспорт і сховище сирого `raw/`; перед видаленням розпакований окремо й звірений з диском через `diff -r` —
нуль розбіжностей). Лише на цій машині. У git — паспорт `corpus/index.json` і кеш `index/passages.json.gz`.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/nvidia-container-toolkit-corpus-РРРР-ММ-ДД.tar.gz -C instances/nvidia-container-toolkit corpus raw
find instances/nvidia-container-toolkit/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/nvidia-container-toolkit/raw
gzip -9 -c instances/nvidia-container-toolkit/index/passages.json > instances/nvidia-container-toolkit/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/nvidia-container-toolkit-corpus-2026-10-18.tar.gz -C instances/nvidia-container-toolkit
./df nvidia-container-toolkit smoke
```

**Оновлення.** Новий випуск: першим рядком у `versions` джерела `site` (номер теки, якщо сайт її виклав), у `tags`
джерел `toolkit-docs` і `cli` («"v1.21.0": "1.21.0"»), у `tags` джерела `libnvidia-container-docs`; у `tags` джерела
`code` і в адресах `toolkit-changelog` та `libnvidia-container-changelog` — замінити v1.20.1 новим тегом. Релізи, APT і
pkg.go.dev підхоплюються самі; архівні nvidia-docker і nvidia-container-runtime більше не змінюються, новий тег CDI —
рядок у `tags` джерела `cdi-spec` («"v1.2.0": "cdi-1.2.0"»). Далі `./df nvidia-container-toolkit list`, `refresh`,
`manifest`, `vectors`, `smoke`, `quality`. Перший повний `refresh` мережею тривав близько 6 хвилин (сайт — 3, решта —
3), `vectors` — 12.

## Установка venv

Власний venv цьому примірнику не потрібен: `./df nvidia-container-toolkit …` бере спільне середовище з кореня
репозиторію (`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому
README.md, розділ «Спільне середовище». Свій `.env` примірник тримає в `instances/nvidia-container-toolkit/.env`
(`cp .env.example .env`; для кроку `ask` потрібен `ANTHROPIC_API_KEY`); `GITHUB_TOKEN`, якого немає в цьому `.env`,
береться з кореневого.

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають. Для роботи сервера збирати нічого не
треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df nvidia-container-toolkit sources --why      # перелік джерел і білий список
./df nvidia-container-toolkit refresh            # завантажити все задеклароване
./df nvidia-container-toolkit manifest           # оновити паспорт
./df nvidia-container-toolkit setup              # Qdrant чи пошук лише по словах
./df nvidia-container-toolkit vectors            # залити корпус у docs-nvidia-container-toolkit
./df nvidia-container-toolkit smoke              # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df nvidia-container-toolkit serve             # порт 8861
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8861/mcp`. Якщо порт зайнятий,
сервер скаже про це й вийде: значить, `serve` цього примірника вже десь запущений; хто тримає порт, покаже
`ss -ltnp | grep 8861`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user nvidia-container-toolkit-docs http://127.0.0.1:8861/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User). Замість запису на рівні користувача можна відкрити Claude Code у цій теці:
`.mcp.json` тут уже називає сервер.

**3. Перевірити.** `/mcp` — має бути `nvidia-container-toolkit-docs` і два інструменти `search_docs`,
`read_section`. Якщо там «failed / not connected» — майже завжди сервер не піднятий (крок 1) або адреса не збігається
з полем `port` у `config.json`.

Зупинка — Ctrl+C у терміналі сервера.
