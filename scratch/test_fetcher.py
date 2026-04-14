
from web_fetch import HTMLFetcher

url = "https://cloud.tencent.com/developer/article/2422770"
try:
    fetcher = HTMLFetcher()
    # Based on general patterns, it might be fetch() or get()
    # Let's try to see the methods of HTMLFetcher
    print("HTMLFetcher Methods:", dir(fetcher))
    
    # Try fetching
    # content = fetcher.fetch(url)
    # print("Content Preview:", str(content)[:500])
except Exception as e:
    print(f"Error: {e}")
