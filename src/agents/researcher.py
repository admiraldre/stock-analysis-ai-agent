class Researcher:
    def __init__(self):
        pass

    def gather_data(self, company_name):
        # mock data for now
        print(f"Researching data for {company_name}...")
        return {
            "financials": {"revenue": "10B", "profit": "2B"},
            "news": ["Company hits new revenue milestone.", "Strong market performance."],
            "trends": ["Bullish sentiment", "Increasing market share"]
        }