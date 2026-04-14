import asyncio
import os
import re
import argparse
import requests
import hashlib
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from web_fetch import HTMLFetcher
from web_fetch.web_fetch import SearchResult
from pathlib import Path

def download_image(img_url, save_dir, base_url):
    """
    Download image to local directory and return local filename
    """
    try:
        # Clean URL
        full_url = urljoin(base_url, img_url)
        print(f"[*] Downloading Image: {full_url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(full_url, headers=headers, timeout=15)
        if response.status_code == 200:
            # Determine extension
            path = urlparse(full_url).path
            ext = os.path.splitext(path)[1]
            if not ext or len(ext) > 5:
                # Try to get from Content-Type
                content_type = response.headers.get('Content-Type', '')
                if 'image/jpeg' in content_type: ext = '.jpg'
                elif 'image/png' in content_type: ext = '.png'
                elif 'image/gif' in content_type: ext = '.gif'
                elif 'image/webp' in content_type: ext = '.webp'
                else: ext = '.png'
            
            # Use hash for filename to avoid collisions and invalid chars
            filename = hashlib.md5(full_url.encode()).hexdigest() + ext
            target_path = Path(save_dir) / filename
            
            os.makedirs(save_dir, exist_ok=True)
            with open(target_path, "wb") as f:
                f.write(response.content)
            return filename
    except Exception as e:
        print(f"[!] Image Download Error: {e}")
    return None

async def fetch_and_parse(url, output_path=None):
    """
    Verbatim Article Scraper with Image Localization
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
    
    # 1. Improved Selectors (Added Tencent Cloud support)
    title = "无标题"
    content_node = None
    author = "未知作者"

    # Try to find the title
    title_node = soup.find(class_=re.compile("js-issue-title|gh-header-title|entry-title|article-title|r-article-title"))
    if not title_node:
        title_node = soup.find("h1")
    
    if title_node:
        title = title_node.get_text(strip=True)
        title = re.sub(r'\s*#\d+$', '', title) # Remove #100

    # Try to find the content
    content_selectors = [
        {"class": "comment-body"},
        {"class": "edit-comment-hide"},
        {"class": "markdown-body"},
        {"class": re.compile("article-content|post-content|main-content|r-article-content|cl-artical-content")}
    ]
    
    for selector in content_selectors:
        content_node = soup.find(attrs=selector)
        if content_node:
            break

    if not content_node:
        print("[!] Warning: Specific content container not found. Falling back to body.")
        content_node = soup.find("body")

    # Author
    author_node = soup.find(class_=re.compile("author|user-name|author-link|r-article-author"))
    if not author_node:
        author_node = soup.find("a", class_=re.compile("author"))
    author = author_node.get_text(strip=True) if author_node else author

    # 2. Image Localization
    img_save_dir = None
    if output_path:
        # Determine image dir based on output path
        # docs/reprint/foo.md -> docs/assets/images/reprint/foo/
        rel_name = os.path.splitext(os.path.basename(output_path))[0]
        # Calculate real path for saving
        # Assuming script is run from project root
        base_dir = os.getcwd()
        img_save_dir = os.path.join(base_dir, "docs", "assets", "images", "reprint", rel_name)
        # For markdown replacement, use relative path or absolute from web root
        web_img_prefix = f"./assets/images/reprint/{rel_name}/"

    for img in content_node.find_all("img"):
        original_src = None
        for attr in ["src", "data-src", "data-actualsrc", "data-original-src"]:
            if img.get(attr):
                original_src = img[attr]
                break
        
        if original_src:
            if img_save_dir:
                local_filename = download_image(original_src, img_save_dir, url)
                if local_filename:
                    img["src"] = web_img_prefix + local_filename
                else:
                    img["src"] = urljoin(url, original_src)
            else:
                img["src"] = urljoin(url, original_src)
        
        if not img.get("alt"):
            img["alt"] = "Image"
        if img.get("class"):
            del img["class"]
        # Remove unwanted styles/dims to let CSS handle it
        for attr in ["width", "height", "style"]:
            if img.get(attr): del img[attr]

    for a in content_node.find_all("a"):
        if a.get("href"):
            a["href"] = urljoin(url, a["href"])

    # 3. Clean UI junk
    for junk in content_node.find_all(class_=re.compile("discussion-item|timeline-comment-actions|reaction|issue-meta|gh-header-meta|article-meta|header-meta")):
        junk.decompose()
        
    for junk in content_node(["script", "style", "nav", "footer", "header", "aside", "button", "input", "textarea", "form", "svg"]):
        # Keep SVG if it's important, but usually junk in reprints
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
    
    # Use current date
    from datetime import datetime
    today = datetime.now().strftime("%Y年%m月%d日")
    final_output = header + markdown_body.strip() + f"\n\n---\n*转载于 {today}*"

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_output)
        print(f"[SUCCESS] Saved to: {output_path}")
    else:
        print(final_output)

async def main():
    parser = argparse.ArgumentParser(description="Async Scraper Tool with Image Localization")
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("-o", "--output", help="Output path", default=None)
    
    args = parser.parse_args()
    await fetch_and_parse(args.url, output_path=args.output)

if __name__ == "__main__":
    asyncio.run(main())
