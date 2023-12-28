function addOption(element, value, text) {
    var newOption = document.createElement('option');
    newOption.value = value;
    newOption.textContent = text;
    newOption.setAttribute('selected', 'selected');

    element.appendChild(newOption);
}

const form = document.getElementById('profile-update-form');

form.addEventListener('submit', () => {
    const phoneNumbersSelect = document.getElementById('phone-numbers');

    document.querySelectorAll('.phone-number').forEach((element) => {
        const phoneNumberId = element.getAttribute('data-phone-number-id');
        const phoneNumber = element.innerHTML;

        addOption(phoneNumbersSelect, phoneNumberId, phoneNumber);
    });
});

document.querySelectorAll('.phone-number-delete').forEach((element) => {
    element.addEventListener('click', (event) => {
        const apiEndpoint = JSON.parse(document.getElementById('remove-phone-number-url').textContent);
        const phoneNumberId = event.target.closest('.phone-number-delete').getAttribute('data-phone-number-id');
        const csrfToken = document.getElementById('profile-update-form').querySelector('[name="csrfmiddlewaretoken"]').value;
        
        fetch(apiEndpoint, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }, 
            body: JSON.stringify({
                'phone_number_id': phoneNumberId
            })
        }).then(res => {
            if (res.status === 200) {
                location.reload();
            }
        });
    })
})