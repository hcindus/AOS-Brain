#!/usr/bin/env python3
"""
Visual Cortex - Three-Stream Vision System for Ternary Brain
============================================================
V1: Geometry & Motion ("Where/How")
V2: Objects & Affordances ("What/Can-Do")  
V3: Narrative & Prediction ("When/Why")

Designed for DOOM but generalizable to any visual input.
"""

import sys
import time
import math
import random
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple

# Optional: OpenCV for geometry
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False


# ═══════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════

@dataclass
class Object:
    """Detected object in scene"""
    id: int
    class_name: str  # "enemy", "health", "ammo", "wall", "door", "projectile"
    bbox: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    position_3d: Optional[Tuple[float, float, float]] = None
    velocity: Tuple[float, float, float] = (0, 0, 0)
    affordances: Set[str] = field(default_factory=set)
    confidence: float = 1.0
    last_seen: float = field(default_factory=time.time)
    trajectory: List[Tuple[float, float, float]] = field(default_factory=list)


@dataclass  
class SceneGraph:
    """Spatial relations between objects"""
    nodes: Dict[int, str] = field(default_factory=dict)  # object_id -> class
    edges: Dict[Tuple[int, int], str] = field(default_factory=dict)  # (from, to) -> relation


# ═══════════════════════════════════════════════════════════════════
# AFFORDANCE MAP (Domain Knowledge)
# ═══════════════════════════════════════════════════════════════════

AFFORDANCE_MAP = {
    "enemy": {"shootable", "danger", "moving"},
    "health": {"pickup", "healing", "static"},
    "ammo": {"pickup", "static"},
    "wall": {"cover", "blocking", "static"},
    "door": {"openable", "blocking"},
    "projectile": {"danger", "moving"},
    "agent": {"self"},
}


# ═══════════════════════════════════════════════════════════════════
# V1: GEOMETRY & MOTION
# ═══════════════════════════════════════════════════════════════════

class GeometryMotionV1:
    """
    V1 Stream: Geometry & Motion ("Where/How")
    - Edge/orientation detection
    - Optical flow / motion vectors
    - Ego-motion estimation
    - Free space map
    """
    
    def __init__(self, width=320, height=240):
        self.width = width
        self.height = height
        self.last_frame = None
        self.ego_motion = (0.0, 0.0, 0.0)  # dx, dy, dtheta
        self.motion_field = []
        self.free_space = []  # regions where agent can move
        
    def process(self, frame) -> Dict:
        """
        Process frame, return geometry + motion features.
        """
        result = {
            "ego_motion": self.ego_motion,
            "motion_field": self.motion_field,
            "free_space": self.free_space,
            "edges": [],
            "moving_regions": [],
        }
        
        if not HAS_CV2 or frame is None:
            # Fallback: random but consistent
            result["ego_motion"] = (random.uniform(-1, 1), random.uniform(-1, 1), 0)
            return result
        
        # Convert to grayscale
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        else:
            gray = frame
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        result["edges"] = edges
        
        # Optical flow (if we have last frame)
        if self.last_frame is not None:
            flow = cv2.calcOpticalFlowFarneback(
                self.last_frame, gray, None,
                0.5, 3, 15, 3, 5, 1.2, 0
            )
            
            # Extract motion vectors
            h, w = flow.shape[:2]
            flow_uv = flow[int(h/4):int(3*h/4), int(w/4):int(3*w/4)]
            fx, fy = flow_uv[..., 0].mean(), flow_uv[..., 1].mean()
            result["ego_motion"] = (float(fx), float(fy), 0)
            
            # Motion regions
            magnitude = cv2.magnitude(flow[..., 0], flow[..., 1])
            moving = magnitude > 2.0
            result["moving_regions"] = moving.tolist()
        
        self.last_frame = gray
        self.ego_motion = result["ego_motion"]
        
        # Simple free space: bottom half of image
        result["free_space"] = [(0, self.height//2, self.width, self.height)]
        
        return result


# ═══════════════════════════════════════════════════════════════════
# V2: OBJECTS & AFFORDANCES
# ═══════════════════════════════════════════════════════════════════

class ObjectsAffordancesV2:
    """
    V2 Stream: Objects & Affordances ("What/Can-Do")
    - Object detection / classification
    - Track objects across frames
    - Attach affordances
    """
    
    def __init__(self):
        self.objects = {}  # id -> Object
        self.next_id = 0
        self.tracked_classes = ["enemy", "health", "ammo", "wall", "projectile"]
        
    def detect_and_track(self, frame, geom_out) -> List[Object]:
        """
        Detect objects and track across frames.
        For DOOM: uses game variables + simple color detection.
        """
        detected = []
        
        # Simplified: create synthetic objects based on motion
        # In real implementation: YOLO, color blobs, or game API
        
        moving_regions = geom_out.get("moving_regions", [])
        
        # If there's significant motion, assume enemy
        if moving_regions and random.random() > 0.5:
            obj = Object(
                id=self._get_next_id(),
                class_name="enemy",
                bbox=(100, 80, 220, 160),
                affordances=AFFORDANCE_MAP.get("enemy", set()),
                confidence=0.8,
            )
            detected.append(obj)
        
        # Random health/ammo for demo
        if random.random() > 0.7:
            obj = Object(
                id=self._get_next_id(),
                class_name="health",
                bbox=(150, 100, 170, 120),
                affordances=AFFORDANCE_MAP.get("health", set()),
                confidence=0.9,
            )
            detected.append(obj)
        
        # Always have some walls
        obj = Object(
            id=self._get_next_id(),
            class_name="wall",
            bbox=(0, 0, 320, 60),  # top
            affordances=AFFORDANCE_MAP.get("wall", set()),
            confidence=1.0,
        )
        detected.append(obj)
        
        # Update tracked objects
        self.objects = {o.id: o for o in detected}
        
        return detected
    
    def _get_next_id(self) -> int:
        self.next_id += 1
        return self.next_id


# ═══════════════════════════════════════════════════════════════════
# V3: NARRATIVE & PREDICTION
# ═══════════════════════════════════════════════════════════════════

class NarrativePredictionV3:
    """
    V3 Stream: Narrative & Prediction ("When/Why")
    - Track object trajectories
    - Predict next positions
    - Detect threat timelines
    - Generate surprise signals
    """
    
    def __init__(self):
        self.object_history = defaultdict(lambda: deque(maxlen=30))
        self.predictions = {}
        self.threat_timeline = []
        self.surprise = 0.0
        
    def update(self, objects: List[Object], geom_out: Dict, time_t: float) -> Dict:
        """
        Update narratives and predictions from detected objects.
        """
        result = {
            "predictions": {},
            "threat_timeline": [],
            "surprise": 0.0,
            "event_hypotheses": [],
        }
        
        # Track trajectories
        for obj in objects:
            # Update history
            pos = self._bbox_center(obj.bbox)
            self.object_history[obj.id].append((pos[0], pos[1], time_t))
            
            # Simple linear prediction
            history = list(self.object_history[obj.id])
            if len(history) >= 2:
                # Velocity estimate
                dx = history[-1][0] - history[-2][0]
                dy = history[-1][1] - history[-2][1]
                
                # Predict next position (2 frames ahead)
                pred_x = history[-1][0] + dx * 2
                pred_y = history[-1][1] + dy * 2
                
                self.predictions[obj.id] = (pred_x, pred_y, time_t + 0.1)
        
        result["predictions"] = self.predictions
        
        # Threat timeline: enemies moving toward center
        for obj in objects:
            if obj.class_name == "enemy":
                cx, cy = self._bbox_center(obj.bbox)
                # Moving toward agent (center of screen)?
                if abs(cx - 160) < 80 and abs(cy - 120) < 60:
                    result["threat_timeline"].append({
                        "object_id": obj.id,
                        "time_to_impact": 1.0,  # frames
                        "severity": "high",
                    })
        
        result["threat_timeline"] = self.threat_timeline
        
        # Surprise: prediction error
        # (simplified: random for demo)
        self.surprise = random.random() * 0.2 if random.random() > 0.8 else 0.0
        result["surprise"] = self.surprise
        
        # Event hypotheses
        if len(self.threat_timeline) > 0:
            result["event_hypotheses"].append("ambush_detected")
        
        return result
    
    def _bbox_center(self, bbox) -> Tuple[float, float]:
        return ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)


# ═══════════════════════════════════════════════════════════════════
# BUILD SCENE GRAPH
# ═══════════════════════════════════════════════════════════════

def build_scene_graph(objects: List[Object], geom_out: Dict) -> SceneGraph:
    """
    Build spatial relations between objects.
    Connects to your existing semantic graph.
    """
    graph = SceneGraph()
    
    # Add nodes
    for obj in objects:
        graph.nodes[obj.id] = obj.class_name
    
    # Add edges based on spatial relations
    agent_pos = (160, 120)  # Center of screen
    
    for obj in objects:
        cx, cy = ((obj.bbox[0] + obj.bbox[2]) / 2, 
                  (obj.bbox[1] + obj.bbox[3]) / 2)
        
        # In front of agent
        if cy < agent_pos[1]:
            graph.edges[(obj.id, -1)] = "in_front_of"
            graph.edges[(-1, obj.id)] = "behind"
        
        # Blocking
        if obj.class_name in ["wall", "door"]:
            graph.edges[(obj.id, -1)] = "blocking"
        
        # Danger relations
        if "danger" in obj.affordances:
            graph.edges[(obj.id, -1)] = "threat"
    
    return graph


# ═══════════════════════════════════════════════════════════════════
# MAIN VISUAL CORTEX
# ═══════════════════════════════════════════════════════════════════

class VisualCortex:
    """
    Three-Stream Visual Cortex for Ternary Brain
    
    Processes frames through V1 → V2 → V3 and exports
    structured perception for higher layers.
    """
    
    def __init__(self, width=320, height=240):
        self.width = width
        self.height = height
        self.time = 0.0
        
        # Initialize three streams
        self.v1 = GeometryMotionV1(width, height)
        self.v2 = ObjectsAffordancesV2()
        self.v3 = NarrativePredictionV3()
        
        # Shared state
        self.objects = []
        self.scene_graph = SceneGraph()
        self.predictions = {}
        
    def process_frame(self, frame) -> Dict:
        """
        Main perception loop (per frame):
        1. V1: Geometry & motion
        2. V2: Objects & affordances  
        3. V3: Narrative & prediction
        4. Build scene graph
        5. Export for Brain
        """
        self.time += 1.0 / 30.0  # Assume 30fps
        
        # V1: Geometry & motion
        geom_out = self.v1.process(frame)
        
        # V2: Objects & affordances
        objects = self.v2.detect_and_track(frame, geom_out)
        
        # V3: Narrative & prediction
        narr_out = self.v3.update(objects, geom_out, self.time)
        
        # Scene graph
        scene_graph = build_scene_graph(objects, geom_out)
        
        # Update shared state
        self.objects = objects
        self.scene_graph = scene_graph
        self.predictions = narr_out["predictions"]
        
        # Export for higher layers
        return self._export_perception(objects, scene_graph, geom_out, narr_out)
    
    def _export_perception(self, objects, scene_graph, geom_out, narr_out) -> Dict:
        """
        Export structured perception for Brain.
        """
        # Extract symbolic features (for RL)
        enemy_visible = any(o.class_name == "enemy" for o in objects)
        health_visible = any(o.class_name == "health" for o in objects)
        ammo_visible = any(o.class_name == "ammo" for o in objects)
        
        # Threat assessment
        threat_level = len(narr_out.get("threat_timeline", [])) / max(len(objects), 1)
        
        return {
            # Raw objects
            "objects": [
                {
                    "id": o.id,
                    "class": o.class_name,
                    "bbox": o.bbox,
                    "affordances": list(o.affordances),
                    "confidence": o.confidence,
                }
                for o in objects
            ],
            # Scene graph
            "scene_graph": {
                "nodes": scene_graph.nodes,
                "edges": {f"{k[0]}-{k[1]}": v for k, v in scene_graph.edges.items()},
            },
            # Symbolic features (for RL)
            "enemy_visible": enemy_visible,
            "health_visible": health_visible,
            "ammo_visible": ammo_visible,
            "danger_level": threat_level,
            "moving_count": len([o for o in objects if "moving" in o.affordances]),
            # Geometry
            "ego_motion": geom_out["ego_motion"],
            "free_space": geom_out["free_space"],
            # Narrative
            "predictions": narr_out["predictions"],
            "threat_timeline": narr_out["threat_timeline"],
            "surprise": narr_out["surprise"],
            "event_hypotheses": narr_out.get("event_hypotheses", []),
        }


# ═══════════════════════════════════════════════════════════════════
# INTEGRATION WITH RL
# ═══════════════════════════════════════════════════════════════════

def perception_to_rl_state(perception: Dict) -> Dict:
    """
    Convert visual cortex output to RL state.
    """
    return {
        "enemy_visible": perception.get("enemy_visible", 0),
        "health_visible": perception.get("health_visible", 0),
        "ammo_visible": perception.get("ammo_visible", 0),
        "danger_level": perception.get("danger_level", 0),
        "moving_count": perception.get("moving_count", 0),
        "surprise": perception.get("surprise", 0),
    }


# ═══════════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🧠 Testing Visual Cortex...")
    
    # Create cortex
    cortex = VisualCortex()
    
    # Simulate frames
    for i in range(5):
        # Create dummy frame (240x320x3)
        import numpy as np
        frame = np.random.randint(0, 255, (240, 320, 3), dtype=np.uint8)
        
        # Process
        perception = cortex.process_frame(frame)
        
        print(f"\n📹 Frame {i}:")
        print(f"   Objects: {[o['class'] for o in perception['objects']]}")
        print(f"   Enemy: {perception['enemy_visible']} | Health: {perception['health_visible']}")
        print(f"   Danger: {perception['danger_level']:.2f} | Surprise: {perception['surprise']:.2f}")
        print(f"   Events: {perception['event_hypotheses']}")
    
    print("\n✅ Visual Cortex test complete!")