# Оновлення корпусу csharp

Руками прив'язано три речі: коміти dotnet/docs на день виходу кожної версії C# (джерела `site-X-Y`), гілки
dotnet/csharpstandard (джерела `std-N`) і теки `proposals/csharp-X.Y` та файли критичних змін (джерела `proposals-X-Y`,
`roslyn-breaking-X-Y`). Чинний сайт (`site-main`), документація Roslyn (`roslyn-docs`) і PDF Ecma підхоплюють зміни
самі.

Правило: **нічого не видаляється.** Ані `refresh`, ані `build`, ані `vectors`, ані `manifest` нічого не стирають самі.

**Спершу — повернути тексти.** Корпус примірника в архіві: у `corpus/` лежить лише паспорт, а `check`, `refresh`,
`build` і `manifest` працюють із файлами. Перед роботою нижче тексти й сховище `raw/` розпаковують, а після неї —
пакують і виносять знову; обидві дії описані в [README, розділ «Архівний режим»](README.md#архівний-режим-сервер-без-корпусу).

## Чинний сайт змінився

```
./df csharp check site-main       # чи змінилося щось нагорі
./df csharp refresh site-main     # мережею, ~1 000 сторінок з паузою 0,15 с — кілька хвилин
./df csharp manifest
./df csharp vectors
./df csharp smoke
# Ctrl+C у терміналі з serve, і знову: ./df csharp serve
```

Так само оновлюють `roslyn-docs`, `roslyn-breaking-*`, `std-14` (чернетка комітету живе) і `proposals-14-0`.

## Вийшла нова версія мови (C# 15)

1. Знайти коміт dotnet/docs на день виходу: `commits?sha=main&per_page=1&until=<наступний день>T00:00:00Z` в API
   GitHub. Додати джерело `site-15-0` за зразком `site-14-0` (дерево коміту, `version: "15.0"`, `link: "github"`,
   `within` з цим комітом) і перевести `site-main` на `version: "15.0"`; у `exclude` всіх знімків прибрати
   `whats-new/csharp-15\.md` і за потреби додати сторінку прев'ю наступної версії.
2. Додати `std-15` (гілка `draft-v15`), `proposals-15-0` (тека `proposals/csharp-15.0`) і `roslyn-breaking-15-0`
   (файл `Compiler Breaking Changes - DotNet 11.md`, `version: "15.0"`); додати `site-15-0` до родини `site`, а `std-15`
   до родини `standard` у `config.json`.
3. Засіяти сховище для нового знімка з голого клону й зібрати:

```
git clone --bare https://github.com/dotnet/docs.git /tmp/docs.git
.venvs/gpu/bin/python tools/seed_git_store.py --instance csharp --clone dotnet/docs=/tmp/docs.git
./df csharp build site-15-0 site-main
./df csharp refresh std-15 proposals-15-0 roslyn-breaking-15-0 roslyn-docs
./df csharp manifest
./df csharp vectors
./df csharp smoke
```

4. У `prompts/search.txt`, `prompts/loaded.txt` і `prompts/agent.txt` замінити «14» на «15» у переліках версій і у
   версії за замовчуванням; у `checks.json` звірити цілі десяток `quality` і `quality_model`, а `version_probe` лишити.

Якщо `smoke` скаржиться на число фрагментів — корпус підріс; нове число записують у `checks.json` полем
`expected_passages`, а в `expected_note` — коли й чому його знято.

## Вийшло нове видання стандарту

Коли комітет публікує видання (гілка `draft-vN` стає `standard-vN`), у джерелі `std-N` міняють гілку в `url` і
`within`, а в `title` і `note` — «чернетка» на «опубліковане видання». Текст той самий, тож фрагменти не зміняться.

Токен GitHub (`GITHUB_TOKEN` у кореневому `.env`) потрібен: дерева гілок і тек беруться через API, а без токена
вікно — 60 звернень на годину.

## Уточнення відповідей після оновлення

Після кожного оновлення корпусу — цикл із [кроку 7 загального довідника](../../UPDATE.md#крок-7--відновити-уточнення-відповідей):
`./df csharp quality --show`, порівняння обох десяток з попереднім результатом, розбір промахів, правка промпту,
знову замір. Останній результат — у README, розділ «Скільки цього».
