const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatMessages = document.getElementById('chat-messages');

chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;

  // Append user message
  appendMessage(message, 'user');
  userInput.value = '';

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    appendMessage(data.reply, 'bot', data.timestamp);
  } catch (error) {
    appendMessage('Unable to reach AgileBot server. Please check your CI/CD connection.', 'bot');
  }
});

function sendQuickMessage(text) {
  userInput.value = text;
  chatForm.dispatchEvent(new Event('submit'));
}

function appendMessage(text, sender, timeStr = null) {
  const msgDiv = document.createElement('div');
  msgDiv.className = `message ${sender}-message`;

  const avatar = sender === 'bot' ? '🤖' : '👤';
  const now = timeStr ? new Date(timeStr).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  msgDiv.innerHTML = `
    <div class="msg-avatar">${avatar}</div>
    <div class="msg-content">
      <p>${text}</p>
      <span class="timestamp">${now}</span>
    </div>
  `;

  chatMessages.appendChild(msgDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}
