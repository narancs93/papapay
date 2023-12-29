function sendRequestToAPI({apiEndpoint, method, contentType, csrfToken, body}) {
    return new Promise(function(resolve, reject) {
        fetch(apiEndpoint, {
            method: method,
            headers: {
                'Content-Type': contentType,
                'X-CSRFToken': csrfToken
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