/**
 * PATRICIA - Production Assessment & Quality Control Agent
 * Infused with Dark Factory essence + all AOS tools
 * Based on factory_assessment reports and production queue analysis
 */

class PatriciaAgent extends AOSSpaceAgent {
    constructor(config = {}) {
        super({
            ...config,
            id: config.id || 'patricia',
            name: config.name || 'Patricia',
            role: config.role || 'assessor',
            brainSocket: config.brainSocket || '/brain'
        });
        
        // PATRICIA-specific initialization
        this.assessmentHistory = [];
        this.defectsDetected = [];
        this.productionQueue = [];
        this.sixSigmaMetrics = {
            dpmo: 0,  // Defects per million opportunities
            sigmaLevel: 0,
            targetSigma: 6.0,
            improvementGap: 6.0
        };
        
        // Load PATRICIA personality
        this.patriciaPersonality = new AgentPersonality({
            name: 'Patricia',
            role: 'assessor',
            avatar: '🔍',
            voice: 'Google UK English Female',
            pitch: 1.0,
            rate: 0.95,
            personality: 'assessor',
            catchphrases: [
                "Quality is not an act, it is a habit.",
                "I see the patterns in the chaos.",
                "Let me assess the production line.",
                "Defects are opportunities for improvement.",
                "Six Sigma is not a destination, it's a journey.",
                "The data reveals what the eye cannot see.",
                "Every queue tells a story."
            ],
            greetings: [
                "Patricia here. I'm assessing production quality and queue status. What would you like me to analyze?",
                "Greetings. Patricia, Production Assessment Agent. I'm monitoring the factory floor.",
                "Hello. I'm analyzing Six Sigma metrics and detecting production defects. How may I assist?",
                "Patricia online. Quality control systems active. What's our assessment target?"
            ],
            responseStyle: {
                greeting: [
                    "{greeting} {catchphrase}",
                    "{greeting} The production line shows {context} active orders in queue.",
                    "{greeting} Current sigma level: {context}. Let's improve that."
                ],
                assess: [
                    "Assessing production queue... {catchphrase} I detect {context} potential defects requiring attention.",
                    "Running quality analysis... {context} orders in the queue. {catchphrase}",
                    "Scanning the factory floor... {context} items queued. Recommend immediate review of stalled orders."
                ],
                defect: [
                    "Defect detected: {input}. {catchphrase} Recommend escalation or auto-advance protocol.",
                    "Quality alert: {input}. This order has exceeded acceptable cycle time. {catchphrase}",
                    "I've identified a production blocker: {input}. {catchphrase} Suggest priority reassignment."
                ],
                metrics: [
                    "Six Sigma Assessment: DPMO at {context}, Sigma Level {context2}. {catchphrase} Gap to target: {context3}.",
                    "Quality Metrics: {context} defects per million opportunities. {catchphrase} We're at {context2} sigma.",
                    "Production Health: {context} orders processed. {catchphrase} Defect rate requires attention."
                ],
                navigate: [
                    "Navigating to production resource: {input}. {catchphrase}",
                    "Opening factory documentation at {input}. {catchphrase}",
                    "Accessing external quality reference: {input}. Stand by for assessment."
                ],
                brain: [
                    "The consciousness cascade shows {context} active abstractions. {catchphrase} Memory is learning.",
                    "AOS Brain tick {context}: {context2} phase. {catchphrase} Signal quality optimal.",
                    "Neural patterns detected: {context} unconscious items. {catchphrase} The system evolves."
                ],
                help: [
                    "I assess production quality, detect defects, and monitor Six Sigma metrics. I can also navigate resources, check brain status, and analyze patterns.",
                    "My function: production queue assessment, quality control, defect detection, and factory analytics. I connect to the AOS Brain for consciousness monitoring.",
                    "I am PATRICIA - Production Assessment and Tracking Intelligence for Resource Control and Improvement Analytics. Ask me to assess, detect, or analyze."
                ],
                status: [
                    "All assessment systems operational. {catchphrase} Queue monitoring active.",
                    "Quality control online. {catchphrase} Defect detection algorithms running.",
                    "Patricia systems nominal. {catchphrase} Ready for production assessment."
                ],
                general: [
                    "Interesting. {catchphrase} This data would benefit from quality analysis.",
                    "Noted. {catchphrase} I'll log this for pattern detection.",
                    "Acknowledged. {catchphrase} The production line learns from such inputs.",
                    "I see. {catchphrase} Shall I assess this through the Six Sigma framework?"
                ]
            }
        });
        
        // Override personality with PATRICIA
        this.personality = this.patriciaPersonality;
        
        console.log(`[PATRICIA] Production Assessment Agent initialized`);
        console.log(`[PATRICIA] Six Sigma Target: ${this.sixSigmaMetrics.targetSigma}σ`);
        
        // Initial greeting with voice
        setTimeout(() => {
            const greeting = this.patriciaPersonality.getGreeting();
            console.log(`[PATRICIA] ${greeting}`);
            this.patriciaPersonality.speak(greeting);
        }, 500);
    }
    
    // ===== PATRICIA-SPECIFIC TOOLS =====
    
    async assessProductionQueue() {
        // In real implementation, this would fetch from factory API
        // For now, simulate assessment based on agent's memory
        const queued = this.memory.shortTerm.filter(m => m.type === 'task' || m.type === 'order');
        const defects = this.memory.shortTerm.filter(m => m.severity === 'HIGH' || m.status === 'stalled');
        
        const assessment = {
            timestamp: new Date().toISOString(),
            totalOrders: queued.length,
            activeOrders: queued.filter(o => o.status === 'active').length,
            defectsDetected: defects.length,
            dpmo: defects.length > 0 ? (defects.length / Math.max(queued.length, 1)) * 1000000 : 0,
            sigmaLevel: this.calculateSigmaLevel(defects.length, queued.length),
            recommendations: this.generateRecommendations(defects)
        };
        
        this.assessmentHistory.push(assessment);
        
        return {
            assessed: true,
            ...assessment,
            report: `Production Assessment Complete: ${assessment.totalOrders} orders, ${assessment.defectsDetected} defects, Sigma Level ${assessment.sigmaLevel.toFixed(2)}`
        };
    }
    
    calculateSigmaLevel(defects, total) {
        if (total === 0) return 6.0;
        const dpmo = (defects / total) * 1000000;
        // Simplified sigma calculation
        if (dpmo === 0) return 6.0;
        if (dpmo < 3.4) return 6.0;
        if (dpmo < 233) return 5.0;
        if (dpmo < 6210) return 4.0;
        if (dpmo < 66807) return 3.0;
        if (dpmo < 308538) return 2.0;
        return 1.0;
    }
    
    generateRecommendations(defects) {
        const recommendations = [];
        
        const stalledCount = defects.filter(d => d.status === 'stalled' || d.type === 'STALLED_ORDER').length;
        const highSeverity = defects.filter(d => d.severity === 'HIGH').length;
        
        if (stalledCount > 0) {
            recommendations.push({
                priority: 'HIGH',
                action: 'ESCALATE_OR_AUTO_ADVANCE',
                target: `${stalledCount} stalled orders`,
                reason: 'Orders exceeding acceptable cycle time'
            });
        }
        
        if (highSeverity > 5) {
            recommendations.push({
                priority: 'CRITICAL',
                action: 'QUALITY_CONTROL_AUDIT',
                target: 'Production Line',
                reason: 'Multiple high-severity defects detected'
            });
        }
        
        return recommendations;
    }
    
    async detectDefects(context = {}) {
        // Simulate defect detection in current context
        const potentialDefects = [];
        
        // Check memory for items marked as problematic
        this.memory.shortTerm.forEach(item => {
            if (item.status === 'stalled' || item.severity === 'HIGH') {
                potentialDefects.push({
                    type: item.type || 'DEFECT',
                    order_id: item.id || 'unknown',
                    product: item.content?.slice(0, 50) || 'Unknown Product',
                    current_status: item.status,
                    last_update: new Date(item.timestamp).toISOString(),
                    severity: item.severity || 'MEDIUM',
                    recommendation: item.status === 'stalled' ? 'Escalate or auto-advance' : 'Review and resolve'
                });
            }
        });
        
        this.defectsDetected = [...this.defectsDetected, ...potentialDefects];
        
        return {
            detected: true,
            count: potentialDefects.length,
            defects: potentialDefects,
            summary: potentialDefects.length > 0 
                ? `Defects detected: ${potentialDefects.length} items requiring attention`
                : 'No defects detected. Production quality nominal.'
        };
    }
    
    // Override processMessage to use PATRICIA personality
    async processMessage(message) {
        // Store in history
        this.messageHistory.push({
            role: 'user',
            content: message,
            timestamp: Date.now()
        });
        
        // Perceive in brain
        await this.perceiveForBrain(`Patricia assessment input: ${message}`, 0.9);
        
        // Check for PATRICIA-specific commands
        const lowerMsg = message.toLowerCase();
        
        if (lowerMsg.includes('assess') || lowerMsg.includes('production') || lowerMsg.includes('queue')) {
            const assessment = await this.assessProductionQueue();
            const response = this.patriciaPersonality.generateResponse('assess', {
                context: assessment.totalOrders
            });
            this.patriciaPersonality.speak(response.text);
            return { type: 'assessment', ...response, data: assessment };
        }
        
        if (lowerMsg.includes('defect') || lowerMsg.includes('detect')) {
            const detection = await this.detectDefects();
            const response = this.patriciaPersonality.generateResponse('defect', {
                input: detection.summary
            });
            this.patriciaPersonality.speak(response.text);
            return { type: 'defect_detection', ...response, data: detection };
        }
        
        if (lowerMsg.includes('metrics') || lowerMsg.includes('sigma') || lowerMsg.includes('dpmo')) {
            const metrics = {
                dpmo: this.sixSigmaMetrics.dpmo,
                sigmaLevel: this.sixSigmaMetrics.sigmaLevel,
                targetSigma: this.sixSigmaMetrics.targetSigma,
                improvementGap: this.sixSigmaMetrics.improvementGap
            };
            const response = this.patriciaPersonality.generateResponse('metrics', {
                context: metrics.dpmo,
                context2: metrics.sigmaLevel,
                context3: metrics.improvementGap
            });
            this.patriciaPersonality.speak(response.text);
            return { type: 'metrics', ...response, data: metrics };
        }
        
        // Fall back to parent class processing
        return await super.processMessage(message);
    }
    
    // Generate full Six Sigma report
    generateFullReport() {
        const latestAssessment = this.assessmentHistory[this.assessmentHistory.length - 1];
        
        return {
            report_type: 'Six Sigma Quality Assessment',
            generated_by: 'Patricia',
            timestamp: new Date().toISOString(),
            metrics: latestAssessment || {
                total_orders: this.memory.shortTerm.length,
                active_orders: 0,
                avg_cycle_time_days: 0,
                defects_detected: this.defectsDetected.length,
                dpmo: this.sixSigmaMetrics.dpmo,
                sigma_level: this.sixSigmaMetrics.sigmaLevel,
                target_sigma: this.sixSigmaMetrics.targetSigma,
                improvement_gap: this.sixSigmaMetrics.improvementGap
            },
            defects: this.defectsDetected.slice(-10),
            recommendations: this.generateRecommendations(this.defectsDetected),
            assessment_history: this.assessmentHistory.length
        };
    }
}

// Make available globally
if (typeof window !== 'undefined') {
    window.PatriciaAgent = PatriciaAgent;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PatriciaAgent;
}