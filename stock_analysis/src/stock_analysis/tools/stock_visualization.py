from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import matplotlib.pyplot as plt
import yfinance as yf

class StockVisualizationInput(BaseModel):
    """
    Input schema for Stock Visualization Tool.
    """
    symbol: str = Field(..., description="The stock ticker symbol (e.g., AAPL for Apple, TSLA for Tesla).")
    visualization_type: str = Field(..., description="Type of visualization: 'trend', 'moving_average', 'volume'.")

class StockVisualizationTool(BaseTool):
    """
    LangChain Tool for generating stock visualizations.
    """
    name: str = "Stock Visualization Tool"
    description: str = "Generates visualizations for stock trends, moving averages, and volume."
    args_schema: Type[BaseModel] = StockVisualizationInput

    def _run(self, symbol: str, visualization_type: str) -> str:
        """
        Generates stock visualizations based on the visualization type.
        """
        try:
            if visualization_type == "trend":
                return self.plot_stock_trend(symbol)
            elif visualization_type == "moving_average":
                return self.plot_moving_average(symbol)
            elif visualization_type == "volume":
                return self.plot_volume_trend(symbol)
            else:
                return "Invalid visualization type. Use 'trend', 'moving_average', or 'volume'."
        except Exception as e:
            return f"Error generating visualization: {str(e)}"

    def plot_stock_trend(self, symbol: str) -> str:
        """
        Plots the stock's historical price trend using matplotlib.
        """
        stock = yf.Ticker(symbol)
        history = stock.history(period="1mo")
        if history.empty:
            return "No historical data found for the stock."

        plt.figure(figsize=(10, 6))
        plt.plot(history['Close'], label='Close Price', color='blue')
        plt.title(f"{symbol} Stock Price Trend (1 Month)")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.legend()
        plt.grid(True)
        image_path = f"{symbol}_trend.png"
        plt.savefig(image_path)  # Save the plot as an image
        plt.close()
        return image_path

    def plot_moving_average(self, symbol: str) -> str:
        """
        Plots the stock's moving average using matplotlib.
        """
        stock = yf.Ticker(symbol)
        history = stock.history(period="1mo")
        if history.empty:
            return "No historical data found for the stock."

        # Calculate moving averages
        history['MA_7'] = history['Close'].rolling(window=7).mean()  # 7-day moving average
        history['MA_30'] = history['Close'].rolling(window=30).mean()  # 30-day moving average

        plt.figure(figsize=(10, 6))
        plt.plot(history['Close'], label='Close Price', color='blue')
        plt.plot(history['MA_7'], label='7-Day MA', color='orange')
        plt.plot(history['MA_30'], label='30-Day MA', color='green')
        plt.title(f"{symbol} Moving Averages (1 Month)")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.legend()
        plt.grid(True)
        image_path = f"{symbol}_moving_average.png"
        plt.savefig(image_path)  # Save the plot as an image
        plt.close()
        return image_path

    def plot_volume_trend(self, symbol: str) -> str:
        """
        Plots the stock's trading volume trend using matplotlib.
        """
        stock = yf.Ticker(symbol)
        history = stock.history(period="1mo")
        if history.empty:
            return "No historical data found for the stock."

        plt.figure(figsize=(10, 6))
        plt.bar(history.index, history['Volume'], label='Volume', color='blue')
        plt.title(f"{symbol} Trading Volume Trend (1 Month)")
        plt.xlabel("Date")
        plt.ylabel("Volume")
        plt.legend()
        plt.grid(True)
        image_path = f"{symbol}_volume.png"
        plt.savefig(image_path)  # Save the plot as an image
        plt.close()
        return image_path