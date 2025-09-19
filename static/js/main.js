// static/js/main.js
let chatSocket = null;
let currentCarId = null;

function openChat(carId) {
  currentCarId = carId;
  const modal = new bootstrap.Modal(document.getElementById('chatModal'));
  modal.show();

  // Подключаемся к WebSocket
  if (chatSocket) {
    chatSocket.close();
  }

  chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + carId + '/'
  );

  chatSocket.onopen = function (e) {
    console.log('WebSocket подключен к чату по авто ID: ' + carId);
    document.getElementById('chat-messages').innerHTML = '<div class="alert alert-info">Чат открыт. Можете отправить сообщение.</div>';
  };

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const messageDiv = document.createElement('div');
    messageDiv.className = 'mb-2 p-2 border rounded';
    messageDiv.innerHTML = `
            <strong>${data.username}:</strong> ${data.message}
            <div class="text-muted small">${new Date(data.timestamp).toLocaleString()}</div>
        `;
    document.getElementById('chat-messages').appendChild(messageDiv);
    // Прокручиваем вниз
    document.getElementById('chat-messages').scrollTop = document.getElementById('chat-messages').scrollHeight;
  };

  chatSocket.onclose = function (e) {
    console.log('WebSocket отключен');
    document.getElementById('chat-messages').innerHTML = '<div class="alert alert-warning">Соединение закрыто.</div>';
  };

  // Отправка сообщения
  document.getElementById('send-chat-btn').onclick = function () {
    const input = document.getElementById('chat-input');
    if (input.value && chatSocket.readyState === WebSocket.OPEN) {
      chatSocket.send(JSON.stringify({
        'message': input.value
      }));
      input.value = '';
    }
  };
}