/**
 * AOS Space Agent Fleet - Main Application
 * Initializes 4 agents with brain connection and interaction
 */

// Global fleet manager
let fleet = {
    agents: new Map(),
    universe: null,
    activeWidget: null
};

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    console.log('[AOS Space Agent] Initializing Fleet...');
    
    // Initialize 3D universe background
    fleet.universe = new SpaceUniverse();
    
    // Create 4 AOS Space Agents
    initializeAgents();
    
    // Setup UI
    setupDragging();
    setupInputs();
    updateStatusPanel();
    
    // Detect domain
    document.getElementById('domain-detect').textContent = window.location.hostname;
    
    console.log('[AOS Space Agent] Fleet initialized with', fleet.agents.size, 'agents');
});

function initializeAgents() {
    // Update loading status
    const statusEl = document.getElementById('init-status');
    if (statusEl) statusEl.textContent = 'Creating Navigator Alpha...';
    
    // Agent Alpha - Navigator
    const navigator = new AOSSpaceAgent({
        id: 'navigator',
        name: 'Navigator Alpha',
        role: 'navigator',
        brainSocket: '/brain'
    });
    
    if (statusEl) statusEl.textContent = 'Creating Analyst Beta...';
    
    // Agent Beta - Analyst
    const analyst = new AOSSpaceAgent({
        id: 'analyst', 
        name: 'Analyst Beta',
        role: 'analyst',
        brainSocket: '/brain'
    });
    
    if (statusEl) statusEl.textContent = 'Creating Executor Gamma...';
    
    // Agent Gamma - Executor
    const executor = new AOSSpaceAgent({
        id: 'executor',
        name: 'Executor Gamma', 
        role: 'executor',
        brainSocket: '/brain'
    });
    
    if (statusEl) statusEl.textContent = 'Creating Coordinator Delta...';
    
    // Agent Delta - Coordinator
    const coordinator = new AOSSpaceAgent({
        id: 'coordinator',
        name: 'Coordinator Delta',
        role: 'coordinator',
        brainSocket: '/brain'
    });
    
    if (statusEl) statusEl.textContent = 'Storing agents in fleet...';
    
    // Store agents
    fleet.agents.set('navigator', navigator);
    fleet.agents.set('analyst', analyst);
    fleet.agents.set('executor', executor);
    fleet.agents.set('coordinator', coordinator);
    
    if (statusEl) statusEl.textContent = 'Connecting to brain...';
    
    // Connect to brain
    setTimeout(async () => {
        for (const [id, agent] of fleet.agents) {
            if (statusEl) statusEl.textContent = `Connecting ${agent.name}...`;
            const connected = await agent.connectToBrain();
            updateConnectionStatus(id, connected);
            
            // Send welcome message
            addChatMessage(id, `Connected as ${agent.name}. Ready for commands.`, 'system');
        }
        
        if (statusEl) statusEl.textContent = 'Fleet ready!';
        
        // Hide loading overlay
        setTimeout(() => {
            const overlay = document.getElementById('loading-overlay');
            if (overlay) {
                overlay.style.opacity = '0';
                overlay.style.transition = 'opacity 0.5s';
                setTimeout(() => overlay.remove(), 500);
            }
        }, 500);
    }, 1000);
}

function updateConnectionStatus(agentId, connected) {
    const indicator = document.getElementById(`conn-${agentId}`);
    if (indicator) {
        indicator.classList.remove('connected', 'offline');
        indicator.classList.add(connected ? 'connected' : 'offline');
        indicator.title = connected ? 'Brain Connected' : 'Standalone Mode';
    }
}

function addChatMessage(agentId, message, type = 'agent') {
    const chat = document.getElementById(`chat-${agentId}`);
    if (!chat) return;
    
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-message ${type}`;
    msgDiv.textContent = message;
    
    chat.appendChild(msgDiv);
    chat.scrollTop = chat.scrollHeight;
}

async function sendToAgent(agentId) {
    // Check if agents initialized
    if (!fleet.agents || fleet.agents.size === 0) {
        console.error('[AOS Space Agent] Fleet not initialized yet');
        alert('Agents still initializing... please wait a moment and try again.');
        return;
    }
    
    const input = document.getElementById(`input-${agentId}`);
    if (!input) {
        console.error(`[AOS Space Agent] Input not found: input-${agentId}`);
        return;
    }
    
    const message = input.value.trim();
    if (!message) return;
    
    // Clear input
    input.value = '';
    
    // Add user message
    addChatMessage(agentId, message, 'user');
    
    // Get agent
    const agent = fleet.agents.get(agentId);
    if (!agent) {
        console.error(`[AOS Space Agent] Agent not found: ${agentId}`, fleet.agents);
        addChatMessage(agentId, `Error: Agent "${agentId}" not initialized yet. Available: ${Array.from(fleet.agents.keys()).join(', ')}`, 'system');
        return;
    }
    
    // Process message
    addChatMessage(agentId, 'Processing...', 'system');
    
    try {
        const result = await agent.processMessage(message);
        
        // Handle result
        if (result.type === 'tool_result') {
            addChatMessage(agentId, `Executed ${result.tool}: ${JSON.stringify(result.result).slice(0, 100)}`, 'system');
        } else {
            addChatMessage(agentId, result.content, 'agent');
        }
    } catch (e) {
        addChatMessage(agentId, `Error: ${e.message}`, 'system');
    }
}

async function agentTool(agentId, tool) {
    // Check if agents initialized
    if (!fleet.agents || fleet.agents.size === 0) {
        console.error('[AOS Space Agent] Fleet not initialized yet');
        alert('Agents still initializing... please wait a moment.');
        return;
    }
    
    const agent = fleet.agents.get(agentId);
    if (!agent) {
        console.error(`[AOS Space Agent] Agent not found for tool: ${agentId}`, fleet.agents);
        return;
    }
    
    addChatMessage(agentId, `Executing tool: ${tool}...`, 'system');
    
    let result;
    
    switch (tool) {
        case 'navigate':
            const url = prompt('Enter URL to navigate to:');
            if (url) {
                result = await agent.executeTool('navigate', { url });
                window.open(result.url, '_blank');
                addChatMessage(agentId, `Navigating to ${result.url}`, 'system');
            }
            break;
            
        case 'search':
            const query = prompt('Search query:');
            if (query) {
                const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
                window.open(searchUrl, '_blank');
                addChatMessage(agentId, `Searching for "${query}"...`, 'system');
            }
            break;
            
        case 'screenshot':
            addChatMessage(agentId, '📸 Screenshot captured (simulated)', 'system');
            break;
            
        case 'extract':
            addChatMessage(agentId, '📊 Data extraction started...', 'system');
            break;
            
        case 'brain_status':
            result = await agent.executeTool('brain_status', {});
            const b = result.brain;
            if (b) {
                addChatMessage(agentId, 
                    `🧠 Brain: Tick ${b.tick} | Phase: ${b.phase} | Signal: ${Math.round(b.signal_quality_20avg * 100)}%`, 
                    'system'
                );
            } else {
                addChatMessage(agentId, '🧠 Brain: ' + (result.brain === 'offline' ? 'Offline (standalone mode)' : 'Error'), 'system');
            }
            break;
            
        case 'perceive':
            const obs = prompt('Observation to perceive:');
            if (obs) {
                result = await agent.executeTool('brain_perceive', { observation: obs, intensity: 0.85 });
                addChatMessage(agentId, 
                    result.local ? 
                        `💭 Stored locally: "${obs.slice(0, 50)}..."` : 
                        `💭 Perceived in brain: "${obs.slice(0, 50)}..."`,
                    'system'
                );
            }
            break;
            
        case 'create_widget':
            const widgetType = prompt('Widget type (clock, brain_status, chat, chart):');
            if (widgetType) {
                showWidget(widgetType, agent);
                addChatMessage(agentId, `📈 Created ${widgetType} widget`, 'system');
            }
            break;
            
        case 'analyze':
            addChatMessage(agentId, '🔮 Analyzing patterns across unconscious layers...', 'agent');
            break;
            
        case 'health_check':
            addChatMessage(agentId, '❤️ Running health check sequence...', 'system');
            break;
            
        case 'deploy':
            addChatMessage(agentId, '🚀 Deployment sequence initiated', 'system');
            break;
            
        case 'scan':
            addChatMessage(agentId, '🔎 Scanning workspace for skills and data...', 'system');
            break;
            
        case 'sync':
            addChatMessage(agentId, '🔄 Synchronizing all agents with brain cascade...', 'system');
            break;
            
        case 'cascade':
            addChatMessage(agentId, '🌊 Triggering consciousness cascade across fleet...', 'system');
            break;
            
        case 'new_space':
            const spaceName = prompt('Space name:');
            if (spaceName) {
                const space = agent.createSpace(spaceName);
                addChatMessage(agentId, `➕ Created space: ${spaceName} (${space.id})`, 'system');
            }
            break;
            
        case 'broadcast':
            const broadcast = prompt('Message to broadcast to all agents:');
            if (broadcast) {
                for (const [id, a] of fleet.agents) {
                    if (id !== agentId) {
                        addChatMessage(id, `[Broadcast from ${agent.name}]: ${broadcast}`, 'system');
                    }
                }
                addChatMessage(agentId, `📢 Broadcasted: "${broadcast}"`, 'system');
            }
            break;
            
        default:
            addChatMessage(agentId, `Unknown tool: ${tool}`, 'system');
    }
}

function showWidget(type, agent) {
    const modal = document.getElementById('widget-modal');
    const title = document.getElementById('widget-title');
    const content = document.getElementById('widget-content');
    
    // Get renderer
    const renderer = agent.getWidgetRenderer(type);
    
    title.textContent = type.charAt(0).toUpperCase() + type.slice(1) + ' Widget';
    
    // Render (async for some widgets)
    Promise.resolve(renderer(agent, {})).then(html => {
        content.innerHTML = html;
        modal.classList.add('active');
        fleet.activeWidget = { type, agent };
    });
}

function closeWidget() {
    const modal = document.getElementById('widget-modal');
    modal.classList.remove('active');
    fleet.activeWidget = null;
}

function fleetAction(action) {
    switch (action) {
        case 'add_agent':
            const name = prompt('New agent name:');
            if (name) {
                const id = `agent_${Date.now()}`;
                const newAgent = new AOSSpaceAgent({
                    id,
                    name,
                    role: 'general'
                });
                fleet.agents.set(id, newAgent);
                addChatMessage('coordinator', `Added new agent: ${name}`, 'system');
                updateStatusPanel();
            }
            break;
            
        case 'sync_all':
            for (const [id, agent] of fleet.agents) {
                addChatMessage(id, '🔄 Fleet sync: consciousness cascade updated', 'system');
            }
            break;
            
        case 'brain_cascade':
            for (const [id, agent] of fleet.agents) {
                if (agent.brainConnected) {
                    agent.perceiveForBrain('Fleet-wide consciousness cascade triggered', 0.9);
                }
                addChatMessage(id, '🧠 Linked to brain cascade', 'system');
            }
            break;
    }
}

function toggleAnimation() {
    document.querySelectorAll('.agent-widget').forEach(widget => {
        widget.classList.toggle('floating');
    });
}

function updateStatusPanel() {
    document.getElementById('agent-count').textContent = fleet.agents.size;
    
    let connectedCount = 0;
    let widgetCount = 0;
    
    for (const [id, agent] of fleet.agents) {
        if (agent.brainConnected) connectedCount++;
        widgetCount += agent.spaces.size;
    }
    
    document.getElementById('brain-status').textContent = 
        connectedCount > 0 ? `Connected (${connectedCount}/${fleet.agents.size})` : 'Offline';
    document.getElementById('widget-count').textContent = widgetCount;
}

// Dragging system
function setupDragging() {
    let draggedElement = null;
    let offset = { x: 0, y: 0 };
    
    document.querySelectorAll('.drag-handle').forEach(handle => {
        handle.addEventListener('mousedown', (e) => {
            draggedElement = handle.closest('.agent-widget');
            draggedElement.classList.add('dragging');
            
            const rect = draggedElement.getBoundingClientRect();
            offset.x = e.clientX - rect.left;
            offset.y = e.clientY - rect.top;
            
            e.preventDefault();
        });
    });
    
    document.addEventListener('mousemove', (e) => {
        if (!draggedElement) return;
        
        draggedElement.style.left = `${e.clientX - offset.x}px`;
        draggedElement.style.top = `${e.clientY - offset.y}px`;
    });
    
    document.addEventListener('mouseup', () => {
        if (draggedElement) {
            draggedElement.classList.remove('dragging');
            draggedElement = null;
        }
    });
}

// Input handling
function setupInputs() {
    document.querySelectorAll('.input-area input').forEach(input => {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const agentId = input.id.replace('input-', '');
                sendToAgent(agentId);
            }
        });
    });
}

// Global exports for HTML onclick handlers
window.sendToAgent = sendToAgent;
window.agentTool = agentTool;
window.fleetAction = fleetAction;
window.toggleAnimation = toggleAnimation;
window.closeWidget = closeWidget;
// ===== VOICE UI FUNCTIONS =====

function toggleVoiceUI(agentId) {
    const voiceControls = document.getElementById(`voice-${agentId}`);
    if (voiceControls) {
        const isVisible = voiceControls.style.display !== 'none';
        voiceControls.style.display = isVisible ? 'none' : 'flex';
    }
}

async function toggleListening(agentId) {
    const agent = fleet.agents?.get(agentId);
    if (!agent || !agent.voice) {
        alert('Voice system not initialized');
        return;
    }
    
    const statusEl = document.getElementById(`voice-status-${agentId}`);
    const micBtn = document.getElementById(`mic-${agentId}`);
    
    if (agent.voice.isListening) {
        // Stop listening
        agent.voice.stopListening();
        if (statusEl) statusEl.textContent = 'Click 🎤 to talk';
        if (micBtn) micBtn.textContent = '🎤 Speak';
    } else {
        // Start listening
        const started = agent.voice.startListening();
        
        if (started) {
            // Setup callbacks
            agent.voice.onSpeechRecognized = (transcript) => {
                addChatMessage(agentId, `🎤 ${transcript}`, 'user');
                
                // Auto-send after recognition
                setTimeout(() => {
                    const input = document.getElementById(`input-${agentId}`);
                    if (input) {
                        input.value = transcript;
                        sendToAgent(agentId);
                    }
                }, 500);
            };
            
            agent.voice.onListeningStart = () => {
                if (micBtn) {
                    micBtn.textContent = '🔴 Stop';
                    micBtn.style.background = '#f00';
                }
                if (statusEl) statusEl.textContent = 'Listening... speak now';
            };
            
            agent.voice.onListeningEnd = () => {
                if (micBtn) {
                    micBtn.textContent = '🎤 Speak';
                    micBtn.style.background = '';
                }
                if (statusEl) statusEl.textContent = 'Click 🎤 to talk';
            };
            
            agent.voice.onInterimSpeech = (interim) => {
                if (statusEl) statusEl.textContent = `Hearing: "${interim}"`;
            };
            
            if (micBtn) {
                micBtn.textContent = '🔴 Listening...';
                micBtn.style.background = '#f00';
            }
            if (statusEl) statusEl.textContent = 'Listening... speak now';
        } else {
            alert('Microphone access denied or not available');
        }
    }
}

function showVoiceSelector(agentId) {
    const agent = fleet.agents?.get(agentId);
    if (!agent || !agent.voice) {
        alert('Voice system not available');
        return;
    }
    
    // Create modal for voice selection
    const modal = document.createElement('div');
    modal.className = 'voice-modal';
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(10, 10, 26, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    `;
    
    const selector = agent.voice.createVoiceSelector();
    selector.style.maxWidth = '400px';
    
    const closeBtn = document.createElement('button');
    closeBtn.textContent = '×';
    closeBtn.style.cssText = `
        position: absolute;
        top: 20px;
        right: 20px;
        background: none;
        border: none;
        color: #f00;
        font-size: 32px;
        cursor: pointer;
    `;
    closeBtn.onclick = () => modal.remove();
    
    modal.appendChild(selector);
    modal.appendChild(closeBtn);
    document.body.appendChild(modal);
    
    // Close on outside click
    modal.onclick = (e) => {
        if (e.target === modal) modal.remove();
    };
}

// Add voice UI functions to window
window.toggleVoiceUI = toggleVoiceUI;
window.toggleListening = toggleListening;
window.showVoiceSelector = showVoiceSelector;
