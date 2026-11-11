# Розбір читання. День 5. Асинхронність

Цей файл пояснює, що саме написано в матеріалах дня. Лекція розповідає про саму тему, а розбір допомагає читати чужі
тексти: він показує, де що шукати, що означають незнайомі слова й що із прочитаного стане в пригоді в React. Оригінали
англійською, тому назви розділів наведено англійською, щоб їх легко було знайти.

Читайте в такому порядку: лекція, `Using promises`, `async function`, `Promise.all()`, `Promise.allSettled()`, розділ
стандарту HTML і наприкінці розділ книжки. Стандарт написано не так, як посібник, тому перед ним є окреме пояснення,
як його читати.

## Using promises (MDN)

**Де читати:** [Using promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises).

**Що це за текст.** Це посібник MDN про те, як користуватися промісами, а не як їх створювати. **Проміс** означає
об'єкт, що представляє результат незавершеної роботи. Сторінка починає з вигаданої функції `createAudioFileAsync`, яка
створює звуковий файл. Спершу MDN показує, як цю функцію викликали б без промісів:

```js
function successCallback(result) {
  console.log(`Audio file ready at URL: ${result}`);
}

function failureCallback(error) {
  console.error(`Error generating audio file: ${error}`);
}

createAudioFileAsync(audioSettings, successCallback, failureCallback);
```

Тут ви самі пишете дві функції й передаєте їх у `createAudioFileAsync` разом із налаштуваннями `audioSettings`.
Функцію `successCallback` вона викличе, коли файл буде готовий, а функцію `failureCallback` викличе, якщо станеться
помилка. Далі MDN показує ту саму дію з промісом:

```js
createAudioFileAsync(audioSettings).then(successCallback, failureCallback);
```

Тепер `createAudioFileAsync` приймає лише налаштування й повертає проміс. Ті самі дві функції ви передаєте вже не
їй, а методу `then` цього проміса. Функцію `createAudioFileAsync` вигадано для прикладу, тому цей код сам по собі не
запуститься.

**Якщо часу мало,** прочитайте `Chaining`, `Error handling`, `Composition` і `Timing`.

### Chaining

**Ланцюжок** (chaining) означає кілька асинхронних кроків поспіль, де кожен використовує результат попереднього.
**Зворотний виклик** (callback) — це функція, яку ви передаєте комусь, щоб він викликав її пізніше. Без промісів
кожен наступний крок доводиться передавати зворотним викликом усередину попереднього. MDN показує, який вигляд має
такий код:

```js
doSomething(function (result) {
  doSomethingElse(result, function (newResult) {
    doThirdThing(newResult, function (finalResult) {
      console.log(`Got the final result: ${finalResult}`);
    }, failureCallback);
  }, failureCallback);
}, failureCallback);
```

Функція `doSomething` після своєї роботи викликає першу передану функцію. Та викликає `doSomethingElse` і передає їй
другу функцію, а друга викликає `doThirdThing` із третьою. Кожен крок зсуває код праворуч, і функцію `failureCallback`
доводиться передавати тричі, по разу на кожен крок. Такий код прийнято називати callback hell, тобто «пекло зворотних
викликів». Усі функції в прикладах цього розділу вигадано, тому код сам по собі не запуститься.

Головна думка розділу: `then` повертає новий проміс, а не той самий. MDN показує це двома рядками:

```js
const promise = doSomething();
const promise2 = promise.then(successCallback, failureCallback);
```

Проміс `promise2` стане виконаним не тоді, коли закінчиться `doSomething`, а тоді, коли закінчиться ще й функція,
передана в `then`. Якщо ця функція сама повертає проміс, `promise2` чекає ще й на нього. Тому до `promise2` можна
приєднати наступний `then`, і так утворюється ланцюжок. Той самий триступеневий код із промісами MDN записує так:

```js
doSomething()
  .then((result) => doSomethingElse(result))
  .then((newResult) => doThirdThing(newResult))
  .then((finalResult) => {
    console.log(`Got the final result: ${finalResult}`);
  })
  .catch(failureCallback);
```

Кожен `then` отримує результат попереднього кроку. Стрілкова функція без фігурних дужок повертає свій вираз, тому
запис `(result) => doSomethingElse(result)` повертає проміс від `doSomethingElse`, і наступний `then` чекає на нього.
Функція `failureCallback` тепер стоїть один раз, у `catch` наприкінці.

Важливе застереження стосується **забутих промісів** (floating promises), про які розповідала лекція. Забутим
називають проміс, який хтось запустив, але не повернув, тому за ним ніхто не стежить. MDN показує таку помилку:

```js
doSomething()
  .then((url) => {
    // Missing `return` keyword in front of fetch(url).
    fetch(url);
  })
  .then((result) => {
    // result is undefined, because nothing is returned from the previous
    // handler. There's no way to know the return value of the fetch()
    // call anymore, or whether it succeeded at all.
  });
```

Перша функція запускає запит `fetch(url)`, але перед ним немає `return`, тому функція нічого не повертає. Через це
другий `then` не чекає на запит, а отримує `undefined`, як пише коментар MDN. Дізнатися, чим закінчився запит, тепер
неможливо. Сторінка дає просте правило: щойно з'являється проміс, поверніть його. Тоді наступний `then` дочекається
запиту й отримає його результат.

Наприкінці розділу той самий ланцюжок переписано через `async` і `await`:

```js
async function logIngredients() {
  const url = await doSomething();
  const res = await fetch(url);
  const data = await res.json();
  listOfIngredients.push(data);
  console.log(listOfIngredients);
}
```

Кожен `await` чекає на проміс і дає його значення, тому код читається зверху вниз, як звичайний синхронний. Сторінка
попереджає, що слово `await` легко забути. Також вона каже, що `await` призупиняє лише код цієї функції, який залежить
від значення, а не всю програму: інший код тим часом працює далі.

### Error handling

Відхилення, тобто стан проміса, коли робота закінчилася помилкою, проходить ланцюжком униз до найближчого `catch`.
Так само виняток у звичайному коді йде до найближчого `try…catch`. MDN показує цю схожість синхронним варіантом того
самого ланцюжка з розділу `Chaining`:

```js
try {
  const result = syncDoSomething();
  const newResult = syncDoSomethingElse(result);
  const finalResult = syncDoThirdThing(newResult);
  console.log(`Got the final result: ${finalResult}`);
} catch (error) {
  failureCallback(error);
}
```

Якщо будь-який із трьох рядків кине виняток, решта рядків у `try` не виконається, і керування перейде в `catch`.
Ланцюжок промісів поводиться так само: якщо будь-який крок відхилиться, наступні `then` пропускаються, і спрацьовує
`catch` наприкінці. Тому зазвичай досить одного `catch` наприкінці. Те саме стосується винятків, кинутих усередині
функції з `then`: проміс перетворює такий виняток на відхилення. Приклад цього є нижче, у розділі
`Chaining after a catch`.

### Nesting

**Вкладений** ланцюжок означає ланцюжок, що стоїть усередині функції, переданої в `then` іншого ланцюжка. Він обмежує
дію `catch`: зовнішній `catch` не побачить помилок, які перехопив внутрішній. Це корисно для необов'язкових кроків,
бо збій необов'язкового кроку тоді не зупиняє головну роботу. Ось приклад MDN:

```js
doSomethingCritical()
  .then((result) =>
    doSomethingOptional(result)
      .then((optionalResult) => doSomethingExtraNice(optionalResult))
      .catch((e) => {}),
  ) // Ignore if optional stuff fails; proceed.
  .then(() => moreCriticalStuff())
  .catch((e) => console.error(`Critical failure: ${e.message}`));
```

Тут два ланцюжки. Зовнішній ланцюжок складається з `doSomethingCritical`, першого `then`, другого `then` із
`moreCriticalStuff` і останнього `catch`. Внутрішній ланцюжок стоїть у дужках першого `then` і складається з
`doSomethingOptional`, `doSomethingExtraNice` і порожнього `catch`. MDN звертає увагу, що вкладеність створюють саме
ці дужки, а не відступи. Порожній `catch((e) => {})` перехоплює помилку необов'язкових кроків і нічого з нею не
робить, тому внутрішній ланцюжок усе одно стає виконаним, і зовнішній іде далі до `moreCriticalStuff`.

Функції в прикладі вигадані. Щоб побачити, як приклад працює, ми написали заглушки. Кожна заглушка друкує свою назву
й повертає виконаний проміс. Лише та заглушка, чию назву передали під час запуску, повертає відхилений проміс. Нижче
весь файл `nest.mjs`: спершу наші заглушки, а після них без змін код MDN із прикладу вище. Без коду MDN заглушок ніхто
не викликає, і файл нічого не надрукує.

```js
// Наші заглушки. Аргумент запуску вибирає, який крок зламається.
const broken = process.argv[2];
const step = (name) => (input) => {
  console.log("крок", name);
  return broken === name
    ? Promise.reject(new Error(name + " зламався"))
    : Promise.resolve(name + " готово");
};
const doSomethingCritical = step("critical");
const doSomethingOptional = step("optional");
const doSomethingExtraNice = step("extraNice");
const moreCriticalStuff = step("moreCritical");

// Код MDN без змін.
doSomethingCritical()
  .then((result) =>
    doSomethingOptional(result)
      .then((optionalResult) => doSomethingExtraNice(optionalResult))
      .catch((e) => {}),
  ) // Ignore if optional stuff fails; proceed.
  .then(() => moreCriticalStuff())
  .catch((e) => console.error(`Critical failure: ${e.message}`));
```

Ми запустили файл у Node 24 тричі: без збою, зі збоєм необов'язкового кроку й зі збоєм головного кроку. Рядки, що
починаються з `==`, друкує сама команда запуску, щоб було видно, де закінчується один запуск і починається інший:

```bash
for b in none optional critical; do echo "== $b"; node nest.mjs $b; done
```

```text
== none
крок critical
крок optional
крок extraNice
крок moreCritical
== optional
крок critical
крок optional
крок moreCritical
== critical
крок critical
Critical failure: critical зламався
```

Без збою виконуються всі чотири кроки. Коли зламався `doSomethingOptional`, крок `doSomethingExtraNice` пропущено,
бо він стоїть у тому самому внутрішньому ланцюжку після зламаного кроку. Внутрішній `catch` мовчки перехопив помилку,
тому `moreCriticalStuff` усе одно виконався, а зовнішній `catch` нічого не надрукував. Коли зламався
`doSomethingCritical`, внутрішній ланцюжок навіть не почався, бо перший `then` пропущено. Помилку перехопив лише
зовнішній `catch`, і він надрукував `Critical failure`.

Автори застерігають: якщо у вас немає складної обробки помилок, вкладені `then` вам, найімовірніше, не потрібні.

### Chaining after a catch

Після `catch` можна поставити ще `then`. MDN показує це на такому прикладі:

```js
doSomething()
  .then(() => {
    throw new Error("Something failed");

    console.log("Do this");
  })
  .catch(() => {
    console.error("Do that");
  })
  .then(() => {
    console.log("Do this, no matter what happened before");
  });
```

Щоб запустити його, ми поставили перед ним функцію `doSomething` із шаблону, який MDN дає в розділі `Chaining`. Ця
функція через 200 мс друкує `Did something` і виконує свій проміс. Нижче код шаблону, а під ним вивід Node 24 для
обох фрагментів разом:

```js
function doSomething() {
  return new Promise((resolve) => {
    setTimeout(() => {
      // Other things to do before completion of the promise
      console.log("Did something");
      // The fulfillment value of the promise
      resolve("https://example.com/");
    }, 200);
  });
}
```

```text
Did something
Do that
Do this, no matter what happened before
```

Перший рядок друкує сама `doSomething`. Далі функція з першого `then` кидає виняток. Рядок `console.log("Do this")`
стоїть після `throw`, тому він не виконується, і `Do this` не друкується. Виняток робить проміс від першого `then`
відхиленим, тому спрацьовує `catch` і друкує `Do that`. Функція з `catch` закінчилася без помилки, тож проміс, який
повертає `catch`, стає виконаним. Через це спрацьовує останній `then` і друкує свій рядок. На сторінці MDN вивід має
два рядки, бо там не враховано рядок `Did something` від шаблону.

Отже, кроки після `catch` виконуються незалежно від того, чи була помилка. Це той самий механізм, який дає значення за
замовчуванням у лекції.

### Promise rejection events

Якщо відхилення ніхто не обробив, браузер запускає подію `unhandledrejection` на глобальному об'єкті. **Глобальний
об'єкт** — це об'єкт, який існує один на всю сторінку й доступний з будь-якого місця коду. На звичайній сторінці це
`window`, а у воркері це об'єкт самого воркера. Якщо обробник додали пізніше, запускається `rejectionhandled`. Обидві
події мають поле `promise` із самим відхиленим промісом і поле `reason` із причиною відхилення. Подію
`unhandledrejection` можна використати, щоб надсилати такі помилки на сервер.

У Node замість цього ставлять **слухача**, тобто функцію, яку Node викличе, коли станеться подія. MDN наводить такий
запис:

```js
process.on("unhandledRejection", (reason, promise) => {
  // Add code here to examine the "promise" and "reason" values
});
```

Зверніть увагу на назву: у Node подія пишеться `unhandledRejection`, з великою літерою R. Сторінка застерігає: якщо
поставити такий слухач і нічого в ньому не робити, помилки зникатимуть мовчки. Типова поведінка Node без слухача
інша: процес завершується з кодом 1.

### Composition

Тут названо чотири методи, що працюють з кількома промісами одночасно: `Promise.all()`, `Promise.allSettled()`,
`Promise.any()` і `Promise.race()`. Лекція розбирає кожен із них. Сторінка показує перший так:

```js
Promise.all([func1(), func2(), func3()]).then(([result1, result2, result3]) => {
  // use result1, result2 and result3
});
```

Усі три функції викликано одразу, тому три роботи йдуть одночасно. Функція з `then` отримує масив із трьох
результатів і запис `[result1, result2, result3]` одразу розкладає його по трьох змінних.
Сторінка каже прямо: якщо `Promise.all` відхилено, інші операції тривають, просто їхні результати вже не потрапляють
у результат `Promise.all`.

Далі йде **послідовне поєднання**: функції викликаються по черзі, і кожна отримує результат попередньої. MDN записує
його через метод масиву `reduce`, знайомий з лекції дня 2. Цей метод проходить масив і щоразу поєднує вже накопичене
значення з наступним елементом:

```js
[func1, func2, func3]
  .reduce((p, f) => p.then(f), Promise.resolve())
  .then((result3) => {
    /* use result3 */
  });
```

Накопичене значення тут є промісом `p`. Спочатку це готовий проміс `Promise.resolve()`. На кожному кроці `reduce`
дописує до нього ще один `then` із наступною функцією `f`. Після трьох кроків виходить ланцюжок, який MDN виписує
окремо:

```js
Promise.resolve()
  .then(func1)
  .then(func2)
  .then(func3)
  .then((result3) => {
    /* use result3 */
  });
```

Функції `func1`, `func2` і `func3` на сторінці вигадані. Щоб побачити порядок, ми написали заглушки й поставили їх
перед кодом MDN із `reduce`. Кожна заглушка чекає 100 мс, друкує, що отримала, і повертає наступне число. У порожній
функції з останнього `then` ми додали лише рядок `console.log`:

```js
// Наші заглушки: кожна функція чекає 100 мс, друкує, що отримала, і повертає наступне число.
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const func1 = async (x) => { await wait(100); console.log("func1 отримала", x); return 1; };
const func2 = async (x) => { await wait(100); console.log("func2 отримала", x); return 2; };
const func3 = async (x) => { await wait(100); console.log("func3 отримала", x); return 3; };

// Код зі сторінки MDN.
[func1, func2, func3]
  .reduce((p, f) => p.then(f), Promise.resolve())
  .then((result3) => {
    /* use result3 */
    console.log("result3 =", result3);
  });
```

```text
func1 отримала undefined
func2 отримала 1
func3 отримала 2
result3 = 3
```

Функція `func1` отримала `undefined`, бо проміс `Promise.resolve()` не має значення. Кожна наступна функція отримала
те, що повернула попередня, і почала роботу лише після того, як попередня закінчилася.

Потім MDN загортає цей прийом у функцію `composeAsync`, яку можна використати повторно:

```js
const applyAsync = (acc, val) => acc.then(val);
const composeAsync =
  (...funcs) =>
  (x) =>
    funcs.reduce(applyAsync, Promise.resolve(x));
```

Функція `composeAsync` приймає будь-яку кількість функцій і повертає нову функцію. Нова функція приймає початкове
значення `x` і пропускає його через усі функції по черзі тим самим `reduce`. Функцію `applyAsync` винесено окремо, і
вона робить те саме, що й `(p, f) => p.then(f)` вище. Сторінка показує виклик:

```js
const transformData = composeAsync(func1, func2, func3);
const result3 = transformData(data);
```

Ми запустили цей код із заглушками, які додають 1, множать на 2 і віднімають 3, і з початковим значенням 10. Окремо
ми надрукували змінну `result3` і значення, яке вона дасть:

```js
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const func1 = async (x) => { await wait(100); console.log("func1 отримала", x); return x + 1; };
const func2 = async (x) => { await wait(100); console.log("func2 отримала", x); return x * 2; };
const func3 = async (x) => { await wait(100); console.log("func3 отримала", x); return x - 3; };

const applyAsync = (acc, val) => acc.then(val);
const composeAsync =
  (...funcs) =>
  (x) =>
    funcs.reduce(applyAsync, Promise.resolve(x));

const transformData = composeAsync(func1, func2, func3);
const result3 = transformData(10);
console.log(result3);
result3.then((value) => console.log("значення:", value));
```

```text
Promise { <pending> }
func1 отримала 10
func2 отримала 11
func3 отримала 22
значення: 19
```

Перший рядок показує важливу річ, яку назва змінної на сторінці приховує: `result3` є не числом, а промісом, і в мить
друку він ще очікує. Саме значення 19 можна отримати лише через `then` або `await`.

Наостанок MDN показує те саме послідовне поєднання через цикл:

```js
let result;
for (const f of [func1, func2, func3]) {
  result = await f(result);
}
/* use last result (i.e. result3) */
```

Метод `reduce` тут не є обов'язковим, бо `for…of` із `await` робить те саме й читається легше. Сторінка радить
спершу подумати, чи потрібен послідовний порядок узагалі. Якщо одна робота не залежить від результату іншої, краще
запускати їх разом, щоб вони не чекали одна на одну.

### Cancellation

Цей розділ має одне речення: у промісів немає вбудованого скасування, а скасовувати треба саму операцію, зазвичай
через `AbortController`. Детальніше про це розповість день 6.

### Creating a Promise around an old callback API

Старі функції приймають зворотний виклик і нічого не повертають, а `new Promise` дозволяє загорнути їх у проміс.
Найвідоміша така функція — `setTimeout`. MDN показує, у чому з нею проблема:

```js
setTimeout(() => saySomething("10 seconds passed"), 10 * 1000);
```

Через 10 секунд таймер викличе функцію, а та викличе `saySomething`. Якщо `saySomething` кине виняток, його ніхто не
перехопить, бо так влаштовано `setTimeout`. Ми перевірили це в Node 24: поставили перед цим рядком свою заглушку
`saySomething`, яка завжди кидає виняток. Через 10 секунд Node надрукував помилку й завершив процес із кодом 1. У
виводі нижче ми прибрали рядки зі шляхом до файла й переліком викликів:

```js
// Наша заглушка: функція, яка завжди кидає виняток.
function saySomething(text) {
  throw new Error("не вдалося сказати: " + text);
}
```

```text
Error: не вдалося сказати: 10 seconds passed

Node.js v24.22.0
```

Далі MDN загортає `setTimeout` у проміс:

```js
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

wait(10 * 1000)
  .then(() => saySomething("10 seconds"))
  .catch(failureCallback);
```

Функція `wait` створює проміс. Конструктор `new Promise` одразу викликає функцію, яку йому передали, і дає їй функцію
`resolve`. Таку передану функцію називають **виконавцем** (executor). Тут виконавець лише ставить таймер, а таймер
через `ms` мілісекунд викликає `resolve`, і проміс стає виконаним. Другу функцію, `reject`, конструктор теж дає, але
виконавець її не бере. MDN пояснює чому: `setTimeout` насправді не може зламатися. Тепер `saySomething` викликається
всередині `then`, тому її виняток стає відхиленням і потрапляє в `catch`. Ми запустили цей код із тією самою заглушкою
`saySomething` і з такою функцією `failureCallback`:

```js
// Наш обробник помилки.
function failureCallback(error) {
  console.log("Помилку перехоплено:", error.message);
}
```

```text
Помилку перехоплено: не вдалося сказати: 10 seconds
```

Отже, `setTimeout` загорнуто у функцію `wait` рівно один раз. Сторінка радить робити таке загортання на найнижчому
рівні й потім ніде не викликати стару функцію напряму. На цьому ж прийомі побудовано вигадані запити в завданні дня.

### Timing

Цей розділ найважливіший для дня. Він пояснює, **коли саме** виконується функція, яку передали в `then`. Розділ має
три підрозділи. Перші два показують фрагменти коду, і нижче кожен фрагмент наведено разом із тим, що він надрукував у
Node 24.

**Підрозділ `Guarantees`, тобто «гарантії».** Він починає з проблеми, яку мали старі функції без промісів. Така
функція приймала зворотний виклик, тобто функцію, яку вона мала викликати, коли закінчить роботу. Коли саме його
викликати, вирішував автор такої функції. MDN показує невдалий приклад, де автор вирішує це навмання:

```js
function doSomething(callback) {
  if (Math.random() > 0.5) {
    callback(); // викликати одразу, ще до виходу з doSomething
  } else {
    setTimeout(() => callback(), 1000); // викликати через секунду
  }
}

let value = 1;
doSomething(() => {
  value = 2;
});
console.log(value);
```

Функція `Math.random()` повертає випадкове число від 0 до 1, тому `doSomething` у половині випадків викликає зворотний
виклик одразу, а в іншій половині викликає його через секунду. Ми запустили цей код десять разів: сім запусків
надрукували `2`, а три запуски надрукували `1`. Коли зворотний виклик спрацював одразу, змінна `value` встигла стати 2
ще до рядка `console.log`. Коли він спрацював через секунду, рядок `console.log` уже надрукував 1. Код, який викликає
`doSomething`, не може заздалегідь знати, який випадок станеться, і тому не може покладатися на значення `value`. MDN
називає таку поведінку «станом Zalgo» (state of Zalgo). Назва походить зі статті Designing APIs for Asynchrony, де цю
проблему вперше описали.

Проміс цю проблему прибирає. Коли викликати функцію з `then`, вирішує не автор функції, а сам механізм промісів, і він
щоразу діє однаково. MDN перелічує три гарантії:

| Гарантія | Що вона дає вашому коду |
|----------|-------------------------|
| Функцію з `then` ніколи не викликають одразу, навіть якщо проміс уже виконано. Її викликають лише після того, як закінчиться весь поточний код | Код, що стоїть після виклику `then`, завжди виконується раніше за функцію з `then`. Випадку «то одразу, то пізніше» не буває |
| Функцію з `then` викликають навіть тоді, коли `then` додали вже після того, як робота завершилася | Значення не пропадає, якщо ви підписалися на проміс запізно |
| Якщо викликати `then` кілька разів, передані функції виконуються в тому порядку, у якому їх додали | Порядок можна передбачити заздалегідь |

Першу гарантію MDN показує двома рядками коду:

```js
Promise.resolve().then(() => console.log(2));
console.log(1);
```

```text
1
2
```

Функція `Promise.resolve()` створює проміс, який уже виконано. Попри це функція з `then` не виконується одразу. Вона
стає в чергу мікрозадач, про яку розповідала лекція, і чекає, поки закінчиться поточний код. Тому першим друкується
`1`, хоча рядок `console.log(1)` стоїть нижче, а `2` друкується після нього.

Другий фрагмент додає до цього таймер:

```js
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

wait(0).then(() => console.log(4));
Promise.resolve()
  .then(() => console.log(2))
  .then(() => console.log(3));
console.log(1);
```

```text
1
2
3
4
```

Функція `wait` загортає `setTimeout` у проміс, який виконується, коли спрацює таймер. Число `1` друкує поточний код.
Числа `2` і `3` друкують функції з `then`, тобто мікрозадачі, тому вони виконуються одразу після поточного коду.
Число `4` друкує функція з `then` проміса від таймера. Таймер є задачею, а задача починається лише тоді, коли черга
мікрозадач спорожніла. Тому `4` друкується останнім, хоча затримка таймера дорівнює 0.

**Підрозділ `Task queues vs. microtasks`, тобто «черги задач і мікрозадачі».** Він повторює те саме правило: функції з
`then` виконуються як мікрозадачі, а функція з `setTimeout` виконується як окрема задача. Фрагмент коду цього
підрозділу показує ще й стан проміса до того, як виконалася функція з `then`, і після цього:

```js
const promise = new Promise((resolve, reject) => {
  console.log("Promise callback");
  resolve();
}).then((result) => {
  console.log("Promise callback (.then)");
});

setTimeout(() => {
  console.log("event-loop cycle: Promise (fulfilled)", promise);
}, 0);

console.log("Promise (pending)", promise);
```

```text
Promise callback
Promise (pending) Promise { <pending> }
Promise callback (.then)
event-loop cycle: Promise (fulfilled) Promise { undefined }
```

Розберемо, що відбувається в цьому коді, по порядку. Спершу одна річ, яку легко пропустити: у коді **два** проміси, а
не один. Перший проміс створює запис `new Promise(...)`, назвемо його промісом А. Другий проміс створює виклик
`.then(...)`, бо метод `then` завжди повертає новий проміс. Назвемо його промісом Б. У змінну `promise` потрапляє саме
проміс Б, тобто результат усього виразу `new Promise(...).then(...)`. Проміс А не лежить у жодній змінній.

Тепер про слово «викликати». Проміс не викликають, бо проміс — це не функція. Це об'єкт, у якому записано одне:
результат уже готовий чи ще ні. Викликаються функції, які передали промісу. У цьому коді таких функцій дві: та, що
стоїть у дужках `new Promise(...)`, і та, що стоїть у дужках `then(...)`. Щоб зрозуміти вивід, треба знати, хто й коли
викликає кожну з них.

Функцію з дужок `new Promise(...)` конструктор викликає одразу, у ту саму мить, коли створює проміс А. Тому першим
друкується `Promise callback`. Усередині цієї функції стоїть виклик `resolve()`. Функцію `resolve` дав конструктор, і
її виклик робить проміс А виконаним. Отже, проміс А готовий уже тоді, коли виконалися перші три рядки коду.

Далі виконується `.then(...)`. Він створює проміс Б і запам'ятовує функцію, яку треба викликати, коли проміс А буде
виконано. Проміс А вже виконано, але функцію з `then` і тепер не викликають одразу. Її ставлять у чергу мікрозадач, і
там вона чекає, поки закінчиться весь поточний код файла. Проміс Б тим часом очікує, бо він стане виконаним лише тоді,
коли функція з `then` відпрацює.

Потім виконується `setTimeout`. Він нічого не друкує, а лише ставить таймер у чергу задач.

Останній рядок файла друкує змінну `promise`, тобто проміс Б. Функція з `then` ще стоїть у черзі й не виконалася, тому
проміс Б очікує, і друкується `Promise (pending) Promise { <pending> }`.

На цьому поточний код закінчився. Тепер черга мікрозадач запускає функцію з `then`. Вона друкує `Promise callback
(.then)` і закінчується. Щойно вона закінчилася, проміс Б стає виконаним. Його значенням стає те, що функція
повернула. У функції немає `return`, тому значення дорівнює `undefined`.

Останнім спрацьовує таймер, бо таймер є задачею, а задача починається лише після всіх мікрозадач. Таймер друкує змінну
`promise` ще раз. Тепер проміс Б виконано, і Node показує його як `Promise { undefined }`: у фігурних дужках стоїть
значення проміса. Браузер показує той самий стан як `Promise {<fulfilled>}`, і саме такий запис стоїть на сторінці
MDN.

Звідси відповідь на запитання, коли виконується функція з `then`. Для цього мають статися дві речі. Проміс, на якому
викликали `then`, має стати виконаним, і має закінчитися весь поточний код. У цьому прикладі перша умова виконалася
вже всередині `new Promise(...)`, а друга лише після останнього рядка файла. Тому функція з `then` друкує свій рядок
третьою, хоча в коді її записано другою.

**Підрозділ `When promises and tasks collide`, тобто «коли проміси й задачі зіштовхуються».** Він складається з двох
речень і не має коду. Сторінка каже, що коли проміси й задачі виконуються в непередбачуваному порядку, може допомогти
функція `queueMicrotask()`, і відсилає до окремого посібника про мікрозадачі. Цей підрозділ можна пропустити, бо
`queueMicrotask` уже показала лекція.

**Навіщо це в React.** Розділи про ланцюжок і помилки показують, як записати завантаження даних кількома кроками і де
ловити помилки. Розділ `Timing` пояснює порядок виконання коду, і в React цей порядок трапиться вам постійно. Якщо
функція записує дані в стан після `await`, цей запис станеться пізніше, ніж код, що стоїть після виклику цієї
функції. Причина та сама, що в прикладах вище: усе, що стоїть після `await`, виконується мікрозадачею, тобто лише
після поточного коду.

## async function (MDN)

**Де читати:** [async
function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function).

**Що це за текст.** Це довідкова сторінка, тому спершу йде формальний запис, а суть починається в `Description`.

**Якщо часу мало,** прочитайте `Description` і підрозділ `await and concurrency`.

### Syntax

Запис має вигляд `async function name(param0) { statements }`. Між словами `async` і `function` не можна переносити
рядок. Якщо перенести, мова сама вставить після `async` крапку з комою. Тоді `async` стане окремим іменем, а далі
буде звичайна функція.

### Description

Цей розділ варто прочитати уважно. Він містить п'ять думок:

| Що написано | Що це означає |
|-------------|---------------|
| Виклик завжди повертає проміс | Значення з `return` стає значенням проміса, а виняток робить його відхиленим |
| `return 1` приблизно дорівнює `Promise.resolve(1)`, але не повністю | `async`-функція завжди дає новий проміс, навіть якщо ви повертаєте вже готовий |
| Код до першого `await` виконується синхронно | Функція без `await` виконується вся одразу, хоч і повертає проміс |
| Код після кожного `await` можна вважати функцією, переданою в `then` | Після `await` код виконується окремою мікрозадачею |
| `await` дозволяє звичайний `try…catch` | Приклад із запасним завантаженням у розділі `Rewriting a Promise chain with an async function` показує це |

Другу думку сторінка показує прикладом. Проміс `p` створено заздалегідь, і дві функції повертають його по-різному:

```js
const p = new Promise((res, rej) => {
  res(1);
});

async function asyncReturn() {
  return p;
}

function basicReturn() {
  return Promise.resolve(p);
}

console.log(p === basicReturn()); // true
console.log(p === asyncReturn()); // false
```

```text
true
false
```

Як пояснювала лекція дня 1, оператор `===` для об'єктів перевіряє, чи це той самий об'єкт. Якщо `Promise.resolve`
отримує проміс, він повертає той самий проміс, тому перше порівняння дає `true`. Функція `asyncReturn` позначена
словом `async`, тому її виклик завжди створює новий проміс, навіть коли вона повертає готовий проміс `p`. Тому друге
порівняння дає `false`.

**Застереження про масив.** Сторінка показує запис `[await p1, await p2]` і прямо каже його не використовувати:

```js
async function foo() {
  const p1 = new Promise((resolve) => setTimeout(() => resolve("1"), 1000));
  const p2 = new Promise((_, reject) =>
    setTimeout(() => reject(new Error("failed")), 500),
  );
  const results = [await p1, await p2]; // Do not do this! Use Promise.all or Promise.allSettled instead.
}
foo().catch(() => {}); // Attempt to swallow all errors...
```

```text
Error: failed

Node.js v24.22.0
```

Це вивід Node 24, з якого ми прибрали рядки зі шляхом до файла й переліком викликів. Проміс `p1` виконається через
1000 мс, а проміс `p2` відхилиться через 500 мс. Вираз `[await p1, await p2]` спершу чекає на `p1`. Поки код чекає
`p1`, ніхто не поставив обробника на `p2`. Тому через 500 мс відхилення `p2` стає необробленим, хоча зовні стоїть
`catch`, який мав би перехопити всі помилки. Node надрукував помилку через пів секунди після запуску й завершив процес
із кодом 1, так і не дочекавшись `p1`. Лекція пояснює, чому Node у такому разі завершує процес.

**Паралельність.** Робота починається в ту мить, коли викликають функцію, що її запускає, а не тоді, коли до неї
доходить `await`. Сам `await` нічого не запускає, він лише чекає на вже запущену роботу. Тому, щоб дві роботи йшли
одночасно, треба спершу створити обидва проміси й лише потім чекати на них. Щоб дочекатися кількох робіт, сторінка
радить `Promise.all` або `Promise.allSettled`. Приклад нижче показує це на таймерах.

### Async functions and execution order

Приклад використовує дві допоміжні функції. Функція `resolveAfter2Seconds` повертає проміс, який виконується через
2 секунди значенням `"slow"`, тобто «повільний». Функція `resolveAfter1Second` повертає проміс, який виконується через
1 секунду значенням `"fast"`, тобто «швидкий». Обидві друкують рядок, коли починають, і рядок, коли таймер спрацював.
Далі йдуть чотири варіанти:

| Функція | Що вона робить | Час |
|---------|----------------|-----|
| `sequentialStart` | запускає повільну, чекає, потім запускає швидку | близько 3 с |
| `sequentialWait` | запускає обидві, потім чекає їх по черзі | близько 2 с, але швидка друкується після повільної |
| `concurrent1` | `await Promise.all([...])` | близько 2 с, помилки перехоплюються |
| `concurrent2` | кожна функція всередині `Promise.all` сама друкує результат | швидка друкується через 1 с, повільна через 2 с |

Ось увесь код прикладу. Останні рядки запускають чотири варіанти по черзі, з паузами, щоб вони не змішувалися:

```js
function resolveAfter2Seconds() {
  console.log("starting slow promise");
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve("slow");
      console.log("slow promise is done");
    }, 2000);
  });
}

function resolveAfter1Second() {
  console.log("starting fast promise");
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve("fast");
      console.log("fast promise is done");
    }, 1000);
  });
}

async function sequentialStart() {
  console.log("== sequentialStart starts ==");

  // 1. Start a timer, log after it's done
  const slow = resolveAfter2Seconds();
  console.log(await slow);

  // 2. Start the next timer after waiting for the previous one
  const fast = resolveAfter1Second();
  console.log(await fast);

  console.log("== sequentialStart done ==");
}

async function sequentialWait() {
  console.log("== sequentialWait starts ==");

  // 1. Start two timers without waiting for each other
  const slow = resolveAfter2Seconds();
  const fast = resolveAfter1Second();

  // 2. Wait for the slow timer to complete, and then log the result
  console.log(await slow);
  // 3. Wait for the fast timer to complete, and then log the result
  console.log(await fast);

  console.log("== sequentialWait done ==");
}

async function concurrent1() {
  console.log("== concurrent1 starts ==");

  // 1. Start two timers concurrently and wait for both to complete
  const results = await Promise.all([
    resolveAfter2Seconds(),
    resolveAfter1Second(),
  ]);
  // 2. Log the results together
  console.log(results[0]);
  console.log(results[1]);

  console.log("== concurrent1 done ==");
}

async function concurrent2() {
  console.log("== concurrent2 starts ==");

  // 1. Start two timers concurrently, log immediately after each one is done
  await Promise.all([
    (async () => console.log(await resolveAfter2Seconds()))(),
    (async () => console.log(await resolveAfter1Second()))(),
  ]);
  console.log("== concurrent2 done ==");
}

sequentialStart(); // after 2 seconds, logs "slow", then after 1 more second, "fast"

// wait above to finish
setTimeout(sequentialWait, 4000); // after 2 seconds, logs "slow" and then "fast"

// wait again
setTimeout(concurrent1, 7000); // same as sequentialWait

// wait again
setTimeout(concurrent2, 10000); // after 1 second, logs "fast", then after 1 more second, "slow"
```

Ми запустили цей код у Node 24 без змін. Ліворуч від кожного рядка виводу ми дописали, на якій секунді від запуску
він з'явився:

```text
 0 с  == sequentialStart starts ==
 0 с  starting slow promise
 2 с  slow promise is done
 2 с  slow
 2 с  starting fast promise
 3 с  fast promise is done
 3 с  fast
 3 с  == sequentialStart done ==
 4 с  == sequentialWait starts ==
 4 с  starting slow promise
 4 с  starting fast promise
 5 с  fast promise is done
 6 с  slow promise is done
 6 с  slow
 6 с  fast
 6 с  == sequentialWait done ==
 7 с  == concurrent1 starts ==
 7 с  starting slow promise
 7 с  starting fast promise
 8 с  fast promise is done
 9 с  slow promise is done
 9 с  slow
 9 с  fast
 9 с  == concurrent1 done ==
10 с  == concurrent2 starts ==
10 с  starting slow promise
10 с  starting fast promise
11 с  fast promise is done
11 с  fast
12 с  slow promise is done
12 с  slow
12 с  == concurrent2 done ==
```

Розберемо варіанти за цим виводом.

У `sequentialStart` швидкий таймер створюється лише після того, як повільний уже спрацював. Тому рядок
`starting fast promise` з'являється на 2-й секунді, а весь варіант закінчується на 3-й.

У `sequentialWait` обидва таймери створено одразу, на 4-й секунді, тому вони йдуть одночасно. Швидкий таймер спрацював
на 5-й секунді, але `fast` надруковано лише на 6-й, разом із `slow`. Причина в тому, що перший `await` чекає на
повільний проміс, і до другого `await` код доходить лише після нього. Варіант зайняв 2 секунди замість 3.

У `concurrent1` час той самий, що в `sequentialWait`: 2 секунди, і обидва результати надруковано разом на 9-й секунді.
Різниця між цими варіантами не в часі, а в помилках, і її пояснює наступний підрозділ.

У `concurrent2` кожен проміс має власну `async`-функцію, записану стрілкою. Дужки `()` після неї одразу її
викликають. Кожна така функція чекає на свій проміс і друкує його результат, щойно він прийде. Тому `fast`
надруковано на 11-й секунді, через 1 секунду після початку, а `slow` на 12-й, через 2 секунди.

**`await and concurrency`.** Цей підрозділ пояснює, чому `sequentialWait` і `concurrent1` не рівнозначні. Якщо швидкий
проміс відхиляється раніше за завершення повільного, у `sequentialWait` з'являється необроблене відхилення, навіть
якщо є `catch`. Це той самий випадок, що й у застереженні про масив вище. `Promise.all` підписується на всі проміси
одразу, тому такого не буває.

### Rewriting a Promise chain with an async function

Сторінка бере ланцюжок завантаження із **запасним варіантом**, тобто з другим джерелом даних на випадок, якщо перше
не відповіло:

```js
function getProcessedData(url) {
  return downloadData(url) // returns a promise
    .catch((e) => downloadFallbackData(url)) // returns a promise
    .then((v) => processDataInWorker(v)); // returns a promise
}
```

Функція `downloadData` завантажує дані. Якщо вона відхилилася, `catch` викликає `downloadFallbackData`, і ланцюжок
отримує запасні дані. Потім `then` передає дані в `processDataInWorker` для обробки, незалежно від того, з якого
джерела вони прийшли. Усі три функції вигадано, тому код сам по собі не запуститься.

Цей ланцюжок переписано двома способами. Перший спосіб використовує `try…catch`:

```js
async function getProcessedData(url) {
  let v;
  try {
    v = await downloadData(url);
  } catch (e) {
    v = await downloadFallbackData(url);
  }
  return processDataInWorker(v);
}
```

Другий спосіб ставить `.catch()` просто після виклику, в одному рядку з `await`:

```js
async function getProcessedData(url) {
  const v = await downloadData(url).catch((e) => downloadFallbackData(url));
  return processDataInWorker(v);
}
```

Обидва закінчуються `return` без `await`, бо значення все одно буде загорнуто в проміс. Сторінка каже, що
`return await` теж припустимий. Усередині `try` різниця є: без `await` локальний `catch` не
побачить помилки. Це показує лекція.

**Навіщо це в React.** У React функцію, яку передають у `useEffect`, не позначають словом `async`. Чому так, пояснює
лекція в розділі «Як це проявиться в React»: ця функція може повернути функцію очищення, а `async`-функція завжди
повертає проміс. Тому в документації React `async`-функцію оголошують усередині функції ефекту й одразу її викликають.

## Promise.all() (MDN)

**Де читати:**
[Promise.all()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all).

**Якщо часу мало,** прочитайте `Return value`, `Description` і `Promise.all fail-fast behavior`.

### Syntax, Parameters

Метод приймає **ітерований об'єкт** (iterable): те, що можна перебрати через `for…of`, найчастіше масив. На кожне
значення з нього метод чекає так, ніби перед значенням стоїть `await`. Тому звичайні значення, наприклад числа, теж
дозволені: метод кладе їх у результат без змін.

### Return value

Сторінка описує три випадки:

| Стан | Коли |
|------|------|
| Вже виконано | Вхід порожній |
| Асинхронно виконано | Усі вхідні проміси виконано. Значення йдуть у порядку передачі, а не завершення |
| Асинхронно відхилено | Будь-який проміс відхилено. Причина береться від першого відхилення |

Важливе слово тут **asynchronously**: навіть якщо всі вхідні значення готові, результат стане готовим не одразу.

### Description

`Promise.all` підходить, коли кілька пов'язаних робіт мають усі вдатися, перш ніж код піде далі. Метод одразу
відхиляється за першої помилки. Дві подробиці варто знати. Перша подробиця: щойно метод викликали, він ставить
обробник на кожен вхідний проміс через його `then`. Тому всі вхідні проміси вважаються обробленими, і їхні пізніші
відхилення не викликають `unhandledrejection`. Друга подробиця: відхилення `Promise.all` не скасовує інших операцій,
вони тривають далі.

### Examples

| Назва прикладу | Що він показує |
|----------------|----------------|
| `Using Promise.all()` | звичайні значення в масиві теж потрапляють у результат |
| `Destructuring the result` | `const [a, b] = await Promise.all(...)`, і попередження про перестановку елементів |
| `Asynchronicity or synchronicity of Promise.all` | відразу після виклику стан очікує, навіть якщо все готове; лише порожній масив дає готовий результат |
| `Using Promise.all() with async functions` | вибір страви й завантаження цін незалежні, тому їх запускають разом; передавати саму функцію замість виклику марно |
| `Promise.all fail-fast behavior` | один негайно відхилений проміс із п'яти відхиляє все; `.catch` на кожному вході дозволяє отримати решту |

Нижче кожен приклад наведено з кодом. Те, що можна запустити без браузера, ми запустили в Node 24.

**Приклад `Using Promise.all()`.** Перший фрагмент передає в метод готовий проміс, звичайне число й проміс, який
виконається через 100 мс:

```js
const p1 = Promise.resolve(3);
const p2 = 1337;
const p3 = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve("foo");
  }, 100);
});

Promise.all([p1, p2, p3]).then((values) => {
  console.log(values); // [3, 1337, "foo"]
});
```

```text
[ 3, 1337, 'foo' ]
```

Метод дочекався проміса з таймером і поклав у масив три значення в тому порядку, у якому вони стояли на вході. Число
`1337` не є промісом, але теж потрапило в результат без змін.

Другий фрагмент створює три виклики `Promise.all` і друкує їхні стани через таймер, тобто вже після всіх мікрозадач:

```js
// All values are non-promises, so the returned promise gets fulfilled
const p = Promise.all([1, 2, 3]);
// The only input promise is already fulfilled,
// so the returned promise gets fulfilled
const p2 = Promise.all([1, 2, 3, Promise.resolve(444)]);
// One (and the only) input promise is rejected,
// so the returned promise gets rejected
const p3 = Promise.all([1, 2, 3, Promise.reject(new Error("bad"))]);

// Using setTimeout, we can execute code after the queue is empty
setTimeout(() => {
  console.log(p);
  console.log(p2);
  console.log(p3);
});

// Logs:
// Promise { <state>: "fulfilled", <value>: Array[3] }
// Promise { <state>: "fulfilled", <value>: Array[4] }
// Promise { <state>: "rejected", <reason>: Error: bad }
```

Коментар `// Logs:` у кінці показує вивід, який наводить сторінка: перші два проміси виконано, а третій відхилено з
причиною `Error: bad`. У Node 24 цей фрагмент поводиться інакше. Проміс `p3` відхилено, і ніхто не поставив на нього
обробника, тому Node завершує процес із кодом 1 ще до того, як спрацює таймер, і жоден рядок із таймера не друкується.
Це те саме необроблене відхилення, про яке розповідала лекція.

**Приклад `Destructuring the result`.** Він показує, як одразу розкласти масив результатів по змінних:

```js
// With then()
Promise.all([p1, p2, p3]).then(([a, b, c]) => {
  console.log(a, b, c); // 3 1337 "foo"
});

// With await
const [a, b, c] = await Promise.all([p1, p2, p3]);
```

Змінні `p1`, `p2` і `p3` тут ті самі, що в першому фрагменті попереднього прикладу. Запис `[a, b, c]` бере перший
елемент масиву в змінну `a`, другий у `b`, третій у `c`. Сторінка попереджає: якщо переставити проміси на вході й
забути переставити змінні, змінна отримає не той результат, і помилку буде важко помітити.

**Приклад `Asynchronicity or synchronicity of Promise.all`.** Перший фрагмент передає в метод два вже виконані проміси
й одразу друкує результат:

```js
// Passing an array of promises that are already resolved,
// to trigger Promise.all as soon as possible
const resolvedPromisesArray = [Promise.resolve(33), Promise.resolve(44)];

const p = Promise.all(resolvedPromisesArray);
// Immediately logging the value of p
console.log(p);

// Using setTimeout, we can execute code after the queue is empty
setTimeout(() => {
  console.log("the queue is now empty");
  console.log(p);
});

// Logs, in order:
// Promise { <state>: "pending" }
// the queue is now empty
// Promise { <state>: "fulfilled", <value>: Array[2] }
```

```text
Promise { <pending> }
the queue is now empty
Promise { [ 33, 44 ] }
```

Обидва вхідні проміси готові, але одразу після виклику `Promise.all` повертає проміс, що очікує. Він стає виконаним
лише після поточного коду, і таймер бачить його вже виконаним. Node показує виконаний проміс як
`Promise { [ 33, 44 ] }`: у фігурних дужках стоїть його значення, тобто масив. Коментар MDN показує той самий
результат в іншому записі. Другий фрагмент сторінки робить те саме з одним відхиленим промісом. У Node він, як і
другий фрагмент попереднього прикладу, завершує процес через необроблене відхилення. Третій фрагмент показує єдиний
виняток:

```js
const p = Promise.all([]); // Will be immediately resolved
const p2 = Promise.all([1337, "hi"]); // Non-promise values are ignored, but the evaluation is done asynchronously
console.log(p);
console.log(p2);
setTimeout(() => {
  console.log("the queue is now empty");
  console.log(p2);
});

// Logs:
// Promise { <state>: "fulfilled", <value>: Array[0] }
// Promise { <state>: "pending" }
// the queue is now empty
// Promise { <state>: "fulfilled", <value>: Array[2] }
```

```text
Promise { [] }
Promise { <pending> }
the queue is now empty
Promise { [ 1337, 'hi' ] }
```

Порожній масив дає вже виконаний проміс зі значенням `[]`. Масив `[1337, "hi"]` не містить жодного проміса, але
результат однаково спершу очікує й стає виконаним лише після поточного коду.

**Приклад `Using Promise.all() with async functions`.** Він потребує браузера, бо показує на сторінці вікно вибору
страви, тому ми його не запускали. Функція `promptForDishChoice` повертає проміс, який виконується назвою страви, коли
користувач її вибрав. Функція `fetchPrices` завантажує ціни. Спершу MDN показує повільний варіант:

```js
async function getPrice() {
  const choice = await promptForDishChoice();
  const prices = await fetchPrices();
  return prices[choice];
}
```

Перший `await` чекає, поки користувач вибере страву, і лише після цього починається завантаження цін. Але ці дві
роботи одна від одної не залежать, тому MDN переписує функцію так:

```js
async function getPrice() {
  const [choice, prices] = await Promise.all([
    promptForDishChoice(),
    fetchPrices(),
  ]);
  return prices[choice];
}
```

Тепер обидві функції викликано одразу, і ціни завантажуються, поки користувач вибирає. Далі сторінка застерігає від
помилки, коли в масив кладуть самі функції замість їхніх викликів:

```js
async function getPrice() {
  const [choice, prices] = await Promise.all([
    promptForDishChoice,
    fetchPrices,
  ]);
  // `choice` and `prices` are still the original async functions;
  // Promise.all() does nothing to non-promises
}
```

Тут після імен функцій немає дужок, тому функції ніхто не викликає, і жодна робота не починається. Метод
`Promise.all` залишає значення, які не є промісами, без змін, тому змінні `choice` і `prices` отримують самі функції.

**Приклад `Promise.all fail-fast behavior`.** Чотири проміси виконуються через 1, 2, 3 і 4 секунди, а п'ятий
відхиляється одразу:

```js
const p1 = new Promise((resolve, reject) => {
  setTimeout(() => resolve("one"), 1000);
});
const p2 = new Promise((resolve, reject) => {
  setTimeout(() => resolve("two"), 2000);
});
const p3 = new Promise((resolve, reject) => {
  setTimeout(() => resolve("three"), 3000);
});
const p4 = new Promise((resolve, reject) => {
  setTimeout(() => resolve("four"), 4000);
});
const p5 = new Promise((resolve, reject) => {
  reject(new Error("reject"));
});

// Using .catch:
Promise.all([p1, p2, p3, p4, p5])
  .then((values) => {
    console.log(values);
  })
  .catch((error) => {
    console.error(error.message);
  });

// Logs:
// "reject"
```

```text
reject
```

Рядок `reject` з'явився одразу після запуску, бо `Promise.all` відхилився разом із п'ятим промісом і не чекав на
решту. Проте процес Node завершився лише через 4 секунди: таймери інших промісів працювали далі. Це й означає речення
сторінки, що відхилення не скасовує інших операцій. Другий фрагмент показує, як отримати всі результати попри помилку:

```js
const p1 = new Promise((resolve, reject) => {
  setTimeout(() => resolve("p1_delayed_resolution"), 1000);
});

const p2 = new Promise((resolve, reject) => {
  reject(new Error("p2_immediate_rejection"));
});

Promise.all([p1.catch((error) => error), p2.catch((error) => error)]).then(
  (values) => {
    console.log(values[0]); // "p1_delayed_resolution"
    console.error(values[1]); // "Error: p2_immediate_rejection"
  },
);
```

```text
p1_delayed_resolution
Error: p2_immediate_rejection
    at …
```

Кожен проміс тут отримав власний `catch`, який повертає помилку як звичайне значення. Тому жоден вхід не
відхиляється, і `Promise.all` через секунду виконується масивом із двох елементів: рядка від `p1` та об'єкта помилки
від `p2`. Під об'єктом помилки Node друкує перелік викликів, і ми замінили його трьома крапками.

Сторінка також згадує новий метод `Promise.allKeyed()`, який пов'язує результати за ключами. Node 24 його ще не має:
ми перевірили, і `typeof Promise.allKeyed` дає `undefined`. Використовувати його в цьому дні не треба.

**Навіщо це в React.** На цьому методі будується завантаження кількох незалежних частин сторінки одним кроком.

## Promise.allSettled() (MDN)

**Де читати:**
[Promise.allSettled()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled).
Сторінка коротка, тому читати її можна повністю.

### Syntax, Parameters, Return value

Метод приймає те саме, що й `Promise.all`. Він ніколи не відхиляється через вхідні проміси. Результатом є масив
об'єктів у порядку передачі:

| Поле | Коли є | Що містить |
|------|--------|------------|
| `status` | завжди | `"fulfilled"` або `"rejected"` |
| `value` | якщо виконано | значення |
| `reason` | якщо відхилено | причина відхилення |

Слово **settled** означає «завершений», тобто виконаний або відхилений.

### Description

Сторінка дає коротке правило вибору. `Promise.allSettled` підходить для незалежних робіт, коли потрібен результат
кожної. `Promise.all` підходить, коли роботи залежать одна від одної або коли треба одразу зупинитися за першої
помилки.

### Examples

Приклад передає виконаний проміс, проміс із таймером, звичайне значення `99` і відхилений проміс, а отримує чотири
об'єкти:

```js
Promise.allSettled([
  Promise.resolve(33),
  new Promise((resolve) => setTimeout(() => resolve(66), 0)),
  99,
  Promise.reject(new Error("an error")),
]).then((values) => console.log(values));
```

Наш запуск у Node 24 надрукував таке. Під причиною відхилення Node друкує перелік викликів, і ми замінили його трьома
крапками:

```text
[
  { status: 'fulfilled', value: 33 },
  { status: 'fulfilled', value: 66 },
  { status: 'fulfilled', value: 99 },
  {
    status: 'rejected',
    reason: Error: an error
        at …
  }
]
```

Це той самий результат, що й у коментарі на сторінці. Метод дочекався проміса з таймером, і об'єкти йдуть у тому
порядку, у якому проміси стояли на вході. Значення `99` не є промісом, тому стало об'єктом зі
`status: 'fulfilled'`. Відхилений проміс став об'єктом зі `status: 'rejected'` і причиною в полі `reason`, а сам
`Promise.allSettled` не відхилився.

Другий фрагмент сторінки показує, як розкласти результат по змінних:

```js
const [status1, status2] = Promise.allSettled([
  Promise.resolve(33),
  new Promise((resolve) => setTimeout(() => resolve(66), 0)),
]);
```

У цьому фрагменті на сторінці бракує `await` перед `Promise.allSettled`. Без нього праворуч від `=` стоїть проміс, а
не масив, і розкласти проміс по змінних неможливо. Node 24 на цьому рядку кидає виняток
`TypeError: object is not iterable`. Правильний запис такий самий, як у прикладі `Destructuring the result` сторінки
`Promise.all()`: `const [status1, status2] = await Promise.allSettled([...])`. З `await` ми запустили той самий
фрагмент у Node 24 і надрукували обидві змінні. Змінна `status1` отримала `{ status: 'fulfilled', value: 33 }`, а
змінна `status2` отримала `{ status: 'fulfilled', value: 66 }`, як і пише коментар на сторінці.

Є й згадка `Promise.allSettledKeyed()`, яка за своїм призначенням схожа на `Promise.allKeyed()`.

**Навіщо це в React.** Цей метод дає показати ті блоки сторінки, що завантажилися, а замість решти показати
повідомлення про помилку.

## HTML Standard: 8.1.7 Event loops

**Де читати:** [розділ 8.1.7 Event loops](https://html.spec.whatwg.org/multipage/webappapis.html#event-loops). Весь
розділ 8 `Web application APIs` дуже великий, а для цього дня потрібен лише він.

**Що це за текст.** Це **специфікація**: документ, за яким браузери реалізують свою поведінку. Її пишуть не для
навчання, а щоб різні браузери поводилися однаково. Тому стандарт описує поведінку алгоритмами, ніби псевдокодом.
Читати його легко, якщо знати кілька правил.

### Як читати специфікацію

| Запис | Що він означає |
|-------|----------------|
| **user agent** | браузер |
| **must** | обов'язкова вимога до браузера, а не порада |
| «Let *x* be …» | створити змінну `x` алгоритму |
| «Set *x* to …» | присвоїти змінній нове значення |
| «Perform …», «Run …» | виконати інший алгоритм, зазвичай на нього є посилання |
| «in parallel» | ці кроки йдуть окремо, поза звичайним кодом сторінки |
| «implementation-defined» | кожен браузер вирішує сам |
| **set** (множина), **queue** (черга), **struct** (структура) | види даних зі стандарту Infra: множина не має повторів, з черги беруть лише перший елемент, структура є об'єктом із полями |
| Текст у блоці Note | пояснення для читача, а не вимога |

Кожен термін у стандарті є посиланням на своє визначення. Якщо незрозуміло слово, клацніть на ньому, а не читайте все
підряд. Не намагайтеся прочитати все: для цього дня потрібні кілька абзаців першого підрозділу й перші кроки третього.

**Якщо часу мало,** прочитайте початок `8.1.7.1 Definitions`, перші кроки `8.1.7.3 Processing model` і абзац `perform
a microtask checkpoint`.

### 8.1.7.1 Definitions

Перше речення каже, навіщо все це: браузер мусить використовувати цикли подій, щоб узгоджувати події, дії користувача,
скрипти, малювання й мережу. Далі йдуть думки, яких немає в більшості статей:

| Що сказано | Що це означає |
|------------|---------------|
| Кожен **agent** має власний цикл подій | Агент — це сторінка чи кілька пов'язаних сторінок. Web Worker має окремий цикл |
| Цикл подій не обов'язково відповідає потоку | Це логічний механізм, а не вказівка, як браузер має його збудувати |
| Цикл має **одну або кілька** черг задач | Це не одна черга: браузер може мати окрему чергу для миші й клавіатури |
| Черга задач є множиною, а не чергою | Браузер бере першу задачу, готову до виконання, а не просто першу |
| Черга мікрозадач не є чергою задач | Це окрема справжня черга, і мікрозадачі беруться строго по порядку |
| Мікрозадача є розмовною назвою | Це задача, створена алгоритмом `queue a microtask` |

Перелік того, що роблять задачі, теж важливий: **Events** означає надсилання подій, **Parsing** означає розбір HTML,
**Callbacks** означає виклик функцій, **Using a resource** означає обробку завантаженого, **Reacting to DOM
manipulation** означає реакцію на зміну сторінки.

**Task source** (джерело задач) позначає, звідки прийшла задача. Задачі з одного джерела виконуються по порядку, а між
різними джерелами браузер вибирає сам. Стандарт описує приклад: браузер може віддавати перевагу клавіатурі й миші, щоб
сторінка лишалася чутливою. Отже, порядок таймера й клацання стандарт не гарантує.

### 8.1.7.2 Queuing tasks

Цей підрозділ описує, як інші частини стандарту ставлять задачу чи мікрозадачу в чергу. Важливі лише дві назви:
**queue a task** ставить задачу, а **queue a microtask** ставить мікрозадачу. Решта стосується авторів стандартів,
тому її можна пропустити.

### 8.1.7.3 Processing model

Це серце розділу. Цикл постійно проходить такі кроки:

| Що написано в кроках | Простими словами |
|----------------------|------------------|
| Вибрати чергу задач, де є готова задача, на розсуд браузера | Браузер вирішує, з якої черги брати |
| Узяти з неї першу готову задачу | Вийняти задачу |
| Виконати її кроки | Запустити її до кінця |
| **Perform a microtask checkpoint** | Виконати всі мікрозадачі |
| Записати час, повідомити про довгі задачі | Тут працюють інструменти вимірювання швидкодії |
| Якщо задач немає, почати період простою | Тут запускаються функції `requestIdleCallback` |

Функцію `requestIdleCallback` дає браузер. Вона приймає вашу функцію й просить браузер викликати її в період простою,
тобто тоді, коли браузерові немає чого робити. Так можна виконати другорядну роботу й не затримати анімацію чи
відповідь на дії користувача.

**Де тут малювання.** Багато старих статей показують «оновити екран» як крок цього самого списку. У чинному тексті
стандарту це інакше. Окремий абзац нижче каже: цикл вікна паралельно чекає на **можливість малювання** (rendering
opportunity) і тоді ставить звичайну задачу з джерела `rendering task source`, яка оновлює сторінку. Висновок для вас
той самий: малювання не втрутиться посеред задачі чи між нею й мікрозадачами. Можливість малювання залежить від
екрана: стандарт наводить приклад 60 разів на секунду, тобто близько 16,7 мс.

Далі йде довгий перелік кроків оновлення сторінки. Ось порядок частин, які ви зустрінете в React і в браузері: події
зміни розміру й прокрутки, анімації, функції `requestAnimationFrame`, обчислення стилів і розташування елементів,
функції `ResizeObserver`, перевірка фокуса, `IntersectionObserver` і саме малювання. Запам'ятовувати весь перелік не
треба. Досить знати, що `requestAnimationFrame` виконується перед обчисленням стилів.

**Абзац `perform a microtask checkpoint`.** Назву можна перекласти як «контрольна точка мікрозадач»: це місце, де
браузер виконує всі мікрозадачі, що накопичилися. Алгоритм складається з кількох кроків. Перший крок перевіряє
прапорець `performing a microtask checkpoint`. Якщо прапорець уже стоїть, тобто алгоритм уже виконується, браузер
одразу виходить. Стандарт пояснює, навіщо це: мікрозадача сама виконує код, а після коду браузер знову викликає цей
алгоритм, і без прапорця він запустився б усередині самого себе. Далі браузер ставить прапорець і повторює, поки
черга мікрозадач не порожня: виймає найстарішу мікрозадачу й виконує її. Якщо мікрозадача поставила нову
мікрозадачу, черга знову не порожня, тому нова мікрозадача виконається в цьому самому проході. Після циклу стандарт
повідомляє про відхилені проміси, і саме звідси береться подія `unhandledrejection`. Наприкінці браузер знімає
прапорець.

**Ще одне місце, де виконуються мікрозадачі.** Той самий алгоритм викликається з кроку [clean up after running
script](https://html.spec.whatwg.org/multipage/webappapis.html#clean-up-after-running-script): якщо стек виконання
(перелік функцій, які зараз працюють) порожній, виконати мікрозадачі. Звідси випливає наслідок, який можна побачити в
браузері. Якщо кнопка має два слухачі подій, а перший ставить мікрозадачу, то під час справжнього клацання мишею
мікрозадача виконається між двома слухачами, бо між ними стек порожній. Якщо ж викликати `button.click()` у коді, стек
не порожній, тому мікрозадача виконається пізніше. У Node ми відтворили другий випадок. Метод `dispatchEvent`
запускає подію з коду, як і `button.click()`. Він викликає всіх слухачів цієї події синхронно, тобто одразу й по
черзі, ще до того, як сам закінчиться. Код такий:

```js
const button = new EventTarget();
button.addEventListener("click", () => {
  console.log("слухач 1");
  queueMicrotask(() => console.log("мікрозадача зі слухача 1"));
});
button.addEventListener("click", () => {
  console.log("слухач 2");
});

button.dispatchEvent(new Event("click"));
console.log("після dispatchEvent");
```

```text
слухач 1
слухач 2
після dispatchEvent
мікрозадача зі слухача 1
```

Об'єкт `EventTarget` уміє приймати слухачів і запускати події, тому тут він замінює кнопку. Перший слухач ставить
мікрозадачу, але вона не виконується між слухачами. Причина в тому, що обидва слухачі викликано зсередини
`dispatchEvent`, а `dispatchEvent` викликано з коду файла, тому стек виконання весь час не порожній. Мікрозадача
виконалася лише після останнього рядка файла. Випадок зі справжнім клацанням мишею можна перевірити лише в браузері,
тому його ми не запускали.

### 8.1.7.4 Generic task sources

Тут названо спільні джерела задач: **DOM manipulation** (реакція на зміни сторінки), **user interaction** (клавіатура
й миша), **networking** (мережа), **navigation and traversal** (перехід між сторінками) і **rendering** (оновлення
сторінки).

### 8.1.7.5 Dealing with the event loop from other specifications

Цей підрозділ написано для авторів інших стандартів. Вам він не потрібен.

### Поруч у стандарті

| Де | Що там |
|----|--------|
| [8.1.6.6.4 HostEnqueuePromiseJob](https://html.spec.whatwg.org/multipage/webappapis.html#hostenqueuepromisejob) | місце, де специфікація мови віддає проміси в чергу мікрозадач |
| [8.7 Timers](https://html.spec.whatwg.org/multipage/timers-and-user-prompts.html#timers) | як працює `setTimeout`, зокрема мінімум 4 мс для вкладених таймерів |
| [8.8 Microtask queuing](https://html.spec.whatwg.org/multipage/timers-and-user-prompts.html#microtask-queuing) | функція `queueMicrotask` |

**Node.** Цей стандарт описує браузери. Node має власний цикл подій у бібліотеці libuv. У прикладах лекції порядок той
самий, але в Node є ще власна функція `process.nextTick`, якої немає в браузері.

**Навіщо це в React.** Розуміння циклу пояснює, чому довгий код заморожує екран і чому код після `await` виконується
окремою мікрозадачею. Сам React планує свою роботу поверх цього циклу.

## How to Design Programs, розділ 3.1

**Де читати:** [`3.1 Designing
Functions`](https://htdp.org/2024-11-6/Book/part_one.html#%28part._sec~3adesign-func%29) книжки How to Design
Programs. Текст книжки не можна поширювати, тому тут є лише короткий переказ. Сам рецепт пояснено в [розборі дня
4](f0-d04-reading.md), а тут є лише те нове, що додають проміси.

### Рецепт для функції, що повертає проміс

У книжці немає промісів, бо її мова для новачків проста. Завдання дня застосовує той самий рецепт до асинхронної
функції, і кожен крок трохи змінюється:

| Крок книжки | Що змінюється для проміса |
|-------------|---------------------------|
| Опис даних | Описуєте значення, яке прийде, а не сам проміс |
| Сигнатура | Праворуч від стрілки стоїть `Promise<тип>`, тобто проміс, у якому буде значення цього типу |
| Заглушка | Потрібен готовий проміс: `Promise.resolve(значення)`. В `async`-функції досить `return значення` |
| Приклади | Тест сам стає `async`, а перед викликом стоїть `await` |
| Тіло | Використовує `await` чи `then` |
| Перевірка | Час не точний, тому очікування щодо часу записують проміжком |

Приклад на іншому об'єкті:

```js
// string -> Promise<number>
// Проміс, який через 20 мс виконується курсом валюти code.
export function rateOf(code) {
  return Promise.resolve(0);
}
```

Тест записано так: `assert.strictEqual(await rateOf("USD"), 41.5)`. Функція `assert.strictEqual` з модуля
`node:assert` порівнює два значення й кидає виняток, якщо вони різні. Ми поставили тест після заглушки в одному файлі
й запустили його в Node 24:

```js
import assert from "node:assert";

// string -> Promise<number>
// Проміс, який через 20 мс виконується курсом валюти code.
export function rateOf(code) {
  return Promise.resolve(0);
}

assert.strictEqual(await rateOf("USD"), 41.5);
```

```text
AssertionError [ERR_ASSERTION]: Expected values to be strictly equal:

0 !== 41.5

    at … {
  generatedMessage: true,
  code: 'ERR_ASSERTION',
  actual: 0,
  expected: 41.5,
  operator: 'strictEqual',
  diff: 'simple'
}
```

Це вивід Node 24 без перших рядків, які показують внутрішнє місце Node, звідки кинуто виняток. Шлях до файла й перелік
викликів ми замінили трьома крапками. Заглушка повертає 0, тому тест падає з `actual: 0` і `expected: 41.5`, і це
правильно: тіла функції ще немає. Без `await` тест порівнював би число із самим промісом і падав би завжди, навіть зі
справжнім тілом. Ми перевірили й це: написали справжнє тіло, яке через 20 мс виконує проміс числом 41.5, і прибрали
`await` із тесту:

```js
import assert from "node:assert";

// Справжнє тіло: через 20 мс проміс виконується числом 41.5.
export function rateOf(code) {
  return new Promise((resolve) => setTimeout(() => resolve(41.5), 20));
}

assert.strictEqual(rateOf("USD"), 41.5);
```

```text
AssertionError [ERR_ASSERTION]: Expected values to be strictly equal:
+ actual - expected

+ Promise {
+   <pending>
+ }
- 41.5
```

Ми навели лише початок повідомлення про помилку. Рядки з плюсом показують фактичне значення, а рядок із мінусом
показує очікуване. Фактичним значенням став проміс, що очікує, а не число. Тест порівняв проміс із числом і впав,
хоча функція працює правильно.

**Навіщо це в React.** Функції, що завантажують дані, становлять окремий шар проєкту. Їхня сигнатура каже компонентам,
що саме вони отримають після очікування.

## Запитання до читання

**1. MDN називає три гарантії промісів. Яка з них пояснює, чому `then` на вже виконаному промісі все одно спрацьовує
пізніше?**

<details><summary>Відповідь</summary>

Перша: функцію з `then` ніколи не викликають раніше, ніж закінчиться поточний прохід циклу подій. Навіть готовий
проміс не викликає її синхронно.

</details>

**2. Чому MDN забороняє запис `[await p1, await p2]`, хоча обидва проміси вже створені?**

<details><summary>Відповідь</summary>

Поки код чекає на `p1`, на `p2` ніхто не підписаний. Якщо `p2` відхилиться раніше, це відхилення вважатиметься
необробленим, навіть якщо зовні є `catch`. `Promise.all` підписується на всі проміси одразу.

</details>

**3. Що станеться з `Promise.all([])` і чим відрізняється `Promise.all([1, 2])`?**

<details><summary>Відповідь</summary>

Порожній масив дає вже виконаний проміс. Масив `[1, 2]` дає проміс, який виконується асинхронно, хоч у вході немає
нічого незавершеного. Одразу після виклику його стан є очікуванням.

</details>

**4. Який об'єкт отримаєте від `Promise.allSettled` за відхилений проміс і за звичайне значення 99?**

<details><summary>Відповідь</summary>

`{ status: "rejected", reason: … }` і `{ status: "fulfilled", value: 99 }`.

</details>

**5. Стандарт HTML пише, що черга задач є множиною. Що це дає браузеру?**

<details><summary>Відповідь</summary>

Браузер бере першу задачу, готову до виконання, а не просто першу в черзі. Він також сам вибирає, з якої черги брати,
і може надати перевагу клавіатурі й миші. Порядок усередині одного джерела задач зберігається.

</details>

**6. Де за стандартом стоїть малювання сторінки відносно мікрозадач?**

<details><summary>Відповідь</summary>

Оновлення сторінки є окремою задачею з джерела `rendering task source`. Тому воно не втрутиться посеред задачі, а всі
мікрозадачі виконуються до наступної задачі. Якщо мікрозадачі весь час створюють нові, малювання не настане.

</details>

**7. Як змінюється заглушка функції, що повертає проміс?**

<details><summary>Відповідь</summary>

Вона повертає готовий проміс потрібного типу: `Promise.resolve(0)`. В `async`-функції досить написати `return 0`, бо
функція сама загорне значення в проміс.

</details>

---

Цей розбір написано для плану. Він своїми словами переказує сторінки MDN `Using promises`, `async function`,
`Promise.all()` і `Promise.allSettled()`, розділ 8.1.7 стандарту HTML і розділ 3.1 книжки How to Design Programs
(Felleisen, Findler, Flatt, Krishnamurthi). Права на оригінальні тексти належать їхнім авторам.
