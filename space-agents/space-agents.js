/**
 * Space Agent Fleet Controller
 * Manages draggable agents, tool execution, and brain connectivity
 */

class SpaceAgentFleet {
    constructor() {
        this.agents = new Map();
        this.dragState = {
            active: false,
            agent: null,
            offset: { x: 0, y: 0 }
        };
        this.brainConnected = false;
        this.init();
    }

    init() {
        this.setupDragging();
        this.setupInputs();
        this.detectDomain();
        this.tryBrainConnection();
    }

    detectDomain() {
        const domain = window.location.hostname;
        document.getElementById('domain').textContent = domain;
        console.log(`[Fleet] Domain detected: ${domain}`);
    }

    async tryBrainConnection() {
        try {
            // Try to connect to local brain via API
            const response = await fetch('/brain/api/status', {
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });
            
            if (response.ok) {
                const data = await response.json();
                this.brainConnected = true;
                console.log('[Fleet] Brain connected:', data.brain?.version || 'v4.5');
                this.broadcastToAgents('🧠 Brain link established');
            }
        } catch (e) {
            console.log('[Fleet] Brain not available locally, using standalone mode');
            this.brainConnected = false;
        }
    }

    setupDragging() {
        const widgets = document.querySelectorAll('.agent-widget');
        
        widgets.forEach(widget => {
            const handle = widget.querySelector('.drag-handle');
            
            handle.addEventListener('mousedown', (e) => {
                this.dragState.active = true;
                this.dragState.agent = widget;
                
                const rect = widget.getBoundingClientRect();
                this.dragState.offset = {
                    x: e.clientX - rect.left,
                    y: e.clientY - rect.top
                };
                
                widget.classList.add('dragging');
                e.preventDefault();
            });
        });

        document.addEventListener('mousemove', (e) => {
            if (!this.dragState.active || !this.dragState.agent) return;
            
            const widget = this.dragState.agent;
            const x = e.clientX - this.dragState.offset.x;
            const y = e.clientY - this.dragState.offset.y;
            
            widget.style.left = `${x}px`;
            widget.style.top = `${y}px`;
            
            // Update connections
            this.updateAgentConnections();
        });

        document.addEventListener('mouseup', () => {
            if (this.dragState.active && this.dragState.agent) {
                this.dragState.agent.classList.remove('dragging');
                this.dragState.active = false;
                this.dragState.agent = null;
            }
        });
    }

    setupInputs() {
        ['alpha', 'beta', 'gamma'].forEach(agentId => {
            const input = document.getElementById(`input-${agentId}`);
            if (input) {
                input.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        sendToAgent(agentId);
                    }
                });
            }
        });
    }

    updateAgentConnections() {
        // Visual connections between agents could be drawn here
        const agents = document.querySelectorAll('.agent-widget');
        agents.forEach((agent1, i) => {
            agents.forEach((agent2, j) => {
                if (i >= j) return;
                
                const rect1 = agent1.getBoundingClientRect();
                const rect2 = agent2.getBoundingClientRect();
                
                const x1 = rect1.left + rect1.width / 2;
                const y1 = rect1.top + rect1.height / 2;
                const x2 = rect2.left + rect2.width / 2;
                const y2 = rect2.top + rect2.height / 2;
                
                const distance = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
                
                if (distance < 400) {
                    // Agents are close - could trigger sync behavior
                    this.onAgentsClose(agent1.id, agent2.id, distance);
                }
            });
        });
    }

    onAgentsClose(id1, id2, distance) {
        // Agents floating near each other
        console.log(`[Fleet] Agents close: ${id1} <-> ${id2} (${Math.round(distance)}px)`);
    }

    broadcastToAgents(message) {
        ['alpha', 'beta', 'gamma'].forEach(agentId => {
            this.addChatMessage(agentId, message, false);
        });
    }

    addChatMessage(agentId, message, isUser = false) {
        const chat = document.getElementById(`chat-${agentId}`);
        if (!chat) return;
        
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-message ${isUser ? 'user' : ''}`;
        msgDiv.textContent = message;
        
        chat.appendChild(msgDiv);
        chat.scrollTop = chat.scrollHeight;
    }
}

// Global fleet instance
let fleet;

document.addEventListener('DOMContentLoaded', () => {
    fleet = new SpaceAgentFleet();
});

// Agent communication functions
async function sendToAgent(agentId) {
    const input = document.getElementById(`input-${agentId}`);
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add to chat
    fleet.addChatMessage(agentId, message, true);
    input.value = '';
    
    // Process based on agent type
    const response = await processAgentCommand(agentId, message);
    
    // Add response
    setTimeout(() => {
        fleet.addChatMessage(agentId, response);
    }, 500 + Math.random() * 500);
}

async function processAgentCommand(agentId, message) {
    const lowerMsg = message.toLowerCase();
    
    // Agent Alpha - Browser/Navigation
    if (agentId === 'alpha') {
        if (lowerMsg.includes('navigate') || lowerMsg.includes('go to') || lowerMsg.startsWith('http')) {
            let url = message.replace(/navigate to|go to/i, '').trim();
            if (!url.startsWith('http')) url = 'https://' + url;
            
            // Open in new tab (browser automation would happen server-side)
            window.open(url, '_blank');
            return `🌐 Opening ${url} in new tab...`;
        }
        
        if (lowerMsg.includes('search')) {
            const query = message.replace(/search for|search/i, '').trim();
            const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
            window.open(searchUrl, '_blank');
            return `🔍 Searching for "${query}"...`;
        }
        
        return `🤔 I'm a browser agent. Try: "navigate to example.com" or "search for AI agents"`;
    }
    
    // Agent Beta - Brain/Analytics
    if (agentId === 'beta') {
        if (lowerMsg.includes('status') || lowerMsg.includes('brain')) {
            try {
                const response = await fetch('/brain/api/status');
                if (response.ok) {
                    const data = await response.json();
                    const b = data.brain;
                    return `🧠 Brain tick ${b.tick} | Phase: ${b.phase} | Signal: ${Math.round(b.signal_quality_20avg * 100)}%`;
                }
            } catch (e) {
                return `🧠 Brain not connected locally. Using standalone mode.`;
            }
        }
        
        if (lowerMsg.includes('perceive') || lowerMsg.includes('feed')) {
            const content = message.replace(/perceive|feed/i, '').trim();
            try {
                await fetch('/brain/api/command', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        cmd: 'perceive',
                        params: { observation: content, intensity: 0.8 }
                    })
                });
                return `💭 Perceived: "${content.substring(0, 50)}..."`;
            } catch (e) {
                return `💭 Would perceive (brain offline): "${content.substring(0, 50)}..."`;
            }
        }
        
        return `📊 I'm connected to the Brain. Try: "brain status" or "perceive [observation]"`;
    }
    
    // Agent Gamma - Executor
    if (agentId === 'gamma') {
        if (lowerMsg.includes('health') || lowerMsg.includes('check')) {
            return `✅ Health check would run: agent_keepalive.sh --no-restart`;
        }
        
        if (lowerMsg.includes('deploy')) {
            return `🚀 Deployment sequence initiated...`;
        }
        
        if (lowerMsg.includes('bash') || lowerMsg.includes('command')) {
            return `💻 Bash execution requires server-side. Commands: health-check, deploy, scan`;
        }
        
        return `⚡ I'm a task executor. Try: "health check" or "deploy"`;
    }
    
    return `Unknown agent: ${agentId}`;
}

async function agentTool(agentId, tool) {
    const toolActions = {
        'alpha': {
            'navigate': () => {
                const url = prompt('Enter URL:');
                if (url) window.open(url.startsWith('http') ? url : 'https://' + url, '_blank');
            },
            'search': () => {
                const query = prompt('Search query:');
                if (query) window.open(`https://www.google.com/search?q=${encodeURIComponent(query)}`, '_blank');
            },
            'screenshot': () => alert('📸 Screenshot would capture current page'),
            'extract': () => alert('📊 Data extraction would analyze page content')
        },
        'beta': {
            'brain-status': async () => {
                try {
                    const res = await fetch('/brain/api/status');
                    const data = await res.json();
                    fleet.addChatMessage('beta', `🧠 Brain v${data.brain?.version || '4.5'} | Tick ${data.brain?.tick || 'N/A'} | ${data.brain?.phase || 'unknown'}`);
                } catch (e) {
                    fleet.addChatMessage('beta', '🧠 Brain connection failed. Standalone mode.');
                }
            },
            'perceive': () => {
                const obs = prompt('Observation to feed to brain:');
                if (obs) fleet.addChatMessage('beta', `💭 Would perceive: ${obs}`);
            },
            'analyze': () => fleet.addChatMessage('beta', '📈 Analysis mode: examining patterns...'),
            'forecast': () => fleet.addChatMessage('beta', '🔮 Forecasting based on unconscious patterns...')
        },
        'gamma': {
            'bash': () => {
                const cmd = prompt('Command:');
                if (cmd) fleet.addChatMessage('gamma', `💻 Would execute: ${cmd}`);
            },
            'health-check': () => fleet.addChatMessage('gamma', '❤️ Running: bash agent_keepalive.sh --no-restart'),
            'deploy': () => fleet.addChatMessage('gamma', '🚀 Deployment: staging files...'),
            'scan': () => fleet.addChatMessage('gamma', '🔎 Scanning workspace...')
        }
    };
    
    const action = toolActions[agentId]?.[tool];
    if (action) {
        await action();
    }
}

function addAgent() {
    const id = `agent-${Date.now()}`;
    alert(`New agent would be created: ${id}`);
    // Could dynamically create new agent widgets here
}

function fleetAction(action) {
    if (action === 'sync') {
        fleet.broadcastToAgents('🔄 Fleet synchronization complete');
    } else if (action === 'cascade') {
        fleet.broadcastToAgents('🌊 Consciousness cascade initiated');
    }
}

function toggleFloat() {
    document.querySelectorAll('.agent-widget').forEach(widget => {
        widget.classList.toggle('floating');
    });
}

// Export for global access
window.sendToAgent = sendToAgent;
window.agentTool = agentTool;
window.addAgent = addAgent;
window.fleetAction = fleetAction;
window.toggleFloat = toggleFloat;
