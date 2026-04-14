
import asyncio
from web_fetch import HTMLFetcher

async def test_simple():
    fetcher = HTMLFetcher()
    it = fetcher.fetch_html_batch(["https://www.google.com"])
    print("Iterator type:", type(it))
    try:
        # If it's an async generator
        async for item in it:
            print("Item type:", type(item))
            print("Item repr:", repr(item)[:200])
    except Exception as e:
        print("Error in loop:", e)

if __name__ == "__main__":
    asyncio.run(test_simple())
