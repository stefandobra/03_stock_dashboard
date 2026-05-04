# 03 Stock Dashboard

A Flask web dashboard for live stock data, news, AI insights and portfolio tracking. Built in Python as part of a portfolio project series demonstrating AI and full-stack development skills.

## Features

- Live stock prices — current price, change, % change, high, low, open, previous close
- Price history with multiple timeframes — 1D, 5D, 1M, 6M, 1Y, ALL via Twelve Data API
- Watchlist — save and track favourite stocks
- News feed per stock
- Compare two stocks side by side — financials, earnings, market cap
- Portfolio tracker — shares owned, average buy price, total value, P&L
- Price alerts — set target price and direction (above/below), background scheduler checks every 60s, in-page banner notification on trigger
- AI summary — portfolio and alerts insights via Anthropic API

> Note: Volume and candlestick data require a Finnhub premium plan and are not included in the free tier.

## Project Structure

```
03_stock_dashboard/
│
├── app.py                   # Flask entry point — routes and request handling
├── db.py                    # SQLite connection management and schema creation
├── stock_service.py         # Finnhub API — live quotes
├── history_service.py       # Twelve Data API — price history (OHLCV)
├── news_service.py          # Finnhub API — company news feed
├── company_service.py       # Finnhub API — company profiles and market cap
├── compare_service.py       # Financial metrics and earnings for comparison
├── watchlist_service.py     # SQLite CRUD — watchlist
├── portfolio_service.py     # SQLite CRUD — portfolio with P&L calculations
├── alerts_service.py        # SQLite CRUD — price alerts + trigger/notify state
├── scheduler_service.py     # APScheduler background job — checks alert conditions every 60s
├── ai_service.py            # Anthropic API — AI-generated portfolio and alerts summary
├── templates/               # Jinja2 HTML templates
├── static/
│   ├── css/                 # Stylesheets
│   └── js/
│       └── alerts.js        # Polls /alerts/pending every 30s, shows in-page banner on trigger
├── requirements.txt
└── .env                     # API keys (not committed)
```

## How to Run

```powershell
cd 03_stock_dashboard
venv\Scripts\activate
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

Requires a `.env` file with:

```
STOCK_DASHBOARD_FINNHUB_APIKEY=...
STOCK_DASHBOARD_TWELVEDATA_APIKEY=...
ANTHROPIC_API_KEY=...
```

## APIs Used

- [Finnhub](https://finnhub.io/) — live stock quotes, news, company profiles (free tier)
- [Twelve Data](https://twelvedata.com/) — price history with OHLCV data (free tier)
- [Anthropic](https://www.anthropic.com/) — AI summary and insights

## Concepts Demonstrated

- Flask web framework — routing, GET/POST handling, action-based form branching, debug mode
- Jinja2 templating — variables, conditionals, loops, template reuse
- SQLite — schema design, CRUD operations, row factory for dict-style access
- REST API integration — Finnhub and Twelve Data
- AJAX — fetch() for watchlist/portfolio actions and alert polling without page reload
- Chart.js — interactive price history chart with multiple timeframes
- APScheduler — background job running independently of the request cycle
- Price alerts — trigger/notify state machine to prevent repeat notifications
- Browser notifications — in-page DOM banner with dismiss, stacking support
- Separation of concerns — thin route layer delegating to single-responsibility service modules
- Input validation — server-side validation layered under HTML required attributes
- Environment variables — secure API key management with python-dotenv
- Anthropic API — prompt caching on system prompt, structured JSON response parsing

## Part of a Larger Project Series

| # | Project | Status |
|---|---------|--------|
| 01 | Finance Tracker | ✅ Complete |
| 02 | Booking System | ✅ Complete |
| 03 | Stock Dashboard | ✅ Complete |
| 04 | Fraud Detection ML | ⏳ Planned |
| 05 | RAG System | ⏳ Planned |
| 06 | AI Agent | ⏳ Planned |
| 07 | Multi-Agent System | ⏳ Planned |
| 08 | AI Receptionist SaaS (Capstone) | ⏳ Planned |

---

*All code written by Stefan Dobra. Claude Code (Anthropic) was used as a terminal coding assistant from the price alerts feature onwards.*
