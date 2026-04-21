from dotenv import load_dotenv
import os
import finnhub

load_dotenv()
APIKEY = os.getenv("STOCK_DASHBOARD_APIKEY")

finnhub_client = finnhub.Client(api_key=APIKEY)

def get_quote(symbol: str):
    quote = finnhub_client.quote(symbol)
    if quote['c'] == 0:
        return None
    else:
        return quote