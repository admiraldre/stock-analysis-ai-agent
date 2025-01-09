from agents.analyst import AnalystAgent
from agents.investment_advisor import InvestmentAdvisorAgent
from agents.researcher import ResearcherAgent

def main():
    company_name = input("Enter the stock ticker or company name: ")
    
    # Initialize the agents
    analyst = AnalystAgent()
    investment_advisor = InvestmentAdvisorAgent()
    researcher = ResearcherAgent()
    
    # Research company info with the ResearcherAgent
    research_summary = researcher.summarize_topic(company_name)
    print("\nResearch Summary:\n", research_summary)
    
    # Analyze data with the AnalystAgent
    analyst_summary = analyst.analyze_data(company_name)
    print("\nAnalyst Summary:\n", analyst_summary)
    
    # Get investment strategies from the InvestmentAdvisorAgent
    market_conditions = f"Company: {company_name}\n{analyst_summary}"  
    investment_advice = investment_advisor.recommend_investments(market_conditions)
    print("\nInvestment Advice:\n", investment_advice)

if __name__ == "__main__":
    main()