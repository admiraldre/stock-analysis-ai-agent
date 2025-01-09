import requests

class InvestmentAdvisorAgent:
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
            result = response.json().get("response", "")
            print(f"Model response: {result}")  # Debugging output
            return result
        else:
            raise Exception(f"Error querying the model: {response.text}")

    def recommend_investments(self, market_conditions):
        prompt = f"""
        The current market conditions are as follows:
        {market_conditions}
        Based on these conditions, what is your recommendation for investing in this company at this moment? 
        Should investors buy, hold, or sell the stock, and why?
        """
        return self.query_model(prompt)