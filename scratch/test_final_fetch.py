
import asyncio
from web_fetch import HTMLFetcher
from web_fetch.web_fetch import SearchResult

async def test_final():
    fetcher = HTMLFetcher()
    sr = SearchResult(url="https://www.google.com")
    try:
        async for res in fetcher.fetch_html_batch([sr]):
            print("URL:", res.url)
            print("HTML Length:", len(res.html_content))
            print("HTML Preview:", res.html_content[:200])
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(test_final())
