#!/usr/bin/env python3
"""
AOS CROSS-MODAL TRIGGERS v1.0
Sensory integration - one sense triggers responses in others
"""

import numpy as np
import json
import socket
import time
import threading
from typing import Dict, List, Callable
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SensoryEvent:
    modality: str  # 'vision', 'audio', 'market', 'text'
    pattern: str   # Pattern name
    intensity: float  # 0-1
    data: Dict
    timestamp: float

class CrossModalIntegrator:
    """
    Integrates multiple senses - sound triggers vision, etc.
    """
    
    def __init__(self, brain_socket='/tmp/aos_brain.sock', agent_id="cross_modal"):
        self.brain_socket = brain_socket
        self.agent_id = agent_id
        self.running = False
        
        # Event buffer
        self.recent_events: List[SensoryEvent] = []
        self.max_events = 50
        
        # Cross-modal mappings
        self.mappings: Dict[str, List[Dict]] = {
            'audio_loud': [
                {'target': 'vision', 'effect': 'bright_flash', 'strength': 0.8},
                {'target': 'thyroid', 'effect': 'stimulate', 'strength': 0.6}
            ],
            'vision_bright': [
                {'target': 'audio', 'effect': 'high_tone', 'strength': 0.5},
                {'target': 'market', 'effect': 'hold_position', 'strength': 0.3}
            ],
            'market_volatile': [
                {'target': 'vision', 'effect': 'red_pulsing', 'strength': 0.9},
                {'target': 'audio', 'effect': 'alert_chime', 'strength': 0.7}
            ],
            'text_urgent': [
                {'target': 'vision', 'effect': 'attention_grab', 'strength': 0.8},
                {'target': 'thyroid', 'effect': 'secrete', 'strength': 0.9}
            ],
            'vision_motion': [
                {'target': 'audio', 'effect': 'spatial_sound', 'strength': 0.6},
                {'target': 'market', 'effect': 'watch_close', 'strength': 0.4}
            ],
            'market_breakout': [
                {'target': 'vision', 'effect': 'green_flash', 'strength': 0.85},
                {'target': 'audio', 'effect': 'success_tone', 'strength': 0.7}
            ]
        }
        
        # Stats
        self.cross_activations = 0
        
        print("[CrossModal] Initialized")
        print(f"  Mappings: {len(self.mappings)}")
    
    def _send(self, cmd, params):
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
    
    def receive_event(self, event: SensoryEvent):
        """Receive event from any sensory modality"""
        self.recent_events.append(event)
        if len(self.recent_events) > self.max_events:
            self.recent_events.pop(0)
        
        # Check for cross-modal triggers
        pattern_key = f"{event.modality}_{event.pattern}"
        
        if pattern_key in self.mappings:
            mappings = self.mappings[pattern_key]
            
            for mapping in mappings:
                if event.intensity * mapping['strength'] > 0.5:
                    self._trigger_cross_modal(mapping, event)
    
    def _trigger_cross_modal(self, mapping: Dict, source_event: SensoryEvent):
        """Trigger response in another modality"""
        target = mapping['target']
        effect = mapping['effect']
        strength = mapping['strength'] * source_event.intensity
        
        print(f"  🔄 CROSS-MODAL: {source_event.modality} → {target} "
              f"({effect}, strength={strength:.2f})")
        
        # Encode as cortical hotspot
        hotspots = self._encode_cross_modal(target, effect, strength)
        
        # Send to integration region
        self._send('cortex_write', {
            'agent_id': self.agent_id,
            'regions': [3, 4],  # Integration regions
            'activations': hotspots,
            'priority': 0.6 + strength * 0.3,
            'ephemeral': False
        })
        
        self._send('cortex_tick', {})
        self.cross_activations += 1
        
        # If thyroid target
        if target == 'thyroid':
            self._send('stimulate', {'importance': strength})
    
    def _encode_cross_modal(self, target: str, effect: str, strength: float) -> List[List[int]]:
        """Encode cross-modal signal to ternary"""
        hotspots = []
        
        # Target modality → spatial zone
        target_zones = {
            'vision': (0, 8),
            'audio': (8, 16),
            'market': (16, 24),
            'text': (24, 32)
        }
        
        z_min, z_max = target_zones.get(target, (0, 32))
        
        # Strength → number of hotspots
        num_hotspots = int(5 + strength * 20)
        
        for i in range(num_hotspots):
            x = (i * 3) % 32
            y = (i * 5 + ord(effect[0])) % 32
            z = z_min + (i % (z_max - z_min))
            t = 1 if strength > 0.5 else -1
            hotspots.append([x, y, z, t])
        
        return hotspots
    
    def _detect_synchrony(self) -> List[str]:
        """Detect when multiple senses fire together"""
        if len(self.recent_events) < 3:
            return []
        
        # Look at last 3 seconds
        now = time.time()
        recent = [e for e in self.recent_events if now - e.timestamp < 3.0]
        
        modalities = set(e.modality for e in recent)
        
        patterns = []
        
        # Multi-modal detection
        if len(modalities) >= 3:
            patterns.append("multi_modal_sync")
            print(f"  ✨ SYNCHRONY: {len(modalities)} senses aligned!")
        
        # Vision + Audio sync
        if 'vision' in modalities and 'audio' in modalities:
            patterns.append("audio_visual_sync")
        
        # Market + Vision (watching charts)
        if 'market' in modalities and 'vision' in modalities:
            patterns.append("trading_focus")
        
        return patterns
    
    def run_monitor(self, interval=1.0):
        """Monitor for cross-modal patterns"""
        self.running = True
        self._send('cortex_register', {'agent_id': self.agent_id})
        
        print("[CrossModal] Monitoring...")
        while self.running:
            patterns = self._detect_synchrony()
            if patterns:
                print(f"[CrossModal] Patterns: {patterns}")
            time.sleep(interval)
    
    def simulate_cross_modal(self):
        """Simulate cross-modal events for testing"""
        events = [
            SensoryEvent('audio', 'loud', 0.8, {}, time.time()),
            SensoryEvent('vision', 'bright', 0.7, {}, time.time()),
            SensoryEvent('market', 'volatile', 0.9, {}, time.time()),
            SensoryEvent('vision', 'motion', 0.6, {}, time.time()),
            SensoryEvent('market', 'breakout', 0.85, {'symbol': 'BTC'}, time.time()),
        ]
        
        print("\n[CrossModal] Simulating events...")
        for event in events:
            self.receive_event(event)
            time.sleep(0.5)
        
        print(f"\n[CrossModal] Total cross-activations: {self.cross_activations}")

def main():
    integrator = CrossModalIntegrator()
    
    # Run simulation
    integrator.simulate_cross_modal()
    
    # Start monitoring
    integrator.run_monitor()

if __name__ == "__main__":
    main()
