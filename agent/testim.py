import asyncio
import re
from mcp.client.sse import sse_client
from mcp import ClientSession


def find_ref(snapshot_text: str, kind: str, label: str) -> str | None:
    pat = re.compile(rf'\b{re.escape(kind)}\s+"{re.escape(label)}"\s+\[ref=(e\d+)\]')
    m = pat.search(snapshot_text)
    return m.group(1) if m else None


async def main():

    async with sse_client("http://localhost:8831/sse") as (r, w):
        async with ClientSession(r, w) as session:

            await session.initialize()

            await session.call_tool("browser_navigate", {"url": "https://hh.ru"})
            await session.call_tool("browser_wait_for", {"time": 1.5})  # НЕ пустым!
            snap = await session.call_tool("browser_snapshot", {})
            print(snap.content[0].text)
            login_ref = find_ref(snap.content[0].text, "link", "Войти")
            print(login_ref)


asyncio.run(main())
