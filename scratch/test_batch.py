
import asyncio
from web_fetch import HTMLFetcher

async def test_batch():
    fetcher = HTMLFetcher()
    results = await fetcher.fetch_html_batch(["https://github.com/coderPerseus/blog/issues/100"])
    
    for res in results:
        print("URL:", res.url)
        print("HTML Type:", type(res.html))
        print("HTML Preview:", str(res.html)[:500])

if __name__ == "__main__":
    asyncio.run(test_batch())
