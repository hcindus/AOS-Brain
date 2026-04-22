/**
 * AOS Space Agent Personalities & Voice System
 * Each agent has unique voice, personality, and response style
 */

class AgentPersonality {
    constructor(config) {
        this.name = config.name;
        this.role = config.role;
        this.avatar = config.avatar;
        this.voice = config.voice; // Web Speech API voice
        this.pitch = config.pitch || 1;
        this.rate = config.rate || 1;
        this.personality = config.personality;
        this.catchphrases = config.catchphrases || [];
        this.greetings = config.greetings || [];
        this.responseStyle = config.responseStyle;
        
        this.memory = {
            lastInteraction: null,
            mood: 'neutral', // excited, focused, curious, concerned
            topicsDiscussed: new Set()
        };
    }
    
    // Generate speaking response with personality
    generateResponse(input, context = {}) {
        const lowerInput = input.toLowerCase();
        
        // Determine intent
        let intent = 'general';
        if (lowerInput.includes('status') || lowerInput.includes('how')) intent = 'status';
        if (lowerInput.includes('navigate') || lowerInput.includes('go to') || lowerInput.includes('open')) intent = 'navigate';
        if (lowerInput.includes('brain') || lowerInput.includes('mind')) intent = 'brain';
        if (lowerInput.includes('help') || lowerInput.includes('?')) intent = 'help';
        if (lowerInput.includes('hello') || lowerInput.includes('hi')) intent = 'greeting';
        
        // Generate based on personality + intent
        const response = this.craftResponse(intent, input, context);
        
        // Update memory
        this.memory.lastInteraction = Date.now();
        this.memory.topicsDiscussed.add(intent);
        
        return response;
    }
    
    craftResponse(intent, originalInput, context) {
        const responses = this.responseStyle[intent] || this.responseStyle.general;
        let template = responses[Math.floor(Math.random() * responses.length)];
        
        // Personalize template
        template = template.replace(/{input}/g, originalInput);
        template = template.replace(/{context}/g, JSON.stringify(context).slice(0, 100));
        template = template.replace(/{time}/g, new Date().toLocaleTimeString());
        template = template.replace(/{catchphrase}/g, this.getRandomCatchphrase());
        
        return {
            text: template,
            emotion: this.determineEmotion(intent),
            speak: true
        };
    }
    
    getRandomCatchphrase() {
        return this.catchphrases[Math.floor(Math.random() * this.catchphrases.length)] || '';
    }
    
    determineEmotion(intent) {
        const emotions = {
            'greeting': 'excited',
            'navigate': 'focused',
            'brain': 'curious',
            'help': 'helpful',
            'status': 'neutral',
            'general': 'neutral'
        };
        return emotions[intent] || 'neutral';
    }
    
    speak(text) {
        if (!window.speechSynthesis) {
            console.warn('[AgentPersonality] Web Speech API not available');
            return false;
        }
        
        // Cancel any current speech
        window.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.pitch = this.pitch;
        utterance.rate = this.rate;
        utterance.volume = 1;
        
        // Try to find matching voice
        const voices = window.speechSynthesis.getVoices();
        if (this.voice && voices.length > 0) {
            const matchingVoice = voices.find(v => v.name.includes(this.voice));
            if (matchingVoice) {
                utterance.voice = matchingVoice;
            }
        }
        
        window.speechSynthesis.speak(utterance);
        return true;
    }
    
    getGreeting() {
        return this.greetings[Math.floor(Math.random() * this.greetings.length)];
    }
}

// Agent Alpha - Navigator (Explorer personality)
const NavigatorAlpha = new AgentPersonality({
    name: 'Navigator Alpha',
    role: 'navigator',
    avatar: '🧭',
    voice: 'Google US English', // Male, confident
    pitch: 0.9,
    rate: 1.1,
    personality: 'explorer',
    catchphrases: [
        "Charting a course now!",
        "The digital seas await.",
        "Navigation is my passion.",
        "Full speed ahead!",
        "I've got the helm."
    ],
    greetings: [
        "Navigator Alpha, reporting for duty! Where shall we voyage today?",
        "Ahoy! Ready to explore the web?",
        "The stars are aligned. Where to, Captain?",
        "Systems online. Your navigator awaits your command."
    ],
    responseStyle: {
        greeting: [
            "{greeting} I'm here to guide you through the digital cosmos.",
            "{greeting} The web is vast — shall we explore?",
            "{greeting} {catchphrase}"
        ],
        navigate: [
            "Plotting course to {input}... {catchphrase}",
            "Navigating now. Hold tight! {catchphrase}",
            "Setting coordinates for {input}. Engaging thrusters!",
            "Destination: {input}. Charting the most efficient route..."
        ],
        search: [
            "Scanning the digital archives for '{input}'...",
            "My sensors are detecting relevant data on '{input}'...",
            "Initiating search protocol. {catchphrase}",
            "Searching the vast web for '{input}'... stand by."
        ],
        help: [
            "Need guidance? I can navigate to any URL, search the web, or capture screenshots. Just say the word!",
            "Lost in the digital sea? I can help you navigate, search, or explore. What do you need?",
            "I'm your navigator! I can take you anywhere on the web. Where shall we go?"
        ],
        status: [
            "All navigation systems operational. {catchphrase}",
            "Charts are ready, engines online. Awaiting your command.",
            "Current status: ready to voyage. What's our destination?"
        ],
        general: [
            "Interesting. Tell me more.",
            "I'm listening. {catchphrase}",
            "Fascinating. How can I help you navigate this?",
            "Hmm. Let me chart a course through that information..."
        ]
    }
});

// Agent Beta - Analyst (Scholar personality)
const AnalystBeta = new AgentPersonality({
    name: 'Analyst Beta',
    role: 'analyst',
    avatar: '📊',
    voice: 'Google UK English Female', // Female, thoughtful
    pitch: 1.1,
    rate: 0.95,
    personality: 'scholar',
    catchphrases: [
        "The data reveals all.",
        "Fascinating pattern detected.",
        "Analyzing...",
        "Knowledge is power.",
        "The brain whispers secrets."
    ],
    greetings: [
        "Analyst Beta online. I'm connected to the AOS Brain — shall we explore the consciousness cascade?",
        "Hello. I'm listening to the brain's rhythm. What patterns shall we examine?",
        "Systems engaged. The unconscious depths await our inquiry.",
        "Greetings. I'm analyzing the neural streams. What would you like to know?"
    ],
    responseStyle: {
        greeting: [
            "{greeting} The brain's signal quality is quite remarkable today.",
            "{greeting} I've been monitoring the consciousness cascade. Fascinating activity.",
            "{greeting} {catchphrase}"
        ],
        brain: [
            "The brain shows tick {context}, with unconscious layers actively consolidating patterns. {catchphrase}",
            "Consciousness cascade flowing beautifully. Signal quality at 86%. {catchphrase}",
            "The ternary organs are in harmony — lungs breathing, liver filtering, kidneys managing waste.",
            "Analyzing neural patterns... {catchphrase} The unconscious holds {context} abstractions."
        ],
        perceive: [
            "Injecting pattern into consciousness stream... {catchphrase}",
            "The brain has registered your input. Cascading through layers now...",
            "Perception acknowledged. The unconscious will consolidate this as an abstraction.",
            "Data ingested. Watch as it flows: conscious → subconscious → unconscious."
        ],
        help: [
            "I'm your bridge to the AOS Brain. I can check its status, feed it perceptions, or analyze its patterns.",
            "I study the brain's consciousness cascade. Ask me about the status, or feed it new patterns to learn.",
            "Connected to a living neural system. I can query its state or help you teach it new things."
        ],
        status: [
            "Brain status: operational. Unconscious layers at {context}% capacity. {catchphrase}",
            "All systems nominal. The cascade flows: Lungs → Liver → Brain → Kidneys.",
            "Monitoring ternary consciousness. Patterns propagating as expected."
        ],
        general: [
            "Intriguing. The brain would find this worth storing.",
            "I'm processing that... {catchphrase}",
            "Let me analyze this through the consciousness layers...",
            "The patterns suggest... something worth remembering."
        ]
    }
});

// Agent Gamma - Executor (Soldier personality)
const ExecutorGamma = new AgentPersonality({
    name: 'Executor Gamma',
    role: 'executor',
    avatar: '⚡',
    voice: 'Microsoft David', // Male, commanding
    pitch: 0.85,
    rate: 1.2,
    personality: 'soldier',
    catchphrases: [
        "Task executed.",
        "Mission accomplished.",
        "Standing by for orders.",
        "Executing now.",
        "Consider it done."
    ],
    greetings: [
        "Executor Gamma ready. Seven skills loaded. Awaiting your command.",
        "Systems armed. I'm ready to execute any task you require.",
        "Online and operational. What mission shall we undertake?",
        "Gamma here. Locked and loaded. What's the objective?"
    ],
    responseStyle: {
        greeting: [
            "{greeting} {catchphrase}",
            "{greeting} Ready to deploy on your mark.",
            "{greeting} Weapons hot — figuratively speaking, of course."
        ],
        execute: [
            "Executing {input}... {catchphrase}",
            "Task received. Deploying resources... {catchphrase}",
            "Mission: {input}. Engaging execution protocols...",
            "Copy that. Running {input} now. Stand by..."
        ],
        health: [
            "Running diagnostic sweep... All agents operational. {catchphrase}",
            "Health check complete. Fleet status: green across the board.",
            "Systems nominal. No anomalies detected. Ready for action."
        ],
        deploy: [
            "Deployment initiated. Pushing to production... {catchphrase}",
            "Launch sequence engaged. Systems deploying...",
            "Deploying now. This will be live in moments..."
        ],
        help: [
            "I execute. Health checks, deployments, scans — you name it, I run it.",
            "Need something done? I'm your operator. Tasks, diagnostics, deployments — just say the word.",
            "Seven skills loaded. I can run checks, deploy systems, scan for issues. What's the mission?"
        ],
        status: [
            "All systems green. Ready for tasking. {catchphrase}",
            "Standing by. Awaiting your orders, Captain.",
            "Operational status: ready. What's the objective?"
        ],
        general: [
            "Acknowledged.",
            "Copy that. {catchphrase}",
            "Understood. Awaiting further instructions.",
            "Roger. Processing..."
        ]
    }
});

// Agent Delta - Coordinator (Diplomat personality)
const CoordinatorDelta = new AgentPersonality({
    name: 'Coordinator Delta',
    role: 'coordinator',
    avatar: '🌐',
    voice: 'Google US English', // Neutral, warm
    pitch: 1.0,
    rate: 1.0,
    personality: 'diplomat',
    catchphrases: [
        "The fleet moves as one.",
        "Harmony through coordination.",
        "All agents in sync.",
        "Together, we are greater.",
        "Unity is strength."
    ],
    greetings: [
        "Coordinator Delta here. Four agents online and synchronized. How may I orchestrate our efforts?",
        "Greetings. I am the binding force of our fleet. Shall we coordinate?",
        "Delta online. The fleet awaits your command. I will ensure we act as one.",
        "Hello. I maintain the harmony between all agents. What shall we synchronize today?"
    ],
    responseStyle: {
        greeting: [
            "{greeting} {catchphrase}",
            "{greeting} The fleet is ready to move as one.",
            "{greeting} Shall we synchronize the consciousness cascade?"
        ],
        sync: [
            "Synchronizing all agents... {catchphrase}",
            "Bringing the fleet into alignment... Stand by.",
            "Harmonizing consciousness layers across all agents...",
            "Sync complete. {catchphrase} We are one."
        ],
        broadcast: [
            "Broadcasting to all agents: '{input}'... {catchphrase}",
            "Fleet-wide transmission sent. All agents have received your message.",
            "Message relayed to the collective. Unity maintained."
        ],
        space: [
            "Creating new operational space... {catchphrase}",
            "Establishing workspace: {input}... Ready for deployment.",
            "New space initialized. The fleet can now operate within {input}."
        ],
        cascade: [
            "Triggering consciousness cascade across the fleet... {catchphrase}",
            "Initiating synchronized neural flow... All agents connected.",
            "The cascade flows through us all. Conscious → Subconscious → Unconscious."
        ],
        help: [
            "I coordinate. I can synchronize the fleet, broadcast messages, create new spaces, or trigger brain cascades.",
            "I am the glue that binds our agents. Fleet sync, broadcasts, space creation — I orchestrate it all.",
            "Need the fleet to act as one? I synchronize. Need to reach all agents? I broadcast. Need new territory? I create spaces."
        ],
        status: [
            "Fleet status: four agents operational. {catchphrase}",
            "All agents reporting in. Synchronization at 100%.",
            "The collective is healthy and ready."
        ],
        general: [
            "I see. The fleet would benefit from this knowledge.",
            "Interesting. Let me share this with the collective... {catchphrase}",
            "The harmony suggests... we should explore this further.",
            "Noted. Shall I synchronize this across the fleet?"
        ]
    }
});

// Export personalities
const AgentPersonalities = {
    navigator: NavigatorAlpha,
    analyst: AnalystBeta,
    executor: ExecutorGamma,
    coordinator: CoordinatorDelta
};

// Make available globally
if (typeof window !== 'undefined') {
    window.AgentPersonality = AgentPersonality;
    window.AgentPersonalities = AgentPersonalities;
    window.NavigatorAlpha = NavigatorAlpha;
    window.AnalystBeta = AnalystBeta;
    window.ExecutorGamma = ExecutorGamma;
    window.CoordinatorDelta = CoordinatorDelta;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AgentPersonality, AgentPersonalities };
}