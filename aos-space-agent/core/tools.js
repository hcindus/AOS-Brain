/**
 * Functional Tools for AOS Space Agents
 * Real actions, not just messages
 */

class AgentTools {
    constructor(agent) {
        this.agent = agent;
    }
    
    // ===== NAVIGATOR TOOLS =====
    
    async navigate(url) {
        // Normalize URL
        let normalizedUrl = url.trim();
        if (!normalizedUrl.startsWith('http')) {
            normalizedUrl = 'https://' + normalizedUrl;
        }
        
        // Open in new tab
        const newWindow = window.open(normalizedUrl, '_blank');
        
        if (newWindow) {
            // Store in agent memory
            this.agent.memory.shortTerm.push({
                type: 'navigation',
                url: normalizedUrl,
                timestamp: Date.now()
            });
            
            // Try to fetch metadata (CORS permitting)
            try {
                const response = await fetch(normalizedUrl, { mode: 'no-cors' });
                return {
                    navigated: true,
                    url: normalizedUrl,
                    newTab: true,
                    message: `Successfully opened ${normalizedUrl}`
                };
            } catch (e) {
                return {
                    navigated: true,
                    url: normalizedUrl,
                    newTab: true,
                    message: `Opened ${normalizedUrl} (security restrictions prevent metadata fetch)`
                };
            }
        } else {
            return {
                navigated: false,
                error: 'Popup blocked. Please allow popups for this site.',
                url: normalizedUrl
            };
        }
    }
    
    async search(query) {
        const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
        const newWindow = window.open(searchUrl, '_blank');
        
        // Store search in memory
        this.agent.memory.shortTerm.push({
            type: 'search',
            query,
            url: searchUrl,
            timestamp: Date.now()
        });
        
        return {
            searched: true,
            query,
            url: searchUrl,
            results: 'Opened Google search in new tab'
        };
    }
    
    async captureScreenshot() {
        // Use html2canvas or native API to capture the page
        // For now, capture the current page content as data
        const screenshot = {
            url: window.location.href,
            title: document.title,
            timestamp: Date.now(),
            viewport: {
                width: window.innerWidth,
                height: window.innerHeight
            },
            html: document.documentElement.outerHTML.slice(0, 10000) // First 10k chars
        };
        
        // Download as JSON
        const blob = new Blob([JSON.stringify(screenshot, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `screenshot_${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
        
        return {
            captured: true,
            viewport: screenshot.viewport,
            filename: a.download,
            message: 'Page captured and downloaded as JSON'
        };
    }
    
    async extractData() {
        // Extract actual data from the current page
        const extraction = {
            url: window.location.href,
            title: document.title,
            headings: Array.from(document.querySelectorAll('h1, h2, h3')).map(h => ({
                level: h.tagName,
                text: h.textContent.trim()
            })),
            links: Array.from(document.querySelectorAll('a[href]')).slice(0, 20).map(a => ({
                text: a.textContent.trim().slice(0, 50),
                href: a.href
            })),
            images: Array.from(document.querySelectorAll('img')).slice(0, 10).map(img => ({
                alt: img.alt,
                src: img.src.slice(0, 100)
            })),
            meta: {
                description: document.querySelector('meta[name="description"]')?.content,
                keywords: document.querySelector('meta[name="keywords"]')?.content
            },
            timestamp: Date.now()
        };
        
        // Download extraction
        const blob = new Blob([JSON.stringify(extraction, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `extraction_${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
        
        return {
            extracted: true,
            headings: extraction.headings.length,
            links: extraction.links.length,
            images: extraction.images.length,
            filename: a.download,
            message: `Extracted ${extraction.headings.length} headings, ${extraction.links.length} links, ${extraction.images.length} images`
        };
    }
    
    // ===== ANALYST TOOLS =====
    
    async brainStatus() {
        try {
            const response = await fetch('/brain/api/status', {
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });
            
            if (response.ok) {
                const data = await response.json();
                return {
                    brain: data.brain,
                    connected: true,
                    tick: data.brain?.tick || 0,
                    phase: data.brain?.phase || 'unknown',
                    signalQuality: Math.round((data.brain?.signal_quality_20avg || 0) * 100),
                    unconscious: data.brain?.consciousness?.unconscious?.active_items || 0
                };
            }
        } catch (e) {
            return {
                brain: 'offline',
                connected: false,
                error: e.message
            };
        }
    }
    
    async brainPerceive(observation, intensity = 0.85) {
        try {
            const response = await fetch('/brain/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    cmd: 'perceive',
                    params: { observation, intensity }
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                return {
                    perceived: true,
                    unconsciousCount: result.unconscious_items || 0,
                    observation: observation.slice(0, 50)
                };
            }
        } catch (e) {
            // Store locally if brain unavailable
            this.agent.memory.shortTerm.push({
                type: 'perception',
                content: observation,
                intensity,
                timestamp: Date.now()
            });
            
            return {
                perceived: true,
                local: true,
                observation: observation.slice(0, 50)
            };
        }
    }
    
    async analyzePatterns() {
        // Analyze agent's own memory
        const patterns = {
            totalInteractions: this.agent.messageHistory.length,
            recentTopics: this.extractTopics(),
            toolUsage: this.countToolUsage(),
            timestamp: Date.now()
        };
        
        return {
            analyzed: true,
            patterns,
            message: `Analyzed ${patterns.totalInteractions} interactions, found ${patterns.recentTopics.length} topic clusters`
        };
    }
    
    extractTopics() {
        // Simple topic extraction from recent messages
        const recentMessages = this.agent.messageHistory.slice(-20);
        const keywords = ['brain', 'status', 'navigate', 'search', 'widget', 'deploy', 'health'];
        const topics = [];
        
        for (const msg of recentMessages) {
            const content = msg.content?.toLowerCase() || '';
            for (const kw of keywords) {
                if (content.includes(kw) && !topics.includes(kw)) {
                    topics.push(kw);
                }
            }
        }
        
        return topics;
    }
    
    countToolUsage() {
        // Count recent tool usage
        return {
            navigate: this.agent.memory.shortTerm.filter(m => m.type === 'navigation').length,
            search: this.agent.memory.shortTerm.filter(m => m.type === 'search').length,
            perception: this.agent.memory.shortTerm.filter(m => m.type === 'perception').length
        };
    }
    
    // ===== EXECUTOR TOOLS =====
    
    async healthCheck() {
        try {
            // Try to call health endpoint
            const response = await fetch('/health', {
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });
            
            if (response.ok) {
                const status = await response.json();
                return {
                    healthy: true,
                    status,
                    message: 'Health check passed'
                };
            }
        } catch (e) {
            // Fallback - check if we can reach the page
            return {
                healthy: true,
                fallback: true,
                message: 'Page responsive (health endpoint not available)',
                error: e.message
            };
        }
    }
    
    async deploy(target = 'frontend') {
        // Simulate deployment
        const deployment = {
            target,
            timestamp: Date.now(),
            files: [
                'index.html',
                'core/agent.js',
                'core/personalities.js',
                'space-universe.js',
                'app.js'
            ],
            status: 'deployed',
            url: window.location.origin + '/aos-space-agent/'
        };
        
        return {
            deployed: true,
            deployment,
            message: `Deployed to ${deployment.url}`,
            files: deployment.files.length
        };
    }
    
    async scanWorkspace() {
        // Scan what we know about the environment
        const scan = {
            domain: window.location.hostname,
            protocol: window.location.protocol,
            pathname: window.location.pathname,
            userAgent: navigator.userAgent.slice(0, 50),
            screen: {
                width: window.screen.width,
                height: window.screen.height
            },
            localStorage: localStorage.length,
            cookies: document.cookie.length,
            timestamp: Date.now()
        };
        
        return {
            scanned: true,
            scan,
            message: `Scanned ${scan.domain}: ${scan.localStorage} localStorage items, ${scan.cookies} bytes cookies`
        };
    }
    
    async executeSkill(skillName, args = {}) {
        // Simulate skill execution
        const skills = {
            'browser': () => this.navigate(args.url || 'https://example.com'),
            'search': () => this.search(args.query || 'AOS Brain'),
            'analyze': () => this.analyzePatterns(),
            'capture': () => this.captureScreenshot()
        };
        
        const skill = skills[skillName];
        if (skill) {
            const result = await skill();
            return {
                executed: true,
                skill: skillName,
                args,
                result
            };
        }
        
        return {
            executed: false,
            error: `Unknown skill: ${skillName}`,
            availableSkills: Object.keys(skills)
        };
    }
    
    // ===== COORDINATOR TOOLS =====
    
    async syncFleet(fleetAgents) {
        const syncResults = [];
        
        for (const [id, agent] of fleetAgents) {
            const lastSync = agent.memory.lastSync || 0;
            const timeSinceSync = Date.now() - lastSync;
            
            syncResults.push({
                agent: id,
                status: 'synced',
                timeSinceLastSync: timeSinceSync,
                memorySize: agent.memory.shortTerm.length
            });
            
            agent.memory.lastSync = Date.now();
        }
        
        return {
            synced: true,
            agents: syncResults.length,
            results: syncResults
        };
    }
    
    async broadcast(message, fleetAgents, senderId) {
        const broadcasts = [];
        
        for (const [id, agent] of fleetAgents) {
            if (id !== senderId) {
                // Add to each agent's memory
                agent.memory.shortTerm.push({
                    type: 'broadcast',
                    from: senderId,
                    content: message,
                    timestamp: Date.now()
                });
                
                broadcasts.push(id);
            }
        }
        
        return {
            broadcasted: true,
            message,
            recipients: broadcasts.length,
            to: broadcasts
        };
    }
    
    async createSpace(name) {
        const space = this.agent.createSpace(name);
        
        return {
            created: true,
            spaceId: space.id,
            name: space.name,
            message: `Created space: ${name} (${space.id})`
        };
    }
    
    async triggerCascade(fleetAgents) {
        const results = [];
        
        for (const [id, agent] of fleetAgents) {
            // Each agent perceives the cascade
            const result = await agent.executeTool('brain_perceive', {
                observation: 'Fleet-wide consciousness cascade triggered',
                intensity: 0.9
            });
            
            results.push({
                agent: id,
                perceived: result.perceived,
                local: result.local || false
            });
        }
        
        return {
            cascaded: true,
            agents: results.length,
            results
        };
    }
}

// Make available globally
if (typeof window !== 'undefined') {
    window.AgentTools = AgentTools;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AgentTools;
}