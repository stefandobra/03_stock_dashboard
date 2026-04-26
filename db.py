import sqlite3

def create_tables():
    con = sqlite3.connect("stock_dashboard.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS watchlist(symbol TEXT, dateadded TEXT)")

def get_connection():
    con = sqlite3.connect("stock_dashboard.db")
    cur = con.cursor()

    return con, cur