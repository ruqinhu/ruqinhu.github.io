
import web_fetch.web_fetch as wf
import inspect

print("SearchResult init:", inspect.signature(wf.SearchResult.__init__))
# Let's try to create one
try:
    s = wf.SearchResult(url="https://www.google.com")
    print("Success creating SearchResult:", s)
except Exception as e:
    print(f"Error creating SearchResult: {e}")
