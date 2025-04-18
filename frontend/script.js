const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', async () => {
    const message = userInput.value.trim();
    if (!message) return;
    addMessageToChat('You', message);
    userInput.value = '';

    try {
        const response = await fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message }),
        });
        const data = await response.json();
        addMessageToChat('ZOOR AI', data.response || "Sorry, I couldn't understand that.");
    } catch (error) {
        addMessageToChat('ZOOR AI', "Sorry, there was an error connecting to the server.");
    }
});

function addMessageToChat(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.textContent = `${sender}: ${message}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}