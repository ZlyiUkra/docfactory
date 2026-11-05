# Лекція. Фаза 1, день 15. Ref

Досі все, що компонент мав пам'ятати, лежало в стані. Ця лекція пояснює, що робити зі значенням, яке компонент має
пам'ятати, але екран від нього не залежить: як працює такий тип пам'яті, чому його не можна читати під час рендеру, як
дістати через нього елемент сторінки й чому таймер може пережити компонент. Читання займе близько 45 хвилин.

Приклади запущено на React 19.3 у Vitest під jsdom, тобто в імітації браузера всередині Node. Вивід під прикладами
справжній. Типи перевірено компілятором `tsc` версії 6.0, а лінт перевірено ESLint із тим самим набором правил
`react-hooks`, що й у проєкті `spa`. У справжньому браузері приклади цієї лекції не запускалися, тому біля кожного
твердження про браузер сказано, на чому воно тримається.

У справжньому браузері запущено інші матеріали цього дня: частину дослідів теорії й частину практики. Для них узято
Chrome без вікна, тобто браузер Chrome, який працює без вікна на екрані, а керує ним програма. Теорія й практика
кажуть про такий запуск там, де його зроблено.

Практика дня просить зробити фокус на полі форми, прокручування до нового елемента списку, секундомір і лічильник
кліків. Щоб не показувати готового розв'язку, лекція бере інші об'єкти: кнопку скасування листа, поле промокоду,
запитання з відповідями й зміст статті.

**Після лекції ви зможете пояснити:**

- чому звичайна змінна компонента не може зберігати ідентифікатор таймера;
- чим ref відрізняється від стану і за яким запитанням обирати між ними;
- чому значення в ref змінюється одразу, а значення стану чекає наступного рендеру;
- чому читання й запис `ref.current` під час рендеру роблять компонент непередбачуваним і де є виняток;
- у який момент React кладе елемент у `ref.current` і чому там буває `null`;
- чому після `set` елемента, який мав з'явитися, ще немає;
- як отримати багато елементів через функцію в атрибуті `ref` і чому така функція інколи спрацьовує на кожному
  рендері;
- як передати ref власному компоненту в React 19;
- чому не можна вилучати вручну те, чим керує React;
- що відбувається з таймером після повторного клацання й після зникнення компонента.

## Лист, який не вдається скасувати

Ви робите кнопку надсилання листа. Лист іде через три секунди, а до того часу кнопка «скасувати» може це зупинити.
Браузерна функція `setTimeout` запускає таймер і повертає його **ідентифікатор**, тобто значення, за яким
`clearTimeout` пізніше знайде саме цей таймер. Отже, ідентифікатор треба десь зберегти між клацанням «надіслати» й
клацанням «скасувати». Спершу кладемо його у звичайну змінну:

```tsx
function WithLet() {
  const [status, setStatus] = useState('чернетка')
  let timerId: ReturnType<typeof setTimeout> | null = null

  function send() {
    setStatus('надсилається')
    timerId = setTimeout(() => setStatus('надіслано'), 3000)
  }

  function undo() {
    if (timerId !== null) clearTimeout(timerId)
    setStatus('скасовано')
  }

  return (
    <>
      <p role="status">{status}</p>
      <button onClick={send}>надіслати</button>
      <button onClick={undo}>скасувати</button>
    </>
  )
}
```

Запис `ReturnType<typeof setTimeout>` бере тип результату функції `setTimeout`, тому вам не треба знати, що саме вона
повертає. `ReturnType` є вбудованим у TypeScript дженериком, який з типу функції дістає тип її результату. Тест клацає
кнопки, а час перемотує штучними таймерами Vitest, які показала лекція «Рендер, коміт і знімок стану». Тест лежить в
одному файлі з компонентом:

```tsx
// @vitest-environment jsdom
import { useRef, useState } from 'react'
import { act, fireEvent, render, screen } from '@testing-library/react'
import { test, vi } from 'vitest'

// status читає текст єдиного абзацу зі статусом, а statuses читає тексти всіх таких абзаців.
const status = () => screen.getByRole('status').textContent
const statuses = () => screen.getAllByRole('status').map((p) => p.textContent).join(' | ')

// Тут стоїть компонент WithLet.

test('let', () => {
  vi.useFakeTimers() // Відтепер час іде лише тоді, коли тест його перемотує.
  render(<WithLet />)
  fireEvent.click(screen.getByText('надіслати'))
  console.log('let | після «надіслати»:', status())
  fireEvent.click(screen.getByText('скасувати'))
  console.log('let | після «скасувати»:', status())
  act(() => { vi.advanceTimersByTime(3000) }) // Перемотуємо три секунди, і таймер спрацьовує.
  console.log('let | через 3 секунди:', status())
})
```

Команда `npx vitest run src/let.test.tsx --disable-console-intercept` запускає цей файл, а прапорець у кінці прибирає
службові рядки навколо друку. Вона друкує:

```text
let | після «надіслати»: надсилається
let | після «скасувати»: скасовано
let | через 3 секунди: надіслано
```

Користувач побачив «скасовано», а через три секунди лист усе одно пішов. Ось що сталося.

| Крок | Хто діє | Що відбувається |
|------|---------|-----------------|
| 1 | React | викликає компонент, і створюється змінна `timerId` цього рендеру, у ній `null` |
| 2 | обробник `send` першого рендеру | записує ідентифікатор у змінну першого рендеру і викликає `setStatus` |
| 3 | React | викликає компонент знову, і створюється нова змінна `timerId`, у ній знову `null` |
| 4 | обробник `undo` другого рендеру | читає змінну другого рендеру, бачить `null` і нічого не зупиняє |

Лекція «Рендер, коміт і знімок стану» пояснила, що кожен рендер є окремим викликом функції зі своїми змінними.
Ідентифікатор лежить у змінній рендеру, який уже закінчився, і його ніхто більше не прочитає. Лінт попереджає про це
заздалегідь: правило `react-hooks/immutability` каже `Cannot reassign variable after render completes`.

Нам потрібна пам'ять із двома властивостями: вона переживає рендери й не просить нового рендеру. Порівняймо чотири
місця, де її можна шукати.

| Де лежить ідентифікатор | Чи переживає рендер | Чи просить рендеру | Чи окремий для кожного компонента |
|-------------------------|---------------------|---------------------|-----------------------------------|
| змінна всередині компонента | ні | ні | так |
| стан | так | так | так |
| змінна модуля | так | ні | ні |
| ref | так | ні | так |

Стан теж дає правильний результат, але просить зайвого рендеру. Заміряємо це на кнопці «нагадати», де стан лежить лише
для ідентифікатора, а кожне клацання перезапускає таймер. Кожен наступний дослід лекції лежить у власному файлі тесту з
такими самими першими рядками, тому далі лекція показує лише компоненти й рядки, які стоять усередині `test`.

```tsx
let calls = 0 // Рахує виклики компонента лише для цього заміру.

function RemindInState() {
  calls++
  const [timerId, setTimerId] = useState<ReturnType<typeof setTimeout> | null>(null)
  function remind() {
    if (timerId !== null) clearTimeout(timerId)
    setTimerId(setTimeout(() => console.log('нагадування'), 3000)) // Цей виклик просить рендер.
  }
  return <button onClick={remind}>нагадати</button>
}

function RemindInRef() {
  calls++
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  function remind() {
    if (timerRef.current !== null) clearTimeout(timerRef.current)
    timerRef.current = setTimeout(() => console.log('нагадування'), 3000) // Цей запис рендеру не просить.
  }
  return <button onClick={remind}>нагадати</button>
}
```

Тест показує кожен компонент окремо й тричі клацає його кнопку:

```tsx
vi.useFakeTimers()

const first = render(<RemindInState />)
for (let i = 0; i < 3; i++) fireEvent.click(first.getByText('нагадати'))
console.log('ідентифікатор у стані | викликів компонента після трьох клацань:', calls)
first.unmount()

calls = 0
const second = render(<RemindInRef />)
for (let i = 0; i < 3; i++) fireEvent.click(second.getByText('нагадати'))
console.log('ідентифікатор у ref | викликів компонента після трьох клацань:', calls)
```

```text
ідентифікатор у стані | викликів компонента після трьох клацань: 4
ідентифікатор у ref | викликів компонента після трьох клацань: 1
```

Чотири виклики зі станом складаються з першого показу й трьох рендерів після трьох клацань. Один виклик із ref є лише
першим показом, бо запис у `current` рендеру не просить. Отже, якщо екран не показує ідентифікатора, кладіть його в ref,
і компонент не виконуватиме зайвої роботи.

Змінна модуля не загубиться між рендерами, але вона одна на всі копії компонента. Поставимо поруч два листи, надішлемо
обидва й скасуємо перший:

```tsx
let moduleTimer: ReturnType<typeof setTimeout> | null = null // Ця змінна одна на всі копії компонента.

function WithModuleVariable() {
  const [status, setStatus] = useState('чернетка')

  function send() {
    setStatus('надсилається')
    moduleTimer = setTimeout(() => setStatus('надіслано'), 3000)
  }

  function undo() {
    if (moduleTimer !== null) clearTimeout(moduleTimer)
    setStatus('скасовано')
  }

  return (
    <>
      <p role="status">{status}</p>
      <button onClick={send}>надіслати</button>
      <button onClick={undo}>скасувати</button>
    </>
  )
}
```

```tsx
vi.useFakeTimers()
render(<><WithModuleVariable /><WithModuleVariable /></>)
// getAllByText знаходить кнопки обох копій у такому порядку, у якому вони стоять на сторінці.
const sendButtons = screen.getAllByText('надіслати')
fireEvent.click(sendButtons[0])
fireEvent.click(sendButtons[1])
fireEvent.click(screen.getAllByText('скасувати')[0])
console.log('змінна модуля | перший скасовано:', statuses())
act(() => { vi.advanceTimersByTime(3000) })
console.log('змінна модуля | через 3 секунди:', statuses())
```

```text
змінна модуля | перший скасовано: скасовано | надсилається
змінна модуля | через 3 секунди: надіслано | надсилається
```

Перший компонент зупинив таймер другого, бо в змінній лежав останній записаний ідентифікатор. Через три секунди
спрацював таймер першого: лист, який показував «скасовано», пішов, а лист другого компонента назавжди завис у стані
«надсилається».

## Як працює `useRef`

Хук `useRef` дає саме потрібну пам'ять. Він повертає звичайний об'єкт JavaScript з одним полем `current`, а React
зберігає цей об'єкт між рендерами. Такий об'єкт називають **посиланням**, англійською **ref**. Лекція «TypeScript у
React» уже коротко показала його типи. Заміна в прикладі мінімальна:

```tsx
let bodies = 0

function WithRef() {
  bodies++
  const [status, setStatus] = useState('чернетка')
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  function send() {
    setStatus('надсилається')
    timerRef.current = setTimeout(() => setStatus('надіслано'), 3000)
  }

  function undo() {
    if (timerRef.current !== null) clearTimeout(timerRef.current)
    setStatus('скасовано')
  }

  return (
    <>
      <p role="status">{status}</p>
      <button onClick={send}>надіслати</button>
      <button onClick={undo}>скасувати</button>
    </>
  )
}
```

Тест спершу робить ті самі клацання, що й перший дослід, а потім ставить поруч два листи:

```tsx
vi.useFakeTimers()
const view = render(<WithRef />)
fireEvent.click(screen.getByText('надіслати'))
fireEvent.click(screen.getByText('скасувати'))
act(() => { vi.advanceTimersByTime(3000) })
console.log('ref | через 3 секунди:', status(), '| викликів компонента:', bodies)
view.unmount()

render(<><WithRef /><WithRef /></>)
const sendButtons = screen.getAllByText('надіслати')
fireEvent.click(sendButtons[0])
fireEvent.click(sendButtons[1])
fireEvent.click(screen.getAllByText('скасувати')[0])
act(() => { vi.advanceTimersByTime(3000) })
console.log('ref | два листи, через 3 секунди:', statuses())
```

```text
ref | через 3 секунди: скасовано | викликів компонента: 3
ref | два листи, через 3 секунди: скасовано | надіслано
```

Запис `bodies++` лише рахує виклики для цього заміру. Обробник другого рендеру тепер читає те саме поле того самого
об'єкта, у яке писав обробник першого рендеру. Другий рядок виводу показує, що кожна копія компонента має власний ref,
тому два листи більше не заважають один одному. Три виклики компонента потрібні через `setStatus`, а запис у
`timerRef.current` не додав жодного.

### Той самий об'єкт на кожному рендері

Сторінка `Referencing Values with Refs` пропонує уявити, що `useRef` міг би бути написаний поверх `useState`: стан, у
якому лежить об'єкт, а функції `set` ніхто ніколи не викликає. Запуск це підтверджує:

```tsx
const seen: { current: { number: number } }[] = [] // Кожен рендер кладе сюди об'єкт, який дав useRef.
let made = 0 // Рахує виклики makeLog.

function makeLog() {
  made++
  return { number: made }
}

function Identity() {
  const [n, setN] = useState(0)
  const log = useRef(makeLog())
  seen.push(log)
  return <button onClick={() => setN(n + 1)}>ще</button>
}
```

Тест двічі клацає кнопку, тобто разом із першим показом дає три рендери:

```tsx
render(<Identity />)
fireEvent.click(screen.getByText('ще'))
fireEvent.click(screen.getByText('ще'))
console.log(
  'рендерів:', seen.length,
  '| той самий об’єкт:', new Set(seen).size === 1, // Set лишає лише різні об'єкти.
  '| викликів makeLog:', made,
  '| у current лежить запис №', seen[0].current.number,
)
```

```text
рендерів: 3 | той самий об’єкт: true | викликів makeLog: 3 | у current лежить запис № 1
```

Усі три рендери отримали той самий об'єкт. Аргумент `useRef` має значення лише на першому рендері, а далі React його
ігнорує. Проте сам вираз `makeLog()` обчислюється при кожному виклику компонента, бо JavaScript обчислює аргументи до
того, як функція їх отримає. Для числа чи `null` це байдуже. Для дорогого об'єкта є окремий запис, і про нього йдеться
нижче.

### Запис видно одразу

Значення в ref не є знімком. Запис змінює звичайне поле об'єкта, тому наступний рядок уже бачить нове значення:

```tsx
function Immediate() {
  const [inState, setInState] = useState(0)
  const inRef = useRef(0)
  function handle() {
    setInState(inState + 1)
    inRef.current = inRef.current + 1
    console.log('в обробнику | стан:', inState, '| ref:', inRef.current)
  }
  return <><button onClick={handle}>плюс</button><p role="status">{inState}</p></>
}
```

Тест двічі клацає кнопку й наприкінці читає екран:

```tsx
render(<Immediate />)
fireEvent.click(screen.getByText('плюс'))
fireEvent.click(screen.getByText('плюс'))
console.log('на екрані:', status())
```

```text
в обробнику | стан: 0 | ref: 1
в обробнику | стан: 1 | ref: 2
на екрані: 2
```

Перші два рядки друкує обробник. Значення стану в кожному з них на одиницю менше за значення ref, бо обробник бачить
стан свого рендеру, а поле ref читає вже після запису. Останній рядок друкує тест після двох клацань, тому екран показує
нове значення стану.

Звідси випливає корисний наслідок для коду, який спрацьовує пізніше. Лекція «Рендер, коміт і знімок стану» показала,
що таймер бачить змінну стану того рендеру, який його створив. Значення з ref таймер читає в момент спрацювання.
Користувач почав писати повідомлення, натиснув «надіслати пізніше» й дописав текст:

```tsx
function Chat() {
  const [draft, setDraft] = useState('')
  const latest = useRef('')
  function handleChange(value: string) {
    setDraft(value)
    latest.current = value
  }
  function sendLater() {
    setTimeout(() => {
      console.log('зі стану:', draft, '| з ref:', latest.current)
    }, 3000)
  }
  return (
    <>
      <input aria-label="чат" value={draft} onChange={(e) => handleChange(e.target.value)} />
      <button onClick={sendLater}>надіслати пізніше</button>
    </>
  )
}
```

```tsx
vi.useFakeTimers()
render(<Chat />)
const field = screen.getByLabelText('чат')
fireEvent.change(field, { target: { value: 'при' } })
fireEvent.click(screen.getByText('надіслати пізніше')) // Таймер стартує, коли в полі написано «при».
fireEvent.change(field, { target: { value: 'привіт' } })
act(() => { vi.advanceTimersByTime(3000) })
```

```text
зі стану: при | з ref: привіт
```

Таймер запам'ятав змінну `draft` того рендеру, у якому користувач клацнув кнопку, тому він надрукував «при». Поле
`latest.current` таймер прочитав через три секунди, тому він надрукував «привіт».

Зазвичай потрібна саме поведінка стану: лист іде таким, яким він був у момент клацання. Сторінка React показує цей
прийом як рідкісний випадок, коли код, який спрацьовує пізніше, справді має прочитати найновіше значення.

### Стан чи ref

| Запитання | Стан | Ref |
|-----------|------|-----|
| Що повертає хук | значення й функцію `set` | об'єкт `{ current: значення }` |
| Чи запускає зміна рендер | так | ні |
| Як змінювати | лише через функцію `set` | присвоєнням у `current` |
| Коли видно нове значення | у наступному рендері | одразу |
| Чи можна читати під час рендеру | так | ні |

Обирати допомагає одне запитання: чи залежить від цього значення те, що компонент показує? Якщо залежить, то потрібен
стан. Якщо значення потрібне лише обробникам подій і екран від нього не залежить, то підходить ref. Сторінка React
називає ref запасним виходом із React: він потрібен рідко, переважно для роботи зі сторонніми системами й браузером.
Якщо більшість логіки компонента тримається на ref, варто переглянути підхід.

## Правило: не під час рендеру

Подивімося, що станеться, якщо значення з ref показати на екрані. Компонент рахує натискання клавіш у ref, а
збереження в стані:

```tsx
function BadDraft() {
  const [saves, setSaves] = useState(0)
  const keys = useRef(0)
  return (
    <>
      <input aria-label="лист" onChange={() => { keys.current = keys.current + 1 }} />
      <button onClick={() => setSaves(saves + 1)}>зберегти</button>
      <p role="status">Натискань: {keys.current}, збережень: {saves}</p>
    </>
  )
}
```

Тест тричі змінює значення поля, а потім клацає «зберегти»:

```tsx
render(<BadDraft />)
const field = screen.getByLabelText('лист')
for (const value of ['а', 'аб', 'абв']) fireEvent.change(field, { target: { value } })
console.log('три натискання, на екрані:', status())
fireEvent.click(screen.getByText('зберегти'))
console.log('після «зберегти», на екрані:', status())
```

```text
три натискання, на екрані: Натискань: 0, збережень: 0
після «зберегти», на екрані: Натискань: 3, збережень: 1
```

Екран показує неправильне число: користувач натиснув три клавіші, а бачить нуль. Потім він клацає іншу кнопку, і число
раптом стрибає. React не знає, коли змінюється `ref.current`, тому на екрані лежить значення з тієї миті, коли хтось
випадково викликав компонент. Лінт не пропустить такий запис. Команда `npx eslint` для файла з цим компонентом друкує
довге повідомлення, а тут показано лише назву правила й перший рядок повідомлення:

```text
react-hooks/refs Error: Cannot access refs during render
```

Правильний запис для такої задачі нічого не читає під час рендеру. Показує лише стан, а значення з ref друкує
обробник:

```tsx
function Draft() {
  const [saves, setSaves] = useState(0)
  const keys = useRef(0)
  function handleInput() {
    keys.current = keys.current + 1
    console.log('натискань:', keys.current)
  }
  return (
    <>
      <input aria-label="лист" onChange={handleInput} />
      <button onClick={() => setSaves(saves + 1)}>зберегти</button>
      <p role="status">Збережень: {saves}</p>
    </>
  )
}
```

```tsx
render(<Draft />)
const field = screen.getByLabelText('лист')
for (const value of ['а', 'аб', 'абв']) {
  fireEvent.change(field, { target: { value } })
  console.log('на екрані:', status())
}
fireEvent.click(screen.getByText('зберегти'))
console.log('після «зберегти», на екрані:', status())
```

```text
натискань: 1
на екрані: Збережень: 0
натискань: 2
на екрані: Збережень: 0
натискань: 3
на екрані: Збережень: 0
після «зберегти», на екрані: Збережень: 1
```

Саме цю картину вимагає перевірка дня: журнал показує, що лічильник у ref зростає, а екран змінюється лише зі станом.
Якщо у вашому компоненті число з ref стоїть прямо в розмітці, це і є сьогоднішня пастка, навіть коли демонстрація
начебто працює.

Запис під час рендеру ще гірший. Лічильник рендерів здається безневинним:

```tsx
function RenderCounter() {
  const count = useRef(0)
  count.current = count.current + 1
  return <p role="status">Рендерів: {count.current}</p>
}
```

Тест показує компонент, викликає `rerender`, щоб React виконав ще один рендер, а потім робить те саме в обгортці
`<StrictMode>`:

```tsx
import { StrictMode } from 'react'

const plain = render(<RenderCounter />)
console.log('без StrictMode | показ:', status())
plain.rerender(<RenderCounter />)
console.log('без StrictMode | ще:', status())
plain.unmount()

const strict = render(<StrictMode><RenderCounter /></StrictMode>)
console.log('StrictMode | показ:', status())
strict.rerender(<StrictMode><RenderCounter /></StrictMode>)
console.log('StrictMode | ще:', status())
```

```text
без StrictMode | показ: Рендерів: 1
без StrictMode | ще: Рендерів: 2
StrictMode | показ: Рендерів: 2
StrictMode | ще: Рендерів: 4
```

Той самий код дав інші числа лише через обгортку. Тема «Чистота й дерево» пояснила, що рендер має бути чистим
обчисленням: React вправі викликати компонент двічі, а результат виклику відкинути. Запис у ref є змінною, яка
переживає такі виклики, тому кожен зайвий виклик лишає в ній слід. Лінт теж про це повідомляє тим самим правилом
`react-hooks/refs`, а місце в коді позначає написом `Cannot update ref during render`.

Є один виняток. Запис, який виконується лише раз і завжди дає той самий результат, дозволений. Він розв'язує проблему
дорогого початкового значення, про яку йшлося вище:

```tsx
class Player {
  play() {} // Тут стоїть справжня дорога робота. Для прикладу клас порожній.
}

export function LazyInit() {
  const player = useRef<Player | null>(null)
  if (player.current === null) {
    player.current = new Player()
  }
  return <button onClick={() => player.current?.play()}>грати</button>
}
```

Довідник `useRef` прямо дозволяє цей запис, і лінт на нього не скаржиться. Читання в обробнику `onClick` теж не
порушує правила, бо обробник виконується після рендеру.

## Ref на елемент сторінки

Найчастіше ref тримає **вузол DOM**, тобто об'єкт браузера, який представляє елемент сторінки. Лекція «DOM і події»
пояснила, що таке вузол. Вузол має методи, наприклад `focus()`, який переводить на елемент фокус клавіатури. Зазвичай
у React такі методи не потрібні, бо ви описуєте результат, а документ змінює React. Проте деякі дії не можна описати
розміткою: перевести фокус, прокрутити сторінку, виміряти розмір. Для них потрібен сам вузол.

Якщо передати ref в атрибут `ref` вбудованого тега, React покладе туди вузол:

```tsx
function CouponCopy() {
  const inputRef = useRef<HTMLInputElement>(null)
  return (
    <>
      <input ref={inputRef} defaultValue="KAVA-2026" aria-label="код" readOnly />
      <button onClick={() => {
        inputRef.current?.focus()
        inputRef.current?.select()
      }}>виділити код</button>
    </>
  )
}
```

Функція `report` друкує, який елемент має фокус і які символи поля виділено:

```tsx
render(<CouponCopy />)
const input = screen.getByLabelText<HTMLInputElement>('код')
const report = (label: string) =>
  console.log(label, 'у фокусі:', document.activeElement?.tagName, '| виділено:', input.selectionStart, input.selectionEnd)

report('до клацання,')
fireEvent.click(screen.getByText('виділити код'))
report('після клацання,')
input.blur() // Забирає фокус із поля, щоб перевірити select() окремо.
input.select()
report('після blur() і select(),')
```

```text
до клацання, у фокусі: BODY | виділено: 9 9
після клацання, у фокусі: INPUT | виділено: 0 9
після blur() і select(), у фокусі: BODY | виділено: 0 9
```

Перші два рядки виводу означають, що до клацання фокус стояв на всій сторінці, а після клацання він стоїть у полі й
виділено символи від 0 до 9, тобто весь код. Це поведінка jsdom. Останній рядок показує, що метод `select()` окремо
фокуса в jsdom не переводить. У браузері фокус теж не гарантовано: сторінка MDN каже, що `select()` не завжди дає фокус,
тому поруч викликають `focus()`. У браузері ми цього не запускали, але очікуйте побачити той самий результат: текст у
полі виділено, а курсор стоїть у полі.

Знак `?.` і тип `useRef<HTMLInputElement>(null)` пояснила лекція «TypeScript у React»: у `current` лежить `null`, поки
вузла немає. Тепер подивімося, коли саме він там з'являється.

### Коли React кладе вузол

Лекція «Рендер, коміт і знімок стану» поділила оновлення на два кроки: **рендер**, коли React викликає компоненти, і
**коміт**, коли React вносить зміни в документ. Вузол з'являється в `ref.current` під час коміту. Ось журнал
компонента з полем, яке можна сховати. Рядки, які починаються словом «рендер», записує само тіло компонента. Так
писати не можна, а тут це потрібно лише заради цього досліду:

```tsx
const stages: string[] = [] // Журнал досліду.
const tag = (node: HTMLElement | null) => node?.tagName ?? 'null' // Назва тега або слово null.

function Coupon() {
  const [shown, setShown] = useState(true)
  const inputRef = useRef<HTMLInputElement>(null)
  stages.push('рендер: ' + tag(inputRef.current))
  function hide() {
    setShown(false)
    stages.push('обробник, щойно після set: ' + tag(inputRef.current))
  }
  return (
    <>
      <button onClick={hide}>сховати</button>
      <button onClick={() => stages.push('інший обробник: ' + tag(inputRef.current))}>глянути</button>
      {shown && <input ref={inputRef} defaultValue="KAVA-2026" aria-label="код" />}
    </>
  )
}
```

Тест показує компонент, клацає «глянути», потім «сховати», потім знову «глянути» й друкує журнал:

```tsx
render(<Coupon />)
fireEvent.click(screen.getByText('глянути'))
fireEvent.click(screen.getByText('сховати'))
fireEvent.click(screen.getByText('глянути'))
console.log(stages.join('\n'))
```

```text
рендер: null
інший обробник: INPUT
обробник, щойно після set: INPUT
рендер: INPUT
інший обробник: null
```

| Рядок журналу | Що там сталося |
|---------------|----------------|
| `рендер: null` | перший рендер: документа ще не змінено, вузла немає |
| `інший обробник: INPUT` | після першого коміту React поклав вузол, і обробник його бачить |
| `обробник, щойно після set: INPUT` | функція `set` лише попросила рендер, тому поле ще в документі |
| `рендер: INPUT` | другий рендер бачить старий вузол, бо коміту ще не було |
| `інший обробник: null` | другий коміт вилучив поле, і React записав `null` |

Четвертий рядок показує, чому читати вузол під час рендеру завжди зарано. На першому рендері там `null`, а на
наступних лежить вузол ще зі старого стану документа. Тому вузол читають в обробниках подій. Якщо події немає,
потрібен ефект, якому присвячена тема «Синхронізація ефектами».

### Елемента ще немає

Тепер поглянемо на випадок навпаки: елемент має з'явитися, і вам одразу потрібен його вузол. Запитання розгортає
відповідь, а обробник хоче її прочитати. Щоб не показувати готового розв'язку, тут обробник лише друкує текст, а в
практиці ви застосуєте те саме міркування до своїх дій:

```tsx
import { flushSync } from 'react-dom'

function Faq({ mode }: { mode: 'звичайно' | 'flushSync' }) {
  const [open, setOpen] = useState(false)
  const answerRef = useRef<HTMLParagraphElement>(null)
  function openAnswer() {
    if (mode === 'flushSync') {
      flushSync(() => setOpen(true))
    } else {
      setOpen(true)
    }
    console.log(mode, '| вузол відповіді:', answerRef.current?.textContent ?? null)
  }
  return (
    <>
      <button onClick={openAnswer}>відкрити</button>
      {open && <p ref={answerRef}>Так, повертаємо за 14 днів.</p>}
    </>
  )
}
```

```tsx
const first = render(<Faq mode="звичайно" />)
fireEvent.click(first.getByText('відкрити'))
first.unmount()

const second = render(<Faq mode="flushSync" />)
fireEvent.click(second.getByText('відкрити'))
```

```text
звичайно | вузол відповіді: null
flushSync | вузол відповіді: Так, повертаємо за 14 днів.
```

Функція `set` не змінює документа одразу: вона просить рендер, а коміт відбудеться після кінця обробника. Отже, у
цьому самому обробнику нового вузла ще немає. Функція `flushSync` з пакета `react-dom`, яку показала лекція «Рендер,
коміт і знімок стану», змушує React виконати рендер і коміт просто в цьому місці, тому наступний рядок уже бачить
вузол. Ця функція змушує React працювати в момент, який він сам не вибрав, а довідник `flushSync` попереджає, що це
може погіршити швидкодію, тому її вживають лише для таких випадків. Сторінка `Manipulating the DOM with Refs` показує
її в згорнутому блоці `Flushing state updates synchronously with flushSync`.

Коли вузол потрібен лише тоді, коли він з'явився, є ще два шляхи. Перший шлях є функцією в атрибуті `ref`, про яку
йдеться в наступному розділі. Другий шлях є ефектом, який ви вивчите в наступний день.

## Функція в атрибуті `ref`

Поки елементів кілька й ви знаєте їх заздалегідь, можна викликати `useRef` кілька разів. Для списку невідомої довжини
це не працює: виклик хука всередині `map` дає помилку правила `react-hooks/rules-of-hooks`, бо хуки викликають лише на
верхньому рівні компонента. Натомість в атрибут `ref` передають функцію. Її називають **ref-колбеком**: React викликає
її з вузлом, коли той з'являється, а функцію, яку вона повернула, викликає, коли вузол зникає.

Зміст довгої статті тримає всі розділи в об'єкті `Map`, який лежить у ref. Цей об'єкт екран не показує, тому мутувати
його дозволено:

```tsx
const SECTIONS = [
  { id: 'intro', title: 'Вступ' },
  { id: 'recipe', title: 'Рецепт' },
  { id: 'tips', title: 'Поради' },
]

function Article() {
  const nodes = useRef(new Map<string, HTMLElement>())
  return (
    <>
      <nav>
        {SECTIONS.map((s) => (
          <button key={s.id} onClick={() => nodes.current.get(s.id)?.scrollIntoView()}>{s.title}</button>
        ))}
      </nav>
      {SECTIONS.map((s) => (
        <section
          key={s.id}
          ref={(node) => {
            if (node !== null) nodes.current.set(s.id, node)
            return () => {
              nodes.current.delete(s.id)
            }
          }}
        >
          {s.title}
        </section>
      ))}
    </>
  )
}
```

```tsx
console.log('у jsdom scrollIntoView:', Element.prototype.scrollIntoView)

// jsdom не має цього методу, тому тест ставить власну функцію, яка лише записує текст вузла.
const scrolled: (string | null)[] = []
Element.prototype.scrollIntoView = function () {
  scrolled.push(this.textContent)
}

render(<Article />)
fireEvent.click(screen.getByRole('button', { name: 'Рецепт' }))
fireEvent.click(screen.getByRole('button', { name: 'Поради' }))
console.log('прокручено до:', scrolled.join(', '))
```

```text
у jsdom scrollIntoView: undefined
прокручено до: Рецепт, Поради
```

Перший рядок важливий для ваших тестів: jsdom не вміє розташовувати елементи на сторінці, тому методу `scrollIntoView`
у нього немає зовсім. Виклик без підготовки кине `TypeError`. Тест підставляє власну функцію в
`Element.prototype.scrollIntoView` і записує, до чого його просили прокрутити, тому рядок доводить лише те, що виклик
відбувся на потрібному вузлі. Саму прокрутку виконує браузер, і ми її не бачили. Сторінка MDN описує параметри цього
методу, зокрема `behavior: 'smooth'` для плавної прокрутки й `block` для вирівнювання.

Запис `if (node !== null)` потрібен через типи: параметр має тип `HTMLElement | null`, хоч у React 19 із функцією
прибирання `null` не приходить. Також зверніть увагу на фігурні дужки в тілі колбека. Запис `ref={(n) => (saved = n)}`
неявно повертає значення, а тип дозволяє повертати лише функцію прибирання, тому компілятор дає `TS2322`.

### Колбек, створений на кожному рендері

Запис `ref={(node) => ...}` прямо в розмітці створює нову функцію при кожному виклику компонента. Побачивши іншу
функцію, React відв'язує стару й прив'язує нову. Перевіримо це на трьох компонентах. Перший пише колбек прямо в
розмітці, другий додає до нього функцію прибирання, а третій бере функцію, оголошену поза компонентом:

```tsx
const log: string[] = []

function Inline() {
  const [n, setN] = useState(0)
  return (
    <aside ref={(node) => { log.push(node ? 'прив’язано' : 'null') }}>
      <button onClick={() => setN(n + 1)}>ще</button>
    </aside>
  )
}

function WithCleanup() {
  const [n, setN] = useState(0)
  return (
    <aside
      ref={(node) => {
        log.push('прив’язано ' + node?.tagName)
        return () => { log.push('прибирання') }
      }}
    >
      <button onClick={() => setN(n + 1)}>ще</button>
    </aside>
  )
}

function stable(node: HTMLElement | null) {
  log.push('stable: ' + (node?.tagName ?? 'null'))
}

function Stable() {
  const [n, setN] = useState(0)
  return (
    <aside ref={stable}>
      <button onClick={() => setN(n + 1)}>ще</button>
    </aside>
  )
}
```

Тест робить з кожним компонентом те саме: показує його, двічі клацає кнопку, щоб запустити рендер, і вилучає компонент.
Останній запуск повторює `Stable` в обгортці `<StrictMode>`:

```tsx
import { StrictMode, type ReactElement } from 'react'

function run(name: string, ui: ReactElement) {
  log.length = 0 // Кожен запуск починає журнал спочатку.
  const view = render(ui)
  fireEvent.click(view.getByText('ще'))
  fireEvent.click(view.getByText('ще'))
  view.unmount()
  console.log(name, '|', log.join(', '))
}

run('inline', <Inline />)
run('cleanup', <WithCleanup />)
run('stable', <Stable />)
run('stable у StrictMode', <StrictMode><Stable /></StrictMode>)
```

```text
inline | прив’язано, null, прив’язано, null, прив’язано, null
cleanup | прив’язано ASIDE, прибирання, прив’язано ASIDE, прибирання, прив’язано ASIDE, прибирання
stable | stable: ASIDE, stable: null
stable у StrictMode | stable: ASIDE, stable: null, stable: ASIDE, stable: null
```

Рядок `inline` показує колбек без функції прибирання: замість неї React викликає сам колбек із `null`. Рядок `cleanup`
показує той самий цикл із функцією прибирання. Рядок `stable` показує функцію, оголошену поза компонентом: вона та
сама на кожному рендері, тому React викликав її лише двічі. Для запису в `Map` цикл нешкідливий, але якщо колбек
робить щось помітне, наприклад переводить фокус, то він робитиме це на кожному рендері й забиратиме фокус у
користувача. Останній рядок показує, що `<StrictMode>` у режимі розробки навмисно проганяє цей цикл зайвий раз, щоб ви
побачили, чи прибирання працює.

## Ref власному компоненту

Атрибут `ref` на вбудованому тегу дає вузол. Власний компонент не віддає своїх вузлів сам. У React 19 `ref` є
звичайним пропсом, і компонент сам вирішує, куди його передати:

```tsx
import type { ComponentType, Ref } from 'react'

function CityField({ label, ref }: { label: string; ref?: Ref<HTMLInputElement> }) {
  return <label>{label}<input ref={ref} /></label>
}
```

Батьківський компонент `Form` читає `fieldRef.current` і викликає `focus()`. Він отримує поле пропсом `Field`, тому той
самий батько може перевірити різні поля. Компонент `Ignoring` приймає `ref`, але нікуди його не передає:

```tsx
function Ignoring({ label }: { label: string; ref?: Ref<HTMLInputElement> }) {
  return <label>{label}<input /></label>
}

function Form({ Field }: { Field: ComponentType<{ label: string; ref?: Ref<HTMLInputElement> }> }) {
  const fieldRef = useRef<HTMLInputElement>(null)
  function goToField() {
    console.log('вузол у батька:', fieldRef.current?.tagName ?? null)
    fieldRef.current?.focus()
    console.log('у фокусі:', document.activeElement?.tagName)
  }
  return (
    <>
      <Field label="Місто" ref={fieldRef} />
      <button onClick={goToField}>до поля</button>
    </>
  )
}
```

Тест показує батька спершу з `Ignoring`, а потім із `CityField`:

```tsx
const first = render(<Form Field={Ignoring} />)
fireEvent.click(first.getByText('до поля'))
first.unmount()

const second = render(<Form Field={CityField} />)
fireEvent.click(second.getByText('до поля'))
```

```text
вузол у батька: null
у фокусі: BODY
вузол у батька: INPUT
у фокусі: INPUT
```

Перша пара рядків пояснює поширену проблему: під час виконання такий запис не дає жодної помилки, а в `current`
лишається `null`, бо компонент не передав пропс далі. У TypeScript вас попередить компілятор: якщо в типі пропсів
немає `ref`, він дасть `TS2322: Property 'ref' does not exist`. Приклади React написано на JavaScript, тому там цього
не видно, і довідник `useRef` описує проблему в розділі `Troubleshooting`. Тип `Ref<HTMLInputElement>` приймає і
об'єкт ref, і функцію. Якщо компонент просто загортає `input`, зручно взяти всі його пропси записом
`ComponentProps<'input'>`, і `ref` прийде разом з ними.

У старому коді ви побачите обгортку `forwardRef`, бо до React 19 `ref` не приходив як пропс. Передамо батькові `Form`
таке старе поле:

```tsx
import { forwardRef } from 'react'

const OldCityField = forwardRef<HTMLInputElement, { label: string }>(({ label }, ref) => (
  <label>{label}<input ref={ref} /></label>
))

// Далі рядки тесту.
render(<Form Field={OldCityField} />)
fireEvent.click(screen.getByText('до поля'))
```

```text
вузол у батька: INPUT
у фокусі: INPUT
```

Обгортка досі працює й дає той самий результат, що й `CityField`, але довідник каже, що вона вже не потрібна й буде
позначена застарілою в одній із майбутніх версій. У новому коді передавайте `ref` звичайним пропсом.

Сторінка `Manipulating the DOM with Refs` радить обережність: чужі вузли змінювати небезпечно, тому компонент може
віддати лише частину можливостей. Для цього є хук `useImperativeHandle`, де ви самі описуєте об'єкт, який отримає
батько:

```tsx
import { useImperativeHandle, type Ref } from 'react'

type FieldHandle = { focus: () => void }

function GuardedField({ ref }: { ref?: Ref<FieldHandle> }) {
  const inputRef = useRef<HTMLInputElement>(null)
  useImperativeHandle(ref, () => ({
    focus() {
      inputRef.current?.focus()
    },
  }))
  return <input ref={inputRef} />
}

function Page() {
  const fieldRef = useRef<FieldHandle>(null)
  function goToField() {
    fieldRef.current?.focus()
    // Object.keys показує, які поля має об'єкт, що лежить у ref батька.
    console.log('у фокусі:', document.activeElement?.tagName, '| що бачить батько:', Object.keys(fieldRef.current ?? {}))
  }
  return (
    <>
      <GuardedField ref={fieldRef} />
      <button onClick={goToField}>до поля</button>
    </>
  )
}
```

```tsx
render(<Page />)
fireEvent.click(screen.getByText('до поля'))
```

```text
у фокусі: INPUT | що бачить батько: [ 'focus' ]
```

Батько може поставити фокус, але не може змінити стилі поля чи його значення. Цей хук потрібен рідко, і сьогоднішня
практика без нього обходиться.

## Не змінюйте те, чим керує React

Фокус і прокрутка нічого не міняють у структурі документа. Вилучення вузла міняє, і тоді React і браузер починають
бачити різне:

```tsx
function Banner() {
  const [shown, setShown] = useState(true)
  const bannerRef = useRef<HTMLParagraphElement>(null)
  return (
    <div>
      <button onClick={() => setShown(!shown)}>перемкнути</button>
      <button onClick={() => bannerRef.current?.remove()}>вилучити вручну</button>
      {shown && <p ref={bannerRef}>Знижка до неділі</p>}
    </div>
  )
}
```

Тест клацає «вилучити вручну», а потім «перемкнути». Помилку другого клацання він ловить, щоб надрукувати її текст:

```tsx
const { container } = render(<Banner />)
fireEvent.click(screen.getByText('вилучити вручну'))
console.log('після вилучення вручну, абзац у документі:', screen.queryByText('Знижка до неділі') !== null)

const errors: string[] = []
try {
  fireEvent.click(screen.getByText('перемкнути'))
} catch (error) {
  errors.push('кинуто: ' + error)
}
console.log('помилки:', JSON.stringify(errors))
console.log('вміст контейнера після збою:', JSON.stringify(container.innerHTML))
```

```text
після вилучення вручну, абзац у документі: false
помилки: ["кинуто: NotFoundError: The node to be removed is not a child of this node."]
вміст контейнера після збою: ""
```

Клацання «вилучити вручну» спрацювало, а наступне клацання «перемкнути» зламало весь застосунок. React намагався
вилучити абзац, який уже зник, отримав помилку, і на сторінці не лишилося нічого. Текст помилки тут належить jsdom. У
браузері текст може бути іншим, а документація описує такий самий результат: збій застосунку. Правило сторінки таке:
не міняйте вузлів, якими керує React, але можете вільно працювати там, де React нема чого оновлювати, наприклад у
`div`, який у розмітці завжди порожній.

## Таймери: що ще може піти не так

Практика дня має секундомір, тому знайте дві пастки таймерів. Покажемо їх на нашому листі й на окремому таймері.

**Повторний запуск.** Якщо клацнути «надіслати» двічі, то стартують два таймери, а в ref лишиться лише другий
ідентифікатор. Тест бере компонент `WithRef`:

```tsx
vi.useFakeTimers()
render(<WithRef />)
fireEvent.click(screen.getByText('надіслати'))
fireEvent.click(screen.getByText('надіслати'))
fireEvent.click(screen.getByText('скасувати'))
console.log('двічі «надіслати», потім «скасувати»:', status())
act(() => { vi.advanceTimersByTime(3000) })
console.log('через 3 секунди:', status())
```

```text
двічі «надіслати», потім «скасувати»: скасовано
через 3 секунди: надіслано
```

Перший таймер загубився, і зупинити його вже нікому. Користувач знову бачить «скасовано», а лист іде. Перед новим
запуском зупиняйте попередній таймер або забороняйте запускати другий, поки працює перший.

**Зникнення компонента.** Таймером керує браузер, а не React. Ось компонент, який запускає `setInterval`, а тест
вилучає компонент через три секунди:

```tsx
let ticks = 0 // Рахує спрацювання таймера.

function Ticker() {
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null)
  function start() {
    timerRef.current = setInterval(() => { ticks++ }, 1000)
  }
  return <button onClick={start}>запустити</button>
}
```

```tsx
vi.useFakeTimers()
const view = render(<Ticker />)
fireEvent.click(screen.getByText('запустити'))
vi.advanceTimersByTime(3000)
console.log('за 3 секунди спрацювань:', ticks)
view.unmount() // Компонент зникає зі сторінки.
vi.advanceTimersByTime(3000)
console.log('компонент прибрано, ще за 3 секунди:', ticks)
```

```text
за 3 секунди спрацювань: 3
компонент прибрано, ще за 3 секунди: 6
```

Функція продовжує спрацьовувати для компонента, якого вже немає. Обробник клацання цього не вирішить, бо жодного
клацання вже не буде. Прибрати таймер у момент зникнення компонента вміє ефект, і це одна з причин, навіщо ефекти
існують. Сьогодні досить знати, що ця проблема є й у вашому секундомірі.

Сторінка MDN про `setInterval` додає ще два факти для секундоміра. Функція повертає додатне ціле число, а
`setInterval` і `setTimeout` мають спільний набір ідентифікаторів, хоча для ясності зупиняти таймер варто функцією з
тієї самої пари. Також реальний проміжок між викликами може бути довшим за заданий, тому час не варто рахувати
кількістю спрацювань. Сторінка React будує секундомір на різниці двох моментів часу. Цього ми в браузері не заміряли.

## Ref і рецепт

Практика цього плану йде за рецептом книжки How to Design Programs. Рецепт вимагає прикладів із відомим результатом, а
вони можливі для функцій, які обчислюють значення. Ref і таймери є діями: вони змінюють щось поза функцією, тому їхній
результат не можна описати рівністю. Тому розділяйте. Те, що можна обчислити, наприклад перетворення мілісекунд на
рядок для екрана, винесіть у чисту функцію з прикладами. Те, що є дією, лишіть в обробнику й перевіряйте тестом
компонента, як у цій лекції: подія, штучний час, текст у документі.

## Типові хибні уявлення

**«Ref є заміною стану, просто без зайвих рендерів».** Ref не оновлює екран. Якщо значення показують, то його місце в
стані, і кнопка, у якій число не змінюється після клацання, це підтвердить.

**«Запис `<p>{ref.current}</p>` безпечний, бо я нічого не змінюю».** Читання під час рендеру теж порушує правило.
Компонент покаже значення з випадкової миті, а лінт повідомить про помилку `react-hooks/refs`.

**«У `ref.current` вузол є відразу, як я написав `ref={...}`».** Запис лише просить React покласти вузол під час
коміту. До коміту там `null`, а після вилучення елемента там теж `null`.

**«Після `setOpen(true)` елемент уже в документі».** Функція `set` просить рендер, а коміт відбудеться після кінця
обробника. Новий вузол з'явиться лише після нього або після `flushSync`.

**«Можна просто взяти `let` чи змінну модуля».** Змінна компонента зникає після кожного рендеру, а змінна модуля одна
на всі копії. Обидва запуски на початку лекції лишили лист, який пішов після скасування.

**«`ref` на власному компоненті дасть мені його вузол».** Він дасть вузол, лише якщо компонент передасть пропс `ref`
тегу. Інакше в `current` лишиться `null`, а під час виконання жодної помилки не буде.

**«Для `ref` у власному компоненті потрібен `forwardRef`».** У React 19 `ref` є звичайним пропсом.

**«Таймер зупиниться разом із компонентом».** Браузер не знає про компоненти, тому таймер працює далі, поки його не
зупинить код.

## Як це проявиться далі в React

- **День 16, синхронізація ефектами.** Ефект дає місце, де можна прочитати вузол без події й де є прибирання для
  таймера. Сьогоднішні запуски показують, навіщо воно потрібне.
- **День 19, залежності ефекту.** Об'єкт ref лишається тим самим між рендерами, тому він не запускає ефект знову, а
  зміна його поля лишається для React непомітною.
- **Фаза 3, день 15, доступність.** Перехід фокуса на заголовок після зміни екрана роблять тим самим викликом
  `focus()` через ref.
- **Графіки й інші сторонні бібліотеки.** Коли ви дійдете до бібліотеки, яка малює у власному елементі, цей елемент
  дасть ref, а її об'єкт теж зберігатиме ref, бо екран React від нього не залежить.

## Перевірте себе

**1. Компонент оголошує `let timerId = null`, обробник запуску записує туди ідентифікатор і викликає `set`. Чому
обробник зупинки бачить `null`?**

<details><summary>Відповідь</summary>

Виклик `set` запускає новий рендер, а кожен рендер створює власну змінну. Обробник зупинки належить новому рендеру й
читає його змінну, у якій знову `null`. Ідентифікатор лишився у змінній попереднього рендеру.

</details>

**2. Чому не покласти ідентифікатор таймера в стан, якщо це теж працює?**

<details><summary>Відповідь</summary>

Кожна зміна стану запускає рендер, а екран від ідентифікатора не залежить. У замірі кнопка, що перезапускає таймер,
давала чотири виклики компонента зі станом і один виклик із ref.

</details>

**3. У чому проблема цього запису: `const log = useRef(makeLog())`, якщо `makeLog` створює великий об'єкт? Як це
виправити?**

<details><summary>Відповідь</summary>

React використовує аргумент лише на першому рендері, але JavaScript викликає `makeLog` на кожному рендері, і результат
викидається. Виправлення полягає в тому, щоб почати з `useRef(null)` і створити об'єкт за перевіркою `if (log.current
=== null)`. Це єдиний запис у `current` під час рендеру, який дозволено.

</details>

**4. Обробник робить `setCount(count + 1)` і `ref.current = ref.current + 1`, а потім друкує обидва значення. Що він
побачить і чому?**

<details><summary>Відповідь</summary>

Він побачить старе значення `count` і нове значення `ref.current`. Змінна `count` є знімком цього рендеру, а
`ref.current` є полем звичайного об'єкта, запис у яке діє негайно.

</details>

**5. Лічильник у ref стоїть прямо в розмітці, і після клацання нічого не змінюється. Потім стан змінився, і число
стрибнуло. Чому це пастка, навіть якщо вигляд вас влаштовує?**

<details><summary>Відповідь</summary>

React не знає про зміну `ref.current`, тому показує значення з тієї миті, коли компонент випадково викликали. Це
читання під час рендеру, і лінт повідомляє про нього правилом `react-hooks/refs`. Для перевірки дня лічильник у ref
треба друкувати в обробнику, а на екрані показувати лише стан.

</details>

**6. Обробник робить `setOpen(true)` і відразу читає `panelRef.current`, а панель показується лише за умовою `open`.
Що там лежить? Що може це змінити?**

<details><summary>Відповідь</summary>

Там лежить `null`, бо `set` лише попросив рендер, а вузол з'являється під час коміту, який відбудеться після
обробника. Якщо загорнути `set` у `flushSync`, коміт відбудеться раніше, і наступний рядок побачить вузол. Також це
можна зробити в ref-колбеку чи в ефекті.

</details>

**7. Батько пише `<Field ref={r} />`, а `Field` приймає лише `label` і показує `<input />`. Що лежить у `r.current`
після показу? Чи буде помилка?**

<details><summary>Відповідь</summary>

Там лежить `null`. Під час виконання помилки немає, а компілятор дасть `TS2322`, бо в типі пропсів `Field` немає
`ref`. Компонент має прийняти `ref` як пропс і передати його в `<input ref={ref} />`.

</details>

**8. Що станеться з `setInterval`, якщо ідентифікатор лежить у ref, а компонент вилучили з екрана?**

<details><summary>Відповідь</summary>

Таймер продовжить спрацьовувати, бо ним керує браузер. У нашому запуску лічильник зріс із трьох до шести після
вилучення компонента. Зупинити такий таймер у момент зникнення компонента допоможе прибирання в ефекті, яке вивчає
тема «Синхронізація ефектами».

</details>

## Словничок лекції

| Слово | Що означає |
|-------|------------|
| ref, посилання | об'єкт `{ current: значення }`, який React зберігає між рендерами й зміну якого не помічає |
| ідентифікатор таймера | значення, яке повертає `setTimeout` чи `setInterval` і за яким таймер потім зупиняють |
| вузол DOM | об'єкт браузера, який представляє елемент сторінки |
| рендер | виклик функції компонента, який дає опис розмітки |
| коміт | запис результату рендеру в документ; саме тоді React заповнює `ref.current` |
| `flushSync` | функція, яка змушує React виконати рендер і коміт негайно |
| ref-колбек | функція в атрибуті `ref`, яку React викликає з вузлом, коли той з'являється |
| функція прибирання | функція, яку повертає ref-колбек; React викликає її, коли вузол зникає |
| `useImperativeHandle` | хук, який визначає, який об'єкт отримає батько замість вузла |

## Що читати далі

- [Розбір читання до цього дня](../reading/f1-d15-reading.md): що саме написано в матеріалах дня й де що шукати.
- Referencing Values with Refs і Manipulating the DOM with Refs: дві глави React, які ви читаєте сьогодні.
- useRef: довідник із застереженнями й записом про початкове значення.
- refs: сторінка правила лінту.
- Ref-колбек: розділ довідника про функцію в атрибуті `ref`.
- HTMLElement.focus(), Element.scrollIntoView() і setInterval(): сторінки MDN про браузерні функції дня.

---

Лекцію написано для цього плану. Вона спирається на документацію React, сторінки MDN і коротко згадує рецепт із книжки
How to Design Programs. Усе переказано своїми словами, а права на ці тексти належать їхнім авторам.
