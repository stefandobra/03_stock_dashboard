window.onload = function() {
    Notification.requestPermission();

    const notifiedIds = new Set()

    setInterval(function() {
        fetch('/alerts/pending')
        .then(response => response.json())
        .then(alerts => {
            for (const alert of alerts) {
                if (!notifiedIds.has(alert.id)) {
                    notifiedIds.add(alert.id)
                    const notification = new Notification("Price Alert", { body: alert.symbol + " went " + alert.direction + " $" + alert.target_price })
                    window.location.reload()
                }
            }
        });

    }, 30000);
}
