#!/usr/bin/env python3
"""
AOS CAMERA VISION v2.0
Real camera support with fallback to simulation
+ Visual trigger system for brain reactions
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import json
import socket
import time
import threading
import hashlib
import subprocess
from datetime import datetime
from typing import Optional, List, Tuple, Dict, Callable

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

class CameraVision:
    """Camera interface with simulation fallback"""
    
    def __init__(self, camera_id=0, width=640, height=480):
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.cap = None
        self.simulation_mode = True
        
    def open(self) -> bool:
        """Try to open real camera"""
        if not CV2_AVAILABLE:
            print("[Camera] OpenCV not available, using simulation")
            return False
        
        # Check if camera device exists
        try:
            result = subprocess.run(['ls', f'/dev/video{self.camera_id}'], 
                                  capture_output=True, timeout=2)
            if result.returncode != 0:
                print(f"[Camera] /dev/video{self.camera_id} not found")
                return False
        except:
            pass
        
        # Try to open
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret and frame is not None:
                    print(f"[Camera] Real camera opened! {self.width}x{self.height}")
                    self.simulation_mode = False
                    return True
        except Exception as e:
            print(f"[Camera] Error opening: {e}")
        
        print("[Camera] Falling back to simulation mode")
        return False
    
    def capture(self) -> Optional[Image.Image]:
        """Capture frame (real or simulated)"""
        if not self.simulation_mode and self.cap:
            ret, frame = self.cap.read()
            if ret:
                # Convert BGR to RGB
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return Image.fromarray(rgb)
        
        return None  # Let simulation handle it
    
    def close(self):
        if self.cap:
            self.cap.release()

class VisualTrigger:
    """Pattern-based trigger for brain reactions"""
    
    def __init__(self, name: str, condition: Callable, action: str):
        self.name = name
        self.condition = condition  # Function that returns bool
        self.action = action  # What to do when triggered
        self.trigger_count = 0
        self.last_triggered = 0
        self.cooldown = 5  # Seconds between triggers
    
    def check(self, features: Dict, tick: int) -> bool:
        """Check if trigger condition met"""
        if tick - self.last_triggered < self.cooldown * 10:  # Approximate ticks
            return False
        
        if self.condition(features):
            self.trigger_count += 1
            self.last_triggered = tick
            return True
        return False

class CameraVisionDaemon:
    """
    Vision daemon with camera support + visual triggers
    """
    
    def __init__(self, brain_socket='/tmp/aos_brain.sock',
                 capture_interval=2.0,
                 agent_id="camera_vision"):
        self.brain_socket = brain_socket
        self.capture_interval = capture_interval
        self.agent_id = agent_id
        
        self.running = False
        self.thread = None
        self.tick_count = 0
        
        # Camera
        self.camera = CameraVision()
        self.simulation_tick = 0
        
        # Triggers
        self.triggers: List[VisualTrigger] = []
        self._setup_triggers()
        
        # Stats
        self.stats = {
            'captures': 0,
            'real_frames': 0,
            'sim_frames': 0,
            'triggers_fired': 0,
            'hotspots_sent': 0,
            'errors': 0
        }
        
        print(f"[CameraVision] Initialized")
        print(f"  Agent: {agent_id}")
        print(f"  Interval: {capture_interval}s")
    
    def _setup_triggers(self):
        """Setup visual pattern triggers"""
        
        # Trigger 1: High motion detected
        self.triggers.append(VisualTrigger(
            name="motion_alert",
            condition=lambda f: f.get('motion_energy', 0) > 0.7,
            action="brain_alert"
        ))
        
        # Trigger 2: Bright light detected
        self.triggers.append(VisualTrigger(
            name="bright_light",
            condition=lambda f: f.get('brightness', 0.5) > 0.8,
            action="thyroid_stimulate"
        ))
        
        # Trigger 3: Red dominance (alert color)
        self.triggers.append(VisualTrigger(
            name="red_alert",
            condition=lambda f: f.get('dominant_color') == 'red' and f.get('color_intensity', 0) > 0.6,
            action="heart_accelerate"
        ))
        
        # Trigger 4: Complex pattern (novelty)
        self.triggers.append(VisualTrigger(
            name="novelty_detected",
            condition=lambda f: f.get('edge_complexity', 0) > 0.8 and f.get('texture_variance', 0) > 0.7,
            action="memory_consolidate"
        ))
        
        # Trigger 5: Darkness (low light)
        self.triggers.append(VisualTrigger(
            name="low_light",
            condition=lambda f: f.get('brightness', 0.5) < 0.2,
            action="thyroid_baseline"
        ))
        
        print(f"[CameraVision] {len(self.triggers)} triggers configured")
    
    def _send(self, cmd, params):
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
    
    def _generate_simulated_frame(self) -> Image.Image:
        """Enhanced simulation with camera-like patterns"""
        tick = self.simulation_tick
        
        # Create base
        img = Image.new('RGB', (640, 480))
        draw = ImageDraw.Draw(img)
        
        # Mode: rotating scenes
        scene_mode = tick % 5
        
        if scene_mode == 0:
            # Calm blue ocean
            for y in range(480):
                wave = int(50 + 50 * np.sin((y + tick * 2) / 30))
                draw.line([(0, y), (640, y)], fill=(20, 40, 60 + wave))
            
        elif scene_mode == 1:
            # Fiery red/orange
            for y in range(480):
                fire = int(100 + 155 * np.sin((y + tick * 5) / 50))
                draw.line([(0, y), (640, y)], fill=(fire, fire // 2, 20)])
            
        elif scene_mode == 2:
            # Green forest
            for x in range(640):
                tree = int(30 + 100 * abs(np.sin((x + tick) / 40)))
                draw.line([(x, 0), (x, 480)], fill=(20, 60 + tree, 20)])
            
        elif scene_mode == 3:
            # Bright white/light
            brightness = int(200 + 55 * np.sin(tick / 10))
            draw.rectangle([0, 0, 640, 480], fill=(brightness, brightness, brightness))
            
        else:
            # Complex pattern (for novelty trigger)
            for y in range(0, 480, 4):
                for x in range(0, 640, 4):
                    val = int(128 + 127 * np.sin(x/20 + tick) * np.cos(y/20 + tick))
                    draw.rectangle([x, y, x+3, y+3], fill=(val, 255-val, val//2))
        
        # Add motion elements
        for i in range(3):
            angle = (tick * 0.1) + (i * 2.094)
            x = 320 + int(200 * np.cos(angle))
            y = 240 + int(150 * np.sin(angle))
            r = 20 + i * 10
            color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)][i]
            draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
        
        self.simulation_tick += 1
        return img
    
    def _extract_features(self, img: Image.Image) -> Dict:
        """Extract rich visual features"""
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get pixel data
        pixels = list(img.getdata())
        r_vals = [p[0] for p in pixels]
        g_vals = [p[1] for p in pixels]
        b_vals = [p[2] for p in pixels]
        
        # Color features
        r_mean, g_mean, b_mean = np.mean(r_vals)/255, np.mean(g_vals)/255, np.mean(b_vals)/255
        r_std, g_std, b_std = np.std(r_vals)/255, np.std(g_vals)/255, np.std(b_vals)/255
        
        # Dominant color
        means = [r_mean, g_mean, b_mean]
        dominant_idx = np.argmax(means)
        colors = ['red', 'green', 'blue']
        
        # Brightness
        brightness = np.mean([r_mean, g_mean, b_mean])
        
        # Edges/texture (using filter)
        edges = img.filter(ImageFilter.FIND_EDGES)
        edge_pixels = list(edges.getdata())
        edge_strength = np.mean([sum(p)/3 for p in edge_pixels]) / 255
        
        # Texture variance
        texture_var = np.std([sum(p)/3 for p in edge_pixels]) / 255
        
        # Complexity (edge density)
        edge_density = sum(1 for p in edge_pixels if sum(p) > 100) / len(edge_pixels)
        
        # Motion energy (simulated)
        motion = 0.5 + 0.5 * np.sin(self.tick_count * 0.3)
        
        return {
            'brightness': brightness,
            'dominant_color': colors[dominant_idx],
            'color_intensity': means[dominant_idx],
            'color_variance': np.std(means),
            'edge_complexity': edge_density,
            'edge_strength': edge_strength,
            'texture_variance': texture_var,
            'motion_energy': motion,
            'r_mean': r_mean,
            'g_mean': g_mean,
            'b_mean': b_mean
        }
    
    def _encode_to_ternary(self, features: Dict, tick: int) -> List[List[int]]:
        """Encode features to 32x32x32 ternary"""
        hotspots = []
        
        # Feature vector
        vec = np.array([
            features['brightness'],
            features['color_intensity'],
            features['edge_complexity'],
            features['texture_variance'],
            features['motion_energy'],
            features['r_mean'],
            features['g_mean'],
            features['b_mean'],
            features['color_variance'],
            features['edge_strength']
        ])
        
        vec = (vec - 0.5) * 2  # Normalize to -1,1
        
        # Quantize
        ternary = np.where(vec > 0.3, 1, np.where(vec < -0.3, -1, 0))
        
        # Spatial distribution based on dominant color
        color_offsets = {'red': 0, 'green': 10, 'blue': 20}
        z_base = color_offsets.get(features['dominant_color'], 0)
        
        for i, val in enumerate(ternary):
            if val != 0:
                x = (i * 3 + tick * 7) % 32
                y = (i * 5 + tick * 13) % 32
                z = (z_base + i) % 32
                hotspots.append([int(x), int(y), int(z), int(val)])
        
        return hotspots
    
    def _check_triggers(self, features: Dict, tick: int) -> List[str]:
        """Check all triggers and return fired actions"""
        fired = []
        for trigger in self.triggers:
            if trigger.check(features, tick):
                fired.append(trigger.action)
                self.stats['triggers_fired'] += 1
                print(f"  🔥 TRIGGER: {trigger.name} -> {trigger.action}")
        return fired
    
    def _execute_action(self, action: str):
        """Execute brain action"""
        if action == "thyroid_stimulate":
            self._send('stimulate', {'importance': 0.8})
        elif action == "thyroid_baseline":
            self._send('stimulate', {'importance': 0.3})
        elif action == "heart_accelerate":
            # Would trigger heart rate increase
            pass
        elif action == "memory_consolidate":
            # Trigger cortex save
            self._send('save', {})
    
    def _capture_and_feed(self):
        """Main capture and feed cycle"""
        try:
            # Try camera first, then simulation
            img = self.camera.capture()
            if img is None:
                img = self._generate_simulated_frame()
                self.stats['sim_frames'] += 1
            else:
                self.stats['real_frames'] += 1
            
            # Extract features
            features = self._extract_features(img)
            
            # Check triggers
            actions = self._check_triggers(features, self.tick_count)
            for action in actions:
                self._execute_action(action)
            
            # Encode to ternary
            hotspots = self._encode_to_ternary(features, self.tick_count)
            
            # Priority based on triggers
            priority = 0.6 + (0.3 if actions else 0)
            
            # Send to brain
            result = self._send('cortex_write', {
                'agent_id': self.agent_id,
                'regions': list(range(8)),
                'activations': hotspots,
                'priority': priority,
                'ephemeral': False
            })
            
            self._send('cortex_tick', {})
            
            written = result.get('write_result', {}).get('written', 0)
            self.stats['hotspots_sent'] += len(hotspots)
            self.stats['captures'] += 1
            
            # Log every 10
            if self.tick_count % 10 == 0:
                mode = "SIM" if self.stats['sim_frames'] > self.stats['real_frames'] else "CAM"
                triggers = len(actions)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                      f"Tick {self.tick_count} [{mode}] "
                      f"{features['dominant_color']:5s} "
                      f"B={features['brightness']:.2f} "
                      f"M={features['motion_energy']:.2f} "
                      f"T={triggers}")
            
            self.tick_count += 1
            
        except Exception as e:
            self.stats['errors'] += 1
            print(f"[CameraVision] Error: {e}")
    
    def _run_loop(self):
        print(f"\n[CameraVision] Running...")
        print(f"  Press Ctrl+C to stop\n")
        
        while self.running:
            start = time.time()
            self._capture_and_feed()
            elapsed = time.time() - start
            sleep_time = max(0, self.capture_interval - elapsed)
            time.sleep(sleep_time)
    
    def start(self):
        if self.running:
            return
        
        # Try to open camera
        self.camera.open()
        
        # Register
        print("[CameraVision] Registering with brain...")
        self._send('cortex_register', {'agent_id': self.agent_id})
        
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print(f"[CameraVision] Started (interval: {self.capture_interval}s)")
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        self.camera.close()
        
        print(f"\n[CameraVision] Stopped")
        print(f"  Captures: {self.stats['captures']}")
        print(f"  Real frames: {self.stats['real_frames']}")
        print(f"  Sim frames: {self.stats['sim_frames']}")
        print(f"  Triggers: {self.stats['triggers_fired']}")
        print(f"  Hotspots: {self.stats['hotspots_sent']}")

def main():
    daemon = CameraVisionDaemon(capture_interval=2.0)
    daemon.start()
    
    try:
        while daemon.running:
            time.sleep(1)
    except KeyboardInterrupt:
        daemon.stop()

if __name__ == "__main__":
    main()
