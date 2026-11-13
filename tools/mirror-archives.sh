#!/usr/bin/env bash
# mirror-archives.sh — звірити архіви корпусів з їхньою копією на диску Windows і докопіювати відсутнє.
#
#   tools/mirror-archives.sh            звірка: показує, що відсутнє в копії; нічого не копіює
#   tools/mirror-archives.sh --apply    докопіювати в копію те, чого там ще немає
#   tools/mirror-archives.sh --deep     до звірки додати порівняння SHA-256 усіх пар (довго: читає все цілком)
#   tools/mirror-archives.sh --help     ця довідка
#
# Два місця й навіщо вони:
#   ~/archives/docfactory   оригінал: звідси відновлюють тексти, диск WSL швидкий;
#   C:\Distr                копія поза WSL: лишається, якщо віртуальний диск WSL пошкодиться.
# Правило одне: кожен архів лежить в обох місцях під одним іменем.
#
# Що скрипт робить:
#   1. Порівнює імена `*.tar.gz` в обох теках. Список теки Windows він просить у cmd.exe, бо
#      звичайне читання цієї теки з WSL іноді падає з помилкою введення-виведення.
#   2. Архів, який уже є в обох місцях, перевіряє за розміром, а з --deep ще й за SHA-256.
#      Розбіжність скрипт показує і не чіпає ні один з двох файлів.
#   3. Архів, якого в копії немає, з --apply копіюється під тимчасовим іменем `.part`; потім
#      скрипт порівнює SHA-256 оригіналу й копії і тільки після збігу дає файлу справжнє ім'я.
#   4. Архів, який є лише в копії, скрипт показує і не копіює назад: це може бути замінена
#      застаріла копія, а може архів без оригіналу, і рішення за людиною.
#
# Скрипт нічого не видаляє й не перезаписує. Код виходу 0, якщо розбіжностей і збоїв немає.
# Іншу теку можна задати змінними DF_ARCHIVES (оригінал) і DF_ARCHIVES_MIRROR (копія).

set -u

SRC="${DF_ARCHIVES:-$HOME/archives/docfactory}"
DST="${DF_ARCHIVES_MIRROR:-/mnt/c/Distr}"

APPLY=0
DEEP=0
for arg in "$@"; do
  case "$arg" in
    -h|--help) sed -n '2,25p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    --apply) APPLY=1 ;;
    --deep) DEEP=1 ;;
    *) echo "Помилка: невідомий аргумент «$arg» (довідка: tools/mirror-archives.sh --help)" >&2; exit 2 ;;
  esac
done

[ -d "$SRC" ] || { echo "Помилка: немає теки з оригіналами: $SRC" >&2; exit 2; }
[ -d "$DST" ] || { echo "Помилка: немає теки з копіями: $DST" >&2; exit 2; }
command -v cmd.exe >/dev/null || { echo "Помилка: потрібен cmd.exe (скрипт працює з WSL)" >&2; exit 2; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Список архівів копії. Запускаємо з диска C:, бо cmd.exe не приймає шлях WSL як поточну теку.
# Лапок навколо шляху немає навмисно: cmd.exe з ними відповідає помилкою синтаксису. Тож у шляху копії
# не може бути пробілів.
DST_WIN="$(wslpath -w "$DST")"
( cd /mnt/c && cmd.exe /c "dir /b $DST_WIN\\*.tar.gz" 2>/dev/null ) | tr -d '\r' | sort > "$TMP/dst.txt"
ls "$SRC" | grep '\.tar\.gz$' | sort > "$TMP/src.txt"
if [ ! -s "$TMP/dst.txt" ]; then
  echo "Помилка: cmd.exe не показав жодного архіву в $DST_WIN — звіряти нема з чим." >&2
  exit 2
fi

comm -23 "$TMP/src.txt" "$TMP/dst.txt" > "$TMP/missing.txt"
comm -13 "$TMP/src.txt" "$TMP/dst.txt" > "$TMP/mirror_only.txt"
comm -12 "$TMP/src.txt" "$TMP/dst.txt" > "$TMP/both.txt"

# Архіви в обох місцях: розмір має збігатися.
: > "$TMP/mismatch.txt"
while IFS= read -r name; do
  a=$(stat -c %s "$SRC/$name"); b=$(stat -c %s "$DST/$name" 2>/dev/null || echo "-")
  [ "$a" = "$b" ] || echo "$name  оригінал $a Б, копія $b Б" >> "$TMP/mismatch.txt"
done < "$TMP/both.txt"

# Повна звірка: SHA-256 обох файлів кожної пари. Читає все цілком, тож довго (десятки гігабайт).
if [ "$DEEP" -eq 1 ]; then
  total=$(wc -l < "$TMP/both.txt")
  echo "── Повна звірка SHA-256: $total пар ──"
  i=0
  while IFS= read -r name; do
    i=$((i + 1))
    if ! grep -qF "$name  " "$TMP/mismatch.txt"; then
      ha=$(sha256sum < "$SRC/$name" | cut -d' ' -f1); hb=$(sha256sum < "$DST/$name" | cut -d' ' -f1)
      [ "$ha" = "$hb" ] || echo "$name  SHA-256 оригіналу $ha, копії $hb" >> "$TMP/mismatch.txt"
    fi
    [ $((i % 20)) -eq 0 ] && echo "  звірено $i з $total"
  done < "$TMP/both.txt"
fi

need=0
while IFS= read -r name; do need=$((need + $(stat -c %s "$SRC/$name"))); done < "$TMP/missing.txt"

n_src=$(wc -l < "$TMP/src.txt"); n_dst=$(wc -l < "$TMP/dst.txt")
n_both=$(wc -l < "$TMP/both.txt"); n_miss=$(wc -l < "$TMP/missing.txt")
n_only=$(wc -l < "$TMP/mirror_only.txt"); n_bad=$(wc -l < "$TMP/mismatch.txt")

echo "── Оригінали $SRC: $n_src · копії $DST_WIN: $n_dst ──"
echo "в обох місцях $n_both · лише в оригіналі $n_miss ($((need / 1048576)) МіБ) · лише в копії $n_only · розбіжностей $n_bad"
if [ "$n_miss" -gt 0 ]; then echo; echo "Немає в копії:"; sed 's/^/  /' "$TMP/missing.txt"; fi
if [ "$n_only" -gt 0 ]; then echo; echo "Лише в копії (нічого не роблю):"; sed 's/^/  /' "$TMP/mirror_only.txt"; fi
if [ "$n_bad" -gt 0 ]; then echo; echo "РОЗБІЖНОСТІ (нічого не чіпаю):"; sed 's/^/  /' "$TMP/mismatch.txt"; fi

fail=0
[ "$n_bad" -gt 0 ] && fail=1

if [ "$APPLY" -eq 1 ] && [ "$n_miss" -gt 0 ]; then
  free=$(df -B1 --output=avail "$DST" | tail -1 | tr -d ' ')
  # Запас у гігабайт лишаємо, щоб не забити диск C: до нуля.
  if [ "$((need + 1073741824))" -gt "$free" ]; then
    echo; echo "Помилка: на $DST_WIN вільно $((free / 1048576)) МіБ, а треба $((need / 1048576)) МіБ і запас 1 ГіБ. Нічого не копіюю." >&2
    exit 1
  fi
  echo; echo "── Копіюю $n_miss архівів ──"
  done_n=0
  while IFS= read -r name; do
    part="$DST/$name.part"
    if [ -e "$DST/$name" ] || [ -e "$part" ]; then
      echo "  пропущено (уже є або лишився $name.part): $name"; fail=1; continue
    fi
    if cp "$SRC/$name" "$part" \
       && [ "$(sha256sum < "$SRC/$name" | cut -d' ' -f1)" = "$(sha256sum < "$part" | cut -d' ' -f1)" ]; then
      mv "$part" "$DST/$name"
      done_n=$((done_n + 1))
      echo "  ok  $name"
    else
      echo "  ЗБІЙ  $name — SHA-256 не збігся або копіювання впало; $name.part лишено для огляду"
      fail=1
    fi
  done < "$TMP/missing.txt"
  echo "── Скопійовано і звірено за SHA-256: $done_n з $n_miss ──"
elif [ "$n_miss" -gt 0 ]; then
  echo; echo "Це звірка. Щоб докопіювати: tools/mirror-archives.sh --apply"
fi

exit "$fail"
