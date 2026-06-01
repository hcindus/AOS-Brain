#!/usr/bin/env python3
"""
AOS AUDIO SENSE v1.0
Simulated audio processing for brain
"""

import numpy as np
import json
import socket
import time
import threading
import hashlib
from typing import List, Dict
from datetime import datetime

class AudioSense:
    """
    Audio processing - simulated soundscapes
    """
    
    def __init__(self, brain_socket='/tmp/aos_brain.sock', agent_id="audio_sense"):
        self.brain_socket = brain_socket
        self.agent_id = agent_id
        self.running = False
        self.tick = 0
        self.stats = {'captures': 0, 'hotspots': 0}
        
        # Audio patterns
        self.frequencies = [100, 440, 880, 1760, 3520]  # Musical notes
        self.amplitudes = [0.5] * 5
        
        print("[AudioSense] Initialized")
    
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
    
    def _generate_audio(self) -> np.ndarray:
        """Generate audio spectrum"""
        # Simulate audio waveform
        sample_rate = 44100
        duration = 0.1  # 100ms
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Mix frequencies
        signal = np.zeros_like(t)
        for freq, amp in zip(self.frequencies, self.amplitudes):
            signal += amp * np.sin(2 * np.pi * freq * t + self.tick * 0.1)
        
        # FFT to spectrum
        fft = np.abs(np.fft.fft(signal))[:len(signal)//2]
        spectrum = fft / np.max(fft + 1e-10)
        
        # Vary amplitudes for next cycle
        self.amplitudes = [
            0.3 + 0.7 * np.abs(np.sin(self.tick * 0.2 + i * 0.5))
            for i in range(5)
        ]
        
        return spectrum
    
    def _encode_spectrum(self, spectrum: np.ndarray) -> List[List[int]]:
        """Encode audio to ternary"""
        hotspots = []
        
        # Sample 32 frequency bins
        bins = np.linspace(0, len(spectrum)-1, 32, dtype=int)
        values = spectrum[bins]
        
        for i, val in enumerate(values):
            if val > 0.3:
                t = 1 if val > 0.6 else 0
                if t != 0:
                    x = i % 32
                    y = (i // 8) % 32
                    z = 28 + (i % 4)  # Audio occupies top of cortex
                    hotspots.append([x, y, z, t])
        
        return hotspots
    
    def capture(self):
        """Capture and send audio"""
        spectrum = self._generate_audio()
        hotspots = self._encode_spectrum(spectrum)
        
        result = self._send('cortex_write', {
            'agent_id': self.agent_id,
            'regions': [6, 7],  # Auditory regions
            'activations': hotspots,
            'priority': 0.5,
            'ephemeral': True
        })
        
        self._send('cortex_tick', {})
        
        self.stats['captures'] += 1
        self.stats['hotspots'] += len(hotspots)
        
        if self.tick % 30 == 0:
            print(f"[Audio] Tick {self.tick}: {len(hotspots)} hotspots, "
                  f"freqs={[f'{a:.2f}' for a in self.amplitudes[:3]]}")
        
        self.tick += 1
    
    def run(self, interval=0.5):
        self.running = True
        self._send('cortex_register', {'agent_id': self.agent_id})
        
        print("[AudioSense] Running...")
        while self.running:
            self.capture()
            time.sleep(interval)

def main():
    audio = AudioSense()
    audio.run()

if __name__ == "__main__":
    main()
