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