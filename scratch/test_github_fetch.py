
from web_fetch import HTMLFetcher
from bs4 import BeautifulSoup
from markdownify import markdownify as md

url = "https://github.com/coderPerseus/blog/issues/100"

def test_github_scrape():
    fetcher = HTMLFetcher()
    try:
        print(f"[*] Fetching: {url}")
        html = fetcher._fetch_html(url)
        
        if not html:
            print("[!] Failed to fetch HTML")
            return

        soup = BeautifulSoup(html, "html.parser")
        
        # GitHub issue title
        title = soup.find("span", class_="js-issue-title").get_text(strip=True) if soup.find("span", class_="js-issue-title") else "GitHub Issue"
        print(f"[*] Title: {title}")
        
        # GitHub issue content is usually in the first .edit-comment-hide container's .comment-body
        content_node = soup.find("td", class_="comment-body")
        
        if content_node:
            markdown_content = md(str(content_node), heading_style="ATX")
            print("[*] Content extracted successfully.")
            print("-" * 20)
            print(markdown_content[:500])
            print("-" * 20)
        else:
            print("[!] Could not find comment-body")
            
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    test_github_scrape()
