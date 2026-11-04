# Лекція. Фаза 1, день 1. Компоненти й модулі

З цієї лекції починається сам React. Вона пояснює, що таке компонент, коли React його викликає, як розкласти
компоненти по файлах і чому компонент не можна оголошувати всередині іншого компонента. Читання займе близько 50
хвилин.

Усі приклади з React запущено на версії 19.3 у Vitest під jsdom, тобто в імітації браузера всередині Node. Приклади
без React запущено на Node 24. Вивід під прикладами справжній. У справжньому браузері приклади не запускалися, тому
кожне твердження про браузер позначено поруч із ним, і там же сказано, де ви перевірите це самі.

**Після лекції ви зможете пояснити:**

- чим компонент відрізняється від елемента, а елемент від вузла DOM;
- у якому порядку React викликає компоненти і куди при цьому йдуть дані;
- чому велика літера в назві змінює значення запису;
- що станеться, якщо переплутати типовий та іменований імпорт, і чому різні інструменти кажуть про це по-різному;
- як React вирішує, оновити компонент чи створити його заново;
- чому компонент, оголошений усередині іншого компонента, втрачає стан, і що робити замість цього.

## Сторінка, яку важко змінювати

Уявіть сторінку погоди. Для кожного міста на ній стоїть такий самий блок:

```html
<section>
  <h2>Львів</h2>
  <p>Вітер: 5 м/с</p>
  <p>Вологість: 62 %</p>
</section>
<section>
  <h2>Одеса</h2>
  <p>Вітер: 9 м/с</p>
  <p>Вологість: 71 %</p>
</section>
```

Поки міст два, це терпимо. Коли міст стане тридцять, а замовник попросить виділити назву показника жирним, правити
доведеться шістдесят рядків. Одну з копій ви неодмінно пропустите, і сторінка стане неоднаковою.

У лекції «DOM і події» ви вже будували вузли зі звичайного JavaScript. Повтор можна винести у функцію, але тоді всі
подальші зміни на екрані ви теж описуєте самі: знайти вузол, змінити текст, додати клас. Хотілося б іншого: один раз
описати блок, дати йому назву, вживати його як тег з різними даними, а про зміни в DOM не думати. Саме це дає React, і
цей блок у ньому називається компонентом.

## Компонент: функція, яка описує шматок екрана

**Компонент** — це звичайна функція JavaScript, назва якої починається з великої літери і яка повертає опис того, що
показати. Ось компонент для одного показника погоди:

```tsx
type ReadingProps = { label: string; value: string }

function Reading({ label, value }: ReadingProps) {
  return <p>{label}: {value}</p>
}
```

Подивимося на кожен рядок:

- `type ReadingProps` описує дані, які компонент отримує. Це звичайний тип TypeScript із лекції «TypeScript: основи».
- `function Reading(...)` оголошує функцію. Нічого особливого в ній немає, і React не вимагає жодного спеціального
  слова.
- `<p>{label}: {value}</p>` схоже на HTML, але це **JSX**: запис усередині JavaScript, який описує розмітку. Фігурні
  дужки вставляють значення змінної. Докладно про JSX розповість наступний день.

Вживають компонент як тег:

```tsx
<Reading label="Вітер" value="5 м/с" />
```

Значення, які батьківський компонент передає дитині в такому тегу, називаються **пропсами** (англійською props,
скорочено від properties). Для цього запису React викличе `Reading` з одним аргументом, об'єктом усіх пропсів:
`{ label: 'Вітер', value: '5 м/с' }`. Запис `({ label, value }: ReadingProps)` одразу дістає з цього об'єкта два поля.
Цей запис називається деструктуризацією: він розкладає поля об'єкта на окремі змінні.

Компоненти вкладаються один в одного так само, як теги. Компонент міста вживає `Reading` двічі, а сторінка вживає
компонент міста стільки разів, скільки їй треба:

```tsx
type StationProps = { city: string; wind: number; humidity: number }

function Station({ city, wind, humidity }: StationProps) {
  return (
    <section>
      <h2>{city}</h2>
      <Reading label="Вітер" value={`${wind} м/с`} />
      <Reading label="Вологість" value={`${humidity} %`} />
    </section>
  )
}

function WeatherPage() {
  return (
    <div>
      <Station city="Львів" wind={5} humidity={62} />
      <Station city="Одеса" wind={9} humidity={71} />
    </div>
  )
}
```

Тепер, щоб виділити назву показника жирним, треба змінити один рядок у `Reading`, і зміна потрапить в усі міста.
`WeatherPage` тут **батько** компонентів `Station`, а вони його **діти**. Круглі дужки після `return` потрібні, коли
розмітка займає кілька рядків. Чому без них код ламається, показано в розборі читання.

## Три різні речі: компонент, елемент і вузол DOM

Новачки часто називають усе це одним словом, і через це потім не можуть зрозуміти головну помилку дня. Подивімося, що
лежить у змінних:

```tsx
// @vitest-environment jsdom
// Цей коментар просить Vitest створити імітацію браузера, бо без документа компонент показати ніде.
import { render } from '@testing-library/react'
import { test } from 'vitest'

type ReadingProps = { label: string; value: string }

let calls = 0

function Reading({ label, value }: ReadingProps) {
  calls = calls + 1
  return <p>{label}: {value}</p>
}

test('три різні речі', () => {
  const element = <Reading label="Вітер" value="5 м/с" />
  console.log('typeof Reading:', typeof Reading)
  console.log('typeof element:', typeof element)
  console.log('element.type === Reading:', element.type === Reading)
  console.log('element.props:', element.props)
  console.log('викликів Reading до render:', calls)

  const { container } = render(element)
  console.log('викликів Reading після render:', calls)
  console.log('вузол:', container.firstChild?.nodeName, '|', container.innerHTML)
})
```

Компонент і тест лежать в одному файлі, ім'я якого закінчується на `.test.tsx`, наприклад `src/three.test.tsx`. Запускає
цей файл команда `npx vitest run src/three.test.tsx --disable-console-intercept`. Прапорець у кінці просить Vitest одразу
друкувати кожен `console.log`, бо без нього Vitest не показує друк тестів, які пройшли. Решта прикладів із React у цій
лекції запускаються так само й починаються з таких самих рядків. Короткі блоки без `test` вставляйте в тіло тесту. Під
прикладами ми показуємо лише те, що надрукував сам код, без службових рядків Vitest. Ось вивід цього тесту:

```text
typeof Reading: function
typeof element: object
element.type === Reading: true
element.props: { label: 'Вітер', value: '5 м/с' }
викликів Reading до render: 0
викликів Reading після render: 1
вузол: P | <p>Вітер: 5 м/с</p>
```

Запис із тегом не викликав функцію. Він лише створив простий об'єкт, у полі `type` якого лежить сама функція
`Reading`, а в полі `props` лежать пропси. Такий об'єкт називають **елементом**. Функцію викликав React, коли `render`
із бібліотеки Testing Library попросив його показати елемент у документі. Лише після цього з'явився вузол DOM.

| Що це | Приклад | Хто створює | Навіщо існує |
|-------|---------|-------------|--------------|
| компонент | функція `Reading` | ви, у коді, один раз | описує, що показати для даних пропсів |
| елемент | об'єкт із `type` і `props` | запис `<Reading … />`, щоразу, коли він виконується | каже React, який компонент потрібен і з якими даними |
| вузол DOM | тег `<p>` у документі | React через DOM браузера | те, що бачить користувач |

Звідси випливає правило: компонент уживають як тег і не викликають як функцію. Порівняємо обидва записи:

```tsx
const asTag = <Reading label="Вітер" value="5 м/с" />
const asCall = Reading({ label: 'Вітер', value: '5 м/с' })
console.log('як тег, type:', asTag.type.name)
console.log('як виклик, type:', asCall.type)
```

```text
як тег, type: Reading
як виклик, type: p
```

Після звичайного виклику React отримує лише тег `<p>` і не знає, що тут був компонент `Reading`. Тому він не зможе
дати цьому компонентові власний стан і сам вирішувати, коли його викликати. Цю причину описує сторінка [React calls
Components and Hooks](https://react.dev/reference/rules/react-calls-components-and-hooks).

## Рендер: хто кого викликає

**Рендером** React називає виклик функції компонента, щоб дізнатися, що показати. Не плутайте це слово з рендерингом у
браузері, про який ішлося в лекції «Як браузер малює»: там браузер перетворює сторінку на пікселі. Додамо в кожен
компонент прикладу про погоду по одному `console.log` і виконаємо `render(<WeatherPage />)`:

```tsx
function Reading({ label, value }: ReadingProps) {
  console.log('    Reading', label) // пробіли на початку рядка показують глибину вкладення
  return <p>{label}: {value}</p>
}

function Station({ city, wind, humidity }: StationProps) {
  console.log('  Station', city)
  return (
    <section>
      <h2>{city}</h2>
      <Reading label="Вітер" value={`${wind} м/с`} />
      <Reading label="Вологість" value={`${humidity} %`} />
    </section>
  )
}

function WeatherPage() {
  console.log('WeatherPage')
  return (
    <div>
      <Station city="Львів" wind={5} humidity={62} />
      <Station city="Одеса" wind={9} humidity={71} />
    </div>
  )
}

test('порядок викликів', () => {
  const element = <WeatherPage /> // цей запис лише створює об'єкт і не викликає жодної функції
  console.log('елемент створено')
  const { container } = render(element) // лише тут React починає викликати компоненти
  console.log(container.innerHTML) // розмітка, яку React поставив у документ
})
```

```text
елемент створено
WeatherPage
  Station Львів
    Reading Вітер
    Reading Вологість
  Station Одеса
    Reading Вітер
    Reading Вологість
<div><section><h2>Львів</h2><p>Вітер: 5 м/с</p><p>Вологість: 62 %</p></section><section><h2>Одеса</h2><p>Вітер: 9 м/с</p><p>Вологість: 71 %</p></section></div>
```

Рядок `елемент створено` стоїть першим, бо запис `<WeatherPage />` ще не викликає функцію. Останній рядок виводу
надрукував останній `console.log` тесту: це розмітка, яку React поставив у документ. Рядки між ними надрукували самі
компоненти, коли React їх викликав. Покроково це відбувається так:

| Крок | Хто діє | Що відбувається | Викликів усього |
|------|---------|-----------------|-----------------|
| 1 | React | викликає `WeatherPage`, функція повертає два елементи `Station` | 1 |
| 2 | React | викликає `Station` для Львова, функція отримала `wind: 5` і повертає два елементи `Reading` | 2 |
| 3 | React | викликає `Reading` двічі, для вітру й для вологості | 4 |
| 4 | React | закінчив зі Львовом і викликає `Station` для Одеси | 5 |
| 5 | React | викликає `Reading` ще двічі | 7 |
| 6 | React | вносить результат у DOM | 7 |

З таблиці видно три речі.

**Перша: порядок задано вкладеністю.** React доходить до найглибшого компонента в першій гілці, потім переходить до
наступної. Батько завжди викликається раніше за своїх дітей, бо діти стають відомі лише з того, що батько повернув.

**Друга: виклики незалежні.** Для кожного тега React робить окремий виклик з іншими пропсами. Сім викликів складаються
з однієї сторінки, двох міст і чотирьох показників.

**Третя: дані йдуть згори вниз.** `Reading` не бачить ні `wind`, ні `Station`, ні `WeatherPage`. Він знає лише те, що
батько передав йому в пропсах. Якщо дитині щось потрібно від батька, батько передає це пропсом.

Одне застереження про перегляд у браузері. Шаблон проєкту у файлі `src/main.tsx` загортає застосунок у `<StrictMode>`.
Цей компонент у режимі розробки навмисно викликає кожен компонент двічі, щоб виявити певні помилки. Тому під час
`npm run dev` ви можете побачити кожен `console.log` двічі. **Запуском у браузері ми це не перевіряли.** Під jsdom ми
виконали такий тест із компонентом `Reading` попереднього прикладу:

```tsx
import { StrictMode } from 'react'

test('один render усередині StrictMode', () => {
  render(<StrictMode><Reading label="Вітер" value="5 м/с" /></StrictMode>)
})
```

```text
    Reading Вітер
    Reading Вітер
```

Тест зробив один `render` і показав один тег `<Reading>`, а рядок надруковано двічі. Отже, `<StrictMode>` викликав
функцію `Reading` двічі. Для вашого коду це означає таке: подвоєний рядок у консолі під час розробки ще не є помилкою.
Подивитися на це в браузері ви зможете самі, якщо додасте `console.log` у компонент і відкриєте консоль. Докладно про
`<StrictMode>` розповідає день 5 цієї фази.

## Велика літера вирішує, що це

Напишемо той самий тег з малої літери:

```tsx
const bad = <reading label="Вітер" value="5 м/с" />
const good = <Reading label="Вітер" value="5 м/с" />
console.log('type з малої:', typeof bad.type, bad.type)
console.log('type з великої:', typeof good.type, good.type.name)
console.log(render(bad).container.innerHTML)
```

```text
type з малої: string reading
type з великої: function Reading
<reading label="Вітер" value="5 м/с"></reading>
```

Компілятор JSX дивиться на першу літеру. Запис із малої літери він вважає тегом HTML і кладе в `type` рядок
`'reading'`. Запис із великої літери він вважає змінною з таким іменем і кладе в `type` те, що в ній лежить. Тому
`<section>` у прикладі вище працює як тег, а `<Station>` працює як компонент. Велика літера тут не питання стилю.

Запис із малої літери не зупиняє програму: React створює в документі невідомий браузеру елемент `<reading>`, а ваш
текст на екрані не з'являється. Попередити про це можуть двоє:

- **React** у режимі розробки пише в консоль:
  `The tag <reading> is unrecognized in this browser. If you meant to render a React component, start its name with an uppercase letter.`
  Цей рядок надрукував під jsdom той самий код вище, а ми винесли його сюди з виводу. У консолі справжнього браузера ми
  його не перевіряли запуском.
- **TypeScript** не пропускає такий запис ще до запуску. Команда `npx tsc --noEmit -p tsconfig.app.json` для цього коду
  друкує:
  `error TS2339: Property 'reading' does not exist on type 'JSX.IntrinsicElements'.`

## Файли: компонент у своєму модулі

Коли компонентів стає багато, їх розкладають по файлах. Механізм ви вже знаєте з лекції «Модулі й пакети»: файл
показує назовні лише те, що експортує, а інший файл бере це через `import`. React нічого до цього не додає. Це
звичайні модулі JavaScript, у яких лежать функції.

| Вид | Як експортують | Як імпортують | Скільки на файл | Ім'я при імпорті |
|-----|----------------|---------------|-----------------|------------------|
| типовий | `export default function Title() {}` | `import Title from './Title'` | один | будь-яке |
| іменований | `export function Note() {}` | `import { Note } from './Note'` | скільки завгодно | те саме |

Сторінка React радить таке: типовий експорт, коли файл віддає один компонент, а іменовані, коли компонентів чи значень
кілька. Компонент без `export` лишається приватною справою файла, і це корисно, коли дрібний компонент потрібен лише
сусідові. Типовий експорт теж варто називати: функція в записі `export default () => {}` має ім'я `default`, і таке
ім'я нічого не скаже вам у повідомленні про помилку. Застосунок починається з **кореневого компонента**. У шаблоні
Vite це `App` у файлі `src/App.tsx`, а файл `src/main.tsx` просить React показати його на сторінці.

Найцікавіше в цій темі те, як поводяться інструменти, коли ви переплутали вид імпорту. Візьмемо файл із двома
експортами і файл з одним іменованим:

```tsx
// файл parts.tsx
export default function Title({ text }: { text: string }) {
  return <h2>{text}</h2>
}
export function Note({ text }: { text: string }) {
  return <p>{text}</p>
}

// файл only.tsx
export function Sensor() {
  return <p>датчик</p>
}
```

Покладемо обидва файли в теку `src/mix` і допишемо поруч файл `imports.test.tsx` із трьома помилками імпорту. Кожна
помилка стоїть в окремому рядку `import`:

```tsx
// @vitest-environment jsdom
import { render } from '@testing-library/react'
import { test } from 'vitest'
import { Title } from './parts' // помилка: Title експортовано типово, а тут дужки
import Sensor from './only' // помилка: у only.tsx немає типового експорту, а тут немає дужок
import Note from './parts' // помилка: без дужок сюди потрапить типовий експорт, а не Note

test('іменований імпорт типового експорту', () => {
  console.log('Title:', Title)
  console.log((() => Title).toString()) // показує код, який Vitest виконує замість слова Title
  render(<Title text="Сьогодні дощ" />)
})

test('типовий імпорт із файла без типового експорту', () => {
  console.log('Sensor:', Sensor)
  render(<Sensor />)
})

test('типовий імпорт замість іменованого', () => {
  const { container } = render(<Note text="Сьогодні дощ" />)
  console.log(container.innerHTML)
})
```

Спершу запустимо цей файл у Vitest. Два тести падають, а третій проходить:

```text
Title: undefined
() => __vite_ssr_import_2__.Title
Sensor: undefined
<h2>Сьогодні дощ</h2>
FAIL  src/mix/imports.test.tsx > іменований імпорт типового експорту
FAIL  src/mix/imports.test.tsx > типовий імпорт із файла без типового експорту
Error: Element type is invalid: expected a string (for built-in components) or a class/function (for composite components) but got: undefined. You likely forgot to export your component from the file it's defined in, or you might have mixed up default and named imports.
```

Рядки `Title: undefined` і `Sensor: undefined` надрукували два перші тести: у цих змінних нічого немає. Тому `render`
отримав `undefined` замість компонента, і React кинув помилку `Element type is invalid`. Vitest показує її один раз на
обидва тести, бо текст однаковий. Рядок `<h2>Сьогодні дощ</h2>` надрукував третій тест, який пройшов, хоча показав не той
тег.

Тепер перевіримо ті самі файли командою `npx tsc --noEmit -p tsconfig.app.json`. Команда `tsc` лише перевіряє типи й
нічого не запускає. Довгий шлях до теки проєкту в її виводі ми замінили трьома крапками:

```text
src/mix/imports.test.tsx(4,10): error TS2614: Module '"./parts"' has no exported member 'Title'. Did you mean to use 'import Title from "./parts"' instead?
src/mix/imports.test.tsx(5,8): error TS2613: Module '"…/src/mix/only"' has no default export. Did you mean to use 'import { Sensor } from "…/src/mix/only"' instead?
```

`tsc` знайшов дві перші помилки, а про третю не сказав нічого, бо пропси `Title` і `Note` однакові. Третю помилку він
побачить лише тоді, коли пропси не збігаються. Перевіримо це таким файлом `mismatch.tsx`:

```tsx
import Note from './parts'

export const wrong = <Note tone="дощ" />
```

```text
src/mix/mismatch.tsx(3,28): error TS2322: Type '{ tone: string; }' is not assignable to type 'IntrinsicAttributes & { text: string; }'.
  Property 'tone' does not exist on type 'IntrinsicAttributes & { text: string; }'.
```

Останній інструмент — Node. Він не розуміє JSX, тому ті самі три помилки ми записали у файлах `.mjs`, де функції просто
повертають текст:

```js
// файл parts.mjs
export default function Title() {
  return 'це функція Title'
}
export function Note() {
  return 'це функція Note'
}

// файл only.mjs
export function Sensor() {
  return 'це функція Sensor'
}

// файл case1.mjs
import { Title } from './parts.mjs'
console.log(Title())

// файл case2.mjs
import Sensor from './only.mjs'
console.log(Sensor())

// файл case3.mjs
import Note from './parts.mjs'
console.log(Note())
```

Команди `node case1.mjs`, `node case2.mjs` і `node case3.mjs` друкують таке. У виводі двох перших Node показує ще шлях до
файла й стек викликів, а ми залишили рядок із текстом помилки:

```text
SyntaxError: The requested module './parts.mjs' does not provide an export named 'Title'
SyntaxError: The requested module './only.mjs' does not provide an export named 'default'
це функція Title
```

У двох перших випадках модуль не запустився зовсім, тому жоден `console.log` не спрацював. Третій випадок запустився і
без жодної помилки викликав не ту функцію. Зведемо всі результати в одну таблицю:

| Запис | `tsc` | Node | Vitest |
|-------|-------|------|--------|
| `import { Title } from './parts'` | `TS2614: … has no exported member 'Title'` | `SyntaxError: … does not provide an export named …`, модуль не запускається | `Title` дорівнює `undefined`, а React пише `Element type is invalid … but got: undefined` |
| `import Sensor from './only'` | `TS2613: … has no default export` | `SyntaxError: … does not provide an export named 'default'` | так само `undefined` і те саме повідомлення React |
| `import Note from './parts'` | `TS2322` на пропсах, якщо вони не збігаються | помилки немає | помилки немає, а `<Note text="Сьогодні дощ" />` показує `<h2>Сьогодні дощ</h2>` замість абзацу |

Тут є дві важливі думки.

**Запис `import Note from './parts'` небезпечний.** Ім'я при типовому імпорті довільне, тому змінна `Note` насправді
містить типовий експорт, тобто `Title`. Жоден запуск не впаде. Якщо пропси випадково збіглися, як у цьому файлі, то
`tsc` теж мовчить, і знайти помилку допоможе лише приклад, який шукає на сторінці правильний тег.

**Одна помилка виглядає по-різному.** Node зупиняє модуль ще до запуску, бо імпорт зв'язується з експортом на етапі
завантаження. За специфікацією так само чинить браузер, тому під час `npm run dev` у консолі має з'явитися
`SyntaxError`, а її текст залежить від браузера. **Цей випадок описано за специфікацією, у браузері ми його не
запускали.** Vitest запускає код через власний завантажувач, який перетворює імпорт на читання поля об'єкта-модуля. Це
видно у виводі Vitest вище. Рядок `console.log((() => Title).toString())` надрукував текст функції після перетворення,
і замість `Title` там стоїть `__vite_ssr_import_2__.Title`. Читання відсутнього поля дає `undefined`. Отже, `undefined`
тут дає саме завантажувач Vitest, а сам JavaScript цю помилку не пропускає. Тому в тестах повідомлення приходить від
React, і в ньому є підказка про змішані імпорти. Коли бачите `got: undefined`, насамперед перевірте рядок `import`.

Є ще один вид імпорту, потрібний для типів. У шаблоні проєкту ввімкнено `verbatimModuleSyntax`, тому тип імпортують зі
словом `type`. Причину пояснює лекція «Проєкт: Vite, лінт, TypeScript»: перетворювач бачить лише один файл і не може
сам дізнатися, що назва означає тип.

## Стан: пам'ять компонента

Щоб зрозуміти головну помилку дня, потрібне ще одне поняття. Докладно його вивчає день 7 цієї фази, а тут вистачить
короткого пояснення. Ось термостат, який пам'ятає температуру:

```tsx
function Thermostat() {
  const [degrees, setDegrees] = useState(20)
  return <button onClick={() => setDegrees(degrees + 1)}>Температура: {degrees}</button>
}
```

Локальна змінна функції зникає, коли функція завершилася. Це ви бачили в лекції «Функції та замикання». Тому значення,
яке має дожити до наступного виклику, зберігає сам React. Таке значення називається **станом**.

- `useState(20)` просить React зберегти значення для цього компонента. Такі функції React, назва яких починається з
  `use`, називають **хуками**. Початкове значення `20` враховується лише під час першого показу. Функція повертає
  пару: поточне значення й функцію, яка його змінює.
- `setDegrees(21)` записує нове значення і просить React викликати компонент ще раз. Цей повторний виклик називають
  **перерендером**, або перемальовуванням.
- `onClick` призначає функцію, яка спрацює під час натискання.

React зберігає стан не у функції. Він будує власне дерево компонентів, що зараз на екрані, і прив'язує стан до місця в
цьому дереві. Запис про компонент на конкретному місці разом зі станом і вузлами називають **екземпляром**. На
сторінці погоди є два окремі екземпляри `Station`, хоча функція одна.

## Як React вирішує: оновити чи створити заново

Після кожного рендеру React порівнює нове дерево елементів зі старим, місце за місцем. На кожному місці він дивиться
на поле `type` і порівнює старе значення з новим через `===`. Результатів два:

| Порівняння `type` | Що робить React | Що зі станом і вузлами |
|-------------------|-----------------|------------------------|
| рівні | оновлює наявний екземпляр новими пропсами | стан і вузли зберігаються |
| різні | **знімає** старий екземпляр і **монтує** новий | старий стан зникає, старі вузли видаляються, новий стан починається з початкового значення |

Слово **монтувати** означає вперше створити екземпляр і поставити його вузли в документ, а слово **знімати** означає
прибрати їх звідти разом зі станом. Коли знято батька, зникає і все, що під ним.

Для тегів HTML у `type` лежить рядок. Рядки порівнюються за вмістом, тому `'div'` завжди дорівнює `'div'`. Для
компонентів у `type` лежить функція. Функції порівнюються за посиланням, як об'єкти в лекції «Значення й посилання»:
важливо, чи це той самий об'єкт, а не чи однаковий у них текст. Подивімося на функції, створені в різних викликах:

```js
function makeInner() {
  function inner() {
    return 42
  }
  return inner
}

const first = makeInner()
const second = makeInner()
console.log(first === second)
console.log(first.toString() === second.toString())
console.log(first() === second())
```

```text
false
true
true
```

Код однаковий, результат однаковий, а функції різні. Кожен виклик `makeInner` виконує оголошення `function inner` і
створює новий об'єкт функції, як пояснювала лекція «Функції та замикання».

## Компонент усередині компонента

Тепер усе складається докупи. Кімната має світло, а термостат оголошено всередині кімнати:

```tsx
function Room() {
  const [lights, setLights] = useState(false)

  function Thermostat() {                       // оголошено всередині Room
    const [degrees, setDegrees] = useState(20)
    console.log('Thermostat:', degrees)
    return <button onClick={() => setDegrees(degrees + 1)}>Температура: {degrees}</button>
  }

  return (
    <div>
      <Thermostat />
      <button onClick={() => setLights(!lights)}>Світло: {lights ? 'так' : 'ні'}</button>
    </div>
  )
}
```

Тест натискає кнопку термостата тричі, а потім кнопку світла. Перед кожним кроком він шукає кнопку в документі заново.
Перший знайдений вузол тест зберігає у змінній `before`, щоб наприкінці порівняти його з новим вузлом:

```tsx
// На початку файла стоять такі рядки, далі йде компонент Room, а за ним цей тест.
// @vitest-environment jsdom
import { useState } from 'react'
import { fireEvent, render, screen } from '@testing-library/react'
import { test } from 'vitest'

test('кімната', () => {
  render(<Room />)
  const before = screen.getByText(/Температура/)
  fireEvent.click(before)
  fireEvent.click(screen.getByText(/Температура/))
  fireEvent.click(screen.getByText(/Температура/))
  console.log('після трьох натискань:', screen.getByText(/Температура/).textContent)

  fireEvent.click(screen.getByText(/Світло/))
  const after = screen.getByText(/Температура/)
  console.log('після світла:', after.textContent)
  console.log('той самий вузол:', before === after, '| старий у документі:', document.contains(before))
})
```

Функція `fireEvent.click` імітує натискання на вузол, а `screen.getByText` знаходить вузол за текстом. Другий варіант
відрізняється лише одним: функцію `Thermostat` перенесено над `Room`, на рівень файла.

Вивід варіанта, де `Thermostat` оголошено всередині `Room`:

```text
Thermostat: 20
Thermostat: 21
Thermostat: 22
Thermostat: 23
після трьох натискань: Температура: 23
Thermostat: 20
після світла: Температура: 20
той самий вузол: false | старий у документі: false
```

Вивід варіанта, де `Thermostat` оголошено над `Room`:

```text
Thermostat: 20
Thermostat: 21
Thermostat: 22
Thermostat: 23
після трьох натискань: Температура: 23
Thermostat: 23
після світла: Температура: 23
той самий вузол: true | старий у документі: true
```

Пройдемо перший вивід кроками. Функцію `Thermostat`, створену першим викликом `Room`, позначимо `T1`, а створену
другим викликом позначимо `T2`.

| Подія | Хто викликаний | `type` на місці термостата | Рішення React | `degrees` |
|-------|----------------|----------------------------|---------------|-----------|
| перший показ | `Room`, потім `T1` | `T1` | монтує | 20 |
| перше натискання на термостат | лише `T1`, бо змінився її стан | `T1` | оновлює | 21 |
| друге й третє натискання | лише `T1` | `T1` | оновлює | 22, потім 23 |
| натискання на світло | `Room`, бо змінився її стан, потім `T2` | `T2`, а `T1 === T2` дає `false` | знімає `T1` разом із числом 23 і кнопкою, монтує `T2` | 20 |

Зверніть увагу на дві речі. Поки ви натискаєте термостат, `Room` не викликається і нової функції не створює, тому
число росте і здається, що все добре. Помилка проявляється лише тоді, коли перемальовується батько. А ще кнопка світла
не змінювала `degrees`: вона замінила цілий компонент, і значення зникло разом із ним. У другому варіанті `Thermostat`
теж викликано ще раз після натискання на світло, бо батько перемальовує дітей. Але `type` лишився тим самим, тому стан
збережено. Перемалювати й створити заново — різні речі.

Документація React прямо каже про цей випадок: «This is why you should not nest component function definitions». Вона
попереджає, що такий код повільний і веде до помилок. Повільний він тому, що при кожному рендері батька React видаляє
й будує заново всі вузли під цією дитиною.

### Навіщо так пишуть і як це виправити

Компонент оголошують усередині іншого найчастіше заради зручності: так дитина бачить змінні батька без пропсів. Ось
такий випадок із найпомітнішим симптомом. Стан запиту лежить у батька, а поле пошуку оголошено всередині:

```tsx
function Catalog() {
  const [query, setQuery] = useState('')

  function SearchBox() {                        // хочеться читати query без пропсів
    return <input aria-label="Пошук" value={query} onChange={(e) => setQuery(e.target.value)} />
  }

  return <div><SearchBox /><p>Шукаємо: {query}</p></div>
}
```

Тест набирає `кава` через бібліотеку `user-event`. Вона імітує окремі натискання клавіш, а після набору тест друкує вміст
поля й назву вузла, який тримає фокус:

```tsx
import userEvent from '@testing-library/user-event'

test('набір у полі пошуку', async () => {
  render(<Catalog />)
  const user = userEvent.setup()
  await user.type(screen.getByLabelText('Пошук'), 'кава')
  const box = screen.getByLabelText<HTMLInputElement>('Пошук') // поле в документі зараз
  console.log(`у полі: "${box.value}"`)
  console.log('фокус на:', document.activeElement?.tagName)
})
```

```text
у полі: "к"
фокус на: BODY
```

Перша літера змінила стан батька. Батько перемалювався і створив нову функцію `SearchBox`. React зняв старе поле, а
разом із ним зник і фокус клавіатури. Решта літер уже нікуди не потрапила.

**Це результат під jsdom, де набір імітує бібліотека `user-event`. У справжньому браузері ми цей приклад не
запускали.** За тим самим механізмом там фокус теж має зникати, і поле доведеться клацати знову після кожної літери.
Перевірити це можна самостійно: вставте такий компонент у сторінку під час `npm run dev` і спробуйте набрати слово.

Виправлення завжди одне: оголосити компонент на рівні файла, а потрібне від батька передати пропсами.

```tsx
type SearchBoxProps = { query: string; onQueryChange: (text: string) => void }

function SearchBox({ query, onQueryChange }: SearchBoxProps) {
  return <input aria-label="Пошук" value={query} onChange={(e) => onQueryChange(e.target.value)} />
}

function Catalog() {
  const [query, setQuery] = useState('')
  return <div><SearchBox query={query} onQueryChange={setQuery} /><p>Шукаємо: {query}</p></div>
}
```

Той самий тест для цього варіанта друкує:

```text
у полі: "кава"
фокус на: INPUT
```

### Хто ловить цю помилку

React під час роботи не кидає помилки й нічого не пише в консоль, бо для нього `<Thermostat />` лише об'єкт, а де
створено функцію з поля `type`, він не перевіряє. Тому тест без явної перевірки проходить. Ловить цю помилку лінтер,
який ви налаштували в лекції «Проєкт: Vite, лінт, TypeScript». Правило `react-hooks/static-components` входить у
пресет `recommended`. Ось вивід команди `npx eslint src/room.test.tsx` для файла досліду з кімнатою. У цьому файлі стоять
рядки імпорту, компонент `Room` і тест, а номери рядків рахуються від початку файла:

```text
…/spa/src/room.test.tsx
  17:8  error  Error: Cannot create components during render

Components created during render will reset their state each time they are created. Declare components outside of render.

…/spa/src/room.test.tsx:17:8
  15 |   return (
  16 |     <div>
> 17 |       <Thermostat />
     |        ^^^^^^^^^^ This component is created during render
  18 |       <button onClick={() => setLights(!lights)}>Світло: {lights ? 'так' : 'ні'}</button>
  19 |     </div>
  20 |   )

…/spa/src/room.test.tsx:9:3
   7 |   const [lights, setLights] = useState(false)
   8 |
>  9 |   function Thermostat() {                       // оголошено всередині Room
     |   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> 10 |     const [degrees, setDegrees] = useState(20)
     | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> 11 |     console.log('Thermostat:', degrees)
     | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> 12 |     return <button onClick={() => setDegrees(degrees + 1)}>Температура: {degrees}</button>
     | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> 13 |   }
     | ^^^^ The component is created during render here
  14 |
  15 |   return (
  16 |     <div>  react-hooks/static-components

✖ 1 problem (1 error, 0 warnings)
```

Зверніть увагу, що лінтер вказує насамперед на місце, де компонент **використано**, а оголошення показує лише другим.

### Що всередині компонента оголошувати можна

Заборона стосується тільки функцій, які ви вживаєте як тег. Звичайні функції всередині компонента цілком нормальні.
Команда `npx eslint` для цього файла не друкує нічого, а тест, який натискає термостат і потім світло, показує, що стан
термостата зберігся:

```tsx
function Thermostat() {
  const [degrees, setDegrees] = useState(20)
  function raise() {                            // обробник: нова функція щоразу, і це нормально
    setDegrees(degrees + 1)
  }
  return <button onClick={raise}>Температура: {degrees}</button>
}

function Room() {
  const [lights, setLights] = useState(false)
  function caption() {                          // допоміжна функція: її викликають, а не малюють як тег
    return lights ? 'так' : 'ні'
  }
  return (
    <div>
      <Thermostat />
      <button onClick={() => setLights(!lights)}>Світло: {caption()}</button>
    </div>
  )
}

test('функції всередині компонента', () => {
  render(<Room />)
  fireEvent.click(screen.getByText(/Температура/))
  fireEvent.click(screen.getByText(/Світло/))
  console.log(screen.getByText(/Температура/).textContent)
  console.log(screen.getByText(/Світло/).textContent)
})
```

```text
Температура: 21
Світло: так
```

Функції `raise` і `caption` теж нові при кожному рендері, але вони ніколи не потрапляють у поле `type`, тому React їх
не порівнює.

## Рецепт: компонент проєктують як функцію

З днів фази 0 ви знаєте рецепт із книжки How to Design Programs. Компонент — це функція, тому рецепт працює без змін.
Покажемо його на компоненті `Reading`.

| Крок рецепта | Що він означає для компонента |
|--------------|-------------------------------|
| опис даних | тип пропсів, тут `ReadingProps` |
| сигнатура | параметр із типом у коді: `({ label, value }: ReadingProps)` |
| призначення | одне речення в коментарі над функцією про те, що компонент показує |
| заглушка | `return null`: компонент, який нічого не показує |
| приклади | файл тестів, написаний до тіла компонента |
| перелік вхідних даних | коментар у тілі, що в компонента є |
| тіло | розмітка замість заглушки |
| перевірка | запуск прикладів |

```tsx
// файл Reading.tsx
type ReadingProps = { label: string; value: string }

// Показує один показник погоди абзацом «назва: значення».
export function Reading({ label, value }: ReadingProps) {
  // Є: label — назва показника, value — готовий текст значення.
  return null
}

// файл examples.test.tsx
// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest' // додає перевірку toBeInTheDocument
import { cleanup, render, screen } from '@testing-library/react'
import { afterEach, expect, test } from 'vitest'
import { Reading } from './Reading'

afterEach(cleanup) // прибирає компонент із документа після кожного прикладу

test('Reading: показує назву й значення', () => {
  render(<Reading label="Вітер" value="5 м/с" />)
  expect(screen.getByText('Вітер: 5 м/с')).toBeInTheDocument()
})

test('Reading: інші пропси дають інший текст', () => {
  render(<Reading label="Вологість" value="62 %" />)
  expect(screen.getByText('Вологість: 62 %')).toBeInTheDocument()
})
```

Приклад для функції порівнював результат зі значенням. Приклад для компонента показує компонент у документі й шукає
те, що побачив би користувач. Об'єкт `screen` з бібліотеки Testing Library шукає по всій сторінці, `getByText`
знаходить вузол із таким текстом, а `toBeInTheDocument` перевіряє, що вузол стоїть у документі. Поки в компоненті
стоїть заглушка, обидва приклади падають, і сторінка порожня:

```text
TestingLibraryElementError: Unable to find an element with the text: Вітер: 5 м/с. This could be because the text is broken up by multiple elements. In this case, you can provide a function for your text matcher to make your matcher more flexible.

Ignored nodes: comments, script, style
<body>
  <div />
</body>
```

Цей знімок розмітки під помилкою читайте першим, бо він показує, що насправді є на сторінці. Коли замість
`return null` стоїть розмітка, обидва приклади проходять. Запит `getByRole`, який шукає за роллю елемента, і функцію
`within` докладно пояснює розбір читання.

## Типові хибні уявлення

**«Батько перемалювався, отже, діти створилися заново».** Діти справді викликаються ще раз, але React створює
екземпляр заново лише тоді, коли змінився `type`. У варіанті з `Thermostat` над `Room` тіло компонента виконалося, а
число 23 лишилося.

**«Стан зникає через те, що `useState` скидається під час рендеру батька».** Хук нічого не скидає. Стан зникає, бо
React зняв екземпляр, якому цей стан належав. Вузол DOM зникає разом із ним, тому навіть текст у полі без жодного
`useState` теж пропаде.

**«Функції всередині компонента оголошувати не можна».** Не можна лише компоненти, тобто функції, які вживають як тег.
Обробники подій і допоміжні функції всередині компонента звичайні й потрібні.

**«Вкладати компоненти не можна».** Вкладати можна й потрібно **вживання**: `<Station>` усередині розмітки
`WeatherPage`. Заборонено вкладати **оголошення**: `function Station` усередині `function WeatherPage`.

**«Той самий код і те саме ім'я означають той самий компонент».** React порівнює не текст функції й не її ім'я, а сам
об'єкт функції.

**«Якщо обгорнути внутрішній компонент у `useCallback`, проблема зникне».** Хук `useCallback` повертає ту саму функцію
між рендерами, доки не зміняться його залежності, тому він сховає симптом лише до цього моменту. Перевіримо це на
кімнаті. Файл починається тими самими рядками, що й дослід вище, лише до першого імпорту додано `useCallback`. Пропс
`version` стоїть тут лише для того, щоб тест міг змінити залежність, а функція `rerender` показує той самий компонент із
новими пропсами:

```tsx
function Room({ version }: { version: number }) {
  const [lights, setLights] = useState(false)

  const Thermostat = useCallback(function Thermostat() {
    const [degrees, setDegrees] = useState(20)
    return <button onClick={() => setDegrees(degrees + 1)}>Температура: {degrees}</button>
  }, [version]) // нова функція з'явиться лише тоді, коли зміниться version

  return (
    <div>
      <Thermostat />
      <button onClick={() => setLights(!lights)}>Світло: {lights ? 'так' : 'ні'}</button>
    </div>
  )
}

test('useCallback ховає симптом', () => {
  const { rerender } = render(<Room version={1} />)
  fireEvent.click(screen.getByText(/Температура/))
  fireEvent.click(screen.getByText(/Світло/))
  console.log('після світла:', screen.getByText(/Температура/).textContent)
  rerender(<Room version={2} />)
  console.log('після зміни залежності:', screen.getByText(/Температура/).textContent)
})
```

```text
після світла: Температура: 21
після зміни залежності: Температура: 20
```

Перший рядок показує, що кнопка світла вже не скидає число: `useCallback` повернув ту саму функцію, і `type` не змінився.
Другий рядок показує, що число все одно скинулося, коли змінилася залежність: `useCallback` повернув нову функцію, і
React зняв старий екземпляр. Функція й далі створюється під час рендеру, тому лінтер лишається червоним. Серед рядків,
які `npx eslint` друкує для цього файла, стоїть та сама помилка:

```text
  16:8  error    Error: Cannot create components during render
```

Правильне виправлення одне: рівень файла й пропси.

**«Vitest зелений, отже, імпорти правильні».** Vitest не перевіряє типів, а типовий імпорт чужого компонента взагалі
не дає помилки. Запускайте ще й `tsc`, а в прикладах шукайте конкретний вміст сторінки.

## Як це проявиться далі в React

- **День 2, JSX.** Ви дізнаєтеся, у що саме компілюється запис із тегом і звідки беруться елементи.
- **День 3, пропси.** Те, що тут було лише способом передати дані, отримає докладні правила.
- **День 4, списки й ключі.** Ключ `key` доповнює порівняння за місцем і типом, коли елементи стоять у списку.
- **День 5, чистота й дерево.** Ви побачите `<StrictMode>` і дерево рендеру, а також дізнаєтеся, чому рендер не
  повинен нічого змінювати назовні.
- **День 7, події й стан.** Короткий опис `useState` із цієї лекції стане повним.
- **День 12, спільний стан і скидання стану.** Правило про місце й тип стане інструментом: ви навмисно скидатимете
  стан.
- **Фаза 2, день 2, узгодження дерева.** Порівняння `type` розглядається там зсередини, разом із вартістю цієї роботи.

## Перевірте себе

**1. Що лежить у змінній після `const x = <Reading label="Вітер" value="5 м/с" />` і чи викликано вже `Reading`?**

<details><summary>Відповідь</summary>

У змінній лежить елемент, простий об'єкт, у якого `type` дорівнює функції `Reading`, а `props` містить обидва
значення. Функцію ще не викликано. Її викличе React, коли цей елемент треба буде показати.

</details>

**2. На сторінці `Station` ужито три рази, а в кожному `Station` по два `Reading`. Скільки викликів зробить React під
час першого показу разом зі сторінкою?**

<details><summary>Відповідь</summary>

Десять: один виклик сторінки, три виклики `Station` і шість викликів `Reading`. Під `<StrictMode>` у режимі розробки
кожен компонент викликається двічі, тому рядків у консолі буде вдвічі більше. Подвоєння ми бачили під jsdom, а в
браузері його не запускали.

</details>

**3. Чому `<card />` і `<Card />` дають різний результат, хоча функція `Card` є у файлі?**

<details><summary>Відповідь</summary>

Компілятор JSX дивиться на першу літеру. З малої літери виходить рядок `'card'`, і React створює невідомий тег, не
чіпаючи вашої функції, а в режимі розробки ще й пише попередження в консоль. З великої літери виходить посилання на
змінну `Card`, і React її викликає.

</details>

**4. Файл експортує `export default function Title` і `export function Note`. Що потрапить у змінну після
`import Note from './parts'`?**

<details><summary>Відповідь</summary>

Типовий експорт, тобто `Title`. Ім'я при типовому імпорті довільне, тому помилки під час запуску не буде. Помітити її
можуть `tsc`, якщо пропси не збігаються, або приклад, який шукає на сторінці правильний тег.

</details>

**5. Той самий хибний імпорт `import { Title } from './parts'` у Node дає `SyntaxError`, а у Vitest дає повідомлення
React про `undefined`. Чому?**

<details><summary>Відповідь</summary>

Node зв'язує імпорти з експортами під час завантаження модуля й зупиняється, якщо експорту немає. Завантажувач Vitest
перетворює імпорт на читання поля об'єкта-модуля. Відсутнє поле дає `undefined`, а React отримує `undefined` замість
компонента й повідомляє про це.

</details>

**6. У прикладі з кімнатою натискання на термостат не скидає число, а натискання на світло скидає. Поясніть різницю.**

<details><summary>Відповідь</summary>

Термостат має власний стан, тому після його зміни React викликає лише функцію термостата, і нова функція не
створюється. Кнопка світла змінює стан кімнати, тому React викликає `Room`. Тіло `Room` створює нову функцію
`Thermostat`, і на тому самому місці стоїть інший `type`. React знімає старий екземпляр зі станом і монтує новий.

</details>

**7. Усередині компонента оголошено функцію `formatDate` і її викликають як `{formatDate(day)}`. Це та сама помилка?**

<details><summary>Відповідь</summary>

Ні. Функцію викликано як звичайну, її результат стає частиною розмітки, а в поле `type` вона не потрапляє. React її не
порівнює, і лінтер не скаржиться. Помилкою це стало б у записі `<FormatDate day={day} />` з функцією, оголошеною
всередині компонента.

</details>

## Словничок лекції

| Слово | Що означає |
|-------|------------|
| компонент | функція з великою літерою в назві, яка повертає опис того, що показати |
| JSX | запис, схожий на HTML, усередині JavaScript |
| проп (prop) | значення, яке батько передає дитині; усі пропси приходять одним об'єктом |
| елемент | простий об'єкт із полями `type` і `props`, який описує, що показати |
| батько, дитина | компонент, який уживає інший у своїй розмітці, і той, кого він уживає |
| кореневий компонент | компонент, з якого починається застосунок |
| рендер | виклик функції компонента, щоб дізнатися, що показати |
| стан | значення, яке React зберігає для компонента між рендерами |
| хук | функція React із назвою на `use`, наприклад `useState` |
| екземпляр | запис React про компонент на конкретному місці дерева разом зі станом |
| монтувати, знімати | створити екземпляр і поставити його вузли в документ; прибрати їх разом зі станом |

## Що читати далі

- [Розбір читання до цього дня](../reading/f1-d01-reading.md): що саме написано в матеріалах дня й де що шукати.
- Preserving and Resetting State, розділи `Same component at the same position preserves state` і `Different
  components at the same position reset state`. Це джерело правила про місце й тип, а докладно його вивчає день 12.
- `static-components`: сторінка правила лінтера з прикладами й порадою передавати дані пропсами.

---

Лекцію написано для цього плану. Вона спирається на документацію React, сторінки Testing Library, специфікацію
ECMA-262 і переказує рецепт із книжки How to Design Programs. Усе переказано своїми словами, а права на ці тексти
належать їхнім авторам.
