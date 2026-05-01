from db import get_connection
from datetime import datetime
import uuid

def create_alert(symbol, target_price, direction):
    """Creates a new alert. target_price cast to float because HTML form inputs return strings.
    Dateadded stored as ISO format string for consistent sorting.
    Triggered defaults to 0 as alert has not fired yet."""
    con, cur = get_connection()
    
    date_time = datetime.now().isoformat()
    alert_id = uuid.uuid4().hex
    target_price = float(target_price)
    triggered = 0
    
    data = (alert_id, symbol, target_price, direction, triggered, date_time)
    
    cur.execute("INSERT INTO alerts VALUES (?, ?, ?, ?, ?, ?)", data)
    con.commit()
    
def get_alerts():
    """Returns all alerts from the database. Used by the alerts page to 
    display current alerts and by the scheduler to check prices against targets."""  
    con, cur = get_connection()
    
    cur.execute("SELECT * FROM alerts ORDER BY dateadded")
    alerts = cur.fetchall()
    
    return alerts