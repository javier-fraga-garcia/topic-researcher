import textwrap
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from agents import function_tool

@function_tool
def scrape_url(url: str) -> list[str]:
    """
    Scrape visible text content from a web page.

    This function launches a headless Chromium browser using Playwright,
    navigates to the given URL, extracts the text from the `<body>` tag,
    removes HTML tags, and returns the content split into text batches.

    Args:
        url (str): The URL of the web page to scrape.

    Returns:
        list[str]: A list of text chunks extracted from the page body,
        cleaned of scripts/styles and ready for downstream processing
        (e.g., feeding into an LLM or indexing).
    """

    print(f"Scraping page {url}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            page_content = page.content()
            browser.close()

        html = HTMLParser(page_content)

        for tag in ["script", "style", "noscript", "iframe", "nav", "footer"]:
            for node in html.css(tag):
                node.decompose()

        text = html.css_first("body").text(separator="\n", strip=True)

        lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 20]

        cleaned_text = " ".join(lines)

        batches = textwrap.wrap(cleaned_text, 1500, break_long_words=False)

        return batches

    except Exception as e:
        print(f"Error scraping page: {str(e)}")
        return f"Error scraping page {url}"
