#!/usr/bin/env python3
"""
AOS AGENT SDK v1.0
Python client library for brain/cortex interaction
"""

import socket
import json
import time
import numpy as np
from typing import Dict, List, Tuple, Optional, Callable, Any
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import hashlib

class CortexLayer(Enum):
    CONSCIOUS = 0b001
    SUBCONSCIOUS = 0b010
    UNCONSCIOUS = 0b100
    ALL = 0b111

@dataclass
class CortexHotspot:
    x: int
    y: int
    z: int
    value: int  # -1, 0, 1
    activation: float = 1.0
    
    def to_tuple(self) -> Tuple[int, int, int, int]:
        return (self.x, self.y, self.z, self.value)

@dataclass
class CortexSnapshot:
    tick: int
    coherence: float
    pattern_hash: Optional[str]
    hotspots: List[CortexHotspot]
    temporal_context: List[Dict]
    timestamp: float = 0.0
    
    def get_region_summary(self) -> Dict[int, int]:
        """Count hotspots per region"""
        summary = {}
        for h in self.hotspots:
            region = (h.x // 16) * 4 + (h.y // 16) * 2 + (h.z // 16)
            summary[region] = summary.get(region, 0) + 1
        return summary

@dataclass
class BrainState:
    tick: int
    phase: str
    signal_quality: float
    heart_bpm: float
    thyroid_state: str
    liver_state: str
    kidneys_state: str
    active_agents: int

class AOSBrainClient:
    """
    High-level client for AOS Brain interaction
    
    Usage:
        client = AOSBrainClient(agent_id="my_agent")
        client.register()
        
        # Write thoughts to cortex
        client.write_thought("processing visual input", priority=0.8)
        
        # Read current state
        snapshot = client.read_cortex()
        
        # Get full brain status
        status = client.get_brain_status()
    """
    
    def __init__(self, agent_id: str, socket_path: str = '/tmp/aos_brain.sock',
                 auto_tick: bool = True, default_regions: List[int] = None):
        self.agent_id = agent_id
        self.socket_path = socket_path
        self.auto_tick = auto_tick
        self.default_regions = default_regions or list(range(8))
        self._registered = False
        self._callbacks: Dict[str, List[Callable]] = {
            'on_tick': [],
            'on_state_change': [],
            'on_pattern_match': []
        }
        self._last_tick = 0
        self._background_thread: Optional[threading.Thread] = None
        self._running = False
        
    def _send(self, cmd: str, params: Dict = None, timeout: float = 5.0) -> Dict:
        """Send command to brain socket"""
        params = params or {}
        params.setdefault('agent_id', self.agent_id)
        
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect(self.socket_path)
            
            request = json.dumps({'cmd': cmd, 'params': params})
            sock.sendall(request.encode() + b'\n')
            
            data = b''
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                data += chunk
                if len(chunk) < 4096:
                    break
            
            sock.close()
            return json.loads(data.decode()) if data else {'error': 'no response'}
        except Exception as e:
            return {'error': str(e), 'cmd': cmd}
    
    def register(self) -> bool:
        """Register this agent with the brain"""
        result = self._send('cortex_register', {'agent_id': self.agent_id})
        self._registered = result.get('registered', False)
        return self._registered
    
    def unregister(self):
        """Unregister from brain"""
        self._registered = False
    
    def write_cortex(self, hotspots: List[CortexHotspot], 
                     regions: List[int] = None,
                     priority: float = 1.0,
                     ephemeral: bool = False) -> Dict:
        """
        Write activations to cortex
        
        Args:
            hotspots: List of hotspot coordinates and values
            regions: Which regions to write to (default: all)
            priority: Signal strength (0.0-1.0)
            ephemeral: If True, cleared on next tick
        """
        if not self._registered:
            self.register()
        
        activations = [h.to_tuple() for h in hotspots]
        
        return self._send('cortex_write', {
            'agent_id': self.agent_id,
            'regions': regions or self.default_regions,
            'activations': activations,
            'priority': priority,
            'ephemeral': ephemeral
        })
    
    def write_thought(self, thought: str, priority: float = 0.7) -> Dict:
        """
        Encode a thought string into cortex hotspots
        
        Uses text hashing to generate deterministic coordinates
        """
        # Hash thought to generate hotspots
        hotspots = []
        words = thought.lower().split()
        
        for i, word in enumerate(words[:20]):  # Limit to 20 words
            hash_val = int(hashlib.md5(word.encode()).hexdigest(), 16)
            
            x = (hash_val % 32)
            y = ((hash_val // 32) % 32)
            z = ((hash_val // (32*32)) % 32)
            
            # Positive activation for presence
            hotspots.append(CortexHotspot(x, y, z, 1, activation=priority))
        
        return self.write_cortex(hotspots, priority=priority, ephemeral=True)
    
    def read_cortex(self, regions: List[int] = None, 
                    max_hotspots: int = 64,
                    layer_mask: int = 0b111) -> Optional[CortexSnapshot]:
        """
        Read current cortical state
        
        Returns snapshot of active hotspots and coherence
        """
        if not self._registered:
            self.register()
        
        result = self._send('cortex_read', {
            'agent_id': self.agent_id,
            'regions': regions or self.default_regions,
            'max_hotspots': max_hotspots,
            'layer_mask': layer_mask
        })
        
        if 'error' in result:
            return None
        
        hotspots = [
            CortexHotspot(h['x'], h['y'], h['z'], h['val'])
            for h in result.get('hotspots', [])
        ]
        
        return CortexSnapshot(
            tick=result.get('tick', 0),
            coherence=result.get('coherence', 0.0),
            pattern_hash=result.get('pattern_hash'),
            hotspots=hotspots,
            temporal_context=result.get('temporal_context', []),
            timestamp=time.time()
        )
    
    def tick(self) -> Dict:
        """Manually trigger a cortex tick"""
        return self._send('cortex_tick')
    
    def get_cortex_stats(self) -> Dict:
        """Get cortex performance statistics"""
        return self._send('cortex_stats')
    
    def get_brain_status(self) -> Optional[BrainState]:
        """Get full brain status"""
        result = self._send('status')
        if 'error' in result:
            return None
        
        return BrainState(
            tick=result.get('tick', 0),
            phase=result.get('phase', 'unknown'),
            signal_quality=result.get('signal_quality_20avg', 0.5),
            heart_bpm=result.get('cortex', {}).get('conscious_mean', 60),
            thyroid_state=result.get('thyroid', {}).get('state', 'unknown'),
            liver_state=result.get('liver', {}).get('state', 'unknown'),
            kidneys_state=result.get('kidneys', {}).get('state', 'unknown'),
            active_agents=len(result.get('cortex_stats', {}).get('agents', {}))
        )
    
    def ingest(self, content: str, source: str = "agent", priority: float = 0.8) -> Dict:
        """Feed content into brain's stomach"""
        return self._send('ingest', {
            'content': content,
            'source': source,
            'priority': priority
        })
    
    def perceive(self, observation: str, intensity: float = 0.8) -> Dict:
        """Add observation to consciousness"""
        return self._send('perceive', {
            'observation': observation,
            'intensity': intensity
        })
    
    def on_tick(self, callback: Callable[[Dict], None]):
        """Register callback for tick events"""
        self._callbacks['on_tick'].append(callback)
    
    def start_background_poll(self, interval: float = 1.0):
        """Start background thread polling for state changes"""
        self._running = True
        
        def poll():
            while self._running:
                try:
                    status = self.get_brain_status()
                    if status and status.tick != self._last_tick:
                        self._last_tick = status.tick
                        for cb in self._callbacks['on_tick']:
                            cb({'tick': status.tick, 'phase': status.phase})
                except Exception as e:
                    print(f"[AgentSDK] Poll error: {e}")
                time.sleep(interval)
        
        self._background_thread = threading.Thread(target=poll, daemon=True)
        self._background_thread.start()
    
    def stop_background_poll(self):
        """Stop background polling"""
        self._running = False


class MultiAgentCoordinator:
    """
    Coordinate multiple agents sharing the brain
    
    Usage:
        coord = MultiAgentCoordinator()
        
        agent1 = coord.create_agent("explorer")
        agent2 = coord.create_agent("analyzer")
        
        # Share state between agents
        snapshot = agent1.read_cortex()
        coord.broadcast_pattern("interesting_find", snapshot)
    """
    
    def __init__(self, socket_path: str = '/tmp/aos_brain.sock'):
        self.socket_path = socket_path
        self.agents: Dict[str, AOSBrainClient] = {}
        self.shared_patterns: Dict[str, CortexSnapshot] = {}
        
    def create_agent(self, agent_id: str, **kwargs) -> AOSBrainClient:
        """Create and register a new agent"""
        agent = AOSBrainClient(agent_id, self.socket_path, **kwargs)
        agent.register()
        self.agents[agent_id] = agent
        return agent
    
    def broadcast_pattern(self, pattern_name: str, snapshot: CortexSnapshot,
                          exclude_agent: str = None):
        """Share a pattern with all agents"""
        self.shared_patterns[pattern_name] = snapshot
        
        for agent_id, agent in self.agents.items():
            if agent_id != exclude_agent:
                # Agents can check shared_patterns
                pass
    
    def get_collective_state(self) -> Dict:
        """Get aggregate state across all agents"""
        states = {}
        for agent_id, agent in self.agents.items():
            states[agent_id] = agent.get_brain_status()
        return states


# === CONVENIENCE FUNCTIONS ===

def quick_thought(thought: str, agent_id: str = "quick_agent", priority: float = 0.7) -> bool:
    """One-shot write a thought to cortex"""
    client = AOSBrainClient(agent_id, auto_tick=False)
    result = client.write_thought(thought, priority)
    return 'error' not in result

def get_brain_summary() -> Dict:
    """Get quick brain status summary"""
    client = AOSBrainClient("summary_reader", auto_tick=False)
    return client.get_brain_status()


if __name__ == "__main__":
    print("=" * 70)
    print("  AOS AGENT SDK v1.0 TEST")
    print("=" * 70)
    
    # Create test agent
    agent = AOSBrainClient("test_agent_sdk")
    
    print("\n[Test 1] Register agent")
    success = agent.register()
    print(f"  Registered: {success}")
    
    print("\n[Test 2] Write thought")
    result = agent.write_thought("analyzing pattern in visual field", priority=0.8)
    print(f"  Write result: {result.get('write_result', {}).get('written', 0)} activations")
    
    print("\n[Test 3] Trigger tick")
    tick_result = agent.tick()
    print(f"  Tick: {tick_result.get('tick')}, time: {tick_result.get('tick_time_ms', 0):.2f}ms")
    
    print("\n[Test 4] Read cortex")
    snapshot = agent.read_cortex(max_hotspots=16)
    if snapshot:
        print(f"  Snapshot: tick={snapshot.tick}, coherence={snapshot.coherence:.3f}")
        print(f"  Hotspots: {len(snapshot.hotspots)}")
        print(f"  Region summary: {snapshot.get_region_summary()}")
    
    print("\n[Test 5] Get brain status")
    status = agent.get_brain_status()
    if status:
        print(f"  Brain: tick={status.tick}, phase={status.phase}, quality={status.signal_quality:.3f}")
    
    print("\n[Test 6] Ingest content")
    result = agent.ingest("New data for processing", source="sdk_test")
    print(f"  Ingested: {'error' not in result}")
    
    print("\n[Test 7] Multi-agent coordinator")
    coord = MultiAgentCoordinator()
    agent1 = coord.create_agent("explorer_1")
    agent2 = coord.create_agent("analyzer_1")
    print(f"  Created {len(coord.agents)} coordinated agents")
    
    collective = coord.get_collective_state()
    print(f"  Collective state: {len(collective)} agents reporting")
    
    print("\n" + "=" * 70)
    print("  SDK TESTS COMPLETE")
    print("=" * 70)