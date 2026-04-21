from flask import Flask, render_template, request
from stock_service import get_quote

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    quote = None
    if request.method == 'GET':
        return render_template('index.html', quote=quote)
    else:
        symbol = request.form.get('symbol')
        if symbol:
            quote = get_quote(symbol.upper())
            return render_template('index.html', quote=quote, symbol=symbol)
        return render_template('index.html', quote=quote)

if __name__ == '__main__':
    app.run(debug=True)
    





