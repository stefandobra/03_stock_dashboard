# 03 Stock Dashboard

A Flask web dashboard for live stock data, news, AI insights and portfolio tracking. Built in Python as part of a portfolio project series demonstrating AI and full-stack development skills.

## Features (Planned)

- Live stock prices — current price, change, % change, high, low, open, previous close
- Price history with multiple timeframes — via Twelve Data API
- Watchlist — save and track favourite stocks
- News feed per stock
- Price alerts
- Paper trading simulator
- Compare two stocks side by side
- Sector and industry info
- Portfolio tracker — shares owned, total value, P&L
- AI summary and insights — via Anthropic API

> Note: Volume and candlestick data require a Finnhub premium plan and are not included in the free tier.

## Project Structure

```
03_stock_dashboard/
│
├── app.py                  # Flask entry point — routes and request handling
├── stock_service.py        # Finnhub API — live quotes
├── news_service.py         # News feed per stock
├── portfolio_service.py    # Portfolio and watchlist logic
├── trade_service.py        # Paper trading simulator
├── ai_service.py           # Anthropic API — AI summary and insights
├── templates/
│   └── index.html          # Main dashboard HTML template
├── static/
│   ├── css/                # Stylesheets
│   └── js/                 # JavaScript
├── requirements.txt
└── .env                    # API keys (not committed)
```

## Concepts Demonstrated

- Flask web framework — routing, GET/POST handling, debug mode
- Jinja2 templating — variables, if/elif/endif, loops
- REST API integration — Finnhub (live quotes) and Twelve Data (price history)
- Virtual environment — isolated dependencies with venv
- Environment variables — secure API key management with python-dotenv
- Separation of concerns — logic split across service files
- Input validation — invalid symbol handling with user-friendly error messages
- Anthropic API — AI-generated stock insights

## How to Run

```bash
cd 03_stock_dashboard
venv\Scripts\activate
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## APIs Used

- [Finnhub](https://finnhub.io/) — live stock quotes and news (free tier)
- [Twelve Data](https://twelvedata.com/) — price history and volume (free tier)
- [Anthropic](https://www.anthropic.com/) — AI summary and insights

## Part of a Larger Project Series

| # | Project | Status |
|---|---------|--------|
| 01 | Finance Tracker | ✅ Complete |
| 02 | Booking System | ✅ Complete |
| 03 | Stock Dashboard | 🔄 In Progress |
| 04 | Fraud Detection ML | ⏳ Planned |
| 05 | Security Tool | ⏳ Planned |
| 06 | YouTube/TikTok Pipeline | ⏳ Planned |
| 07 | AI Receptionist (SaaS) | ⏳ Capstone |