# Розбір читання. День 10. TypeScript: дженерики

Лекція цього дня розповідає про саму тему, а цей розбір допомагає прочитати три сторінки документації TypeScript і
згадати рецепт із книжки. Він показує, де що шукати, що означають незнайомі слова й що із прочитаного стане в пригоді
в React. Оригінали написано англійською, тому назви розділів подано англійською, щоб їх легко було знайти. Розбір не
перекладає текст, а переказує його своїми словами.

Читайте в такому порядку: лекція, потім Generics (30 хвилин), Keyof Type Operator (5 хвилин), Utility Types (20
хвилин), а наприкінці рецепт книжки (10 хвилин).

**Як ми запускали приклади.** Усе тут зроблено так само, як учора. Приклади перевірено компілятором TypeScript 7.0.2,
найновішою стабільною версією в реєстрі npm, і запущено в Node 24.22. Команда перевірки та сама, що в лекції:
`npx tsc --noEmit --strict --target es2022 --pretty false файл.ts`. Її прапорці пояснює лекція дня 9 у розділі «Що
додає TypeScript». Як Node виконує файл `.ts`, пояснено у вступі вчорашнього розбору, в абзаці з такою самою назвою.
Якщо у вашій теці лежить файл `tsconfig.json`, ця команда замість перевірки друкує помилку `TS5112`. Що вона означає,
пояснює лекція дня 9 у тому самому розділі «Що додає TypeScript». Вступ лекції цього дня нагадує, що тоді до кожної
команди треба додати прапорець `--ignoreConfig`. Коли програма падає, Node друкує ще шлях до файла, рядок коду й
перелік викликів. Ці рядки ми пропустили.

**Службові рядки в прикладах посібника.** Приклади посібника містять позначки для програми, яка будує сайт:
`// @errors`, `// ---cut---` і `//   ^?`. Що вони означають, пояснено у вступі вчорашнього розбору, в абзаці
«Службові рядки в прикладах посібника». Ми ці позначки прибрали. Сьогодні трапиться ще одна така позначка,
`// @strict: false`. Про неї йдеться в розділі `Generic Classes` нижче. Щоб побачити тип у певному місці, ми, як і
вчора, пишемо навмисно неправильний рядок `const a: never = x`. Компілятор відхиляє такий рядок і в повідомленні
називає тип, який має `x`.

## Generics

**Де читати:** [Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html) у посібнику TypeScript
Handbook, який пишуть автори самої мови. У примірнику `typescript` це `handbook-v2/Type Manipulation/Generics`.

**Що там є.** Це основний текст дня. На початку автори кажуть, що дженерики дозволяють будувати частини програми, які
працюють із багатьма типами, а не з одним. Вони зазначають, що подібний механізм є в мовах C# і Java. Параметр типу в
цьому тексті називається `Type`, а на сторінці плану й у коді React частіше `T`. Різниці немає, бо це лише назва.

**Якщо часу мало,** прочитайте `Hello World of Generics`, `Generic Types`, `Generic Constraints` і `Using Type
Parameters in Generic Constraints`.

### Hello World of Generics

Розділ пояснює дженерики на функції `identity`, яка повертає свій аргумент без змін. Автори порівнюють її з командою
терміналу `echo`, яка друкує те, що їй дали. Спершу вони пробують два записи без дженериків. Запис
`identity(arg: number): number` годиться лише для чисел. Запис `identity(arg: any): any` приймає все, але про
результат компілятор уже нічого не знає. Ту саму проблему лекція розбирає на функції `last` у розділі «Проблема: одна
дія, багато типів», тому повторювати її тут не будемо.

Потім автори вводять **змінну типу** (type variable). Так посібник називає те, що лекція називає параметром типу:
ім'я, замість якого компілятор підставляє справжній тип. Далі показано два способи викликати таку функцію. Обидва
виклики стоять у файлі нижче, а третій виклик ми додали самі. Файл `identity.ts`:

```ts
function identity<Type>(arg: Type): Type {
  return arg;
}

let output = identity<string>("myString");
let output2 = identity("myString");
const output3 = identity("myString");
console.log(output, output2, output3);

const a: never = output;
const b: never = output2;
const c: never = output3;
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false identity.ts
identity.ts(10,7): error TS2322: Type 'string' is not assignable to type 'never'.
identity.ts(11,7): error TS2322: Type 'string' is not assignable to type 'never'.
identity.ts(12,7): error TS2322: Type '"myString"' is not assignable to type 'never'.
$ node identity.ts
myString myString myString
```

Перший виклик сам пише тип у кутових дужках, і `Type` стає `string`. Другий виклик покладається на **виведення
аргументу типу** (type argument inference): компілятор дивиться на значення `"myString"` і сам добирає `Type`. Автори
радять другий спосіб, бо він коротший і легше читається. Явний запис вони лишають для випадків, коли компілятор не
може вивести тип. Лекція показує такі випадки в розділі «Як компілятор добирає `T`», і найважливіший з них для React —
початкове значення `null`.

Третій виклик ми додали, щоб пояснити, чому посібник показує для `output` тип `string`, а не `"myString"`. Компілятор
вивів для `Type` літеральний тип `"myString"`, тобто тип, у якому є лише одне це значення. Змінна `const` цей тип
зберегла, бо змінити її значення не можна. Змінна `let` розширила його до `string`, бо в неї згодом можна покласти
інший рядок. Те саме міркування вчорашній розбір наводить у розділі `Literal Types` для поля об'єкта: те, що можна
змінити пізніше, отримує ширший тип. Node надрукував одне й те саме для всіх трьох змінних, бо типи існують лише для
компілятора.

### Working with Generic Type Variables

Тут автори показують помилку, яку робить кожен новачок. Файл `logging.ts` містить три функції з цього розділу, а два
виклики наприкінці ми додали самі:

```ts
function loggingIdentity<Type>(arg: Type): Type {
  console.log(arg.length);
  return arg;
}

function loggingIdentity2<Type>(arg: Type[]): Type[] {
  console.log(arg.length);
  return arg;
}

function loggingIdentity3<Type>(arg: Array<Type>): Array<Type> {
  console.log(arg.length);
  return arg;
}

loggingIdentity2([80, 150, 42]);
loggingIdentity3(["Чай"]);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false logging.ts
logging.ts(2,19): error TS2339: Property 'length' does not exist on type 'Type'.
$ node logging.ts
3
1
```

У посібнику всі три функції звуться `loggingIdentity`. Ми додали до назв цифри, щоб вони вмістилися в одному файлі.

Компілятор позначив лише першу функцію. Повідомлення каже, що в типі `Type` немає поля `length`. Причина в тому, що
замість `Type` можуть підставити будь-який тип, наприклад число, а в числа довжини немає. Тіло дженерик-функції
компілятор перевіряє так, ніби `Type` може виявитися чим завгодно, і дозволяє лише те, що законно для всіх типів.

Друга й третя функції правильні. Тепер параметр є масивом елементів типу `Type`, а довжина є в будь-якого масиву.
Записи `Type[]` і `Array<Type>` означають одне й те саме. Автори пропонують читати заголовок другої функції так: вона
бере параметр типу `Type` і масив елементів цього типу, а повертає масив елементів того самого типу. Отже, параметр
типу може бути частиною більшого типу, а не лише цілим типом параметра. Інший спосіб виправити цю помилку, обмеження,
показано в розділі `Generic Constraints` нижче.

### Generic Types

Тут автори записують **тип** самої дженерик-функції, тобто опис, який можна дати змінній, у якій лежить така функція.
Вони показують кілька записів одного й того самого типу, а потім переносять його в інтерфейс. Ось усі ці записи в
одному файлі, `generic-types.ts`:

```ts
function identity<Type>(arg: Type): Type {
  return arg;
}

let myIdentity: <Type>(arg: Type) => Type = identity;
let myIdentity2: <Input>(arg: Input) => Input = identity;
let myIdentity3: { <Type>(arg: Type): Type } = identity;

interface GenericIdentityFn {
  <Type>(arg: Type): Type;
}
let anyType: GenericIdentityFn = identity;

// У посібнику цей інтерфейс теж зветься GenericIdentityFn.
// Тут назву змінено, щоб обидва описи вмістилися в одному файлі.
interface GenericIdentityFnOf<Type> {
  (arg: Type): Type;
}
let onlyNumbers: GenericIdentityFnOf<number> = identity;

console.log(anyType(5), anyType("чай"));
console.log(onlyNumbers(5), onlyNumbers("чай"));
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false generic-types.ts
generic-types.ts(22,41): error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
$ node generic-types.ts
5 чай
5 чай
```

Розберемо записи по черзі.

- `<Type>(arg: Type) => Type` читається так: функція, яка має власний параметр типу `Type`, приймає значення цього
  типу й повертає значення того самого типу. Кутові дужки стоять перед дужками параметрів, як і в оголошенні функції.
- У запису для `myIdentity2` параметр типу має іншу назву, `Input`. Автори пояснюють, що назва не важлива. Важливо
  лише, щоб кількість параметрів типу збігалася і щоб вони стояли на тих самих місцях.
- Запис для `myIdentity3` описує той самий тип як об'єктний тип у фігурних дужках. Усередині стоїть **сигнатура
  виклику**, тобто запис про те, з якими аргументами значення можна викликати як функцію. Цей термін пояснює вчорашній
  розбір у розділі `Static type-checking`.
- Інтерфейс `GenericIdentityFn` переносить ту саму сигнатуру виклику в інтерфейс із назвою.

Інтерфейс `GenericIdentityFnOf` показує другий спосіб перенести тип в інтерфейс, і виклики наприкінці файла показують,
чим два способи відрізняються. У першому інтерфейсі параметр типу стоїть на сигнатурі виклику. Тому функція лишається
дженериком, і кожен виклик `anyType` добирає `Type` заново: `anyType(5)` і `anyType("чай")` обидва законні. У другому
інтерфейсі параметр стоїть на самому інтерфейсі. Тип задають один раз, коли пишуть `GenericIdentityFnOf<number>`, і
далі функція приймає лише числа. Тому компілятор відхилив виклик `onlyNumbers("чай")`. Автори кажуть про це так: сама
сигнатура тепер не дженерик, а частина дженерик-типу. Node надрукував обидва рядки, бо під час роботи в обох змінних
лежить та сама функція `identity`.

Для завдання дня потрібен другий спосіб. Сховище `Store<T>` має кілька методів, і всі вони мусять говорити про той
самий тип: що поклали через `set`, те й отримують через `get`. Параметр на самому інтерфейсі дає саме це. Так само
влаштовано стек `Stack<T>` у лекції, у розділі «Узагальнені типи». Там же показано, яку помилку дає назва такого
інтерфейсу без аргументу типу.

### Generic Classes

**Клас**, як пояснювала лекція дня 1, — це шаблон, за яким оператор `new` створює об'єкти з однаковими полями й
методами. Клас теж може мати параметр типу. Приклад розділу описує клас `GenericNumber` і створює за ним об'єкт для
рядків. Файл `classes.ts`:

```ts
class GenericNumber<NumType> {
  zeroValue: NumType;
  add: (x: NumType, y: NumType) => NumType;
}

let stringNumeric = new GenericNumber<string>();
stringNumeric.zeroValue = "";
stringNumeric.add = function (x, y) {
  return x + y;
};

console.log(stringNumeric.add(stringNumeric.zeroValue, "test"));
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false classes.ts
classes.ts(2,3): error TS2564: Property 'zeroValue' has no initializer and is not definitely assigned in the constructor.
classes.ts(3,3): error TS2564: Property 'add' has no initializer and is not definitely assigned in the constructor.
$ npx tsc --noEmit --strict false --target es2022 --pretty false classes.ts
$ node classes.ts
test
```

У посібнику обидва приклади з цим класом починаються рядком `// @strict: false`. Це ще одна позначка для програми, яка
будує сайт: вона перевіряє приклад із вимкненим суворим режимом. Що таке суворий режим компілятора, пояснює вчорашній
розбір у розділі `Strictness`. Ми прибрали позначку й перевірили код із `--strict`, як і решту прикладів. Компілятор
дав дві помилки `TS2564`, і вони стосуються не дженериків.

Повідомлення каже, що поле не має **початкового значення** і не отримує значення в конструкторі. **Конструктор** — це
функція класу, яку `new` викликає, щоб заповнити щойно створений об'єкт. У цьому класі конструктора немає, і поля
`zeroValue` й `add` після `new` дорівнюють `undefined`, хоча тип обіцяє рядок і функцію. Суворий режим не дозволяє
такої розбіжності. З прапорцем `--strict false` компілятор нічого не надрукував, тобто для м'якого режиму приклад
правильний. Node надрукував `test`, бо `add` склеїв порожній рядок `zeroValue` з рядком `"test"`.

Наприкінці розділу автори кажуть, що параметр класу бачать лише поля й методи об'єктів. **Статичні** поля, тобто ті,
що належать самому класу, а не його об'єктам, параметра типу не бачать. У фазі 0 класи не потрібні. Документація React
теж радить писати компоненти функціями, а не класами.

### Generic Constraints

Тут автори виправляють першу функцію `loggingIdentity` іншим способом: вони додають **обмеження**. Що означає слово
`extends` у такому записі, пояснює лекція в розділі «Обмеження: `extends`». Файл `lengthwise.ts` містить код розділу,
а виклики з рядком і масивом ми додали самі:

```ts
interface Lengthwise {
  length: number;
}

function loggingIdentity<Type extends Lengthwise>(arg: Type): Type {
  console.log(arg.length);
  return arg;
}

loggingIdentity({ length: 10, value: 3 });
loggingIdentity("чай");
loggingIdentity([80, 150]);
loggingIdentity(3);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false lengthwise.ts
lengthwise.ts(13,17): error TS2345: Argument of type 'number' is not assignable to parameter of type 'Lengthwise'.
$ node lengthwise.ts
10
3
2
undefined
```

Інтерфейс `Lengthwise` описує вимогу: значення мусить мати числове поле `length`. Об'єкт `{ length: 10, value: 3 }`
проходить, хоча в ньому є зайве поле `value`. Компілятор спершу виводить `Type` як повний тип цього об'єкта, разом із
`value`, а потім перевіряє, чи цей тип має поле `length`. Обмеження вимагає щонайменше цього поля й не забороняє
інших. Рядок і масив теж мають `length`, тому проходять.

Число довжини не має, і компілятор відхилив виклик `loggingIdentity(3)`. Останній рядок виводу Node показує, від чого
захищає ця помилка. Node типів не перевіряє, тому виконав і цей виклик, а `arg.length` для числа дав `undefined`.

### Using Type Parameters in Generic Constraints

Це найкорисніший розділ для завдання дня. Один параметр типу може обмежувати інший. Автори пишуть функцію, яка читає
поле об'єкта за назвою, і хочуть, щоб компілятор не пропускав назв, яких в об'єкті немає. Файл `get-property.ts`
містить приклад розділу, а `console.log` ми додали, щоб запустити його:

```ts
function getProperty<Type, Key extends keyof Type>(obj: Type, key: Key) {
  return obj[key];
}

let x = { a: 1, b: 2, c: 3, d: 4 };

console.log(getProperty(x, "a"));
console.log(getProperty(x, "m"));
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false get-property.ts
get-property.ts(8,28): error TS2345: Argument of type '"m"' is not assignable to parameter of type '"a" | "b" | "c" | "d"'.
$ node get-property.ts
1
undefined
```

Повідомлення називає дозволені ключі: `"a" | "b" | "c" | "d"`. Це і є `keyof Type`, коли `Type` дорівнює типу
об'єкта `x`. Компілятор спершу визначив `Type` з першого аргументу, потім обчислив `keyof Type`, а потім перевірив за
цим списком другий аргумент. Покроково цей порядок розібрано в лекції, у розділі «`keyof` і `T[K]`: доступ за назвою
поля», на функції `pluck`. Node надрукував `undefined` для `"m"`, бо обмеження існує лише для компілятора. Лекція
показує те саме в розділі «Типові хибні уявлення». Той самий запис `K extends keyof T` стоїть у функції `pick` із
завдання дня.

### Using Class Types in Generics

Розділ показує, як передати у функцію сам клас, щоб функція створила за ним об'єкт. Перший приклад розділу — функція
`create`. Ми додали до неї невеликий клас `Cart`, схожий на кошик із лекції дня 1, і два виклики. Файл `create.ts`:

```ts
function create<Type>(c: { new (): Type }): Type {
  return new c();
}

class Cart {
  count = 0;
}

const cart = create(Cart);
cart.count += 1;
console.log(cart);
const wrong: string = create(Cart);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false create.ts
create.ts(12,7): error TS2322: Type 'Cart' is not assignable to type 'string'.
$ node create.ts
Cart { count: 1 }
```

Запис `{ new (): Type }` описує значення, яке можна викликати через `new` без аргументів і отримати об'єкт типу
`Type`. Клас `Cart` саме таке значення, тому компілятор вивів `Type = Cart`. Повідомлення про змінну `wrong` це
підтверджує: функція повертає `Cart`, а не рядок. Решта розділу будує довший приклад на наслідуванні класів, тобто на
створенні одного класу на основі іншого. У цьому плані наслідування не потрібне, тому решту розділу можна пропустити.

### Generic Parameter Defaults

Параметр типу може мати **значення за замовчуванням**, наприклад `<T = HTMLDivElement>`. Його беруть, коли тип не
вказано й вивести його нема з чого. Автори пояснюють це на функції, яка створює елемент сторінки. Без аргументів вона
створює блок `div`. З елементом в аргументі вона повертає елемент того самого типу. Типи `HTMLElement`,
`HTMLDivElement` і `HTMLParagraphElement` описують елементи сторінки в браузері. Компілятор має їхні описи й без
жодних прапорців.

Спершу автори показують, як таку функцію описували раніше, через **перевантаження**. Так називають кілька оголошень
однієї функції з різними наборами параметрів. Компілятор порівнює виклик з оголошеннями по черзі й бере перше, яке
підходить. Записи `declare function` лише кажуть компілятору, що така функція десь існує, і тіла не мають. Вчорашній
розбір згадував їх в абзаці «Службові рядки в прикладах посібника». Файл `overloads.ts` містить код посібника, а два
виклики й рядки з `never` ми додали самі:

```ts
type Container<T, U> = {
  element: T;
  children: U;
};

declare function create(): Container<HTMLDivElement, HTMLDivElement[]>;
declare function create<T extends HTMLElement>(element: T): Container<T, T[]>;
declare function create<T extends HTMLElement, U extends HTMLElement>(
  element: T,
  children: U[]
): Container<T, U[]>;

const div = create();
const p = create(new HTMLParagraphElement());

const a: never = div;
const b: never = p;
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false overloads.ts
overloads.ts(16,7): error TS2322: Type 'Container<HTMLDivElement, HTMLDivElement[]>' is not assignable to type 'never'.
overloads.ts(17,7): error TS2322: Type 'Container<HTMLParagraphElement, HTMLParagraphElement[]>' is not assignable to type 'never'.
```

Потім автори замінюють три оголошення одним, у якому обидва параметри типу мають значення за замовчуванням. Файл
`defaults.ts`:

```ts
type Container<T, U> = {
  element: T;
  children: U;
};

declare function create<T extends HTMLElement = HTMLDivElement, U extends HTMLElement[] = T[]>(
  element?: T,
  children?: U
): Container<T, U>;

const div = create();
const p = create(new HTMLParagraphElement());

const a: never = div;
const b: never = p;
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false defaults.ts
defaults.ts(14,7): error TS2322: Type 'Container<HTMLDivElement, HTMLDivElement[]>' is not assignable to type 'never'.
defaults.ts(15,7): error TS2322: Type 'Container<HTMLParagraphElement, HTMLParagraphElement[]>' is not assignable to type 'never'.
```

Типи вийшли ті самі, що з трьома оголошеннями. Простежимо, звідки вони взялися. Виклик `create()` не має аргументів,
тому вивести `T` нема з чого, і компілятор бере значення за замовчуванням `HTMLDivElement`. Значення за замовчуванням
для `U` записано через попередній параметр, `T[]`, тому `U` стає `HTMLDivElement[]`. У виклику
`create(new HTMLParagraphElement())` компілятор виводить `T` з аргументу. Другого аргументу немає, тому `U` знову
береться за замовчуванням і дорівнює `T[]`, тобто `HTMLParagraphElement[]`.

Ці два файли ми лише перевірили компілятором, а не запускали. Функція `create` не має тіла, а в Node немає елементів
сторінки. Крім того, у браузері запис `new HTMLParagraphElement()` не працює. Ми перевірили його в Chrome 157, і
браузер кинув помилку `TypeError: Failed to construct 'HTMLParagraphElement': Illegal constructor`. Справжній абзац
створюють викликом `document.createElement("p")`. Посібникові цей запис потрібен лише для того, щоб показати тип.

Далі автори перелічують правила. Перевіримо чотири з них. Файл `default-rules.ts`:

```ts
function pair<A, B = unknown>(a: A, b: B): [A, B] {
  return [a, b];
}

const inferred = pair(1, "два");
const onlyA = pair<number>(1, "два");

const x: never = inferred;
const y: never = onlyA;

function wrongOrder<A = string, B>(a: A, b: B) {}
function wrongDefault<T extends string = number>(value: T) {}
console.log(onlyA);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false default-rules.ts
default-rules.ts(8,7): error TS2322: Type '[number, string]' is not assignable to type 'never'.
default-rules.ts(9,7): error TS2322: Type '[number, unknown]' is not assignable to type 'never'.
default-rules.ts(11,33): error TS2706: Required type parameters may not follow optional type parameters.
default-rules.ts(12,42): error TS2344: Type 'number' does not satisfy the constraint 'string'.
$ node default-rules.ts
[ 1, 'два' ]
```

- **Параметр зі значенням за замовчуванням стає необов'язковим.** Тому виклик `pair<number>(1, "два")` вказує лише
  `A`, і компілятор не скаржиться. Лекція в розділі «Як компілятор добирає `T`» показує, що без значення за
  замовчуванням такий виклик дає помилку `Expected 2 type arguments, but got 1`.
- **Невказаний параметр бере значення за замовчуванням, а не виводиться з аргументу.** Друге повідомлення показує
  наслідок: `B` дорівнює `unknown`, хоча другим аргументом передано рядок. Отже, часткового виведення немає й тут.
  Коли вказано хоч один параметр типу, компілятор нічого не виводить, а решту бере за замовчуванням. Без кутових дужок
  компілятор вивів обидва параметри, і перше повідомлення показує `[number, string]`. Node надрукував справжній
  рядок, бо під час роботи типів немає.
- **Обов'язковий параметр не може стояти після необов'язкового.** Це повідомлення `TS2706` до функції `wrongOrder`.
- **Значення за замовчуванням мусить відповідати обмеженню.** Це повідомлення `TS2344` до функції `wrongDefault`:
  число не є рядком.

Останні два правила списку стосуються **злиття оголошень**. Так називають випадок, коли один інтерфейс оголошено
кілька разів, і компілятор зводить ці оголошення в одне. У цьому плані таке не трапляється.

У React цей прийом теж є. Пакет `@types/react` версії 19.3.0 описує `useState` двома оголошеннями, тобто через
перевантаження:

```ts
function useState<S>(initialState: S | (() => S)): [S, Dispatch<SetStateAction<S>>];
function useState<S = undefined>(): [S | undefined, Dispatch<SetStateAction<S | undefined>>];
```

Друге оголошення спрацьовує, коли `useState` викликають без аргументу. Ось що з цього виходить. Файл
`state-default.ts`:

```ts
import { useState } from "react";

export function Hooks() {
  const [nothing] = useState();
  const [name] = useState<string>();

  const a: never = nothing;
  const b: never = name;
}
```

```text
$ npm i -D @types/react
$ npx tsc --noEmit --strict --target es2022 --pretty false state-default.ts
state-default.ts(7,9): error TS2322: Type 'undefined' is not assignable to type 'never'.
state-default.ts(8,9): error TS2322: Type 'string | undefined' is not assignable to type 'never'.
  Type 'undefined' is not assignable to type 'never'.
```

Перша команда ставить у теку проєкту пакет `@types/react`, бо без нього компілятор не знає, що таке `useState`.
Виклик без аргументу й без кутових дужок дав `S = undefined`, тому в такому стані може лежати лише `undefined`. Виклик
`useState<string>()` дав `string | undefined`: рядок там може з'явитися пізніше, але початкового значення не передано,
тому спершу стан дорівнює `undefined`. Запускати цей файл у Node немає сенсу, бо хук працює лише всередині компонента,
який показує React.

### Variance Annotations

Цей розділ можна пропустити, але його думка пояснює, чому компілятор інколи не дає підставити один дженерик-тип
замість іншого. Автори пояснюють, коли дженерик-тип для одного типу можна підставити туди, де чекають дженерик-тип
для іншого. Вони беруть два інтерфейси:
`Producer<T>` має метод, який створює значення типу `T`, а `Consumer<T>` має метод, який приймає значення типу `T`.
Типи `Animal` і `Cat` посібник не описує, тому ми описали їх самі. Файл `variance.ts`:

```ts
type Animal = { name: string };
type Cat = { name: string; meow(): string };

interface Producer<T> {
  make(): T;
}
interface Consumer<T> {
  consume: (arg: T) => void;
}

const catMaker: Producer<Cat> = {
  make: () => ({ name: "Мурка", meow: () => "Няв" }),
};
const animalMaker: Producer<Animal> = {
  make: () => ({ name: "Сірко" }),
};

const p1: Producer<Animal> = catMaker;
const p2: Producer<Cat> = animalMaker;

const animalEater: Consumer<Animal> = { consume: (a) => console.log(a.name) };
const catEater: Consumer<Cat> = { consume: (c) => console.log(c.meow()) };

const c1: Consumer<Cat> = animalEater;
const c2: Consumer<Animal> = catEater;

c2.consume({ name: "Сірко" });
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false variance.ts
variance.ts(19,7): error TS2322: Type 'Producer<Animal>' is not assignable to type 'Producer<Cat>'.
  Property 'meow' is missing in type 'Animal' but required in type 'Cat'.
variance.ts(25,7): error TS2322: Type 'Consumer<Cat>' is not assignable to type 'Consumer<Animal>'.
  Property 'meow' is missing in type 'Animal' but required in type 'Cat'.
$ node variance.ts
TypeError: c.meow is not a function
```

Кожен кіт є твариною, бо має поле `name`. Тому об'єкт, який створює котів, годиться туди, де чекають об'єкт, який
створює тварин: рядок із `p1` пройшов. Навпаки не можна, і компілятор відхилив рядок із `p2`. Таке відношення, коли
напрям для `Producer<T>` той самий, що й для `T`, називають **коваріантністю**.

Зі споживачем напрям обернений. Функція, яка вміє обробити будь-яку тварину, обробить і кота, тому рядок із `c1`
пройшов. Функція, яка вміє обробити лише кота, не впорається з будь-якою твариною, і компілятор відхилив рядок із
`c2`. Таке обернене відношення називають **контраваріантністю**. Останній рядок файла показує, що сталося б без цієї
перевірки. Node типів не перевіряє, тому передав функції для котів об'єкт без методу `meow`, і програма впала.

Ці відношення компілятор обчислює сам за будовою типу. Позначки `in` і `out` перед параметром типу дозволяють указати
їх явно. Автори кажуть, що вони потрібні вкрай рідко, і застерігають: не пишіть позначки, яка суперечить справжній
будові типу.

## Keyof Type Operator

**Де читати:** [Keyof Type Operator](https://www.typescriptlang.org/docs/handbook/2/keyof-types.html). У примірнику
`typescript` це `handbook-v2/Type Manipulation/Keyof Type Operator`.

**Що там є.** Це дуже коротка сторінка, яку легко прочитати цілком.

### The `keyof` type operator

Сторінка має два приклади. Ось обидва в одному файлі, а рядки з присвоєнням ми додали, щоб побачити типи. Файл
`keyof.ts`:

```ts
type Point = { x: number; y: number };
type P = keyof Point;

type Arrayish = { [n: number]: unknown };
type A = keyof Arrayish;

type Mapish = { [k: string]: boolean };
type M = keyof Mapish;

const p: P = "z";
const a: A = "0";
const m: M = true;
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false keyof.ts
keyof.ts(10,7): error TS2322: Type '"z"' is not assignable to type 'keyof Point'.
keyof.ts(11,7): error TS2322: Type 'string' is not assignable to type 'number'.
keyof.ts(12,7): error TS2322: Type 'boolean' is not assignable to type 'string | number'.
```

Перший приклад показує головне. Автори кажуть, що `keyof Point` — це той самий тип, що й `"x" | "y"`, тобто
об'єднання літеральних типів, про які йшлося вчора. Тому назва `"z"` не підходить. Сам компілятор у повідомленні
пише тип коротко, `keyof Point`, і не розгортає його.

Другий приклад стосується **індексної сигнатури**. Що це таке, пояснює лекція в розділі «`keyof` і `T[K]`: доступ за
назвою поля». Запис `{ [k: string]: boolean }` описує об'єкт, у якому може бути скільки завгодно полів з будь-якими
рядковими назвами, і значення кожного поля логічне. Ім'я `k` у дужках нічого не означає, воно лише нагадує, що там
стоїть ключ. Для числової сигнатури `Arrayish` оператор `keyof` дає `number`, тому рядок `"0"` не підходить. Для
рядкової сигнатури `Mapish` він дає `string | number`, і це дивує. Автори пояснюють причину: у JavaScript ключі
об'єкта завжди перетворюються на рядки, тому `obj[0]` і `obj["0"]` означають те саме поле. Перевіримо це в Node. Файл
`mapish.ts`:

```ts
const flags: { [k: string]: boolean } = {};
flags[0] = true;
console.log(Object.keys(flags), flags["0"]);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false mapish.ts
$ node mapish.ts
[ '0' ] true
```

Ключ, записаний числом `0`, зберігся як рядок `'0'`, і за рядком `"0"` знайшлося те саме значення. Тому для рядкової
сигнатури числовий ключ теж законний.

Наприкінці сторінка каже, що `keyof` особливо корисний разом зі **зіставленими типами**. Так називають типи, які
перебирають ключі іншого типу й будують поле для кожного. Сторінка не показує прикладу, але лекція в розділі «Службові
типи» розбирає один: так оголошено `Partial`.

Ще два випадки сторінка не розбирає, а вони корисні для читання повідомлень компілятора. Файл `union-keys.ts`:

```ts
type Product = { id: number; name: string };
type Parcel = { id: number; weight: number };

const common: keyof (Product | Parcel) = "name";

const tea = { id: 1, name: "Чай" };
type TeaKey = keyof tea;
type TeaKeyRight = keyof typeof tea;
const key: TeaKeyRight = "price";
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false union-keys.ts
union-keys.ts(4,7): error TS2322: Type '"name"' is not assignable to type '"id"'.
union-keys.ts(7,21): error TS2749: 'tea' refers to a value, but is being used as a type here. Did you mean 'typeof tea'?
union-keys.ts(9,7): error TS2322: Type '"price"' is not assignable to type '"id" | "name"'.
```

**Об'єднання типів.** Значення типу `Product | Parcel` може виявитися будь-яким із двох варіантів. Тому без перевірки
можна читати лише ті поля, які є в обох. Отже, `keyof` для об'єднання дає лише спільні ключі, тут лише `"id"`.

**Значення замість типу.** Оператор `keyof` працює лише з типами, а `tea` — це змінна зі значенням. Компілятор так і
каже: `tea` означає значення, а стоїть там, де очікують тип. Він же підказує виправлення, `typeof tea`. У місці, де
очікують тип, запис `typeof tea` означає тип змінної `tea`. Це не той оператор `typeof`, який під час роботи програми
повертає рядок на кшталт `"object"`. Запис `keyof typeof tea` спершу бере тип змінної, а потім назви його полів, тому
назва `"price"` не підходить.

Чому `Object.keys` повертає `string[]`, а не назви полів, пояснює лекція в розділі «`keyof` і `T[K]`: доступ за назвою
поля».

## Utility Types

**Де читати:** [Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html) у довіднику
TypeScript. У примірнику `typescript` це `reference/Utility Types`.

**Що там є.** Це довідник, а не розповідь. Кожен розділ описує один службовий тип. Після назви стоїть рядок
`Released` з версією TypeScript, у якій цей тип з'явився, далі короткий опис і приклад. Читати довідник варто
частинами.

**Якщо часу мало,** прочитайте `Partial`, `Pick`, `Omit` і `Record`. Для завдання дня цього досить.

**Де лежать оголошення.** Службові типи оголошено у файлі `lib.es5.d.ts`, який постачається разом із компілятором. У
TypeScript 7 цей файл лежить не в пакеті `typescript`, а в окремому пакеті для вашої системи, який npm ставить разом
із ним. У Linux на процесорі x86-64 шлях такий: `node_modules/@typescript/typescript-linux-x64/lib/lib.es5.d.ts`.

Оголошення `Partial`, `Pick` і `Omit` із цього файла наводить і розбирає лекція в розділі «Службові типи». Там же
пояснено, що таке зіставлений тип. Ось ще чотири оголошення з того самого файла у версії 7.0.2:

```ts
type Required<T> = { [P in keyof T]-?: T[P]; };
type Readonly<T> = { readonly [P in keyof T]: T[P]; };
type Record<K extends keyof any, T> = { [P in K]: T; };
type Exclude<T, U> = T extends U ? never : T;
```

У файлі перші три оголошення займають по кілька рядків. Тут кожне стиснуто до одного рядка, а коментарі прибрано.
Перші три рядки — зіставлені типи, і читаються вони так само, як `Partial` у лекції. У `Required` знак `-?` прибирає
позначку необов'язковості з кожного поля. У `Readonly` слово `readonly` забороняє переприсвоювати поле. `Record`
перебирає ключі `K` і дає кожному ключу той самий тип значення `T`.

Рядок з `Exclude` написано іншим записом, який у цьому плані не вивчають. Він називається **умовним типом**, і його
описує окрема глава посібника, Conditional Types. Запис `T extends U ? never : T` читається так: якщо `T` підходить
під `U`, то результат `never`, тобто жодного значення, а інакше результат `T`. Коли замість `T` підставляють
об'єднання, компілятор застосовує цю умову до кожного варіанта окремо, а результати знову збирає в об'єднання.
Примітки до версії 2.8, у якій з'явилися умовні типи, називають такі типи розподільними (distributive conditional
types). Так `Exclude` викидає з об'єднання ті варіанти, які підходять під `U`. Решта службових типів, `Extract`,
`Parameters`, `ReturnType` і подібні, теж є умовними типами, тому їхні оголошення можна не читати.

### `Awaited<Type>`

Цей тип описує те, що дасть `await`. Автори кажуть, що він розгортає проміси так само, як `await` і метод `then`:
якщо в промісі лежить ще один проміс, розгортається й він. Файл `awaited.ts` містить три типи з прикладу довідника, а
функцію `load` ми додали самі:

```ts
const a: Awaited<Promise<string>> = 1;
const b: Awaited<Promise<Promise<number>>> = "x";
const c: Awaited<boolean | Promise<number>> = "x";

async function load() {
  return 42;
}
async function main() {
  const promise = load();
  const value = await promise;
  const p: never = promise;
  const v: never = value;
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false awaited.ts
awaited.ts(1,7): error TS2322: Type 'number' is not assignable to type 'string'.
awaited.ts(2,7): error TS2322: Type 'string' is not assignable to type 'number'.
awaited.ts(3,7): error TS2322: Type '"x"' is not assignable to type 'number | boolean'.
awaited.ts(11,9): error TS2322: Type 'Promise<number>' is not assignable to type 'never'.
awaited.ts(12,9): error TS2322: Type 'number' is not assignable to type 'never'.
```

Подвійний проміс розгорнувся до `number`. В об'єднанні `boolean | Promise<number>` проміс розгорнувся, а `boolean`
лишився, бо це не проміс. Останні два рядки показують зв'язок із `await`: функція `async` повертає `Promise<number>`,
а `await` дає `number`, тобто саме `Awaited<Promise<number>>`.

### `Partial<Type>`

Усі поля стають необов'язковими. Приклад довідника показує типове застосування. Файл `partial.ts` містить код
довідника, а два рядки з `console.log` ми додали:

```ts
interface Todo {
  title: string;
  description: string;
}

function updateTodo(todo: Todo, fieldsToUpdate: Partial<Todo>) {
  return { ...todo, ...fieldsToUpdate };
}

const todo1 = {
  title: "organize desk",
  description: "clear clutter",
};

const todo2 = updateTodo(todo1, {
  description: "throw out trash",
});

console.log(todo1);
console.log(todo2);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false partial.ts
$ node partial.ts
{ title: 'organize desk', description: 'clear clutter' }
{ title: 'organize desk', description: 'throw out trash' }
```

Функція `updateTodo` приймає повний об'єкт і часткові зміни, у яких може бути будь-яке з полів або жодного. Вона
повертає новий об'єкт, зібраний трьома крапками з лекції дня 1, розділ «Що роблять три крапки»: спершу всі поля
старого об'єкта, потім поля змін, які перекривають старі. Старий об'єкт `todo1` лишився без змін. Завдання дня містить
таку функцію, `applyEdit`, готовою. Пастку з явним `undefined` у частковому об'єкті розбирає лекція в розділі
«Службові типи».

### `Required<Type>`

Це протилежне до `Partial`: усі поля стають обов'язковими. Файл `required.ts` містить приклад довідника:

```ts
interface Props {
  a?: number;
  b?: string;
}

const obj: Props = { a: 5 };

const obj2: Required<Props> = { a: 5 };
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false required.ts
required.ts(8,7): error TS2741: Property 'b' is missing in type '{ a: number; }' but required in type 'Required<Props>'.
```

Знак питання після назви поля означає, що поле можна пропустити. Тому для `Props` вистачає одного поля `a`. Тип
`Required<Props>` прибрав ці знаки, і компілятор повідомив, що поля `b` бракує.

### `Readonly<Type>`

Поля нового типу не можна переприсвоїти. Файл `readonly.ts` містить приклад довідника, а рядки з `Object.freeze` ми
додали самі:

```ts
interface Todo {
  title: string;
}

const todo: Readonly<Todo> = {
  title: "Delete inactive users",
};

todo.title = "Hello";

const frozen = Object.freeze({ title: "Delete inactive users" });
frozen.title = "Hello";

console.log(todo.title, "|", frozen.title);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false readonly.ts
readonly.ts(9,6): error TS2540: Cannot assign to 'title' because it is a read-only property.
readonly.ts(12,8): error TS2540: Cannot assign to 'title' because it is a read-only property.
$ node readonly.ts
Hello | Delete inactive users
```

Автори кажуть, що цей тип описує присвоєння, які не вдадуться під час роботи, зокрема присвоєння полю замороженого
об'єкта. Підрозділ `Object.freeze` показує, як описано цей метод: `function freeze<Type>(obj: Type): Readonly<Type>`.
Тому компілятор відхилив обидва присвоєння однаковим повідомленням.

Вивід Node показує різницю між типом і методом. Об'єкт `todo` лише має тип `Readonly`, тому присвоєння виконалося, і
поле стало `Hello`. Те, що `Readonly` існує лише для компілятора, показує й лекція в розділі «Службові типи». Об'єкт
`frozen` справді заморожено, тому його поле не змінилося. Помилки під час роботи при цьому не було, бо файл виконано
без суворого режиму JavaScript. Чому так і як заморожений об'єкт поводиться в суворому режимі, пояснює лекція дня 2 в
розділі «`Object.freeze`: як перевірити, що нічого не змінюється».

### `Record<Keys, Type>`

Цей тип описує об'єкт із ключами `Keys` і значеннями `Type`. Файл `record.ts` містить приклад довідника, а об'єкт
`fewer` без третього ключа ми додали:

```ts
type CatName = "miffy" | "boris" | "mordred";

interface CatInfo {
  age: number;
  breed: string;
}

const cats: Record<CatName, CatInfo> = {
  miffy: { age: 10, breed: "Persian" },
  boris: { age: 5, breed: "Maine Coon" },
  mordred: { age: 16, breed: "British Shorthair" },
};

const fewer: Record<CatName, CatInfo> = {
  miffy: { age: 10, breed: "Persian" },
  boris: { age: 5, breed: "Maine Coon" },
};

console.log(cats.boris);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false record.ts
record.ts(14,7): error TS2741: Property 'mordred' is missing in type '{ miffy: { age: number; breed: string; }; boris: { age: number; breed: string; }; }' but required in type 'Record<CatName, CatInfo>'.
$ node record.ts
{ age: 5, breed: 'Maine Coon' }
```

Тип `CatName` є об'єднанням трьох імен, тому `Record<CatName, CatInfo>` вимагає всі три ключі. Компілятор назвав ключ,
якого бракує в `fewer`. Запис `Record<string, number>` поводиться інакше: ключів там безліч, і компілятор не може
вимагати кожного. Пастку, яка з цього випливає, показує лекція в розділі «Службові типи».

### `Pick<Type, Keys>` і `Omit<Type, Keys>`

`Pick` лишає лише названі поля, а `Omit` прибирає названі поля. Файл `pick-omit.ts` містить типи з прикладів
довідника, а об'єкти з помилками ми написали самі:

```ts
interface Todo {
  title: string;
  description: string;
  completed: boolean;
  createdAt: number;
}

type TodoPreview = Pick<Todo, "title" | "completed">;
type TodoWithoutDescription = Omit<Todo, "description">;
type TodoInfo = Omit<Todo, "completed" | "createdAt">;

const preview: TodoPreview = {
  title: "Clean room",
  completed: false,
  createdAt: 1615544252770,
};

const info: TodoInfo = {
  title: "Pick up kids",
};
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false pick-omit.ts
pick-omit.ts(15,3): error TS2353: Object literal may only specify known properties, and 'createdAt' does not exist in type 'TodoPreview'.
pick-omit.ts(18,7): error TS2741: Property 'description' is missing in type '{ title: string; }' but required in type 'TodoInfo'.
```

`TodoPreview` — це коротка версія `Todo` для списку, з двома полями. Поле `createdAt` у ній уже зайве. Чому компілятор
не дозволяє зайвого поля в літералі об'єкта, пояснює лекція дня 9 у розділі «Як записують типи». Інтерфейс `Todo` ми
взяли з прикладу для `Omit`, бо там є ще поле `createdAt`. У тому прикладі тип `Omit<Todo, "description">` теж зветься
`TodoPreview`, як і тип із прикладу для `Pick`. Ми дали йому окрему назву `TodoWithoutDescription`, щоб обидва типи
вмістилися в одному файлі. `TodoInfo` лишив поля `title` і `description`, тому
об'єкту `info` бракує опису.

Завдання дня використовує `Pick` у типі результату функції `pick`. Чому `Pick` перевіряє назви полів, а `Omit` ні,
пояснює лекція в розділі «Службові типи»: у `Pick` стоїть обмеження `K extends keyof T`, а в `Omit` обмеження
`K extends keyof any`, тобто будь-який можливий ключ. Там же показано, що описка в назві поля для `Omit` проходить
непомітно.

### `Exclude<UnionType, ExcludedMembers>`, `Extract<Type, Union>` і `NonNullable<Type>`

Ці три типи працюють із варіантами об'єднання, а не з полями об'єкта. `Exclude` прибирає варіанти, які підходять під
другий параметр. `Extract` робить протилежне: лишає лише такі варіанти. `NonNullable` прибирає `null` і `undefined`.
Файл `unions.ts` містить типи з прикладів довідника, а значення з помилками ми підібрали самі:

```ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; x: number }
  | { kind: "triangle"; x: number; y: number };

const t1: Exclude<"a" | "b" | "c", "a" | "b"> = "a";
const t3: Exclude<Shape, { kind: "circle" }> = { kind: "circle", radius: 1 };
const t0: Extract<"a" | "b" | "c", "a" | "f"> = "b";
const t2: Extract<Shape, { kind: "circle" }> = { kind: "square", x: 1 };
const n1: NonNullable<string[] | null | undefined> = null;
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false unions.ts
unions.ts(6,7): error TS2322: Type '"a"' is not assignable to type '"c"'.
unions.ts(7,50): error TS2322: Type '"circle"' is not assignable to type '"square" | "triangle"'.
unions.ts(8,7): error TS2322: Type '"b"' is not assignable to type '"a"'.
unions.ts(9,50): error TS2322: Type '"square"' is not assignable to type '"circle"'.
unions.ts(10,7): error TS2322: Type 'null' is not assignable to type 'string[]'.
```

Тип `Shape` — розрізнюване об'єднання з лекції дня 9, розділ «Розрізнюване об'єднання: варіанти зі спільним полем»:
кожен варіант має власне значення поля `kind`. Повідомлення
до рядка 7 показує, що `Exclude` прибрав цілий варіант кола, і лишилися квадрат і трикутник. `Extract` у рядку 9,
навпаки, лишив тільки коло. У рядку 8 `Extract` лишив лише `"a"`, бо `"f"` у першому об'єднанні й не було.

Не плутайте `Exclude` з `Omit`. `Exclude` прибирає варіанти з об'єднання, а `Omit` прибирає поля з об'єктного типу.
Оголошення `Omit`, яке наводить лекція в розділі «Службові типи», показує, як вони пов'язані: `Omit` бере об'єднання
назв полів `keyof T`, викидає з нього непотрібні назви через `Exclude`, а решту передає в `Pick`.

### `Parameters<Type>` і `ReturnType<Type>`

`Parameters` збирає типи аргументів функції в **кортеж**, тобто масив фіксованої довжини, у якому кожне місце має свій
тип. Кортеж пояснює вчорашній розбір у розділі `Arrays`. `ReturnType` дає тип результату функції. Він зручний, коли
функцію написав хтось інший, а окремої назви для її результату немає. Приклади довідника для цих типів довгі й містять
багато особливих випадків, тому ми взяли власний приклад. Файл `functions.ts`:

```ts
function total(price: number, count: number): string {
  return String(price * count);
}

type TotalArgs = Parameters<typeof total>;
type TotalResult = ReturnType<typeof total>;

const args: TotalArgs = [80, 3];
console.log(total(...args));

const short: Parameters<typeof total> = [80];
const result: ReturnType<typeof total> = 5;
const wrong: ReturnType<total> = "240";
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false functions.ts
functions.ts(11,7): error TS2322: Type '[number]' is not assignable to type '[price: number, count: number]'.
  Source has 1 element(s) but target requires 2.
functions.ts(12,7): error TS2322: Type 'number' is not assignable to type 'string'.
functions.ts(13,25): error TS2749: 'total' refers to a value, but is being used as a type here. Did you mean 'typeof total'?
$ node functions.ts
240
```

Обидва типи приймають тип функції, а не саму функцію. Тому пишуть `typeof total`, як у розділі про `keyof` вище.
Останній рядок без `typeof` дав ту саму помилку `TS2749`, що й там. Кортеж у першому повідомленні містить назви
параметрів, `price` і `count`. Вони лише допомагають читати тип і нічого не перевіряють. Типи `ConstructorParameters`
і `InstanceType` роблять те саме для класу: перший дає типи аргументів конструктора, а другий тип об'єкта, який
створює клас.

### `NoInfer<Type>`

Цей тип з'явився у версії 5.4. Він забороняє компілятору виводити параметр типу з цього місця. В усьому іншому
`NoInfer<C>` означає те саме, що й `C`. Файл `noinfer.ts` містить приклад довідника, а функцію `createLoose` без
`NoInfer` ми додали для порівняння:

```ts
function createStreetLight<C extends string>(
  colors: C[],
  defaultColor?: NoInfer<C>,
) {
  // ...
}

createStreetLight(["red", "yellow", "green"], "red");  // OK
createStreetLight(["red", "yellow", "green"], "blue");  // Error

function createLoose<C extends string>(colors: C[], defaultColor?: C) {}
createLoose(["red", "yellow", "green"], "blue");
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false noinfer.ts
noinfer.ts(9,47): error TS2345: Argument of type '"blue"' is not assignable to parameter of type '"green" | "red" | "yellow" | undefined'.
```

Функція описує світлофор. Список кольорів задає, які кольори можливі, а колір за замовчуванням має бути одним із них.
У функції `createLoose` компілятор збирає кандидатів для `C` з обох аргументів. Тому `"blue"` теж став можливим
кольором, і помилки немає. У `createStreetLight` другий аргумент загорнуто в `NoInfer`, тому `C` виводиться лише зі
списку, а `"blue"` лише перевіряється за цим списком. Сьогодні цей тип не потрібен.

### `ThisParameterType<Type>`, `OmitThisParameter<Type>` і `ThisType<Type>`

Ці три типи працюють зі словом `this` у функціях і методах. У цьому плані вони не знадобляться, тому розділи можна
пропустити.

### Intrinsic String Manipulation Types

`Uppercase`, `Lowercase`, `Capitalize` і `Uncapitalize` змінюють літеральні рядки на рівні типів. Довідник лише
називає їх і відсилає до сторінки Template Literal Types. Файл `strings.ts`:

```ts
const loud: Uppercase<"чай"> = "чай";
const drink: Capitalize<"кава"> = "Кава";
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false strings.ts
strings.ts(1,7): error TS2322: Type '"чай"' is not assignable to type '"ЧАЙ"'.
```

`Uppercase<"чай">` дорівнює `"ЧАЙ"`, тому рядок малими літерами не підійшов. `Capitalize<"кава">` дорівнює `"Кава"`,
і другий рядок пройшов. У цьому плані ці типи не потрібні.

## How to Design Programs: 3.1 Designing Functions

**Де читати:** [розділ 3.1 книжки](https://htdp.org/2024-11-6/Book/part_one.html#%28part._sec~3adesign-func%29). У
примірнику `htdp` це розділ `3.1 Designing Functions`. Вчорашній розбір уже переказав цей розділ, тому тут важливо
лише, що змінюється для дженериків. Текст книжки тут лише коротко переказано.

**Якщо часу мало,** досить прочитати абзаци нижче.

### The Design Process

Шість кроків рецепта лишаються тими самими. Змінюється лише те, що функція й опис даних тепер можуть мати параметр
типу.

Перший крок, опис даних, сам може мати параметр. Сховище з завдання дня описують як `Store<T>`, і цей тип годиться для
чисел, задач чи будь-чого іншого.

Другий крок — сигнатура, призначення й заглушка. Сигнатура отримує кутові дужки з параметрами типу. Речення про
призначення каже, що саме параметр зв'язує, наприклад: «повертає об'єкт лише з тими полями `obj`, назви яких
передано в `keys`».

Третій крок — приклади. Тепер потрібні приклади для різних типів, щоб перевірити, що функція справді не залежить від
конкретного типу. Крім того, потрібні приклади для компілятора: рядки, які мусять не компілюватися, наприклад виклик з
неправильною назвою поля. Над кожним таким рядком пишуть коментар `// @ts-expect-error`. Він каже компілятору, що в
наступному рядку очікується помилка. Якщо помилка є, компілятор мовчить. Якщо помилки немає, компілятор сам повідомляє
про це. Файл `expect.ts`:

```ts
function last<T>(list: T[]): T | undefined {
  return list[list.length - 1];
}

// Цю функцію ніхто не викликає: її рядки читає лише компілятор.
function typeExamples(): void {
  // @ts-expect-error: у рядка немає методу toFixed
  last(["Чай"])?.toFixed(2);

  // @ts-expect-error: тут помилки немає, і компілятор про це скаже
  last([80])?.toFixed(2);
}

console.log(last([80, 150]));
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false expect.ts
expect.ts(10,3): error TS2578: Unused '@ts-expect-error' directive.
$ node expect.ts
150
```

Перший приклад справді помилковий, тому компілятор про нього мовчить. Другий приклад правильний, і компілятор
повідомив, що коментар `@ts-expect-error` над ним зайвий. Такі рядки кладуть у функцію, яку ніхто не викликає. Інакше
Node виконав би їх, і програма впала б на першому ж, бо в рядка немає методу `toFixed`. Файл прикладів завдання дня
влаштовано так само.

Четвертий крок — перелік вхідних даних. Крім параметрів, сюди входить те, що живе між викликами, наприклад поточне
значення сховища, яке зберігає замикання з лекції дня 3.

П'ятий крок — код. Тіло дженерик-функції не може залежати від конкретного типу, бо заздалегідь його не знає. Воно може
користуватися лише тим, що дозволяє обмеження, як у розділі `Generic Constraints` вище.

Шостий крок — перевірка. Команда `tsc` перевіряє типи, а команда `node --test` перевіряє поведінку. Одна з них не
замінює іншої: приклад `get-property.ts` вище показав, що функція з правильними типами може повернути `undefined`.

Сама книжка повертається до цієї теми пізніше, у частині про абстракцію. Розділ [14.3 Similarities in Data
Definitions](https://htdp.org/2024-11-6/Book/part_three.html) показує два майже однакові означення списку, для чисел і
для рядків. Вони відрізняються лише одним місцем, типом елемента. Автори роблять це місце параметром і отримують одне
означення `[List-of ITEM]`. Це та сама думка, що лежить в основі `Array<T>`. Розділ `15.2 Similarities in Signatures`
робить те саме із сигнатурами функцій. Обидва розділи не входять у завдання дня.

## Додатково: Guidelines for Writing Good Generic Functions

**Де читати:** однойменний розділ сторінки [More on
Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html). Його немає в обов'язковому списку, але саме
він підтримує пастку цього дня. Автори попереджають, що зайві параметри типу й зайві обмеження заважають компілятору
виводити типи. Розділ містить три короткі правила.

**Push Type Parameters Down.** Назву правила можна перекласти як «опускайте параметри типу нижче». Автори порівнюють
дві схожі функції. Файл `first.ts`:

```ts
function firstElement1<Type>(arr: Type[]) {
  return arr[0];
}

function firstElement2<Type extends any[]>(arr: Type) {
  return arr[0];
}

const a = firstElement1([1, 2, 3]);
const b = firstElement2([1, 2, 3]);

const checkA: never = a;
const checkB: never = b;
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false first.ts
first.ts(12,7): error TS2322: Type 'number' is not assignable to type 'never'.
first.ts(13,7): error TS2322: Type 'any' is not assignable to type 'never'.
```

Перша функція дала `number`, а друга `any`, тобто перевірку вимкнено. Автори пояснюють різницю. У першій функції
параметр типу стоїть на елементі масиву, і компілятор підставляє справжній тип елемента під час виклику. У другій
параметр типу означає весь масив, а тип результату `arr[0]` компілятор обчислює заздалегідь, з обмеження `any[]`. Тому
результат завжди `any`. Правило звучить так: де можна, беріть сам параметр типу, а не обмеження.

**Use Fewer Type Parameters.** Друге правило: беріть якомога менше параметрів типу. Ось дві функції з розділу, а
виклики ми додали самі. Файл `filter.ts`:

```ts
function filter1<Type>(arr: Type[], func: (arg: Type) => boolean): Type[] {
  return arr.filter(func);
}

function filter2<Type, Func extends (arg: Type) => boolean>(
  arr: Type[],
  func: Func
): Type[] {
  return arr.filter(func);
}

const cheap1 = filter1<number>([80, 150, 42], (p) => p < 100);
const cheap2 = filter2<number>([80, 150, 42], (p) => p < 100);
console.log(cheap1);
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false filter.ts
filter.ts(13,24): error TS2558: Expected 2 type arguments, but got 1.
filter.ts(13,54): error TS2365: Operator '<' cannot be applied to types 'Type' and 'number'.
$ node filter.ts
[ 80, 42 ]
```

Параметр `Func` у другій функції не зв'язує двох значень: він трапляється лише в одному місці. Автори кажуть, що це
завжди тривожна ознака. Наслідок видно в першому повідомленні: хто хоче вказати тип явно, мусить вказати й зайвий
`Func`. Друге повідомлення — наслідок першого. Виклик не вдався, тому компілятор так і не підставив `number` замість
`Type` у тип параметра `p`.

**Type Parameters Should Appear Twice.** Третє правило: якщо параметр типу трапляється лише в одному місці, майже
напевно він не потрібен. Лекція розбирає це правило в розділі «Коли дженерик не потрібен». Приклад розділу — функція
`greet` і її простіша версія. Ми назвали простішу версію `greetPlain`, бо в посібнику обидві звуться `greet`, а
функцію `echo` додали самі. Файл `greet.ts`:

```ts
function greet<Str extends string>(s: Str) {
  console.log("Hello, " + s);
}

greet("world");

function greetPlain(s: string) {
  console.log("Hello, " + s);
}

greetPlain("world");

function echo<Str extends string>(s: Str) {
  return s;
}

const word = echo("world");
const check: never = word;
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false greet.ts
greet.ts(18,7): error TS2322: Type '"world"' is not assignable to type 'never'.
$ node greet.ts
Hello, world
Hello, world
```

Функції `greet` і `greetPlain` працюють однаково, і компілятор не має до них претензій. Параметр `Str` у `greet`
стоїть лише в типі аргументу й нічого ні з чим не зв'язує, тому простіша версія краща. Автори додають одне уточнення:
тип результату, який компілятор вивів сам, теж рахується. Функція `echo` показує такий випадок. У її тексті `Str`
написано один раз, але вона повертає свій аргумент, тому виведений тип результату теж `Str`. Отже, параметр зв'язує
вхід із виходом, і виклик `echo("world")` дав точний тип `"world"`, а не просто `string`.

**Working with Constrained Values.** На цій самій сторінці, трохи вище, є розділ про помилку, про яку часто
запитують. Файл `minimum.ts` містить приклад розділу:

```ts
function minimumLength<Type extends { length: number }>(
  obj: Type,
  minimum: number
): Type {
  if (obj.length >= minimum) {
    return obj;
  } else {
    return { length: minimum };
  }
}
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false minimum.ts
minimum.ts(8,5): error TS2322: Type '{ length: number; }' is not assignable to type 'Type'.
  '{ length: number; }' is assignable to the constraint of type 'Type', but 'Type' could be instantiated with a different subtype of constraint '{ length: number; }'.
```

Функція обіцяє повернути `Type`, тобто той самий тип, який їй передали. Об'єкт `{ length: minimum }` підходить під
обмеження, але не є саме цим типом. Друге речення повідомлення каже саме це: об'єкт підходить під обмеження, але
замість `Type` могли підставити інший тип, який теж має `length`, а крім того ще й інші поля чи методи. Масив саме
такий тип, і наступний приклад показує, що з цього виходить.

Автори показують, що сталося б, якби компілятор це пропустив. Їхній приклад описує функцію через `declare function`.
Ми замість цього змусили компілятор прийняти той самий об'єкт записом `as Type`, щоб код можна було запустити. Файл
`minimum-run.ts`:

```ts
function minimumLength<Type extends { length: number }>(
  obj: Type,
  minimum: number
): Type {
  if (obj.length >= minimum) {
    return obj;
  } else {
    return { length: minimum } as Type;
  }
}

const arr = minimumLength([1, 2, 3], 6);
console.log(arr);
console.log(arr.slice(0));
```

```text
$ npx tsc --noEmit --strict --target es2022 --pretty false minimum-run.ts
$ node minimum-run.ts
{ length: 6 }
TypeError: arr.slice is not a function
```

Компілятор помилок не знайшов. За типом `arr` є масивом чисел, бо `Type` вивели з аргументу `[1, 2, 3]`. Насправді
функція повернула об'єкт `{ length: 6 }`, у якого немає методу `slice`, і програма впала. Це той самий урок, що й у
лекції про `parse<T>` у розділі «Коли дженерик не потрібен»: запис `as` лише змушує компілятор повірити, нічого не
перевіряючи.

## Запитання для самоперевірки

**1. Що означає «виведення аргументу типу» і коли його не вистачає?**

<details><summary>Відповідь</summary>

Компілятор сам визначає параметр типу з аргументів виклику. Його не вистачає, коли з аргументу не видно задуму,
наприклад коли початкове значення `null`, або коли аргументів немає взагалі. Тоді тип пишуть у кутових дужках.

</details>

**2. Чим відрізняються `interface F { <Type>(arg: Type): Type; }` і `interface F<Type> { (arg: Type): Type; }`?**

<details><summary>Відповідь</summary>

У першому випадку кожен виклик добирає тип окремо. У другому тип задають один раз, коли пишуть `F<number>`, і далі він
закріплений. Для сховища з кількома методами потрібен другий варіант, бо всі методи говорять про той самий тип.

</details>

**3. Чому `keyof { [k: string]: boolean }` дорівнює `string | number`?**

<details><summary>Відповідь</summary>

Ключі об'єкта в JavaScript завжди стають рядками, тому `obj[0]` означає те саме, що `obj["0"]`. Отже, числовий ключ
теж законний для рядкової індексної сигнатури.

</details>

**4. Чому `Pick` перевіряє назву поля, а `Omit` ні?**

<details><summary>Відповідь</summary>

`Pick` оголошено з обмеженням `K extends keyof T`, а `Omit` з обмеженням `K extends keyof any`, тобто будь-який ключ.
Опис `Omit` не вимагає, щоб ключ належав типу `T`.

</details>

**5. Чим `Exclude` відрізняється від `Omit`?**

<details><summary>Відповідь</summary>

`Exclude` прибирає варіанти з об'єднання, а `Omit` прибирає поля з об'єктного типу. `Omit` якраз і використовує
`Exclude` над об'єднанням назв полів.

</details>

**6. Чому приклад `GenericNumber` із посібника дає у вас помилку, хоча на сторінці її немає?**

<details><summary>Відповідь</summary>

Посібник перевіряє цей приклад із вимкненим суворим режимом: про це каже позначка `// @strict: false`. У TypeScript
7.0.2 з `--strict` компілятор вимагає, щоб кожне поле класу отримало значення під час створення об'єкта, і друкує
`TS2564`. Ця помилка стосується суворого режиму, а не дженериків.

</details>

**7. Що дасть виклик `pair<number>(1, "два")` для функції `pair<A, B = unknown>(a: A, b: B): [A, B]`?**

<details><summary>Відповідь</summary>

Тип `[number, unknown]`. Параметр `B` має значення за замовчуванням, тому його можна не вказувати. Проте коли хоч один
параметр типу вказано, компілятор решту не виводить, а бере за замовчуванням. Тому `B` дорівнює `unknown`, хоча
передано рядок.

</details>

**8. Яке правило допомагає вирішити, чи потрібен параметр типу?**

<details><summary>Відповідь</summary>

Параметр має траплятися принаймні у двох місцях і зв'язувати їх, наприклад вхід і вихід. Якщо він є лише в одному
місці, його майже завжди можна прибрати.

</details>
