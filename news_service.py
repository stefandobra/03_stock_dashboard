from dotenv import load_dotenv
import os
import finnhub
import datetime

load_dotenv()
FINNHUB_APIKEY = os.getenv('STOCK_DASHBOARD_FINNHUB_APIKEY')
finnhub_client = finnhub.Client(api_key=FINNHUB_APIKEY)

# Defaults to last 7 days of news — None parameters allow custom date ranges if needed elsewhere
def get_news(symbol, from_date=None, to_date=None):
    
    from_date = datetime.date.today() - datetime.timedelta(days=7) if from_date is None else from_date
    to_date = datetime.date.today() if to_date is None else to_date

    company_news = finnhub_client.company_news(symbol, from_date, to_date)
    if company_news:
        return company_news
    else:
        return None
