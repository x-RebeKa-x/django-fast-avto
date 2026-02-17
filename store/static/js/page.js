let currentCarId = null;

function openBookingModal(carId, carName) {
    currentCarId = carId;

    document.getElementById('modalCarId').value = carId;
    document.getElementById('carModel').value = carName;

    const form = document.getElementById('bookingForm');
    form.action = `/cars/basket-add/${carId}/`;

    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').min = today;
    document.getElementById('date').value = today;

    document.getElementById('address').value = '';
    document.getElementById('time').value = '';

    document.getElementById('bookingModal').style.display = 'block';
}

document.getElementById('bookingForm').addEventListener('submit', function(e) {
    const address = document.getElementById('address').value.trim();
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;

    let errors = [];

    if (address.length < 5) {
        errors.push('Адрес должен содержать минимум 5 символов');
    }

    if (date) {
        const selectedDate = new Date(date);
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        if (selectedDate < today) {
            errors.push('Дата не может быть в прошлом');
        }
    }

    if (time) {
        const [hours, minutes] = time.split(':');
        if (hours < 9 || hours > 21) {
            errors.push('Время должно быть с 9:00 до 21:00');
        }
    }

    if (errors.length > 0) {
        e.preventDefault();
        alert('Ошибки:\n- ' + errors.join('\n- '));
        return false;
    }
});

document.getElementById('address').addEventListener('input', function() {
    if (this.value.length < 5) {
        this.style.borderColor = '#ff6b6b';
    } else {
        this.style.borderColor = '#28a745';
    }
});

document.querySelector('.close').onclick = function() {
    document.getElementById('bookingModal').style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('bookingModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

document.getElementById('date').addEventListener('change', function() {
    const selectedDate = new Date(this.value);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    if (selectedDate < today) {
        alert('Нельзя выбрать прошедшую дату');
        this.value = '';
    }
});

document.getElementById('time').addEventListener('change', function() {
    const [hours] = this.value.split(':');
    if (hours < 9 || hours > 21) {
        alert('Время должно быть с 9:00 до 21:00');
        this.value = '';
    }
});