# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```powershell
# Activate virtual environment (Windows)
venv\Scripts\activate

# Run the Flask dev server
python app.py
```

App runs at http://127.0.0.1:5000. The SQLite database (`stock_dashboard.db`) is created automatically on first run.

Requires a `.env` file with:
```
FINNHUB_API_KEY=...
TWELVE_DATA_API_KEY=...
ANTHROPIC_API_KEY=...
```

There are no tests and no build/lint commands configured.

## Architecture

Flask app with a thin route layer (`app.py`) delegating to single-responsibility service modules. Data flows: route handler → service → external API or SQLite → Jinja2 template.

### Service Modules

| File | Responsibility |
|---|---|
| `stock_service.py` | Live quotes via Finnhub |
| `history_service.py` | Price history via Twelve Data (timeframes: 1D, 5D, 1M, 6M, 1Y, ALL) |
| `news_service.py` | Company news via Finnhub (7-day window) |
| `company_service.py` | Company profiles and market cap formatting |
| `compare_service.py` | Financial metrics and earnings for side-by-side comparison |
| `watchlist_service.py` | SQLite CRUD for the watchlist |
| `portfolio_service.py` | Portfolio holdings with average price and P&L calculations |
| `alerts_service.py` | SQLite CRUD for price alerts + trigger/notify state management |
| `scheduler_service.py` | APScheduler background job checking alert conditions every 60s via Finnhub |
| `ai_service.py` | Calls Anthropic API with portfolio and alerts data, returns two-section JSON summary |
| `db.py` | SQLite connection management and schema creation |

### Routes (`app.py`)

| Route | Methods | Description |
|---|---|---|
| `/` | GET, POST | Dashboard: quote + history + profile + news |
| `/watchlist` | GET, POST | View/remove watchlist entries |
| `/add_to_watchlist` | POST | Add symbol to watchlist |
| `/portfolio` | GET, POST | Holdings with P&L |
| `/add_to_portfolio` | POST | Add shares with average price |
| `/compare` | GET, POST | Side-by-side stock comparison |
| `/alerts` | GET, POST | View/create/delete price alerts |
| `/alerts/pending` | GET | JSON: triggered+unnotified alerts (polled by alerts.js every 30s) |
| `/alerts/triggered` | POST | Marks an alert as notified so the banner doesn't reappear |
| `/ai_summary` | GET | AI-generated portfolio and alerts summary via Anthropic |

### Database Schema (SQLite)

```sql
watchlist(symbol TEXT, dateadded TEXT)
portfolio(symbol TEXT, dateadded TEXT, sharesowned REAL, avgprice REAL)
alerts(id TEXT PRIMARY KEY, symbol TEXT, target_price REAL, direction TEXT, triggered INTEGER, notified INTEGER, dateadded TEXT)
```

### Frontend

Templates live in `templates/` (Jinja2). Static assets (CSS, JS) in `static/`.

## External APIs

- **Finnhub** (`finnhub-python`) — quotes, news, company profiles
- **Twelve Data** (`twelvedata`) — price history with OHLCV data
- **Anthropic** (`anthropic`) — called from `ai_service.py`; model `claude-sonnet-4-5` with prompt caching on the system prompt
