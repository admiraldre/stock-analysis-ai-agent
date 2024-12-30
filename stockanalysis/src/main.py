from agents.stock_agent import StockAgent


def main():
    stock_agent = StockAgent()
    query = input("Enter query (e.g., `AAPL|What was last quarter's revenue?`): ")
    result = stock_agent.analyze_stock(query)
    print("Result:", result)


if __name__ == "__main__":
    main()