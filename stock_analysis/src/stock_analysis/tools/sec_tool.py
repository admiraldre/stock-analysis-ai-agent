from crewai.tools import BaseTool
from typing import Type, ClassVar
from pydantic import BaseModel, Field
import requests

class SECFilingsInput(BaseModel):
    company_ticker: str = Field(..., description="The stock ticker of the company (e.g., TSLA).")
    filing_type: str = Field(..., description="The type of SEC filing, e.g., 10-Q or 10-K.")

class SECFilingsTool(BaseTool):
    name: str = "SEC Filings Fetcher"
    description: str = "Fetches the latest SEC filings for a given company ticker."
    args_schema: Type[BaseModel] = SECFilingsInput

    SEC_API_KEY: ClassVar[str] = "d5443893aa14e1c2228a4d4ce2e48936a47060119fb67402992ace39e41ff666"

    def _run(self, company_ticker: str, filing_type: str) -> str:
        if not self.SEC_API_KEY:
            return "Error: Missing SEC API key."

        url = "https://api.sec-api.io/filings"
        headers = {"Authorization": f"Bearer {self.SEC_API_KEY}"}
        params = {"ticker": company_ticker, "formType": filing_type, "size": 1}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("filings", [{}])[0].get("linkToFilingDetails", "No filings found.")
        except requests.RequestException as e:
            return f"Error fetching data: {e}"
