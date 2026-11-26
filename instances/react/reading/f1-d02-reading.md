# Розбір читання. Фаза 1, день 2. JSX

Цей файл допомагає прочитати те, що задано на день. Лекція пояснює саму тему, а розбір показує, де в чужих текстах що
шукати, що означають незнайомі слова й навіщо це вашому проєкту. Усі тексти написано англійською, і розбір їх не
перекладає, а переказує своїми словами. Назви розділів лишено англійською, щоб ви легко їх знайшли.

Читайте в такому порядку: спершу лекцію, потім `Writing Markup with JSX` і `JavaScript in JSX with Curly Braces`. Далі
прочитайте лише вказані частини довідника `Common components (e.g. <div>)` і блогу React, на яких тримається пастка
дня. Наприкінці подивіться `Queries: About` і розділ із книжки. Обидва тексти ви розбирали вчора, тому сьогодні розбір
показує в них лише те, що нове для цього дня. Специфікацій у сьогоднішньому читанні немає.

Приклади в документації React написані на JavaScript у файлах `.js`, а ваш проєкт написано на TypeScript у файлах
`.tsx`. Короткі фрагменти коду зі сторінок react.dev і з блогу React наведено з підписом, звідки вони, за ліцензією
CC BY 4.0, а фрагменти зі сторінок Testing Library наведено за ліцензією MIT.

Приклади цього розбору, як і приклади лекції, запущено на React 19.3 у Vitest під jsdom, тобто в імітації браузера
всередині Node, а не в самому браузері. Кожен приклад із React ми вставляли в тіло тесту у файлі
`src/reading.test.tsx` і запускали командою `npx vitest run src/reading.test.tsx --disable-console-intercept`, як і
вчора. Файл починається такими рядками:

```tsx
import { render, screen } from '@testing-library/react'
import { test } from 'vitest'

test('дослід', () => {
  // сюди вставляли рядки досліду
})
```

Функція `render` показує елемент у документі jsdom і повертає об'єкт. У полі `container` цього об'єкта лежить блок
`<div>`, у який React поставив розмітку, а властивість `innerHTML` цього блока дає розмітку рядком. Тому більшість
прикладів друкує саме `container.innerHTML`. Під прикладами показано лише те, що надрукував сам код. Приклади без
React запущено на Node 24. Дві речі, яких jsdom показати не може, ми перевірили в Chrome 158 без вікна, і в цих місцях
так і сказано.

## `Writing Markup with JSX`

**Де читати:** [react.dev/learn/writing-markup-with-jsx](https://react.dev/learn/writing-markup-with-jsx).

**Що це за текст.** Це сторінка команди React, яка вводить запис JSX. Вона відповідає на три запитання: навіщо
змішувати розмітку з кодом, чим JSX відрізняється від HTML і як перенести наявний HTML у компонент. Сторінка коротка й
завершується однією вправою.

**Якщо часу мало,** прочитайте `The Rules of JSX` разом із трьома пронумерованими правилами всередині.

### `JSX: Putting markup into JavaScript`

Сторінка починає з історії. Раніше вебсторінку ділили на три частини: вміст у HTML, вигляд у CSS, логіку в JavaScript,
зазвичай в окремих файлах. Коли сторінки стали інтерактивними, код почав вирішувати, що саме показати. Тому React
тримає в одному місці розмітку шматка екрана й код, який вирішує, що в цій розмітці показати, і такий шматок є
компонентом. Сторінка показує це на схемах із вигаданими файлами `Sidebar.js` і `Form.js`: те, що змінюється разом,
лежить поруч, а те, що не пов'язане, лежить окремо.

**JSX** сторінка називає розширенням синтаксису, тобто додатковим записом поверх мови, якого сама мова не має. Поруч
стоїть примітка, що JSX і React є різними речами: JSX є записом, React є бібліотекою, і кожен із них можна вживати без
іншого. З цієї примітки видно, чому JSX перетворює не React. React є бібліотекою, яка працює вже під час роботи
програми, а запис JSX треба перетворити ще до запуску, бо браузер його не розуміє. Це робить компілятор, про якого
розповідає лекція в розділі «Що відбувається з тегом до запуску».

### `Converting HTML to JSX`

Сторінка бере правильний HTML зі списком справ винахідниці Геді Ламарр: заголовок, картинку `<img>` і список, у якому
теги `<li>` не закрито. Потім вона вставляє цей HTML без змін у `return` компонента `TodoList` і каже, що так він не
запрацює, бо JSX суворіший за HTML і має більше правил. Самі повідомлення компілятора сторінка показує лише у
вбудованому вікні з кодом. Ми повторили цей дослід компілятором вашого проєкту, тією самою функцією
`transformWithOxc`, що й лекція, і виправляли розмітку по одному кроку:

```js
// файл todo-steps.mjs: HTML зі сторінки, виправлене крок за кроком
import { transformWithOxc } from 'vite'

const html = `<h1>Hedy Lamarr's Todos</h1>
<img src="https://react.dev/images/docs/scientists/yXOvdOSs.jpg" alt="Hedy Lamarr" class="photo">
<ul>
  <li>Invent new traffic lights
  <li>Rehearse a movie scene
</ul>`
const closedImg = html.replace('class="photo">', 'class="photo" />')
const steps = {
  'без змін': html,
  'у фрагменті': `<>${html}</>`,
  'у фрагменті, <img /> закрито': `<>${closedImg}</>`,
  'у фрагменті, усе закрито': `<>${closedImg.replace(/lights|scene/g, '$&</li>')}</>`,
}
for (const [name, markup] of Object.entries(steps)) {
  const source = `export default function TodoList() {\n  return (\n${markup}\n  )\n}`
  try {
    await transformWithOxc(source, 'TodoList.jsx', { jsx: { runtime: 'automatic' } })
    console.log(`${name}: компілюється`)
  } catch (error) {
    // Прибираємо коди кольору й друкуємо лише текст помилки та місце: файл, рядок і знак.
    const message = error.message.replace(/\x1b\[[0-9;]*m/g, '')
    const text = message.match(/\[PARSE_ERROR\] (.*)/)[1]
    const place = message.match(/TodoList\.jsx:\d+:\d+/)[0]
    console.log(`${name}: ${text} ${place}`)
  }
}
```

Розмітку взято зі сторінки react.dev `Writing Markup with JSX`, розділ `Converting HTML to JSX`. Ми скоротили список
до двох пунктів і записали `<img>` в один рядок.

```text
$ node todo-steps.mjs
без змін: Adjacent JSX elements must be wrapped in an enclosing tag. TodoList.jsx:4:1
у фрагменті: Unexpected token. Did you mean `{'}'}` or `&rbrace;`? TodoList.jsx:10:1
у фрагменті, <img /> закрито: Unexpected token. Did you mean `{'}'}` or `&rbrace;`? TodoList.jsx:10:1
у фрагменті, усе закрито: компілюється
```

Перший рядок показує ту саму помилку, що й лекція в розділі «Один кореневий елемент»: на четвертому рядку файла
починається тег `<img>`, який стоїть поруч із заголовком, а не всередині нього. Далі цікавіше. Коли ми загорнули
розмітку у фрагмент, компілятор показав на рядок 10. Це останній рядок файла, і там стоїть закривна дужка функції
`}`, а не незакритий тег. Компілятор так і не знайшов, де закінчуються незакриті теги, тому читав далі все як
розмітку й зупинився аж на знаку `}`, який у тексті розмітки стояти не може. Підказка `Did you mean …` пропонує
записати цей знак як текст, але тут вона не про нашу причину. Закритий `<img />` нічого не змінив, бо незакритими
лишилися теги `<li>`. Скомпілювався лише останній варіант, у якому закрито все.

Лекція в розділі «Кожен тег закритий» показує для короткого запису `<ul><li>Кава<li>Чай</ul>` точніше повідомлення,
`Expected corresponding JSX closing tag for 'li'`. У довшій розмітці компілятор, як бачите, може зупинитися значно
нижче за винний тег. Отже, якщо компілятор скаржиться на кінець компонента, шукайте вище незакритий тег. Причину цієї
суворості сторінка тут не називає, а лекція пояснює її так: тег стає викликом функції, а компілятор не знає, які теги
HTML можна не закривати.

### `The Rules of JSX`

**`1. Return a single root element`.** Кілька елементів треба загорнути в одного батька. Сторінка показує два
варіанти: `<div>` і порожні дужки `<>…</>`. Другий запис називається **Fragment**, тобто фрагмент, і в дереві DOM він
не лишає жодного вузла. Лекція показує це запуском у розділі «Один кореневий елемент».

**`Why do multiple JSX tags need to be wrapped?`** Це згорнутий блок, який відкривається клацанням. Він пояснює
причину правила: JSX перетворюється на звичайні об'єкти JavaScript, а функція не може повернути два об'єкти, якщо не
загорнути їх у масив. Лекція показує, як це виглядає після компілятора, у розділі «Що відбувається з тегом до
запуску». Там фрагмент `<><dt>Кава</dt><dd>25 грн</dd></>` став одним викликом
`_jsxs(_Fragment, { children: [ … ] })`, і обидва теги лежать у масиві `children`. У виводі `show-compiled.mjs` у
практиці дня ви знайдете такий самий виклик, тільки з функцією режиму розробки, про який розповідає лекція в розділі
«Режим розробки»: `_jsxDEV(_Fragment, { children: [ … ] }, …)`. Прочитайте цей блок уважно, бо з тієї самої причини, з
того, що тег стає об'єктом, випливають і два інші правила сторінки.

**`2. Close all the tags`.** Самозакриті теги пишуть зі скісною рискою, наприклад `<img />`, а теги з вмістом мають
закривний тег, наприклад `<li>oranges</li>`. Сторінка лише формулює правило і показує, як тепер виглядають `<img>` і
список справ.

**`3. camelCase ~~all~~ most of the things!`**. У заголовку слово `all` перекреслено, тобто правило стосується не
всього. **camelCase** означає запис складеного слова без пробілів, де кожне слово після першого починається з великої
літери: `strokeWidth`. Причину сторінка пояснює так: атрибути стають ключами об'єктів, а компонент часто читає їх у
змінні, для яких є обмеження мови. Вона каже про це так: «their names can't contain dashes or be reserved words like
`class`». Лекція в розділі «Назви атрибутів» показує цю межу запуском: як поле об'єкта слово `class` дозволене, а як
змінна заборонене.

Сторінка наводить `className` як приклад заміни. Повний список назв, за її словами, стоїть на сторінці пропсів
вбудованих тегів, тобто на `Common components (e.g. <div>)`, яку розібрано нижче. Вона додає, що за неправильної назви
React надрукує в консоль браузера повідомлення з можливим виправленням. Запуск, у якому React пише саме таке
повідомлення, ``Invalid DOM property `class`. Did you mean `className`?``, показує та сама лекція в розділі «Назви
атрибутів».

**Застереження `Pitfall`.** Записи `aria-*` і `data-*` з історичних причин пишуть із дефісами, як в HTML. **ARIA** є
набором атрибутів, які описують елемент для екранного читача, тобто програми, що промовляє сторінку вголос. Екранний
читач пояснює вчорашній розбір, розділ `Priority`. Атрибути `data-*` дозволяють класти у вузол власні дані, яких
людина на екрані не бачить. Сьогодні в практиці ви пишете `aria-valuenow`, `aria-valuemin` і `aria-valuemax`. Разом із
`role="progressbar"` вони кажуть екранному читачу, що блок є смужкою прогресу, і дають йому три числа: поточне
значення, найменше й найбільше.

### `Pro-tip: Use a JSX Converter`

Сторінка радить для великого шматка HTML онлайн-перетворювач
[transform.tools/html-to-jsx](https://transform.tools/html-to-jsx) і додає, що правила все одно варто розуміти.
Наприкінці стоїть виправлений `TodoList`. Для сьогоднішньої практики перетворювач не потрібен, бо в ній ви вчитеся
писати ці правила самі.

### `Recap` і `Challenges`

`Recap` повторює причини існування JSX і його правила. Єдина вправа, `Convert some HTML to JSX`, дає компонент `Bio` з
кількома помилками одразу. Спробуйте знайти їх самі за правилами сторінки, а вже потім дивіться відповідь, бо це добра
розминка перед практикою дня.

**Навіщо це вам.** Сьогодні ви пишете компонент `Profile` із восьми частин розмітки, і в них трапляється кожне
правило сторінки: фрагмент на верхньому рівні, самозакриті `<img />` і `<input />`, назви `className` і `htmlFor`.
Файл прихованих перевірок `Profile.test.tsx` збирає всі повідомлення, які React пише через `console.error`, і після
кожного тесту перевіряє, що їх не було. Так зроблено тому, що React показує кожне таке попередження лише раз за запуск
і його легко не помітити. Тому помилка з назвою атрибута дасть впалий тест.

## `JavaScript in JSX with Curly Braces`

**Де читати:**
[react.dev/learn/javascript-in-jsx-with-curly-braces](https://react.dev/learn/javascript-in-jsx-with-curly-braces).

**Що це за текст.** Сторінка продовжує попередню й показує, як усередині розмітки взяти значення з JavaScript. Вона
містить кілька вікон із кодом, які можна правити просто на сторінці, і три вправи.

**Якщо часу мало,** прочитайте `Where to use curly braces` і `Using "double curlies": CSS and other objects in JSX`.

### `Passing strings with quotes`

Значення атрибута в лапках передає рядок. Сторінка показує компонент `Avatar`, у якого всі три атрибути записано
рядками в лапках. Потім вона виносить адресу картинки й підпис у змінні:

```js
export default function Avatar() {
  const avatar = 'https://react.dev/images/docs/scientists/7vQD0fPs.jpg';
  const description = 'Gregorio Y. Zara';
  return (
    <img
      className="avatar"
      src={avatar}
      alt={description}
    />
  );
}
```

Код зі сторінки react.dev `JavaScript in JSX with Curly Braces`, розділ `Passing strings with quotes`. Ми вставили цю
функцію в тіло тесту без слів `export default` і надрукували `render(<Avatar />).container.innerHTML`:

```text
<img class="avatar" alt="Gregorio Y. Zara" src="https://react.dev/images/docs/scientists/7vQD0fPs.jpg">
```

Запис `className="avatar"` у лапках дав рядок `avatar`, а `src={avatar}` і `alt={description}` дали значення змінних.
Сторінка наголошує саме на цій різниці: лапки передають той рядок, що написаний, а дужки просять прочитати змінну.
Атрибут `src` у виводі стоїть останнім, хоча в коді він другий. React записав його останнім, і на роботу картинки це
не впливає.

### `Using curly braces: A window into the JavaScript world`

Сторінка каже, що JSX є особливим способом писати JavaScript, тому в дужках може стояти будь-який вираз. Дужки вона
образно називає «вікном у світ JavaScript». Без образу це означає таке: усе між `{` і `}` компілятор читає як
звичайний код JavaScript, а не як розмітку. Що таке вираз і чому `if` у дужках не працює, пояснює лекція в розділі
«Фігурні дужки: вираз замість значення».

Приклад `TodoList` спершу підставляє в заголовок змінну `name`, а потім викликає в дужках власну функцію
`formatDate(today)`. Функція вживає вбудований об'єкт `Intl.DateTimeFormat`, який записує дату за правилами певної
мови. Налаштування `{ weekday: 'long' }` просить лише повну назву дня тижня. Ось ця функція в Node з датою, яку
задали ми:

```js
// файл format-date.mjs: функція formatDate зі сторінки і та сама функція з українською мовою
function formatDate(date) {
  return new Intl.DateTimeFormat(
    'en-US',
    { weekday: 'long' }
  ).format(date);
}
// Дата разом із часом і без поясу означає місцевий час, тому день тижня не залежить від часового поясу.
const day = new Date('2026-11-02T12:00')
console.log(formatDate(day))
console.log(new Intl.DateTimeFormat('uk-UA', { weekday: 'long' }).format(day))
```

Функцію `formatDate` взято зі сторінки react.dev `JavaScript in JSX with Curly Braces`, розділ `Using curly braces: A
window into the JavaScript world`.

```text
$ node format-date.mjs
Monday
понеділок
```

Дату ми задали разом із часом `T12:00`, і на це є причина. Рядок із самою датою, `'2026-11-02'`, JavaScript читає як
північ за всесвітнім часом UTC. Так пише MDN на сторінці `Date`, у розділі `Date time string format`. У західних
часових поясах ця північ ще припадає на попередній день, тобто неділю.

### `Where to use curly braces`

Сторінка називає лише два місця. Перше є текстом між тегами, наприклад `<h1>{name}'s To Do List</h1>`. Друге є
значенням атрибута одразу після знака `=`, наприклад `src={avatar}`. Запис `<{tag}>…</{tag}>` не працює, бо дужки не
можуть бути назвою тега. Запис `src="{avatar}"` передає рядок із самими цими знаками. Ось наш дослід з `alt`:

```tsx
const name = 'Зерно'
console.log(render(<img alt="{name}" />).container.innerHTML)
console.log(render(<img alt={name} />).container.innerHTML)
```

```text
<img alt="{name}">
<img alt="Зерно">
```

Помилки немає, тому таку описку легко пропустити. Третя вправа сторінки, `Write an expression inside JSX curly
braces`, побудована саме на ній: там адресу картинки записано як
`src="{baseUrl}{person.imageId}{person.imageSize}.jpg"`.

### `Using "double curlies": CSS and other objects in JSX`

Об'єкт теж пишуть у дужках, тому для об'єкта в атрибуті потрібна друга пара:
`person={{ name: 'Hedy Lamarr', inventions: 5 }}`. Сторінка наголошує, що `{{` і `}}` не є особливим записом. Це
звичайний об'єкт усередині дужок JSX. Найчастіше такий запис трапляється в `style`. Ось приклад сторінки, скорочений
нами до одного пункту списку:

```tsx
function TodoList() {
  return (
    <ul style={{
      backgroundColor: 'black',
      color: 'pink'
    }}>
      <li>Improve the videophone</li>
    </ul>
  );
}
console.log(render(<TodoList />).container.innerHTML)
```

Функцію `TodoList` взято зі сторінки react.dev `JavaScript in JSX with Curly Braces`, розділ `Using "double curlies":
CSS and other objects in JSX`.

```text
<ul style="background-color: black; color: pink;"><li>Improve the videophone</li></ul>
```

Ключ `backgroundColor` в атрибуті `style` став властивістю CSS `background-color`. Застереження `Pitfall` стосується
саме цих назв: `style="background-color: black"` з HTML у JSX пишуть як `style={{ backgroundColor: 'black' }}`.
Сторінка каже й про те, що вбудовані стилі потрібні рідко. **Вбудованим стилем** (inline style) називають стиль,
записаний просто в атрибуті `style` елемента, а не в окремому файлі CSS. Здебільшого досить класів CSS. Числа в
`style` ця сторінка не згадує, про них написано в довіднику нижче.

### `More fun with JavaScript objects and curly braces`

Сторінка збирає дані в один об'єкт `person` із вкладеним об'єктом `theme` і читає їх через крапку:

```tsx
const person = {
  name: 'Gregorio Y. Zara',
  theme: {
    backgroundColor: 'black',
    color: 'pink'
  }
};
console.log(render(
  <div style={person.theme}>
    <h1>{person.name}'s Todos</h1>
  </div>
).container.innerHTML)
```

Об'єкт `person` і розмітку взято зі сторінки react.dev `JavaScript in JSX with Curly Braces`, розділ `More fun with
JavaScript objects and curly braces`. Картинку й список ми прибрали.

```text
<div style="background-color: black; color: pink;"><h1>Gregorio Y. Zara's Todos</h1></div>
```

Тут дужка одна, бо `person.theme` уже є об'єктом. Сторінка завершує думкою, що JSX є дуже простою мовою шаблонів.
**Мовою шаблонів** називають запис розмітки з пропусками, у які програма підставляє дані. Багато таких мов мають
власні цикли й умови, а JSX їх не має: усе складне ви пишете звичайним JavaScript.

### `Recap` і `Challenges`

`Recap` повторює все сказане: лапки дають рядок, дужки дають значення з JavaScript, а `{{ }}` є об'єктом у дужках.
Вправи варто зробити просто на сторінці, бо кожна з них займає кілька хвилин:

| Вправа | Що вона тренує |
|--------|----------------|
| `Fix the mistake` | React не показує об'єкт у дужках |
| `Extract information into an object` | читання полів об'єкта в атрибуті |
| `Write an expression inside JSX curly braces` | лапки навколо дужок, тобто запис, який помилки не дає й не працює |

Перша вправа дає помилку, яку ви запам'ятаєте. У її коді в заголовок потрапляє цілий об'єкт `person` замість його
поля. Ми додали цей рядок у той самий тест, де вище створили `person`:

```tsx
try {
  render(<h1>{person}'s Todos</h1>)
} catch (error) {
  console.log((error as Error).message)
}
```

```text
Objects are not valid as a React child (found: object with keys {name, theme}). If you meant to render a collection of children, use an array instead.
```

Повідомлення називає ключі об'єкта, `name` і `theme`, і за ними легко знайти, який саме об'єкт потрапив у розмітку.
Коли побачите таке повідомлення, шукайте дужки, куди потрапив цілий об'єкт замість його поля.

**Навіщо це вам.** Ім'я, відсоток, колір статусу й ширина смужки на сьогоднішній картці є виразами саме в цих двох
місцях. Запис `style={{ width: … }}` у практиці стоїть подвійними дужками, бо там об'єкт записано одразу в атрибуті.

## `Common components (e.g. <div>)`

**Де читати:**
[react.dev/reference/react-dom/components/common](https://react.dev/reference/react-dom/components/common).

**Що це за текст.** Це сторінка довідника, а не підручника: вона перелічує пропси, які приймають усі вбудовані теги
HTML. Читати її повністю не треба. Пастка дня бере звідси попередження про `dangerouslySetInnerHTML`, тому потрібні
лише вказані нижче частини. Заголовки шукайте у двох великих розділах, `Reference` і `Usage`.

**Якщо часу мало,** прочитайте опис пропа в `Props` і підрозділ `Dangerously setting the inner HTML`.

### `Props`: `dangerouslySetInnerHTML`, `style`, `className`

Це довгий список у розділі `Reference`. Знайдіть у ньому три пункти.

**`dangerouslySetInnerHTML`** приймає об'єкт вигляду `{ __html: '<p>some html</p>' }` із рядком HTML. Сторінка каже,
що React записує цей рядок у властивість `innerHTML` вузла DOM, тобто браузер розбирає рядок як HTML. Далі стоїть
речення, яке цитує пастка плану: «If the HTML inside isn't trusted (for example, if it's based on user data), you risk
introducing an XSS vulnerability». Що таке атака XSS і як вона працює, пояснює лекція в розділі «Яку атаку це
зупиняє». Сторінка згадує й **TrustedHTML**. Сайт може ввімкнути в браузері правило, за яким у `innerHTML` можна
записати лише значення особливого типу `TrustedHTML`, створене перевіркою самого сайту. Для сьогоднішнього дня це не
потрібно.

**`style`** приймає об'єкт, а назви властивостей CSS пишуться в camelCase, як `fontWeight`. Значеннями можуть бути
рядки або числа. До числа React сам допише `px`, якщо властивість має одиниці виміру. Властивості без одиниць
документація називає unitless. Саме цей опис пояснює вивід лекції в розділі «`style` приймає об'єкт»: `width: 75` дає
`75px`, а `opacity: 0.5` лишається `0.5`. Сторінка радить уживати `style` лише для значень, які стають відомі під час
роботи програми, а решту оформлювати класами.

**`className`** є рядком із назвою класу CSS.

Підрозділ `Caveats` у цьому самому розділі додає межу: одночасно передати `children` і `dangerouslySetInnerHTML` не
можна. Запуск такої спроби показує лекція в розділі «`dangerouslySetInnerHTML`», і React кидає там помилку ``Can only
set one of `children` or `props.dangerouslySetInnerHTML`.``. Другий пункт `Caveats`, про події, вам поки не потрібен.

### `Applying CSS styles`

Цей підрозділ стоїть у `Usage`. Він каже, що `className` працює як атрибут `class` в HTML, а `style` потрібен, коли
значення залежить від даних. Ось його компонент `Avatar`, у якого розмір картинки береться з даних користувача:

```tsx
function Avatar({ user }: { user: { name: string; imageUrl: string; imageSize: number } }) {
  return (
    <img
      src={user.imageUrl}
      alt={'Photo of ' + user.name}
      className="avatar"
      style={{
        width: user.imageSize,
        height: user.imageSize
      }}
    />
  );
}
const user = {
  name: 'Hedy Lamarr',
  imageUrl: 'https://react.dev/images/docs/scientists/yXOvdOSs.jpg',
  imageSize: 90,
}
console.log(render(<Avatar user={user} />).container.innerHTML)
```

Компонент і об'єкт `user` взято зі сторінки react.dev `Common components (e.g. <div>)`, розділ `Applying CSS styles`.
Тип параметра дописали ми.

```text
<img alt="Photo of Hedy Lamarr" class="avatar" style="width: 90px; height: 90px;" src="https://react.dev/images/docs/scientists/yXOvdOSs.jpg">
```

Число `90` отримало одиницю `px`, як і обіцяє опис пропа `style` вище. Нижче стоїть згорнутий блок `How to apply
multiple CSS classes conditionally`. Він показує, як скласти рядок `className` за умовою, і він знадобиться пізніше.
Сьогодні смужка прогресу є саме таким випадком, як `Avatar`, бо її ширина залежить від даних.

### `Dangerously setting the inner HTML`

Цей підрозділ теж стоїть у `Usage`. Він починає з найкоротшого запису:

```js
const markup = { __html: '<p>some raw html</p>' };
return <div dangerouslySetInnerHTML={markup} />;
```

Код зі сторінки react.dev `Common components (e.g. <div>)`, розділ `Dangerously setting the inner HTML`.

Одразу під ним жирним шрифтом стоїть попередження. Цей проп так само небезпечний, як властивість `innerHTML`. Якщо
розмітка прийшла не з цілком довіреного джерела, так дуже легко відкрити сторінку для атаки XSS.

Далі стоїть приклад `MarkdownEditor`, у якому людина пише текст у полі вводу, а компонент `MarkdownPreview` показує
його як HTML. **Markdown** є простим форматом розмітки тексту, у якому, наприклад, `**слово**` означає жирне слово.
**Remarkable** є бібліотекою, яка перетворює Markdown на HTML. Чому цей випадок законний, пояснює коментар у самому
коді:

```js
function renderMarkdownToHTML(markdown) {
  // This is ONLY safe because the output HTML
  // is shown to the same user, and because you
  // trust this Markdown parser to not have bugs.
  const renderedHTML = md.render(markdown);
  return {__html: renderedHTML};
}
```

Код зі сторінки react.dev `Common components (e.g. <div>)`, розділ `Dangerously setting the inner HTML`. Ми цей
приклад не запускали, бо бібліотеки Remarkable у вашому проєкті немає.

Коментар називає дві умови. Перша: HTML бачить лише та сама людина, яка написала текст, тому чужий код до неї не
потрапить. Друга: ви довіряєте бібліотеці, що вона не має помилок і не пропустить у HTML небезпечного. Якщо хоч одна
умова не виконується, приклад стає дірою.

Є одна порада, яку легко пропустити. Сторінка каже, що об'єкт `{__html}` слід створювати якомога ближче до місця, де
створено сам HTML, як у функції `renderMarkdownToHTML`. Тоді кожен рядок HTML у коді позначено явно, і в цей проп
потрапляють лише ті змінні, у яких ви справді чекаєте HTML. Запис об'єкта просто в атрибуті сторінка не радить. На
сторінці дня такий запис у загадці теорії все ж стоїть: `dangerouslySetInnerHTML={{ __html: fromUser }}`. Там це
навмисна демонстрація небезпеки в кількох рядках, а не зразок.

Останній приклад показує саму діру. У вміст поста, який ніби лежить у базі даних, вкладено тег `<img>` з порожньою
адресою й кодом в атрибуті `onerror`. Браузер не може завантажити картинку з порожньої адреси й тому викликає цей
обробник помилки. Під jsdom цього не видно, бо jsdom картинок не завантажує. Тому ми зібрали той самий компонент
командою `vite build` і відкрили сторінку в Chrome без вікна. Сторінка `chk/index.html` містить порожні блоки
`<div id="root">` і `<pre id="log">` і підключає такий файл:

```tsx
// файл chk/main.tsx
import { createRoot } from 'react-dom/client'

// Журнал на сторінці: сюди потрапляють виклики alert і помилки.
const log = (line: string) => { document.getElementById('log')!.textContent += line + '\n' }
window.alert = (message?: unknown) => log('alert: ' + String(message))
window.addEventListener('error', (event) => log('error: ' + event.message))

const post = {
  // Imagine this content is stored in the database.
  content: `<img src="" onerror='alert("you were hacked")'>`
};
function MarkdownPreview() {
  // 🔴 SECURITY HOLE: passing untrusted input to dangerouslySetInnerHTML
  const markup = { __html: post.content };
  return <div dangerouslySetInnerHTML={markup} />;
}
const userProfile = {
  website: "javascript: alert('you got hacked')",
};
function App() {
  return <><MarkdownPreview /><a href={userProfile.website}>Profile</a><p>{post.content}</p></>
}
createRoot(document.getElementById('root')!).render(<App />)
// Через 300 мс, коли React уже показав сторінку, клацаємо посилання.
setTimeout(() => {
  const link = document.querySelector('a')!
  log('href: ' + link.getAttribute('href'))
  link.click()
}, 300)
```

Об'єкт `post` і компонент `MarkdownPreview` взято зі сторінки react.dev `Common components (e.g. <div>)`, розділ
`Dangerously setting the inner HTML`. Об'єкт `userProfile` і посилання взято з блогу React, про який ідеться в
наступному розділі. Журнал, абзац `<p>{post.content}</p>` і клацання дописали ми. Функцію `alert` ми замінили записом
у журнал, щоб побачити її виклик без діалогового вікна. Параметр `--dump-dom` просить Chrome надрукувати документ
таким, яким він став після роботи скриптів. Ось вміст журналу `<pre id="log">` з документа, який надрукував
Chrome 158:

```text
alert: you were hacked
href: javascript:throw new Error('React has blocked a javascript: URL as a security precaution.')
error: Uncaught Error: React has blocked a javascript: URL as a security precaution.
```

Перший рядок означає, що код з `onerror` справді виконався. Виклик `alert` у журналі лише один. Отже, той самий рядок
в абзаці `<p>{post.content}</p>` нічого не виконав: React показав його через фігурні дужки як текст. Решту рядків
пояснює наступний розділ, про адреси `javascript:`.

Висновок сторінки такий: давати цьому пропу лише довірені й очищені дані. Що означає очищення і яку бібліотеку для
нього радить MDN, пояснює лекція в розділі «`dangerouslySetInnerHTML`».

**Навіщо це вам.** Цей проп у практиці дня ви не пишете. Він є предметом пастки: ви маєте впізнати цей запис і знати,
чому `{user.bio}` безпечний, а `dangerouslySetInnerHTML` з тим самим рядком ні. Журнал Chrome вище показує обидва
випадки поруч.

## `React v16.9.0 and the Roadmap Update`

**Де читати:** [розділ `Deprecating javascript: URLs` у блозі
React](https://legacy.reactjs.org/blog/2019/08/08/react-v16.9.0.html#deprecating-javascript-urls). Прочитайте лише цей
розділ, бо решта статті описує зміни версії 16.9, потрібні нині лише тим, хто оновлює старий проєкт.

**Що це за текст.** Це запис у блозі React від серпня 2019 року. Блог описує стан на момент написання, тому те, що там
названо майбутнім, треба звіряти з нинішньою версією.

### `Deprecating javascript: URLs`

Слово **deprecating** означає оголошення застарілим: запис поки працює, але про нього вже попереджають. Розділ
пояснює, що адреси, які починаються з `javascript:`, є зручним місцем для атаки. Дані, яких ніхто не перевірив, легко
потрапляють в атрибут `href`, а браузер, перейшовши за такою адресою, виконує написаний у ній код. Ось приклад статті:

```jsx
const userProfile = {
  website: "javascript: alert('you got hacked')",
};
// This will now warn:
<a href={userProfile.website}>Profile</a>
```

Код із блогу React, `React v16.9.0 and the Roadmap Update`, розділ `Deprecating javascript: URLs`.

Версія 16.9 такий запис ще виконувала, але виводила попередження. Якщо такою адресою запускали власну логіку, стаття
радить узяти обробники подій React, тобто функції в пропсах на кшталт `onClick`, про які розповість день 7. Обхід
через `dangerouslySetInnerHTML` вона називає крайнім виходом і застерігає, що він часто веде до дір у безпеці.
Наостанок стаття обіцяє, що майбутня велика версія кидатиме помилку.

**Як воно нині.** Обіцянку виконала версія 19: посібник `React 19 Upgrade Guide` у блозі React серед змін називає
помилку для адрес `javascript:` в атрибутах `src` і `href`. Але помилка виникає не під час показу компонента. React
лишає посилання на сторінці й підміняє адресу кодом, який кидає помилку, а кидає він її лише тоді, коли людина клацне
посилання. Саму підміну під jsdom показує лекція в розділі «Адреса в `href`». Клацання ми перевірили в Chrome файлом
`chk/main.tsx` із попереднього розділу. Рядок `href:` у журналі показує підмінену адресу, рядок `error:` показує
помилку після клацання, а виклику `alert` з текстом `you got hacked` у журналі немає.

Сама стаття згадує лише `javascript:`, і та сама лекція показує, що адреси `data:` та `vbscript:` React пропускає без
змін. Тому правило дня перелічує дозволені схеми, а не заборонені.

**Навіщо це вам.** Функція `isSafeUrl` у практиці дня існує саме через цей розділ.

## `Queries: About` у Testing Library

**Де читати:** [testing-library.com/docs/queries/about](https://testing-library.com/docs/queries/about). Сервер цього
матеріалу — `testing-library-docs`.

**Що це за текст.** Цю сторінку ви розбирали вчора. Що таке запит і з яких двох частин складається його назва, пояснює
розбір читання дня 1 цієї фази, розділ `Queries: About` у Testing Library. Там же, у підрозділі `Types of Queries`,
стоїть таблиця, чим `getBy` відрізняється від `queryBy`. Сьогодні план просить згадати саме цю різницю, бо в практиці
ви вперше перевіряєте, що елемента **немає**. Нижче стоїть лише те, що для цього нове.

**Якщо часу мало,** перечитайте таблицю в `Types of Queries`.

### `Types of Queries`: перевірка, що елемента немає

Учорашня таблиця каже: `getBy` кидає помилку, якщо не знайшов нічого, а `queryBy` у цьому випадку повертає `null`.
Сторінка прямо каже, що `queryBy` корисний для перевірки того, що елемента немає. З цього випливає пастка, яку легко
написати. Ось файл `src/nolink.test.tsx` із двома тестами, які хочуть перевірити одне й те саме:

```tsx
import { render, screen } from '@testing-library/react'
import { expect, test } from 'vitest'

test('getByRole: посилання немає', () => {
  render(<p>Зерно</p>)
  expect(screen.getByRole('link')).toBeNull()
})

test('queryByRole: посилання немає', () => {
  render(<p>Зерно</p>)
  expect(screen.queryByRole('link')).toBeNull()
})
```

```text
$ npx vitest run src/nolink.test.tsx
 FAIL  src/nolink.test.tsx > getByRole: посилання немає
TestingLibraryElementError: Unable to find an accessible element with the role "link"
…
      Tests  1 failed | 1 passed (2)
```

Тут показано лише перший рядок помилки й підсумок. На сторінці справді немає посилання, тобто це саме той випадок,
який перший тест мав підтвердити, а тест на ньому впав. Причина в порядку обчислення. JavaScript спершу обчислює
аргумент `expect(...)`, тобто викликає `screen.getByRole('link')`, і цей виклик кидає помилку. Тому `expect` так і не
отримує значення, і перевірка `toBeNull` не виконується. Другий тест пройшов, бо `queryByRole` повернув `null`.

У файлі прикладів дня ви побачите ще перевірку `toBeInTheDocument()`. Її дає пакет `@testing-library/jest-dom`, який
підключає ваш `setupTests.ts`. Для перевірки, що елемента немає, підходить і запис
`expect(screen.queryByRole('link')).not.toBeInTheDocument()`. Учорашня таблиця нагадує ще одну межу: якщо посилань
знайдеться два, `queryByRole` теж кине помилку.

### `TextMatch`: рядок із тегами

Учорашній розбір у розділі `TextMatch` пояснив, що рядок має збігтися з текстом елемента повністю. Сьогодні з цього
випливає зручна перевірка захисту. Ось два досліди з тим самим рядком. У першому рядок вставлено через фігурні дужки:

```tsx
const bio = '<b>Сашко</b> був тут'
render(<p>{bio}</p>)
console.log('через {}:', screen.getByText('<b>Сашко</b> був тут').nodeName)
```

```text
через {}: P
```

У другому той самий рядок вставлено через `dangerouslySetInnerHTML`. Об'єкт записано просто в атрибуті лише для
стислості досліду:

```tsx
const bio = '<b>Сашко</b> був тут'
render(<p dangerouslySetInnerHTML={{ __html: bio }} />)
try {
  screen.getByText('<b>Сашко</b> був тут')
} catch (error) {
  console.log('як HTML:', (error as Error).message.split('\n')[0])
}
```

```text
як HTML: Unable to find an element with the text: <b>Сашко</b> був тут. This could be because the text is broken up by multiple elements. In this case, you can provide a function for your text matcher to make your matcher more flexible.
```

У першому досліді React записав рядок як текст, тому знаки `<` і `>` є частиною тексту абзацу. Запит знайшов абзац і
надрукував назву його тега, `P`. У другому досліді браузер розібрав рядок як HTML: в абзаці з'явився елемент `<b>` з
текстом `Сашко` і поруч текст ` був тут`. Жоден елемент тепер не має тексту з кутовими дужками, тому запит не знайшов
нічого. Отже, запит `getByText` із тегами в рядку проходить лише тоді, коли рядок показано як текст, і саме так у
практиці перевіряють захист.

**Навіщо це вам.** У `examples.test.tsx` ви пишете приклад, де посилання бути не повинно, і приклад, де текст «про
себе» показано як текст. Перший проходить уже на заглушці `return null`, тому потребує пари, де посилання має бути.
Чому так, пояснює лекція в розділі «Рецепт: приклад на кожну гілку».

## How to Design Programs, `3.1 Designing Functions`

**Де читати:** [розділ у книжці](https://htdp.org/2023-8-14/Book/part_one.html#%28part._sec~3adesign-func%29). Сервер
цього матеріалу — `htdp-book`.

**Що це за текст.** Це книжка How to Design Programs, друге видання, авторів Matthias Felleisen, Robert Bruce Findler,
Matthew Flatt і Shriram Krishnamurthi, видавництва MIT Press, 2018 року. Той самий розділ ви читали вчора, і розбір
читання дня 1 цієї фази переказує його в розділі How to Design Programs, `3.1 Designing Functions`. Тут ми не
повторюємо цей переказ, а показуємо лише, як розділ стосується сьогоднішньої заготовки.

**Якщо часу мало,** перегляньте `The Design Process` і прочитайте два підрозділи нижче.

### `Information and Data`

Що таке опис даних, тобто коментар, який пояснює, що означають дані програми, вчорашній розбір пояснив на типі `Coin`.
У сьогоднішньому файлі `Profile.tsx` цю роботу робить тип `User` разом із коментарями до його полів. Сам тип каже
лише, що `bio` і `site` є рядками. Коментарі кажуть те, чого тип не скаже: ці рядки ввів сам користувач, тому довіряти
їм не можна. Із цього опису даних випливають два кроки практики: `bio` показують лише через `{}`, а адресу `site`
спершу перевіряє `isSafeUrl`. Тут опис даних прямо стосується безпеки.

### `The Design Process`

Що просить кожен із шести кроків книжки, переказує розбір читання дня 4 фази 0, розділ «3.1 Designing Functions».
Ось де кожен крок стоїть у сьогоднішній заготовці:

| Крок у книжці | Де це в заготовці дня |
|---------------|-----------------------|
| подати інформацію даними | тип `User` і приклад під ним |
| сигнатура, призначення, заголовок | сигнатура в коді, коментар над функцією, тіло `return false` або `return null` |
| приклади | `examples.test.tsx` |
| перелік вхідних даних | коментар `// Вхідні дані: …` у тілі |
| код | ваш код за підказками в коментарях |
| перевірка | `npx vitest run src/lessons/f1-d02` |

Зразком усіх кроків сьогодні є функція `percentDone`, а для `isSafeUrl` і `Profile` рецепт ви виконуєте самі. На
прикладах `percentDone` видно, навіщо прикладів більше одного. Приклад «3 з 4 дає 75» не помітить, якщо забути
округлення `Math.round`, бо 75 і так ціле число. Тому в заготовці є другий приклад, «1 з 3 дає 33», який перевіряє
саме округлення, обіцяне в призначенні.

**Навіщо це вам.** Файл `recipe.test.tsx` перевіряє призначення над кожною функцією й рахує ваші приклади: щонайменше
два на кожну з трьох функцій. Учора рецепт застосовувався до компонентів без умов, а сьогодні в тілі є розгалуження,
тому прикладів потрібно більше: по одному на кожну гілку й кожну особливість, обіцяну в призначенні.

## Перевірте себе

**1. Чому сторінка `Writing Markup with JSX` вимагає один кореневий елемент?**

<details><summary>Відповідь</summary>

JSX перетворюється на об'єкти, а функція не може повернути два об'єкти, не загорнувши їх у масив. Тому сусідні теги
загортають у батьківський елемент або у фрагмент `<>…</>`. Фрагмент стає одним викликом, у полі `children` якого
лежить масив з обома тегами.

</details>

**2. Запис `src="{avatar}"` не дає помилки. Що потрапить на сторінку?**

<details><summary>Відповідь</summary>

Рядок із самими знаками `{avatar}`. Лапки означають рядок, і дужки всередині них нічого не роблять. Щоб узяти значення
змінної, пишуть `src={avatar}`.

</details>

**3. Де за сторінкою `JavaScript in JSX with Curly Braces` можуть стояти фігурні дужки?**

<details><summary>Відповідь</summary>

У двох місцях: як текст між тегами й як значення атрибута одразу після знака `=`. Назвою тега вони бути не можуть.

</details>

**4. Чому в `style={{ color: 'pink' }}` дві пари дужок, а в `style={person.theme}` одна?**

<details><summary>Відповідь</summary>

Зовнішня пара щоразу вводить вираз JavaScript. У першому записі цей вираз є літералом об'єкта, який має власні дужки.
У другому записі вираз є читанням поля, значення якого вже є об'єктом.

</details>

**5. Компілятор скаржиться на `Unexpected token` у рядку із закривною дужкою `}` компонента. Що шукати?**

<details><summary>Відповідь</summary>

Незакритий тег вище, наприклад `<img>` без скісної риски чи `<li>` без `</li>`. Компілятор так і не знайшов, де
закінчується такий тег, читав далі все як розмітку й зупинився аж на знаку `}`.

</details>

**6. Де прочитати, що `dangerouslySetInnerHTML` не можна поєднувати з дітьми, і що станеться при спробі?**

<details><summary>Відповідь</summary>

У підрозділі `Caveats` на сторінці `Common components (e.g. <div>)`. React кине помилку ``Can only set one of
`children` or `props.dangerouslySetInnerHTML`.``.

</details>

**7. Блог про версію 16.9 обіцяв, що React кидатиме помилку на адреси `javascript:`. Що відбувається у версії 19.3?**

<details><summary>Відповідь</summary>

Показ компонента не падає. React лишає посилання й підміняє адресу на `javascript:throw new Error(…)`, тому помилка
виникає лише після клацання, а чужий код не виконується. Посилання при цьому лишається на сторінці, а адреси `data:`
React не чіпає, тому перевіряти адреси доводиться самому.

</details>

**8. Чому `expect(screen.getByRole('link')).toBeNull()` не перевіряє, що посилання немає?**

<details><summary>Відповідь</summary>

JavaScript спершу обчислює аргумент `expect`, і `getByRole` кидає помилку, коли нічого не знайшов. Тест падає ще до
перевірки `toBeNull`, причому саме тоді, коли посилання справді немає. Для такої перевірки беруть `queryByRole`, який
повертає `null`.

</details>

**9. Приклад перевіряє `queryByRole('link')` на `null`. Чому його одного замало?**

<details><summary>Відповідь</summary>

Такий приклад проходить уже на заглушці `return null`, бо на порожній сторінці посилання теж немає. Тому потрібен ще
приклад, де посилання є й знаходиться запитом `getByRole`.

</details>
