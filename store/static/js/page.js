document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('bookingModal');
    const closeBtn = document.querySelector('.close');
    const bookButtons = document.querySelectorAll('.book-btn');
    const carModelInput = document.getElementById('carModel');
    const bookingForm = document.getElementById('bookingForm');
    
    // Открытие модального окна
    bookButtons.forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.card');
            const carName = card.querySelector('h3').textContent;
            carModelInput.value = carName;
            modal.style.display = 'block';
        });
    });
    
    // Закрытие модального окна
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    // Закрытие при клике вне окна
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Обработка формы
    bookingForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const carModel = carModelInput.value;
        const address = document.getElementById('address').value;
        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;
        
        // Здесь можно добавить отправку данных на сервер
        alert(`Автомобиль "${carModel}" успешно забронирован!\n\nАдрес: ${address}\nДата: ${date}\nВремя: ${time}`);
        
        // Сброс формы и закрытие модального окна
        bookingForm.reset();
        modal.style.display = 'none';
    });
    
    // Установка минимальной даты на сегодня
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').min = today;
});