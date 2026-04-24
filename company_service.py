from dotenv import load_dotenv
import os
import finnhub

load_dotenv()
FINNHUB_APIKEY = os.getenv('STOCK_DASHBOARD_FINNHUB_APIKEY')
finnhub_client = finnhub.Client(api_key=FINNHUB_APIKEY)

def get_profile(symbol):
    company_profile = finnhub_client.company_profile2(symbol=symbol)
    if company_profile:
        return company_profile
    else:
        return None
