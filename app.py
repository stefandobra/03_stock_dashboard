from flask import Flask, render_template
from stock_service import get_quote

app = Flask(__name__)

@app.route('/')
def index():
    quote = get_quote('AAPL')
    return render_template('index.html', quote=quote)
    

if __name__ == '__main__':
    app.run(debug=True)
    





