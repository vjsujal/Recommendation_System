const chatbot = document.getElementById('chatbot');
const chatContent = document.getElementById('chat-content');
const messageInput = document.getElementById('message');
let isChatbotMinimized = false;
const openChatButton = document.getElementById('open-chat-button');
const imageUploadInput = document.getElementById('image-upload');
let uploadedImage = null;

function sendMessage() {
    const messageText = document.getElementById('message').value;
    const imageFile = imageUploadInput.files[0];

    if (messageText.trim() === '' && !imageFile) {
        return;
    }

    // Create a container for the user message
    const userMessageContainer = document.createElement('div');
    userMessageContainer.classList.add('user-message');

    // Add text message to the container
    if (messageText.trim() !== '') {
        const textMessage = document.createElement('div');
        textMessage.textContent = messageText;
        userMessageContainer.appendChild(textMessage);
    }

    // Add image to the container
    if (imageFile) {
        const uploadedImage = document.createElement('img');
        uploadedImage.src = URL.createObjectURL(imageFile);
        userMessageContainer.appendChild(uploadedImage);
    }

    chatContent.appendChild(userMessageContainer);

    document.getElementById('message').value = '';
    imageUploadInput.value = ''; // Clear the file input
    imageUploadInput.type = 'text'; // Reset the input type to 'text' to clear the file selection
    imageUploadInput.type = 'file'; // Restore the input type to 'file' for future image uploads
    document.getElementById('message').focus();
}


function openChat() {
    chatbot.style.display = 'block';
    openChatButton.style.display = 'none'; // Hide the "Open Chat" button
}

function closeChat() {
    chatbot.style.display = 'none';
    openChatButton.style.display = 'block'; // Show the "Open Chat" button
}

function toggleChatSize() {
    const chatContainer = document.getElementById('chat-container');

    if (isChatbotMinimized) {
        // Maximize the chatbot
        chatContainer.style.height = '400px';
        isChatbotMinimized = false;
        document.getElementById('minimize-chat').textContent = '-';
    } else {
        // Minimize the chatbot
        chatContainer.style.height = '50px';
        isChatbotMinimized = true;
        document.getElementById('minimize-chat').textContent = '+';
    }
}

messageInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
});


