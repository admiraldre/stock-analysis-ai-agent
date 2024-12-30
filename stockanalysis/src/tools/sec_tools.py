import os
from langchain.tools import tool
from sec_api import QueryApi
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from unstructured.partition.html import partition_html
import requests


class SECTools:
    def __init__(self):
        self.query_api = QueryApi(api_key=os.getenv("SEC_API_API_KEY"))

    @tool("Search 10-Q form")
    def search_10q(self, data):
        """
        Search the latest 10-Q form for a given stock and answer a specific question.
        Input: `stock_ticker|question`
        """
        stock, ask = data.split("|")
        return self._fetch_and_answer(stock, ask, "10-Q")

    @tool("Search 10-K form")
    def search_10k(self, data):
        """
        Search the latest 10-K form for a given stock and answer a specific question.
        Input: `stock_ticker|question`
        """
        stock, ask = data.split("|")
        return self._fetch_and_answer(stock, ask, "10-K")

    def _fetch_and_answer(self, stock, ask, form_type):
        query = {
            "query": {"query_string": {"query": f'ticker:{stock} AND formType:"{form_type}"'}},
            "from": "0",
            "size": "1",
            "sort": [{"filedAt": {"order": "desc"}}],
        }

        filings = self.query_api.get_filings(query).get("filings", [])
        if not filings:
            return f"Sorry, I couldn't find any {form_type} filings for {stock}."

        link = filings[0]["linkToFilingDetails"]
        return self._embedding_search(link, ask)

    def _embedding_search(self, url, ask):
        text = self._download_form_html(url)
        elements = partition_html(text=text)
        content = "\n".join([str(el) for el in elements])
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        docs = text_splitter.create_documents([content])

        retriever = FAISS.from_documents(docs, OllamaEmbeddings(model="mistral")).as_retriever()
        answers = retriever.get_relevant_documents(ask, top_k=4)
        return "\n\n".join([a.page_content for a in answers])

    def _download_form_html(self, url):
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        return response.text