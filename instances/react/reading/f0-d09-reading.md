# Розбір читання. День 9. TypeScript: основи

Лекція цього дня розповідає про саму тему, а цей розбір допомагає прочитати чужі тексти. Він показує, де що шукати, що
означають незнайомі слова й що із прочитаного стане в пригоді в React. Оригінали написано англійською, тому назви
розділів подано англійською, щоб їх легко було знайти. Розбір не перекладає текст, а переказує його своїми словами.

Читайте в такому порядку: лекція, потім The Basics (20 хвилин), Everyday Types (40 хвилин), Narrowing (40 хвилин), а
наприкінці два уривки книжки How to Design Programs (30 хвилин).

**Важливе застереження про версії.** Посібник TypeScript написано для старіших версій компілятора, і в кількох місцях
він описує налаштування, які відтоді змінилися. Типові налаштування змінила версія 6.0. Версія 7.0 — це той самий
компілятор, переписаний мовою Go, і вона остаточно прибрала налаштування, які версія 6.0 оголосила застарілими. Ми
перевірили ці місця на TypeScript 7.0.2, найновішій стабільній версії в реєстрі npm, і позначили їх словами «Зміна в
нових версіях». Решта прикладів працює так, як написано.

**Як ми запускали приклади.** Компілятор ми встановили в робочу теку командою `npm i -D typescript`, як радить лекція
в розділі «Що додає TypeScript». Там само пояснено прапорці команди перевірки, яку ми вживаємо в усьому розборі:
`npx tsc --noEmit --strict --target es2022 --pretty false файл.ts`. Файли ми запускали командою `node файл.ts` у Node
24.22. Node виконує файл `.ts` без жодних прапорців: він замінює запис типів пробілами й типів не перевіряє, як
розповідає лекція в розділі «Перевірка й запуск — дві окремі дії». Документація Node.js пише, що Node поводиться так
типово з версій 22.18 і 23.6, а з версії 24.12 ця можливість стабільна. Коли програма падає, Node друкує ще шлях до
файла, рядок коду й перелік викликів. Ці рядки ми пропустили, крім одного випадку, де рядок коду сам щось показує.

**Службові рядки в прикладах посібника.** Сайт посібника будує сторінки спеціальною програмою, і ця програма читає в
коді власні позначки. Рядок `// @errors: 2345` каже їй, яку помилку показати на сторінці, рядок `// ---cut---` каже,
звідки почати показ, а позначка `//  ^?` просить намалювати під змінною її тип, ніби ви навели на неї мишу в
редакторі. Компілятор цих позначок не потребує, тому ми їх прибрали. Записи `declare function`, які кажуть
компілятору «така функція десь існує», не даючи її тіла, ми замінили справжніми функціями, щоб приклад можна було
запустити.

Щоб побачити тип у певному місці без редактора, ми користуємося прийомом із лекції, з розділу «`any`, `unknown` і
`as`: що робити з даними ззовні». Рядок `const a: never = x` навмисно неправильний, бо в тип `never` не можна
покласти нічого. Компілятор відхиляє такий рядок і в повідомленні називає тип, який має `x` саме в цьому місці.

## The Basics

**Де читати:** [The Basics](https://www.typescriptlang.org/docs/handbook/2/basic-types.html) у посібнику TypeScript
Handbook, який пишуть автори самої мови. У примірнику `typescript` цей текст лежить як `handbook-v2/Basics`.

**Що там є.** Текст пояснює, навіщо потрібна перевірка типів і як працює компілятор `tsc`. Синтаксису типів тут
небагато, бо він іде в наступному тексті.

**Якщо часу мало,** прочитайте `Static type-checking`, `Erased Types` і `Strictness`.

### Static type-checking

Автори починають із того, що JavaScript вирішує, що робити зі значенням, лише в момент виконання. Запис
`message.toLowerCase()` може спрацювати, а може й ні, і прочитати це з коду неможливо, доки не відомо, що лежить у
`message`. **Статична перевірка типів** описує значення заздалегідь і знаходить помилки, не запускаючи програму.
Слово «статична» тут означає «без виконання».

Приклад із посібника викликає рядок як функцію. Файл `callable.ts`:

```ts
const message = "hello!";

message();
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false callable.ts
callable.ts(3,1): error TS2349: This expression is not callable.
  Type 'String' has no call signatures.
$ node callable.ts
TypeError: message is not a function
```

Компілятор знайшов помилку, читаючи текст, а Node дізнався про неї, лише коли дійшов до рядка 3. Перший рядок
повідомлення каже «цей вираз не можна викликати». Рядок із відступом пояснює причину. Методи рядка компілятор описує
вбудованим типом `String`, і в цьому описі немає **сигнатури виклику**, тобто запису про те, з якими аргументами
значення можна викликати як функцію. Тип `String` із великої літери згадано ще раз у розділі `The primitives` нижче.

### Non-exception Failures

Заголовок означає «збої без винятку». **Виняток** (exception) — це помилка часу виконання, яка зупиняє код, як
`TypeError` вище. Автори показують випадки, коли JavaScript не кидає винятку, а просто видає щось безглузде, і
TypeScript усе одно позначає такий код. Ось чотири приклади з цього розділу в одному файлі, `typos.ts`:

```ts
const user = {
  name: "Daniel",
  age: 26,
};
console.log(user.location);

const announcement = "Hello World!";
announcement.toLocaleLowercase();
announcement.toLocalLowerCase();

function flipCoin() {
  // Мали на увазі Math.random()
  return Math.random < 0.5;
}

const value = Math.random() < 0.5 ? "a" : "b";
if (value !== "a") {
  // ...
} else if (value === "b") {
  // сюди виконання не дійде ніколи
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false typos.ts
typos.ts(5,18): error TS2339: Property 'location' does not exist on type '{ name: string; age: number; }'.
typos.ts(8,14): error TS2551: Property 'toLocaleLowercase' does not exist on type '"Hello World!"'. Did you mean 'toLocaleLowerCase'?
typos.ts(9,14): error TS2551: Property 'toLocalLowerCase' does not exist on type '"Hello World!"'. Did you mean 'toLocaleLowerCase'?
typos.ts(13,10): error TS2365: Operator '<' cannot be applied to types '() => number' and 'number'.
typos.ts(19,12): error TS2367: This comparison appears to be unintentional because the types '"a"' and '"b"' have no overlap.
$ node typos.ts
undefined
TypeError: announcement.toLocaleLowercase is not a function
```

Node надрукував `undefined` і впав лише на першій описці, тобто про три помилки з п'яти він не повідомив би ніколи.
Розберемо повідомлення компілятора по черзі.

- **Неіснуюче поле.** JavaScript на `user.location` повертає `undefined` без жодної помилки, що й видно в першому
  рядку виводу Node. Компілятор бачить, що в об'єкта є лише `name` і `age`, і позначає читання третього поля.
- **Описки в назвах методів.** Компілятор не лише позначає неіснуючий метод, а й пропонує схожу назву. Тип рядка тут
  записано як `"Hello World!"`, а не `string`, бо значення в `const` змінитися не може. Про такі типи йдеться в
  розділі `Literal Types` нижче.
- **Функція, яку забули викликати.** Без дужок `Math.random` означає саму функцію, а не випадкове число. Запис
  `() => number` у повідомленні означає «функція без параметрів, яка повертає число», і порівнювати її з `0.5`
  безглуздо.
- **Перевірка, яка ніколи не справдиться.** Друга гілка `else if` виконується лише тоді, коли умова `value !== "a"`
  не справдилася, тобто коли в `value` лежить `"a"`. Порівнювати `"a"` з `"b"` немає сенсу, і компілятор каже, що
  в цих двох типів немає спільних значень (`no overlap`).

Для React це головна цінність TypeScript. Компонент отримує свої вхідні дані одним об'єктом, і лекція дня в розділі
«Як це проявиться в React» називає цей об'єкт пропсами. Якщо в назві пропса є описка, JavaScript дає `undefined`.
Документація React у статті «JSX In Depth» старого сайту пише, що `undefined` у JSX нічого не показує, тому на екрані
лишиться порожнє місце, а помилки не буде. Ось те саме без React, лише з об'єктом. Файл `card.js`:

```js
function Card(props) {
  return "Заголовок: " + props.titel;
}

console.log(Card({ title: "Чай" }));
```

```text
$ node card.js
Заголовок: undefined
```

Той самий код із типом пропсів, файл `props.ts`:

```ts
type CardProps = { title: string };

function Card(props: CardProps) {
  return "Заголовок: " + props.titel;
}

console.log(Card({ title: "Чай" }));
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false props.ts
props.ts(4,32): error TS2551: Property 'titel' does not exist on type 'CardProps'. Did you mean 'title'?
```

Без типу описку знайшов би лише той, хто помітив порожнє місце на екрані. З типом її знаходить компілятор ще до
запуску й одразу підказує правильну назву.

### Types for Tooling

Той самий механізм дає редактору коду автодоповнення, швидкі виправлення й перехід до оголошення. Читати цей розділ
уважно не обов'язково.

### `tsc`, the TypeScript compiler

Тут показано встановлення глобальною командою `npm install -g typescript`. У цьому плані робіть інакше: сторінка дня
встановлює TypeScript у проєкт (`npm i -D typescript`), а команду викликає через `npx tsc`. Так кожен проєкт має
власну версію компілятора.

Перший приклад розділу — файл `hello.ts`, у якому немає жодного типу:

```ts
// Greets the world.
console.log("Hello world!");
```

```text
$ npx tsc --pretty false hello.ts
$ echo $?
0
$ cat hello.js
"use strict";
// Greets the world.
console.log("Hello world!");
```

Посібник радить почати з порожньої теки, і в нових версіях це важливо. Якщо в теці лежить файл налаштувань
`tsconfig.json`, команда з назвою файла, як `tsc hello.ts`, не спрацює. Ми поклали в теку з тим самим `hello.ts`
файл `tsconfig.json` із вмістом `{}`:

```text
$ npx tsc --pretty false hello.ts
error TS5112: tsconfig.json is present but will not be loaded if files are specified on commandline. Use '--ignoreConfig' to skip this error.
$ echo $?
1
```

Що означає це повідомлення і що з ним робити, пояснює лекція в розділі «Що додає TypeScript». Усі команди цього
розбору ми запускали в теці без `tsconfig.json`.

Повернімося до першого виводу, отриманого в теці без цього файла. Команда без `--noEmit` нічого не надрукувала, але
створила поруч файл `hello.js`. Він відрізняється від того, що показує посібник, одним рядком: `"use strict"`. Цей
рядок вмикає суворий режим JavaScript, про який розповідає лекція дня 2 в розділі «`Object.freeze`: як перевірити, що
нічого не змінюється». Дописувати його наказує налаштування компілятора `alwaysStrict`. Посібник писали тоді, коли
це налаштування типово було вимкнене. У версії 7.0 його вже не вимкнеш: ми спробували `--alwaysStrict false` і
отримали помилку `TS5108` про те, що налаштування прибрано.

Потім автори переписують `hello.ts` так, щоб функцію `greet` викликали з одним аргументом замість двох:

```ts
// This is an industrial-grade general-purpose greeter function:
function greet(person, date) {
  console.log(`Hello ${person}, today is ${date}!`);
}

greet("Brendan");
```

```text
$ npx tsc --pretty false hello.ts
hello.ts(2,16): error TS7006: Parameter 'person' implicitly has an 'any' type.
hello.ts(2,24): error TS7006: Parameter 'date' implicitly has an 'any' type.
hello.ts(6,1): error TS2554: Expected 2 arguments, but got 1.
$ echo $?
2
$ node hello.js
Hello Brendan, today is undefined!
```

Посібник показує лише останню помилку, про кількість аргументів. Дві помилки `TS7006` додала версія компілятора: вона
типово вимагає типів у параметрів. Про це йдеться в розділі `Strictness` нижче, а про саму помилку — в розділі
`noImplicitAny`.

### Emitting with Errors

Слово **emit** означає «створити файл `.js`». У попередньому виводі видно несподівану річ: `tsc` знайшов три помилки,
але файл `hello.js` усе одно створив, і Node його запустив. Автори пояснюють причину. Людина, яка переводить робочий
проєкт із JavaScript на TypeScript, бачить багато помилок типів, а її код при цьому вже працював. Компілятор не хоче
зупиняти таку людину через кожну помилку.

Код завершення 2 у виводі вище означає саме це: помилки є, але файл створено. Код 1, який ви бачили в лекції з
прапорцем `--noEmit`, означає, що помилки є, а файлів не створено. Прапорець `--noEmitOnError` забороняє створювати
файл, якщо є хоч одна помилка. Ми видалили старий `hello.js` і запустили компілятор із цим прапорцем на тому самому
файлі `hello.ts`, де `greet` викликають з одним аргументом:

```text
$ npx tsc --noEmitOnError --pretty false hello.ts
hello.ts(2,16): error TS7006: Parameter 'person' implicitly has an 'any' type.
hello.ts(2,24): error TS7006: Parameter 'date' implicitly has an 'any' type.
hello.ts(6,1): error TS2554: Expected 2 arguments, but got 1.
$ echo $?
1
$ ls
hello.ts
```

Файла `hello.js` немає, і запускати нічого. Без цього прапорця, як видно в попередньому розділі, файл з'являється
попри помилки й запускається. Це та сама думка, що й у лекції: помилка типу сама собою не заважає коду виконуватися,
і зупинити його може лише ваше рішення не створювати файла.

### Explicit Types

Тут вперше з'являються анотації. Функція `greet(person: string, date: Date)` очікує рядок і дату. Далі автори
навмисно викликають її з `Date()` без слова `new`:

```ts
function greet(person: string, date: Date) {
  console.log(`Hello ${person}, today is ${date.toDateString()}!`);
}

greet("Maddison", Date());
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false hello.ts
hello.ts(5,19): error TS2345: Argument of type 'string' is not assignable to parameter of type 'Date'.
$ node hello.ts
TypeError: date.toDateString is not a function
```

Причина повчальна: `Date()` без `new` у JavaScript повертає рядок із поточною датою, а `new Date()` повертає об'єкт
дати з методами. Перевірити це можна командою `node -p`, яка обчислює вираз і друкує його значення:

```text
$ node -p "typeof Date()"
string
$ node -p "typeof new Date()"
object
```

Компілятор зловив помилку, яку легко пропустити навіть досвідченій людині. Виправлення — написати `new Date()`.

Наприкінці автори нагадують про виведення типу: у `let msg = "hello there!"` анотація не потрібна, бо компілятор сам
бачить, що значення є рядком.

### Erased Types

Це найважливіший розділ тексту. Автори показують, у що компілятор перетворює виправлену функцію `greet`:

```ts
function greet(person: string, date: Date) {
  console.log(`Hello ${person}, today is ${date.toDateString()}!`);
}

greet("Maddison", new Date());
```

```text
$ npx tsc --pretty false hello.ts
$ cat hello.js
"use strict";
function greet(person, date) {
    console.log(`Hello ${person}, today is ${date.toDateString()}!`);
}
greet("Maddison", new Date());
```

У файлі `.js` немає жодного типу: `: string` і `: Date` просто зникли. Правило авторів таке: анотації типів ніколи не
змінюють поведінку програми під час виконання. Node 24 робить те саме стирання, коли запускає `.ts` напряму, і лекція
пояснює це в розділі «Перевірка й запуск — дві окремі дії».

Посібник у цьому розділі показує ще одну зміну: рядковий шаблон зі зворотними лапками перетворився на звичайні рядки.
У нашому виводі шаблон лишився без змін. Чому так, пояснює наступний розділ.

### Downleveling

**Ціль компіляції** (target) — це версія JavaScript, для якої компілятор пише файл `.js`. **Пониження версії**
(downleveling) означає, що компілятор переписує новий синтаксис старішим, щоб код працював там, де нового синтаксису
не знають, наприклад у старих браузерах. Автори показують, як рядковий шаблон стає ланцюжком викликів `concat`:

```js
"Hello ".concat(person, ", today is ").concat(date.toDateString(), "!");
```

**Зміна в нових версіях.** Текст каже, що типова ціль дорівнює ES5, тобто версії стандарту 2009 року. Примітки до
версії 6.0 кажуть інакше: типова ціль тепер збігається з найновішою версією стандарту, зараз це `es2025`, а ціль
`es5` оголошено застарілою. Версія 7.0 цю ціль прибрала зовсім:

```text
$ npx tsc --target es5 --pretty false hello.ts
error TS5108: Option 'target=ES5' has been removed. Please remove it from your configuration.
$ echo $?
2
```

Помилка каже, що налаштування прибрано і його треба видалити. Файл `hello.js` після цієї команди з'явився, але
рядковий шаблон у ньому лишився без змін, тобто понижувати до ES5 компілятор уже не вміє. Прапорець
`--target es2015` із тексту працює й дає той самий файл, що й вище, бо рядкові шаблони з'явилися саме в ES2015.

Саме пониження в нових версіях не зникло. Його видно на новішому синтаксисі, наприклад на необов'язковому ланцюжку
`?.`, який лекція дня 2 пояснює в розділі «Як це проявиться в React». Цей запис з'явився в ES2020. Файл `last.ts`:

```ts
function shout(obj: { last?: string }) {
  return obj.last?.toUpperCase();
}
```

```text
$ npx tsc --target es2019 --pretty false last.ts
$ cat last.js
"use strict";
function shout(obj) {
    var _a;
    return (_a = obj.last) === null || _a === void 0 ? void 0 : _a.toUpperCase();
}
```

Компілятор переписав `?.` так, як це довелося б робити вручну в старому JavaScript. Він кладе `obj.last` у тимчасову
змінну `_a` і перевіряє, чи це не `null` і не `undefined`. Запис `void 0` завжди дає `undefined`. Для цього плану
розділ можна лише переглянути, бо сучасні браузери й Node виконують новий JavaScript без пониження.

### Strictness

**Суворість** тут означає набір перевірок, які можна вмикати окремо. Автори описують їх як регулятор: у м'якому режимі
типи необов'язкові, а що далі повертати регулятор, то більше компілятор вимагає. Прапорець `--strict` вмикає всі
суворі перевірки разом. Найважливіші з них дві, і кожній присвячено окремий підрозділ.

**Зміна в нових версіях.** Текст каже, що типовий режим м'який. Примітки до версії 6.0 кажуть, що `strict` тепер
увімкнено типово. Це видно у виводі розділу про `tsc` вище: команда без жодного прапорця надрукувала помилки `TS7006`.
Ми запустили той самий файл `hello.ts` із `--strict false`. Нагадаємо його:

```ts
// This is an industrial-grade general-purpose greeter function:
function greet(person, date) {
  console.log(`Hello ${person}, today is ${date}!`);
}

greet("Brendan");
```

```text
$ npx tsc --strict false --pretty false hello.ts
hello.ts(6,1): error TS2554: Expected 2 arguments, but got 1.
```

Помилок `TS7006` не стало, лишилася тільки помилка про кількість аргументів, як у посібнику. У завданні дня прапорець
`--strict` усе одно написано явно, щоб із команди було видно, які перевірки ввімкнено.

### `noImplicitAny`

Коли компілятор не може визначити тип, він бере `any`, тобто вимикає перевірку для цього значення. Прапорець
`noImplicitAny` перетворює такий випадок на помилку. Слово **implicit** означає «неявний», тобто такий, який ніхто не
написав. У `greet(person, date)` компілятору нема звідки дізнатися тип параметрів, і саме це повідомляє помилка
`TS7006`: `Parameter 'person' implicitly has an 'any' type`. Ту саму помилку ви побачите на заглушках дня.

### `strictNullChecks`

Без цього прапорця `null` і `undefined` можна покласти в будь-який тип. Автори кажуть, що забуту перевірку на
`null` дехто називає «помилкою на мільярд доларів», бо через неї виникає безліч збоїв. З цим прапорцем `null`
доводиться записувати в типі явно й перевіряти. Завдяки цьому в загадці дня компілятор каже `'user' is possibly
'null'`.

## Everyday Types

**Де читати:** [Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html). У примірнику
`typescript` це `handbook-v2/Everyday Types`.

**Що там є.** Це довідка про типи, які трапляються щодня. Більшість розділів короткі.

**Якщо часу мало,** прочитайте `Object Types`, `Union Types`, `Type Aliases`, `Interfaces`, `Type Assertions` і
`Literal Types`.

### The primitives: `string`, `number`, and `boolean`

**Примітиви** — це прості значення, які не є об'єктами. Окремих типів для цілих і дробових чисел немає: усі вони
`number`. Не плутайте `string` із `String`. Запис `new String("Чай")` створює об'єкт, усередині якого лежить рядок,
тобто об'єкт-обгортку, а тип `String` описує саме такі об'єкти й методи рядка:

```text
$ node -p 'typeof new String("Чай")'
object
$ node -p 'typeof "Чай"'
string
```

Автори пишуть, що типи `String`, `Number` і `Boolean` з великої літери у вашому коді майже не потрібні, і радять
завжди писати `string`, `number` і `boolean`.

### Arrays

`number[]` і `Array<number>` означають те саме: масив чисел. Другий запис містить кутові дужки, які пояснить
завтрашній день. Запис `[number]` означає інше: масив рівно з одного числа. Такий тип називається **кортежем**, і
посібник розбирає його на іншій сторінці.

### `any`

Автори показують, що зі значенням типу `any` дозволено все. Файл `anyobj.ts`:

```ts
let obj: any = { x: 0 };
// Жоден із цих рядків не дасть помилки компіляції.
obj.foo();
obj();
obj.bar = 100;
obj = "hello";
const n: number = obj;
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false anyobj.ts
$ echo $?
0
$ node anyobj.ts
TypeError: obj.foo is not a function
```

Компілятор мовчить, хоча вже третій рядок падає: методу `foo` в об'єкта немає. Останній рядок кладе рядок `"hello"`
у змінну типу `number`, і компілятор це теж пропускає. Автори радять обмежувати вживання `any`, а завдання дня
взагалі його забороняє. Підрозділ `noImplicitAny` повторює думку з попереднього тексту.

### Type Annotations on Variables

Анотація пишеться після імені: `let myName: string = "Alice"`. У більшості випадків вона зайва, бо компілятор виводить
тип сам із початкового значення.

### Functions

Підрозділи `Parameter Type Annotations` і `Return Type Annotations` показують, де писати тип параметра, як у
`greet(name: string)`, і тип результату, як у `getFavoriteNumber(): number`. Підрозділ
`Functions Which Return Promises` показує запис `Promise<number>` для функції `async`, яка повертає число. Такий самий
запис ви допишете у `fakeRequest`.

У підрозділі `Anonymous Functions` є важливе поняття **контекстної типізації**. Коли функцію передають у
`names.forEach`, компілятор уже знає, що її параметр є рядком, бо бачить масив рядків. Приклад із посібника, у якому
ми в другому виклику навмисно зробили описку, `foreach.ts`:

```ts
const names = ["Alice", "Bob", "Eve"];

// Контекстна типізація: параметр s отримав тип string
names.forEach(function (s) {
  console.log(s.toUpperCase());
});

// Те саме працює для стрілкових функцій
names.forEach((s) => {
  console.log(s.toUppercase());
});
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false foreach.ts
foreach.ts(10,17): error TS2551: Property 'toUppercase' does not exist on type 'string'. Did you mean 'toUpperCase'?
$ node foreach.ts
ALICE
BOB
EVE
TypeError: s.toUppercase is not a function
```

У параметра `s` немає анотації, і все одно немає помилки `TS7006`. Компілятор узяв тип із контексту: `forEach`
викликає функцію з елементами масиву, а масив складається з рядків. Тому він і знайшов описку в `toUppercase`.

Те саме відбувається в React. Документація React у статті «Using TypeScript», у розділі `DOM Events`, пише, що тип
події часто виводиться з обробника. Коли ви пишете функцію прямо в атрибуті, наприклад
`<input onChange={(event) => ...} />`, опис компонента `input` уже каже, з яким аргументом React її викличе, тому
анотацію `event` писати не треба. Якщо ж функцію винесено окремо, тип події доводиться писати явно.

### Object Types

Об'єктний тип перелічує поля та їхні типи. Роздільником може бути кома або крапка з комою. Підрозділ
`Optional Properties` вводить знак `?` після назви поля: таке поле може бути відсутнім. Приклад із посібника, до якого
ми дописали два виклики, `printname.ts`:

```ts
function printName(obj: { first: string; last?: string }) {
  // Помилка: програма впаде, якщо obj.last не передали.
  console.log(obj.last.toUpperCase());
  if (obj.last !== undefined) {
    // Тут усе гаразд.
    console.log(obj.last.toUpperCase());
  }
  // Безпечний запис сучасним JavaScript:
  console.log(obj.last?.toUpperCase());
}

printName({ first: "Alice", last: "Alisson" });
printName({ first: "Bob" });
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false printname.ts
printname.ts(3,15): error TS18048: 'obj.last' is possibly 'undefined'.
$ node printname.ts
ALISSON
ALISSON
ALISSON
TypeError: Cannot read properties of undefined (reading 'toUpperCase')
```

Компілятор позначив лише рядок 3, де поле читають без перевірки. Два інші способи він дозволив: перевірку
`!== undefined` і необов'язковий ланцюжок `?.`, який дає `undefined` і не викликає методу, коли ліворуч `undefined`.
Перший виклик пройшов усі три рядки, а другий упав саме на рядку 3, бо поля `last` у Боба немає.

Цей текст не згадує перевірку на зайві поля, тому помилка `Object literal may only specify known properties` може
здивувати. Лекція пояснює її в розділі «Як записують типи», в абзаці «Компілятор порівнює форму, а не назву». У
посібнику ця перевірка описана в розділі `Excess Property Checks` окремої сторінки
[Object Types](https://www.typescriptlang.org/docs/handbook/2/objects.html).

### Union Types

Підрозділ `Defining a Union Type` вводить запис `number | string`. Підрозділ `Working with Union Types` пояснює
правило, з яким стикаються всі: операцію дозволено, лише якщо вона законна для кожного варіанта. Обидва приклади з
посібника в одному файлі. Другу функцію посібник теж називає `printId`, а ми перейменували її на `shoutId`, щоб дві
функції могли стояти поруч. Файл `printid.ts`:

```ts
function printId(id: number | string) {
  console.log("Your ID is: " + id);
}
printId(101);
printId("202");
printId({ myID: 22342 });

function shoutId(id: number | string) {
  console.log(id.toUpperCase());
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false printid.ts
printid.ts(6,9): error TS2345: Argument of type '{ myID: number; }' is not assignable to parameter of type 'string | number'.
printid.ts(9,18): error TS2339: Property 'toUpperCase' does not exist on type 'string | number'.
  Property 'toUpperCase' does not exist on type 'number'.
$ node printid.ts
Your ID is: 101
Your ID is: 202
Your ID is: [object Object]
```

Перша помилка про те, що передати можна лише значення одного з варіантів, а об'єкт не підходить ні під число, ні під
рядок. JavaScript цей виклик виконав і склеїв рядок з об'єктом, тому на екрані з'явилося безглузде
`[object Object]`. Друга помилка про читання: метод `toUpperCase` є лише в рядка.

Автори показують два шляхи далі. Перший — звузити тип перевіркою `typeof id === "string"` або `Array.isArray(x)`,
після якої в кожній гілці лишається один варіант. Другий — скористатися тим, що є в усіх варіантах: метод `slice` є і
в рядка, і в масиву, тому функцію `getFirstThree(x: number[] | string)` можна написати без перевірки.

Там же є примітка про те, чому слово «об'єднання» здається неправильним. Об'єднання типів містить більше значень, ніж
кожен тип окремо, а доступних полів у ньому менше. Автори пояснюють це прикладом із двома кімнатами. В одній сидять
високі люди в капелюхах, у другій люди, які говорять іспанською, теж у капелюхах. Коли людей з обох кімнат зібрали
разом, про кожного напевно відомо лише одне: він у капелюсі. Так само зі значенням типу `number | string` можна
робити лише те, що вміють і числа, і рядки.

### Type Aliases

**Псевдонім типу** (type alias) — це назва для будь-якого типу, створена словом `type`. Важлива деталь: псевдонім не
створює нового типу. Приклад із посібника, де замість `declare function` стоїть справжня функція, `alias.ts`:

```ts
type UserInputSanitizedString = string;

function sanitizeInput(str: string): UserInputSanitizedString {
  return str.trim();
}

let userInput = sanitizeInput("  <b>hi</b>  ");
userInput = "new input";
console.log(userInput);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false alias.ts
$ node alias.ts
new input
```

Назва `UserInputSanitizedString` означає «рядок, який уже очистили від небезпечного вмісту». Проте компілятор вважає
її тим самим `string`, тому без жодної помилки дозволив покласти в змінну звичайний неочищений рядок. Назва нічого не
гарантує, і рядок від неї не стає перевіреним.

### Interfaces

Це другий спосіб назвати об'єктний тип, словом `interface`. Тут автори прямо згадують **структурну типізацію**:
компілятор перевіряє лише форму значення, тобто чи є в ньому потрібні поля потрібних типів. Лекція пояснює це в
розділі «Як записують типи».

Підрозділ `Differences Between Type Aliases and Interfaces` порівнює два слова в таблиці. Головна відмінність така:
`interface` з тією самою назвою можна оголосити вдруге, і поля обох оголошень зіллються, а другий `type` з тією самою
назвою дасть помилку. Ми написали для цього короткий приклад за зразком таблиці, `merge.ts`:

```ts
interface Box {
  width: number;
}
interface Box {
  height: number;
}
const box: Box = { width: 10 };

type Card = {
  title: string;
};
type Card = {
  price: number;
};
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false merge.ts
merge.ts(7,7): error TS2741: Property 'height' is missing in type '{ width: number; }' but required in type 'Box'.
merge.ts(9,6): error TS2300: Duplicate identifier 'Card'.
merge.ts(12,6): error TS2300: Duplicate identifier 'Card'.
```

Перша помилка показує, що два оголошення `Box` злилися: тепер у ньому обов'язкові і `width`, і `height`. Друга й
третя помилки кажуть, що назву `Card` оголошено двічі.

Розширюють два слова теж по-різному. `interface` бере поля іншого типу словом `extends`, а `type` — знаком `&`. Знак
`&` означає **перетин**: значення має відповідати обом частинам одночасно. Типи з таблиці посібника, до яких ми
дописали три значення, `bear.ts`:

```ts
interface Animal {
  name: string;
}
interface Bear extends Animal {
  honey: boolean;
}

type AnimalType = {
  name: string;
};
type BearType = AnimalType & {
  honey: boolean;
};

const bear: Bear = { name: "Бурий", honey: true };
const bearToo: BearType = bear;
const noHoney: BearType = { name: "Білий" };
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false bear.ts
bear.ts(17,7): error TS2322: Type '{ name: string; }' is not assignable to type 'BearType'.
  Property 'honey' is missing in type '{ name: string; }' but required in type '{ honey: boolean; }'.
```

Значення типу `Bear` підійшло до `BearType` без помилки, бо форма в них однакова. Об'єкт без `honey` не підійшов: він
відповідає лише одній частині перетину. Автори радять типово брати `interface`, доки не знадобиться те, що вміє лише
`type`, а сторінка дня у прикладах вживає `type`. Обидва варіанти правильні.

### Type Assertions

Цей розділ пояснює `as`. Приклад із посібника — `document.getElementById("main_canvas") as HTMLCanvasElement`. Метод
`getElementById` шукає на сторінці елемент за його атрибутом `id`, і компілятор знає лише, що це буде якийсь елемент
або `null`. Ви ж знаєте, що на вашій сторінці з таким `id` стоїть полотно для малювання, `canvas`. Подивимося типи з
`as` і без нього, `canvas.ts`:

```ts
const myCanvas = document.getElementById("main_canvas") as HTMLCanvasElement;
const plain = document.getElementById("main_canvas");
const a: never = plain; // який тип без as?
const b: never = myCanvas; // який тип з as?
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false canvas.ts
canvas.ts(3,7): error TS2322: Type 'HTMLElement | null' is not assignable to type 'never'.
  Type 'null' is not assignable to type 'never'.
canvas.ts(4,7): error TS2322: Type 'HTMLCanvasElement' is not assignable to type 'never'.
```

Без `as` тип `HTMLElement | null`, а з `as` — `HTMLCanvasElement`. Отже, `as` не лише уточнив вид елемента, а й мовчки
прибрав із типу `null`. Якщо елемента з таким `id` на сторінці не виявиться, у `myCanvas` під час роботи лежатиме
`null`, а компілятор цього вже не помітить. Автори прямо попереджають: під час виконання `as` нічого не перевіряє.
Неправильне твердження не кидає винятку й не підміняє значення, тому в змінній лежить саме те, що повернув
`getElementById`. Запустити цей файл у Node не можна, бо в Node немає сторінки й об'єкта `document`. Тут перевірено
лише вивід компілятора.

Компілятор дозволяє `as` лише тоді, коли один тип є окремим випадком іншого. Запис, який перетворює рядок на число,
він відхиляє, `hellonum.ts`:

```ts
const x = "hello" as number;
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false hellonum.ts
hellonum.ts(1,11): error TS2352: Conversion of type 'string' to type 'number' may be a mistake because neither type sufficiently overlaps with the other. If this was intentional, convert the expression to 'unknown' first.
```

Повідомлення радить обхід, і посібник його теж показує: спершу перетворити на `unknown` або `any`, а потім на
потрібний тип. Запис `as unknown as T` дозволяє назвати що завгодно чим завгодно. Що з цього виходить, лекція
показує в розділі «Типові хибні уявлення» на прикладі `as-number.ts`.

Правило «окремий випадок» пропускає більше, ніж здається. Файл `assert.ts`:

```ts
type Rate = { currency: string; value: number };

const partial = { currency: "EUR" } as Rate;
const other = { title: "EUR" } as Rate;
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false assert.ts
assert.ts(4,15): error TS2352: Conversion of type '{ title: string; }' to type 'Rate' may be a mistake because neither type sufficiently overlaps with the other. If this was intentional, convert the expression to 'unknown' first.
  Type '{ title: string; }' is missing the following properties from type 'Rate': currency, value
```

Перший рядок пройшов, хоча поля `value` немає. Причина така: будь-яке значення типу `Rate` має поле `currency`, тож
`Rate` є окремим випадком типу `{ currency: string }`, і компілятор вважає перетворення можливим. Другий рядок не
пройшов, бо в типів `{ title: string }` і `Rate` немає жодного спільного поля. Отже, `as` порівнює лише типи й
відхиляє тільки очевидну нісенітницю. Завдання дня забороняє `as` у коді, щоб ви щоразу писали справжню перевірку.

### Literal Types

**Літеральний тип** дозволяє одне значення, а об'єднання літералів дозволяє кілька. Приклад із посібника,
`literal.ts`:

```ts
function printText(s: string, alignment: "left" | "right" | "center") {
  // ...
}
printText("Hello, world", "left");
printText("G'day, mate", "centre");
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false literal.ts
literal.ts(5,26): error TS2345: Argument of type '"centre"' is not assignable to parameter of type '"center" | "left" | "right"'.
```

Слово `centre` — британський запис слова «центр», і компілятор його не прийняв, бо в переліку стоїть лише `center`.
Автори також зазначають, що тип `boolean` насправді є об'єднанням двох літералів, `true | false`.

Підрозділ `Literal Inference` описує пастку, яку ви майже напевно зустрінете. Коли поле об'єкта отримує рядок,
компілятор виводить для поля тип `string`, а не літерал. Причина в тому, що поле можна змінити пізніше, і компілятор
не хоче забороняти таку зміну. Приклад із посібника, де ми замінили `declare function` справжньою функцією й дописали
спосіб `as const`, `req.ts`:

```ts
function handleRequest(url: string, method: "GET" | "POST") {
  console.log(method, url);
}

const req = { url: "https://example.com", method: "GET" };
handleRequest(req.url, req.method);

const fixed = { url: "https://example.com", method: "GET" } as const;
handleRequest(fixed.url, fixed.method);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false req.ts
req.ts(6,24): error TS2345: Argument of type 'string' is not assignable to parameter of type '"GET" | "POST"'.
$ node req.ts
GET https://example.com
GET https://example.com
```

Поле `req.method` має тип `string`, бо між створенням `req` і викликом хтось міг би записати туди, наприклад,
`"GUESS"`. Запис `as const` наприкінці об'єкта робить усі його поля незмінними й дає кожному літеральний тип, тому
другий виклик пройшов. Node обидва виклики виконав однаково, бо помилка тут лише в типах. Ось та сама пастка на
варіантах доставки з лекції, `widen.ts`:

```ts
type Delivery =
  | { stage: "packing" }
  | { stage: "onTheWay"; courier: string };

function save(delivery: Delivery) {}

const guessed = { stage: "packing" };
save(guessed);

const declared: Delivery = { stage: "packing" };
save(declared);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false widen.ts
widen.ts(8,6): error TS2345: Argument of type '{ stage: string; }' is not assignable to parameter of type 'Delivery'.
  Property 'courier' is missing in type '{ stage: string; }' but required in type '{ stage: "onTheWay"; courier: string; }'.
```

Текст помилки вводить в оману, бо говорить про кур'єра. Справжня причина стоїть у першому рядку: `stage: string`
замість літерала. Рядок із відступом з'являється тому, що компілятор шукав, до якого варіанта об'єкт підходить
найближче, і пояснив, чого бракує для варіанта з кур'єром. Анотація, як у `declared`, розв'язує проблему простіше за
`as const`: компілятор одразу звіряє об'єкт із типом `Delivery` і дає полю `stage` літеральний тип.

### `null` and `undefined`

Два підрозділи описують поведінку без `strictNullChecks` і з ним. У суворому режимі значення, яке може бути `null`,
треба перевірити перед використанням, наприклад умовою `x === null`.

Підрозділ `Non-null Assertion Operator (Postfix !)` описує знак оклику після виразу: запис `x!` прибирає `null` і
`undefined` із типу `x`, нічого не перевіряючи. Приклад із посібника, до якого ми дописали два виклики, `bang.ts`:

```ts
function liveDangerously(x?: number | null) {
  // Помилки компіляції немає
  console.log(x!.toFixed());
}

liveDangerously(4.7);
liveDangerously(null);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false bang.ts
$ node bang.ts
5
  console.log(x .toFixed());
                 ^
TypeError: Cannot read properties of null (reading 'toFixed')
```

Компілятор мовчить. Перший виклик надрукував `5`, бо `toFixed()` без аргументу округлює до цілого. Другий виклик упав.
Рядок коду, який надрукував Node, показує стирання типів наочно: на місці знака оклику стоїть пробіл. Отже, `!` — це
такий самий `as`, тобто обіцянка без перевірки, і передача `null` усе одно дає `TypeError` під час роботи.

### Enums

**Перелік** (enum) додає в код іменовані сталі. На відміну від майже всього в TypeScript, він не лише описує тип, а
й створює під час роботи справжній об'єкт. Тому Node 24 такого файла не запускає. Файл `enum.ts`:

```ts
enum Direction {
  Up,
  Down,
}

console.log(Direction.Up, Direction[0]);
```

```text
$ node enum.ts
SyntaxError [ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX]: TypeScript enum is not supported in strip-only mode
$ npx tsc --pretty false enum.ts
$ cat enum.js
"use strict";
var Direction;
(function (Direction) {
    Direction[Direction["Up"] = 0] = "Up";
    Direction[Direction["Down"] = 1] = "Down";
})(Direction || (Direction = {}));
console.log(Direction.Up, Direction[0]);
$ node enum.js
0 Up
```

Node каже, що в режимі «лише стирання» (`strip-only mode`) перелік не підтримано. Стирання вміє лише прибирати
текст, а перелік вимагає дописати новий код. Що саме треба дописати, видно з файла, який створив `tsc`: змінну
`Direction` і функцію, що заповнює її полями. Документація Node.js згадує прапорець `--experimental-transform-types`,
який дозволяє Node самому дописувати такий код, але в цьому плані він не потрібен. Для кількох варіантів беріть
об'єднання рядків, як `"left" | "right" | "center"`.

### Less Common Primitives

`bigint` описує дуже великі цілі числа, а `symbol` — унікальні мітки. У фазі 0 вони не потрібні. Просто запам'ятайте,
що такі типи є в переліку результатів `typeof`.

## Narrowing

**Де читати:** [Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html). У примірнику `typescript`
це `handbook-v2/Narrowing`.

**Що там є.** Це головний текст дня. Він перелічує всі перевірки, які розуміє компілятор, і завершується
розрізнюваними об'єднаннями. Саме поняття звуження пояснює лекція в розділі «Звуження: `if` як доказ для
компілятора», тому тут лише показано, що додає посібник.

На початку автори розбирають функцію `padLeft`. Вона приймає число або рядок: число означає, скільки пробілів
дописати ліворуч, а рядок треба дописати як є. Перша спроба, `padleft.ts`:

```ts
function padLeft(padding: number | string, input: string): string {
  return " ".repeat(padding) + input;
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false padleft.ts
padleft.ts(2,21): error TS2345: Argument of type 'string | number' is not assignable to parameter of type 'number'.
  Type 'string' is not assignable to type 'number'.
```

Метод `repeat` приймає лише число, а `padding` може виявитися рядком. Автори виправляють це перевіркою
`if (typeof padding === "number")` перед `repeat` і показують, що всередині цієї гілки `padding` уже має тип `number`.

**Якщо часу мало,** прочитайте `typeof` type guards, `The in operator narrowing`, `Discriminated unions` і
`Exhaustiveness checking`.

### `typeof` type guards

**Охоронець типу** (type guard) — це перевірка, після якої компілятор звужує тип. Автори перелічують вісім рядків, які
повертає `typeof`: `"string"`, `"number"`, `"bigint"`, `"boolean"`, `"symbol"`, `"undefined"`, `"object"`,
`"function"`. Рядка `"null"` серед них немає.

Приклад `printAll` показує ту саму пастку, що в загадці дня. Функція приймає рядок, масив рядків або `null`. Ми
дописали два виклики, `printall.ts`:

```ts
function printAll(strs: string | string[] | null) {
  if (typeof strs === "object") {
    for (const s of strs) {
      console.log(s);
    }
  } else if (typeof strs === "string") {
    console.log(strs);
  } else {
    // нічого не робимо
  }
}

printAll(["a", "b"]);
printAll(null);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false printall.ts
printall.ts(3,21): error TS18047: 'strs' is possibly 'null'.
$ node printall.ts
a
b
TypeError: strs is not iterable
```

Автори хотіли перевіркою `typeof strs === "object"` розпізнати масив, бо масив у JavaScript теж об'єкт. Але й
`typeof null` дорівнює `"object"`, тому після такої перевірки в `strs` лишається `string[] | null`, і компілятор
попереджає, що цикл може отримати `null`. Запуск підтверджує: масив надруковано, а на `null` цикл `for...of` упав.
Посібник наводить інший текст цієї помилки, `null is not iterable`. Node 24 називає в ній змінну, а не значення.

### Truthiness narrowing

Що таке **істинне значення** (truthy), пояснює лекція дня 2 в розділі «Методи з функцією: `filter`, `find`, `some`,
`map`». Посібник додає до переліку хибних значень ще одне: `0n`, нуль типу `bigint`. Перевірка
`if (strs && typeof strs === "object")` відсіює `null`, бо `null` хибне, і цей прийом часто трапляється.

Далі автори показують пастку, позначену коментарем «не робіть так». Ми запустили їхній варіант із порожнім рядком,
`emptystr.ts`:

```ts
function printAll(strs: string | string[] | null) {
  // НЕ РОБІТЬ ТАК (з посібника)
  if (strs) {
    if (typeof strs === "object") {
      for (const s of strs) {
        console.log(s);
      }
    } else if (typeof strs === "string") {
      console.log(strs);
    }
  }
}

printAll("рядок");
printAll(""); // дописано: порожній рядок
printAll(null);
console.log("кінець");
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false emptystr.ts
$ node emptystr.ts
рядок
кінець
```

Порожній рядок хибний, тому умова `if (strs)` мовчки пропустила його разом із `null`, і функція нічого не надрукувала.
Компілятор цього не бачить, бо з типами тут усе гаразд, а неправильний лише зміст. Те саме трапляється в React.
[Документація](https://react.dev/learn/conditional-rendering) попереджає: запис `{count && <span>…</span>}` при
`count`, рівному `0`, покаже на екрані нуль. Оператор `&&` повертає ліве значення, якщо воно хибне, тобто сам `0`, а
число `0` React показує. Документація радить писати ліворуч справжню умову: `count > 0 && …`.

### Equality narrowing

Перевірки `===` і `!==` теж звужують тип, і компілятор порівнює типи обох частин. Приклад із посібника, де замість
позначок `^?` стоїть прийом із `never`, `equal.ts`:

```ts
function example(x: string | number, y: string | boolean) {
  if (x === y) {
    const a: never = x; // який тип має x?
    const b: never = y; // який тип має y?
  } else {
    const c: never = x;
    const d: never = y;
  }
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false equal.ts
equal.ts(3,11): error TS2322: Type 'string' is not assignable to type 'never'.
equal.ts(4,11): error TS2322: Type 'string' is not assignable to type 'never'.
equal.ts(6,11): error TS2322: Type 'string | number' is not assignable to type 'never'.
  Type 'string' is not assignable to type 'never'.
equal.ts(7,11): error TS2322: Type 'string | boolean' is not assignable to type 'never'.
  Type 'string' is not assignable to type 'never'.
```

Якщо `x` і `y` рівні, то вони одного типу, а спільний варіант в обох лише один, `string`. Тому в першій гілці обидві
змінні мають тип `string`. У гілці `else` компілятор нічого не звузив, бо нерівні значення можуть бути будь-якими.

Там же сказано про нестрогу перевірку `!=`. Вираз `value != null` правдивий, коли значення не дорівнює ні `null`, ні
`undefined`, тому він відсіює обидва одразу. Приклад із посібника, до якого ми дописали виклики, `multiply.ts`:

```ts
interface Container {
  value: number | null | undefined;
}

function multiplyValue(container: Container, factor: number) {
  // Прибирає з типу і null, і undefined.
  if (container.value != null) {
    container.value *= factor;
    console.log(container.value);
  }
}

multiplyValue({ value: 5 }, 2);
multiplyValue({ value: null }, 2);
multiplyValue({ value: undefined }, 2);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false multiply.ts
$ node multiply.ts
10
```

Компілятор дозволив множення, бо всередині `if` у полі може бути лише число. Під час роботи гілку виконав лише перший
виклик, а `null` і `undefined` одна умова відсіяла обидва.

### The `in` operator narrowing

Що робить оператор `in` у JavaScript, пояснює лекція дня 2 в розділі «Об'єкти без мутацій». Компілятор використовує
його як охоронця: `"swim" in animal` розрізняє рибу й птаха за наявністю поля. Важлива деталь: тип із
необов'язковим полем лишається можливим в обох гілках, бо поле в такого значення може бути, а може й не бути.
Приклад із посібника з людиною, яка зі спорядженням уміє і плавати, і літати, `human.ts`:

```ts
type Fish = { swim: () => void };
type Bird = { fly: () => void };
type Human = { swim?: () => void; fly?: () => void };

function move(animal: Fish | Bird | Human) {
  if ("swim" in animal) {
    const a: never = animal; // який тип у першій гілці?
  } else {
    const b: never = animal; // який тип у другій гілці?
  }
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false human.ts
human.ts(7,11): error TS2322: Type 'Fish | Human' is not assignable to type 'never'.
  Type 'Fish' is not assignable to type 'never'.
human.ts(9,11): error TS2322: Type 'Bird | Human' is not assignable to type 'never'.
  Type 'Bird' is not assignable to type 'never'.
```

У першій гілці лишилися риба й людина, у другій — птах і людина. `Human` є в обох, бо поле `swim` у нього
необов'язкове.

Коли ліворуч від `in` стоїть тип `object`, а не об'єднання, після перевірки компілятор дописує до типу поле
невідомого типу. Лекція показує це в розділі «`any`, `unknown` і `as`: що робити з даними ззовні», у виводі файла
`rate-stages.ts`. Цього випадку посібник не розбирає, а завдання дня спирається саме на нього.

### `instanceof` narrowing

Що таке клас і що питає `instanceof`, пояснює лекція дня 1 у розділі «Що роблять три крапки», в абзаці про методи
класу. Компілятор теж вважає `instanceof` охоронцем. Приклад із посібника, до якого ми дописали виклики,
`logvalue.ts`:

```ts
function logValue(x: Date | string) {
  if (x instanceof Date) {
    console.log(x.toUTCString());
  } else {
    console.log(x.toUpperCase());
  }
}

logValue(new Date(0));
logValue("hello");
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false logvalue.ts
$ node logvalue.ts
Thu, 01 Jan 1970 00:00:00 GMT
HELLO
```

У першій гілці компілятор дозволив метод дати, у другій метод рядка. Праворуч від `instanceof` мусить стояти клас,
тобто щось, що існує під час роботи програми. Назва, оголошена словом `type`, не підходить, бо її стирають. Лекція
показує цю помилку в розділі «Типові хибні уявлення», на прикладі `instanceof.ts`.

### Assignments

Коли змінній присвоюють значення, компілятор звужує її тип за правою частиною. Але дозволене присвоєння він звіряє з
**оголошеним типом**, тобто з тим, який змінна отримала при створенні. Приклад із посібника, `assign.ts`:

```ts
let x = Math.random() < 0.5 ? 10 : "hello world!";
x = 1;
x = "goodbye!";
x = true;
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false assign.ts
assign.ts(4,1): error TS2322: Type 'boolean' is not assignable to type 'string | number'.
```

Перший рядок дає змінній оголошений тип `string | number`, бо права частина може бути і числом, і рядком. Після
`x = 1` компілятор вважає `x` числом, проте рядок `x = "goodbye!"` теж законний, бо рядок входить в оголошений тип.
Лише `true` туди не входить, і компілятор назвав саме оголошений тип.

### Control flow analysis

**Аналіз потоку керування** означає, що компілятор проходить гілки коду й обчислює тип змінної в кожній точці. Перший
приклад розділу знову `padLeft`: після `if`, який завершився через `return`, варіант `number` уже неможливий. Як
компілятор міркує в такому випадку, крок за кроком пояснює лекція на прикладі `discount.ts`, у розділі «Звуження:
`if` як доказ для компілятора».

Другий приклад показує, що буває, коли гілки знову сходяться. Ми замінили позначки `^?` прийомом із `never`,
`flow.ts`:

```ts
function example() {
  let x: string | number | boolean;
  x = Math.random() < 0.5;
  const a: never = x; // після першого присвоєння
  if (Math.random() < 0.5) {
    x = "hello";
    const b: never = x; // у гілці if
  } else {
    x = 100;
    const c: never = x; // у гілці else
  }
  const d: never = x; // після злиття гілок
  return x;
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false flow.ts
flow.ts(4,9): error TS2322: Type 'boolean' is not assignable to type 'never'.
flow.ts(7,11): error TS2322: Type 'string' is not assignable to type 'never'.
flow.ts(10,11): error TS2322: Type 'number' is not assignable to type 'never'.
flow.ts(12,9): error TS2322: Type 'string | number' is not assignable to type 'never'.
  Type 'string' is not assignable to type 'never'.
```

Після злиття гілок тип став об'єднанням того, що лишилося в кожній гілці: `string | number`. Варіанта `boolean` там
уже немає, бо обидві гілки записали в `x` нове значення.

### Using type predicates

Функція може сама бути перевіркою, якщо її тип результату записано як `pet is Fish`. Такий запис називається
**предикатом типу** і означає: «якщо функція повернула `true`, то `pet` є `Fish`». Приклад із посібника, де замість
`declare function getSmallPet` стоїть масив із двох тварин, `fish.ts`:

```ts
type Fish = { swim: () => void; name: string };
type Bird = { fly: () => void; name: string };

function isFish(pet: Fish | Bird): pet is Fish {
  return (pet as Fish).swim !== undefined;
}

const zoo: (Fish | Bird)[] = [
  { name: "Немо", swim: () => {} },
  { name: "Кеша", fly: () => {} },
];
const underWater: Fish[] = zoo.filter(isFish);
console.log(underWater.map((pet) => pet.name));

for (const pet of zoo) {
  if (isFish(pet)) {
    pet.swim();
    console.log(pet.name, "пливе");
  } else {
    pet.fly();
    console.log(pet.name, "летить");
  }
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false fish.ts
$ node fish.ts
[ 'Немо' ]
Немо пливе
Кеша летить
```

Після `if (isFish(pet))` компілятор дозволив `pet.swim()`, а в гілці `else` дозволив `pet.fly()`, бо зрозумів, що там
лишився птах. Виклик `zoo.filter(isFish)` дав масив типу `Fish[]`. Зверніть увагу: усередині `isFish` самі автори
пишуть `as Fish`, бо інакше прочитати `swim` у значення типу `Fish | Bird` не можна.

Тіло такої функції компілятор не звіряє з обіцянкою. Це та сама небезпека, що в `as`. Файл `predicate.ts`:

```ts
function isRate(x: unknown): x is { value: number } {
  return true;
}

const text: unknown = "рядок";
if (isRate(text)) {
  console.log(text.value.toFixed(2));
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false predicate.ts
$ node predicate.ts
TypeError: Cannot read properties of undefined (reading 'toFixed')
```

Функція завжди повертає `true`, і компілятор повірив, що в рядку є поле `value` з числом. Під час роботи
`text.value` дало `undefined`, і виклик `toFixed` упав.

### Assertion functions

Це одне речення з посиланням на примітки до версії 3.7. **Функція-твердження** (assertion function) кидає помилку,
якщо умова не виконалась, а після її виклику компілятор вважає тип звуженим. Сьогодні такі функції не потрібні.

### Discriminated unions

Тут автори проходять той самий шлях, що й лекція в розділі «Розрізнюване об'єднання: варіанти зі спільним полем»,
але на фігурах. Спершу вони описують фігуру одним інтерфейсом `Shape` з полем `kind` і необов'язковими `radius` та
`sideLength`. Дві спроби з посібника в одному файлі, `shape-loose.ts`:

```ts
interface Shape {
  kind: "circle" | "square";
  radius?: number;
  sideLength?: number;
}

function handleShape(shape: Shape) {
  if (shape.kind === "rect") {
    // ...
  }
}

function getArea(shape: Shape) {
  if (shape.kind === "circle") {
    return Math.PI * shape.radius ** 2;
  }
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false shape-loose.ts
shape-loose.ts(8,7): error TS2367: This comparison appears to be unintentional because the types '"circle" | "square"' and '"rect"' have no overlap.
shape-loose.ts(15,22): error TS18048: 'shape.radius' is possibly 'undefined'.
```

Перша помилка показує користь літералів у полі `kind`: описку `"rect"` компілятор помітив. Друга помилка показує
ваду цього опису: навіть після перевірки `kind` компілятор не знає, що в кола обов'язково є радіус. Знак оклику
`shape.radius!` прибирає цю помилку, але автори називають такий код крихким: якщо код пересунуть, обіцянка може
стати хибною, і ніхто цього не помітить.

Потім автори розділяють `Circle` і `Square` з різними літералами в `kind` і об'єднують їх у `type Shape`. Ми додали
виклик, щоб запустити файл, `shape.ts`:

```ts
interface Circle {
  kind: "circle";
  radius: number;
}
interface Square {
  kind: "square";
  sideLength: number;
}
type Shape = Circle | Square;

function areaWithoutCheck(shape: Shape) {
  return Math.PI * shape.radius ** 2;
}

function getArea(shape: Shape) {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.sideLength ** 2;
  }
}

console.log(getArea({ kind: "square", sideLength: 3 }));
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false shape.ts
shape.ts(12,26): error TS2339: Property 'radius' does not exist on type 'Shape'.
  Property 'radius' does not exist on type 'Square'.
$ node shape.ts
9
```

Без перевірки читати `radius` усе одно не можна, бо фігура може виявитися квадратом. Але тепер помилка інша: не
«може бути `undefined`», а «у квадрата такого поля немає». Усередині `case "circle"` компілятор вибрав варіант
`Circle`, і `radius` там обов'язковий, тому функція `getArea` пройшла без помилок і без знаків оклику. Автори
зазначають, що цей прийом добре підходить для повідомлень, які програма отримує мережею, і для змін стану. Стан
запиту в React саме такий: «завантажується», «готово з даними», «помилка з текстом».

### The `never` type

Коли звуження прибирає всі варіанти, лишається тип `never`. Він означає стан, якого не має бути.

### Exhaustiveness checking

Слово **exhaustive** означає «вичерпний», тобто такий, що охоплює всі варіанти. Автори нагадують два правила про
`never`. Значення типу `never` можна покласти в змінну будь-якого типу, бо такого значення ніколи не буває. А в змінну
типу `never` не можна покласти нічого, крім `never`. На цьому побудовано прийом із гілкою `default` і рядком
`const _exhaustiveCheck: never = shape`. Автори додають третю фігуру, `Triangle`, яку `switch` не обробляє,
`triangle.ts`:

```ts
interface Circle {
  kind: "circle";
  radius: number;
}
interface Square {
  kind: "square";
  sideLength: number;
}
interface Triangle {
  kind: "triangle";
  sideLength: number;
}
type Shape = Circle | Square | Triangle;

function getArea(shape: Shape) {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.sideLength ** 2;
    default:
      const _exhaustiveCheck: never = shape;
      return _exhaustiveCheck;
  }
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false triangle.ts
triangle.ts(22,13): error TS2322: Type 'Triangle' is not assignable to type 'never'.
```

У гілку `default` дійшов трикутник, якого не обробив жоден `case`, і компілятор назвав його в повідомленні. Лекція
показує той самий прийом на доставці, у файлі `delivery-never.ts`. У завданні `renderState` гілки `default` немає:
там повноту перевіряє сам `switch` разом із типом результату. Якщо пропустити варіант, функція на одному зі шляхів
нічого не поверне, і компілятор скаже `Function lacks ending return statement`, як у лекційному файлі
`delivery-errors.ts`.

## How to Design Programs: 3.1 Designing Functions

**Де читати:** [розділ 3.1 книжки](https://htdp.org/2024-11-6/Book/part_one.html#%28part._sec~3adesign-func%29). У
примірнику `htdp` це розділ `3.1 Designing Functions`.

**Що там є.** Цю книжку написали Маттіас Феллайзен, Роберт Фіндлер, Метью Флетт і Шрірам Крішнамурті. Вона вчить
проєктувати програми за чітким рецептом на прикладах мови BSL, навчального варіанта мови Racket, тому код виглядає
незвично: дужки стоять перед назвою функції. Читати її синтаксис докладно не треба. Сьогодні потрібна сама
послідовність кроків, бо за нею побудовано всю практику дня. Текст книжки тут лише коротко переказано.

**Якщо часу мало,** прочитайте підрозділ `The Design Process` і пропустіть вправи.

### Information and Data

Автори розрізняють **інформацію** зі світу й **дані** в програмі. Програма перекладає факти в дані, обробляє їх і
перекладає результат назад. Те саме число 42 може означати температуру чи кількість символів, і лише програміст
вирішує, що саме. Тому вони пишуть **означення даних**: коментар, який дає назву класу значень і пояснює, що це
значення означає.

### The Design Process

Рецепт має шість кроків. Функція-приклад обчислює площу квадрата за довжиною сторони (`area-of-square`). Таблиця
нижче коротко показує, чим кожен крок став у TypeScript.

| Крок книжки | Що ви робите | Де це в завданні дня |
|-------------|--------------|----------------------|
| Подати інформацію як дані | написати означення даних | типи у `data.ts`, наприклад `UserState` |
| Сигнатура, призначення, заголовок | записати, що функція приймає й повертає, одним реченням сказати навіщо вона, написати заглушку | сигнатура стала частиною коду, а заглушка лежить у файлі готовою |
| Приклади | вирахувати очікувані результати до написання тіла | `types.test.ts` і рядки `@ts-expect-error` |
| Перелік вхідних даних | виписати, що є в розпорядженні функції | коментар у тілі функції |
| Код | замінити заглушку виразом | тіла `toUser` і `renderState` |
| Перевірка | запустити приклади | `tsc`, `node --test`, `node index.ts` |

Автори радять, якщо приклад не пройшов, спершу перевірити сам приклад, а вже потім код. Головна думка розділу така:
сигнатура й призначення дозволяють зрозуміти функцію, не читаючи тіла. У книжці сигнатура є лише коментарем, і її
ніхто не перевіряє. У TypeScript та сама сигнатура стоїть у заголовку функції, і `tsc` перевіряє її під час
компіляції.

## How to Design Programs: 4.5 Itemizations

**Де читати:** [розділ 4.5
книжки](https://htdp.org/2024-11-6/Book/part_one.html#%28part._itemization._sec~3aitemization%29). У примірнику `htdp`
це `4.5 Itemizations`.

**Що там є.** Розділ завершує тему даних із кількома варіантами. Попередні розділи описали **перелічення**, тобто
кілька конкретних значень, та **інтервали**, тобто проміжки чисел. Слово **itemization** означає «перелік варіантів»,
і він дозволяє поєднувати те й інше: в одному рядку цілий клас значень, в іншому одне значення. Розділ невеликий, тому
читайте його цілком.

### `NorF` and `add3`

Функція `string->number` повертає число або `#false`, якщо рядок не вдалося перетворити. Автори дають такому
результату назву `NorF`. У TypeScript той самий тип записують як `number | false`. Функція `add3`, яка приймає `NorF`,
містить умову з однією гілкою на кожен варіант. Це головне правило розділу: кількість гілок у функції повторює
кількість варіантів у типі.

### `LR` and `LRCD`

Це стан ракети: вона або стоїть на землі, або летить на певній висоті. Потім автори додають третій варіант, зворотний
відлік перед стартом, і позначають його від'ємними числами від -3 до -1. Коли з'являється новий варіант, змінюється
кожна функція, яка обробляє цей тип.

Порівняйте це зі станом запиту з завдання дня. Книжка розрізняє варіанти за самим значенням, а TypeScript дозволяє
додати до кожного варіанта поле-розрізнювач. Правило лишається те саме: одна гілка на варіант. Компілятор TypeScript
ще й нагадає про забуту гілку, як у прикладі з трикутником вище, а мова книжки такої перевірки не має.

## Як читати посилання на стандарт ECMAScript

Сторінка дня посилається на стандарт ECMA-262, щоб підтвердити результат `typeof null`. Цього тексту немає в списку
читання, але корисно знати, як знайти таке місце. Стандарт описує оператори не прозою, а покроковими алгоритмами:
кожен крок каже, що обчислити, а крок зі словом `return` повертає результат і завершує алгоритм.

Відкрийте [розділ 13.5.3 The typeof
Operator](https://tc39.es/ecma262/multipage/ecmascript-language-expressions.html#sec-typeof-operator). Підрозділ
`13.5.3.1 Runtime Semantics: Evaluation` описує, що відбувається під час виконання. Алгоритм спершу обчислює вираз
праворуч від `typeof`, а потім перевіряє отримане значення по черзі: чи це `undefined`, чи `null`, чи рядок, символ,
логічне значення, число або `bigint`. Для `null` окремий крок прямо повертає `"object"`, і далі алгоритм не йде. Для
об'єкта наприкінці є ще одна перевірка: якщо об'єкт можна викликати, результат `"function"`, інакше `"object"`. Один
необов'язковий крок стосується особливого старого об'єкта браузера, і його можна пропустити. Так видно, що
`typeof null` дорівнює `"object"` не через випадкову помилку браузера, а тому, що цього вимагає стандарт.

## Запитання для самоперевірки

**1. Посібник каже, що типова ціль компіляції дорівнює ES5 і що типовий режим м'який. Як воно в TypeScript 7.0?**

<details><summary>Відповідь</summary>

Типова ціль дорівнює найновішій версії стандарту, зараз це `es2025`. Ціль `es5` прибрано зовсім, і `--target es5`
дає помилку `TS5108` про те, що налаштування видалено. Суворий режим увімкнено типово, тому без жодного прапорця
параметр без типу дає `TS7006`. Сторінка дня пише `--strict` явно, щоб із команди було видно, які перевірки
ввімкнено.

</details>

**2. Що означає правило з розділу `Erased Types` і який висновок із нього для відповіді сервера?**

<details><summary>Відповідь</summary>

Анотації ніколи не змінюють поведінку програми під час виконання, бо компілятор і Node їх просто видаляють. Тому
анотація чи `as` на відповіді сервера нічого не перевіряє, і перевірка мусить бути звичайним кодом JavaScript.

</details>

**3. Чому `type Sanitized = string` не захищає від неочищеного рядка?**

<details><summary>Відповідь</summary>

Псевдонім лише дає назву наявному типу. Компілятор вважає його тим самим `string`, тому прийме будь-який рядок. Нової
перевірки назва не створює.

</details>

**4. Чому в прикладі `Shape` після перевірки `kind` компілятор не дозволив читати `radius` у першому варіанті опису й
дозволив у другому?**

<details><summary>Відповідь</summary>

У першому варіанті один тип містив необов'язкові поля, і компілятор не знав зв'язку між `kind` і `radius`. У другому
кожен варіант має власний літерал у `kind`, тому перевірка цього поля вибирає один варіант, а в ньому `radius`
обов'язковий.

</details>

**5. Що спільного в `as`, у знака `!` і в предиката `pet is Fish` з неправильним тілом?**

<details><summary>Відповідь</summary>

Усі троє змушують компілятор повірити без перевірки. Якщо обіцянка хибна, помилка виникне під час роботи програми.
Справжній доказ дає лише код, який виконується й перевіряє значення.

</details>

**6. Яке правило спільне для розділу книжки про перелік варіантів і для `switch` за полем `status`?**

<details><summary>Відповідь</summary>

Одна гілка на кожен варіант даних. Форма функції повторює форму даних. Коли з'являється новий варіант, треба додати
гілку в кожній функції, яка обробляє цей тип, а компілятор TypeScript знайде забуті місця.

</details>
