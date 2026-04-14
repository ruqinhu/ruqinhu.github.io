
import web_fetch
import json

url = "https://cloud.tencent.com/developer/article/2422770" # A sample article
try:
    # Testing the basic fetch functionality
    # Based on the summary, it likely has a fetch or fetch_article method
    # Let's try to inspect the module
    print("Module Attributes:", dir(web_fetch))
    
    # Attempting a likely usage pattern
    # result = web_fetch.fetch(url)
    # print(result)
except Exception as e:
    print(f"Error testing web_fetch: {e}")
