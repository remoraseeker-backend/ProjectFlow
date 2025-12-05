function assignValueToHiddenField() {
    const date = new Date();
    const offsetMinutes = date.getTimezoneOffset();
    const offsetHours = -(offsetMinutes / 60);
    const hiddenField = document.getElementById('id_client_timezone_offset');

    if (hiddenField) {
        hiddenField.value = offsetHours;
    }
}

document.addEventListener('DOMContentLoaded', assignValueToHiddenField);
