from alerts_service import get_untriggered_alerts, trigger_alert
from stock_service import get_quote

def check_alerts():
    """Checks untriggered alerts against current prices and marks them as triggered if the condition is met.
    Skips already-triggered alerts so the JS polling endpoint only notifies the user once per alert.
    """
    untriggered_alerts = get_untriggered_alerts()
    
    for alert in untriggered_alerts:
        quote = get_quote(alert['symbol'])
        if quote:
            current_price = quote['c']
            if alert['direction'] == 'above' and current_price >= alert['target_price']:
                trigger_alert(alert['id'])
            elif alert['direction'] == 'below' and current_price <= alert['target_price']:
                trigger_alert(alert['id'])
            
                
                
