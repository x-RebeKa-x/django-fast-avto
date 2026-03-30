function initPhoneMask() {
    const phoneInput = document.querySelector('input[name="phone_number"]');

    if (phoneInput) {
        phoneInput.placeholder = '+7 9xx xxx xx xx';
        phoneInput.classList.add('form-group');

        // Маска для телефона
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');

            if (value.length > 0) {
                if (value.startsWith('8')) {
                    value = '7' + value.substring(1);
                }

                let formatted = '+7';
                if (value.length > 1) {
                    formatted += ' ' + value.substring(1, 4);
                }
                if (value.length > 4) {
                    formatted += ' ' + value.substring(4, 7);
                }
                if (value.length > 7) {
                    formatted += '-' + value.substring(7, 9);
                }
                if (value.length > 9) {
                    formatted += '-' + value.substring(9, 11);
                }

                e.target.value = formatted;
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', initPhoneMask);