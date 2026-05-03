function showBanner(alertData) {
    const banner = document.createElement('div')
    banner.className = 'alert-banner'
    banner.style.position = 'fixed'
    banner.style.top = (20 + document.querySelectorAll('.alert-banner').length * 80) + 'px'
    banner.style.left = '50%'
    banner.style.transform = 'translateX(-50%)'
    banner.style.backgroundColor = 'green'
    banner.style.padding = '15px'
    banner.style.zIndex = '10'
    banner.innerHTML = alertData.symbol + " went " + alertData.direction + " $" + alertData.target_price
    const button = document.createElement('button')
    button.style.display = 'block'                                                          
    button.style.marginTop = '8px'
    button.innerHTML = "Dismiss"
    button.onclick = function() {
        banner.remove()
    }
    banner.appendChild(button)
    document.body.appendChild(banner)
    
    fetch('/alerts/triggered', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ alert_id: alertData.id })
    })
}



window.onload = function() {

    const notifiedIds = new Set()

    setInterval(function() {
        fetch('/alerts/pending')
        .then(response => response.json())
        .then(alerts => {
            for (const alert of alerts) {
                if (!notifiedIds.has(alert.id)) {
                    notifiedIds.add(alert.id)
                    showBanner(alert)
                }
            }
        });

    }, 30000);
}
