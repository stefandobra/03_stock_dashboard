from dotenv import load_dotenv
import os
from twelvedata import TDClient

load_dotenv()
TWELVEDATA_APIKEY = os.getenv('STOCK_DASHBOARD_TWELVEDATA_APIKEY')

td = TDClient(apikey=TWELVEDATA_APIKEY)

def get_price_history(symbol, timeframe):
    interval = {
        '1D': '1min',
        '5D': '15min',
        '1M': '1h',
        '6M': '1day',
        '1Y': '1week',
        'ALL': '1month'
    }

    outputsize = {
        '1D': 390,
        '5D': 130,
        '1M': 137,
        '6M': 126,
        '1Y': 52,
        'ALL': 240
    }
    selected_interval = interval[timeframe]
    correct_outputsize = outputsize[timeframe]

    ts = td.time_series(
        symbol=symbol,
        interval=selected_interval,
        outputsize=correct_outputsize
    )

    return ts.as_json()


if __name__ == '__main__':
    print(get_price_history('AAPL', '5D'))