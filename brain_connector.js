/**
 * AOS Brain v4.5 Connector for brain.html
 * Connects AgentVerse Assistant to Miles Brain
 */

class AOSBrainConnector {
    constructor(apiUrl = 'http://localhost:8080') {
        this.apiUrl = apiUrl;
        this.statusInterval = null;
        this.onStatusUpdate = null;
        this.onError = null;
    }

    async getStatus() {
        try {
            const response = await fetch(`${this.apiUrl}/api/status`);
            return await response.json();
        } catch (e) {
            if (this.onError) this.onError(e);
            return null;
        }
    }

    async sendPerception(text, intensity = 0.8) {
        try {
            // Use direct socket for perception
            const response = await fetch(`${this.apiUrl}/api/command`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    cmd: 'perceive',
                    params: { observation: text, intensity: intensity }
                })
            });
            return await response.json();
        } catch (e) {
            if (this.onError) this.onError(e);
            return null;
        }
    }

    startMonitoring(intervalMs = 1000) {
        this.statusInterval = setInterval(async () => {
            const status = await this.getStatus();
            if (status && this.onStatusUpdate) {
                this.onStatusUpdate(this.formatStatus(status));
            }
        }, intervalMs);
    }

    stopMonitoring() {
        if (this.statusInterval) {
            clearInterval(this.statusInterval);
            this.statusInterval = null;
        }
    }

    formatStatus(raw) {
        const b = raw.brain;
        const c = b.consciousness;
        return {
            tick: b.tick,
            phase: b.phase,
            signalQuality: Math.round(b.signal_quality_20avg * 100),
            conscious: `${c.conscious.active_items}/${c.conscious.capacity}`,
            subconscious: `${c.subconscious.active_items}/${c.subconscious.capacity}`,
            unconscious: `${c.unconscious.active_items}/${c.unconscious.capacity}`,
            crossTalk: c.cross_talk_events,
            lungs: `${b.lungs.phase} (${b.lungs.cycles.inhale} breaths)`,
            liver: b.liver.state,
            kidneys: `${b.kidneys.bladder_level}/${b.kidneys.bladder_capacity}`,
            timestamp: new Date().toISOString()
        };
    }

    // Format status for chat display
    formatForChat(status) {
        return `
🧠 AOS Brain v4.5 Status (Tick ${status.tick})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Signal Quality: ${status.signalQuality}%
🎛️  Phase: ${status.phase}

Consciousness Layers:
  • Conscious: ${status.conscious}
  • Subconscious: ${status.subconscious}
  • Unconscious: ${status.unconscious}
  • Cross-talk: ${status.crossTalk} events

Ternary Organs:
  🫁 Lungs: ${status.lungs}
  🫘 Liver: ${status.liver}
  🫀 Kidneys: ${status.kidneys}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        `.trim();
    }
}

// Export for use in brain.html
if (typeof window !== 'undefined') {
    window.AOSBrainConnector = AOSBrainConnector;
}

// Node.js export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AOSBrainConnector;
}
