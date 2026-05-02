window.onload = function() {
    Notification.requestPermission();

    const notifiedIds = new Set()

    setInterval(function() {
        fetch('/alerts/pending')
        .then(response => response.json())
        .then(alerts => {
            let newNotification = false
            for (const alert of alerts) {
                if (!notifiedIds.has(alert.id)) {
                    notifiedIds.add(alert.id)
                    const notification = new Notification("Price Alert", { body: alert.symbol + " went " + alert.direction + " $" + alert.target_price })
                    newNotification = true
                }
            }
            if (newNotification) {
                setTimeout(function() {
                window.location.reload();
                }, 5000);
            }
            
        });

    }, 30000);
}
