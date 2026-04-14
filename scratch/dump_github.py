
import asyncio
from web_fetch import HTMLFetcher
from web_fetch.web_fetch import SearchResult

async def dump_html():
    fetcher = HTMLFetcher()
    sr = SearchResult(url="https://github.com/coderPerseus/blog/issues/100")
    async for res in fetcher.fetch_html_batch([sr]):
        with open("scratch/github_dump.html", "w", encoding="utf-8") as f:
            f.write(res.html_content)
        print("HTML Dumped to scratch/github_dump.html")

if __name__ == "__main__":
    asyncio.run(dump_html())
