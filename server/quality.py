"""
ОСНОВА · чи додає пошук за змістом те, чого не давав пошук по словах.

Це замір, а не перевірка: він нічого не провалює і ні на що не скаржиться. Він
відповідає на одне питання, на яке інакше довелося б відповідати відчуттям — чи
варті сорок хвилин рахунку векторів того, що вони дають на запитах.

ЯК ВІН МІРЯЄ

Нижче десять запитів, і для кожного наперед названо номер розділу, який мав би
знайтися. Кожен запит проганяється трьома способами — самим пошуком по словах,
самим пошуком за змістом і їхнім злиттям, тим самим, яким користується сервер, —
і рахується, чи потрапив потрібний розділ у перші k.

Просять, згортають повтори розділу і зливають на ту саму глибину, що й сам сервер
(DEPTH і `_dedup` беруться з `spec_mcp`, глибина злиття — з поля fusion_depth у
config.json примірника): замір, що міряв би не те, що віддає сервер, був би гіршим
за відсутній.

ЩО ЦЕ ЧИСЛО ОЗНАЧАЄ І ЧОГО НЕ ОЗНАЧАЄ

Запити й очікувані розділи дібрані руками, тож «4 з 10» саме по собі не є оцінкою
пошуку: інша десятка дала б інше число. Сенс має тільки порівняння трьох стовпців
між собою на одній і тій самій десятці — вони бачать однакові запити й однакові
документи. Якщо злиття дає більше за кожен зі способів окремо, воно робить те,
заради чого його взяли; якщо не дає, вектори на цих документах не окупаються.

Половина запитів навмисне перефразована так, щоб жодне слово не збігалося з
текстом розділу — саме на них пошук по словах безсилий за побудовою. Друга
половина написана словами специфікації, але без її ідентифікаторів.

    python -m server.quality           # $0, десятки секунд
    python -m server.quality --show    # ще й що саме знайшов кожен спосіб

Без піднятого Qdrant міряти нема чого: буде виміряний лише пошук по словах, і
скрипт про це скаже.
"""

import sys
import time

from common import profile

# (запит, розділи, з яких будь-який зараховується) — з checks.json примірника,
# поле quality. У специфікації розділ — номер («20.1.3.6»), у документації
# markdown — ім'я документа й шлях заголовків («reference-react-usestate#reference»)
# або саме ім'я документа, коли відповідь — документ цілком. Ціль — рядок або
# список рядків: усі сторінки, які знаюча людина прийняла б як відповідь.
# Добирається вона з документації, а не з видачі: ціль, дописана під те, що
# пошук знайшов, робить замір зеленим і порожнім. Якщо правильних сторінок
# виходить пʼять, розмите питання — переписують запит, а не розширюють ціль.
CASES = [(q, [w] if isinstance(w, str) else list(w))
         for q, w in profile.checks()["quality"]]

K = 5
WARMUP_SEC = 90


def within(section: str, want: str) -> bool:
    """Чи є розділ шуканим або його підрозділом.

    Номери з крапками порівнюються по межі сегмента, а не як рядки: «9.2.1» —
    префікс для «9.2.10»…«9.2.15», але то сусіди, а не підрозділи. Голий
    startswith зараховував їх за влучання — шість чужих розділів на одну з
    десяти цілей, і стовпці заміру могли розійтися на відповіді, якої спосіб
    не давав. Той самий вираз доречний усюди, де номер розділу порівнюють
    як префікс. Шлях заголовків markdown ділиться «/», і межа там та сама.
    """
    # Ціль без «#» у режимі markdown — цілий документ: будь-який його розділ.
    # Так називають лише документ, що весь про це питання, — довідка useEffect
    # про запуск і прибирання від першого розділу до останнього.
    if "#" not in want and "#" in section:
        return section.split("#", 1)[0] == want
    return (section == want or section.startswith(want + ".")
            or section.startswith(want + "/"))


def wait_for_vectors(spec_mcp) -> bool:
    """Чекає, поки фонова нитка сервера прогріє пошук за змістом.

    Сервер прогріває модель уже після того, як відповів клієнтові, і для клієнта
    це правильно. Але замір, який спитає готовність одразу після імпорту, завжди
    міряв би самий пошук по словах. Тут чекати можна: це не сервер.
    """
    if not spec_mcp._VECTORS_ASKED:
        return False
    if not spec_mcp._VECTORS_READY:
        print(f"чекаю прогріву пошуку за змістом (до {WARMUP_SEC} с)...")
        deadline = time.time() + WARMUP_SEC
        while (time.time() < deadline and not spec_mcp._VECTORS_READY
               and not spec_mcp._VECTORS_WHY):
            time.sleep(1)
    return spec_mcp._VECTORS_READY


def main(argv: list[str]) -> int:
    show = "--show" in argv

    from server import spec_mcp
    from common import embed, nform, vectorstore
    from common.corpus import DOC_SET

    ready = wait_for_vectors(spec_mcp)
    total = len(spec_mcp._INDEX.passages)
    print(f"набір «{DOC_SET}», {total} "
          f"{nform(total, 'фрагмент', 'фрагменти', 'фрагментів')}, k={K}")
    if ready:
        points = vectorstore.count()
        print(f"пошук за змістом: {embed.MODEL_NAME}, {points} "
              f"{nform(points, 'точка', 'точки', 'точок')} "
              f"у {vectorstore.COLLECTION}\n")
    else:
        print(f"пошук за змістом недоступний ({spec_mcp._VECTORS_WHY or '—'}); "
              f"міряю лише пошук по словах\n")

    ways = ["по словах"] + (["за змістом", "разом"] if ready else [])
    score = dict.fromkeys(ways, 0)
    t_words = t_meaning = 0.0

    # Глибина злиття — та сама, що в сервері (spec_mcp._find): без поля fusion_depth
    # у config.json це K, і кожен спосіб окремо міряється своїми першими K місцями.
    fuse = profile.FUSION_DEPTH or K
    for query, wants in CASES:
        deep = max(K * spec_mcp.DEPTH, fuse)
        t0 = time.perf_counter()
        # Той самий відсів варіантів, що в spec_mcp._find; без variant_strict — None.
        keep = spec_mcp._only_wanted(query)
        words = spec_mcp._dedup(spec_mcp._INDEX.retrieve(query, deep, keep), fuse, query)
        t_words += time.perf_counter() - t0
        found = {"по словах": words[:K]}

        if ready:
            t0 = time.perf_counter()
            limit = deep if keep is None else max(50, deep * 2)
            hits = vectorstore.search(embed.embed_query(query), limit)
            t_meaning += time.perf_counter() - t0
            meaning = [spec_mcp._BY_ID[h["uid"]] for h in hits
                       if h.get("uid") in spec_mcp._BY_ID]
            if keep is not None:
                meaning = [p for p in meaning if keep(p)]
            meaning = spec_mcp._dedup(meaning, fuse, query)
            found["за змістом"] = meaning[:K]
            found["разом"] = spec_mcp._dedup(spec_mcp._rrf([words, meaning], K * 2), K,
                                             query)

        marks = []
        for way in ways:
            hit = any(within(p.anchor, w) for p in found[way] for w in wants)
            score[way] += hit
            marks.append(f"{way} {'+' if hit else '-'}")
        want = " | ".join(wants)
        print(f"· {query}\n    треба {want:<11} {'   '.join(marks)}")
        if show:
            for way in ways:
                names = ", ".join(p.anchor for p in found[way])
                print(f"      {way:<11} {names}")

    n = len(CASES)
    print()
    for way in ways:
        print(f"{way:<11} {score[way]} із {n}")
    print(f"\nчас на запит: по словах {t_words / n * 1000:.0f} мс"
          + (f", за змістом {t_meaning / n * 1000:.0f} мс" if ready else ""))
    if ready:
        best = max(score["по словах"], score["за змістом"])
        print("злиття дає більше за кожен спосіб окремо"
              if score["разом"] > best else
              "злиття не дало більше за кращий зі способів")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
