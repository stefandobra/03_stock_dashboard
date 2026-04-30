from db import get_connection
from datetime import date

def add_to_portfolio(symbol, shares, price):
    """Connects to portfolio database, parses date to ISO format and inserts data into portfolio table"""
    con, cur = get_connection()

    shares = float(shares)
    price = float(price)
    date_time = date.today().strftime("%Y-%m-%d")
    
    cur.execute("SELECT symbol, dateadded, sharesowned, avgprice FROM portfolio WHERE symbol=?", (symbol, ))
    stock = cur.fetchone()

    if stock:
        existing_shares = stock['sharesowned']
        average_price = stock['avgprice']

        total_shares = existing_shares + shares
        new_avg = (existing_shares * average_price + shares * price) / (total_shares)

        data = (total_shares, new_avg, symbol)
        cur.execute("UPDATE portfolio SET sharesowned=?, avgprice=? WHERE symbol = ?", data)
        con.commit()
    else:
        data = (symbol, date_time, shares, price)
        cur.execute("INSERT INTO portfolio VALUES (?, ?, ?, ?)", data)
        con.commit()

def view_portfolio():
    """Connects to database, fetches all data in portfolio and returns it"""
    con, cur = get_connection()

    cur.execute("SELECT * FROM portfolio ORDER BY dateadded")
    portfolio = cur.fetchall()

    return portfolio

def remove_from_portfolio(symbol):
    """Connects to database and deletes one entry from table"""
    con, cur = get_connection()

    data = (symbol, )
    cur.execute("DELETE FROM portfolio WHERE symbol = (?)", data)
    con.commit()