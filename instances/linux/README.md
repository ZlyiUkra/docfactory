# linux — примірник фабрики docfactory

Двадцять другий примірник фабрики: захищений MCP-сервер, що відповідає на питання про адміністрування Linux за
документацією, з якої працює адміністратор, — man-сторінки Ubuntu 22.04, 24.04 і 26.04, проєкт man-pages (системні
виклики, файли, огляди ядра), admin-guide ядра, systemd, посібники GNU (bash, coreutils, grep, sed, findutils, tar),
довідка vim, Debian Administrator's Handbook, документація Ubuntu Server і Rocky Linux, і сторінка іспиту LFCS. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../../README.md).

## Навіщо

Перший крок навчальної лінії «Linux → Docker → Kubernetes» (сертифікати LFCS → CKAD → CKA): контейнер — це процес
Linux із namespaces і cgroups, а вузол кластера — машина, яку адмініструють тими самими `systemctl`, `ip` і
`journalctl`. Мета — іспит LFCS (Linux Foundation Certified System Administrator).

На іспиті LFCS із довідки дозволено лише man-сторінки й `/usr/share/doc` — тобто рівно те, з чого тут зібрано
відповіді. Команда документується в десятку проєктів, і кожен пише по-своєму: man-сторінка coreutils лише відсилає
до посібника info, `systemctl` описано в DocBook, а різниця між Ubuntu й родиною RHEL (apt проти dnf, ufw проти
firewalld, AppArmor проти SELinux) — у різних посібниках. Тому джерел багато, і кожне взято всіма версіями: опція
з'являється в певному випуску, а машина користувача рідко найновіша.

## Скільки цього

Корпус зібрано 03–04.10.2026.

| Шар | Документів | Звідки |
|-----|-----------:|--------|
| Man-сторінки Ubuntu 26.04, 24.04, 22.04: ~560 команд і файлів налаштувань адміністратора, з пакетом | 1 627 | manpages.ubuntu.com |
| Проєкт man-pages 2.00–6.19, розділи 2, 4, 5, 7 | 15 889 | kernel.org, архів кожного випуску |
| Ядро: admin-guide і `/proc`, лінії 5.10–7.2 | 3 320 | torvalds/linux, теги |
| systemd: документація systemd.io, релізи 183–262 | 1 197 | systemd/systemd, теги |
| systemd: man-сторінки (DocBook), релізи 183–262 | 6 871 | systemd/systemd, теги |
| Посібники GNU: coreutils, bash, grep, sed, findutils, tar — кожен випуск | 223 | ftp.gnu.org, дзеркало kernel.org |
| Довідка vim 7.0–9.2 | 1 569 | vim/vim, теги |
| Debian Administrator's Handbook, Debian 6–13 | 159 | salsa.debian.org |
| Ubuntu Server | 255 | canonical/ubuntu-server-documentation |
| Rocky Linux | 369 | rocky-linux/documentation |
| Сторінка іспиту LFCS: розділи з вагами, компетенції, формат | 1 | training.linuxfoundation.org |

Документ тут — сторінка у версії. Однаковий текст різних випусків у пошуку лежить один раз із переліком усіх версій,
де він був таким.

## Мітки версій

Версія в кожного проєкту своя, і числа перетинаються: «6.18» — і ядро, і випуск man-pages; «9.2» — vim і coreutils;
«13» — Debian. Тому назва документа каже, чий він:

| Назва | Що це | Мітка версії |
|-------|-------|--------------|
| `Ubuntu man: ip(8) — …` | man-сторінка випуску Ubuntu; перший рядок — «Ubuntu 24.04 (noble), package …» | `26.04`, `24.04`, `22.04` |
| `man-pages: clone(2) — …` | проєкт man-pages | `6.19` … `2.00` |
| `Linux kernel: …` | admin-guide ядра | `7.2` … `5.10` |
| `systemd: …`, `systemd man: …` | документація й man-сторінки systemd | `262` … `183` |
| `GNU coreutils 9.12 manual` | посібник GNU | номер випуску (`9.12`, `5.2.37`) |
| `vim help: change.txt` | довідка vim | `9.2` … `7.0` |
| `Debian Handbook: …` | посібник Debian | `13` … `6` |
| `Ubuntu Server: …`, `Rocky Linux: …`, сторінка LFCS | одна, поточна редакція | без версії |

Лінія — два числа (`"version_line_depth": 2` у `config.json`): `5.2.37` належить лінії `5.2`, і фільтр
`version: "5.2"` бере всі її випуски.

## Нові читачі

- `ubuntu-man` — man-сторінки з manpages.ubuntu.com: перелік сторінок явний (адміністраторові потрібні сотні з
  десятків тисяч), які з них є у випуску — з мапи сайту. Mandoc уже віддав усі формати (groff, mdoc, DocBook, POD)
  однаковим HTML.
- `man-pages` — архів кожного випуску проєкту man-pages, groff → markdown (макроси, таблиці tbl, приклади коду).
  Розділ COLOPHON («This page is part of release X») і коментарі зрізаються перед порівнянням версій: інакше жодна
  сторінка не збіглася б із сусіднім випуском, і документів було б 59 тисяч замість 16.
- `gnu-info` — готовий файл info з архіву випуску GNU: вузли — розділи, меню й покажчики відкидаються. ftp.gnu.org
  буває недосяжний годинами, тож у джерела є поле `mirrors` (дзеркало kernel.org, теж у білому списку).
- `docbook-gh`, `docbook-gitlab` — DocBook XML з GitHub (man-сторінки systemd) і GitLab (Debian Handbook), зі
  вставками `xi:include`.
- `vim-help` — розмітка довідки vim: розділи з тегами, підзаголовки, приклади.

Сторінка LFCS — лендинг курсу без `<h1>`; читач `html-list` отримав для неї необов'язкове поле `doc_title`.

## Межі, про які треба пам'ятати

- **Дистрибутив іспиту LFCS не названо.** Відповіді — для поточних випусків; де Ubuntu й родина RHEL розходяться
  (apt/dnf, ufw/firewalld, AppArmor/SELinux, netplan/NetworkManager), промпт велить назвати обидва варіанти.
- **Man-сторінки Ubuntu — лише явний перелік** (`pages` у `sources.json`). Команди поза ним шукаються в man-pages,
  посібниках GNU чи systemd або не знаходяться зовсім; нова потрібна сторінка дописується в перелік.
- **Сторінки RHEL-родини** — лише з документації Rocky Linux; man-сторінок dnf, firewalld, SELinux тут немає.
- **Ліцензії** сторінки LFCS і документації Ubuntu Server не підтверджено; узято за рішенням власника 03.10.2026.
- Docker, Kubernetes, Ansible і хмарні консолі — в інших примірниках або ніде.

## Збирання корпусу

```
./df linux sources --why
./df linux list
./df linux refresh --missing <джерело>   # по джерелу за раз, кілька годин разом
./df linux manifest
./df linux vectors
./df linux smoke
./df linux quality
```

`list` не зважає на назви джерел — завжди перелічує всі. Мережа до manpages.ubuntu.com, GitHub і серверів GNU
буває нестабільною: джерело, чий перелік обірвався, повторюють тією ж командою з `--missing`.

## Сервер під Claude Code

```
./df linux serve
claude mcp add --transport http --scope user linux-docs http://127.0.0.1:8782/mcp
```

Порт `8782`, колекція у Qdrant — `docs-linux`, модель векторів — `bge-small`, інструменти `search_docs` і
`read_section`. Опис `search_docs` довший за 2 048 знаків; головні правила стоять у перших 1 431 — див. «Межа опису
інструмента» в [../../README.md](../../README.md).
