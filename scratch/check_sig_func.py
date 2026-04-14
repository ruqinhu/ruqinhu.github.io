
import web_fetch
import inspect

try:
    print("Signature of web_fetch.web_fetch:", inspect.signature(web_fetch.web_fetch))
except Exception as e:
    print(f"Error: {e}")
