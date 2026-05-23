#!/usr/bin/env python3
"""
TracRay - Memory Trajectory and Replay System
Ported from legacy brain architecture
"""

import time
import json
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import deque
from pathlib import Path
import numpy as np


@dataclass
class TrajectoryPoint:
    """A point in memory trajectory"""
    timestamp: float
    tick: int
    phase: str
    limbic_state: Dict
    observation: str
    action: str
    novelty: float
    reward: float
    
    def to_vector(self) -> np.ndarray:
        """Convert to feature vector for trajectory analysis"""
        return np.array([
            self.tick,
            self.novelty,
            self.reward,
            self.limbic_state.get("arousal", 0.5),
            self.limbic_state.get("coherence", 0.5),
            self.limbic_state.get("valence", 0.0),
            hash(self.action) % 1000 / 1000.0  # Action encoding
        ])


class TracRay:
    """
    Trajectory Analysis and Replay System
    
    Captures and analyzes the brain's trajectory through state space.
    Enables:
    - Trajectory replay for learning
    - Pattern detection in state evolution
    - Path analysis for decision optimization
    """
    
    def __init__(self, capacity: int = 10000, state_path: Optional[Path] = None):
        self.capacity = capacity
        self.state_path = state_path or Path.home() / ".aos" / "brain" / "state" / "tracray.json"
        
        # Trajectory storage
        self.trajectory: deque = deque(maxlen=capacity)
        self.episodes: List[List[TrajectoryPoint]] = []
        
        # Current episode
        self.current_episode: List[TrajectoryPoint] = []
        
        # Pattern cache
        self.detected_patterns: Dict[str, List] = {}
        
        print(f"[TracRay] Initialized with capacity {capacity}")
        self._load_state()
    
    def record(self, tick: int, phase: str, limbic: Dict, 
               observation: str, action: str) -> TrajectoryPoint:
        """Record a trajectory point"""
        point = TrajectoryPoint(
            timestamp=time.time(),
            tick=tick,
            phase=phase,
            limbic_state=limbic.copy(),
            observation=observation[:100],  # Truncate
            action=action[:50],
            novelty=limbic.get("novelty", 0.5),
            reward=limbic.get("reward", 0.3)
        )
        
        self.trajectory.append(point)
        self.current_episode.append(point)
        
        return point
    
    def end_episode(self, reason: str = "tick_limit"):
        """End current episode and store it"""
        if len(self.current_episode) > 10:  # Minimum episode length
            self.episodes.append(self.current_episode.copy())
            print(f"[TracRay] Episode ended: {len(self.current_episode)} points ({reason})")
        
        self.current_episode = []
        self._save_state()
    
    def analyze_trajectory(self, n_points: int = 100) -> Dict:
        """Analyze recent trajectory"""
        if len(self.trajectory) < n_points:
            n_points = len(self.trajectory)
        
        recent = list(self.trajectory)[-n_points:]
        
        # Convert to vectors
        vectors = np.array([p.to_vector() for p in recent])
        
        # Calculate trajectory statistics
        mean_position = np.mean(vectors, axis=0)
        velocity = np.diff(vectors[:, :2], axis=0) if len(vectors) > 1 else np.zeros((1, 2))
        mean_velocity = np.mean(np.linalg.norm(velocity, axis=1)) if len(velocity) > 0 else 0
        
        # Novelty trend
        novelty_values = [p.novelty for p in recent]
        novelty_trend = "increasing" if novelty_values[-1] > novelty_values[0] else "decreasing"
        
        return {
            "mean_position": mean_position.tolist(),
            "mean_velocity": float(mean_velocity),
            "novelty_trend": novelty_trend,
            "novelty_mean": float(np.mean(novelty_values)),
            "novelty_std": float(np.std(novelty_values)),
            "reward_mean": float(np.mean([p.reward for p in recent])),
            "phase_distribution": self._count_phases(recent)
        }
    
    def _count_phases(self, points: List[TrajectoryPoint]) -> Dict[str, int]:
        """Count phase distribution"""
        phases = {}
        for p in points:
            phases[p.phase] = phases.get(p.phase, 0) + 1
        return phases
    
    def detect_cycles(self, min_length: int = 4) -> List[Dict]:
        """Detect cyclic patterns in trajectory"""
        if len(self.trajectory) < min_length * 2:
            return []
        
        cycles = []
        points = list(self.trajectory)
        
        # Simple cycle detection via phase sequence matching
        phase_seq = [p.phase for p in points]
        
        for i in range(len(phase_seq) - min_length * 2):
            pattern = tuple(phase_seq[i:i+min_length])
            for j in range(i + min_length, len(phase_seq) - min_length):
                if tuple(phase_seq[j:j+min_length]) == pattern:
                    cycles.append({
                        "start": i,
                        "end": j,
                        "pattern": pattern,
                        "period": j - i
                    })
        
        return cycles[:5]  # Return top 5 cycles
    
    def replay_episode(self, episode_idx: int = -1, speed: float = 1.0) -> List[TrajectoryPoint]:
        """Replay an episode"""
        if not self.episodes:
            return []
        
        episode = self.episodes[episode_idx]
        print(f"[TracRay] Replaying episode with {len(episode)} points")
        
        for point in episode:
            print(f"  Tick {point.tick}: {point.phase} | {point.action[:30]}...")
            if speed > 0:
                time.sleep(0.1 / speed)
        
        return episode
    
    def predict_next(self, n_recent: int = 10) -> Dict:
        """Predict next state based on trajectory"""
        if len(self.trajectory) < n_recent:
            return {"prediction": "insufficient_data"}
        
        recent = list(self.trajectory)[-n_recent:]
        phases = [p.phase for p in recent]
        rewards = [p.reward for p in recent]
        
        # Simple prediction: phase transition probability
        phase_transitions = {}
        for i in range(len(phases) - 1):
            key = f"{phases[i]}->{phases[i+1]}"
            phase_transitions[key] = phase_transitions.get(key, 0) + 1
        
        # Most likely next phase
        current_phase = phases[-1]
        next_probs = {}
        for key, count in phase_transitions.items():
            if key.startswith(current_phase):
                next_phase = key.split("->")[1]
                next_probs[next_phase] = next_probs.get(next_phase, 0) + count
        
        # Normalize
        total = sum(next_probs.values()) if next_probs else 1
        for phase in next_probs:
            next_probs[phase] /= total
        
        return {
            "current_phase": current_phase,
            "likely_next": max(next_probs.items(), key=lambda x: x[1])[0] if next_probs else "unknown",
            "next_probabilities": next_probs,
            "reward_trend": "improving" if rewards[-1] > rewards[0] else "declining"
        }
    
    def _save_state(self):
        """Save trajectory state"""
        try:
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            state = {
                "episodes": len(self.episodes),
                "trajectory_points": len(self.trajectory),
                "timestamp": time.time()
            }
            with open(self.state_path, 'w') as f:
                json.dump(state, f)
        except Exception as e:
            print(f"[TracRay] Save error: {e}")
    
    def _load_state(self):
        """Load trajectory state"""
        if self.state_path.exists():
            try:
                with open(self.state_path) as f:
                    data = json.load(f)
                    print(f"[TracRay] Loaded state: {data.get('trajectory_points', 0)} points")
            except:
                pass
    
    def get_stats(self) -> Dict:
        """Get TracRay statistics"""
        return {
            "total_points": len(self.trajectory),
            "episodes": len(self.episodes),
            "current_episode_length": len(self.current_episode),
            "capacity": self.capacity,
            "utilization": len(self.trajectory) / self.capacity
        }


if __name__ == "__main__":
    print("=" * 70)
    print("  TRACRAY TEST")
    print("=" * 70)
    
    tracray = TracRay(capacity=1000)
    
    # Record test trajectory
    print("\nRecording test trajectory...")
    for i in range(20):
        limbic = {
            "novelty": 0.3 + (i * 0.03),
            "reward": 0.5 + (i % 5) * 0.1,
            "arousal": 0.5,
            "coherence": 0.6
        }
        phase = ["Observe", "Orient", "Decide", "Act"][i % 4]
        tracray.record(
            tick=i,
            phase=phase,
            limbic=limbic,
            observation=f"Test observation {i}",
            action=f"Test action {i}"
        )
    
    # Analyze
    print("\nAnalyzing trajectory...")
    analysis = tracray.analyze_trajectory(n_points=20)
    print(f"  Mean velocity: {analysis['mean_velocity']:.3f}")
    print(f"  Novelty trend: {analysis['novelty_trend']}")
    print(f"  Phase distribution: {analysis['phase_distribution']}")
    
    # Detect cycles
    print("\nDetecting cycles...")
    cycles = tracray.detect_cycles()
    print(f"  Found {len(cycles)} cycles")
    
    # Predict
    print("\nPredicting next state...")
    prediction = tracray.predict_next(n_recent=10)
    print(f"  Current phase: {prediction['current_phase']}")
    print(f"  Likely next: {prediction['likely_next']}")
    
    print("\n" + "=" * 70)
