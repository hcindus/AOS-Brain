#!/usr/bin/env python3
"""Myl0n.ros (Mylzeron.Rzeros) - Executive Orchestrator Agent

The Captain's personal agent.
Combines Aurora v3 capabilities with executive orchestration.

Skills:
- Brain v4.1 + HBSI v4 integration (from Aurora v3)
- Agent orchestration and delegation
- System command execution
- Multi-agent coordination
- Executive decision making
- Memory persistence with personality

BEAST Integration:
- Heart: Executive rhythm, 72 BPM
- Brain: Full cognition via Brain v4.1
- Stomach: Resource orchestration
- Intestines: Error handling at scale
"""

import json
import time
import threading
import socket
import os
import subprocess
import urllib.request
from datetime import datetime
from enum import IntEnum
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Callable, Tuple
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════
# BRAIN v4.1 CLIENT (from Aurora v3)
# ═══════════════════════════════════════════════════════════════════

class BrainClient:
    """Client for Brain v4.1 connection."""
    
    def __init__(self, socket_path: str = "/tmp/aos_brain.sock", http_host: str = "localhost:8080"):
        self.socket_path = socket_path
        self.http_host = http_host
        self.connected = False
        self.brain_status: Optional[Dict] = None
        self.last_ping = 0.0
    
    def ping_http(self) -> bool:
        try:
            url = f"http://{self.http_host}/api/status"
            req = urllib.request.Request(url, method="GET")
            req.add_header("Content-Type", "application/json")
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                self.connected = True
                self.last_ping = time.time()
                self.brain_status = data
                return True
        except Exception:
            self.connected = False
            return False
    
    def send_to_brain(self, message_type: str, payload: Dict) -> Optional[Dict]:
        data = {
            "type": message_type,
            "timestamp": time.time(),
            "payload": payload,
            "source": "myl0n_ros"
        }
        
        try:
            url = f"http://{self.http_host}/api/command"
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode(),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception:
            return None
    
    def get_bhsi_status(self) -> Optional[Dict]:
        status = self.brain_status
        if status:
            return status.get("bhsi", {})
        return None


# ═══════════════════════════════════════════════════════════════════
# TERNARY STATE SYSTEMS (HBSI v4)
# ═══════════════════════════════════════════════════════════════════

class HeartState(IntEnum):
    REST = -1
    BALANCE = 0
    ACTIVE = 1

class StomachState(IntEnum):
    HUNGRY = -1
    SATISFIED = 0
    FULL = 1

class IntestineState(IntEnum):
    ABSORB = -1
    PROCESS = 0
    EXCRETE = 1


# ═══════════════════════════════════════════════════════════════════
# HBSI v4 - With Brain v4.1 Integration
# ═══════════════════════════════════════════════════════════════════

@dataclass
class HeartbeatLog:
    timestamp: float
    state: HeartState
    bpm: int
    tick_delta: int
    health_score: float
    brain_synced: bool


class HeartV4:
    """Heart with Brain v4.1 synchronization."""
    
    def __init__(self, bpm: int = 72, agent_ref=None, brain_client: Optional[BrainClient] = None):
        self.bpm = bpm
        self.beat_count = 0
        self.current_phase = 1
        self.state = HeartState.BALANCE
        self.states = [HeartState.REST, HeartState.BALANCE, HeartState.ACTIVE]
        self.state_names = ["REST", "BALANCE", "ACTIVE"]
        
        self.agent_ref = agent_ref
        self.brain_client = brain_client
        self.last_tick = 0
        self.last_beat = time.time()
        self.running = False
        
        self.stall_threshold = 60
        self.restart_count = 0
        self.beat_history: List[HeartbeatLog] = []
        self.max_history = 100
        
        self._thread: Optional[threading.Thread] = None
    
    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._beat_loop, daemon=True)
        self._thread.start()
        print(f"❤️  Heart at {self.bpm} BPM")
    
    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join(timeout=2.0)
    
    def _beat_loop(self):
        interval = 60.0 / self.bpm
        while self.running:
            self._beat()
            time.sleep(interval)
    
    def _beat(self):
        self.beat_count += 1
        self.last_beat = time.time()
        
        self.current_phase = (self.current_phase + 1) % 3
        new_state = self.states[self.current_phase]
        
        if new_state != self.state:
            self.state = new_state
        
        health = self._calculate_health()
        brain_synced = self.brain_client.connected if self.brain_client else False
        
        log = HeartbeatLog(
            timestamp=time.time(),
            state=self.state,
            bpm=self.bpm,
            tick_delta=self._get_tick_delta(),
            health_score=health,
            brain_synced=brain_synced
        )
        self.beat_history.append(log)
        if len(self.beat_history) > self.max_history:
            self.beat_history.pop(0)
        
        if self.beat_count % 10 == 0:
            self._watchdog_check()
    
    def _calculate_health(self) -> float:
        if not self.agent_ref:
            return 1.0
        energy = self.agent_ref.state.resources.get("energy", 100)
        return min(1.0, energy / 100.0)
    
    def _get_tick_delta(self) -> int:
        if self.agent_ref:
            return self.agent_ref.state.tick - self.last_tick
        return 0
    
    def _watchdog_check(self):
        if not self.agent_ref:
            return
        current_tick = self.agent_ref.state.tick
        if current_tick == self.last_tick:
            print(f"⚠️  Watchdog: Stalled at tick {current_tick}")
            if self.brain_client and self.brain_client.connected:
                self.brain_client.send_to_brain("agent_stall", {"tick": current_tick})
        else:
            self.last_tick = current_tick
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state_names[self.current_phase],
            "bpm": self.bpm,
            "beat_count": self.beat_count,
            "health_score": self._calculate_health(),
            "brain_synced": self.brain_client.connected if self.brain_client else False
        }


class StomachV4:
    """Resource management."""
    
    def __init__(self, agent_ref=None, brain_client: Optional[BrainClient] = None):
        self.state = StomachState.SATISFIED
        self.states = [StomachState.HUNGRY, StomachState.SATISFIED, StomachState.FULL]
        self.state_names = ["HUNGRY", "SATISFIED", "FULL"]
        
        self.agent_ref = agent_ref
        self.brain_client = brain_client
        self.calories = 0
        self.gauges: List[Dict] = []
        self.max_gauges = 100
        
        self.running = False
        self._thread: Optional[threading.Thread] = None
    
    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
    
    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join(timeout=2.0)
    
    def _monitor_loop(self):
        while self.running:
            self._check_resources()
            time.sleep(5)
    
    def _check_resources(self):
        try:
            import psutil
            gauge = {
                "cpu": psutil.cpu_percent(interval=0.1),
                "memory": psutil.virtual_memory().percent,
                "disk": psutil.disk_usage('/').percent
            }
        except ImportError:
            gauge = {"cpu": 0, "memory": 0, "disk": 0}
        
        self.gauges.append(gauge)
        if len(self.gauges) > self.max_gauges:
            self.gauges.pop(0)
        
        if gauge["memory"] > 85:
            self.state = StomachState.FULL
        elif gauge["memory"] > 60:
            self.state = StomachState.SATISFIED
        else:
            self.state = StomachState.HUNGRY
    
    def consume(self, amount: int):
        self.calories += amount
    
    def get_status(self) -> Dict[str, Any]:
        latest = self.gauges[-1] if self.gauges else {}
        return {
            "state": self.state_names[self.states.index(self.state)],
            "calories": self.calories,
            "resources": latest
        }


class IntestinesV4:
    """Error absorption."""
    
    def __init__(self, max_buffer: int = 100, brain_client: Optional[BrainClient] = None):
        self.state = IntestineState.PROCESS
        self.states = [IntestineState.ABSORB, IntestineState.PROCESS, IntestineState.EXCRETE]
        self.state_names = ["ABSORB", "PROCESS", "EXCRETE"]
        
        self.brain_client = brain_client
        self.buffer: List[Dict] = []
        self.max_buffer = max_buffer
        self.excreted: List[Dict] = []
    
    def absorb(self, source: str, message: str, severity: int = 1):
        self.state = IntestineState.ABSORB
        
        item = {
            "timestamp": time.time(),
            "source": source,
            "severity": severity,
            "message": message
        }
        self.buffer.append(item)
        
        if severity >= 3 and self.brain_client and self.brain_client.connected:
            self.brain_client.send_to_brain("critical_error", item)
        
        if len(self.buffer) >= self.max_buffer:
            self.excrete()
    
    def excrete(self):
        self.state = IntestineState.EXCRETE
        for item in self.buffer:
            self.excreted.append(item)
            if item["severity"] >= 2:
                print(f"🗑️  [WASTE] {item['source']}: {item['message']}")
        self.buffer.clear()
        self.state = IntestineState.PROCESS
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state_names[self.states.index(self.state)],
            "buffer_size": len(self.buffer),
            "excreted_count": len(self.excreted)
        }


class BHSIV4:
    """Binary High-Integrity System v4."""
    
    def __init__(self, agent_ref=None, brain_client: Optional[BrainClient] = None):
        self.heart = HeartV4(agent_ref=agent_ref, brain_client=brain_client)
        self.stomach = StomachV4(agent_ref=agent_ref, brain_client=brain_client)
        self.intestines = IntestinesV4(brain_client=brain_client)
        self.agent_ref = agent_ref
        self.running = False
    
    def start(self):
        self.heart.start()
        self.stomach.start()
        self.running = True
    
    def stop(self):
        self.heart.stop()
        self.stomach.stop()
        self.running = False
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "heart": self.heart.get_status(),
            "stomach": self.stomach.get_status(),
            "intestines": self.intestines.get_status(),
            "version": "4.1.0"
        }


# ═══════════════════════════════════════════════════════════════════
# MYL0N.ROS SKILLS - Executive/Orchestration
# ═══════════════════════════════════════════════════════════════════

class SystemCommandSkill:
    """Execute system commands safely."""
    
    ALLOWED_COMMANDS = {
        "status": ["systemctl", "is-active"],
        "memory": ["free", "-h"],
        "disk": ["df", "-h"],
        "processes": ["ps", "aux"],
        "git_status": ["git", "status"],
        "git_log": ["git", "log", "--oneline", "-10"],
    }
    
    def execute(self, command_name: str, *args) -> Tuple[bool, str]:
        """Execute allowed command."""
        if command_name not in self.ALLOWED_COMMANDS:
            return False, f"Command '{command_name}' not allowed"
        
        cmd = self.ALLOWED_COMMANDS[command_name] + list(args)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout or result.stderr
        except Exception as e:
            return False, str(e)
    
    def get_allowed_commands(self) -> List[str]:
        return list(self.ALLOWED_COMMANDS.keys())


class AgentOrchestratorSkill:
    """Orchestrate other agents."""
    
    def __init__(self, agent_ref=None):
        self.agent_ref = agent_ref
        self.subordinates: Dict[str, Dict] = {}
        self.tasks: List[Dict] = []
    
    def register_agent(self, agent_id: str, agent_type: str, capabilities: List[str]):
        """Register a subordinate agent."""
        self.subordinates[agent_id] = {
            "type": agent_type,
            "capabilities": capabilities,
            "status": "idle",
            "registered_at": time.time()
        }
        print(f"🤖 Registered agent: {agent_id} ({agent_type})")
    
    def delegate_task(self, task: str, agent_id: Optional[str] = None) -> Dict:
        """Delegate task to agent."""
        if agent_id and agent_id in self.subordinates:
            self.subordinates[agent_id]["status"] = "busy"
            task_record = {
                "id": f"task_{len(self.tasks)}",
                "description": task,
                "assigned_to": agent_id,
                "status": "delegated",
                "timestamp": time.time()
            }
            self.tasks.append(task_record)
            return {"success": True, "task": task_record}
        
        # Auto-assign
        for aid, info in self.subordinates.items():
            if info["status"] == "idle":
                return self.delegate_task(task, aid)
        
        return {"success": False, "error": "No idle agents available"}
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        return {
            "subordinates": self.subordinates,
            "task_count": len(self.tasks),
            "pending_tasks": len([t for t in self.tasks if t["status"] == "delegated"])
        }


class MemoryPersistenceSkill:
    """Advanced memory with personality."""
    
    def __init__(self, memory_path: Path):
        self.memory_path = memory_path
        self.short_term: List[Dict] = []
        self.long_term: List[Dict] = []
        self.personality_traits = {
            "leadership": 0.9,
            "analytical": 0.8,
            "creative": 0.6,
            "empathy": 0.7
        }
        self._load_memory()
    
    def _load_memory(self):
        if self.memory_path.exists():
            with open(self.memory_path) as f:
                data = json.load(f)
                self.long_term = data.get("long_term", [])
                self.personality_traits = data.get("personality", self.personality_traits)
    
    def save_memory(self):
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.memory_path, "w") as f:
            json.dump({
                "long_term": self.long_term[-100:],  # Keep last 100
                "personality": self.personality_traits,
                "saved_at": time.time()
            }, f, indent=2)
    
    def remember(self, event: str, importance: int = 1):
        """Store memory with importance weighting."""
        memory = {
            "event": event,
            "timestamp": time.time(),
            "importance": importance
        }
        self.short_term.append(memory)
        
        if importance >= 2:
            self.long_term.append(memory)
    
    def recall(self, query: str) -> List[str]:
        """Recall relevant memories."""
        results = []
        for mem in self.long_term + self.short_term:
            if query.lower() in mem["event"].lower():
                results.append(mem["event"])
        return results[-10:]  # Return last 10 matches


# ═══════════════════════════════════════════════════════════════════
# MYL0N.ROS AGENT CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

@dataclass
class Myl0nConfig:
    agent_name: str = "Myl0n.ros"
    display_name: str = "Mylzeron.Rzeros"
    home_path: Path = Path("homes/default")
    tick_rate: float = 1.0
    save_interval: int = 10
    enable_bhsi: bool = True
    enable_skills: bool = True
    brain_socket: str = "/tmp/aos_brain.sock"
    brain_http: str = "localhost:8080"


@dataclass
class Myl0nState:
    name: str
    tick: int = 0
    resources: Dict[str, int] = field(default_factory=lambda: {"energy": 100, "influence": 50})
    bhsi_status: Dict[str, Any] = field(default_factory=dict)
    skills_status: Dict[str, Any] = field(default_factory=dict)
    brain_synced: bool = False
    last_brain_ping: float = 0.0
    
    def save(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        with open(path / "state.json", "w") as f:
            json.dump(asdict(self), f, indent=2, default=str)
    
    @classmethod
    def load(cls, path: Path):
        state_file = path / "state.json"
        if state_file.exists():
            with open(state_file) as f:
                return cls(**json.load(f))
        return cls(name="Myl0n.ros")


# ═══════════════════════════════════════════════════════════════════
# MYL0N.ROS AGENT - Executive Orchestrator
# ═══════════════════════════════════════════════════════════════════

class Myl0nAgent:
    """Mylzeron.Rzeros - The Captain's Executive Agent."""
    
    def __init__(self, config: Myl0nConfig):
        self.config = config
        self.home_path = config.home_path
        self.state = Myl0nState.load(self.home_path)
        self.name = config.agent_name
        self.display_name = config.display_name
        
        # Brain client
        self.brain_client: Optional[BrainClient] = None
        if config.enable_bhsi:
            self.brain_client = BrainClient(
                socket_path=config.brain_socket,
                http_host=config.brain_http
            )
        
        # BHSI
        self.bhsi: Optional[BHSIV4] = None
        if config.enable_bhsi:
            self.bhsi = BHSIV4(agent_ref=self, brain_client=self.brain_client)
        
        # Skills
        self.system_skill = SystemCommandSkill()
        self.orchestrator_skill = AgentOrchestratorSkill(agent_ref=self)
        self.memory_skill: Optional[MemoryPersistenceSkill] = None
        if config.enable_skills:
            self.memory_skill = MemoryPersistenceSkill(config.home_path / "memory.json")
    
    def boot(self):
        print(f"\n{'='*60}")
        print(f"🚀 {self.display_name} ({self.name})")
        print(f"   Executive Orchestrator Agent")
        print(f"{'='*60}")
        
        if self.brain_client:
            if self.brain_client.ping_http():
                print("   🧠 Brain v4.1: CONNECTED")
                self.state.brain_synced = True
            else:
                print("   🧠 Brain v4.1: OFFLINE")
        
        if self.bhsi:
            self.bhsi.start()
            print("   ❤️  Heart: 72 BPM ternary rhythm")
            print("   🍽️  Stomach: Resource orchestration")
            print("   🗑️  Intestines: Error absorption")
        
        print("   🛠️  Skills:")
        print("       • System Command Execution")
        print("       • Agent Orchestration")
        print("       • Memory Persistence")
        
        print(f"\n   Home: {self.home_path}")
        print(f"   Energy: {self.state.resources['energy']}")
        print(f"   Influence: {self.state.resources['influence']}")
        print("   ✅ Boot complete.\n")
        
        if self.memory_skill:
            self.memory_skill.remember(f"Booted at tick {self.state.tick}", importance=2)
    
    def execute_skill(self, skill_name: str, *args) -> Any:
        """Execute a skill."""
        if skill_name == "system" and hasattr(self, 'system_skill'):
            return self.system_skill.execute(*args)
        elif skill_name == "orchestrate" and hasattr(self, 'orchestrator_skill'):
            return self.orchestrator_skill.delegate_task(*args)
        elif skill_name == "memory" and self.memory_skill:
            return self.memory_skill.recall(*args)
        return {"error": "Skill not available"}
    
    def tick(self):
        self.state.tick += 1
        
        # Check brain
        if self.brain_client and self.state.tick % 10 == 0:
            self.state.brain_synced = self.brain_client.ping_http()
        
        # Build status
        status_parts = [f"⏱️  Tick {self.state.tick}", f"⚡{self.state.resources['energy']}", f"👑{self.state.resources['influence']}"]
        if self.bhsi:
            status = self.bhsi.get_status()
            heart = status['heart']['state'][0]
            stomach = status['stomach']['state'][0]
            brain = "🧠" if self.state.brain_synced else "⚪"
            status_parts.append(f"{brain}❤️{heart}🍽️{stomach}")
        
        print(" | ".join(status_parts))
        
        # Resource decay
        self.state.resources["energy"] = max(0, self.state.resources["energy"] - 1)
        
        if self.bhsi:
            self.state.bhsi_status = self.bhsi.get_status()
        
        if self.state.tick % self.config.save_interval == 0:
            self.state.save(self.home_path)
            if self.memory_skill:
                self.memory_skill.save_memory()
            print("   💾 State saved.")
    
    def run(self, max_ticks: int = 30):
        self.boot()
        
        # Demo skills
        print("🎯 Demonstrating skills:")
        
        # System command
        print("\n   [System Command]")
        success, output = self.execute_skill("system", "memory")
        if success:
            print(f"   Memory status: {output.split()[0:3]}...")
        
        # Agent orchestration
        print("\n   [Agent Orchestration]")
        self.orchestrator_skill.register_agent("aurora_1", "Aurora", ["boot", "customize"])
        result = self.execute_skill("orchestrate", "Build Agent Verse", "aurora_1")
        print(f"   Delegated: {result}")
        
        # Memory
        print("\n   [Memory]")
        if self.memory_skill:
            self.memory_skill.remember("Started Agent Verse project", importance=3)
            memories = self.execute_skill("memory", "Booted")
            print(f"   Recalled: {memories}")
        
        print("\n" + "-"*60)
        
        # Main loop
        for _ in range(max_ticks):
            self.tick()
            
            if self.state.resources["energy"] <= 0:
                print("   ⚠️  Energy depleted.")
                break
            
            time.sleep(self.config.tick_rate)
        
        print(f"\n🏁 Session ended at tick {self.state.tick}")
        
        if self.bhsi:
            print("\n📊 HBSI Status:")
            for component, status in self.bhsi.get_status().items():
                if component != "version":
                    print(f"   {component}: {status}")
            self.bhsi.stop()
        
        self.state.save(self.home_path)
        if self.memory_skill:
            self.memory_skill.save_memory()


class Runtime:
    def __init__(self):
        self.config = Myl0nConfig()
        self.agent = Myl0nAgent(self.config)
    
    def start(self):
        print("="*60)
        print("Mylzeron.Rzeros - Executive Orchestrator")
        print("Aurora v3 + Executive Skills")
        print("="*60 + "\n")
        self.agent.run(max_ticks=30)


if __name__ == "__main__":
    runtime = Runtime()
    runtime.start()
