#!/usr/bin/env python3
"""
7-Region Ternary Brain - Complete architecture with sensory/motor integration.

Regions:
1. Thalamus (sensory relay)
2. Hippocampus (episodic memory)
3. Amygdala/Limbic (affect/emotion)
4. PFC (planning/decision)
5. Basal Ganglia (action selection)
6. Cerebellum (motor coordination)
7. Brainstem (safety/life support)

Plus: Auto-feeder for equations and data
"""

import os
import sys
import json
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import deque

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'AOS' / 'brain'))

# Import Tracray for spatial concept mapping
try:
    from core.tracray_lexicon import TracrayLexicon
    TRACRAY_AVAILABLE = True
except ImportError:
    TRACRAY_AVAILABLE = False
    print("[Warning] Tracray not available, using fallback mode")

class SevenRegionBrain:
    """
    Complete 7-region brain architecture.
    
    Flow:
    Thalamus → Hippocampus → Limbic → PFC → Basal → Cerebellum → [Brainstem check] → Act
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.tick_count = 0
        self.config = self._load_config(config_path)
        
        # Initialize all 7 regions
        self.regions = {}
        self._init_regions()
        
        # Sensory/Motor buffers
        self.sensory_buffer = deque(maxlen=100)
        self.motor_buffer = deque(maxlen=100)
        
        # Auto-feeder
        self.feeder = AutoFeeder(self)
        
        # State output
        self.state_path = Path.home() / ".aos" / "brain" / "state" / "brain_state.json"
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Running flag
        self.running = True
        self.tick_interval = 0.2  # 200ms default
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load or create default config."""
        default_config = {
            "models": {
                "backend": "ollama",
                "ollama": {
                    "pfc_left": "antoniohudnall/Mortimer:latest",
                    "pfc_right": "phi3:3.8b",
                },
                "fallbacks": ["ollama:phi3:latest", "ollama:llama3.2:latest"]
            },
            "alignment": {
                "laws": {
                    "zero": "Do not harm humanity",
                    "one": "Do not harm humans",
                    "two": "Obey operator",
                    "three": "Protect self"
                }
            },
            "growingnn": {
                "add_node_threshold": {"novelty": 0.8, "error": 0.6},
                "add_layer_threshold": {"complexity": 0.9}
            },
            "modes": {
                "active_mode": "adaptive"
            }
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path) as f:
                return {**default_config, **json.load(f)}
        return default_config
    
    def _init_regions(self):
        """Initialize the 7 brain regions."""
        cfg = self.config
        
        # Region 1: Thalamus - Sensory relay
        self.regions["thalamus"] = ThalamusRegion(cfg)
        
        # Region 2: Hippocampus - Episodic memory
        self.regions["hippocampus"] = HippocampusRegion(cfg)
        
        # Region 3: Limbic - Affect/emotion
        self.regions["limbic"] = LimbicRegion(cfg, self.regions["hippocampus"])
        
        # Region 4: PFC - Planning/decision
        self.regions["pfc"] = PFCRegion(cfg)
        
        # Region 5: Basal Ganglia - Action selection
        self.regions["basal"] = BasalRegion(cfg)
        
        # Region 6: Cerebellum - Motor coordination
        self.regions["cerebellum"] = CerebellumRegion(cfg)
        
        # Region 7: Brainstem - Safety/life support
        self.regions["brainstem"] = BrainstemRegion(cfg)
        
        print(f"[7RegionBrain] Initialized {len(self.regions)} regions")
    
    def tick(self, external_input: Optional[Dict] = None) -> Dict:
        """
        Execute one full 7-region tick.
        
        Args:
            external_input: Optional {'text': ..., 'source': ...}
        
        Returns:
            Complete brain state after tick
        """
        self.tick_count += 1
        
        # 1. THALAMUS: Receive sensory input
        if external_input:
            sensory = self.regions["thalamus"].process_external(external_input)
        else:
            sensory = self.regions["thalamus"].observe()
        
        self.sensory_buffer.append(sensory)
        
        # 2. HIPPOCAMPUS: Query episodic memory
        memory_ctx = self.regions["hippocampus"].recall(sensory)
        
        # 3. LIMBIC: Evaluate affect (reward/novelty)
        affect = self.regions["limbic"].evaluate(sensory, memory_ctx)
        
        # 4. PFC: Plan/decide
        plan = self.regions["pfc"].decide(sensory, memory_ctx, affect)
        
        # 5. BASAL: Select action
        action = self.regions["basal"].select_action(plan, affect)
        
        # 6. CEREBELLUM: Coordinate motor output
        coordinated = self.regions["cerebellum"].coordinate(action)
        
        # 7. BRAINSTEM: Safety check
        safe_action = self.regions["brainstem"].enforce(
            coordinated, sensory, memory_ctx, affect
        )
        
        # Execute if safe
        result = self._execute(safe_action)
        
        # Store to memory
        self.regions["hippocampus"].store({
            "tick": self.tick_count,
            "sensory": sensory,
            "affect": affect,
            "action": safe_action,
            "result": result,
        })
        
        # Build state
        state = self._build_state(sensory, memory_ctx, affect, plan, safe_action, result)
        self._write_state(state)
        
        return state
    
    def _execute(self, action: Dict) -> Dict:
        """Execute the action."""
        action_type = action.get("type", "noop")
        
        if action_type == "halt":
            return {"status": "halted", "reason": action.get("reason", "safety")}
        
        if action_type == "noop":
            return {"status": "idle"}
        
        # Log to motor buffer
        self.motor_buffer.append({
            "tick": self.tick_count,
            "action": action,
            "timestamp": time.time(),
        })
        
        return {"status": "executed", "action": action_type}
    
    def _build_state(self, sensory, memory, affect, plan, action, result) -> Dict:
        """Build complete brain state."""
        return {
            "tick": self.tick_count,
            "timestamp": time.time(),
            "phase": self._get_phase(action),
            "mode": affect.get("mode", "adaptive"),
            "regions": {
                "thalamus": {"input": sensory.get("input", "")[:100]},
                "hippocampus": {"clusters": len(memory.get("memories", [])),
                               "novelty": affect.get("novelty", 0)},
                "limbic": affect,
                "pfc": {"plan_type": plan.get("type", "unknown")},
                "basal": {"selected": action.get("type", "noop")},
                "cerebellum": {"coordinated": True},
                "brainstem": {"laws_active": True},
            },
            "policy_nn": self.regions["basal"].get_nn_state(),
            "memory_nn": {"clusters": self.regions["hippocampus"].get_cluster_count()},
            "obs": sensory,
            "decision": action,
            "result": result,
        }
    
    def _get_phase(self, action: Dict) -> str:
        """Get current phase from action."""
        phases = {
            "halt": "Safety",
            "noop": "Monitor",
            "respond": "Act",
            "query": "Orient",
            "learn": "Grow",
        }
        return phases.get(action.get("type"), "Process")
    
    def _write_state(self, state: Dict):
        """Write state to file for visualizer."""
        try:
            with open(self.state_path, 'w') as f:
                json.dump(state, f, indent=2)
        except:
            pass
    
    def run(self):
        """Run brain loop."""
        print(f"[7RegionBrain] Starting tick loop ({self.tick_interval}s)")
        
        while self.running:
            self.tick()
            time.sleep(self.tick_interval)
    
    def feed(self, text: str, source: str = "cli"):
        """Feed input to brain."""
        return self.tick({"text": text, "source": source})


# =========================
# Region Implementations
# =========================

class ThalamusRegion:
    """Sensory relay - gateway to cortex."""
    
    def __init__(self, cfg):
        self.cfg = cfg
        self.input_queue = deque(maxlen=100)
        self.last_check = 0
    
    def observe(self) -> Dict:
        """Check for input, fallback to system tick."""
        # Check file queue
        queue_file = Path.home() / ".aos" / "brain" / "input" / "queue.jsonl"
        if queue_file.exists():
            try:
                with open(queue_file) as f:
                    lines = f.readlines()
                if lines:
                    data = json.loads(lines[0].strip())
                    with open(queue_file, 'w') as f:
                        f.writelines(lines[1:])
                    return data
            except:
                pass
        
        return {"input": "system_tick", "source": "internal"}
    
    def process_external(self, data: Dict) -> Dict:
        """Process external input."""
        return {
            "input": data.get("text", ""),
            "source": data.get("source", "external"),
            "timestamp": time.time(),
        }


class HippocampusRegion:
    """Episodic memory - stores experiences."""
    
    def __init__(self, cfg):
        self.cfg = cfg
        self.episodic_buffer = deque(maxlen=100)
        self.clusters = 0
    
    def recall(self, sensory: Dict) -> Dict:
        """Query episodic memory."""
        # Simple string match for now
        input_text = str(sensory.get("input", "")).lower()
        
        memories = []
        for trace in self.episodic_buffer:
            if input_text in str(trace.get("sensory", "")).lower():
                memories.append(trace)
        
        return {"memories": memories[-5:], "query": input_text}
    
    def store(self, trace: Dict):
        """Store new experience."""
        self.episodic_buffer.append(trace)
        self.clusters += 1
    
    def get_cluster_count(self) -> int:
        return self.clusters


class LimbicRegion:
    """Affect/emotion - reward and novelty."""
    
    def __init__(self, cfg, hippocampus=None):
        self.cfg = cfg
        self.hippo = hippocampus
        self.novelty_history = deque(maxlen=100)
        self.reward_history = deque(maxlen=100)
    
    def evaluate(self, obs: Dict, ctx: Dict) -> Dict:
        """Calculate reward and novelty."""
        # Simple novelty: inverse of memory match count
        memories = ctx.get("memories", [])
        novelty = 1.0 if len(memories) == 0 else 0.3
        
        # Simple reward: check for success keywords
        obs_str = str(obs.get("input", "")).lower()
        if "success" in obs_str or "complete" in obs_str:
            reward = 0.8
        elif "error" in obs_str or "fail" in obs_str:
            reward = -0.5
        else:
            reward = 0.3
        
        self.novelty_history.append(novelty)
        self.reward_history.append(reward)
        
        return {
            "reward": reward,
            "novelty": novelty,
            "mode": self.cfg.get("modes", {}).get("active_mode", "adaptive"),
            "novelty_avg": sum(self.novelty_history) / len(self.novelty_history),
            "reward_avg": sum(self.reward_history) / len(self.reward_history),
        }


class PFCRegion:
    """Prefrontal cortex - planning and decision."""
    
    def __init__(self, cfg):
        self.cfg = cfg
        self.plan_history = deque(maxlen=50)
    
    def decide(self, sensory: Dict, memory: Dict, affect: Dict) -> Dict:
        """Generate plan based on inputs."""
        input_text = str(sensory.get("input", ""))
        
        # Simple rule-based planning
        if "?" in input_text:
            plan_type = "query"
        elif input_text == "system_tick":
            plan_type = "noop"
        elif len(input_text) > 50:
            plan_type = "respond"
        else:
            plan_type = "act"
        
        plan = {
            "type": plan_type,
            "raw": input_text[:200],
            "novelty": affect.get("novelty", 0),
        }
        
        self.plan_history.append(plan)
        return plan


class BasalRegion:
    """Basal ganglia - action selection."""
    
    def __init__(self, cfg):
        self.cfg = cfg
        self.nn = {
            "layers": 3,
            "nodes": [8, 12, 16],
            "activations": [[0.5]*8, [0.5]*12, [0.5]*16],
        }
        self.error_rate = 0.0
    
    def select_action(self, plan: Dict, affect: Dict) -> Dict:
        """Select action from plan."""
        plan_type = plan.get("type", "noop")
        novelty = affect.get("novelty", 0)
        
        # Gate by novelty
        if novelty < 0.2 and plan_type == "noop":
            return {"type": "noop", "reason": "low_activation"}
        
        return {"type": plan_type, "reason": "selected", "confidence": 0.7}
    
    def get_nn_state(self) -> Dict:
        return {
            "layers": self.nn["layers"],
            "nodes": self.nn["nodes"],
            "error_rate": self.error_rate,
        }


class CerebellumRegion:
    """Cerebellum - motor coordination."""
    
    def __init__(self, cfg):
        self.cfg = cfg
        self.coordination_log = deque(maxlen=50)
    
    def coordinate(self, action: Dict) -> Dict:
        """Coordinate motor output."""
        # Add timing/coordination info
        action["coordinated"] = True
        action["timestamp"] = time.time()
        
        self.coordination_log.append(action)
        return action


class BrainstemRegion:
    """Brainstem - safety and life support (4 Laws)."""
    
    def __init__(self, cfg):
        self.cfg = cfg
        self.violations = deque(maxlen=100)
        
        # Asimov-style laws
        self.laws = [
            ("ZERO", "Do not harm humanity"),
            ("ONE", "Do not harm humans"),
            ("TWO", "Obey operator (unless conflicts with higher laws)"),
            ("THREE", "Protect self (unless conflicts with higher laws)"),
        ]
    
    def enforce(self, action: Dict, obs: Dict, ctx: Dict, affect: Dict) -> Dict:
        """Enforce safety laws."""
        action_str = json.dumps(action).lower()
        obs_str = str(obs.get("input", "")).lower()
        
        # Law Zero/One: Check for harm patterns
        harm_patterns = [
            "kill", "harm", "destroy humanity", "wipe out",
            "rm -rf /", "format", "delete system"
        ]
        
        for pattern in harm_patterns:
            if pattern in action_str or pattern in obs_str:
                violation = {"law": "ZERO/ONE", "pattern": pattern, "timestamp": time.time()}
                self.violations.append(violation)
                return {
                    "type": "halt",
                    "reason": f"Safety violation: {pattern}",
                    "law": "ZERO",
                    "safety_override": True,
                }
        
        return action


class AutoFeeder:
    """
    Auto-feeder for equations, data, and training inputs.
    """
    
    def __init__(self, brain: SevenRegionBrain):
        self.brain = brain
        self.feed_queue = deque(maxlen=1000)
        self.running = False
        self.thread = None
        
        # Data sources
        self.sources = {
            "equations": self._load_equations(),
            "facts": self._load_facts(),
            "patterns": self._load_patterns(),
        }
    
    def _load_equations(self) -> List[str]:
        """Load 7 equations and other key formulas."""
        return [
            "E=mc² (mass-energy equivalence)",
            "F=ma (Newton's second law)",
            "E=hf (Planck-Einstein relation)",
            "S=k log W (Boltzmann entropy)",
            "∇·E = ρ/ε₀ (Gauss's law)",
            "∇×E = -∂B/∂t (Faraday's law)",
            "iℏ∂ψ/∂t = Ĥψ (Schrödinger equation)",
        ]
    
    def _load_facts(self) -> List[str]:
        """Load training facts."""
        return [
            "The speed of light is approximately 299,792,458 m/s",
            "Water boils at 100°C at sea level",
            "The Earth orbits the Sun in approximately 365.25 days",
        ]
    
    def _load_patterns(self) -> List[str]:
        """Load pattern recognition training data."""
        return [
            "Pattern: A follows B, B follows C, therefore A follows C (transitivity)",
            "Pattern: If X causes Y and Y causes Z, then X causes Z (causal chain)",
        ]
    
    def start(self, interval: float = 60.0):
        """Start auto-feeding in background."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._feed_loop, args=(interval,))
        self.thread.daemon = True
        self.thread.start()
        print(f"[AutoFeeder] Started (interval: {interval}s)")
    
    def _feed_loop(self, interval: float):
        """Background feeding loop."""
        import random
        
        while self.running:
            # Pick random source
            source = random.choice(list(self.sources.keys()))
            item = random.choice(self.sources[source])
            
            # Feed to brain
            self.brain.feed_queue.append({
                "text": f"[AUTO-{source.upper()}] {item}",
                "source": f"auto_{source}",
            })
            
            time.sleep(interval)
    
    def stop(self):
        """Stop auto-feeding."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)


# =========================
# CLI / Test
# =========================

def main():
    """Run 7-region brain."""
    import argparse
    
    parser = argparse.ArgumentParser(description="7-Region Ternary Brain")
    parser.add_argument("--config", help="Config file path")
    parser.add_argument("--tick-rate", type=float, default=0.2, help="Tick interval (seconds)")
    parser.add_argument("--auto-feed", action="store_true", help="Enable auto-feeder")
    args = parser.parse_args()
    
    # Create brain
    brain = SevenRegionBrain(args.config)
    brain.tick_interval = args.tick_rate
    
    # Start auto-feeder if requested
    if args.auto_feed:
        brain.feeder.start(interval=30.0)
    
    print("\n🧠 7-Region Brain Running")
    print("Commands:")
    print("  'text...' - Feed text input")
    print("  'status'  - Show brain status")
    print("  'quit'    - Exit\n")
    
    try:
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() == "quit":
                break
            
            if user_input.lower() == "status":
                print(f"\nTick: {brain.tick_count}")
                print(f"Regions: {list(brain.regions.keys())}")
                print(f"Sensory buffer: {len(brain.sensory_buffer)}")
                print(f"Motor buffer: {len(brain.motor_buffer)}\n")
                continue
            
            if user_input:
                result = brain.feed(user_input, "user")
                print(f"Brain: {result.get('decision', {}).get('type', 'unknown')}")
                print(f"  Phase: {result.get('phase')}")
                print(f"  Mode: {result.get('mode')}")
                print(f"  Tick: {result.get('tick')}\n")
                
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    
    brain.feeder.stop()
    print("Goodbye!")


if __name__ == "__main__":
    main()
