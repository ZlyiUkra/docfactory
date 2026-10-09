"""Читач журналів змін монорепозиторію: CHANGELOG пакета з префіксом імені документа.

`changelog-named` — CHANGELOG.md, поділений на версії, одна версія — один документ, як у
                    `changelog-v`; заголовок версії — «## 3.13.12» чи «## v3.13.12».
                    `name_prefix` — рядок перед іменем документа («react-virtual» →
                    «react-virtual-3.13.12»).

Навіщо. Changesets пише журнал кожному пакету монорепозиторію, і номери в них ті самі: у
TanStack Virtual запис «Updated dependencies … @tanstack/virtual-core@3.13.12» стоїть дослівно
в журналах react-virtual, lit-virtual та angular-virtual. `changelog-v` називає документ самим
номером, тож однаковий запис трьох журналів злився б в один фрагмент, і журнал двох пакетів
випав би з видачі.

Чому не поле в `changelog-v`: примірники, чиї журнали вже поділено на документи, звірені, а
правка спільного читача — ризик зсуву в готовій роботі. Розбір той самий, що в
`sentry-changelog` (див. `sentry.py`): він і реєструється тут під загальним ім'ям, нічого в
ньому не змінюючи.
"""

from engine.readers import register
from engine.readers.sentry import sentry_changelog

register("changelog-named")(sentry_changelog)
