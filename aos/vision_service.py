#!/usr/bin/env python3
"""
AOS VISION SERVICE v1.0
Continuous visual processing for the brain using Pillow
No OpenCV required - runs on NumPy/Pillow only
"""

import os
import sys
import time
import json
import socket
import threading
from pathlib import Path
from PIL import Image, ImageFilter, ImageStat, ImageDraw
import numpy as np

sys.path.insert(0, '/root/.aos/aos')

class VisionService:
    """
    Continuous vision service that feeds visual data to brain cortex
    """
    
    def __init__(self, socket_path='/tmp/aos_brain.sock', 
                 capture_interval=5.0,  # seconds between captures
                 enable_camera=False,     # True for real camera
                 camera_simulate=True):   # Simulate if no camera
        self.socket_path = socket_path
        self.capture_interval = capture_interval
        self.enable_camera = enable_camera
        self.camera_simulate = camera_simulate
        
        self.running = False
        self.capture_thread = None
        self.agent_id = "vision_service"
        
        # Stats
        self.stats = {
            'captures': 0,
            'features_extracted': 0,
            'hotspots_sent': 0,
            'errors': 0
        }
        
        print(f"[VisionService] Initialized")
        print(f"  Capture interval: {capture_interval}s")
        print(f"  Camera: {'enabled' if enable_camera else 'simulated'}")
    
    def _send_to_brain(self, cmd: str, params: dict) -> dict:
        """Send command to brain socket"""
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(self.socket_path)
            
            request = json.dumps({'cmd': cmd, 'params': params})
            sock.sendall(request.encode() + b'\n')
            
            data = sock.recv(4096)
            sock.close()
            
            return json.loads(data.decode()) if data else {'error': 'no response'}
        except Exception as e:
            self.stats['errors'] += 1
            return {'error': str(e)}
    
    def _create_simulated_image(self, tick: int) -> Image.Image:
        """Create a simulated visual scene"""
        # Time-based color cycling
        hue = (tick * 15) % 360
        
        # Create base image
        img = Image.new('RGB', (640, 480))
        pixels = img.load()
        
        # Generate gradient background based on "time of day"
        for y in range(480):
            for x in range(640):
                # Sinusoidal pattern
                r = int(128 + 127 * np.sin((x + tick * 10) / 100.0))
                g = int(128 + 127 * np.sin((y + tick * 15) / 80.0))
                b = int(128 + 127 * np.sin((x + y + tick * 5) / 120.0))
                pixels[x, y] = (r, g, b)
        
        # Add moving "objects"
        draw = ImageDraw.Draw(img)
        
        # Moving rectangles
        for i in range(3):
            x = int(320 + 200 * np.sin((tick + i * 120) / 30.0))
            y = int(240 + 150 * np.cos((tick + i * 90) / 25.0))
            size = 30 + i * 20
            color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)][i]
            draw.rectangle([x-size, y-size, x+size, y+size], fill=color)
        
        # Pulsing circle
        cx = int(320 + 150 * np.sin(tick / 20.0))
        cy = int(240 + 100 * np.cos(tick / 15.0))
        radius = int(20 + 15 * np.sin(tick / 5.0))
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], 
                     fill=(255, 255, 0))
        
        return img
    
    def _extract_features(self, img: Image.Image) -> list:
        """Extract visual features from image"""
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        features = []
        
        # Basic stats
        stat = ImageStat.Stat(img)
        mean_rgb = np.array(stat.mean) / 255.0
        std_rgb = np.array(stat.stddev) / 255.0
        
        # Edge detection
        edges = img.filter(ImageFilter.FIND_EDGES)
        edge_stat = ImageStat.Stat(edges)
        edge_strength = np.mean(edge_stat.mean) / 255.0
        
        # Blur/texture
        blur = img.filter(ImageFilter.BLUR)
        blur_stat = ImageStat.Stat(blur)
        blur_score = np.std(blur_stat.mean) / 255.0
        
        width, height = img.size
        aspect = width / height if height > 0 else 1.0
        
        # Create feature vector
        feature_vec = np.array([
            mean_rgb[0], mean_rgb[1], mean_rgb[2],  # Color
            std_rgb[0], std_rgb[1], std_rgb[2],      # Variance
            edge_strength,                            # Edges
            blur_score,                               # Texture
            aspect,                                   # Shape
            width / 1920.0                            # Scale
        ])
        
        features.append({
            'label': 'scene',
            'confidence': 1.0,
            'vector': feature_vec
        })
        
        # Color dominance
        dominant = np.argmax(mean_rgb)
        color_names = ['red', 'green', 'blue']
        features.append({
            'label': f'dominant_{color_names[dominant]}',
            'confidence': float(mean_rgb[dominant]),
            'vector': feature_vec * 0.5
        })
        
        # Brightness level
        brightness = np.mean(mean_rgb)
        features.append({
            'label': 'bright' if brightness > 0.5 else 'dark',
            'confidence': abs(brightness - 0.5) * 2,
            'vector': feature_vec * 0.3
        })
        
        # Texture complexity
        complexity = std_rgb.mean()
        features.append({
            'label': 'complex' if complexity > 0.3 else 'simple',
            'confidence': min(1.0, complexity * 3),
            'vector': feature_vec * 0.4
        })
        
        return features
    
    def _encode_to_ternary(self, features: list) -> list:
        """Encode features to ternary hotspots"""
        import hashlib
        hotspots = []
        
        for feat in features:
            vec = feat['vector'][:10]
            vec = (vec - vec.mean()) / (vec.std() + 1e-8)
            
            # Quantize to ternary
            ternary = np.where(vec > 0.3, 1, np.where(vec < -0.3, -1, 0))
            
            # Label hash for spatial distribution
            label_hash = int(hashlib.md5(feat['label'].encode()).hexdigest(), 16)
            conf = feat['confidence']
            
            for i, val in enumerate(ternary):
                if val != 0:
                    x = (label_hash + i * 137) % 32
                    y = (label_hash + i * 239) % 32
                    z = (label_hash + i * 541) % 32
                    
                    # Scale by confidence
                    if conf > 0.5:
                        hotspots.append([int(x), int(y), int(z), int(val)])
        
        return hotspots
    
    def _capture_and_send(self, tick: int):
        """Capture image and send to brain"""
        try:
            # Create or capture image
            img = self._create_simulated_image(tick)
            
            # Extract features
            features = self._extract_features(img)
            self.stats['features_extracted'] += len(features)
            
            # Encode to ternary
            hotspots = self._encode_to_ternary(features)
            
            if hotspots:
                # Send to brain cortex
                result = self._send_to_brain('cortex_write', {
                    'agent_id': self.agent_id,
                    'regions': list(range(8)),
                    'activations': hotspots,
                    'priority': 0.6,
                    'ephemeral': True  # Visual data is ephemeral
                })
                
                if 'write_result' in result:
                    self.stats['hotspots_sent'] += len(hotspots)
                
                # Trigger propagation
                self._send_to_brain('cortex_tick', {})
            
            self.stats['captures'] += 1
            
            # Log occasionally
            if tick % 10 == 0:
                feat_summary = ', '.join([f"{f['label']}:{f['confidence']:.2f}" 
                                         for f in features])
                print(f"[Vision] Tick {tick}: {feat_summary} | {len(hotspots)} hotspots")
            
        except Exception as e:
            self.stats['errors'] += 1
            print(f"[Vision] Error: {e}")
    
    def _run_loop(self):
        """Main capture loop"""
        tick = 0
        while self.running:
            self._capture_and_send(tick)
            tick += 1
            time.sleep(self.capture_interval)
    
    def start(self):
        """Start the vision service"""
        if self.running:
            return
        
        self.running = True
        self.capture_thread = threading.Thread(target=self._run_loop, daemon=True)
        self.capture_thread.start()
        print(f"[VisionService] Started")
    
    def stop(self):
        """Stop the vision service"""
        self.running = False
        if self.capture_thread:
            self.capture_thread.join(timeout=2)
        print(f"[VisionService] Stopped")
        print(f"  Captures: {self.stats['captures']}")
        print(f"  Features: {self.stats['features_extracted']}")
        print(f"  Hotspots: {self.stats['hotspots_sent']}")
        print(f"  Errors: {self.stats['errors']}")
    
    def get_status(self) -> dict:
        """Get service status"""
        return {
            'running': self.running,
            'agent_id': self.agent_id,
            'stats': self.stats.copy()
        }

def main():
    """Run vision service"""
    print("=" * 70)
    print("  AOS VISION SERVICE v1.0")
    print("  Continuous visual processing for the brain")
    print("=" * 70)
    
    service = VisionService(
        capture_interval=3.0,  # Every 3 seconds
        enable_camera=False,    # Simulation mode (no camera needed)
        camera_simulate=True
    )
    
    try:
        service.start()
        print("\n[Running] Press Ctrl+C to stop\n")
        
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n[Shutting down...]")
    finally:
        service.stop()
    
    print("=" * 70)

if __name__ == "__main__":
    main()
