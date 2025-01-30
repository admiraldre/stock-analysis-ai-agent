from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests
from dotenv import load_dotenv
from serper_tool import SerperSearchTool  

load_dotenv()

class SECFilingsInput(BaseModel):
    company_name: str = Field(..., description="The name of the company to get SEC filings for.")
    filing_type: str = Field(..., description="The type of filing, e.g., 10-Q or 10-K.")

class SECFilingsTool(BaseTool):
    name: str = "SEC Filings Fetcher"
    description: str = "Fetches the latest financial filings (e.g., 10-Q, 10-K) from the SEC API."
    args_schema: Type[BaseModel] = SECFilingsInput

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_company_ticker(self, company_name: str) -> str:
        search_tool = SerperSearchTool()
        search_results = search_tool._run(company_name, "stock")
        
        if not search_results:
            return "Error: Unable to fetch company ticker from SERPER."
        
        if 'ticker' in search_results:
            return search_results['ticker']
        
        return "Error: Ticker not found in SERPER search results."

    def _run(self, company_name: str, filing_type: str) -> str:
        api_key = os.getenv("SEC_API_API_KEY")
        if not api_key:
            return "Error: SEC API key is missing in environment variables."
        
        company_ticker = self.get_company_ticker(company_name)
        if "Error" in company_ticker:
            return company_ticker

        base_url = "https://api.sec-api.io"
        headers = {"User-Agent": "drevivar2001@gmail.com", "Authorization": f"Bearer {api_key}"}
        params = {"q": company_ticker, "formType": filing_type, "size": 1, "sort": [{"filedAt": {"order": "desc"}}]}

        response = requests.get(base_url + "/filings", headers=headers, params=params)
        
        if response.status_code != 200:
            return f"Error fetching SEC filings: {response.status_code}"
        
        filings = response.json().get("filings", [])
        if not filings:
            return "No filings found."
        
        filing_details = filings[0]
        return filing_details.get("linkToFilingDetails", "No filing details found.")
