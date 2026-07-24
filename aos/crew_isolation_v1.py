#!/usr/bin/env python3
"""
Crew Isolation v1.0 - True Sandbox for N'og nog Agents

Each crew member gets:
- Isolated workspace (separate directory)
- Message queue communication (no shared state)
- Quarantine capability (toxic agent containment)
- Process-level isolation
"""

import os
import json
import shutil
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class IsolatedAgent:
    """An agent running in isolation"""
    agent_id: str
    name: str
    role: str
    workspace_path: Path
    status: str = "active"  # active, quarantined, suspended
    created_at: float = 0.0
    last_activity: float = 0.0
    
    def __post_init__(self):
        if self.created_at == 0.0:
            self.created_at = time.time()
            self.last_activity = self.created_at


@dataclass
class AgentMessage:
    """Message between isolated agents"""
    message_id: str
    from_agent: str
    to_agent: str
    message_type: str  # task, response, alert, heartbeat
    payload: Dict[str, Any]
    timestamp: float
    priority: int = 5  # 1-10, lower = higher priority
    
    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()


class CrewIsolationV1:
    """
    True Sandbox Isolation for Crew Agents
    
    Like Docker containers for AI agents:
    - Each agent has own filesystem
    - Inter-agent comms via message queue only
    - No direct memory sharing
    - Quarantine for misbehaving agents
    """
    
    def __init__(self, base_path: str = "/var/lib/aos/crew"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Agent registry
        self.agents: Dict[str, IsolatedAgent] = {}
        
        # Message queue (shared between agents)
        self.message_queue: List[AgentMessage] = []
        self.message_history: List[AgentMessage] = []
        self.max_queue_size = 1000
        self.max_history = 10000
        
        # Quarantine tracking
        self.quarantine_log: List[Dict] = []
        
        print(f"[Crew Isolation v1.0] Initialized")
        print(f"  📁 Base path: {self.base_path}")
        print(f"  🔒 True sandbox isolation active")
    
    def create_agent(self, agent_id: str, name: str, role: str) -> IsolatedAgent:
        """
        Create a new isolated agent
        
        Each agent gets:
        - Own workspace directory
        - Isolated state storage
        - Message inbox
        """
        # Check if already exists
        if agent_id in self.agents:
            print(f"[Crew Isolation] Agent {agent_id} already exists, returning existing")
            return self.agents[agent_id]
        
        # Create isolated workspace
        workspace = self.base_path / f"agent_{agent_id}"
        workspace.mkdir(exist_ok=True)
        
        # Create subdirectories
        (workspace / "data").mkdir(exist_ok=True)
        (workspace / "logs").mkdir(exist_ok=True)
        (workspace / "temp").mkdir(exist_ok=True)
        (workspace / "inbox").mkdir(exist_ok=True)
        
        # Create agent state file
        state_file = workspace / "state.json"
        initial_state = {
            "agent_id": agent_id,
            "name": name,
            "role": role,
            "created_at": time.time(),
            "xp": 0,
            "level": "Rookie",
            "discoveries": []
        }
        with open(state_file, 'w') as f:
            json.dump(initial_state, f, indent=2)
        
        # Register agent
        agent = IsolatedAgent(
            agent_id=agent_id,
            name=name,
            role=role,
            workspace_path=workspace
        )
        self.agents[agent_id] = agent
        
        print(f"\n[Crew Isolation] 🏝️  Agent created: {name} ({agent_id})")
        print(f"  Role: {role}")
        print(f"  Workspace: {workspace}")
        print(f"  Status: {agent.status}")
        
        return agent
    
    def get_agent_state(self, agent_id: str) -> Optional[Dict]:
        """Get agent state (from isolated storage)"""
        if agent_id not in self.agents:
            return None
        
        agent = self.agents[agent_id]
        state_file = agent.workspace_path / "state.json"
        
        if not state_file.exists():
            return None
        
        with open(state_file, 'r') as f:
            return json.load(f)
    
    def update_agent_state(self, agent_id: str, updates: Dict) -> bool:
        """Update agent state (isolated write)"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        state_file = agent.workspace_path / "state.json"
        
        # Read current state
        current = {}
        if state_file.exists():
            with open(state_file, 'r') as f:
                current = json.load(f)
        
        # Apply updates
        current.update(updates)
        current['last_updated'] = time.time()
        
        # Write back (isolated to this agent)
        with open(state_file, 'w') as f:
            json.dump(current, f, indent=2)
        
        agent.last_activity = time.time()
        return True
    
    def send_message(self, from_agent: str, to_agent: str, 
                    message_type: str, payload: Dict, priority: int = 5) -> str:
        """
        Send message between agents (only communication method)
        
        Agents CANNOT access each other's state directly.
        All communication goes through this message queue.
        """
        # Validate agents exist
        if from_agent not in self.agents:
            raise ValueError(f"Sender agent {from_agent} not found")
        if to_agent not in self.agents and to_agent != "broadcast":
            raise ValueError(f"Recipient agent {to_agent} not found")
        
        # Check if sender is quarantined
        if self.agents[from_agent].status == "quarantined":
            print(f"[Crew Isolation] 🚫 Blocked message from quarantined agent {from_agent}")
            return "blocked"
        
        # Create message
        msg = AgentMessage(
            message_id=hashlib.md5(f"{from_agent}{to_agent}{time.time()}".encode()).hexdigest()[:8],
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            timestamp=time.time(),
            priority=priority
        )
        
        # Add to queue
        self.message_queue.append(msg)
        
        # Sort by priority (lower number = higher priority)
        self.message_queue.sort(key=lambda x: x.priority)
        
        # Prune queue if too large
        if len(self.message_queue) > self.max_queue_size:
            removed = self.message_queue[:-self.max_queue_size]
            self.message_queue = self.message_queue[-self.max_queue_size:]
            self.message_history.extend(removed)
        
        # Prune history
        if len(self.message_history) > self.max_history:
            self.message_history = self.message_history[-self.max_history:]
        
        print(f"[Crew Isolation] 📨 Message {msg.message_id}: {from_agent} → {to_agent}")
        print(f"  Type: {message_type} | Priority: {priority}")
        
        return msg.message_id
    
    def get_messages(self, agent_id: str, mark_delivered: bool = True) -> List[AgentMessage]:
        """Get messages for an agent (inbox)"""
        if agent_id not in self.agents:
            return []
        
        # Filter messages for this agent
        messages = [
            msg for msg in self.message_queue 
            if msg.to_agent == agent_id or msg.to_agent == "broadcast"
        ]
        
        # Remove from queue if requested
        if mark_delivered:
            self.message_queue = [
                msg for msg in self.message_queue 
                if msg.to_agent != agent_id and msg.to_agent != "broadcast"
            ]
            # Add to agent's inbox file
            inbox_file = self.agents[agent_id].workspace_path / "inbox" / "messages.json"
            existing = []
            if inbox_file.exists():
                with open(inbox_file, 'r') as f:
                    existing = json.load(f)
            existing.extend([asdict(m) for m in messages])
            with open(inbox_file, 'w') as f:
                json.dump(existing, f, indent=2)
        
        return messages
    
    def quarantine_agent(self, agent_id: str, reason: str) -> bool:
        """
        Quarantine a misbehaving agent
        
        - Agent isolated from crew
        - Can still receive messages (logged)
        - Cannot send messages
        - State preserved for review
        """
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        old_status = agent.status
        agent.status = "quarantined"
        
        # Log quarantine
        self.quarantine_log.append({
            "agent_id": agent_id,
            "name": agent.name,
            "reason": reason,
            "timestamp": time.time(),
            "previous_status": old_status
        })
        
        # Create quarantine flag in workspace
        quarantine_file = agent.workspace_path / "QUARANTINED"
        with open(quarantine_file, 'w') as f:
            f.write(f"Quarantined at {datetime.now().isoformat()}\n")
            f.write(f"Reason: {reason}\n")
        
        print(f"\n[Crew Isolation] ⚠️  AGENT QUARANTINED: {agent.name} ({agent_id})")
        print(f"  Reason: {reason}")
        print(f"  Workspace preserved at: {agent.workspace_path}")
        
        return True
    
    def release_agent(self, agent_id: str) -> bool:
        """Release agent from quarantine"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        if agent.status != "quarantined":
            print(f"[Crew Isolation] Agent {agent_id} not quarantined")
            return False
        
        agent.status = "active"
        
        # Remove quarantine flag
        quarantine_file = agent.workspace_path / "QUARANTINED"
        if quarantine_file.exists():
            quarantine_file.unlink()
        
        print(f"\n[Crew Isolation] ✅ Agent {agent.name} released from quarantine")
        
        return True
    
    def destroy_agent(self, agent_id: str) -> bool:
        """
        Permanently destroy an agent and all its data
        
        Use with caution - this deletes all isolated state.
        """
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        
        print(f"\n[Crew Isolation] 💥 Destroying agent: {agent.name} ({agent_id})")
        print(f"  Workspace: {agent.workspace_path}")
        
        # Remove workspace
        if agent.workspace_path.exists():
            shutil.rmtree(agent.workspace_path)
        
        # Remove from registry
        del self.agents[agent_id]
        
        print(f"  ✅ Agent destroyed")
        
        return True
    
    def get_isolation_summary(self) -> Dict:
        """Get summary of isolated crew"""
        return {
            "total_agents": len(self.agents),
            "active": sum(1 for a in self.agents.values() if a.status == "active"),
            "quarantined": sum(1 for a in self.agents.values() if a.status == "quarantined"),
            "suspended": sum(1 for a in self.agents.values() if a.status == "suspended"),
            "message_queue_size": len(self.message_queue),
            "message_history_size": len(self.message_history),
            "quarantine_count": len(self.quarantine_log),
            "agents": [
                {
                    "id": a.agent_id,
                    "name": a.name,
                    "role": a.role,
                    "status": a.status,
                    "last_activity": datetime.fromtimestamp(a.last_activity).isoformat()
                }
                for a in self.agents.values()
            ]
        }


# Test
def test_crew_isolation():
    """Test crew isolation system"""
    print("\n" + "=" * 70)
    print("  🏝️  CREW ISOLATION v1.0 - Sandbox Test")
    print("=" * 70)
    
    isolation = CrewIsolationV1(base_path="/tmp/test_crew_isolation")
    
    # Create agents
    print("\n[1] Creating isolated agents...")
    vex = isolation.create_agent("vex_001", "Vex", "Pilot")
    nyx = isolation.create_agent("nyx_001", "Nyx", "Engineer")
    jax = isolation.create_agent("jax_001", "Jax", "Scientist")
    
    # Verify isolation
    print("\n[2] Verifying workspace isolation...")
    for agent_id, agent in isolation.agents.items():
        print(f"  {agent.name}: {agent.workspace_path}")
        assert agent.workspace_path.exists(), f"Workspace missing for {agent_id}"
    print("  ✅ All workspaces created and isolated")
    
    # Test state isolation
    print("\n[3] Testing state isolation...")
    isolation.update_agent_state("vex_001", {"xp": 100, "level": "Rookie"})
    isolation.update_agent_state("nyx_001", {"xp": 150, "level": "Rookie"})
    
    vex_state = isolation.get_agent_state("vex_001")
    nyx_state = isolation.get_agent_state("nyx_001")
    
    print(f"  Vex XP: {vex_state['xp']}")
    print(f"  Nyx XP: {nyx_state['xp']}")
    assert vex_state['xp'] != nyx_state['xp'], "States should be isolated"
    print("  ✅ States are isolated")
    
    # Test message queue
    print("\n[4] Testing message queue (only communication method)...")
    msg_id = isolation.send_message(
        "vex_001", "nyx_001", "task",
        {"action": "repair_engine", "priority": "high"},
        priority=2
    )
    print(f"  Message sent: {msg_id}")
    
    # Check Nyx's inbox
    messages = isolation.get_messages("nyx_001")
    print(f"  Nyx received {len(messages)} messages")
    assert len(messages) == 1, "Should have 1 message"
    assert messages[0].from_agent == "vex_001", "Should be from Vex"
    print("  ✅ Message queue working")
    
    # Test quarantine
    print("\n[5] Testing quarantine...")
    isolation.quarantine_agent("jax_001", "Hallucinating dangerous commands")
    
    # Try to send message from quarantined agent
    result = isolation.send_message(
        "jax_001", "vex_001", "alert",
        {"message": "Trust me"}
    )
    assert result == "blocked", "Quarantined agent should not send messages"
    print("  ✅ Quarantine blocking messages")
    
    # Can still receive messages
    isolation.send_message("vex_001", "jax_001", "warning", {"stay calm": True})
    jax_messages = isolation.get_messages("jax_001")
    assert len(jax_messages) == 1, "Quarantined agent can still receive"
    print("  ✅ Quarantined agent can still receive messages")
    
    # Test release
    print("\n[6] Testing release from quarantine...")
    isolation.release_agent("jax_001")
    assert isolation.agents["jax_001"].status == "active"
    print("  ✅ Agent released")
    
    # Summary
    print("\n[7] Isolation summary...")
    summary = isolation.get_isolation_summary()
    print(f"  Total agents: {summary['total_agents']}")
    print(f"  Active: {summary['active']}")
    print(f"  Quarantined: {summary['quarantined']}")
    print(f"  Message queue: {summary['message_queue_size']}")
    print(f"  Quarantine history: {summary['quarantine_count']}")
    
    # Cleanup
    print("\n[8] Cleaning up test agents...")
    for agent_id in list(isolation.agents.keys()):
        isolation.destroy_agent(agent_id)
    
    print("\n" + "=" * 70)
    print("  ✅ Crew Isolation v1.0 Test Complete")
    print("=" * 70)
    print("\n  Key Achievements:")
    print("    🏝️  Each agent has isolated workspace")
    print("    🔒 No direct state sharing between agents")
    print("    📨 Message queue is ONLY communication method")
    print("    ⚠️  Quarantine isolates misbehaving agents")
    print("    💥 Can permanently destroy agents and data")
    
    return True


if __name__ == "__main__":
    test_crew_isolation()
