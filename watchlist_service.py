from db import get_connection
from datetime import date

def add_symbol(symbol):
    con, cur = get_connection()

    date_time = date.today().strftime("%Y-%m-%d")
    data = (symbol, date_time)

    cur.execute("INSERT INTO watchlist VALUES (?, ?)", data) 
    con.commit()

def view_watchlist():
    con, cur = get_connection()

    cur.execute("SELECT * FROM watchlist ORDER BY dateadded")
    watchlist = cur.fetchall()
    
    return watchlist
