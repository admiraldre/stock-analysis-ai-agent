from langchain_community.embeddings import OllamaEmbeddings


class LLMTools:
    def __init__(self, model_name="mistral"):
        self.embedding_model = OllamaEmbeddings(model=model_name)

    def generate_embeddings(self, text):
        """
        Generates embeddings for a given text using a local LLM.
        """
        return self.embedding_model.embed_query(text)