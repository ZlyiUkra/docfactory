# Оновлення корпусу claude-code

Сайт code.claude.com/docs, розділ Claude Tag сайту claude.com/docs, журнали змін Claude Code й обох Agent SDK і
таблиці npm та PyPI беруться щоразу заново. Репозиторії без тегів закріплено комітом: поле `tags` джерел `repo-docs`,
`repo-examples`, `sdk-ts-docs`, `sdk-ts-examples`, `sdk-py-docs`, `sdk-py-examples`, `skills`, `plugins`, `handbook`,
`handbook-scripts` і `handbook-cheatsheet` тримає повний хеш коміту гілки main. claude-code-action закріплено тегами:
останній тег кожної мінорної (`v1.0.264` — версія `action-1.0.264`, `v0.0.63` — `action-0.0.63`).

Правило: **нічого не видаляється.** Ані `refresh`, ані `vectors`, ані `manifest` нічого не стирають самі.

**Спершу — повернути тексти.** Корпус примірника в архіві: у `corpus/` лежить лише паспорт, а `check`, `refresh` і
`manifest` працюють із файлами. Перед роботою нижче тексти розпаковують, а після неї — пакують і виносять знову;
обидві дії описані в [README, розділ «Архівний режим»](README.md#архівний-режим-сервер-без-корпусу).

**Новий знімок репозиторію.** Замінити хеш у `tags` джерел цього репозиторію на новий коміт гілки main. Довідник
sfrangulov оновлюється майже щодня; його три джерела (`handbook`, `handbook-scripts`, `handbook-cheatsheet`) беруть
той самий коміт. **Новий тег claude-code-action** — замінити тег і версію його мінорної в `tags` джерел `action-docs`
і `action-code`; нова мінорна — додати рядок нагорі.

```
./df claude-code check                 # чи змінилося щось нагорі за джерелом
./df claude-code refresh               # повне перезавантаження (кілька хвилин)
./df claude-code refresh site changelog sdk-ts-changelog sdk-py-changelog npm-claude-code npm-agent-sdk pypi-agent-sdk
./df claude-code manifest
./df claude-code vectors
./df claude-code smoke
# Ctrl+C у терміналі з serve, і знову: ./df claude-code serve
```

`refresh` джерела `site` щоразу показує один збій: сторінка `claude-tag` переадресовує на claude.com/docs, а її
зміст бере джерело `claude-tag` (README, «Чого немає»). Інші збої — привід подивитися.

Найновіші версії на 27.10.2026 — Claude Code 2.1.312, Agent SDK для TypeScript 0.3.312, для Python 0.2.174,
claude-code-action 1.0.264. Приклади версій стоять у `prompts/search.txt` (абзац «Which version to answer for»),
`prompts/agent.txt` і в README; коли вони застаріють, їх замінюють там.

Якщо `smoke` скаржиться на число фрагментів, корпус підріс. Нове число записують у `checks.json` полем
`expected_passages`, а в `expected_note` — коли й чому його знято.

## Уточнення відповідей після оновлення

Після кожного оновлення корпусу — цикл із [кроку 7 загального довідника](../../UPDATE.md#крок-7--відновити-уточнення-відповідей):
`./df claude-code quality --show`, порівняння обох десяток з попереднім результатом, розбір промахів, правка промпту,
знову замір. Останній результат — у README, розділ «Скільки цього».
