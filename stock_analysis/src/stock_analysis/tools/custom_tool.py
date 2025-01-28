from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

# Define input schema for SEC filings tool
class SECFilingsInput(BaseModel):
    company_name: str = Field(..., description="The name of the company to get SEC filings for.")
    filing_type: str = Field(..., description="The type of filing, e.g., 10-Q or 10-K.")

# SEC filings tool to fetch data
class SECFilingsTool(BaseTool):
    name: str = "SEC Filings Fetcher"
    description: str = "Fetches the latest financial filings (e.g., 10-Q, 10-K) from the SEC API."
    args_schema: Type[BaseModel] = SECFilingsInput

    def get_company_ticker(self, company_name: str) -> str:
        """
        Fetches the company ticker from the SEC API using the company's name.
        """
        base_url = "https://www.sec.gov/files/company_tickers.json"
        print(f"Fetching company ticker for: {company_name}")
        response = requests.get(base_url)
        
        if response.status_code != 200:
            print(f"Error: Unable to fetch company tickers from SEC API. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return f"Error: Unable to fetch company tickers from SEC API. Status Code: {response.status_code}"

        tickers = response.json()
        print(f"Tickers data: {tickers}")  # Debug print to inspect the returned data
        # Iterate through the tickers to find the company
        for key, value in tickers.items():
            if value["title"] and company_name.lower() in value["title"].lower():
                print(f"Found ticker for {company_name}: {value['symbol']}")
                return value["symbol"]
        
        print(f"Error: Ticker for company {company_name} not found.")
        return f"Error: Ticker for company {company_name} not found."

    def _run(self, company_name: str, filing_type: str) -> str:
        # Load the API key
        api_key = os.getenv("SEC_API_API_KEY")
        if not api_key:
            print("Error: SEC API key is missing in environment variables.")
            return "Error: SEC API key is missing in environment variables."
        
        # Step 1: Get the company ticker from SEC
        company_ticker = self.get_company_ticker(company_name)
        if "Error" in company_ticker:
            return company_ticker  # Return error if ticker is not found

        # API request setup
        base_url = "https://www.sec.gov/edgar/search-api/search"
        headers = {
            "User-Agent": "drevivar2001@gmail.com",
            "Authorization": f"Bearer {api_key}"
        }
        params = {
            "q": company_ticker,  # Use the ticker instead of the company name
            "category": "forms",
            "type": filing_type,
            "count": 1  # Fetch the most recent filing
        }
        
        print(f"Making API request to SEC: {base_url}/company with params: {params}")
        # Make the API request
        response = requests.get(f"{base_url}/company", headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: Unable to fetch data from SEC API. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return f"Error: Unable to fetch data from SEC API. Status Code: {response.status_code}"

        # Parse response data
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse response JSON. Exception: {e}")
            return "Error: Failed to parse SEC API response."

        print(f"API Response Data: {data}")  # Debug print to inspect the full response

        filings = data.get("hits", [])
        if not filings:
            print(f"No filings found for {company_name} (Ticker: {company_ticker}) of type {filing_type}.")
            return f"No filings found for {company_name} (Ticker: {company_ticker}) of type {filing_type}."
        
        # Return the most recent filing
        filing = filings[0]
        print(f"Most Recent Filing: {filing}")  # Debug print to inspect the filing data
        return f"Filing Title: {filing.get('title')}\nURL: {filing.get('file_url')}"

    def get_final_answer(self, action_result: str) -> str:
        # Directly return the formatted result or error message
        return action_result


# Define input schema for SERPER search tool
class SerperSearchInput(BaseModel):
    company_name: str = Field(..., description="The name of the company to search for.")
    query_type: str = Field(..., description="The type of search query, e.g., 'news', 'press release', 'market analysis'")

# SERPER search tool to fetch search results
class SerperSearchTool(BaseTool):
    name: str = "SERPER Search Tool"
    description: str = "Fetches search results from the SERPER API."
    args_schema: Type[BaseModel] = SerperSearchInput

    def _run(self, company_name: str, query_type: str) -> str:
        # Load the API key
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return "Error: SERPER API key is missing in environment variables."

        # API request setup
        query = f"{company_name} {query_type}"
        url = f"https://google.serper.dev/search?q={query}"
        headers = {"X-API-KEY": api_key}

        # Make the API request
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Error: Unable to fetch data from SERPER API. Status Code: {response.status_code}"

        # Parse response data
        data = response.json()
        results = data.get("organic", [])
        if not results:
            return f"No search results found for query '{query}'."
        
        # Return formatted search results
        search_results = "\n".join([f"{result['title']}: {result['link']}" for result in results[:5]])
        return f"Search Results:\n{search_results}"

    def get_final_answer(self, action_result: str) -> str:
        # Directly return the formatted result or error message
        return action_result

# Example usage of the tools
def run_serper_search(company_name: str, query_type: str):
    serper_search_tool = SerperSearchTool()

    # Step 1: Run search for the user-defined company name and query type
    print(f"Running search for: {company_name} with query type: {query_type}")
    action_result = serper_search_tool._run(company_name=company_name, query_type=query_type)  # Perform the action
    final_answer = serper_search_tool.get_final_answer(action_result)  # Process and get final answer
    print(final_answer)

def run_sec_filings_search(company_name: str, filing_type: str):
    sec_filings_tool = SECFilingsTool()

    # Step 1: Run search for the user-defined company name and filing type
    print(f"Running SEC filings search for: {company_name} with filing type: {filing_type}")
    action_result = sec_filings_tool._run(company_name=company_name, filing_type=filing_type)  # Perform the action
    final_answer = sec_filings_tool.get_final_answer(action_result)  # Process and get final answer
    print(final_answer)

