// static/js/chatbot_js.js

document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const chatOptions = document.getElementById('chat-options');
    const scenarioSelect = document.getElementById('scenario-select');
    const startChatBtn = document.getElementById('start-chat-btn');
    const scenarioSelectionSection = document.getElementById('scenario-selection-section');
    const chatbotInterface = document.getElementById('chatbot-interface');
    const chatInput = document.getElementById('chat-input');
    const messageInput = document.getElementById('message-input');
    const sendMessageBtn = document.getElementById('send-message-btn');
    const endSessionBtn = document.getElementById('end-session-btn');
    const chatHeader = document.getElementById('chat-header-title');

    let currentScenarioId = null;

    // Function to add a message to the chat display
    function addMessage(sender, text, options = [], actions = []) {
        const messageBubble = document.createElement('div');
        messageBubble.classList.add('message-bubble');
        if (sender === 'user') {
            messageBubble.classList.add('user');
        }
        messageBubble.innerHTML = formatMessageText(text); // Use innerHTML for markdown-like formatting
        chatMessages.appendChild(messageBubble);

        // Clear and display options
        chatOptions.innerHTML = '';
        if (options.length > 0) {
            options.forEach(option => {
                const button = document.createElement('button');
                button.classList.add('option-button');
                button.textContent = option.charAt(0).toUpperCase() + option.slice(1); // Capitalize first letter
                button.addEventListener('click', () => sendResponse(option));
                chatOptions.appendChild(button);
            });
            chatOptions.style.display = 'flex'; // Show options
            chatInput.style.display = 'none'; // Hide text input
        } else if (actions.length > 0) {
            // Display actions if terminal state
            displayActions(actions);
            chatOptions.style.display = 'none'; // Hide options
            chatInput.style.display = 'none'; // Hide text input
            endSessionBtn.style.display = 'block'; // Show end session button
        } else {
            // No options, no actions, just text input or end of conversation
            chatOptions.style.display = 'none';
            chatInput.style.display = 'flex'; // Show text input by default if no options
            messageInput.focus();
        }

        chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to bottom
    }

    // Basic markdown-like formatting
    function formatMessageText(text) {
        // Bold
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Italics
        text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
        // Links (simple URL to clickable link)
        text = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
        return text;
    }

    // Function to display actions for terminal states
    function displayActions(actions) {
        const actionsContainer = document.createElement('div');
        actionsContainer.classList.add('chatbot-actions');

        actions.sort((a, b) => a.priority - b.priority); // Sort by priority

        actions.forEach(action => {
            const actionGroup = document.createElement('div');
            actionGroup.classList.add('action-group');

            const title = document.createElement('h3');
            title.textContent = `${action.priority}. ${action.title}`;
            actionGroup.appendChild(title);

            const why = document.createElement('p');
            why.textContent = `Why: ${action.why}`;
            actionGroup.appendChild(why);

            const stepsList = document.createElement('ul');
            action.steps.forEach(step => {
                const li = document.createElement('li');
                li.textContent = step;
                stepsList.appendChild(li);
            });
            actionGroup.appendChild(stepsList);
            actionsContainer.appendChild(actionGroup);
        });
        chatMessages.appendChild(actionsContainer);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }


    // Fetch available scenarios from the backend
    async function fetchScenarios() {
        try {
            const response = await fetch('/api/chatbot/scenarios');
            const scenarios = await response.json();
            
            scenarioSelect.innerHTML = '<option value="">Select a scenario</option>';
            scenarios.forEach(scenario => {
                const option = document.createElement('option');
                option.value = scenario.id;
                option.textContent = scenario.name;
                scenarioSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching scenarios:', error);
            addMessage('bot', 'Oops! Could not load scenarios. Please try again later.');
        }
    }

    // Start a new chat session
    startChatBtn.addEventListener('click', async function() {
        currentScenarioId = scenarioSelect.value;
        if (!currentScenarioId) {
            alert('Please select a scenario to start.');
            return;
        }

        try {
            const response = await fetch('/api/chatbot/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ scenario_id: currentScenarioId })
            });
            const data = await response.json();

            if (response.ok) {
                scenarioSelectionSection.style.display = 'none';
                chatbotInterface.style.display = 'flex';
                chatMessages.innerHTML = ''; // Clear previous messages
                chatHeader.textContent = data.scenario_name || 'Chatbot';
                addMessage('bot', data.message, data.options, data.terminal ? data.actions : []);
            } else {
                addMessage('bot', `Error starting chat: ${data.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error starting chat:', error);
            addMessage('bot', 'Could not start chat. Please check your connection.');
        }
    });

    // Send user response to the backend
    async function sendResponse(input) {
        addMessage('user', input); // Display user's input immediately

        try {
            const response = await fetch('/api/chatbot/respond', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ input: input })
            });
            const data = await response.json();

            if (response.ok) {
                if (data.terminal) {
                    addMessage('bot', data.message, [], data.actions);
                } else {
                    addMessage('bot', data.message, data.options);
                }
            } else {
                addMessage('bot', `Error: ${data.error || 'Unknown error'}`);
                // If there's an error, try to restore options if possible
                fetchCurrentChatState(); 
            }
        } catch (error) {
            console.error('Error sending response:', error);
            addMessage('bot', 'Could not send response. Please check your connection.');
            fetchCurrentChatState(); // Attempt to restore state
        }
    }

    // Handle text input submission
    sendMessageBtn.addEventListener('click', function() {
        const input = messageInput.value.trim();
        if (input) {
            sendResponse(input);
            messageInput.value = '';
        }
    });

    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessageBtn.click();
        }
    });

    // End session button
    endSessionBtn.addEventListener('click', async function() {
        if (confirm("Are you sure you want to end this chat session?")) {
            try {
                await fetch('/api/chatbot/end_session', { method: 'POST' });
                alert('Chat session ended.');
                location.reload(); // Reload the page to reset the interface
            } catch (error) {
                console.error('Error ending session:', error);
                alert('Could not end session. Please try again.');
            }
        }
    });

    // Fetch current chat state when page loads (e.g., after refresh)
    async function fetchCurrentChatState() {
        try {
            const response = await fetch('/api/chatbot/current_state');
            const data = await response.json();

            if (response.ok && data.scenario_name) {
                currentScenarioId = session.get('active_scenario_id'); // Re-set from session or API response
                scenarioSelectionSection.style.display = 'none';
                chatbotInterface.style.display = 'flex';
                chatHeader.textContent = data.scenario_name || 'Chatbot';
                addMessage('bot', data.message, data.options, data.terminal ? data.actions : []);
            } else {
                // No active session or error, show scenario selection
                scenarioSelectionSection.style.display = 'block';
                chatbotInterface.style.display = 'none';
                fetchScenarios();
            }
        } catch (error) {
            console.error('Error fetching current chat state:', error);
            scenarioSelectionSection.style.display = 'block';
            chatbotInterface.style.display = 'none';
            fetchScenarios();
        }
    }

    // Initial load
    fetchCurrentChatState();
});