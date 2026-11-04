# Лекція. День 7. DOM і події

Ця лекція пояснює, у якому вигляді сторінка існує всередині браузера і як браузер повідомляє код про дії людини.
Читання займе близько 35 хвилин. Приклади призначені для консолі браузера. Їхній вивід ми отримали в jsdom, тобто в
імітації браузера для Node, і звірили з браузером Chrome. У вашій консолі він може виглядати трохи інакше, а теги й
значення будуть ті самі.

**Після лекції ви зможете пояснити:**

- що таке дерево DOM і чому у `<ul>` із двома пунктами п'ять дітей;
- чим атрибут відрізняється від властивості;
- яким шляхом проходить подія й у якому порядку працюють обробники;
- чому `currentTarget` після `await` дорівнює `null`;
- чим скасування дії браузера відрізняється від зупинки події;
- чому делегування зручне і де воно не працює;
- де справжні обробники в застосунку на React.

## Ситуація: сердечко, яке відкриває картку

Уявіть каталог товарів. Кожна картка веде на сторінку товару: клацнули по картці, і сторінка відкрилася. У картці є
кнопка із сердечком, яка додає товар в обране. Людина клацає по сердечку, товар додається, а сторінка товару
відкривається теж. Хтось виправляє це через `preventDefault()`, і нічого не змінюється. Хтось додає перевірку
`event.target.tagName === "BUTTON"`, і вона то спрацьовує, то ні: якщо клацнути по самому малюнку сердечка, то
`target` виявляється не кнопкою.

Щоб такі випадки перестали бути загадкою, треба знати дві речі: як влаштована сторінка в браузері й яким шляхом
проходить подія.

## Сторінка як дерево об'єктів

Коли браузер отримує HTML, він читає цей текст і будує в пам'яті об'єкти. Кожен об'єкт пов'язаний із батьком і дітьми,
тому разом вони утворюють дерево. Це дерево і є **DOM** (Document Object Model, об'єктна модель документа). JavaScript
працює лише з цими об'єктами, а не з текстом HTML. Після побудови дерева вихідний текст браузеру вже не потрібен.

Кожен об'єкт дерева називають **вузлом**. Найважливіші види вузлів:

- **елемент** відповідає тегу, наприклад `<li>`;
- **текстовий вузол** містить текст між тегами;
- **документ** є коренем дерева, він доступний як `document`.

Текстові вузли дають перший сюрприз. Пробіли й переноси рядків між тегами теж є текстом:

```js
const list = document.createElement("ul");
list.innerHTML = `
  <li>Чай</li>
  <li>Кава</li>
`;
console.log("childNodes:", list.childNodes.length, "| children:", list.children.length);
console.log("перший вузол:", list.firstChild.nodeName, "| перший елемент:", list.firstElementChild.nodeName);

const box = document.createElement("div");
box.innerHTML = "<table><tr><td>1</td></tr></table>";
console.log(box.innerHTML);
```

```text
childNodes: 5 | children: 2
перший вузол: #text | перший елемент: LI
<table><tbody><tr><td>1</td></tr></tbody></table>
```

Розберемо вивід:

- `childNodes` містить усіх дітей: перенос рядка, `<li>`, перенос рядка, `<li>`, перенос рядка. Це п'ять вузлів.
  `children` містить лише елементи, тому їх два. У прикладному коді майже завжди потрібне `children`.
- `firstChild` повертає текстовий вузол із переносом рядка, а не перший пункт. Це стара пастка: код чекає елемент і
  падає на полі, якого в тексту немає.
- Останній рядок показує, що браузер виправляє HTML під час читання. Ми не писали `<tbody>`, а в дереві він є. Тому
  дерево DOM не завжди збігається з написаним текстом, і в інструментах розробника ви бачите саме дерево.

### Що відбувається із заміною `innerHTML`

Запис у `innerHTML` просить браузер прочитати рядок як HTML і створити нові вузли замість старих. Тому запис
`panel.innerHTML += "..."` не дописує текст, хоч так і виглядає. Він читає старий HTML у рядок, додає до нього новий
шматок і створює все заново:

```js
document.body.innerHTML = `<div id="panel"><input id="name"><button id="save">Зберегти</button></div>`;
const panel = document.querySelector("#panel");
const oldButton = document.querySelector("#save");
oldButton.addEventListener("click", () => console.log("збережено"));
document.querySelector("#name").value = "Оксана";    // людина вже надрукувала ім'я

panel.innerHTML += "<p>Підказка</p>";                // дописуємо один абзац

const newButton = document.querySelector("#save");
console.log("та сама кнопка?", newButton === oldButton);
newButton.click();
console.log("що в полі:", JSON.stringify(document.querySelector("#name").value));
```

```text
та сама кнопка? false
що в полі: ""
```

Рядка `збережено` немає: обробник залишився на старому об'єкті, якого вже немає на сторінці. Надрукований текст теж
зник. Щоб дописати без цієї шкоди, існують `append` і `insertAdjacentHTML`, бо вони не чіпають наявних вузлів. Є й
небезпека іншого роду: рядок від користувача в `innerHTML` стає справжнім HTML, зокрема здатним виконати чужий код.
Для звичайного тексту користуйтеся `textContent`.

## Атрибут і властивість

**Атрибут** — це запис у розмітці: `href="/about"` у тегу. **Властивість** — це поле JavaScript-об'єкта вузла:
`link.href`. Під час побудови вузла браузер створює і те, й інше, а далі зв'язок між ними у кожної пари свій. Назва
цього зв'язку — **відображення** (англійською reflection): стандарт HTML описує для кожної властивості, як вона
пов'язана з атрибутом.

Подивимося, чим відрізняються ці зв'язки. Приклад запущено на сторінці з адресою `https://shop.example/`. На іншій
сторінці початок повної адреси в першому рядку виводу буде іншим:

```js
document.body.innerHTML = `
  <a id="more" class="link big" href="/about">Докладніше</a>
  <input id="agree" type="checkbox" checked>
  <button id="send" disabled>Надіслати</button>`;
const link = document.querySelector("#more");
const box = document.querySelector("#agree");
const button = document.querySelector("#send");

console.log("атрибут href:", link.getAttribute("href"), "| властивість href:", link.href);
console.log("атрибут class:", link.getAttribute("class"), "| властивість className:", link.className);

box.checked = false;                         // так робить користувач, коли знімає прапорець
console.log("checked:", box.checked, "| атрибут є:", box.hasAttribute("checked"));

button.disabled = false;
console.log("disabled:", button.disabled, "| атрибут є:", button.hasAttribute("disabled"));
```

```text
атрибут href: /about | властивість href: https://shop.example/about
атрибут class: link big | властивість className: link big
checked: false | атрибут є: true
disabled: false | атрибут є: false
```

| Пара | Як пов'язані | Що варто пам'ятати |
|------|--------------|-------------------|
| `href` | властивість читає атрибут і дає повну адресу | атрибут містить написане, властивість містить обчислене |
| `class` і `className` | одне значення під різними назвами | слово `class` колись не можна було використати для імені поля |
| `checked` і `value` поля | атрибут задає лише початкове значення | поточний стан лежить у властивості |
| `disabled` | властивість додає чи прибирає атрибут | значення має лише наявність атрибута, текст у ньому не важливий |
| `data-*` і `dataset` | одне значення, завжди рядок | число `7` повернеться як рядок `"7"` |

Головна пара для інтерфейсів — третя. Атрибут `checked` означає «з якого стану починати», а властивість `checked`
означає «який стан зараз». Те саме стосується `value`: у теорії дня це показано на полі вводу. Коли людина змінює
поле, браузер запам'ятовує, що воно вже змінене, і більше не бере значення з атрибута.

## Що таке подія і як її слухати

Коли щось стається, браузер створює **об'єкт події** й повідомляє про нього вузол. Об'єкт містить назву (`type`),
вузол, де все сталося (`target`), і подробиці. Функцію, яку браузер викликає, називають **обробником** або
**слухачем** (англійською listener).

Обробник додають через `addEventListener`. Цей метод має кілька властивостей, яких не видно з першого погляду:

```js
document.body.innerHTML = `<button id="buy">Купити</button>`;
const buy = document.querySelector("#buy");
const log = () => console.log("  той самий обробник");

buy.addEventListener("click", log);
buy.addEventListener("click", log);                   // та сама функція: другий запис ігнорується
buy.addEventListener("click", () => console.log("  другий обробник, один раз"), { once: true });
const stopper = new AbortController();
buy.addEventListener("click", () => console.log("  третій обробник, до abort"), { signal: stopper.signal });

console.log("перше клацання:");
buy.click();
stopper.abort();
console.log("друге клацання:");
buy.click();
```

```text
перше клацання:
  той самий обробник
  другий обробник, один раз
  третій обробник, до abort
друге клацання:
  той самий обробник
```

Рядок за рядком:

- Та сама функція на тому самому вузлі й для тієї самої події реєструється один раз, тому другий виклик нічого не
  додає. Дві однакові на вигляд стрілкові функції є різними об'єктами, тому вони додадуться обидві, а прибрати їх
  через `removeEventListener` неможливо, бо немає посилання.
- На одному вузлі обробники працюють у порядку додавання.
- Параметр `once` прибирає обробник після першого виклику.
- Параметр `signal` приймає той самий сигнал, що й `fetch` у дні 6: `abort()` прибирає обробник. Так одним викликом
  прибирають одразу кілька обробників.

## Шлях події

Найважливіше: подія не залишається там, де виникла. Браузер проводить її шляхом через усіх предків. Порядок такий:

1. **Побудова шляху.** Ще до першого обробника браузер запам'ятовує список: ціль, батько цілі, його батько й так далі
   до `document` і вікна. Стандарт DOM описує це в алгоритмі розсилання події.
2. **Занурення** (capture). Подія йде від вікна вниз до цілі. За замовчуванням обробники цю фазу пропускають. Щоб
   спрацювати тут, обробник додають із параметром `{ capture: true }`.
3. **Ціль.** Подія дійшла до вузла, де все сталося.
4. **Спливання** (bubbling). Подія йде від цілі назад угору.
5. **Дія браузера.** Якщо подію не скасовано, браузер виконує свою звичайну дію.

Подивимося на весь шлях у каталозі. Символ сердечка `<b>` лежить у кнопці, кнопка в картці, картка в секції. На
кожному вузлі висить по два обробники: для занурення (`↓`) і для спливання (`↑`).

```js
document.body.innerHTML = `
  <section id="catalog">
    <article id="card">
      <button id="like"><b id="heart">♥</b></button>
    </article>
  </section>`;
const say = (name) => (event) =>
  console.log(name.padEnd(8), "фаза", event.eventPhase, "| currentTarget:", event.currentTarget.id);

for (const id of ["catalog", "card", "like", "heart"]) {
  const node = document.getElementById(id);
  node.addEventListener("click", say(id + " ↓"), { capture: true });
  node.addEventListener("click", say(id + " ↑"));
}
document.getElementById("heart").click();
```

```text
catalog ↓ фаза 1 | currentTarget: catalog
card ↓   фаза 1 | currentTarget: card
like ↓   фаза 1 | currentTarget: like
heart ↓  фаза 2 | currentTarget: heart
heart ↑  фаза 2 | currentTarget: heart
like ↑   фаза 3 | currentTarget: like
card ↑   фаза 3 | currentTarget: card
catalog ↑ фаза 3 | currentTarget: catalog
```

Число в кожному рядку — це поле `event.eventPhase`: 1 означає занурення, 2 означає, що подія дійшла до цілі, а 3
означає спливання. Перші три рядки показують рух згори вниз через секцію, картку й кнопку. Потім спрацювали обидва
обробники на символі `heart`, бо він і є ціллю. Останні три рядки показують той самий шлях у зворотному порядку.

Тепер можна пояснити ситуацію зі сердечком.

| Запитання | Відповідь | Чому |
|-----------|-----------|------|
| Чому відкрилась сторінка товару? | Обробник картки побачив клацання | Спливання проходить через картку |
| Чому `tagName === "BUTTON"` спрацьовує не завжди? | `target` — це `<b>`, якщо клацнули по символу | Подія виникає на найглибшому вузлі під курсором |
| Чому не допоміг `preventDefault()`? | Він не зупиняє спливання | Він стосується лише дії браузера |
| Що допоможе? | Перевірка через `closest` в обробнику картки | Обробник дізнається, чи клацання прийшло з кнопки |

Можна також викликати `stopPropagation()` в обробнику кнопки, але це має ціну. Подія не дійде й до інших обробників
вище, наприклад до аналітики на `document` чи коду закриття меню по клацанню за його межами.

### Крайні випадки шляху

**Шлях не змінюється після старту.** Браузер будує список один раз. Якщо обробник прибере вузол зі сторінки, подія все
одно пройде далі старим списком:

```js
document.body.innerHTML = `
  <section id="catalog"><article id="card"><button id="remove">Прибрати</button></article></section>`;
const catalog = document.querySelector("#catalog");
const card = document.querySelector("#card");
const button = document.querySelector("#remove");

button.addEventListener("click", () => {
  card.remove();                                       // картки вже немає в документі
  console.log("кнопка: картку прибрано");
});
catalog.addEventListener("click", (event) => {
  console.log("catalog бачить клацання, target:", event.target.id);
  console.log("catalog.contains(target):", catalog.contains(event.target));
  console.log("target.closest('#card'):", event.target.closest("#card")?.id);
  console.log("target.closest('#catalog'):", event.target.closest("#catalog"));
});
button.click();
```

```text
кнопка: картку прибрано
catalog бачить клацання, target: remove
catalog.contains(target): false
target.closest('#card'): card
target.closest('#catalog'): null
```

Секція почула клацання, хоч ціль уже не лежить усередині неї. Метод `closest` іде лише за поточними батьками, тому
знаходить картку, яку забрали разом із кнопкою, а секцію не знаходить. Отже, якщо нижчий обробник змінює дерево, вищий
обробник не може вважати дерево незмінним.

**`currentTarget` існує лише під час обробки.** Коли подія пройшла свій шлях, браузер очищає це поле. `await` віддає
керування, тому код після нього працює вже пізніше:

```js
document.body.innerHTML = `<button id="save"><b id="icon">✓</b></button>`;
const button = document.querySelector("#save");
button.addEventListener("click", async (event) => {
  console.log("до await: target =", event.target.id, "| currentTarget =", event.currentTarget.id);
  await new Promise((r) => setTimeout(r, 10));  // очікування, наприклад запит у мережу
  console.log("після await: target =", event.target.id, "| currentTarget =", event.currentTarget?.id ?? null);
});
document.querySelector("#icon").click();
```

```text
до await: target = icon | currentTarget = save
після await: target = icon | currentTarget = null
```

Поле `target` лишається. Поле `currentTarget` дорівнює `null`. Якщо вузол знадобиться після очікування, збережіть його
в змінну до `await`.

Зовсім коротке очікування може дати інший результат. Замініть у цьому коді рядок очікування на `await
Promise.resolve();`, приберіть останній рядок із `click()` і клацніть по кнопці мишею. Запуск дає такий вивід:

```text
до await: target = icon | currentTarget = save
після await: target = icon | currentTarget = save
```

Другий рядок показує, що `currentTarget` ще на місці. Код після `await` тут є мікрозадачею, тобто коротким завданням,
яке браузер виконує, коли поточний код закінчився. Про це йшлося в дні 5. Справжнє клацання приходить окремою задачею,
тому після обробника поточного коду вже немає, і браузер виконує мікрозадачу, хоч подія ще не закінчила шлях. Виклик
`click()` із коду працює інакше: цей код ще не завершився, тому мікрозадача чекає на його кінець. На той час подія вже
пройшла шлях, і поле дорівнює `null`. На таку різницю не варто покладатися, тому правило лишається те саме: зберігайте
вузол у змінну до `await`.

**Не всі події спливають.** Прапорець `event.bubbles` каже, чи спливає подія. Подія отримання фокуса `focus` не
спливає. Перевіримо це на формі з полем. На формі висять три обробники, а четвертий висить на самому полі й друкує
прапорець:

```js
document.body.innerHTML = `<form id="order"><input id="field"></form>`;
const form = document.querySelector("#order");
const field = document.querySelector("#field");

form.addEventListener("focus", () => console.log("focus на формі, спливання"));
form.addEventListener("focus", () => console.log("focus на формі, занурення"), { capture: true });
form.addEventListener("focusin", () => console.log("focusin на формі, спливання"));
field.addEventListener("focus", (event) => console.log("event.bubbles у focus:", event.bubbles));

field.focus();
```

```text
focus на формі, занурення
event.bubbles у focus: false
focusin на формі, спливання
```

Якщо ви запускаєте код у консолі й вивід порожній, клацніть мишею по полю на сторінці. Тоді сторінка отримає фокус, і
браузер надішле ті самі події.

Рядка `focus на формі, спливання` у виводі немає, бо `focus` не спливає, і звичайний обробник на формі не спрацював.
Обробник `focusin` спрацював, бо ця подія спливає. Обробник `focus` із параметром `{ capture: true }` теж спрацював,
бо занурення проходить незалежно від `bubbles`. Отже, щоб на формі дізнатися про фокус у будь-якому її полі, потрібен
`focusin` або обробник із `capture`.

**Є два способи зупинити подію.** `stopPropagation()` зупиняє рух до наступних вузлів, але інші обробники на поточному
вузлі ще спрацюють. `stopImmediatePropagation()` зупиняє ще й їх.

## Дія браузера й `preventDefault`

Для багатьох подій браузер має власну реакцію. Клацання по посиланню веде за адресою, клацання по кнопці в формі
надсилає форму, клацання по прапорцю перемикає його. Метод `preventDefault()` просить цього не робити. Він працює лише
тоді, коли подія позначена як скасовна (`event.cancelable`), і не працює в обробнику, зареєстрованому з `{ passive:
true }`.

Дія браузера виконується після всього шляху події. Звідси наслідок, який дивує: скасувати перехід може не лише
обробник на посиланні, а й будь-який його предок.

```js
document.body.innerHTML = `<nav id="menu"><a id="go" href="#orders">Замовлення</a></nav>`;
const menu = document.querySelector("#menu");
const go = document.querySelector("#go");
const tick = () => new Promise((r) => setTimeout(r, 20));

go.click();
await tick();
console.log("без скасування адреса:", location.hash);
location.hash = "";
await tick();

menu.addEventListener("click", (event) => event.preventDefault());   // скасовує БАТЬКО
go.click();
await tick();
console.log("зі скасуванням на батькові адреса:", JSON.stringify(location.hash));
```

```text
без скасування адреса: #orders
зі скасуванням на батькові адреса: ""
```

Перший рядок показує звичайний перехід: обробників ще немає, тому браузер записав у адресу `#orders`. Другий рядок
показує, що обробник на `<nav>` скасував перехід, хоч сам `<nav>` не є посиланням. Отже, коли посилання перестало
працювати, шукайте `preventDefault()` не лише на самому посиланні, а й на всіх його предках.

**Пастка з кнопкою у формі.** Тег `<button>` без атрибута `type` усередині форми надсилає форму. Перевіримо це на двох
кнопках:

```js
document.body.innerHTML = `
  <form id="order">
    <button id="plain">Без type</button>
    <button id="safe" type="button">Не надсилає</button>
  </form>`;
const form = document.querySelector("#order");
form.addEventListener("submit", (event) => {
  event.preventDefault();                      // щоб браузер не пішов на нову адресу й вивід не зник
  console.log("  подія submit, її викликала кнопка:", event.submitter.id);
});

console.log('клацання по кнопці з type="button":');
document.querySelector("#safe").click();
console.log("клацання по кнопці без type:");
document.querySelector("#plain").click();
```

```text
клацання по кнопці з type="button":
клацання по кнопці без type:
  подія submit, її викликала кнопка: plain
```

Клацання по кнопці без `type` викликало подію `submit`, а клацання по кнопці з `type="button"` не викликало нічого.
Без `preventDefault()` на події `submit` браузер перейшов би на нову адресу, і стан сторінки зник би. Тому кнопки, що
не надсилають форму, завжди отримують `type="button"`.

## Делегування

**Делегування** означає один обробник на спільному предку замість окремого обробника на кожному дочірньому елементі.
Воно можливе завдяки спливанню. Покажемо його на панелі інструментів текстового редактора. Завдання дня робить таке
для списку, тому там ваш код буде іншим.

```js
document.body.innerHTML = `
  <div id="toolbar">
    <button data-action="bold"><b>Ж</b></button>
    <button data-action="italic"><i>К</i></button>
    <span id="hint">Виберіть дію</span>
  </div>`;
const toolbar = document.querySelector("#toolbar");
toolbar.addEventListener("click", (event) => {
  const button = event.target.closest("[data-action]");
  if (!button || !toolbar.contains(button)) return;     // клацнули повз кнопки
  console.log("дія:", button.dataset.action, "| target:", event.target.tagName);
});
toolbar.querySelector("b").click();
toolbar.querySelector('[data-action="italic"]').click();
toolbar.querySelector("#hint").click();
toolbar.insertAdjacentHTML("beforeend", `<button data-action="link">URL</button>`);
toolbar.querySelector('[data-action="link"]').click();
```

```text
дія: bold | target: B
дія: italic | target: BUTTON
дія: link | target: BUTTON
```

Розберемо тіло обробника:

- `event.target` — найглибший вузол під курсором. Це може бути символ усередині кнопки.
- `closest` перевіряє сам вузол, потім його предків і повертає перший збіг або `null`.
- Перевірка `!button` обробляє клацання по підказці: третє клацання нічого не надрукувало.
- Перевірка `toolbar.contains(button)` потрібна, коли вся панель лежить усередині іншого елемента з таким самим
  атрибутом. Тоді `closest` міг би вийти за межі панелі.
- Кнопка `link` додана вже після реєстрації обробника, і він її однаково бачить. Це найважливіша перевага делегування.

Економія пам'яті на сотні елементів теж існує, але для сторінки зі ста кнопками вона невелика. Важливіша причина інша:
не треба стежити за обробниками, коли елементи з'являються й зникають. Межі теж є: подію, що не спливає, обробник на
предку почує лише під час занурення, а якщо нижчий обробник зупинив спливання, обробник на предку не почує нічого.

## Типові хибні уявлення

**«`event.target` — це елемент, на який я повісив обробник».** Це `currentTarget`. Поле `target` вказує, де подія
виникла, і це може бути глибокий нащадок.

**«`preventDefault()` зупиняє подію».** Він скасовує лише дію браузера. Шлях події продовжується, тому обробники вище
спрацюють.

**«`stopPropagation()` скасовує перехід за посиланням».** Навпаки, перехід відбудеться, бо дію браузера ніхто не
скасовував.

**«Атрибут і властивість — це те саме».** Для `id` майже так. Для `checked` і `value` це різні речі, а `href` має
різний вміст.

**«`innerHTML +=` дописує текст».** Запис створює всі вузли заново, і стара кнопка втрачає обробники.

## Як це проявиться в React

Коли ви пишете `onClick` у React, це не `addEventListener` на вашому вузлі. Починаючи з версії 17, React реєструє
обробники на **корені**, тобто на вузлі, куди змонтовано застосунок. Там він ловить події, що спливли, і сам викликає
ваші функції за деревом компонентів. Це те саме делегування.

Приклади цього розділу використовують React, тому консоль браузера для них не підійде. Проєкт React ви створите в
дні 11. У ньому можна замінити вміст файла `src/main.tsx` кодом прикладу й побачити вивід у консолі браузера. Зараз
достатньо прочитати код і вивід.

Спершу порахуємо слухачі на корені. Код нижче підміняє метод `addEventListener` на майбутньому корені, щоб записати
кожну реєстрацію, а потім просить React створити корінь:

```tsx
import { createRoot } from "react-dom/client";

const container = document.createElement("div");
const registered: string[] = [];
const realAdd = container.addEventListener.bind(container);

// Запам'ятовуємо назву кожної події й фазу, а тоді реєструємо обробник як зазвичай.
container.addEventListener = (
  type: string,
  listener: EventListenerOrEventListenerObject,
  options?: boolean | AddEventListenerOptions,
) => {
  const capture = options === true || (typeof options === "object" && options.capture === true);
  registered.push(type + (capture ? " занурення" : " спливання"));
  realAdd(type, listener, options);
};

createRoot(container);                         // компонент ще не показано, а слухачі вже є
console.log("слухачів на корені:", registered.length);
console.log(registered.filter((name) => name.startsWith("click ")).join(" | "));
```

```text
слухачів на корені: 142
click спливання | click занурення
```

Перший рядок показує, що React зареєстрував 142 слухачі ще до показу першого компонента. Другий рядок показує, що
подія `click` має два слухачі: для занурення й для спливання. Отже, на корені висить не один обробник на весь
застосунок, а окремий обробник майже для кожного типу події.

Тепер зберемо ту саму картку з кнопкою, додамо справжні обробники через `addEventListener` і клацнемо по символу.
Обробник React друкує три поля, а `nativeEvent` є справжньою подією браузера:

```tsx
import type { MouseEvent } from "react";
import { flushSync } from "react-dom";
import { createRoot } from "react-dom/client";

document.body.innerHTML = `<div id="root"></div>`;

const report = (name: string) => (e: MouseEvent) => {
  const target = e.target as Element;                    // де виникла подія
  const own = e.currentTarget as Element;                // ваш елемент, чий onClick зараз працює
  const real = e.nativeEvent.currentTarget as Element;   // де зараз стоїть справжня подія браузера
  console.log(name, "target", target.tagName, "| currentTarget", own.tagName, "| nativeEvent.currentTarget", real.id);
};

function Card() {
  return (
    <article onClick={report("article")}>
      <button id="like" onClick={report("button")}><b id="heart">♥</b></button>
    </article>
  );
}

// flushSync просить React показати компонент одразу, щоб наступні рядки вже знайшли кнопку.
flushSync(() => createRoot(document.querySelector("#root")!).render(<Card />));

// Це справжні обробники браузера, React про них нічого не знає.
document.querySelector("#like")!.addEventListener("click", () => console.log("справжній обробник на кнопці"));
document.addEventListener("click", () => console.log("справжній обробник на document"));

document.querySelector<HTMLElement>("#heart")!.click();
```

```text
справжній обробник на кнопці
button target B | currentTarget BUTTON | nativeEvent.currentTarget root
article target B | currentTarget ARTICLE | nativeEvent.currentTarget root
справжній обробник на document
```

Порядок пояснює шлях події. Справжній обробник на кнопці спрацював першим, бо подія ще не дійшла до кореня. Коли подія
дійшла, React викликав обробники кнопки й картки. Поле `currentTarget` у React показує ваш елемент, а справжня подія в
цю мить стоїть на корені. `document` лежить вище за корінь, тому він спрацював останнім.

Такий порядок має кілька наслідків.

**Зупинка в обробнику React.** `e.stopPropagation()` у React зупиняє рух по дереву компонентів і справжню подію теж.
Щоб це побачити, замініть у прикладі вище рядок кнопки на такий:

```tsx
      <button id="like" onClick={(e) => { report("button")(e); e.stopPropagation(); }}><b id="heart">♥</b></button>
```

```text
справжній обробник на кнопці
button target B | currentTarget BUTTON | nativeEvent.currentTarget root
```

Рядка `article` немає, тому `onClick` на батьку не спрацював. Рядка `document` теж немає. Справжній обробник на кнопці
лежить нижче кореня, тому він устиг спрацювати раніше.

**Зупинка у справжньому обробнику.** Справжній `stopPropagation()` на вузлі нижче кореня не дає події дійти до кореня,
тому не спрацює жоден `onClick`. Щоб це побачити, поверніть рядок кнопки й замініть у тому самому прикладі справжній
обробник на кнопці:

```tsx
document.querySelector("#like")!.addEventListener("click", (event) => {
  console.log("справжній обробник зупинив подію");
  event.stopPropagation();
});
```

```text
справжній обробник зупинив подію
```

У виводі лише один рядок: React не дізнався про клацання взагалі. Таке трапляється, коли сторонній код сам додає
обробники на вузли. Тому, якщо `onClick` раптом перестав працювати, перевірте справжні обробники на вузлах нижче
кореня.

**`currentTarget` після `await`.** `e.currentTarget` після `await` дорівнює `null` і в React:

```tsx
import type { MouseEvent } from "react";
import { flushSync } from "react-dom";
import { createRoot } from "react-dom/client";

document.body.innerHTML = `<div id="root"></div>`;

function SaveButton() {
  const save = async (e: MouseEvent<HTMLButtonElement>) => {
    console.log("до await:", e.currentTarget.tagName);
    await new Promise((r) => setTimeout(r, 10));
    console.log("після await:", e.currentTarget);
  };
  return <button id="save" onClick={save}>Зберегти</button>;
}

flushSync(() => createRoot(document.querySelector("#root")!).render(<SaveButton />));
document.querySelector<HTMLElement>("#save")!.click();
```

```text
до await: BUTTON
після await: null
```

Рядок після `await` друкує `null`, тому читання `e.currentTarget.dataset` у цьому місці впаде. Вузол зберігають у
змінну до `await`, так само як у коді без React.

**Інші події.** Частина подій поводиться інакше, ніж у браузері. Документація React каже, що `onFocus` і `onBlur`
спливають, а `onScroll` не спливає.

**Атрибути й властивості.** Проп `value` робить поле **керованим**: React щоразу наводить властивість `value` у
відповідність до стану, а без `onChange` поле не зміниться під руками людини. Проп `defaultValue` задає лише початкове
значення. Це ті самі атрибут і властивість, тільки під іншими назвами. Той самий поділ є між `checked` і
`defaultChecked`.

**Заміна `innerHTML`.** React змінює в DOM лише те, що справді відрізняється між двома рендерами, тому незмінені вузли
лишаються, а текст у полі не зникає.

## Перевірте себе

Спершу дайте відповідь самі, вголос або письмово, і лише потім розгортайте наші пояснення.

**1. У `<ul>` два `<li>`, між тегами є перенос рядка. Чому `childNodes.length` дорівнює 5, а `children.length`
дорівнює 2?**

<details><summary>Відповідь</summary>

Перенос рядка між тегами є текстовим вузлом. `childNodes` містить три текстові вузли й два елементи, а `children`
містить лише елементи.

</details>

**2. Обробник висить на `<article>`, людина клацнула по `<b>` усередині кнопки. Що буде в `target` і
`currentTarget`?**

<details><summary>Відповідь</summary>

`target` — `<b>`, бо там виникла подія. `currentTarget` — `<article>`, бо там висить обробник, що зараз працює.

</details>

**3. Обробник клацання є і на `<a>`, і на `<nav>` над ним. `<nav>` викликає `preventDefault()`. Чи буде перехід? Чи
спрацює обробник на `<a>`?**

<details><summary>Відповідь</summary>

Переходу не буде, бо браузер виконує дію після всього шляху події й бачить скасування. Обробник на `<a>` спрацює,
причому раніше, бо він нижче на шляху спливання.

</details>

**4. Обробник кнопки робить `await`, а потім читає `event.currentTarget.dataset.id` і падає. Чому й що зробити?**

<details><summary>Відповідь</summary>

Після `await` подія вже закінчила шлях, тому браузер очистив `currentTarget`, і там лежить `null`. Вузол треба
зберегти в змінну до `await`.

</details>

**5. Людина надрукувала текст у полі, а потім код виконав `form.innerHTML += "<p>підказка</p>"`. Що станеться?**

<details><summary>Відповідь</summary>

Усе, що всередині форми, створиться заново. Поле стане новим вузлом із порожнім значенням, а обробники на старих
вузлах зникнуть. Потрібно використовувати `append` чи `insertAdjacentHTML`.

</details>

**6. У React `e.stopPropagation()` викликано в обробнику кнопки. Чи спрацює `onClick` батька й обробник на `document`,
доданий через `addEventListener`?**

<details><summary>Відповідь</summary>

У нашому досліді не спрацював жоден. React зупинив рух по дереву компонентів і зупинив справжню подію на корені, тому
вона не піднялася до `document`.

</details>

## Словничок лекції

| Слово | Що означає |
|-------|------------|
| DOM | дерево об'єктів, яким браузер представляє сторінку |
| атрибут | запис у розмітці, доступний через `getAttribute` |
| властивість | поле JavaScript-об'єкта вузла |
| ціль, `target` | вузол, де виникла подія |
| `currentTarget` | вузол, на якому висить обробник, що зараз працює |
| занурення | перша фаза шляху: від вікна вниз до цілі |
| спливання | остання фаза шляху: від цілі вгору |
| дія браузера | власна реакція браузера на подію, наприклад перехід за посиланням |
| делегування | один обробник на предку для подій з усіх дітей |

## Що читати далі

- [Розбір читання до цього дня](../reading/f0-d07-reading.md): що саме написано в матеріалах дня.
- Event bubbling на MDN, особливо розділи про делегування й `target`.
- Responding to Events у документації React, коли дійдете до подій у React.

---

Лекцію написано для цього плану. Вона спирається на MDN (тексти за ліцензією CC BY-SA 2.5), стандарти WHATWG DOM і
HTML (ліцензія CC BY 4.0), документацію React і запис про зміни в React 17, переказуючи їх своїми словами. Приклади
коду написано для лекції. Їхній вивід отримано в jsdom 30 і React 19.3 та звірено в Chrome 157 без вікна.