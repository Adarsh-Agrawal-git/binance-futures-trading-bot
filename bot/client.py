from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

def get_client():
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("API keys missing. Check .env file")

    client = Client(api_key, api_secret)

    # Futures Testnet URL
    client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    return client