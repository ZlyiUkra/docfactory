# Оновлення корпусу golevelup-nestjs-rabbitmq

Перелік версій README і реєстру тут не оголошується руками: читачі беруть його з опису пакета в реєстрі npm
(`https://registry.npmjs.org/@golevelup%2Fnestjs-rabbitmq`), журнал змін — з `packages/rabbitmq/CHANGELOG.md` на master,
тож нова версія потрапляє туди сама. Руками оголошено лише коміт сторінки сайту (джерело `gl-site`): з новим випуском
його замінюють на свіжий коміт master (`https://api.github.com/repos/golevelup/nestjs/commits/master`), а версію в `tags`
— на нову.

Правило: **нічого не видаляється.** Ані `refresh`, ані `vectors`, ані `manifest` нічого не стирають самі.

**Спершу — повернути тексти.** Корпус примірника в архіві: у `corpus/` лежить лише паспорт, а `check`, `refresh` і
`manifest` працюють із файлами. Перед роботою нижче тексти розпаковують, а після неї — пакують і виносять знову;
обидві дії описані в [README, розділ «Архівний режим»](README.md#архівний-режим-сервер-без-корпусу).

## Вийшла нова версія

```
./df golevelup-nestjs-rabbitmq check                 # чи змінилося щось нагорі за джерелом
./df golevelup-nestjs-rabbitmq refresh               # повне перезавантаження, близько хвилини
./df golevelup-nestjs-rabbitmq manifest
./df golevelup-nestjs-rabbitmq vectors
./df golevelup-nestjs-rabbitmq smoke
# Ctrl+C у терміналі з serve, і знову: ./df golevelup-nestjs-rabbitmq serve
```

`refresh` повний, не `--missing`: у документі стоять усі версії, де текст був таким, тож нова версія змінює й старі
документи.

Якщо зміниться версія, яку завантажують найбільше, — у `prompts/search.txt` (абзац «Which version to search first») і
`prompts/agent.txt` замінити її, звіривши з `https://api.npmjs.org/versions/@golevelup%2Fnestjs-rabbitmq/last-week`;
на 25.10.2026 лінія 9 мала близько 27 %, лінія 5 — 25 %.

Якщо `smoke` скаржиться на число фрагментів — корпус підріс; нове число записують у `checks.json` полем
`expected_passages`, а в `expected_note` — коли й чому його знято.

## Уточнення відповідей після оновлення

Після кожного оновлення корпусу — цикл із [кроку 7 загального довідника](../../UPDATE.md#крок-7--відновити-уточнення-відповідей):
`./df golevelup-nestjs-rabbitmq quality --show`, порівняння обох десяток з попереднім результатом, розбір промахів, правка промпту, знову
замір. Останній результат — у README, розділ «Скільки цього».
