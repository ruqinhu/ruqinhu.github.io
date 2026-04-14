
import web_fetch
import inspect

fetcher = web_fetch.HTMLFetcher()
print("fetch_html_batch signature:", inspect.signature(fetcher.fetch_html_batch))
