# flux — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про Flux — набір інструментів GitOps для Kubernetes від CNCF (сайт
fluxcd.io, репозиторії fluxcd/flux2, fluxcd/website і контролерів), а також про те, що ставлять поруч із ним: Flagger
(прогресивна доставка), Flux Operator з його Helm-чартами і Terraform-провайдер для Flux. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо окремий примірник

Flux, як і Argo CD (примірник `argocd`), — контролер GitOps: бажаний стан кластера лежить у Git чи в OCI-реєстрі, а
контролери в самому кластері звіряють з ним живі ресурси. Flux розкладений на окремі контролери з власними ресурсами:
source-controller тягне джерела (`GitRepository`, `OCIRepository`, `HelmRepository`, `Bucket`), kustomize-controller
застосовує `Kustomization`, helm-controller — `HelmRelease`, notification-controller шле сповіщення (`Provider`,
`Alert`) і приймає вебхуки (`Receiver`), image-reflector і image-automation оновлюють теги образів просто в Git.
`flux bootstrap` ставить усе це в кластер і записує в репозиторій. У плані Next.js (фулстек-родина) — у розділі
«знати, що існує» й у «Що далі»: викот «з репозиторію».

Супутні проєкти взято за статистикою використання (26.10.2026): Flagger — 103 млн завантажень образу з Docker Hub і
5,4 тис. зірок, terraform-provider-flux — 47 млн завантажень з Terraform Registry, Flux Operator — 2,67 млн завантажень
релізів (і він тепер постачає офіційний Helm-чарт). Не взято Flux v1 (fluxcd/flux, архівований 2022 року),
tofu-controller (732 тис. завантажень, вузька ніша Terraform), weave-gitops (компанія-розробник закрилася) і
спільнотний чарт fluxcd-community (статистики немає).

## Скільки цього

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| Сайт fluxcd.io і блог | 509 | 11 | `content/en/flux` і `content/en/blog` гілок v2-0…v2-10 репозиторію fluxcd/website |
| Документація Flux 0.x | 582 | 42 | тека `docs/` і README репозиторію fluxcd/flux2, останній тег кожної мінорної 0.x |
| Релізи Flux | 207 | 207 | стабільні релізи fluxcd/flux2 |
| Специфікації CRD, довідники API, README семи контролерів | 671 | 23–48 | `docs/spec`, `docs/api`, останній тег кожної мінорної контролера |
| Журнали змін семи контролерів | 660 | 660 | `CHANGELOG.md` гілки main, по документу на версію |
| Flagger: сайт і README | 310 | 46 | `docs/gitbook` (docs.flagger.app) fluxcd/flagger |
| Flagger: релізи | 100 | 100 | стабільні релізи |
| Flux Operator: документація, README, чарти | 234 | 63 | `docs/`, README кореня й чартів `flux-operator` і `flux-instance` |
| Flux Operator: релізи | 72 | 72 | стабільні релізи |
| terraform-provider-flux: документація | 92 | 37 | `docs/` (Terraform Registry) і README |
| terraform-provider-flux: релізи | 128 | 128 | стабільні релізи |

Контролери: source-controller (191 документ, 48 мінорних), kustomize-controller (108, 47), helm-controller (86, 46),
notification-controller (148, 45), image-reflector-controller (69, 39), image-automation-controller (56, 45),
source-watcher (13, 23).

Разом 3565 записів паспорта; в індексі 3364 документи і 14 715 фрагментів (`expected_passages` у `checks.json`):
однаковий текст різних версій — один уривок із переліком версій. Замір `quality`: по словах 4 із 10, за змістом 4,
разом 4, «як модель» 10 із 10, без жодного перемикача (`max_per_doc`, `fusion_depth`, `title_match` не дали більше, а
`fusion_depth` і `max_per_doc: 1` знижували «як модель» до 8–9). Своїми словами нижче, бо перша десятка питає
побутовими словами («надіслати повідомлення в Slack, коли викот не вдався»), а сторінки говорять назвами ресурсів
(`Provider`, `Alert`). Дві цілі доповнено сторінками, що справді відповідають: довідником команди
`flux bootstrap github` (документація 0.x) і сторінкою сповіщень `monitoring/alerts` нинішнього сайту.

Чого немає. Довідника команд CLI для 2.x (`fluxcd.io/flux/cmd/`): сайт генерує його з бінарника під час збирання, у
репозиторіях markdown немає — є довідник 0.x з репозиторію flux2 і самі команди в посібниках і релізах. Пізніших 0.x
сайту: гілок версій у fluxcd/website до 2.0 немає. Також вихідний код (Go) і тести, пререлізи (`-rc`), Flux v1,
Kubernetes, Helm, Kustomize, SOPS і Terraform як окремі проєкти.

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

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df flux <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сайт fluxcd.io, блог | дерева голів 11 гілок `v2-N` fluxcd/website: `content/en/flux`, `content/en/blog` | `ghdocs-history` |
| документація Flux 0.x | дерева 42 тегів `v0.X.Y` fluxcd/flux2: `docs/`, `README.md` | `ghdocs-history` |
| контролери | дерева останнього тегу кожної мінорної семи репозиторіїв fluxcd/*-controller і source-watcher: `docs/spec`, `docs/api`, `README.md` | `ghdocs-history` |
| журнали контролерів | `CHANGELOG.md` гілки main, заголовок запису «## X.Y.Z» | `changelog-regex` |
| Flagger, Flux Operator, terraform-provider-flux | дерева останнього тегу кожної мінорної: `docs/gitbook`; `docs/` і README чартів; `docs/` | `ghdocs-history` |
| релізи | api.github.com, `/repos/…/releases` flux2, flagger, flux-operator, terraform-provider-flux, без передрелізів | `ghreleases` |

Нових читачів не знадобилося. Сайт fluxcd.io зібрано Hugo; кожна мінорна Flux 2 має власну гілку `v2-N`, тож
береться голова гілки, а версією стає найновіший патч flux2 цієї мінорної. Сторінки цитуються адресами fluxcd.io (поле
`site`), Flagger — docs.flagger.app, terraform-provider-flux — Terraform Registry, контролери й Flux Operator — файлами
на GitHub. Вставки Hugo в блозі (`imgproc`, `youtube`, `tweet`) лишаються в тексті як є. Специфікації CRD сайт
підтягує з репозиторіїв контролерів під час збирання, тому вони взяті звідти, з версіями самих контролерів.

## Версії

Сторінки сайту несуть версію Flux (`2.10.0`), документація 0.x — версію тегу flux2, релізи — версію релізу. Номери
контролерів і супутніх проєктів (1.x, 0.x) збігаються з номерами Flux, тож їх записано з префіксом:
`source-controller-1.10.1`, `kustomize-controller-1.10.1`, `helm-controller-1.7.1`, `flagger-1.45.0`,
`flux-operator-0.62.0`, `terraform-1.10.0`. Фільтр `version` бере мажор (`"2"`), мінор (`"2.6"`) або точну версію
(`"2.10.0"`); голе число лишає лише сам Flux, `"helm-controller-1"` — лінію контролера. Промпт відповідає для Flux 2.x
(найновіша — 2.10.0), а про поля CRD — за специфікацією найновішої лінії контролера, якщо користувач не назвав
старішу версію API.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку: у `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/flux-corpus-2026-10-26.tar.gz` (3565 текстів, паспорт і сховище
сирого `raw/`; перед видаленням текстів розпакований окремо й звірений із диском) і в копії на Windows
`C:\Distr\flux-corpus-2026-10-26.tar.gz` (звірено за SHA-256). В історії git текстів немає ніде.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/flux/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/flux-corpus-РРРР-ММ-ДД.tar.gz -C instances/flux corpus raw
find instances/flux/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/flux/raw
gzip -9 -c instances/flux/index/passages.json > instances/flux/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти й сховище — лише після того, як
архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із ними повертається сховище сирого:

```
tar -xzf ~/archives/docfactory/flux-corpus-2026-10-26.tar.gz -C instances/flux
./df flux smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати; їхні
перевірки `smoke` чесно пропускаються («корпус в архіві»).

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/flux/index/passages.json.gz`; далі
`./df flux vectors` заллє колекцію Qdrant (секунди на відеокарті, кілька хвилин на процесорі).

## Установка venv

Власний venv цьому примірнику не потрібен: `./df flux …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README, розділ
«Спільне середовище».

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df flux sources --why   # перелік джерел і білий список
./df flux refresh         # завантажити все задеклароване (близько 40 хвилин)
./df flux manifest        # оновити паспорт
./df flux setup           # Qdrant чи пошук лише по словах
./df flux vectors         # залити корпус у docs-flux
./df flux smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df flux serve          # порт 8908
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8908/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user flux-docs http://127.0.0.1:8908/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `flux-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у [README
примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
