/**
 * AOS Space Agent Voice System
 * TTS + STT with gender/character voice selection
 * Supports Web Speech API + Ollama (Mort_II) voices
 */

class AgentVoiceSystem {
    constructor(agent) {
        this.agent = agent;
        this.synthesis = window.speechSynthesis;
        this.recognition = null;
        this.isListening = false;
        
        // Voice library with characters
        this.voiceCharacters = {
            // Female voices
            'sarah': { name: 'Google US English', gender: 'female', pitch: 1.1, rate: 0.95 },
            'emma': { name: 'Google UK English Female', gender: 'female', pitch: 1.15, rate: 0.9 },
            'victoria': { name: 'Microsoft Zira', gender: 'female', pitch: 1.2, rate: 0.95 },
            'cortana': { name: 'Microsoft Cortana', gender: 'female', pitch: 1.0, rate: 1.0 },
            // Male voices
            'adam': { name: 'Google US English', gender: 'male', pitch: 0.9, rate: 1.0 },
            'david': { name: 'Microsoft David', gender: 'male', pitch: 0.85, rate: 1.1 },
            'mark': { name: 'Microsoft Mark', gender: 'male', pitch: 0.9, rate: 0.95 },
            // Neutral
            'alex': { name: 'Apple Alex', gender: 'neutral', pitch: 1.0, rate: 1.0 }
        };
        
        // Assign default voice based on role
        this.defaultVoices = {
            'navigator': 'adam',      // Male explorer
            'analyst': 'emma',        // Female scholar
            'executor': 'david',      // Male soldier
            'coordinator': 'sarah'    // Female diplomat
        };
        
        this.currentVoice = this.defaultVoices[agent.role] || 'sarah';
        this.setupSTT();
    }
    
    setupSTT() {
        // Setup Web Speech Recognition
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            this.recognition.continuous = true;
            this.recognition.interimResults = true;
            this.recognition.lang = 'en-US';
            
            this.recognition.onstart = () => {
                this.isListening = true;
                console.log(`[${this.agent.name}] 🎤 Listening...`);
                this.onListeningStart?.();
            };
            
            this.recognition.onresult = (event) => {
                const results = event.results;
                const lastResult = results[results.length - 1];
                
                if (lastResult.isFinal) {
                    const transcript = lastResult[0].transcript.trim();
                    console.log(`[${this.agent.name}] 🎤 Heard: "${transcript}"`);
                    this.onSpeechRecognized?.(transcript);
                } else {
                    // Interim results for visual feedback
                    const interim = lastResult[0].transcript.trim();
                    this.onInterimSpeech?.(interim);
                }
            };
            
            this.recognition.onerror = (event) => {
                console.error(`[${this.agent.name}] STT Error:`, event.error);
                if (event.error === 'no-speech') {
                    // Auto-restart if no speech detected
                    setTimeout(() => this.startListening(), 1000);
                }
                this.onListeningError?.(event.error);
            };
            
            this.recognition.onend = () => {
                this.isListening = false;
                console.log(`[${this.agent.name}] 🎤 Stopped listening`);
                this.onListeningEnd?.();
            };
        } else {
            console.warn(`[${this.agent.name}] STT not supported in this browser`);
        }
    }
    
    // Start listening for speech
    startListening() {
        if (!this.recognition) {
            console.error('Speech recognition not available');
            return false;
        }
        
        try {
            this.recognition.start();
            return true;
        } catch (e) {
            console.error('Failed to start listening:', e);
            return false;
        }
    }
    
    // Stop listening
    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
    }
    
    // Toggle listening
    toggleListening() {
        if (this.isListening) {
            this.stopListening();
        } else {
            this.startListening();
        }
        return this.isListening;
    }
    
    // Get available voices
    getAvailableVoices() {
        if (!this.synthesis) return [];
        return this.synthesis.getVoices();
    }
    
    // List all voice characters
    listVoiceCharacters() {
        return Object.entries(this.voiceCharacters).map(([id, char]) => ({
            id,
            ...char,
            isCurrent: id === this.currentVoice
        }));
    }
    
    // Set voice by character ID
    setVoice(characterId) {
        if (this.voiceCharacters[characterId]) {
            this.currentVoice = characterId;
            return true;
        }
        return false;
    }
    
    // Speak text with current voice
    speak(text, options = {}) {
        if (!this.synthesis) {
            console.warn('Speech synthesis not available');
            return false;
        }
        
        // Cancel any current speech
        this.synthesis.cancel();
        
        const character = this.voiceCharacters[this.currentVoice];
        const utterance = new SpeechSynthesisUtterance(text);
        
        // Apply voice settings
        utterance.pitch = options.pitch || character.pitch;
        utterance.rate = options.rate || character.rate;
        utterance.volume = options.volume || 1.0;
        
        // Find matching voice
        const voices = this.getAvailableVoices();
        const matchingVoice = voices.find(v => 
            v.name.includes(character.name) || 
            v.lang.includes('en')
        );
        
        if (matchingVoice) {
            utterance.voice = matchingVoice;
        }
        
        // Events
        utterance.onstart = () => {
            console.log(`[${this.agent.name}] 🔊 Speaking: "${text.slice(0, 50)}..."`);
            this.onSpeakStart?.(text);
        };
        
        utterance.onend = () => {
            this.onSpeakEnd?.();
            // Auto-restart listening after speaking (for conversation flow)
            if (options.autoListen) {
                setTimeout(() => this.startListening(), 500);
            }
        };
        
        utterance.onerror = (e) => {
            console.error(`[${this.agent.name}] TTS Error:`, e);
            this.onSpeakError?.(e);
        };
        
        this.synthesis.speak(utterance);
        return true;
    }
    
    // Speak with Ollama/Mort_II (higher quality, requires backend)
    async speakWithOllama(text, voice = 'alloy') {
        try {
            // This would call the Ollama TTS endpoint
            const response = await fetch('/brain/api/speak', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: text,
                    voice: voice,
                    agent: this.agent.id
                })
            });
            
            if (response.ok) {
                const audioBlob = await response.blob();
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                audio.play();
                return true;
            }
        } catch (e) {
            console.warn('Ollama TTS failed, falling back to Web Speech:', e);
            // Fallback to Web Speech
            return this.speak(text);
        }
    }
    
    // Stop speaking
    stopSpeaking() {
        if (this.synthesis) {
            this.synthesis.cancel();
        }
    }
    
    // Create voice selector UI
    createVoiceSelector() {
        const selector = document.createElement('div');
        selector.className = 'voice-selector';
        selector.innerHTML = `
            <style>
                .voice-selector {
                    background: rgba(10, 10, 26, 0.9);
                    border: 1px solid #00f3ff;
                    border-radius: 12px;
                    padding: 16px;
                    max-width: 300px;
                    color: white;
                    font-family: 'Inter', sans-serif;
                }
                .voice-selector h3 {
                    margin: 0 0 12px 0;
                    color: #00f3ff;
                    font-size: 14px;
                }
                .voice-option {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    padding: 8px;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: all 0.3s;
                }
                .voice-option:hover {
                    background: rgba(0, 243, 255, 0.1);
                }
                .voice-option.active {
                    background: rgba(0, 243, 255, 0.2);
                    border: 1px solid #00f3ff;
                }
                .voice-icon {
                    font-size: 20px;
                }
                .voice-info {
                    flex: 1;
                }
                .voice-name {
                    font-size: 13px;
                    font-weight: 600;
                }
                .voice-desc {
                    font-size: 11px;
                    color: #888;
                }
                .voice-gender {
                    font-size: 10px;
                    text-transform: uppercase;
                    padding: 2px 6px;
                    border-radius: 4px;
                    background: rgba(139, 92, 246, 0.3);
                }
                .voice-gender.female { background: rgba(255, 0, 255, 0.3); }
                .voice-gender.male { background: rgba(0, 243, 255, 0.3); }
            </style>
            <h3>🎤 Voice Selection</h3>
        `;
        
        const characters = this.listVoiceCharacters();
        characters.forEach(char => {
            const option = document.createElement('div');
            option.className = `voice-option ${char.isCurrent ? 'active' : ''}`;
            option.innerHTML = `
                <span class="voice-icon">${char.gender === 'female' ? '👩' : char.gender === 'male' ? '👨' : '🧑'}</span>
                <div class="voice-info">
                    <div class="voice-name">${char.id.charAt(0).toUpperCase() + char.id.slice(1)}</div>
                    <div class="voice-desc">${char.name}</div>
                </div>
                <span class="voice-gender ${char.gender}">${char.gender}</span>
            `;
            
            option.onclick = () => {
                this.setVoice(char.id);
                // Update UI
                selector.querySelectorAll('.voice-option').forEach(opt => opt.classList.remove('active'));
                option.classList.add('active');
                // Test voice
                this.speak(`Hello, I'm ${this.agent.name} using ${char.id}'s voice.`);
            };
            
            selector.appendChild(option);
        });
        
        return selector;
    }
    
    // Create microphone button
    createMicButton() {
        const button = document.createElement('button');
        button.className = 'voice-mic-btn';
        button.innerHTML = '🎤';
        button.title = 'Click to speak';
        
        button.style.cssText = `
            background: ${this.isListening ? '#f00' : 'rgba(0, 243, 255, 0.2)'};
            border: 2px solid ${this.isListening ? '#f00' : '#00f3ff'};
            border-radius: 50%;
            width: 48px;
            height: 48px;
            font-size: 24px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 ${this.isListening ? '30px #f00' : '10px #00f3ff'};
            animation: ${this.isListening ? 'pulse-mic 1s infinite' : 'none'};
        `;
        
        // Add pulse animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes pulse-mic {
                0%, 100% { box-shadow: 0 0 20px #f00; transform: scale(1); }
                50% { box-shadow: 0 0 40px #f00; transform: scale(1.1); }
            }
        `;
        document.head.appendChild(style);
        
        button.onclick = () => {
            this.toggleListening();
            this.updateMicButton(button);
        };
        
        // Update button when listening state changes
        this.onListeningStart = () => this.updateMicButton(button);
        this.onListeningEnd = () => this.updateMicButton(button);
        
        return button;
    }
    
    updateMicButton(button) {
        button.style.background = this.isListening ? '#f00' : 'rgba(0, 243, 255, 0.2)';
        button.style.borderColor = this.isListening ? '#f00' : '#00f3ff';
        button.style.boxShadow = this.isListening ? '0 0 30px #f00' : '0 0 10px #00f3ff';
        button.style.animation = this.isListening ? 'pulse-mic 1s infinite' : 'none';
        button.innerHTML = this.isListening ? '🔴' : '🎤';
        button.title = this.isListening ? 'Listening... (click to stop)' : 'Click to speak';
    }
}

// Make available
if (typeof window !== 'undefined') {
    window.AgentVoiceSystem = AgentVoiceSystem;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AgentVoiceSystem;
}