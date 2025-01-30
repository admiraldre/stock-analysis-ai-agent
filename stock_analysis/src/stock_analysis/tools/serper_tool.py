from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class SerperSearchInput(BaseModel):
    company_name: str = Field(..., description="The name of the company to search for.")
    query_type: str = Field(..., description="The type of search query, e.g., 'news', 'press release', 'market analysis'")

class SerperSearchTool(BaseTool):
    name: str = "SERPER Search Tool"
    description: str = "Fetches recent news, press releases, and market analysis from the SERPER API."
    args_schema: Type[BaseModel] = SerperSearchInput

    def _run(self, company_name: str, query_type: str) -> str:
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return "Error: SERPER API key is missing in environment variables."

        query = f"{company_name} {query_type}"
        url = f"https://google.serper.dev/search?q={query}"
        headers = {"X-API-KEY": api_key}

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Error: Unable to fetch data from SERPER API. Status Code: {response.status_code}"

        data = response.json()
        results = data.get("organic", [])
        if not results:
            return f"No search results found for query '{query}'."

        search_results = "\n".join([f"{result['title']}: {result['link']}" for result in results[:5]])
        
        return search_results
