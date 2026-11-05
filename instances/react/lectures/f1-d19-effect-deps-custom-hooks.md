# Лекція. Фаза 1, день 19. Залежності ефекту й власні хуки

Лекція з теми «Життєвий цикл ефекту й події поза ним» показала, що список залежностей описує код. Ця лекція пояснює,
що робити, коли такий список вас не влаштовує: як змінити код, щоб залежність зникла, чому вимкнений лінт лишає
помилку в коді й як винести ефект у власний хук. Читання займе близько 50 хвилин.

Приклади запущено на React 19.3 у Vitest під jsdom, тобто в імітації браузера всередині Node. Вивід під прикладами
справжній. Типи перевірено компілятором `tsc` версії 6.0, а лінт перевірено ESLint 10 із набором правил `react-hooks`
версії 7. У справжньому браузері приклади не запускалися, і біля тверджень про браузер сказано, на чому вони
тримаються.

Застереження про версію компілятора: у перших лекціях про TypeScript команда `tsc` мала версію 7, а в проєкті `spa`
вона має версію 6.0. Це вимушене обмеження через ESLint. ESLint читає файли TypeScript через пакет
`typescript-eslint`, а цей пакет у версії 8.72 працює лише з TypeScript, нижчим за 6.1. Тому версію TypeScript у `spa`
закріплено на 6.0. Коли `typescript-eslint` запрацює з TypeScript 7, обмеження можна буде зняти.

Практика дня просить прибрати об'єкт чи функцію зі списку залежностей у заготовці дня й написати хуки
`useOnlineStatus` і `useDebouncedValue`. Щоб не показувати готового розв'язку, лекція бере той самий канал служби доставки, що й
попередня лекція, а хуки пише інші: ширину вікна, зворотний відлік і читання каналу. Для відкладеного значення лекція
показує лише тест і поведінку, а коду самого хука не показує.

**Після лекції ви зможете пояснити:**

- чому об'єкт чи функція в списку запускають ефект після кожного рендеру, навіть якщо вміст той самий;
- чому список не обирають, а змінюють код;
- за якими п'ятьма запитаннями шукати спосіб прибрати залежність;
- як функція-оновлювач прибирає стан зі списку;
- чому коментар `eslint-disable` не прибирає помилку й що саме він робить із застарілими значеннями;
- що таке власний хук, чому важлива його назва і чим спільна логіка відрізняється від спільного стану;
- як передавати у власний хук значення й функції;
- як типізувати власний хук;
- чому хук `useMount` є поганою ідеєю і як лінт перевіряє власні хуки.

## Канал, який відкривається від кожної літери

Служба доставки, як і в попередній лекції, існує поза React, а справжньої мережі в прикладах немає. Усі досліди беруть
її функції з одного файлу. Функція `createTracking` створює канал, метод `open` відкриває його, `close` закриває, а
`onPosition` задає функцію, яку канал викличе при новій відстані. Функція `step` виконує одну дію тесту й друкує все,
що за цю дію потрапило в журнал. Функція `reportOpened` друкує, скільки разів канал відкрито від початку тесту.

```ts
// src/tracking.ts
export const SERVER = 'wss://delivery.example'

export type Options = { server: string; orderId: string }
type Listener = (km: number) => void

// Журнал збирає дії одного кроку тесту, а лічильник рахує відкриття каналу.
let journal: string[] = []
let openedCount = 0

export function say(line: string) {
  journal.push(line)
}

// Тут лежать усі канали, відкриті зараз.
const openChannels = new Set<Listener>()

export function createTracking({ orderId }: Options) {
  let listener: Listener = () => {}
  const deliver: Listener = (km) => listener(km)
  return {
    onPosition(callback: Listener) {
      listener = callback
    },
    open() {
      openedCount += 1
      openChannels.add(deliver)
      say(`відкрито ${orderId}`)
    },
    close() {
      openChannels.delete(deliver)
      say(`закрито ${orderId}`)
    },
  }
}

// Служба надсилає нову відстань усім відкритим каналам.
export function sendPosition(km: number) {
  openChannels.forEach((deliver) => deliver(km))
}

// Очищає журнал, виконує дію, друкує рядок і повертає результат дії.
export function step<T>(name: string, action: () => T): T {
  journal = []
  const result = action()
  console.log(`${name} | ${journal.join(', ')}`)
  return result
}

export function resetOpened() {
  openedCount = 0
}

export function reportOpened(name: string) {
  console.log(`${name} | відкрито разів: ${openedCount}`)
}
```

Компоненти й тести лекції лежать в одному файлі `src/deps.test.tsx`, а всі наступні приклади дописуються в нього ж.
Файл починається так:

```tsx
// src/deps.test.tsx
// @vitest-environment jsdom
import { useEffect, useEffectEvent, useMemo, useState } from 'react'
import { act, cleanup, fireEvent, render, renderHook, screen } from '@testing-library/react'
import { afterEach, beforeEach, test, vi } from 'vitest'
import {
  createTracking, reportOpened, resetOpened, say, sendPosition, SERVER, step, type Options,
} from './tracking'

// Прибирає компонент після кожного тесту, тому його канал не отримає чужих відстаней.
afterEach(cleanup)
// Кожен тест рахує відкриття каналу з нуля.
beforeEach(resetOpened)
```

Другий рядок файлу просить Vitest запускати його під jsdom. Команда
`npx vitest run src/deps.test.tsx --disable-console-intercept` запускає файл, а прапорець у кінці прибирає службові
рядки навколо `console.log`.

Перевірка дня шукає в теці `src` коментарі `eslint-disable`, а ця лекція показує такі коментарі навмисно. Тому
запускайте приклади лекції в окремій копії проєкту, а не в `spa`, де лежить ваша практика.

На сторінці кур'єра з'явилося поле нотатки. Канал тепер приймає об'єкт із налаштуваннями, тому зручно зібрати цей
об'єкт перед ефектом:

```tsx
function ObjectDep({ orderId }: { orderId: string }) {
  const [note, setNote] = useState('')
  const options = { server: SERVER, orderId }

  useEffect(() => {
    const tracking = createTracking(options)
    tracking.open()
    return () => tracking.close()
  }, [options])

  return <input aria-label="нотатка" value={note} onChange={(e) => setNote(e.target.value)} />
}
```

Список тут збігається з кодом: ефект читає `options`, і `options` стоїть у списку. Тест показує компонент і вводить у
поле три символи:

```tsx
// Вводить у поле нотатки три символи, кожен окремою подією.
function typeThree() {
  for (const value of ['к', 'ко', 'код']) {
    fireEvent.change(screen.getByLabelText('нотатка'), { target: { value } })
  }
}

test('об’єкт у залежностях', () => {
  render(<ObjectDep orderId="A-17" />)
  typeThree()
  reportOpened('об’єкт у залежностях, показ і три символи')
})
```

```text
об’єкт у залежностях, показ і три символи | відкрито разів: 4
```

Канал відкрито чотири рази: один раз під час показу й по одному разу після кожного символу. Замовлення при цьому не
змінювалося. Лекція «Значення й посилання» пояснила причину. Функція `Object.is` порівнює об'єкти за посиланням, тобто
за тим, чи це той самий об'єкт, а не за вмістом. Цей тест порівнює два об'єкти з однаковими полями й два однакові
рядки:

```tsx
test('порівняння', () => {
  const first = { server: SERVER, orderId: 'A-17' }
  const second = { server: SERVER, orderId: 'A-17' }
  console.log('той самий вміст, Object.is:', Object.is(first, second))
  console.log('той самий рядок, Object.is:', Object.is('A-17', 'A-17'))
})
```

```text
той самий вміст, Object.is: false
той самий рядок, Object.is: true
```

Кожна літера змінює стан `note`, стан запускає рендер, рендер заново виконує тіло компонента, і рядок
`const options = ...` створює новий об'єкт. Для React це змінена залежність. Те саме стосується функції, яку оголошено
в тілі компонента, бо функція теж є об'єктом:

```tsx
function FunctionDep({ orderId }: { orderId: string }) {
  const [note, setNote] = useState('')
  function buildOptions() {
    return { server: SERVER, orderId }
  }

  useEffect(() => {
    const tracking = createTracking(buildOptions())
    tracking.open()
    return () => tracking.close()
  }, [buildOptions])

  return <input aria-label="нотатка" value={note} onChange={(e) => setNote(e.target.value)} />
}

test('функція в залежностях', () => {
  render(<FunctionDep orderId="A-17" />)
  typeThree()
  reportOpened('функція в залежностях, показ і три символи')
})
```

```text
функція в залежностях, показ і три символи | відкрито разів: 4
```

Число те саме, що й для об'єкта: кожен рендер створив нову функцію `buildOptions`, і React побачив змінену залежність.

Лінт це помічає, але лише як попередження, і воно дуже точне. Покладіть компонент `ObjectDep` в окремий файл
`src/lint/ObjectDep.tsx`. Перед словом `function` допишіть `export`, а над компонентом поставте два рядки імпорту:
перший бере `useEffect` і `useState` з `react`, другий бере `createTracking` і `SERVER` з `../tracking`. Команда
`npx eslint src/lint/ObjectDep.tsx; echo "код завершення $?"` друкує шлях до файлу, а під ним такі рядки:

```text
  6:9  warning  The 'options' object makes the dependencies of useEffect Hook (at line 12) change on every render. Move it inside the useEffect callback. Alternatively, wrap the initialization of 'options' in its own useMemo() Hook  react-hooks/exhaustive-deps
✖ 1 problem (0 errors, 1 warning)
код завершення 0
```

Код завершення 0 означає, що для оболонки команда пройшла успішно. Отже, звичайний запуск лінту такий код не зупинить,
і попередження треба читати самому.

## Список описує код

Перша думка зазвичай така: «приберу `options` зі списку». Лінт не дасть цього зробити, і він має рацію, бо ефект читає
цей об'єкт. Сторінка `Removing Effect Dependencies` формулює правило: ви не обираєте залежності, бо список описує код.
Робота йде за колом:

1. Ви змінюєте код ефекту або те, як оголошено значення. 2. Ви записуєте в список те, що просить лінт, і список знову
збігається з кодом. 3. Якщо новий список вас не влаштовує, ви повертаєтеся до першого кроку.

Щоб прибрати залежність, треба довести лінту, що вона не потрібна. Глава пропонує п'ять запитань. Ми пройдемо кожне із
запуском.

| Запитання | Якщо так, то що робити |
|-----------|------------------------|
| Чи має цей код виконатися через певну дію користувача? | перенести код в обробник |
| Чи робить ефект кілька непов'язаних речей? | розділити на кілька ефектів |
| Чи читає ефект стан, щоб обчислити наступний стан? | передати функцію-оновлювач |
| Чи треба прочитати свіже значення, не реагуючи на нього? | винести читання в подію ефекту |
| Чи змінюється значення випадково, бо це об'єкт чи функція? | винести його з компонента, перенести в ефект або взяти з нього прості значення |

### Обробник замість ефекту

Форма надсилає заявку. Стан `sent` стає `true`, а ефект, який реагує на нього, показує сповіщення в поточній темі.
Тема реактивна, тому лінт вимагає записати її в список:

```tsx
function SignupEffect({ theme }: { theme: string }) {
  const [sent, setSent] = useState(false)
  useEffect(() => {
    if (sent) {
      say(`надіслано, сповіщення в темі ${theme}`)
    }
  }, [sent, theme])
  return <button onClick={() => setSent(true)}>надіслати</button>
}
```

Лінт більше не скаржиться. Другий компонент тримає той самий код у функції `handleClick`, яку викликає кнопка. Тест
клацає кнопку в кожному компоненті один раз, а потім двічі змінює тему:

```tsx
function SignupHandler({ theme }: { theme: string }) {
  function handleClick() {
    say(`надіслано, сповіщення в темі ${theme}`)
  }
  return <button onClick={handleClick}>надіслати</button>
}

function clickAndSwitch(Form: typeof SignupHandler, name: string) {
  const view = render(<Form theme="світла" />)
  step(name, () => {
    fireEvent.click(screen.getByRole('button'))
    view.rerender(<Form theme="темна" />)
    view.rerender(<Form theme="світла" />)
  })
}

test('заявка', () => {
  clickAndSwitch(SignupEffect, 'логіка в ефекті, клік і два перемикання теми')
  cleanup()
  clickAndSwitch(SignupHandler, 'логіка в обробнику, клік і два перемикання теми')
})
```

```text
логіка в ефекті, клік і два перемикання теми | надіслано, сповіщення в темі світла, надіслано, сповіщення в темі темна, надіслано, сповіщення в темі світла
логіка в обробнику, клік і два перемикання теми | надіслано, сповіщення в темі світла
```

У першому рядку заявку надіслано тричі: один раз після кліку й двічі після зміни теми. Другий рядок показує функцію
`handleClick`, яка спрацювала один раз: там немає списку, бо обробник не реактивний. Тема «Коли ефект не потрібен» уже
вчила переносити реакцію на клік в обробник, а цей запуск показує ще одну причину.

### Два ефекти замість одного

Каталог завантажує товари категорії й відгуки вибраного товару. Якщо обидва запити лежать в одному ефекті, список
містить обидва значення. Другий компонент розділяє запити на два ефекти. Тест змінює лише товар:

```tsx
type CatalogProps = { category: string; productId: number }

function OneEffect({ category, productId }: CatalogProps) {
  useEffect(() => {
    say(`/products?category=${category}`)
    say(`/reviews?product=${productId}`)
  }, [category, productId])
  return null
}

function TwoEffects({ category, productId }: CatalogProps) {
  useEffect(() => {
    say(`/products?category=${category}`)
  }, [category])
  useEffect(() => {
    say(`/reviews?product=${productId}`)
  }, [productId])
  return null
}

function changeProduct(Catalog: typeof OneEffect, name: string) {
  const view = render(<Catalog category="книжки" productId={1} />)
  step(name, () => view.rerender(<Catalog category="книжки" productId={2} />))
}

test('запити каталогу', () => {
  changeProduct(OneEffect, 'один ефект, змінився товар')
  cleanup()
  changeProduct(TwoEffects, 'два ефекти, змінився товар')
})
```

```text
один ефект, змінився товар | /products?category=книжки, /reviews?product=2
два ефекти, змінився товар | /reviews?product=2
```

Один ефект зробив зайвий запит до списку товарів. Два ефекти мають по власному списку й не заважають один одному.

### Функція-оновлювач замість читання стану

Сторінка веде історію відстаней. Функція в `onPosition` читає `history`, щоб дописати нове число, тому лінт вимагає
`history` у списку:

```tsx
function HistoryRead({ orderId }: { orderId: string }) {
  const [history, setHistory] = useState<number[]>([])

  useEffect(() => {
    const tracking = createTracking({ server: SERVER, orderId })
    tracking.onPosition((km) => {
      setHistory([...history, km])
    })
    tracking.open()
    return () => tracking.close()
  }, [orderId, history])

  return <p role="status">{history.join(' ')}</p>
}
```

Кожне нове число змінює `history`, а отже, перезапускає канал. Спробуємо прибрати `history` зі списку, вимкнувши лінт:

```tsx
function HistoryStale({ orderId }: { orderId: string }) {
  const [history, setHistory] = useState<number[]>([])

  useEffect(() => {
    const tracking = createTracking({ server: SERVER, orderId })
    tracking.onPosition((km) => {
      setHistory([...history, km])
    })
    tracking.open()
    return () => tracking.close()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [orderId])

  return <p role="status">{history.join(' ')}</p>
}
```

Тепер зробимо правильно, передавши оновлювач:

```tsx
function HistoryUpdater({ orderId }: { orderId: string }) {
  const [history, setHistory] = useState<number[]>([])

  useEffect(() => {
    const tracking = createTracking({ server: SERVER, orderId })
    tracking.onPosition((km) => {
      setHistory((previous) => [...previous, km])
    })
    tracking.open()
    return () => tracking.close()
  }, [orderId])

  return <p role="status">{history.join(' ')}</p>
}
```

Тест показує кожен із трьох компонентів і надсилає три відстані: 5, 4 і 3.

```tsx
function sendThree(History: typeof HistoryRead, name: string) {
  render(<History orderId="A-17" />)
  for (const km of [5, 4, 3]) {
    act(() => sendPosition(km))
  }
  console.log(`${name} | на екрані:`, screen.getByRole('status').textContent)
  reportOpened(name)
}

test('стан у залежностях', () => sendThree(HistoryRead, 'стан у залежностях'))
test('стан без залежності', () => sendThree(HistoryStale, 'стан без залежності'))
test('оновлювач', () => sendThree(HistoryUpdater, 'оновлювач'))
```

```text
стан у залежностях | на екрані: 5 4 3
стан у залежностях | відкрито разів: 4
стан без залежності | на екрані: 3
стан без залежності | відкрито разів: 1
оновлювач | на екрані: 5 4 3
оновлювач | відкрито разів: 1
```

Лише оновлювач дав обидва правильні результати. Варіант із вимкненим лінтом загубив дві відстані, бо функція назавжди
бачить порожню `history` першого рендеру. Лекція «Рендер, коміт і знімок стану» пояснила, що **оновлювач** є функцією,
яку ви передаєте у `set` і яка отримує попереднє значення. Ефект його більше не читає, тому залежність зникає.

Коли стан у списку ще й змінюється самим ефектом, виходить нескінченний цикл: ефект ставить стан, стан запускає
рендер, рендер змінює залежність, і ефект запускається знову. Щоб дочекатися кінця тесту, цей компонент обмежує цикл
двома сотнями кроків:

```tsx
let loopCalls = 0

function Loop() {
  const [n, setN] = useState(0)
  loopCalls += 1

  useEffect(() => {
    // Умова потрібна лише для того, щоб тест закінчився.
    if (n < 200) {
      setN(n + 1)
    }
  }, [n])

  return null
}

test('цикл', () => {
  // Перехоплює застереження React, щоб надрукувати лише його початок.
  const errors = vi.spyOn(console, 'error').mockImplementation(() => {})
  let thrown = 'нічого'
  try {
    render(<Loop />)
  } catch (error) {
    thrown = String(error)
  }
  console.log(`цикл із межею 200 | викликів компонента: ${loopCalls} | кинуто: ${thrown}`)
  console.log('цикл із межею 200 | console.error:', String(errors.mock.calls[0]?.[0]).slice(0, 60))
  errors.mockRestore()
})
```

```text
цикл із межею 200 | викликів компонента: 201 | кинуто: нічого
цикл із межею 200 | console.error: Maximum update depth exceeded. This can happen when a compon
```

Перший рядок показує, що React викликав компонент 201 раз і не кинув помилки: один виклик дав перший показ, а двісті
дав цикл. Другий рядок показує початок застереження, яке React надрукував, не зупиняючи цикл. Якщо прибрати умову
`if (n < 200)`, межі в циклу немає, і тест сам не завершується. У нашому запуску процес мав обмеження пам'яті 1,5
гігабайта, бо запускався з `NODE_OPTIONS=--max-old-space-size=1500`, і приблизно за хвилину впав з помилкою
`JavaScript heap out of memory`. Отже, застереження React від цього циклу не рятує, і такий ефект треба виправляти в
коді.

Лінт ловить такий код раніше правилом `react-hooks/set-state-in-effect`, про яке йшлося в темі «Коли ефект не
потрібен». У браузері цього ми не запускали. Сторінка React описує ту саму помилку як нескінченний цикл.

### Подія ефекту замість реакції

Цей випадок повністю розібрала лекція з теми «Життєвий цикл ефекту й події поза ним», тому тут лише нагадування.
Значення, яке треба прочитати свіжим, але не реагувати на нього, читає функція від `useEffectEvent`. Глава додає ще
один варіант: якщо компонент отримав пропсом функцію-обробник і батько щоразу передає нову, ефект викликає її через
подію ефекту. Запуск цього випадку є нижче, у власному хуку.

### Об'єкт чи функція

Тепер повернімося до нашого поля нотатки. Глава дає чотири способи, а обирати між ними допомагає запитання, звідки
беруться дані об'єкта.

**Об'єкт залежить від пропсів чи стану.** Перенесіть його створення всередину ефекту:

```tsx
function ObjectInside({ orderId }: { orderId: string }) {
  const [note, setNote] = useState('')

  useEffect(() => {
    const options = { server: SERVER, orderId }
    const tracking = createTracking(options)
    tracking.open()
    return () => tracking.close()
  }, [orderId])

  return <input aria-label="нотатка" value={note} onChange={(e) => setNote(e.target.value)} />
}

test('об’єкт в ефекті', () => {
  const view = render(<ObjectInside orderId="A-17" />)
  typeThree()
  reportOpened('об’єкт в ефекті, показ і три символи')
  step('об’єкт в ефекті, перехід на B-42', () => view.rerender(<ObjectInside orderId="B-42" />))
})
```

```text
об’єкт в ефекті, показ і три символи | відкрито разів: 1
об’єкт в ефекті, перехід на B-42 | закрито A-17, відкрито B-42
```

Це той результат, який ми хотіли: літери не перепідключають канал, а зміна замовлення перепідключає. Об'єкт зник зі
списку, а його місце зайняв рядок `orderId`, який порівнюється за значенням. Функцію, яка потрібна лише ефекту,
переносять так само. Об'єкт, створений усередині ефекту, більше не є значенням рендеру, тому він не реактивний.

**Об'єкт не залежить ні від чого.** Винесіть його поза компонент, і тоді рендер його не створює наново:

```tsx
const FIXED_OPTIONS = { server: SERVER, orderId: 'A-17' }

function ObjectOutside() {
  const [note, setNote] = useState('')

  useEffect(() => {
    const tracking = createTracking(FIXED_OPTIONS)
    tracking.open()
    return () => tracking.close()
  }, [])

  return <input aria-label="нотатка" value={note} onChange={(e) => setNote(e.target.value)} />
}

test('об’єкт поза компонентом', () => {
  render(<ObjectOutside />)
  typeThree()
  reportOpened('об’єкт поза компонентом, показ і три символи')
})
```

```text
об’єкт поза компонентом, показ і три символи | відкрито разів: 1
```

Канал відкрито один раз, бо ефект не читає жодного реактивного значення, і список порожній.

**Об'єкт приходить пропсом.** Батько може створювати його під час свого рендеру, і дочірній компонент на це не
впливає. Перший компонент нижче записує в список сам об'єкт. Другий компонент дістає прості значення до ефекту й
записує в список саме їх:

```tsx
function PropObject({ options }: { options: Options }) {
  useEffect(() => {
    const tracking = createTracking(options)
    tracking.open()
    return () => tracking.close()
  }, [options])

  return null
}

function PropFields({ options }: { options: Options }) {
  const { server, orderId } = options

  useEffect(() => {
    const tracking = createTracking({ server, orderId })
    tracking.open()
    return () => tracking.close()
  }, [server, orderId])

  return null
}

// Кожен запис options={{ ... }} створює новий об'єкт, як це робить батько під час рендеру.
function threeRenders(Child: typeof PropObject) {
  const view = render(<Child options={{ server: SERVER, orderId: 'A-17' }} />)
  view.rerender(<Child options={{ server: SERVER, orderId: 'A-17' }} />)
  view.rerender(<Child options={{ server: SERVER, orderId: 'A-17' }} />)
  return view
}

test('об’єкт із пропса', () => {
  threeRenders(PropObject)
  reportOpened('об’єкт із пропса, три рендери батька')
})

test('поля з пропса', () => {
  const view = threeRenders(PropFields)
  reportOpened('поля з пропса, три рендери батька')
  step('поля з пропса, справді інше замовлення', () =>
    view.rerender(<PropFields options={{ server: SERVER, orderId: 'B-42' }} />),
  )
})
```

```text
об’єкт із пропса, три рендери батька | відкрито разів: 3
поля з пропса, три рендери батька | відкрито разів: 1
поля з пропса, справді інше замовлення | закрито A-17, відкрито B-42
```

Код трохи повторюється, зате видно, від чого ефект справді залежить. **Функція приходить пропсом** за тією самою
логікою: чисту функцію викликають до ефекту й читають її результат. Обробник події не викликають під час рендеру, тому
його загортають у подію ефекту.

**А як щодо `useMemo`?** Попередження лінту пропонує загорнути об'єкт у цей хук. Він запам'ятовує об'єкт, поки його
вхідні значення не зміняться, і наш запуск справді дав один запуск ефекту:

```tsx
function ObjectMemo({ orderId }: { orderId: string }) {
  const [note, setNote] = useState('')
  const options = useMemo(() => ({ server: SERVER, orderId }), [orderId])

  useEffect(() => {
    const tracking = createTracking(options)
    tracking.open()
    return () => tracking.close()
  }, [options])

  return <input aria-label="нотатка" value={note} onChange={(e) => setNote(e.target.value)} />
}

test('useMemo', () => {
  render(<ObjectMemo orderId="A-17" />)
  typeThree()
  reportOpened('useMemo, показ і три символи')
})
```

```text
useMemo, показ і три символи | відкрито разів: 1
```

Попередження називає цей спосіб запасним. Простіше перенести об'єкт в ефект, бо тоді в списку лишається лише те, що
ефект справді використовує. План розбирає `useMemo` і `useCallback` у фазі 2, у дні «Мемоізація і React Compiler».

## Чому коментар не прибирає помилку

Тепер подивімося на найгірший спосіб розв'язати проблему зі списком. Лічильник щосекунди додає крок до суми:

```tsx
function Elapsed({ step }: { step: number }) {
  const [total, setTotal] = useState(0)
  function tick() {
    setTotal(total + step)
  }

  useEffect(() => {
    const id = setInterval(tick, 1000)
    return () => clearInterval(id)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return <p role="status">{total}</p>
}
```

Автор хотів один інтервал, тому поставив порожній масив і заглушив лінт. Тест чекає п'ять секунд, змінює крок на 10 і
чекає ще п'ять. Функція `vi.useFakeTimers` підміняє таймери, тому тест пересуває час вручну й не чекає насправді:

```tsx
function tenSeconds(Counter: typeof Elapsed, name: string) {
  vi.useFakeTimers()
  const view = render(<Counter step={1} />)
  act(() => {
    vi.advanceTimersByTime(5000)
  })
  console.log(`${name} | через 5 секунд на екрані:`, screen.getByRole('status').textContent)
  view.rerender(<Counter step={10} />)
  act(() => {
    vi.advanceTimersByTime(5000)
  })
  console.log(`${name} | ще через 5 секунд із кроком 10:`, screen.getByRole('status').textContent)
  vi.useRealTimers()
}

test('вимкнений лінт', () => tenSeconds(Elapsed, 'вимкнений лінт'))
```

```text
вимкнений лінт | через 5 секунд на екрані: 1
вимкнений лінт | ще через 5 секунд із кроком 10: 1
```

Ось що сталося крок за кроком.

| Крок | Хто діє | Що відбувається |
|------|---------|-----------------|
| 1 | React | викликає компонент, створює `tick`, у цьому рендері `total` = 0 і `step` = 1 |
| 2 | ефект | передає в `setInterval` функцію `tick` першого рендеру |
| 3 | таймер, перша секунда | викликає `tick`, той викликає `setTotal(0 + 1)` |
| 4 | React | новий рендер, нова `tick`, але ефект не запускається, бо список порожній |
| 5 | таймер, друга секунда | викликає ту саму `tick` першого рендеру, той знову просить `setTotal(0 + 1)` |
| 6 | React | бачить те саме значення 1, і на екрані лишається 1 |

Це поведінка замикання, яку показала лекція «Функції та замикання»: функція пам'ятає змінні того рендеру, у якому її
створено, а застаріле значення виникає, коли функція пережила цей рендер. Коментар нічого не змінив у цій логіці. Він
лише заборонив інструменту сказати про це. Правильний запис поєднує оновлювач і подію ефекту:

```tsx
function ElapsedFixed({ step }: { step: number }) {
  const [total, setTotal] = useState(0)
  const onTick = useEffectEvent(() => {
    setTotal((previous) => previous + step)
  })

  useEffect(() => {
    const id = setInterval(() => onTick(), 1000)
    return () => clearInterval(id)
  }, [])

  return <p role="status">{total}</p>
}

test('подія ефекту', () => tenSeconds(ElapsedFixed, 'подія ефекту'))
```

```text
подія ефекту | через 5 секунд на екрані: 5
подія ефекту | ще через 5 секунд із кроком 10: 55
```

За перші п'ять секунд сума дійшла до 5, а наступні п'ять секунд додали по 10, тому вийшло 55. Отже, інтервал лишився
один, а функція щоразу бачить свіжий крок. Лінт не знаходить у цьому коді проблем. Сторінка React радить ставитися до
цього попередження так, як до помилки компіляції.

### Друга шкода коментаря

Коментар дає і другу шкоду. Він вимикає правило для рядка зі списком цього ефекту, тому нове значення, яке хтось
допише сюди через місяць, теж лишиться без попередження. Ось такий випадок: ефект читає `orderId`, а список порожній.

```tsx
// src/lint/Suppressed.tsx
import { useEffect } from 'react'
import { createTracking, SERVER } from '../tracking'

export function Suppressed({ orderId }: { orderId: string }) {
  useEffect(() => {
    const tracking = createTracking({ server: SERVER, orderId })
    tracking.open()
    return () => tracking.close()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return null
}
```

Команда `npx eslint src/lint/Suppressed.tsx` нічого не друкує, бо коментар вимкнув правило для цього рядка. Тому
перевірка дня просить знайти в проєкті такі коментарі пошуком. Команда `grep -rn "eslint-disable" src/lint` друкує
файл, номер рядка й сам коментар:

```text
src/lint/Suppressed.tsx:10:    // eslint-disable-next-line react-hooks/exhaustive-deps
```

Є ще два корисні запуски ESLint. Параметр `--no-inline-config` ігнорує всі такі коментарі й показує приховані
попередження. Команда `npx eslint src/lint/Suppressed.tsx --no-inline-config` друкує шлях до файлу, а під ним такі
рядки:

```text
  11:6  warning  React Hook useEffect has a missing dependency: 'orderId'. Either include it or remove the dependency array  react-hooks/exhaustive-deps
✖ 1 problem (0 errors, 1 warning)
```

А коментар, який більше нічого не приховує, сам дає попередження, бо ESLint за замовчуванням повідомляє про непотрібні
директиви. У цьому файлі `orderId` уже стоїть у списку, тому коментарю нічого приховувати:

```tsx
// src/lint/Unused.tsx
import { useEffect } from 'react'
import { createTracking, SERVER } from '../tracking'

export function Unused({ orderId }: { orderId: string }) {
  useEffect(() => {
    const tracking = createTracking({ server: SERVER, orderId })
    tracking.open()
    return () => tracking.close()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [orderId])

  return null
}
```

Команда `npx eslint src/lint/Unused.tsx` друкує шлях до файлу, а під ним такі рядки:

```text
  10:5  warning  Unused eslint-disable directive (no problems were reported from 'react-hooks/exhaustive-deps')
✖ 1 problem (0 errors, 1 warning)
  0 errors and 1 warning potentially fixable with the `--fix` option.
```

Усі ці попередження не зупиняють команду: вона завершується кодом 0. Параметр `--max-warnings 0` перетворює
попередження на провал команди. Команда `npx eslint src/lint/Unused.tsx --max-warnings 0; echo "код завершення $?"`
наприкінці друкує такі рядки:

```text
ESLint found too many warnings (maximum: 0).
код завершення 1
```

Отже, у перевірці запускайте лінт із цим параметром, інакше жодне попередження її не зупинить.

## Власний хук

Сторінка показує ширину вікна на лінійці, а макет обирає вузький чи широкий вигляд за цією самою шириною. Кожному
компоненту потрібні той самий стан і той самий ефект. Логіку можна скопіювати, але її можна й винести. **Власний хук**
є функцією, назва якої починається з `use` і великої літери і яка сама викликає інші хуки:

```tsx
function useWindowWidth(): number {
  const [width, setWidth] = useState(window.innerWidth)

  useEffect(() => {
    function handleResize() {
      setWidth(window.innerWidth)
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return width
}
function Ruler() {
  const width = useWindowWidth()
  return <p role="status">Ширина: {width}</p>
}
function Layout() {
  const width = useWindowWidth()
  return <p role="status">{width < 600 ? 'Вузький макет' : 'Широкий макет'}</p>
}
```

Код компонента тепер каже, що він хоче, а не як це робиться: він хоче ширину, а про підписку знає лише хук. Подія
`resize` є браузерною подією зміни розміру вікна. Функцію `handleResize` оголошено всередині ефекту, тому вона не
стоїть у списку, а саме цей прийом ви щойно бачили на об'єкті. Тест показує обидва компоненти, змінює ширину вікна й
прибирає компоненти:

```tsx
// Збирає текст усіх елементів із role="status" в один рядок.
function statusTexts() {
  return screen.getAllByRole('status').map((element) => element.textContent).join(' | ')
}

test('ширина вікна', () => {
  // Функція vi.spyOn записує кожен виклик методу вікна, а сам метод працює, як і раніше.
  const added = vi.spyOn(window, 'addEventListener')
  const removed = vi.spyOn(window, 'removeEventListener')
  const countResize = (calls: unknown[][]) => calls.filter((call) => call[0] === 'resize').length

  const view = render(<><Ruler /><Layout /></>)
  console.log('підписок на resize:', countResize(added.mock.calls))
  console.log('показ |', statusTexts())

  window.innerWidth = 500
  fireEvent(window, new Event('resize'))
  console.log('після зміни вікна |', statusTexts())

  view.unmount()
  console.log('після зникнення, відписок від resize:', countResize(removed.mock.calls))
  vi.restoreAllMocks()
})
```

```text
підписок на resize: 2
показ | Ширина: 1024 | Широкий макет
після зміни вікна | Ширина: 500 | Вузький макет
після зникнення, відписок від resize: 2
```

Значення 1024 є значенням jsdom за замовчуванням. У браузері там буде справжня ширина вікна, але цього ми не
запускали. Подію `resize` тест надіслав сам, змінивши перед тим `window.innerWidth`.

### Чому назва важлива

Назва на `use` є домовленістю, яку перевіряє лінт. Вона каже читачеві, що всередині може бути стан чи ефект, а отже,
цю функцію не можна викликати в умові чи циклі. Перейменуємо хук на `getWindowWidth`, подивимося також на маленьку
літеру й додамо функцію `useSorted`, яка не викликає хуків:

```ts
// src/lint/names.ts
import { useState } from 'react'

export function getWindowWidth() {
  const [width] = useState(window.innerWidth)
  return width
}

export function usewidth() {
  const [width] = useState(window.innerWidth)
  return width
}

export function useSorted(items: number[]) {
  return [...items].sort((a, b) => a - b)
}
```

Команда `npx eslint src/lint/names.ts` друкує шлях до файлу, а під ним такі рядки:

```text
   5:19  error  React Hook "useState" is called in function "getWindowWidth" that is neither a React function component nor a custom React Hook function. React component names must start with an uppercase letter. React Hook names must start with the word "use"  react-hooks/rules-of-hooks
  10:19  error  React Hook "useState" is called in function "usewidth" that is neither a React function component nor a custom React Hook function. React component names must start with an uppercase letter. React Hook names must start with the word "use"        react-hooks/rules-of-hooks
✖ 2 problems (2 errors, 0 warnings)
```

Правило справді вимагає великої літери після `use`, тому `usewidth` воно не приймає. Обернене правило лінт не
перевіряє: функція `useSorted`, яка не викликає хуків, помилки не дала. Сторінка React усе одно радить таку функцію
назвати `getSorted`. Вона не потребує обмежень хука, і її можна викликати в умові.

### Спільна логіка, а не спільний стан

У запуску вище обидва компоненти змінилися одночасно, тому легко вирішити, що в них один стан. Це не так. Рядок
`підписок на resize: 2` показує дві окремі підписки. Значення збіглися, бо обидва хуки читають одне вікно. Щоб
побачити різницю, потрібен хук, який має різні вхідні дані:

```tsx
function useCountdown(seconds: number): number {
  const [left, setLeft] = useState(seconds)

  useEffect(() => {
    const id = setInterval(() => {
      setLeft((current) => Math.max(current - 1, 0))
    }, 1000)
    return () => clearInterval(id)
  }, [])

  return left
}
function Offer({ name, seconds }: { name: string; seconds: number }) {
  const left = useCountdown(seconds)
  return <p role="status">{name}: {left}</p>
}

test('відлік', () => {
  vi.useFakeTimers()
  const view = render(<><Offer name="знижка" seconds={10} /><Offer name="доставка" seconds={30} /></>)
  console.log('на старті |', statusTexts())
  act(() => {
    vi.advanceTimersByTime(4000)
  })
  console.log('через 4 секунди |', statusTexts())
  view.rerender(<><Offer name="знижка" seconds={60} /><Offer name="доставка" seconds={60} /></>)
  console.log('новий аргумент 60 |', statusTexts())
  vi.useRealTimers()
})
```

Перші два рядки виводу такі:

```text
на старті | знижка: 10 | доставка: 30
через 4 секунди | знижка: 6 | доставка: 26
```

Кожен виклик хука має власний стан і власний ефект, ніби ви написали `useState` і `useEffect` прямо в компоненті. Це
та сама поведінка, що й до винесення. Хук ділиться кодом, а не даними. Якщо компонентам потрібен один стан, його
піднімають до спільного батька, як пояснила лекція «Спільний стан і скидання стану», або передають через контекст.

Цей запуск показує ще одну межу. Останній крок тесту змінює аргумент хука на 60, і третій рядок виводу такий:

```text
новий аргумент 60 | знижка: 6 | доставка: 26
```

Нічого не змінилося. Аргумент `useState` діє лише на першому рендері, про що йшлося в лекції «Події й стан», а в
ефекті `seconds` не читається. Для цього хука така поведінка прийнятна, бо відлік починається один раз. Якщо ж ваш хук
має відстежувати значення, яке приходить аргументом, то це значення має читати ефект, а отже, воно стоятиме в списку
залежностей хука.

### Хук виконується разом із компонентом

Тіло власного хука є частиною тіла компонента. Цей тест записує в журнал кожне виконання обох тіл:

```tsx
function useTrace(value: string) {
  say(`тіло хука: ${value}`)
  return value
}

function Traced({ value }: { value: string }) {
  say('тіло компонента')
  useTrace(value)
  return null
}

test('тіло хука', () => {
  step('два рендери', () => {
    const view = render(<Traced value="а" />)
    view.rerender(<Traced value="аб" />)
  })
})
```

```text
два рендери | тіло компонента, тіло хука: а, тіло компонента, тіло хука: аб
```

Із цього випливають два наслідки. Перший наслідок: код хука має бути таким самим чистим, як код компонента, адже він
виконується під час рендеру. Другий наслідок: хук завжди отримує свіжі значення. Сторінка
`Reusing Logic with Custom Hooks` показує це на ланцюжку, де результат одного хука стає аргументом іншого, і при зміні
першого другий отримує нове значення під час того самого рендеру.

### Хук, який отримує функцію

Хук каналу добре приймати номер замовлення й функцію, яка реагує на відстань. Перша спроба записує обидва значення в
список:

```tsx
function useTrackingBad(orderId: string, onPosition: (km: number) => void) {
  useEffect(() => {
    const tracking = createTracking({ server: SERVER, orderId })
    tracking.onPosition(onPosition)
    tracking.open()
    return () => tracking.close()
  }, [orderId, onPosition])
}
```

Компонент передає функцію прямо в аргументі, тому кожен рендер дає нову функцію, і ми знову прийшли до знайомої
проблеми. Виправлення загортає отриману функцію в подію ефекту всередині хука:

```tsx
function useTracking(orderId: string, onPosition: (km: number) => void) {
  const handlePosition = useEffectEvent(onPosition)

  useEffect(() => {
    const tracking = createTracking({ server: SERVER, orderId })
    tracking.onPosition((km) => {
      handlePosition(km)
    })
    tracking.open()
    return () => tracking.close()
  }, [orderId])
}
function Page({ units }: { units: string }) {
  useTracking('A-17', (km) => say(`${km} ${units}`))
  return null
}
function PageBad({ units }: { units: string }) {
  useTrackingBad('A-17', (km) => say(`${km} ${units}`))
  return null
}

test('хук без події ефекту', () => {
  const view = render(<PageBad units="км" />)
  view.rerender(<PageBad units="км" />)
  view.rerender(<PageBad units="милі" />)
  reportOpened('хук без події ефекту, три рендери')
})

test('хук із подією ефекту', () => {
  const view = render(<Page units="км" />)
  view.rerender(<Page units="км" />)
  view.rerender(<Page units="милі" />)
  reportOpened('хук із подією ефекту, три рендери')
  step('хук із подією ефекту, позиція', () => act(() => sendPosition(5)))
})
```

```text
хук без події ефекту, три рендери | відкрито разів: 3
хук із подією ефекту, три рендери | відкрито разів: 1
хук із подією ефекту, позиція | 5 милі
```

Компонент передав нові `units`, канал лишився відкритим, і сповіщення показало найновіші одиниці. Подію ефекту створює
сам хук. Передати хуку вже готову подію не можна, про що повідомляє лінт, як показала попередня лекція.

### Типи власного хука

Хук є звичайною функцією TypeScript, тому параметри типізують як завжди. Результат TypeScript виводить сам, а явний
запис `: number` зручний, бо робить результат частиною контракту, тобто описом того, що хук обіцяє. Якщо хук працює з
різними типами, допомагає дженерик, який пояснила лекція «TypeScript: дженерики». Функції `subscribeChannel` і
`sendToChannel` нижче імітують окремий канал повідомлень, який передає рядки:

```tsx
const channelListeners = new Map<string, Set<(raw: string) => void>>()

function subscribeChannel(channelId: string, listener: (raw: string) => void) {
  const listeners = channelListeners.get(channelId) ?? new Set()
  channelListeners.set(channelId, listeners)
  listeners.add(listener)
  return () => {
    listeners.delete(listener)
  }
}

function sendToChannel(channelId: string, raw: string) {
  channelListeners.get(channelId)?.forEach((listener) => listener(raw))
}

function useChannelValue<T>(channelId: string, parse: (raw: string) => T): T | null {
  const [value, setValue] = useState<T | null>(null)
  const onMessage = useEffectEvent((raw: string) => {
    setValue(parse(raw))
  })

  useEffect(() => {
    return subscribeChannel(channelId, (raw) => onMessage(raw))
  }, [channelId])

  return value
}
function Prices() {
  const price = useChannelValue('ціна', Number)
  const tags = useChannelValue('ціна', (raw) => raw.split('.'))
  return <p role="status">{price === null ? 'немає' : price.toFixed(2)} {tags?.length}</p>
}

test('дженерик', () => {
  render(<Prices />)
  console.log('дженерик, показ |', screen.getByRole('status').textContent)
  act(() => sendToChannel('ціна', '19.5'))
  console.log('дженерик, повідомлення |', screen.getByRole('status').textContent)
})
```

```text
дженерик, показ | немає 
дженерик, повідомлення | 19.50 2
```

Спершу значення немає, тому `price` дорівнює `null`, а `tags?.length` не дає тексту. Після повідомлення `19.5` перший
виклик хука повертає число, а другий повертає масив із двох частин.

Компілятор вивів `T` із функції `parse`: для `Number` результат має тип `number | null`, а для другого виклику
`string[] | null`. Допишіть у тіло `Prices` рядок `const wrong: string | null = price` або виклик `price.toFixed(2)`
без перевірки, і команда `npx tsc --noEmit -p tsconfig.app.json` після шляху до файлу надрукує такі помилки:

```text
error TS2322: Type 'number | null' is not assignable to type 'string | null'.
  Type 'number' is not assignable to type 'string'.
error TS18047: 'price' is possibly 'null'.
```

Ще одна пастка стосується хуків, які повертають масив на кшталт `useState`. Запис `return [on, toggle]` дає тип
масиву, де кожен елемент може бути і прапорцем, і функцією:

```tsx
// src/lint/toggle.tsx
import { useState } from 'react'

function useToggle() {
  const [on, setOn] = useState(false)
  const toggle = () => setOn((current) => !current)
  return [on, toggle]
}

export function Switch() {
  const [on, toggle] = useToggle()
  return <button onClick={toggle}>{on ? 'увімкнено' : 'вимкнено'}</button>
}
```

Команда `npx tsc --noEmit -p tsconfig.app.json` після шляху до файлу друкує таку помилку:

```text
error TS2322: Type 'boolean | (() => void)' is not assignable to type 'MouseEventHandler<HTMLButtonElement> | undefined'.
  Type 'boolean' is not assignable to type 'MouseEventHandler<HTMLButtonElement>'.
```

Запис `return [on, toggle] as const` виправляє це, бо дає кортеж, тобто масив із відомим типом кожної позиції.
Перевірка `tsc` після такої правки цього рядка більше не згадує.

### Відкладене значення: що саме має відбуватися

Практика просить хук `useDebouncedValue`. **Відкладене значення** працює так: хук отримує значення, яке часто
змінюється, і повертає його лише тоді, коли воно якийсь час лишалося незмінним. Типовий випадок є рядком пошуку:
шукати варто не після кожної літери, а коли людина перестала друкувати. Англійською таку поведінку називають debounce.

Ми написали власну реалізацію для перевірки, але не показуємо її, бо це ваше завдання. Людина вводить `к` на 0-й
мілісекунді, `ки` на 100-й і `киї` на 200-й, а затримка становить 300 мілісекунд. Тест кожні 100 мілісекунд дивиться на
екран і записує в журнал кожне нове значення. Цей тест не показує, як написано хук. Коли ви напишете власний хук,
покладіть його в копію проєкту поруч із тестом, і тест надрукує такий самий журнал:

```tsx
// src/debounce.test.tsx
// @vitest-environment jsdom
import { act, cleanup, render, screen } from '@testing-library/react'
import { afterEach, test, vi } from 'vitest'
import { useDebouncedValue } from './useDebouncedValue'

// Назва реалізації, яка стоїть на початку рядка журналу.
const LABEL = 'із прибиранням'
const TYPED = new Map([[0, 'к'], [100, 'ки'], [200, 'киї']])

afterEach(cleanup)

function Shown({ value, delayMs }: { value: string; delayMs: number }) {
  const shown = useDebouncedValue(value, delayMs)
  return <p role="status">{shown}</p>
}

test('журнал екрана', () => {
  vi.useFakeTimers()
  const view = render(<Shown value="" delayMs={300} />)
  const journal: string[] = []
  let last = ''
  for (let ms = 0; ms <= 600; ms += 100) {
    const typed = TYPED.get(ms)
    if (typed) {
      view.rerender(<Shown value={typed} delayMs={300} />)
    }
    const text = screen.getByRole('status').textContent
    if (text !== last) {
      journal.push(`${ms} мс «${text}»`)
      last = text ?? ''
    }
    act(() => {
      vi.advanceTimersByTime(100)
    })
  }
  console.log(`${LABEL} | ${journal.join(', ')}`)
  vi.useRealTimers()
})
```

Ми запустили цей тест для двох власних реалізацій, і різниця між ними полягає лише в прибиранні в ефекті:

```text
із прибиранням | 500 мс «киї»
без прибирання | 300 мс «к», 400 мс «ки», 500 мс «киї»
```

Перший журнал є потрібною поведінкою: одне значення через 300 мілісекунд після останньої зміни. Другий журнал лише
відкладає кожне значення окремо. Він лишає всі три запити до сервера, тому пошук не став економнішим. Лекція з теми
«Синхронізація ефектами» пояснює, коли React викликає прибирання. Вправа `Implement a staggering movement` на сторінці
React навмисно потребує саме другої поведінки, тому її розв'язок не підходить для вашого завдання.

Два компоненти з різними значеннями й затримками 300 і 800 мілісекунд поводяться незалежно. Наступний тест лежить у
тому самому файлі й показує обидва значення окремими елементами:

```tsx
test('два виклики', () => {
  vi.useFakeTimers()
  const view = render(<><Shown value="" delayMs={300} /><Shown value="" delayMs={800} /></>)
  view.rerender(<><Shown value="кава" delayMs={300} /><Shown value="чай" delayMs={800} /></>)
  const texts = () => screen.getAllByRole('status').map((element) => element.textContent).join(' | ')
  act(() => {
    vi.advanceTimersByTime(300)
  })
  console.log('через 300 мс |', texts())
  act(() => {
    vi.advanceTimersByTime(500)
  })
  console.log('через 800 мс |', texts())
  vi.useRealTimers()
})
```

```text
через 300 мс | кава | 
через 800 мс | кава | чай
```

Через 300 мілісекунд перший компонент уже показує `кава`, а другий ще чекає своєї паузи. Отже, кожен виклик хука має
власний таймер, і компоненти один одному не заважають.

### Хук `useMount` і межі лінту

Не кожне повторення варто виносити. Сторінка каже, що хук навколо одного `useState` зазвичай зайвий, зате майже кожен
ефект добре виглядає всередині хука. Ім'я хука має називати конкретну справу: `useWindowWidth`, `useChatRoom`. Назви
`useMount` чи `useEffectOnce` описують лише час запуску, і саме про такі хуки сторінка попереджає окремо:

```ts
// src/lint/mount.ts
import { useEffect } from 'react'

export function useMount(fn: () => void) {
  useEffect(() => {
    fn()
  }, [])
}
```

Лінт бачить проблему всередині хука, а компонент, який викликає такий хук і читає в ньому пропс, лишається без жодного
попередження. Ось такий компонент:

```tsx
// src/lint/MountUser.tsx
import { say } from '../tracking'
import { useMount } from './mount'

export function MountUser({ orderId }: { orderId: string }) {
  useMount(() => say(`візит ${orderId}`))
  return null
}
```

Команда `npx eslint src/lint/mount.ts src/lint/MountUser.tsx` друкує шлях лише до файлу `mount.ts`, а під ним такі
рядки:

```text
  7:6  warning  React Hook useEffect has a missing dependency: 'fn'. Either include it or remove the dependency array. If 'fn' changes too often, find the parent component that defines it and wrap that definition in useCallback  react-hooks/exhaustive-deps
✖ 1 problem (0 errors, 1 warning)
```

Отже, через `useMount` компонент повторює помилку з порожнім масивом, а лінт про неї не знає. Причина в тому, що
правило `exhaustive-deps` перевіряє лише відомі йому хуки: `useEffect`, `useMemo`, `useCallback` та інші. Ось хук зі
списком залежностей другим аргументом і компонент, який його викликає:

```ts
// src/lint/delayed.ts
import { useEffect, type DependencyList } from 'react'

export function useDelayedEffect(effect: () => void, deps: DependencyList) {
  useEffect(() => {
    const id = setTimeout(effect, 100)
    return () => clearTimeout(id)
  }, deps)
}
```

```tsx
// src/lint/DelayedUser.tsx
import { say } from '../tracking'
import { useDelayedEffect } from './delayed'

export function DelayedUser({ orderId }: { orderId: string }) {
  useDelayedEffect(() => {
    say(`візит ${orderId}`)
  }, [])
  return null
}
```

Команда `npx eslint src/lint/DelayedUser.tsx` нічого не друкує, хоча ефект читає `orderId`. Такий хук можна додати в
перевірку налаштуванням. Допишіть у масив файлу `eslint.config.js` ще один об'єкт:

```js
{
  files: ['**/*.{ts,tsx}'],
  rules: {
    'react-hooks/exhaustive-deps': ['warn', {
      additionalHooks: '(useDelayedEffect)',
    }],
  },
},
```

Та сама команда тепер показує, що лінт почав перевіряти компонент, який викликає такий хук:

```text
  8:6  warning  React Hook useDelayedEffect has a missing dependency: 'orderId'. Either include it or remove the dependency array  react-hooks/exhaustive-deps
✖ 1 problem (0 errors, 1 warning)
```

README плагіна радить вживати цей параметр дуже рідко й краще взагалі не робити власних хуків зі списком залежностей.
Приймайте у хуку конкретні значення, як `useTracking`, а не список.

### Перевірка хука тестом

Testing Library має функцію `renderHook`, яка викликає хук у маленькому тестовому компоненті. Властивість
`result.current` містить результат останнього рендеру:

```tsx
test('renderHook', () => {
  vi.useFakeTimers()
  const { result } = renderHook(() => useCountdown(3))
  console.log('renderHook | на старті:', result.current)
  act(() => { vi.advanceTimersByTime(2000) })
  console.log('renderHook | через 2 секунди:', result.current)
  act(() => { vi.advanceTimersByTime(5000) })
  console.log('renderHook | через 7 секунд:', result.current)
  vi.useRealTimers()
})
```

```text
renderHook | на старті: 3
renderHook | через 2 секунди: 1
renderHook | через 7 секунд: 0
```

Відлік зупинився на нулі, бо функція в хуку не дає значенню стати меншим за нуль. Отже, такий тест перевіряє межі хука
без окремого компонента.

Для вашого хука про мережу знайте про межу jsdom. Там `navigator.onLine` завжди `true`, а подія `offline`, надіслана
вручну, це значення не змінює:

```tsx
test('мережа в jsdom', () => {
  console.log('jsdom | navigator.onLine:', navigator.onLine)
  let received = 0
  const onOffline = () => {
    received += 1
  }
  window.addEventListener('offline', onOffline)
  window.dispatchEvent(new Event('offline'))
  window.removeEventListener('offline', onOffline)
  console.log(`jsdom | подію offline отримано разів: ${received} | navigator.onLine після неї: ${navigator.onLine}`)
})
```

```text
jsdom | navigator.onLine: true
jsdom | подію offline отримано разів: 1 | navigator.onLine після неї: true
```

Отже, тест перевіряє реакцію вашого коду на подію. Те, як браузер сам визначає стан мережі, тест не перевіряє.
Сторінка MDN про `navigator.onLine` каже, що браузери визначають це по-різному, що підключення до локальної мережі
зазвичай рахується як онлайн, і тому значення ненадійне: його варто використовувати лише для підказки користувачеві, а
не для вимкнення можливостей. У браузері ми цього не запускали. Ручну перевірку ви зробите самі, вимкнувши мережу в
інструментах браузера.

## Хук і рецепт

Практика цього плану йде за рецептом книжки How to Design Programs: спершу опис даних і прикладів, потім код. Для хука
рецепт працює так. Опишіть словами, що він приймає й що повертає, запишіть типи, а приклади запишіть як послідовність
подій і очікуваних значень, як журнал із `к`, `ки`, `киї` вище. Обчислення всередині хука, наприклад наступне значення
відліку, можна винести в чисту функцію й перевірити рівностями, а підписки й таймери перевіряє тест.

## Типові хибні уявлення

**«Я не хочу цю залежність, тому приберу її зі списку».** Список описує код. Щоб прибрати значення, змінюйте код, а
потім звіряйте список із лінтом.

**«Об'єкти з однаковим вмістом однакові».** Для `Object.is` це різні об'єкти, тому канал у запуску відкрився чотири
рази.

**«`useMemo` є першим способом лікувати об'єкт у списку».** Спершу спробуйте перенести об'єкт в ефект чи винести поза
компонент. Попередження лінту згадує `useMemo` лише як альтернативу.

**«Вимкнути лінт на один рядок нічого не коштує».** Запуск лічильника показав 1 на екрані після десяти секунд.
Заглушений рядок мовчатиме й про значення, які в цей ефект допишуть пізніше.

**«Власний хук ділить стан між компонентами».** Він ділить логіку. Кожен виклик має власний стан, що показав відлік 6
і 26.

**«Два компоненти з `useOnlineStatus` показують те саме, отже, стан спільний».** Значення збігаються лише тому, що
обидва хуки стежать за однією мережею. Так само ми бачили дві окремі підписки на `resize`.

**«Будь-яку функцію варто назвати `useЩось`».** Префікс означає, що функція викликає інші хуки. Функцію без хуків
називайте звичайно, щоб її можна було викликати де завгодно.

**«`useMount` спрощує код».** Він ховає порожній масив від лінту, тому компонент втрачає реакцію на зміну значень, і
ніхто про це не повідомляє.

**«Лінт перевіряє кожен мій хук зі списком залежностей».** Без налаштування `additionalHooks` він цього не робить.

## Як це проявиться далі в React

- **Фаза 2, день «Мемоізація і React Compiler».** Там ви виміряєте, коли `useMemo` і `useCallback` справді
  допомагають.
- **Фаза 3, день «Серверний стан: TanStack Query».** Бібліотека дає готові хуки, усередині яких лежить та сама ідея:
  компонент каже, що йому потрібно, а не як це отримати.
- **Фаза 3, день «Стор поза React і перепідключення».** Там з'являється `useSyncExternalStore`. Сторінка
  `Reusing Logic with Custom Hooks` показує, що на нього можна перевести хук стану мережі, не змінюючи компонентів, бо
  вони знають лише про хук.

## Перевірте себе

**1. Чому об'єкт, оголошений у тілі компонента, запускає ефект після кожного рендеру, якщо він стоїть у списку?**

<details><summary>Відповідь</summary>

Кожен рендер створює новий об'єкт, а `Object.is` порівнює об'єкти за посиланням, а не за вмістом. Для React це змінена
залежність, навіть якщо поля ті самі.

</details>

**2. Об'єкт залежить від пропса `orderId`. Як позбутися його в списку так, щоб ефект реагував на зміну замовлення?**

<details><summary>Відповідь</summary>

Перенести створення об'єкта всередину ефекту. У списку лишається `orderId`, рядок порівнюється за значенням, тому
ефект запускається лише при справжній зміні.

</details>

**3. Батько передає `options` пропсом і щоразу створює новий об'єкт. Що може зробити дочірній компонент сам?**

<details><summary>Відповідь</summary>

Дістати потрібні поля до ефекту й записати в список їх, а об'єкт для виклику створити вже в ефекті. У запуску це дало
один запуск за три рендери батька й перепідключення лише при справді іншому замовленні.

</details>

**4. Ефект робить `setHistory([...history, km])`, і кожне нове число перепідключає канал. Як це виправити? Що
станеться, якщо замість цього вимкнути лінт?**

<details><summary>Відповідь</summary>

Передати оновлювач `setHistory((previous) => [...previous, km])`, тоді ефект не читає `history`, і залежність зникає.
Якщо вимкнути лінт, функція назавжди бачить порожню `history` першого рендеру, і на екрані лишається тільки останнє
число.

</details>

**5. Чому лічильник із заглушеним лінтом показує 1 навіть через десять секунд?**

<details><summary>Відповідь</summary>

Таймер викликає функцію першого рендеру, а та пам'ятає `total` = 0. Вона щоразу просить записати `0 + 1`. Значення 1
уже стоїть, тож на екрані нічого не змінюється. Це замикання, яке пережило свій рендер.

</details>

**6. Два компоненти викликають той самий власний хук. Скільки станів і ефектів існує? Чому значення можуть
збігатися?**

<details><summary>Відповідь</summary>

По одному стану й ефекту на кожен виклик, тобто два. Значення збігаються лише тоді, коли обидва виклики читають одне
зовнішнє джерело, наприклад вікно браузера.

</details>

**7. Чому в хук, який приймає функцію, варто покласти `useEffectEvent`, а не писати функцію в список залежностей?**

<details><summary>Відповідь</summary>

Компонент зазвичай передає нову функцію на кожному рендері, тому список перезапускав би ефект щоразу. Подія ефекту дає
найновішу функцію без перезапуску. У запуску це дало одне відкриття каналу за три рендери замість трьох.

</details>

**8. Чим шкідливий `useMount` навіть тоді, коли лінт усередині хука заглушено?**

<details><summary>Відповідь</summary>

Компонент передає функцію, яка читає пропси, але лінт не перевіряє виклик `useMount`, тому жодного попередження там
немає. При зміні пропса ефект не запуститься знову, і компонент лишиться зі старим значенням.

</details>

## Словничок лекції

| Слово | Що означає |
|-------|------------|
| список залежностей | другий аргумент `useEffect`, де записано реактивні значення, які читає ефект |
| порівняння за посиланням | перевірка, чи це той самий об'єкт, без погляду на вміст |
| функція-оновлювач | функція, яку передають у `set` і яка отримує попереднє значення стану |
| застаріле значення | значення зі старого рендеру, яке читає функція, що пережила цей рендер |
| директива | коментар на кшталт `eslint-disable-next-line`, який змінює поведінку ESLint |
| власний хук | функція з назвою на `use` і велику літеру, яка викликає інші хуки |
| debounce, відкладене значення | значення, яке оновлюється лише після паузи у змінах |
| `renderHook` | функція Testing Library, яка викликає хук у тестовому компоненті |
| `additionalHooks` | параметр правила `exhaustive-deps`, який додає власні хуки до перевірки |

## Що читати далі

- [Розбір читання до цього дня](../reading/f1-d19-reading.md): що саме написано в матеріалах дня й де що шукати.
- Removing Effect Dependencies і Reusing Logic with Custom Hooks: дві глави React, які ви читаєте сьогодні.
- README `eslint-plugin-react-hooks` і exhaustive-deps: налаштування й опис правила.
- Navigator: onLine: сторінка MDN про стан мережі.
- renderHook: опис функції для тестів.

---

Лекцію написано для цього плану. Вона спирається на документацію React, README плагіна лінту, сторінки MDN і коротко
згадує рецепт із книжки How to Design Programs. Усе переказано своїми словами, а права на ці тексти належать їхнім
авторам.
