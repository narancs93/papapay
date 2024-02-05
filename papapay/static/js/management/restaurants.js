function ready(fn) {
    if (document.readyState !== 'loading') {
        fn();
        return;
    }
    document.addEventListener('DOMContentLoaded', fn);
}

function displayDeleteModal() {
    document.getElementById('delete-restaurant-modal').classList.remove('hidden')
}

function hideDeleteModal() {
    document.getElementById('delete-restaurant-modal').classList.add('hidden');
}

function deleteConfirmCallback() {
    const deleteRestaurantAPI = JSON.parse(document.getElementById('deleteRestaurantAPI').textContent);
    const restaurantId = parseInt(document.getElementById('delete-confirm').getAttribute('restaurant-id'));

    sendRequestToAPI({
        'apiEndpoint': deleteRestaurantAPI,
        'method': 'POST',
        'contentType': 'application/json',
        'body': JSON.stringify({
            id: restaurantId
        })
    })
    .then(res => {
        if (res.status === 200) {
            location.reload();
        }
    });
}

function deleteClickCallback(event) {
    event.preventDefault();
    displayDeleteModal();

    const button = event.target;
    const row = button.closest('tr');
    const restaurantId = event.target.getAttribute('data-restaurant-id');
    const restaurantName = row.querySelector('p.restaurant-name').innerText;
    const restaurantAddress = row.querySelector('p.restaurant-address').innerText;
    
    document.getElementById('restaurant-to-delete').innerText = `${restaurantName} (${restaurantAddress})`;
    document.getElementById('delete-confirm').setAttribute('restaurant-id', restaurantId);
}

ready(() => {
    const closeModalButton = document.getElementById('close-modal');
    closeModalButton.addEventListener('click', () => {
        hideDeleteModal();
    });

    const deleteConfirmButton = document.getElementById('delete-confirm');
    deleteConfirmButton.addEventListener('click', deleteConfirmCallback);

    document.querySelectorAll('button.delete-restaurant').forEach((el, index) => {
        el.addEventListener('click', deleteClickCallback)
    });
});