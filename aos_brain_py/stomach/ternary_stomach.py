#!/usr/bin/env python3
"""
Ternary Stomach - Energy and Metabolism System.

The stomach processes inputs (data/experiences) and converts them to energy.
It feeds the heart and brain, providing the resources they need to function.

3 States:
- HUNGRY (-1): Needs input, low energy
- SATISFIED (0): Optimal energy level  
- FULL (+1): Overloaded, needs processing time

Smaller than heart: ~250 lines
"""

import time
import math
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import deque


class StomachState(Enum):
    """Ternary stomach states."""
    HUNGRY = -1     # Needs input, low energy
    SATISFIED = 0   # Optimal energy
    FULL = 1        # Overloaded, processing


@dataclass
class DigestionTask:
    """A task being digested (processed)."""
    content: Any
    complexity: float  # 0-1 how hard to process
    nutrition: float   # 0-1 energy value
    timestamp: float = field(default_factory=time.time)
    processed: bool = False


class TernaryStomach:
    """
    Ternary Stomach - Energy processing system.
    
    Takes in:
    - Data/experiences (to digest)
    - Tasks (to metabolize)
    - Information (to extract energy from)
    
    Provides:
    - Energy to heart (for rhythm)
    - Nutrients to brain (for cognition)
    - Metabolic state to system
    
    Much simpler than brain (250 lines vs 646)
    """
    
    def __init__(self):
        self.state = StomachState.SATISFIED
        self.energy_level = 0.5  # 0-1
        self.max_energy = 1.0
        self.min_energy = 0.0
        
        # Digestion queue
        self.stomach_queue = deque(maxlen=50)  # Being processed
        self.intestine_queue = deque(maxlen=100)  # Being absorbed
        
        # Metabolism
        self.metabolic_rate = 0.05  # Energy burn per tick
        self.digestion_rate = 0.1   # How fast to process
        
        # State history
        self.state_history = []
        self.max_history = 50
        
        # Outputs
        self.energy_output = 0.0
        self.waste_accumulated = 0.0
        
        print("[TernaryStomach] Initialized - HUNGRY/SATISFIED/FULL")
    
    def consume(self, item: Any, complexity: float = 0.5, nutrition: float = 0.5) -> Dict:
        """
        Consume (eat) something.
        
        Args:
            item: What to consume (data, task, experience)
            complexity: How hard to digest (0-1)
            nutrition: Energy value (0-1)
            
        Returns:
            Digestion status
        """
        task = DigestionTask(
            content=item,
            complexity=complexity,
            nutrition=nutrition
        )
        
        # Add to stomach
        self.stomach_queue.append(task)
        
        # Check if getting full
        if len(self.stomach_queue) > 40:
            self.state = StomachState.FULL
            print(f"[Stomach] State: SATISFIED → FULL (queue: {len(self.stomach_queue)})")
        elif len(self.stomach_queue) > 20 and self.state == StomachState.HUNGRY:
            self.state = StomachState.SATISFIED
            print(f"[Stomach] State: HUNGRY → SATISFIED")
        
        return {
            "status": "consumed",
            "queue_size": len(self.stomach_queue),
            "state": self.state.name
        }
    
    def digest(self) -> Dict:
        """
        Digest one cycle.
        
        Processes items in stomach, converts to energy.
        """
        # 1. METABOLIZE (burn energy)
        self.energy_level -= self.metabolic_rate
        
        # 2. DIGEST (process items)
        digested = 0
        energy_gained = 0
        
        # Process up to 3 items per tick
        for _ in range(min(3, len(self.stomach_queue))):
            if not self.stomach_queue:
                break
            
            task = self.stomach_queue.popleft()
            
            # Digest based on complexity
            digestion_time = task.complexity * 10
            if digestion_time <= 0:
                # Fully digested
                energy_gained += task.nutrition * 0.2
                digested += 1
            else:
                # Partially digested, move to intestine
                task.complexity -= self.digestion_rate
                if task.complexity <= 0:
                    energy_gained += task.nutrition * 0.2
                    digested += 1
                else:
                    self.intestine_queue.append(task)
        
        # 3. ABSORB (from intestine)
        absorbed = 0
        for _ in range(min(2, len(self.intestine_queue))):
            if not self.intestine_queue:
                break
            
            task = self.intestine_queue.popleft()
            energy_gained += task.nutrition * 0.1
            absorbed += 1
        
        # 4. UPDATE ENERGY
        self.energy_level += energy_gained
        self.energy_level = max(0.0, min(1.0, self.energy_level))
        
        # 5. UPDATE STATE (ternary)
        if self.energy_level < 0.3:
            if self.state != StomachState.HUNGRY:
                self.state = StomachState.HUNGRY
                print(f"[Stomach] State: {self._previous_state()} → HUNGRY (energy: {self.energy_level:.2f})")
        elif self.energy_level > 0.8:
            if self.state != StomachState.FULL:
                self.state = StomachState.FULL
                print(f"[Stomach] State: {self._previous_state()} → FULL (energy: {self.energy_level:.2f})")
        else:
            if self.state == StomachState.HUNGRY and self.energy_level > 0.4:
                self.state = StomachState.SATISFIED
                print(f"[Stomach] State: HUNGRY → SATISFIED")
            elif self.state == StomachState.FULL and self.energy_level < 0.7:
                self.state = StomachState.SATISFIED
                print(f"[Stomach] State: FULL → SATISFIED")
        
        # 6. PRODUCE OUTPUTS
        self.energy_output = self.energy_level
        self.waste_accumulated += 0.01  # Small waste per tick
        
        # Record
        self.state_history.append({
            "state": self.state,
            "energy": self.energy_level,
            "digested": digested,
            "absorbed": absorbed,
            "timestamp": time.time()
        })
        if len(self.state_history) > self.max_history:
            self.state_history.pop(0)
        
        return {
            "state": self.state.name,
            "energy": self.energy_level,
            "digested": digested,
            "absorbed": absorbed,
            "stomach_load": len(self.stomach_queue),
            "intestine_load": len(self.intestine_queue),
        }
    
    def _previous_state(self) -> str:
        """Get previous state name."""
        if self.state_history:
            return self.state_history[-1]["state"].name
        return "UNKNOWN"
    
    def get_outputs(self) -> Dict:
        """Get energy outputs for heart and brain."""
        # Energy allocation
        heart_allocation = self.energy_output * 0.3  # 30% to heart
        brain_allocation = self.energy_output * 0.6  # 60% to brain
        system_allocation = self.energy_output * 0.1   # 10% to system
        
        # Hunger signal
        hunger = 1.0 - self.energy_level  # Inverse of energy
        
        # Satisfaction signal
        satisfaction = self.energy_level if self.state == StomachState.SATISFIED else 0.5
        
        return {
            "stomach_state": self.state.name,
            "energy_available": self.energy_output,
            "hunger_level": hunger,
            "satisfaction": satisfaction,
            "heart_energy": heart_allocation,
            "brain_energy": brain_allocation,
            "system_energy": system_allocation,
            "metabolic_status": self._metabolic_status(),
        }
    
    def _metabolic_status(self) -> str:
        """Get metabolic status."""
        if self.state == StomachState.HUNGRY:
            return "seeking_nutrients"
        elif self.state == StomachState.SATISFIED:
            return "optimal_metabolism"
        else:  # FULL
            return "processing_overload"
    
    def consume_large_data(self, data: str, data_type: str = "text", chunk_size: int = 100) -> Dict:
        """
        Consume large amounts of data by chunking for brain consumption.
        
        Args:
            data: Large data string to process
            data_type: Type of data (text, json, csv, etc.)
            chunk_size: Size of chunks to create
            
        Returns:
            Chunking status and queue info
        """
        chunks = []
        
        # Parse based on data type
        if data_type == "text":
            # Split by sentences/paragraphs
            paragraphs = data.split('\n\n')
            for para in paragraphs:
                if len(para) > chunk_size:
                    # Further split
                    words = para.split()
                    current_chunk = []
                    current_len = 0
                    
                    for word in words:
                        if current_len + len(word) > chunk_size:
                            chunks.append(' '.join(current_chunk))
                            current_chunk = [word]
                            current_len = len(word)
                        else:
                            current_chunk.append(word)
                            current_len += len(word) + 1
                    
                    if current_chunk:
                        chunks.append(' '.join(current_chunk))
                else:
                    chunks.append(para)
        
        elif data_type == "json":
            try:
                import json
                parsed = json.loads(data)
                # Break into key-value chunks
                if isinstance(parsed, dict):
                    for key, value in parsed.items():
                        chunk = json.dumps({key: value})
                        chunks.append(chunk)
                elif isinstance(parsed, list):
                    # Process in batches
                    for i in range(0, len(parsed), 5):
                        batch = parsed[i:i+5]
                        chunks.append(json.dumps(batch))
            except:
                chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        
        elif data_type == "csv":
            lines = data.split('\n')
            header = lines[0] if lines else ""
            # Group rows
            for i in range(1, len(lines), 10):
                batch = [header] + lines[i:i+10]
                chunks.append('\n'.join(batch))
        
        else:
            # Default: fixed size chunks
            chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        
        # Add all chunks as digestion tasks
        total_nutrition = 0
        for i, chunk in enumerate(chunks):
            # Complexity based on chunk size
            complexity = min(1.0, len(chunk) / 500)
            # Nutrition based on information density
            nutrition = min(1.0, len(chunk) / 200)
            total_nutrition += nutrition
            
            self.consume(f"[CHUNK_{i+1}/{len(chunks)}] {chunk[:100]}...", 
                        complexity=complexity, 
                        nutrition=nutrition)
        
        return {
            "status": "chunked",
            "total_chunks": len(chunks),
            "original_size": len(data),
            "avg_chunk_size": len(data) / len(chunks) if chunks else 0,
            "total_nutrition": total_nutrition,
            "chunks_in_queue": len(self.stomach_queue),
        }
    
    def get_chunks_for_brain(self, count: int = 3) -> List[Dict]:
        """
        Get digested chunks ready for brain consumption.
        
        Returns processed chunks in brain-friendly format.
        """
        ready_chunks = []
        
        # Get from intestine (fully processed)
        for _ in range(min(count, len(self.intestine_queue))):
            if self.intestine_queue:
                task = self.intestine_queue.popleft()
                ready_chunks.append({
                    "content": task.content,
                    "nutrition": task.nutrition,
                    "processed_at": time.time(),
                    "ready": True
                })
        
        # If not enough, get from stomach (partially processed)
        remaining = count - len(ready_chunks)
        for _ in range(min(remaining, len(self.stomach_queue))):
            if self.stomach_queue:
                task = self.stomach_queue[0]  # Peek first
                # Quick process
                task.complexity -= self.digestion_rate * 2
                if task.complexity <= 0:
                    task = self.stomach_queue.popleft()
                    ready_chunks.append({
                        "content": task.content,
                        "nutrition": task.nutrition * 0.8,  # Slightly less nutrition
                        "processed_at": time.time(),
                        "ready": True
                    })
        
        return ready_chunks
    
    def get_status(self) -> str:
        """Get formatted status."""
        emoji = {
            StomachState.HUNGRY: "🍽️",
            StomachState.SATISFIED: "😌",
            StomachState.FULL: "🤢",
        }
        
        return (
            f"{emoji[self.state]} Stomach: {self.state.name} | "
            f"Energy: {self.energy_level:.2f} | "
            f"Stomach: {len(self.stomach_queue)} items | "
            f"Intestine: {len(self.intestine_queue)} items"
        )


def demo_ternary_stomach():
    """Demo ternary stomach."""
    print("=" * 70)
    print("🍽️ TERNARY STOMACH DEMO")
    print("=" * 70)
    print("Energy processing system for AGI")
    print("Smaller than heart: ~250 lines")
    print()
    
    stomach = TernaryStomach()
    
    # Scenario 1: Consume tasks
    print("--- Consuming 5 tasks ---")
    for i in range(5):
        stomach.consume(f"Task_{i}", complexity=0.3, nutrition=0.5)
        time.sleep(0.1)
    
    print(stomach.get_status())
    print()
    
    # Scenario 2: Digest cycles
    print("--- Running 10 digestion cycles ---")
    for i in range(10):
        result = stomach.digest()
        if i % 3 == 0:
            print(f"  Cycle {i+1}: {stomach.get_status()}")
        time.sleep(0.2)
    
    print()
    
    # Scenario 3: Energy outputs
    print("--- Energy Outputs ---")
    outputs = stomach.get_outputs()
    print(f"Stomach State: {outputs['stomach_state']}")
    print(f"Energy Available: {outputs['energy_available']:.2f}")
    print(f"  → Heart: {outputs['heart_energy']:.2f}")
    print(f"  → Brain: {outputs['brain_energy']:.2f}")
    print(f"  → System: {outputs['system_energy']:.2f}")
    print(f"Hunger Level: {outputs['hunger_level']:.2f}")
    print(f"Metabolic Status: {outputs['metabolic_status']}")
    
    # Scenario 4: Large data chunking
    print()
    print("--- Large Data Chunking Demo ---")
    large_text = """
    The Python programming language was created by Guido van Rossum and first released in 1991.
    It emphasizes code readability with its use of significant indentation.
    Python is dynamically typed and garbage-collected.
    It supports multiple programming paradigms including structured, object-oriented, and functional programming.
    Python is often described as a "batteries included" language due to its comprehensive standard library.
    """ * 5  # Make it larger
    
    result = stomach.consume_large_data(large_text, data_type="text", chunk_size=200)
    print(f"Chunked {result['original_size']} chars into {result['total_chunks']} chunks")
    print(f"Avg chunk size: {result['avg_chunk_size']:.0f} chars")
    
    # Digest some chunks
    print("\nDigesting chunks...")
    for _ in range(3):
        stomach.digest()
    
    # Get chunks ready for brain
    brain_chunks = stomach.get_chunks_for_brain(count=3)
    print(f"\nChunks ready for brain: {len(brain_chunks)}")
    for i, chunk in enumerate(brain_chunks, 1):
        print(f"  Chunk {i}: {chunk['content'][:60]}... (nutrition: {chunk['nutrition']:.2f})")
    
    print()
    print("=" * 70)
    print("✅ Ternary Stomach Demo Complete!")
    print("=" * 70)
    print("\nThe stomach feeds the system:")
    print("  - Consumes data/tasks/experiences")
    print("  - Digests into energy")
    print("  - Provides energy to heart (30%) and brain (60%)")
    print("  - Ternary states: HUNGRY/SATISFIED/FULL")
    print("  - NEW: Chunks large data for brain consumption")
    print("=" * 70)


if __name__ == "__main__":
    demo_ternary_stomach()
