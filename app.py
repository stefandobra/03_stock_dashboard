from flask import Flask, render_template, request, redirect
from stock_service import get_quote
from history_service import get_price_history
from news_service import get_news
from company_service import get_profile, format_market_cap, format_shares
from db import create_tables
from watchlist_service import view_watchlist, add_symbol, remove_symbol
from portfolio_service import view_portfolio, remove_from_portfolio, add_to_portfolio

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
    
@app.route('/watchlist', methods=['GET', 'POST'])
def watchlist():
    if request.method == 'GET':
        watchlist = view_watchlist()
        watchlist_data = {}
        for row in watchlist:
            symbol = row['symbol']
            quote = get_quote(symbol.upper())
            watchlist_data[symbol] = quote
        return render_template('watchlist.html', watchlist_data=watchlist_data)
    else:
        symbol = request.form.get('symbol')
        remove_symbol(symbol)
        return redirect('/watchlist')
    
@app.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    symbol = request.form.get('symbol')
    if symbol:
        watchlist = view_watchlist()
        for row in watchlist:
            if row['symbol'] == symbol.upper():
                return {"success": False}
        add_symbol(symbol.upper())
        return {"success": True}
    return {"success": False}

@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    if request.method == 'GET':
        portfolio = view_portfolio()
        portfolio_data = {}
        for row in portfolio:
            symbol = row['symbol']
            shares = row['sharesowned']
            avg_price = row['avgprice']
            quote = get_quote(symbol.upper())
            if quote:
                current_price = quote['c']
                value = current_price * shares
                pl = (current_price - avg_price) * shares
                portfolio_data[symbol] = {
                    'shares': shares,
                    'avg_price': avg_price,
                    'current_price': current_price,
                    'value': value,
                    'pl': pl
                }
        return render_template('portfolio.html', portfolio_data=portfolio_data)
    else:
        symbol = request.form.get('symbol')
        remove_from_portfolio(symbol)
        return redirect('/portfolio')
    
@app.route('/add_to_portfolio', methods=['POST'])
def add_portfolio_entry():
    symbol = request.form.get('symbol')
    if symbol:
        portfolio = view_portfolio()
        shares = request.form.get('shares')
        price = request.form.get('price')
        add_to_portfolio(symbol.upper(), shares, price)
        return {"success": True}
    return {"success": False}


if __name__ == '__main__':
    app.run(debug=True)
    





