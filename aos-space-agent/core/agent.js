/**
 * AOS Space Agent Core Runtime
 * Browser-first JavaScript agent with socket bridge to AOS Brain v4.5
 * Based on Space Agent architecture (space-agent.ai / agent-zero.ai)
 */

class AOSSpaceAgent {
    constructor(config = {}) {
        this.id = config.id || `agent_${Date.now()}`;
        this.name = config.name || 'AOS Agent';
        this.role = config.role || 'general'; // navigator, analyst, executor, coordinator
        this.brainSocketUrl = config.brainSocket || '/brain';
        
        // Load personality if available
        this.personality = null;
        if (typeof AgentPersonalities !== 'undefined' && AgentPersonalities[this.role]) {
            this.personality = AgentPersonalities[this.role];
            this.name = this.personality.name;
            console.log(`[AOS Space Agent] Personality loaded: ${this.personality.name} (${this.personality.personality})`);
        }
        
        // Agent state
        this.memory = {
            shortTerm: [], // Last 10 messages
            longTerm: new Map(), // Key-value persistent
            skills: new Map() // Loaded skills
        };
        
        this.spaces = new Map(); // Widget instances
        this.activeSpace = null;
        this.messageHistory = [];
        
        // Connection state
        this.brainConnected = false;
        this.pendingMessages = [];
        
        // Tool registry
        this.tools = new Map();
        this.registerCoreTools();
        
        // Initialize functional tools
        if (typeof AgentTools !== 'undefined') {
            this.toolsImpl = new AgentTools(this);
        }
        
        console.log(`[AOS Space Agent] Initialized: ${this.name} (${this.id})`);
        
        // Speak greeting if personality loaded
        if (this.personality && typeof window !== 'undefined') {
            setTimeout(() => {
                const greeting = this.personality.getGreeting();
                console.log(`[${this.name}] ${greeting}`);
            }, 100);
        }
    }
    
    registerCoreTools() {
        // Core agent tools
        this.tools.set('navigate', this.toolNavigate.bind(this));
        this.tools.set('create_widget', this.toolCreateWidget.bind(this));
        this.tools.set('modify_widget', this.toolModifyWidget.bind(this));
        this.tools.set('brain_perceive', this.toolBrainPerceive.bind(this));
        this.tools.set('brain_status', this.toolBrainStatus.bind(this));
        this.tools.set('search_memory', this.toolSearchMemory.bind(this));
        this.tools.set('execute_skill', this.toolExecuteSkill.bind(this));
    }
    
    // ========== BRAIN INTEGRATION ==========
    
    async connectToBrain() {
        try {
            const response = await fetch(`${this.brainSocketUrl}/api/status`);
            if (response.ok) {
                const data = await response.json();
                this.brainConnected = true;
                console.log(`[Agent ${this.id}] Brain connected:`, data.brain?.version);
                return true;
            }
        } catch (e) {
            console.log(`[Agent ${this.id}] Brain not available, standalone mode`);
            this.brainConnected = false;
        }
        return false;
    }
    
    async perceiveForBrain(observation, intensity = 0.8) {
        if (!this.brainConnected) {
            // Store locally
            this.memory.shortTerm.push({
                type: 'perception',
                content: observation,
                intensity,
                timestamp: Date.now()
            });
            if (this.memory.shortTerm.length > 10) {
                this.memory.shortTerm.shift();
            }
            return { perceived: true, local: true };
        }
        
        try {
            const response = await fetch(`${this.brainSocketUrl}/api/command`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    cmd: 'perceive',
                    params: { observation, intensity }
                })
            });
            return await response.json();
        } catch (e) {
            return { perceived: false, error: e.message };
        }
    }
    
    async getBrainStatus() {
        if (!this.brainConnected) {
            return { brain: 'offline', agent_memory: this.memory.shortTerm.length };
        }
        
        try {
            const response = await fetch(`${this.brainSocketUrl}/api/status`);
            return await response.json();
        } catch (e) {
            return { brain: 'error', message: e.message };
        }
    }
    
    // ========== SPACE/WIDGET SYSTEM ==========
    
    createSpace(name, config = {}) {
        const spaceId = `space_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        const space = {
            id: spaceId,
            name,
            widgets: new Map(),
            layout: config.layout || 'grid',
            created: Date.now(),
            modified: Date.now()
        };
        
        this.spaces.set(spaceId, space);
        this.activeSpace = spaceId;
        
        console.log(`[Agent ${this.id}] Created space: ${name} (${spaceId})`);
        return space;
    }
    
    createWidget(spaceId, type, config = {}) {
        const space = this.spaces.get(spaceId);
        if (!space) return null;
        
        const widgetId = `widget_${Date.now()}`;
        
        const widget = {
            id: widgetId,
            type,
            config,
            position: config.position || { x: 0, y: 0 },
            size: config.size || { w: 200, h: 150 },
            renderer: this.getWidgetRenderer(type),
            data: config.data || {},
            created: Date.now()
        };
        
        space.widgets.set(widgetId, widget);
        space.modified = Date.now();
        
        // Perceive widget creation
        this.perceiveForBrain(`Created ${type} widget in space ${space.name}`, 0.7);
        
        return widget;
    }
    
    getWidgetRenderer(type) {
        const renderers = {
            'clock': (ctx, data) => {
                const now = new Date();
                return `
                    <div class="widget-clock">
                        <div class="time">${now.toLocaleTimeString()}</div>
                        <div class="date">${now.toLocaleDateString()}</div>
                    </div>
                `;
            },
            'brain_status': async (ctx, data) => {
                const status = await ctx.getBrainStatus();
                const b = status.brain;
                if (!b) return '<div class="widget-error">Brain offline</div>';
                
                return `
                    <div class="widget-brain-status">
                        <div class="tick">Tick: ${b.tick || 'N/A'}</div>
                        <div class="phase">Phase: ${b.phase || 'unknown'}</div>
                        <div class="signal">Signal: ${Math.round((b.signal_quality_20avg || 0) * 100)}%</div>
                        <div class="layers">
                            Con: ${b.consciousness?.conscious?.active_items || 0}/10 |
                            Sub: ${b.consciousness?.subconscious?.active_items || 0}/100 |
                            Unc: ${b.consciousness?.unconscious?.active_items || 0}/2000
                        </div>
                    </div>
                `;
            },
            'chat': (ctx, data) => {
                const messages = data.messages || ctx.memory.shortTerm.slice(-5);
                return `
                    <div class="widget-chat">
                        ${messages.map(m => `
                            <div class="message ${m.type}">
                                <span class="content">${m.content}</span>
                            </div>
                        `).join('')}
                    </div>
                `;
            },
            'code_editor': (ctx, data) => {
                return `
                    <div class="widget-code">
                        <pre><code>${data.code || '// Type code here...'}</code></pre>
                    </div>
                `;
            },
            'chart': (ctx, data) => {
                // Simple SVG bar chart
                const values = data.values || [30, 50, 80, 40, 60];
                const max = Math.max(...values);
                const bars = values.map((v, i) => `
                    <rect x="${i * 25 + 10}" y="${100 - (v/max * 80)}" 
                          width="20" height="${v/max * 80}" 
                          fill="#00f3ff" />
                `).join('');
                
                return `
                    <div class="widget-chart">
                        <svg viewBox="0 0 130 100">${bars}</svg>
                    </div>
                `;
            }
        };
        
        return renderers[type] || ((ctx, data) => `<div class="widget-unknown">Unknown: ${type}</div>`);
    }
    
    // ========== MESSAGE PROCESSING ==========
    
    async processMessage(message) {
        // Store in history
        this.messageHistory.push({
            role: 'user',
            content: message,
            timestamp: Date.now()
        });
        
        // Perceive in brain
        await this.perceiveForBrain(`User message: ${message}`, 0.85);
        
        // Parse for tool calls
        const toolCall = this.parseToolCall(message);
        
        if (toolCall) {
            const result = await this.executeTool(toolCall.tool, toolCall.params);
            
            // Generate personality response for tool execution
            let responseText;
            if (this.personality) {
                const personalityResponse = this.personality.generateResponse(message, { tool: toolCall.tool, result });
                responseText = personalityResponse.text;
                
                // Speak the response
                if (personalityResponse.speak) {
                    this.personality.speak(responseText);
                }
            } else {
                responseText = `Executed ${toolCall.tool}: ${JSON.stringify(result).slice(0, 100)}`;
            }
            
            return {
                type: 'tool_result',
                tool: toolCall.tool,
                text: responseText,
                result
            };
        }
        
        // Generate response based on role (with personality)
        let response;
        if (this.personality) {
            const personalityResponse = this.personality.generateResponse(message, {});
            response = personalityResponse.text;
            
            // Speak!
            if (personalityResponse.speak) {
                this.personality.speak(response);
            }
        } else {
            response = this.generateResponse(message);
        }
        
        this.messageHistory.push({
            role: 'assistant',
            content: response,
            timestamp: Date.now()
        });
        
        return {
            type: 'text',
            content: response
        };
    }
    
    parseToolCall(message) {
        // Parse natural language tool calls
        // Format: "navigate to google.com" or "create clock widget"
        
        const patterns = [
            { pattern: /navigate to (.+)/i, tool: 'navigate', paramKey: 'url' },
            { pattern: /create (\w+) widget/i, tool: 'create_widget', paramKey: 'type' },
            { pattern: /brain status/i, tool: 'brain_status' },
            { pattern: /show brain/i, tool: 'brain_status' },
            { pattern: /open (.+)/i, tool: 'navigate', paramKey: 'url' }
        ];
        
        for (const { pattern, tool, paramKey } of patterns) {
            const match = message.match(pattern);
            if (match) {
                const params = paramKey ? { [paramKey]: match[1] } : {};
                return { tool, params };
            }
        }
        
        return null;
    }
    
    async executeTool(toolName, params) {
        const tool = this.tools.get(toolName);
        if (!tool) {
            return { error: `Unknown tool: ${toolName}` };
        }
        
        try {
            return await tool(params);
        } catch (e) {
            return { error: e.message };
        }
    }
    
    // ========== TOOL IMPLEMENTATIONS (Using Functional Tools) ==========
    
    async toolNavigate(params) {
        // Use functional tools if available
        if (this.toolsImpl) {
            return await this.toolsImpl.navigate(params.url);
        }
        
        // Fallback to simple implementation
        let url = params.url;
        if (!url.startsWith('http')) {
            url = 'https://' + url;
        }
        
        if (typeof window !== 'undefined') {
            window.open(url, '_blank');
        }
        
        await this.perceiveForBrain(`Navigated to ${url}`, 0.7);
        
        return { navigated: true, url };
    }
    
    async toolCreateWidget(params) {
        const type = params.type;
        const spaceId = this.activeSpace || this.createSpace('Auto Space').id;
        
        const widget = this.createWidget(spaceId, type, {
            data: params.data || {}
        });
        
        return { 
            created: true, 
            widgetId: widget.id, 
            type,
            spaceId
        };
    }
    
    async toolModifyWidget(params) {
        const { widgetId, modifications } = params;
        // Implementation would modify existing widget
        return { modified: true, widgetId };
    }
    
    async toolBrainPerceive(params) {
        const { observation, intensity = 0.8 } = params;
        return await this.perceiveForBrain(observation, intensity);
    }
    
    async toolBrainStatus() {
        // Use functional tools if available
        if (this.toolsImpl) {
            return await this.toolsImpl.brainStatus();
        }
        return await this.getBrainStatus();
    }
    
    async toolSearchMemory(params) {
        const { query } = params;
        const results = this.memory.shortTerm.filter(m => 
            m.content && m.content.includes(query)
        );
        return { results, count: results.length };
    }
    
    async toolExecuteSkill(params) {
        const { skillName, args } = params;
        // Skill execution would load from skills/ directory
        return { executed: true, skill: skillName, args };
    }
    
    // ========== RESPONSE GENERATION ==========
    
    generateResponse(message) {
        const lower = message.toLowerCase();
        
        // Role-based responses
        if (this.role === 'navigator') {
            if (lower.includes('go') || lower.includes('open')) {
                return "I'll open that for you. Navigate to where?";
            }
            return "I can help you navigate the web. Try: 'go to example.com' or 'search for...'";
        }
        
        if (this.role === 'analyst') {
            if (lower.includes('brain')) {
                return "Connected to AOS Brain v4.5. Checking consciousness cascade...";
            }
            if (lower.includes('status')) {
                return "I'll pull the current system status from the brain.";
            }
            return "I analyze data and connect to the brain. Try 'brain status' or 'create chart widget'.";
        }
        
        if (this.role === 'executor') {
            if (lower.includes('run') || lower.includes('execute')) {
                return "Ready to execute. What command or task?";
            }
            return "I execute tasks and commands. Try 'run health check' or 'deploy'.";
        }
        
        // General response
        return `I'm ${this.name}, an AOS Space Agent. I can navigate, analyze, create widgets, and connect to the brain. What would you like to do?`;
    }
    
    // ========== SKILL SYSTEM ==========
    
    async loadSkill(skillName) {
        try {
            const response = await fetch(`/aos-space-agent/skills/${skillName}.json`);
            if (response.ok) {
                const skill = await response.json();
                this.memory.skills.set(skillName, skill);
                return skill;
            }
        } catch (e) {
            console.log(`[Agent ${this.id}] Failed to load skill: ${skillName}`);
        }
        return null;
    }
    
    // ========== PERSISTENCE ==========
    
    exportState() {
        return {
            id: this.id,
            name: this.name,
            role: this.role,
            memory: {
                shortTerm: this.memory.shortTerm,
                longTerm: Array.from(this.memory.longTerm.entries())
            },
            spaces: Array.from(this.spaces.entries()).map(([id, space]) => ({
                ...space,
                widgets: Array.from(space.widgets.entries())
            })),
            activeSpace: this.activeSpace,
            messageHistory: this.messageHistory.slice(-50) // Last 50
        };
    }
    
    importState(state) {
        this.id = state.id || this.id;
        this.name = state.name || this.name;
        this.memory.shortTerm = state.memory?.shortTerm || [];
        this.memory.longTerm = new Map(state.memory?.longTerm || []);
        this.spaces = new Map(state.spaces?.map(s => [s.id, {
            ...s,
            widgets: new Map(s.widgets || [])
        }]) || []);
        this.activeSpace = state.activeSpace;
        this.messageHistory = state.messageHistory || [];
    }
}

// Export for use
if (typeof window !== 'undefined') {
    window.AOSSpaceAgent = AOSSpaceAgent;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AOSSpaceAgent;
}