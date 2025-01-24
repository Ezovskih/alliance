const messageBox = document.getElementById('message-box');

// Устанавливаем соединение
const socket = new WebSocket('ws://127.0.0.1:8000/ws/notifications/');

// Обрабатываем полученное сообщение
socket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    // Формируем HTML сообщения
    let messageHTML = `<p>${data.message}</p>`;
    if (data.url) messageHTML += `<a href="${data.url}">Перейти</a>`;

    messageBox.innerHTML = messageHTML;
    messageBox.style.display = 'block';  // размещаем поверх страницы

    // Скрываем сообщение через 5 секунд
    setTimeout(() => { messageBox.style.display = 'none'; }, 5000);
};

// Обрабатываем полученные ошибки
socket.onerror = function(error) {
    console.error('Ошибка обработки сообщения:', error);
};

// Закрываем соединение
socket.onclose = function(event) {
    console.log('Соединение успешно закрыто:', event);
};