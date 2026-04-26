from flask import Flask, render_template, request
from stock_service import get_quote
from history_service import get_price_history
from news_service import get_news
from company_service import get_profile, format_market_cap, format_shares
from db import create_tables

app = Flask(__name__)
create_tables()

@app.route('/', methods=['GET', 'POST'])
def index():
    quote = None
    if request.method == 'GET':
        return render_template('index.html', quote=quote, symbol=None)
    else:
        symbol = request.form.get('symbol')
        timeframe = request.form.get('timeframe')
        if symbol:
            quote = get_quote(symbol.upper())

            price_history = get_price_history(symbol.upper(), timeframe)
            date_time = []
            close_price = []
            for price in price_history:
                date_time.append(price['datetime'])
                close_price.append(price['close'])
            date_time.reverse()
            close_price.reverse()

            company_profile = get_profile(symbol)
            company_news = get_news(symbol)
            
            market_cap = format_market_cap(company_profile['marketCapitalization']) if company_profile else None
            shares = format_shares(company_profile['shareOutstanding']) if company_profile else None
            return render_template('index.html', quote=quote, symbol=symbol, date_time=date_time, 
                    close_price=close_price, company_profile=company_profile, company_news=company_news,
                    market_cap=market_cap, shares=shares)
        return render_template('index.html', quote=quote)

if __name__ == '__main__':
    app.run(debug=True)
    





