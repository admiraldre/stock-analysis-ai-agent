import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from tools.sec_tool import SECFilingsTool
from tools.serper_tool import SerperSearchTool

# Initialize the LLM model (this part can be changed based on LLM setup)
llm = LLM(
    model='ollama/mistral',
    temperature=0.7,
    base_url='http://localhost:11434',
)

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
            tools=[SerperSearchTool()],
            verbose=True
        )

    @agent
    def financial_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst'],
            llm=llm,
            tools=[SECFilingsTool(),
                   SerperSearchTool()],
            verbose=True
        )

    @agent
    def investment_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['investment_advisor'],
            llm=llm,
            verbose=True
        )

    # Tasks for performing actions
    @task
    def research(self) -> Task:
        # Task action - gather news, data, and analysis
        # You can also log this output for debugging
        action_result = "Research data gathered."
        return Task(
            config=self.tasks_config['research'],
            # output_file='research_report.md',
            result=action_result  # Pass the result of the action
        )
    
    @task
    def financial_analysis(self) -> Task:
        # Perform financial analysis after research task is completed
        action_result = "Financial analysis completed."
        return Task(
            config=self.tasks_config['financial_analysis'],
            dependencies=[self.research],
            result=action_result  # Pass the result of the analysis
        )
    
    @task
    def filings_analysis(self) -> Task:
        # Perform SEC filings analysis after financial analysis
        action_result = "SEC filings analysis completed."
        return Task(
            config=self.tasks_config['filings_analysis'],
            dependencies=[self.financial_analysis],
            result=action_result  # Pass the result of the filings analysis
        )
    
    @task
    def recommend(self) -> Task:
        # Final recommendation task after all analysis is completed
        action_result = "Recommendation generated based on the analysis."
        return Task(
            config=self.tasks_config['recommend'],
            dependencies=[self.financial_analysis, self.research, self.filings_analysis],
            output_file='recommendation_report.md',
            result=action_result  # Pass the result of the recommendation
        )

    # Crew configuration
    @crew
    def crew(self) -> Crew:
        """Creates the StockAnalysis crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,  # Sequential process flow
            verbose=True,
        )
