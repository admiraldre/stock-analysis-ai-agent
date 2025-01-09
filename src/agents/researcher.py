import requests

class ResearcherAgent:
    def __init__(self, model_name="mistral", server_url="http://localhost:11434/api/chat"):
        self.model_name = model_name
        self.server_url = server_url

    def query_model(self, prompt):
        payload = {
            "model": self.model_name,
            "prompt": prompt
        }
        response = requests.post(self.server_url, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            raise Exception(f"Error querying the model: {response.text}")

    def summarize_topic(self, topic):
        # Refine the prompt to make it more specific for the researcher model
        prompt = f"""
        Please provide a detailed summary of {topic}. 
        Include any recent developments, advancements, and any important business-related insights.
        What are the potential implications of these developments for the company's future prospects?
        """
        return self.query_model(prompt)