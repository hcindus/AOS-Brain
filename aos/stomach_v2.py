#!/usr/bin/env python3
"""
AOS Information Stomach v2.0 - Implements IStomach
Digests raw information, produces energy for brain
"""

import sys
sys.path.insert(0, '/root/.aos/aos')

import time
import hashlib
from typing import List, Dict
from dataclasses import dataclass
from collections import deque

from ternary_interfaces import IStomach, StomachState, DigestionInput, DigestionOutput


@dataclass
class InformationChunk:
    """Raw information chunk"""
    source: str
    content: str
    timestamp: float
    priority: float
    digestibility: float  # 0-1, how easily processed


class InformationStomach(IStomach):
    """
    Information Stomach - Digests raw data into energy
    
    Ternary States:
    - HUNGRY: Needs more information
    - SATISFIED: Optimal processing
    - FULL: Overloaded, slow digestion
    """
    
    def __init__(self, capacity: int = 100):
        self.state = StomachState.SATISFIED
        self.fullness = 0.5  # 0-1
        self.capacity = capacity
        
        # Input buffer (what's waiting to be digested)
        self.input_buffer: deque = deque(maxlen=capacity)
        
        # Processing
        self.digestion_rate = 0.15  # How fast we process
        self.energy_efficiency = 0.7  # Conversion efficiency
        
        # Tracking
        self.total_digested = 0.0
        self.total_energy_produced = 0.0
        self.cycle_count = 0
        
        # Output queue (digested info ready for intestine)
        self.digested_queue: List[Dict] = []
        
        print("[InformationStomach] Initialized - HUNGRY/SATISFIED/FULL")
    
    def ingest(self, source: str, content: str, priority: float = 0.5):
        """
        Ingest raw information
        
        Args:
            source: Where info came from (api, file, sensor, etc)
            content: The actual information
            priority: How important (0-1)
        """
        chunk = InformationChunk(
            source=source,
            content=content[:500],  # Truncate for processing
            timestamp=time.time(),
            priority=priority,
            digestibility=self._calculate_digestibility(content)
        )
        
        self.input_buffer.append(chunk)
        
        # Update fullness
        self.fullness = len(self.input_buffer) / self.capacity
        self._update_state()
    
    def _calculate_digestibility(self, content: str) -> float:
        """Calculate how digestible content is"""
        # Shorter, structured content = more digestible
        length_factor = max(0.3, 1.0 - len(content) / 1000)
        
        # Structured data (JSON, key-value) = more digestible
        structure_score = 0.5
        if any(marker in content for marker in ['{', '}', ':', ',']):
            structure_score = 0.9
        elif any(marker in content for marker in ['=', '|', '-']):
            structure_score = 0.7
        
        return (length_factor + structure_score) / 2
    
    def _update_state(self):
        """Update stomach state based on fullness"""
        if self.fullness < 0.3:
            if self.state != StomachState.HUNGRY:
                print(f"[Stomach] {self.state.value} -> HUNGRY (need more information)")
                self.state = StomachState.HUNGRY
        elif self.fullness > 0.9:
            if self.state != StomachState.FULL:
                print(f"[Stomach] {self.state.value} -> FULL (processing backlog)")
                self.state = StomachState.FULL
        else:
            if self.state != StomachState.SATISFIED:
                print(f"[Stomach] {self.state.value} -> SATISFIED (optimal flow)")
                self.state = StomachState.SATISFIED
    
    def digest(self, inputs: DigestionInput = None) -> DigestionOutput:
        """
        Implements IStomach.digest()
        Process information chunks into energy
        """
        self.cycle_count += 1
        
        # Amount to process based on state
        if self.state == StomachState.FULL:
            # Slow down when full
            process_amount = self.digestion_rate * 0.5
        elif self.state == StomachState.HUNGRY:
            # Process faster when hungry
            process_amount = self.digestion_rate * 1.5
        else:
            process_amount = self.digestion_rate
        
        # Process chunks
        energy_produced = 0.0
        digested_count = 0
        
        while self.input_buffer and process_amount > 0:
            chunk = self.input_buffer.popleft()
            
            # Calculate energy from this chunk
            chunk_energy = (
                chunk.digestibility * 
                chunk.priority * 
                self.energy_efficiency
            )
            
            energy_produced += chunk_energy
            digested_count += 1
            process_amount -= 0.1  # Each chunk takes processing power
            
            # Add to digested queue for intestine
            self.digested_queue.append({
                "source": chunk.source,
                "content": chunk.content,
                "energy": chunk_energy,
                "timestamp": chunk.timestamp
            })
        
        # Update fullness
        self.fullness = len(self.input_buffer) / self.capacity
        self._update_state()
        
        # Update totals
        self.total_digested += digested_count
        self.total_energy_produced += energy_produced
        
        # Create waste (information loss)
        waste = digested_count * (1 - self.energy_efficiency)
        
        return DigestionOutput(
            timestamp=time.time(),
            state=self.state,
            fullness=self.fullness,
            energy_produced=energy_produced,
            efficiency=self.energy_efficiency,
            waste_generated=waste,
            cycle_count=self.cycle_count,
            total_digested=self.total_digested,
            total_energy_produced=self.total_energy_produced,
            model_id="stomach_v2"
        )
    
    def get_status(self) -> Dict:
        """Implements IStomach.get_status()"""
        return {
            "state": self.state.value,
            "fullness": self.fullness,
            "buffer_size": len(self.input_buffer),
            "digested_queue": len(self.digested_queue),
            "total_digested": self.total_digested,
            "total_energy": self.total_energy_produced,
            "cycle_count": self.cycle_count
        }
    
    def get_digested_batch(self, n: int = 10) -> List[Dict]:
        """Get batch of digested info for intestine"""
        batch = self.digested_queue[:n]
        self.digested_queue = self.digested_queue[n:]
        return batch


if __name__ == "__main__":
    print("=" * 70)
    print("  INFORMATION STOMACH v2.0 - TEST")
    print("=" * 70)
    
    stomach = InformationStomach(capacity=50)
    
    # Ingest some information
    print("\nIngesting information...")
    stomach.ingest("api", "System status: CPU 45%, Memory 60%", priority=0.7)
    stomach.ingest("log", "Error: Connection timeout after 30s", priority=0.9)
    stomach.ingest("sensor", "Temperature: 72°F, Humidity: 45%", priority=0.4)
    stomach.ingest("file", "{\"users\": 150, \"active\": 42, \"load\": 0.3}", priority=0.6)
    
    print(f"Buffer: {len(stomach.input_buffer)} items")
    print(f"State: {stomach.state.value}")
    
    # Digest
    print("\nDigesting...")
    for i in range(3):
        output = stomach.digest()
        print(f"Cycle {i+1}: {output.state.value}, "
              f"energy={output.energy_produced:.2f}, "
              f"fullness={output.fullness:.2f}")
    
    print(f"\nDigested queue: {len(stomach.digested_queue)} items ready")
    print("=" * 70)
