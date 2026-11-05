# Лекція. День 10. TypeScript: дженерики

Ця лекція пояснює, як написати одну функцію чи один тип для багатьох типів даних, не втрачаючи перевірки. Вона
спирається на вчорашню лекцію: типи, об'єднання, звуження, `unknown` і `as`. Читання займе близько 30 хвилин. Вивід
кожної команди наведено таким, яким він був насправді.

**Після лекції ви зможете пояснити:**

- яку проблему розв'язує параметр типу і чому кажуть, що він зв'язує вхід із виходом;
- як компілятор добирає параметр типу і коли його треба вказати самому;
- що роблять обмеження `extends`, оператор `keyof` і запис `T[K]`;
- як `Partial`, `Pick`, `Omit` і `Record` будують нові типи зі старих і де вони мовчки підводять;
- коли дженерик не потрібен і чому функція `parse<T>` нічого не гарантує;
- чому `useState(null)` у React не приймає нічого, крім `null`.

## Проблема: одна дія, багато типів

У магазині часто потрібен останній елемент списку: остання ціна, остання назва товару, останнє замовлення. Дія завжди
однакова, а тип елементів різний. Спробуємо записати це тим, що вже знаємо.

Файл `last-bad.ts`:

```ts
function lastNumber(list: number[]): number | undefined {
  return list[list.length - 1];
}
function lastAny(list: any[]): any {
  return list[list.length - 1];
}
function lastUnknown(list: unknown[]): unknown {
  return list[list.length - 1];
}

const a = lastNumber(["Чай"]);

const b = lastAny(["Чай"]);
console.log(b.toFixed(2));

const c = lastUnknown(["Чай"]);
console.log(c.toUpperCase());
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false last-bad.ts
last-bad.ts(11,23): error TS2322: Type 'string' is not assignable to type 'number'.
last-bad.ts(17,13): error TS18046: 'c' is of type 'unknown'.
```

Такий вивід команда дає в теці, де немає файла `tsconfig.json`. Це файл, у якому проєкт зберігає налаштування
компілятора TypeScript. Якщо такий файл лежить у вашій теці або в теці над нею, TypeScript 6.0 не перевіряє
`last-bad.ts`, а друкує одну помилку:

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false last-bad.ts
error TS5112: tsconfig.json is present but will not be loaded if files are specified on commandline. Use '--ignoreConfig' to skip this error.
```

Помилка `TS5112` каже таке. Файл названо просто в команді, тому компілятор не візьме налаштувань із `tsconfig.json`.
Компілятор вимагає, щоб ви це підтвердили. Для цього додайте до команди прапорець `--ignoreConfig`:

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false --ignoreConfig last-bad.ts
last-bad.ts(11,23): error TS2322: Type 'string' is not assignable to type 'number'.
last-bad.ts(17,13): error TS18046: 'c' is of type 'unknown'.
```

З прапорцем `--ignoreConfig` компілятор бере налаштування лише з прапорців команди. Вивід тоді той самий, що й у теці
без `tsconfig.json`. Якщо `tsconfig.json` у вас є, додавайте цей прапорець до кожної команди цієї лекції.

Тепер повернімося до трьох функцій. Кожен спосіб має свою ваду:

| Спосіб | Що добре | Що погано |
|--------|----------|-----------|
| `lastNumber` | результат точно число | для рядків доведеться написати другу таку саму функцію |
| `lastAny` | приймає все | перевірку вимкнено: `b.toFixed(2)` пройшов компілятор і впаде під час роботи |
| `lastUnknown` | приймає все й нічого не обіцяє | у масиві були рядки, а на виході компілятор цього вже не знає |

Бракує способу сказати: «тип результату такий самий, як тип елементів, які мені дали, хоч би яким він був».

## Параметр типу

Для цього існує **параметр типу**. Звичайний параметр функції стоїть замість значення, яке передадуть під час виклику.
Параметр типу стоїть замість типу, який компілятор підставить для кожного виклику. Функції й типи з таким параметром
називають **дженериками** (generics, узагальнені типи).

Файл `last.ts`:

```ts
function last<T>(list: T[]): T | undefined {
  return list[list.length - 1];
}

const price = last([80, 150, 42]);
const word = last(["Чай", "Кава"]);

console.log(price?.toFixed(2));
console.log(word?.toUpperCase());
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false last.ts
(tsc нічого не надрукував: помилок немає)
$ node last.ts
42.00
КАВА
```

Рядок за рядком:

- `<T>` після назви функції оголошує параметр типу. Назва довільна. Часто пишуть одну літеру, а посібник TypeScript
  пише `Type`.
- `list: T[]` каже, що параметр є масивом елементів типу `T`.
- `: T | undefined` каже, що результат має той самий тип `T`, а масив може бути порожнім.
- `last([80, 150, 42])`: компілятор бачить масив чисел і підставляє `T = number`. Тому `price` має тип `number |
  undefined`, і метод `toFixed` дозволено.
- `last(["Чай", "Кава"])`: той самий код, але тепер `T = string`. Рядок `word?.toFixed(2)` компілятор відхилив би.

Запис `T` зустрічається і у вході, і у виході. Саме це мають на увазі, коли кажуть, що параметр типу **зв'язує вхід із
виходом**. Без цього зв'язку параметр нічого не дає, і до цього ми ще повернемося.

Як і решта типів, `T` існує лише для компілятора. Під час запуску `node` викидає `<T>` і виконує одну звичайну
функцію. Окремих версій для чисел і рядків не створюється, тому під час роботи `T` дізнатися неможливо.

## Як компілятор добирає `T`

Зазвичай `T` не пишуть, бо компілятор визначає його з аргументів. Ось що він робить у різних випадках. Файл навмисно
містить помилки, щоб побачити результат.

Файл `infer.ts`:

```ts
function last<T>(list: T[]): T | undefined { return list[list.length - 1]; }
function same<T>(a: T, b: T): T[] { return [a, b]; }
function box<T>(value: T) { return { value }; }
function empty<T>(): T[] { return []; }

const mixed: number = last([1, "два"]);
const pair = same(1, "два");
const pairOk = same<number | string>(1, "два");

const none: string = last([]);
const unknownList: string = empty();

let nothing = box(null);
nothing = box(5);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false infer.ts
infer.ts(6,7): error TS2322: Type 'string | number | undefined' is not assignable to type 'number'.
  Type 'undefined' is not assignable to type 'number'.
infer.ts(7,22): error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
infer.ts(10,7): error TS2322: Type 'undefined' is not assignable to type 'string'.
infer.ts(11,7): error TS2322: Type 'unknown[]' is not assignable to type 'string'.
infer.ts(14,1): error TS2322: Type '{ value: number; }' is not assignable to type '{ value: null; }'.
  Types of property 'value' are incompatible.
    Type 'number' is not assignable to type 'null'.
```

| Виклик | Яким став `T` | Чому |
|--------|---------------|------|
| `last([1, "два"])` | `string \| number` | масив уже має елементи такого типу, і `T` дорівнює типу елемента |
| `same(1, "два")` | `number`, і другий аргумент не підходить | кожен аргумент дає кандидата, і об'єднання компілятор сам не будує |
| `same<number \| string>(1, "два")` | `number \| string` | тип вказано явно в кутових дужках |
| `last([])` | `never` | у порожньому масиві елементів немає, тому результат дорівнює просто `undefined` |
| `empty()` | `unknown` | аргументів немає, тому `T` нема звідки взяти |
| `box(null)` | `null` | компілятор бере те, що бачить, і не знає ваших намірів |

Останній рядок таблиці найважливіший для React. Значення `null` часто означає «поки що нічого», а згодом там з'явиться
об'єкт. Компілятор цього передбачити не може, тому такий випадок вимагає явного запису: `box<Product | null>(null)`.

**Вказувати `T` треба для всіх параметрів одразу.** Якщо параметрів типу два, а в дужках указано один, компілятор
відповість `Expected 2 type arguments, but got 1`. Часткового виведення немає. Перевіримо це на функції з двома
параметрами типу.

Файл `partial-args.ts`:

```ts
function pair<A, B>(a: A, b: B): [A, B] {
  return [a, b];
}

// Указано лише A, а B компілятор мав би добрати сам.
const wrong = pair<number>(1, "два");
// Указано обидва параметри, тому помилки немає.
const right = pair<number, string>(1, "два");
// Не вказано жодного, тому компілятор добирає обидва.
const inferred = pair(1, "два");
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false partial-args.ts
partial-args.ts(6,20): error TS2558: Expected 2 type arguments, but got 1.
```

Компілятор поскаржився лише на рядок зі змінною `wrong`, бо там указано один параметр із двох. На практиці є два
робочі записи: або вкажіть усі параметри, або не вказуйте жодного й дайте компілятору добрати їх з аргументів.

## Обмеження: `extends`

Усередині функції `T` може виявитися будь-чим, тому компілятор дозволяє лише те, що законно для будь-якого типу.
Припустімо, що треба вибрати з двох значень довше.

Файл `longer.ts`:

```ts
function size<T>(value: T): number {
  return value.length;
}

function longer<T extends { length: number }>(a: T, b: T): T {
  return a.length >= b.length ? a : b;
}

const text: string = longer("чай", "кава");
const list: number[] = longer([1, 2], [3]);
longer(5, 6);

function longerPlain(a: { length: number }, b: { length: number }) {
  return a.length >= b.length ? a : b;
}
longerPlain("чай", "кава").toUpperCase();
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false longer.ts
longer.ts(2,16): error TS2339: Property 'length' does not exist on type 'T'.
longer.ts(11,8): error TS2345: Argument of type 'number' is not assignable to parameter of type '{ length: number; }'.
longer.ts(16,28): error TS2339: Property 'toUpperCase' does not exist on type '{ length: number; }'.
```

Запис `T extends { length: number }` називається **обмеженням**. Він каже, що `T` може бути будь-яким типом, у якому є
числове поле `length`. Слово `extends` тут не має стосунку до наслідування класів. Тут воно означає «підходить під
такий опис».

Обмеження дає дві речі. Усередині функції стало законним `a.length`. Під час виклику компілятор відхиляє числа.
Останній приклад показує, чому не можна просто написати тип параметра `{ length: number }`: результат такої функції
знає лише про `length`, і `toUpperCase` уже недоступний. Обмеження перевіряє тип, але не забуває його: `longer("чай",
"кава")` повертає рядок.

## `keyof` і `T[K]`: доступ за назвою поля

Тепер припустімо, що треба витягти один стовпець зі списку товарів: усі ціни або всі назви. Для цього потрібні два
оператори типів.

**`keyof`** бере об'єктний тип і дає об'єднання назв його полів. Для `type Product = { id: number; name: string;
price: number }` запис `keyof Product` означає `"id" | "name" | "price"`.

**`T[K]`** означає тип поля `K` в типі `T`. Цей запис називають **індексованим доступом**. `Product["price"]` дорівнює
`number`, а `Product["name"]` дорівнює `string`.

Файл `pluck.ts`:

```ts
type Product = { id: number; name: string; price: number };

function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  return items.map((item) => item[key]);
}

const shelf: Product[] = [
  { id: 1, name: "Чай", price: 80 },
  { id: 2, name: "Кава", price: 150 },
];

const prices = pluck(shelf, "price");
const names = pluck(shelf, "name");
console.log(prices, names);
console.log(prices.reduce((sum, price) => sum + price, 0));
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false pluck.ts
(tsc нічого не надрукував: помилок немає)
$ node pluck.ts
[ 80, 150 ] [ 'Чай', 'Кава' ]
230
```

Простежимо, як компілятор обробляє виклик `pluck(shelf, "price")`:

| Крок | Що бачить компілятор | Висновок |
|------|----------------------|----------|
| перший аргумент | `shelf` має тип `Product[]`, а параметр має тип `T[]` | `T = Product` |
| обмеження | `K extends keyof T` | `K` може бути лише `"id"`, `"name"` або `"price"` |
| другий аргумент | рядок `"price"` | `K = "price"`, він підходить під обмеження |
| тип результату | `T[K][]` | `Product["price"][]`, тобто `number[]` |
| наступний рядок | `prices.reduce` | компілятор знає, що `sum` і `price` є числами |

Файл нижче показує, що цей опис забороняє.

Файл `pluck-errors.ts`:

```ts
type Product = { id: number; name: string; price: number };

function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  return items.map((item) => item[key]);
}
function pluckLoose<T>(items: T[], key: keyof T) {
  return items.map((item) => item[key]);
}

const shelf: Product[] = [{ id: 1, name: "Чай", price: 80 }];

pluck(shelf, "prise");
const wrong: string[] = pluck(shelf, "price");
const loose: number[] = pluckLoose(shelf, "price");

for (const key of Object.keys(shelf[0])) {
  console.log(shelf[0][key]);
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false pluck-errors.ts
pluck-errors.ts(12,14): error TS2345: Argument of type '"prise"' is not assignable to parameter of type 'keyof Product'.
pluck-errors.ts(13,7): error TS2322: Type 'number[]' is not assignable to type 'string[]'.
  Type 'number' is not assignable to type 'string'.
pluck-errors.ts(14,7): error TS2322: Type '(string | number)[]' is not assignable to type 'number[]'.
  Type 'string | number' is not assignable to type 'number'.
    Type 'string' is not assignable to type 'number'.
pluck-errors.ts(17,15): error TS7053: Element implicitly has an 'any' type because expression of type 'string' can't be used to index type 'Product'.
  No index signature with a parameter of type 'string' was found on type 'Product'.
```

Перші два повідомлення очікувані: описку в назві поля зупинено, а тип результату точний. Два інші варто розібрати.

**Навіщо окремий параметр `K`.** Функція `pluckLoose` обходиться без нього, і `key: keyof T` теж не пропустить описку.
Проте результат втратив зв'язок із конкретним полем: компілятор знає лише, що це значення якогось поля, тобто `string | number`.
Саме параметр `K` запам'ятовує, яке поле передали.

**Чому `Object.keys` дає помилку.** Цей метод повертає `string[]`, а не `(keyof T)[]`. Причина у структурній типізації
з учорашньої лекції: у значення можуть бути поля, не описані в типі, тому твердження «тут лише ці ключі» було б
неправдою.

## Узагальнені типи

Параметр типу може мати не лише функція, а й тип. Ви вже користуєтеся такими типами: `number[]` є скороченням для
`Array<number>`, а `Promise<string>` означає проміс, який дасть рядок. Опишемо стек дій для кнопки «Скасувати»:
останнє додане забирають першим.

Файл `stack.ts`:

```ts
interface Stack<T> {
  push(item: T): void;
  pop(): T | undefined;
  size(): number;
}

function createStack<T>(): Stack<T> {
  const items: T[] = [];
  return {
    push(item) { items.push(item); },
    pop() { return items.pop(); },
    size() { return items.length; },
  };
}

const undo = createStack<string>();
undo.push("Додано товар");
undo.push("Змінено ціну");
console.log(undo.pop(), undo.size());
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false stack.ts
(tsc нічого не надрукував: помилок немає)
$ node stack.ts
Змінено ціну 1
```

Рядок за рядком:

- `interface Stack<T>` оголошує параметр на всьому типі, тому всі методи говорять про той самий `T`. Написати `Stack`
  без аргументу не можна: компілятор відповість `Generic type 'Stack<T>' requires 1 type argument(s)`.
- `createStack<T>(): Stack<T>` не має аргументів, тому `T` тут нема звідки вивести. Тому виклик пише
  `createStack<string>()` явно. Без цього вийшов би `Stack<unknown>`.
- Об'єкт із методами не повторює типів `item`, бо компілятор бере їх з `Stack<T>`, указаного як тип результату.
- Вивід `Змінено ціну 1` містить два значення: `undo.pop()` забрав і повернув останній доданий запис, а `undo.size()`
  після цього показав, що в стеку лишився один запис.

Перевірмо дві помилки, про які щойно йшлося. Допишіть у кінець файлу `stack.ts` такі рядки:

```ts
// Тип Stack записано без аргументу.
const noArgument: Stack = createStack<string>();

// Виклик без кутових дужок: аргументів немає, тому T нема звідки взяти.
const noType = createStack();
const item: string | undefined = noType.pop();
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false stack.ts
stack.ts(21,19): error TS2314: Generic type 'Stack<T>' requires 1 type argument(s).
stack.ts(25,7): error TS2322: Type 'unknown' is not assignable to type 'string | undefined'.
```

Перше повідомлення стосується запису `Stack` без аргументу. Друге показує, що `noType.pop()` повертає `unknown`, тобто
компілятор підставив `T = unknown`. Отже, коли функція не має аргументів, з яких можна вивести `T`, пишіть тип у
кутових дужках самі. Інакше результат доведеться перевіряти перед кожним вживанням.

Параметр можна поставити й в об'єднанні з учорашньої лекції. Запис `type Loaded<T> = { status: "ok"; value: T } | {
status: "fail"; reason: string }` описує результат будь-якого завантаження, а `Loaded<number>` і `Loaded<Product[]>`
підставляють конкретний тип.

## Службові типи

TypeScript має вбудовані дженерики, які будують новий тип зі старого. Їх називають **службовими типами** (utility
types). Візьмемо товар.

```text
Product = { id: number; name: string; price: number; description: string }
```

| Запис | Що вийде | Для чого |
|-------|----------|----------|
| `Partial<Product>` | усі поля необов'язкові | часткове оновлення |
| `Readonly<Product>` | поля не можна переприсвоїти | значення, яке не можна змінювати |
| `Pick<Product, "name" \| "price">` | лише `name` і `price` | картка товару |
| `Omit<Product, "id">` | усі поля, крім `id` | новий товар, якому сервер ще не дав `id` |
| `Record<"low" \| "high", string>` | об'єкт із ключами `low` і `high`, значення рядки | таблиця підписів |

Їх можна вкладати, і читати такий запис треба зсередини назовні. `Partial<Pick<Product, "name" | "price">>` спершу
лишає два поля, а потім робить їх необов'язковими.

Усередині це звичайні дженерики. `Partial` оголошено у вбудованому файлі `lib.es5.d.ts` так: `type Partial<T> = { [P
in keyof T]?: T[P] }`. Читається це так: для кожного ключа `P` з `keyof T` створити необов'язкове поле типу `T[P]`.
Усе в цьому записі ви вже знаєте, крім циклу `in`, який називається зіставленим типом (mapped type).

Службові типи мають чотири тихі пастки. Перевіримо їх.

Файл `traps.ts`:

```ts
type Product = { id: number; name: string; price: number };

const typoOmit: Omit<Product, "prise"> = { id: 1, name: "Чай", price: 80 };
const typoPick: Pick<Product, "prise"> = { prise: 1 };

const tea: Product = { id: 1, name: "Чай", price: 80 };
const patch: Partial<Product> = { price: undefined };
const updated: Product = { ...tea, ...patch };
console.log(updated.price);

const prices: Record<string, number> = { tea: 80 };
const coffee: number = prices.coffee;
console.log(coffee);

const frozen: Readonly<Product> = { ...tea };
frozen.price = 100;
console.log(frozen.price);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false traps.ts
traps.ts(4,31): error TS2344: Type '"prise"' does not satisfy the constraint 'keyof Product'.
traps.ts(16,8): error TS2540: Cannot assign to 'price' because it is a read-only property.
$ node traps.ts
undefined
undefined
100
```

- `Omit` не перевіряє назв. Його другий параметр обмежено будь-яким ключем, а не `keyof T`, тому описка `"prise"` у
  третьому рядку пройшла й нічого не прибрала. `Pick` у наступному рядку таку описку зупинив.
- `Partial` дозволяє явне `undefined`. Об'єкт `updated` за типом `Product`, а ціна в ньому `undefined`, і компілятор
  мовчить. Це значення надрукував `console.log(updated.price)` у першому рядку виводу.
- `Record<string, number>` обіцяє число за будь-яким ключем, навіть за неіснуючим. Тому другий рядок виводу теж
  `undefined`: його надрукував `console.log(coffee)`. Прапорець `--noUncheckedIndexedAccess` змушує враховувати
  `undefined`, проте `--strict` його не вмикає.
- `Readonly` існує лише для компілятора. Файл `node` запустив, і рядок із присвоєнням виконався: третій рядок виводу
  `100` є новою ціною. Заморозити об'єкт під час роботи може лише `Object.freeze`. Крім того, `Readonly` і `Partial`
  діють лише на верхній рівень полів.

## Коли дженерик не потрібен

Посібник TypeScript дає просте правило: параметр типу виправданий, коли зв'язує принаймні два місця. Якщо він
трапляється лише раз, він нічого не зв'язує.

| Запис | Чи потрібен параметр | Чому |
|-------|---------------------|------|
| `function log<T>(value: T): void` | ні | досить `value: unknown` |
| `function count<T>(list: T[]): number` | ні | досить `list: unknown[]`, бо результат не залежить від типу |
| `function last<T>(list: T[]): T \| undefined` | так | зв'язує елементи з результатом |
| `function parse<T>(text: string): T` | небезпечно | `T` є лише у виході, тому зв'язувати нема з чим |

Зайвий параметр робить код важчим для читання й не дає жодної користі. Це і є пастка цього дня. Останній рядок таблиці
ще гірший, бо виглядає безпечно.

Файл `parse.ts`:

```ts
type Rate = { currency: string; value: number };

function parse<T>(text: string): T {
  return JSON.parse(text);
}

const rate = parse<Rate>('{"currency": "EUR", "value": "41.5"}');
console.log(typeof rate.value);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false parse.ts
(tsc нічого не надрукував: помилок немає)
$ node parse.ts
string
```

Вивід `string` показує неправду в типі: за типом `Rate` поле `value` є числом, а в тексті JSON там стоїть рядок
`"41.5"`. Компілятор мовчить, бо `JSON.parse` повертає `any`, а `any` можна покласти куди завгодно. Запис
`parse<Rate>` читається як перевірка, але є тим самим твердженням `as Rate` в іншому записі. Функція
`async function getJson<T>(url: string): Promise<T>`, яка повертає `response.json()`, має ту саму ваду. Такий запис
можна використовувати як угоду з сервером, але дані лишаються неперевіреними, доки їх не перевірить код.

Інколи `as` усередині дженерика виправданий, бо компілятор не може простежити цикл. Наприклад, `const result = {} as
Record<K, number>` у функції, яка далі заповнює всі ключі `K`. Функція `zeros` нижче створює таблицю лічильників, де
кожен лічильник дорівнює нулю. Рядок зі змінною `plain` навмисно записано без `as`, щоб побачити відповідь
компілятора.

Файл `zeros.ts`:

```ts
function zeros<K extends string>(keys: K[]): Record<K, number> {
  // Без as: компілятор бачить порожній об'єкт, а не об'єкт з усіма ключами K.
  const plain: Record<K, number> = {};

  // З as: автор функції обіцяє, що цикл нижче заповнить усі ключі K.
  const result = {} as Record<K, number>;
  for (const key of keys) {
    result[key] = 0;
  }
  return result;
}

console.log(zeros(["low", "high"]));
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false zeros.ts
zeros.ts(3,9): error TS2322: Type '{}' is not assignable to type 'Record<K, number>'.
$ node zeros.ts
{ low: 0, high: 0 }
```

Без `as` компілятор відповів `Type '{}' is not assignable to type 'Record<K, number>'`, і ця відповідь стосується лише
рядка зі змінною `plain`. Рядок із `as` компілятор пропустив, а `node` надрукував таблицю з усіма ключами, тобто цикл
справді виконав обіцянку. Тут обіцянку дає сам автор функції, і вона стосується коду, який він бачить, а не даних зі
світу.

## Типові хибні уявлення

**«`K extends keyof T` не пропустить чужий ключ під час роботи».** Обмеження живе лише в компіляторі. Виклик
`pluck(shelf, "prise" as "price")` компілюється, а `node` друкує `[ undefined, undefined ]`. Щоб побачити це, допишіть
у кінець файлу `pluck.ts` такий рядок:

```ts
// as змушує компілятор вважати описку "prise" правильною назвою "price".
console.log(pluck(shelf, "prise" as "price"));
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false pluck.ts
(tsc нічого не надрукував: помилок немає)
$ node pluck.ts
[ 80, 150 ] [ 'Чай', 'Кава' ]
230
[ undefined, undefined ]
```

Перші два рядки виводу надрукував старий код файлу, а останній надрукував новий рядок. Поля `prise` в об'єктах немає,
тому `item[key]` дає `undefined` для кожного з двох товарів. Отже, обмеження зупиняє описку лише доти, доки компілятор
бачить справжню назву поля. Запис `as` цю перевірку обходить.

**«`Partial` дозволяє покласти в поле що завгодно».** Він дозволяє лише пропустити поле або покласти `undefined`.
Поле, яке є, зберігає свій тип, тому `{ price: "99" }` компілятор відхилить.

Файл `partial-type.ts`:

```ts
type Product = { id: number; name: string; price: number };

// Поле пропущено або дорівнює undefined: це Partial дозволяє.
const empty: Partial<Product> = {};
const cleared: Partial<Product> = { price: undefined };

// Поле є, але тип інший: це Partial не дозволяє.
const wrong: Partial<Product> = { price: "99" };
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false partial-type.ts
partial-type.ts(8,35): error TS2322: Type 'string' is not assignable to type 'number'.
```

Компілятор поскаржився лише на останній рядок. Отже, `Partial` робить поле необов'язковим, але перевірку типу поля не
вимикає: ціну рядком він у код не пропустить.

**«Чим більше параметрів типу, тим гнучкіша функція».** Гнучкість дає зв'язок між типами, а не кількість параметрів.
Посібник радить брати якомога менше параметрів.

## Як це проявиться в React

Хуки React у фазі 1 є дженериками. У пакеті описів `@types/react` `useState` оголошено так: `function
useState<S>(initialState: S | (() => S)): [S, Dispatch<SetStateAction<S>>]`. Параметр `S` зв'язує початкове значення,
поточне значення й функцію зміни. Запускати файл нижче зараз не треба.

Файл `hooks.tsx`:

```tsx
import { useState, useRef, type ReactNode } from "react";

type Product = { id: number; name: string };

export function Hooks() {
  const [count, setCount] = useState(0);
  setCount("один");

  const [stuck, setStuck] = useState(null);
  setStuck({ id: 1, name: "Чай" });

  const [chosen, setChosen] = useState<Product | null>(null);
  setChosen({ id: 1, name: "Чай" });
  console.log(chosen.name);

  const [list, setList] = useState([]);
  setList([{ id: 1, name: "Чай" }]);

  const inputRef = useRef<HTMLInputElement>(null);
  inputRef.current.focus();
  return <input ref={inputRef} />;
}

function List<T>(props: { items: T[]; render: (item: T) => ReactNode }) {
  return <ul>{props.items.map((item, i) => <li key={i}>{props.render(item)}</li>)}</ul>;
}

export const row = <List items={[{ id: 1, name: "Чай" }]} render={(p) => p.title} />;
```

```text
$ npx tsc --noEmit --strict --target es2022 --module esnext --moduleResolution bundler --jsx react-jsx --lib es2022,dom --pretty false hooks.tsx
hooks.tsx(7,12): error TS2345: Argument of type 'string' is not assignable to parameter of type 'SetStateAction<number>'.
hooks.tsx(10,14): error TS2353: Object literal may only specify known properties, and 'id' does not exist in type '(prevState: null) => null'.
hooks.tsx(14,15): error TS18047: 'chosen' is possibly 'null'.
hooks.tsx(17,12): error TS2322: Type '{ id: number; name: string; }' is not assignable to type 'never'.
hooks.tsx(20,3): error TS18047: 'inputRef.current' is possibly 'null'.
hooks.tsx(28,76): error TS2339: Property 'title' does not exist on type '{ id: number; name: string; }'.
```

Кожне повідомлення повторює те, що вже пояснено:

| Рядок | Що сталося | Правило |
|-------|-----------|---------|
| `useState(null)` | `S = null`, і нічого іншого покласти не можна; текст помилки незграбний | компілятор бере те, що бачить |
| `useState<Product \| null>(null)` | працює, а читання `chosen.name` вимагає перевірки на `null` | явний параметр і звуження |
| `useState([])` | елемент має тип `never`, тому потрібно `useState<Product[]>([])` | порожній масив |
| `useRef<HTMLInputElement>(null)` | `current` може бути `null`, бо елемент з'явиться після показу | явний параметр і звуження через `?.` |
| `List<T>` | компонент теж може бути дженериком, і `T` виводиться з `items` | зв'язок пропсів між собою |

Хук запиту, який повертає `T`, потрапляє в ту саму пастку, що й `parse<T>`. Він зручний у вжитку, але відповідь
сервера лишається неперевіреною, доки всередині немає перевірки. Також у файлах `.tsx` запис стрілкової функції
`<T>(...) => ...` конфліктує із синтаксисом JSX, тому там пишуть `<T,>`.

## Перевірте себе

Спершу дайте відповідь самі, уголос або письмово, і лише потім розгортайте пояснення.

**1. Чим `function last<T>(list: T[]): T | undefined` краща за `function last(list: unknown[]): unknown`?**

<details><summary>Відповідь</summary>

Обидві приймають будь-який масив, але друга забуває тип елементів, і результат доводиться перевіряти. Перша зв'язує
вхід із виходом: для масиву чисел результат має тип `number | undefined`. Під час роботи вони однакові, різниця існує
лише для компілятора.

</details>

**2. Навіщо у `pluck` два параметри типу, якщо `key: keyof T` теж зупиняє описку?**

<details><summary>Відповідь</summary>

Параметр `K` запам'ятовує конкретне поле. З ним результат має тип `T[K][]`, для `"price"` це `number[]`. Без нього
компілятор знає лише, що ключ є якимось ключем `T`, і результат стає об'єднанням типів усіх полів.

</details>

**3. У `Omit<Product, "prise">` є описка. Що скаже компілятор і чому?**

<details><summary>Відповідь</summary>

Нічого. Другий параметр `Omit` обмежено будь-яким ключем, а не `keyof T`. Описка нічого не прибере, і тип лишиться
повним `Product`. `Pick` має обмеження `K extends keyof T`, тому там компілятор повідомить про помилку.

</details>

**4. Чому `parse<Rate>(text)` не краща за `JSON.parse(text) as Rate`?**

<details><summary>Відповідь</summary>

Обидва записи лише наказують компілятору вважати значення типом `Rate`. Параметр `T` трапляється лише у виході, тому
нічого не зв'язує. Перевірити дані може лише код, який виконується.

</details>

**5. Що потрібно змінити в `useState(null)`, якщо там згодом буде товар, і що зміниться для коду, який читає стан?**

<details><summary>Відповідь</summary>

Написати `useState<Product | null>(null)`. Тоді функція зміни прийме товар, а код, який читає стан, мусить спершу
перевірити значення на `null`, бо інакше компілятор скаже `'chosen' is possibly 'null'`.

</details>

## Словничок лекції

| Слово | Що означає |
|-------|------------|
| дженерик (generic) | функція або тип із параметром типу |
| параметр типу | ім'я, замість якого компілятор підставляє конкретний тип |
| виведення параметра | компілятор визначає `T` з аргументів виклику |
| обмеження, `extends` | вимога до параметра типу: чому він має відповідати |
| `keyof T` | об'єднання назв полів типу `T` |
| індексований доступ, `T[K]` | тип поля `K` у типі `T` |
| службовий тип (utility type) | вбудований дженерик, який будує новий тип зі старого |
| зіставлений тип (mapped type) | тип, який перебирає ключі й будує поле для кожного |

## Що читати далі

- Розбір читання цього дня проводить через Generics, Keyof Type Operator і Utility Types.
- Розділ Guidelines for Writing Good Generic Functions сторінки More on Functions дає правила, коли дженерик не
  потрібен.

---

Лекцію написано для цього плану. Вона спирається на TypeScript Handbook і на сторінки useState та useRef документації
React, переказані своїми словами. Код запущено на Node 24 і перевірено компілятором TypeScript 6.0.3; файл для React
перевірено з пакетом `@types/react` 19.3.