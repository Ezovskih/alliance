const messageBox = document.getElementById('message-box');

// Устанавливаем соединение
const socket = new WebSocket('ws://' + window.location.host + '/ws/messages/');

// Отправляем запрос при подключении
socket.onopen = function(e) {
    socket.send(JSON.stringify({'action': 'get_message'}));
};

// Обрабатываем полученное сообщение
socket.onmessage = function(event) {
    const message = JSON.parse(event.data);
    console.log("MESSAGE:", message);
    // Формируем HTML сообщения
    messageBox.innerHTML = `<i>${message.text}</i>`;
    if (message.link) messageBox.innerHTML += `&nbsp;<a href="${message.link}">Перейти</a>`;
};

// Обрабатываем полученные ошибки
socket.onerror = function(error) {
    console.error("Ошибка обработки сообщения:", error);
};