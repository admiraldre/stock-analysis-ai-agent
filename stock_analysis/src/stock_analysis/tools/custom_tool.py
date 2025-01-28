from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

import requests
from dotenv import load_dotenv
load_dotenv()

class SECFilingsInput(BaseModel):
    """Input schema for the SEC Filings tool."""
    company_name: str = Field(..., description="The name of the company to get SEC filings for.")
    filing_type: str = Field(..., description="The type of filing, e.g., 10-Q or 10-K.")

class SECFilingsTool(BaseTool):
    name: str = "SEC Filings Fetcher"
    description: str = "Fetches the latest financial filings (e.g., 10-Q, 10-K) from the SEC API."
    args_schema: Type[BaseModel] = SECFilingsInput

    def _run(self, company_name: str, filing_type: str) -> str:
        # Use SEC's EDGAR API (or the SEC EDGAR RSS feed)
        base_url = "https://www.sec.gov/edgar/search-api"
        headers = {"User-Agent": "YourAppName/1.0 (your.email@example.com)"}
        params = {
            "q": company_name,
            "category": "forms",
            "type": filing_type,
            "count": 1,  # Fetch the most recent
        }

        response = requests.get(f"{base_url}/company", headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            filings = data.get("hits", [])
            if filings:
                filing = filings[0]
                return f"Filing Title: {filing['title']}\nURL: {filing['file_url']}"
            else:
                return f"No {filing_type} filings found for {company_name}."
        else:
            return f"Error fetching data from SEC API: {response.status_code}"