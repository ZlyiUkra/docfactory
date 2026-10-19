# Оновлення корпусу passport

Перелік версій npm тут не оголошується руками: читачі пакетів беруть його з опису пакета в реєстрі
(`https://registry.npmjs.org/<пакет>` для passport, passport-strategy, passport-jwt, passport-oauth2, passport-local,
passport-google-oauth20, passport-github2, passport-facebook, passport-http-bearer і passport-openidconnect), тож нова
версія потрапляє в README і реєстр сама, коли вийде в npm. Журнали змін беруться з гілки master репозиторіїв
`jaredhanson/passport`, `jaredhanson/passport-oauth2`, `jaredhanson/passport-google-oauth2`,
`jaredhanson/passport-http-bearer` та `jaredhanson/passport-openidconnect`. Сайт читається з `sitemap.xml`.

Руками оголошено лише теги репозиторіїв: поле `tags` джерел `<пакет>-code` (десять) і `<пакет>-gh-docs` (passport,
passport-jwt, passport-google-oauth20, passport-facebook). Новий стабільний тег дописують першим рядком у код-джерело
пакета та, якщо воно є, в його `gh-docs`, у вигляді `"v0.8.0": "0.8.0"`. Версію без тегу записують повним SHA коміту
публікації (поле `gitHead` її запису в реєстрі npm), так зроблено для passport-jwt 2.1.1 і passport-github2
0.1.8–0.1.12. Джерела `<пакет>-readme-tags` закриті: це версії, опубліковані без README (passport, passport-local,
passport-facebook, passport-http-bearer), нових не буде.

Правило: **нічого не видаляється.** Ані `refresh`, ані `vectors`, ані `manifest` нічого не стирають самі.

**Спершу — повернути тексти.** Корпус примірника в архіві: у `corpus/` лежить лише паспорт, а `check`, `refresh` і
`manifest` працюють із файлами. Перед роботою нижче тексти розпаковують, а після неї — пакують і виносять знову;
обидві дії описані в [README, розділ «Архівний режим»](README.md#архівний-режим-сервер-без-корпусу).

## Вийшла нова версія

```
./df passport check                 # чи змінилося щось нагорі за джерелом
./df passport refresh               # повне перезавантаження, близько 20 хвилин
./df passport manifest
./df passport vectors
./df passport smoke
# Ctrl+C у терміналі з serve, і знову: ./df passport serve
```

`refresh` повний, не `--missing`: у документі стоять усі версії, де текст був таким, тож нова версія змінює й старі
документи (README, що не змінився, дописує нову версію в рядок `# версія:`).

Якщо вийшла нова лінія passport (0.8 чи 1.0):

- у `prompts/search.txt` (абзац «Which version to search first») та `prompts/agent.txt` переглянути лінію за
  замовчуванням: вона — найпопулярніша за завантаженнями npm (на 19.10.2026 — 0.7, 77 %; друга — 0.6, 16 %), і де
  дві лінії близькі, відповідь дається для обох;
- у `checks.json`, у десятці `quality_model`, замінити `"0.7"` там, де питання про поточну поведінку, і звірити цілі;
- у `config.json` лінії версій складаються з двох чисел (`version_line_depth: 2`); для 1.x це лишається чинним.

Якщо `smoke` скаржиться на число фрагментів — корпус підріс; нове число записують у `checks.json` полем
`expected_passages`, а в `expected_note` — коли й чому його знято.

Токен GitHub (`GITHUB_TOKEN` у `.env`) потрібен для дерев тегів (близько двохсот звернень) і журналів змін: без нього
вистачає годинного вікна в 60 звернень лише впритул.

## Уточнення відповідей після оновлення

Після кожного оновлення корпусу — цикл із [кроку 7 загального довідника](../../UPDATE.md#крок-7--відновити-уточнення-відповідей):
`./df passport quality --show`, порівняння обох десяток з попереднім результатом, розбір промахів, правка промпту,
знову замір. Останній результат — у README, розділ «Скільки цього».
