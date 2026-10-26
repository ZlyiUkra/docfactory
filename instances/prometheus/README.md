# prometheus — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про Prometheus — систему моніторингу й базу часових рядів CNCF
(репозиторій prometheus/prometheus) — і про Alertmanager, що групує, приглушує й розсилає сповіщення
(prometheus/alertmanager). Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає
самі дані домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

Prometheus сам опитує (scrape) цілі, які знаходить через виявлення сервісів (service discovery), і зберігає метрики як
часові ряди. Мова запитів PromQL рахує з них швидкості, перцентилі й суми, а правила сповіщень (alerting rules)
передають спрацювання в Alertmanager. Grafana малює ці ряди (примірник `grafana`). У плані Next.js (фулстек-родина)
Prometheus стоїть поруч із Grafana і Loki: метрики з історією, коли кластеру вистачає пам'яті.

Сайт prometheus.io збирається з трьох репозиторіїв: власні сторінки й блог — з prometheus/docs, документація
сервера — з `docs/` prometheus/prometheus, документація Alertmanager — з `docs/` prometheus/alertmanager (так каже
`docs-config.ts` сайту). Усі три тут є.

Супутніх проєктів не взято: клієнтських бібліотек (Go, Java, Python, `prom-client` для Node.js), експортерів
(`node_exporter`, `blackbox_exporter`, `pushgateway`), Prometheus Operator і Helm-чартів prometheus-community. Їх можна
додати окремими джерелами, якщо знадобляться.

## Скільки цього

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| Документація сервера | 522 | 73 | `docs/` prometheus/prometheus, останній тег кожної мінорної 1.8–3.15 |
| Документація Alertmanager | 51 | 14 | `docs/` prometheus/alertmanager, останній тег кожної мінорної 0.21–0.34 |
| Сайт prometheus.io | 70 | 1 | `docs/` prometheus/docs, знімок 24.10.2026 |
| Блог prometheus.io | 60 | 1 | `blog/posts` prometheus/docs, той самий знімок |
| Релізи Prometheus | 234 | 234 | стабільні релізи GitHub, 0.11–3.15 |
| Релізи Alertmanager | 58 | 58 | стабільні релізи GitHub, 0.1–0.34 |

Документів менше, ніж версій, бо файл, що не мінявся між мінорними, — один документ із переліком версій.

Разом 995 записів паспорта. В індексі 920 документів і 4346 фрагментів (`expected_passages` у `checks.json`):
однаковий текст різних версій дає один уривок із переліком версій. Замір `quality`: по словах 8 із 10, за змістом 5,
разом 8, «як модель» 10 із 10. Перемикачі не потрібні. Ціль запиту «counter gauge metric types» доповнено справжньою
відповіддю — розділом «Counter vs. gauge, summary vs. histogram» сторінки найкращих практик інструментування.

Чого немає:

- Тегів `v0.35`–`v0.315` репозиторію prometheus: це номери Go-модуля для 2.35–3.x, а не окремі випуски.
- Документації сервера до 1.8: до неї `docs/` у репозиторії не було, сторінки жили на сайті.
- Релізів зі збірками на кшталт `v2.43.0+stringlabels` і пререлізів (`-rc`).
- Вихідного коду (Go) і тестів.
- Grafana, Kubernetes, Thanos, Mimir, OpenTelemetry як окремих проєктів.

## Що в цій теці

- `corpus/` — паспорт `index.json`, тобто опис копії: адреса, дата завантаження й сума тексту кожного документа. Самих
  текстів тут немає: корпус в архіві (розділ «Архівний режим» нижче).
- `index/` — кеш фрагментів, з якого підіймається сервер. У git лежить стиснений `passages.json.gz`; розпакований
  `passages.json` лежить поруч і в git не потрапляє.
- `sources.json` — звідки будується корпус. Він же білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.mcp.json` — запис HTTP-сервера для Claude Code. `ANTHROPIC_API_KEY` (лише для кроку `ask`) і `GITHUB_TOKEN` (лише
  для завантаження корпусу) беруться з кореневого `.env`.

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df prometheus <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сервер | дерева 73 тегів `vX.Y.Z` prometheus/prometheus (1.8.2–3.15.1): `docs/` | `ghdocs-history` |
| Alertmanager | дерева 14 тегів `vX.Y.Z` prometheus/alertmanager (0.21.0–0.34.1): `docs/` | `ghdocs-history` |
| сайт | дерево коміту 3576591 prometheus/docs (24.10.2026): `docs/` | `ghdocs-history` |
| блог | той самий коміт: `blog/posts` | `ghdocs-history` |
| релізи | api.github.com, `/repos/prometheus/{prometheus,alertmanager}/releases`, без передрелізів і збірок з `+` | `ghreleases` |

Нових читачів не знадобилося: сторінки — звичайний markdown із шапкою YAML. Цитуються вони адресами prometheus.io
(поле `site`): сервер — `/docs/prometheus/latest/…`, Alertmanager — `/docs/alerting/latest/…`, сайт — `/docs/…`,
блог — `/blog/РРРР/ММ/ДД/…`; релізи — сторінками GitHub.

## Версії

Сторінки сервера несуть версію Prometheus (`3.15.1`), релізи — версію запису. Сайт і блог версій не мають, тож несуть
чинну версію Prometheus на день знімка (`3.15.1`). Номери Alertmanager (0.x) — окрема нумерація, тож вони записані з
префіксом: `alertmanager-0.34.1`. Фільтр `version` приймає мажор (`"3"`), мінор (`"3.15"`) або точну версію
(`"3.15.1"`); старі релізи Prometheus 0.x мають лінії з двох чисел (`"0.20"`). Голе число лишає лише Prometheus, сайт
і блог; `"alertmanager-0"` лишає Alertmanager. Промпт відповідає для найновіших версій (Prometheus 3.15.1, лінія
довгої підтримки 3.13, Alertmanager 0.34.1), якщо користувач не назвав старішу.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку. У `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant. Відповіді ті самі до символа, бо кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/prometheus-corpus-2026-10-26.tar.gz` (995 текстів, паспорт і сховище
сирого `raw/`; перед видаленням текстів архів розпаковано окремо й звірено з диском) і в копії на Windows
`C:\Distr\prometheus-corpus-2026-10-26.tar.gz` (звірено за SHA-256). В історії git текстів немає ніде.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/prometheus/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/prometheus-corpus-РРРР-ММ-ДД.tar.gz -C instances/prometheus corpus raw
find instances/prometheus/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/prometheus/raw
gzip -9 -c instances/prometheus/index/passages.json > instances/prometheus/index/passages.json.gz
```

Після цього закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Тексти й сховище видаляють лише тоді,
коли архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із текстами повертається сховище сирого:

```
tar -xzf ~/archives/docfactory/prometheus-corpus-2026-10-26.tar.gz -C instances/prometheus
./df prometheus smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Їхні
перевірки `smoke` чесно пропускає з позначкою «корпус в архіві».

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/prometheus/index/passages.json.gz`.
Далі `./df prometheus vectors` заллє колекцію Qdrant: секунди на відеокарті, хвилина на процесорі.

## Установка venv

Власний venv цьому примірнику не потрібен: `./df prometheus …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як збудувати його один раз і як `df` обирає між ними — у кореневому README, розділ
«Спільне середовище».

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df prometheus sources --why   # перелік джерел і білий список
./df prometheus refresh         # завантажити все задеклароване (близько 8 хвилин)
./df prometheus manifest        # оновити паспорт
./df prometheus setup           # Qdrant чи пошук лише по словах
./df prometheus vectors         # залити корпус у docs-prometheus
./df prometheus smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити його працювати:

```
cd ~/Projects/docfactory
./df prometheus serve          # порт 8910
```

Сервер готовий, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8910/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user prometheus-docs http://127.0.0.1:8910/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування. Вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell або додати сервер кнопкою «Add server» у вікні
`/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` має показати `prometheus-docs` і два інструменти: `search_docs` і `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта (scope запису, «address already in use») — так само, як у [README
примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
