from tools.sec_tools import SECTools
from tools.scrape_tools import scrape_website


class StockAgent:
    def __init__(self):
        self.sec_tools = SECTools()

    def analyze_stock(self, query):
        """
        Handles a stock analysis query (e.g., `AAPL|What was last quarter's revenue?`).
        """
        stock_data = self.sec_tools.search_10q(query)
        if stock_data.startswith("http"):
            scraped_data = scrape_website(stock_data)
            return scraped_data
        return stock_data