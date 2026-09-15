"""
ОСНОВА · перевірка сервера так, як його бачить чужий клієнт.

Те саме, що робить Inspector, тільки без браузера: піднімаємо spec_mcp.py окремим
процесом, говоримо з ним по stdio, беремо перелік інструментів, кличемо
search_spec, витягаємо з відповіді ідентифікатор фрагмента і кличемо з ним
read_section. Якщо сервер щось надрукує в stdout повз протокол, ця перевірка
розсиплеться першою — саме тому вона окрема від smoke.py.

За зразок узято курсовий test_mcp_client.py; відмінність одна — тут перевіряється
ще й те, що інструментів рівно два і що зв'язка «пошук → читання» працює.

    python -m server.check           # $0, секунди
"""

import asyncio
import json
import os
import pathlib
import sys

SERVER = pathlib.Path(__file__).resolve().parent / "spec_mcp.py"

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    raise SystemExit("Потрібно:  pip install 'mcp[cli]'")

from common import profile  # noqa: E402

EXPECTED_TOOLS = [profile.SEARCH_TOOL, profile.READ_TOOL]
# Запит і вигаданий id — з checks.json примірника: що знаходиться, знає корпус.
CHECKS = profile.checks()


def payload(result) -> dict:
    """Відповідь інструмента як словник. Сервер віддає dict, клієнт бачить його
    текстом у content — розбираємо назад, щоб перевіряти поля, а не рядок."""
    return json.loads(result.content[0].text)


async def main() -> int:
    # env=… обовʼязково: інакше підпроцес сервера не успадкує DF_INSTANCE_DIR
    # і не знатиме, чий домен обслуговувати (докладніше — в agent.py).
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)],
                                   env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            names = [t.name for t in tools.tools]
            print(f"Інструменти сервера ({len(names)}):")
            for t in tools.tools:
                first_line = (t.description or "").strip().split("\n")[0]
                print(f"  · {t.name} — {first_line}")
            if sorted(names) != sorted(EXPECTED_TOOLS):
                print(f"\nОчікувались {EXPECTED_TOOLS}, а сервер віддав {names}")
                return 1

            query = CHECKS["find"]["query"]
            search_tool, read_tool = EXPECTED_TOOLS
            hits = payload(await session.call_tool(search_tool,
                                                   {"query": query, "k": 2}))
            # Поле search друкується поруч із found навмисне: сервер піднімає
            # пошук за змістом у фоні вже після того, як відповів на initialize,
            # тож перші виклики цілком законно приходять із «words». Без цього
            # рядка різницю між «вектори ще гріються» і «вектори не працюють»
            # з виводу не видно.
            print(f"\n{search_tool}({query!r}, k=2) → found={hits.get('found')}, "
                  f"search={hits.get('search')}")
            for p in hits.get("passages", []):
                print(f"  [{p['id']}] {p['section']}")
                print(f"      {p['text'][:120]}...")

            if not hits.get("passages"):
                print("\nПошук нічого не повернув — читати нічого.")
                return 1

            pid = hits["passages"][0]["id"]
            full = payload(await session.call_tool(read_tool, {"id": pid}))
            print(f"\n{read_tool}({pid!r}) → {len(full.get('text', ''))} символів")
            print(f"  розділ: {full.get('section')}")
            print(f"  джерело: {full.get('url')}")

            bad_id = CHECKS["bad_id"]
            bad = payload(await session.call_tool(read_tool, {"id": bad_id}))
            print(f"\n{read_tool}({bad_id!r}) → {bad.get('error')}")
            print(f"  підказка: {bad.get('hint')}")

            print("\nСервер відповів на всі виклики. Протокол живий.")
            return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
