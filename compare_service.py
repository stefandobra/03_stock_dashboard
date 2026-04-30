from dotenv import load_dotenv
import os
import finnhub

load_dotenv()
FINNHUB_APIKEY = os.getenv('STOCK_DASHBOARD_FINNHUB_APIKEY')
finnhub_client = finnhub.Client(api_key=FINNHUB_APIKEY)

def get_financials(symbol):
    financials = finnhub_client.company_basic_financials(symbol=symbol, metric='all')
    if financials['metric']:
        return financials['metric']
    else:
        return None
    
def get_earnings(symbol):
    earnings = finnhub_client.company_earnings(symbol=symbol)
    if earnings:
        return earnings
    else:
        return None
