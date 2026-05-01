import sqlite3

def create_tables():
    """Creates database file and watchlist table if doesn't exist"""
    con = sqlite3.connect("stock_dashboard.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS watchlist(symbol TEXT, dateadded TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS portfolio(symbol TEXT, dateadded TEXT, sharesowned REAL, avgprice REAL)")
    cur.execute("CREATE TABLE IF NOT EXISTS alerts(id TEXT PRIMARY KEY, symbol TEXT, target_price REAL, direction TEXT, triggered INTEGER, dateadded TEXT)")
    
def get_connection():
    """Returns connection and cursor for the database"""
    con = sqlite3.connect("stock_dashboard.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    return con, cur