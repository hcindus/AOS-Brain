#!/usr/bin/env python3
"""
Vision Module for Ternary Brain - Camera/Visual Processing.

Provides:
- Camera capture and frame processing
- Object detection and recognition
- Visual pattern matching
- Integration with 7-region brain
- Spatial understanding (coordinate with Tracray)

Requirements:
- opencv-python (cv2)
- numpy
- PIL (optional)

Features:
- Real-time video capture
- Frame preprocessing
- Motion detection
- Object tracking
- Visual memory storage
"""

import os
import sys
import json
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from collections import deque

# Try to import OpenCV
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("[Warning] OpenCV not available, vision module in stub mode")


@dataclass
class VisionConfig:
    """Configuration for vision processing."""
    camera_id: int = 0  # Default camera
    width: int = 640
    height: int = 480
    fps: int = 30
    enable_motion: bool = True
    enable_recognition: bool = True
    memory_size: int = 100  # Frames to keep in memory


class VisionProcessor:
    """
    Vision processor for the ternary brain.
    
    Handles:
    - Camera capture
    - Frame preprocessing
    - Object detection
    - Visual memory
    - Spatial mapping
    """
    
    def __init__(self, brain=None, config: Optional[VisionConfig] = None):
        self.brain = brain
        self.config = config or VisionConfig()
        
        # Camera
        self.camera = None
        self.is_running = False
        self.capture_thread = None
        
        # Memory
        self.frame_buffer = deque(maxlen=self.config.memory_size)
        self.visual_memories = {}
        
        # Processing
        self.last_frame = None
        self.motion_detected = False
        self.detected_objects = []
        
        # Initialize if OpenCV available
        if CV2_AVAILABLE:
            self._init_camera()
    
    def _init_camera(self):
        """Initialize camera capture."""
        if not CV2_AVAILABLE:
            return False
        
        try:
            self.camera = cv2.VideoCapture(self.config.camera_id)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.height)
            self.camera.set(cv2.CAP_PROP_FPS, self.config.fps)
            
            if self.camera.isOpened():
                print(f"[Vision] Camera initialized: {self.config.width}x{self.config.height}")
                return True
            else:
                print("[Vision] Failed to open camera")
                return False
        except Exception as e:
            print(f"[Vision] Camera error: {e}")
            return False
    
    def capture_frame(self) -> Optional[Any]:
        """Capture single frame from camera."""
        if not CV2_AVAILABLE or not self.camera:
            return None
        
        ret, frame = self.camera.read()
        if ret:
            self.last_frame = frame
            self.frame_buffer.append({
                "frame": frame,
                "timestamp": time.time(),
            })
            return frame
        return None
    
    def detect_motion(self, frame: Any, threshold: int = 25) -> bool:
        """Detect motion between frames."""
        if not CV2_AVAILABLE or self.last_frame is None:
            return False
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        last_gray = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate difference
        diff = cv2.absdiff(gray, last_gray)
        _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
        
        # Count changed pixels
        motion_pixels = cv2.countNonZero(thresh)
        self.motion_detected = motion_pixels > 1000  # Threshold
        
        return self.motion_detected
    
    def detect_objects(self, frame: Any) -> List[Dict]:
        """Simple object detection using contours."""
        if not CV2_AVAILABLE:
            return []
        
        # Convert to grayscale and blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        objects = []
        for i, contour in enumerate(contours):
            if cv2.contourArea(contour) > 500:  # Filter small contours
                x, y, w, h = cv2.boundingRect(contour)
                objects.append({
                    "id": i,
                    "x": x, "y": y,
                    "width": w, "height": h,
                    "area": cv2.contourArea(contour),
                })
        
        self.detected_objects = objects
        return objects
    
    def process_visual_input(self) -> Dict:
        """
        Process visual input and return structured data.
        
        Returns:
            Dict with visual observations for brain
        """
        if not CV2_AVAILABLE:
            return {"error": "OpenCV not available", "input_type": "visual_stub"}
        
        frame = self.capture_frame()
        if frame is None:
            return {"error": "No frame captured", "input_type": "visual"}
        
        # Process frame
        motion = self.detect_motion(frame) if self.config.enable_motion else False
        objects = self.detect_objects(frame) if self.config.enable_recognition else []
        
        # Create observation
        observation = {
            "input_type": "visual",
            "timestamp": time.time(),
            "frame_shape": frame.shape,
            "motion_detected": motion,
            "object_count": len(objects),
            "objects": objects,
            "brightness": np.mean(frame),
        }
        
        # Store in visual memory
        memory_key = f"frame_{int(time.time() * 1000)}"
        self.visual_memories[memory_key] = observation
        
        return observation
    
    def start_capture(self):
        """Start continuous capture in background thread."""
        if self.is_running:
            return
        
        self.is_running = True
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
        print("[Vision] Capture started")
    
    def _capture_loop(self):
        """Background capture loop."""
        while self.is_running:
            self.process_visual_input()
            time.sleep(0.033)  # ~30 FPS
    
    def stop_capture(self):
        """Stop capture."""
        self.is_running = False
        if self.capture_thread:
            self.capture_thread.join(timeout=1.0)
        
        if self.camera:
            self.camera.release()
        
        print("[Vision] Capture stopped")
    
    def get_last_frame(self) -> Optional[Any]:
        """Get last captured frame."""
        return self.last_frame
    
    def get_visual_memory(self, limit: int = 10) -> List[Dict]:
        """Get recent visual memories."""
        sorted_memories = sorted(
            self.visual_memories.items(),
            key=lambda x: x[1]["timestamp"],
            reverse=True
        )
        return [mem for _, mem in sorted_memories[:limit]]
    
    def save_frame(self, filename: str = None) -> str:
        """Save current frame to file."""
        if not CV2_AVAILABLE or self.last_frame is None:
            return ""
        
        if filename is None:
            filename = f"frame_{int(time.time())}.jpg"
        
        path = Path.home() / ".aos" / "vision" / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        
        cv2.imwrite(str(path), self.last_frame)
        return str(path)


class VisionBrainIntegration:
    """
    Integration between VisionProcessor and SevenRegionBrain.
    
    Connects visual input to the OODA loop.
    """
    
    def __init__(self, brain):
        self.brain = brain
        self.vision = VisionProcessor(brain)
        
    def feed_visual_to_brain(self) -> Dict:
        """
        Capture visual input and feed to brain.
        
        Returns:
            Brain state after processing visual input
        """
        # Get visual observation
        visual_obs = self.vision.process_visual_input()
        
        # Feed to brain as sensory input
        brain_input = {
            "text": f"[Visual] Motion: {visual_obs.get('motion_detected', False)}, Objects: {visual_obs.get('object_count', 0)}",
            "source": "vision",
            "visual_data": visual_obs,
        }
        
        # Process through brain
        if self.brain:
            return self.brain.tick(brain_input)
        
        return {"status": "no_brain", "visual": visual_obs}
    
    def start_vision_loop(self):
        """Start continuous vision-brain loop."""
        self.vision.start_capture()
        print("[VisionBrain] Vision loop started")
    
    def stop_vision_loop(self):
        """Stop vision loop."""
        self.vision.stop_capture()
        print("[VisionBrain] Vision loop stopped")


def test_vision():
    """Test vision module."""
    print("=" * 70)
    print("👁️ VISION MODULE TEST")
    print("=" * 70)
    print()
    
    if not CV2_AVAILABLE:
        print("❌ OpenCV not available. Install with: pip install opencv-python")
        return
    
    vision = VisionProcessor()
    
    print("Testing camera...")
    frame = vision.capture_frame()
    
    if frame is not None:
        print(f"✅ Frame captured: {frame.shape}")
        
        # Test motion detection
        print("Testing motion detection...")
        motion = vision.detect_motion(frame)
        print(f"   Motion detected: {motion}")
        
        # Test object detection
        print("Testing object detection...")
        objects = vision.detect_objects(frame)
        print(f"   Objects found: {len(objects)}")
        for obj in objects[:5]:  # Show first 5
            print(f"     - Object {obj['id']}: {obj['width']}x{obj['height']} at ({obj['x']}, {obj['y']})")
        
        # Test visual input
        print("Testing visual input processing...")
        obs = vision.process_visual_input()
        print(f"   Observation keys: {list(obs.keys())}")
        
        print()
        print("✅ Vision module working!")
    else:
        print("⚠️ No camera available or camera access denied")
        print("   Vision module loaded in stub mode")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    test_vision()
