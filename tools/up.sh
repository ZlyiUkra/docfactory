#!/usr/bin/env bash
# up.sh — підняти кілька примірників разом, дивитися виклики до них і зупинити всі разом.
#
#   tools/up.sh                       примірники з масиву INSTANCES нижче
#   tools/up.sh astro express mdn     примірники з аргументів (масив тоді не діє)
#   tools/up.sh --help                ця довідка
#
# Що відбувається по черзі:
#   1. Для кожного примірника скрипт бере порт із його config.json. Якщо порт уже хтось
#      слухає, примірник пропускається: той сервер підняв не цей скрипт, тож і зупиняти
#      його не йому.
#   2. Решта піднімаються командою `./df <примірник> serve`. Вивід сервера дописується в
#      instances/<примірник>/out/serve.log (старий вміст лишається).
#   3. Коли всі порти слухають, скрипт друкує таблицю і далі показує стрічку викликів:
#      кожен новий рядок журналу instances/<примірник>/out/calls.log з назвою примірника.
#      Старі рядки журналу в стрічку не потрапляють. Виклики від smoke чи quality теж
#      пишуться в цей журнал, тож і вони з'являться в стрічці.
#   4. Ctrl+C (або закрите вікно термінала) зупиняє ті сервери, які підняв цей скрипт, і
#      лише їх, за їхніми PID. Корпус, журнали й вектори скрипт не чіпає.
#
# Запускати з будь-якої теки: скрипт сам переходить у корінь docfactory/.

set -u

# Примірники за замовчуванням. Аргументи командного рядка заміняють цей список.
INSTANCES=(astro express postgresql node-postgres mdn)

# Скільки секунд чекати, поки сервер почне слухати порт. Холодний старт astro з диска
# Windows колись тривав близько трьох хвилин, тож межа з запасом.
READY_TIMEOUT=300

cd "$(dirname "$0")/.." || exit 1

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
fi
[ $# -gt 0 ] && INSTANCES=("$@")

listening() { ss -ltn "sport = :$1" 2>/dev/null | grep -q LISTEN; }

NAMES=(); PORTS=(); PIDS=()
STOPPING=0
TAIL_PID=""

stop_all() {
  [ "$STOPPING" = 1 ] && return
  STOPPING=1
  # $! стрічки — це awk; tail поруч із ним теж дитина цього скрипта, і сам він не
  # помітить зупинки, поки не спробує щось дописати.
  if [ -n "$TAIL_PID" ]; then
    kill "$TAIL_PID" 2>/dev/null
    pkill -P $$ -x tail 2>/dev/null
  fi
  [ ${#PIDS[@]} -eq 0 ] && exit 0
  echo
  echo "── зупиняю ──"
  local i
  for i in "${!PIDS[@]}"; do
    kill -0 "${PIDS[$i]}" 2>/dev/null && kill -TERM "${PIDS[$i]}" 2>/dev/null
  done
  # Сервер сам рве з'єднання й виходить за кілька секунд; 15 — запас.
  local t
  for t in $(seq 1 30); do
    local alive=0
    for i in "${!PIDS[@]}"; do kill -0 "${PIDS[$i]}" 2>/dev/null && alive=1; done
    [ "$alive" = 0 ] && break
    sleep 0.5
  done
  for i in "${!PIDS[@]}"; do
    if kill -0 "${PIDS[$i]}" 2>/dev/null; then
      printf "%-22s pid %-8s не зупинився; зупинити силою: kill -9 %s\n" \
        "${NAMES[$i]}" "${PIDS[$i]}" "${PIDS[$i]}"
    else
      printf "%-22s pid %-8s зупинено\n" "${NAMES[$i]}" "${PIDS[$i]}"
    fi
  done
  exit 0
}
trap stop_all INT TERM HUP

# ── 1–2. Перевірка й запуск ──
for inst in "${INSTANCES[@]}"; do
  dir="instances/$inst"
  if [ ! -f "$dir/config.json" ]; then
    printf "%-22s немає %s/config.json, пропускаю\n" "$inst" "$dir"
    continue
  fi
  port=$(grep -o '"port"[[:space:]]*:[[:space:]]*[0-9]*' "$dir/config.json" | grep -o '[0-9]*$')
  if [ -z "$port" ]; then
    printf "%-22s у config.json немає поля port, пропускаю\n" "$inst"
    continue
  fi
  if listening "$port"; then
    printf "%-22s порт %s уже зайнятий, пропускаю (хто тримає: ss -ltnp | grep %s)\n" \
      "$inst" "$port" "$port"
    continue
  fi
  # Без файла рішення df у живому терміналі спитав би про Qdrant; тут вводу немає, і
  # сервер мовчки шукав би лише за словами. Краще сказати про це вголос.
  [ -f "$dir/out/mode.json" ] || printf "%-22s %s (записати: ./df %s setup)\n" \
    "$inst" "режим пошуку не записано: шукатиме лише за словами" "$inst"
  mkdir -p "$dir/out"
  ./df "$inst" serve >>"$dir/out/serve.log" 2>&1 </dev/null &
  NAMES+=("$inst"); PORTS+=("$port"); PIDS+=("$!")
done

if [ ${#PIDS[@]} -eq 0 ]; then
  echo "Жодного сервера не піднято."
  exit 1
fi

echo "Чекаю, поки сервери почнуть слухати порти (до ${READY_TIMEOUT} с)…"
declare -A DONE=()
for t in $(seq 1 "$READY_TIMEOUT"); do
  for i in "${!PIDS[@]}"; do
    [ -n "${DONE[$i]:-}" ] && continue
    if listening "${PORTS[$i]}"; then
      DONE[$i]=ok
      printf "%-22s порт %-5s pid %-8s готовий\n" "${NAMES[$i]}" "${PORTS[$i]}" "${PIDS[$i]}"
    elif ! kill -0 "${PIDS[$i]}" 2>/dev/null; then
      DONE[$i]=dead
      printf "%-22s порт %-5s не піднявся; кінець instances/%s/out/serve.log:\n" \
        "${NAMES[$i]}" "${PORTS[$i]}" "${NAMES[$i]}"
      tail -n 5 "instances/${NAMES[$i]}/out/serve.log" | sed 's/^/    /'
    fi
  done
  [ ${#DONE[@]} -eq ${#PIDS[@]} ] && break
  sleep 1
done
for i in "${!PIDS[@]}"; do
  [ -z "${DONE[$i]:-}" ] && printf "%-22s порт %-5s за %s с так і не почав слухати\n" \
    "${NAMES[$i]}" "${PORTS[$i]}" "$READY_TIMEOUT"
done

# Ті, що не піднялися, з подальшого стеження прибираємо: зупиняти там уже нічого.
for i in "${!PIDS[@]}"; do
  [ "${DONE[$i]:-}" = dead ] && unset 'NAMES[i]' 'PORTS[i]' 'PIDS[i]'
done
if [ ${#PIDS[@]} -eq 0 ]; then
  echo "Жоден сервер не працює."
  exit 1
fi

# ── 3. Стрічка викликів ──
FILES=()
for i in "${!PIDS[@]}"; do FILES+=("instances/${NAMES[$i]}/out/calls.log"); done
echo "── виклики (Ctrl+C — зупинити всі підняті цим скриптом) ──"
# tail -v ставить перед порцією рядків заголовок «==> файл <==», з нього awk бере
# назву примірника. Рядок журналу: «дата час pid=N інструмент запит -> результат».
tail -v -n0 -F "${FILES[@]}" 2>/dev/null | awk '
  /^==> .* <==$/ { n = $2; sub(/^instances\//, "", n); sub(/\/.*/, "", n); next }
  NF == 0 { next }
  {
    t = $2
    line = $0
    sub(/^[^ ]+ [^ ]+ pid=[0-9]+ /, "", line)
    printf "%s  %-18s %s\n", t, n, line
    fflush()
  }' &
TAIL_PID=$!

# Поки стрічка йде, раз на дві секунди перевіряємо, чи сервери живі: сервер, що впав
# сам, інакше просто замовк би в стрічці.
while :; do
  sleep 2
  alive=0
  for i in "${!PIDS[@]}"; do
    if kill -0 "${PIDS[$i]}" 2>/dev/null; then
      alive=1
    else
      printf "── %s (pid %s) зупинився сам; кінець instances/%s/out/serve.log:\n" \
        "${NAMES[$i]}" "${PIDS[$i]}" "${NAMES[$i]}"
      tail -n 5 "instances/${NAMES[$i]}/out/serve.log" | sed 's/^/    /'
      unset 'NAMES[i]' 'PORTS[i]' 'PIDS[i]'
    fi
  done
  if [ "$alive" = 0 ]; then
    echo "Усі сервери зупинились."
    stop_all
  fi
done
