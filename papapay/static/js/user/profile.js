function addOption(element, value, text) {
    var newOption = document.createElement('option');
    newOption.value = value;
    newOption.textContent = text;
    newOption.setAttribute('selected', 'selected');

    element.appendChild(newOption);
}

const phoneNumberInputElement = document.getElementById('add-phone-number-form').querySelector('[name="phone_number"]');
const phoneNumberInput =  window.intlTelInput(phoneNumberInputElement, {
    utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@18.2.1/build/js/utils.js",
});

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

        sendRequestToAPI({
            apiEndpoint: apiEndpoint,
            method: 'POST',
            contentType: 'application/json',
            csrfToken: csrfToken,
            body: JSON.stringify({
                phone_number_id: phoneNumberId
            })
        })
        .then(res => {
            console.log(res);
            if (res.status === 200) {
                location.reload();
            }
        });
    })
});


document.getElementById('add-phone-number-button').addEventListener('click', (event) => {
    const form = document.getElementById('add-phone-number-form');
    document.getElementById('save-phone-number-button').textContent='Save';
    document.getElementById('add-phone-number-modal').classList.toggle('hidden');
    form.querySelector('[name="_update_type"]').value = 'add_phone_number';
    form.querySelector('[name="phone_number_id"]').value = '';
    
    setPhoneNumberFormValues(document.getElementById('add-phone-number-form'), {
        name: '',
        country: 'us',
        number: ''
    });
});


document.querySelectorAll('.phone-number-update').forEach((element) => {
    element.addEventListener('click', (event) => {
        const form = document.getElementById('add-phone-number-form');
        document.getElementById('save-phone-number-button').textContent='Update';
        document.getElementById('add-phone-number-modal').classList.toggle('hidden');
        form.querySelector('[name="_update_type"]').value = 'update_phone_number';

        const updateEl = event.target.closest('.phone-number-update');
        const phoneNumberId = updateEl.getAttribute('data-phone-number-id');
        const phoneNumberName = updateEl.getAttribute('data-phone-number-name');
        const phoneNumberAlpha2Code = updateEl.getAttribute('data-phone-number-alpha2-code');
        const phoneNumber = updateEl.getAttribute('data-phone-number');

        form.querySelector('[name="phone_number_id"]').value = phoneNumberId;

        setPhoneNumberFormValues(document.getElementById('add-phone-number-form'), {
            name: phoneNumberName,
            country: phoneNumberAlpha2Code.toLowerCase(),
            number: phoneNumber
        });
    })
})


document.querySelectorAll('.close-modal-button').forEach((element) => {
    element.addEventListener('click', (event) => {
        const modalId = event.target.getAttribute('data-target');
        document.getElementById(modalId).classList.toggle('hidden');
    })
});

function setPhoneNumberFormValues(form, {name, country, number}) {
    form.querySelector('[name="name"]').value = name;
    form.querySelector('[name="phone_number"]').value = number;
    phoneNumberInput.setCountry(country);
}

function validatePhoneNumber(input) {
    const error = input.getValidationError();

    let errorMessage;
    if (error === intlTelInputUtils.validationError.TOO_SHORT) {
        errorMessage = 'Invalid phone number: too short.';
    }
    else if (error === intlTelInputUtils.validationError.TOO_LONG) {
        errorMessage = 'Invalid phone number: too long.';
    }
    else if (error !== 0) {
        errorMessage = 'Invalid phone number.';
    }
    return errorMessage;
}


function displayPhoneNumberError(error) {
    const errorElement = document.getElementById('add-phone-number-error');
    errorElement.classList.remove('hidden');
    errorElement.classList.add('text-red-500', 'pb-2')
    errorElement.textContent = error;
}


document.getElementById('save-phone-number-button').addEventListener('click', () => {
    let errorMessage = validatePhoneNumber(phoneNumberInput);
    if (errorMessage) {
        displayPhoneNumberError(errorMessage);
        return;
    }

    const form = document.getElementById('add-phone-number-form');
    var formData = new FormData(form);
    const csrfToken = document.getElementById('add-phone-number-form').querySelector('[name="csrfmiddlewaretoken"]').value;

    const data = {};
    formData.forEach(function(value, key){
        data[key] = value;
    });
    data['alpha2_code'] = phoneNumberInput.getSelectedCountryData()['iso2']

    sendRequestToAPI({
        apiEndpoint: location,
        method: 'POST',
        contentType: 'application/json',
        csrfToken: csrfToken,
        body: JSON.stringify(data),
    })
    .then(() => {
        location.reload();
    })
    .catch(() => {
        displayPhoneNumberError('Something went wrong.');
    })
});
