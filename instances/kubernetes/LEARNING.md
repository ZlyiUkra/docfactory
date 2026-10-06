# Kubernetes — план вивчення

План для того, хто пройшов плани Linux і Docker цієї лінії (або вже впевнено адмініструє Linux і пакує застосунки
в образи) і хоче працювати з Kubernetes на рівні двох сертифікатів: CKAD (Certified Kubernetes Application
Developer) і CKA (Certified Kubernetes Administrator). Ціль — не «знати kubectl», а впевнено, на час і без шпаргалки
розгорнути застосунок у кластері з конфігурацією, секретами, мережею, перевірками стану й правами — а далі самому
підняти кластер kubeadm, оновити його, зробити й відновити резервну копію etcd і знайти, чому вузол `NotReady`.

**Обидва сертифікати — обов'язкова частина лінії.** План поділено на дві частини за ними: частина A готує до CKAD
(застосунок у кластері), частина B — до CKA (сам кластер). CKAD легший і йде першим: усе, що він питає, CKA
вважає відомим. Кожна фаза відповідає розділу програми іспиту, ваги розділів — у таблиці.

Це третій план лінії віртуалізації застосунків: Linux → Docker → Kubernetes. З плану Linux ви знаєте namespaces,
cgroups, systemd, мережу й сховища вузла; з плану Docker — образи, які тут запускаються. Лінія незалежна від
родини React → NestJS → Next.js: дотик лише там, де фулстек-плани викочують застосунок у кластер k3s, — хто пройшов
цей план, ті дні фулстек-планів проходить швидше.

Усього — сімдесят шість навчальних днів по півтори-дві години: 42 у частині A і 34 у частині B. П'ять днів на
тиждень дають близько чотирьох місяців.

| Фаза | Тема | Розділ програми | Днів |
|------|------|-----------------|------|
| **A** | **CKAD — застосунок у кластері** | | **42** |
| 0 | Робоче місце, kubectl і перший под | — | 4 |
| 1 | Робочі навантаження й томи | Application Design and Build, 20 % | 8 |
| 2 | Конфігурація, ресурси й безпека застосунку | Application Environment, Configuration and Security, 25 % | 9 |
| 3 | Сервіси й мережа | Services and Networking, 20 % | 6 |
| 4 | Розгортання: оновлення, стратегії, Helm, Kustomize | Application Deployment, 20 % | 6 |
| 5 | Спостереження й налагодження | Application Observability and Maintenance, 15 % | 5 |
| 6 | Іспит CKAD | усі | 4 |
| **B** | **CKA — сам кластер** | | **34** |
| 7 | Кластер з нуля: kubeadm, CNI, HA | Cluster Architecture, Installation and Configuration, 25 % | 8 |
| 8 | Життєвий цикл кластера й доступ | той самий розділ | 5 |
| 9 | Планування й автомасштабування | Workloads and Scheduling, 15 % | 4 |
| 10 | Сховища | Storage, 10 % | 3 |
| 11 | Мережа кластера | Servicing and Networking, 20 % | 4 |
| 12 | Пошук несправностей | Troubleshooting, 30 % | 6 |
| 13 | Іспит CKA | усі | 4 |

## Порядок трьох планів

| Етап | План | Сертифікат | Що виходить наприкінці |
|------|------|------------|------------------------|
| 1 | Linux | LFCS — факультатив | дві власні машини, налаштовані з нуля; контейнер, зібраний руками з namespaces і cgroups |
| 2 | Docker | — | образи власного застосунку, `compose`, збірка під дві архітектури з CI, реєстр |
| 3 | Kubernetes — цей план | CKAD, потім CKA — обов'язково | застосунок у кластері з Helm і Kustomize; власний кластер kubeadm з HA, оновленням і резервною копією etcd |

## Іспити CKAD і CKA

Що це за іспити, на 04.10.2026 (звіряйте на сторінках іспитів і в Candidate Handbook перед реєстрацією):

- **практичні, не тест:** 2 години, онлайн під наглядом проктора, задачі розв'язуються `kubectl` у кількох
  справжніх кластерах; кожна задача каже, в якому контексті її робити;
- **програми** — документи `CKAD Curriculum v1.33, v1.34, v1.35, v1.37` і `CKA Curriculum v1.32, v1.33, v1.34,
  v1.35` у цьому примірнику, з вагами розділів; план посилається на їхні пункти дослівно. Іспит іде на версії
  Kubernetes, близькій до поточної: на 04.10.2026 програма CKAD названа для 1.37, CKA — для 1.35;
- **довідка під час іспиту** — документація Kubernetes (kubernetes.io/docs) і ще кілька сайтів, перелік — в
  Important Instructions. Тому план вчить знаходити потрібну сторінку й копіювати з неї YAML, а не пам'ятати його;
- **симулятор:** дві спроби Killer.sh разом з іспитом — фази 6 і 13;
- **вартість** — $445 за кожен іспит разом із симулятором і повторною спробою; прохідний бал на момент написання —
  66 %, сертифікат дійсний 2 роки.

## З чого почати

**Кластери.** Частина A — на легкому кластері k3d (k3s у контейнерах Docker) на машині `ubu` з плану Linux, де вже
стоїть Docker: три вузли піднімаються за хвилину, видаляються за секунду. Частина B — на «справжньому» кластері
kubeadm з трьох нових віртуальних машин Ubuntu Server 24.04 (`cp1` — 2 ядра, 4 ГБ; `w1`, `w2` — 2 ядра, 2 ГБ), до
яких у фазі 7 додадуться ще два вузли керування для HA. Знімки — як у плані Linux: перед кожним днем, що ламає.

**Версія.** Вчіть на поточній лінії Kubernetes — 1.37; кластер kubeadm у фазі 7 ставте на попередню лінію, щоб у
фазі 8 оновити його до наступної, як на іспиті CKA. Між 1.35 і 1.37 у темах іспитів відчутних розбіжностей немає;
де вони є, план каже.

**Наскрізний проєкт.** Той самий застосунок з плану Docker — фронт, API і PostgreSQL, з образами в GHCR. У частині A
він переїжджає в кластер маніфестами, потім чартом Helm і оверлеями Kustomize; у частині B живе на власному кластері
й переживає його оновлення та відновлення etcd.

**Який сервер документації запустити.** З кореня фабрики: `./df kubernetes serve`. Корпус — документація Kubernetes
усіх ліній 1.0–1.37, журнали змін, а поруч — k3s, k3d, Gateway API, Traefik, cert-manager, Helm, Kustomize, книга
kubectl, metrics-server і програми іспитів CNCF. Назви глав у плані (у `такому вигляді`) — назви документів
корпусу на лінії 1.37; документи інструментів мають префікс («Helm: …», «Gateway API: …»). Питайте з версією:
`version: "1.37"` (Kubernetes), `"4"` (Helm), `"1.6"` (Gateway API).

**Репозиторій.** Тека `k8s/` у репозиторії застосунку або в `infra-notes`: маніфести, чарт, оверлеї, скрипти
підняття кластера kubeadm, README з відповідями на контрольні питання й чекбоксами днів `- [ ] Ф0 Д1. kubectl`.

## Як користуватися планом

У кожного дня сім рядків, як у планах Linux і Docker: **Навіщо**, **Що це**, **Читати**, **Сервери MCP**, **Зробити**,
**Перевірити себе**, **Пастка**. Пункт програми іспиту, якого стосується день, стоїть у дужках після назви дня.

**Сервери MCP.** Імена — як у Claude Code: сервер примірника `x` зветься `x-docs` (`react-docs`, `mdn-docs`,
`webstandards-docs`). Під заголовком кожної фази — усі сервери фази разом: їх варто підняти до її початку (`./df
<примірник> serve` з кореня фабрики) і додати в Claude Code командою з README примірника. Сервер відповідає з тих
самих глав, що названі в рядку «Читати», і дає адресу джерела, за якою відповідь можна перевірити. «Жодного» — джерела
дня поза фабрикою; чого бракує — у [карті навчання](../../docs/learning-map.md).

**Імперативно, потім YAML.** На іспиті немає часу писати маніфести з нуля. Звичка з першого дня:
`kubectl create … --dry-run=client -o yaml > файл.yaml`, правка, `kubectl apply -f`. `kubectl explain поле
--recursive` — довідник полів без браузера.

**Таймер з фази 1.** Кожна вправа наступного дня повторюється з чистого кластера на час — без плану, лише з
kubernetes.io/docs (саме це дозволено на іспиті). Час — у журнал. На іспиті на задачу в середньому 6–8 хвилин.

## Словник

- **Кластер, вузол, площина керування.** Кластер — машини (вузли), якими керує площина керування: `kube-apiserver`
  (вхід для всього), `etcd` (сховище стану), `kube-scheduler` (куди поставити под), `kube-controller-manager`
  (контролери, що доводять стан до бажаного). На кожному вузлі — `kubelet` (запускає поди через containerd) і
  `kube-proxy` (правила сервісів).
- **Об'єкт і маніфест.** Об'єкт — запис у кластері з бажаним станом (`spec`) і фактичним (`status`). Маніфест — YAML
  з описом об'єкта; `kubectl apply` надсилає його в apiserver.
- **Под (Pod).** Найменша одиниця: один чи кілька контейнерів зі спільною мережею (одна IP-адреса) і томами.
  Поди смертні й замінні — напряму їх майже не створюють.
- **Контролер.** Цикл, що порівнює бажаний стан з фактичним і виправляє різницю: Deployment тримає потрібну
  кількість подів, Job — доводить задачу до кінця.
- **Мітки й селектори.** Мітки — пари ключ-значення на об'єктах; селектор — запит за мітками. Так Deployment
  знаходить свої поди, а Service — поди, на які слати трафік.
- **Простір імен (namespace).** Логічна тека об'єктів у кластері (не плутати з namespace ядра з плану Linux).
- **Service.** Стабільна адреса й ім'я DNS для набору подів, адреси яких змінюються.
- **Ingress і Gateway API.** Правила, як HTTP-трафік ззовні доходить до сервісів; Gateway API — новіший і
  виразніший наступник Ingress.
- **ConfigMap і Secret.** Конфігурація й секрети окремо від образу; поди беруть їх змінними чи файлами.
- **PV, PVC, StorageClass.** Том (PersistentVolume), заявка на том (PersistentVolumeClaim) і клас, за яким тома
  створюються автоматично.
- **RBAC.** Хто (користувач, група, ServiceAccount) що може робити з якими об'єктами: Role/ClusterRole — дозволи,
  RoleBinding/ClusterRoleBinding — кому їх видано.
- **CRD й оператор.** CRD додає в API новий тип об'єкта; оператор — контролер, що вміє ним керувати.
- **CNI, CSI, CRI.** Інтерфейси розширення: мережа подів, сховища й рантайм контейнерів — їх реалізують плагіни, а не
  сам Kubernetes.

## П'ять пасток, які переживають будь-який рівень

- **Не той контекст.** На іспиті кілька кластерів; задача, зроблена не в тому, не зараховується. Перша команда
  кожної задачі — `kubectl config use-context …`, скопійована з умови.
- **Не той простір імен.** Об'єкт створено в `default`, а задача казала `-n prod`. Простір — у кожній команді або
  `kubectl config set-context --current --namespace=…`.
- **Мітки селектора не збігаються.** Service без ендпоінтів, Deployment, що «не бачить» своїх подів, NetworkPolicy, що
  нікого не пускає — майже завжди мітка з одруківкою. `kubectl get pods --show-labels` і `kubectl get endpointslices`.
- **Под у CrashLoopBackOff — читайте попередній журнал.** Поточний контейнер щойно стартував і порожній; причина —
  в `kubectl logs --previous` і в `kubectl describe` (Last State, Reason, Exit Code).
- **Зміна руками в кластері, а не в маніфесті.** `kubectl edit` працює, але наступний `apply` з git поверне старе.
  Правда — у файлах; руками — лише на іспиті й під час пожежі.

# Частина A. CKAD — застосунок у кластері

# Фаза 0. Робоче місце, kubectl і перший под — 4 дні

**Сервери MCP фази:** `kubernetes-docs`.

### День 1. Кластер k3d і kubectl

- **Навіщо.** Кластер, який піднімається за хвилину й не шкода зламати, — головний тренажер частини A.
- **Що це.** k3d запускає вузли k3s як контейнери Docker; `kubectl` говорить з кластером через kubeconfig
  (`~/.kube/config`): кластери, користувачі, контексти. Автодоповнення й псевдонім `k` — як на іспиті.
- **Читати:** `k3d: Overview`; `k3d: k3d cluster create`; `Organizing Cluster Access Using kubeconfig Files`;
  `Configure Access to Multiple Clusters`; `kubectl Quick Reference` — розділи про автодоповнення й контексти.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) поставити `kubectl` і k3d на `ubu`; 2) кластер `dev` з одним сервером і двома агентами; 3) другий
  кластер `stage` і перемикання між ними; 4) автодоповнення bash і `alias k=kubectl` з доповненням.
- **Перевірити себе:** `kubectl get nodes` — три вузли `Ready`; `kubectl config get-contexts` — два контексти,
  поточний позначено.
- **Пастка:** два термінали з різними контекстами — і `delete` летить не в той кластер. Контекст у запрошенні
  оболонки (kube-ps1) або щоразу `kubectl config current-context`.

### День 2. Об'єкти, API і `explain`

- **Навіщо.** На іспиті без браузера поле маніфесту швидше знайти в `kubectl explain`, ніж у документації.
- **Що це.** Кожен об'єкт має `apiVersion`, `kind`, `metadata`, `spec`, `status`. `kubectl api-resources` — усі
  типи, їхні короткі імена й чи вони в просторі імен; `kubectl explain pod.spec.containers --recursive` — поля.
  Імперативні команди (`run`, `create deployment`, `expose`) з `--dry-run=client -o yaml` дають заготовку маніфесту.
- **Читати:** `Kubernetes Components`; `Command line tool (kubectl)`; `Namespaces`; `Labels and Selectors`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) простір `app`; 2) заготовки маніфестів пода, Deployment і Service імперативними командами в
  файли; 3) за `explain` знайти, де в поді задається політика завантаження образу і як зветься поле команди.
- **Перевірити себе:** три YAML-файли, створені без набору руками; `kubectl api-resources --namespaced=false` —
  ви пояснюєте, чому вузли не в просторі імен.
- **Пастка:** `kubectl run` для Deployment — він створює лише под. Deployment — `kubectl create deployment`.

### День 3. Под

- **Навіщо.** Під — цеглинка всього іншого: усі поля контейнера, що будуть далі, живуть у його специфікації.
- **Що це.** `spec.containers`: `image`, `command`/`args` (перекривають `ENTRYPOINT`/`CMD` образу), `env`, `ports`,
  `resources`. Фази пода (Pending, Running, Succeeded, Failed) і стани контейнерів; `restartPolicy`. `kubectl
  describe`, `logs`, `exec`, `get -o wide`, `-o yaml`.
- **Читати:** `Pods`; `Pod Lifecycle`; `Images`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) под з API наскрізного проєкту з образу GHCR (з секретом реєстру `imagePullSecrets`, якщо образ
  приватний); 2) перекрити команду й аргументи; 3) под з помилкою в імені образу — знайти причину в `describe`.
- **Перевірити себе:** `kubectl get pod api -o jsonpath='{.status.phase}'` — Running; для зламаного — `ErrImagePull`
  чи `ImagePullBackOff` і повідомлення в Events.
- **Пастка:** `command` у маніфесті вважають аналогом `CMD`. `command` перекриває `ENTRYPOINT`, `args` — `CMD`.

### День 4. Простори імен, мітки, анотації

- **Навіщо.** Порядок у кластері й основа всього, що вибирає об'єкти: сервісів, політик мережі, розгортань.
- **Що це.** Мітки (`app`, `tier`, `version`) і селектори за рівністю й за множинами; анотації — довільні
  метадані, не для вибору. `kubectl label`, `annotate`, `get -l`, `--show-labels`. Рекомендовані мітки
  `app.kubernetes.io/*`.
- **Читати:** `Labels and Selectors`; `Namespaces`; `Annotations`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) десять подів з різними мітками й вибрати їх кількома селекторами; 2) перемітити под так, щоб
  він «випав» з вибірки; 3) видалити всі поди з міткою однією командою.
- **Перевірити себе:** `kubectl get pods -l 'tier in (api,web),version!=v1'` повертає очікуване.
- **Пастка:** видалити простір імен «щоб прибрати» — разом з усім у ньому, назавжди і без запитання.

# Фаза 1. Робочі навантаження й томи — 8 днів

**Сервери MCP фази:** `kubernetes-docs`.

Розділ Application Design and Build — 20 % CKAD: `Define, build and modify container images`, `Choose and use the
right workload resource (Deployment, DaemonSet, CronJob, etc.)`, `Understand multi-container Pod design patterns
(e.g. sidecar, init and others)`, `Utilize persistent and ephemeral volumes`.

### День 1. Образи для кластера (Define, build and modify container images)

- **Навіщо.** CKAD прямо питає: зібрати образ, змінити його й запустити в поді.
- **Що це.** Усе з плану Docker (фази 1 і 6): Dockerfile, теги, не root з числовим UID, сигнали. На іспиті часто
  `podman` чи `docker` під рукою і задача «змініть Dockerfile, зберіть, збережіть образ архівом» (`save`).
  `imagePullPolicy`: `IfNotPresent`, `Always`, `Never`; тег `latest` змінює типову політику.
- **Читати:** `Images`; план Docker, фаза 1.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) змінити Dockerfile API (нова змінна, інший порт), зібрати, `docker save` в архів; 2) імпортувати
  образ у k3d (`k3d image import`) і запустити под з `imagePullPolicy: Never`.
- **Перевірити себе:** под стартує з локального образу без реєстру.
- **Пастка:** тег `latest` у поді — `imagePullPolicy` стає `Always`, і без реєстру под не стартує, хоч образ лежить на
  вузлі.

### День 2. Deployment і ReplicaSet (Choose and use the right workload resource)

- **Навіщо.** Головний спосіб запускати застосунки без стану: потрібна кількість реплік, самовідновлення, оновлення.
- **Що це.** Deployment керує ReplicaSet, той — подами за селектором і шаблоном. `kubectl scale`, `kubectl set
  image`, `kubectl rollout status/history/undo`. Шаблон пода змінився — новий ReplicaSet.
- **Читати:** `Deployments`; `ReplicaSet`; `Workload Management`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) Deployment API на 3 репліки; 2) видалити под — побачити заміну; 3) змінити образ і дивитися
  `rollout status`; 4) відкотити.
- **Перевірити себе:** `kubectl get rs` — два ReplicaSet, старий на 0; `rollout history` — дві ревізії.
- **Пастка:** змінити мітки в `selector` Deployment після створення — поле незмінне, apply відмовить. Селектор
  обирають раз.

### День 3. DaemonSet, Job, CronJob (Choose and use the right workload resource)

- **Навіщо.** Не все є «N реплік»: агент на кожному вузлі, одноразова задача, задача за розкладом.
- **Що це.** DaemonSet — под на кожному (чи вибраних) вузлі. Job — доводить под(и) до успіху: `completions`,
  `parallelism`, `backoffLimit`, `activeDeadlineSeconds`, `ttlSecondsAfterFinished`. CronJob — Job за розкладом
  cron (формат з плану Linux), `concurrencyPolicy`, історія.
- **Читати:** `DaemonSet`; `Jobs`; `CronJob`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) DaemonSet, що на кожному вузлі пише ім'я вузла в журнал; 2) Job міграції бази наскрізного проєкту;
  3) CronJob резервної копії бази щоночі; 4) Job, що завжди падає, — подивитися на `backoffLimit`.
- **Перевірити себе:** `kubectl get pods -o wide -l app=node-agent` — по одному на вузол; `kubectl get jobs` —
  міграція `Complete`; CronJob створює Job за розкладом (`kubectl create job --from=cronjob/…` для перевірки
  зараз).
- **Пастка:** `restartPolicy: Always` у Job — не дозволено; для Job лише `OnFailure` або `Never`.

### День 4. StatefulSet

- **Навіщо.** База в кластері: стабільні імена подів і власний том на кожну репліку.
- **Що це.** StatefulSet дає подам імена `db-0`, `db-1`, запускає їх по черзі, кожному — PVC з
  `volumeClaimTemplates`; потрібен headless Service (`clusterIP: None`) для DNS-імен окремих подів.
- **Читати:** `StatefulSets`; `Debug a StatefulSet`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** PostgreSQL наскрізного проєкту як StatefulSet з одним подом, headless Service і PVC; видалити под —
  новий `db-0` підхоплює той самий том.
- **Перевірити себе:** дані пережили видалення пода; `nslookup db-0.db` з іншого пода повертає адресу.
- **Пастка:** видалення StatefulSet не видаляє PVC — і це правильно; але й нова установка «з нуля» підхоплює старі
  дані.

### День 5. Init-контейнери й sidecar (Understand multi-container Pod design patterns)

- **Навіщо.** Задачі «перед стартом» і «поруч із застосунком» — класика CKAD.
- **Що це.** Init-контейнери виконуються по черзі до основних і мусять завершитися успіхом. Sidecar — з 1.33
  стабільні «рідні» sidecar: init-контейнер з `restartPolicy: Always`, що стартує перед основним і живе поруч. Інші
  шаблони: ambassador, adapter — звичайні додаткові контейнери зі спільною мережею й томами.
- **Читати:** `Init Containers`; `Sidecar Containers`; `Debug Init Containers`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) init-контейнер, що чекає на базу (`until nc -z db 5432`); 2) sidecar, що читає журнал застосунку
  зі спільного `emptyDir` і віддає його в stdout; 3) зламати init-контейнер і подивитися статус `Init:Error`.
- **Перевірити себе:** `kubectl get pod` — `Init:0/1`, поки база не готова; потім `2/2 Running` для пода з sidecar.
- **Пастка:** sidecar як звичайний другий контейнер у Job — Job ніколи не завершиться, бо sidecar живе вічно.
  Рідний sidecar (init з `restartPolicy: Always`) цю проблему розв'язує.

### День 6. Томи: ефемерні (Utilize persistent and ephemeral volumes)

- **Навіщо.** Спільні файли між контейнерами пода, тимчасовий кеш, конфіг файлом.
- **Що це.** `emptyDir` (живе з подом; `medium: Memory` — tmpfs), `configMap`/`secret` як файли, `projected`,
  `downwardAPI` (метадані пода у файли чи змінні), загальні ефемерні томи (`ephemeral` — PVC на час життя пода).
- **Читати:** `Volumes`; `Ephemeral Volumes`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) `emptyDir` спільний для двох контейнерів; 2) ім'я пода й ліміт пам'яті в змінні через downward
  API; 3) `emptyDir` з `sizeLimit` — переповнити й побачити виселення пода.
- **Перевірити себе:** `kubectl exec … env | grep POD_NAME` — ім'я пода; переповнений под — `Evicted`.
- **Пастка:** вважати `emptyDir` постійним — він зникає з подом, а не з контейнером (перезапуск контейнера дані
  лишає, видалення пода — ні).

### День 7. Томи: постійні (Utilize persistent and ephemeral volumes)

- **Навіщо.** Дані, що переживають под: база, завантажені файли.
- **Що це.** Под не просить диск напряму — він посилається на PVC, а PVC зв'язується з PV (вручну створеним чи
  створеним StorageClass динамічно). У k3s/k3d типовий клас — `local-path`. Режими доступу (`ReadWriteOnce`,
  `ReadWriteMany`, `ReadWriteOncePod`).
- **Читати:** `Persistent Volumes`; `Configure a Pod to Use a PersistentVolume for Storage`; `Dynamic Volume
  Provisioning`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) PVC з типовим класом і под, що пише в нього; 2) PV `hostPath` руками і PVC, що зв'язується саме з
  ним (за класом і розміром); 3) PVC, що лишається `Pending`, — знайти причину.
- **Перевірити себе:** `kubectl get pvc` — `Bound`; дані пережили видалення пода.
- **Пастка:** PVC просить 5Gi, а PV — 2Gi: зв'язку не буде, і PVC мовчки `Pending`. `describe pvc` каже чому.

### День 8. Підсумок фази: проєкт у кластері

- **Навіщо.** Усе разом на власному застосунку — контрольна точка частини A.
- **Що це.** Маніфести наскрізного проєкту: StatefulSet бази, Job міграції, Deployment API й фронту, init-контейнер
  очікування бази.
- **Читати:** `Managing Workloads`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** маніфести в теці `k8s/base/`, `kubectl apply -f k8s/base/` на чистому кластері.
- **Перевірити себе:** з чистого кластера одна команда — і все `Running`/`Complete`; `kubectl port-forward` до
  фронту показує дані з бази.
- **Пастка:** застосувати теку, де Job міграції вже `Complete`, — повторний `apply` не перезапускає Job; для нової
  міграції — нове ім'я Job.

# Фаза 2. Конфігурація, ресурси й безпека застосунку — 9 днів

**Сервери MCP фази:** `kubernetes-docs`, `webstandards-docs`.

Розділ Application Environment, Configuration and Security — 25 % CKAD, найбільший. Пункти: CRD й оператори;
автентифікація, авторизація й контроль допуску; запити, ліміти, квоти; ConfigMap; Secret; ServiceAccount;
безпека застосунку (SecurityContext, можливості).

### День 1. ConfigMap (Understand ConfigMaps)

- **Навіщо.** Той самий образ — різні середовища, без перезбирання.
- **Що це.** ConfigMap з літералів, файлів чи теки; у под — `env.valueFrom.configMapKeyRef`, `envFrom` чи том. Том
  оновлюється при зміні ConfigMap (із затримкою), змінні — ні (лише перезапуск пода). `immutable: true`.
- **Читати:** `ConfigMaps`; `Configure a Pod to Use a ConfigMap`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) конфіг API через `envFrom`; 2) конфіг nginx фронту файлом з ConfigMap; 3) змінити ConfigMap і
  перевірити, що змінилося у файлі, а що — ні у змінних; 4) `kubectl rollout restart` для підхоплення.
- **Перевірити себе:** нове значення у файлі пода через хвилину; у змінних — лише після `rollout restart`.
- **Пастка:** `subPath`-монтування ConfigMap не оновлюється ніколи — лише перезапуском пода.

### День 2. Secret (Create & consume Secrets)

- **Навіщо.** Паролі, токени й ключі TLS окремо від конфігурації — і з окремими правами доступу.
- **Що це.** Типи: `Opaque`, `kubernetes.io/tls`, `kubernetes.io/dockerconfigjson`. `kubectl create secret generic
  --from-literal/--from-file`. Значення — base64, тобто **не** шифрування; шифрування в etcd — налаштування кластера
  (фаза 8). Секрет у змінні чи файлами з правами 0400.
- **Читати:** `Secrets`; `Distribute Credentials Securely Using Secrets`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) пароль бази — Secret, і база, і API беруть його звідти; 2) секрет реєстру для приватного образу;
  3) розкодувати секрет з `kubectl get secret -o jsonpath` і зрозуміти, кому це дозволено.
- **Перевірити себе:** у маніфестах у git немає жодного пароля; API підключається до бази.
- **Пастка:** Secret у git «бо base64». Base64 — кодування, читається однією командою. У git — лише зашифровані (SOPS
  — у плані його вчать фулстек-плани) або згенеровані в кластері.

### День 3. Запити й ліміти (Define resource requirements)

- **Навіщо.** Планувальник ставить под за запитами, ядро обмежує за лімітами; без них один под з'їдає вузол.
- **Що це.** `requests` — скільки под гарантовано отримує (для планування), `limits` — стеля (cgroup з плану Linux).
  Перевищення пам'яті — OOMKilled, процесора — пригальмовування. Класи QoS: Guaranteed, Burstable, BestEffort — від
  них залежить, кого виселять першим.
- **Читати:** `Resource Management for Pods and Containers`; `Assign Memory Resources to Containers and Pods`;
  `Assign CPU Resources to Containers and Pods`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) запити й ліміти для всіх контейнерів проєкту; 2) под, що перевищує ліміт пам'яті, — `OOMKilled`;
  3) под із запитом більшим, ніж є на будь-якому вузлі, — `Pending`.
- **Перевірити себе:** `kubectl describe pod` — `Last State: Terminated, Reason: OOMKilled`; для `Pending` — подія
  `Insufficient memory`.
- **Пастка:** ліміт процесора на застосунку, чутливому до затримок, — пригальмовування кожні 100 мс при середньому
  навантаженні нижче ліміту. Пам'ять — ліміт обов'язково, процесор — свідомо.

### День 4. LimitRange і ResourceQuota (Understand requests, limits, quotas)

- **Навіщо.** Межі на простір імен: команда не забере весь кластер, і под без запитів отримає типові.
- **Що це.** LimitRange — типові й межові значення запитів/лімітів для кожного контейнера простору. ResourceQuota —
  сума на весь простір (процесор, пам'ять, кількість подів, PVC, сервісів). З квотою под без запитів не створиться.
- **Читати:** `Limit Ranges`; `Resource Quotas`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) квота простору `app`: 2 CPU, 2Gi, 10 подів; 2) LimitRange з типовими значеннями; 3) масштабувати
  Deployment понад квоту й знайти, чому нових подів немає.
- **Перевірити себе:** `kubectl describe quota -n app` — використано/межа; подія ReplicaSet `exceeded quota`.
- **Пастка:** шукати помилку квоти в подах — подів немає, бо їх не створено; помилка в подіях ReplicaSet.

### День 5. ServiceAccount (Understand ServiceAccounts)

- **Навіщо.** Під, що звертається до API кластера (оператор, CI-агент), має власну ідентичність з мінімальними
  правами.
- **Що це.** Кожен под працює від ServiceAccount (типово `default` простору); токен — у томі з обмеженим часом
  життя (projected). `automountServiceAccountToken: false` — для подів, яким API не потрібен. `kubectl create
  token`.
- **Читати:** `Service Accounts`; `Configure Service Accounts for Pods`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) ServiceAccount `reader` і под з ним; 2) з пода спробувати `kubectl get pods` (образ з kubectl) —
  відмова; 3) вимкнути автомонтування токена для API проєкту.
- **Перевірити себе:** `kubectl auth can-i list pods --as=system:serviceaccount:app:reader` — `no` (поки).
- **Пастка:** видати права типовому ServiceAccount `default` — і їх отримують усі поди простору.

### День 6. Автентифікація, авторизація, допуск і RBAC

- **Навіщо.** Пункт програми `Understand authentication, authorization and admission control`. Кожен запит до API
  проходить три ворота; CKAD питає розуміння, CKA — налаштування.
- **Що це.** Автентифікація — хто ви (сертифікат, токен ServiceAccount, OIDC). Авторизація — чи можна (RBAC: Role,
  ClusterRole, RoleBinding, ClusterRoleBinding). Контролери допуску — змінюють чи відхиляють об'єкт після
  авторизації (LimitRange, ResourceQuota, Pod Security Admission). `kubectl auth can-i`.
- **Читати:** `Authenticating`; `Authorization`; `Using RBAC Authorization`; `Admission Control in Kubernetes`; у
  примірнику `webstandards` — `OpenID Connect Core 1.0: 2 ID Token`.
- **Сервери MCP:** `kubernetes-docs`, `webstandards-docs`.
- **Зробити:** 1) Role «читати поди й журнали» в `app` і RoleBinding на `reader`; 2) перевірити `can-i` і з пода;
  3) ClusterRole з агрегацією або для читання вузлів і ClusterRoleBinding.
- **Перевірити себе:** `kubectl auth can-i get pods/log -n app --as=system:serviceaccount:app:reader` — `yes`;
  `delete pods` — `no`.
- **Пастка:** RoleBinding на ClusterRole діє лише в просторі RoleBinding — і це нормальний спосіб перевикористати
  ClusterRole; а ClusterRoleBinding дає права в усьому кластері.

### День 7. Безпека застосунку (Understand Application Security)

- **Навіщо.** Той самий захист контейнера, що в плані Docker, — тепер полями маніфесту, і з перевіркою на рівні
  простору імен.
- **Що це.** `securityContext` пода й контейнера: `runAsUser`, `runAsNonRoot`, `fsGroup`, `readOnlyRootFilesystem`,
  `allowPrivilegeEscalation: false`, `capabilities.drop: ["ALL"]`, `seccompProfile`. Pod Security Standards
  (privileged, baseline, restricted) і їх застосування мітками простору (Pod Security Admission).
- **Читати:** `Configure a Security Context for a Pod or Container`; `Pod Security Standards`; `Pod Security
  Admission`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) простір `app` з міткою `pod-security.kubernetes.io/enforce=restricted`; 2) привести поди проєкту до
  restricted; 3) спробувати під з root і `privileged` — відмова з поясненням.
- **Перевірити себе:** усі поди проєкту `Running` у просторі restricted; `kubectl exec api -- id` — не 0.
- **Пастка:** `runAsNonRoot: true` з образом, де `USER` — ім'я, а не число: под не стартує
  (`CreateContainerConfigError`). Числовий UID в образі (план Docker, фаза 6).

### День 8. CRD й оператори (Discover and use resources that extend Kubernetes)

- **Навіщо.** Половина того, що ставлять у кластер (cert-manager, Gateway API, оператори баз), — це нові типи
  об'єктів.
- **Що це.** CustomResourceDefinition додає тип в API; після цього `kubectl get <тип>` працює як для вбудованих.
  Оператор — контролер, що виконує дії за цими об'єктами. `kubectl api-resources`, `kubectl explain` працюють і для
  CRD.
- **Читати:** `Custom Resources`; `Extend the Kubernetes API with CustomResourceDefinitions`; `Operator pattern`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) власний CRD `Backup` зі схемою й створити об'єкт; 2) поставити cert-manager і знайти його CRD;
  3) `kubectl explain certificate.spec`.
- **Перевірити себе:** `kubectl get crd` — ваш і cert-manager-ів; `kubectl get backups` повертає ваш об'єкт.
- **Пастка:** видалити CRD — разом з усіма його об'єктами в кластері.

### День 9. Підсумок фази

- **Навіщо.** Проєкт з конфігурацією, секретами, лімітами, квотою, мінімальними правами й рівнем restricted.
- **Що це.** Чек-лист фази по маніфестах проєкту.
- **Читати:** `Configuration Best Practices`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** привести `k8s/base/` до чек-листа й застосувати на чистому кластері.
- **Перевірити себе:** проєкт стартує в просторі restricted з квотою; жодного секрету в git.
- **Пастка:** забути про квоту при масштабуванні у фазі 4 — нові поди не створяться, і шукати доведеться в подіях
  ReplicaSet.

# Фаза 3. Сервіси й мережа — 6 днів

**Сервери MCP фази:** `kubernetes-docs`.

Розділ Services and Networking — 20 % CKAD: NetworkPolicy, доступ до застосунків через сервіси, Ingress.

### День 1. Service (Provide and troubleshoot access to applications via services)

- **Навіщо.** Поди приходять і йдуть зі своїми адресами; сервіс дає стабільне ім'я й балансування.
- **Що це.** Типи: `ClusterIP` (усередині), `NodePort` (порт на кожному вузлі), `LoadBalancer` (зовнішня адреса — в
  k3s її дає ServiceLB), `ExternalName`. Селектор → EndpointSlice з адресами готових подів. `port`, `targetPort`,
  `nodePort`. `kubectl expose`.
- **Читати:** `Service`; `Use a Service to Access an Application in a Cluster`; `EndpointSlices`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) ClusterIP для API і бази; 2) NodePort для фронту; 3) сервіс з одруківкою в селекторі — порожні
  ендпоінти, знайти й виправити.
- **Перевірити себе:** `kubectl get endpointslices -l kubernetes.io/service-name=api` — адреси трьох подів; фронт
  відкривається на порту вузла.
- **Пастка:** `targetPort` — порт контейнера, `port` — порт сервісу; переплутати — і сервіс приймає з'єднання, яке
  нікуди не веде.

### День 2. DNS у кластері

- **Навіщо.** Застосунки знаходять одне одного за іменами; помилка DNS схожа на помилку мережі.
- **Що це.** CoreDNS: `сервіс` (у тому самому просторі), `сервіс.простір`, повне `сервіс.простір.svc.cluster.local`;
  headless-сервіс віддає адреси подів; `/etc/resolv.conf` пода з `search` і `ndots:5`.
- **Читати:** `DNS for Services and Pods`; `Debugging DNS Resolution`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) з пода в іншому просторі звернутися до API коротким і повним іменем; 2) подивитися `resolv.conf`
  пода; 3) зламати DNS (масштабувати CoreDNS до 0) і впізнати симптоми.
- **Перевірити себе:** `kubectl exec tmp -- nslookup api.app` повертає ClusterIP.
- **Пастка:** коротке ім'я з іншого простору не резолвиться — потрібно `api.app`.

### День 3. Ingress (Use Ingress rules to expose applications)

- **Навіщо.** Один вхід HTTP(S) на кластер з маршрутизацією за хостом і шляхом.
- **Що це.** Ingress — правила; працюють лише з контролером Ingress (у k3s — Traefik). `ingressClassName`, правила
  `host`/`path` з `pathType`, `tls` з секретом.
- **Читати:** `Ingress`; `Ingress Controllers`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) Ingress: `/` → фронт, `/api` → API, хост `app.localhost`; 2) TLS із самопідписаним сертифікатом з
  плану Linux; 3) Ingress з неіснуючим класом — знайти, чому не працює.
- **Перевірити себе:** `curl -k https://app.localhost/api/health` — 200.
- **Пастка:** `pathType: Exact` на `/api` — запити `/api/health` не підходять. Для префіксів — `Prefix`.

### День 4. Gateway API

- **Навіщо.** Наступник Ingress: CKA прямо питає «Use the Gateway API to manage Ingress traffic», і нові кластери
  переходять на нього.
- **Що це.** Ролі розділено: GatewayClass (реалізація), Gateway (вхід — порти, TLS), HTTPRoute (маршрути до сервісів,
  ваги, заголовки). Traefik у k3s підтримує Gateway API провайдером.
- **Читати:** `Gateway API`; `Gateway API: Getting started with Gateway API`; `Gateway API: HTTP routing`;
  `Gateway API: HTTPRoute`; `Gateway API: Migrating from Ingress`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) встановити CRD Gateway API й увімкнути провайдер у Traefik; 2) Gateway і HTTPRoute, що повторюють
  Ingress дня 3; 3) прибрати Ingress.
- **Перевірити себе:** `kubectl get gateway,httproute` — `Programmed`/`Accepted`; `curl` як учора.
- **Пастка:** HTTPRoute у просторі, з якого Gateway не дозволяє маршрути (`allowedRoutes`), — маршрут не
  приймається, і причина лише в `status` маршруту.

### День 5. NetworkPolicy (Demonstrate basic understanding of NetworkPolicies)

- **Навіщо.** За замовчуванням будь-який под говорить з будь-яким — і зламаний фронт дістає до бази.
- **Що це.** NetworkPolicy вибирає поди (`podSelector`) і дозволяє вхідний (`ingress`) чи вихідний (`egress`)
  трафік від/до подів, просторів, блоків IP і портів. Щойно под вибраний політикою певного типу — усе не дозволене
  заборонено. Працює лише з CNI, що підтримує політики (у k3s — вбудований контролер).
- **Читати:** `Network Policies`; `Declare Network Policy`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) «заборонити все» на вхід у просторі `app`; 2) дозволити фронт → API і API → база на 5432;
  3) заборонити вихід бази в інтернет; 4) не забути DNS для egress.
- **Перевірити себе:** з пода фронту `nc -zv db 5432` — тайм-аут; з API — успіх.
- **Пастка:** політика egress без дозволу на порт 53 до CoreDNS — під перестає резолвити імена, і все виглядає як
  «мережа впала».

### День 6. Доступ і діагностика (Provide and troubleshoot access to applications via services)

- **Навіщо.** «Сервіс не відповідає» — щоденна задача й половина задач іспиту про мережу.
- **Що це.** Ланцюг: под готовий? → сервіс має ендпоінти? → порт правильний? → DNS? → політика? → Ingress/Gateway?
  `kubectl port-forward`, тимчасовий под `kubectl run tmp --rm -it --image=busybox -- sh`.
- **Читати:** `Debug Services`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** напарник (або ви самі) ламає одне з п'яти: селектор, `targetPort`, readiness, NetworkPolicy, клас
  Ingress. Знайти кожне за п'ять хвилин.
- **Перевірити себе:** у журналі — команда, що показала причину, для кожної поломки.
- **Пастка:** `kubectl port-forward` працює, а сервіс — ні: port-forward іде прямо в под повз сервіс і політики.

# Фаза 4. Розгортання — 6 днів

**Сервери MCP фази:** `kubernetes-docs`.

Розділ Application Deployment — 20 % CKAD: стратегії розгортання (blue/green, canary), оновлення Deployment, Helm,
Kustomize.

### День 1. Оновлення й відкат (Understand Deployments and how to perform rolling updates)

- **Навіщо.** Нова версія без простою, і повернення за хвилину, якщо вона зламана.
- **Що це.** Стратегія `RollingUpdate` з `maxSurge` і `maxUnavailable`; `Recreate`. `minReadySeconds`,
  `progressDeadlineSeconds`. `kubectl rollout status/history/undo --to-revision`, `pause`/`resume`. Анотація
  `kubernetes.io/change-cause`.
- **Читати:** `Deployments` — розділи про оновлення, відкат і стратегії.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) `maxSurge: 1, maxUnavailable: 0` і оновлення під навантаженням `curl` у циклі без жодної помилки;
  2) оновити на неіснуючий образ — оновлення застрягає, старі поди живуть; 3) відкат на конкретну ревізію.
- **Перевірити себе:** цикл `curl` під час кроку 1 — нуль помилок; після кроку 2 — `rollout status` повідомляє про
  перевищення дедлайну.
- **Пастка:** без readiness-проби (фаза 5) «нуль простою» не працює: новий под отримує трафік до того, як готовий.

### День 2. Blue/green і canary (Use Kubernetes primitives to implement common deployment strategies)

- **Навіщо.** Іспит питає зробити це самими примітивами — двома Deployment і сервісом.
- **Що це.** Blue/green — два Deployment з мітками `version: blue|green`, сервіс перемикає селектор. Canary — два
  Deployment з однаковою міткою `app` і різною кількістю реплік (частка трафіку ≈ частка реплік), або вагами
  HTTPRoute у Gateway API.
- **Читати:** `Managing Workloads` — розділ про canary; `Gateway API: HTTP traffic splitting`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) blue/green для API з перемиканням селектора сервісу; 2) canary 1 з 5 реплік; 3) canary 10 %
  вагами HTTPRoute.
- **Перевірити себе:** 100 запитів `curl` на canary — близько 10 відповідей нової версії.
- **Пастка:** у blue/green сервіс вибирає лише за `app` — і трафік іде в обидві версії одночасно.

### День 3. Helm (Use the Helm package manager to deploy existing packages)

- **Навіщо.** Готові компоненти (бази, контролери, моніторинг) ставлять чартами; CKAD питає встановити наявний.
- **Що це.** Чарт — шаблони маніфестів з `values.yaml`; реліз — встановлений чарт. `helm repo add`, `helm search
  repo`, `helm show values`, `helm install -f values.yaml --set`, `helm upgrade --install`, `helm rollback`, `helm
  list -A`, `helm uninstall`. Helm 4 — поточна лінія.
- **Читати:** `Helm: Quickstart Guide`; `Helm: Using Helm`; `Helm: Helm Commands`; `Helm: helm install`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) встановити PostgreSQL чартом з власними значеннями замість StatefulSet фази 1; 2) оновити значення;
  3) відкотити реліз.
- **Перевірити себе:** `helm history` — три ревізії; `helm get values` — ваші значення.
- **Пастка:** `helm upgrade` без `-f` тих самих values — значення повертаються до типових чарту (`--reuse-values`
  має свої пастки — краще завжди передавати файл).

### День 4. Власний чарт

- **Навіщо.** Проєкт для кількох середовищ одним пакетом.
- **Що це.** `helm create`, шаблони з `{{ .Values }}`, `_helpers.tpl`, `helm template` і `helm lint` для перевірки
  без кластера, хуки (міграції як `pre-upgrade`).
- **Читати:** `Helm: Charts`; `Helm: Chart Template Guide`; `Helm: Chart Hooks`; `Helm: helm create`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** чарт проєкту з фронтом і API, база — залежністю; Job міграції — хуком `pre-upgrade`.
- **Перевірити себе:** `helm lint` чисто; `helm upgrade --install` з чистого кластера піднімає проєкт.
- **Пастка:** хук без `hook-delete-policy` — наступний `upgrade` падає, бо Job з таким іменем уже є.

### День 5. Kustomize (Kustomize)

- **Навіщо.** Інший підхід: без шаблонів, база й накладки для середовищ; вбудований у `kubectl`.
- **Що це.** `kustomization.yaml`: `resources`, `namePrefix`, `commonLabels`/`labels`, `images` (заміна тегу),
  `configMapGenerator`/`secretGenerator` (з хешем в імені — поди перезапускаються при зміні), `patches`. Оверлеї
  `overlays/dev`, `overlays/prod` поверх `base`. `kubectl apply -k`, `kubectl kustomize`.
- **Читати:** `Declarative Management of Kubernetes Objects Using Kustomize`; `kubectl book: The Kustomization
  File`; `kubectl book: patches`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** `k8s/base` з фази 1 стає базою; оверлеї `dev` (1 репліка, без лімітів) і `prod` (3 репліки, ліміти,
  інший тег).
- **Перевірити себе:** `kubectl kustomize k8s/overlays/prod | grep replicas` — 3; `apply -k` працює.
- **Пастка:** змінити ConfigMap, згенерований `configMapGenerator`, — ім'я з новим хешем, старий лишається в
  кластері, поки його не прибрати (`--prune` чи руками).

### День 6. Автомасштабування

- **Навіщо.** Кількість реплік за навантаженням — і пункт `Configure workload autoscaling` програми CKA.
- **Що це.** HorizontalPodAutoscaler (`autoscaling/v2`) змінює кількість реплік за метриками процесора, пам'яті чи
  власними; потребує metrics-server і запитів ресурсів у подах. `behavior` — швидкість масштабування.
- **Читати:** `Horizontal Pod Autoscaling`; `HorizontalPodAutoscaler Walkthrough`; `metrics-server: Kubernetes
  Metrics Server`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) HPA для API: 2–6 реплік, 60 % процесора; 2) навантаження — масштабування вгору; 3) прибрати
  навантаження — масштабування вниз після вікна стабілізації.
- **Перевірити себе:** `kubectl get hpa -w` — ріст реплік під навантаженням.
- **Пастка:** HPA показує `<unknown>` — немає запитів процесора в подах або не працює metrics-server.

# Фаза 5. Спостереження й налагодження — 5 днів

**Сервери MCP фази:** `kubernetes-docs`.

Розділ Application Observability and Maintenance — 15 % CKAD: застарілі API, проби, вбудовані засоби моніторингу,
журнали контейнерів, налагодження.

### День 1. Проби (Implement probes and health checks)

- **Навіщо.** Kubernetes має знати, коли под готовий приймати трафік і коли він завис.
- **Що це.** `startupProbe` (повільний старт), `readinessProbe` (чи слати трафік — под без готовності випадає з
  ендпоінтів), `livenessProbe` (чи перезапустити). Типи: `httpGet`, `tcpSocket`, `exec`, `grpc`; параметри
  `initialDelaySeconds`, `periodSeconds`, `failureThreshold`.
- **Читати:** `Configure Liveness, Readiness and Startup Probes`; `Pod Lifecycle` — розділ про проби.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) три проби для API на `/readyz` і `/healthz` (ендпоінти з плану Docker, фаза 6); 2) зламати
  готовність — под зникає з ендпоінтів, але живе; 3) зламати liveness — под перезапускається.
- **Перевірити себе:** оновлення з фази 4 тепер під навантаженням без жодної помилки.
- **Пастка:** liveness перевіряє базу — база впала, і Kubernetes перезапускає всі поди API, які були здорові. Liveness
  — лише про сам процес.

### День 2. Журнали (Utilize container logs)

- **Навіщо.** Перше, куди дивляться при будь-якій проблемі.
- **Що це.** `kubectl logs под [-c контейнер] [--previous] [-f] [--since] [--tail]`, `-l мітка` для кількох подів,
  `--all-containers`. Журнали контейнерів лежать на вузлі (kubelet ротує їх); центральний збір — окремий стек.
- **Читати:** `Logging Architecture`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) журнал попереднього екземпляра впалого контейнера; 2) журнали всіх реплік API однією командою;
  3) знайти файли журналів на вузлі k3d.
- **Перевірити себе:** `kubectl logs -l app=api --prefix --tail=5` — по п'ять рядків з кожного пода.
- **Пастка:** застосунок пише журнал у файл, а не в stdout — `kubectl logs` порожній.

### День 3. Засоби моніторингу (Use built-in CLI tools to monitor Kubernetes applications)

- **Навіщо.** Хто скільки їсть зараз і що відбувалося хвилину тому.
- **Що це.** `kubectl top pods/nodes` (metrics-server), `kubectl get events --sort-by=.lastTimestamp`, `kubectl get
  -w`, `kubectl describe`, `-o custom-columns`, `jsonpath`.
- **Читати:** `Resource metrics pipeline`; `Tools for Monitoring Resources`; `kubectl Quick Reference` — розділ про
  форматування виводу.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) три поди з найбільшою пам'яттю у всьому кластері; 2) події простору за останню годину,
  відсортовані; 3) таблиця «под, вузол, образ, рестарти» через `custom-columns`.
- **Перевірити себе:** одна команда для кожного пункту — у журналі.
- **Пастка:** `kubectl top` показує фактичне споживання, а не запити — і не пояснює, чому под не планується.

### День 4. Налагодження (Debugging in Kubernetes)

- **Навіщо.** Под не стартує, падає, не відповідає — і треба знайти причину за хвилини.
- **Що це.** Стани й причини: `Pending` (ресурси, PVC, taint), `ImagePullBackOff`, `CrashLoopBackOff`,
  `CreateContainerConfigError` (немає ConfigMap/Secret), `OOMKilled`. `kubectl describe` (Events), `logs --previous`,
  `exec`, `kubectl debug` (ефемерний контейнер у под без оболонки, копія пода, вузол).
- **Читати:** `Debug Pods`; `Debug Running Pods`; `Determine the Reason for Pod Failure`; `Ephemeral Containers`;
  `Troubleshooting Applications`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** вісім поломок (кожен стан вище, плюс під без оболонки, якому треба `kubectl debug`) — знайти кожну.
- **Перевірити себе:** для кожної — команда й рядок виводу з причиною.
- **Пастка:** видалити й створити заново замість читати `describe` — проблема повертається, а причина губиться.

### День 5. Застарілі API (Understand API deprecations)

- **Навіщо.** Маніфест з `extensions/v1beta1` не застосується в сучасному кластері; іспит питає оновити.
- **Що це.** Політика застарівання: бета-API живуть щонайменше 3 випуски після застарівання; міграційний посібник
  перелічує, що прибрано в якій версії. `kubectl explain` показує поточну версію, `kubectl convert` (плагін)
  переписує маніфести.
- **Читати:** `Kubernetes Deprecation Policy`; `Deprecated API Migration Guide`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** взяти маніфести Deployment, Ingress і HPA старих версій API (`extensions/v1beta1`,
  `autoscaling/v2beta2`) і привести до 1.37.
- **Перевірити себе:** `kubectl apply --dry-run=server` для всіх — без помилок.
- **Пастка:** змінити лише `apiVersion` — у нових версіях змінилися й поля (Ingress `backend.serviceName` →
  `backend.service.name`).

# Фаза 6. Іспит CKAD — 4 дні

**Сервери MCP фази:** `kubernetes-docs`.

### День 1. Стратегія й перша пробна

- **Навіщо.** Формат до того, як заплачено.
- **Що це.** Правила, що економлять бали: перша команда — контекст з умови; простір імен у кожній команді;
  імперативно + `--dry-run=client -o yaml`; YAML — копіювати з kubernetes.io/docs, а не писати; задача понад 8 хвилин
  — позначка і далі; перевіряти результат командою.
- **Читати:** документ `CKAD Curriculum v1.33, v1.34, v1.35, v1.37` — позначити слабкі пункти; Candidate Handbook і
  Important Instructions (поза корпусом).
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** пробний іспит із 16 задач, пропорційно вагам розділів, на чистому кластері k3d за 2 години.
- **Перевірити себе:** бали й список задач понад 8 хвилин.
- **Пастка:** витратити 20 хвилин на задачу з вагою 2 %.

### День 2. Слабкі місця

- **Навіщо.** Лише туди, де втрачено час.
- **Що це.** Повтор днів плану, що відповідають повільним задачам; закладки на сторінки kubernetes.io/docs, з яких
  ви копіювали YAML.
- **Читати:** сторінки документації повільних задач.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** кожна слабка задача — тричі з чистого кластера, поки не вкладеться в 6 хвилин.
- **Перевірити себе:** другий пробний іспит — понад 80 %.
- **Пастка:** вчити YAML напам'ять. Пам'ятати треба, на якій сторінці документації він лежить.

### День 3. Симулятор Killer.sh

- **Навіщо.** Задачі складніші за справжні, середовище — як на іспиті.
- **Що це.** Дві спроби по 36 годин доступу; після — розбір кожної задачі.
- **Читати:** розбори симулятора.
- **Сервери MCP:** жодного — джерела дня поза фабрикою.
- **Зробити:** перша спроба за 2 години, потім розбір і повтор незарахованого, поки доступ не скінчився; через день —
  друга.
- **Перевірити себе:** друга спроба на третину швидша.
- **Пастка:** обидві спроби в один вечір.

### День 4. Іспит CKAD

- **Навіщо.** Скласти.
- **Що це.** Іспит під наглядом через браузер; середовище — віддалений робочий стіл з терміналом і браузером
  документації.
- **Читати:** Important Instructions CKAD — у день реєстрації.
- **Сервери MCP:** жодного — джерела дня поза фабрикою.
- **Зробити:** перевірка системи заздалегідь, іспит, за потреби — повторна спроба.
- **Перевірити себе:** сертифікат CKAD у профілі Linux Foundation і в резюме.
- **Пастка:** почати з довгої задачі з малою вагою.

# Частина B. CKA — сам кластер

# Фаза 7. Кластер з нуля: kubeadm, CNI, HA — 8 днів

**Сервери MCP фази:** `kubernetes-docs`.

Розділ Cluster Architecture, Installation and Configuration — 25 % CKA: RBAC, підготовка інфраструктури, kubeadm,
життєвий цикл, HA площини керування, Helm і Kustomize для компонентів, інтерфейси розширення, CRD й оператори.

### День 1. Архітектура кластера

- **Навіщо.** Без картини компонентів пошук несправностей (30 % CKA) — вгадування.
- **Що це.** Площина керування: apiserver, etcd, scheduler, controller-manager (у kubeadm — статичні поди з
  `/etc/kubernetes/manifests`). Вузол: kubelet (служба systemd), containerd (CRI), kube-proxy (DaemonSet), CNI-плагін.
  Порти й протоколи між ними. Лізинги для обрання лідера.
- **Читати:** `Cluster Architecture`; `Kubernetes Components`; `Nodes`; `Ports and Protocols`; `Leases`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** намалювати (у README, ASCII) кластер з трьох вузлів: кожен компонент, де він працює, хто кого кличе і
  на якому порту.
- **Перевірити себе:** ви пояснюєте шлях `kubectl apply -f deploy.yaml` до запущеного контейнера через усі
  компоненти.
- **Пастка:** вважати kubelet подом — це служба systemd на вузлі, і полагодити його через kubectl не можна.

### День 2. Підготовка вузлів (Prepare underlying infrastructure for installing a Kubernetes cluster)

- **Навіщо.** kubeadm мовчки не працює на машині, де вимкнено пересилання пакетів чи ввімкнено swap.
- **Що це.** Три нові машини Ubuntu 24.04 з плану Linux: унікальні імена й MAC, `br_netfilter` і `overlay` в
  модулях, `net.ipv4.ip_forward=1`, containerd з `SystemdCgroup = true`, swap — вимкнено або налаштовано, відкриті
  порти. Потім `kubeadm`, `kubelet`, `kubectl` з репозиторію pkgs.k8s.io для потрібної лінії й `apt-mark hold`.
- **Читати:** `Installing kubeadm`; `Container Runtimes`; `Linux Kernel Version Requirements`; план Linux — фаза 3,
  дні 6 і 8.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** підготувати `cp1`, `w1`, `w2` на лінію 1.36 скриптом у репозиторії (щоб повторити за хвилини).
- **Перевірити себе:** на кожній — `containerd config dump | grep SystemdCgroup` — `true`; `sysctl
  net.ipv4.ip_forward` — 1; `kubeadm version` — 1.36.
- **Пастка:** різні драйвери cgroup у kubelet і containerd — вузол то `Ready`, то ні, і поди перезапускаються без
  видимої причини.

### День 3. kubeadm init і join (Create and manage Kubernetes clusters using kubeadm)

- **Навіщо.** Головна навичка CKA і основа розуміння будь-якого кластера.
- **Що це.** `kubeadm init --pod-network-cidr … --kubernetes-version …` на `cp1`: сертифікати, статичні поди, токен
  приєднання; kubeconfig адміністратора; `kubeadm join` на робочих вузлах; `kubeadm token create
  --print-join-command`. Фази init і `kubeadm config print init-defaults`.
- **Читати:** `Creating a cluster with kubeadm`; `Troubleshooting kubeadm`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) `kubeadm init` на `cp1`; 2) приєднати `w1`; 3) через годину приєднати `w2` новим токеном.
- **Перевірити себе:** `kubectl get nodes` — три вузли, поки `NotReady` (немає CNI — це наступний день).
- **Пастка:** `--pod-network-cidr` перетинається з мережею машин — після встановлення CNI маршрути ламаються так,
  що причину важко впізнати.

### День 4. Мережа подів: CNI (Understand extension interfaces (CNI, CSI, CRI, etc.))

- **Навіщо.** Без CNI вузли `NotReady`, а поди без адрес.
- **Що це.** CNI-плагін (Calico, Cilium, Flannel) дає подам адреси й маршрути між вузлами; від нього залежать
  NetworkPolicy. CSI — плагіни сховищ (фаза 10), CRI — рантайм (`crictl`). Документація самих плагінів — поза
  корпусом.
- **Читати:** `Network Plugins`; `Cluster Networking`; `Container Runtime Interface (CRI)`; `Troubleshooting CNI
  plugin-related errors`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) встановити Calico (маніфестом чи оператором) з тим самим CIDR, що в init; 2) переконатися, що
  NetworkPolicy з фази 3 працюють; 3) `crictl ps` на вузлі.
- **Перевірити себе:** вузли `Ready`; поди CoreDNS `Running`; под на `w1` пінгує под на `w2`.
- **Пастка:** два CNI одночасно (залишки першого в `/etc/cni/net.d`) — поди отримують адреси не того плагіна.

### День 5. Helm і Kustomize для компонентів (Use Helm and Kustomize to install cluster components)

- **Навіщо.** Компоненти кластера (контролер Ingress, metrics-server, cert-manager) ставлять так само, як застосунки.
- **Що це.** `helm install` з `--namespace --create-namespace` і власними значеннями; Kustomize поверх офіційних
  маніфестів компонента (патч ресурсів чи аргументів).
- **Читати:** `Helm: Using Helm`; `metrics-server: Kubernetes Metrics Server`; `cert-manager: Installation`;
  `kubectl book: patches`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) metrics-server чартом (з `--kubelet-insecure-tls` для лабораторного кластера); 2) Traefik чи інший
  контролер Ingress/Gateway чартом; 3) cert-manager маніфестами через Kustomize з патчем ресурсів.
- **Перевірити себе:** `kubectl top nodes` працює; `helm list -A` — ваші релізи.
- **Пастка:** `--kubelet-insecure-tls` в робочому кластері — вимкнена перевірка сертифікатів kubelet; лише для
  лабораторії.

### День 6. HA площини керування (Implement and configure a highly-available control plane)

- **Навіщо.** Один вузол керування — одна точка відмови; CKA питає розуміння й налаштування HA.
- **Що це.** Кілька вузлів керування за балансувальником (HAProxy з плану Linux, фаза 5, день 10) на порту 6443;
  etcd — «складений» (на тих самих вузлах) або зовнішній; `--control-plane-endpoint` у init, `kubeadm join
  --control-plane --certificate-key`. Кворум etcd: 3 з 3 живуть з втратою одного.
- **Читати:** `Options for Highly Available Topology`; `Creating Highly Available Clusters with kubeadm`; `Set up a
  High Availability etcd Cluster with kubeadm`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** другий кластер з нуля: HAProxy на окремій машині, три вузли керування, один робочий; вимкнути один
  вузол керування — кластер працює.
- **Перевірити себе:** `kubectl get nodes` — три control-plane; після вимкнення одного `kubectl get pods -A`
  відповідає.
- **Пастка:** `init` без `--control-plane-endpoint` — перетворити кластер на HA потім неможливо без перевстановлення.

### День 7. CRD й оператори з боку адміністратора (Understand CRDs, install and configure operators)

- **Навіщо.** Адміністратор ставить оператори й стежить за їхніми CRD і правами.
- **Що це.** Оператор = CRD + контролер (Deployment) + RBAC; встановлення чартом чи маніфестами; оновлення CRD —
  окремий крок (Helm не оновлює CRD з `crds/`).
- **Читати:** `Operator pattern`; `Custom Resources`; `Gateway API: CRD Management`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** поставити оператор бази (CloudNativePG чи інший — поза корпусом) і створити ним кластер PostgreSQL для
  проєкту; знайти його CRD, ServiceAccount і ClusterRole.
- **Перевірити себе:** `kubectl get crd | grep` оператор; під бази, створений оператором, `Running`.
- **Пастка:** оновити чарт оператора й вважати, що оновилися CRD, — Helm їх не чіпає, і новий контролер падає на
  старій схемі.

### День 8. Підсумок фази

- **Навіщо.** Кластер з нуля скриптом за 20 хвилин — і проєкт у ньому.
- **Що це.** Скрипти фази 7 у репозиторії, повторені з чистих знімків.
- **Читати:** нотатки фази.
- **Сервери MCP:** жодного — джерела дня поза фабрикою.
- **Зробити:** від порожніх машин до проєкту в кластері kubeadm — скриптами й `helm`/`kubectl apply -k`; час — у
  журнал.
- **Перевірити себе:** проєкт працює в кластері kubeadm так само, як у k3d.
- **Пастка:** лишити у скриптах ручні кроки «а тут я ще щось поправив» — на третій раз вони забуваються.

# Фаза 8. Життєвий цикл кластера й доступ — 5 днів

**Сервери MCP фази:** `kubernetes-docs`.

Той самий розділ CKA: `Manage the lifecycle of Kubernetes clusters` і `Manage role based access control (RBAC)`.

### День 1. Оновлення кластера (Manage the lifecycle of Kubernetes clusters)

- **Навіщо.** Найчастіша задача CKA і щорічна робота адміністратора.
- **Що це.** Порядок: `kubeadm` на першому вузлі керування → `kubeadm upgrade plan` → `kubeadm upgrade apply v1.37.x`
  → `drain` вузла → `kubelet` і `kubectl` → `uncordon`; на інших вузлах — `kubeadm upgrade node`. Лише на одну
  мінорну версію за раз; репозиторій pkgs.k8s.io — свій на кожну лінію.
- **Читати:** `Upgrading kubeadm clusters`; `Safely Drain a Node`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** оновити кластер з фази 7 з 1.36 до 1.37 під навантаженням проєкту.
- **Перевірити себе:** `kubectl get nodes` — усі 1.37; проєкт не мав простою (цикл `curl`).
- **Пастка:** забути змінити репозиторій pkgs.k8s.io на нову лінію — `apt` не бачить нових версій, і здається, що
  оновлення «немає».

### День 2. Резервна копія і відновлення etcd

- **Навіщо.** Стан кластера — це etcd; без копії зламаний кластер не повернути.
- **Що це.** `etcdctl snapshot save` з сертифікатами з `/etc/kubernetes/pki/etcd/`; відновлення — `etcdutl snapshot
  restore` у нову теку даних і правка маніфесту статичного пода etcd на неї.
- **Читати:** `Operating etcd clusters for Kubernetes` — розділи про резервні копії й відновлення.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) знімок etcd; 2) видалити простір проєкту; 3) відновити знімок і побачити простір знову.
- **Перевірити себе:** після відновлення `kubectl get ns` — простір проєкту на місці.
- **Пастка:** відновити в ту саму теку даних поверх живого etcd — або правка маніфесту не підхоплюється, або etcd не
  стартує. Нова тека й зміна `hostPath` у маніфесті.

### День 3. Сертифікати

- **Навіщо.** Сертифікати kubeadm діють рік; прострочені — кластер «раптом» перестає відповідати.
- **Що це.** `kubeadm certs check-expiration`, `kubeadm certs renew all` і перезапуск статичних подів; оновлення
  кластера теж поновлює сертифікати. CSR API для сертифікатів користувачів.
- **Читати:** `Certificate Management with kubeadm`; `Certificates and Certificate Signing Requests`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) подивитися строки; 2) поновити всі й перевірити, що apiserver підхопив нові; 3) сертифікат для
  користувача `dev` через CSR API.
- **Перевірити себе:** `kubeadm certs check-expiration` — нові дати; `kubectl get csr` — `Approved,Issued`.
- **Пастка:** поновити сертифікати й не перезапустити статичні поди — вони працюють зі старими до перезапуску.

### День 4. Користувачі й RBAC (Manage role based access control (RBAC))

- **Навіщо.** Розробникам — доступ лише до свого простору; CI — лише на розгортання.
- **Що це.** Користувач у Kubernetes — це сертифікат (CN — ім'я, O — групи) чи токен; Role/ClusterRole з
  `rules`, прив'язки до користувачів і груп; `kubectl auth can-i --as`; kubeconfig для користувача.
- **Читати:** `Using RBAC Authorization`; `Certificates and Certificate Signing Requests` — розділ про звичайного
  користувача.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** kubeconfig для `dev` (сертифікат з дня 3): повні права в `app`, лише читання в `kube-system`, нічого
  на рівні кластера.
- **Перевірити себе:** `kubectl --kubeconfig dev.conf get nodes` — Forbidden; `… -n app delete pod …` — працює.
- **Пастка:** група `system:masters` у сертифікаті — обходить RBAC повністю, і відкликати це неможливо, лише
  замінити CA.

### День 5. Обслуговування вузлів

- **Навіщо.** Вузол на обслуговування, новий вузол у кластер, вузол з кластера — без простою застосунків.
- **Що це.** `kubectl cordon`, `drain --ignore-daemonsets --delete-emptydir-data`, `uncordon`; PodDisruptionBudget —
  скільки подів можна виселити одночасно; видалення вузла (`kubectl delete node`, `kubeadm reset` на ньому).
- **Читати:** `Safely Drain a Node`; `Specifying a Disruption Budget for your Application`;
  `Nodes`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) PDB для API (мінімум 2 доступні); 2) `drain` вузла з репліками API; 3) прибрати вузол з кластера й
  повернути заново.
- **Перевірити себе:** під час `drain` доступних реплік API не менше двох; вузол повернувся `Ready`.
- **Пастка:** PDB з `minAvailable`, рівним кількості реплік, — `drain` чекає вічно.

# Фаза 9. Планування й автомасштабування — 4 дні

**Сервери MCP фази:** `kubernetes-docs`.

Розділ Workloads and Scheduling — 15 % CKA. Розгортання, ConfigMap, Secret і автомасштабування ви знаєте з частини A;
тут — те, чого не було: `Configure Pod admission and scheduling (limits, node affinity, etc.)`.

### День 1. Вибір вузла

- **Навіщо.** База — на вузлі з SSD, агент — на кожному вузлі, дві репліки — не на одному.
- **Що це.** `nodeSelector`; `nodeAffinity` (`required…`/`preferred…`); `podAffinity`/`podAntiAffinity` за
  `topologyKey`; `topologySpreadConstraints`; `nodeName` (повз планувальник).
- **Читати:** `Assigning Pods to Nodes`; `Pod Topology Spread Constraints`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) мітка `disk=ssd` на `w1` і база лише там; 2) репліки API — на різних вузлах; 3) рівномірний
  розподіл фронту.
- **Перевірити себе:** `kubectl get pods -o wide` — розміщення як задумано.
- **Пастка:** `requiredDuringScheduling…` з міткою, якої немає на жодному вузлі, — под вічно `Pending`.

### День 2. Taints і tolerations

- **Навіщо.** Вузли «лише для своїх»: вузли керування, вузли з GPU, вузол на обслуговуванні.
- **Що це.** Taint на вузлі (`key=value:NoSchedule|PreferNoSchedule|NoExecute`) відштовхує поди без відповідного
  toleration. Вузли керування мають taint `node-role.kubernetes.io/control-plane`. `NoExecute` виселяє вже запущені.
- **Читати:** `Taints and Tolerations`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) taint `w2` під «спеціальні» навантаження; 2) под з toleration і nodeAffinity — лише туди;
  3) `NoExecute` на вузлі з подами — побачити виселення.
- **Перевірити себе:** на `w2` лише поди з toleration; після `NoExecute` інші поди переїхали.
- **Пастка:** toleration не притягує под на вузол — лише дозволяє. Щоб «лише туди», потрібна ще й affinity.

### День 3. Пріоритети, ресурси вузлів і статичні поди

- **Навіщо.** Що буде, коли вузол заповнений, і як площина керування запускається без площини керування.
- **Що це.** PriorityClass і витіснення; alocatable вузла проти capacity; виселення за тиском пам'яті й диска
  kubelet-ом. Статичні поди — маніфести в `/etc/kubernetes/manifests`, які kubelet запускає сам.
- **Читати:** `Pod Priority and Preemption`; `Create static Pods`; `Node-pressure Eviction`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) PriorityClass для бази й заповнений кластер — під бази витісняє менш важливі; 2) статичний под на
  `w1`; 3) спробувати видалити його через kubectl.
- **Перевірити себе:** `kubectl get pods` показує статичний под з суфіксом імені вузла, і після `delete` він
  повертається.
- **Пастка:** правити статичний под через `kubectl edit` — дзеркальний об'єкт не змінює файл; правка — лише у файлі
  на вузлі.

### День 4. Автомасштабування й допуск подів (Configure workload autoscaling)

- **Навіщо.** HPA з частини A — тепер з боку адміністратора: метрики, межі, поведінка під навантаженням.
- **Що це.** HPA `autoscaling/v2` з `behavior` (вікна стабілізації, політики кроку); VPA і автомасштабування вузлів —
  поза програмою, але варто знати, що вони є. LimitRange і квоти як частина допуску (частина A, фаза 2).
- **Читати:** `Horizontal Pod Autoscaling`; `Limit Ranges`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** HPA для API з повільним масштабуванням вниз і швидким вгору; перевірити під навантаженням.
- **Перевірити себе:** `kubectl describe hpa` — події масштабування з вашими кроками.
- **Пастка:** HPA і ручний `kubectl scale` на тому самому Deployment — HPA повертає свою кількість за хвилину.

# Фаза 10. Сховища — 3 дні

**Сервери MCP фази:** `kubernetes-docs`.

Розділ Storage — 10 % CKA: класи сховищ і динамічне створення томів, типи томів, режими доступу й політики
повернення, PV і PVC.

### День 1. StorageClass і динамічні томи (Implement storage classes and dynamic volume provisioning)

- **Навіщо.** У кластері kubeadm сховища «з коробки» немає — його ставить адміністратор.
- **Що це.** StorageClass вказує provisioner (CSI-драйвер), параметри, `reclaimPolicy`, `volumeBindingMode`
  (`WaitForFirstConsumer` — створити том там, де под), `allowVolumeExpansion`; типовий клас — анотацією.
- **Читати:** `Storage Classes`; `Dynamic Volume Provisioning`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) поставити local-path-provisioner (чи NFS CSI з NFS-сервером з плану Linux); 2) зробити клас
  типовим; 3) PVC без класу — том створюється сам.
- **Перевірити себе:** `kubectl get sc` — `(default)`; PVC `Bound` без ручного PV.
- **Пастка:** два типові класи — PVC без класу отримує випадковий з них.

### День 2. Режими доступу й політики повернення (Configure volume types, access modes and reclaim policies)

- **Навіщо.** Що буде з даними після видалення PVC — і хто може писати в том одночасно.
- **Що це.** `ReadWriteOnce` (один вузол), `ReadOnlyMany`, `ReadWriteMany` (NFS), `ReadWriteOncePod`; політики
  `Delete` і `Retain`; том у стані `Released` і як повернути його в роботу; розширення тому.
- **Читати:** `Persistent Volumes` — розділи про режими доступу, повернення й розширення.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) PV з `Retain`, видалити PVC — дані лишились, PV `Released`; 2) повернути PV у `Available` і
  прив'язати новим PVC; 3) розширити PVC.
- **Перевірити себе:** дані старого PVC читаються з нового; розмір PVC — новий.
- **Пастка:** `ReadWriteOnce` вважають «один под» — це «один вузол»: два поди на одному вузлі пишуть в один том.

### День 3. PV і PVC руками (Manage persistent volumes and persistent volume claims)

- **Навіщо.** Задача іспиту: створити PV певного типу й розміру, PVC до нього, под, що його використовує.
- **Що це.** Статичне зв'язування: клас (чи `""`), розмір, режими, `volumeName` чи селектор міток.
- **Читати:** `Configure a Pod to Use a PersistentVolume for Storage`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** три задачі в стилі іспиту на час: PV hostPath 1Gi RWO, PVC до нього в просторі `prod`, под з
  монтуванням; те саме з NFS; PVC, прив'язаний до конкретного PV за іменем.
- **Перевірити себе:** кожна задача — до 6 хвилин.
- **Пастка:** PVC з типовим класом не зв'язується з вашим PV без класу — у PVC потрібно `storageClassName: ""`.

# Фаза 11. Мережа кластера — 4 дні

**Сервери MCP фази:** `kubernetes-docs`.

Розділ Servicing and Networking — 20 % CKA. Сервіси, Ingress, Gateway API і NetworkPolicy з частини A — тепер на
власному кластері, де контролер і CNI ставите ви.

### День 1. Зв'язок між подами (Understand connectivity between Pods)

- **Навіщо.** Модель мережі Kubernetes: кожен под має адресу, і будь-який под бачить будь-який без NAT.
- **Що це.** CNI роздає адреси з CIDR вузла; маршрути між вузлами (BGP, VXLAN); kube-proxy робить правила
  сервісів (iptables, IPVS чи nftables); EndpointSlices.
- **Читати:** `Cluster Networking`; `Virtual IPs and Service Proxies`; `EndpointSlices`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) знайти CIDR кожного вузла; 2) простежити пакет під→під між вузлами (`tcpdump` з плану Linux);
  3) знайти правила сервісу API в netfilter вузла.
- **Перевірити себе:** у README — шлях пакета від пода фронту до ClusterIP API й до пода на іншому вузлі.
- **Пастка:** ClusterIP не пінгується — він віртуальний, відповідає лише на порти сервісу.

### День 2. CoreDNS (Understand and use CoreDNS)

- **Навіщо.** Налаштувати DNS кластера: пересилання на корпоративний DNS, власна зона.
- **Що це.** CoreDNS — Deployment у `kube-system` з конфігом Corefile у ConfigMap; плагіни `forward`, `hosts`,
  `rewrite`; заглушка зони.
- **Читати:** `DNS for Services and Pods`; `Debugging DNS Resolution`; `Customizing DNS Service`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) переслати зону `lab.` на DNS машини `ubu` (чи прописати `hosts`); 2) перевірити з пода.
- **Перевірити себе:** `nslookup rocky.lab` з пода повертає адресу машини.
- **Пастка:** синтаксична помилка в Corefile — поди CoreDNS у `CrashLoopBackOff`, і весь DNS кластера лежить.

### День 3. Ingress і Gateway API на власному кластері

- **Навіщо.** Пункти програми `Use the Gateway API to manage Ingress traffic` і `Know how to use Ingress controllers
  and Ingress resources`. На kubeadm немає ні контролера Ingress, ні зовнішніх адрес — усе ставить адміністратор.
- **Що це.** Контролер Ingress/Gateway (Traefik, ingress-nginx, Envoy Gateway) чартом; сервіс контролера як NodePort
  чи LoadBalancer (MetalLB — поза корпусом); IngressClass і GatewayClass.
- **Читати:** `Ingress Controllers`; `Gateway API: Deploying a simple Gateway`; `Gateway API: Getting started with
  Gateway API`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** контролер з підтримкою Gateway API, Gateway з TLS (cert-manager з власним CA), HTTPRoute проєкту.
- **Перевірити себе:** `curl --cacert ca.crt https://app.lab` через NodePort чи адресу балансувальника — 200.
- **Пастка:** Gateway без контролера, що реалізує його GatewayClass, — об'єкт створено, але `status` порожній.

### День 4. Сервіси й політики

- **Навіщо.** Пункти програми `Use ClusterIP, NodePort, LoadBalancer service types and endpoints` і
  `Define and enforce Network Policies`. Повтор частини A у стилі CKA: швидко, на чужому кластері, з перевіркою.
- **Що це.** Сервіси без селектора з ручними EndpointSlices; політики за просторами (`namespaceSelector`) і блоками
  IP.
- **Читати:** `Service` — розділ про сервіси без селектора; `Network Policies`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** 1) сервіс без селектора на базу поза кластером (машина `rocky`); 2) політика: до API лише з
  простору `frontend` і з адрес моніторингу.
- **Перевірити себе:** під з простору `frontend` доходить до API, з `default` — ні.
- **Пастка:** `namespaceSelector` і `podSelector` в одному елементі списку — «І», у двох елементах — «АБО».

# Фаза 12. Пошук несправностей — 6 днів

**Сервери MCP фази:** `kubernetes-docs`.

Розділ Troubleshooting — 30 % CKA, найбільший. Кожен день — серія поломок на кластері kubeadm, які ламаєте ви самі
(або напарник), і пошук на час.

### День 1. Вузли (Troubleshoot clusters and nodes)

- **Навіщо.** `NotReady` — найчастіша задача про вузли.
- **Що це.** `kubectl describe node` (Conditions, події), на вузлі — `systemctl status kubelet`, `journalctl -u
  kubelet`, `crictl`; причини: зупинений kubelet, containerd, повний диск, неправильний конфіг kubelet, сертифікат.
- **Читати:** `Troubleshooting Clusters`; `Debugging Kubernetes nodes with crictl`; `Debugging Kubernetes Nodes With
  Kubectl`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** п'ять поломок `w1`: зупинений kubelet, зупинений containerd, зламаний `/var/lib/kubelet/config.yaml`,
  заповнений диск, неправильний шлях до сертифіката CA.
- **Перевірити себе:** кожна знайдена й виправлена за 6 хвилин.
- **Пастка:** шукати причину `NotReady` у `kubectl` — вона на вузлі, у журналі kubelet.

### День 2. Компоненти кластера (Troubleshoot cluster components)

- **Навіщо.** Зламаний статичний под площини керування — і `kubectl` не відповідає зовсім.
- **Що це.** Маніфести в `/etc/kubernetes/manifests`; без apiserver — лише `crictl ps -a` і `crictl logs` на вузлі
  керування; журнал kubelet; типові поломки — одруківка в маніфесті, неправильний порт etcd, неправильний шлях до
  сертифіката.
- **Читати:** `Troubleshooting Clusters`; `Create static Pods`; `Troubleshooting kubeadm`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** п'ять поломок `cp1`: apiserver з одруківкою в аргументі, scheduler з неіснуючим файлом конфігурації,
  controller-manager зупинений, etcd з неправильною текою даних, kubeconfig адміністратора з неправильним портом.
- **Перевірити себе:** для кожної — команда `crictl`/`journalctl`, що показала причину.
- **Пастка:** правити маніфест статичного пода, лишивши копію `.bak` у тій самій теці, — kubelet запускає обидва.

### День 3. Ресурси (Monitor cluster and application resource usage)

- **Навіщо.** «Повільно» і «не планується» — питання про ресурси.
- **Що це.** `kubectl top`, `describe node` (Allocated resources), запити проти фактичного споживання, `kubectl get
  pods --field-selector=status.phase=Pending`.
- **Читати:** `Resource metrics pipeline`; `Tools for Monitoring Resources`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** знайти: вузол з найбільшою пам'яттю, под з найбільшим процесором у кластері, поди без лімітів, чому
  нова репліка `Pending`.
- **Перевірити себе:** одна команда на кожне питання.
- **Пастка:** судити про заповненість вузла за `top` — планувальник дивиться на запити, а не на споживання.

### День 4. Журнали й потоки виводу (Manage and evaluate container output streams)

- **Навіщо.** Задачі «збережіть журнал контейнера X з помилками у файл».
- **Що це.** `kubectl logs` з фільтрами й перенаправленням (план Linux, фаза 0, день 4), журнали на вузлі
  `/var/log/pods/`, `crictl logs`, журнали контейнерів, яких уже немає.
- **Читати:** `Logging Architecture`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** п'ять задач: рядки з `ERROR` з усіх реплік у файл, журнал попереднього контейнера, журнал
  статичного пода без apiserver, журнал init-контейнера, журнал контейнера, що впав учора (з вузла).
- **Перевірити себе:** кожна — до 3 хвилин.
- **Пастка:** `kubectl logs` пода з кількома контейнерами без `-c` — помилка або журнал не того контейнера.

### День 5. Сервіси й мережа (Troubleshoot services and networking)

- **Навіщо.** Найскладніша категорія поломок — і найчастіша в роботі.
- **Що це.** Ланцюг частини A (фаза 3, день 6) плюс рівень кластера: kube-proxy, CNI, CoreDNS, NetworkPolicy,
  маршрути між вузлами.
- **Читати:** `Debug Services`; `Debugging DNS Resolution`; `Troubleshooting CNI plugin-related errors`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** шість поломок: kube-proxy зупинений на вузлі, CoreDNS масштабований до 0, NetworkPolicy, що ріже
  DNS, неправильний `targetPort`, CNI зламаний на одному вузлі, сервіс з одруківкою в селекторі.
- **Перевірити себе:** кожна знайдена — команда й причина в журналі.
- **Пастка:** перевіряти мережу з вузла, а не з пода, — вузол може бачити те, чого не бачить под (і навпаки).

### День 6. Повний прогін

- **Навіщо.** Пошук несправностей — це вміння вибрати, куди дивитися першим.
- **Що це.** Порядок: що каже `kubectl get` → `describe` (події) → журнали → вузол → компоненти.
- **Читати:** `Troubleshooting Applications`; `Troubleshooting Clusters`.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** напарник (або скрипт, що ламає випадкову річ з дня 1–5) — десять поломок за 60 хвилин.
- **Перевірити себе:** вісім з десяти знайдено в межах часу.
- **Пастка:** перезапускати все підряд — проблема зникає, причина лишається невідомою і повертається.

# Фаза 13. Іспит CKA — 4 дні

**Сервери MCP фази:** `kubernetes-docs`.

### День 1. Стратегія й перша пробна

- **Навіщо.** Формат CKA важчий за CKAD: кластери з поломками, kubeadm, etcd.
- **Що це.** Ті самі правила, що для CKAD (фаза 6), плюс: задачі на вузлах — через `ssh` на вузол з умови і `sudo
  -i`; після правки статичного пода — чекати, доки він підніметься; знімок etcd — сертифікати з маніфесту etcd.
- **Читати:** документ `CKA Curriculum v1.32, v1.33, v1.34, v1.35` — позначити слабкі пункти; Candidate Handbook і
  Important Instructions (поза корпусом).
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** пробний іспит із 17 задач пропорційно вагам, з поломками й оновленням, на кластерах фази 7 за 2 години.
- **Перевірити себе:** бали й задачі понад 8 хвилин.
- **Пастка:** робити задачу на вузлі, не вийшовши з `ssh` попередньої задачі, — не той вузол.

### День 2. Слабкі місця

- **Навіщо.** Лише туди, де втрачено час.
- **Що це.** Повтор днів частини B за повільними задачами; закладки документації.
- **Читати:** сторінки документації повільних задач.
- **Сервери MCP:** `kubernetes-docs`.
- **Зробити:** кожна слабка задача тричі з чистого знімка.
- **Перевірити себе:** другий пробний іспит — понад 80 %.
- **Пастка:** пропустити Troubleshooting як «зрозумілий» — це 30 % балів.

### День 3. Симулятор Killer.sh

- **Навіщо.** Як для CKAD.
- **Що це.** Дві спроби по 36 годин.
- **Читати:** розбори.
- **Сервери MCP:** жодного — джерела дня поза фабрикою.
- **Зробити:** перша спроба, розбір, через день — друга.
- **Перевірити себе:** друга на третину швидша.
- **Пастка:** обидві спроби в один вечір.

### День 4. Іспит CKA

- **Навіщо.** Скласти.
- **Що це.** Як CKAD.
- **Читати:** Important Instructions CKA — у день реєстрації.
- **Сервери MCP:** жодного — джерела дня поза фабрикою.
- **Зробити:** перевірка системи заздалегідь, іспит, за потреби — повторна спроба.
- **Перевірити себе:** сертифікати CKAD і CKA в профілі й у резюме.
- **Пастка:** почати з довгої задачі з малою вагою.

# Після плану

**Що лишається в портфоліо.** Репозиторій з маніфестами проєкту (база й оверлеї Kustomize), власним чартом Helm,
скриптами підняття кластера kubeadm з HA, оновлення й резервної копії etcd, журналом поломок і їхніх причин —
і два сертифікати. Це відповідь на питання «ви працювали з Kubernetes?» на рівні, де питають уже не «що таке под»,
а «як ви оновлювали кластер».

**Питання, які ставлять майже завжди** — і де лежить відповідь:

| Питання | Де відповідь |
|---------|--------------|
| Що відбувається від `kubectl apply` до запущеного контейнера | `Kubernetes Components`; фаза 7, день 1 |
| Чим Deployment відрізняється від StatefulSet і DaemonSet | `Deployments`, `StatefulSets`, `DaemonSet`; фаза 1, дні 2–4 |
| Чим readiness відрізняється від liveness | `Configure Liveness, Readiness and Startup Probes`; фаза 5, день 1 |
| Що таке requests і limits і що буде при перевищенні | `Resource Management for Pods and Containers`; фаза 2, день 3 |
| Чи шифрує Secret дані | `Secrets`; фаза 2, день 2 |
| Як под знаходить сервіс за іменем | `DNS for Services and Pods`; фаза 3, день 2 |
| Чим Ingress відрізняється від Gateway API | `Ingress`, `Gateway API`; фаза 3, дні 3–4 |
| Як працює NetworkPolicy і що буде без CNI з її підтримкою | `Network Policies`; фаза 3, день 5 |
| Як оновити кластер без простою | `Upgrading kubeadm clusters`; фаза 8, день 1 |
| Як зробити й відновити резервну копію etcd | `Operating etcd clusters for Kubernetes`; фаза 8, день 2 |
| Що робити з вузлом `NotReady` | `Troubleshooting Clusters`; фаза 12, день 1 |
| Чим taint відрізняється від affinity | `Taints and Tolerations`, `Assigning Pods to Nodes`; фаза 9, дні 1–2 |
| Як дати розробнику доступ лише до його простору | `Using RBAC Authorization`; фаза 8, день 4 |

# Застереження про документацію

У корпусі цього примірника — документація Kubernetes усіх ліній 1.0–1.37 з журналами змін і розкладом релізів, а
поруч — k3s, k3d, Gateway API, Traefik, cert-manager, Helm, Kustomize, книга kubectl, SOPS, age, metrics-server,
Let's Encrypt і програми іспитів CNCF. Про інші бібліотеки й інструменти сервер `kubernetes-docs` відмовить або
поверне лише уривки, де їх згадано. Для яких із них у фабриці є власний примірник, а для яких його ще немає, — у
підрозділі «Документація у фабриці» нижче; там же — що беруть із сайтів самих інструментів.

**Версії.** Сторінка тієї самої теми на різних лініях каже різне (sidecar-контейнери — beta у 1.29, stable з 1.33;
`autoscaling/v2` — з 1.23). Сервер документації каже версію кожного уривка; у питанні передавайте `version: "1.37"`
або лінію свого кластера. Усе, що позначено «на 04.10.2026» — формат, ціна, умови й версії іспитів, — звіряйте на
сторінках іспитів перед реєстрацією.

## Документація у фабриці

**Є примірник** — питати його сервер документації:

- Kubernetes 1.0–1.37, k3s, k3d, Gateway API, Traefik, cert-manager, Helm, Kustomize, книга kubectl, SOPS, age,
  metrics-server, Let's Encrypt, програми іспитів CNCF — `kubernetes`;
- тексти стандартів (OpenID Connect для входу в кластер) — `webstandards`;
- Docker і Compose — `docker`; Linux: man-сторінки, systemd, мережа — `linux`;
- PostgreSQL — база наскрізного проєкту (`psql`, `pg_dump`, налаштування сервера) — `postgresql`.

**Примірника ще немає** — відповідь лише з практики або з чужого сайту:

- CNI-плагіни: Calico, Cilium, Flannel;
- MetalLB, ingress-nginx, Envoy Gateway, local-path-provisioner;
- оператори баз; Prometheus і Grafana;
- Candidate Handbook і Important Instructions іспитів.
