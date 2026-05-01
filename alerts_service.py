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

def delete_alert(alert_id):
    """Deletes alert based in unique id to handle multiple alerts for same stock"""
    con, cur = get_connection()
    
    data = (alert_id, )
    cur.execute("DELETE FROM alerts WHERE id = (?)", data)
    con.commit()
    
def trigger_alert(alert_id):
    """Marks alert as triggered so the scheduler skips it on future checks and it doesn't fire repeatedly"""
    con, cur = get_connection()
    
    data = (1, alert_id)
    cur.execute("UPDATE alerts SET triggered = (?) WHERE id = (?)", data)
    con.commit()
    
def get_untriggered_alerts():
    """Returns only untriggered alerts so the scheduler avoids wasting API calls on alerts that have already fired"""
    con, cur = get_connection()
    
    data = (0, )
    cur.execute("SELECT * FROM alerts WHERE triggered = (?)", data)
    untriggered = cur.fetchall()
    
    return untriggered