
import web_fetch
import inspect

fetcher = web_fetch.HTMLFetcher()
print("Signature of _fetch_html:", inspect.signature(fetcher._fetch_html))
