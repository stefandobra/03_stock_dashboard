from db import get_connection
from datetime import date

def add_to_portfolio(symbol, shares, price):
    """Connects to portfolio database, parses date to ISO format and inserts data into portfolio table"""
    con, cur = get_connection()

    date_time = date.today().strftime("%Y-%m-%d")

    data = (symbol, date_time, shares, price)

    cur.execute("INSERT INTO portfolio VALUES (?, ?, ?, ?)", data)
    con.commit()

def view_portfolio():
    """Connects to database, fetches all data in portfolio and returns it"""
    con, cur = get_connection()

    cur.execute("SELECT * FROM portfolio ORDER BY dateadded")
    portfolio = cur.fetchall()

    return portfolio