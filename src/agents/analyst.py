import yfinance as yf

class AnalystAgent:
    def fetch_company_data(self, company_name):
        stock = yf.Ticker(company_name)
        info = stock.info
        return {
            "name": info.get("longName", "Unknown"),
            "summary": info.get("longBusinessSummary", "No summary available."),
            "current_price": info.get("currentPrice", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "recommendation": info.get("recommendationKey", "N/A")
        }

    def analyze_data(self, company_name):
        data = self.fetch_company_data(company_name)
        analysis = (
            f"{data['name']}:\n"
            f"Market Cap: ${data['market_cap']:,}\n"
            f"Current Price: ${data['current_price']}\n"
            f"P/E Ratio: {data['pe_ratio']}\n"
            f"Recommendation: {data['recommendation']}\n"
            f"Summary: {data['summary']}"
        )
        return analysis