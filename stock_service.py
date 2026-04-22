from dotenv import load_dotenv
import os
import finnhub

load_dotenv()
FINNHUB_APIKEY = os.getenv('STOCK_DASHBOARD_FINNHUB_APIKEY')

finnhub_client = finnhub.Client(api_key=FINNHUB_APIKEY)

def get_quote(symbol: str):
    quote = finnhub_client.quote(symbol)
    if quote['c'] == 0:
        return None
    else:
        return quote