#!/data/data/com.termux/files/usr/bin/env node
/**
 * MYL0N.js - Voice Interface for AOS-Lite Brain
 * Termux/Android Voice I/O Bridge
 * 
 * Features:
 * - Speech-to-text (Termux API)
 * - Text-to-speech (Termux API)
 * - WebSocket connection to AOS-Lite Brain
 * - Continuous listening mode
 * - Wake word detection ("Hey Myl0n")
 */

const { exec, spawn } = require('child_process');
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
    brainSocketUrl: 'ws://localhost:8765',
    wakeWord: 'hey mylon',
    wakeWordAlt: ['hey miles', 'hey mortimer', 'mylon', 'miles'],
    voiceLang: 'en-US',
    ttsEngine: 'com.google.android.tts',
    logFile: path.join(process.env.HOME, '.aos-lite/logs/myl0n.log'),
    stateFile: path.join(process.env.HOME, '.aos-lite/state/myl0n_state.json')
};

// State management
let state = {
    isListening: false,
    isSpeaking: false,
    lastWakeTime: 0,
    conversationHistory: [],
    connectedToBrain: false
};

// Logger
function log(level, message) {
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] [${level}] ${message}`;
    console.log(logEntry);
    
    // Append to log file
    const logDir = path.dirname(CONFIG.logFile);
    if (!fs.existsSync(logDir)) {
        fs.mkdirSync(logDir, { recursive: true });
    }
    fs.appendFileSync(CONFIG.logFile, logEntry + '\n');
}

// Check if Termux API is available
function checkTermuxAPI() {
    return new Promise((resolve) => {
        exec('termux-api-version', (error, stdout) => {
            if (error) {
                log('ERROR', 'Termux API not available. Install with: pkg install termux-api');
                resolve(false);
            } else {
                log('INFO', `Termux API available: ${stdout.trim()}`);
                resolve(true);
            }
        });
    });
}

// Text-to-Speech
function speak(text) {
    return new Promise((resolve, reject) => {
        if (state.isSpeaking) {
            log('WARN', 'Already speaking, queueing...');
            setTimeout(() => speak(text).then(resolve).catch(reject), 1000);
            return;
        }
        
        state.isSpeaking = true;
        log('INFO', `Speaking: "${text.substring(0, 50)}..."`);
        
        // Use termux-tts-speak
        const proc = spawn('termux-tts-speak', ['-r', '1.0', '-p', '1.0', text]);
        
        proc.on('close', (code) => {
            state.isSpeaking = false;
            if (code === 0) {
                resolve();
            } else {
                reject(new Error(`TTS exited with code ${code}`));
            }
        });
        
        proc.on('error', (err) => {
            state.isSpeaking = false;
            reject(err);
        });
    });
}

// Speech-to-Text
function listen(duration = 5) {
    return new Promise((resolve, reject) => {
        if (state.isListening) {
            reject(new Error('Already listening'));
            return;
        }
        
        state.isListening = true;
        log('INFO', `Listening for ${duration} seconds...`);
        
        // Use termux-speech-to-text
        const proc = spawn('termux-speech-to-text', ['-l', CONFIG.voiceLang]);
        
        let transcript = '';
        
        proc.stdout.on('data', (data) => {
            transcript += data.toString();
        });
        
        proc.on('close', (code) => {
            state.isListening = false;
            transcript = transcript.trim();
            
            if (code === 0 && transcript) {
                log('INFO', `Heard: "${transcript}"`);
                resolve(transcript);
            } else if (code === 0) {
                resolve(null); // No speech detected
            } else {
                reject(new Error(`STT exited with code ${code}`));
            }
        });
        
        // Timeout
        setTimeout(() => {
            if (state.isListening) {
                proc.kill();
                state.isListening = false;
                resolve(null);
            }
        }, duration * 1000);
        
        proc.on('error', (err) => {
            state.isListening = false;
            reject(err);
        });
    });
}

// Check for wake word
function checkWakeWord(text) {
    const lowerText = text.toLowerCase();
    const wakeWords = [CONFIG.wakeWord, ...CONFIG.wakeWordAlt];
    
    for (const wake of wakeWords) {
        if (lowerText.includes(wake)) {
            return true;
        }
    }
    return false;
}

// Connect to AOS-Lite Brain
function connectToBrain() {
    return new Promise((resolve, reject) => {
        log('INFO', `Connecting to AOS-Lite Brain at ${CONFIG.brainSocketUrl}...`);
        
        const ws = new WebSocket(CONFIG.brainSocketUrl);
        
        ws.on('open', () => {
            log('INFO', 'Connected to AOS-Lite Brain');
            state.connectedToBrain = true;
            resolve(ws);
        });
        
        ws.on('message', (data) => {
            try {
                const response = JSON.parse(data);
                handleBrainResponse(response);
            } catch (e) {
                log('ERROR', `Failed to parse brain response: ${e.message}`);
            }
        });
        
        ws.on('error', (err) => {
            log('ERROR', `WebSocket error: ${err.message}`);
            state.connectedToBrain = false;
            reject(err);
        });
        
        ws.on('close', () => {
            log('WARN', 'Disconnected from AOS-Lite Brain');
            state.connectedToBrain = false;
        });
    });
}

// Handle response from brain
async function handleBrainResponse(response) {
    if (response.text) {
        log('INFO', `Brain response: "${response.text.substring(0, 100)}..."`);
        
        // Add to conversation history
        state.conversationHistory.push({
            role: 'assistant',
            text: response.text,
            timestamp: Date.now()
        });
        
        // Speak the response
        try {
            await speak(response.text);
        } catch (e) {
            log('ERROR', `Failed to speak: ${e.message}`);
        }
    }
}

// Send message to brain
function sendToBrain(ws, text) {
    if (!state.connectedToBrain) {
        log('ERROR', 'Not connected to brain');
        return;
    }
    
    const message = {
        type: 'user_input',
        text: text,
        timestamp: Date.now(),
        source: 'myl0n_voice'
    };
    
    ws.send(JSON.stringify(message));
    
    // Add to history
    state.conversationHistory.push({
        role: 'user',
        text: text,
        timestamp: Date.now()
    });
}

// Main conversation loop
async function conversationLoop(ws) {
    log('INFO', 'Starting conversation loop...');
    
    // Welcome message
    await speak("Hello, I'm Myl0n. I'm ready to help you. Say 'Hey Myl0n' to wake me up.");
    
    while (true) {
        try {
            // Always listening for wake word
            const heard = await listen(10);
            
            if (!heard) {
                continue;
            }
            
            // Check for wake word
            if (checkWakeWord(heard)) {
                log('INFO', 'Wake word detected!');
                await speak("Yes? I'm listening.");
                
                // Listen for command
                const command = await listen(10);
                
                if (command) {
                    // Send to brain
                    sendToBrain(ws, command);
                    
                    // Wait for response (handled by WebSocket handler)
                    await new Promise(resolve => setTimeout(resolve, 2000));
                } else {
                    await speak("I didn't catch that. Could you repeat?");
                }
            }
        } catch (e) {
            log('ERROR', `Conversation loop error: ${e.message}`);
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }
}

// Save state on exit
function saveState() {
    const stateDir = path.dirname(CONFIG.stateFile);
    if (!fs.existsSync(stateDir)) {
        fs.mkdirSync(stateDir, { recursive: true });
    }
    fs.writeFileSync(CONFIG.stateFile, JSON.stringify(state, null, 2));
    log('INFO', 'State saved');
}

// Load state on startup
function loadState() {
    if (fs.existsSync(CONFIG.stateFile)) {
        try {
            const saved = JSON.parse(fs.readFileSync(CONFIG.stateFile, 'utf8'));
            state = { ...state, ...saved };
            log('INFO', 'State loaded');
        } catch (e) {
            log('ERROR', `Failed to load state: ${e.message}`);
        }
    }
}

// Main entry point
async function main() {
    console.log('╔════════════════════════════════════════╗');
    console.log('║     MYL0N.js Voice Interface           ║');
    console.log('║     For AOS-Lite Brain                 ║');
    console.log('╚════════════════════════════════════════╝');
    console.log('');
    
    // Load state
    loadState();
    
    // Check Termux API
    const hasAPI = await checkTermuxAPI();
    if (!hasAPI) {
        console.error('Termux API is required. Install with:');
        console.error('  pkg install termux-api');
        console.error('And allow microphone permission');
        process.exit(1);
    }
    
    // Connect to brain
    let ws;
    try {
        ws = await connectToBrain();
    } catch (e) {
        log('WARN', 'Could not connect to brain, running in standalone mode');
        // Create dummy WebSocket for standalone mode
        ws = {
            send: (msg) => {
                log('INFO', 'Standalone mode - would send: ' + msg);
                // Echo back
                setTimeout(() => {
                    handleBrainResponse({
                        text: "I'm running in standalone mode. Connect AOS-Lite Brain for full functionality."
                    });
                }, 500);
            }
        };
        state.connectedToBrain = false;
    }
    
    // Handle graceful shutdown
    process.on('SIGINT', () => {
        log('INFO', 'Shutting down...');
        saveState();
        if (ws && ws.close) ws.close();
        process.exit(0);
    });
    
    process.on('SIGTERM', () => {
        log('INFO', 'Shutting down...');
        saveState();
        if (ws && ws.close) ws.close();
        process.exit(0);
    });
    
    // Start conversation loop
    await conversationLoop(ws);
}

// Run main
main().catch(e => {
    log('FATAL', e.message);
    process.exit(1);
});
