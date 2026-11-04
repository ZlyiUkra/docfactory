# Лекція. Фаза 1, день 4. Списки й ключі

Ця лекція пояснює, як показати масив даних на екрані і як React після зміни масиву розуміє, який рядок який. Майже вся
тема тримається на одному маленькому атрибуті `key`. Читання займе близько 45 хвилин.

Приклади з React запущено на версії 19.3 у Vitest під jsdom, тобто в імітації браузера всередині Node. Вивід під
прикладами справжній. Типи перевірено компілятором `tsc` версії 6.0. У справжньому браузері приклади не запускалися,
тому там, де йдеться про браузер, поруч сказано, на чому це твердження тримається.

**Після лекції ви зможете пояснити:**

- як масив даних стає рядками на екрані і чому записані вручну рядки ключів не потребують;
- де лежить ключ, чому компонент не може його прочитати і чому `1` та `"1"` для React той самий ключ;
- як React зіставляє рядки двох рендерів, де текст поля зберігає вузол, а де значення зберігає сам React;
- чому `key={index}` часто здається робочим, за яких дій він ламається, а за яких ні;
- чому випадковий ключ видаляє весь список при кожному рендері;
- на якому елементі стоїть ключ і звідки його брати, якщо в даних немає `id`;
- чому відсутність попередження нічого не каже про якість ключа.

## Журнал, у якому оцінка дісталася іншому учневі

Ви робите журнал для вчительки. Кожен рядок містить ім'я учня, поле для оцінки й кнопку, яка прибирає учня зі списку.
Код виглядає правильно, і він справді показує всіх. Ось весь файл разом із тестом. Ім'я такого файлу закінчується на
`.test.tsx`, а запускає його команда `npx vitest run`:

```tsx
// @vitest-environment jsdom
// Цей коментар просить Vitest створити імітацію браузера, бо без документа компонент показати ніде.
import { useState } from 'react'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { test } from 'vitest'

type Student = { id: number; name: string }
const STUDENTS: Student[] = [
  { id: 11, name: 'Марта' },
  { id: 12, name: 'Богдан' },
  { id: 13, name: 'Соломія' },
]

function Journal() {
  const [students, setStudents] = useState(STUDENTS)
  return (
    <ul>
      {students.map((student, index) => (
        <li key={index}>
          {student.name} <input aria-label={student.name} />
          <button onClick={() => setStudents(students.filter((s) => s.id !== student.id))}>
            Вибув: {student.name}
          </button>
        </li>
      ))}
    </ul>
  )
}

test('журнал', async () => {
  const user = userEvent.setup() // цей об'єкт набирає текст і натискає кнопки замість людини
  render(<Journal />)
  await user.type(screen.getByLabelText('Марта'), '12')
  await user.type(screen.getByLabelText('Богдан'), '7')
  await user.type(screen.getByLabelText('Соломія'), '10')
  await user.click(screen.getByRole('button', { name: 'Вибув: Марта' }))
  for (const field of screen.getAllByRole<HTMLInputElement>('textbox')) {
    console.log(field.getAttribute('aria-label'), '=', field.value)
  }
})
```

```text
Богдан = 12
Соломія = 7
```

Марта мала 12, Богдан 7, а Соломія 10. Учениця Марта вибула, і тепер 12 стоїть у Богдана, 7 стоїть у Соломії, а її
власна десятка зникла. Програма не надрукувала жодної помилки чи попередження. Перший показ цього не виявляє, бо до
видалення все правильно. Якби вчителька не помітила, в журналі лишилися б чужі оцінки.

Щоб зрозуміти, що сталося, треба відповісти на два запитання. Перше: як масив даних стає рядками на екрані? Друге: як
React після зміни масиву вирішує, який новий рядок відповідає якому старому? Відповідь на друге запитання й містить
весь зміст слова `key`.

Решта прикладів із React у цій лекції запускаються так само, як цей файл. Кожен приклад лежить у власному файлі тесту
й починається з тих самих рядків імпорту та з того самого типу `Student` і масиву `STUDENTS`. Дії лежать усередині
виклику `test('…', async () => { … })`, а першим рядком там стоїть `const user = userEvent.setup()`. Далі ми цих
рядків не повторюємо. Якщо прикладу потрібні ще якісь функції, їх імпортують із тих самих пакетів: `act` і `fireEvent`
із `@testing-library/react`, `vi` із `vitest`, `Fragment` із `react`.

## Список є масивом елементів

Лекція «JSX» уже показала, що кожен тег компілятор перетворює на виклик функції, а виклик дає **елемент**, тобто
об'єкт з описом того, що показати. Елемент є звичайним значенням, тому його можна покласти в масив. Метод `map` з
лекції «Масиви й об'єкти функційно» будує новий масив, викликаючи функцію для кожного значення старого. Разом це дає
список:

```tsx
function Roster() {
  const rows = STUDENTS.map((student) => <li key={student.id}>{student.name}</li>)
  console.log(Array.isArray(rows), rows.length, rows[0].type, rows[0].key)
  return <ul>{rows}</ul>
}

console.log(render(<Roster />).container.innerHTML)
```

```text
true 3 li 11
<ul><li>Марта</li><li>Богдан</li><li>Соломія</li></ul>
```

Масив `rows` містить три елементи, а React, отримавши масив у дужках, показує його елементи підряд. Окремого запису
для циклу в JSX немає, як немає його й для умов. Усе робить звичайний JavaScript, тому `filter` можна поставити перед
`map`, а результат спершу покласти в змінну, як тут.

Дві знайомі пастки стоять поруч із цим записом.

**Фігурні дужки після стрілки.** Лекція «Масиви й об'єкти функційно» пояснила, що `{` одразу після `=>` відкриває тіло
функції, а не значення. Якщо в такому тілі немає `return`, функція повертає `undefined`, і React не показує нічого:

```tsx
// файл src/no-return.tsx
const names = ['Марта', 'Богдан']

export function NoReturn() {
  // Дужка { після стрілки відкриває тіло функції. У тілі немає return, тому map отримує undefined.
  return <ul>{names.map((name) => { <li key={name}>{name}</li> })}</ul>
}
```

Тест показує цей компонент викликом `render(<NoReturn />)` і друкує `container.innerHTML`. Під цим виводом стоїть
результат перевірки того самого файлу компілятором `tsc`, а з його довгого повідомлення показано лише перший рядок:

```text
<ul></ul>
```

```text
$ npx tsc --noEmit -p tsconfig.app.json
src/no-return.tsx(6,14): error TS2322: Type 'void[]' is not assignable to type 'ReactNode'.
```

Список `<ul>` порожній, бо жоден виклик функції не повернув рядка. Під час запуску React не надрукував нічого, тому
про цю помилку каже лише `tsc`. Він повідомляє, що `map` дав масив `void[]`, тобто масив значень, яких функція не
повертала. Отже, якщо список раптом порожній, подивіться на дужку після стрілки. Круглі дужки, `=> (<li>…</li>)`,
означають один вираз, і його значення повертається саме.

**Нуль замість порожнього списку.** Лекція «Пропси й умовний рендер» обіцяла, що пастка з `&&` повернеться:

```tsx
const nobody: Student[] = []
function Empty() {
  return <section>{nobody.length && <ul>{nobody.map((s) => <li key={s.id}>{s.name}</li>)}</ul>}</section>
}

console.log(render(<Empty />).container.innerHTML)
```

```text
<section>0</section>
```

Довжина порожнього масиву дорівнює `0`, оператор `&&` повертає цей нуль, а числа React показує. Для списку перевірка
звучить як `nobody.length > 0`. Порожній масив у дужках нічого зайвого не показує, тому часто перевірка взагалі не
потрібна, а умова стає потрібною лише тоді, коли порожній список має показати інший напис.

### Чому записаним вручну рядкам ключ не потрібен

Лекція «Пропси й умовний рендер» згадувала, що елементи масиву в `children` отримають ключі. Це правда лише для
масиву, який створили ви самі. Ось два записи, а під ними те, що залишає компілятор:

```js
// файл compile.mjs
import { transformWithOxc } from 'vite'
const show = async (source) => {
  const { code } = await transformWithOxc(source, 'x.jsx', { jsx: { runtime: 'automatic' } })
  console.log(code.split('\n').slice(1).join('\n').replaceAll('/* @__PURE__ */ ', ''))
}
await show('export const a = <ul><li>Марта</li><li>Богдан</li></ul>')
await show('export const b = <ul>{names.map((n) => <li key={n.id}>{n.name}</li>)}</ul>')
```

```text
$ node compile.mjs
export const a = _jsxs("ul", { children: [_jsx("li", { children: "Марта" }), _jsx("li", { children: "Богдан" })] });

export const b = _jsx("ul", { children: names.map((n) => _jsx("li", { children: n.name }, n.id)) });

```

У першому записі дітей кілька, і компілятор бачить їх усіх у тексті програми. Він викликає окрему функцію `_jsxs`, яка
каже React, що цей масив написано вручну. Такий масив не може змінити ні довжину, ні порядок, тому порівняння за
номером тут завжди правильне. У другому записі компілятор бачить лише вираз. Він не знає, скільки рядків дасть `map` і
чи зміниться їхній порядок, тому викликає `_jsx`, і масив перевіряє вже React.

Звідси випливає межа, яку корисно запам'ятати. Масив, записаний дужками прямо в розмітці, `{[<li>а</li>,
<li>б</li>]}`, для React теж є масивом із виразу, і без ключів він дає попередження, хоча виглядає статичним:

```tsx
// Рядок друку тут не потрібен, бо попередження в консоль пише сам React.
render(<ul>{[<li>а</li>, <li>б</li>]}</ul>)
```

```text
Each child in a list should have a unique "key" prop.

Check the top-level render call using <ul>. See https://react.dev/link/warning-keys for more information.
```

Перший рядок називає помилку, а останній каже, де її шукати: у виклику, який показує `<ul>`. Отже, якщо рядки відомі
заздалегідь, пишіть їх просто тегами, без масиву. Тоді компілятор викличе `_jsxs`, і ключі не знадобляться.

## Що таке ключ

**Ключем** називають атрибут `key`, який позначає елемент серед його сусідів. Він виглядає як проп, але проп не є.
Лекція «JSX» уже показала його місце: це третій аргумент виклику `jsx`. Ось що компілятор робить із рядком, де є і
проп, і ключ:

```text
<li key={7} title="x">Марта</li>

_jsx("li", {
	title: "x",
	children: "Марта"
}, 7);
```

Поле `title` пішло в об'єкт пропсів, а `7` стало окремим аргументом. Подивимося, що з цього вийшло:

```tsx
const el = <li key={7} title="x">Марта</li>
console.log(el.key, typeof el.key, '| без ключа:', (<li />).key)
console.log(Object.keys(el.props as object))
```

```text
7 string | без ключа: null
[ 'title', 'children' ]
```

Із цього випливає три наслідки.

**Ключ завжди є рядком.** React перетворює значення на рядок, тому число `1` і рядок `"1"` для нього той самий ключ.
Два такі рядки поруч дадуть попередження про однакові ключі:

```tsx
// Рядок друку не потрібен: попередження в консоль пише сам React.
render(<ul>{[1, '1'].map((id) => <li key={id}>{id}</li>)}</ul>)
```

```text
Encountered two children with the same key, `1`. Keys should be unique so that components maintain their identity across updates. Non-unique keys may cause children to be duplicated and/or omitted — the behavior is unsupported and could change in a future version.
```

React назвав повторений ключ просто `1`, хоча одне значення було числом, а інше рядком. Отже, якщо дані приходять із
двох джерел, де той самий номер записано по-різному, ці номери все одно збігаються.

**Компонент свого ключа не бачить.** Функція компонента отримує об'єкт пропсів, а ключа в ньому немає. Спроба
прочитати `props.key` дає `undefined`, а React у режимі розробки пише: `` `key` is not a prop. Trying to access it
will result in `undefined` being returned. `` `tsc` цього не зупиняє: запис `function P({ key }: { key: string })`
компілюється, хоча значення там ніколи не буде. Ось такий компонент у роботі:

```tsx
function P({ key }: { key: string }) {
  console.log('компонент прочитав key:', key)
  return <p>Марта</p>
}

render(<P key="a" />) // батько передав ключ "a"
```

```text
P: `key` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://react.dev/link/special-props)
компонент прочитав key: undefined
```

Перший рядок надрукував React, а другий надрукував сам компонент. Батько передав `"a"`, а компонент отримав
`undefined`. Якщо компоненту потрібен той самий номер, батько передає його вдруге окремим пропом, наприклад `<Row
key={s.id} studentId={s.id} />`.

**Ключ не передають через розгортання.** Запис `{...row}` з лекції «Пропси й умовний рендер» працює для пропсів. Якщо
в об'єкті `row` є поле `key`, React застосує його, але напише `A props object containing a "key" prop is being spread
into JSX`:

```tsx
const row = { key: 'a', title: 'x' }
const el = <li {...row}>Марта</li> // поле key потрапляє в елемент через розгортання
console.log('ключ елемента:', el.key)
```

```text
A props object containing a "key" prop is being spread into JSX:
  let props = {key: someKey, title: ..., children: ...};
  <li {...props} />
React keys must be passed directly to JSX without using spread:
  let props = {title: ..., children: ...};
  <li key={someKey} {...props} />
ключ елемента: a
```

Останній рядок показує, що ключ спрацював, а решту надрукував React, щоб попередити про такий запис. Такий запис
просять замінити явним `key={row.key}` перед розгортанням, як показує нижня частина повідомлення.

Ключ також не потрапляє в документ. Для браузера ключа не існує, і в розмітці сторінки ви його не знайдете.

## Як React зіставляє два списки

Лекція «Компоненти й модулі» пояснила загальне правило. Після кожного рендеру React порівнює нове дерево елементів зі
старим, місце за місцем. Якщо на місці лишився той самий `type`, React оновлює наявний **екземпляр**, тобто свій запис
про компонент на цьому місці разом зі станом і вузлами. Якщо `type` інший, React видаляє старий екземпляр і створює
новий. Там же було сказано, що ключ доповнює це правило, і тепер видно навіщо.

Для списку «місце за місцем» погано підходить, бо місце в масиві залежить від сусідів. Коли зникає перший рядок, усі
наступні зсуваються на одне місце вперед. Тому React порівнює дітей одного батька за парою значень: тип і ключ.

| Старий рядок і новий рядок | Що робить React | Що лишається |
|----------------------------|-----------------|--------------|
| той самий ключ, той самий тип | оновлює наявний екземпляр новими пропсами | вузол документа й стан |
| той самий ключ, інший тип | видаляє старий, створює новий | нічого |
| ключ є лише в старому списку | видаляє екземпляр і його вузли | нічого |
| ключ є лише в новому списку | створює екземпляр і вузли | нове порожнє |

Сторінка `Rendering Lists` каже ще одну річ, важливу для наступних прикладів: якщо ключа немає зовсім, React бере
індекс. Отже, рядок без ключа й рядок із `key={index}` зіставляються однаково. Різниця лише в тому, що в першому
випадку React друкує попередження.

Ключі порівнюються лише між дітьми одного батька. Рядок із тим самим ключем, перенесений в інший `<ul>`, вважається
новим рядком. Рядок, який за тим самим ключем змінив тег із `<li>` на `<p>`, теж отримує нове поле. Запустимо обидва
випадки. В обох випадках ключ лишається `m`, а в поле спершу набрано `12`:

```tsx
// Той самий рядок із тим самим ключем стоїть то в першому <ul>, то в другому.
function Lists({ inFirst }: { inFirst: boolean }) {
  const row = <li key="m"><input aria-label="Марта" /></li>
  return (
    <>
      <ul>{inFirst ? [row] : []}</ul>
      <ul>{inFirst ? [] : [row]}</ul>
    </>
  )
}

// Рядок лишається в тому самому <ul> із тим самим ключем, але тег змінюється.
function Tagged({ tag: Tag }: { tag: 'li' | 'p' }) {
  return <ul>{[<Tag key="m"><input aria-label="Марта" /></Tag>]}</ul>
}

const moved = render(<Lists inFirst={true} />)
await user.type(screen.getByLabelText('Марта'), '12')
moved.rerender(<Lists inFirst={false} />)
console.log('інший <ul>:', JSON.stringify(screen.getByLabelText<HTMLInputElement>('Марта').value))
moved.unmount()

const retagged = render(<Tagged tag="li" />)
await user.type(screen.getByLabelText('Марта'), '12')
retagged.rerender(<Tagged tag="p" />)
console.log('інший тег:', JSON.stringify(screen.getByLabelText<HTMLInputElement>('Марта').value))
```

```text
інший <ul>: ""
інший тег: ""
```

Обидва рядки друкують порожній текст, тому оцінка `12` пропала разом зі старим вузлом. Отже, ключ не збереже поле,
якщо рядок перейшов до іншого батька або змінив тег.

Тепер видно, що сталося в журналі. Ключ `index` є лише номером, а не тим, хто стоїть у рядку.

## Покроковий приклад: Марта виходить із журналу

Простежимо обидва варіанти ключа на тих самих даних.

| Крок | Хто діє | `key={index}` | `key={student.id}` |
|------|---------|---------------|--------------------|
| 1 | React, перший показ | рядки з ключами 0, 1, 2 | рядки з ключами 11, 12, 13 |
| 2 | вчителька набирає оцінки | у трьох полях лежать 12, 7, 10 | так само |
| 3 | кнопка викликає `setStudents` | новий масив: Богдан, Соломія | так само |
| 4 | React викликає `Journal` ще раз | нові рядки з ключами 0, 1 | нові рядки з ключами 12, 13 |
| 5 | React порівнює ключі | 0 і 1 є в обох списках, 2 зник | 12 і 13 є в обох списках, 11 зник |
| 6 | React оновлює те, що лишилося | вузол 0 отримує ім'я Богдан, вузол 1 отримує ім'я Соломія | у вузлах 12 і 13 нічого не змінюється |
| 7 | React видаляє зайве | вузол 2 з оцінкою 10 | вузол 11 з оцінкою 12 |
| 8 | на екрані | Богдан 12, Соломія 7 | Богдан 7, Соломія 10 |

Вирішальним є шостий крок. React оновив ім'я і підпис поля, бо вони приходять із елемента. Набране значення він не
змінив, бо елемент про нього нічого не каже. Запустимо той самий журнал із `key={student.id}`:

```text
Богдан = 7
Соломія = 10
```

Функція `Journal` виконалася так само, і так само отримала двох учнів. Змінився лише вираз у `key`. Отже, справа не в
тому, що React щось перемальовує не так. React виконує ту саму роботу з іншими вхідними даними.

## Стан у цьому прикладі: коротко

Докладно стан вивчає день 7, а сьогодні потрібно лише те, що вже показала лекція «Компоненти й модулі». Виклик
`useState(STUDENTS)` просить React зберегти значення для цього екземпляра й повертає його разом із функцією, яка його
замінює. Виклик `setStudents(новий)` записує нове значення й просить React викликати компонент ще раз.

Для сьогоднішньої теми важливі дві властивості.

**Початкове значення читається один раз.** Аргумент `useState` діє лише під час першого показу екземпляра. Якщо батько
передасть інший масив, стан лишиться старим:

```tsx
function Names({ initial }: { initial: string[] }) {
  const [names] = useState(initial)
  return <p>{names.join(', ')}</p>
}

const { container, rerender } = render(<Names initial={['Марта']} />)
rerender(<Names initial={['Богдан']} />)
console.log(container.innerHTML)
```

```text
<p>Марта</p>
```

Завдяки цьому в перевірках дня виклик `rerender` із новим масивом не змінює рядки списку й перевіряє лише те, що рядки
пережили новий рендер.

**Стан замінюють новим масивом.** Лекція «Значення й посилання» пояснила, що React порівнює нове значення зі старим
через `Object.is`. Якщо змінити той самий масив методом `splice` і передати його знову, React побачить те саме
посилання й не викличе компонент. Тому видаляють через `filter`, який не чіпає старий масив, а будує новий. День 9
розбере всі такі дії докладно.

## Що саме переїжджає: три місця зберігання

Пояснення «текст поїхав за ключем» є неповним, бо зміст рядка може лежати в різних місцях. Від місця залежить, чи
зашкодить поганий ключ.

### У вузлі документа

Поле `<input />` без атрибута `value` називають **некерованим**. Сторінка довідника про `<input>` каже, що JSX такого
поля задає щонайбільше початкове значення через `defaultValue`. Решту часу текст тримає сам браузер, а React цього
тексту не записує. Текст лежить у властивості `value` вузла, тому живе, поки живе вузол. Це випадок журналу.

Саме так поводяться й інші властивості, які користувач змінює сам і які не описані в елементі: позиція курсора, фокус,
розкритий стан згорнутого блоку, позиція прокрутки. Для фокуса лекція «Компоненти й модулі» вже показала, як він
зникає разом із вузлом. Для решти цих властивостей ми покладаємося на той самий механізм, а в браузері цього не
перевіряли.

### У стані, який тримає React

Тепер у рядку немає поля. Компонент `Row` рахує позначки, які вчителька поставила учневі, і тримає лічильник у
власному стані. Число показано як звичайний текст, тому у вузлах документа нічого прихованого не лежить:

```tsx
function Row({ name, onDrop }: { name: string; onDrop: () => void }) {
  const [marks, setMarks] = useState(0)
  return (
    <li>
      {name}: {marks}
      <button onClick={() => setMarks(marks + 1)}>плюс {name}</button>
      <button onClick={onDrop}>вибув {name}</button>
    </li>
  )
}

function Marks({ byIndex }: { byIndex: boolean }) {
  const [rows, setRows] = useState(STUDENTS)
  return (
    <ul>
      {rows.map((s, i) => (
        <Row key={byIndex ? i : s.id} name={s.name} onDrop={() => setRows(rows.filter((r) => r.id !== s.id))} />
      ))}
    </ul>
  )
}

for (const byIndex of [true, false]) {
  const { unmount } = render(<Marks byIndex={byIndex} />)
  await user.click(screen.getByRole('button', { name: 'плюс Марта' }))
  await user.click(screen.getByRole('button', { name: 'плюс Марта' }))
  await user.click(screen.getByRole('button', { name: 'плюс Богдан' }))
  await user.click(screen.getByRole('button', { name: 'вибув Марта' }))
  console.log(byIndex ? 'індекс:' : 'id:', screen.getAllByRole('listitem').map((li) => li.textContent?.split('плюс')[0]).join(' | '))
  unmount()
}
```

```text
індекс: Богдан: 2 | Соломія: 1
id: Богдан: 1 | Соломія: 0
```

Плюси переїхали так само, як оцінки. Важливо, де цей стан лежить. Сторінка `Preserving and Resetting State` прямо
каже, що стан тримає сам React, а не компонент, і пов'язує його з місцем компонента в дереві. Отже, стан не лежить у
вузлі документа, а лежить поруч: і вузол, і стан належать одному екземпляру, а екземпляр React знаходить за ключем.
Тому фраза «стан належить позиції з ключем» є точною. Після видалення Марти ключ 0 означає вже Богдана, а екземпляр із
ключем 0 лишається зі своїм станом і лише отримує нові пропси.

### У даних батька

Третій варіант виглядає майже так само, але оцінки лежать у стані батька, в об'єкті, де ключем є `id` учня, а поле
отримує значення через атрибут `value`. Таке поле називають **керованим**, і докладно його вивчає день 7. Коротко:
тепер текст у поле щоразу пише React, а значення бере з даних.

```tsx
function Held({ byIndex }: { byIndex: boolean }) {
  const [rows, setRows] = useState(STUDENTS)
  const [grades, setGrades] = useState<Record<number, string>>({})
  return (
    <ul>
      {rows.map((s, i) => (
        <li key={byIndex ? i : s.id}>
          <input
            aria-label={s.name}
            value={grades[s.id] ?? ''}
            onChange={(e) => setGrades({ ...grades, [s.id]: e.target.value })}
          />
        </li>
      ))}
      <li><button onClick={() => setRows(rows.slice(1))}>прибрати першого</button></li>
    </ul>
  )
}

for (const byIndex of [true, false]) {
  const { unmount } = render(<Held byIndex={byIndex} />)
  await user.type(screen.getByLabelText('Марта'), '12')
  await user.type(screen.getByLabelText('Богдан'), '7')
  act(() => screen.getByRole('button', { name: 'прибрати першого' }).click())
  const fields = screen.getAllByRole<HTMLInputElement>('textbox')
  console.log(byIndex ? 'індекс:' : 'id:', fields.map((f) => `${f.getAttribute('aria-label')}=${f.value}`).join(', '),
    '| фокус:', document.activeElement?.getAttribute('aria-label'))
  unmount()
}
```

```text
індекс: Богдан=7, Соломія= | фокус: Соломія
id: Богдан=7, Соломія= | фокус: Богдан
```

Оцінки тепер правильні навіть із `key={index}`, бо значення приходить із даних за `id`, а не з вузла. Проте вузол,
який мав фокус, лишився на другому місці, а це місце тепер належить Соломії. Людина набирала оцінку Богдану, а
наступна літера потрапить Соломії. Функція `click()` тут викликана напряму, а обгортка `act` просить React завершити
оновлення, щоб фокус не перейшов на кнопку й ми побачили саму поведінку вузла. У браузері цей приклад не запускали,
тому твердження про фокус спирається на jsdom, де фокус теж належить вузлу.

Отже, правило таке. Поганий ключ шкодить тоді, коли в рядку є щось своє, чого немає в елементі: текст у вузлі, стан
дитини або фокус. Якщо рядок складається лише з тексту, зсув ключів на екрані непомітний:

```tsx
function Plain({ rows }: { rows: Student[] }) {
  return <ul>{rows.map((s, i) => <li key={i}>{s.name}</li>)}</ul>
}

const { container, rerender } = render(<Plain rows={STUDENTS} />)
rerender(<Plain rows={STUDENTS.slice(1)} />)
console.log(container.innerHTML)
```

```text
<ul><li>Богдан</li><li>Соломія</li></ul>
```

Результат правильний. Саме тому `key={index}` живе в коді довго: доки хтось не додасть у рядок поле чи компонент зі
станом.

## Коли індекс ламається, а коли ні

Той самий журнал, ті самі оцінки 12, 7 і 10, але шість різних змін списку. Новий масив передає батько, а ключ вибирає
проп:

```tsx
function Grades({ rows, byIndex }: { rows: Student[]; byIndex: boolean }) {
  return (
    <ul>
      {rows.map((s, i) => (
        <li key={byIndex ? i : s.id}>{s.name} <input aria-label={s.name} /></li>
      ))}
    </ul>
  )
}

async function change(next: Student[], byIndex: boolean) {
  const { rerender, unmount } = render(<Grades rows={STUDENTS} byIndex={byIndex} />)
  await user.type(screen.getByLabelText('Марта'), '12')
  await user.type(screen.getByLabelText('Богдан'), '7')
  await user.type(screen.getByLabelText('Соломія'), '10')
  rerender(<Grades rows={next} byIndex={byIndex} />)
  const text = screen.getAllByRole<HTMLInputElement>('textbox').map((f) => `${f.getAttribute('aria-label')} ${f.value}`).join(', ')
  unmount()
  return text
}

const [marta, bohdan, solomia] = STUDENTS
const front = { id: 10, name: 'Остап' }
const back = { id: 14, name: 'Остап' }
const changes: [string, Student[]][] = [
  ['прибрати останнього', [marta, bohdan]],
  ['додати в кінець', [marta, bohdan, solomia, back]],
  ['прибрати першого', [bohdan, solomia]],
  ['прибрати середнього', [marta, solomia]],
  ['додати на початок', [front, marta, bohdan, solomia]],
  ['обернути порядок', [solomia, bohdan, marta]],
]
for (const [what, next] of changes) {
  console.log(what, '|', await change(next, true), '|', await change(next, false))
}
```

```text
прибрати останнього | Марта 12, Богдан 7 | Марта 12, Богдан 7
додати в кінець | Марта 12, Богдан 7, Соломія 10, Остап  | Марта 12, Богдан 7, Соломія 10, Остап 
прибрати першого | Богдан 12, Соломія 7 | Богдан 7, Соломія 10
прибрати середнього | Марта 12, Соломія 7 | Марта 12, Соломія 10
додати на початок | Остап 12, Марта 7, Богдан 10, Соломія  | Остап , Марта 12, Богдан 7, Соломія 10
обернути порядок | Соломія 12, Богдан 7, Марта 10 | Соломія 10, Богдан 7, Марта 12
```

Ліва колонка є результатом ключа-індексу, а права результатом ключа-`id`. Перші два рядки однакові. Коли зміна
стосується лише кінця списку, номери всіх решти рядків не змінюються. Отже, якщо ви перевіряєте список лише додаванням
нового запису в кінець, помилки не побачите. Вона з'являється при будь-якій зміні на початку чи в середині. Рядок про
обернений порядок показує ще одну деталь: Богдан стоїть посередині, його номер не змінився, тому його оцінка лишилася
правильною випадково.

### Скільки роботи робить React

Ключ також вирішує, скільки вузлів React чіпає. Ось список із тисячі рядків простого тексту, з якого прибрано перший.
Вбудований у браузер і в jsdom об'єкт `MutationObserver` записує кожну зміну документа, тому ми порахували ці зміни, а
не час. Час у jsdom нічого не каже про браузер.

```tsx
type KeyOf = (student: Student, index: number) => string | number

function Long({ rows, keyOf }: { rows: Student[]; keyOf: KeyOf }) {
  return <ul>{rows.map((s, i) => <li key={keyOf(s, i)}>{s.name}</li>)}</ul>
}

const thousand = Array.from({ length: 1000 }, (_, i) => ({ id: i + 1, name: `Учень ${i + 1}` }))
const variants: [string, KeyOf][] = [
  ['key={index}', (_, i) => i],
  ['key={student.id}', (s) => s.id],
  ['key={Math.random()}', () => Math.random()],
]

for (const [what, keyOf] of variants) {
  const { container, rerender, unmount } = render(<Long rows={thousand} keyOf={keyOf} />)
  // Спостерігач починає записувати лише зараз, тому перший показ у записи не потрапляє.
  const observer = new MutationObserver(() => {})
  observer.observe(container, { subtree: true, childList: true, characterData: true })
  rerender(<Long rows={thousand.slice(1)} keyOf={keyOf} />) // прибрано перший рядок
  const records = observer.takeRecords() // забирає всі записи про зміни
  observer.disconnect()
  const texts = records.filter((r) => r.type === 'characterData').length
  const removed = records.reduce((sum, r) => sum + r.removedNodes.length, 0)
  const added = records.reduce((sum, r) => sum + r.addedNodes.length, 0)
  console.log(what, '| змінено текстів:', texts, '| видалено вузлів:', removed, '| створено вузлів:', added)
  unmount()
}
```

```text
key={index} | змінено текстів: 999 | видалено вузлів: 1 | створено вузлів: 0
key={student.id} | змінено текстів: 0 | видалено вузлів: 1 | створено вузлів: 0
key={Math.random()} | змінено текстів: 0 | видалено вузлів: 1000 | створено вузлів: 999
```

Ті самі числа в таблиці:

| Ключ | Змінено текстів | Видалено вузлів | Створено вузлів |
|------|-----------------|-----------------|-----------------|
| `key={index}` | 999 | 1 | 0 |
| `key={student.id}` | 0 | 1 | 0 |
| `key={Math.random()}` | 0 | 1000 | 999 |

Усі три варіанти дають однаковий вигляд сторінки. Ключ-індекс змушує React переписати текст майже в кожному рядку, бо
кожен рядок тепер показує сусіда. Ключ-`id` прибирає один вузол і більше нічого не робить. Випадковий ключ видаляє
весь список і будує його знову. Ці числа отримано в jsdom, а в браузері їх не перераховували. Проте кількість змін
визначає сам React, а не браузер. Отже, ключ-`id` заощаджує роботу в довгому списку навіть тоді, коли в рядках немає
полів.

## Випадковий ключ

Запис `key={Math.random()}` дає при кожному рендері нове значення, тому жоден старий ключ не збігається з новим, і за
таблицею вище всі старі рядки видаляються, а всі нові створюються. Сторінка `Rendering Lists` застерігає, що так
втрачається все введене користувачем у цих рядках, а ще повільно. Запустимо це. Тест набирає оцінку в поле, просить
батька показати компонент ще раз із тими самими даними й дивиться на поле. Функцію, яка дає ключ, тест передає пропом,
щоб перевірити одразу дві такі функції:

```tsx
function Fresh({ makeKey }: { makeKey: () => string | number }) {
  return <ul>{STUDENTS.map((s) => <li key={makeKey()}><input aria-label={s.name} /></li>)}</ul>
}

const errors = vi.spyOn(console, 'error').mockImplementation(() => {}) // рахує повідомлення React
const variants: [string, () => string | number][] = [
  ['Math.random()', () => Math.random()],
  ['crypto.randomUUID()', () => crypto.randomUUID()],
]

for (const [what, makeKey] of variants) {
  const { rerender, unmount } = render(<Fresh makeKey={makeKey} />)
  const field = screen.getByLabelText<HTMLInputElement>('Марта')
  await user.type(field, '12')
  rerender(<Fresh makeKey={makeKey} />) // дані ті самі, новий лише виклик компонента
  const now = screen.getByLabelText<HTMLInputElement>('Марта')
  console.log(what, '| той самий вузол:', now === field, '| текст:', JSON.stringify(now.value),
    '| фокус у полі:', document.activeElement === now, '| повідомлень React:', errors.mock.calls.length)
  unmount()
}
```

```text
Math.random() | той самий вузол: false | текст: "" | фокус у полі: false | повідомлень React: 0
crypto.randomUUID() | той самий вузол: false | текст: "" | фокус у полі: false | повідомлень React: 0
```

Вираз `той самий вузол: false` означає, що React видалив старе поле й створив нове. Нове поле порожнє, а фокус зник
разом зі старим. React при цьому не надрукував нічого, тому помилку знайде лише приклад із повторним рендером.

Пастка має кілька видів.

**Час.** Запис `key={Date.now()}` схожий на випадковий, але поводиться ще дивніше. Усі рядки одного рендеру зазвичай
створюються за одну мілісекунду, тому отримують той самий ключ, і React пише про однакові ключі. На наступному рендері
час інший. Щоб обидва рендери щоразу давали той самий результат, тест заморожує годинник: `vi.spyOn(Date, 'now')`
підміняє функцію `Date.now`, і вона повертає задане число.

```tsx
const clock = vi.spyOn(Date, 'now').mockReturnValue(1000) // увесь перший рендер бачить час 1000
const errors = vi.spyOn(console, 'error').mockImplementation(() => {}) // рахує повідомлення React

function Stamped() {
  return <ul>{STUDENTS.map((s) => <li key={Date.now()}>{s.name}</li>)}</ul>
}

const { container, rerender } = render(<Stamped />)
console.log('перший рендер:', container.innerHTML)
console.log('повідомлень React:', errors.mock.calls.length, '| повторений ключ:', errors.mock.calls[0][1])

clock.mockReturnValue(2000) // годинник пішов уперед, другий рендер бачить час 2000
rerender(<Stamped />)
console.log('другий рендер:', container.innerHTML)
```

```text
перший рендер: <ul><li>Марта</li><li>Богдан</li><li>Соломія</li></ul>
повідомлень React: 2 | повторений ключ: 1000
другий рендер: <ul><li>Марта</li><li>Богдан</li><li>Марта</li><li>Богдан</li><li>Соломія</li></ul>
```

Перший рендер показує трьох учнів, але React двічі попереджає, що ключ `1000` повторюється. Після другого рендеру на
екрані п'ять рядків замість трьох. Усі три нові рядки отримали новий ключ `2000`, тому React створив їх заново. Зі
старих рядків він видалив лише Соломію. Старі рядки мали той самий ключ, а React зберігає для кожного ключа один
рядок, тому він знав лише про останній із них. Отже, такий ключ може залишити на екрані чужі рядки, а наступний розділ
показує, чому на це не можна покладатися.

**`crypto.randomUUID()` під час рендеру.** Ця функція дає унікальний рядок, і сторінка `Rendering Lists` її радить,
але для запису, який тільки-но створюється. Викликана просто в `map`, вона є тим самим випадковим ключем: другий рядок
виводу вище збігається з першим. Лінтер цього не помічає, як показує таблиця нижче.

**`useId`.** Хук `useId` створює стабільний унікальний рядок для зв'язування полів із підписами. Сторінка цього хука
окремо каже, що для ключів списку він не призначений: «`useId` **should not be used to generate keys** in a list.»

Правило одне: ключ має бути той самий для того самого запису в кожному рендері. Значення, обчислене заново під час
рендеру, цього не гарантує. Це та сама думка, яку день 5 назве чистотою компонента: виклик під час рендеру не повинен
давати щоразу інший результат.

## Однакові ключі

Назва схожа на ключ, поки вона не повторилася. Ось список, де перший і третій рядки мають той самий ключ `a`, а тексти
в рядках показують, що насправді відбувається:

```tsx
function Tags({ rows }: { rows: [string, string][] }) {
  return <ul>{rows.map(([key, text]) => <li key={key}>{text}</li>)}</ul>
}

const { container, rerender } = render(<Tags rows={[['a', 'один'], ['b', 'два'], ['a', 'три']]} />)
console.log(container.innerHTML)
rerender(<Tags rows={[['b', 'два'], ['a', 'один']]} />)
console.log(container.innerHTML)
```

```text
Encountered two children with the same key, `a`. Keys should be unique so that components maintain their identity across updates. Non-unique keys may cause children to be duplicated and/or omitted — the behavior is unsupported and could change in a future version.
<ul><li>один</li><li>два</li><li>три</li></ul>
<ul><li>один</li><li>два</li><li>один</li></ul>
```

У другому показі в даних два записи, а на екрані три рядки. Повідомлення React саме попереджало про це: `` Encountered
two children with the same key, `a` ``, а далі йдеться про те, що рядки можуть подвоюватися чи пропадати, і така
поведінка не підтримується. У цьому прикладі вона подвоїла рядок. Покладатися на цей результат не можна, бо наступна
версія React має право поводитися інакше.

Правило унікальності діє лише серед сусідів одного масиву. Два окремі `map` в одному батьку можуть мати однакові
ключі, і попередження там немає:

```tsx
function Two() {
  return (
    <ul>
      {STUDENTS.map((s) => <li key={s.id}>{s.name}</li>)}
      {STUDENTS.map((s) => <li key={s.id}>{s.id}</li>)}
    </ul>
  )
}

const errors = vi.spyOn(console, 'error').mockImplementation(() => {}) // рахує повідомлення React
console.log(render(<Two />).container.innerHTML)
console.log('повідомлень React:', errors.mock.calls.length)
```

```text
<ul><li>Марта</li><li>Богдан</li><li>Соломія</li><li>11</li><li>12</li><li>13</li></ul>
повідомлень React: 0
```

На екрані всі шість рядків, а ключ `11` стоїть двічі. React не попередив про це, бо кожен `map` дав окремий масив.
Отже, той самий `id` можна спокійно вживати у двох списках поруч.

Особливі значення теж варто знати, бо вони приходять із даних. Два значення перевіримо запуском. Кожен список стоїть у
своєму тегу, бо попередження про відсутній ключ React друкує один раз для назви батька:

```tsx
const noKey = [undefined, undefined].map((id, i) => <li key={id}>{i}</li>)
const nullKey = [null, null].map((id, i) => <li key={id}>{i}</li>)
console.log('ключ із undefined:', noKey[0].key, '| ключ із null:', JSON.stringify(nullKey[0].key))
// Рядки друку для двох наступних викликів не потрібні: попередження в консоль пише сам React.
render(<ul>{noKey}</ul>)
render(<ol>{nullKey}</ol>)
```

```text
ключ із undefined: null | ключ із null: "null"
Each child in a list should have a unique "key" prop.

Check the top-level render call using <ul>. See https://react.dev/link/warning-keys for more information.
Encountered two children with the same key, `null`. Keys should be unique so that components maintain their identity across updates. Non-unique keys may cause children to be duplicated and/or omitted — the behavior is unsupported and could change in a future version.
```

Тут `null` у виводі означає, що ключа в елемента немає, а `"null"` є звичайним рядком. Третє значення, об'єкт, не
доходить до запуску, бо його зупиняє `tsc`. Ось його вивід для файлу `src/object-key.tsx`, у якому стоїть один рядок
`export const wrong = <li key={{ id: 1 }}>Марта</li>`:

```text
$ npx tsc --noEmit -p tsconfig.app.json
src/object-key.tsx(1,26): error TS2322: Type '{ id: number; }' is not assignable to type 'Key | null | undefined'.
```

Ті самі результати в таблиці:

| Значення ключа | Що отримує React | Що станеться |
|----------------|------------------|--------------|
| `undefined` | ключа немає | попередження `Each child in a list…`, далі зіставлення за номером |
| `null` | рядок `"null"` | `tsc` дозволяє `null`, тому два рядки дають попередження про однаковий ключ `null` |
| об'єкт | компілятор не пропустить | `tsc` друкує `TS2322`, бо об'єкт не можна присвоїти типу ключа |

Перші два рядки типово виникають, коли сервер не надіслав `id`, а тип даних не точний.

## Де стоїть ключ

Ключ потрібен елементу, який безпосередньо лежить у масиві, тобто тому, що повертає функція в `map`. Є дві типові
помилки.

**Ключ усередині рядка.** Якщо рядок винесено в окремий компонент, ключ ставлять на тег цього компонента, а не на
`<li>` усередині нього:

```tsx
function Line({ name }: { name: string }) {
  return <li key={name}>{name}</li>
}
function Lines() {
  return <ul>{STUDENTS.map((s) => <Line name={s.name} />)}</ul>
}

render(<Lines />) // рядок друку не потрібен: попередження в консоль пише сам React
```

```text
Each child in a list should have a unique "key" prop.

Check the render method of `Lines`. See https://react.dev/link/warning-keys for more information.
```

Тут масив містить елементи `Line`, і саме в них ключа немає. Ключ у `<li>` стоїть уже всередині, серед дітей `Line`,
де порівнювати його немає з чим. Така сама помилка виникає, коли ключ поставлено на поле всередині рядка, а не на сам
рядок.

**Рядок із кількох тегів.** Лекція «JSX» показала фрагмент `<>…</>`, який групує теги без зайвого вузла. Скорочений
запис не приймає атрибутів, тому фрагмент із ключем пишуть повністю й імпортують `Fragment` із `react`:

```tsx
function Definitions() {
  return (
    <dl>
      {STUDENTS.map((s) => (
        <Fragment key={s.id}>
          <dt>{s.name}</dt>
          <dd>{s.id}</dd>
        </Fragment>
      ))}
    </dl>
  )
}

console.log(render(<Definitions />).container.innerHTML)
```

```text
<dl><dt>Марта</dt><dd>11</dd><dt>Богдан</dt><dd>12</dd><dt>Соломія</dt><dd>13</dd></dl>
```

Фрагмент не залишає в документі нічого, а ключ він проте має, бо ключ потрібен React, а не документу.

## Звідки взяти ключ

Сторінка `Rendering Lists` у розділі `Where to get your key` називає два джерела, а решта випливає з правил.

| Звідки дані | Ключ |
|-------------|------|
| із бази чи сервера | `id` запису, бо база вже гарантує, що він не повторюється |
| створюються в застосунку | лічильник або `crypto.randomUUID()`, викликаний один раз, коли запис створено |
| два джерела в одному списку | поєднання, наприклад `` `teacher-${t.id}` `` і `` `student-${s.id}` ``, бо `id` з різних таблиць можуть збігтися |
| статичний масив, який ніколи не змінюється і не містить стану | індекс теж годиться; сторінка дає такий приклад для рядків вірша |
| назви, які гарантовано різні | назва теж годиться, як `key={name}` у лекції про чистоту, де імена в черзі не повторюються |

Якщо дані прийшли без `id`, ідентифікатор додають один раз, коли дані отримано, а не під час рендеру:

```js
let nextId = 1
const withIds = (names) => names.map((name) => ({ id: nextId++, name }))

const loaded = withIds(['Марта', 'Марта'])
console.log(loaded)
console.log(withIds(['Богдан']))
```

```text
[ { id: 1, name: 'Марта' }, { id: 2, name: 'Марта' } ]
[ { id: 3, name: 'Богдан' } ]
```

Далі в кожному рендері використовується вже збережений `id`. Лічильник має межу: якщо записи збережено й після
перезавантаження сторінки вони повернулися, лічильник почнеться з одиниці й видасть уже зайняті номери. У такому разі
лічильник треба починати з найбільшого збереженого значення або взяти `crypto.randomUUID()`. За даними MDN, цей метод
у браузері доступний лише в захищеному контексті, тобто на сторінках HTTPS. Ми цього в браузері не перевіряли, тому,
якщо застосунок відкривають через звичайний HTTP, перевірте це самі.

## Коли React попереджає

Попередження про ключі зручне, але в нього три межі.

**Воно є лише в режимі розробки.** Лекція «Інструменти браузера» пояснила, що збірка для користувачів вирізає код,
загорнутий у перевірку `NODE_ENV`. Попередження теж там. Цей файл запускають самим Node, без Vitest, тому імітацію
браузера він готує сам, а теги записує викликом `createElement`, бо JSX у Node не працює. Він показує той самий список
без ключів і з однаковими ключами:

```js
// файл prod.mjs
import { JSDOM } from 'jsdom'
import { createElement as h } from 'react'
import { flushSync } from 'react-dom'

// Пакет react-dom/client шукає документ під час завантаження, тому імітацію браузера готують раніше.
const { window } = new JSDOM('<div id="a"></div><div id="b"></div>')
globalThis.window = window
globalThis.document = window.document
const { createRoot } = await import('react-dom/client')

let messages = 0
console.error = () => { messages += 1 } // рахує все, що React пише про помилки

const names = ['а', 'б']
const show = (id, element) => flushSync(() => createRoot(document.getElementById(id)).render(element))
show('a', h('ul', null, names.map((n) => h('li', null, n)))) // список без ключів
show('b', h('ul', null, names.map((n) => h('li', { key: 'той самий' }, n)))) // однакові ключі
console.log('NODE_ENV =', process.env.NODE_ENV, '| повідомлень React:', messages)
```

Ми запустили цей файл двома способами:

```text
$ node prod.mjs
NODE_ENV = undefined | повідомлень React: 2
$ NODE_ENV=production node prod.mjs
NODE_ENV = production | повідомлень React: 0
```

У першому запуску змінна `NODE_ENV` не задана, тому React працює в режимі розробки й пише два попередження. У другому
запуску ті самі помилки в ключах лишилися, а React не написав нічого. Отже, у збірці для користувачів консоль про
ключі мовчить, і шукати такі помилки треба під час розробки.

**Воно друкується один раз для назви батька.** React пам'ятає, для якої назви батьківського тега чи компонента вже
попередив. Другий `<ul>` без ключів, навіть в іншому компоненті, мовчить, доки сторінку не перезавантажено, а `<ol>`
знову дає попередження:

```tsx
const names = ['а', 'б']
function First() { return <ul>{names.map((n) => <li>{n}</li>)}</ul> }
function Second() { return <ul>{names.map((n) => <li>{n}</li>)}</ul> }
function Third() { return <ol>{names.map((n) => <li>{n}</li>)}</ol> }

const errors = vi.spyOn(console, 'error').mockImplementation(() => {})
render(<First />)
console.log('після першого:', errors.mock.calls.length)
render(<Second />)
console.log('після другого:', errors.mock.calls.length)
render(<Third />)
console.log('після третього:', errors.mock.calls.length)
```

```text
після першого: 1
після другого: 1
після третього: 2
```

Функція `vi.spyOn` тимчасово підміняє `console.error` і рахує виклики. Цей наслідок стосується вашої практики:
перевірки дня збирають виклики `console.error` після кожного тесту, тому при забутому ключі падає лише перший приклад
із повідомленням про ключ, а наступні такого повідомлення вже не отримують. Vitest запускає кожен файл окремо, тому в
іншому файлі лічба починається знову.

**Воно перевіряє наявність, а не якість.** `key={index}` дає ключі `0`, `1`, `2`, вони є і не повторюються, тому React
мовчить. Журнал на початку лекції не надрукував нічого. Тиша в консолі не є доказом правильного ключа.

## Як тест діє замість людини

Завдання дня перевіряє поведінку поля, тому тести мають набирати текст. Це робить бібліотека `user-event`. Вона є
окремим пакетом, а показує компоненти інша бібліотека, `@testing-library/react`. Сторінка `user-event: Introduction`
пояснює, чим вона відрізняється від простішого `fireEvent`: той надсилає одну подію, а `user-event` відтворює всю дію
людини.

Це видно на одній літері:

```tsx
const log: string[] = []
const note = (e: { type: string }) => { log.push(e.type) }
render(<input aria-label="поле" onMouseDown={note} onFocus={note} onClick={note} onKeyDown={note} onChange={note} onKeyUp={note} />)
const field = screen.getByLabelText<HTMLInputElement>('поле')

await user.type(field, 'а')
console.log('user.type:', log.join(' '), '| значення:', field.value, '| фокус:', document.activeElement === field)

field.blur()
log.length = 0
fireEvent.change(field, { target: { value: 'бб' } })
console.log('fireEvent:', log.join(' '), '| значення:', field.value, '| фокус:', document.activeElement === field)
```

```text
user.type: mousedown focus click keydown change keyup | значення: а | фокус: true
fireEvent: change | значення: бб | фокус: false
```

Метод `user.type` натиснув на поле, надав йому фокус і лише потім ввів літеру. Саме тому перевірка дня може сказати,
що «після перемалювання поле втратило фокус»: спершу фокус там справді був. Записом `fireEvent.change` такого б не
вийшло.

Три правила запису.

**Спершу `setup`, потім `render`.** Виклик `const user = userEvent.setup()` створює об'єкт `user`, методи якого ділять
між собою стан пристроїв введення, наприклад затиснуту клавішу. Сторінка радить робити це на початку тесту, а не в
спільних `beforeEach` чи поза тестом.

**Кожну дію чекають через `await`.** Методи повертають проміс, про який ви читали в лекції «Асинхронність». Якщо
забути `await`, наступний рядок виконається раніше, ніж текст з'явиться в полі:

```tsx
render(<input aria-label="поле" />)
const field = screen.getByLabelText<HTMLInputElement>('поле')
const typing = user.type(field, 'abc')
console.log('без await:', JSON.stringify(field.value))
await typing
console.log('з await:', JSON.stringify(field.value))
```

```text
без await: ""
з await: "abc"
```

Функція тесту через це має бути позначена `async`.

**Елемент шукають за тим, що бачить людина.** У полів немає видимого підпису, тому їм дають атрибут `aria-label`,
тобто підпис для програм читання екрана. Запит `getByRole('textbox', { name: '…' })` знаходить поле за цим підписом.
Докладно запити за роллю пояснює розбір читання до дня «Пропси й умовний рендер». Роль `textbox` має текстове поле, а
роль `listitem` має тег `<li>`.

## Рецепт для списку

Рецепт із книжки How to Design Programs не змінюється, бо компонент зі списком залишається функцією. Сьогоднішнє
завдання цікаве тим, що частину логіки легко винести з компонента, і вона стає простою функцією з прикладами.

| Крок рецепта | Що це для списку |
|--------------|------------------|
| опис даних | тип запису з `id` і назвою, тип з двох рядкових варіантів для способу вибрати ключ; поля пояснено в коментарі |
| призначення й сигнатура | одне речення над кожною функцією, типи в коді |
| приклади | функції перевіряють `expect`, компонент перевіряють `render` і дії через `userEvent` |
| перелік вхідних даних | коментар у тілі: пропси, стан, функція його зміни й допоміжні функції |
| тіло | функції спершу, компонент останнім, бо він їх викликає |
| перевірка | Vitest запускає приклади, а `tsc` перевіряє типи |

Ось чому варто виносити таку логіку. Якщо функція просто отримує масив і повертає новий, її приклад не потребує ні
сторінки, ні кліків, а межі можна перебрати за секунду: запис, якого немає, порожній масив, перевірка, що вхідний
масив не змінився. Компонент лишається лише зв'язком між цими функціями й екраном.

Приклад, який перевіряє поведінку поганого ключа, тут особливий. Він навмисно записує неправильний результат, бо
завдання дня показує саме цю поведінку. У справжньому проєкті ви не писатимете проп, що вибирає ключ, а напишете один
ключ за `id`, і приклад перевірятиме лише правильну поведінку.

Подивитися на сторінку можна запуском `npm run dev` за адресою `/f1-d04.html`. Саму сторінку ми в браузері не
відкривали. Те, що ви там побачите, випливає з тестів: `user-event` набирає текст і натискає кнопки в jsdom так, як
описано вище.

## Хто яку помилку ловить

Колонку React у таблиці нижче показали приклади цієї лекції. Колонки `tsc` і ESLint отримано на окремому файлі, де
кожна помилка стоїть у своєму компоненті:

```tsx
// файл src/mistakes.tsx
type Row = { id: number; name: string }
const ROWS: Row[] = [{ id: 1, name: 'Марта' }]

export function NoKey() {
  return <ul>{ROWS.map((r) => <li>{r.name}</li>)}</ul>
}
export function IndexKey() {
  return <ul>{ROWS.map((r, i) => <li key={i}>{r.name}</li>)}</ul>
}
export function RandomKey() {
  return <ul>{ROWS.map((r) => <li key={Math.random()}>{r.name}</li>)}</ul>
}
export function TimeKey() {
  return <ul>{ROWS.map((r) => <li key={Date.now()}>{r.name}</li>)}</ul>
}
export function UuidKey() {
  return <ul>{ROWS.map((r) => <li key={crypto.randomUUID()}>{r.name}</li>)}</ul>
}
export function NameKey() {
  return <ul>{ROWS.map((r) => <li key={r.name}>{r.name}</li>)}</ul>
}
export function NullKey({ rows }: { rows: { id: number | null }[] }) {
  return <ul>{rows.map((r) => <li key={r.id}>рядок</li>)}</ul>
}
function Line({ name }: { name: string }) {
  return <li key={name}>{name}</li>
}
export function KeyInside() {
  return <ul>{ROWS.map((r) => <Line name={r.name} />)}</ul>
}
export function ReadsKey({ key }: { key: string }) {
  return <p>{key}</p>
}
```

Команда `npx tsc --noEmit -p tsconfig.app.json` про цей файл не друкує нічого. ESLint до кожної знахідки друкує довге
пояснення, тому цей короткий файл просить у нього лише назву правила й рядок, де правило спрацювало:

```js
// файл lint.mjs
import { ESLint } from 'eslint'

const [result] = await new ESLint().lintFiles(['src/mistakes.tsx'])
const lines = result.source.split('\n')
for (const m of result.messages) console.log(m.ruleId, '|', lines[m.line - 1].trim())
console.log('знахідок:', result.messages.length)
```

```text
$ node lint.mjs
react-hooks/purity | return <ul>{ROWS.map((r) => <li key={Math.random()}>{r.name}</li>)}</ul>
react-hooks/purity | return <ul>{ROWS.map((r) => <li key={Date.now()}>{r.name}</li>)}</ul>
знахідок: 2
```

Отже, ESLint помітив лише дві помилки з дев'яти, а `tsc` жодної. Те саме разом із колонкою React:

| Помилка | `tsc` | ESLint | React у режимі розробки | Що ще помітить |
|---------|-------|--------|-------------------------|----------------|
| ключа немає | мовчить | мовчить | `Each child in a list…`, один раз на назву батька | приклад із видаленням |
| `key={index}` при зміні складу | мовчить | мовчить | мовчить | лише приклад із видаленням не останнього рядка |
| `key={Math.random()}` | мовчить | `react-hooks/purity` | мовчить | приклад із повторним рендером |
| `key={Date.now()}` | мовчить | `react-hooks/purity` | `Encountered two children…`, якщо час той самий | приклад із повторним рендером |
| `key={crypto.randomUUID()}` у `map` | мовчить | мовчить | мовчить | приклад із повторним рендером |
| ключ-назва, яка повторюється | мовчить | мовчить | `Encountered two children…` | приклад з однаковими назвами |
| `key={row.id}`, коли `id` дорівнює `null` | мовчить | мовчить | `Encountered two children…` із ключем `null` | дані сервера |
| ключ усередині компонента рядка | мовчить | мовчить | `Each child in a list…` | приклад із видаленням |
| `props.key` | мовчить | мовчить | `` `key` is not a prop `` | значення `undefined` |

Рядки ESLint перевірено набором `typescript-eslint` recommended і `react-hooks` recommended, тобто тим самим, що
підключив шаблон проєкту. Існує окреме правило проти індекса в ключі, `react/no-array-index-key` із пакета
`eslint-plugin-react`, але цього пакета в проєкті немає. Найнебезпечніша помилка дня стоїть у другому рядку таблиці,
бо її не помічає жоден автоматичний інструмент. Її знайде лише приклад із видаленням, тому такий приклад і є в
завданні.

## Типові хибні уявлення

**«Ключ потрібен, щоб прибрати попередження».** Попередження є лише нагадуванням. Ключ потрібен, щоб React правильно
зіставив рядки двох рендерів. Індекс прибирає попередження, але не проблему.

**«Індекс завжди поганий ключ».** Для списку, який не змінюється, або для рядків без власного вмісту індекс працює.
Сторінка `Rendering Lists` сама вживає його для рядків вірша. Погано те, що ця умова легко перестає виконуватися після
дрібної зміни рядка.

**«Ключ має бути унікальним на всю сторінку».** Лише серед сусідів в одному масиві. Той самий `id` може стояти в
іншому списку.

**«React перемалював список і заповнив рядки по черзі».** React заповнює рядки за збігом ключа, а не за чергою. З
ключем `id` компонент викликається так само, а результат правильний.

**«Текст поїхав, бо поле некероване».** Некерованість пояснює, чому React не переписав текст. Те, куди поїхав вміст,
вирішує ключ. Стан компонента в рядку поводиться так само, хоча React про нього знає.

**«Стан лежить у вузлі документа».** Текст некерованого поля лежить у вузлі, а значення `useState` тримає сам React.
Вузол і стан належать одному екземпляру, тому переїжджають разом, але лежать у різних місцях.

**«Переміщений рядок React створює заново».** З тим самим ключем у того самого батька вузли лишаються тими самими
навіть після зміни порядку. Це можна перевірити порівнянням вузлів через `===`:

```tsx
function Order({ rows }: { rows: Student[] }) {
  return <ul>{rows.map((s) => <li key={s.id}><input aria-label={s.name} /></li>)}</ul>
}

const { rerender } = render(<Order rows={STUDENTS} />)
const before = STUDENTS.map((s) => screen.getByLabelText(s.name)) // поля до зміни порядку
rerender(<Order rows={[...STUDENTS].reverse()} />)
const after = STUDENTS.map((s) => screen.getByLabelText(s.name)) // поля тих самих учнів після зміни
console.log('порядок на екрані:', screen.getAllByRole('textbox').map((f) => f.getAttribute('aria-label')).join(', '))
console.log('ті самі вузли:', before.map((node, i) => node === after[i]))
```

```text
порядок на екрані: Соломія, Богдан, Марта
ті самі вузли: [ true, true, true ]
```

Порядок змінився, а всі три поля лишилися тими самими об'єктами. Отже, зі стабільним ключем React лише переставляє
наявні вузли, і текст у полях нікуди не зникає.

**«Якщо тести зелені, ключ правильний».** У тесті без видалення й без перевірки значення жоден ключ нічим не
відрізняється від іншого.

## Як це проявиться далі в React

- **День 5, чистота й дерево.** Лекція почне з `key={name}` у списку талонів. Заборона викликати під час рендеру те,
  що щоразу дає інший результат, стане загальним правилом.
- **День 6, TypeScript у React.** Ви побачите, чому `key` дозволено в кожному компоненті, хоча в типі пропсів його
  немає.
- **День 7, події й стан.** Кероване поле з цієї лекції отримає докладний розбір, а кнопка в рядку передаватиме
  батькові, що саме видалити.
- **День 9, об'єкти й масиви в стані.** Ви побачите всі дії над масивом без зміни старого і зміну одного запису
  всередині масиву.
- **День 12, спільний стан і скидання стану.** Ключ стане інструментом поза списками: запис `<Chat key={contact.id}
  />` навмисно скидає стан, коли змінюється контакт. Це той самий механізм: новий ключ означає новий екземпляр.
- **Фаза 2, день 7, віртуалізація.** Довгий список показують частинами: рядки з'являються й зникають під час
  прокрутки, і React упізнає їх за тими самими ключами.

## Перевірте себе

**1. Два рядки написано вручну: `<ul><li>а</li><li>б</li></ul>`. Чому ключі не потрібні, а для `map` потрібні?**

<details><summary>Відповідь</summary>

Компілятор бачить обидва рядки в тексті програми й викликає `_jsxs`. Такий набір не може змінити порядок чи кількість,
тому порівняння за номером завжди правильне. Результат `map` залежить від даних, і компілятор про нього нічого не
знає.

</details>

**2. Компонент оголошено як `function Row({ key, name })`. Що буде в змінній `key`, і що робити, якщо значення справді
потрібне?**

<details><summary>Відповідь</summary>

`undefined`, а React у режимі розробки попередить, що `key` не є пропом. Значення передають другим пропом: `<Row
key={s.id} studentId={s.id} name={s.name} />`.

</details>

**3. Список із `key={index}` містить поля. Ви перевірили додавання в кінець і видалення останнього рядка, і все
правильно. Чому це нічого не доводить?**

<details><summary>Відповідь</summary>

Ці дві дії не змінюють номерів рядків, що лишилися, тому ключі збігаються зі змістом. Помилка з'являється при
видаленні першого чи середнього рядка, при додаванні на початок і при зміні порядку.

</details>

**4. Рядок показує лише назву, без поля й без стану. Чи шкодить тут `key={index}` при видаленні першого рядка?**

<details><summary>Відповідь</summary>

На екрані результат правильний, бо текст приходить із елемента. Проте React переписує текст майже в кожному рядку: для
тисячі рядків це 999 змін замість жодної. І щойно в рядку з'явиться поле чи компонент зі станом, з'явиться й помилка.

</details>

**5. У рядку є компонент зі станом, а ключ дорівнює індексу. Де лежить стан і чому він переїжджає, хоча вузол
документа тут ні до чого?**

<details><summary>Відповідь</summary>

Стан тримає React і пов'язує його з екземпляром на місці, яке задає ключ. Після видалення першого рядка ключ `0`
належить уже наступному запису, але екземпляр із ключем `0` зі своїм станом лишився і отримує нові пропси.

</details>

**6. Чому `key={crypto.randomUUID()}` у `map` є помилкою, якщо сторінка `Rendering Lists` радить
`crypto.randomUUID()`?**

<details><summary>Відповідь</summary>

Сторінка радить викликати його один раз, коли запис створено, і зберігати результат у даних. У `map` він викликається
в кожному рендері й щоразу дає нове значення, тому всі рядки видаляються й створюються знову, як із `Math.random()`.

</details>

**7. Під час розробки React не написав нічого про ключі цього списку. Чи означає це, що ключі правильні?**

<details><summary>Відповідь</summary>

Ні. React перевіряє лише, чи ключ є і чи він не повторюється, а попередження про відсутній ключ ще й друкує один раз
на назву батька. Індекс і випадкове число для нього цілком допустимі.

</details>

## Словничок лекції

| Слово | Що означає |
|-------|------------|
| елемент | об'єкт з описом того, що показати, результат виклику `jsx` |
| ключ | значення `key`, яке позначає елемент серед сусідів, завжди рядок |
| зіставлення | порівняння React старих і нових дітей одного батька за типом і ключем |
| екземпляр | запис React про компонент на конкретному місці разом зі станом і вузлами |
| вузол | об'єкт документа, який браузер показує на екрані |
| некероване поле | поле без `value`, його текст лежить у вузлі |
| кероване поле | поле з `value`, текст у нього пише React зі стану |
| `aria-label` | атрибут, який дає елементу підпис для програм читання екрана |
| `user-event` | бібліотека, яка в тесті відтворює дії людини цілком |
| `MutationObserver` | вбудований об'єкт, який записує зміни документа |

## Що читати далі

- [Розбір читання до цього дня](../reading/f1-d04-reading.md): що саме написано в матеріалах дня й де що шукати.
- Rendering Lists: головна сторінка дня.
- Preserving and Resetting State: сторінка, яку ви читатимете в день 12, а вправа `Fix misplaced state in the list`
  там є тією самою помилкою з індексом.
- Fragment: розділ про список фрагментів.
- Crypto: randomUUID(): сторінка MDN про метод і захищений контекст.
- Differences from fireEvent: чим `user-event` відрізняється від простих подій.

---

Лекцію написано для цього плану. Вона спирається на документацію React, Testing Library і MDN, а також переказує
рецепт із книжки How to Design Programs. Усе переказано своїми словами, а права на ці тексти належать їхнім авторам.
