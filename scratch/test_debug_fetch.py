
import asyncio
from web_fetch import HTMLFetcher

async def test_debug():
    fetcher = HTMLFetcher()
    try:
        async for res in fetcher.fetch_html_batch(["https://github.com/coderPerseus/blog/issues/100"]):
            print("Type of res:", type(res))
            print("res content:", str(res)[:200])
            # Check if it's a dict or object
            if hasattr(res, 'html'):
                print("Has html attribute")
            elif isinstance(res, dict) and 'html' in res:
                print("is dict and has html key")
    except Exception as e:
        print(f"Error during loop: {e}")

if __name__ == "__main__":
    asyncio.run(test_debug())
