# Оновлення корпусу agent-harness-course

Курс і 12-Factor Agents закріплені комітом, LearnHarness — тегом, статті беруться такими, як їх віддає сайт. Тому нагорі
може змінитися будь-що, але корпус зміниться лише після правки `sources.json` або нового `refresh` статей.

Правило: **нічого не видаляється.** Ані `refresh`, ані `vectors`, ані `manifest` нічого не стирають самі.

**Спершу — повернути тексти** з архіву ([README, розділ «Корпус лише локально»](README.md#корпус-лише-локально)).

**Новий коміт курсу.** Тегів у курсі немає. Хеш останнього коміту:

```
gh api repos/justxor/agent-harness-course/commits/main --jq .sha
```

Новий хеш замінити в полі `tags` джерел `course-docs` і `course-code`. Якщо в курсі змінилися модулі чи функції, переглянути
[LEARNING.md](LEARNING.md) і перелік у `prompts/search.txt`.

**Новий реліз LearnHarness.** Тег замінити в полі `tags` джерел `lh-docs`, `lh-prompts` і `lh-code`, і номер — у
`prompts/search.txt`, `prompts/loaded.txt`, `prompts/agent.txt`, `prompts/read.txt` і README.

**Стаття переїхала.** Статті Anthropic уже раз змінили адресу з `/engineering/` на `/research/`. Така зміна видна на кроці
`list` як «редирект на адресу поза оголошенням»; нову адресу прописують і в `url` з `index`, і у `within`.

```
./df agent-harness-course list                # чи всі джерела складають перелік
./df agent-harness-course refresh             # повне перезавантаження
./df agent-harness-course manifest
./df agent-harness-course vectors
./df agent-harness-course smoke
./df agent-harness-course quality
# Ctrl+C у терміналі з serve, і знову: ./df agent-harness-course serve
```

Якщо `smoke` скаржиться на число фрагментів, корпус підріс. Нове число записують у `checks.json` у полі
`expected_passages`, а в `expected_note` — коли й чому його знято.

## Уточнення відповідей після оновлення

Після кожного оновлення корпусу — цикл із [кроку 7 загального довідника](../../UPDATE.md#крок-7--відновити-уточнення-відповідей):
«як модель» має лишатися 10 із 10; ціль у `checks.json` доповнюють лише справжньою відповіддю.

Наприкінці тексти знову виносять в архів (README, той самий розділ).
