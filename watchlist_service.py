from db import get_connection
from datetime import date

def add_symbol(symbol):
    """Connects to database, parses date to ISO format and inserts symbol and date into watchlist table"""
    con, cur = get_connection()

    date_time = date.today().strftime("%Y-%m-%d")
    data = (symbol, date_time)

    cur.execute("INSERT INTO watchlist VALUES (?, ?)", data) 
    con.commit()

def view_watchlist():
    """Connects to database, fetches all data in watchlist and returns it"""
    con, cur = get_connection()

    cur.execute("SELECT * FROM watchlist ORDER BY dateadded")
    watchlist = cur.fetchall()
    
    return watchlist

def remove_symbol(symbol):
    """Connects to database and deletes one entry from table"""
    con, cur = get_connection()

    data = (symbol, )
    cur.execute("DELETE FROM watchlist WHERE symbol = (?)", data)
    con.commit()