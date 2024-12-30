from crewai.tools.scrape_website_tool import ScrapeWebsiteTool


def scrape_website(url):
    """
    Scrapes a given URL using CrewAI's ScrapeWebsiteTool.
    """
    scraper = ScrapeWebsiteTool()
    result = scraper.run(url)
    return result if result else "Failed to scrape content."