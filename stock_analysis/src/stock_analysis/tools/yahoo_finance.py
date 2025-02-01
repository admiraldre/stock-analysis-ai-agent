from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import yfinance as yf

class YahooFinanceInput(BaseModel):
    symbol: str = Field(..., description="The stock ticker symbol (e.g., AAPL for Apple, TSLA for Tesla).")
    query_type: str = Field(..., description="Type of data: 'news', 'historical', or 'company_info'.")

class YahooFinanceLangChainTool(BaseTool):
    name: str = "Yahoo Finance Stock Data Tool"
    description: str = "Fetches stock news, historical data, and company information using Yahoo Finance API."
    args_schema: Type[BaseModel] = YahooFinanceInput

    def _run(self, symbol: str, query_type: str) -> str:
        try:
            stock = yf.Ticker(symbol)
            
            if query_type == "news":
                news = stock.news
                if not news:
                    return f"No recent news found for {symbol}."
                news_summary = "\n".join([f"{item['title']}: {item['link']}" for item in news[:5]])
                return f"Latest news for {symbol}:\n{news_summary}"

            elif query_type == "historical":
                history = stock.history(period="1mo")
                if history.empty:
                    return f"No historical data found for {symbol}."
                history_summary = history[['Open', 'High', 'Low', 'Close', 'Volume']].to_string()
                return f"Historical data for {symbol} (Last 1 Month):\n{history_summary}"

            elif query_type == "company_info":
                info = stock.info
                if not info:
                    return f"No company information found for {symbol}."
                company_summary = f"""
                Company: {info.get('longName', 'N/A')}
                Sector: {info.get('sector', 'N/A')}
                Market Cap: {info.get('marketCap', 'N/A')}
                P/E Ratio: {info.get('trailingPE', 'N/A')}
                EPS: {info.get('trailingEps', 'N/A')}
                Revenue Growth: {info.get('revenueGrowth', 'N/A')}
                """
                return f"Company Info for {symbol}:\n{company_summary}"

            else:
                return "Invalid query type. Use 'news', 'historical', or 'company_info'."

        except Exception as e:
            return f"Error fetching data for {symbol}: {str(e)}"