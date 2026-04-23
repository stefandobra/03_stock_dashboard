from flask import Flask, render_template, request
from stock_service import get_quote
from history_service import get_price_history

app = Flask(__name__)

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
            return render_template('index.html', quote=quote, symbol=symbol, price_history=price_history)
        return render_template('index.html', quote=quote)

if __name__ == '__main__':
    app.run(debug=True)
    





