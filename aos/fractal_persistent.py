#!/usr/bin/env python3
"""
FRACTAL VISION v2.0 - Persistent RL Feeder
Non-ephemeral fractals for brain memory
"""

import numpy as np
from PIL import Image
import json
import socket
import time
import hashlib

class PersistentFractalFeeder:
    def __init__(self, brain_socket='/tmp/aos_brain.sock'):
        self.brain_socket = brain_socket
        self.agent_id = "fractal_rl_agent"
        self.frames = 0
    
    def _send(self, cmd, params):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(self.brain_socket)
            sock.sendall((json.dumps({'cmd': cmd, 'params': params}) + '\n').encode())
            data = sock.recv(8192)
            sock.close()
            return json.loads(data.decode()) if data else {'error': 'empty'}
        except Exception as e:
            return {'error': str(e)}
    
    def _mandelbrot(self, width=64, height=64, max_iter=50):
        """Fast mandelbrot for cortex feeding"""
        y, x = np.ogrid[-1.25:1.25:height*1j, -2.5:1.0:width*1j]
        c = x + y*1j
        z = np.zeros_like(c)
        divtime = max_iter + np.zeros(z.shape, dtype=int)
        
        for i in range(max_iter):
            z = z**2 + c
            diverge = z*np.conj(z) > 2**2
            div_now = diverge & (divtime == max_iter)
            divtime[div_now] = i
            z[diverge] = 2
        
        return divtime
    
    def _to_hotspots(self, fractal, pattern_type):
        """Convert to 32x32x32 ternary hotspots"""
        hotspots = []
        h, w = fractal.shape
        
        # Normalize
        max_val = fractal.max()
        
        # Pattern hash for spatial distribution
        z_base = int(hashlib.md5(pattern_type.encode()).hexdigest(), 16) % 24
        
        for y in range(min(32, h)):
            for x in range(min(32, w)):
                val = fractal[y % h, x % w] / max_val
                
                # Ternary: -1 (diverged), 0 (neutral), 1 (converged)
                if val < 0.3:
                    t = -1
                elif val > 0.8:
                    t = 1
                else:
                    continue  # Skip neutral
                
                z = (z_base + int(val * 8)) % 32
                hotspots.append([x, y, z, t])
        
        return hotspots
    
    def feed_fractal(self, pattern='mandelbrot'):
        """Generate and feed one fractal"""
        # Generate
        fractal = self._mandelbrot()
        
        # Encode
        hotspots = self._to_hotspots(fractal, pattern)
        
        # Send to brain - NOT ephemeral (persistent memory)
        result = self._send('cortex_write', {
            'agent_id': self.agent_id,
            'regions': list(range(8)),  # All regions
            'activations': hotspots[:512],  # Limit for efficiency
            'priority': 0.8,
            'ephemeral': False  # PERSISTENT
        })
        
        # Trigger propagation
        self._send('cortex_tick', {})
        
        self.frames += 1
        
        return {
            'hotspots': len(hotspots),
            'brain_result': result.get('write_result', {}),
            'pattern': pattern
        }
    
    def run_batch(self, count=10):
        """Feed multiple fractals"""
        print(f"Feeding {count} fractals to brain cortex...")
        print("="*60)
        
        patterns = ['mandelbrot', 'julia', 'burning_ship', 'tricorn', 'multibrot']
        
        for i in range(count):
            pattern = patterns[i % len(patterns)]
            result = self.feed_fractal(pattern)
            
            print(f"Frame {i+1}/{count}: {pattern}")
            print(f"  Hotspots: {result['hotspots']}")
            print(f"  Written: {result['brain_result'].get('written', 'N/A')}")
            print(f"  Regions: {result['brain_result'].get('regions_affected', 'N/A')}")
            time.sleep(0.5)
        
        print("="*60)
        print(f"Total frames: {self.frames}")
        
        # Check brain status
        print("\nChecking brain cortex...")
        status = self._send('status', {})
        agents = status.get('cortex', {}).get('agents', {})
        
        if self.agent_id in agents:
            stats = agents[self.agent_id]
            print(f"✓ {self.agent_id} registered!")
            print(f"  Writes: {stats['writes']}")
            print(f"  Reads: {stats['reads']}")
        else:
            print(f"~ Agent not yet visible (may take a moment)")
        
        # Read back
        print("\nReading cortex...")
        read = self._send('cortex_read', {
            'agent_id': self.agent_id,
            'regions': [0, 1, 2, 3],
            'max_hotspots': 10
        })
        
        print(f"  Coherence: {read.get('coherence', 'N/A')}")
        print(f"  Hotspots: {read.get('hotspot_count', 0)}")

if __name__ == "__main__":
    feeder = PersistentFractalFeeder()
    feeder.run_batch(count=5)
