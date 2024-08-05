document.addEventListener('DOMContentLoaded', function() {
    const content = document.getElementById('content');
    const submitButton = document.getElementById('submitButton');
    const chatLog = document.getElementById('chatLog');
    const button1 = document.getElementById('button1');
    const button2 = document.getElementById('button2');
    const button3 = document.getElementById('button3');
    const button4 = document.getElementById('button4');

    submitButton.addEventListener('click', handleSubmit);
    content.addEventListener('keydown', handleKeyDown);
    content.addEventListener('input', handleInput);
    button1.addEventListener('click', () => handleSidebarButtonClick('Button 1 clicked'));
    button2.addEventListener('click', () => handleSidebarButtonClick('Button 2 clicked'));
    button3.addEventListener('click', () => handleSidebarButtonClick('Button 3 clicked'));
    button4.addEventListener('click', () => handleSidebarButtonClick('Button 4 clicked'));

    async function handleSubmit() {
        const message = content.value.trim();
        if (message) {
            addMessageToChatLog(`${message}`, 'user');
            clearInput();
            scrollChatToBottom();
            console.log(`Task Executing: ${message}`);

            try {
                const response = await fetch('http://127.0.0.1:8000/process/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({ 'user_input': message }),
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                addMessageToChatLog(`Agent: ${data.result}`, 'agent');
                scrollChatToBottom();
            } catch (error) {
                console.error('Error:', error);
                alert('There was a problem with your request.');
            }
        }
    }

    function handleKeyDown(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            handleSubmit();
        }
    }

    function handleInput() {
        if (content.value.trim()) {
            submitButton.classList.add('active');
        } else {
            submitButton.classList.remove('active');
        }
    }

    function addMessageToChatLog(message, type) {
        const messageWrapper = document.createElement('div');
        messageWrapper.classList.add('message');

        // Apply different class based on the type of message
        if (type === 'user') {
            messageWrapper.classList.add('user-message');
        } else if (type === 'agent') {
            messageWrapper.classList.add('agent-message');
        }

        const messageElement = document.createElement('p');
        messageElement.textContent = message;

        messageWrapper.appendChild(messageElement);
        chatLog.appendChild(messageWrapper);
    }

    function clearInput() {
        content.value = '';
        submitButton.classList.remove('active');
    }

    function scrollChatToBottom() {
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    function handleSidebarButtonClick(message) {
        addMessageToChatLog(message, 'user');
        scrollChatToBottom();
    }

    content.focus();
});
