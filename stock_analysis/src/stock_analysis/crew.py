import sys
import os
import yfinance as yf
import logging
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from tools.google_serper import GoogleSerperLangChainTool
from tools.yahoo_finance import YahooFinanceLangChainTool
from tools.stock_visualization import StockVisualizationTool
from langsmith import Client, traceable 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up LangSmith client
langsmith_client = Client()

# Initialize the LLM model (this part can be changed based on LLM setup)
llm = LLM(
    model='ollama/mistral',
    temperature=0.1,
    base_url='http://localhost:11434',
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@traceable
@CrewBase
class StockAnalysis():
    """StockAnalysis crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def research_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['research_analyst'],
            llm=llm,
            tools=[GoogleSerperLangChainTool()],
            max_iter=5,
            max_execution_time=60,
            verbose=True,
        )

    @agent
    def financial_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst'],
            llm=llm,
            tools=[YahooFinanceLangChainTool()],
            max_iter=5,
            max_execution_time=60,
            verbose=True,
        )

    @agent
    def investment_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['investment_advisor'],
            llm=llm,
            tools=[StockVisualizationTool()],
            max_iter=5, 
            max_execution_time=60,
            verbose=True,
            allow_parallel_execution=False,  
        )

    
    @task
    def research(self) -> Task:
        def gather_research(inputs):
            topic = inputs.get("topic")
            logger.info(f"Gathering research data for {topic}...")

            try:
                # Fetch news and press releases
                news = GoogleSerperLangChainTool()._run(topic, "news")
                press_releases = GoogleSerperLangChainTool()._run(topic, "press release")

                # Summarize findings
                research_summary = f"""
                ### Research Summary for {topic}
                - **News**: {news}
                - **Press Releases**: {press_releases}
                """
                return research_summary

            except Exception as e:
                logger.error(f"Error gathering research data: {str(e)}")
                return f"Error gathering research data: {str(e)}"

        return Task(
            config=self.tasks_config['research'],
            action=gather_research
        )

    @task
    def financial_analysis(self) -> Task:
        def analyze_financials(inputs):
            topic = inputs.get("topic")
            logger.info(f"Analyzing financial data for {topic}...")

            try:
                # Fetch historical data
                historical_data = YahooFinanceLangChainTool()._run(topic, "historical")
                logger.info(f"Historical data fetched: {historical_data}")

                # Fetch company info
                company_info = YahooFinanceLangChainTool()._run(topic, "company_info")
                logger.info(f"Company info fetched: {company_info}")

                # Combine results
                financial_summary = f"""
                ### Financial Analysis for {topic}
                - **Historical Data**: {historical_data}
                - **Company Info**: {company_info}
                """
                return financial_summary

            except Exception as e:
                logger.error(f"Error analyzing financial data: {str(e)}")
                return f"Error analyzing financial data: {str(e)}"

        return Task(
            config=self.tasks_config['financial_analysis'],
            dependencies=[self.research],
            action=analyze_financials
        )

    @task
    def recommend(self) -> Task:
        def generate_recommendation(inputs):
            topic = inputs.get("topic")
            logger.info(f"Generating recommendation for {topic}...")

            try:
                # Fetch historical stock data
                stock = yf.Ticker(topic)
                history = stock.history(period="1mo")  # Fetch 1 month of historical data
                if history.empty:
                    return f"No historical data found for {topic}."

                # Generate stock trend visualization
                logger.info("Generating stock trend visualization...")
                trend_image = StockVisualizationTool()._run(topic, "trend")
                logger.info(f"Stock trend visualization saved at: {trend_image}")

                # Fetch company info for financial metrics
                info = stock.info
                company_summary = f"""
                Company: {info.get('longName', 'N/A')}
                Sector: {info.get('sector', 'N/A')}
                Market Cap: {info.get('marketCap', 'N/A')}
                P/E Ratio: {info.get('trailingPE', 'N/A')}
                EPS: {info.get('trailingEps', 'N/A')}
                Revenue Growth: {info.get('revenueGrowth', 'N/A')}
                """

                # Calculate percentage change in stock price over the past month
                price_change_percentage = ((history['Close'][-1] - history['Close'][0]) / history['Close'][0]) * 100

                # Fetch research and financial analysis summaries
                research_summary = self.research().action({"topic": topic})
                financial_summary = self.financial_analysis().action({"topic": topic})

                # Generate recommendation based on findings
                recommendation = "Hold"  # Default recommendation
                rationale = "Insufficient data to make a strong recommendation."

                # Example logic for generating recommendations
                if price_change_percentage > 5:  # If stock price increased by more than 5%
                    recommendation = "Buy"
                    rationale = "The stock has shown strong growth over the past month."
                elif price_change_percentage < -5:  # If stock price decreased by more than 5%
                    recommendation = "Sell"
                    rationale = "The stock has shown significant decline over the past month."

                # Generate recommendation text
                recommendation_text = f"""
                # Investment Recommendation Report for {topic}

                ## Qualitative Analysis
                {research_summary}

                ## Quantitative Analysis
                {financial_summary}

                ## Stock Performance
                - **Price Change (1 Month)**: {price_change_percentage:.2f}%
                - **Trend Visualization**: ![Stock Trend]({trend_image})

                ## Recommendation
                - **Recommendation**: {recommendation}
                - **Rationale**: {rationale}
                """

                # Save the recommendation report
                with open("recommendation_report.md", "w") as file:
                    file.write(recommendation_text)

                logger.info("Recommendation report generated successfully.")
                return recommendation_text

            except Exception as e:
                logger.error(f"Error generating recommendation: {str(e)}")
                return f"Error generating recommendation: {str(e)}"

        return Task(
            config=self.tasks_config['recommend'],
            dependencies=[self.financial_analysis, self.research],
            output_file='recommendation_report.md',
            action=generate_recommendation
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StockAnalysis crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,  # Sequential process flow
            verbose=True
        )