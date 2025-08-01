# Web Scraping Script

This script (`url2text.py`) can scrape web pages and convert them to markdown files.

## Features

- Scrapes both regular websites and Notion pages
- Converts HTML content to clean markdown format
- Adds metadata headers with source URL and timestamp
- Handles different content extraction strategies for different site types
- Respectful scraping with delays between requests

## Usage

### Command Line

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the script to scrape the certification challenge URLs
python scripts/url2text.py
```

### Programmatic Usage

```python
from scripts.url2text import scrape_url_to_markdown, scrape_multiple_urls

# Scrape a single URL
filepath = scrape_url_to_markdown("https://example.com", output_dir="../data")

# Scrape multiple URLs
urls = ["https://example1.com", "https://example2.com"]
saved_files = scrape_multiple_urls(urls, output_dir="../data")

# Scrape the specific certification challenge URLs
from scripts.url2text import scrape_specific_urls
saved_files = scrape_specific_urls()
```

## Output

The script saves markdown files in the `../data` directory with:
- Clean filenames based on page titles
- Metadata headers with source URL and timestamp
- Converted HTML content in markdown format

## Dependencies

- `requests`: HTTP requests
- `beautifulsoup4`: HTML parsing
- `html2text`: HTML to markdown conversion

## Limitations

- **Notion pages**: Many Notion pages require JavaScript to load content, so simple HTTP requests may not capture the full content. For such cases, consider using browser automation tools like Selenium.
- **Dynamic content**: Sites that heavily rely on JavaScript for content loading may not be fully captured.
- **Rate limiting**: The script includes delays between requests, but some sites may still block rapid requests.

## Example Output

```markdown
# Page Title

**Source URL:** https://example.com
**Scraped on:** 2025-08-01 15:36:54

---

# Main Content

This is the converted content from the web page...

## Subsection

More content here...
``` 