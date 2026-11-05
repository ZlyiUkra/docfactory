# Лекція. Фаза 1, день 17. Коли ефект не потрібен

Попередня лекція навчила писати ефекти. Ця лекція вчить їх прибирати, і для плану це головний день фази. Якщо людина
вперше дізналася про `useEffect`, вона часто починає розв'язувати ним усе підряд: перерахунок суми, реакцію на клік,
очищення форми. Такий код начебто працює, але дає зайві рендери, застарілі значення й помилки, які важко знайти.
Читання займе близько 45 хвилин.

Приклади запущено на React 19.3 у Vitest під jsdom, тобто в імітації браузера всередині Node. Вивід під прикладами
справжній. Типи перевірено компілятором `tsc` версії 6.0, а лінт перевірено ESLint із тим самим набором правил
`react-hooks`, що й у проєкті `spa`. Один дослід потребував справжнього малювання сторінки, тому ми запустили його в
Chrome 157 без вікна, на зібраному застосунку, і біля нього про це сказано.

Застереження про версію компілятора: у перших лекціях про TypeScript команда `tsc` мала версію 7, а в проєкті `spa`
вона має версію 6.0. Це вимушене обмеження через ESLint. ESLint читає файли TypeScript через пакет
`typescript-eslint`, а цей пакет у версії 8.72 працює лише з TypeScript, нижчим за 6.1. Тому версію TypeScript у `spa`
закріплено на 6.0. Коли `typescript-eslint` запрацює з TypeScript 7, обмеження можна буде зняти.

Практика дня дає заготовку із зайвими ефектами й просить їх прибрати. Лекція бере інший об'єкт, кав'ярню, тому
компоненти заготовки доведеться переробити самостійно.

**Після лекції ви зможете пояснити:**

- за яким запитанням відрізнити потрібний ефект від зайвого;
- чому значення, обчислене ефектом, спершу показує застарілий результат і коштує зайвий рендер;
- коли обчислення треба загорнути в `useMemo` і як це заміряти;
- чому реакція на клік в ефекті спрацьовує тоді, коли ніхто нічого не клацав;
- як `key` скидає весь стан і чого це коштує;
- що робити, якщо скинути треба лише частину стану;
- чому копія значення в стані розходиться з оригіналом;
- як ланцюг ефектів множить рендери й чому він ламається від нової вимоги;
- як повідомити батька без ефекту;
- що лінт бачить, а чого не бачить, і чому чистий лінт не означає відсутності зайвих ефектів;
- які ефекти лишаються, бо вони справді потрібні.

## Сума, яка на мить неправильна

Ви робите кошик кав'ярні. Батько передає позиції замовлення, а компонент показує підсумок. Лекція «Структура стану»
вчила не зберігати те, що можна обчислити, але на практиці рука часто тягнеться до такого запису:

```tsx
function TotalByEffect({ lines }: { lines: Line[] }) {
  const [total, setTotal] = useState(0)
  useEffect(() => {
    log.push('ефект: у документі «' + document.querySelector('p')?.textContent + '»')
    setTotal(lines.reduce((sum, l) => sum + l.price * l.qty, 0))
  }, [lines])
  log.push(`рендер: позицій ${lines.length}, разом ${total}`)
  return <p role="status">Разом: {total} грн</p>
}
```

Рядки `log.push` записують журнал лише для досліду. У кошику лежить дві чашки лате по 80 гривень, а людина додає чай
за 50 гривень. Поруч стоїть той самий компонент без ефекту:

```tsx
function TotalDirect({ lines }: { lines: Line[] }) {
  const total = lines.reduce((sum, l) => sum + l.price * l.qty, 0)
  log.push(`рендер: позицій ${lines.length}, разом ${total}`)
  return <p role="status">Разом: {total} грн</p>
}
```

Кожен дослід цієї лекції є окремим файлом тесту, наприклад `total.test.tsx`. Файл починається такими рядками, а далі
в нього йдуть блоки коду з розділу. Команда `npx vitest run total.test.tsx --disable-console-intercept` запускає файл,
а прапорець прибирає службові підписи біля кожного надрукованого рядка.

```tsx
// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest'
import { act, fireEvent, render, screen } from '@testing-library/react'
import { StrictMode, useEffect, useMemo, useState, useSyncExternalStore, type FC, type ReactNode } from 'react'
import { expect, test } from 'vitest'
```

Тест спершу показує кошик із лате, потім очищує журнал і передає кошик із лате й чаєм. Тому в журналі лишається тільки
те, що сталося після додавання чаю:

```tsx
type Line = { name: string; price: number; qty: number }
const LATTE: Line = { name: 'лате', price: 80, qty: 2 }
const TEA: Line = { name: 'чай', price: 50, qty: 1 }
const log: string[] = []

function addTea(title: string, Total: FC<{ lines: Line[] }>) {
  const { rerender, unmount } = render(<Total lines={[LATTE]} />)
  log.length = 0 // Журнал першого показу нам не потрібен.
  rerender(<Total lines={[LATTE, TEA]} />) // Людина додала чай, і батько передає новий масив.
  console.log(title + '\n' + log.join('\n'))
  expect(screen.getByRole('status')).toHaveTextContent('Разом: 210 грн')
  unmount()
}

test('кошик', () => {
  addTea('з ефектом', TotalByEffect)
  addTea('без ефекту', TotalDirect)
})
```

```text
з ефектом
рендер: позицій 2, разом 160
ефект: у документі «Разом: 160 грн»
рендер: позицій 2, разом 210
без ефекту
рендер: позицій 2, разом 210
```

Читайте рядки згори вниз. Перший рендер варіанта з ефектом уже бачить дві позиції, але суму ще стару. React записує
цей результат у документ, і лише потім запускає ефект. Рядок «ефект» показує, що в документі в цю мить справді лежить
160 гривень при двох позиціях. Ефект просить новий рендер, і тоді сума стає правильною. Варіант без ефекту робить усе
за один виклик, і дані в ньому завжди узгоджені.

Чи побачить людина цю суму? Лекція «Спільний стан і скидання стану» пояснила, що довідник `useEffect` це не визначає
однозначно: після клацання React може виконати ефект до малювання, а після таймера чи відповіді мережі зазвичай після
нього. Ми заміряли це для кошика в Chrome без вікна на зібраному застосунку. Перед кожним кадром функція
`requestAnimationFrame` порівнювала кількість позицій і суму. Компонент ми навмисно уповільнили, щоб рендер займав 6
мс, а таймер ставив оновлення в різні моменти кадру. Команда `npx vite build` збирає таку сторінку, а `npx vite
preview` показує її, і результат друкується в консоль браузера:

```tsx
// src/main.tsx
import { useEffect, useState, type FC } from 'react'
import { createRoot } from 'react-dom/client'

type Line = { name: string; price: number; qty: number }
const LATTE: Line = { name: 'лате', price: 80, qty: 2 }
const TEA: Line = { name: 'чай', price: 50, qty: 1 }
const RENDER_MS = 6 // Скільки мілісекунд компонент навмисно зайнятий під час кожного рендеру.
const sum = (lines: Line[]) => lines.reduce((s, l) => s + l.price * l.qty, 0)

function slowDown() {
  const end = performance.now() + RENDER_MS
  while (performance.now() < end); // Порожній цикл просто тримає рендер зайнятим.
}

function TotalByEffect({ lines }: { lines: Line[] }) {
  slowDown()
  const [total, setTotal] = useState(0)
  useEffect(() => {
    effectRan = lines.length === 2
    setTotal(sum(lines))
  }, [lines])
  return <p data-count={lines.length} data-total={total}>Разом: {total} грн</p>
}

function TotalDirect({ lines }: { lines: Line[] }) {
  slowDown()
  const total = sum(lines)
  return <p data-count={lines.length} data-total={total}>Разом: {total} грн</p>
}

let effectRan = false // Чи встиг ефект цієї спроби виконатися після додавання чаю.
let afterEffect = 0 // Скільки застарілих кадрів прийшло вже після ефекту.
let addTea = () => {} // Кошик записує сюди функцію, щоб таймер міг додати чай без клацання.

function Cart({ Total }: { Total: FC<{ lines: Line[] }> }) {
  const [lines, setLines] = useState([LATTE])
  addTea = () => setLines([LATTE, TEA])
  return <><button onClick={addTea}>чай</button><Total lines={lines} /></>
}

const nextFrame = () => new Promise(requestAnimationFrame)

async function staleFrames(Total: FC<{ lines: Line[] }>, how: string, attempt: number) {
  const box = document.body.appendChild(document.createElement('div'))
  const root = createRoot(box)
  root.render(<Cart Total={Total} />)
  await nextFrame()
  await nextFrame()
  const shown = box.querySelector('p')!
  let stale = 0
  let watching = true
  function beforeFrame() {
    // Дві позиції й сума не 210 означають, що цей кадр покаже застарілу суму.
    if (shown.dataset.count === '2' && shown.dataset.total !== '210') {
      stale++
      if (effectRan) afterEffect++
    }
    if (watching) requestAnimationFrame(beforeFrame)
  }
  requestAnimationFrame(beforeFrame)
  // Різна затримка ставить оновлення в різні моменти кадру.
  setTimeout(() => (how === 'клацання' ? box.querySelector('button')!.click() : addTea()), 20 + (attempt % 17))
  await new Promise((done) => setTimeout(done, 100))
  watching = false
  root.unmount()
  box.remove()
  return stale
}

for (const how of ['клацання', 'таймер']) {
  let byEffect = 0
  let direct = 0
  afterEffect = 0
  for (let attempt = 0; attempt < 60; attempt++) {
    byEffect += await staleFrames(TotalByEffect, how, attempt)
    direct += await staleFrames(TotalDirect, how, attempt)
  }
  console.log(`${how} | спроб 60 | кадрів зі старою сумою: з ефектом ${byEffect}, із них після ефекту ${afterEffect}, без ефекту ${direct}`)
}
```

| Що викликало оновлення | Спроб | Кадрів зі старою сумою, з ефектом | Із них кадрів уже після ефекту | Кадрів зі старою сумою, без ефекту |
|------------------------|-------|-----------------------------------|--------------------------------|------------------------------------|
| клацання, викликане кодом | 60 | 23 | 23 | 0 |
| таймер | 60 | 22 | 0 | 0 |

Отже, неправильна сума справді потрапляла на кадр приблизно в кожній третій спробі. Це те мерехтіння, яке згадує план.
Стовпець «Із них кадрів уже після ефекту» показує різницю між двома рядками. Після таймера кадр прийшов ще до ефекту.
Після клацання ефект уже виконався, але новий рендер, який попросив виклик `setTotal`, ще не встиг статися, тому
клацання теж не захищає від застарілого кадру. Коли ми поставили `RENDER_MS = 0`, той самий дослід дав лише по одному
такому кадру в кожному рядку, тому число залежить від машини й важкості рендеру. Гарантії немає, а варіант без ефекту
ніколи не дає такого кадру, бо в нього немає проміжного стану.

Обидва варіанти проходять той самий тест `expect(screen.getByRole('status')).toHaveTextContent('Разом: 210 грн')`, бо
Testing Library дочікується ефектів. Звідси практичний висновок: після вилучення ефекту тести мають лишитися зеленими,
але вони нічого не скажуть про зайві рендери. Рендери треба рахувати окремо.

## Головне запитання

Сторінка `You Might Not Need an Effect` пропонує два запитання. Перше: чи бере участь у задачі система поза React?
Якщо ні, ефект, найімовірніше, не потрібен. Друге: чому цей код має виконатися? Ефект потрібен для коду, який
виконується тому, що компонент показано людині. Усе інше належить іншому місцю.

| Що ви хочете зробити | Куди це покласти | Розділ нижче |
|----------------------|------------------|--------------|
| обчислити значення з пропсів чи стану | у тіло компонента | «Обчислення під час рендеру» |
| те саме, але обчислення дороге | у `useMemo` | «Дорогий підрахунок» |
| відреагувати на дію людини | в обробник події | «Реакція на дію людини» |
| почати все спочатку, коли змінився пропс | у `key` | «Скидання всього стану» |
| змінити лише частину стану, коли змінився пропс | краще обчислити, а в рідкому випадку змінити під час рендеру | «Скидання частини стану» |
| зберегти значення, яке випливає з іншого поля | нікуди, його обчислюють | «Поле, обчислене з іншого поля» |
| підписатися на сховище поза React | у `useSyncExternalStore` | «Сховище поза React» |
| підключитися, підписатися, завантажити дані, поки компонент на екрані | в ефект із прибиранням | «Що лишається ефектом» |

## Обчислення під час рендеру

Перший випадок ви вже бачили на кошику. Правило сторінки React звучить так: якщо щось можна обчислити з наявних
пропсів чи стану, не кладіть це в стан, а обчислюйте під час рендеру. Такий код швидший, бо немає зайвих оновлень,
простіший, бо менше рядків, і надійніший, бо дві змінні не можуть розійтися.

Лінт проєкту помічає цю помилку. Правило `react-hooks/set-state-in-effect`, яке показувала лекція «Структура стану»,
повідомляє про рядок із `setTotal`.

### Дорогий підрахунок

Перше заперечення звучить так: «Але ж обчислення виконуватиметься при кожному рендері». Так, виконуватиметься.
Подивімося на пошук у меню, де є ще поле нотатки, яке нічого не змінює в меню:

```tsx
function SearchPlain({ menu, query }: { menu: string[]; query: string }) {
  const [note, setNote] = useState('')
  const shown = pickActive(menu, query)
  return <><input aria-label="нотатка" value={note} onChange={(e) => setNote(e.target.value)} /><p>{shown.length}</p></>
}
```

Хук `useMemo` приймає функцію й список залежностей, запам'ятовує результат і перераховує його, лише коли змінилося
якесь значення зі списку. Це називають **мемоізацією**. Лекція «Контекст» уже показала цей хук для іншої мети, а саме
щоб не створювати новий об'єкт:

```tsx
function SearchMemo({ menu, query }: { menu: string[]; query: string }) {
  const [note, setNote] = useState('')
  const shown = useMemo(() => pickActive(menu, query), [menu, query])
  return <><input aria-label="нотатка" value={note} onChange={(e) => setNote(e.target.value)} /><p>{shown.length}</p></>
}
```

Лічильник у `pickActive` рахує виклики. Сценарій такий: показ, три літери в нотатці, потім новий запит:

```tsx
const MENU = ['лате', 'чай', 'какао']
let calls = 0

function pickActive(menu: string[], query: string) {
  calls++ // Лічильник показує, скільки разів фільтр справді виконався.
  return menu.filter((name) => name.includes(query))
}

function typeNote(title: string, Search: FC<{ menu: string[]; query: string }>) {
  calls = 0
  const { rerender, unmount } = render(<Search menu={MENU} query="лате" />)
  for (const value of ['б', 'бе', 'без']) {
    fireEvent.change(screen.getByLabelText('нотатка'), { target: { value } })
  }
  const afterNote = calls
  rerender(<Search menu={MENU} query="чай" />)
  console.log(`${title} | показ і три літери в нотатці: ${afterNote} | новий запит: ${calls}`)
  unmount()
}

test('пошук', () => {
  typeNote('без useMemo', SearchPlain)
  typeNote('з useMemo', SearchMemo)
})
```

```text
без useMemo | показ і три літери в нотатці: 4 | новий запит: 5
з useMemo | показ і три літери в нотатці: 1 | новий запит: 2
```

Хук справді прибрав три зайві виклики. Чи варто було? Сторінка React радить міряти. Вартим уваги вона вважає
обчислення, на яке за одну дію набігає близько однієї мілісекунди, а якщо ви не створюєте й не обходите тисячі
об'єктів, обчислення, мабуть, недороге. Ось наш замір у файлі `filter.mjs`, який запускає команда `node filter.mjs`:

```js
const rows = Array.from({ length: 1000 }, (_, i) => ({ name: 'напій ' + i, active: i % 2 === 0 }))
const times = []
let found = 0
for (let run = 0; run < 200; run++) {
  const start = performance.now()
  found = rows.filter((row) => row.active && row.name.includes('7')).length
  times.push(performance.now() - start)
}
times.sort((a, b) => a - b) // Посередині відсортованого списку лежить медіана.
console.log('фільтр 1000 рядків, медіана з 200 запусків, мс:', times[100].toFixed(3))
```

```text
фільтр 1000 рядків, медіана з 200 запусків, мс: 0.018
```

Близько двадцяти мікросекунд на тисячу рядків менше за одну мілісекунду приблизно в п'ятдесят разів. Тому для такого
меню хук нічого не дає, а лише додає код. На вашій машині число буде іншим, і машина користувача теж інша, тому
міряйте функцією `console.time` у зібраному застосунку, бо режим розробки працює повільніше й подвоює виклики.

Функція в `useMemo` виконується під час рендеру, тому має бути чистою, як і все інше в рендері. Запит у мережу чи
запис у стан у неї не кладіть. Докладно мемоізацію вивчає фаза 2.

## Реакція на дію людини

Другий випадок виглядає зовсім інакше. Напій можна додати в кошик двома кнопками, а після додавання треба показати
сповіщення. Писати виклик у двох обробниках здається повторенням, тому його кладуть в ефект, який стежить за напоєм:

```tsx
function DrinkByEffect({ drink, addToCart, notify }: { drink: Drink; addToCart: () => void; notify: (t: string) => void }) {
  useEffect(() => {
    if (drink.inCart) {
      notify('Додано: ' + drink.name)
    }
  }, [drink, notify])
  return <button onClick={addToCart}>купити</button>
}
```

Клацання справді показує сповіщення. Тепер уявімо, що кошик пам'ятається між перезавантаженнями сторінки, тому напій
може бути в кошику вже на самому початку. Тест запускає обидва сценарії в `<StrictMode>`, а батько `Shop` тримає напій
у стані:

```tsx
type Drink = { name: string; inCart: boolean }
type CardProps = { drink: Drink; addToCart: () => void; notify: (t: string) => void }
const log: string[] = []
let toasts = 0
const notify = () => {
  toasts++ // Лічильник замість справжнього сповіщення.
}

function Shop({ Card, inCart }: { Card: FC<CardProps>; inCart: boolean }) {
  const [drink, setDrink] = useState({ name: 'лате', inCart })
  return <Card drink={drink} addToCart={() => setDrink({ ...drink, inCart: true })} notify={notify} />
}

function openAndBuy(title: string, Card: FC<CardProps>) {
  toasts = 0
  const opened = render(<StrictMode><Shop Card={Card} inCart={true} /></StrictMode>)
  console.log(`${title} | сторінка відкрита, напій уже в кошику: сповіщень ${toasts}`)
  opened.unmount()

  toasts = 0
  const empty = render(<StrictMode><Shop Card={Card} inCart={false} /></StrictMode>)
  const beforeClick = toasts
  fireEvent.click(screen.getByRole('button', { name: 'купити' }))
  console.log(`${title} | напою немає в кошику: до клацання ${beforeClick}, після клацання ${toasts}`)
  empty.unmount()
}

test('ефект', () => openAndBuy('ефект', DrinkByEffect))
```

```text
ефект | сторінка відкрита, напій уже в кошику: сповіщень 2
ефект | напою немає в кошику: до клацання 0, після клацання 1
```

Людина просто відкрила сторінку, нічого не клацала, а сповіщення «Додано» спливло. Сторінка в `<StrictMode>` дала два
сповіщення, а в збірці буде одне, проте зайве воно в обох випадках, і показуватиметься при кожному оновленні сторінки.
Причина в тому, що ефект бачить лише результат: напій у кошику. Він не знає, що зробила людина і чи зробила вона щось
узагалі.

Виправлення переносить дію туди, де її причину відомо, а спільний код стає звичайною функцією:

```tsx
function DrinkByHandler({ drink, addToCart, notify }: { drink: Drink; addToCart: () => void; notify: (t: string) => void }) {
  function buy() {
    addToCart()
    notify('Додано: ' + drink.name)
  }
  function handleBuyClick() {
    buy()
  }
  function handleCheckoutClick() {
    buy()
    log.push('перехід до каси')
  }
  return (
    <>
      <button onClick={handleBuyClick}>купити</button>
      <button onClick={handleCheckoutClick}>до каси</button>
    </>
  )
}
```

Той самий сценарій тепер отримує новий компонент:

```tsx
test('обробник', () => openAndBuy('обробник', DrinkByHandler))
```

```text
обробник | сторінка відкрита, напій уже в кошику: сповіщень 0
обробник | напою немає в кошику: до клацання 0, після клацання 1
```

Найважливіше тут інше: **лінт про це мовчить**. Ефект не записує стан, а викликає функцію, тому правило
`set-state-in-effect` не спрацьовує, і компілятор теж не має претензій. Цей зайвий ефект ви можете знайти лише очима,
запитавши себе, чому цей код має виконатися. Те саме стосується запиту на реєстрацію, який сторінка React розбирає в
розділі `Sending a POST request`: людина надіслала форму, отже, запит належить обробнику. Звіт про відвідування там
само лишається в ефекті, бо його причина саме показ форми.

Той самий критерій діє для обох випадків. Якщо людина скаже «сповіщення з'явилось, бо я натиснув кнопку», це обробник.
Якщо вона скаже «звіт пішов, бо я побачив форму», це ефект.

## Скидання всього стану

Третій випадок ви знаєте з лекції «Спільний стан і скидання стану», тому тут лише коротке повторення на новому
прикладі й нові межі. Форма столика в кав'ярні має нотатку офіціанта й вкладений компонент чайових, який тримає
власний стан. Коли офіціант переходить до іншого столика, форма має почати спочатку. Спершу варіант з ефектом:

```tsx
function NoteByEffect({ tableId }: { tableId: number }) {
  const [note, setNote] = useState('')
  useEffect(() => {
    setNote('')
  }, [tableId])
  log.push(`рендер: стіл ${tableId}, нотатка «${note}»`)
  return (
    <>
      <input aria-label="нотатка" value={note} onChange={(e) => setNote(e.target.value)} />
      <Tip />
    </>
  )
}
```

Другий варіант ділить компонент на два. Зовнішній компонент передає `tableId` внутрішньому як `key`. Тому код, який
показує форму столика, нічого не знає про ключ і передає `tableId` як звичайний пропс:

```tsx
function TableNote({ tableId }: { tableId: number }) {
  return <Note key={tableId} tableId={tableId} />
}
```

Внутрішній компонент `Note` має той самий вміст, але без ефекту скидання. Натомість у нього ми поставили ефект, який
показує, що станеться зі справжнім підключенням. Сценарій такий: ввести нотатку, клацнути чайові один раз, перейти до
столика 2.

```tsx
const log: string[] = []

function Tip() {
  const [percent, setPercent] = useState(0)
  return <button onClick={() => setPercent(percent + 5)}>чайові {percent}%</button>
}

function Note({ tableId }: { tableId: number }) {
  const [note, setNote] = useState('')
  useEffect(() => {
    log.push('підключено стіл ' + tableId) // Рядок журналу замість справжнього підключення.
    return () => {
      log.push('відключено стіл ' + tableId)
    }
  }, [tableId])
  log.push(`рендер: стіл ${tableId}, нотатка «${note}»`)
  return (
    <>
      <input aria-label="нотатка" value={note} onChange={(e) => setNote(e.target.value)} />
      <Tip />
    </>
  )
}

function moveToTable2(title: string, Form: FC<{ tableId: number }>) {
  const { rerender, unmount } = render(<Form tableId={1} />)
  const oldField = screen.getByLabelText('нотатка')
  fireEvent.change(oldField, { target: { value: 'без цукру' } })
  fireEvent.click(screen.getByRole('button'))
  oldField.focus()
  log.length = 0 // Далі журнал показує лише перехід до іншого столика.
  rerender(<Form tableId={2} />)
  const sameNode = screen.getByLabelText('нотатка') === oldField
  console.log(title + '\n' + log.join('\n'))
  console.log(
    `${title} | кнопка: ${screen.getByRole('button').textContent} | той самий вузол поля: ${sameNode} | у фокусі: ${document.activeElement?.tagName}`,
  )
  unmount()
}

test('столик', () => {
  moveToTable2('ефект', NoteByEffect)
  moveToTable2('key', TableNote)
})
```

```text
ефект
рендер: стіл 2, нотатка «без цукру»
рендер: стіл 2, нотатка «»
ефект | кнопка: чайові 5% | той самий вузол поля: true | у фокусі: INPUT
key
рендер: стіл 2, нотатка «»
відключено стіл 1
підключено стіл 2
key | кнопка: чайові 0% | той самий вузол поля: false | у фокусі: BODY
```

| Що порівнюємо | Ефект | Ключ |
|---------------|-------|------|
| рендерів на перехід | 2 | 1 |
| чи бачив рендер новий стіл зі старою нотаткою | так | ні |
| чайові вкладеного компонента | лишилися від попереднього столика | скинуто |
| вузли документа | ті самі | створено нові |
| фокус у полі | лишився | втрачено |

Перші три рядки є причиною обирати ключ. Два останні є його ціною: React прибирає старий компонент із документа й
створює новий, тому поле втрачає фокус, а всі ефекти всередині проходять прибирання й запуск знову. Це правильна
поведінка для іншого столика. Для випадку, де фокус має лишитися, потрібен інший спосіб.

## Скидання частини стану

Буває, що все скидати не треба. Людина обирає напій у меню, а меню змінилося. Вибір скинути потрібно, а решту стану
залишити. Ось три способи для компонента, який показує обраний напій у вкладеному компоненті `Picked`. Спершу людина
обрала чай, а потім прийшло нове меню, де чай теж є.

```tsx
function PickByEffect({ items }: { items: Item[] }) {
  const [selection, setSelection] = useState<Item | null>(null)
  useEffect(() => {
    setSelection(null)
  }, [items])
  return <><button onClick={() => setSelection(items[1])}>чай</button><Picked item={selection} /></>
}
```

```tsx
function PickDuringRender({ items }: { items: Item[] }) {
  const [selection, setSelection] = useState<Item | null>(null)
  const [prevItems, setPrevItems] = useState(items)
  if (items !== prevItems) {
    setPrevItems(items)
    setSelection(null)
  }
  return <><button onClick={() => setSelection(items[1])}>чай</button><Picked item={selection} /></>
}
```

```tsx
function PickById({ items }: { items: Item[] }) {
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const selection = items.find((item) => item.id === selectedId) ?? null
  return <><button onClick={() => setSelectedId(items[1].id)}>чай</button><Picked item={selection} /></>
}
```

Тест показує меню, клацає чай, а потім передає нове меню й друкує, що за цей час побачив `Picked`:

```tsx
type Item = { id: number; name: string }
const MORNING: Item[] = [{ id: 1, name: 'лате' }, { id: 2, name: 'чай' }]
const EVENING: Item[] = [{ id: 3, name: 'какао' }, { id: 2, name: 'чай' }]
const log: string[] = []

function Picked({ item }: { item: Item | null }) {
  const name = item ? item.name : 'нічого'
  log.push('Picked бачить: ' + name)
  return <p role="status">{name}</p>
}

function changeMenu(title: string, Pick: FC<{ items: Item[] }>) {
  const { rerender, unmount } = render(<Pick items={MORNING} />)
  fireEvent.click(screen.getByRole('button', { name: 'чай' })) // Людина обрала чай.
  log.length = 0
  rerender(<Pick items={EVENING} />) // Прийшло нове меню, у якому чай теж є.
  console.log(`${title} | інше меню: ${log.join(', ')} | на екрані: ${screen.getByRole('status').textContent}`)
  unmount()
}

test('вибір', () => {
  changeMenu('ефект', PickByEffect)
  changeMenu('під час рендеру', PickDuringRender)
  changeMenu('за id', PickById)
})
```

```text
ефект | інше меню: Picked бачить: чай, Picked бачить: нічого | на екрані: нічого
під час рендеру | інше меню: Picked бачить: нічого | на екрані: нічого
за id | інше меню: Picked бачить: чай | на екрані: чай
```

Перший рядок показує знайому проблему: вкладений компонент спершу отримав застарілий вибір із нового меню, а вже потім
правильний.

Другий спосіб викликає `set` просто під час рендеру. Чи не заборонено це? Сторінка React пояснює виняток: якщо
компонент оновлює **власний** стан під час рендеру, React викидає щойно повернену розмітку й одразу викликає компонент
знову, ще до рендеру дітей і запису в документ. Тому `Picked` ніколи не бачить застарілого вибору. Умова `items !==
prevItems` обов'язкова, бо без неї компонент викликав би себе нескінченно, і лінт не пропускає такий запис: правило
`react-hooks/set-state-in-render` друкує `Cannot call setState during render`. З умовою лінт мовчить. Сторінка
попереджає, що такий запис важко читати, і більшості компонентів він не потрібен.

Третій спосіб найкращий, і він не скидає нічого. Стан зберігає лише ідентифікатор, а сам напій обчислюється під час
рендеру. Якщо обраного напою немає в новому меню, `find` не знайде його, і вибір зникне сам. Зверніть увагу, що
поведінка змінилася: чай є в обох меню, тому він лишився обраним. Сторінка React вважає таку поведінку зазвичай
кращою, а для вашої задачі це вирішуєте ви. Якщо вимога інша, це вже зміна поведінки, а не лише прибирання ефекту.

## Поле, обчислене з іншого поля

Четвертий випадок стосується самого стану. Часто в стан кладуть копію значення, яке вже лежить в іншому полі. Така
копія називається **похідним значенням**, бо його можна вивести з іншого. Адміністратор кав'ярні змінює ціни в меню, а
поруч показано обраний напій. Обраний напій лежить у стані окремим об'єктом:

```tsx
function PriceCopy() {
  const [items, setItems] = useState(HOT)
  const [selected, setSelected] = useState(HOT[0])
  log.push('рендер')
  function raise() {
    setItems(items.map((i) => (i.id === 1 ? { ...i, price: i.price + 10 } : i)))
  }
  return <><button onClick={raise}>дорожче</button><button onClick={() => setSelected(items[0])}>обрати</button><p role="status">{selected.name}: {selected.price} грн</p></>
}
```

Спочатку лате коштує 80 гривень, а кнопка «дорожче» додає 10. Копія не оновлюється, і людина бачить стару ціну. Перша
думка полагодити це ефектом, який оновлює копію щоразу, коли змінилося меню. Така думка лише лікує наслідок, а причина
лишається. Правильний варіант зберігає ідентифікатор, а об'єкт знаходить під час рендеру. Ось обидва варіанти й тест,
який один раз клацає «дорожче»:

```tsx
function PriceCopyEffect() {
  const [items, setItems] = useState(HOT)
  const [selected, setSelected] = useState(HOT[0])
  useEffect(() => {
    // Ефект шукає в новому меню той самий напій і оновлює копію.
    setSelected((old) => items.find((i) => i.id === old.id) ?? old)
  }, [items])
  log.push('рендер')
  function raise() {
    setItems(items.map((i) => (i.id === 1 ? { ...i, price: i.price + 10 } : i)))
  }
  return <><button onClick={raise}>дорожче</button><button onClick={() => setSelected(items[0])}>обрати</button><p role="status">{selected.name}: {selected.price} грн</p></>
}

function PriceById() {
  const [items, setItems] = useState(HOT)
  const [selectedId, setSelectedId] = useState(HOT[0].id)
  const selected = items.find((i) => i.id === selectedId)! // Об'єкт завжди береться з поточного меню.
  log.push('рендер')
  function raise() {
    setItems(items.map((i) => (i.id === 1 ? { ...i, price: i.price + 10 } : i)))
  }
  return <><button onClick={raise}>дорожче</button><button onClick={() => setSelectedId(items[0].id)}>обрати</button><p role="status">{selected.name}: {selected.price} грн</p></>
}

const HOT = [{ id: 1, name: 'лате', price: 80 }, { id: 2, name: 'чай', price: 50 }]
const log: string[] = []

function raiseOnce(title: string, Menu: FC) {
  const { unmount } = render(<Menu />)
  log.length = 0 // Рахуємо лише рендери після клацання.
  fireEvent.click(screen.getByRole('button', { name: 'дорожче' }))
  console.log(`${title} | на екрані ${screen.getByRole('status').textContent} | рендерів на одне клацання: ${log.length}`)
  unmount()
}

test('ціни', () => {
  raiseOnce('копія в стані', PriceCopy)
  raiseOnce('копія й ефект', PriceCopyEffect)
  raiseOnce('id і обчислення', PriceById)
})
```

```text
копія в стані | на екрані лате: 80 грн | рендерів на одне клацання: 1
копія й ефект | на екрані лате: 90 грн | рендерів на одне клацання: 2
id і обчислення | на екрані лате: 90 грн | рендерів на одне клацання: 1
```

Лекція «Структура стану» докладно пояснила таке дублювання. Ефект лише додає до нього зайвий рендер. Шукайте в своєму
коді такі пари: якщо значення в стані можна вирахувати з іншого, то в стані зайве.

## Ланцюг ефектів

Тепер подивимося, що стається, коли таких ефектів кілька й кожен запускає наступний. Це пастка дня. Картка постійного
гостя збирає штампи: лате дає штамп, вода не дає, три штампи дають новий рівень, а рівень 2 робить картку золотою.
Кожне правило лягло в окремий ефект:

```tsx
function StampsChain() {
  parentRenders++
  const [cup, setCup] = useState<Cup | null>(null)
  const [stamps, setStamps] = useState(0)
  const [level, setLevel] = useState(1)
  const [isGold, setIsGold] = useState(false)

  useEffect(() => {
    if (cup !== null && cup.counts) {
      setStamps((s) => s + 1)
    }
  }, [cup])

  useEffect(() => {
    if (stamps === 3) {
      setStamps(0)
      setLevel((l) => l + 1)
    }
  }, [stamps])

  useEffect(() => {
    if (level === 2) {
      setIsGold(true)
    }
  }, [level])

  return (
    <>
      <button onClick={() => setCup({ ...LATTE_CUP })}>лате</button>
      <button onClick={() => setCup({ ...WATER_CUP })}>вода</button>
      <button onClick={() => setCup({ ...LATTE_CUP })}>показати минулу чашку</button>
      <Receipt text={`штампів ${stamps}, рівень ${level}, золота картка: ${isGold}`} />
    </>
  )
}
```

Той самий код без ланцюга обчислює все в обробнику, а золотий статус випливає з рівня:

```tsx
function StampsHandler() {
  parentRenders++
  const [, setCup] = useState<Cup | null>(null)
  const [stamps, setStamps] = useState(0)
  const [level, setLevel] = useState(1)
  const isGold = level >= 2

  function handleCup(next: Cup) {
    setCup(next)
    if (!next.counts) return
    if (stamps + 1 === 3) {
      setStamps(0)
      setLevel(level + 1)
    } else {
      setStamps(stamps + 1)
    }
  }

  return (
    <>
      <button onClick={() => handleCup({ ...LATTE_CUP })}>лате</button>
      <button onClick={() => handleCup({ ...WATER_CUP })}>вода</button>
      <button onClick={() => setCup({ ...LATTE_CUP })}>показати минулу чашку</button>
      <Receipt text={`штампів ${stamps}, рівень ${level}, золота картка: ${isGold}`} />
    </>
  )
}
```

Гість купує три лате. Лічильники рахують виклики батька й вкладеного чека:

```tsx
type Cup = { name: string; counts: boolean }
const LATTE_CUP: Cup = { name: 'лате', counts: true }
const WATER_CUP: Cup = { name: 'вода', counts: false }
let parentRenders = 0
let receiptRenders = 0

function Receipt({ text }: { text: string }) {
  receiptRenders++
  return <p role="status">{text}</p>
}

function threeCups(title: string, Card: FC) {
  const { unmount } = render(<Card />)
  for (let cup = 1; cup <= 3; cup++) {
    parentRenders = 0
    receiptRenders = 0
    fireEvent.click(screen.getByRole('button', { name: 'лате' }))
    console.log(`${title} | чашка ${cup}: рендерів батька ${parentRenders}, чека ${receiptRenders} | ${screen.getByRole('status').textContent}`)
  }
  unmount()
}

test('три чашки', () => {
  threeCups('ланцюг', StampsChain)
  threeCups('обробник', StampsHandler)
})
```

```text
ланцюг | чашка 1: рендерів батька 2, чека 2 | штампів 1, рівень 1, золота картка: false
ланцюг | чашка 2: рендерів батька 2, чека 2 | штампів 2, рівень 1, золота картка: false
ланцюг | чашка 3: рендерів батька 4, чека 4 | штампів 0, рівень 2, золота картка: true
обробник | чашка 1: рендерів батька 1, чека 1 | штампів 1, рівень 1, золота картка: false
обробник | чашка 2: рендерів батька 1, чека 1 | штампів 2, рівень 1, золота картка: false
обробник | чашка 3: рендерів батька 1, чека 1 | штампів 0, рівень 2, золота картка: true
```

Простежимо третю чашку в ланцюгу.

| Рендер | Що його спричинило | Що бачить компонент | Який ефект спрацював |
|--------|--------------------|---------------------|----------------------|
| перший | клацання, `setCup` | штампів 2 | ефект чашки додає штамп |
| другий | `setStamps` | штампів 3 | ефект штампів скидає їх і підвищує рівень |
| третій | `setStamps`, `setLevel` | штампів 0, рівень 2, картка ще не золота | ефект рівня ставить золотий статус |
| четвертий | `setIsGold` | картка золота | нічого |

Кожна ланка додала один рендер батька й усіх його дітей. У чеку другий і третій рендери показували проміжний стан,
якого в задачі не існує, наприклад рівень 2 зі звичайною карткою. Це перша проблема ланцюга, і вона є проблемою
швидкодії.

Друга проблема важливіша. Сторінка React пропонує уявити нову вимогу: перегляд історії. Кнопка «показати минулу чашку»
лише показує минулу покупку, тобто змінює `cup` на старе значення. Тест знову купує три лате, а потім клацає цю
кнопку:

```tsx
function viewPastCup(title: string, Card: FC) {
  const { unmount } = render(<Card />)
  for (let cup = 1; cup <= 3; cup++) {
    fireEvent.click(screen.getByRole('button', { name: 'лате' }))
  }
  fireEvent.click(screen.getByRole('button', { name: 'показати минулу чашку' }))
  console.log(`${title} | перегляд минулої чашки: ${screen.getByRole('status').textContent}`)
  unmount()
}

test('перегляд', () => {
  viewPastCup('ланцюг', StampsChain)
  viewPastCup('обробник', StampsHandler)
})
```

```text
ланцюг | перегляд минулої чашки: штампів 1, рівень 2, золота картка: true
обробник | перегляд минулої чашки: штампів 0, рівень 2, золота картка: true
```

Перегляд у ланцюгу подарував гостю штамп. Ефект не знає, чому змінилася чашка, бо він бачить лише нове значення, тому
застосовує правило покупки. В обробнику правило виконується лише під час покупки, тому перегляд нічого не ламає. Отже,
ланцюг ламається не тоді, коли ви його пишете, а коли вимоги змінюються.

Обробник у варіанті без ланцюга зважає на те, що стан є знімком. Лекція «Рендер, коміт і знімок стану» пояснила, що
після `setStamps` змінна `stamps` у цьому обробнику лишається старою, тому умова пише `stamps + 1`, а не читає змінну
після запису.

Є й законний ланцюг. Сторінка React наводить форму, у якій варіанти другого списку залежать від вибору в першому й
приходять із мережі. Там кожен ефект синхронізується з мережею, тому вони й мають бути ефектами.

## Як повідомити батька

Перемикач тримає власний стан, а батько хоче знати про зміну. Спокуса знову в тому, щоб викликати функцію батька в
ефекті:

```tsx
function ToggleEffect({ onChange }: { onChange: (on: boolean) => void }) {
  togglePasses++
  const [isOn, setIsOn] = useState(false)
  useEffect(() => {
    onChange(isOn)
  }, [isOn, onChange])
  return <button onClick={() => setIsOn(!isOn)}>{isOn ? 'увімкнено' : 'вимкнено'}</button>
}
```

Правильніше оновити обидва стани в тому самому обробнику, бо React збирає оновлення однієї події разом:

```tsx
function ToggleHandler({ onChange }: { onChange: (on: boolean) => void }) {
  togglePasses++
  const [isOn, setIsOn] = useState(false)
  function updateToggle(next: boolean) {
    setIsOn(next)
    onChange(next)
  }
  return <button onClick={() => updateToggle(!isOn)}>{isOn ? 'увімкнено' : 'вимкнено'}</button>
}
```

Третій спосіб найпростіший: перемикач узагалі не тримає стану, а отримує `isOn` від батька, як навчила лекція
«Спільний стан і скидання стану». Ось цей варіант і тест, який клацає перемикач один раз, а лічильники рахують виклики
батька й перемикача:

```tsx
function ToggleControlled({ isOn, onChange }: { isOn: boolean; onChange: (on: boolean) => void }) {
  togglePasses++
  return <button onClick={() => onChange(!isOn)}>{isOn ? 'увімкнено' : 'вимкнено'}</button>
}

let togglePasses = 0
let parentPasses = 0

function ParentKnows({ Toggle }: { Toggle: FC<{ onChange: (on: boolean) => void }> }) {
  parentPasses++
  const [knows, setKnows] = useState(false)
  return <><Toggle onChange={setKnows} /><p role="status">{String(knows)}</p></>
}

function ParentOwns() {
  parentPasses++
  const [isOn, setIsOn] = useState(false)
  return <><ToggleControlled isOn={isOn} onChange={setIsOn} /><p role="status">{String(isOn)}</p></>
}

function oneClick(title: string, page: ReactNode) {
  const { unmount } = render(page)
  parentPasses = 0
  togglePasses = 0
  fireEvent.click(screen.getByRole('button'))
  console.log(`${title} | одне клацання: батько ${parentPasses}, перемикач ${togglePasses} | батько знає: ${screen.getByRole('status').textContent}`)
  unmount()
}

test('перемикач', () => {
  oneClick('батьку, ефект', <ParentKnows Toggle={ToggleEffect} />)
  oneClick('батьку, обробник', <ParentKnows Toggle={ToggleHandler} />)
  oneClick('батьку, стан у батька', <ParentOwns />)
})
```

```text
батьку, ефект | одне клацання: батько 1, перемикач 2 | батько знає: true
батьку, обробник | одне клацання: батько 1, перемикач 1 | батько знає: true
батьку, стан у батька | одне клацання: батько 1, перемикач 1 | батько знає: true
```

Лінт тут теж мовчить, бо ефект викликає пропс, а не функцію `set`. Схожий випадок є зворотним: дитина завантажила дані
й передає їх батькові в ефекті. Тоді дані йдуть угору, і коли на екрані щось неправильно, ви не зможете знайти
джерело, рухаючись згори вниз. Сторінка React радить завантажувати дані в батька й передавати їх униз пропсом.

## Запуск застосунку

Перевірка токена входу має виконатися один раз за запуск застосунку. Покласти її в ефект кореневого компонента
здається природно, але перевірка `<StrictMode>` запустить ефект двічі, а токен може бути одноразовим. Сторінка React
радить таку перевірку не прибирати, а поставити поза компонентом або обгородити змінною модуля:

```tsx
let didInit = false
function AppOnce() {
  useEffect(() => {
    if (!didInit) {
      didInit = true
      checkToken()
    }
  }, [])
  return <h1>Кав'ярня</h1>
}
```

Поруч стоїть звичайний ефект без змінної. Функція `checkToken` тут лише рахує виклики:

```tsx
let checks = 0
function checkToken() {
  checks++
}

function AppPlain() {
  useEffect(() => {
    checkToken()
  }, [])
  return <h1>Кав'ярня</h1>
}

function start(title: string, App: FC) {
  checks = 0
  const { unmount } = render(<StrictMode><App /></StrictMode>)
  console.log(`${title} | перевірок токена: ${checks}`)
  unmount()
}

test('запуск', () => {
  start('запуск, звичайний ефект, StrictMode', AppPlain)
  start('запуск, змінна didInit, StrictMode', AppOnce)
})
```

```text
запуск, звичайний ефект, StrictMode | перевірок токена: 2
запуск, змінна didInit, StrictMode | перевірок токена: 1
```

Це не суперечить попередній лекції про ref-запобіжник. Там компонент мав з'єднання, яке треба було закривати, а тут
дія за визначенням належить усьому запуску застосунку, а не показу компонента.

## Сховище поза React

Значення може жити поза React, наприклад статус `navigator.onLine` у браузері, а компонент має оновлюватися, коли воно
змінюється. Це зовнішня система, тому ефект тут працює. Проте сторінка React радить спеціальний хук
`useSyncExternalStore`, який приймає функцію підписки й функцію читання значення:

```tsx
function useOnline() {
  return useSyncExternalStore(subscribe, () => navigator.onLine)
}

let subscriptions = 0 // Лічильник показує, скільки підписок діє зараз.

function subscribe(onChange: () => void) {
  subscriptions++
  window.addEventListener('online', onChange)
  window.addEventListener('offline', onChange)
  return () => {
    subscriptions--
    window.removeEventListener('online', onChange)
    window.removeEventListener('offline', onChange)
  }
}

function Status() {
  return <p role="status">{useOnline() ? 'у мережі' : 'без мережі'}</p>
}

test('сховище', () => {
  let online = true
  Object.defineProperty(navigator, 'onLine', { configurable: true, get: () => online })
  const { unmount } = render(<Status />)
  const first = screen.getByRole('status').textContent
  act(() => {
    online = false
    window.dispatchEvent(new Event('offline')) // Подію викликаємо вручну, бо в jsdom немає мережі.
  })
  console.log(`сховище | спочатку: ${first} | після події: ${screen.getByRole('status').textContent} | підписок: ${subscriptions}`)
  unmount()
  console.log(`сховище | компонент зник, підписок: ${subscriptions}`)
})
```

```text
сховище | спочатку: у мережі | після події: без мережі | підписок: 1
сховище | компонент зник, підписок: 0
```

Функція `subscribe` підписується на події `online` та `offline` і повертає функцію відписки. Її оголошено поза
компонентом, бо React підписується знову, якщо отримав іншу функцію. Кількість підписок показує, що React сам викликав
і підписку, і відписку. Подію `offline` у цьому досліді ми викликали вручну й підставили значення `navigator.onLine`,
бо jsdom не має справжньої мережі.

## Що лишається ефектом

Прибирати все не треба. Ось що лишається, і причина завжди та сама: зовнішня система.

- **Завантаження даних.** Сторінка React каже прямо: цей запит не треба переносити в обробник, хоч він і стоїть поруч
  із вводом. Причина запиту не в натисканні клавіші, бо рядок пошуку міг прийти з адреси сторінки чи кнопки «назад».
  Поки компонент на екрані, результати мають відповідати запиту, а це синхронізація. Прибирання проти гонки показала
  попередня лекція, і забувати його не можна.
- **Підключення й підписки**, які треба закрити: табло, подія вікна.
- **Таймери**, які мають працювати, поки компонент на екрані.
- **Сторонні віджети**, якими React не керує: карта, плеєр, діалог браузера.
- **Звіт про відвідування**, бо його причина саме показ.

Ефекти з днів «Чистота й дерево» та «Синхронізація ефектами» саме такі, і прибирати їх не треба. Прибирання потрібного
ефекту зламає поведінку, яку перевірка дня просить зберегти.

## Що бачить лінт

Перевірка дня вимагає, щоб лінт не видавав попереджень правила `set-state-in-effect`. Сторінка правила каже, що воно
спрацьовує на синхронному виклику `set` у тілі ефекту. Ми запустили ESLint на окремому файлі з кожним записом, щоб
побачити межі цього правила. Коментар над кожним компонентом каже, який запис він перевіряє:

```tsx
// src/lint-cases.tsx
import { useEffect, useLayoutEffect, useRef, useState } from 'react'

// set прямо в тілі ефекту
export function DirectSet({ value }: { value: number }) {
  const [copy, setCopy] = useState(0)
  useEffect(() => {
    setCopy(value)
  }, [value])
  return <p>{copy}</p>
}

// set усередині if в ефекті
export function SetInIf({ value }: { value: number }) {
  const [copy, setCopy] = useState(0)
  useEffect(() => {
    if (value > 0) {
      setCopy(value)
    }
  }, [value])
  return <p>{copy}</p>
}

// set у локальній функції, яку ефект одразу викликає
export function SetInLocal({ value }: { value: number }) {
  const [copy, setCopy] = useState(0)
  useEffect(() => {
    function update() {
      setCopy(value)
    }
    update()
  }, [value])
  return <p>{copy}</p>
}

// сповіщення за значенням стану
export function NotifyOnState({ notify }: { notify: (t: string) => void }) {
  const [paid, setPaid] = useState(false)
  useEffect(() => {
    if (paid) {
      notify('Оплачено')
    }
  }, [paid, notify])
  return <button onClick={() => setPaid(true)}>оплатити</button>
}

// виклик пропса onChange
export function CallProp({ onChange }: { onChange: (on: boolean) => void }) {
  const [on, setOn] = useState(false)
  useEffect(() => {
    onChange(on)
  }, [on, onChange])
  return <button onClick={() => setOn(!on)}>перемкнути</button>
}

// set у .then після запиту
export function SetInThen({ url }: { url: string }) {
  const [text, setText] = useState('')
  useEffect(() => {
    fetch(url).then((r) => r.text()).then((body) => setText(body))
  }, [url])
  return <p>{text}</p>
}

// set у функції таймера
export function SetInTimer() {
  const [ticks, setTicks] = useState(0)
  useEffect(() => {
    const id = setInterval(() => setTicks((t) => t + 1), 1000)
    return () => clearInterval(id)
  }, [])
  return <p>{ticks}</p>
}

// set зі значенням, виміряним через ref у useLayoutEffect
export function Measure() {
  const box = useRef<HTMLDivElement>(null)
  const [height, setHeight] = useState(0)
  useLayoutEffect(() => {
    const rect = box.current!.getBoundingClientRect()
    setHeight(rect.height)
  }, [])
  return <div ref={box}>{height}</div>
}

// set під час рендеру за умовою
export function RenderWithCondition({ items }: { items: string[] }) {
  const [prevItems, setPrevItems] = useState(items)
  const [picked, setPicked] = useState('')
  if (items !== prevItems) {
    setPrevItems(items)
    setPicked('')
  }
  return <button onClick={() => setPicked(items[0])}>{picked}</button>
}

// set під час рендеру без умови
export function RenderNoCondition({ value }: { value: number }) {
  const [copy, setCopy] = useState(0)
  setCopy(value)
  return <p>{copy}</p>
}
```

Звичайний вивід ESLint тут дуже довгий, бо кожне повідомлення має кілька абзаців пояснення. Тому ми запустили ESLint
із маленького файлу `lint-report.mjs`, який лежить у корені проєкту й запускається командою `node lint-report.mjs`.
Цей файл друкує лише номер рядка, правило й перший рядок повідомлення:

```js
import { ESLint } from 'eslint'

const [result] = await new ESLint().lintFiles(['src/lint-cases.tsx'])
for (const m of result.messages) {
  console.log(`${m.line}: ${m.ruleId} | ${m.message.split('\n')[0]}`)
}
```

```text
8: react-hooks/set-state-in-effect | Error: Calling setState synchronously within an effect can trigger cascading renders
18: react-hooks/set-state-in-effect | Error: Calling setState synchronously within an effect can trigger cascading renders
100: react-hooks/set-state-in-render | Error: Cannot call setState during render
```

Рядок 8 лежить у `DirectSet`, рядок 18 у `SetInIf`, а рядок 100 у `RenderNoCondition`. Решта сім компонентів не дали
жодного повідомлення. Таблиця зводить цей вивід разом, а останній стовпець уже не є виводом лінту, а нашою оцінкою за
критерієм цієї лекції:

| Запис | Що каже лінт | Чи зайвий ефект |
|-------|--------------|-----------------|
| `set` прямо в тілі ефекту | помилка `set-state-in-effect` | майже завжди |
| `set` усередині `if` в ефекті | помилка `set-state-in-effect` | майже завжди |
| `set` у локальній функції, яку ефект одразу викликає | мовчить | так, правило цього не простежило |
| сповіщення за значенням стану | мовчить | так, це реакція на подію |
| виклик пропса `onChange` | мовчить | так, це реакція на подію |
| `set` у `.then` після запиту | мовчить | ні, дозволено |
| `set` у функції таймера | мовчить | ні, дозволено |
| `set` зі значенням, виміряним через ref у `useLayoutEffect` | мовчить | ні, дозволено сторінкою правила |
| `set` під час рендеру за умовою | мовчить | дозволено, але рідко потрібно |
| `set` під час рендеру без умови | помилка `Cannot call setState during render` | помилка |

Отже, чистий лінт є необхідною, але не достатньою умовою. Він не знає причини, через яку виконується ваш код, тому
реакцію на клік в ефекті доведеться знайти самостійно. Запис `// eslint-disable-next-line` прибирає повідомлення, але
не помилку.

## Як рахувати ефекти

Практика просить записати два числа: скільки ефектів було й скільки стало. Для цього підходить пошук рядка, але
результат доведеться прочитати. Ось невеликий зразок проєкту кав'ярні з трьох файлів. Перший файл,
`shop/src/Menu.tsx`, завантажує меню, а коментар у ньому залишився від старого коду:

```tsx
import { useEffect, useState } from 'react'
// Раніше тут стояв useEffect(() => ...) для підрахунку, тепер підрахунок іде під час рендеру.
export function Menu() {
  const [items, setItems] = useState<string[]>([])
  useEffect(() => {
    fetch('/api/menu').then((r) => r.json()).then(setItems)
  }, [])
  return <ul>{items.map((name) => <li key={name}>{name}</li>)}</ul>
}
```

Другий файл, `shop/src/cart/Cart.tsx`, обчислює суму ефектом:

```tsx
import { useEffect, useState } from 'react'
export function Cart({ prices }: { prices: number[] }) {
  const [total, setTotal] = useState(0)
  useEffect(() => {
    setTotal(prices.reduce((sum, price) => sum + price, 0))
  }, [prices])
  return <p>{total}</p>
}
```

Третій файл, `shop/src/cart/Cart.test.tsx`, належить тестам:

```tsx
import { useEffect } from 'react'
export function Probe() { useEffect(() => {}, []); return null }
```

Такий пошук друкує кожен рядок, де стоїть `useEffect(`. Порядок файлів у вашому виводі може бути іншим, бо він
залежить від файлової системи:

```bash
grep -rn "useEffect(" shop/src --include="*.tsx"
```

```text
shop/src/cart/Cart.test.tsx:2:export function Probe() { useEffect(() => {}, []); return null }
shop/src/cart/Cart.tsx:4:  useEffect(() => {
shop/src/Menu.tsx:2:// Раніше тут стояв useEffect(() => ...) для підрахунку, тепер підрахунок іде під час рендеру.
shop/src/Menu.tsx:5:  useEffect(() => {
```

Команда знайшла чотири рядки, але справжніх ефектів застосунку лише два. Один рядок є коментарем, а інший лежить у
файлі тесту. Тому не вірте числу сліпо: перегляньте кожен рядок і вирішіть, що рахувати. У нашому прикладі ефект у
`Menu.tsx` завантажує дані й лишається, а ефект у `Cart.tsx` обчислює суму, і його треба прибрати.

Для кожного знайденого ефекту поставте ті самі запитання: яка тут зовнішня система, і чому цей код має виконатися?
Перш ніж прибирати ефект, запустіть тести й запишіть, що вони зелені. Після прибирання тести мають дати той самий
результат. Вони не помітять зайвих рендерів, зате зловлять зміну поведінки.

## Ефекти, зайві рендери й рецепт

Практика цього плану йде за рецептом книжки How to Design Programs. Рецепт вимагає прикладів із відомим результатом, а
вони можливі для функцій, які обчислюють значення. Сьогоднішня тема допомагає рецепту: значення, яке обчислював ефект,
стає звичайною чистою функцією. Для неї легко написати приклади, бо сума позицій лате й чаю дорівнює 210, і це можна
записати рівністю, без компонента й без таймерів. Обробник події теж зручно розбити так: нове значення обчислює чиста
функція, а обробник лише викликає `set`. Редюсер, який вивчала лекція «Редюсер», побудовано на тій самій думці.

## Типові хибні уявлення

**«Ефект потрібен, щоб компонент оновився, коли змінився пропс».** Компонент і так викликається знову, коли змінюються
пропси, тому обчислення в тілі виконається саме. Ефект лише додає другий рендер.

**«Значення в стані й ефект, який його оновлює, це нормальне розділення логіки».** Це два місця для одного факту. Вони
можуть розійтися, і на кадрі можна побачити проміжний результат: у нашому досліді це сталося приблизно в кожній третій
спробі.

**«`useMemo` треба ставити на будь-яке обчислення».** Хук сам додає код і порівняння. Фільтр тисячі рядків зайняв у
нас близько двадцяти мікросекунд, тому там нічого економити. Міряйте.

**«Ефект зручніший для спільної логіки двох кнопок».** Спільну логіку виносять у звичайну функцію. Ефект не знає, що
натиснула людина, і спрацює також під час відкриття сторінки.

**«Лінт чистий, отже, зайвих ефектів немає».** Правило бачить лише запис стану прямо в ефекті. Сповіщення, виклик
пропса й запис через локальну функцію воно пропускає.

**«Тести зелені, отже, ефект не шкодить».** Обидва варіанти кошика пройшли той самий тест, хоча один робив зайвий
рендер і показував проміжну суму.

**«`key` є дешевим способом скинути що завгодно».** Ключ створює нові вузли документа. Поле втрачає фокус, а вкладені
ефекти проходять прибирання й запуск. Для іншої сутності це правильно, а для незначної зміни це забагато.

**«Якщо запит пов'язаний з уводом, його місце в обробнику».** Для пошуку це не так, бо результати мають відповідати
рядку, звідки б той не прийшов. Це ефект із прибиранням.

**«Усі ефекти погані».** Ефект є єдиним правильним місцем для синхронізації із зовнішньою системою. Зайвий ефект той,
у якого цієї системи немає.

## Як це проявиться далі в React

- **Тема «Життєвий цикл ефекту й події поза ним».** Запитання «чому цей код виконується» там стає прийомом: одна
  частина логіки є подією, а інша синхронізацією, і їх можна розділити навіть усередині ефекту.
- **Тема «Залежності ефекту й власні хуки».** Чим менше зайвих ефектів, тим менше списків залежностей. Там ви також
  винесете ефект у власний хук, і сторінка React радить цей шлях для завантаження даних.
- **Фаза 2, мемоізація.** Там `useMemo` повернеться разом із профайлером, і ви заміряєте його на справжньому
  компоненті.
- **Фаза 3, дані.** Навіть законний ефект завантаження там поступиться бібліотеці.

## Перевірте себе

**1. Компонент тримає `fullName` у стані й оновлює його ефектом, коли змінюються `first` та `last`. Що конкретно
відбувається після зміни `first` і чому це гірше за обчислення в тілі?**

<details><summary>Відповідь</summary>

React викликає компонент із новим `first` і старим `fullName`, записує результат у документ, запускає ефект, той
просить новий рендер, і лише другий рендер дає правильне значення. Це два рендери замість одного й момент, коли
документ показує неузгоджені дані. Лінт повідомляє про такий запис правилом `set-state-in-effect`. Обчислення в тілі
дає один рендер і завжди узгоджене значення.

</details>

**2. Коли варто загорнути обчислення в `useMemo`, а коли ні?**

<details><summary>Відповідь</summary>

Коли заміряно, що обчислення дороге: сторінка React називає межу приблизно в одну мілісекунду на дію, і міряти треба
на зібраному застосунку. Для фільтра тисячі рядків наш замір дав близько двадцяти мікросекунд, тому хук нічого не дає.
Функція в `useMemo` має бути чистою, бо виконується під час рендеру.

</details>

**3. Ефект показує сповіщення, коли `order.isPaid` стає `true`. Яку помилку побачить людина після перезавантаження
сторінки вже оплаченого замовлення? Чи скаже про це лінт?**

<details><summary>Відповідь</summary>

Сповіщення спливе без жодної дії людини, бо значення вже `true` під час першого запуску ефекту. Лінт мовчить, бо ефект
не записує стан. Сповіщення треба перенести в обробник, у якому людина оплачує замовлення.

</details>

**4. Чим `key` кращий за ефект, який очищує нотатку при зміні столика, і чого він коштує?**

<details><summary>Відповідь</summary>

Ключ скидає весь стан усього піддерева, зокрема вкладених компонентів, і дає один рендер без проміжного стану. Ефект
очищує лише перелічене, а вкладені чайові лишилися від минулого столика. Коштує ключ нових вузлів документа, тому поле
втрачає фокус, а вкладені ефекти запускаються заново.

</details>

**5. Чому запис у стан під час рендеру за умовою `items !== prevItems` не дає застарілого показу в дітей, а такий
самий запис в ефекті дає?**

<details><summary>Відповідь</summary>

Під час рендеру React викидає повернену розмітку й одразу викликає компонент знову, ще до рендеру дітей і запису в
документ. Ефект запускається після коміту, тому діти вже отримали застаріле значення. Без умови запис під час рендеру
дав би нескінченний цикл, і лінт такий запис не пропускає.

</details>

**6. Третя чашка кави в ланцюгу ефектів дала чотири рендери. Звідки вони, і чому друга проблема ланцюга важливіша за
швидкодію?**

<details><summary>Відповідь</summary>

Перший рендер дає `setCup`, другий дає `setStamps` з першого ефекту, третій дає скидання штампів і новий рівень,
четвертий дає `setIsGold`. Важливіше те, що ефект реагує на значення, а не на причину, тому перегляд минулої чашки в
нашому досліді подарував гостю штамп. Така помилка з'являється, коли додається нова вимога.

</details>

**7. Лінт чистий, тести зелені. Як знайти, що ще лишилося зайвим?**

<details><summary>Відповідь</summary>

Прочитати кожен ефект і спитати, яка тут зовнішня система й чому цей код має виконатися. Лінт бачить лише запис стану
в тілі ефекту, а тести не бачать зайвих рендерів. Рендери можна порахувати лічильником у тілі компонента на час
перевірки.

</details>

**8. Пошук дає запит під час введення рядка в ефекті. Колега пропонує перенести його в обробник `onChange` за
правилами цієї лекції. Що ви скажете?**

<details><summary>Відповідь</summary>

Це той випадок, коли ефект потрібен. Результати мають відповідати рядку незалежно від того, як той з'явився: з адреси
сторінки чи кнопкою «назад». Це синхронізація з мережею, і ефект потребує прибирання проти гонки.

</details>

## Словничок лекції

| Слово | Що означає |
|-------|------------|
| зайвий ефект | ефект, у задачі якого немає системи поза React |
| похідне значення | значення, яке можна обчислити з пропсів чи іншого стану, тому зберігати його не треба |
| мемоізація | запам'ятовування результату обчислення, поки вхідні значення не змінилися |
| `useMemo` | хук, який мемоізує результат функції під час рендеру |
| ланцюг ефектів | кілька ефектів, у яких кожен записує стан, на який реагує наступний |
| `set-state-in-effect` | правило лінту, яке повідомляє про синхронний запис стану в тілі ефекту |
| `set-state-in-render` | правило лінту, яке повідомляє про запис стану під час рендеру без умови |
| `useSyncExternalStore` | хук для підписки на сховище поза React |

## Що читати далі

- [Розбір читання до цього дня](../reading/f1-d17-reading.md): що саме написано в матеріалах дня й де що шукати.
- You Might Not Need an Effect: глава React, яку ви читаєте сьогодні.
- set-state-in-effect: сторінка правила лінту.
- useMemo: довідник про мемоізацію.
- useSyncExternalStore: довідник про підписку на сховище.

---

Лекцію написано для цього плану. Вона спирається на документацію React і коротко згадує рецепт із книжки How to Design
Programs. Усе переказано своїми словами, а права на ці тексти належать їхнім авторам.
