#!/usr/bin/env python3
"""
AOS VOICE SYSTEM v1.1 - Brain-Integrated TTS + STT
Uses espeak-ng for TTS, encodes speech to cortex
"""

import numpy as np
import json
import socket
import time
import threading
import subprocess
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Tuple

class VoiceSystem:
    """
    Voice I/O for Brain - TTS + STT + Neural encoding
    """
    
    def __init__(self, brain_socket='/tmp/aos_brain.sock', agent_id="voice_system"):
        self.brain_socket = brain_socket
        self.agent_id = agent_id
        self.running = False
        
        # Check TTS
        self.tts_tool = None
        self._find_tts()
        
        # Voice state
        self.utterance_queue = []
        self.last_speech = ""
        
        # Stats
        self.stats = {'spoken': 0, 'heard': 0, 'encoded': 0}
        
        print("[VoiceSystem] Initialized")
        print(f"  TTS: {self.tts_tool or 'text-only'}")
    
    def _find_tts(self):
        """Find available TTS tool"""
        for tool in ['espeak-ng', 'espeak']:
            result = subprocess.run(['which', tool], capture_output=True)
            if result.returncode == 0:
                self.tts_tool = tool
                break
    
    def _send(self, cmd, params) -> Dict:
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(self.brain_socket)
            sock.sendall((json.dumps({'cmd': cmd, 'params': params}) + '\n').encode())
            data = sock.recv(4096)
            sock.close()
            return json.loads(data.decode()) if data else {}
        except:
            return {}
    
    def speak(self, text: str, save_audio: bool = False) -> bool:
        """Synthesize speech and encode to brain"""
        if not text:
            return False
        
        print(f"[Voice] 🔊 {text[:60]}...")
        
        # Physical TTS
        if self.tts_tool:
            try:
                # Use subprocess without waiting for audio output
                subprocess.Popen(
                    [self.tts_tool, text],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except:
                pass
        
        # Encode to neural pattern
        hotspots = self._text_to_cortex(text, 'spoken')
        
        # Send to brain's language region
        self._send('cortex_write', {
            'agent_id': self.agent_id,
            'regions': [7],  # Language region
            'activations': hotspots,
            'priority': 0.8,
            'ephemeral': False
        })
        
        self._send('cortex_tick', {})
        
        self.last_speech = text
        self.stats['spoken'] += 1
        self.stats['encoded'] += len(hotspots)
        
        return True
    
    def hear(self, text: str) -> bool:
        """Process heard speech and encode to brain"""
        if not text:
            return False
        
        print(f"[Voice] 👂 Heard: {text[:60]}...")
        
        # Encode to neural pattern
        hotspots = self._text_to_cortex(text, 'heard')
        
        # Send to brain
        self._send('cortex_write', {
            'agent_id': self.agent_id,
            'regions': [7, 3],  # Language + processing
            'activations': hotspots,
            'priority': 0.75,
            'ephemeral': False
        })
        
        self._send('cortex_tick', {})
        
        self.stats['heard'] += 1
        self.stats['encoded'] += len(hotspots)
        
        return True
    
    def _text_to_cortex(self, text: str, mode: str) -> List[List[int]]:
        """Convert text to 32x32x32 ternary hotspots"""
        hotspots = []
        
        # Tokenize (simple word splitting)
        words = text.lower().split()[:20]  # First 20 words
        
        for i, word in enumerate(words):
            # Hash word for spatial encoding
            word_hash = int(hashlib.md5(word.encode()).hexdigest(), 16)
            
            # Word position in space
            x = (word_hash % 32)
            y = ((word_hash // 32) % 32)
            z = 24 + ((word_hash // 1024) % 8)  # Language zone
            
            # Polarity: +1 for spoken, -1 for heard
            polarity = 1 if mode == 'spoken' else -1
            
            # Multiple hotspots per word (importance weighting)
            weight = min(5, len(word))  # Longer words = more hotspots
            for w in range(weight):
                offset = (w * 7) % 32
                hotspots.append([
                    (x + offset) % 32,
                    (y + offset * 3) % 32,
                    (z + w) % 32,
                    polarity
                ])
        
        return hotspots
    
    def say_status(self):
        """Announce system status"""
        status = self._send('status', {})
        tick = status.get('tick', 0)
        phase = status.get('phase', 'unknown')
        
        msg = f"Brain tick {tick}. Phase {phase}."
        self.speak(msg)
        return msg
    
    def run_announcements(self, interval: int = 60):
        """Periodically announce status"""
        self.running = True
        
        # Initial greeting
        self.speak("Voice system online. Multi-sense brain active.")
        
        while self.running:
            time.sleep(interval)
            if self.running:
                self.say_status()
    
    def stop(self):
        self.running = False
        print(f"\n[VoiceSystem] Stopped")
        print(f"  Spoken: {self.stats['spoken']}")
        print(f"  Heard: {self.stats['heard']}")
        print(f"  Hotspots encoded: {self.stats['encoded']}")

def main():
    voice = VoiceSystem()
    
    # Demo
    voice.speak("Hello. This is the AOS voice system speaking to the brain.")
    time.sleep(2)
    
    voice.hear("User said: What is your status?")
    time.sleep(2)
    
    voice.say_status()
    
    # Keep running
    try:
        voice.run_announcements(interval=30)
    except KeyboardInterrupt:
        voice.stop()

if __name__ == "__main__":
    main()
