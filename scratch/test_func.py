
import web_fetch

try:
    print("web_fetch.web_fetch type:", type(web_fetch.web_fetch))
    # It might be a shorthand for HTMLFetcher()._fetch_html
except Exception as e:
    print(f"Error: {e}")
