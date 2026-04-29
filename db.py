import sqlite3

def create_tables():
    """Creates database file and watchlist table if doesn't exist"""
    con = sqlite3.connect("stock_dashboard.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS watchlist(symbol TEXT, dateadded TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS portfolio(symbol TEXT, dateadded TEXT, sharesowned REAL, avgprice REAL)")

def get_connection():
    """Returns connection and cursor for the database"""
    con = sqlite3.connect("stock_dashboard.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    return con, cur