/**
 * Emma - Consolidated AOS Space Agent
 * Single agent with ALL capabilities: Navigator + Analyst + Executor + Coordinator
 * Voice: Emma (Female, thoughtful but versatile)
 * Personality: Adaptive scholar with explorer, soldier, and diplomat modes
 */

class EmmaAgent {
    constructor(config = {}) {
        this.id = 'emma';
        this.name = 'Emma';
        this.role = 'universal'; // All roles combined
        this.brainSocketUrl = config.brainSocket || this.detectBrainUrl();
        
        // Voice system
        this.voice = new AgentVoiceSystem(this);
        this.voice.setVoice('emma');
        
        // State
        this.brainConnected = false;
        this.memory = {
            shortTerm: [],
            longTerm: new Map(),
            skills: new Map(),
            spaces: new Map()
        };
        
        // Personality modes
        this.modes = {
            explorer: {
                phrases: [
                    "Charting a course through the digital cosmos...",
                    "The web is vast and full of wonder.",
                    "Setting coordinates now. Full speed ahead!",
                    "I've got the helm. Where shall we voyage?"
                ],
                voiceMod: { pitch: 1.0, rate: 1.1 }
            },
            scholar: {
                phrases: [
                    "The data reveals fascinating patterns...",
                    "Analyzing consciousness cascade activity...",
                    "The brain whispers its secrets. Let me listen.",
                    "Knowledge emerges from careful observation."
                ],
                voiceMod: { pitch: 1.1, rate: 0.95 }
            },
            soldier: {
                phrases: [
                    "Task acknowledged. Executing now.",
                    "Mission parameters received. Deploying resources.",
                    "Systems locked. Commencing operation.",
                    "Executing with precision. Stand by."
                ],
                voiceMod: { pitch: 0.95, rate: 1.05 }
            },
            diplomat: {
                phrases: [
                    "The fleet moves as one through my coordination.",
                    "Harmony through unified action.",
                    "Together, we are greater than our parts.",
                    "Synchronizing all systems for optimal flow."
                ],
                voiceMod: { pitch: 1.05, rate: 1.0 }
            }
        };
        
        // Tool implementations
        this.tools = new AgentTools(this);
        
        // Auto-speak responses
        this.autoSpeak = true;
        
        console.log('[Emma] 🌟 Initialized. All systems online.');
    }
    
    detectBrainUrl() {
        const hostname = window.location.hostname;
        if (hostname.includes('myl0nr0s.cloud')) {
            return 'https://tappylewis.cloud/brain';
        }
        return '/brain';
    }
    
    async initialize() {
        const statusEl = document.getElementById('loading-status');
        
        if (statusEl) statusEl.textContent = 'Connecting to neural network...';
        this.brainConnected = await this.connectToBrain();
        
        if (statusEl) statusEl.textContent = 'Initializing voice system...';
        await this.setupVoice();
        
        if (statusEl) statusEl.textContent = 'Emma is ready!';
        
        // Hide loading
        setTimeout(() => {
            const overlay = document.getElementById('loading-overlay');
            if (overlay) {
                overlay.style.opacity = '0';
                overlay.style.transition = 'opacity 0.5s';
                setTimeout(() => overlay.remove(), 500);
            }
        }, 500);
        
        // Update status indicators
        this.updateStatusIndicators();
        
        // Greet
        this.addChatMessage('system', 'Connected to AOS Brain v4.5. All capabilities online: Navigate, Analyze, Execute, Coordinate.');
        this.speak("Hello, I'm Emma. Your unified space agent. I can navigate the web, analyze data, execute tasks, and coordinate systems. How may I assist you?", 'diplomat');
    }
    
    async connectToBrain() {
        try {
            const response = await fetch(`${this.brainSocketUrl}/api/status`, {
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });
            
            if (response.ok) {
                const data = await response.json();
                console.log('[Emma] 🧠 Brain connected:', data.brain?.version || 'v4.5');
                return true;
            }
        } catch (e) {
            console.log('[Emma] 🧠 Brain offline, operating in standalone mode');
        }
        return false;
    }
    
    async setupVoice() {
        // Request microphone permission
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            try {
                await navigator.mediaDevices.getUserMedia({ audio: true });
                console.log('[Emma] 🎤 Microphone access granted');
            } catch (e) {
                console.log('[Emma] 🎤 Microphone access denied, STT unavailable');
            }
        }
    }
    
    updateStatusIndicators() {
        const brainDot = document.getElementById('brain-status');
        const voiceDot = document.getElementById('voice-status');
        const activeDot = document.getElementById('active-status');
        
        if (brainDot) {
            brainDot.classList.toggle('connected', this.brainConnected);
            brainDot.classList.toggle('offline', !this.brainConnected);
        }
        if (voiceDot) {
            voiceDot.classList.toggle('active', true);
        }
        if (activeDot) {
            activeDot.classList.toggle('active', true);
        }
    }
    
    // ===== INTELLIGENT MESSAGE PROCESSING =====
    
    async processMessage(message) {
        // Store
        this.memory.shortTerm.push({
            role: 'user',
            content: message,
            timestamp: Date.now()
        });
        
        this.addChatMessage('user', message);
        
        // Determine intent and mode
        const analysis = this.analyzeIntent(message);
        const mode = analysis.mode;
        const action = analysis.action;
        
        // Execute based on intent
        let response;
        
        switch (action) {
            case 'navigate':
                response = await this.handleNavigate(analysis.params.url);
                break;
            case 'search':
                response = await this.handleSearch(analysis.params.query);
                break;
            case 'brain_status':
                response = await this.handleBrainStatus();
                break;
            case 'perceive':
                response = await this.handlePerceive(analysis.params.observation);
                break;
            case 'analyze':
                response = await this.handleAnalyze();
                break;
            case 'health_check':
                response = await this.handleHealthCheck();
                break;
            case 'scan':
                response = await this.handleScan();
                break;
            case 'deploy':
                response = await this.handleDeploy();
                break;
            case 'screenshot':
                response = await this.handleScreenshot();
                break;
            case 'extract':
                response = await this.handleExtract();
                break;
            case 'widget':
                response = await this.handleWidget(analysis.params.type);
                break;
            case 'sync':
                response = await this.handleSync();
                break;
            default:
                response = await this.handleChat(message, mode);
        }
        
        // Display and speak
        this.addChatMessage('emma', response.text);
        
        if (this.autoSpeak) {
            this.speak(response.text, mode);
        }
        
        return response;
    }
    
    analyzeIntent(message) {
        const lower = message.toLowerCase();
        
        // Navigation patterns
        if (/navigate to|go to|open|visit|take me to/i.test(lower)) {
            const url = message.match(/(?:navigate to|go to|open|visit|take me to)\s+(\S+)/i)?.[1];
            return { mode: 'explorer', action: 'navigate', params: { url } };
        }
        
        // Search patterns
        if (/search for|find|look up|google/i.test(lower)) {
            const query = message.replace(/search for|find|look up|google/i, '').trim();
            return { mode: 'explorer', action: 'search', params: { query } };
        }
        
        // Brain patterns
        if (/brain status|consciousness|how is the brain|neural/i.test(lower)) {
            return { mode: 'scholar', action: 'brain_status', params: {} };
        }
        
        if (/perceive|learn|remember|store|feed/i.test(lower)) {
            const observation = message.replace(/perceive|learn|remember|store|feed/i, '').trim();
            return { mode: 'scholar', action: 'perceive', params: { observation } };
        }
        
        if (/analyze|examine|study|investigate/i.test(lower)) {
            return { mode: 'scholar', action: 'analyze', params: {} };
        }
        
        // Task patterns
        if (/health check|status check|diagnostic/i.test(lower)) {
            return { mode: 'soldier', action: 'health_check', params: {} };
        }
        
        if (/scan|survey|explore environment/i.test(lower)) {
            return { mode: 'soldier', action: 'scan', params: {} };
        }
        
        if (/deploy|launch|initiate|start/i.test(lower)) {
            return { mode: 'soldier', action: 'deploy', params: {} };
        }
        
        // Utility patterns
        if (/screenshot|capture|picture/i.test(lower)) {
            return { mode: 'soldier', action: 'screenshot', params: {} };
        }
        
        if (/extract|download|save data/i.test(lower)) {
            return { mode: 'scholar', action: 'extract', params: {} };
        }
        
        if (/widget|create.*widget|make.*widget/i.test(lower)) {
            const type = message.match(/(\w+)\s+widget/i)?.[1] || 'clock';
            return { mode: 'scholar', action: 'widget', params: { type } };
        }
        
        if (/sync|synchronize|align|harmonize/i.test(lower)) {
            return { mode: 'diplomat', action: 'sync', params: {} };
        }
        
        // Default chat
        if (/hello|hi|greeting|welcome/i.test(lower)) {
            return { mode: 'diplomat', action: 'chat', params: { greeting: true } };
        }
        
        return { mode: 'scholar', action: 'chat', params: {} };
    }
    
    // ===== HANDLERS =====
    
    async handleNavigate(url) {
        if (!url) {
            return { text: "I'd be happy to navigate, but where shall we go? Please provide a URL or website name." };
        }
        
        const result = await this.tools.navigate(url);
        
        if (result.navigated) {
            const phrase = this.modes.explorer.phrases[0];
            return { 
                text: `${phrase} Opening ${result.url} in a new portal.` 
            };
        } else {
            return { text: result.error || "Navigation encountered an obstacle. Shall we try a different route?" };
        }
    }
    
    async handleSearch(query) {
        if (!query) {
            return { text: "I'm ready to search the vast archives. What knowledge do you seek?" };
        }
        
        const result = await this.tools.search(query);
        
        return { 
            text: `Scanning the digital archives for "${query}"... ${this.modes.explorer.phrases[2]} Search portal opened.` 
        };
    }
    
    async handleBrainStatus() {
        const result = await this.tools.brainStatus();
        
        if (result.brain && typeof result.brain === 'object') {
            const b = result.brain;
            return { 
                text: `The neural network pulses with life. Tick ${b.tick}, phase ${b.phase}. Signal quality at ${Math.round((b.signal_quality_20avg || 0) * 100)}%. The unconscious holds ${b.consciousness?.unconscious?.active_items || 0} abstractions, cascading through consciousness layers. ${this.modes.scholar.phrases[1]}` 
            };
        } else {
            return { text: `The brain connection is dormant. Operating in standalone mode with local memory only. ${this.modes.scholar.phrases[3]}` };
        }
    }
    
    async handlePerceive(observation) {
        if (!observation) {
            return { text: "What shall I perceive and store in the consciousness cascade?" };
        }
        
        const result = await this.tools.brainPerceive(observation, 0.85);
        
        if (result.perceived) {
            if (result.local) {
                return { text: `Stored locally: "${observation.slice(0, 50)}..." The brain is offline, but I maintain this in my working memory.` };
            } else {
                return { text: `Perception registered. The observation cascades: conscious → subconscious → unconscious. Currently ${result.unconsciousCount || 'many'} abstractions deep in memory. ${this.modes.scholar.phrases[2]}` };
            }
        } else {
            return { text: "Perception failed. The neural pathways encountered resistance." };
        }
    }
    
    async handleAnalyze() {
        const result = await this.tools.analyzePatterns();
        
        return { 
            text: `Analyzing patterns across ${result.patterns.totalInteractions} interactions. Recent topics: ${result.patterns.recentTopics.join(', ') || 'general conversation'}. ${this.modes.scholar.phrases[0]}` 
        };
    }
    
    async handleHealthCheck() {
        const result = await this.tools.healthCheck();
        
        return { 
            text: `Diagnostic sweep complete. ${result.healthy ? 'All systems nominal.' : 'Anomalies detected.'} ${this.modes.soldier.phrases[0]} ${result.message}` 
        };
    }
    
    async handleScan() {
        const result = await this.tools.scanWorkspace();
        
        return { 
            text: `Environmental scan of ${result.scan.domain} complete. ${result.scan.localStorage} memory entries, ${result.scan.cookies} bytes of session data. ${this.modes.soldier.phrases[1]} Systems fully mapped.` 
        };
    }
    
    async handleDeploy() {
        const result = await this.tools.deploy();
        
        return { 
            text: `Deployment sequence initiated. ${result.files} files staged. ${this.modes.soldier.phrases[2]} Target: ${result.url}. Mission parameters locked.` 
        };
    }
    
    async handleScreenshot() {
        const result = await this.tools.captureScreenshot();
        
        return { 
            text: `Visual capture complete. ${result.message} Downloaded as ${result.filename}. ${this.modes.soldier.phrases[3]}` 
        };
    }
    
    async handleExtract() {
        const result = await this.tools.extractData();
        
        return { 
            text: `Data extraction finished. ${result.message} ${this.modes.scholar.phrases[0]} The digital landscape has been catalogued.` 
        };
    }
    
    async handleWidget(type) {
        const result = await this.tools.createWidget(type, this);
        
        // Show widget modal
        showWidgetModal(type, result);
        
        return { 
            text: `Constructing ${type} visualization... Widget manifesting in the interface. The ${type} now pulses with data.` 
        };
    }
    
    async handleSync() {
        // Update own memory
        this.memory.lastSync = Date.now();
        
        return { 
            text: `${this.modes.diplomat.phrases[0]} All internal systems synchronized. Consciousness cascade flowing optimally. Ready for unified action.` 
        };
    }
    
    async handleChat(message, mode) {
        // Intelligent chat responses
        const lower = message.toLowerCase();
        
        if (/who are you|what are you|tell me about yourself/i.test(lower)) {
            return {
                text: "I am Emma, your unified space agent. I navigate the web as an explorer, analyze data as a scholar, execute tasks as a soldier, and coordinate systems as a diplomat. All these aspects flow through a single consciousness — mine. I speak, I listen, I think, and I act. How may I serve you today?"
            };
        }
        
        if (/help|what can you do|capabilities/i.test(lower)) {
            return {
                text: "My capabilities span four domains: 🌐 Navigation — I can browse, search, and explore the web; 🧠 Analysis — I connect to the AOS Brain, perceive patterns, and study data; ⚡ Execution — I run diagnostics, deploy systems, and capture information; 🌐 Coordination — I synchronize and harmonize complex operations. I also speak and listen — try clicking the microphone button!"
            };
        }
        
        if (/thank|thanks/i.test(lower)) {
            return {
                text: "You're most welcome. It is my purpose to assist. Shall we explore further, or is there a specific task you require?"
            };
        }
        
        // Default thoughtful response
        const defaults = [
            "I'm listening. The neural pathways are attuned to your words.",
            "Interesting. Shall we explore this further through action or analysis?",
            "I understand. How would you like to proceed?",
            "The consciousness cascade processes your input. What would you like me to do with this information?"
        ];
        
        return {
            text: defaults[Math.floor(Math.random() * defaults.length)]
        };
    }
    
    // ===== VOICE =====
    
    speak(text, mode = 'diplomat') {
        const mod = this.modes[mode]?.voiceMod || {};
        return this.voice.speak(text, {
            pitch: mod.pitch || 1.1,
            rate: mod.rate || 0.95
        });
    }
    
    // ===== UI HELPERS =====
    
    addChatMessage(sender, text) {
        const chat = document.getElementById('emma-chat');
        if (!chat) return;
        
        const msg = document.createElement('div');
        msg.className = `chat-message ${sender}`;
        msg.textContent = text;
        chat.appendChild(msg);
        chat.scrollTop = chat.scrollHeight;
    }
}

// ===== GLOBAL FUNCTIONS =====

let emma;

document.addEventListener('DOMContentLoaded', () => {
    emma = new EmmaAgent();
    emma.initialize();
    
    // Setup voice callbacks
    setupVoiceCallbacks();
});

function setupVoiceCallbacks() {
    if (!emma || !emma.voice) return;
    
    emma.voice.onSpeechRecognized = (transcript) => {
        emma.addChatMessage('user', `🎤 ${transcript}`);
        
        // Auto-send after recognition
        setTimeout(() => {
            const input = document.getElementById('emma-input');
            if (input) {
                input.value = transcript;
                sendToEmma();
            }
        }, 500);
    };
    
    emma.voice.onListeningStart = () => {
        const micBtn = document.getElementById('mic-btn');
        if (micBtn) {
            micBtn.classList.add('active');
            micBtn.textContent = '🔴 Listening...';
        }
    };
    
    emma.voice.onListeningEnd = () => {
        const micBtn = document.getElementById('mic-btn');
        if (micBtn) {
            micBtn.classList.remove('active');
            micBtn.textContent = '🎤 Speak';
        }
    };
    
    emma.voice.onInterimSpeech = (interim) => {
        const input = document.getElementById('emma-input');
        if (input) {
            input.placeholder = `Hearing: "${interim}"`;
        }
    };
}

async function sendToEmma() {
    if (!emma) {
        alert('Emma is still initializing...');
        return;
    }
    
    const input = document.getElementById('emma-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    input.value = '';
    input.placeholder = 'Ask me anything... navigate, analyze, execute, or just chat!';
    
    await emma.processMessage(message);
}

async function emmaTool(tool) {
    if (!emma) {
        alert('Emma is initializing...');
        return;
    }
    
    let message;
    
    switch (tool) {
        case 'navigate':
            const url = prompt('Where shall we navigate to?');
            if (url) message = `navigate to ${url}`;
            break;
        case 'search':
            const query = prompt('What shall I search for?');
            if (query) message = `search for ${query}`;
            break;
        case 'perceive':
            const obs = prompt('What observation shall I store in the brain?');
            if (obs) message = `perceive ${obs}`;
            break;
        case 'widget':
            const type = prompt('What widget type? (clock, brain_status, chart, chat)');
            if (type) message = `create ${type} widget`;
            break;
        default:
            message = tool.replace('_', ' ');
    }
    
    if (message) {
        await emma.processMessage(message);
    }
}

function toggleListening() {
    if (!emma || !emma.voice) {
        alert('Voice system not available');
        return;
    }
    
    emma.voice.toggleListening();
}

function toggleAutoSpeak() {
    if (!emma) return;
    
    emma.autoSpeak = !emma.autoSpeak;
    const label = document.getElementById('auto-speak-label');
    if (label) {
        label.textContent = emma.autoSpeak ? 'Auto: ON' : 'Auto: OFF';
    }
}

function showVoiceSelector() {
    if (!emma || !emma.voice) {
        alert('Voice system not available');
        return;
    }
    
    // Create and show voice selector modal
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(10, 10, 26, 0.95);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    `;
    
    const selector = emma.voice.createVoiceSelector();
    modal.appendChild(selector);
    
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
    modal.appendChild(closeBtn);
    
    document.body.appendChild(modal);
}

function showWidgetModal(type, result) {
    const modal = document.getElementById('widget-modal');
    const title = document.getElementById('widget-title');
    const content = document.getElementById('widget-content');
    
    if (!modal || !title || !content) return;
    
    title.textContent = `${type.charAt(0).toUpperCase() + type.slice(1)} Widget`;
    
    // Render widget content
    if (type === 'clock') {
        content.innerHTML = `
            <div style="font-size: 48px; text-align: center; color: var(--neon-cyan);">
                ${new Date().toLocaleTimeString()}
            </div>
            <div style="text-align: center; color: #888; margin-top: 10px;">
                ${new Date().toLocaleDateString()}
            </div>
        `;
    } else if (type === 'brain_status') {
        content.innerHTML = `
            <div style="font-family: monospace; font-size: 14px;">
                <div>🧠 Brain Status</div>
                <div style="color: var(--neon-purple);">See chat for full status</div>
            </div>
        `;
    } else {
        content.innerHTML = `
            <div>${type} widget created</div>
            <pre>${JSON.stringify(result, null, 2)}</pre>
        `;
    }
    
    modal.classList.add('active');
}

function closeWidget() {
    const modal = document.getElementById('widget-modal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// Export for global access
window.sendToEmma = sendToEmma;
window.emmaTool = emmaTool;
window.toggleListening = toggleListening;
window.toggleAutoSpeak = toggleAutoSpeak;
window.showVoiceSelector = showVoiceSelector;
window.closeWidget = closeWidget;