import asyncio
import os
import re
import argparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from web_fetch import HTMLFetcher
from web_fetch.web_fetch import SearchResult

async def fetch_and_parse(url, output_path=None):
    """
    Verbatim Article Scraper (Robust Version for GitHub issues)
    """
    print(f"[*] Fetching: {url}")
    
    fetcher = HTMLFetcher()
    html_content = None
    
    try:
        sr = SearchResult(url=url)
        async for res in fetcher.fetch_html_batch([sr]):
            if res.html_content:
                html_content = res.html_content
                break
        
        if not html_content:
            print("[!] Failed to retrieve content.")
            return
    except Exception as e:
        print(f"[!] Fetch Error: {e}")
        return

    soup = BeautifulSoup(html_content, "html.parser")
    
    # 1. Improved Selectors
    title = "无标题"
    content_node = None
    author = "未知作者"

    # Try to find the title
    title_node = soup.find(class_=re.compile("js-issue-title|gh-header-title|entry-title"))
    if not title_node:
        title_node = soup.find("h1")
    
    if title_node:
        title = title_node.get_text(strip=True)
        title = re.sub(r'\s*#\d+$', '', title) # Remove #100

    # Try to find the content
    # GitHub Issues bodies are usually inside .comment-body or .edit-comment-hide
    content_selectors = [
        {"class": "comment-body"},
        {"class": "edit-comment-hide"},
        {"class": "markdown-body"},
        {"class": re.compile("article-content|post-content|main-content")}
    ]
    
    for selector in content_selectors:
        content_node = soup.find(attrs=selector)
        if content_node:
            break

    if not content_node:
        print("[!] Warning: Specific content container not found. Falling back to body.")
        content_node = soup.find("body")

    # Author
    author_node = soup.find(class_=re.compile("author|user-name|author-link"))
    if not author_node:
        author_node = soup.find("a", class_=re.compile("author"))
    author = author_node.get_text(strip=True) if author_node else author

    # 2. Fix URLs
    for img in content_node.find_all("img"):
        for attr in ["src", "data-src", "data-actualsrc"]:
            if img.get(attr):
                img["src"] = urljoin(url, img[attr])
                break
        if not img.get("alt"):
            img["alt"] = "Image"
        if img.get("class"):
            del img["class"]

    for a in content_node.find_all("a"):
        if a.get("href"):
            a["href"] = urljoin(url, a["href"])

    # 3. Clean UI junk
    for junk in content_node.find_all(class_=re.compile("discussion-item|timeline-comment-actions|reaction|issue-meta|gh-header-meta")):
        junk.decompose()
        
    for junk in content_node(["script", "style", "nav", "footer", "header", "aside", "button", "input", "textarea", "form"]):
        junk.decompose()

    # 4. Convert to Markdown
    markdown_body = md(
        str(content_node),
        heading_style="ATX",
        bullets="-",
        code_language="javascript",
        escape_misc=False
    )

    # 5. Polish formatting
    markdown_body = re.sub(r'\n{3,}', '\n\n', markdown_body)
    
    # 6. Final assembly
    header = f"# 转载：{title}\n\n"
    header += f"作者：{author}  \n原文链接：{url}\n\n---\n\n"
    
    final_output = header + markdown_body.strip() + "\n\n---\n*转载于 2026年4月14日*"

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_output)
        print(f"[SUCCESS] Saved to: {output_path}")
    else:
        print(final_output)

async def main():
    parser = argparse.ArgumentParser(description="Async Scraper Tool")
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("-o", "--output", help="Output path", default=None)
    
    args = parser.parse_args()
    await fetch_and_parse(args.url, output_path=args.output)

if __name__ == "__main__":
    asyncio.run(main())
