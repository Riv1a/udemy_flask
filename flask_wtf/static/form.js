const response = fetch(url, {
    method: 'POST',
    headers: {
        'X-CSRFToken' : document.getElementById('csrf_token').value,
        'Content-Type' : 'application/x-www-form-urlencoded'
    },
})