#!/usr/bin/env python3
"""
FRACTAL VISION FEEDER v1.0
Generates Mandelbrot/Julia fractals and feeds them to AOS Brain cortex
Tests vision + RL learning via pattern recognition reward
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import json
import socket
import time
import threading
from typing import Tuple, List, Dict
from dataclasses import dataclass
import hashlib

@dataclass
class FractalFrame:
    """Generated fractal frame with metadata"""
    image: Image.Image
    pattern_type: str  # 'mandelbrot', 'julia', 'burning_ship'
    complexity: float  # 0-1 scale
    zoom_level: float
    coordinates: Tuple[float, float, float, float]  # x_min, x_max, y_min, y_max
    hotspots: List[Tuple[int, int, int, int]]  # Pre-encoded ternary

class FractalVisionFeeder:
    """
    Generates fractals and feeds them to Brain vision
    Uses RL reward signal based on pattern novelty
    """
    
    def __init__(self, brain_socket='/tmp/aos_brain.sock', capture_interval=2.0):
        self.brain_socket = brain_socket
        self.capture_interval = capture_interval
        self.agent_id = "fractal_vision"
        
        # RL state
        self.exploration_rate = 1.0  # Start fully exploring
        self.exploration_decay = 0.995
        self.min_exploration = 0.1
        
        # Pattern memory for novelty detection
        self.pattern_history = []
        self.max_history = 100
        
        # Fractal parameters
        self.current_zoom = 1.0
        self.center_x, self.center_y = -0.5, 0.0
        
        # Stats
        self.frames_generated = 0
        self.total_reward = 0.0
        
        print("[FractalVision] Initialized")
        print(f"  Agent: {self.agent_id}")
        print(f"  Capture interval: {capture_interval}s")
    
    def _send_to_brain(self, cmd: str, params: dict) -> dict:
        """Send command to brain socket"""
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(self.brain_socket)
            
            request = json.dumps({'cmd': cmd, 'params': params})
            sock.sendall(request.encode() + b'\n')
            
            data = sock.recv(4096)
            sock.close()
            
            return json.loads(data.decode()) if data else {'error': 'no response'}
        except Exception as e:
            return {'error': str(e)}
    
    def _mandelbrot(self, width=640, height=480, max_iter=100,
                    x_min=-2.5, x_max=1.0, y_min=-1.25, y_max=1.25) -> np.ndarray:
        """Generate Mandelbrot set"""
        y, x = np.ogrid[y_min:y_max:height*1j, x_min:x_max:width*1j]
        c = x + y*1j
        z = np.zeros_like(c)
        divtime = max_iter + np.zeros(z.shape, dtype=int)
        
        for i in range(max_iter):
            z = z**2 + c
            diverge = z*np.conj(z) > 2**2
            div_now = diverge & (divtime == max_iter)
            divtime[div_now] = i
            z[diverge] = 2  # Avoid overflow
        
        return divtime
    
    def _julia(self, width=640, height=480, max_iter=100,
               c_real=-0.7, c_imag=0.27015,
               x_min=-2.0, x_max=2.0, y_min=-1.5, y_max=1.5) -> np.ndarray:
        """Generate Julia set"""
        y, x = np.ogrid[y_min:y_max:height*1j, x_min:x_max:width*1j]
        z = x + y*1j
        c = complex(c_real, c_imag)
        divtime = max_iter + np.zeros(z.shape, dtype=int)
        
        for i in range(max_iter):
            z = z**2 + c
            diverge = z*np.conj(z) > 2**2
            div_now = diverge & (divtime == max_iter)
            divtime[div_now] = i
            z[diverge] = 2
        
        return divtime
    
    def _burning_ship(self, width=640, height=480, max_iter=100,
                      x_min=-2.5, x_max=1.5, y_min=-2.0, y_max=1.0) -> np.ndarray:
        """Generate Burning Ship fractal"""
        y, x = np.ogrid[y_min:y_max:height*1j, x_min:x_max:width*1j]
        c = x + y*1j
        z = np.zeros_like(c)
        divtime = max_iter + np.zeros(z.shape, dtype=int)
        
        for i in range(max_iter):
            z = (np.abs(z.real) + 1j*np.abs(z.imag))**2 + c
            diverge = z*np.conj(z) > 2**2
            div_now = diverge & (divtime == max_iter)
            divtime[div_now] = i
            z[diverge] = 2
        
        return divtime
    
    def _fractal_to_image(self, fractal: np.ndarray, colormap='fire') -> Image.Image:
        """Convert fractal array to colored image"""
        # Normalize to 0-255
        normalized = (fractal / fractal.max() * 255).astype(np.uint8)
        
        # Create RGB image
        img = Image.new('RGB', (fractal.shape[1], fractal.shape[0]))
        pixels = img.load()
        
        # Fire colormap (black → red → yellow → white)
        for y in range(fractal.shape[0]):
            for x in range(fractal.shape[1]):
                val = normalized[y, x]
                if colormap == 'fire':
                    r = min(255, val * 3)
                    g = min(255, max(0, (val - 85) * 3))
                    b = min(255, max(0, (val - 170) * 3))
                elif colormap == 'ocean':
                    r = 0
                    g = val // 2
                    b = val
                elif colormap == 'neon':
                    r = val if val % 2 == 0 else 0
                    g = val if val % 3 == 0 else 0
                    b = val if val % 5 == 0 else val
                else:
                    r = g = b = val
                
                pixels[x, y] = (int(r), int(g), int(b))
        
        return img
    
    def _extract_features(self, fractal: np.ndarray) -> Dict:
        """Extract RL-relevant features from fractal"""
        # Edge complexity (borders between regions)
        edges = np.diff(fractal, axis=0)[:-1, :] != 0
        edge_complexity = np.sum(edges) / edges.size
        
        # Pattern density
        unique_values = len(np.unique(fractal))
        density = unique_values / fractal.max()
        
        # Symmetry score
        h_sym = np.corrcoef(fractal.flatten(), np.fliplr(fractal).flatten())[0,1]
        v_sym = np.corrcoef(fractal.flatten(), np.flipud(fractal).flatten())[0,1]
        symmetry = (h_sym + v_sym) / 2
        
        return {
            'edge_complexity': float(edge_complexity),
            'density': float(density),
            'symmetry': float(symmetry),
            'unique_values': int(unique_values)
        }
    
    def _encode_to_ternary(self, fractal: np.ndarray, pattern_type: str) -> List[Tuple[int, int, int, int]]:
        """Encode fractal to ternary hotspots for brain cortex"""
        hotspots = []
        
        # Sample points from fractal (32x32 grid → 32×32×32 cortex)
        h, w = fractal.shape
        sample_h = min(32, h)
        sample_w = min(32, w)
        
        y_indices = np.linspace(0, h-1, sample_h, dtype=int)
        x_indices = np.linspace(0, w-1, sample_w, dtype=int)
        
        # Pattern type hash for spatial distribution
        type_hash = hashlib.md5(pattern_type.encode()).hexdigest()
        z_offset = int(type_hash, 16) % 32
        
        for i, y in enumerate(y_indices):
            for j, x in enumerate(x_indices):
                val = fractal[y, x]
                normalized = val / fractal.max()
                
                # Map to ternary: -1 (diverged early), 0 (mid), 1 (converged)
                if normalized < 0.3:
                    ternary = -1
                elif normalized > 0.7:
                    ternary = 1
                else:
                    ternary = 0
                
                if ternary != 0:
                    hotspots.append((j, i, (z_offset + int(normalized * 8)) % 32, ternary))
        
        return hotspots
    
    def _calculate_novelty(self, features: Dict) -> float:
        """Calculate pattern novelty reward for RL"""
        if not self.pattern_history:
            return 1.0  # First pattern is maximally novel
        
        # Compare to history
        distances = []
        for hist in self.pattern_history[-20:]:  # Compare to recent
            dist = abs(hist['edge_complexity'] - features['edge_complexity']) + \
                   abs(hist['density'] - features['density']) * 0.5 + \
                   abs(hist['symmetry'] - features['symmetry'])
            distances.append(dist)
        
        # Novelty = average distance to recent patterns
        novelty = np.mean(distances) if distances else 1.0
        return min(1.0, novelty * 2)  # Scale to 0-1
    
    def _generate_frame(self) -> FractalFrame:
        """Generate a fractal frame with RL exploration"""
        # Choose pattern type with exploration
        if np.random.random() < self.exploration_rate:
            pattern_type = np.random.choice(['mandelbrot', 'julia', 'burning_ship'])
        else:
            # Exploit - use type that gave highest recent reward
            pattern_type = 'mandelbrot'  # Default for now
        
        # Calculate zoom region
        zoom_factor = 2.0 ** (np.random.random() * 4)  # Zoom 1x to 16x
        zoom_width = 3.5 / zoom_factor
        zoom_height = 2.5 / zoom_factor
        
        # Random center for exploration
        if np.random.random() < 0.3:
            self.center_x = -0.5 + np.random.randn() * 0.5
            self.center_y = np.random.randn() * 0.5
        
        x_min = self.center_x - zoom_width/2
        x_max = self.center_x + zoom_width/2
        y_min = self.center_y - zoom_height/2
        y_max = self.center_y + zoom_height/2
        
        # Generate fractal
        if pattern_type == 'mandelbrot':
            fractal = self._mandelbrot(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
        elif pattern_type == 'julia':
            c_real = -0.7 + np.random.randn() * 0.1
            c_imag = 0.27015 + np.random.randn() * 0.1
            fractal = self._julia(c_real=c_real, c_imag=c_imag,
                                  x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
        else:  # burning_ship
            fractal = self._burning_ship(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
        
        # Extract features
        features = self._extract_features(fractal)
        
        # Calculate RL reward (novelty)
        reward = self._calculate_novelty(features)
        self.total_reward += reward
        
        # Update exploration
        self.exploration_rate = max(self.min_exploration, 
                                    self.exploration_rate * self.exploration_decay)
        
        # Store pattern
        self.pattern_history.append(features)
        if len(self.pattern_history) > self.max_history:
            self.pattern_history.pop(0)
        
        # Create image
        colormap = np.random.choice(['fire', 'ocean', 'neon'])
        image = self._fractal_to_image(fractal, colormap)
        
        # Encode to ternary
        hotspots = self._encode_to_ternary(fractal, pattern_type)
        
        # Complexity score
        complexity = features['edge_complexity'] * features['density']
        
        self.frames_generated += 1
        
        return FractalFrame(
            image=image,
            pattern_type=pattern_type,
            complexity=complexity,
            zoom_level=zoom_factor,
            coordinates=(x_min, x_max, y_min, y_max),
            hotspots=hotspots
        )
    
    def feed_to_brain(self, frame: FractalFrame) -> dict:
        """Send fractal to brain cortex"""
        # Write hotspots
        result = self._send_to_brain('cortex_write', {
            'agent_id': self.agent_id,
            'regions': list(range(8)),
            'activations': frame.hotspots,
            'priority': 0.7 + frame.complexity * 0.3,  # Higher priority for complex patterns
            'ephemeral': True
        })
        
        # Trigger propagation
        self._send_to_brain('cortex_tick', {})
        
        return result
    
    def run_episode(self, num_frames=10):
        """Run a full RL episode"""
        print(f"\n{'='*70}")
        print(f"  FRACTAL RL EPISODE: {num_frames} frames")
        print(f"{'='*70}\n")
        
        rewards = []
        
        for i in range(num_frames):
            # Generate fractal
            frame = self._generate_frame()
            
            # Feed to brain
            result = self.feed_to_brain(frame)
            
            # Calculate reward
            reward = self._calculate_novelty(self._extract_features(
                self._mandelbrot()  # Re-generate for feature extraction
            ))
            rewards.append(reward)
            
            # Log
            print(f"Frame {i+1}/{num_frames}: {frame.pattern_type.upper()}")
            print(f"  Complexity: {frame.complexity:.3f} | Zoom: {frame.zoom_level:.1f}x")
            print(f"  Hotspots: {len(frame.hotspots)} | Reward: {reward:.3f}")
            print(f"  Exploration: {self.exploration_rate:.3f}")
            print(f"  Brain: {result.get('write_result', 'error')}")
            print()
            
            time.sleep(self.capture_interval)
        
        # Episode summary
        avg_reward = np.mean(rewards)
        print(f"{'='*70}")
        print(f"  EPISODE COMPLETE")
        print(f"  Average Reward: {avg_reward:.3f}")
        print(f"  Total Exploration: {self.exploration_rate:.3f}")
        print(f"  Frames Generated: {self.frames_generated}")
        print(f"{'='*70}\n")
        
        return avg_reward

def demo():
    """Demo fractal vision feeding"""
    feeder = FractalVisionFeeder(capture_interval=1.0)
    
    # Run episode
    feeder.run_episode(num_frames=5)
    
    # Check brain status
    print("\nChecking brain integration...")
    status = feeder._send_to_brain('status', {})
    print(f"Brain tick: {status.get('tick', 'N/A')}")
    
    agents = status.get('cortex', {}).get('agents', {})
    if feeder.agent_id in agents:
        agent_stats = agents[feeder.agent_id]
        print(f"Fractal agent writes: {agent_stats.get('writes', 0)}")
    else:
        print(f"Fractal agent not yet in cortex (normal - takes a few seconds)")

if __name__ == "__main__":
    demo()
