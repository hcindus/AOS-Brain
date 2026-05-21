#!/usr/bin/env python3
"""
AOS Vision Manager - Camera/Visual Processing
Ported from legacy brain to Ternary System
"""

import os
import time
import threading
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from collections import deque

# Try to import OpenCV
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("[Warning] OpenCV not available, vision in stub mode")


@dataclass
class VisionFrame:
    """Processed vision frame"""
    timestamp: float
    width: int
    height: int
    data: bytes
    features: Dict  # Detected features
    motion_score: float  # 0-1


class VisionManager:
    """
    Vision processing for Ternary Brain
    Ported from legacy brain architecture
    """
    
    def __init__(self, camera_id: int = 0, width: int = 640, height: int = 480):
        self.camera_id = camera_id
        self.width = width
        self.height = height
        
        self.cap = None
        self.is_running = False
        self.frame_buffer: deque = deque(maxlen=30)  # 1 second at 30fps
        
        # Motion detection
        self.prev_frame = None
        self.motion_threshold = 20
        
        # Feature detection
        self.features_detected = 0
        
        print(f"[VisionManager] Initialized ({width}x{height})")
        if not CV2_AVAILABLE:
            print("[VisionManager] Running in stub mode (no OpenCV)")
    
    def open(self) -> bool:
        """Open camera"""
        if not CV2_AVAILABLE:
            return False
        
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            
            if self.cap.isOpened():
                print(f"[VisionManager] Camera opened")
                return True
        except:
            pass
        
        print("[VisionManager] Failed to open camera")
        return False
    
    def capture_frame(self) -> Optional[VisionFrame]:
        """Capture and process single frame"""
        if not CV2_AVAILABLE or not self.cap:
            # Generate stub frame
            return VisionFrame(
                timestamp=time.time(),
                width=self.width,
                height=self.height,
                data=b"stub_frame",
                features={"stub": True},
                motion_score=0.0
            )
        
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Process frame
        processed = self._process_frame(frame)
        
        # Detect motion
        motion = self._detect_motion(frame)
        
        # Extract features
        features = self._extract_features(frame)
        
        vision_frame = VisionFrame(
            timestamp=time.time(),
            width=frame.shape[1],
            height=frame.shape[0],
            data=processed.tobytes(),
            features=features,
            motion_score=motion
        )
        
        # Add to buffer
        self.frame_buffer.append(vision_frame)
        
        return vision_frame
    
    def _process_frame(self, frame):
        """Process raw frame"""
        if not CV2_AVAILABLE:
            return frame
        
        import numpy as np
        
        # Convert to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Resize
        resized = cv2.resize(rgb, (self.width, self.height))
        
        return resized
    
    def _detect_motion(self, frame) -> float:
        """Detect motion in frame"""
        if not CV2_AVAILABLE:
            return 0.0
        
        import numpy as np
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if self.prev_frame is None:
            self.prev_frame = gray
            return 0.0
        
        # Calculate difference
        frame_delta = cv2.absdiff(self.prev_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        
        motion = np.sum(thresh) / 255.0
        motion_score = min(1.0, motion / (self.width * self.height * 0.1))
        
        self.prev_frame = gray
        return motion_score
    
    def _extract_features(self, frame) -> Dict:
        """Extract visual features"""
        features = {
            "brightness": 0.5,
            "contrast": 0.5,
            "color_dominant": "unknown",
            "edges": 0.0,
            "objects": []
        }
        
        if not CV2_AVAILABLE:
            return features
        
        import numpy as np
        
        # Calculate brightness
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        features["brightness"] = np.mean(gray) / 255.0
        
        # Calculate contrast
        features["contrast"] = np.std(gray) / 128.0
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        features["edges"] = np.sum(edges > 0) / (frame.shape[0] * frame.shape[1])
        
        return features
    
    def get_visual_summary(self) -> str:
        """Get summary of recent visual input"""
        if not self.frame_buffer:
            return "No visual input"
        
        recent = list(self.frame_buffer)[-10:]
        avg_motion = sum(f.motion_score for f in recent) / len(recent)
        
        return f"Visual: {len(self.frame_buffer)} frames buffered, avg_motion={avg_motion:.2f}"
    
    def get_status(self) -> Dict:
        """Get vision status"""
        return {
            "running": self.is_running,
            "buffer_size": len(self.frame_buffer),
            "camera": self.camera_id if self.cap else None,
            "opencv": CV2_AVAILABLE
        }
    
    def close(self):
        """Close camera"""
        if self.cap:
            self.cap.release()
            print("[VisionManager] Camera closed")


class VisionInterface:
    """
    High-level vision interface for Ternary Brain
    """
    
    def __init__(self):
        self.vision_manager = VisionManager()
        self.enabled = CV2_AVAILABLE
        
    def observe(self) -> Optional[str]:
        """Get visual observation for brain"""
        if not self.enabled:
            return "Vision not available"
        
        if not self.vision_manager.open():
            return "Camera not available"
        
        frame = self.vision_manager.capture_frame()
        if frame is None:
            return "No visual input"
        
        # Convert to text description for brain
        features = frame.features
        
        desc = f"Visual: brightness={features['brightness']:.2f}, "
        desc += f"motion={frame.motion_score:.2f}, "
        desc += f"contrast={features['contrast']:.2f}"
        
        return desc
    
    def start_continuous(self):
        """Start continuous capture"""
        if self.enabled:
            self.vision_manager.open()
            print("[Vision] Continuous capture started")


if __name__ == "__main__":
    print("=" * 70)
    print("  AOS Vision Manager - Test")
    print("=" * 70)
    
    vision = VisionInterface()
    
    print(f"\nOpenCV available: {CV2_AVAILABLE}")
    print(f"Camera status: {vision.vision_manager.get_status()}")
    
    if CV2_AVAILABLE:
        print("\nAttempting to capture frame...")
        observation = vision.observe()
        print(f"Observation: {observation}")
    else:
        print("\nVision in stub mode (no OpenCV)")
    
    print("=" * 70)
