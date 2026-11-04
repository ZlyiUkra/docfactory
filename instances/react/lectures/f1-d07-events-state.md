# Лекція. Фаза 1, день 7. Події й стан

Досі ваші компоненти лише показували те, що отримали від батька. Ця лекція пояснює, як компонент реагує на дії людини
і як він запам'ятовує результат: що означає передати функцію обробнику, чому звичайна змінна не годиться для пам'яті,
що робить `useState`, як поле вводу стає керованим, як дитина повідомляє батькові про вибір і кому належить стан, коли
компонентів на екрані два. Читання займе близько 50 хвилин.

Приклади з React запущено на версії 19.3 у Vitest під jsdom, тобто в імітації браузера всередині Node. Вивід під
прикладами справжній. Типи перевірено компілятором `tsc` версії 6.0, а правила лінтера запущено через ESLint із
набором `react-hooks`. У справжньому браузері приклади не запускалися, тому там, де йдеться про браузер, поруч
сказано, на чому це твердження тримається.

**Після лекції ви зможете пояснити:**

- чим `onClick={addCup}` відрізняється від `onClick={addCup()}` і що саме отримує React у кожному випадку;
- що React робить зі значенням пропа `onClick`, якщо це не функція;
- чому звичайна змінна всередині компонента не може бути пам'яттю, навіть якщо компонент перемалювати;
- які дві речі дає `useState` і чому початкове значення читається лише один раз;
- що відбувається від натискання клавіші до появи літери в керованому полі;
- як дитина змінює стан батька, якщо прочитати цей стан вона не може;
- кому належить стан і коли він зникає.

## Кав'ярня, де нічого не відбувається

Ви робите екран замовлення для кав'ярні. На ньому є напис «Чашок: 0» і кнопка «Ще чашка». Людина клацає, а число має
зрости. Із того, що ви вже знаєте про JavaScript, природно написати так:

```tsx
function Order() {
  let cups = 0
  function addCup() {
    cups = cups + 1
  }
  return <button onClick={addCup()}>Чашок: {cups}</button>
}
```

Цей короткий компонент містить одразу дві різні помилки, і кожна з них не дасть йому запрацювати. Функція `addCup`
запускається не тоді, коли ви очікуєте. Змінна `cups` не вміє пам'ятати. Коли ви їх виправите, з'являться ще дві
потреби. Вибір напою зручно винести в окремий компонент із кнопками, і цьому компоненту треба якось повідомити батька,
що саме вибрали. А ще столів у кав'ярні кілька, і замовлення кожного столу мусить бути окремим.

Отже, сьогодні є чотири запитання. Коли виконується обробник? Де живе пам'ять компонента? Як дитина говорить із
батьком? Кому належить ця пам'ять, якщо компонентів кілька? Лекція проходить їх саме в цьому порядку.

## Обробник: функція, яку викличуть пізніше

Лекція «DOM і події» пояснила, що **подія** є повідомленням браузера про те, що щось сталося, а **обробник** є
функцією, яку браузер викликає у відповідь. У React обробник передають пропом. Назва пропа відповідає назві події,
наприклад `onClick` для клацання або `onChange` для зміни поля. Та сама лекція показала, що React реєструє слухачі на
корені застосунку й сам викликає ваші функції. Вам важливо одне: React мусить отримати **функцію**, щоб викликати її
пізніше.

### Що лежить у фігурних дужках

Лекція «JSX» пояснила, що у фігурних дужках стоїть звичайний вираз JavaScript, а компілятор кладе його значення в
об'єкт пропсів. Тому вираз обчислюється щоразу, коли виконується функція компонента, тобто під час рендеру. Запис
`onClick={...}` не є винятком. Подивімося на дві кнопки. Функція `pour` друкує назву напою й повертає її. Компонент і
тест лежать в одному файлі, ім'я якого закінчується на `.test.tsx`, наприклад `src/menu.test.tsx`. Команда
`npx vitest run src/menu.test.tsx` запускає такий файл:

```tsx
// @vitest-environment jsdom
// Цей коментар просить Vitest створити імітацію браузера, бо без документа компонент показати ніде.
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { test } from 'vitest'

function pour(drink: string) {
  console.log('наливаємо:', drink)
  return drink
}

function Menu() {
  console.log('рендер Menu')
  return (
    <>
      <button onClick={() => pour('Лате')}>Лате</button>
      {/* @ts-expect-error навмисна помилка */}
      <button onClick={pour('Чай')}>Чай</button>
    </>
  )
}

test('Menu', async () => {
  const user = userEvent.setup() // об'єкт user виконує дії людини, а його метод click клацає елемент
  render(<Menu />) // render показує компонент, тобто React викликає Menu
  console.log('рендер завершено, клацань ще не було')
  await user.click(screen.getByRole('button', { name: 'Лате' }))
})
```

Решта прикладів цієї лекції запускаються так само. Кожен дослід лежить у власному файлі, а рядки показу, клацання й
друку стоять усередині `test`. Перші рядки файла, `test` і створення `user` ми далі не повторюємо. Коли приклад
цього потребує, до імпортів додається `useState` з `react`, `within` з `@testing-library/react`, `vi` або `expect` з `vitest`. Vitest
друкує ще назву тесту й підсумок, а ми показуємо лише рядки, які надрукував сам код:

```text
рендер Menu
наливаємо: Чай
рендер завершено, клацань ще не було
наливаємо: Лате
```

Рядок «наливаємо: Чай» стоїть перед клацаннями. Запис `pour('Чай')` є звичайним викликом функції, тому JavaScript
виконав його, коли будував розмітку, і лише результат цього виклику потрапив у проп. Запис `() => pour('Лате')` теж
виконався під час рендеру, але результатом цього виразу є нова функція, а тіло цієї функції ще не виконувалося. React
запам'ятав її і викликав при клацанні.

Сторінка `Responding to Events` формулює це правило так: «Functions passed to event handlers must be passed, not
called». Ось три правильні й один неправильний запис поруч:

| Запис | Що обчислюється під час рендеру | Що отримує React |
|-------|---------------------------------|------------------|
| `onClick={addCup}` | лише ім'я | саму функцію |
| `onClick={() => addCup()}` | вираз зі стрілкою | нову функцію, яка викличе `addCup` |
| `onClick={function () { addCup() }}` | вираз із функцією | те саме, але довше |
| `onClick={addCup()}` | виклик `addCup` | результат виклику |

### Що React робить із тим, що отримав

У попередньому прикладі кнопка «Чай» отримала рядок. Наступний дослід передає в `onClick` чотири різні значення й
клацає кожну кнопку. React друкує свої повідомлення через `console.error`, а разом із текстом іде довгий стек викликів.
Тому дослід замінює `console.error` функцією `printMessage`, яка друкує лише текст. Помилку, яка виникає під час
клацання, ловить слухач події `error` на `window`:

```tsx
// React передає шаблон із позначками %s і окремо значення для них, а ця функція складає їх у текст.
function printMessage(template: string, ...values: unknown[]) {
  let next = 0
  console.log('React пише:', template.replace(/%s/g, () => String(values[next++])))
}

function addCup() {
  console.log('addCup виконано')
}
function silent() {
  console.log('silent виконано') // функція нічого не повертає, тому її результат дорівнює undefined
}
const ready = false

function Values() {
  return (
    <>
      <button onClick={addCup}>функція</button>
      {/* @ts-expect-error навмисна помилка */}
      <button onClick={silent()}>undefined</button>
      {/* @ts-expect-error навмисна помилка */}
      <button onClick="Чай">рядок</button>
      {/* @ts-expect-error навмисна помилка */}
      <button onClick={ready && addCup}>false</button>
    </>
  )
}

vi.spyOn(console, 'error').mockImplementation(printMessage) // тепер повідомлення React потрапляють у printMessage
window.addEventListener('error', (event) => {
  event.preventDefault() // прибирає довгий друк цієї помилки, який jsdom робить сам
  console.log('помилка при клацанні:', event.error.message)
})

render(<Values />)
for (const name of ['функція', 'undefined', 'рядок', 'false']) {
  console.log('клацання:', name)
  await user.click(screen.getByRole('button', { name }))
}
```

```text
silent виконано
React пише: Expected `onClick` listener to be a function, instead got a value of `string` type.
React пише: Expected `onClick` listener to be a function, instead got `false`.

If you used to conditionally omit it with onClick={condition && value}, pass onClick={condition ? value : undefined} instead.
клацання: функція
addCup виконано
клацання: undefined
клацання: рядок
помилка при клацанні: Expected `onClick` listener to be a function, instead got a value of `string` type.
клацання: false
помилка при клацанні: listener is not a function
```

Прочитайте вивід зверху вниз. Рядки перед першим словом «клацання» надруковано під час рендеру. Рядок
`silent виконано` показує, що виклик `silent()` спрацював ще під час рендеру, а в проп потрапив `undefined`. Про це React
не написав нічого. Про рядок і про `false` React написав одразу. Потім кнопка з функцією викликала `addCup`, кнопка з
`undefined` не зробила нічого, а кнопки з рядком і `false` дали помилки. Таблиця збирає цей вивід:

| Значення в `onClick` | Звідки береться | Під час рендеру | При клацанні |
|----------------------|-----------------|-----------------|--------------|
| функція | `onClick={addCup}` | нічого | React викликає функцію |
| `undefined` | `onClick={addCup()}`, коли функція нічого не повертає | нічого | нічого, помилки немає |
| рядок | `onClick={pour('Чай')}` | повідомлення ``Expected `onClick` listener to be a function`` | помилка з тим самим текстом |
| `false` | `onClick={ready && addCup}` | схоже повідомлення з порадою писати `onClick={condition ? value : undefined}` | помилка `listener is not a function` |

Отже, в `onClick` кладіть лише функцію, а якщо обробник потрібен за умовою, пишіть `ready ? addCup : undefined`.

Рядок із `undefined` є найнеприємнішим, бо нічого не повідомляє. Функція спрацювала один раз під час рендеру, а кнопка
мовчки не робить нічого. Помилку такого виду бачить лише `tsc`. У досліді вище рядок `@ts-expect-error` просив `tsc` не
повідомляти про помилку в наступному рядку. Покладемо той самий запис без цього рядка у файл `src/dead.tsx`:

```tsx
function silent() {
  console.log('silent виконано')
}

export function Dead() {
  return <button onClick={silent()}>Мертва кнопка</button>
}
```

```text
$ npx tsc --noEmit -p tsconfig.app.json
src/dead.tsx(6,18): error TS2322: Type 'void' is not assignable to type 'MouseEventHandler<HTMLButtonElement> | undefined'.
```

Числа в дужках означають рядок і колонку у файлі. Тип `void` означає, що функція нічого не повертає. Отже, компілятор
каже, що в `onClick` стоїть результат виклику, а не обробник. Якщо кнопка не реагує на клацання, а в консолі порожньо,
запустіть цю команду.

### Навіщо стрілка

Стрілка потрібна тоді, коли функції треба передати аргумент. Якщо написати ім'я без дужок, аргумент передати ніде, а
якщо написати дужки, функція виконається під час рендеру. Стрілка розв'язує обидві проблеми: вона сама є функцією без
обов'язкових аргументів, а всередині викликає те, що треба, з потрібним аргументом.

Стрілка, створена в циклі, пам'ятає свою змінну. Лекція «Функції та замикання» пояснила цей механізм, який називається
**замиканням**: функція бачить змінні місця, де її створено. Для кожного напою в `drinks.map((drink) => ...)`
створюється власна змінна `drink` і власна стрілка, тому кожна кнопка передає свою назву.

### Що отримує обробник

React викликає обробник з одним аргументом, **об'єктом події**. Зазвичай його називають `e`:

```tsx
import type { MouseEvent } from 'react' // тип події React, а не однойменний тип браузера

function Latte() {
  function show(e: MouseEvent<HTMLButtonElement>) {
    const target = e.target as HTMLElement
    console.log(e.constructor.name, '|', e.type)
    console.log('target', target.tagName, '| currentTarget', e.currentTarget.tagName)
    console.log('nativeEvent', e.nativeEvent.constructor.name)
  }
  return <button onClick={show}><b>Лате</b></button>
}

render(<Latte />)
await user.click(screen.getByText('Лате'))
```

```text
SyntheticBaseEvent | click
target B | currentTarget BUTTON
nativeEvent PointerEvent
```

Цей об'єкт створює сам React, і документація називає його React event object або синтетичною подією. За будовою він
повторює звичайну подію браузера, а справжня подія лежить у полі `nativeEvent`. Поля `target` і `currentTarget`
означають те саме, що в лекції «DOM і події»: `target` є вузлом, де подія виникла, а `currentTarget` є вузлом, на
якому стоїть цей обробник.

Звідси випливає наступна пастка. Запис `onClick={pick}`, де функція `pick` чекає на назву напою, передає функцію
правильно, але при клацанні `pick` отримає об'єкт події, а не рядок.

### Як можна назвати проп

Вбудовані теги розуміють лише назви подій браузера. Перевіримо дві помилки в назві пропа. Функція `printMessage` тут
та сама, що в досліді зі значеннями `onClick`:

```tsx
function f() {
  console.log('f викликано')
}

vi.spyOn(console, 'error').mockImplementation(printMessage)
render(
  <>
    {/* @ts-expect-error навмисна помилка */}
    <button onSmash={f}>Перша</button>
    {/* @ts-expect-error навмисна помилка */}
    <button onclick={f}>Друга</button>
  </>,
)
await user.click(screen.getByRole('button', { name: 'Перша' }))
await user.click(screen.getByRole('button', { name: 'Друга' }))
console.log('клацання завершено')
```

```text
React пише: Unknown event handler property `onSmash`. It will be ignored.
React пише: Invalid event handler property `onclick`. Did you mean `onClick`?
клацання завершено
```

Два повідомлення React надрукував під час рендеру. Рядка `f викликано` у виводі немає, отже, в обох випадках обробника
на кнопці немає. Якщо прибрати рядки `@ts-expect-error`, `tsc` повідомляє про зайву властивість:

```text
$ npx tsc --noEmit -p tsconfig.app.json
src/names.test.tsx(22,13): error TS2322: Type '{ children: string; onSmash: () => void; }' is not assignable to type 'DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement>'.
  Property 'onSmash' does not exist on type 'DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement>'.
src/names.test.tsx(23,13): error TS2322: Type '{ children: string; onclick: () => void; }' is not assignable to type 'DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement>'.
  Property 'onclick' does not exist on type 'DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement>'. Did you mean 'onClick'?
```

Отже, вбудованому тегу пишіть назву події точно, а виправити її підкаже `tsc`. У власних компонентах назву вибираєте
ви. Домовленість така: проп зі значенням-функцією називають `on` із великою літерою далі, наприклад
`onPick`, а саму функцію всередині компонента називають `handle` з назвою події, наприклад `handleClick`. Це лише
домовленість, яка робить код зрозумілішим, і React її не перевіряє.

### Подія йде вгору, а кнопка у формі надсилає форму

У лекції «DOM і події» ви бачили, що подія спливає від вузла до його предків. У React це працює так само. Якщо людина
клацнула кнопку всередині картки, спершу спрацює `onClick` кнопки, потім `onClick` картки. Метод `e.stopPropagation()`
це спинить. Метод `e.preventDefault()` робить зовсім інше: він скасовує дію браузера за замовчуванням.

Найчастіша дія за замовчуванням трапляється у формах. За описом MDN, кнопка `<button>` усередині `<form>` без атрибута
`type` є кнопкою надсилання форми. Клацання по ній не лише запускає ваш `onClick`, а й надсилає форму:

```tsx
function Bar() {
  return (
    <form onSubmit={(e) => { e.preventDefault(); console.log('форму надіслано') }}>
      <button onClick={() => console.log('клік без type')}>Без type</button>
      <button type="button" onClick={() => console.log('клік з type')}>З type</button>
    </form>
  )
}

render(<Bar />)
await user.click(screen.getByRole('button', { name: 'Без type' }))
await user.click(screen.getByRole('button', { name: 'З type' }))
```

```text
клік без type
форму надіслано
клік з type
```

Якщо `onSubmit` не викликає `preventDefault`, у браузері форма надсилається звичним способом, і сторінка
перезавантажується разом з усім станом. Це твердження спирається на сторінку `Responding to Events`, бо jsdom переходу
не робить, а лише друкує повідомлення. Ось форма без `onSubmit`:

```tsx
function Plain() {
  return (
    <form>
      <button>Без type</button>
    </form>
  )
}

render(<Plain />)
await user.click(screen.getByRole('button'))
```

```text
Not implemented: HTMLFormElement's requestSubmit() method
```

Цей рядок означає, що клацання справді почало надсилати форму, а jsdom не вміє виконати цю дію. Тому кнопки міст у заготовці дня мають `type="button"`: вони
лежать усередині `<form>` і нічого надсилати не повинні.

## Чому звичайна змінна не може бути пам'яттю

Тепер друга помилка з першого прикладу. Виправимо `onClick` і додамо другу кнопку, яка змусить компонент
перемалюватися. Для цього нам знадобиться `useState`, який ми розберемо трохи нижче. Поки що зверніть увагу лише на
змінну `cups`:

```tsx
let renders = 0

function PlainOrder() {
  renders = renders + 1
  let cups = 0
  const [, setTick] = useState(0)
  return (
    <>
      <p>Чашок: {cups}</p>
      <button onClick={() => { cups = cups + 1; console.log('в обробнику cups =', cups) }}>Ще чашка</button>
      <button onClick={() => setTick(1)}>Перемалювати</button>
    </>
  )
}

render(<PlainOrder />)
await user.click(screen.getByRole('button', { name: 'Ще чашка' }))
await user.click(screen.getByRole('button', { name: 'Ще чашка' }))
console.log(screen.getByText(/Чашок/).textContent, '| рендерів:', renders)
await user.click(screen.getByRole('button', { name: 'Перемалювати' }))
console.log(screen.getByText(/Чашок/).textContent, '| рендерів:', renders)
await user.click(screen.getByRole('button', { name: 'Ще чашка' }))
```

```text
в обробнику cups = 1
в обробнику cups = 2
Чашок: 0 | рендерів: 1
Чашок: 0 | рендерів: 2
в обробнику cups = 1
```

Вивід показує дві незалежні причини, і сторінка `State: A Component's Memory` називає саме їх.

**Перша причина: зміна змінної нічого не просить.** Перші два рядки показують, що обробник працює і змінна справді
росте. Але напис лишився «Чашок: 0», а рендер був один. React не стежить за вашими змінними, тому не знає, що щось
змінилося.

**Друга причина: змінна живе один виклик.** Навіть коли компонент перемалювався, напис знову показує 0. React викликав
`PlainOrder` ще раз, і рядок `let cups = 0` створив нову змінну. Останній рядок виводу доводить це інакше: новий
обробник почав рахувати з одиниці, бо він замкнув нову змінну, а не стару.

Лінтер помічає таку спробу. Звичайний вивід ESLint для кожного зауваження друкує ще цитату коду й абзац пояснень. Тому
ми просимо ESLint видати результат у форматі JSON, а короткий скрипт Node друкує з нього назву правила, перший рядок
повідомлення й рядок коду, якого воно стосується. Файлом досліду тут є `src/plain-order.test.tsx`:

```bash
npx eslint src/plain-order.test.tsx -f json | node -e "
  const [file] = JSON.parse(require('fs').readFileSync(0))
  const lines = file.source.split('\n')
  for (const m of file.messages) console.log(m.ruleId, '|', m.message.split('\n')[0], '|', lines[m.line - 1].trim())"
```

```text
react-hooks/globals | Error: Cannot reassign variables declared outside of the component/hook | renders = renders + 1
react-hooks/immutability | Error: Cannot modify local variables after render completes | <button onClick={() => { cups = cups + 1; console.log('в обробнику cups =', cups) }}>Ще чашка</button>
react-hooks/immutability | Error: Cannot reassign variable after render completes | <button onClick={() => { cups = cups + 1; console.log('в обробнику cups =', cups) }}>Ще чашка</button>
```

Рядок із правилом `react-hooks/globals` стосується лічильника `renders`, який ми поставили лише для досліду. Два рядки
з правилом `react-hooks/immutability` стосуються зміни `cups` в обробнику. Отже, коли лінтер називає це правило, значення
мусить стати станом. `tsc` мовчить, бо для типів тут усе правильно.

### А якщо винести змінну за межі компонента

Змінна поза функцією не створюється заново, тому друга причина зникає. Перша лишається, і з'являється нова проблема:

```tsx
let cups = 0

function SharedOrder({ table }: { table: string }) {
  return <button onClick={() => { cups = cups + 1 }}>{table}: {cups}</button>
}
const page = <><SharedOrder table="Стіл 1" /><SharedOrder table="Стіл 2" /></>

const { rerender } = render(page)
await user.click(screen.getByRole('button', { name: /Стіл 1/ }))
await user.click(screen.getByRole('button', { name: /Стіл 1/ }))
console.log(screen.getAllByRole('button').map((b) => b.textContent))
rerender(<><SharedOrder table="Стіл 1" /><SharedOrder table="Стіл 2" /></>)
console.log(screen.getAllByRole('button').map((b) => b.textContent))
```

```text
[ 'Стіл 1: 0', 'Стіл 2: 0' ]
[ 'Стіл 1: 2', 'Стіл 2: 2' ]
```

Після клацань екран не змінився, бо рендеру ніхто не просив. Функція `rerender` із Testing Library показує той самий
компонент ще раз, і тоді число з'явилося, але відразу на обох столах, хоча клацали лише по першому. Змінна модуля є
однією на всі екземпляри компонента. Вона годиться, щоб у дослідах рахувати рендери, але не годиться, щоб показувати
дані на екрані.

Отже, пам'ять компонента мусить робити дві речі: зберігати значення між викликами функції й просити новий рендер, коли
значення змінилося. Обидві роботи виконує React.

## `useState`: дві роботи в одному виклику

**Хуком** називають функцію, ім'я якої починається з `use` і яка дає компоненту доступ до можливостей React. Її можна
викликати лише під час рендеру. **Станом** називають дані, які React зберігає для компонента між рендерами. Хук
`useState` створює одну таку комірку даних.

```tsx
const [cups, setCups] = useState(1)
```

`useState` повертає масив із двох значень. Квадратні дужки зліва є **деструктуризацією масиву**: перше значення лягає
в `cups`, друге в `setCups`. Імена вибираєте ви, а домовленість така: `щось` і `setЩось`. Перше значення є поточним
станом на цей рендер. Друге є функцією, яка просить React запам'ятати нове значення й викликати компонент знову. Цю
функцію далі будемо називати **функцією `set`**. Єдиний аргумент `useState` є початковим значенням.

### Простежимо за числами

Компонент друкує пару на кожному рендері. Початкове значення приходить з пропа `start`, і ми навмисно змінимо цей проп
після клацання:

```tsx
const setters: unknown[] = []

function Order({ start }: { start: number }) {
  const pair = useState(start)
  const [cups, setCups] = pair
  setters.push(setCups)
  console.log('рендер:', typeof pair[0], typeof pair[1], '| cups =', cups)
  return <button onClick={() => setCups(cups + 1)}>Чашок: {cups}</button>
}

const { rerender } = render(<Order start={2} />)
await user.click(screen.getByRole('button'))
rerender(<Order start={10} />)
console.log('на кнопці:', screen.getByRole('button').textContent)
console.log('та сама функція set?', setters[0] === setters[1], setters[1] === setters[2])
```

```text
рендер: number function | cups = 2
рендер: number function | cups = 3
рендер: number function | cups = 3
на кнопці: Чашок: 3
та сама функція set? true true
```

| Крок | Хто діє | Що відбувається |
|------|---------|-----------------|
| 1 | React | викликає `Order` вперше |
| 2 | `useState(2)` | комірки ще немає, React створює її зі значенням 2 й повертає пару `[2, setCups]` |
| 3 | людина | клацає кнопку, React викликає стрілку |
| 4 | стрілка | обчислює `2 + 1` і викликає `setCups(3)` |
| 5 | React | запам'ятовує 3 й викликає `Order` знову |
| 6 | `useState(2)` | комірка вже є, тому аргумент ігнорується, повертається `[3, setCups]` |
| 7 | батько | передає `start={10}`, React викликає `Order` утретє |
| 8 | `useState(10)` | комірка вже є, тому число 10 теж ігнорується, повертається `[3, setCups]` |

Звідси два наслідки. По-перше, аргумент `useState` є лише **початковим** значенням. Якщо він приходить із пропа,
наступні зміни пропа стан не змінять. По-друге, функція `set` лишається тією самою між рендерами, тому її безпечно
передавати далі.

Сьогодні записуйте лише те, що функція `set` просить новий рендер. Чому `cups` не змінюється в обробнику одразу після
виклику `setCups`, докладно пояснить наступний день, «Рендер, коміт і знімок стану».

### Кілька станів і правило про місце виклику

У компоненті може бути скільки завгодно викликів `useState`. Функція не отримує імені стану, тому React розрізняє їх
за порядком: перший виклик бере першу комірку, другий другу. Лекція «Проєкт: Vite, лінт, TypeScript» уже показала,
чому хук не можна класти під умову: тоді порядок зміниться між рендерами. Сторінка `State: A Component's Memory` прямо
каже, що хуки викликають лише на верхньому рівні компонента або власного хука.

Обробник теж не годиться. Обробник виконується після рендеру, коли React уже не знає, який компонент зараз
обчислюється. Перевіримо це:

```tsx
function HookInHandler() {
  function handleClick() {
    const [cups] = useState(0) // навмисна помилка: хук в обробнику
    console.log('чашок:', cups)
  }
  return <button onClick={handleClick}>Ще чашка</button>
}

window.addEventListener('error', (event) => {
  event.preventDefault()
  console.log('помилка при клацанні:', event.error.message.split('\n')[0]) // перший рядок повідомлення
})
render(<HookInHandler />)
await user.click(screen.getByRole('button'))
```

```text
помилка при клацанні: Invalid hook call. Hooks can only be called inside of the body of a function component. This could happen for one of the following reasons:
```

Рядка `чашок:` немає, бо `useState` зупинив обробник помилкою. Скрипт ESLint із попереднього розділу помічає цю помилку
ще до запуску:

```text
react-hooks/rules-of-hooks | React Hook "useState" is called in function "handleClick" that is neither a React function component nor a custom React Hook function. React component names must start with an uppercase letter. React Hook names must start with the word "use". | const [cups] = useState(0) // навмисна помилка: хук в обробнику
```

Отже, усі `useState` пишіть на верхньому рівні компонента, а в обробнику викликайте лише функцію `set`.

### Виклик `set` під час рендеру

Тепер ви можете передбачити, що станеться з `onClick={setCups(cups + 1)}`. Виклик виконується під час рендеру, тому
просить новий рендер. Новий рендер знову виконує цей вираз, і так без кінця. Другий компонент нижче робить те саме, але
під умовою:

```tsx
function Loop() {
  const [cups, setCups] = useState(0)
  // @ts-expect-error навмисна помилка
  return <button onClick={setCups(cups + 1)}>Чашок: {cups}</button>
}

function Limited() {
  const [cups, setCups] = useState(0)
  // @ts-expect-error навмисна помилка
  return <button onClick={cups < 3 ? setCups(cups + 1) : undefined}>Чашок: {cups}</button>
}

try {
  render(<Loop />)
} catch (error) {
  console.log((error as Error).message) // без цього перехоплення помилка зупинила б тест
}
render(<Limited />)
console.log(screen.getByRole('button').textContent)
```

```text
Too many re-renders. React limits the number of renders to prevent an infinite loop.
Чашок: 3
```

Перший рядок показує, що React помітив цикл і зупинив його. Другий рядок показує випадок із умовою: цикл зупинився сам,
помилки немає, а лічильник показує 3 ще до першого клацання. Теорія дня розбирає саме такий випадок. Скрипт ESLint
указує лише на компонент `Loop`, а запис під умовою пропускає:

```text
react-hooks/set-state-in-render | Error: Cannot call setState during render | return <button onClick={setCups(cups + 1)}>Чашок: {cups}</button>
```

Отже, лінтер не гарантує, що такого виклику немає. Якщо число на екрані виросло без жодного клацання, шукайте виклик
функції `set` у тілі компонента або в `onClick` із дужками.

## Кероване поле

Поле `<input>` має власну пам'ять: браузер зберігає в ньому набраний текст. Лекція «DOM і події» називала цю пам'ять
властивістю `value`. Отже, є два способи працювати з полем.

**Некероване поле** зберігає текст саме. Запис `<input defaultValue="Кава" />` задає лише початкове значення, а далі
людина друкує, що хоче, і React не втручається.

**Кероване поле** отримує `value` зі стану. Сторінка довідника `<input>` описує це так: React змушує поле завжди мати
те значення, яке ви передали. Тому вам потрібен і другий проп, `onChange`, який оновлює стан:

```tsx
const [text, setText] = useState('')
return <input value={text} onChange={(e) => setText(e.target.value)} />
```

### Від клавіші до літери

Людина натискає клавішу «л» у порожньому полі:

| Крок | Хто діє | Що відбувається |
|------|---------|-----------------|
| 1 | браузер | додає літеру до поля, у `value` тепер `л` |
| 2 | браузер | повідомляє про подію, вона доходить до кореня React |
| 3 | React | викликає ваш `onChange` |
| 4 | ваша стрілка | читає `e.target.value`, тобто `л`, і викликає `setText('л')` |
| 5 | React | викликає компонент, тепер `text` дорівнює `л` |
| 6 | React | бачить, що поле вже показує `л`, і лишає все як є |

Шостий крок вирішує все. Поле завжди приводиться до значення зі стану, тому `onChange` не лише зберігає текст, а й
може його змінити. Цей дослід показує, що саме приходить у `e.target.value`, якщо стан відрізняється від набраного:

```tsx
function Shout() {
  const [text, setText] = useState('')
  return (
    <input
      aria-label="напис"
      value={text}
      onChange={(e) => {
        console.log('прийшло:', e.target.value)
        setText(e.target.value.toUpperCase())
      }}
    />
  )
}
function Digits() {
  const [code, setCode] = useState('')
  return <input aria-label="код" value={code} onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))} />
}
const value = (label: string) => screen.getByLabelText<HTMLInputElement>(label).value

render(<><Shout /><Digits /></>)
await user.type(screen.getByLabelText('напис'), 'лате')
await user.type(screen.getByLabelText('код'), 'a1b2')
console.log('у полі напису:', value('напис'))
console.log('у полі коду:', value('код'))
```

```text
прийшло: л
прийшло: Ла
прийшло: ЛАт
прийшло: ЛАТе
у полі напису: ЛАТЕ
у полі коду: 12
```

Прочитайте рядки «прийшло». Перед кожним натисканням поле вже показувало великі літери зі стану, а браузер дописав
нову маленьку. Поле коду показує те саме з іншого боку: літери `a` і `b` стан не прийняв, тому React повернув полю
попереднє значення, і вони не залишилися на екрані.

Такий прийом має межу. Довідник `<input>` у розділі `My input caret jumps to the beginning on every keystroke`
попереджає, що запис у стан чогось іншого, ніж `e.target.value`, може зсунути курсор на початок поля. У jsdom курсора,
який бачить людина, немає, тому ми цього не перевірили. Сьогодні в практиці стан отримує рівно `e.target.value`, і
цієї проблеми немає.

Цей дослід показує ще дві властивості. Проп `onChange` спрацьовує на кожне натискання. За описом MDN, браузерна подія
`change` для текстового поля спрацьовує лише тоді, коли людина завершила зміну, зазвичай при втраті фокуса, а довідник
React порівнює `onChange` саме з браузерною подією `input`. Ми це порівняння в браузері не перевіряли. Крім того,
`e.target.value` завжди є рядком, навіть у полі `type="number"`:

```tsx
function CupCount() {
  return (
    <input
      aria-label="чашки"
      type="number"
      onChange={(e) => {
        console.log('value:', typeof e.target.value, e.target.value)
        console.log('valueAsNumber:', typeof e.target.valueAsNumber, e.target.valueAsNumber)
      }}
    />
  )
}

render(<CupCount />)
await user.type(screen.getByLabelText('чашки'), '5')
```

```text
value: string 5
valueAsNumber: number 5
```

Набране `5` прийшло в `e.target.value` рядком, а число лежить окремо в `e.target.valueAsNumber`. Отже, коли стан має
бути числом, беріть значення з `valueAsNumber`.

### Три типові помилки

Цей дослід ставить поруч три неправильні поля й набирає в кожне літеру `х`. Функція `printMessage` тут та сама, що в
досліді зі значеннями `onClick`:

```tsx
function NoHandler() {
  return <input aria-label="без onChange" value="Кава" />
}
function NoStart() {
  const [text, setText] = useState<string>() // початкового значення немає, тому спершу text дорівнює undefined
  return <input aria-label="без початку" value={text} onChange={(e) => setText(e.target.value)} />
}
function NullValue() {
  // @ts-expect-error навмисна помилка
  return <input aria-label="з null" value={null} />
}

vi.spyOn(console, 'error').mockImplementation(printMessage)
render(<><NoHandler /><NoStart /><NullValue /></>)
for (const label of ['без onChange', 'без початку', 'з null']) {
  const input = screen.getByLabelText<HTMLInputElement>(label)
  await user.type(input, 'х')
  console.log(label, '| у полі:', input.value)
}
```

```text
React пише: You provided a `value` prop to a form field without an `onChange` handler. This will render a read-only field. If the field should be mutable use `defaultValue`. Otherwise, set either `onChange` or `readOnly`.
React пише: `value` prop on `input` should not be null. Consider using an empty string to clear the component or `undefined` for uncontrolled components.
без onChange | у полі: Кава
React пише: A component is changing an uncontrolled input to be controlled. This is likely caused by the value changing from undefined to a defined value, which should not happen. Decide between using a controlled or uncontrolled input element for the lifetime of the component. More info: https://react.dev/link/controlled-components
без початку | у полі: х
з null | у полі: х
```

Два перші повідомлення React надрукував під час першого рендеру: вони стосуються полів `NoHandler` і `NullValue`. Третє
повідомлення з'явилося пізніше, коли після літери `х` значення `text` перестало бути `undefined`. Поле без `onChange`
зберегло слово «Кава», бо стан не змінився. Поле з `null` прийняло літеру, бо React ним не керує. Таблиця збирає цей
вивід:

| Запис | Що виходить | Що пише React |
|-------|-------------|---------------|
| `value={text}` без `onChange` | ввести нічого не можна, текст відразу зникає | ``You provided a `value` prop to a form field without an `onChange` handler`` |
| `useState()` без початкового значення | спершу `value` дорівнює `undefined`, тому поле некероване, а після першої літери стає керованим | `A component is changing an uncontrolled input to be controlled` |
| `value={null}` | поле спочатку порожнє, а далі приймає текст, бо React ним не керує | `` `value` prop on `input` should not be null `` |

Звідси правило: початковим значенням текстового поля є порожній рядок `''`. Якщо поле справді лише показує значення,
додайте проп `readOnly`, і попередження зникне.

### Тип події

Коли стрілка стоїть просто в `onChange`, TypeScript сам знає тип `e`, бо бачить, куди її передано. Якщо винести
обробник в окрему функцію, цей зв'язок зникає. Файл `src/name-field.tsx` має дві такі функції, одну без типу й одну з
типом:

```tsx
import { useState, type ChangeEvent } from 'react'

export function NameField() {
  const [text, setText] = useState('')
  function handleChange(e) { // тип параметра не вказано
    setText(e.target.value)
  }
  function handleTypedChange(e: ChangeEvent<HTMLInputElement>) {
    setText(e.target.value)
  }
  return (
    <>
      <input value={text} onChange={handleChange} />
      <input value={text} onChange={handleTypedChange} />
    </>
  )
}
```

```text
$ npx tsc --noEmit -p tsconfig.app.json
src/name-field.tsx(5,25): error TS7006: Parameter 'e' implicitly has an 'any' type.
```

Помилка стоїть лише на першій функції, а друга функція проходить перевірку. Отже, в окремій функції-обробнику завжди
вказуйте тип параметра. Тип `ChangeEvent` імпортують із пакета `react`. Докладно ці типи розбирає день фази «TypeScript у React».

## Дитина повідомляє батькові

Вибір напою винесемо в окремий компонент `DrinkPicker`. Він малює кнопки, але стан замовлення лежить у батька, тому що
батько показує замовлення в чеку. Лекція «Пропси й умовний рендер» пояснила, що пропси лише для читання, а дані течуть
униз. Дитина не може прочитати стан батька й не може його змінити. Проте батько може дати дитині функцію, бо функція
теж є значенням, а отже, може бути пропом:

```tsx
function DrinkPicker({ drinks, onPick }: { drinks: string[]; onPick: (drink: string) => void }) {
  return (
    <div>
      {drinks.map((drink) => (
        <button key={drink} type="button" onClick={() => onPick(drink)}>{drink}</button>
      ))}
    </div>
  )
}

function Order({ table }: { table: string }) {
  const [drink, setDrink] = useState('')
  const [cups, setCups] = useState(1)
  return (
    <section aria-label={table}>
      <DrinkPicker drinks={['Лате', 'Чай']} onPick={setDrink} />
      <button type="button" onClick={() => setCups(cups + 1)}>Ще чашка</button>
      <p>{table}: {drink || 'нічого'} × {cups}</p>
    </section>
  )
}

render(<Order table="Стіл 1" />)
console.log(screen.getByText(/Стіл 1/).textContent)
await user.click(screen.getByRole('button', { name: 'Чай' }))
console.log(screen.getByText(/Стіл 1/).textContent)
await user.click(screen.getByRole('button', { name: 'Ще чашка' }))
console.log(screen.getByText(/Стіл 1/).textContent)
```

```text
Стіл 1: нічого × 1
Стіл 1: Чай × 1
Стіл 1: Чай × 2
```

Простежимо клацання по кнопці «Чай»:

| Крок | Хто діє | Що відбувається |
|------|---------|-----------------|
| 1 | React | знаходить `onClick` кнопки «Чай» і викликає стрілку з об'єктом події |
| 2 | стрілка | ігнорує подію й викликає `onPick('Чай')`, де змінну `drink` вона замкнула під час рендеру |
| 3 | `onPick` | це та сама функція `setDrink`, яку передав батько, тому React отримує прохання записати `'Чай'` |
| 4 | React | викликає `Order`: тепер `drink` дорівнює `'Чай'`, а `cups` лишається 1 |
| 5 | React | викликає `DrinkPicker`, бо батько перемалювався, і оновлює в документі текст чека |

Дитина нічого не знає про те, що батько робить із вибором. Вона лише повідомила. Завдяки цьому той самий `DrinkPicker`
можна поставити в іншому місці, де вибір надсилають на сервер. Це і є правило: дані йдуть униз пропсами, а
повідомлення йдуть угору через функції-пропси.

Запис `onPick={setDrink}` стоїть без стрілки, тому що `setDrink` вже є функцією, яка приймає один аргумент. Запис
`onPick={(d) => setDrink(d)}` означає те саме, і стрілка потрібна, лише якщо батько хоче зробити щось іще.

### Чотири записи в дитині

Нижче чотири способи написати `onClick` у дитині. Лише перший правильний. Щоб побачити різницю, зробимо по кнопці на
кожен запис і передамо кожній підставну функцію `vi.fn()`. Ця функція запам'ятовує свої виклики, а докладніше про неї
йдеться в розділі про приклади нижче. Vitest типів не перевіряє, тому запускає цей файл, хоча `tsc` має до нього
зауваження:

```tsx
type Props = { drink: string; onPick: (drink: string) => void }

function Right({ drink, onPick }: Props) {
  return <button onClick={() => onPick(drink)}>{drink}</button>
}
function CalledInRender({ drink, onPick }: Props) {
  return <button onClick={onPick(drink)}>{drink}</button>
}
function NameOnly({ drink, onPick }: Props) {
  return <button onClick={onPick}>{drink}</button>
}
function NoCall({ drink, onPick }: Props) {
  return <button onClick={() => onPick}>{drink}</button>
}

for (const Button of [Right, CalledInRender, NameOnly, NoCall]) {
  const onPick = vi.fn()
  const { unmount } = render(<Button drink="Чай" onPick={onPick} />)
  const inRender = onPick.mock.calls.length // скільки викликів було ще до клацання
  await user.click(screen.getByRole('button'))
  const arg = onPick.mock.lastCall?.[0] // що отримав останній виклик
  const shown = typeof arg === 'string' ? arg : arg?.constructor.name
  console.log(Button.name, '| під час рендеру:', inRender, '| усього:', onPick.mock.calls.length, '| аргумент:', shown)
  unmount() // прибираємо кнопку, щоб наступний пошук знайшов лише одну
}
```

```text
Right | під час рендеру: 0 | усього: 1 | аргумент: Чай
CalledInRender | під час рендеру: 1 | усього: 1 | аргумент: Чай
NameOnly | під час рендеру: 0 | усього: 1 | аргумент: SyntheticBaseEvent
NoCall | під час рендеру: 0 | усього: 0 | аргумент: undefined
```

Ось що каже `tsc` про той самий файл `src/writes.test.tsx`:

```text
$ npx tsc --noEmit -p tsconfig.app.json
src/writes.test.tsx(13,18): error TS2322: Type 'void' is not assignable to type 'MouseEventHandler<HTMLButtonElement> | undefined'.
src/writes.test.tsx(16,18): error TS2322: Type '(drink: string) => void' is not assignable to type 'MouseEventHandler<HTMLButtonElement>'.
  Types of parameters 'drink' and 'event' are incompatible.
    Type 'MouseEvent<HTMLButtonElement, MouseEvent>' is not assignable to type 'string'.
```

Запис `CalledInRender` викликав `onPick` ще під час рендеру, а клацання не додало нового виклику. Запис `NameOnly` викликав
`onPick` при клацанні, але аргументом став об'єкт події. Запис `NoCall` не викликав `onPick` жодного разу, і `tsc` про
нього не згадав. Таблиця збирає цей вивід:

| Запис у `DrinkPicker` | Що станеться | Що каже `tsc` |
|-----------------------|--------------|---------------|
| `onClick={() => onPick(drink)}` | клацання передає назву напою | мовчить |
| `onClick={onPick(drink)}` | `onPick` спрацьовує під час рендеру для кожної кнопки, а клацання нічого не роблять | `TS2322`, тип `void` не є обробником |
| `onClick={onPick}` | `onPick` спрацьовує при клацанні, але отримує об'єкт події, а не назву | `TS2322`, параметри несумісні |
| `onClick={() => onPick}` | стрілка повертає функцію, але не викликає її, тому не відбувається нічого | мовчить |

Останній запис особливо підступний, бо типи правильні, а лінтер теж мовчить. Його ловить лише приклад у тесті.

Другий рядок таблиці має ще один наслідок, якщо `onPick` змінює стан батька. Тоді дитина викликає функцію `set` батька
під час власного рендеру. Якщо кнопок кілька, останній виклик перезапише попередні. Функція `printMessage` тут та сама,
що в досліді зі значеннями `onClick`:

```tsx
function Picker({ drinks, onPick }: { drinks: string[]; onPick: (drink: string) => void }) {
  return (
    <div>
      {drinks.map((drink) => (
        // @ts-expect-error навмисна помилка
        <button key={drink} onClick={onPick(drink)}>{drink}</button>
      ))}
    </div>
  )
}

function Cafe() {
  const [drink, setDrink] = useState('')
  return (
    <>
      <Picker drinks={['Лате', 'Чай']} onPick={setDrink} />
      <p>Обрано: {drink || 'нічого'}</p>
    </>
  )
}

vi.spyOn(console, 'error').mockImplementation(printMessage)
render(<Cafe />)
console.log(screen.getByText(/Обрано/).textContent)
```

```text
React пише: Cannot update a component (`Cafe`) while rendering a different component (`Picker`). To locate the bad setState() call inside `Picker`, follow the stack trace as described in https://react.dev/link/setstate-in-render
Обрано: Чай
```

Ніхто нічого не клацав, а в рядку «Обрано» вже стоїть «Чай», бо кнопка «Чай» остання, і її виклик записав стан після виклику кнопки
«Лате». Перший рядок виводу є попередженням React про те, що дитина змінює стан батька під час рендеру. Отже, якщо вибір
з'явився до клацання, шукайте дужки в `onClick`. Сторінка дня показує це на кнопках міст у розділі про типові помилки.

### Кожен рендер створює нові стрілки

Запишемо стрілки кнопок двох рендерів у масив і порівняємо їх:

```tsx
const saved: { latte: () => void; tea: () => void }[] = [] // стрілки кожного рендеру

function Drinks() {
  const [drink, setDrink] = useState('')
  const latte = () => setDrink('Лате')
  const tea = () => setDrink('Чай')
  saved.push({ latte, tea })
  return (
    <>
      <button onClick={latte}>Лате</button>
      <button onClick={tea}>Чай</button>
      <p>{drink}</p>
    </>
  )
}

render(<Drinks />)
await user.click(screen.getByRole('button', { name: 'Лате' }))
console.log('рендерів:', saved.length)
console.log('Лате, перший і другий рендер:', saved[0].latte === saved[1].latte)
console.log('Лате й Чай, перший рендер:', saved[0].latte === saved[0].tea)
```

```text
рендерів: 2
Лате, перший і другий рендер: false
Лате й Чай, перший рендер: false
```

Стрілка кнопки «Лате» першого рендеру не дорівнює стрілці тієї самої кнопки другого рендеру, а стрілки різних кнопок
теж різні. Це звичайна поведінка функцій у
JavaScript, і зазвичай це нікому не шкодить. Фаза 2 покаже, коли така різниця має значення для швидкодії.

## Стан належить екземпляру

Функція `Order` одна, а поставити її можна двічі. **Екземпляром** компонента називають одне конкретне місце на екрані,
де він показаний. Сторінка `State: A Component's Memory` у розділі `State is isolated and private` каже, що стан є
локальним для екземпляра:

```tsx
render(<><Order table="Стіл 1" /><Order table="Стіл 2" /></>)
const first = within(screen.getByRole('region', { name: 'Стіл 1' }))
await user.click(first.getByRole('button', { name: 'Лате' }))
await user.click(first.getByRole('button', { name: 'Ще чашка' }))
console.log(screen.getByText(/Стіл 1:/).textContent)
console.log(screen.getByText(/Стіл 2:/).textContent)
```

```text
Стіл 1: Лате × 2
Стіл 2: нічого × 1
```

Функція `within` з Testing Library обмежує пошук одним вузлом. Вона потрібна тут тому, що кнопка «Лате» є на обох
столах. Запис `getByRole('region', { name: 'Стіл 1' })` знаходить `<section>` за його ім'ям, яке дав атрибут
`aria-label`.

Стан живе, поки екземпляр стоїть на екрані. Якщо батько прибере компонент і поставить знову, це вже новий екземпляр:

```tsx
function Hall() {
  const [open, setOpen] = useState(true)
  return (
    <>
      <button onClick={() => setOpen(!open)}>Сховати чи показати</button>
      {open && <Order table="Стіл 3" />}
    </>
  )
}

render(<Hall />)
await user.click(screen.getByRole('button', { name: 'Ще чашка' }))
console.log(screen.getByText(/Стіл 3:/).textContent)
await user.click(screen.getByRole('button', { name: 'Сховати чи показати' }))
await user.click(screen.getByRole('button', { name: 'Сховати чи показати' }))
console.log(screen.getByText(/Стіл 3:/).textContent)
```

```text
Стіл 3: нічого × 2
Стіл 3: нічого × 1
```

Точне правило, коли React вважає екземпляр тим самим, пов'язане з позицією в дереві й докладно розглядається в день
«Спільний стан і скидання стану». Там само ви побачите, що робити, коли дві форми мають показувати те саме значення:
стан переносять у спільного батька.

Стан також є приватним. Батько не знає, чи є в дитини стан, і не може його прочитати. Якщо дані потрібні батькові,
вони мають лежати в батька, як `drink` у нашому `Order`.

## Кілька полів: кілька станів чи один об'єкт

Для форми з двома полями є два способи: два виклики `useState` або один стан-об'єкт. Обидва працюють, але другий має
пастку. Функція `set` не зливає об'єкти, а замінює значення повністю:

```tsx
function Note() {
  const [order, setOrder] = useState({ drink: 'Лате', note: '' })
  return (
    <>
      {/* @ts-expect-error навмисна помилка */}
      <input aria-label="побажання" value={order.note} onChange={(e) => setOrder({ note: e.target.value })} />
      <p>{JSON.stringify(order)}</p>
    </>
  )
}

render(<Note />)
await user.type(screen.getByLabelText('побажання'), 'х')
console.log(screen.getByText(/note/).textContent)
```

```text
{"note":"х"}
```

Поле `drink` зникло, бо новий об'єкт його не містить. `tsc` тут допомагає. Якщо прибрати з цього коду рядок
`@ts-expect-error`, команда друкує таке:

```text
$ npx tsc --noEmit -p tsconfig.app.json
src/note.test.tsx(12,82): error TS2345: Argument of type '{ note: string; }' is not assignable to parameter of type 'SetStateAction<{ drink: string; note: string; }>'.
  Property 'drink' is missing in type '{ note: string; }' but required in type '{ drink: string; note: string; }'.
```

Тобто об'єкт `{ note: string; }` не підходить під тип стану, бо в ньому немає поля `drink`. Правильний запис копіює решту полів розгортанням, `setOrder({ ...order, note: e.target.value
})`, про що ви вже знаєте з лекції «Масиви й об'єкти функційно». Стани-об'єкти докладно розгляне день «Об'єкти й
масиви в стані». Сьогодні зручніше брати окремий `useState` на кожне поле, бо вони не пов'язані між собою.

## Рецепт: що додає стан

Рецепт із книжки How to Design Programs лишається тим самим, але сьогодні в кроку «перелік вхідних даних» стає більше
рядків. До пропсів додаються значення станів і їхні функції `set`. Це справді вхідні дані тіла компонента, бо воно
будує розмітку з них.

| Крок рецепта | Для компонента `DrinkPicker` |
|--------------|-------------------------------|
| опис даних | тип пропсів і коментар, що `onPick` викликають із назвою напою |
| призначення й сигнатура | одне речення над функцією й тип пропсів у коді |
| приклади | кнопка на кожен напій, виклик під час клацання, нічого під час рендеру |
| перелік вхідних даних | коментар у тілі: `drinks`, `onPick` |
| тіло | `map` і стрілка в `onClick` |
| перевірка | Vitest запускає приклади, а `tsc` перевіряє типи |

### Як написати приклад про дію людини

Бібліотека `user-event` імітує дію людини. Виклик `userEvent.setup()` створює сеанс, `await user.click(елемент)`
клацає, а `await user.type(елемент, текст)` друкує текст по літері. `await` потрібен, бо ці дії асинхронні: між
кроками бібліотека дає виконатися іншому коду.

Функцію-проп перевіряють **шпигуном**, тобто підставною функцією, яка запам'ятовує свої виклики. У Vitest її створює
`vi.fn()`. Ось як виглядають приклади, якщо записати пастку дня наперед, ще до тіла компонента:

```tsx
const onPick = vi.fn()
render(<DrinkPicker drinks={['Лате', 'Чай']} onPick={onPick} />)
expect(onPick).not.toHaveBeenCalled()
await user.click(screen.getByRole('button', { name: 'Чай' }))
expect(onPick).toHaveBeenCalledExactlyOnceWith('Чай')
console.log('виклики:', JSON.stringify(onPick.mock.calls))
```

```text
виклики: [["Чай"]]
```

Вивід досліду з чотирма записами пояснює, що станеться з цими перевірками. Перша перевірка падає на
`onClick={onPick(drink)}`, бо функція спрацювала під час рендеру. Друга падає на
`onClick={onPick}`, бо аргументом був об'єкт події, і на `onClick={() => onPick}`, бо виклику не було. Отже, два рядки
перевіряють усі неправильні записи з таблиці вище, зокрема той, про який мовчать `tsc` і лінтер.

Запит за роллю `form` у файлах дня теж потребує пояснення. Тег `<form>` отримує роль `form` лише тоді, коли має
доступне ім'я, тому в заготовці стоїть `aria-label={title}`. Без цього атрибута `getByRole('form')` нічого не знайде.
Метод `queryAllByRole` шукає так само, але повертає масив і не кидає помилки, тому кількість знайденого можна надрукувати:

```tsx
const { unmount } = render(<form />)
console.log('форма без імені:', screen.queryAllByRole('form').length)
unmount()
render(<form aria-label="Замовлення" />)
console.log('форма з іменем:', screen.queryAllByRole('form').length)
```

```text
форма без імені: 0
форма з іменем: 1
```

Отже, коли тест шукає форму за роллю, дайте формі ім'я.

## Хто яку помилку ловить

Зберемо помилки цієї лекції в один файл `src/mistakes.tsx` і запустимо на ньому `tsc` та скрипт ESLint, який ви бачили в
розділі про звичайну змінну:

```tsx
import { useState } from 'react'

function show() {
  console.log('показ')
}

export function PrintsOnRender() {
  return <button onClick={show()}>Показати</button>
}

export function SetsOnRender() {
  const [cups, setCups] = useState(0)
  function add() {
    setCups(cups + 1)
  }
  return <button onClick={add()}>Чашок: {cups}</button>
}

export function PassesName({ onPick }: { onPick: (drink: string) => void }) {
  return <button onClick={onPick}>Чай</button>
}

export function NeverCalls({ onPick }: { onPick: (drink: string) => void }) {
  return <button onClick={() => onPick}>Чай</button>
}

export function PlainVariable() {
  let cups = 0
  return <button onClick={() => { cups = cups + 1 }}>Чашок: {cups}</button>
}

export function HookInHandler() {
  return <button onClick={() => { const [cups] = useState(0); console.log(cups) }}>Клік</button>
}

export function NoOnChange({ text }: { text: string }) {
  return <input value={text} />
}

export function ReplacesObject() {
  const [order, setOrder] = useState({ drink: 'Лате', note: '' })
  return <input value={order.note} onChange={(e) => setOrder({ note: e.target.value })} />
}

export function NoType() {
  return <form><button onClick={show}>Показати</button></form>
}
```

```text
$ npx tsc --noEmit -p tsconfig.app.json
src/mistakes.tsx(8,18): error TS2322: Type 'void' is not assignable to type 'MouseEventHandler<HTMLButtonElement> | undefined'.
src/mistakes.tsx(16,18): error TS2322: Type 'void' is not assignable to type 'MouseEventHandler<HTMLButtonElement> | undefined'.
src/mistakes.tsx(20,18): error TS2322: Type '(drink: string) => void' is not assignable to type 'MouseEventHandler<HTMLButtonElement>'.
  Types of parameters 'drink' and 'event' are incompatible.
    Type 'MouseEvent<HTMLButtonElement, MouseEvent>' is not assignable to type 'string'.
src/mistakes.tsx(42,62): error TS2345: Argument of type '{ note: string; }' is not assignable to parameter of type 'SetStateAction<{ drink: string; note: string; }>'.
  Property 'drink' is missing in type '{ note: string; }' but required in type '{ drink: string; note: string; }'.
```

```text
react-hooks/set-state-in-render | Error: Cannot call setState during render | return <button onClick={add()}>Чашок: {cups}</button>
react-hooks/immutability | Error: Cannot modify local variables after render completes | return <button onClick={() => { cups = cups + 1 }}>Чашок: {cups}</button>
react-hooks/immutability | Error: Cannot reassign variable after render completes | return <button onClick={() => { cups = cups + 1 }}>Чашок: {cups}</button>
react-hooks/rules-of-hooks | React Hook "useState" cannot be called inside a callback. React Hooks must be called in a React function component or a custom React Hook function. | return <button onClick={() => { const [cups] = useState(0); console.log(cups) }}>Клік</button>
```

`tsc` указав на рядки 8, 16, 20 і 42. ESLint указав на рядки 16, 29 і 33. Компоненти `NeverCalls`, `NoOnChange` і
`NoType` не згадав жоден із них. Таблиця збирає цей вивід, а колонка «Під час роботи» збирає досліди з розділів вище:

| Помилка | `tsc` | ESLint | Під час роботи |
|---------|-------|--------|----------------|
| `onClick={show()}`, функція лише друкує | `TS2322` | мовчить | друкує на кожному рендері, кнопка мертва |
| `onClick={add()}`, функція викликає `set` | `TS2322` | `react-hooks/set-state-in-render` | `Too many re-renders` або неправильне число |
| `onClick={onPick}`, функція чекає рядок | `TS2322` | мовчить | у функцію приходить об'єкт події |
| `onClick={() => onPick}` | мовчить | мовчить | нічого не відбувається |
| `let cups`, зміна в обробнику | мовчить | `react-hooks/immutability` | екран не змінюється |
| `useState` в обробнику | мовчить | `react-hooks/rules-of-hooks` | `Invalid hook call` |
| `value` без `onChange` | мовчить | мовчить | поле не змінюється, у консолі повідомлення |
| `setOrder({ note })` без решти полів | `TS2345` | мовчить | інші поля зникають |
| `<button>` без `type` у формі | мовчить | мовчить | форма надсилається |

Жоден інструмент окремо не ловить усіх цих помилок. Приклади в тестах ловлять ті, про які мовчать і `tsc`, і лінтер.

## Типові хибні уявлення

**«Дужки потрібні, щоб передати функцію».** Дужки викликають функцію. Передають її без дужок або загорнутою в стрілку.

**«`undefined` в `onClick` дасть помилку».** Не дасть. Для React це означає, що обробника немає. Клацання мовчки
нічого не робить.

**«React перемальовує компонент, коли змінюється будь-яка його змінна».** React не стежить за змінними. Просить новий
рендер лише функція `set`, а ще рендер спричиняють новий рендер батька й перший показ.

**«Аргумент `useState` задає значення на кожному рендері».** Він діє лише при створенні комірки. Новий проп у цьому
аргументі стан не змінить.

**«Значення поля зберігається в полі, а стан лише дублює його».** У керованому полі значення вирішує стан. Якщо стан
не змінився, React поверне полю старе значення.

**«`onChange` спрацьовує, коли поле втрачає фокус, як у HTML».** У React він спрацьовує на кожну зміну тексту.

**«Дитина змінює стан батька».** Стан змінює лише функція `set` батька. Дитина лише викликає те, що батько їй дав.

**«Стан належить компоненту, тому всі копії бачать те саме».** Стан належить екземпляру на екрані. Спільною є лише
змінна модуля, а вона не просить рендеру.

## Як це проявиться далі в React

- **День 8, рендер, коміт і знімок стану.** Ви побачите, чому `cups` в обробнику лишається старим після `setCups`, і
  що відбувається, коли функцію `set` викликано кілька разів поспіль.
- **День 9, об'єкти й масиви в стані.** Той самий `setOrder` докладно: копія кожного рівня й заміна замість зміни.
- **День 10, стан як набір станів екрана.** Кілька окремих прапорців стануть одним описом стану екрана.
- **День 11, структура стану.** Сторінка `State: A Component's Memory` згадує, що пов'язані поля можна тримати разом.
  Той день пояснить, коли це варто робити.
- **День 12, спільний стан і скидання стану.** Стан переїде в спільного батька, а ви побачите, що саме вирішує, чи
  екземпляр лишився тим самим.
- **День 15, ref.** Ви отримаєте пам'ять, зміна якої не просить рендеру. Це те, чим не змогла стати звичайна змінна.
- **Фаза 2.** Нові стрілки на кожному рендері матимуть значення, коли ви почнете вимірювати швидкодію.

## Перевірте себе

**1. Функція `save` нічого не повертає. Що станеться з кнопкою `<button onClick={save()}>`, коли вона з'явиться на
екрані й коли її клацнуть?**

<details><summary>Відповідь</summary>

Функція виконається під час рендеру, а в проп потрапить `undefined`. Для React це означає, що обробника немає, тому
клацання нічого не зробить і помилки не буде. Про це скаже лише `tsc`: `TS2322`, тип `void` не є обробником. Якщо
`save` викликає `set`, кожен рендер проситиме новий рендер.

</details>

**2. Компонент пише `let total = 0`, а обробник робить `total = total + 1`. Назвіть дві окремі причини, чому екран не
змінюється.**

<details><summary>Відповідь</summary>

Зміна змінної не просить React зробити новий рендер, бо React за змінними не стежить. Навіть якщо рендер станеться з
іншої причини, виклик функції створить нову змінну й знову запише в неї нуль.

</details>

**3. `function Box({ start }) { const [n, setN] = useState(start) ... }`. Батько спочатку передав `start={1}`, а потім
`start={5}`. Що лежить у `n`, якщо ніхто не викликав `setN`?**

<details><summary>Відповідь</summary>

`1`. Аргумент `useState` читається лише при створенні комірки. Новий проп викликає новий рендер, але комірка вже
існує, тому число 5 ігнорується.

</details>

**4. Поле написано як `<input value={text} onChange={(e) => setText(e.target.value.slice(0, 3))} />`. Людина набирає
`абвг`. Що буде в полі і чому?**

<details><summary>Відповідь</summary>

`абв`. Після четвертої клавіші браузер дописує `г`, у `e.target.value` приходить `абвг`, а `slice` залишає три літери.
Стан не змінюється, тому React повертає полю значення зі стану.

</details>

**5. Чому в дитині пишуть `onClick={() => onPick(drink)}`, а в батька просто `onPick={setDrink}`, без стрілки?**

<details><summary>Відповідь</summary>

Дитині треба передати аргумент, якого в React немає: React передасть обробнику лише об'єкт події. Стрілка отримує цю
подію, ігнорує її й викликає `onPick` із назвою напою. Батькові нічого додавати не треба: дитина викликає функцію з
одним рядком, а `setDrink` якраз приймає одне значення.

</details>

**6. Запис `onClick={() => onPick}` проходить і `tsc`, і лінтер. Що відбувається при клацанні й як це спіймати?**

<details><summary>Відповідь</summary>

Стрілка повертає функцію `onPick`, але не викликає її, тому нічого не відбувається. Спіймати це можна прикладом:
шпигун `vi.fn()` замість `onPick` після клацання має отримати рівно один виклик із назвою.

</details>

**7. На екрані два `<Order />`. Людина клацнула в першому, потім батько прибрав перший і показав знову. Що покаже
перший, а що другий?**

<details><summary>Відповідь</summary>

Другий покаже те саме, що й раніше, бо його стан ніхто не чіпав і він лишався на екрані. Перший покаже початкові
значення, бо стан живе, поки екземпляр стоїть на екрані, а новий показ створює новий екземпляр.

</details>

## Словничок лекції

| Слово | Що означає |
|-------|------------|
| обробник | функція, яку викличуть у відповідь на подію |
| об'єкт події | аргумент обробника, який створює React і в якому описано подію |
| функція-проп | проп, значенням якого є функція, через неї дитина повідомляє батькові |
| стан | дані, які React зберігає для екземпляра компонента між рендерами |
| хук | функція з іменем на `use`, яку викликають лише під час рендеру й лише на верхньому рівні компонента |
| `useState` | хук, який дає поточне значення стану й функцію `set` |
| функція `set` | функція, яка просить React запам'ятати нове значення й зробити новий рендер |
| кероване поле | поле, значення якого задає стан через проп `value` |
| некероване поле | поле, яке саме зберігає текст, а `defaultValue` задає лише початок |
| екземпляр | одне конкретне місце на екрані, де показано компонент |
| шпигун | підставна функція, яка запам'ятовує свої виклики; у Vitest її створює `vi.fn()` |

## Що читати далі

- [Розбір читання до цього дня](../reading/f1-d07-reading.md): що саме написано в матеріалах дня й де що шукати.
- `<input>` у довіднику React: усі пропи поля, зокрема розділ `Controlling an input with a state variable`.
- React event object: поля й методи об'єкта події.
- `<button>` на MDN: атрибут `type` і поведінка кнопки у формі.
- `change` на MDN: коли браузерна подія спрацьовує насправді.
- Render and Commit: сторінка, яку ви читатимете в день 8.

---

Лекцію написано для цього плану. Вона спирається на документацію React, Testing Library, Vitest, сторінки MDN і
переказує рецепт із книжки How to Design Programs. Усе переказано своїми словами, а права на ці тексти належать їхнім
авторам.
