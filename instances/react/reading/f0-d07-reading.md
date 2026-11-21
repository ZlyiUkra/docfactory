# Розбір читання. День 7. DOM і події

Цей файл пояснює, що написано в матеріалах дня. Лекція розповідає про саму тему, а розбір допомагає читати чужі
тексти: він показує, де що шукати, що означають незнайомі слова й навіщо це в React.

Оригінали написано англійською. Розбір не перекладає їх дослівно, а переказує своїми словами. Радимо такий порядок:

1. лекція цього дня;
2. стаття MDN `Introduction to events` (25 хвилин);
3. стаття MDN `Event bubbling` (25 хвилин);
4. сторінка MDN `Event: preventDefault() method` (5 хвилин);
5. стандарт DOM, розділ `2 Events` (40 хвилин, вибірково);
6. розділ книжки How to Design Programs, якщо ви ще не перечитували його після дня 6 (15 хвилин).

**Як ми запускали приклади.** Код прикладів MDN наведено так, як він стоїть на сторінці. Більшість прикладів реагує
на клацання мишею чи натискання клавіш, тому Node тут не допоможе: у ньому немає сторінки. Ми відкривали кожен
приклад як окрему сторінку в браузері Chrome 157, запущеному без вікна. Такий браузер працює як звичайний, тільки
нічого не показує на екрані, а керує ним програма. Ця програма надсилала браузеру ті самі сигнали, які надсилає
справжня миша чи клавіатура, тому браузер обробляв їх як дії людини. Щоб побачити результат, ми часто дописували в
приклад рядок із `console.log`. Такі рядки позначено коментарем «Дописано», а вивід скопійовано з консолі.
Ви можете повторити кожен приклад на живій сторінці MDN або у власному файлі HTML і клацати самі.

## Стаття `Introduction to events`

**Де читати:** [MDN, англійська
версія](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Events). Сервер плану:
`mdn-docs`.

**Що це за текст.** Це урок із навчального курсу MDN для початківців. Він написаний простіше за довідкові сторінки й
містить живі приклади прямо на сторінці.

**Якщо часу мало,** прочитайте `Using addEventListener()`, `Event objects` і `Preventing default behavior`.

### `What is an event?`

Подією стаття називає сигнал про те, що щось сталося: людина клацнула, натиснула клавішу, сторінка завантажилась.
Щоб код міг на це відповісти, до елемента додають функцію, яку браузер викличе, коли подія станеться. Стаття вживає
для цього два слова, `event listener` і `event handler`, майже як синоніми. Точніша різниця така: `listener` слухає
подію, а `handler` є функцією, яка виконується. У плані обидва слова перекладено як «обробник».

### `An example: handling a click event`

Приклад змінює колір тла всієї сторінки при клацанні по кнопці. Ось його код, а останній рядок ми дописали, щоб
надрукувати колір, який поставив обробник:

```html
<button>Change color</button>
```

```js
const btn = document.querySelector("button");

function random(number) {
  return Math.floor(Math.random() * (number + 1));
}

btn.addEventListener("click", () => {
  const rndCol = `rgb(${random(255)} ${random(255)} ${random(255)})`;
  document.body.style.backgroundColor = rndCol;
});

// Дописано для перевірки: другий обробник друкує колір, який поставив перший.
btn.addEventListener("click", () => console.log("тло сторінки:", document.body.style.backgroundColor));
```

Ми двічі клацнули мишею по кнопці:

```text
тло сторінки: rgb(58, 154, 75)
тло сторінки: rgb(90, 189, 97)
```

Кольори випадкові, тому у вас числа будуть інші. Розберемо, що тут сталося:

- Під час завантаження сторінки код нічого не фарбує. Він лише передає браузеру функцію-стрілку, і браузер
  зберігає її у списку обробників кнопки. Функцію викликає сам браузер, і то лише тоді, коли станеться клацання.
- Кожне клацання викликало обидва обробники в тому порядку, у якому їх додали. Тому другий обробник уже бачить
  колір, який поставив перший.
- Код записав колір із пробілами, `rgb(58 154 75)`, а прочитався він із комами. Браузер не зберігає рядок, який ви
  дали, а розбирає його й зберігає колір у власному записі. Читаючи властивість, ви отримуєте вже цей запис.

### `Using addEventListener()`

Метод отримує два аргументи: назву події та функцію. Стаття показує, що функцію можна написати прямо в дужках, як
вище, а можна оголосити окремо з іменем і передати ім'я:

```js
const btn = document.querySelector("button");

function random(number) {
  return Math.floor(Math.random() * (number + 1));
}

function changeBackground() {
  const rndCol = `rgb(${random(255)} ${random(255)} ${random(255)})`;
  document.body.style.backgroundColor = rndCol;
}

btn.addEventListener("click", changeBackground);
```

Після `changeBackground` немає дужок, і це важливо. Ім'я без дужок є самою функцією, тобто значенням, яке можна
передати далі. Ім'я з дужками викликає функцію негайно, і далі передається вже результат виклику. Ось що буде, якщо
помилитися:

```js
const btn = document.querySelector("button");
function changeBackground() {
  console.log("changeBackground викликано");
}

console.log("реєструємо:");
btn.addEventListener("click", changeBackground());   // помилка: дужки викликають функцію одразу
console.log("клацаємо:");
btn.click();
console.log("кінець");
```

```text
реєструємо:
changeBackground викликано
клацаємо:
кінець
```

Функція спрацювала один раз, ще під час реєстрації, а на клацання вже не відповіла. Вона нічого не повертає, тому в
`addEventListener` потрапило `undefined`. Браузер мовчки пропустив такий виклик і не додав жодного обробника. Помилки
в консолі теж немає, тому цю пастку легко не помітити.

Далі в розділі є три підрозділи.

**`Listening for other events`.** Стаття пропонує замінити `click` іншою назвою й подивитися, що зміниться. Подія
`focus` настає, коли кнопка отримує фокус, тобто стає тим елементом, куди йде введення з клавіатури. Подія `blur`
настає, коли кнопка фокус втрачає. Подія `dblclick` означає подвійне клацання, а `mouseover` і `mouseout` означають,
що вказівник миші зайшов на кнопку чи зійшов із неї. Деякі події є майже в усіх елементів, як `click`. Інші бувають
лише в певних, наприклад подія `play` є в `<video>`, бо лише відео можна запустити.

**`Removing listeners`.** Метод `removeEventListener` прибирає обробник. Стаття показує рядок
`btn.removeEventListener("click", changeBackground);`. Методу треба дати ту саму назву події й ту саму функцію, яку
передавали в `addEventListener`. Перевіримо це на коді статті, до якого ми дописали два обробники:

```js
// Код статті з changeBackground, як вище, а далі дописано для перевірки:
// після першого клацання прибираємо changeBackground.
btn.addEventListener("click", () => {
  console.log("тло сторінки:", document.body.style.backgroundColor);
  btn.removeEventListener("click", changeBackground);
});

// Дописано: спроба прибрати анонімну функцію.
btn.addEventListener("click", () => console.log("анонімний обробник працює"));
btn.removeEventListener("click", () => console.log("анонімний обробник працює"));
```

Ми двічі клацнули мишею по кнопці:

```text
тло сторінки: rgb(104, 71, 128)
анонімний обробник працює
тло сторінки: rgb(104, 71, 128)
анонімний обробник працює
```

Перша пара рядків показує звичайне клацання: `changeBackground` поставив колір, а потім обробник надрукував його й
прибрав `changeBackground`. Друга пара показує той самий колір, тобто друге клацання вже нічого не перефарбувало.
Рядок `анонімний обробник працює` надруковано обидва рази, хоч ми й намагалися цей обробник прибрати. Друга стрілка
лише виглядає так само, а насправді є новим об'єктом функції. Браузер шукав у списку саме цей новий об'єкт, не
знайшов і нічого не прибрав. Отже, обробник, який колись доведеться прибрати, зберігають у змінну. Ще один спосіб
прибрати обробник, через параметр `signal`, показано в лекції, у розділі «Що таке подія і як її слухати».

**`Adding multiple listeners for a single event`.** Кілька викликів `addEventListener` із різними функціями додають
кілька обробників, і спрацюють усі. Стаття показує це двома рядками. Ми визначили функції й поставили ці рядки на
кнопку з написом `addEventListener`:

```js
const functionA = () => console.log("  спрацювала functionA");
const functionB = () => console.log("  спрацювала functionB");

const myElement = document.querySelector("#a");
myElement.addEventListener("click", functionA);
myElement.addEventListener("click", functionB);
```

Після клацання мишею по кнопці надруковано обидва рядки:

```text
  спрацювала functionA
  спрацювала functionB
```

### `Other event listener mechanisms`

Цей розділ показує два старіші способи, щоб ви могли їх упізнати в чужому коді.

**`Event handler properties`.** У елемента є поля, назва яких складається з `on` і назви події, наприклад `onclick`.
Таке поле називають властивістю-обробником. Функцію просто присвоюють цьому полю: `btn.onclick = bgChange;`. Головна
вада цього способу в тому, що поле може містити лише одну функцію. Стаття показує це двома рядками. Ми поставили їх
на другу кнопку з тими самими функціями, що й вище:

```js
const element = document.querySelector("#b");
element.onclick = functionA;
element.onclick = functionB;
```

Після клацання мишею по цій кнопці надруковано лише один рядок:

```text
  спрацювала functionB
```

Друге присвоєння замінило перше, так само як друге присвоєння будь-якій змінній замінює її попереднє значення.
`addEventListener` працює інакше: він дописує функцію до списку, тому на першій кнопці спрацювали обидві.

**`Inline event handlers`.** Найстаріший спосіб пише код прямо в атрибуті тегу:

```html
<button onclick="bgChange()">Press me</button>
```

Стаття радить ніколи так не робити й наводить три причини. Перша: розмітка й код перемішуються, і їх важче читати.
Друга: якщо кнопок сто, то атрибут доведеться писати сто разів, а цикл з `addEventListener` робить те саме кількома
рядками. Третя причина найменш очевидна: сервер часто забороняє такі скрипти з міркувань безпеки.

Механізм таких заборон називають **політикою безпеки вмісту** (Content Security Policy, скорочено CSP). Сервер разом
зі сторінкою надсилає браузеру правило, звідки на ній дозволено запускати код. Наприклад, правило `script-src 'self'`
дозволяє лише скрипти з окремих файлів того самого сайту, а код, записаний прямо в HTML, забороняє. Тоді зловмисник,
якому вдалося вписати в сторінку чужий HTML, не зможе виконати в ньому свій код. Щоб показати, як це працює, ми
записали таке правило тегом `<meta>` прямо в сторінці. Сервер зазвичай передає його заголовком
`Content-Security-Policy`, а результат той самий:

```html
<meta http-equiv="Content-Security-Policy" content="script-src 'self'">
<button onclick="console.log('вбудований обробник спрацював')">Press me</button>
```

Без рядка `<meta>` клацання мишею надрукувало `вбудований обробник спрацював`. З ним рядка немає, а браузер записав у
консоль помилку:

```text
Executing inline event handler violates the following Content Security Policy directive 'script-src 'self''. Either the 'unsafe-inline' keyword, a hash ('sha256-...'), or a nonce ('nonce-...') is required to enable inline execution. Note that hashes do not apply to event handlers, style attributes and javascript: navigations unless the 'unsafe-hashes' keyword is present. The action has been blocked.
```

Повідомлення каже: вбудований обробник порушує правило `script-src 'self'`, тому браузер його не виконав. Обробник,
доданий через `addEventListener` зі скрипту в окремому файлі, таке правило пропускає.

**Не сплутайте з React:** запис `onClick={...}` у React виглядає схоже, але працює зовсім інакше. Там передається
функція, а не рядок із кодом, і React обробляє її делегуванням через корінь застосунку. Як саме, пояснено в лекції,
у розділі «Як це проявиться в React».

### `Event objects`

Браузер передає в обробник **об'єкт події**, тобто об'єкт із подробицями про те, що сталося. Параметр для нього часто
називають `e`, `evt` або `event`, але назва не має значення. Стаття переписує приклад із кольором так, щоб фарбувати
не сторінку, а сам елемент, по якому клацнули. Останній обробник ми дописали:

```js
const btn = document.querySelector("button");

function random(number) {
  return Math.floor(Math.random() * (number + 1));
}

function bgChange(e) {
  const rndCol = `rgb(${random(255)} ${random(255)} ${random(255)})`;
  e.target.style.backgroundColor = rndCol;
  console.log(e);
}

btn.addEventListener("click", bgChange);

// Дописано для перевірки.
btn.addEventListener("click", (e) => {
  console.log("тло кнопки:", btn.style.backgroundColor, "| тло сторінки:", JSON.stringify(document.body.style.backgroundColor));
});
```

Після клацання мишею по кнопці:

```text
PointerEvent
тло кнопки: rgb(204, 249, 152) | тло сторінки: ""
```

Перший рядок надрукував `console.log(e)` зі статті. Програма, що керувала браузером, записала лише назву типу об'єкта,
а в консолі інструментів розробника ви побачите цей самий об'єкт, який можна розгорнути й переглянути всі поля. Тип
називається `PointerEvent`, а не `MouseEvent`, як можна було б чекати. Довідка MDN про подію `click` пояснює, що
сучасні браузери створюють для клацання `PointerEvent`, а він є різновидом `MouseEvent` і має всі його поля. Другий
рядок показує, що кольором зафарбовано кнопку, а тло сторінки лишилося порожнім. Поле `target` вказує на елемент, де
сталася подія. Тому той самий `bgChange` можна поставити на багато елементів, і кожен фарбуватиме саме себе.

**`Extra properties of event objects`.** Кожен тип події має свої додаткові поля. Подія `keydown` настає, коли людина
натискає клавішу, і її об'єкт має тип `KeyboardEvent` з полем `key`. Поле `key` містить назву натиснутої клавіші.
Код статті, до якого ми дописали один обробник:

```html
<input id="textBox" type="text" />
<div id="output"></div>
```

```js
const textBox = document.querySelector("#textBox");
const output = document.querySelector("#output");
textBox.addEventListener("keydown", (event) => {
  output.textContent = `You pressed "${event.key}".`;
});

// Дописано для перевірки.
textBox.addEventListener("keydown", (event) => console.log(event.constructor.name, "|", output.textContent));
```

Ми клацнули мишею в поле й натиснули клавіші `a`, Shift і Enter:

```text
KeyboardEvent | You pressed "a".
KeyboardEvent | You pressed "Shift".
KeyboardEvent | You pressed "Enter".
```

Для клавіші з літерою поле `key` містить саму літеру. Для службових клавіш воно містить їхню назву англійською.

### `Preventing default behavior`

Багато подій мають **дію браузера**, тобто те, що браузер робить сам, коли подія сталася. Для форми це надсилання
даних. Стаття показує форму з двома полями для імені й прізвища. Якщо хоч одне поле порожнє, обробник події `submit`
викликає `e.preventDefault()`, тобто просить браузер не надсилати форму, і пише повідомлення в абзац під формою.
Код статті, до якого ми дописали один обробник:

```html
<form action="#">
  <div>
    <label for="fname">First name: </label>
    <input id="fname" type="text" />
  </div>
  <div>
    <label for="lname">Last name: </label>
    <input id="lname" type="text" />
  </div>
  <div>
    <input id="submit" type="submit" />
  </div>
</form>
<p></p>
```

```js
const form = document.querySelector("form");
const fname = document.getElementById("fname");
const lname = document.getElementById("lname");
const para = document.querySelector("p");

form.addEventListener("submit", (e) => {
  if (fname.value === "" || lname.value === "") {
    e.preventDefault();
    para.textContent = "You need to fill in both names!";
  }
});

// Дописано для перевірки.
form.addEventListener("submit", (e) => {
  console.log("submit | defaultPrevented:", e.defaultPrevented, "| абзац:", JSON.stringify(para.textContent));
});
```

Спершу ми клацнули по кнопці надсилання з порожніми полями. Потім надрукували літеру лише в першому полі й натиснули
Enter:

```text
submit | defaultPrevented: true | абзац: "You need to fill in both names!"
submit | defaultPrevented: true | абзац: "You need to fill in both names!"
```

Обидва рази подія `submit` настала, обробник скасував надсилання, а сторінка лишилася на тій самій адресі. Поле
`defaultPrevented` каже, чи хтось уже скасував дію браузера. Тоді ми заповнили обидва поля й клацнули по кнопці.
Обробник надрукував `submit | defaultPrevented: false | абзац: ""`, і браузер надіслав форму: адреса сторінки
закінчилася на `?#`, а сторінка завантажилася наново, тому поля знову стали порожніми.

Автори наголошують, що така перевірка лише базова, бо вона пропускає, наприклад, ім'я з самих пробілів. Дані все одно
перевіряють ще й на сервері, бо будь-хто може надіслати запит в обхід вашої сторінки.

**Чому подію слухають на формі, а не на кнопці.** Може здатися, що причина в клавіші Enter: кнопку не натискали, а
форма надіслалась. Насправді все трохи інакше. Стандарт HTML каже: якщо у формі є кнопка надсилання, то Enter у полі
змушує браузер створити клацання по цій кнопці. Перевіримо це на формі зі статті, дописавши два обробники:

```js
// Дописано до коду статті.
document.getElementById("submit").addEventListener("click", (e) => {
  console.log("click на кнопці | isTrusted:", e.isTrusted, "| тип:", e.constructor.name);
});
form.addEventListener("submit", (e) => console.log("submitter:", e.submitter?.id ?? null));
```

Ми надрукували літеру в першому полі й натиснули Enter, кнопки мишею не торкаючись:

```text
click на кнопці | isTrusted: true | тип: PointerEvent
submit | defaultPrevented: true | абзац: "You need to fill in both names!"
submitter: submit
```

Першим надруковано клацання по кнопці, хоч по ній ніхто не клацав. Браузер створив його сам і позначив як дію
людини. Другий рядок надрукував обробник, дописаний вище, а третій показує, що поле `submitter` події `submit`
назвало цю кнопку тією, що надіслала форму. Отже, обробник `click` на
кнопці побачив би й Enter. Справжня причина в тому, що клацання по кнопці й надсилання форми не завжди трапляються
разом. Ось дві форми й три способи щось надіслати:

```html
<form id="search"><input id="q"></form>
<form id="signup"><input id="email" required><button id="send">Надіслати</button></form>
```

```js
for (const form of document.forms) {
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    console.log("  submit на формі", form.id);
  });
}
document.querySelector("#send").addEventListener("click", () => console.log("  click на кнопці send"));
```

Спершу ми надрукували літеру в полі першої форми й натиснули Enter. Потім клацнули мишею по кнопці другої форми, не
заповнивши обов'язкове поле. Нарешті виконали в консолі `document.querySelector("#search").requestSubmit()`:

```text
  submit на формі search
  click на кнопці send
  submit на формі search
```

Перший рядок показує, що форму без кнопки надіслано клавішею Enter, і жодного клацання не було. Другий рядок
показує, що клацання по кнопці було, а надсилання не було. Поле має атрибут `required`, тобто воно обов'язкове, тому
браузер зупинив надсилання ще до події `submit` і показав підказку біля поля. Третій рядок показує, що метод
`requestSubmit()` надсилає форму з коду, теж без клацання. Отже, подія `submit` на формі настає тоді й лише тоді,
коли форма справді надсилається, хоч би як це почалося.

### `It's not just web pages`

Цей розділ лише попереджає, що в інших середовищах події виглядають інакше. Наприклад, у Node обробники додають через
`on()`. На цьому етапі розділ можна пропустити.

**Навіщо це в React.** Об'єкт події `e`, `e.target`, `e.preventDefault()` і поділ на функцію й виклик функції
лишаються такими самими. Документація React окремо попереджає про помилку `onClick={handleClick()}`, яка викликає
функцію під час рендеру, а не при клацанні. Це та сама пастка, що з `changeBackground()` вище: дужки викликають
функцію одразу, а в `onClick` потрапляє її результат.

### Запитання до статті

**1. Чому `btn.onclick = a; btn.onclick = b;` викликає лише `b`?**

<details><summary>Відповідь</summary>

`onclick` є звичайним полем об'єкта, і в ньому може лежати одне значення. Друге присвоєння замінює перше.
`addEventListener` зберігає цілий список обробників, тому там спрацювали б обидві функції.

</details>

**2. Чому `submit` слухають на формі, а не на кнопці?**

<details><summary>Відповідь</summary>

Бо клацання по кнопці й надсилання форми не завжди збігаються. Форму без кнопки надсилає клавіша Enter, а форму
будь-якого виду надсилає метод `requestSubmit()`, і клацання там немає. Буває й навпаки: клацання по кнопці є, а
форма не надсилається, бо обов'язкове поле порожнє. Подія `submit` настає саме тоді, коли форма надсилається.

</details>

## Стаття `Event bubbling`

**Де читати:** [MDN, англійська
версія](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Event_bubbling). Це наступний
урок того самого курсу.

**Якщо часу мало,** прочитайте `Bubbling example`, `Event delegation` і `target and currentTarget`. Ці розділи прямо
стосуються завдання дня.

У прикладах цієї статті обробники нічого не друкують у консоль. Вони дописують рядки в елемент `<pre id="output">`
на сторінці. Ми клацали мишею так, як просить стаття, а потім копіювали текст із цього елемента.

### `Introducing event bubbling`

**`Setting a listener on a parent element`.** Кнопка лежить у `<div>`, а обробник стоїть лише на `<div>`. Обробник
друкує `e.currentTarget.tagName`, тобто назву тегу того елемента, чий обробник зараз працює:

```html
<div id="container">
  <button>Click me!</button>
</div>
<pre id="output"></pre>
```

```js
const output = document.querySelector("#output");
function handleClick(e) {
  output.textContent += `You clicked on a ${e.currentTarget.tagName} element\n`;
}

const container = document.querySelector("#container");
container.addEventListener("click", handleClick);
```

Після клацання мишею по кнопці в `<pre>` з'явився рядок:

```text
You clicked on a DIV element
```

Ми клацнули по кнопці, а спрацював обробник на `<div>`. Кнопка лежить усередині `<div>`, тому для браузера клацання
по кнопці є також клацанням по `<div>`.

**`Bubbling example`.** Тепер обробник `handleClick` стоїть на кнопці, на `<div>` і на `<body>`. Розмітка та сама, а
три рядки реєстрації такі:

```js
document.body.addEventListener("click", handleClick);
container.addEventListener("click", handleClick);
button.addEventListener("click", handleClick);
```

Після клацання мишею по кнопці:

```text
You clicked on a BUTTON element
You clicked on a DIV element
You clicked on a BODY element
```

Обробники спрацювали від кнопки вгору, хоч реєстрували ми їх у зворотному порядку. Отже, порядок задає місце
елемента в дереві, а не порядок рядків у коді. Звідси й назва: подія піднімається вгору, як бульбашка у воді, тому
цей рух називають **спливанням**. Повний шлях події, з рухом униз і вгору, розібрано в лекції, у розділі «Шлях
події».

**`Video player example`.** Це приклад, де спливання шкодить. На сторінці є кнопка й схований контейнер `<div>` з
відео. Задумано три дії: кнопка показує контейнер, клацання по відео запускає його, а клацання по контейнеру поза
відео ховає контейнер. Розмітка статті:

```html
<button>Display video</button>

<div class="hidden">
  <video>
    <source src="/shared-assets/videos/flower.webm" type="video/webm" />
    <p>
      Your browser doesn't support HTML video. Here is a
      <a href="rabbit320.mp4">link to the video</a> instead.
    </p>
  </video>
</div>
```

Стилі статті роблять клас `hidden` невидимим (`display: none`). Код статті й наші дописані рядки:

```js
const btn = document.querySelector("button");
const box = document.querySelector("div");
const video = document.querySelector("video");

// Дописано для перевірки: після кожного клацання друкуємо, де клацнули і чи схований контейнер.
document.addEventListener("click", (e) => {
  console.log("клацання по", e.target.tagName, "| контейнер схований:", box.classList.contains("hidden"));
});
video.play = () => console.log("  video.play() викликано");

btn.addEventListener("click", () => box.classList.remove("hidden"));
video.addEventListener("click", () => video.play());
box.addEventListener("click", () => box.classList.add("hidden"));
```

Файлу з відео в нас не було, тому справжній `video.play()` нічого б не показав. Ми замінили його функцією, яка
лише друкує рядок. Обробник на `document` стоїть найвище, тому він працює останнім і бачить уже кінцевий стан. Ми
клацнули мишею по кнопці, потім по відео:

```text
клацання по BUTTON | контейнер схований: false
  video.play() викликано
клацання по VIDEO | контейнер схований: true
```

Перший рядок показує, що кнопка відкрила контейнер. Після клацання по відео `play()` викликано, але контейнер знову
схований. Клацання спливло від `<video>` до `<div>`, і там спрацював обробник, який ховає контейнер. Людина бачить,
що відео запустилося й одразу зникло.

**`Fixing the problem with stopPropagation()`.** Стаття виправляє це так: обробник відео викликає
`event.stopPropagation()`, тобто забороняє події йти далі вгору. Решта коду та сама:

```js
video.addEventListener("click", (event) => {
  event.stopPropagation();
  video.play();
});
```

Ті самі два клацання, а третім ми клацнули по сірому контейнеру поза відео:

```text
клацання по BUTTON | контейнер схований: false
  video.play() викликано
клацання по DIV | контейнер схований: true
```

Тепер `play()` викликано, і рядка `клацання по VIDEO` немає. Подія не дійшла до `<div>`, тому контейнер лишився
відкритим. Але вона не дійшла й до нашого обробника на `document`, бо він теж лежить вище. Це і є ціна
`stopPropagation()`: подія зникає для всіх обробників вище, а не лише для того, якому вона заважала. Там може бути,
наприклад, код аналітики, який рахує клацання, або код, що закриває меню при клацанні поза ним. Третє клацання, по
самому контейнеру, сховало його, як і задумано.

Є інше рішення, про яке стаття не каже. Обробник контейнера може перевіряти, чи клацнули по самому контейнеру, а не
по чомусь усередині нього. Відео тоді не зупиняє подію:

```js
btn.addEventListener("click", () => box.classList.remove("hidden"));
video.addEventListener("click", () => video.play());
box.addEventListener("click", (event) => {
  if (event.target === box) box.classList.add("hidden");   // лише клацання по самому контейнеру
});
```

Ті самі три клацання:

```text
клацання по BUTTON | контейнер схований: false
  video.play() викликано
клацання по VIDEO | контейнер схований: false
клацання по DIV | контейнер схований: true
```

Відео запустилося, контейнер лишився відкритим, а обробник на `document` побачив усі три клацання.

### `Event capture`

**Занурення** — це рух події у протилежному напрямку, згори вниз до елемента, де вона сталася. Стаття пояснює, що
обробники цю фазу типово пропускають. Щоб обробник спрацював під час занурення, йому передають `{ capture: true }`.
Код той самий, що в `Bubbling example`, лише на `<body>` і `<div>` додано цей параметр:

```js
document.body.addEventListener("click", handleClick, { capture: true });
container.addEventListener("click", handleClick, { capture: true });
button.addEventListener("click", handleClick);
```

Після клацання мишею по кнопці:

```text
You clicked on a BODY element
You clicked on a DIV element
You clicked on a BUTTON element
```

Порядок обернувся. Подія спершу пройшла згори вниз, і обробники `<body>` та `<div>` спрацювали на цьому шляху. Потім
подія дійшла до кнопки, де обробник стоїть без параметра.

Стаття пояснює, звідки взялися дві фази. Колись два найпопулярніші браузери робили по-різному: Netscape проводив
подію лише згори вниз, а Internet Explorer лише знизу вгору. Організація W3C, яка тоді писала вебстандарти, взяла
обидва способи в один стандарт. Тому зараз є обидві фази, а обробники типово працюють на спливанні.

### `Event delegation`

**Делегування** означає, що один обробник на батьківському елементі обробляє події всіх дітей. Воно можливе завдяки
спливанню: подія з будь-якої дитини доходить до батька. Стаття показує сітку з 16 плиток у контейнері:

```html
<div id="container">
  <div class="tile"></div>
  <!-- ще 15 таких самих плиток -->
</div>
```

```css
#container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 100px;
}
```

```js
function random(number) {
  return Math.floor(Math.random() * number);
}

function bgChange() {
  const rndCol = `rgb(${random(255)} ${random(255)} ${random(255)})`;
  return rndCol;
}

const container = document.querySelector("#container");

container.addEventListener("click", (event) => {
  event.target.style.backgroundColor = bgChange();
});

// Дописано для перевірки: кому дісталося нове тло.
container.addEventListener("click", (event) => {
  console.log("target:", event.target.id || event.target.className || event.target.tagName,
    "| тло:", event.target.style.backgroundColor);
});
```

Після клацання мишею по шостій плитці:

```text
target: tile | тло: rgb(146, 238, 198)
```

Обробник стоїть один, на контейнері, а пофарбувалася та плитка, по якій клацнули. Поле `event.target` вказує на
найглибший елемент під вказівником, а в цьому прикладі всередині плитки нічого немає. Тому `target` завжди є плиткою.

Тепер змінимо дві речі, щоб побачити межі цього коду. У першу плитку покладемо значок `<span class="icon">★</span>`,
а між плитками додамо проміжок `gap: 10px`. Код обробників той самий. Ми клацнули мишею по значку, по другій плитці
й по проміжку між першою та другою плитками:

```text
target: icon | тло: rgb(55, 233, 230)
target: tile | тло: rgb(27, 83, 239)
target: container | тло: rgb(93, 97, 203)
```

Перший рядок показує, що після клацання по значку пофарбувався значок, а не плитка. Третій рядок показує, що після
клацання по проміжку пофарбувався весь контейнер, бо під вказівником не було жодної плитки. Обидва випадки
виправляє метод `closest`, який шукає потрібного предка від `target` угору. Як ним користуватися при делегуванні,
показано в лекції, у розділі «Делегування». Саме цю пастку з іконкою описує й план дня, а завдання дня застосовує
той самий зразок до видалення елемента.

### `target and currentTarget`

Це найважливіший для сьогоднішньої пастки розділ. `event.target` показує елемент, де подія почалась, і не змінюється
під час спливання. `event.currentTarget` показує елемент, чий обробник зараз працює, і тому змінюється на кожному
кроці. Стаття повторює `Bubbling example`, але друкує обидва поля:

```js
const output = document.querySelector("#output");
function handleClick(e) {
  const logTarget = `Target: ${e.target.tagName}`;
  const logCurrentTarget = `Current target: ${e.currentTarget.tagName}`;
  output.textContent += `${logTarget}, ${logCurrentTarget}\n`;
}

const container = document.querySelector("#container");
const button = document.querySelector("button");

document.body.addEventListener("click", handleClick);
container.addEventListener("click", handleClick);
button.addEventListener("click", handleClick);
```

Після клацання мишею по кнопці:

```text
Target: BUTTON, Current target: BUTTON
Target: BUTTON, Current target: DIV
Target: BUTTON, Current target: BODY
```

Ми також клацнули по `<div>` праворуч від кнопки, де самої кнопки вже немає:

```text
Target: DIV, Current target: DIV
Target: DIV, Current target: BODY
```

У першому виводі `target` весь час дорівнює `BUTTON`, бо подія почалася на кнопці, а `currentTarget` іде вгору разом
із подією. У другому виводі подія почалася на `<div>`, тому обробник кнопки не спрацював зовсім: кнопка не лежить на
шляху від `<div>` угору.

### `Summary` і `See also`

У `Summary` стаття нагадує, що події не є частиною самої мови JavaScript, а визначені вебплатформою, тобто
браузерними API. Node показує це наочно. У ньому теж є класи `EventTarget` і `Event`, але документація Node каже, що
там немає ієрархії й спливання. Немає там і сторінки з елементами:

```js
const target = new EventTarget();
target.addEventListener("ping", (e) => console.log("Node отримав", e.type, "| bubbles:", e.bubbles));
console.log("dispatchEvent повернув", target.dispatchEvent(new Event("ping")));
console.log("typeof document:", typeof document);
```

```text
Node отримав ping | bubbles: false
dispatchEvent повернув true
typeof document: undefined
```

Цей код запущено в Node 24. Обробник спрацював, тож механізм обробників у Node є. Але `document` не існує, тому
клацати там нема по чому.

У `See also` є посилання на `domevents.dev`, де можна подивитися рух події наочно.

**Навіщо це в React.** Спливання діє й за деревом компонентів React, а `e.stopPropagation()` зупиняє рух по цьому
дереву. Що з цього виходить, показано в лекції, у розділі «Як це проявиться в React». Сторінка
[Responding to Events](https://react.dev/learn/responding-to-events) радить для складних випадків інший підхід:
дочірній компонент сам викликає функцію, отриману від батька. Тоді шлях виконання легше простежити в коді.

### Запитання до статті

**1. Чому у прикладі з відео контейнер ховається при клацанні по відео?**

<details><summary>Відповідь</summary>

Клацання спливає від відео до контейнера, і там спрацьовує обробник приховування. Для браузера клацання по нащадку є
також клацанням по предку на шляху події.

</details>

**2. В обробнику делегування використано `event.target.style`. Що зламається, якщо в плитку покласти значок?**

<details><summary>Відповідь</summary>

`event.target` стане значком, якщо клацнули по ньому, тому колір зміниться у значка, а не в плитки. Плитку потрібно
знаходити через `event.target.closest(...)`.

</details>

## Сторінка `Event: preventDefault() method`

**Де читати:** [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault). Це довідкова сторінка,
читання займе кілька хвилин.

### Вступ і `Syntax`

Метод каже браузеру, що подію обробляє ваш код, тому браузерна дія не має відбутися. Метод не має аргументів і нічого
не повертає. Сторінка наводить приклади дій: прокручування сторінки, перехід за посиланням, вставлення тексту.

Важливе речення для сьогоднішнього дня: подія продовжує рух як зазвичай, доки хтось не викличе `stopPropagation()` або
`stopImmediatePropagation()`. Тобто скасування дії браузера й зупинка руху події є двома різними речами.

### `Examples`

`Blocking default click handling` показує прапорець, який не можна поставити. Обробник клацання дописує попередження
в `<div>` і викликає `preventDefault()`. Код сторінки й наш дописаний обробник:

```html
<p>Please click on the checkbox control.</p>

<form>
  <label for="id-checkbox">Checkbox:</label>
  <input type="checkbox" id="id-checkbox" />
</form>

<div id="output-box"></div>
```

```js
const checkbox = document.querySelector("#id-checkbox");

checkbox.addEventListener("click", checkboxClick);

function checkboxClick(event) {
  const warn = "preventDefault() won't let you check this!\n";
  document.getElementById("output-box").innerText += warn;
  event.preventDefault();
}

// Дописано для перевірки: стан прапорця під час обробки й після неї.
document.addEventListener("click", (event) => {
  console.log("під час обробки checked:", checkbox.checked, "| defaultPrevented:", event.defaultPrevented);
  setTimeout(() => console.log("після обробки checked:", checkbox.checked));
});
```

Після клацання мишею по прапорцю на сторінці з'явився текст `preventDefault() won't let you check this!`, а в
консолі такі рядки:

```text
під час обробки checked: true | defaultPrevented: true
після обробки checked: false
```

Схожий дослід із прапорцем є в теорії дня, у блоці «`preventDefault` скасовує типову дію, але не зупиняє
спливання». Тут видно ще одну тонкість. Під час обробки поле `checked` уже дорівнює `true`, хоч на екрані позначка
так і не з'явилася. Після обробки воно повернулося до `false`. Браузер перемикає прапорець заздалегідь, ще до
першого обробника, щоб обробники бачили новий стан. Коли подія пройшла весь шлях, браузер дивиться, чи її скасовано,
і якщо так, повертає старий стан. У стандарті DOM це кроки `legacy-pre-activation behavior` і
`legacy-canceled-activation behavior`, і вони існують лише для прапорців і перемикачів. Ці кроки розібрано нижче, у
розділі `2.9 Dispatching events`.

Звідси практичний наслідок. Якщо обробник клацання по прапорцю читає `checked`, він бачить уже новий стан, навіть
якщо хтось потім скасує клацання.

### `Notes`

Подію називають **скасовною**, якщо її дію браузера можна скасувати. Це записано в полі `event.cancelable`. Сторінка
називає дві межі методу `preventDefault()`:

- Виклик на події, яка не є скасовною, нічого не робить. Подія, створена через `new Event(...)`, типово не є
  скасовною.
- Виклик в обробнику з `{ passive: true }` теж нічого не робить, а в консолі може з'явитися попередження.

Першу межу перевіримо власною подією `ping`. Метод `dispatchEvent` розсилає подію з коду й повертає `false`, якщо
її скасовано, інакше `true`:

```js
document.body.innerHTML = `<div id="outer"><span id="inner"></span></div>`;
const outer = document.querySelector("#outer");
const inner = document.querySelector("#inner");
outer.addEventListener("ping", (e) => console.log("  outer побачив", e.type));

let event = new Event("ping");
console.log("типово: bubbles", event.bubbles, "cancelable", event.cancelable);
console.log("dispatchEvent повернув", inner.dispatchEvent(event));

event = new Event("ping", { bubbles: true, cancelable: true });
inner.addEventListener("ping", (e) => e.preventDefault());
console.log("dispatchEvent повернув", inner.dispatchEvent(event), "| defaultPrevented", event.defaultPrevented);

event = new Event("ping", { bubbles: true });      // cancelable: false
console.log("dispatchEvent повернув", inner.dispatchEvent(event), "| defaultPrevented", event.defaultPrevented);
```

```text
типово: bubbles false cancelable false
dispatchEvent повернув true
  outer побачив ping
dispatchEvent повернув false | defaultPrevented true
  outer побачив ping
dispatchEvent повернув true | defaultPrevented false
```

Перший виклик нічого не надрукував від `outer`: власна подія типово не спливає. Другий виклик показує, що
`preventDefault()` спрацював, і метод `dispatchEvent` повернув `false`. Третій показує, що за `cancelable: false` той
самий `preventDefault()` у тому самому обробнику не змінив нічого.

Другу межу перевіримо на прапорці. Клацання по прапорцю скасовне, але обробник зареєстровано як пасивний:

```html
<input type="checkbox" id="agree">
```

```js
const agree = document.querySelector("#agree");
agree.addEventListener("click", (event) => {
  event.preventDefault();                          // пасивний обробник: виклик нічого не дасть
  console.log("пасивний обробник | cancelable:", event.cancelable, "| defaultPrevented:", event.defaultPrevented);
}, { passive: true });
document.addEventListener("click", () => setTimeout(() => console.log("після обробки checked:", agree.checked)));
```

Після клацання мишею по прапорцю браузер спершу записав у консоль попередження, а потім ішли наші рядки:

```text
Unable to preventDefault inside passive event listener invocation.
пасивний обробник | cancelable: true | defaultPrevented: false
після обробки checked: true
```

Подія скасовна, але `defaultPrevented` лишився `false`, а прапорець перемкнувся. Браузер прямо попередив, що
скасування в пасивному обробнику неможливе. Навіщо взагалі потрібні пасивні обробники, пояснено нижче, у розділі
`2.8 Observing event listeners`.

Сторінка також радить не використовувати `preventDefault()` там, де є прямий спосіб. Щоб людина не могла змінити
поле форми, є атрибути `disabled` і `readonly`. Для перевірки введення є вбудована перевірка форм, як атрибут
`required` у прикладі з формою вище. Для заборони прокручування є властивість CSS `overflow`.

**Навіщо це в React.** У React цей метод використовують найчастіше на події форми, щоб сторінка не
перезавантажувалась. Документація React прямо каже, що `preventDefault()` не пов'язаний зі `stopPropagation()`.

### Запитання до сторінки

**1. Чи зупиняє `preventDefault()` рух події?**

<details><summary>Відповідь</summary>

Ні. Він лише скасовує дію браузера. Подія продовжує рух, і обробники вище спрацюють. Вони навіть можуть дізнатися про
скасування через `event.defaultPrevented`.

</details>

**2. Чому `preventDefault()` в обробнику власної події `new Event("ping")` нічого не змінює?**

<details><summary>Відповідь</summary>

Така подія типово має `cancelable` рівне `false`. Метод спрацьовує лише на скасовних подіях, тому подію створюють із
`{ cancelable: true }`.

</details>

## Стандарт DOM, розділ `2 Events`

**Де читати:** [DOM Standard, § 2](https://dom.spec.whatwg.org/#events). Сервер плану: `webstandards-docs`.

### Як читати цей стандарт

Як читати стандарти загалом, пояснено в розборі читання дня 6, у розділі «Як читати стандарти»: там є і мова IDL,
і слово `this`, і короткі описи для розробників. Коротко: стандарт написано для авторів браузерів, тому поведінку
описано як алгоритми з кроками. Браузер не зобов'язаний мати саме такий код, але результат має бути саме таким. Тому
стандарт є найточнішою відповіддю на запитання «у якому порядку це відбувається?».

У розділі про події трапляються нові для вас слова:

| Що ви бачите | Що це означає |
|--------------|---------------|
| `flag`, наприклад `canceled flag` | Внутрішній прапорець події: позначка «так» чи «ні», яку код сторінки напряму не бачить |
| `The stopPropagation() method steps are to set this's stop propagation flag` | Метод насправді лише ставить внутрішній прапорець, а перевіряють його інші кроки |
| `dispatch` | Алгоритм розсилання: провести подію шляхом і викликати обробники |
| `event listener` | Внутрішній запис про обробник: тип, функція, `capture`, `passive`, `once`, `signal`, `removed` |
| `activation behavior` | Дія браузера після клацання, наприклад перехід за посиланням чи надсилання форми |

**Як знайти відповідь.** Натисніть Ctrl+F і шукайте назву поля чи методу. Спершу читайте опис для розробників, а кроки
алгоритму читайте лише для точних деталей.

**Якщо часу мало,** прочитайте `2.1`, опис для розробників у `2.2` і вирізку алгоритму в `2.9` нижче.

Приклади з цього розділу ми запускали так само, як приклади MDN: окремими сторінками в Chrome без вікна. Більшість
із них розсилає подію з коду, тому клацати не треба, і вивід з'являється одразу після завантаження сторінки.

### `2.1 Introduction to "DOM Events"`

Вступ показує кілька коротких прикладів по черзі.

Спершу йде звичайне додавання обробника, як у статтях MDN. Тут же стандарт нагадує два способи прибрати обробник:
`removeEventListener` з тими самими аргументами або сигнал `AbortSignal`, як у лекції.

Далі стандарт показує, що код може сам створити подію й розіслати її. Таку подію називають **синтетичною**. Подія
`CustomEvent` має поле `detail`, куди кладуть власні дані. У стандарті функцію `process` не визначено, тому ми
дописали її, а також другу частину, яка показує повернення `dispatchEvent`:

```html
<div id="obj"></div>
```

```js
const obj = document.querySelector("#obj");
function process(detail) { console.log("detail:", JSON.stringify(detail)); }   // дописано

// add an appropriate event listener
obj.addEventListener("cat", function(e) { process(e.detail) })

// create and dispatch the event
var event = new CustomEvent("cat", {"detail":{"hazcheeseburger":true}})
obj.dispatchEvent(event)

// дописано: те саме повернення dispatchEvent для скасовної події, яку обробник скасував
obj.addEventListener("save", (e) => e.preventDefault());
const save = new CustomEvent("save", { cancelable: true, detail: { id: 7 } });
if (obj.dispatchEvent(save)) {
  console.log("подію не скасовано, зберігаємо");
} else {
  console.log("обробник скасував подію, нічого не робимо");
}
```

```text
detail: {"hazcheeseburger":true}
обробник скасував подію, нічого не робимо
```

Перший рядок показує, що дані з `detail` дійшли до обробника. Другий показує, що `dispatchEvent` повернув `false`,
бо обробник скасував подію. Стандарт пропонує саме так давати обробникам право голосу: код розсилає скасовну подію й
продовжує роботу, лише якщо `dispatchEvent` повернув `true`. Так влаштовано й форму: якщо обробник `submit` скасував
подію, браузер форму не надсилає.

Наприкінці вступу стандарт описує шлях події двома реченнями. Спершу викликаються обробники з `capture`, рівним
`true`, на всіх предках цілі й на ній самій, від кореня вниз. Потім, якщо `bubbles` дорівнює `true`, викликаються
решта обробників у зворотному порядку, знизу вгору. Це показано на документі зі `<span>` усередині абзацу. У стандарті
функцію `debug` не визначено, тому ми дописали її:

```html
<!doctype html>
<html>
 <head>
  <title>Boring example</title>
 </head>
 <body>
  <p>Hello <span id=x>world</span>!</p>
  <script>
   // Дописано: у стандарті debug не визначено, тут він друкує три значення.
   function debug(target, currentTarget, phase) {
     console.log("target:", target.nodeName, "| currentTarget:", currentTarget.nodeName, "| eventPhase:", phase)
   }
   function test(e) {
     debug(e.target, e.currentTarget, e.eventPhase)
   }
   document.addEventListener("hey", test, {capture: true})
   document.body.addEventListener("hey", test)
   var ev = new Event("hey", {bubbles:true})
   document.getElementById("x").dispatchEvent(ev)
  </script>
 </body>
</html>
```

```text
target: SPAN | currentTarget: #document | eventPhase: 1
target: SPAN | currentTarget: BODY | eventPhase: 3
```

Обробник `test` спрацював двічі. Поле `target` обидва рази вказує на `span`, бо подію розіслано саме на нього.
Першим спрацював обробник на документі, бо він стоїть на зануренні, а документ є найвищим вузлом. Число 1 у полі
`eventPhase` означає фазу занурення. Другим спрацював обробник на `body`, вже на спливанні, і число 3 означає саме
цю фазу. Стандарт додає: якби обробник стояв на самому `span`, у полі було б число 2, тобто фаза цілі.

### `2.2 Interface Event`

Тут визначено всі поля об'єкта події. Ось вони коротко:

| Поле чи метод | Що означає |
|---------------|------------|
| `type` | назва події |
| `target` | ціль події. `srcElement` є застарілою назвою того самого |
| `currentTarget` | вузол, чий обробник зараз працює. Поза обробкою містить `null` |
| `composedPath()` | список вузлів на шляху події |
| `eventPhase` | фаза: `NONE` = 0, `CAPTURING_PHASE` = 1, `AT_TARGET` = 2, `BUBBLING_PHASE` = 3 |
| `stopPropagation()` | зупинити рух до наступних вузлів |
| `stopImmediatePropagation()` | те саме й не викликати решту обробників цього вузла |
| `bubbles` | чи спливає подія |
| `cancelable` | чи можна скасувати дію браузера |
| `preventDefault()` | скасувати дію браузера |
| `defaultPrevented` | чи скасовано |
| `composed` | чи перетинає подія межу тіньового дерева |
| `isTrusted` | чи створив подію браузер у відповідь на дію людини |
| `timeStamp` | коли створено подію |

**Тіньове дерево** (shadow tree) — це окреме дерево вузлів, яке елемент може тримати всередині себе. Код сторінки не
бачить його вузлів звичайними методами пошуку, і так компонент захищає свою внутрішню будову. Сьогодні воно не
знадобиться, а поле `composed` має сенс лише для нього.

**Поле `isTrusted`** стандарт описує так: воно істинне, якщо подію розіслав браузер, а не код через
`dispatchEvent()`. Є один старий виняток: подія від методу `click()` має `isTrusted`, рівне `false`. Перевіримо всі
три випадки на одній кнопці:

```html
<button id="btn">OK</button>
```

```js
const btn = document.querySelector("#btn");
btn.addEventListener("click", (e) => console.log("isTrusted:", e.isTrusted, "| тип:", e.constructor.name));
console.log("виклик btn.click():");
btn.click();
console.log("dispatchEvent(new MouseEvent(\"click\")):");
btn.dispatchEvent(new MouseEvent("click"));
console.log("справжнє клацання мишею:");
```

Після цього коду ми клацнули мишею по кнопці:

```text
виклик btn.click():
isTrusted: false | тип: PointerEvent
dispatchEvent(new MouseEvent("click")):
isTrusted: false | тип: MouseEvent
справжнє клацання мишею:
isTrusted: true | тип: PointerEvent
```

Лише справжнє клацання дало `true`. Тому код, який перевіряє `isTrusted`, відрізняє людину від скрипту. Метод
`click()` у прикладах лекції створює подію з `false`, і для більшості обробників це не має значення.

Правило для скасування стоїть у короткому описі алгоритму `set the canceled flag`: прапорець ставиться, лише якщо
подія скасовна й обробник не пасивний. Цей крок пояснює обидві межі зі сторінки `preventDefault()`, які ми бачили
вище: подію `ping` без `cancelable` і пасивний обробник на прапорці.

### `2.3 Legacy extensions to the Window interface`

Тут описано застаріле поле `window.event`. Поки працює обробник, у цьому полі лежить подія, яку він обробляє. Його
використовували старі скрипти, і в новому коді воно не потрібне. Якщо побачите в чужому коді `event` без параметра,
це може бути саме воно. Розмітка та сама кнопка `<button id="btn">OK</button>`:

```js
function oldStyle() {                  // параметра немає, а event є: це window.event
  console.log("event.type:", event.type, "| event === window.event:", event === window.event);
}
document.querySelector("#btn").addEventListener("click", oldStyle);
document.querySelector("#btn").click();
console.log("поза обробкою window.event:", window.event);
```

```text
event.type: click | event === window.event: true
поза обробкою window.event: undefined
```

Усередині обробника слово `event` знайшлося, хоч його ніде не оголошено, бо браузер шукає незнайомі імена серед
полів `window`. Поза обробкою поле порожнє. Такий код ламається, щойно обробник стає асинхронним, тому подію завжди
беруть із параметра.

### `2.4 Interface CustomEvent`

Подія з полем `detail` для власних даних. Використовується, коли код хоче повідомити про щось власною подією й
передати дані. Приклад із подією `cat` у розділі `2.1` вище показує саме її. Сьогодні вона не потрібна.

### `2.5 Constructing events` і `2.6 Defining event interfaces`

Це підрозділи для авторів специфікацій. Вони описують, як створюються об'єкти подій і як визначати нові типи.
Пропустіть їх.

### `2.7 Interface EventTarget`

**`EventTarget`** — це основа всього, на що можна вішати обробники. Вузли, вікно й `AbortSignal` є його різновидами.
Важливі відомості:

- Обробник зберігається як внутрішній запис: тип, функція й параметри `capture`, `passive`, `once`, `signal`.
- Обробник із тим самим типом, функцією й `capture` вдруге не додається. Звідси випливає неочевидний факт: одну
  функцію можна додати двічі, якщо один раз із `capture: true`, бо це різні записи.
- `removeEventListener` порівнює саме тип, функцію й `capture`. Значення `once` та `passive` на порівняння не
  впливають.

Перевіримо обидва правила на кнопці в контейнері:

```html
<div id="box"><button id="btn">OK</button></div>
```

```js
const box = document.querySelector("#box");
const btn = document.querySelector("#btn");
const log = (e) => console.log("  log на", e.currentTarget.id, "| фаза", e.eventPhase);

box.addEventListener("click", log);
box.addEventListener("click", log);                       // той самий запис: не додається
box.addEventListener("click", log, { capture: true });    // інше capture: це вже другий запис

console.log("клацання, обидва записи на місці:");
btn.click();

box.removeEventListener("click", log, { once: true });    // once не важить: прибрано запис без capture
console.log("після removeEventListener без capture:");
btn.click();
```

```text
клацання, обидва записи на місці:
  log на box | фаза 1
  log на box | фаза 3
після removeEventListener без capture:
  log на box | фаза 1
```

Три виклики `addEventListener` дали два записи: один на зануренні (фаза 1) і один на спливанні (фаза 3). Виклик
`removeEventListener` з параметром `once` прибрав запис без `capture`, бо `once` не порівнюється, а `capture` не
вказано, тобто дорівнює `false`. Запис занурення лишився. Отже, обробник, доданий із `capture: true`, прибирають теж
із `capture: true`.

Ще одне правило стосується `passive`. Для чотирьох подій, `touchstart`, `touchmove`, `wheel` і `mousewheel`, стандарт
вважає обробник пасивним за замовчуванням, якщо його поставлено на вікно, документ, елемент `html` чи `body`. Подія
`wheel` настає, коли людина крутить коліщатко миші. Перевіримо це на довгій сторінці:

```html
<div id="feed" style="height: 3000px">Стрічка</div>
```

```js
window.addEventListener("wheel", (e) => {
  e.preventDefault();
  console.log("обробник на window без passive | defaultPrevented:", e.defaultPrevented);
});
window.addEventListener("wheel", () => setTimeout(() => console.log("  scrollY після прокрутки:", scrollY), 500));
```

Поле `scrollY` показує, на скільки пікселів сторінку прокручено вниз. Ми крутнули коліщатко над стрічкою, і
браузер записав у консоль попередження, а потім наші рядки:

```text
Unable to preventDefault inside passive event listener due to target being treated as passive. See https://www.chromestatus.com/feature/6662647093133312
обробник на window без passive | defaultPrevented: false
  scrollY після прокрутки: 200
```

Потім ми поставили той самий обробник не на `window`, а на `<div id="feed">`, і крутнули ще раз:

```text
обробник на div без passive | defaultPrevented: true
  scrollY після прокрутки: 0
```

На `window` ми не писали `passive`, а обробник однаково став пасивним, і сторінка прокрутилася на 200 пікселів.
Браузер у попередженні прямо каже, що вважає ціль пасивною. На звичайному `<div>` того самого правила немає, тому
скасування спрацювало, і сторінка не зрушила. Якщо обробнику на вікні справді треба заборонити прокручування, йому
явно передають `{ passive: false }`.

### `2.8 Observing event listeners`

Підрозділ пояснює, навіщо існує `passive`. Під час прокручування браузер мусив би чекати, чи не викличе обробник
`preventDefault()`, бо тоді прокручувати не можна. Поки обробник не завершився, сторінка не рухалася б, і людина
відчувала б затримку. Обробник, позначений `passive`, обіцяє не скасовувати подію, тому браузер починає прокручування
одразу. Стандарт додає, що через це навіть порожній обробник може помітно сповільнити сторінку. Тому для коліщатка й
дотиків на вікні обробник типово пасивний, як показав дослід у розділі `2.7` вище. Цей підрозділ пов'язує події з
наступним днем, де йдеться про швидкість сторінки.

### `2.9 Dispatching events`

Це головний алгоритм дня. Він довгий, бо охоплює тіньові дерева. Якщо викинути цю частину, лишаються такі кроки,
переказані своїми словами:

1. Поставити прапорець «подія розсилається».
2. Побудувати шлях: іти від цілі вгору за батьками й записувати кожен вузол.
3. Знайти вузол, на якому браузер потім виконає дію. Для клацання це перший вузол на шляху, що має `activation
   behavior`, наприклад посилання чи прапорець. Якщо це прапорець чи перемикач, запустити підготовчий крок
   `legacy-pre-activation behavior`: перемкнути його заздалегідь.
4. Пройти шлях із кінця в початок: це занурення. На кожному вузлі викликати обробники. Для цілі фаза дорівнює
   `AT_TARGET`, для решти `CAPTURING_PHASE`.
5. Пройти шлях від початку в кінець: це спливання. Якщо `bubbles` дорівнює `false`, то пропускати всі вузли, крім
   цілі.
6. Очистити `eventPhase` і `currentTarget`. Тому після обробки поле `currentTarget` містить `null`.
7. Якщо подію не скасовано, виконати дію браузера. Якщо скасовано, а вузол є прапорцем чи перемикачем, запустити
   крок `legacy-canceled-activation behavior`: повернути старий стан.
8. Повернути `false`, якщо подію скасовано, інакше `true`.

Цей алгоритм відповідає на чотири запитання з теорії та лекції.

**Чому видалення вузла не змінює шлях?** Шлях будується один раз, на кроці побудови шляху, ще до першого обробника.
Далі алгоритм іде цим готовим списком, хоч би що обробники робили з деревом. Дослід із прибраною карткою є в лекції, у
розділі «Крайні випадки шляху».

**Чому `preventDefault()` на батькові скасовує перехід за посиланням?** Дію браузера алгоритм виконує на окремому
кроці після всього шляху. На той час кожен обробник на кожному вузлі вже мав нагоду поставити прапорець скасування.
Дослід із `<nav>` є в лекції, у розділі «Дія браузера й `preventDefault`».

**Чому `preventDefault()` не зупиняє подію?** Він лише ставить прапорець скасування. Кроки занурення й спливання, які
проводять подію шляхом, цього прапорця не перевіряють. Його читає лише крок, що виконує дію браузера.

**Чому після `await` поле `currentTarget` порожнє?** Алгоритм очищає це поле одразу після спливання, коли подія
пройшла шлях. Код після `await` виконується пізніше, і зазвичай на той час шлях уже пройдено. Є виняток: після зовсім
короткого `await` при справжньому клацанні поле ще може бути заповненим. Чому так буває, пояснено в лекції, у розділі
«Крайні випадки шляху».

Є окремий допоміжний алгоритм виклику обробників на одному вузлі (`inner invoke`). Він пояснює такі деталі:

- Список обробників копіюється перед обходом, тому обробник, доданий під час обробки цього самого вузла, цього разу не
  спрацює.
- Обробник із позначкою `removed` пропускається, тому обробник, прибраний під час обробки, уже не спрацює.
- Обробник із `once` прибирається ще до виклику функції.
- Для пасивних обробників на час виклику ставиться окремий прапорець, через який `preventDefault()` нічого не робить.
- Після кожного обробника перевіряється прапорець `stopImmediatePropagation`.

Перші три з цих правил видно в одному досліді на кнопці `<button id="btn">OK</button>`:

```js
const btn = document.querySelector("#btn");
const late = () => console.log("  late: доданий під час обробки");
const second = () => console.log("  second");

btn.addEventListener("click", () => {
  console.log("  first: додаю late і прибираю second");
  btn.addEventListener("click", late);
  btn.removeEventListener("click", second);
});
btn.addEventListener("click", second);
btn.addEventListener("click", () => console.log("  once: спрацьовую один раз"), { once: true });

console.log("перше клацання:");
btn.click();
console.log("друге клацання:");
btn.click();
```

```text
перше клацання:
  first: додаю late і прибираю second
  once: спрацьовую один раз
друге клацання:
  first: додаю late і прибираю second
  late: доданий під час обробки
```

Під час першого клацання `late` не спрацював, хоч його додали раніше, ніж черга дійшла до кінця списку. Браузер іде
копією списку, зробленою до першого обробника, а в ній `late` ще немає. Обробник `second` теж не спрацював, хоч у
копії він є: його запис позначено як прибраний, і браузер його пропустив. Отже, додавання під час обробки діє з
наступної події, а прибирання діє одразу. Обробник з `once` спрацював один раз. Під час другого клацання `late` уже
був у списку з самого початку, тому спрацював. Виклик `addEventListener` з `late` у другому клацанні нічого не додав,
бо такий запис уже є.

### `2.10 Firing events`

Вираз `fire an event` означає коротку форму: створити подію, задати поля й розіслати. Інші стандарти, зокрема HTML,
постійно вживають цей вираз. Коли в HTML написано `fire an event named click`, мають на увазі саме цей алгоритм.

### `2.11 Action versus occurrence`

Короткий, але важливий підрозділ про спосіб мислення. Подія сповіщає про те, що щось сталося, і може вплинути на дію,
яка відбувається. Сама подія не запускає дії. Наприклад, подія `submit`, створена власноруч і розіслана через
`dispatchEvent`, не надсилає форму: надсилання запускає алгоритм форми, а подія лише повідомляє про нього.
Перевіримо це. Ми зберегли сторінку у файл `s06-submit.html`, тому його ім'я видно в адресі:

```html
<form id="order" action="#sent"><input name="item" value="чай"></form>
```

```js
const form = document.querySelector("#order");
form.addEventListener("submit", (e) => console.log("  подія submit, isTrusted:", e.isTrusted));
const later = () => new Promise((r) => setTimeout(r, 300));

console.log("dispatchEvent(new Event(\"submit\")):");
form.dispatchEvent(new Event("submit", { cancelable: true }));
later().then(() => console.log("  адреса після:", location.href.split("/").pop()));
```

```text
dispatchEvent(new Event("submit")):
  подія submit, isTrusted: false
  адреса після: s06-submit.html
```

Обробник побачив подію `submit`, а адреса сторінки не змінилася: форму ніхто не надсилав. Потім ми виконали в консолі
`form.requestSubmit()`. Обробник надрукував `подія submit, isTrusted: true`, і браузер перейшов на адресу
`s06-submit.html?item=%D1%87%D0%B0%D0%B9#sent`. У цій адресі `item=` і закодоване слово `чай` є даними з поля форми.
Цього разу надсилання запустив алгоритм форми, а подію розіслав уже він сам. Тому й `isTrusted` дорівнює `true`.

**Навіщо це в React.** React будує власну подію поверх справжньої, але порядок дій браузера незмінний. Коли стається
щось незрозуміле, допомагає послідовність із цього алгоритму. Поле `e.nativeEvent` дає справжню подію, а її
`eventPhase` показує, де вона зараз. Як це виглядає у виводі, показано в лекції, у розділі «Як це проявиться в
React».

### Запитання до розділу

**1. Чому один `preventDefault()` на будь-якому вузлі шляху скасовує перехід за посиланням?**

<details><summary>Відповідь</summary>

Він ставить прапорець на самому об'єкті події, а об'єкт один для всього шляху. Дію браузера алгоритм виконує
наприкінці, перевіряючи цей прапорець.

</details>

**2. Обробник на кнопці додає другий обробник на цю саму кнопку під час клацання. Чи спрацює новий обробник цього ж
клацання?**

<details><summary>Відповідь</summary>

Ні. Список обробників скопійовано перед обходом, тому новий запис спрацює лише при наступному клацанні.

</details>

**3. Чому `bubbles: false` не вимикає обробників занурення?**

<details><summary>Відповідь</summary>

Алгоритм завжди проходить шлях у зворотному порядку для занурення, не перевіряючи `bubbles`. Прапорець перевіряють
лише під час спливання.

</details>

## Книжка How to Design Programs, `3.1 Designing Functions`

**Де читати:** [htdp.org, частина перша,
3.1](https://htdp.org/2023-8-14/Book/part_one.html#%28part._sec~3adesign-func%29). Сервер плану: `htdp-book`. Текст
книжки не можна поширювати, тому нижче лише короткий переказ.

**Що це за текст.** Це розділ із рецептом проєктування функцій, той самий, що в попередні дні. Ключове питання
сьогодні інше: чи годиться рецепт для функцій, що змінюють сторінку й нічого не повертають?

### `Information and Data`

Різницю між інформацією й даними вже пояснено в розборі читання дня 6, у розділі про цю книжку, підрозділ
`3.1 Designing Functions`. Сьогодні інформацією є «людина клацнула по кнопці видалення в п'ятому рядку», а
даними є об'єкт події й вузол, на який вказує його `target`.

У тому самому місці книжка згадує поділ, який інженери називають **MVC** (model-view-controller, тобто модель, вигляд
і контролер). Модель — це обробка даних. Вигляд і контролер — це частини, які перекладають дані на те, що бачить
людина, і перекладають дії людини на дані. Книжка каже, що добре зроблені програми тримають ці частини окремо. Це
важливо для дня 7: щойно обчислення стоїть окремо від клацань, його можна перевірити прикладами, не клацаючи мишею.

### `The Design Process`

Сам рецепт із шести кроків уже розібрано в розборі читання дня 4, у розділі «How to Design Programs, розділ 3».

**Застосування до сторінки.** Функція, що змінює сторінку, нічого не повертає. Її сигнатура записує результат як
`void`, тобто «результату немає», а приклад перевіряє стан вузла після виклику. Ось невелика функція для значка
кошика, не пов'язана із завданням дня:

```js
// Element, number -> void
// Пише в значок кошика кількість товарів. Якщо товарів немає, ховає значок.
function showCount(badge, count) {
  badge.textContent = String(count);
  badge.hidden = count === 0;
}

// Приклади. Функція нічого не повертає, тому перевіряємо стан вузла після виклику.
const badge = document.createElement("span");
showCount(badge, 3);
console.log("після showCount(badge, 3): текст", JSON.stringify(badge.textContent), "| hidden", badge.hidden);
showCount(badge, 0);
console.log("після showCount(badge, 0): текст", JSON.stringify(badge.textContent), "| hidden", badge.hidden);
```

```text
після showCount(badge, 3): текст "3" | hidden false
після showCount(badge, 0): текст "0" | hidden true
```

Вузол для прикладу створено через `document.createElement`, і на сторінку його не додано. Отже, функції не потрібні ні
показана сторінка, ні клацання, тому приклад запускається одразу. Це не відступ від рецепта, а його нове застосування.
Завдання дня також виносить пошук потрібного вузла в окрему чисту функцію, тобто функцію, яка лише повертає результат
і нічого не змінює. Таку функцію перевірити ще легше, ніж `showCount`: досить порівняти результат із очікуваним. Це
той самий поділ обчислення й показу, який описано в книжці.

**Навіщо це в React.** Компонент обчислює вигляд, а обробники змінюють стан. Обчислення зазвичай виносять у звичайні
функції, тому їх перевіряють простими прикладами, без браузера.

### Запитання до книжки

**1. Чому корисно винести пошук вузла з обробника в окрему функцію?**

<details><summary>Відповідь</summary>

Така функція отримує вузол і повертає результат, тому її можна перевірити прикладом без клацання. Обробник стає
коротким, а помилку легше знайти.

</details>

---

Цей розбір написано для плану. Він переказує своїми словами сторінки MDN (CC BY-SA 2.5), стандарти WHATWG DOM і HTML
(CC BY 4.0), документацію Node і React і коротко переказує книжку How to Design Programs. Код прикладів MDN наведено
за ліцензією CC0, код прикладів зі стандарту DOM — за ліцензією CC BY 4.0. Права на оригінальні тексти належать
їхнім авторам. Приклади запущено в Chrome 157 без вікна, а приклад з `EventTarget` у Node — у Node 24.
