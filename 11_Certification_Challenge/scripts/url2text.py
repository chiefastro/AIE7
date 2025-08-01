#!/usr/bin/env python3
"""
Web scraping utility to convert web pages to markdown files.
Supports both regular websites and Notion pages.
"""

import requests
from bs4 import BeautifulSoup
import html2text
import os
import re
from urllib.parse import urlparse
import time
from pathlib import Path


def scrape_url_to_markdown(url, output_dir="./data"):
    """
    Scrape a web page and convert it to markdown format.
    
    Args:
        url (str): The URL to scrape
        output_dir (str): Directory to save the markdown file
    
    Returns:
        str: Path to the saved markdown file
    """
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Set up headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print(f"Scraping: {url}")
        
        # Make the request
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "Untitled"
        
        # Clean up the title for filename
        safe_title = re.sub(r'[^\w\s-]', '', title_text)
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        safe_title = safe_title.strip('-')
        
        # Handle different types of content
        if 'notion.so' in url:
            content = extract_notion_content(soup)
        else:
            content = extract_regular_content(soup)
        
        # Convert HTML to markdown
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.body_width = 0  # Don't wrap text
        markdown_content = h.handle(content)
        
        # Add metadata header
        metadata = f"""# {title_text}

**Source URL:** {url}
**Scraped on:** {time.strftime('%Y-%m-%d %H:%M:%S')}

---

"""
        
        full_markdown = metadata + markdown_content
        
        # Save to file
        filename = f"{safe_title}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_markdown)
        
        print(f"Saved: {filepath}")
        return filepath
        
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error scraping {url}: {e}")
        return None


def extract_notion_content(soup):
    """
    Extract content from Notion pages.
    """
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Try to find the main content area - Notion has specific class names
    main_content = (
        soup.find('main') or 
        soup.find('div', class_='notion-page-content') or 
        soup.find('div', class_='content') or
        soup.find('div', class_='notion-page-view') or
        soup.find('div', class_='notion-page-body') or
        soup.find('div', {'data-block-id': True})  # Notion blocks have data-block-id
    )
    
    if main_content:
        return str(main_content)
    else:
        # Fallback to body content
        body = soup.find('body')
        if body:
            return str(body)
        return str(soup)


def extract_regular_content(soup):
    """
    Extract content from regular websites.
    """
    # Remove script and style elements
    for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
        script.decompose()
    
    # Try to find the main content area
    main_content = (
        soup.find('main') or 
        soup.find('article') or 
        soup.find('div', class_='content') or
        soup.find('div', class_='post-content') or
        soup.find('div', class_='entry-content')
    )
    
    if main_content:
        return str(main_content)
    else:
        # Fallback to body content
        body = soup.find('body')
        if body:
            return str(body)
        return str(soup)


def scrape_multiple_urls(urls, output_dir="./data"):
    """
    Scrape multiple URLs and save them as markdown files.
    
    Args:
        urls (list): List of URLs to scrape
        output_dir (str): Directory to save the markdown files
    
    Returns:
        list: List of saved file paths
    """
    saved_files = []
    
    for url in urls:
        filepath = scrape_url_to_markdown(url, output_dir)
        if filepath:
            saved_files.append(filepath)
        
        # Add a small delay between requests to be respectful
        time.sleep(2)
    
    return saved_files


def scrape_specific_urls():
    """
    Scrape the specific URLs mentioned in the assignment.
    This is a convenience function for the certification challenge.
    """
    urls = [
        "https://www.notion.so/Session-11-Certification-Challenge-21dcd547af3d81cbb16dedda007eb69d",
        "https://skillenai.com/2025/07/30/mental-models-for-the-intelligence-age/"
    ]
    
    print("Scraping certification challenge URLs...")
    print("Note: Notion pages often require JavaScript to load content.")
    print("If the Notion page appears empty, you may need to use a browser automation tool like Selenium.")
    print()
    
    return scrape_multiple_urls(urls)


if __name__ == "__main__":
    # Scrape the specific URLs for the certification challenge
    saved_files = scrape_specific_urls()
    
    print(f"\nScraping completed! Saved {len(saved_files)} files:")
    for filepath in saved_files:
        print(f"  - {filepath}")
