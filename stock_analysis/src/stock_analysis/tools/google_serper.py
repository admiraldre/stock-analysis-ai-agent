from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from langchain_community.utilities import GoogleSerperAPIWrapper
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

class GoogleSerperInput(BaseModel):
    """
    Input schema for Google Serper Tool.
    """
    company_name: str = Field(..., description="The name of the company to search for.")
    query_type: str = Field(..., description="Type of search query: 'news', 'press release', 'market analysis'")

class GoogleSerperLangChainTool(BaseTool):
    """
    LangChain Tool for fetching search results from Google Serper.
    """
    name: str = "Google Serper Search Tool"
    description: str = "Fetches recent news, press releases, and market analysis from the Google Serper API."
    args_schema: Type[BaseModel] = GoogleSerperInput

    def fetch_with_retry(self, url, headers, retries=3, delay=2):
        """Handles retries with exponential backoff."""
        for i in range(retries):
            try:
                response = requests.get(url, headers=headers, timeout=10)  # 10 second timeout
                response.raise_for_status()  # Ensure we handle HTTP errors
                return response.json()
            except requests.exceptions.Timeout:
                if i < retries - 1:
                    time.sleep(delay * (2 ** i))  # Exponential backoff
                else:
                    return "Error: The request timed out. Please try again later."
            except requests.exceptions.RequestException as e:
                return f"Error fetching data: {e}"

    def _run(self, company_name: str, query_type: str) -> str:
        """
        Method to fetch search results from Google Serper API via LangChain.
        """
        try:
            api_key = os.getenv("GOOGLE_SERPER_API_KEY")
            if not api_key:
                return "Error: GOOGLE_SERPER_API_KEY not set in .env file."

            query = f"{company_name} {query_type}"
            url = f"https://google.serper.dev/search?q={query}"
            headers = {"X-API-KEY": api_key}

            # Fetch the results with retry logic
            data = self.fetch_with_retry(url, headers)
            if isinstance(data, str):
                return data

            results = data.get("organic", [])
            if not results:
                return f"No search results found for query '{query}'. Please check the input or try again."

            search_results = "\n".join([f"{result['title']}: {result['link']}" for result in results[:5]])
            return search_results

        except Exception as e:
            return f"Error fetching data: {str(e)}"