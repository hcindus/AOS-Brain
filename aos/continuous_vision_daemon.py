#!/usr/bin/env python3
"""
CONTINUOUS VISION DAEMON v1.0
Persistent visual feeding for AOS Brain
Runs 24/7, feeding simulated and real visual data
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageStat
import json
import socket
import time
import threading
import hashlib
from datetime import datetime
import signal
import sys

class ContinuousVisionDaemon:
    """
    Vision daemon that continuously feeds visual patterns to brain cortex
    """
    
    def __init__(self, brain_socket='/tmp/aos_brain.sock', 
                 capture_interval=3.0,
                 agent_id="vision_daemon"):
        self.brain_socket = brain_socket
        self.capture_interval = capture_interval
        self.agent_id = agent_id
        
        self.running = False
        self.thread = None
        self.tick_count = 0
        
        # Visual state
        self.time_of_day = 0  # 0-24
        self.scene_complexity = 0.5
        
        # Stats
        self.stats = {
            'captures': 0,
            'hotspots_sent': 0,
            'bytes_written': 0,
            'errors': 0,
            'start_time': None
        }
        
        print(f"[VisionDaemon] Initialized")
        print(f"  Agent: {agent_id}")
        print(f"  Interval: {capture_interval}s")
        print(f"  Target: {brain_socket}")
    
    def _send(self, cmd, params):
        """Send command to brain"""
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(self.brain_socket)
            sock.sendall((json.dumps({'cmd': cmd, 'params': params}) + '\n').encode())
            data = sock.recv(4096)
            sock.close()
            return json.loads(data.decode()) if data else {'error': 'empty'}
        except Exception as e:
            self.stats['errors'] += 1
            return {'error': str(e)}
    
    def _generate_scene(self, tick):
        """Generate a synthetic visual scene"""
        # Time-based color cycling
        hue_shift = (tick * 0.5) % 360
        
        # Create base image
        img = Image.new('RGB', (640, 480))
        pixels = img.load()
        
        # Generate dynamic gradient background
        for y in range(480):
            for x in range(640):
                # Time-varying pattern
                phase = (tick * 0.1) + (x / 100.0) + (y / 80.0)
                
                r = int(128 + 127 * np.sin(phase))
                g = int(128 + 127 * np.sin(phase + 2.094))  # 120° offset
                b = int(128 + 127 * np.sin(phase + 4.189))  # 240° offset
                
                pixels[x, y] = (r, g, b)
        
        # Add moving geometric shapes
        draw = ImageDraw.Draw(img)
        
        # Pulsing central orb
        pulse = 0.5 + 0.5 * np.sin(tick * 0.3)
        cx, cy = 320, 240
        radius = int(50 + 30 * pulse)
        
        orb_color = (
            int(255 * (0.5 + 0.5 * np.sin(tick * 0.2))),
            int(255 * (0.5 + 0.5 * np.sin(tick * 0.2 + 1.0))),
            int(255 * (0.5 + 0.5 * np.sin(tick * 0.2 + 2.0)))
        )
        
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], 
                     fill=orb_color, outline=(255, 255, 255), width=2)
        
        # Orbiting satellites
        for i in range(3):
            angle = (tick * 0.15) + (i * 2.094)  # 120° apart
            dist = 150 + i * 40
            sx = cx + int(dist * np.cos(angle))
            sy = cy + int(dist * np.sin(angle))
            sr = 15 + i * 5
            
            sat_color = [
                (255, 100, 100),  # Red satellite
                (100, 255, 100),  # Green satellite
                (100, 100, 255)   # Blue satellite
            ][i]
            
            draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=sat_color)
        
        # Dynamic grid overlay
        grid_spacing = 40 + int(10 * np.sin(tick * 0.1))
        for x in range(0, 640, grid_spacing):
            alpha = int(50 + 50 * np.sin(tick * 0.2 + x / 100))
            draw.line([(x, 0), (x, 480)], fill=(alpha, alpha, alpha), width=1)
        for y in range(0, 480, grid_spacing):
            alpha = int(50 + 50 * np.sin(tick * 0.2 + y / 100))
            draw.line([(0, y), (640, y)], fill=(alpha, alpha, alpha), width=1)
        
        return img
    
    def _extract_features(self, img):
        """Extract visual features"""
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
        
        # Texture/blur
        blur = img.filter(ImageFilter.BLUR)
        blur_stat = ImageStat.Stat(blur)
        texture = np.std(blur_stat.mean) / 255.0
        
        width, height = img.size
        aspect = width / height
        
        # Feature vector
        feature_vec = np.array([
            mean_rgb[0], mean_rgb[1], mean_rgb[2],  # Color
            std_rgb[0], std_rgb[1], std_rgb[2],      # Variance
            edge_strength,                            # Edges
            texture,                                  # Texture
            aspect,                                   # Shape
            width / 1920.0                            # Scale
        ])
        
        # Color dominance
        dominant = np.argmax(mean_rgb)
        color_names = ['red', 'green', 'blue']
        
        features.append({
            'label': 'scene',
            'confidence': 1.0,
            'vector': feature_vec
        })
        
        features.append({
            'label': f'dominant_{color_names[dominant]}',
            'confidence': float(mean_rgb[dominant]),
            'vector': feature_vec * 0.8
        })
        
        # Brightness
        brightness = np.mean(mean_rgb)
        features.append({
            'label': 'bright' if brightness > 0.5 else 'dark',
            'confidence': abs(brightness - 0.5) * 2,
            'vector': feature_vec * 0.5
        })
        
        # Complexity
        complexity = edge_strength * texture * 2
        features.append({
            'label': 'complex' if complexity > 0.3 else 'simple',
            'confidence': min(1.0, complexity),
            'vector': feature_vec * 0.6
        })
        
        # Motion energy (based on tick)
        motion = 0.5 + 0.5 * np.sin(self.tick_count * 0.3)
        features.append({
            'label': 'motion_high' if motion > 0.5 else 'motion_low',
            'confidence': motion,
            'vector': feature_vec * 0.7
        })
        
        return features
    
    def _encode_to_ternary(self, features, tick):
        """Encode features to 32x32x32 ternary hotspots"""
        hotspots = []
        
        for feat in features:
            vec = feat['vector'][:10]
            vec = (vec - vec.mean()) / (vec.std() + 1e-8)
            
            # Quantize to ternary
            ternary = np.where(vec > 0.3, 1, np.where(vec < -0.3, -1, 0))
            
            # Label-based spatial distribution
            label_hash = int(hashlib.md5(feat['label'].encode()).hexdigest(), 16)
            conf = feat['confidence']
            
            for i, val in enumerate(ternary):
                if val != 0 and conf > 0.4:
                    x = (label_hash + i * 137 + tick * 7) % 32
                    y = (label_hash + i * 239 + tick * 13) % 32
                    z = (label_hash + i * 541 + tick * 3) % 32
                    hotspots.append([int(x), int(y), int(z), int(val)])
        
        return hotspots
    
    def _capture_and_feed(self):
        """Generate scene and feed to brain"""
        try:
            # Generate visual scene
            img = self._generate_scene(self.tick_count)
            
            # Extract features
            features = self._extract_features(img)
            
            # Encode to ternary
            hotspots = self._encode_to_ternary(features, self.tick_count)
            
            # Calculate priority based on complexity
            avg_conf = np.mean([f['confidence'] for f in features])
            priority = 0.5 + avg_conf * 0.4
            
            # Send to brain - PERSISTENT
            result = self._send('cortex_write', {
                'agent_id': self.agent_id,
                'regions': list(range(8)),  # All 8 regions
                'activations': hotspots[:256],  # Top hotspots
                'priority': priority,
                'ephemeral': False
            })
            
            # Trigger propagation
            self._send('cortex_tick', {})
            
            # Update stats
            written = result.get('write_result', {}).get('written', 0)
            self.stats['hotspots_sent'] += len(hotspots)
            self.stats['bytes_written'] += written
            self.stats['captures'] += 1
            
            # Log every 10 captures
            if self.tick_count % 10 == 0:
                feat_summary = ', '.join([f"{f['label']}:{f['confidence']:.2f}"[:20] 
                                         for f in features[:3]])
                print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                      f"Tick {self.tick_count}: {len(hotspots)} hotspots, "
                      f"priority={priority:.2f} | {feat_summary}")
            
            self.tick_count += 1
            
        except Exception as e:
            self.stats['errors'] += 1
            print(f"[VisionDaemon] Error: {e}")
    
    def _run_loop(self):
        """Main daemon loop"""
        print(f"\n[VisionDaemon] Starting continuous feed...")
        print(f"  Press Ctrl+C to stop\n")
        
        while self.running:
            start = time.time()
            self._capture_and_feed()
            
            # Sleep to maintain interval
            elapsed = time.time() - start
            sleep_time = max(0, self.capture_interval - elapsed)
            time.sleep(sleep_time)
    
    def start(self):
        """Start the daemon"""
        if self.running:
            return
        
        # Register with brain
        print("[VisionDaemon] Registering with brain...")
        result = self._send('cortex_register', {'agent_id': self.agent_id})
        if result.get('registered') or result.get('error') == 'Agent already registered':
            print(f"[VisionDaemon] Registered as '{self.agent_id}'")
        else:
            print(f"[VisionDaemon] Registration: {result}")
        
        self.running = True
        self.stats['start_time'] = time.time()
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        
        print(f"[VisionDaemon] Running every {self.capture_interval}s")
    
    def stop(self):
        """Stop the daemon"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        
        runtime = time.time() - self.stats['start_time'] if self.stats['start_time'] else 0
        
        print(f"\n[VisionDaemon] Stopped")
        print(f"  Runtime: {runtime:.1f}s")
        print(f"  Captures: {self.stats['captures']}")
        print(f"  Hotspots: {self.stats['hotspots_sent']}")
        print(f"  Bytes: {self.stats['bytes_written']}")
        print(f"  Errors: {self.stats['errors']}")
        print(f"  Rate: {self.stats['captures']/(runtime/60):.1f} captures/min")
    
    def get_status(self):
        """Get daemon status"""
        runtime = time.time() - self.stats['start_time'] if self.stats['start_time'] else 0
        return {
            'running': self.running,
            'agent_id': self.agent_id,
            'tick': self.tick_count,
            'runtime': runtime,
            'stats': self.stats.copy()
        }

def main():
    daemon = ContinuousVisionDaemon(
        capture_interval=3.0,
        agent_id="vision_daemon"
    )
    
    # Handle signals
    def signal_handler(sig, frame):
        print("\n[Signal] Shutting down...")
        daemon.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start
    daemon.start()
    
    # Keep main thread alive
    try:
        while daemon.running:
            time.sleep(1)
    except KeyboardInterrupt:
        daemon.stop()

if __name__ == "__main__":
    main()
