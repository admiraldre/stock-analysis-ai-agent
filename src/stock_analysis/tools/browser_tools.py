from crewai_tools import tool
from crewai import Agent, Task
import requests
from bs4 import BeautifulSoup
from langchain_google_genai import (ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings,HarmBlockThreshold,
    HarmCategory,)
import os
from dotenv import load_dotenv
load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro",
        google_api_key=os.environ.get("GEMINI_API_KEY"),
        temperature=0.1,
        convert_system_message_to_human=True,
        safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
            }
    )

class BrowserTools():
    
    @tool("Scrape website content")
    def scrape_and_summarize_website(source_url: str) -> str:
        """Useful to scrape and summarize a website content with financial news, blog, etc."""
        response = requests.get(source_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            relevant_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'div', 'section', 'article'])    
            content = "\n\n".join([str(el) for el in relevant_elements])
            content_chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]
            summaries = []
            for chunk in content_chunks:
                agent = Agent(
                    role='Principal Researcher',
                    goal=
                    'Do amazing research and summaries based on the content you are working with',
                    backstory=
                    "You're a Principal Researcher at a big company and you need to do research about a given topic.",
                    allow_delegation=False,
                    llm=llm)
                task = Task(
                    agent=agent,
                    description=
                    f'Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}',
                    expected_output='A paragraph of the summary of the content provided. Should be detailed.'
                )
                summary = task.execute()
                summaries.append(summary)
            return "\n\n".join(summaries)
        else:
           return f"Failed to fetch content from {source_url}. Status code: {response.status_code}"