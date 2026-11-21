# Розбір читання. День 6. Мережа

Цей файл пояснює, що написано в матеріалах дня. Лекція розповідає про саму тему, а розбір допомагає читати чужі
тексти: він показує, де що шукати, що означають незнайомі слова й навіщо це в React.

Оригінали написано англійською. Розбір не перекладає їх дослівно, а переказує своїми словами. Код прикладів MDN
наведено так, як він стоїть на сторінці, а поруч стоїть вивід, який він справді надрукував у Node 24. Якщо для запуску
ми щось у коді змінили, про це сказано поруч. Радимо такий порядок:

1. лекція цього дня;
2. стаття MDN `Using the Fetch API` (40 хвилин, якщо читати все);
3. короткі сторінки MDN `Response: ok property` і `AbortController` (5 хвилин разом);
4. стандарт DOM, розділ про скасування (20 хвилин);
5. стандарт Fetch, розділ `Fetch API` (40 хвилин, вибірково);
6. два розділи книжки How to Design Programs (30 хвилин).

## Як читати стандарти

Стандарти DOM і Fetch написано не для тих, хто вчиться користуватися API, а для тих, хто пише браузер. Кожен браузер
мусить поводитися однаково, тому стандарт описує поведінку як алгоритм із пронумерованими кроками. Ці кроки схожі на
код, хоч насправді браузер писати саме так не зобов'язаний. Важливий лише результат.

Вам не треба читати стандарт від початку до кінця. Він потрібен, щоб отримати точну відповідь на вузьке запитання,
наприклад: «Що робить другий виклик `abort()`?». Ось слова й позначення, які там трапляються.

| Що ви бачите | Що це означає |
|--------------|---------------|
| Блок коду з `interface AbortController { ... }` | Опис мовою Web IDL. Це мова, якою стандарти перелічують поля й методи об'єктів. Такий блок править за зміст: з нього швидко видно, що в об'єкта взагалі є |
| Вставка `For web developers` чи блок зі словами `controller = new AbortController()` і поясненням | Короткий опис для розробників сторінок. Починайте з нього: він найлегший |
| `The abort(reason) method steps are:` | Далі йдуть кроки, які браузер виконує при виклику методу |
| `this` | Об'єкт, на якому викликано метод, наприклад контролер у `controller.abort()` |
| `a promise rejected with a TypeError` | Проміс, відхилений помилкою типу `TypeError` |
| `reject p with ...` | `p` тут просто ім'я змінної з кроків алгоритму: проміс, який пізніше отримає ваш код |
| `If ..., then return` | Звичайна умова з виходом з алгоритму |
| `Assert: ...` | Те, що за логікою завжди істинне. Для читача це підказка, а не перевірка |
| `Note` у рамці | Пояснення, яке не змінює вимог, але часто найкорисніше |
| слово з посиланням, наприклад `unusable` | Термін, визначений в іншому місці стандарту. Клацніть, щоб побачити визначення |

**Як знайти потрібне місце.** Відкрийте сторінку стандарту, натисніть Ctrl+F і шукайте назву методу. Потім читайте
опис для розробників, а кроки алгоритму — лише якщо відповідь не очевидна. Номери кроків у стандартах змінюються, бо
їх часто правлять, тому в цьому файлі кроки названо за змістом.

**Приклад читання.** Запитання: «Чому `res.json()` падає на другому читанні?». У стандарті Fetch шукаємо `json()` у
розділі `Body mixin`. Визначення каже, що метод запускає алгоритм `consume body`. Перший крок цього алгоритму
перевіряє, чи об'єкт `unusable`, і якщо так, повертає проміс, відхилений із `TypeError`. Слово `unusable` веде до
визначення: тіло є, а його потік уже прочитано або заблоковано. Що означають ці два стани потоку, пояснено нижче, у
розділі статті `Locked and disturbed streams`. Запитання закрито за три переходи, без читання решти.

## Стаття `Using the Fetch API`

**Де читати:** [MDN, англійська версія](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch).
Сервер плану: `mdn-docs`.

**Що це за текст.** MDN — це довідник із вебтехнологій, який пише компанія Mozilla разом зі спільнотою. Ця стаття є
основним посібником із `fetch` і покриває значно більше, ніж потрібно сьогодні.

**Якщо часу мало,** прочитайте `Canceling a request`, `Handling the response`, `Checking response status`, `Reading
the response body` і `Locked and disturbed streams`. Ці розділи прямо потрібні для завдання.

**Як ми запускали приклади.** Приклади статті звертаються до вигаданих адрес на зразок `https://example.org/post`,
яких насправді немає. Щоб побачити справжній вивід, ми запускали їх у Node 24 з маленьким власним сервером і
підставляли його адресу замість вигаданої. Сервер має кілька адрес: одна відповідає JSON, інша сторінкою HTML, ще
інша відповідає через 500 мс. Кожного разу ми кажемо, яку адресу підставили і що ще змінили в коді. Змінна `base` у
коді містить початок адреси цього сервера, як у лекції. Так само ми запускали й приклади в розділах про стандарти.

### Вступ і `Making a request`

`fetch()` приймає адресу, а другим аргументом необов'язковий об'єкт налаштувань. Адреса може бути рядком, об'єктом
`URL` або об'єктом `Request`. Функція повертає проміс, який виконується об'єктом `Response`. Без налаштувань метод
запиту — `GET`.

### `Setting the method`

Поле `method` задає метод запиту, наприклад `POST`. Стаття згадує, що в режимі `no-cors` дозволено лише `GET`, `POST`
і `HEAD`. Цей режим описано нижче.

### `Setting a body`

Поле `body` містить дані, які запит надсилає на сервер. Стаття перелічує, чим вони можуть бути: рядком, об'єктом
`URLSearchParams` з параметрами форми, об'єктом `FormData` з полями форми разом із файлами, об'єктом `Blob`, тобто
байтами з відомим типом (наприклад, файлом, який вибрала людина), сирими байтами в пам'яті (`ArrayBuffer` і схожі
об'єкти) або потоком. Будь-який інший об'єкт перетворюється на рядок методом `toString()`. Звичайний об'єкт
JavaScript від цього стає рядком `[object Object]`, тому дані для JSON спершу перетворюють на рядок через
`JSON.stringify`. Ось які тіла виходять в обох випадках. Метод `request.text()` читає тіло запиту так само, як
`res.text()` читає тіло відповіді:

```js
const wrong = new Request("https://example.org/orders", { method: "POST", body: { item: "чай" } });
console.log("об'єкт:", await wrong.text());

const right = new Request("https://example.org/orders", { method: "POST", body: JSON.stringify({ item: "чай" }) });
console.log("JSON.stringify:", await right.text());
```

```text
об'єкт: [object Object]
JSON.stringify: {"item":"чай"}
```

У запиту `GET` тіла бути не може. Конструктор `Request` кидає виняток, якщо тіло все ж передати:

```js
try {
  new Request("https://example.org/", { method: "GET", body: "x" });
} catch (e) {
  console.log(e.name + ":", e.message);
}
```

```text
TypeError: Request with GET/HEAD method cannot have body.
```

Останній приклад розділу несподівано важливий для сьогоднішньої теми. Тіло **запиту** теж є потоком, як і тіло
відповіді, і `fetch`, надсилаючи запит, прочитує цей потік. Тому той самий об'єкт `Request` з тілом не можна надіслати
двічі. Ось код статті:

```js
const request = new Request("https://example.org/post", {
  method: "POST",
  body: JSON.stringify({ username: "example" }),
});

const response1 = await fetch(request);
console.log(response1.status);

// Will throw: "Body has already been consumed."
const response2 = await fetch(request);
console.log(response2.status);
```

Ми підставили адресу нашого сервера, який на `POST` відповідає статусом 201. Перший `fetch` надрукував статус. Другий
кинув виняток, якого ніхто не перехопив, тому Node зупинив програму й надрукував виняток. Службові рядки Node ми
прибрали:

```text
201
[TypeError: Cannot construct a Request with a Request object that has already been used.]
```

Коментар у коді MDN наводить текст `Body has already been consumed.`, а Node пише інші слова. Стандарт задає лише тип
помилки `TypeError`, а текст кожна програма пише свій (див. лекцію цього дня, розділ «Коли проміс від `fetch`
відхиляється», абзац «Не спирайтеся на текст помилки»). Текст Node підказує, де саме сталася відмова. `fetch` спершу
будує з переданого запиту новий об'єкт `Request`, а конструктор відмовляється брати запит, тіло якого вже прочитано.
Цей крок описано нижче, у підрозділі `5.6` стандарту Fetch.

Щоб надіслати те саме двічі, стаття робить копію до першого надсилання:

```js
const request1 = new Request("https://example.org/post", {
  method: "POST",
  body: JSON.stringify({ username: "example" }),
});

const request2 = request1.clone();

const response1 = await fetch(request1);
console.log(response1.status);

const response2 = await fetch(request2);
console.log(response2.status);
```

```text
201
201
```

Копію `request2` зроблено до першого надсилання, тому її тіло ще ніхто не читав. Це те саме правило, що й для
відповіді: копію роблять до першого читання.

### `Setting headers`

Поле `headers` задає заголовки запиту. Стаття показує два способи: звичайний об'єкт або об'єкт `Headers`, у який
заголовки додають методом `append`. Об'єкт `Headers` ще й упорядковує те, що в нього кладуть: переводить назви в
нижній регістр і обрізає пробіли на початку й у кінці значення. Перевірка в Node 24:

```js
const headers = new Headers({ "Content-TYPE": "application/json" });
headers.append("X-Trace", "  abc  ");
console.log([...headers.entries()]);
```

```text
[ [ 'content-type', 'application/json' ], [ 'x-trace', 'abc' ] ]
```

Метод `entries()` дає пари «назва й значення». Назва `Content-TYPE` стала `content-type`, а пробіли навколо `abc`
зникли.

**Незнайомі слова.** `forbidden request header` означає заголовок, який сторінці не дозволено задавати власноруч.
Браузер ставить такі заголовки сам і не дає сторінці їх підробити, бо від них залежить правильність і безпека
з'єднання. Приклади таких заголовків — `Host` з іменем сервера чи `Content-Length` з довжиною тіла.

### `Sending data in a GET request`

Параметри `GET` записують в адресу після знака питання. Об'єкт `URLSearchParams` складає цей рядок і кодує символи,
які не можна писати в адресі напряму. Українські літери теж кодуються:

```js
const params = new URLSearchParams({ city: "Івано-Франківськ", days: 3 });
console.log(params.toString());
```

```text
city=%D0%86%D0%B2%D0%B0%D0%BD%D0%BE-%D0%A4%D1%80%D0%B0%D0%BD%D0%BA%D1%96%D0%B2%D1%81%D1%8C%D0%BA&days=3
```

**Навіщо це вам.** Знак `&` в адресі розділяє параметри. Якщо людина введе в пошук `кава & чай`, а код просто додасть
цей текст до адреси, то сервер побачить зовсім не те, що людина шукала. Код нижче складає адресу обома способами, а
потім розбирає її назад так, як розбере сервер. Поле `searchParams` об'єкта `URL` дає параметри адреси парами «назва й
значення»:

```js
const query = "кава & чай";

const glued = new URL("https://example.org/search?q=" + query + "&page=1");
console.log("склеєно рядком:", [...glued.searchParams]);

const params = new URLSearchParams({ q: query, page: 1 });
const encoded = new URL("https://example.org/search?" + params);
console.log("через URLSearchParams:", [...encoded.searchParams]);
console.log(encoded.search);
```

```text
склеєно рядком: [ [ 'q', 'кава ' ], [ ' чай', '' ], [ 'page', '1' ] ]
через URLSearchParams: [ [ 'q', 'кава & чай' ], [ 'page', '1' ] ]
?q=%D0%BA%D0%B0%D0%B2%D0%B0+%26+%D1%87%D0%B0%D0%B9&page=1
```

У склеєній адресі знак `&` розірвав запит на два параметри: `q` отримав лише `кава `, а `чай` став назвою окремого
параметра без значення. `URLSearchParams` закодував знак `&` як `%26`, а пробіл як `+`, тому сервер отримав увесь
текст цілим. Складати адресу звичайним додаванням рядків можна лише тоді, коли значення заздалегідь безпечне,
наприклад, коли це число.

### `Making cross-origin requests`

Поле `mode` каже браузерові, що робити із запитом на інше **джерело**. Що таке джерело і навіщо браузер обмежує
читання чужих відповідей, пояснено в лекції цього дня, розділ «Коли проміс від `fetch` відхиляється», абзац «Заборона
браузера». Там же сказано, що механізм, яким сервер дає дозвіл, називається CORS. Стаття описує три значення `mode`.

Типове значення `cors` вмикає механізм CORS. Далі браузер ділить запити на два види. **Простий запит** (simple
request) — це запит, який вебсторінки вміли надсилати на будь-яке джерело ще до появи `fetch`, звичайною формою HTML:
метод `GET`, `HEAD` чи `POST` і лише кілька дозволених заголовків. Такі запити сервер отримує від форм на чужих
сторінках і без `fetch`, тому мусить бути до них готовим, а дозволу на них не питають. Тому браузер надсилає простий
запит одразу. Відповідь він віддає коду лише тоді, коли сервер додав заголовок `Access-Control-Allow-Origin` з
джерелом сторінки.

Будь-який інший запит браузер не надсилає одразу. Спершу він робить **попередній запит** (preflight) методом `OPTIONS`
і питає сервер, чи той дозволяє такий запит. Справжній запит піде лише після згоди сервера. Наприклад, запит із
заголовком `Content-Type: application/json` не є простим, бо звичайна форма HTML такого заголовка не надсилає, тому
перед ним завжди йде попередній запит.

Значення `same-origin` забороняє запити на інше джерело взагалі: такий запит відхиляється. Значення `no-cors` вимикає
CORS: запит піде, але відповідь буде **непрозорою** (opaque response). Вона існує, але її заголовки й тіло закрито від
коду. Стаття додає, що сайтам це значення майже ніколи не потрібне, а користуються ним переважно сервіс-воркери, про
які сказано нижче, у розділі `Locked and disturbed streams`.

### `Including credentials`

Слово **credentials** тут означає дані, за якими сервер упізнає людину. Стаття називає три їхні види.

- **Cookie** — це невеликий запис, який сервер у відповіді просить браузер зберегти заголовком `Set-Cookie`. Потім
  браузер сам додає цей запис до кожного запиту на той самий сервер. Так сервер знає, що людина вже ввійшла.
- **Сертифікат клієнта** — це файл, яким комп'ютер людини підтверджує себе під час захищеного з'єднання. На звичайних
  сайтах він трапляється рідко.
- Заголовки `Authorization` і `Proxy-Authorization`, у які записують пароль чи рядок-перепустку, виданий сервером
  після входу.

Поле `credentials` має три значення: `omit` не надсилає їх ніколи, `same-origin` надсилає лише на своє джерело і є
типовим, `include` надсилає завжди. Це поле вирішує ще й те, чи прийме браузер нові cookie з відповіді.

Запит із `include` на чуже джерело небезпечний. Будь-яка чужа сторінка могла б тоді надсилати запити від імені
людини, яка ввійшла на сайт, і читати відповіді. Тому сервер мусить окремо погодитися на такі запити: відповісти
заголовком `Access-Control-Allow-Credentials` і назвати в `Access-Control-Allow-Origin` точне джерело сторінки.
Значення `*` («будь-яке джерело») для таких запитів заборонено. Для сайтів із входом це знадобиться пізніше, у
завданні дня цього немає.

### `Creating a Request object`

Конструктор `Request` приймає ті самі аргументи, що й `fetch`. Об'єкт можна підготувати заздалегідь і передати у
`fetch`. Це зручно, коли запит будують в одному місці, а надсилають в іншому.

### `Canceling a request`

Щоб запит можна було скасувати, створюють `AbortController` і передають його сигнал у поле `signal`. Виклик
`abort()` відхиляє проміс `fetch` з `AbortError`. Як влаштовані контролер і сигнал, пояснює лекція цього дня, розділ
«`AbortController` і `AbortSignal`: як зупинити роботу».

Перший приклад статті прив'язує запит і скасування до двох кнопок сторінки:

```js
const controller = new AbortController();

const fetchButton = document.querySelector("#fetch");
fetchButton.addEventListener("click", async () => {
  try {
    console.log("Starting fetch");
    const response = await fetch("https://example.org/get", {
      signal: controller.signal,
    });
    console.log(`Response: ${response.status}`);
  } catch (e) {
    console.error(`Error: ${e}`);
  }
});

const cancelButton = document.querySelector("#cancel");
cancelButton.addEventListener("click", () => {
  controller.abort();
  console.log("Canceled fetch");
});
```

У Node немає сторінки з кнопками, тому для запуску ми замінили кнопки об'єктами `EventTarget`. Це об'єкти, на які
можна вішати обробники подій і на яких можна запустити подію методом `dispatchEvent`. Адресу ми замінили на адресу
сервера, що відповідає через 500 мс. Решту коду статті лишили без змін. Ось що ми дописали до нього: на початку
файла стоять «кнопки», а в кінці стоїть людина, яка натискає «Запит», за 100 мс «Скасувати», а потім ще раз «Запит»:

```js
const pause = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const buttons = { "#fetch": new EventTarget(), "#cancel": new EventTarget() };
const document = { querySelector: (selector) => buttons[selector] };

// … тут код статті …

fetchButton.dispatchEvent(new Event("click"));    // «Запит»
await pause(100);
cancelButton.dispatchEvent(new Event("click"));   // «Скасувати»
await pause(100);
fetchButton.dispatchEvent(new Event("click"));    // знову «Запит»
```

```text
Starting fetch
Canceled fetch
Error: AbortError: This operation was aborted
Starting fetch
Error: AbortError: This operation was aborted
```

Рядок `Canceled fetch` стоїть раніше за помилку. Причина в тому, що `abort()` лише відхиляє проміс, а код після
`await` у першому обробнику продовжиться пізніше, мікрозадачею, коли обробник кнопки «Скасувати» вже закінчив роботу
(мікрозадачі пояснено в лекції дня 5, розділ «Цикл подій: хто вирішує, що виконувати далі»).

Головне видно в останньому рядку: другий запит упав одразу, хоч після нього ніхто нічого не скасовував. Контролер у
прикладі створено один раз, поза обробником. Після першого `abort()` його сигнал скасований назавжди, і кожен
наступний `fetch` із цим сигналом відхиляється відразу. Приклад статті показує лише сам механізм. У справжньому коді
новий контролер створюють перед кожним запитом, як у прикладі зі сторінки `AbortSignal`, наведеному нижче.

Друге, що додає стаття, легко не помітити. Якщо скасування сталося вже після того, як `fetch` виконався, але до
читання тіла, то відхилиться саме читання тіла:

```js
async function get() {
  const controller = new AbortController();
  const request = new Request("https://example.org/get", {
    signal: controller.signal,
  });

  const response = await fetch(request);
  controller.abort();
  // The next line will throw `AbortError`
  const text = await response.text();
  console.log(text);
}
```

Ми підставили адресу сервера, який надсилає статус і заголовки одразу, а тіло через 300 мс, і викликали функцію так,
щоб надрукувати помилку:

```js
try {
  await get();
} catch (e) {
  console.log(e.name + ":", e.message);
}
```

```text
AbortError: This operation was aborted
```

Лекція показує той самий випадок на власному прикладі. Чому так стається за стандартом, сказано нижче, у підрозділі
`5.6` стандарту Fetch.

### `Handling the response`

Стаття пояснює момент виконання: проміс виконується, щойно браузер отримав статус і заголовки, можливо, ще до
отримання тіла. Саме тому в коді з `fetch` стоять два `await`. Докладно це розібрано в лекції цього дня, розділ «Два
`await`: заголовки приходять раніше за тіло».

### `Checking response status`

Стаття наголошує, що `fetch` не вважає статус 404 помилкою, тому статус треба перевірити самому. Ось її зразок:

```js
async function getData() {
  const url = "https://example.org/products.json";
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    // …
  } catch (error) {
    console.error(error.message);
  }
}
```

Щоб побачити, як зразок спрацьовує, ми зробили `url` параметром функції й викликали її двічі. Перший виклик пішов на
адресу, якої на сервері немає, тому сервер відповів 404. Другий пішов на адресу, яка відповідає статусом 500:

```js
await getData(base + "/no-such-page");
await getData(base + "/error-html");
```

```text
Response status: 404
Response status: 500
```

Обидва рази проміс від `fetch` виконався, бо сервер відповів. Помилку кинув сам зразок, коли побачив, що `ok`
дорівнює `false`. Блок `catch` її перехопив і надрукував. Зверніть увагу: `getData` сама ловить свою помилку й лише
друкує її, тому той, хто викликав `getData`, про збій не дізнається. Для нього виклик просто закінчиться без
результату. Перевірка `response.ok` із цього зразка прямо потрібна в завданні дня.

### `Checking the response type`

Поле `Response.type` каже, яка це відповідь: `basic` зі свого джерела, `cors` дозволена сервером із чужого, `opaque`
непрозора або `opaqueredirect` для перенаправлення з налаштуванням `redirect: "manual"`. Для непрозорих відповідей
статус дорівнює 0, заголовків не видно, а тіло дорівнює `null`. Тому на такій відповіді `ok` хибне, хоч сервер міг
відповісти успішно. Сьогодні це не потрібно, але пояснює, чому режим `no-cors` не є способом обійти CORS: запит
справді піде, але прочитати відповідь код однаково не зможе.

### `Checking headers`

Стаття показує, як перевірити `Content-Type` перед розбором, щоб не читати HTML як JSON:

```js
async function fetchJSON(request) {
  try {
    const response = await fetch(request);
    const contentType = response.headers.get("content-type");
    if (!contentType || !contentType.includes("application/json")) {
      throw new TypeError("Oops, we haven't got JSON!");
    }
    // Otherwise, we can read the body as JSON
  } catch (error) {
    console.error("Error:", error);
  }
}
```

Ми викликали функцію двічі. Перший раз пішов на адресу, яка відповідає статусом 200 і сторінкою HTML. Другий раз
пішов на адресу, яка відповідає статусом 200 і справжнім JSON:

```js
await fetchJSON(base + "/html");
await fetchJSON(base + "/products.json");
console.log("кінець");
```

```text
Error: TypeError: Oops, we haven't got JSON!
    at fetchJSON (…)
    …
кінець
```

`console.error` друкує не лише текст помилки, а й перелік викликів, з яких її кинуто. Ми лишили з нього перший рядок,
а шлях до файла й решту рядків замінили трьома крапками. Перший виклик зупинився на перевірці заголовка, бо сервер
надіслав `text/html`. Другий виклик пройшов перевірку й нічого не надрукував.

Ця перевірка є додатковим захистом поверх `res.ok`. Перевірка `res.ok` не допоможе, якщо сервер помилково відповів
статусом 200 і сторінкою HTML: без перевірки заголовка `res.json()` упаде із `SyntaxError`.

### `Reading the response body`

Тут перелічено методи, які читають усе тіло й перетворюють його: `arrayBuffer()` дає сирі байти, `blob()` дає об'єкт
`Blob`, `formData()` розбирає поля форми, `json()` розбирає JSON, `text()` дає рядок. Кожен метод асинхронний і
повертає проміс. Кожен відхиляється, якщо дані не підходять до формату, наприклад якщо `json()` отримав не JSON.

### `Streaming the response body`

Поле `Response.body` дає потік `ReadableStream`, який можна читати частинами, не чекаючи кінця. Це потрібно для
великих файлів і для відповідей, які приходять поступово, наприклад коли сервер друкує довгу відповідь частинами.
Приклад статті читає такий потік і одразу отримує текст:

```js
const url = "https://www.example.org/a-large-file.txt";

async function fetchTextAsStream(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const stream = response.body.pipeThrough(new TextDecoderStream());
    for await (const value of stream) {
      console.log(value);
    }
  } catch (e) {
    console.error(e);
  }
}
```

Ми підставили адресу, яка надсилає три шматки тексту з паузою 50 мс між ними, як адреса `/chunks` у лекції, і
викликали `await fetchTextAsStream(url)`:

```text
перший 
другий 
третій
```

Потік тіла віддає байти. Метод `pipeThrough` пропускає ці байти через інший об'єкт і повертає новий потік з тим, що
вийшло. Тут цим об'єктом є `TextDecoderStream`, який перетворює байти UTF-8 на текст. Цикл `for await` бере з нового
потоку шматок за шматком, щойно той надійде, тому кожен шматок надруковано окремим рядком. У лекції той самий потік
читається без `TextDecoderStream`, через `TextDecoder`, і там пояснено, чому межа шматка може пройти посередині
літери (розділ «Тіло відповіді — це потік»). `TextDecoderStream` таку межу обробляє сам.

### `Processing a text file line by line`

Цей розділ можна пропустити. Його код спирається на асинхронні генератори й регулярні вирази, яких план ще не
пояснював, а завдання дня їх не потребує. Розділ корисний, лише коли ви обробляєте великі текстові файли.

### `Locked and disturbed streams`

Цей розділ пояснює причину одноразового читання двома словами:

- **locked** (заблокований): хтось уже взяв **читача** потоку через `getReader()`. Читач — це об'єкт, який забирає з
  потоку шматки. Поки читач тримає потік, другий читач не може його взяти.
- **disturbed** (потривожений): з потоку вже прочитали хоч щось, тому він не починається спочатку.

Стаття показує це на двох викликах `json()` поспіль:

```js
async function getData() {
  const url = "https://example.org/products.json";
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const result1 = await response.json();
    const result2 = await response.json(); // will throw
  } catch (error) {
    console.error(error.message);
  }
}
```

Ми підставили адресу, яка відповідає JSON, і викликали `await getData()`:

```text
Body is unusable: Body has already been read
```

Перший `json()` прочитав потік до кінця. Другий виклик застав потік потривоженим і відхилився з `TypeError`. Слово
`unusable` у тексті Node — те саме слово, яким стандарт Fetch називає такий стан тіла (див. підрозділ `5.3` нижче).

Заблокований потік від потривоженого відрізняється. Це видно, якщо взяти читача й нічого не прочитати:

```js
const response = new Response("тіло відповіді");
const reader = response.body.getReader();    // беремо читача, але нічого не читаємо
console.log("locked:", response.body.locked, "| bodyUsed:", response.bodyUsed);
try {
  await response.text();
} catch (e) {
  console.log("text() →", e.name + ":", e.message);
}

reader.releaseLock();                         // віддаємо читача назад
console.log("locked:", response.body.locked, "| bodyUsed:", response.bodyUsed);
console.log("text() →", await response.text());
```

```text
locked: true | bodyUsed: false
text() → TypeError: Body is unusable: Body has already been read
locked: false | bodyUsed: false
text() → тіло відповіді
```

Конструктор `new Response(...)` створює відповідь без мережі, тому так зручно перевіряти поведінку об'єкта. Поки читач
тримав потік, `text()` відмовився читати, хоч `bodyUsed` показує, що з тіла ще нічого не прочитано. Текст Node тут
навіть неточний, бо каже «already been read». Тому й тут розрізняйте помилки за типом, а не за текстом. Після
`releaseLock()` читач відпустив потік, і `text()` прочитав усе тіло. Отже, блокування можна зняти, а потривожений
потік лишається таким назавжди.

Щоб прочитати тіло двічі, стаття робить копію через `Response.clone()` до першого читання:

```js
async function getData() {
  const url = "https://example.org/products.json";
  try {
    const response1 = await fetch(url);
    if (!response1.ok) {
      throw new Error(`Response status: ${response1.status}`);
    }

    const response2 = response1.clone();

    const result1 = await response1.json();
    const result2 = await response2.json();
  } catch (error) {
    console.error(error.message);
  }
}
```

Сам приклад нічого не друкує, тому після двох читань ми дописали рядок `console.log(result1, result2)`:

```text
[ { name: 'чай' } ] [ { name: 'чай' } ]
```

Обидва читання дали ті самі дані, бо кожне читало власну копію тіла.

Останній приклад розділу взято з роботи **сервіс-воркера**. Це скрипт, що працює між сторінкою й мережею: він бачить
кожен запит сторінки й може відповісти на нього сам, наприклад збереженою раніше відповіддю. Так сайти працюють без
інтернету.

```js
async function cacheFirst(request) {
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open("MyCache_1");
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    return Response.error();
  }
}

self.addEventListener("fetch", (event) => {
  if (precachedResources.includes(url.pathname)) {
    event.respondWith(cacheFirst(event.request));
  }
});
```

Цей код працює лише всередині сервіс-воркера, бо там є сховище відповідей `caches` і об'єкт `self`. Тому ми його не
запускали. Функція `cacheFirst` спершу шукає відповідь у сховищі. Якщо там нічого немає, вона йде в мережу, кладе в
сховище копію відповіді й повертає оригінал сторінці. Копія потрібна, бо сховище читатиме тіло, щоб зберегти його, і
сторінка теж читатиме тіло. Без копії хтось із них отримав би вже прочитаний потік. Сервіс-воркери поки не потрібні,
важливий лише сам прийом.

**Навіщо все це в React.** Кожен компонент, що завантажує дані, виконує той самий ланцюжок: запит, перевірка статусу,
читання тіла, обробка помилок. Правило одного читання найчастіше ламає код тоді, коли хочеться подивитися, що
прийшло. Ось ланцюжок, схожий на той, що стоїть у компоненті `Forecast` з лекції (розділ «Як це проявиться в React»).
Функція `setData` тут лише друкує, що отримала, замість того щоб записати це в стан компонента. Ми додали один рядок
для налагодження, який читає тіло як текст, щоб надрукувати його:

```js
const setData = (data) => console.log("setData отримав:", data);   // замість стану компонента

await fetch(base + "/products.json")
  .then(async (res) => {
    console.log("тіло для налагодження:", await res.text());   // хочемо подивитися, що прийшло
    return res.json();                                          // і далі розбираємо як завжди
  })
  .then(setData)
  .catch((e) => console.log("catch:", e.name + ":", e.message));
```

```text
тіло для налагодження: [{"name":"чай"}]
catch: TypeError: Body is unusable: Body has already been read
```

Рядок для налагодження прочитав тіло, тому `res.json()` відхилився з `TypeError`, і `setData` не отримав нічого.
Компонент так і лишився б у стані «завантаження». Коли після такої правки код перестав працювати, шукайте друге
читання тієї самої відповіді. Щоб подивитися на дані й нічого не зламати, читайте тіло один раз, а друкуйте вже
прочитане.

### Запитання до статті

**1. Коли саме виконується проміс від `fetch`?**

<details><summary>Відповідь</summary>

Коли браузер отримав статус і заголовки. Тіло може ще надходити, тому його читання є окремою асинхронною дією.

</details>

**2. Запит із `mode: "no-cors"` пройшов. Чому код усе одно не може прочитати дані?**

<details><summary>Відповідь</summary>

Відповідь непрозора: тип `opaque`, статус 0, порожні заголовки й тіло `null`. Режим дозволяє надіслати запит, але не
читати відповідь. Дозвіл на читання може дати лише сервер заголовками CORS.

</details>

**3. Що таке disturbed і чому це забороняє друге читання?**

<details><summary>Відповідь</summary>

Це стан потоку, з якого вже щось прочитали. Потік не зберігає прочитаного й не починається заново, тому повного тіла
вдруге отримати неможливо. Тому стандарт дає `TypeError`.

</details>

## Сторінка `Response: ok property`

**Де читати:** [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Response/ok). Читання займе хвилину.

### Опис і `Value`

Поле `ok` доступне лише для читання і містить логічне значення. Воно дорівнює `true`, коли статус лежить у діапазоні
від 200 до 299. Більше тут нічого немає. Перевірка на межах у Node 24 дає таке:

```js
for (const status of [200, 299, 300, 404, 500]) {
  console.log(status, new Response(null, { status }).ok);
}
```

```text
200 true
299 true
300 false
404 false
500 false
```

Той самий конструктор `new Response(...)` можна використовувати в тестах замість справжнього сервера.

### `Examples`

Приклад сторінки завантажує картинку й друкує `response.ok`:

```js
const myImage = document.querySelector("img");

const myRequest = new Request("flowers.jpg");

fetch(myRequest).then((response) => {
  console.log(response.ok); // returns true if the response returned successfully
  response.blob().then((myBlob) => {
    const objectURL = URL.createObjectURL(myBlob);
    myImage.src = objectURL;
  });
});
```

Цей код працює лише на сторінці: йому потрібні тег `<img>` і файл `flowers.jpg` поруч зі сторінкою. Тому ми його не
запускали, а те, що він надрукує, видно з самого коду. Якщо файл знайдено, `console.log` надрукує `true`, а якщо
сервер відповів 404, то `false`. Далі код читає тіло методом `blob()` у будь-якому разі, бо значення `ok` він не
перевіряє. `URL.createObjectURL` створює тимчасову адресу для байтів у пам'яті, щоб тег `<img>` міг їх показати. За
статусу 404 у тег потраплять байти сторінки помилки, і браузер не зможе показати їх як картинку. Тому не беріть цей
приклад за зразок обробки помилок: зразок є в розділі `Checking response status` статті вище.

**Навіщо це в React.** Перевірка `res.ok` стоїть на межі між мережею й станом компонента. У компоненті `Forecast` з
лекції такої перевірки немає, там стоїть ланцюжок `fetch(...).then((res) => res.json()).then(setData)`. Ми запустили
той самий ланцюжок без React на адресі, яка відповідає статусом 404 і JSON з описом помилки. Так відповідають багато
API. Функція `setData` знову лише друкує те, що отримала:

```js
const setData = (data) => console.log("setData отримав:", data);   // замість стану компонента

await fetch(base + "/not-found-json")
  .then((res) => res.json())
  .then(setData);
```

```text
setData отримав: { error: 'Немає такого міста' }
```

Ланцюжок не впав: тіло є правильним JSON, а `json()` на статус не дивиться. Об'єкт з описом помилки потрапив у стан як
дані. З коду компонента `Forecast` видно, що він намалював би з нього `на екрані: undefined`, бо поля `city` в цьому
об'єкті немає. У React ми цього не запускали. Якщо ж сервер відповість сторінкою HTML, то `json()` упаде із
`SyntaxError`, і людина замість зрозумілого повідомлення побачить незрозумілий збій розбору.

## Сторінка `AbortController`

**Де читати:** [MDN](https://developer.mozilla.org/en-US/docs/Web/API/AbortController). Ця сторінка лише довідкова й
дуже коротка.

### `Constructor`, `Instance properties`, `Instance methods`

Конструктор `AbortController()` створює контролер. Поле `signal` лише для читання повертає об'єкт `AbortSignal`, який
передають у те, що хочуть скасовувати. Метод `abort()` скасовує операцію до її завершення. Сторінка перелічує, що він
здатний зупинити: запити `fetch`, читання тіла відповіді й потоки.

### `Examples`

На самій сторінці коду немає. Вона веде на [сторінку
`AbortSignal`](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal), і приклади варто дивитися саме там.
Нижче кожен із них наведено з кодом. Для запуску ми підставляли адресу сервера, який відповідає через 500 мс.

**Приклад `Aborting a fetch operation using an explicit signal`.** Він схожий на приклад із кнопками в статті вище,
але з однією важливою відмінністю: новий контролер створюється на кожне натискання кнопки «Завантажити».

```js
let controller;
const url = "video.mp4";

const downloadBtn = document.querySelector(".download");
const abortBtn = document.querySelector(".abort");

downloadBtn.addEventListener("click", fetchVideo);

abortBtn.addEventListener("click", () => {
  if (controller) {
    controller.abort();
    console.log("Download aborted");
  }
});

async function fetchVideo() {
  controller = new AbortController();
  const signal = controller.signal;

  try {
    const response = await fetch(url, { signal });
    console.log("Download complete", response);
    // process response further
  } catch (err) {
    console.error(`Download error: ${err.message}`);
  }
}
```

Для запуску ми зробили те саме, що з прикладом статті: кнопки стали об'єктами `EventTarget`, а адреса `video.mp4`
стала адресою нашого сервера. Замість усього об'єкта `response` ми друкуємо лише його статус, бо Node друкує об'єкт
відповіді на багато рядків. Людина знову натискає «Завантажити», за 100 мс «Скасувати», потім знову «Завантажити»:

```text
Download aborted
Download error: This operation was aborted
Download complete 200
```

Тепер другий запит дійшов до кінця. Функція `fetchVideo` створила для нього новий контролер, а скасованим лишився лише
старий. Порівняйте з виводом прикладу статті, де другий запит упав одразу. Другий фрагмент цього прикладу дослівно
повторює функцію `get()` з розділу статті `Canceling a request`, тому тут його не наведено.

**Приклад `Aborting a fetch operation with a timeout`.** Тут сигнал створює сам таймер:

```js
const url = "video.mp4";

try {
  const res = await fetch(url, { signal: AbortSignal.timeout(5000) });
  const result = await res.blob();
  // …
} catch (err) {
  if (err.name === "TimeoutError") {
    console.error("Timeout: It took more than 5 seconds to get the result!");
  } else if (err.name === "AbortError") {
    console.error(
      "Fetch aborted by user action (browser stop button, closing tab, etc.)",
    );
  } else {
    // A network error, or some other problem.
    console.error(`Error: type: ${err.name}, message: ${err.message}`);
  }
}
```

Ми замінили `"video.mp4"` адресою нашого сервера, а 5000 на 100, щоб не чекати п'ять секунд. Сервер відповідає через
500 мс, тому таймер спрацював раніше:

```text
Timeout: It took more than 5 seconds to get the result!
```

Текст повідомлення лишився з MDN, тому в ньому досі сказано про 5 секунд. Важливе інше: помилка має ім'я
`TimeoutError`, а не `AbortError`. Тому код розрізняє дві історії: «сервер довго мовчить» і «людина скасувала сама».

**Приклад `Aborting a fetch with timeout or explicit abort`.** Метод `AbortSignal.any` поєднує кілька сигналів в один,
який спрацьовує разом із першим спрацьованим. Приклад поєднує контролер, яким скасовує людина, і таймер. У коді MDN
гілки `catch` містять лише коментарі, а `url` і момент, коли людина натискає «Скасувати», не задано. Тому ми запустили
трохи змінений код. Ми загорнули приклад у функцію `run`, підставили адресу сервера, замінили 5000 на 100, поставили в
гілки `console.log` і додали рядок із `setTimeout`, який скасовує запит через заданий час:

```js
async function run(cancelAfter) {
  try {
    const controller = new AbortController();
    setTimeout(() => controller.abort(), cancelAfter);   // людина натискає «Скасувати»
    const timeoutSignal = AbortSignal.timeout(100);
    const res = await fetch(url, {
      // This will abort the fetch when either signal is aborted
      signal: AbortSignal.any([controller.signal, timeoutSignal]),
    });
    const body = await res.json();
  } catch (e) {
    if (e.name === "AbortError") {
      console.log("скасувала людина");       // Notify the user of abort.
    } else if (e.name === "TimeoutError") {
      console.log("спрацював таймер");       // Notify the user of timeout
    } else {
      // A network error, or some other problem.
      console.log(`Type: ${e.name}, Message: ${e.message}`);
    }
  }
}

await run(50);      // людина скасовує на 50 мс, раніше за таймер
await run(1000);    // людина не встигає, таймер спрацьовує на 100 мс
```

```text
скасувала людина
спрацював таймер
```

Перший запуск дав `AbortError`, бо першим спрацював контролер. Другий дав `TimeoutError`, бо першим спрацював таймер.
Отже, поєднаний сигнал отримує причину того сигналу, який спрацював першим. Під цим прикладом на сторінці MDN стоїть
примітка, що з поєднаним сигналом не можна дізнатися, чи скасування спричинив таймер. Запуск у Node 24 показує
протилежне, і стандарт DOM каже те саме, що й запуск: сигнал від `AbortSignal.any` отримує причину того сигналу, який
його скасував (див. підрозділ `3.2` стандарту нижче). Тут вірте стандартові, а не примітці.

**Приклад `Removing the abort event listener`.** Він пояснює, навіщо прибирати власного слухача події `abort`, коли
робота скінчилася. Перший варіант функції покладається на `{ once: true }`:

```js
const globalController = new AbortController();

async function doOperation(url, localSignal) {
  const signal = AbortSignal.any([globalController.signal, localSignal]);
  signal.addEventListener("abort", () => console.log(`Aborted: ${url}`), {
    once: true,
  });

  const response = await fetch(url, { signal });
  return response.text();
}
```

Параметр `{ once: true }` прибирає слухача лише тоді, коли подія спрацювала. Якщо ж запит закінчився успішно, подія
`abort` так і не настане, і слухач лишиться на сигналі. Слухач тримає в пам'яті все, що згадує його функція. Поки
живий глобальний контролер `globalController`, поєднані сигнали з такими слухачами теж лишаються в пам'яті, і кожен
новий виклик додає ще один. Тому другий варіант прибирає слухача сам, у блоці `finally`, який виконується і після
успіху, і після помилки:

```js
async function doOperation(url, localSignal) {
  const signal = AbortSignal.any([globalController.signal, localSignal]);
  const onAbort = () => console.log(`Aborted: ${url}`);
  signal.addEventListener("abort", onAbort, { once: true });

  try {
    const response = await fetch(url, { signal });
    return await response.text();
  } finally {
    signal.removeEventListener("abort", onAbort);
  }
}
```

Щоб побачити різницю, ми назвали перший варіант `doOperationOnce` і змінили обидва варіанти так, щоб вони повертали
сам поєднаний сигнал: після `await response.text()` стоїть `return signal`. Слухачів ми порахували функцією
`getEventListeners` з модуля `node:events`. Вона повертає масив слухачів, які висять на об'єкті:

```js
import { getEventListeners } from "node:events";

const s1 = await doOperationOnce(url, new AbortController().signal);
console.log("once, запит скінчився, слухачів abort:", getEventListeners(s1, "abort").length);
const s2 = await doOperation(url, new AbortController().signal);
console.log("finally, запит скінчився, слухачів abort:", getEventListeners(s2, "abort").length);
```

```text
once, запит скінчився, слухачів abort: 2
finally, запит скінчився, слухачів abort: 1
```

Один слухач в обох рядках належить самому `fetch`: ми окремо перевірили, що `fetch` із сигналом без жодного нашого
слухача теж лишає на ньому одного слухача. Другий слухач у першому рядку — той, що поставив перший варіант функції. У
другому варіанті його прибрав блок `finally`. Сторінка MDN теж уточнює, що прибирати треба лише власних слухачів, а
внутрішніми справами `fetch` займається сам.

**Приклад `Implementing an abortable API`.** Він показує, як написати власну функцію зі скасуванням. Функція
`myCoolPromiseAPI` лише чекає секунду, а замість справжньої роботи стоїть таймер:

```js
function myCoolPromiseAPI(/* …, */ { signal }) {
  return new Promise((resolve, reject) => {
    // If the signal is already aborted, immediately throw in order to reject the promise.
    signal.throwIfAborted();

    // Simulate the main operation completing after a delay.
    const timeoutId = setTimeout(() => {
      signal.removeEventListener("abort", onAbort);
      resolve("Operation completed");
    }, 1000);

    function onAbort() {
      // Stop the main operation and reject with the abort reason.
      clearTimeout(timeoutId);
      reject(signal.reason);
    }

    signal.addEventListener("abort", onAbort, { once: true });
  });
}
```

Друга частина прикладу викликає цю функцію й одразу скасовує її:

```js
const controller = new AbortController();
const signal = controller.signal;

startSpinner();

myCoolPromiseAPI({ /* …, */ signal })
  .then((result) => {})
  .catch((err) => {
    if (err.name === "AbortError") return;
    showUserErrorMessage();
  })
  .then(() => stopSpinner());

controller.abort();
```

Функції `startSpinner`, `stopSpinner` і `showUserErrorMessage` у прикладі не визначено. Вони означають «показати
крутилку завантаження», «сховати її» і «показати людині помилку». Ми написали для них заглушки, які лише друкують, що
їх викликали, а після `controller.abort()` дописали рядок `console.log("abort() викликано")`:

```text
крутилку показано
abort() викликано
крутилку сховано
```

Проміс відхилився з `AbortError`, обробник `catch` вийшов без повідомлення людині, а останній `then` сховав крутилку.
Рядок `abort() викликано` стоїть раніше, бо обробники `then` і `catch` виконуються мікрозадачами вже після поточного
коду. Зверніть увагу на `signal.removeEventListener` у таймері: функція прибирає свого слухача, коли робота скінчилася
успішно. Це правило з попереднього прикладу.

**Навіщо це в React.** Функцію очищення ефекту пояснено в лекції дня 5, розділ «Як це проявиться в React»: React
викликає її перед новим запуском ефекту й тоді, коли компонент зникає з екрана. У компоненті `Forecast` з лекції
цього дня ефект на кожному запуску створює новий контролер, а функція очищення скасовує саме його:

```js
useEffect(() => {
  const controller = new AbortController();          // новий контролер на кожен запуск ефекту
  fetch(base + "/weather?city=" + city, { signal: controller.signal })
    .then((res) => res.json())
    .then(setData)
    .catch((e) => { if (e.name !== "AbortError") throw e; console.log("запит скасовано:", city); });
  return () => controller.abort();                   // функція очищення скасовує запит цього запуску
}, [city]);
```

Приклад із кнопками в статті показав, чому контролер не можна створити один раз поза ефектом: після першого
скасування кожен наступний запит із тим самим сигналом відхилявся б одразу. Завдання дня вимагає того самого без
React: кожна нова літера отримує новий контролер, а попередній запит скасовують.

## Стандарт DOM, розділ `3 Aborting ongoing activities`

**Де читати:** [DOM Standard, § 3](https://dom.spec.whatwg.org/#aborting-ongoing-activities). Сервер плану:
`webstandards-docs`.

**Чому механізм скасування описано в стандарті DOM.** На перший погляд тут немає нічого про дерево вузлів. Причина
проста: `AbortSignal` є різновидом `EventTarget`, тобто об'єктом, на який можна вішати обробники подій. `EventTarget`
визначено в цьому стандарті, тому там само описано й скасування. Цей розділ призначений для всіх API, а не лише для
мережі.

**Якщо часу мало,** прочитайте вступний приклад і розділ `3.3`.

### Вступ

Стандарт показує вигадану функцію `doAmazingness` («зробити щось чудове»), яку може зупинити зовнішній код. Спершу він
показує код того, хто її викликає:

```js
const controller = new AbortController();
const signal = controller.signal;

startSpinner();

doAmazingness({ ..., signal })
  .then(result => ...)
  .catch(err => {
    if (err.name == 'AbortError') return;
    showUserErrorMessage();
  })
  .then(() => stopSpinner());

// …

controller.abort();
```

Викликач створює контролер, передає сигнал, показує крутилку завантаження й обробляє відхилення. У гілці помилки він
окремо пропускає `AbortError`: скасування сталося на прохання самого викликача, тому повідомляти людині про збій нема
чого. Три крапки в `{ ..., signal }` і `result => ...` не є кодом JavaScript. Так стандарт позначає місця, де стояли б
інші налаштування й справжня обробка результату.

Потім стандарт показує саму функцію:

```js
function doAmazingness({signal}) {
  return new Promise((resolve, reject) => {
    signal.throwIfAborted();

    // Begin doing amazingness, and call resolve(result) when done.
    // But also, watch for signals:
    signal.addEventListener('abort', () => {
      // Stop doing amazingness, and:
      reject(signal.reason);
    });
  });
}
```

Перша дія функції — `signal.throwIfAborted()`, що кидає причину, якщо сигнал уже скасовано. Друга дія — слухач події
`abort`, що відхиляє проміс із `signal.reason`. Щоб побачити, як ці частини працюють разом, ми поставили на місце
«чудової роботи» таймер на секунду, а замість крутилки й повідомлення написали заглушки, які лише друкують, що їх
викликали. Викликач лишився таким, як у стандарті, лише тепер він отримує функцію `cancel`, яка вирішує, як і коли
скасувати роботу:

```js
const startSpinner = () => console.log("  крутилку показано");
const stopSpinner = () => console.log("  крутилку сховано");
const showUserErrorMessage = () => console.log("  людині показано помилку");

function doAmazingness({ signal }) {
  return new Promise((resolve, reject) => {
    signal.throwIfAborted();
    const timer = setTimeout(() => resolve("готово"), 1000);   // «чудова робота» триває 1 с
    signal.addEventListener("abort", () => {
      clearTimeout(timer);
      reject(signal.reason);
    });
  });
}

function caller(cancel) {
  const controller = new AbortController();
  const signal = controller.signal;
  cancel(controller);

  startSpinner();
  return doAmazingness({ signal })
    .then((result) => console.log("  результат:", result))
    .catch((err) => {
      if (err.name == "AbortError") return;
      showUserErrorMessage();
    })
    .then(() => stopSpinner());
}

console.log("скасування ще до початку:");
await caller((c) => c.abort());
console.log("скасування через 100 мс:");
await caller((c) => setTimeout(() => c.abort(), 100));
console.log("скасування через 100 мс із власною причиною:");
await caller((c) => setTimeout(() => c.abort(new Error("людина пішла")), 100));
```

```text
скасування ще до початку:
  крутилку показано
  крутилку сховано
скасування через 100 мс:
  крутилку показано
  крутилку сховано
скасування через 100 мс із власною причиною:
  крутилку показано
  людині показано помилку
  крутилку сховано
```

У першому запуску сигнал скасовано ще до виклику, тому `throwIfAborted()` кинув причину. Цей виняток кинуто всередині
**виконавця**, тобто функції, яку отримує `new Promise`. Такий виняток не вилітає назовні, а відхиляє проміс, тому
таймер навіть не запустився. У другому запуску скасування прийшло під час роботи, і проміс відхилив слухач події
`abort`. В обох випадках причиною була помилка `AbortError`, тому викликач не показав людині повідомлення. У третьому
запуску причиною стала власна помилка `Error`, її ім'я не `AbortError`, і викликач вирішив, що це справжній збій. Це
перше правило з лекції: код, який упізнає скасування лише за іменем `AbortError`, власної причини не впізнає.

Функція `doAmazingness` майже дослівно збігається з функцією `wait` у лекції цього дня, бо лекція спеціально
дотримується цього зразка.

### `3.1 Interface AbortController`

Опис короткий. Конструктор створює новий сигнал і зберігає його в контролері. Метод `abort(reason)` запускає алгоритм
`signal abort` для цього сигналу. Важливе слово тут — `reason`: якщо причини не передано, стандарт створює об'єкт
`DOMException` з іменем `AbortError`.

**Незнайоме слово.** `DOMException` — це вбудований тип помилки браузерних API. Він має поля `name` і `message`, тому
код розрізняє такі помилки за `name`.

### `3.2 Interface AbortSignal`

Тут визначено сам сигнал. Для зручності ось усі його члени:

| Член | Що робить |
|------|-----------|
| `AbortSignal.abort(reason)` | Повертає новий, уже скасований сигнал |
| `AbortSignal.timeout(ms)` | Повертає сигнал, що скасується через вказаний час із причиною `TimeoutError` |
| `AbortSignal.any(signals)` | Повертає сигнал, що скасується разом із першим скасованим зі списку й отримає його причину |
| `aborted` | Чи скасовано сигнал |
| `reason` | Причина скасування |
| `throwIfAborted()` | Кидає причину, якщо сигнал скасовано, а інакше нічого не робить |
| подія `abort` і поле `onabort` | Спосіб дізнатися про скасування |

Перевірка в Node 24:

```js
const signal = AbortSignal.abort();
console.log(signal.aborted, signal.reason.name);
try {
  signal.throwIfAborted();
} catch (e) {
  console.log("throwIfAborted →", e.name);
}
```

```text
true AbortError
throwIfAborted → AbortError
```

**Незнайоме слово.** **Залежний сигнал** (dependent signal) — це сигнал, який повертає `AbortSignal.any`. Сам він
нічого не скасовує, а скасовується разом із першим скасованим сигналом зі свого списку. Сигнали зі списку стандарт
називає **джерельними** (source signals).

**Алгоритм `signal abort` своїми словами.** Цей алгоритм варто прочитати як вправу:

1. Якщо сигнал уже скасовано, алгоритм одразу закінчується. Звідси правило «другий `abort()` нічого не робить».
2. Сигнал отримує причину: передану або нову помилку `AbortError`.
3. Алгоритм знаходить залежні сигнали цього сигналу, які ще не скасовано, і дає їм ту саму причину.
4. Для самого сигналу виконуються алгоритми скасування, а потім спрацьовує подія `abort`. Те саме далі відбувається із
   залежними сигналами.

Кроки 3 і 4 видно в такому досліді. Сигнал `both` залежить від двох контролерів, `user` і `page`:

```js
const user = new AbortController();
const page = new AbortController();
const both = AbortSignal.any([user.signal, page.signal]);   // залежний сигнал

user.signal.addEventListener("abort", () => console.log("подія abort: user"));
both.addEventListener("abort", () => console.log("подія abort: both"));

user.abort(new Error("людина натиснула «Скасувати»"));
console.log("both.aborted:", both.aborted, "| причина:", both.reason.message);

page.abort(new Error("сторінку закрито"));                  // both уже скасовано, причина лишається
console.log("причина після другого abort:", both.reason.message);
```

```text
подія abort: user
подія abort: both
both.aborted: true | причина: людина натиснула «Скасувати»
причина після другого abort: людина натиснула «Скасувати»
```

Подія на `user` спрацювала раніше, ніж на `both`, бо крок 4 спершу завершує скасування самого сигналу, а потім
залежних. Залежний сигнал отримав ту саму причину, що й `user`. Скасування `page` вже нічого не змінило в `both`: крок
3 пропускає залежні сигнали, які вже скасовано, тому причина лишилася першою.

**Незнайоме слово.** `abort algorithms` — це внутрішній список дій, які інші стандарти реєструють на сигналі. Саме так
Fetch дізнається про скасування. Код сторінки цього списку не бачить: він дізнається про скасування лише з події
`abort` чи з поля `aborted`.

### `3.2.1 Garbage collection`

Цей підрозділ стосується авторів браузерів. Він пояснює, коли сигнал можна прибрати з пам'яті, щоб не перервати таймер
у `AbortSignal.timeout`. Для вас тут немає нічого практичного, тому пропустіть його.

### `3.3 Using AbortController and AbortSignal objects in APIs`

Цей розділ читається як інструкція для авторів API, але він корисний і вам, коли пишете власну функцію зі скасуванням.
Вимоги такі:

- приймати сигнал через поле `signal` в об'єкті налаштувань;
- якщо сигнал уже скасований на старті, одразу відхилити проміс його причиною;
- якщо ні, підписатися на скасування й тоді відхилити проміс його причиною;
- відхиляти невиконані проміси самою причиною, а не власною помилкою.

Останнє правило пояснює, чому `abort(new Error("..."))` дає в `catch` саме вашу помилку. Лекція показала це на функції
`wait`, а третій запуск `doAmazingness` вище показав те саме.

Функції без промісів теж можуть приймати сигнал. Наприклад, `addEventListener` має поле `signal` у налаштуваннях:
скасування просто прибирає слухача. У Node 24 це виглядає так. Об'єкт `EventTarget` стоїть замість кнопки на
сторінці:

```js
const button = new EventTarget();              // замість кнопки на сторінці
const controller = new AbortController();

button.addEventListener("click", () => console.log("клацання оброблено"), {
  signal: controller.signal,
});

button.dispatchEvent(new Event("click"));     // слухач ще є
controller.abort();                           // скасування прибирає слухача
button.dispatchEvent(new Event("click"));     // тепер нічого не друкується
console.log("кінець");
```

```text
клацання оброблено
кінець
```

Перше клацання оброблено, а друге вже ні, бо `abort()` прибрав слухача. Причину скасування тут ніхто не отримує, бо
відхиляти нема чого: функція не повертає проміса.

**Навіщо це в React.** Якщо ваша функція завантаження приймає сигнал і передає його в `fetch`, ефект може скасувати її
так само, як сам `fetch`. Наприклад, винесемо запит із компонента `Forecast` в окрему функцію `loadForecast`:

```js
function loadForecast(city, { signal }) {
  return fetch(base + "/weather?city=" + city, { signal }).then((res) => res.json());
}

useEffect(() => {
  const controller = new AbortController();
  loadForecast(city, { signal: controller.signal })
    .then(setData)
    .catch((e) => { if (e.name !== "AbortError") throw e; });
  return () => controller.abort();
}, [city]);
```

Функція `loadForecast` виконує дві вимоги розділу: приймає сигнал у полі `signal` об'єкта налаштувань і віддає його
`fetch`, який сам відхилить проміс причиною скасування. Ефектові не треба знати, як саме влаштовано завантаження: йому
досить мати контролер і викликати `abort()` у функції очищення. Цей зразок переходить із проєкту в проєкт.

### Запитання до розділу

**1. Чому механізм скасування описано в стандарті DOM, а не Fetch?**

<details><summary>Відповідь</summary>

Механізм спільний для всіх API, а не лише для мережі. `AbortSignal` спирається на `EventTarget`, визначений у
стандарті DOM, тому скасуванням можуть користуватися будь-які функції.

</details>

**2. Як із кроків `signal abort` випливає, що другий `abort()` нічого не змінює?**

<details><summary>Відповідь</summary>

Перший крок перевіряє, чи сигнал уже скасовано, і якщо так, завершує алгоритм. До кроку, що записує причину, виконання
не доходить, тому причина й надалі перша.

</details>

## Стандарт Fetch, розділ `5 Fetch API`

**Де читати:** [Fetch Standard, § 5](https://fetch.spec.whatwg.org/#fetch-api). Сервер плану: `webstandards-docs`.

**Що це за текст.** Попередні розділи стандарту описують внутрішню роботу мережі в браузері. Саме в п'ятому розділі
з'являється те, що бачить код сторінки: `Headers`, `Request`, `Response` і `fetch`. Читати підряд не варто.
Використовуйте його як довідник.

**Якщо часу мало,** прочитайте опис для розробників у `5.5`, а також кроки в `5.3` про `consume body` і в `5.6` про
відхилення проміса.

### `5.1 Headers class`

Опис об'єкта заголовків. Тут же з'являється поняття **guard**, тобто «запобіжник»: кожен об'єкт заголовків має
позначку, які зміни йому дозволені. Заголовки відповіді, яка прийшла з мережі, мають запобіжник `immutable`
(«незмінний»), і змінювати їх не можна. Заголовки відповіді, яку ви створили самі через `new Response`, мають
запобіжник `response`, і їх змінювати можна:

```js
const res = await fetch(base + "/products.json");
try {
  res.headers.set("Content-Type", "text/plain");
} catch (e) {
  console.log("відповідь із мережі:", e.name + ":", e.message);
}

const own = new Response("{}");
own.headers.set("Content-Type", "application/json");
console.log("власна відповідь:", own.headers.get("Content-Type"));
```

```text
відповідь із мережі: TypeError: immutable
власна відповідь: application/json
```

Node у тексті помилки прямо назвав запобіжник: `immutable`.

### `5.2 BodyInit unions`

Перелік типів, які можна передати як тіло: `Blob`, `BufferSource`, `FormData`, `URLSearchParams`, потік і рядок.
`BufferSource` — це спільна назва для сирих байтів у пам'яті: `ArrayBuffer` чи масиву байтів на зразок `Uint8Array`,
який ви бачили в лекції. Тут же описано, який заголовок `Content-Type` браузер поставить сам:

```js
const url = "https://example.org/post";
const form = new Request(url, { method: "POST", body: new URLSearchParams({ city: "lviv" }) });
const text = new Request(url, { method: "POST", body: "привіт" });
const json = new Request(url, { method: "POST", body: JSON.stringify({ city: "lviv" }) });
console.log("URLSearchParams:", form.headers.get("Content-Type"));
console.log("рядок:", text.headers.get("Content-Type"));
console.log("рядок із JSON:", json.headers.get("Content-Type"));
```

```text
URLSearchParams: application/x-www-form-urlencoded;charset=UTF-8
рядок: text/plain;charset=UTF-8
рядок із JSON: text/plain;charset=UTF-8
```

Останній рядок важливий. Результат `JSON.stringify` для браузера є звичайним рядком, і браузер не знає, що всередині
JSON. Тому для JSON заголовок `Content-Type: application/json` ставлять власноруч, як у прикладах статті. Саме такий
заголовок робить запит на чуже джерело непростим, і перед ним піде попередній запит (див. розділ статті `Making
cross-origin requests` вище).

### `5.3 Body mixin`

**Незнайоме слово.** `mixin` означає «домішка»: набір полів і методів, спільний для кількох об'єктів. Тут спільними є
тіла `Request` і `Response`, тому `request.text()` і `response.text()` поводяться однаково.

Це головний для нашого дня підрозділ. Три визначення:

- **`unusable`** (непридатне): об'єкт вважається непридатним, якщо тіло є, а його потік потривожено або заблоковано.
- **`bodyUsed`**: поле повертає `true`, якщо тіло є і потік потривожено.
- **`consume body`**: спільний алгоритм для `json()`, `text()`, `blob()` та інших.

Алгоритм `consume body` переказуємо своїми словами:

1. Якщо об'єкт непридатний, повернути проміс, відхилений із `TypeError`. Ось причина другого читання.
2. Створити новий проміс.
3. Якщо тіла немає, вважати, що прочитано порожню послідовність байтів.
4. Інакше прочитати все тіло.
5. Перетворити байти на результат потрібного формату. Якщо перетворення кинуло помилку, відхилити проміс нею. Так
   з'являється `SyntaxError` для поганого JSON.

Звідси випливають три наслідки. По-перше, на відповіді без тіла поле `bodyUsed` завжди буде `false`, бо потоку немає і
нема чого тривожити. По-друге, `text()` на такій відповіді дасть порожній рядок, а `json()` впаде на розборі
порожнього тексту. По-третє, статус і заголовок `Content-Type` в алгоритмі не згадано, тому `json()` на них не
дивиться. Перевірка в Node 24:

```js
const empty = new Response(null);
console.log("text() без тіла:", JSON.stringify(await empty.text()), "| bodyUsed:", empty.bodyUsed);
try {
  await new Response(null).json();
} catch (e) {
  console.log("json() без тіла →", e.name + ":", e.message);
}

const page = new Response("<html>500</html>", { status: 500, headers: { "Content-Type": "text/html" } });
try {
  await page.json();
} catch (e) {
  console.log("json() на сторінці зі статусом 500 →", e.name + ":", e.message);
}
```

```text
text() без тіла: "" | bodyUsed: false
json() без тіла → SyntaxError: Unexpected end of JSON input
json() на сторінці зі статусом 500 → SyntaxError: Unexpected token '<', "<html>500</html>" is not valid JSON
```

`JSON.stringify` у першому рядку коду потрібен лише для того, щоб порожній рядок було видно у виводі як `""`. Після
`text()` поле `bodyUsed` лишилося `false`, бо тіла не було. Останній рядок показує третій наслідок: статус 500 і тип
`text/html` не завадили `json()` спробувати розібрати сторінку, і впав саме розбір.

### `5.4 Request class`

Опис об'єкта запиту й усіх полів налаштувань. Цей підрозділ довгий, бо кожен параметр має власні обмеження. Тут є й
сигнал: кожен `Request` має власний сигнал, який стежить за переданим у налаштуваннях. Це залежний сигнал з розділу
`3.2` стандарту DOM:

```js
const controller = new AbortController();
const request = new Request("https://example.org/", { signal: controller.signal });
console.log("той самий об'єкт?", request.signal === controller.signal);
console.log("до abort:", request.signal.aborted);
controller.abort();
console.log("після abort:", request.signal.aborted, request.signal.reason.name);
```

```text
той самий об'єкт? false
до abort: false
після abort: true AbortError
```

Сигнал запиту — окремий об'єкт, але скасування контролера дійшло й до нього разом із причиною.

### `5.5 Response class`

Тут визначено поля відповіді. Поле `ok` повертає `true`, якщо статус є `ok status`, а цей термін означає діапазон від
200 до 299 включно. Метод `clone()` кидає `TypeError`, якщо об'єкт непридатний. Три статичні методи створюють готові
відповіді без мережі. `Response.error()` створює відповідь, що зображає мережеву помилку: тип `error` і статус 0.
`Response.redirect()` створює перенаправлення на іншу адресу. `Response.json()` створює відповідь із тілом JSON і
правильним заголовком. Перевірка в Node 24:

```js
const error = Response.error();
console.log("error():", error.type, error.status, error.ok);
const moved = Response.redirect("https://example.org/new", 302);
console.log("redirect():", moved.status, moved.headers.get("Location"));
const data = Response.json({ city: "lviv" });
console.log("json():", data.status, data.headers.get("Content-Type"), await data.json());
```

```text
error(): error 0 false
redirect(): 302 https://example.org/new
json(): 200 application/json { city: 'lviv' }
```

`Response.error()` ви вже бачили в коді сервіс-воркера в розділі статті `Locked and disturbed streams`: там він
повертає сторінці «мережеву помилку», коли запит у мережу не вдався. `Response.json()` зручний у тестах, щоб не писати
`JSON.stringify` і заголовок самому.

### `5.6 Fetch methods`

Найцінніший підрозділ для точної відповіді про `fetch`. Переказуємо кроки, важливі для нашої теми:

1. Створюється об'єкт запиту. Якщо адреса чи налаштування неправильні, тут виникає виняток, і проміс відхиляється.
   Саме на цьому кроці впав другий `fetch` з того самого запиту в розділі статті `Setting a body`: конструктор
   `Request` не взяв запит, тіло якого вже прочитано.
2. Якщо сигнал уже скасовано, проміс відхиляється причиною скасування, і запит не надсилається.
3. Додається дія на сигнал: при скасуванні запит переривається, а проміс відхиляється причиною.
4. Коли прийшла відповідь, алгоритм перевіряє, чи вона не є мережевою помилкою. Якщо є, проміс відхиляється з
   `TypeError`.
5. Інакше створюється об'єкт `Response`, і проміс виконується ним.

Другий крок легко перевірити. Сервер нижче записує кожен запит, який отримав, у масив `seen`:

```js
const controller = new AbortController();
controller.abort();
try {
  await fetch(base + "/products.json", { signal: controller.signal });
} catch (e) {
  console.log("fetch →", e.name);
}
await fetch(base + "/products.json");          // звичайний запит для порівняння
console.log("сервер отримав:", seen);
```

```text
fetch → AbortError
сервер отримав: [ 'GET /products.json' ]
```

Перший `fetch` відхилився з `AbortError`. Сервер отримав лише один запит, тобто другий, звичайний. Запит з уже
скасованим сигналом до сервера не дійшов.

Окремий алгоритм `abort the fetch() call` робить кілька дій. Він відхиляє проміс, але це нічого не змінює, якщо той
уже виконаний. Він скасовує тіло запиту, якщо воно ще читається. Якщо об'єкт відповіді вже існує, він переводить тіло
відповіді в стан помилки. Останній пункт пояснює, чому скасування між заголовками й тілом відхиляє `res.json()`.

**Поняття `network error`.** У стандарті це особливий вид внутрішньої відповіді, а не виняток. Він з'являється, коли
зв'язку немає, CORS заборонив читання або запит не вдалося виконати. Код сторінки ніколи не отримує такої відповіді
від `fetch`, бо `fetch` замість неї відхиляє проміс із `TypeError`. Створити таку відповідь самому можна через
`Response.error()`.

### `5.7 Garbage collection`

Стандарт дозволяє браузеру перервати запит, лише коли результат точно нікому не потрібен і код цього переривання ніяк
не помітить. Для прикладного коду це майже нічого не змінює, тому розділ можна пропустити.

**Навіщо це в React.** Стандарт дає точну відповідь там, де документація бібліотеки мовчить. Ось запитання, яке
виникає з компонентом `Forecast` з лекції: функція очищення викликала `abort()`, коли `fetch` уже виконався, а тіло ще
йшло. Чи може `setData` після цього отримати дані? Алгоритм `abort the fetch() call` відповідає «ні». Він переводить
потік тіла в стан помилки, тому `res.json()` відхиляється причиною скасування. Через це `then(setData)` пропускається,
і відхилення доходить до `catch`, який упізнає `AbortError`. Лекція показала саме цей випадок запуском на адресі
`/slow-body` (розділ «`AbortController` і `AbortSignal`: як зупинити роботу»).

### Запитання до розділу

**1. Чи перевіряє `json()` заголовок `Content-Type`?**

<details><summary>Відповідь</summary>

Ні. Алгоритм `consume body` читає байти й передає їх розбору JSON. Заголовка він не перевіряє. Тому HTML зі статусом
200 дасть `SyntaxError`.

</details>

**2. Запит пішов, прийшли заголовки, потім викликано `abort()`. Чому результат `fetch` не змінюється, але читання тіла
падає?**

<details><summary>Відповідь</summary>

Виконаний проміс не може змінитися, тому відхилення в цьому місці нічого не робить. Алгоритм скасування ще переводить
потік тіла відповіді в стан помилки, тому наступне читання відхиляється причиною скасування.

</details>

## Книжка How to Design Programs, `3.1 Designing Functions` і `4.3 Enumerations`

**Де читати:** [htdp.org, частина перша](https://htdp.org/2023-8-14/Book/part_one.html), розділи
[3.1](https://htdp.org/2023-8-14/Book/part_one.html#%28part._sec~3adesign-func%29) і
[4.3](https://htdp.org/2023-8-14/Book/part_one.html#%28part._sec~3aenums%29). Сервер плану: `htdp-book`. Текст книжки
не можна поширювати, тому нижче лише короткий переказ.

**Що це за текст.** Підручник про систематичне проєктування програм. У ньому використано навчальну мову BSL, але
рецепт не залежить від мови. Ви вже застосовуєте його в днях 4 і 5, тому зараз варто подивитися, що він дає для
мережевого коду.

### `3.1 Designing Functions`

Сам рецепт із шести кроків уже розібрано в [розборі читання дня 4](f0-d04-reading.md), розділ «How to Design
Programs, розділ 3». Як він змінюється для функції, що повертає проміс, сказано в [розборі дня 5](f0-d05-reading.md),
розділ «Рецепт для функції, що повертає проміс». Тут лише те, що варто перечитати сьогодні.

Розділ починається з різниці між **інформацією** й **даними**. Інформація — це факти про світ задачі, наприклад
«сервер не знайшов такого міста». Дані — це те, чим програма записує ці факти, наприклад число 404 у полі
`res.status`. Програма перекладає інформацію в дані, обробляє їх і перекладає результат назад в інформацію для людини.
У мережевому коді цей переклад іде двічі. Сервер записав свою інформацію статусом і тілом відповіді. Ваш код мусить
прочитати ці дані й сказати людині щось зрозуміле, наприклад «Немає такого міста».

**Навіщо це сьогодні.** Новим у мережевому коді є дві речі: прикладам потрібен сервер, а функція ще й приймає сигнал
скасування. Сигнатура показує сигнал так само, як будь-який інший параметр. Ось сигнатура й призначення для функції
`wait` з лекції цього дня:

```js
// number, AbortSignal -> Promise<string>
// Проміс, який через ms мілісекунд виконується рядком "дочекалися",
// а після скасування відхиляється причиною скасування.
function wait(ms, signal) {
  // … тіло з лекції …
}
```

Для функції, що робить запит, приклади мають описати кожен результат, який вона може дати: успішну відповідь зі
статусом 200, відповідь зі статусом помилки, наприклад 404, і скасування.

### `4.3 Enumerations`

**Перелік** (enumeration) — це опис даних, який просто називає всі можливі значення. Книжка показує його на рядках,
якими бібліотека повідомляє програмі про події миші (`"button-down"`, `"move"` та інші), і на трьох кольорах
світлофора. Функція, що приймає перелік, розглядає кожне значення окремою гілкою: у книжці функція, яка повертає
наступний колір світлофора, має три гілки на три кольори. Трохи далі, у прикладі з клавішами, книжка показує й інший
варіант. Коли програмі важливі лише дві клавіші, решту значень можна зібрати в одну гілку `else`.

Скільки прикладів потрібно такій функції, книжка каже трохи пізніше, у розділі `4.6 Designing with Itemizations`:
щонайменше по одному на кожен варіант з опису даних.

**Навіщо це сьогодні.** У практиці дня вигаданий сервер записує кожен запит у журнал. Поле `outcome` у записі журналу
каже, чим скінчився запит, і є саме таким переліком із чотирьох рядків. Коли варіанти названо, забути один із них
стає важче.

**Навіщо це в React.** Стан завантаження компонента майже завжди є таким переліком: «завантажуємо», «є дані»,
«помилка». Його можна записати двома способами:

```js
// Три незалежні поля: ніщо не забороняє заповнити кілька з них водночас.
const flags = { loading: true, error: new Error("500"), data: null };   // «і завантажуємо, і помилка»

// Перелік: поле status — один із рядків "loading", "success", "error".
const state = { status: "error", error: new Error("500") };
```

У першому записі можна випадково отримати стан, де `loading` і `error` заповнено водночас, і компонент мусить
вирішувати, що з цього показати. У другому записі поле `status` має рівно одне значення, тому такого стану записати
неможливо. Компонент тоді розглядає три гілки, як функція світлофора в книжці.

### Запитання до книжки

**1. Чим інформація відрізняється від даних на прикладі статусу 404?**

<details><summary>Відповідь</summary>

Інформація — це факт «сервер не знайшов такої адреси». Дані — це число 404 у полі `res.status`. Програма перетворює
дані на те, що зрозуміє людина: наприклад, на текст «Немає такого міста».

</details>

**2. Скільки прикладів вимагає функція, що приймає перелік із чотирьох значень?**

<details><summary>Відповідь</summary>

Щонайменше по одному на кожне значення, тобто чотири. Інакше одна гілка залишиться неперевіреною.

</details>

---

Цей розбір написано для плану. Він переказує своїми словами сторінки MDN (CC BY-SA 2.5), стандарти WHATWG DOM і Fetch
(CC BY 4.0) і коротко переказує книжку How to Design Programs. Код прикладів MDN наведено за ліцензією CC0, код
прикладів зі стандарту DOM — за ліцензією CC BY 4.0. Права на оригінальні тексти належать їхнім авторам. Приклади коду
запущено в Node 24.
