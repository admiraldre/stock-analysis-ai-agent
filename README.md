# Stock Analysis AI Agent

This project leverages CrewAI's Stock Analysis example as a starting point for building an AI-powered stock analysis tool. The initial example from CrewAI provided the foundational framework, which I’ve extended and modified to meet specific project needs.

In this version of the project, I’ve opted to use open-source alternatives to ensure better scalability and flexibility. Instead of relying on proprietary models, I integrated Local LLMs using **Ollama Mistral** embeddings. This enables more efficient and customizable interactions with the stock data, allowing for faster and more cost-effective processing of stock-related queries.



## Project Report (January 31, 2025) to ChmlTech Ltd.

**Stock Analysis AI Crew**

**w/ CrewAI, LangChain & LangSmith**

**Andrei Vivar**

January 31, 2025


## **1. Introduction**

This project aims to create an AI-powered stock analysis system that helps users make informed investment decisions. By combining real-time data, advanced AI models, and visual reporting tools, the system automates the process of researching stocks, analyzing financial data, and generating investment recommendations. Whether you're a seasoned investor or a beginner, this tool simplifies stock market analysis and provides actionable insights.


## **2. Key Features**


### **Here’s what the system can do:**



* **Automated Stock Research**: AI agents gather data from financial news, press releases, and market analyses.
* **Real-Time Data Analysis**: Tracks stock performance, financial metrics, and market trends as they happen.
* **Investment Recommendations**: Provides personalized suggestions based on historical data, financial health, and market sentiment.
* **Error Handling**: Ensures the system works smoothly even if data is missing or APIs fail.
* **Visual Reporting**: Creates easy-to-understand charts and graphs (e.g., stock trends, moving averages) to support decision-making.


## **3. Tools & Technologies**

The system uses a combination of cutting-edge tools and technologies:



* **CrewAI**: A framework for managing AI agents and coordinating tasks.
* **LangChain**: A tool for chaining language models and workflows, helping with data extraction, analysis, and response generation.
* **LangSmith**: A platform for testing, debugging, and optimizing AI workflows.
* **Ollama Mistral**: A powerful language model for understanding and generating natural language responses.
* **Google Serper API**: Fetches real-time news, press releases, and market analyses.
* **Yahoo Finance API**: Retrieves stock data, financial metrics, and company information.
* **Matplotlib**: A library for creating visualizations like stock price trends and volume charts.
* **yfinance**: A Python library for accessing historical stock data and company information.


## **4. Data Sources**

The system gathers data from multiple sources:



* **Real-Time Stock Market Data**: Fetched via Google Serper API and Yahoo Finance API.
* **Financial Metrics**: Retrieved from Yahoo Finance (e.g., P/E ratio, EPS, market cap).
* **Historical Stock Data**: Accessed via yfinance for trend analysis and visualizations.
* **News and Press Releases**: Collected from Google Serper API for qualitative analysis.


## **5. How It Works**


### **Step-by-Step Process**



1. **Input**: The user provides a company name (e.g., NVIDIA, Tesla, Apple).
2. **Data Collection**:
    * The **Researcher Agent** fetches news, press releases, and market analyses using Google Serper API.
    * The **Financial Analyst Agent** retrieves stock data and financial metrics using Yahoo Finance API and yfinance.
3. **Data Analysis**:
    * The **Researcher Agent** summarizes findings and identifies key events.
    * The **Financial Analyst Agent** analyzes stock performance, valuation metrics, and financial health.
4. **Visualization**:
    * The **Investment Advisor Agent** generates visualizations (e.g., stock trends, moving averages) using Matplotlib.
5. **Output**: The system produces a structured investment recommendation report with visualizations.


## **6. System Architecture**


### **Overview Diagram**



* **User Input**: The user enters a company name.
* **Data Collection**:
    * **Researcher Agent**: Fetches qualitative data (news, press releases, market analyses).
    * **Financial Analyst Agent**: Retrieves quantitative data (stock prices, financial metrics).
* **Data Analysis**:
    * **Researcher Agent**: Summarizes findings.
    * **Financial Analyst Agent**: Analyzes data and generates insights.
* **Visualization**:
    * **Investment Advisor Agent**: Creates charts and graphs.
* **Output**: The system delivers a detailed report with recommendations and visualizations.


## **7. Development Setup**


### **System Requirements**



* **Python 3.7+**
* Required libraries: `crewai`, `langchain`, `yfinance`, `matplotlib`, `requests`, `pydantic`, `dotenv`.


### **Setup Instructions**



1. Clone the repository.
2. Install dependencies: \
pip install -r requirements.txt
3. Set up API keys for Google Serper API and other services in the `.env` file.
4. Configure environment variables for API keys and other settings.


### **Running the System**

Execute the main script:

crewai run

Enter the company name (e.g., NVIDIA) when prompted. View the generated report and visualizations.

Example screenshots of the execution:

![screenshot1](https://i.imgur.com/yMDJRfr.png)

![screenshot2](https://i.imgur.com/gV6RvIq.png)

![screenshot3](https://i.imgur.com/kjnJUU5.png)

![screenshot4](https://i.imgur.com/mRdyBo5.png)

![screenshot5](https://i.imgur.com/Mj7iUIQ.png)

![screenshot6](https://i.imgur.com/bNABXIR.png)

Example outputs:

![screenshot7](https://i.imgur.com/3wjZMVz.png)

![screenshot8](https://i.imgur.com/6IKDxMX.png)

![screenshot9](https://i.imgur.com/sFDXQdK.png)

## **8. Testing and Debugging with LangSmith**

![screenshot10](https://i.imgur.com/CHqzlri.png)

### **What is LangSmith?**

LangSmith is a platform for testing, debugging, and optimizing AI workflows. It helps developers monitor how their AI agents perform, identify issues, and improve the system.


### **How LangSmith is Used in This Project**



* **Testing Workflows**: Tests the agents' ability to retrieve, process, and generate responses correctly.
* **Debugging**: Identifies and fixes issues in the data flow and agent interactions.
* **Optimization**: Provides insights into how to improve the system’s performance and accuracy.

Example View in LangSmith:



## **9. Challenges and Solutions**


### **Challenges**



* **Data Inconsistencies**: Different APIs may return outdated or incomplete data.
* **API Rate Limits**: Free-tier APIs often have limits on the number of queries.
* **Complex Workflows**: Coordinating multiple agents and tasks can be challenging.


### **Solutions**



* **Data Validation**: Ensure data consistency by using reliable sources and validating inputs.
* **Error Handling**: Implement mechanisms to handle API failures and missing data.
* **Workflow Optimization**: Use LangSmith to monitor and optimize workflows.


## **10. Limitations of Ollama Mistral**



* **Limited Financial Domain Knowledge**: While Mistral is good at natural language understanding, it may not have deep financial expertise.
* **Computational Resources**: Running Mistral locally requires substantial CPU/GPU power.
* **Fine-Tuning Challenges**: Limited support for domain-specific fine-tuning without external tools.
* **Output Inconsistencies:** Since this setup is using a local LLM, the setup only has the basic pre-trained version. The model is not trained for stock analysis, therefore causing hallucinations.


### **Configurations for Ollama Mistral**



* **Memory Management**: Adjust memory allocation to prevent slowdowns.
* **Temperature Settings**: Fine-tune response randomness by setting a lower temperature (e.g., `temperature=0.3`).
* **Prompt Engineering**: Structure prompts effectively to improve response quality.


## **11. Future Enhancements**



* **More Agent Roles**: Adding specialized agents for different market sectors.
* **Improved Models**: Implementing advanced models for stock predictions.
* **Broader Data Integration**: Incorporating additional data sources like social media sentiment and earnings call transcripts.
* **Real-Time Alerts**: Notifications for market shifts and anomalies.


## **12. Key Financial Terminologies**



* **P/E Ratio**: Measures a company's stock price relative to earnings.
* **EPS (Earnings Per Share)**: Indicates profitability per share.
* **Moving Averages**: Tracks trends over time.
* **Market Cap**: Total market value of a company’s outstanding shares.


## **13. Conclusion**

This project demonstrates how AI can simplify stock market analysis and provide actionable insights for investors. By combining real-time data, advanced AI models, and visual reporting tools, the system makes stock analysis accessible to everyone. With future enhancements, it has the potential to become an indispensable tool for investors.

**Github repository: [https://github.com/admiraldre/stock-analysis-ai-agent](https://github.com/admiraldre/stock-analysis-ai-agent)**

