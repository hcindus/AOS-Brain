#!/usr/bin/env python3
"""
AOS Intestine v2.0 - Implements IIntestine
Distributes digested information to organs
"""

import sys
sys.path.insert(0, '/root/.aos/aos')

import time
from typing import Dict, List
from dataclasses import dataclass

from ternary_interfaces import IIntestine, IntestineInput, IntestineOutput


class InformationIntestine(IIntestine):
    """
    Information Intestine - Distributes nutrients to organs
    
    Receives digested information from stomach
    Distributes to:
    - Heart (energy for rhythm)
    - Brain (cognition)
    - System (general operations)
    """
    
    def __init__(self):
        self.load = 0.0  # Current processing load
        self.cycle_count = 0
        
        # Distribution history
        self.distribution_log: List[Dict] = []
        
        # Absorption efficiency
        self.absorption_rate = 0.85
        self.processing_efficiency = 0.9
        
        # Current batch being processed
        self.current_batch: List[Dict] = []
        
        print("[InformationIntestine] Initialized - Distribution System")
    
    def process(self, inputs: IntestineInput) -> IntestineOutput:
        """
        Implements IIntestine.process()
        Process digested info and distribute to organs
        """
        self.cycle_count += 1
        
        # Get batch from stomach
        stomach_output = inputs.from_stomach
        batch = stomach_output.__dict__.get('digested_queue', [])
        
        if not batch:
            # No input, return empty distribution
            return IntestineOutput(
                timestamp=time.time(),
                nutrients_to_heart=0.0,
                nutrients_to_brain=0.0,
                nutrients_to_system=0.0,
                absorption_rate=self.absorption_rate,
                processing_efficiency=self.processing_efficiency,
                load=self.load,
                cycle_count=self.cycle_count,
                model_id="intestine_v2"
            )
        
        # Calculate total energy in batch
        total_energy = sum(item.get('energy', 0) for item in batch)
        
        # Determine needs
        heart_needs = inputs.heart_needs  # 0-1
        brain_needs = inputs.brain_needs  # 0-1
        system_needs = inputs.system_needs  # 0-1
        
        # Normalize needs
        total_needs = heart_needs + brain_needs + system_needs
        if total_needs == 0:
            total_needs = 1.5  # Default distribution
        
        # Calculate distribution ratios
        heart_ratio = heart_needs / total_needs
        brain_ratio = brain_needs / total_needs
        system_ratio = system_needs / total_needs
        
        # Distribute with absorption efficiency
        to_heart = total_energy * heart_ratio * self.absorption_rate
        to_brain = total_energy * brain_ratio * self.absorption_rate
        to_system = total_energy * system_ratio * self.absorption_rate
        
        # Apply processing efficiency (some loss in distribution)
        to_heart *= self.processing_efficiency
        to_brain *= self.processing_efficiency
        to_system *= self.processing_efficiency
        
        # Update load based on batch size
        self.load = min(1.0, len(batch) / 20)
        
        # Log distribution
        self.distribution_log.append({
            "timestamp": time.time(),
            "batch_size": len(batch),
            "total_energy": total_energy,
            "to_heart": to_heart,
            "to_brain": to_brain,
            "to_system": to_system
        })
        
        # Trim log
        if len(self.distribution_log) > 100:
            self.distribution_log = self.distribution_log[-50:]
        
        return IntestineOutput(
            timestamp=time.time(),
            nutrients_to_heart=to_heart,
            nutrients_to_brain=to_brain,
            nutrients_to_system=to_system,
            absorption_rate=self.absorption_rate,
            processing_efficiency=self.processing_efficiency,
            load=self.load,
            cycle_count=self.cycle_count,
            model_id="intestine_v2"
        )
    
    def get_status(self) -> Dict:
        """Implements IIntestine.get_status()"""
        return {
            "load": self.load,
            "cycle_count": self.cycle_count,
            "absorption_rate": self.absorption_rate,
            "processing_efficiency": self.processing_efficiency,
            "distributions": len(self.distribution_log)
        }
    
    def get_distribution_summary(self) -> str:
        """Get summary of recent distributions"""
        if not self.distribution_log:
            return "No distributions yet"
        
        recent = self.distribution_log[-10:]
        total_heart = sum(d["to_heart"] for d in recent)
        total_brain = sum(d["to_brain"] for d in recent)
        total_system = sum(d["to_system"] for d in recent)
        
        return (f"Recent distributions: Heart={total_heart:.1f}, "
                f"Brain={total_brain:.1f}, System={total_system:.1f}")


if __name__ == "__main__":
    print("=" * 70)
    print("  INFORMATION INTESTINE v2.0 - TEST")
    print("=" * 70)
    
    intestine = InformationIntestine()
    
    # Create mock stomach output
    from ternary_interfaces import DigestionOutput, StomachState
    
    mock_stomach = DigestionOutput(
        timestamp=time.time(),
        state=StomachState.SATISFIED,
        fullness=0.5,
        energy_produced=2.5,
        efficiency=0.7,
        waste_generated=0.5,
        cycle_count=10,
        total_digested=100.0,
        total_energy_produced=50.0
    )
    
    # Mock digested queue
    mock_stomach.__dict__['digested_queue'] = [
        {"source": "api", "content": "Status OK", "energy": 0.5},
        {"source": "log", "content": "Error processed", "energy": 0.8},
        {"source": "sensor", "content": "Temp 72F", "energy": 0.3},
    ]
    
    # Test processing
    print("\nProcessing digested information...")
    
    inputs = IntestineInput(
        from_stomach=mock_stomach,
        heart_needs=0.6,
        brain_needs=0.8,
        system_needs=0.3
    )
    
    output = intestine.process(inputs)
    
    print(f"\nDistribution:")
    print(f"  To Heart: {output.nutrients_to_heart:.2f}")
    print(f"  To Brain: {output.nutrients_to_brain:.2f}")
    print(f"  To System: {output.nutrients_to_system:.2f}")
    print(f"  Absorption: {output.absorption_rate:.1%}")
    print(f"  Load: {output.load:.2f}")
    
    print("\n" + intestine.get_distribution_summary())
    print("=" * 70)
