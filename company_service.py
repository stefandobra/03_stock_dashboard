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
    
def format_market_cap(market_cap):
    if market_cap >= 1_000_000:
        return f'${market_cap/1_000_000:,.2f}T'
    elif market_cap >= 1_000:
        return f'${market_cap/1_000:,.2f}B'
    else:
        return f'${market_cap:,.2f}M'

def format_shares(shares):
    if shares >= 1_000:
        return f'{shares/1_000:,.2f}B shares'
    elif shares >= 1 :
        return f'{shares:,.2f}M shares'
    else:
        return f'{shares*1_000_000:,.2f} shares'