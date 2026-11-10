# Примірник algorithms

Цей примірник шукає в підручниках, курсах і статтях про алгоритми та структури даних. Алгоритм — це точний порядок дій, який
розв'язує задачу: відсортувати список, знайти найкоротший шлях між містами, перевірити, чи є слово в словнику. Структура даних —
це спосіб розкласти дані в пам'яті так, щоб потрібні дії з ними були швидкими: купа швидко віддає найменший елемент, хеш-таблиця
швидко знаходить запис за ключем, червоно-чорне дерево тримає ключі впорядкованими і не дає дереву перекоситися.

Примірник зібрано під навчальний курс алгоритмів. У ньому є три рівні матеріалу. Перший рівень — підручники, які пояснюють, як
працює алгоритм і чому він правильний. Другий — задачі з розв'язками і книжка про співбесіди, яка вчить впізнавати тип задачі.
Третій — книжки й статті про те, де ці алгоритми живуть у справжніх системах: у базах даних, кешах і розподілених системах.
Довідники мов програмування тут не лежать: вони є в примірниках [`mdn`](../mdn/README.md), [`python`](../python/README.md) і
[`go`](../go/README.md).

Навчальний план за цим примірником лежить у [LEARNING.md](LEARNING.md): 77 днів від асимптотики до алгоритмів усередині
справжніх систем і технічної співбесіди, код на TypeScript з перекладом на Python і Go.

## Що всередині

**Книжки з файлів користувача** (корпус лише на цій машині, див. нижче):

| Книжка | Документів |
|---|---|
| Cormen, Leiserson, Rivest, Stein, Introduction to Algorithms, 4-те вид. (MIT Press, 2022) | 196 |
| Sedgewick, Wayne, Algorithms, 4-те вид. (Addison-Wesley, 2011) | 30 |
| Skiena, The Algorithm Design Manual, 3-тє вид. (Springer, 2020) | 228 |
| Kleinberg, Tardos, Algorithm Design (Pearson, 2005) | 152 |
| Knuth, The Art of Computer Programming, том 1 Fundamental Algorithms, 3-тє вид. (Addison-Wesley, 1997) | 47 |
| Knuth, The Art of Computer Programming, том 2 Seminumerical Algorithms, 3-тє вид. (Addison-Wesley, 1997) | 48 |
| Knuth, The Art of Computer Programming, том 3 Sorting and Searching, 2-ге вид. (Addison-Wesley, 1998) | 45 |
| Okasaki, Purely Functional Data Structures (Cambridge University Press, 1998) | 58 |
| Medjedovic, Tahirovic, Dedović, Algorithms and Data Structures for Massive Datasets, чернетка MEAP v8 (Manning, 2022) | 85 |
| Petrov, Database Internals (O'Reilly, 2019) | 120 |
| Kleppmann, Riccomini, Designing Data-Intensive Applications, 2-ге вид. (O'Reilly, 2026) | 85 |
| Bhargava, Grokking Algorithms, 2-ге вид. (Manning, 2024) | 86 |
| Bae, JavaScript Data Structures and Algorithms (Apress, 2019) | 119 |
| McDowell, Mroczka, Lerner, Mamano, Beyond Cracking the Coding Interview (CareerCup, 2025), розпізнано зі скану | 58 |

**Безкоштовні книжки, курси й статті:**

| Що | Звідки | Документів |
|---|---|---|
| Erickson, Algorithms (2019) | PDF з jeffe.cs.illinois.edu | 136 |
| Erickson, конспекти поза книжкою: хешування, treap і skip list, амортизація, union-find, пошук підрядка, лінійне програмування, наближені алгоритми; Models of Computation | PDF з того самого сайту | 26 |
| Morin, Open Data Structures, видання з псевдокодом (AU Press, 2013) | PDF з opendatastructures.org | 73 |
| Lehman, Leighton, Meyer, Mathematics for Computer Science (MIT, 2018) | PDF з courses.csail.mit.edu | 30 |
| Laaksonen, Competitive Programmer's Handbook (2018) | PDF з cses.fi | 149 |
| MIT 6.006 Introduction to Algorithms, весна 2020: лекції, семінари, домашні завдання й іспити з розв'язками | PDF з ocw.mit.edu | 90 |
| MIT 6.046J Design and Analysis of Algorithms, весна 2015: те саме | PDF з ocw.mit.edu | 62 |
| cp-algorithms: усі статті сайту cp-algorithms.com | markdown репозиторію `cp-algorithms/cp-algorithms`, коміт від 08.11.2026 | 169 |
| Slotin, Algorithms for Modern Hardware | markdown репозиторію `algorithmica-org/algorithmica`, англійська книжка, коміт від 11.12.2022 | 115 |

**Статті:** Sedgewick, Left-leaning Red-Black Trees (2008); Myers, An O(ND) Difference Algorithm (1986); Pugh, Skip Lists (1990);
Bloom про фільтр із допустимими помилками (1970); Karger та ін., Web Caching with Consistent Hashing (1999); Flajolet та ін.,
HyperLogLog (2007); O'Neil та ін., The Log-Structured Merge-Tree (1996); Ongaro, Ousterhout, Raft (2014). Статтю Myers сайт
віддає лише через http, тому її взято з файла, завантаженого вручну.

Усього 2215 документів, з них пошук будує 24 453 фрагменти. Фрагмент — це невеликий шматок тексту, який знаходить пошук. Документ
книжки — глава чи розділ за закладками PDF. В Okasaki закладок немає, тому його поділено на шматки по чотири сторінки з назвою
«pp. N–M». Покажчики книжок (сторінки «A», «B», «Index and Glossary») відкинуто: вони містять лише списки слів і номерів сторінок.

Замір `quality` на 10.11.2026 дав такі числа. Запити назвами алгоритмів знаходять потрібне 10 із 10, а модель зазвичай питає саме
так. Запити своїми словами («як знайти найдешевший маршрут між містами») знаходять потрібне 8 із 10.

**Чого немає.** Статті Cormode і Muthukrishnan про Count-Min (2005) немає: жоден із чотирьох сайтів не віддав файл. Ту саму
структуру пояснюють Medjedovic і конспект Erickson «Filtering and Streaming». Оригінальної статті Karger 1997 року про
консистентне хешування у вільному доступі немає, тому замість неї взято статтю 1999 року тих самих авторів. Рукописні конспекти
лекцій 6.046J не взято: розпізнавання робить із почерку нечитабельний текст, а друковані конспекти тих самих лекцій тут є.
Російські розділи algorithmica.org не взято, бо корпус англійський.

## Обмеження текстів

Формули в PDF витягуються як текст і часто розсипаються, а підписи до рисунків стоять посеред абзаців. Пояснення словами від цього
не страждає.

Книжка Beyond Cracking the Coding Interview існує лише сканом DjVu без текстового шару, тому її текст розпізнано програмою OCR.
У звичайному тексті помилок мало. У коді OCR плутає літеру «l» з цифрою «1»: рядок `l, r = 0, len(s) - 1` може стати
`1, r = 0, len(s) - 1`. Крім того, книжка часто ставить два розв'язки поруч у дві колонки, і рядки обох колонок перемішуються.
Кожен документ цієї книжки починається з позначки, що текст розпізнано, і з номерами сторінок книжки та скану. Код із цієї книжки
треба звіряти зі сторінкою скану.

## Як читаються файли

- `pdf-outline` ділить PDF на документи за закладками до заданої глибини (`depth` у `sources.json`), а глибші закладки робить
  підзаголовками. Колонтитули він прибирає за повторенням на краях сторінок.
- `pdf-list` бере кожен PDF з переліку як один документ. Ним читаються курси MIT, конспекти Erickson і статті. Перелік PDF курсів
  MIT записано в `sources.json` явно: його один раз зібрано зі сторінок курсів, бо сам PDF лежить на окремій сторінці кожного
  матеріалу.
- `ghdocs` бере markdown репозиторію на закріпленому коміті. Для cp-algorithms стоїть `title_from: "h1"`: шапка YAML його статей
  не має поля `title`, тому назва береться з першого заголовка.
- `ocr-pages` написано для цього примірника. Він складає текст книжки з наперед розпізнаних сторінок: один файл JSON на сторінку,
  у ньому рамки рядків і їхній текст. Поле `page_titles` каже, на якій сторінці скану починається кожен розділ; у Beyond CtCI номер
  сторінки скану на 3 більший за номер у книжці.

**Як розпізнано скан.** Розпізнавання 646 сторінок займає близько години, тому його зроблено один раз окремо від збирання. Скрипт
лежить у `out/ocr/ocr_djvu.py`, а після архівування — в архіві разом із розпізнаними сторінками. Він малює кожну сторінку програмою `ddjvu` з пакета `djvulibre-bin` у повній роздільності скану
(400 dpi; у 300 dpi слова злипалися) і розпізнає її бібліотекою `rapidocr-onnxruntime` зі спільного середовища `.venvs/gpu`.
Результат лягає в `out/ocr/beyond-ctci/0001.json` … `0646.json`. Перерваний запуск продовжує з першої відсутньої сторінки:

```
.venvs/gpu/bin/python -I instances/algorithms/out/ocr/ocr_djvu.py instances/algorithms/raw/local/mcdowell-beyond-ctci-2025.djvu instances/algorithms/out/ocr/beyond-ctci
```

## Корпус лише локально

Корпус — це тексти глав і статей, а індекс — кеш фрагментів, з якого підіймається сервер. Платні книжки не можна поширювати, тому
**корпус, індекс, файли книжок і розпізнані сторінки в git не потрапляють** (`corpus/`, `index/`, `raw/` і `out/` у
`.gitignore`). У git лежать лише налаштування примірника, а сервер працює лише на цій машині.

**Де тексти.** Вони лежать в архіві `~/archives/docfactory/algorithms-corpus-2026-11-10.tar.gz` разом із паспортом, сховищем
сирого, файлами книжок у `raw/local/` і розпізнаними сторінками в `out/ocr/`. Копія лежить на Windows:
`C:\Distr\algorithms-corpus-2026-11-10.tar.gz`. Архів звірено з диском файл за файлом, а копію — за SHA-256. Сервер підіймається з
кешу `index/passages.json` і колекції Qdrant, тому тексти йому не потрібні.

**Як повернути тексти** перед оновленням:

```
tar -xzf ~/archives/docfactory/algorithms-corpus-2026-11-10.tar.gz -C instances/algorithms
./df algorithms smoke
```

**Якщо зникне кеш фрагментів.** Спершу поверніть тексти, а потім запустіть `./df algorithms vectors`: кеш збереться заново.

Як оновлювати примірник, описано в [UPDATE.md](UPDATE.md).

## Як запустити

```
./df algorithms serve
```

Сервер слухає порт `8968`. Під'єднати його до Claude Code можна файлом `.mcp.json` цієї теки або командою:

```
claude mcp add --transport http --scope user algorithms-docs http://127.0.0.1:8968/mcp
```

Команда для Claude Code у Windows, коли сервер працює у WSL, та сама. У сесії Claude Code команда `/mcp` має показати сервер
`algorithms-docs` з інструментами `search_docs` і `read_section`. Якщо порт зайнятий, `serve` скаже про це і не підніметься: тоді
сервер цього примірника вже працює в іншому терміналі. Якщо `/mcp` показує помилку з'єднання, сервер не запущено.

Перевірка: `./df algorithms smoke` і `./df algorithms quality`.
