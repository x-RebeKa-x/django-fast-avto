function updateEndTimeMin() {
    const startTime = document.getElementById('time').value;
    const endTimeInput = document.getElementById('time_end');

    if (startTime) {
        endTimeInput.min = startTime;

        if (endTimeInput.value && endTimeInput.value < startTime) {
            endTimeInput.value = '';
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    updateEndTimeMin();
});

document.getElementById('time_end').addEventListener('change', function() {
    const startTime = document.getElementById('time').value;
    const endTime = this.value;

    if (startTime && endTime && endTime < startTime) {
        this.value = '';
    }
});