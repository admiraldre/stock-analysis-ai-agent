import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SEC_API_API_KEY = os.getenv("SEC_API_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")