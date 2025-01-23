const publicAlert = document.getElementById('public-alert');

// Устанавливаем соединение
const socket = new WebSocket('ws://localhost:8000/ws/public_alerts/');

// Обрабатываем полученное сообщение
socket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    // Формируем HTML сообщения
    let alertHTML = `<div>${data.message}</div>`;
    if (data.url) {
        alertHTML += `<a href="${data.url}">Перейти</a>`;
    publicAlert.innerHTML = alertHTML;
    publicAlert.style.display = 'block';  // размешаем поверх страницы

    // Скрываем сообщение через 5 секунд
    setTimeout(() => { publicAlert.style.display = 'none'; }, 5000);
};

// Обрабатываем полученные ошибки
socket.onerror = function(error) {
    console.error('Ошибка обработки сообщения:', error);
};

// Закрываем соединение
socket.onclose = function(event) {
    console.log('Соединение успешно закрыто:', event);
};