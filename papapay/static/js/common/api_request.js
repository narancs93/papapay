function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function sendRequestToAPI({ apiEndpoint, method, contentType, body }) {
    return new Promise(function (resolve, reject) {
        fetch(apiEndpoint, {
            method: method,
            headers: {
                'Content-Type': contentType,
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: body
        }).then(res => {
            if (res.ok) {
                resolve(res);
            }
            else {
                reject(res);
            }
        }).catch((res) => {
            reject(res);
        })
    });
}