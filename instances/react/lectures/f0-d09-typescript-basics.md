# Лекція. День 9. TypeScript: основи

Ця лекція пояснює з самого початку, що таке TypeScript, хто й коли перевіряє типи і чому дані з мережі все одно треба
перевіряти власним кодом. Вона спирається лише на JavaScript із попередніх днів. Читання займе близько 30 хвилин.
Вивід кожної команди наведено таким, яким він був насправді. Лише коли програма падає, Node друкує ще шлях до файла й
перелік викликів, і ці рядки тут пропущено.

**Після лекції ви зможете пояснити:**

- хто перевіряє типи, коли це відбувається і чому файл із помилкою типу все одно запускається;
- що таке об'єднання типів і як звичайний `if` доводить компілятору, яке значення перед ним;
- чому кілька варіантів зі спільним полем кращі за один об'єкт із необов'язковими полями;
- чим відрізняються `any`, `unknown` і `as`, і чому відповідь сервера не можна просто назвати потрібним типом;
- чому помилка типів у React виглядає як помилка React, хоча React тут ні до чого.

## Помилка, яку JavaScript не вважає помилкою

Уявіть інтернет-магазин. Функція додає до суми замовлення вартість доставки. Суму програма бере з поля форми, а поле
форми завжди віддає рядок, навіть коли людина ввела цифри.

Файл `order.js`:

```js
function totalWithDelivery(order, delivery) {
  return order.total + delivery;
}

console.log(totalWithDelivery({ total: "100" }, 50));
console.log(totalWithDelivery({ totl: 100 }, 50));
```

```text
$ node order.js
10050
NaN
```

Програма не впала жодного разу, хоча обидві відповіді неправильні. У першому виклику оператор `+` побачив рядок і
склеїв `"100"` із `50`. У другому виклику в назві поля є описка, читання неіснуючого поля дало `undefined`, а
`undefined + 50` дає `NaN`, тобто «не число».

JavaScript дізнається про значення лише тоді, коли виконує рядок, і навіть тоді не знає, чого ви хотіли. Такі помилки
знаходить покупець. Щоб знаходити їх раніше, потрібна програма, яка прочитає код до запуску й порівняє те, що функція
очікує, з тим, що їй дають.

## Що додає TypeScript

**TypeScript** — це JavaScript, до якого можна дописувати описи значень. Такий опис називається **типом**: він каже,
яке значення може бути в цьому місці. Наприклад, `number` означає «будь-яке число», а `{ total: number }` означає
«об'єкт, у якому є поле `total` із числом».

Описи читає програма `tsc`. Її називають **компілятором**, бо вона вміє ще й перетворювати файл `.ts` на файл `.js`.
Сьогодні нам потрібна лише перша її робота: прочитати код, порівняти значення з описами й повідомити про розбіжності.

Той самий код із типами. Запис `order: Order` після назви параметра називається **анотацією**: він каже, якого типу
цей параметр. Запис `: number` після дужок задає тип результату.

Файл `order.ts`:

```ts
type Order = { total: number };

function totalWithDelivery(order: Order, delivery: number): number {
  return order.total + delivery;
}

console.log(totalWithDelivery({ total: "100" }, 50));
console.log(totalWithDelivery({ totl: 100 }, 50));
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false order.ts
order.ts(7,33): error TS2322: Type 'string' is not assignable to type 'number'.
order.ts(8,33): error TS2561: Object literal may only specify known properties, but 'totl' does not exist in type 'Order'. Did you mean to write 'total'?
$ echo $?
2
```

Запис `order.ts(7,33)` означає «файл, рядок 7, позиція 33». `TS2322` — номер помилки, за яким її легко шукати. Слова
`not assignable` означають, що значення одного типу не можна покласти туди, де обіцяно інший. У другому повідомленні
компілятор ще й пропонує правильну назву поля.

Прапорець `--noEmit` просить лише перевірити код, не створюючи файла `.js`. Прапорець `--strict` вмикає всі суворі
перевірки, `--target es2022` каже, яку версію JavaScript вважати відомою, а `--pretty false` друкує помилки простим
текстом.

Команда `echo $?` друкує код, з яким завершилася попередня команда. Код 0 означає успіх, а будь-який інший код означає
невдачу. Тут `tsc` завершився з кодом 2, бо знайшов помилки.

## Перевірка й запуск — дві окремі дії

Тепер запустимо той самий файл із помилками:

```text
$ node order.ts
10050
NaN
```

Node 24 запускає файли `.ts` напряму й типів не перевіряє. Він замінює все, що стосується типів, пробілами, а решту
виконує як звичайний JavaScript. Тому програма видає ті самі неправильні числа, що й без типів. Це називається
**стиранням типів**.

| | `tsc` | `node` |
|--|-------|--------|
| Коли працює | до запуску програми | під час запуску |
| Що робить із типами | порівнює з ними кожне значення в коді | викидає їх, не читаючи |
| Що бачить | лише текст коду | справжні значення, зокрема дані з мережі |
| Помилка типу | друкує її й завершується з кодом 2 | не шукає її й ніяк не реагує |

З цієї таблиці випливають три наслідки, і на них тримається решта лекції.

**Перший: про типи свідчить лише `tsc`.** Те, що `node` запустив файл, нічого не доводить. Типи збігаються тоді, коли
`tsc` нічого не надрукував і завершився з кодом 0.

**Другий: під час роботи програми типів не існує.** Запитати в значення, чи воно `Order`, неможливо, бо слова `Order`
у виконуваному коді вже немає. Перевіряти під час роботи можна лише засобами JavaScript: `typeof`, порівнянням,
оператором `in`.

**Третій: `tsc` бачить код, а не дані.** Текст, який надішле сервер завтра, у коді не записаний, тому компілятор
нічого про нього не знає. Цьому присвячено окремий розділ нижче.

## Як записують типи

| Запис | Що він означає | Значення, яке підходить |
|-------|----------------|-------------------------|
| `string`, `number`, `boolean` | рядок, число, логічне значення | `"Чай"`, `80`, `true` |
| `number[]` | масив чисел | `[80, 150]` |
| `{ name: string; price: number }` | об'єкт із двома полями | `{ name: "Чай", price: 80 }` |
| `{ note?: string }` | поля `note` може не бути | `{}` або `{ note: "Крихке" }` |
| `(price: number) => string` | функція з числа в рядок | `(price) => price + " грн"` |

**Де анотації потрібні.** Компілятор сам визначає тип, коли бачить значення, і це називається **виведенням типу**.
Запис `let price = 80` дає змінній тип `number`, і наступний рядок `price = "сто"` компілятор відхилить без жодної
анотації. Параметри функції визначити нема з чого, бо функцію можуть викликати звідки завгодно, тому `--strict`
вимагає для них анотації. Звичайна практика така: анотувати параметри й результат функції, а локальні змінні залишати
виведенню.

**`type` і `interface`.** Обидва слова дають типу назву, і для об'єктів вони майже рівноцінні. Лише `type` може
назвати об'єднання, про яке йтиметься далі, і лише `interface` можна оголосити вдруге, щоб додати поля. Документація
радить для об'єктів типово брати `interface`. У реальних проєктах трапляються обидва підходи, тому вирішує
домовленість у проєкті.

**Компілятор порівнює форму, а не назву.** Значення підходить до типу, якщо в ньому є всі потрібні поля потрібних
типів. Змінну із зайвим полем теж можна передати у функцію, бо зайве поле функції не заважає. Це називається
**структурною типізацією**. Виняток стосується об'єкта, написаного прямо там, де очікують тип: зайве поле в ньому
компілятор вважає ймовірною опискою. Саме ця перевірка знайшла `totl` у прикладі вище.

## Об'єднання: одне з кількох

Знижку в нашому магазині можна задати числом, можна кодом-рядком, а можна не задати взагалі. Один тип цього не опише.
**Об'єднання** записують через вертикальну риску: `string | number | null` означає «або рядок, або число, або `null`».

Об'єднання приймає будь-який зі своїх варіантів, зате читати з нього дозволено лише те, що є в усіх варіантах.
Компілятор міркує так: значення може виявитися будь-яким варіантом, тому операція має бути законною для кожного.

Метод `toString` є і в рядка, і в числа, тому для `string | number` його викликати можна. Метод `toUpperCase` є лише в
рядка, тому такий виклик компілятор не пропускає.

Файл `union.ts`:

```ts
function label(value: string | number): string {
  console.log(value.toString()); // метод є в обох варіантах
  return value.toUpperCase(); // метод є лише в рядка
}

console.log(label(5));
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false union.ts
union.ts(3,16): error TS2339: Property 'toUpperCase' does not exist on type 'string | number'.
  Property 'toUpperCase' does not exist on type 'number'.
$ node union.ts
5
TypeError: value.toUpperCase is not a function
```

Компілятор поскаржився лише на рядок 3, а рядок 2 пропустив. Рядок із відступом уточнює причину: цього методу немає у
варіанта `number`. Запуск показує, що компілятор мав рацію: `node` надрукував `5` із рядка 2, а на рядку 3 програма
впала, бо функція отримала саме число. Отже, повідомлення про об'єднання вказує на виклик, який справді може впасти в
покупця, тому такий виклик треба спершу захистити перевіркою.

Значення `null` і `undefined` теж стають варіантами об'єднання. З прапорцем `--strict` тип `string` їх не містить,
тому можливу відсутність значення записують прямо: `string | null`.

## Звуження: `if` як доказ для компілятора

Щоб скористатися об'єднанням, треба з'ясувати, який варіант перед нами. Для цього пишуть звичайну перевірку
JavaScript, а компілятор читає її й робить тип вужчим усередині гілки. Це називається **звуженням**, і окремого
синтаксису воно не потребує.

Файл `discount.ts`:

```ts
function discount(code: string | number | null): number {
  if (code === null) {
    return 0;
  }
  if (typeof code === "number") {
    return code;
  }
  return code === "VIP" ? 20 : 5;
}

console.log(discount(null), discount(15), discount("VIP"), discount("WELCOME"));
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false discount.ts
(tsc нічого не надрукував: помилок немає)
$ echo $?
0
$ node discount.ts
0 15 20 5
```

Компілятор нічого не виконує. Він читає код зверху вниз і стежить, що може лишитися в змінній `code`:

| Місце в коді | Що може бути в `code` | Чому |
|--------------|-----------------------|------|
| початок функції | `string \| number \| null` | так записано в анотації |
| усередині першого `if` | `null` | перевірка `=== null` пройшла |
| після першого `if` | `string \| number` | гілка з `null` завершилась через `return`, тому далі `null` дійти не може |
| усередині другого `if` | `number` | `typeof` дав `"number"` |
| останній рядок | `string` | варіант `number` теж пішов через `return` |

Компілятор розуміє кілька видів перевірок:

| Перевірка | Що вона доводить | На що зважати |
|-----------|------------------|---------------|
| `typeof x === "string"` | примітивний тип значення | `typeof` не відрізняє `null` від об'єкта |
| `x !== null` | значення не `null` | прибирає цей варіант із типу |
| `"field" in x` | в об'єкті є таке поле | тип значення в полі ще невідомий |
| `if (x)` | значення не є хибним | відкидає ще й `0` та порожній рядок |

**Пастка з `typeof null`.** У JavaScript `typeof null` дорівнює `"object"`. Причина історична: у першій реалізації
мови об'єкти й `null` мали однакову внутрішню позначку, а стандарт зберіг такий результат. Компілятор це знає, тому
після `typeof x === "object"` залишає `null` серед можливих варіантів. Прибрати його може лише окрема перевірка `x !==
null`.

**Пастка з `if (x)`.** Значення `0`, `""` і `NaN` теж вважаються хибними. Якщо функція пише `if (price)` для типу
`number | null`, то безкоштовна доставка за нуль гривень потрапить у ту саму гілку, що й відсутня ціна. Компілятор
цього не зупинить, бо типи тут правильні, а неправильний лише зміст.

## Розрізнюване об'єднання: варіанти зі спільним полем

Спершу ще одне поняття. Тип може складатися з одного конкретного значення. Запис `"packing"` як тип означає «лише
рядок `packing`». Це називається **літеральним типом**.

Тепер опишемо доставку посилки, яка буває на трьох етапах. Поки посилку пакують, кур'єра ще немає. Коли її везуть,
кур'єр є. Коли її отримали, відомо, хто підписав. Перший спосіб, який спадає на думку, це один об'єкт із
необов'язковими полями.

Файл `delivery-loose.ts`:

```ts
type Delivery = {
  stage: "packing" | "onTheWay" | "delivered";
  courier?: string;
  signedBy?: string;
};

function courierName(delivery: Delivery): string {
  if (delivery.stage === "onTheWay") {
    return delivery.courier.toUpperCase();
  }
  return "";
}

const nonsense: Delivery = { stage: "packing", signedBy: "Оксана" };
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false delivery-loose.ts
delivery-loose.ts(9,12): error TS18048: 'delivery.courier' is possibly 'undefined'.
```

У цього опису дві вади. Компілятор не знає зв'язку між `stage` і `courier`, хоча ми його знаємо, тому навіть після
перевірки етапу вимагає довести наявність кур'єра. А останній рядок проходить без помилки, хоча описує неможливу
ситуацію: посилку ще пакують, а хтось уже її підписав.

Другий спосіб описує кожен етап окремим варіантом зі своїми полями. Поле `stage` є в усіх варіантах, але в кожному має
свій літерал. Таке об'єднання називається **розрізнюваним**, бо за спільним полем компілятор розрізняє варіанти.

Файл `delivery.ts`:

```ts
type Delivery =
  | { stage: "packing" }
  | { stage: "onTheWay"; courier: string }
  | { stage: "delivered"; signedBy: string };

function describe(delivery: Delivery): string {
  switch (delivery.stage) {
    case "packing":
      return "Пакуємо";
    case "onTheWay":
      return "Везе " + delivery.courier;
    case "delivered":
      return "Отримав " + delivery.signedBy;
  }
}

console.log(describe({ stage: "onTheWay", courier: "Ігор" }));
console.log(describe({ stage: "delivered", signedBy: "Оксана" }));
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false delivery.ts
(tsc нічого не надрукував: помилок немає)
$ node delivery.ts
Везе Ігор
Отримав Оксана
```

Рядок за рядком:

- `switch (delivery.stage)` перевіряє спільне поле. До цього рядка компілятор дозволяє читати лише `stage`, бо лише
  воно є в усіх варіантах.
- Усередині `case "onTheWay"` компілятор уже вибрав варіант із кур'єром, тому `delivery.courier` має тип `string`, а
  не `string | undefined`.
- Гілки `default` немає. Компілятор сам порахував, що три випадки охоплюють усі варіанти, тому не скаржиться, що
  функція може нічого не повернути.

Цей опис забороняє цілий ряд помилок. Запишемо п'ять таких помилок в одному файлі й покажемо його компілятору.

Файл `delivery-errors.ts`:

```ts
type Delivery =
  | { stage: "packing" }
  | { stage: "onTheWay"; courier: string }
  | { stage: "delivered"; signedBy: string };

// Читаємо поле кур'єра, не перевіривши етап.
function courierName(delivery: Delivery): string {
  return delivery.courier;
}

// У switch немає випадку "delivered".
function describe(delivery: Delivery): string {
  switch (delivery.stage) {
    case "packing":
      return "Пакуємо";
    case "onTheWay":
      return "Везе " + delivery.courier;
  }
}

// Описка в назві етапу: мала літера w.
const typo: Delivery = { stage: "onTheway", courier: "Ігор" };

// Кур'єра забули вказати.
const noCourier: Delivery = { stage: "onTheWay" };

// Посилку ще пакують, а кур'єр уже є.
const tooEarly: Delivery = { stage: "packing", courier: "Ігор" };
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false delivery-errors.ts
delivery-errors.ts(8,19): error TS2339: Property 'courier' does not exist on type 'Delivery'.
  Property 'courier' does not exist on type '{ stage: "packing"; }'.
delivery-errors.ts(12,40): error TS2366: Function lacks ending return statement and return type does not include 'undefined'.
delivery-errors.ts(22,26): error TS2820: Type '"onTheway"' is not assignable to type '"packing" | "onTheWay" | "delivered"'. Did you mean '"onTheWay"'?
delivery-errors.ts(25,7): error TS2322: Type '{ stage: "onTheWay"; }' is not assignable to type 'Delivery'.
  Property 'courier' is missing in type '{ stage: "onTheWay"; }' but required in type '{ stage: "onTheWay"; courier: string; }'.
delivery-errors.ts(28,48): error TS2353: Object literal may only specify known properties, and 'courier' does not exist in type '{ stage: "packing"; }'.
```

Кожній помилці в коді відповідає одне повідомлення, а рядки з відступом уточнюють причину. У першому повідомленні
компілятор називає варіант `packing`, у якого немає кур'єра. Отже, описка, забуте поле чи забутий випадок зупиняють
вас ще до запуску, і покупець їх не побачить. Таблиця збирає ці повідомлення скорочено:

| Що написано | Що каже компілятор |
|-------------|--------------------|
| `delivery.courier` без перевірки етапу | `Property 'courier' does not exist on type 'Delivery'` |
| `switch` без випадку `delivered` | `Function lacks ending return statement` |
| `{ stage: "onTheway", courier: "Ігор" }` | `Type '"onTheway"' is not assignable to type …`, а далі підказка `Did you mean '"onTheWay"'?` |
| `{ stage: "onTheWay" }` | `Property 'courier' is missing` |
| `{ stage: "packing", courier: "Ігор" }` | `Object literal may only specify known properties` |

Коротко це формулюють так: неможливі стани не вдасться навіть записати.

**Тип `never`.** Коли всі варіанти вичерпано, у змінній не лишається жодного можливого значення. Для цього існує тип
`never`, «сюди не дійде жодне значення», і покласти в нього можна лише `never`. Тому в гілці `default` часто пишуть
`const rest: never = delivery`. Якщо хтось додасть четвертий етап і забуде про нього в цьому `switch`, компілятор
покаже на цей рядок і назве забутий варіант.

Файл `delivery-never.ts`:

```ts
type Delivery =
  | { stage: "packing" }
  | { stage: "onTheWay"; courier: string }
  | { stage: "delivered"; signedBy: string }
  | { stage: "returned"; reason: string }; // новий етап, для якого немає case

function describe(delivery: Delivery): string {
  switch (delivery.stage) {
    case "packing":
      return "Пакуємо";
    case "onTheWay":
      return "Везе " + delivery.courier;
    case "delivered":
      return "Отримав " + delivery.signedBy;
    default:
      // Сюди доходить лише те, що не обробив жоден case.
      const rest: never = delivery;
      return rest;
  }
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false delivery-never.ts
delivery-never.ts(17,13): error TS2322: Type '{ stage: "returned"; reason: string; }' is not assignable to type 'never'.
```

Компілятор показав на рядок 17 і в лапках назвав варіант `returned`, який ніхто не обробив. Якщо прибрати рядок із
цим варіантом з опису типу, `tsc` не надрукує нічого, бо в гілці `default` не лишиться жодного можливого значення.
Отже, новий етап сам покаже вам кожен `switch` із таким рядком, де про нього забули.

## `any`, `unknown` і `as`: що робити з даними ззовні

Тепер повернімося до третього наслідку: `tsc` не бачить даних. Сервер надсилає текст, програма перетворює його на
значення, і лише під час запуску стає відомо, що там насправді. Є три способи сказати про таке значення компілятору, і
лише один із них безпечний.

| Запис | Що він каже компілятору | Що дозволено зі значенням | Неправильні дані |
|-------|-------------------------|---------------------------|------------------|
| `any` | не перевіряй взагалі | усе | помилка під час роботи, у покупця |
| `as Rate` | вважай, що це `Rate` | усе, що дозволено для `Rate` | помилка під час роботи, у покупця |
| `unknown` | я не знаю, що це | нічого, доки немає перевірки | ваша перевірка відхиляє їх одразу |

**`any` приходить сам.** Вбудований опис `JSON.parse` має результат `any`, а метод `json()` відповіді `fetch` має
результат `Promise<any>`. Тому навіть без слова `any` у вашому коді значення з мережі вже не перевіряється.

**`as` — це обіцянка.** Запис `значення as Тип` називається **твердженням типу**. Він нічого не перевіряє й нічого не
перетворює, а лише наказує компілятору вважати значення таким типом. Припустімо, сервер надіслав курс валюти, але поле
`value` прийшло рядком.

Файл `rate-as.ts`:

```ts
type Rate = { currency: string; value: number };

const rate = JSON.parse('{"currency": "EUR", "value": "41.5"}') as Rate;
console.log(rate.value.toFixed(2));
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false rate-as.ts
(tsc нічого не надрукував: помилок немає)
$ node rate-as.ts
TypeError: rate.value.toFixed is not a function
```

Компілятор мовчить, бо йому пообіцяли `Rate`, а метод `toFixed` у числа є. Програма падає, бо там рядок.

**`unknown` вимагає доказів.** Прочитати поле значення цього типу чи покласти його в змінну типу `number` компілятор
не дасть, доки перевірки не звузять тип. Той самий курс валюти з перевіркою.

Файл `rate.ts`:

```ts
type Rate = { currency: string; value: number };

function toRate(data: unknown): Rate {
  if (
    typeof data === "object" &&
    data !== null &&
    "currency" in data &&
    typeof data.currency === "string" &&
    "value" in data &&
    typeof data.value === "number"
  ) {
    return { currency: data.currency, value: data.value };
  }
  throw new Error("Сервер надіслав не курс валюти");
}

for (const text of [
  '{"currency": "EUR", "value": 41.5}',
  '{"currency": "EUR", "value": "41.5"}',
  '{"currency": "EUR"}',
  "null",
  '"EUR"',
]) {
  try {
    console.log(text, "->", toRate(JSON.parse(text)));
  } catch {
    console.log(text, "-> відхилено");
  }
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false rate.ts
(tsc нічого не надрукував: помилок немає)
$ node rate.ts
{"currency": "EUR", "value": 41.5} -> { currency: 'EUR', value: 41.5 }
{"currency": "EUR", "value": "41.5"} -> відхилено
{"currency": "EUR"} -> відхилено
null -> відхилено
"EUR" -> відхилено
```

Компілятор читає ланцюжок умов зліва направо, і після кожної умови тип стає вужчим. Це можна побачити самому за
допомогою типу `never`. Покласти в `never` не можна нічого, тому кожен рядок `const ...: never = ...` у файлі нижче
навмисно неправильний, а компілятор у повідомленні про нього називає тип, який бачить у цьому місці. Той самий
ланцюжок тут записано вкладеними `if`, щоб після кожної умови стояв окремий рядок. Функцію ніхто не викликає, бо її
читає лише `tsc`.

Файл `rate-stages.ts`:

```ts
function stages(data: unknown) {
  if (typeof data === "object") {
    const a: never = data; // який тип має data?
    if (data !== null) {
      const b: never = data; // який тип має data?
      if ("currency" in data) {
        const c: never = data; // який тип має data?
        if (typeof data.currency === "string") {
          const d: never = data.currency; // який тип має поле?
          if ("value" in data) {
            const e: never = data; // який тип має data?
            if (typeof data.value === "number") {
              const f: never = data.value; // який тип має поле?
            }
          }
        }
      }
    }
  }
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false rate-stages.ts
rate-stages.ts(3,11): error TS2322: Type 'object | null' is not assignable to type 'never'.
  Type 'null' is not assignable to type 'never'.
rate-stages.ts(5,13): error TS2322: Type 'object' is not assignable to type 'never'.
rate-stages.ts(7,15): error TS2322: Type 'object & Record<"currency", unknown>' is not assignable to type 'never'.
rate-stages.ts(9,17): error TS2322: Type 'string' is not assignable to type 'never'.
rate-stages.ts(11,19): error TS2322: Type 'object & Record<"currency", unknown> & Record<"value", unknown>' is not assignable to type 'never'.
rate-stages.ts(13,21): error TS2322: Type 'number' is not assignable to type 'never'.
```

Кожне повідомлення відповідає одному навмисно неправильному рядку, а в перших лапках стоїть тип у цьому місці. Перше
повідомлення показує, що після `typeof` у значенні ще може бути `null`. Знак `&` означає «і те, і те», а запис
`Record<"currency", unknown>` означає «об'єкт, у якому є поле `currency` зі значенням типу `unknown`». Отже, оператор
`in` довів лише наявність поля, і перед використанням значення вам потрібна ще перевірка `typeof`.

Типи в таблиці взято з цих повідомлень:

| Умова | Яким став тип `data` | Який текст вона відхиляє |
|-------|----------------------|--------------------------|
| `typeof data === "object"` | `object \| null` | `"EUR"` |
| `data !== null` | `object` | `null` |
| `"currency" in data` | об'єкт із полем `currency` невідомого типу | об'єкт без цього поля |
| `typeof data.currency === "string"` | поле `currency` стало рядком | об'єкт із числом замість назви |
| `"value" in data` | додалося поле `value` невідомого типу | `{"currency": "EUR"}` |
| `typeof data.value === "number"` | поле `value` стало числом | `{"currency": "EUR", "value": "41.5"}` |

Функція будує новий об'єкт, а не повертає `data`, і цьому є причина. Компілятор звузив окремі поля, а сам `data`
лишився типу «об'єкт із полями невідомого типу», тому рядок `return data` він би не пропустив. Це легко перевірити:
скопіюйте `rate.ts` у файл `rate-return.ts` і замініть у копії рядок `return { currency: data.currency, value:
data.value };` на `return data;`.

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false rate-return.ts
rate-return.ts(12,5): error TS2322: Type 'object & Record<"currency", unknown> & Record<"value", unknown>' is not assignable to type 'Rate'.
  Types of property 'currency' are incompatible.
    Type 'unknown' is not assignable to type 'string'.
```

Читайте це повідомлення з найглибшого рядка: значення типу `unknown` не можна покласти в поле типу `string`. Отже,
функція перевірки повертає новий об'єкт, зібраний із полів, які вона вже перевірила.

Таку перевірку ставлять один раз на межі програми, там, де дані заходять ззовні. Після неї решта коду працює зі
справжнім типом і нічого не перевіряє. Пізніше в плані з'явиться бібліотека `zod`, яка будує такі перевірки з опису.

## Типові хибні уявлення

**«`tsc` не знайшов помилок, отже, дані правильні».** Він перевірив код. Дані з мережі він не бачив, а `as` і `any`
лише приховують це від нього.

**«`as number` перетворить рядок на число».** Перетворення робить лише код, наприклад `Number(text)`.

Файл `as-number.ts`:

```ts
// Спершу as unknown, бо прямий запис "41.5" as number компілятор відхиляє.
const price = "41.5" as unknown as number;

console.log(typeof price); // що насправді лежить у змінній
console.log(price + 1); // компілятор вважає, що це додавання чисел
console.log(typeof Number("41.5")); // справжнє перетворення
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false as-number.ts
(tsc нічого не надрукував: помилок немає)
$ node as-number.ts
string
41.51
number
```

Значення `"41.5" as unknown as number` після запуску лишається рядком. Тому `typeof` дає `string`, а `+ 1` склеює
рядки й дає `41.51`. Лише виклик `Number` дає справжнє число. Отже, коли вам потрібне число, викликайте перетворення,
а запису `as` не вірте.

**«Можна написати `x instanceof Product`, де `Product` — це `type`».**

Файл `instanceof.ts`:

```ts
type Product = { name: string };

function isProduct(x: unknown): boolean {
  return x instanceof Product; // Product тут є лише типом
}

console.log(isProduct({ name: "Чай" }));
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false instanceof.ts
instanceof.ts(4,23): error TS2693: 'Product' only refers to a type, but is being used as a value here.
$ node instanceof.ts
ReferenceError: Product is not defined
```

Компілятор каже, що `Product` є лише типом. Запуск показує те саме з іншого боку: `node` стер опис типу, і назви
`Product` у програмі не лишилося. Під час роботи типів немає, тому перевіряти можна лише значення.

**«`any` зручний, бо не заважає працювати».** Він не заважає лише компілятору. Помилка нікуди не зникає, а переїжджає
до людини, яка користується програмою.

## Як це проявиться в React

У фазі 1 компоненти отримують дані через **пропси**, тобто вхідні параметри компонента, а значення між показами екрана
зберігають через **стан**. Обидва описують типами. Запускати файл нижче зараз не треба, бо React з'явиться пізніше.

Файл `upload.tsx`:

```tsx
import { useState } from "react";

type BadgeProps = { label: string; count?: number };

function Badge({ label, count = 0 }: BadgeProps) {
  return <span>{label}: {count}</span>;
}

export const wrong = <Badge label={5} />;

type UploadState =
  | { stage: "idle" }
  | { stage: "sending"; percent: number };

export function Upload() {
  const [upload, setUpload] = useState<UploadState>({ stage: "idle" });

  if (upload.stage === "idle") {
    return <p>{upload.percent}%</p>;
  }
  return <button onClick={() => setUpload({ stage: "sending" })}>Ще раз</button>;
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --module esnext --moduleResolution bundler --jsx react-jsx --lib es2022,dom --pretty false upload.tsx
upload.tsx(9,29): error TS2322: Type 'number' is not assignable to type 'string'.
upload.tsx(19,23): error TS2339: Property 'percent' does not exist on type '{ stage: "idle"; }'.
upload.tsx(21,43): error TS2345: Argument of type '{ stage: "sending"; }' is not assignable to parameter of type 'SetStateAction<UploadState>'.
  Type '{ stage: "sending"; }' is not assignable to type '{ stage: "sending"; percent: number; } | ((prevState: UploadState) => UploadState)'.
    Property 'percent' is missing in type '{ stage: "sending"; }' but required in type '{ stage: "sending"; percent: number; }'.
```

Кожне повідомлення пояснюється тим, що ви вже знаєте:

- `label={5}` — це звичайна помилка присвоєння, бо пропси компонента перевіряються так само, як поля об'єкта.
- `upload.percent` у гілці `idle` — це звуження за полем `stage`. Прочитати поле, якого в цьому варіанті немає,
  компілятор не дасть. Перевірка цього дня вимагає того самого для `data` в гілці завантаження.
- `SetStateAction<UploadState>` означає просту річ: функція зміни стану приймає нове значення або функцію, яка його
  обчислює. Останнє повідомлення читайте з найглибшого рядка: там названо поле `percent`, якого бракує.

Документація React радить саме таку побудову для стану запиту: об'єднання варіантів зі спільним полем. Кутові дужки в
`useState<UploadState>` пояснить завтрашня лекція.

Побачивши рядок `error TS…`, читайте його як розбіжність двох типів. Помилка самого React виглядає інакше: вона
виникає під час роботи й видна в консолі браузера.

## Перевірте себе

Спершу дайте відповідь самі, уголос або письмово, і лише потім розгортайте пояснення.

**1. `tsc` надрукував помилку, а `node` той самий файл запустив і вивів результат. Хто з них неправий?**

<details><summary>Відповідь</summary>

Обидва праві, бо роблять різну роботу. `tsc` до запуску порівнює значення з типами й знайшов розбіжність. `node` типи
викидає й просто виконує JavaScript. Висновок про типи можна робити лише за виводом `tsc`.

</details>

**2. Значення `x` має тип `number | null`. Який тип у кожній гілці `if (x) { ... } else { ... }` і куди потрапить
`0`?**

<details><summary>Відповідь</summary>

У першій гілці `x` має тип `number`. У другій гілці тип лишається `number | null`, бо хибним може бути і `null`, і
число `0`. Значення `0` потрапить у другу гілку разом із `null`. Щоб їх розрізнити, потрібна умова `x !== null`.

</details>

**3. Чому варіанти доставки не описують одним об'єктом із необов'язковими полями? Назвіть дві причини.**

<details><summary>Відповідь</summary>

Перша: компілятор не знає зв'язку між етапом і полем, тому навіть після перевірки етапу вимагатиме доводити наявність
кур'єра. Друга: спільний об'єкт дозволяє записати неможливі стани, наприклад етап пакування з підписом отримувача.

</details>

**4. Сервер надіслав `{"value": "41.5"}`. Що буде у випадку `JSON.parse(text) as Rate`, а що у випадку перевірки
значення як `unknown`?**

<details><summary>Відповідь</summary>

З `as` компілятор мовчить, бо `JSON.parse` повертає `any`, і помилка виникне аж при першому використанні:
`rate.value.toFixed` не буде функцією. З `unknown` перевірка відхилить дані й кине зрозумілу помилку там, де дані
зайшли в програму.

</details>

**5. Чому після `"currency" in data` не можна одразу написати `data.currency.toUpperCase()`?**

<details><summary>Відповідь</summary>

Оператор `in` довів лише, що поле існує. Тип значення в ньому лишився `unknown`. Потрібна ще перевірка `typeof
data.currency === "string"`, і лише після неї компілятор дозволить методи рядка.

</details>

## Словничок лекції

| Слово | Що означає |
|-------|------------|
| тип | опис того, яке значення може бути в цьому місці коду |
| компілятор, `tsc` | програма, яка до запуску порівнює код із типами |
| стирання типів | під час запуску типи викидаються, і програма про них нічого не знає |
| структурна типізація | значення підходить до типу за набором полів, а не за назвою типу |
| об'єднання (union) | тип `A \| B`, тобто значення або одного типу, або іншого |
| звуження (narrowing) | перевірка в коді робить тип вужчим усередині гілки |
| розрізнюване об'єднання | варіанти зі спільним полем, у кожному з яких це поле має свій літерал |
| `never` | тип, якому не належить жодне значення |
| `any` | вимикає перевірку для значення |
| `unknown` | значення невідоме, і нічого не можна зробити до перевірки |
| твердження типу, `as` | наказ компілятору вважати значення певним типом, без перевірки |

## Що читати далі

- Розбір читання цього дня проводить через The Basics, Everyday Types і Narrowing.
- Using TypeScript у документації React стане в пригоді у фазі 1.

---

Лекцію написано для цього плану. Вона спирається на TypeScript Handbook, примітки до TypeScript 6.0, документацію
Node.js, сторінку про `typeof` на MDN і сторінку Using TypeScript документації React, переказані своїми словами. Код
запущено на Node 24 і перевірено компілятором TypeScript 6.0.3; файл для React перевірено з пакетом `@types/react`
19.3.