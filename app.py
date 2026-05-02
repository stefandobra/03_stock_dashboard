from flask import Flask, render_template, request, redirect, jsonify
from stock_service import get_quote
from history_service import get_price_history
from news_service import get_news
from company_service import get_profile, format_market_cap, format_shares
from db import create_tables
from watchlist_service import view_watchlist, add_symbol, remove_symbol
from portfolio_service import view_portfolio, remove_from_portfolio, add_to_portfolio
from compare_service import get_earnings, get_financials
from alerts_service import get_alerts, create_alert, delete_alert, get_triggered_alerts

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
                                    close_price=close_price, company_profile=company_profile,
                                    company_news=company_news, market_cap=market_cap, shares=shares)
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
        shares = request.form.get('shares')
        price = request.form.get('price')
        add_to_portfolio(symbol.upper(), shares, price)
        return {"success": True}
    return {"success": False}

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'GET':
        return render_template('compare.html')
    else:
        symbol1 = request.form.get('symbol1')
        symbol2 = request.form.get('symbol2')
        
        if symbol1 and symbol2:
            quote1 = get_quote(symbol1.upper())
            quote2 = get_quote(symbol2.upper())
            
            if not quote1 or not quote2:
                return render_template('compare.html', message='One or both symbols are invalid')
            
            profile1 = get_profile(symbol1)
            profile2 = get_profile(symbol2)

            market_cap1 = format_market_cap(profile1['marketCapitalization']) if profile1 else None
            market_cap2 = format_market_cap(profile2['marketCapitalization']) if profile2 else None
            
            financials1 = get_financials(symbol1)
            financials2 = get_financials(symbol2)

            earnings1 = get_earnings(symbol1)
            earnings2 = get_earnings(symbol2)
            
            return render_template('compare.html', symbol1=symbol1, symbol2=symbol2, quote1=quote1, quote2=quote2,
                                   profile1=profile1, profile2=profile2, market_cap1=market_cap1, market_cap2=market_cap2,
                                   financials1=financials1, financials2=financials2, earnings1=earnings1, earnings2=earnings2)
        return render_template('compare.html', symbol1=symbol1, symbol2=symbol2)
    
@app.route('/alerts', methods=['GET', 'POST'])
def alerts():
    if request.method == 'GET':
        alerts = get_alerts()
        alerts_data = {}
        for alert in alerts:
            alert_id = alert['id']
            symbol = alert['symbol']
            target_price = alert['target_price']
            direction = alert['direction']
            triggered = alert['triggered']
            date_time = alert['dateadded']
            quote = get_quote(symbol.upper())
            if quote:
                current_price = quote['c']
                alerts_data[alert_id] = {
                    'symbol': symbol,
                    'target_price': target_price,
                    'current_price': current_price,
                    'direction': direction,
                    'triggered': triggered,
                    'date_added': date_time
                }      
        return render_template('alerts.html', alerts_data=alerts_data)
    else:
        action = request.form.get('action')
        if action == 'create':
            symbol = request.form.get('symbol')
            target_price = request.form.get('target_price')
            direction = request.form.get('direction')
            create_alert(symbol, target_price, direction)
            return redirect('/alerts')
        elif action == 'delete':
            alert_id = request.form.get('alert_id')
            delete_alert(alert_id)
            return redirect('/alerts')

@app.route('/alerts/pending', methods=['GET'])
def alerts_pending():
    triggered_alerts = get_triggered_alerts()
    dict_triggered_alerts = []
    
    dict_triggered_alerts = [dict(alert) for alert in triggered_alerts]
    return jsonify(dict_triggered_alerts)
    
if __name__ == '__main__':
    app.run(debug=True)
    





