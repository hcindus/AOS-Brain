/**
 * AGI Company AI Assistant Chat Widget
 * Floating chat widget for AGI Company website
 */

(function() {
    'use strict';
    
    // Widget configuration
    const CONFIG = {
        position: 'bottom-right',
        primaryColor: '#ed8936',
        botName: 'AGI Assistant',
        botAvatar: '🤖',
        welcomeMessage: 'Hi! I\'m the AGI Assistant. How can I help you today?',
        placeholder: 'Type a message...',
        apiEndpoint: '/api/chat', // Replace with actual endpoint
        maxMessages: 50
    };
    
    // Widget state
    let isOpen = false;
    let messages = [];
    let isTyping = false;
    
    // Create widget HTML
    function createWidget() {
        const widget = document.createElement('div');
        widget.id = 'agi-chat-widget';
        widget.innerHTML = `
            <!-- Chat Button -->
            <div class="agi-chat-button" id="agi-chat-button">
                <span class="agi-chat-icon">${CONFIG.botAvatar}</span>
                <span class="agi-chat-label">AI Assistant</span>
            </div>
            
            <!-- Chat Window -->
            <div class="agi-chat-window" id="agi-chat-window">
                <!-- Header -->
                <div class="agi-chat-header">
                    <div class="agi-chat-header-info">
                        <span class="agi-chat-avatar">${CONFIG.botAvatar}</span>
                        <div class="agi-chat-header-text">
                            <div class="agi-chat-name">${CONFIG.botName}</div>
                            <div class="agi-chat-status">
                                <span class="agi-status-dot"></span>
                                <span>Online</span>
                            </div>
                        </div>
                    </div>
                    <button class="agi-chat-close" id="agi-chat-close" aria-label="Close chat">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M18 6L6 18M6 6l12 12"/>
                        </svg>
                    </button>
                </div>
                
                <!-- Messages -->
                <div class="agi-chat-messages" id="agi-chat-messages">
                    <div class="agi-message agi-message-bot">
                        <div class="agi-message-avatar">${CONFIG.botAvatar}</div>
                        <div class="agi-message-content">
                            <div class="agi-message-text">${CONFIG.welcomeMessage}</div>
                            <div class="agi-message-time">${getCurrentTime()}</div>
                        </div>
                    </div>
                </div>
                
                <!-- Typing Indicator -->
                <div class="agi-chat-typing" id="agi-chat-typing">
                    <div class="agi-typing-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
                
                <!-- Input -->
                <div class="agi-chat-input-container">
                    <form class="agi-chat-form" id="agi-chat-form">
                        <input 
                            type="text" 
                            class="agi-chat-input" 
                            id="agi-chat-input" 
                            placeholder="${CONFIG.placeholder}"
                            autocomplete="off"
                        />
                        <button type="submit" class="agi-chat-send" id="agi-chat-send" aria-label="Send message">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
                            </svg>
                        </button>
                    </form>
                </div>
            </div>
        `;
        
        // Add styles
        addStyles();
        
        // Append to body
        document.body.appendChild(widget);
        
        // Bind events
        bindEvents();
    }
    
    // Add CSS styles
    function addStyles() {
        const styles = document.createElement('style');
        styles.textContent = `
            /* AGI Chat Widget Styles */
            #agi-chat-widget {
                --agi-primary: ${CONFIG.primaryColor};
                --agi-primary-dark: #dd6b20;
                --agi-bg-dark: #0a0a1a;
                --agi-bg-card: rgba(255, 255, 255, 0.05);
                --agi-text: #e5e5e5;
                --agi-text-muted: #a0a0a0;
                --agi-border: rgba(237, 137, 54, 0.3);
                --agi-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
                --agi-radius: 16px;
                --agi-radius-sm: 8px;
                
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 9999;
            }
            
            /* Chat Button */
            .agi-chat-button {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: linear-gradient(135deg, var(--agi-primary) 0%, var(--agi-primary-dark) 100%);
                border-radius: 50px;
                padding: 12px 20px;
                display: flex;
                align-items: center;
                gap: 10px;
                cursor: pointer;
                box-shadow: var(--agi-shadow);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                z-index: 10000;
            }
            
            .agi-chat-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 40px rgba(237, 137, 54, 0.4);
            }
            
            .agi-chat-button.hidden {
                display: none;
            }
            
            .agi-chat-icon {
                font-size: 24px;
            }
            
            .agi-chat-label {
                color: white;
                font-weight: 600;
                font-size: 14px;
            }
            
            /* Chat Window */
            .agi-chat-window {
                position: fixed;
                bottom: 100px;
                right: 20px;
                width: 360px;
                height: 500px;
                background: var(--agi-bg-dark);
                border: 1px solid var(--agi-border);
                border-radius: var(--agi-radius);
                box-shadow: var(--agi-shadow);
                display: flex;
                flex-direction: column;
                opacity: 0;
                visibility: hidden;
                transform: translateY(20px) scale(0.95);
                transition: opacity 0.3s ease, visibility 0.3s ease, transform 0.3s ease;
                z-index: 10001;
            }
            
            .agi-chat-window.open {
                opacity: 1;
                visibility: visible;
                transform: translateY(0) scale(1);
            }
            
            /* Header */
            .agi-chat-header {
                background: rgba(26, 54, 93, 0.95);
                padding: 16px;
                border-radius: var(--agi-radius) var(--agi-radius) 0 0;
                border-bottom: 1px solid var(--agi-border);
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            
            .agi-chat-header-info {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .agi-chat-avatar {
                font-size: 32px;
            }
            
            .agi-chat-header-text {
                display: flex;
                flex-direction: column;
            }
            
            .agi-chat-name {
                color: white;
                font-weight: 700;
                font-size: 16px;
            }
            
            .agi-chat-status {
                display: flex;
                align-items: center;
                gap: 6px;
                color: var(--agi-text-muted);
                font-size: 12px;
                margin-top: 2px;
            }
            
            .agi-status-dot {
                width: 8px;
                height: 8px;
                background: #48bb78;
                border-radius: 50%;
                animation: agi-pulse 2s infinite;
            }
            
            @keyframes agi-pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            .agi-chat-close {
                background: none;
                border: none;
                color: var(--agi-text);
                cursor: pointer;
                padding: 8px;
                border-radius: var(--agi-radius-sm);
                transition: background 0.2s;
            }
            
            .agi-chat-close:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            
            /* Messages */
            .agi-chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 16px;
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            
            .agi-chat-messages::-webkit-scrollbar {
                width: 6px;
            }
            
            .agi-chat-messages::-webkit-scrollbar-track {
                background: transparent;
            }
            
            .agi-chat-messages::-webkit-scrollbar-thumb {
                background: rgba(237, 137, 54, 0.3);
                border-radius: 3px;
            }
            
            .agi-message {
                display: flex;
                gap: 10px;
                max-width: 85%;
            }
            
            .agi-message-bot {
                align-self: flex-start;
            }
            
            .agi-message-user {
                align-self: flex-end;
                flex-direction: row-reverse;
            }
            
            .agi-message-avatar {
                font-size: 24px;
                flex-shrink: 0;
            }
            
            .agi-message-content {
                display: flex;
                flex-direction: column;
                gap: 4px;
            }
            
            .agi-message-text {
                padding: 12px 16px;
                border-radius: var(--agi-radius);
                font-size: 14px;
                line-height: 1.5;
            }
            
            .agi-message-bot .agi-message-text {
                background: var(--agi-bg-card);
                border: 1px solid var(--agi-border);
                color: var(--agi-text);
                border-top-left-radius: 4px;
            }
            
            .agi-message-user .agi-message-text {
                background: var(--agi-primary);
                color: white;
                border-top-right-radius: 4px;
            }
            
            .agi-message-time {
                font-size: 11px;
                color: var(--agi-text-muted);
            }
            
            /* Typing Indicator */
            .agi-chat-typing {
                display: none;
                padding: 8px 16px;
            }
            
            .agi-chat-typing.visible {
                display: block;
            }
            
            .agi-typing-dots {
                display: flex;
                gap: 4px;
            }
            
            .agi-typing-dots span {
                width: 8px;
                height: 8px;
                background: var(--agi-primary);
                border-radius: 50%;
                animation: agi-bounce 1.4s infinite ease-in-out;
            }
            
            .agi-typing-dots span:nth-child(1) { animation-delay: 0s; }
            .agi-typing-dots span:nth-child(2) { animation-delay: 0.2s; }
            .agi-typing-dots span:nth-child(3) { animation-delay: 0.4s; }
            
            @keyframes agi-bounce {
                0%, 80%, 100% { transform: translateY(0); }
                40% { transform: translateY(-8px); }
            }
            
            /* Input */
            .agi-chat-input-container {
                padding: 16px;
                border-top: 1px solid var(--agi-border);
            }
            
            .agi-chat-form {
                display: flex;
                gap: 10px;
            }
            
            .agi-chat-input {
                flex: 1;
                background: var(--agi-bg-card);
                border: 1px solid var(--agi-border);
                border-radius: 25px;
                padding: 12px 16px;
                color: var(--agi-text);
                font-size: 14px;
                outline: none;
                transition: border-color 0.2s;
            }
            
            .agi-chat-input:focus {
                border-color: var(--agi-primary);
            }
            
            .agi-chat-input::placeholder {
                color: var(--agi-text-muted);
            }
            
            .agi-chat-send {
                background: var(--agi-primary);
                border: none;
                border-radius: 50%;
                width: 44px;
                height: 44px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                color: white;
                transition: background 0.2s, transform 0.2s;
            }
            
            .agi-chat-send:hover {
                background: var(--agi-primary-dark);
                transform: scale(1.05);
            }
            
            .agi-chat-send:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            /* Responsive */
            @media (max-width: 480px) {
                .agi-chat-window {
                    width: calc(100vw - 40px);
                    height: calc(100vh - 140px);
                    right: 20px;
                    left: 20px;
                }
            }
        `;
        document.head.appendChild(styles);
    }
    
    // Bind event listeners
    function bindEvents() {
        const button = document.getElementById('agi-chat-button');
        const close = document.getElementById('agi-chat-close');
        const window = document.getElementById('agi-chat-window');
        const form = document.getElementById('agi-chat-form');
        const input = document.getElementById('agi-chat-input');
        
        button.addEventListener('click', toggleChat);
        close.addEventListener('click', toggleChat);
        form.addEventListener('submit', handleSubmit);
        
        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && isOpen) {
                toggleChat();
            }
        });
        
        // Focus input when opening
        window.addEventListener('transitionend', () => {
            if (isOpen) {
                input.focus();
            }
        });
    }
    
    // Toggle chat window
    function toggleChat() {
        const window = document.getElementById('agi-chat-window');
        const button = document.getElementById('agi-chat-button');
        
        isOpen = !isOpen;
        
        if (isOpen) {
            window.classList.add('open');
            button.classList.add('hidden');
        } else {
            window.classList.remove('open');
            setTimeout(() => {
                button.classList.remove('hidden');
            }, 300);
        }
    }
    
    // Handle form submit
    function handleSubmit(e) {
        e.preventDefault();
        
        const input = document.getElementById('agi-chat-input');
        const message = input.value.trim();
        
        if (!message || isTyping) return;
        
        // Add user message
        addMessage(message, 'user');
        input.value = '';
        
        // Show typing indicator
        showTyping();
        
        // Simulate bot response (replace with actual API call)
        setTimeout(() => {
            hideTyping();
            addMessage(generateResponse(message), 'bot');
        }, 1500);
    }
    
    // Add message to chat
    function addMessage(text, sender) {
        const container = document.getElementById('agi-chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `agi-message agi-message-${sender}`;
        
        const avatar = sender === 'bot' ? CONFIG.botAvatar : '👤';
        
        messageDiv.innerHTML = `
            <div class="agi-message-avatar">${avatar}</div>
            <div class="agi-message-content">
                <div class="agi-message-text">${escapeHtml(text)}</div>
                <div class="agi-message-time">${getCurrentTime()}</div>
            </div>
        `;
        
        container.appendChild(messageDiv);
        container.scrollTop = container.scrollHeight;
        
        // Store message
        messages.push({ sender, text, time: new Date() });
        
        // Trim old messages
        if (messages.length > CONFIG.maxMessages) {
            messages = messages.slice(-CONFIG.maxMessages);
        }
    }
    
    // Show typing indicator
    function showTyping() {
        isTyping = true;
        document.getElementById('agi-chat-typing').classList.add('visible');
        document.getElementById('agi-chat-send').disabled = true;
    }
    
    // Hide typing indicator
    function hideTyping() {
        isTyping = false;
        document.getElementById('agi-chat-typing').classList.remove('visible');
        document.getElementById('agi-chat-send').disabled = false;
    }
    
    // Generate simple response (placeholder - replace with API call)
    function generateResponse(input) {
        const lower = input.toLowerCase();
        
        if (lower.includes('hello') || lower.includes('hi')) {
            return 'Hello! Welcome to AGI Company. How can I assist you today?';
        }
        if (lower.includes('price') || lower.includes('cost')) {
            return 'Our AI agents start at $99/month. Would you like to see our full pricing?';
        }
        if (lower.includes('contact') || lower.includes('support')) {
            return 'You can reach our support team through the Contact page or email support@agicompany.ai';
        }
        if (lower.includes('agent') || lower.includes('ai')) {
            return 'We have 36+ AI agents ready to help! They can handle sales, support, coding, and more. Which type interests you?';
        }
        
        return 'Thanks for your message! I\'m connecting you with one of our team members who can help further.';
    }
    
    // Get current time
    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    // Escape HTML
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createWidget);
    } else {
        createWidget();
    }
})();
