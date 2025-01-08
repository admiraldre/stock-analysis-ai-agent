from agents.researcher import Researcher
from agents.analyst import Analyst
from agents.investment_advisor import InvestmentAdvisor

def main():
    print("Welcome to the Stock Analysis AI Team!")
    company_name = input("Enter the name of the company you want to analyze: ")

    # Initialize agents
    researcher = Researcher()
    analyst = Analyst()
    advisor = InvestmentAdvisor()

    # Research phase
    data = researcher.gather_data(company_name)

    # Analysis phase
    insights = analyst.analyze_data(data)

    # Recommendation phase
    recommendation = advisor.provide_recommendation(insights)

    print("\n--- Analysis Results ---")
    print(f"Financial Insights: {insights['financial_insights']}")
    print(f"Market Sentiment: {insights['market_sentiment']}")
    print(f"News Summary: {insights['news_summary']}")
    print(f"\n--- Investment Recommendation ---")
    print(recommendation)

if __name__ == "__main__":
    main()