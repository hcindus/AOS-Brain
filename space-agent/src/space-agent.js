/**
 * Space Agent v1.0 - Browser-First AI Runtime
 * Connects to AOS Brain v4.5 via Mission Control API
 * Token-efficient YAML communication (inspired by Agent Zero)
 */

const SpaceAgent = {
    // Configuration
    config: {
        brainApiUrl: window.location.hostname === 'localhost' 
            ? 'http://localhost:8080' 
            : 'http://miles.myl0nr0s.cloud:8080',
        pollInterval: 1000,
        maxHistory: 50
    },

    // State
    state: {
        connected: false,
        brainStatus: null,
        widgets: new Map(),
        messageHistory: [],
        lastTick: 0
    },

    // WebSocket (for real-time brain updates)
    ws: null,

    /**
     * Initialize Space Agent
     */
    init() {
        console.log('🚀 Space Agent initializing...');
        
        // Start brain monitoring
        this.startBrainMonitor();
        
        // Load saved widgets
        this.loadSavedWidgets();
        
        console.log('✅ Space Agent ready');
    },

    /**
     * Start monitoring brain status
     */
    startBrainMonitor() {
        // Poll brain status
        setInterval(() => this.fetchBrainStatus(), this.config.pollInterval);
        
        // Initial fetch
        this.fetchBrainStatus();
    },

    /**
     * Fetch brain status from Mission Control API
     */
    async fetchBrainStatus() {
        try {
            const response = await fetch(`${this.config.brainApiUrl}/api/status`);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            const data = await response.json();
            this.state.brainStatus = data.brain;
            this.state.connected = true;
            
            // Update UI
            this.updateBrainUI(data.brain);
            
            // Check for tick advancement
            if (data.brain.tick > this.state.lastTick) {
                this.state.lastTick = data.brain.tick;
                this.onBrainTick(data.brain);
            }
            
        } catch (error) {
            this.state.connected = false;
            console.warn('Brain connection lost:', error.message);
            this.updateConnectionStatus(false);
        }
    },

    /**
     * Update brain-related UI elements
     */
    updateBrainUI(brain) {
        // Update header
        const tickEl = document.getElementById('brain-tick');
        const phaseEl = document.getElementById('brain-phase');
        
        if (tickEl) tickEl.textContent = `Tick: ${brain.tick}`;
        if (phaseEl) phaseEl.textContent = `Phase: ${brain.phase}`;
        
        // Update brain widgets
        document.querySelectorAll('[id^="brain-content-"]').forEach(widget => {
            const widgetId = widget.id.replace('brain-content-', '');
            this.updateBrainWidget(widgetId, brain);
        });
    },

    /**
     * Update a specific brain widget
     */
    updateBrainWidget(widgetId, brain) {
        const c = brain.consciousness;
        
        const elements = {
            tick: document.getElementById(`tick-${widgetId}`),
            phase: document.getElementById(`phase-${widgetId}`),
            signal: document.getElementById(`signal-${widgetId}`),
            con: document.getElementById(`con-${widgetId}`),
            sub: document.getElementById(`sub-${widgetId}`),
            uncon: document.getElementById(`uncon-${widgetId}`)
        };
        
        if (elements.tick) elements.tick.textContent = brain.tick;
        if (elements.phase) elements.phase.textContent = brain.phase;
        if (elements.signal) elements.signal.textContent = `${Math.round(brain.signal_quality_20avg * 100)}%`;
        if (elements.con) elements.con.textContent = `${c.conscious.active_items}/${c.conscious.capacity}`;
        if (elements.sub) elements.sub.textContent = `${c.subconscious.active_items}/${c.subconscious.capacity}`;
        if (elements.uncon) elements.uncon.textContent = `${c.unconscious.active_items}/${c.unconscious.capacity}`;
    },

    /**
     * Update connection status indicator
     */
    updateConnectionStatus(connected) {
        const indicator = document.querySelector('.status-dot');
        if (indicator) {
            indicator.style.background = connected ? '#22c55e' : '#ef4444';
            indicator.style.animation = connected ? 'pulse 2s infinite' : 'none';
        }
    },

    /**
     * Called on each brain tick
     */
    onBrainTick(brain) {
        // Could trigger widget updates based on brain state
        //console.log(`Brain tick ${brain.tick}: ${brain.phase}`);
    },

    /**
     * Send message to agent
     * Uses token-efficient format (plain text + YAML-like markers)
     */
    async send(message, widgetId) {
        // Add to history
        this.state.messageHistory.push({
            role: 'user',
            content: message,
            timestamp: Date.now()
        });
        
        // Trim history
        if (this.state.messageHistory.length > this.config.maxHistory) {
            this.state.messageHistory.shift();
        }
        
        // Perceive message in brain (for memory)
        this.perceiveInBrain(message);
        
        // Generate response
        const response = await this.generateResponse(message);
        
        // Display response
        this.displayResponse(response, widgetId);
    },

    /**
     * Perceive message in AOS Brain (stores in consciousness cascade)
     */
    async perceiveInBrain(message) {
        try {
            const response = await fetch(`${this.config.brainApiUrl}/api/command`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    cmd: 'perceive',
                    params: {
                        observation: `User: ${message}`,
                        intensity: 0.8
                    }
                })
            });
            
            if (!response.ok) {
                console.warn('Failed to perceive in brain:', response.status);
            }
        } catch (error) {
            console.warn('Brain perception failed:', error.message);
        }
    },

    /**
     * Generate response to user message
     * Uses simple template matching + brain state context
     */
    async generateResponse(message) {
        const lower = message.toLowerCase();
        
        // Simple pattern matching (token efficient)
        const patterns = [
            {
                pattern: /^(hi|hello|hey)/,
                response: "Hi! I'm Miles, your Space Agent. How can I help you today?"
            },
            {
                pattern: /(brain|consciousness|mind)/,
                response: () => {
                    const b = this.state.brainStatus;
                    if (!b) return "Brain not connected.";
                    const c = b.consciousness;
                    return `Brain v4.5 running. Tick ${b.tick}, Phase ${b.phase}. Consciousness layers: ${c.conscious.active_items}/${c.conscious.capacity} conscious, ${c.subconscious.active_items}/${c.subconscious.capacity} subconscious, ${c.unconscious.active_items}/${c.unconscious.capacity} unconscious.`;
                }
            },
            {
                pattern: /(status|how are you|what.*state)/,
                response: () => {
                    if (!this.state.connected) return "Brain disconnected.";
                    const b = this.state.brainStatus;
                    return `Operating normally. Signal quality ${Math.round(b.signal_quality_20avg * 100)}%. Lungs ${b.lungs.phase.toLowerCase()}, Liver ${b.liver.state.toLowerCase()}, Kidneys ${b.kidneys.state.toLowerCase()}.`;
                }
            },
            {
                pattern: /(help|what can you do)/,
                response: "I can: create widgets, monitor brain status, browse the web, generate code. What would you like to build?"
            },
            {
                pattern: /(\d+\s*[\+\-\*\/]\s*\d+)/,
                response: (match) => {
                    // Simple arithmetic (not using brain - direct calc)
                    try {
                        const result = eval(match[0]);
                        return `${match[0]} = ${result}`;
                    } catch {
                        return "I can't calculate that.";
                    }
                }
            }
        ];
        
        // Check patterns
        for (const p of patterns) {
            const match = lower.match(p.pattern);
            if (match) {
                if (typeof p.response === 'function') {
                    return p.response(match);
                }
                return p.response;
            }
        }
        
        // Default: acknowledge and offer help
        return "I understand. The brain has stored your message in the consciousness cascade. What would you like to do? Create a widget? Check brain status? Browse the web?";
    },

    /**
     * Display response in chat widget
     */
    displayResponse(response, widgetId) {
        const history = document.getElementById(`chat-history-${widgetId}`);
        if (!history) return;
        
        // Add agent message
        const agentMsg = document.createElement('div');
        agentMsg.className = 'msg msg-agent';
        agentMsg.innerHTML = response.replace(/\n/g, '<br>');
        history.appendChild(agentMsg);
        
        // Scroll to bottom
        history.scrollTop = history.scrollHeight;
    },

    /**
     * Save widget state
     */
    saveWidgets() {
        const widgets = [];
        document.querySelectorAll('.widget').forEach(w => {
            widgets.push({
                id: w.id,
                type: w.classList.contains('chat-widget') ? 'chat' : 'brain',
                x: parseInt(w.style.left),
                y: parseInt(w.style.top),
                width: w.offsetWidth,
                height: w.offsetHeight
            });
        });
        
        localStorage.setItem('space-agent-widgets', JSON.stringify(widgets));
    },

    /**
     * Load saved widgets
     */
    loadSavedWidgets() {
        const saved = localStorage.getItem('space-agent-widgets');
        if (!saved) return;
        
        try {
            const widgets = JSON.parse(saved);
            widgets.forEach(w => {
                if (w.type === 'chat') {
                    createChatWidget(w.x, w.y);
                } else if (w.type === 'brain') {
                    createBrainWidget(w.x, w.y);
                }
            });
        } catch (e) {
            console.warn('Failed to load saved widgets:', e);
        }
    },

    /**
     * Create custom widget (agent generates code)
     */
    async createCustomWidget(description) {
        // This would integrate with a code generation API
        // For now, placeholder
        console.log('Creating widget:', description);
        
        // Perceive in brain
        await this.perceiveInBrain(`Created widget: ${description}`);
        
        return {
            success: true,
            message: `Widget "${description}" created (placeholder)`
        };
    }
};

// Auto-save widgets on page unload
window.addEventListener('beforeunload', () => {
    SpaceAgent.saveWidgets();
});

// Expose globally
window.SpaceAgent = SpaceAgent;