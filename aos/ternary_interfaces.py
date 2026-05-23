#!/usr/bin/env python3
"""
AOS Ternary System - Standardized Interfaces
Modular sockets for Heart-Brain-Stomach-Intestine integration

Design Philosophy:
- Each organ implements its interface
- No hard dependencies between organs
- Socket-based communication
- Future-proof assembly
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import time


# ═══════════════════════════════════════════════════════════════════
# HEART INTERFACE - Superior Heart Control
# ═══════════════════════════════════════════════════════════════════

class HeartState(Enum):
    """Ternary heart states"""
    REST = -1      # Recovery
    BALANCE = 0    # Steady
    ACTIVE = 1     # High energy


@dataclass
class HeartBeatOutput:
    """Standardized heart beat output"""
    timestamp: float
    bpm: float
    state: HeartState
    coherence: float          # 0-1
    variability: float        # HRV
    emotional_tone: str       # e.g., "warm", "alert", "calm"
    arousal: float            # 0-1
    energy_output: float      # To brain
    phase: float              # 0-1 in beat cycle
    beat_intensity: float     # Force of beat
    
    # Metadata
    beat_count: int
    model_id: str = "heart_v1"


@dataclass  
class HeartBeatInput:
    """Standardized heart beat input"""
    brain_arousal: float      # 0-1 from brain
    safety: float            # 0-1 safety signal
    stress: float            # 0-1 threat level
    connection: float        # 0-1 social/emotional
    cognitive_load: float    # 0-1 from brain
    
    # Optional feedback
    brain_state: Optional[str] = None
    limbic_reward: Optional[float] = None


class IHeart(ABC):
    """
    Interface: Any Heart must implement this
    
    Usage:
        heart = SuperiorHeart()  # or TernaryHeart(), AdvancedHeart()
        inputs = HeartBeatInput(brain_arousal=0.5, safety=0.8, ...)
        output = heart.beat(inputs)
        
        # output.bpm, output.state, output.emotional_tone, etc.
    """
    
    @abstractmethod
    def beat(self, inputs: HeartBeatInput) -> HeartBeatOutput:
        """
        Single heartbeat cycle
        
        Args:
            inputs: Brain and system feedback
            
        Returns:
            HeartBeatOutput: Rhythm, emotion, arousal signals
        """
        pass
    
    @abstractmethod
    def get_state_summary(self) -> str:
        """Get formatted state summary"""
        pass
    
    @abstractmethod
    def get_metrics(self) -> Dict:
        """Get current metrics for monitoring"""
        pass
    
    # Optional: Connection methods
    def connect_to_brain(self, brain_callback: Callable):
        """Optional: Register brain feedback callback"""
        pass
    
    def receive_brain_feedback(self, feedback: Dict):
        """Optional: Receive direct brain feedback"""
        pass


# ═══════════════════════════════════════════════════════════════════
# BRAIN INTERFACE - Cognitive Core
# ═══════════════════════════════════════════════════════════════════

@dataclass
class BrainInput:
    """Standardized brain input"""
    # From Heart
    heart_bpm: float
    heart_state: HeartState
    heart_coherence: float
    heart_arousal: float
    emotional_tone: str
    
    # Sensory
    observation: Optional[str] = None
    observation_type: str = "system"  # system, user, environment
    
    # Context
    memory_context: Optional[List[Dict]] = None
    urgency: float = 0.5


@dataclass
class BrainOutput:
    """Standardized brain output"""
    timestamp: float
    
    # OODA Phase
    phase: str  # Observe, Orient, Decide, Act
    
    # Decision
    action_type: str
    action_confidence: float
    plan: str
    
    # Affect (to feed back to heart)
    novelty: float        # 0-1
    reward: float         # 0-1
    valence: float        # -1 to 1 (negative/positive)
    risk: float           # 0-1
    
    # Memory
    memory_formed: bool
    memory_novelty: float
    
    # Cognition metrics
    cognitive_load: float
    mode: str  # Analytical, Creative, Cautious, etc.
    
    # Metadata
    tick_count: int
    memories_total: int
    model_id: str = "brain_v3"


class IBrain(ABC):
    """
    Interface: Any Brain must implement this
    
    Usage:
        brain = AOSBrainV3()  # or MinimalBrain(), AdvancedBrain()
        inputs = BrainInput(heart_bpm=72, heart_state=HeartState.BALANCE, ...)
        output = brain.tick(inputs)
        
        # output.action_type, output.novelty, output.memory_formed, etc.
    """
    
    @abstractmethod
    def tick(self, inputs: BrainInput) -> BrainOutput:
        """
        Single OODA cycle
        
        Args:
            inputs: Heart signals and sensory input
            
        Returns:
            BrainOutput: Decision, affect, memory formation
        """
        pass
    
    @abstractmethod
    def get_status(self) -> Dict:
        """Get brain status for monitoring"""
        pass
    
    @abstractmethod
    def save_state(self) -> bool:
        """Save brain state"""
        pass
    
    # Optional: Memory access
    def retrieve_memories(self, query: str, n: int = 3) -> List[Dict]:
        """Optional: Retrieve relevant memories"""
        return []
    
    def receive_heart_signals(self, heart_output: HeartBeatOutput):
        """Optional: Direct heart signal injection"""
        pass


# ═══════════════════════════════════════════════════════════════════
# STOMACH INTERFACE - Energy/Digestion
# ═══════════════════════════════════════════════════════════════════

class StomachState(Enum):
    """Ternary stomach states"""
    HUNGRY = "hungry"
    SATISFIED = "satisfied"
    FULL = "full"


@dataclass
class DigestionOutput:
    """Standardized stomach output"""
    timestamp: float
    
    state: StomachState
    fullness: float           # 0-1
    
    # Energy production
    energy_produced: float    # Output to heart
    efficiency: float         # 0-1
    
    # Waste
    waste_generated: float
    
    # Cycle info
    cycle_count: int
    total_digested: float
    total_energy_produced: float
    
    model_id: str = "stomach_v1"


@dataclass
class DigestionInput:
    """Standardized stomach input"""
    input_amount: float       # How much consumed
    input_type: str = "data"  # data, experience, information
    
    # From Heart
    heart_energy_demand: float = 0.5  # How much energy heart needs
    stress_level: float = 0.0  # Stress affects digestion


class IStomach(ABC):
    """
    Interface: Any Stomach must implement this
    
    Usage:
        stomach = TernaryStomach()
        inputs = DigestionInput(input_amount=0.1, heart_energy_demand=0.6)
        output = stomach.digest(inputs)
        
        # output.energy_produced, output.state, etc.
    """
    
    @abstractmethod
    def digest(self, inputs: DigestionInput) -> DigestionOutput:
        """
        Single digestion cycle
        
        Args:
            inputs: Input amount and heart demand
            
        Returns:
            DigestionOutput: Energy produced, state
        """
        pass
    
    @abstractmethod
    def get_status(self) -> Dict:
        """Get stomach status"""
        pass


# ═══════════════════════════════════════════════════════════════════
# INTESTINE INTERFACE - Processing/Distribution
# ═══════════════════════════════════════════════════════════════════

@dataclass
class IntestineOutput:
    """Standardized intestine output"""
    timestamp: float
    
    # Distribution
    nutrients_to_heart: float
    nutrients_to_brain: float
    nutrients_to_system: float
    
    # Processing
    absorption_rate: float    # 0-1
    processing_efficiency: float
    
    # State
    load: float              # 0-1 how full
    cycle_count: int
    
    model_id: str = "intestine_v1"


@dataclass
class IntestineInput:
    """Standardized intestine input"""
    from_stomach: DigestionOutput
    
    # Distribution requests
    heart_needs: float = 0.5
    brain_needs: float = 0.5
    system_needs: float = 0.3


class IIntestine(ABC):
    """
    Interface: Any Intestine must implement this
    
    Usage:
        intestine = TernaryIntestine()
        inputs = IntestineInput(from_stomach=stomach_output, heart_needs=0.6)
        output = intestine.process(inputs)
        
        # output.nutrients_to_heart, output.absorption_rate, etc.
    """
    
    @abstractmethod
    def process(self, inputs: IntestineInput) -> IntestineOutput:
        """
        Process nutrients and distribute
        
        Args:
            inputs: Digested material and organ needs
            
        Returns:
            IntestineOutput: Distribution to organs
        """
        pass
    
    @abstractmethod
    def get_status(self) -> Dict:
        """Get intestine status"""
        pass


# ═══════════════════════════════════════════════════════════════════
# TERNARY SYSTEM ASSEMBLER
# ═══════════════════════════════════════════════════════════════════

class TernarySystemAssembler:
    """
    Assembles any compatible Heart + Brain + Stomach + Intestine
    
    Usage:
        # Create organs (any implementation)
        heart = SuperiorHeart()
        brain = AOSBrainV3()
        stomach = TernaryStomach()
        intestine = TernaryIntestine()
        
        # Assemble
        system = TernarySystemAssembler()
        system.connect_heart(heart)
        system.connect_brain(brain)
        system.connect_stomach(stomach)
        system.connect_intestine(intestine)
        
        # Run
        system.run()
    """
    
    def __init__(self):
        self.heart: Optional[IHeart] = None
        self.brain: Optional[IBrain] = None
        self.stomach: Optional[IStomach] = None
        self.intestine: Optional[IIntestine] = None
        
        self.running = False
        self.cycle_count = 0
    
    def connect_heart(self, heart: IHeart):
        """Connect any heart implementing IHeart"""
        self.heart = heart
        print(f"[Assembler] Connected Heart: {heart.__class__.__name__}")
    
    def connect_brain(self, brain: IBrain):
        """Connect any brain implementing IBrain"""
        self.brain = brain
        print(f"[Assembler] Connected Brain: {brain.__class__.__name__}")
    
    def connect_stomach(self, stomach: IStomach):
        """Connect any stomach implementing IStomach"""
        self.stomach = stomach
        print(f"[Assembler] Connected Stomach: {stomach.__class__.__name__}")
    
    def connect_intestine(self, intestine: IIntestine):
        """Connect any intestine implementing IIntestine"""
        self.intestine = intestine
        print(f"[Assembler] Connected Intestine: {intestine.__class__.__name__}")
    
    def run_cycle(self):
        """One complete ternary cycle"""
        # 1. STOMACH digests
        if self.stomach:
            stomach_input = DigestionInput(
                input_amount=0.1,
                heart_energy_demand=0.6 if self.heart else 0.5
            )
            stomach_output = self.stomach.digest(stomach_input)
        else:
            stomach_output = None
        
        # 2. INTESTINE processes and distributes
        if self.intestine and stomach_output:
            intestine_input = IntestineInput(
                from_stomach=stomach_output,
                heart_needs=0.6,
                brain_needs=0.5
            )
            intestine_output = self.intestine.process(intestine_input)
            heart_energy = intestine_output.nutrients_to_heart
        else:
            heart_energy = 0.5
        
        # 3. HEART beats (with energy from stomach)
        if self.heart:
            heart_input = HeartBeatInput(
                brain_arousal=self.brain.get_status().get("novelty", 0.5) if self.brain else 0.5,
                safety=0.8,
                stress=0.2,
                connection=0.6,
                cognitive_load=0.5
            )
            heart_output = self.heart.beat(heart_input)
        else:
            # Default heartbeat if no heart
            heart_output = HeartBeatOutput(
                timestamp=time.time(),
                bpm=72,
                state=HeartState.BALANCE,
                coherence=0.5,
                variability=0.5,
                emotional_tone="neutral",
                arousal=0.5,
                energy_output=0.5,
                phase=0.0,
                beat_intensity=0.5,
                beat_count=self.cycle_count
            )
        
        # 4. BRAIN thinks (with heart signals)
        if self.brain:
            brain_input = BrainInput(
                heart_bpm=heart_output.bpm,
                heart_state=heart_output.state,
                heart_coherence=heart_output.coherence,
                heart_arousal=heart_output.arousal,
                emotional_tone=heart_output.emotional_tone,
                observation=f"Heart beat at {heart_output.bpm} BPM, emotion: {heart_output.emotional_tone}"
            )
            brain_output = self.brain.tick(brain_input)
        else:
            brain_output = None
        
        # 5. Update cycle
        self.cycle_count += 1
        
        return {
            "cycle": self.cycle_count,
            "heart": heart_output,
            "brain": brain_output,
            "stomach": stomach_output
        }
    
    def run(self, cycles: int = 100):
        """Run for specified cycles"""
        print("\n" + "=" * 70)
        print("  TERNARY SYSTEM ASSEMBLER - RUNNING")
        print("=" * 70)
        print(f"  Heart: {self.heart.__class__.__name__ if self.heart else 'None'}")
        print(f"  Brain: {self.brain.__class__.__name__ if self.brain else 'None'}")
        print(f"  Stomach: {self.stomach.__class__.__name__ if self.stomach else 'None'}")
        print(f"  Intestine: {self.intestine.__class__.__name__ if self.intestine else 'None'}")
        print("=" * 70 + "\n")
        
        self.running = True
        
        for i in range(cycles):
            result = self.run_cycle()
            
            # Display every 10 cycles
            if i % 10 == 0:
                heart = result["heart"]
                brain = result["brain"]
                
                if brain:
                    print(f"[Cycle {i:3d}] 🫀 {heart.bpm:.0f} BPM ({heart.emotional_tone:10s}) | "
                          f"🧠 {brain.tick_count} ticks | Memories: {brain.memories_total}")
                else:
                    print(f"[Cycle {i:3d}] 🫀 {heart.bpm:.0f} BPM ({heart.emotional_tone:10s})")
            
            # Heart controls timing
            time.sleep(60.0 / result["heart"].bpm)
        
        print("\n" + "=" * 70)
        print("  TERNARY SYSTEM COMPLETE")
        print("=" * 70)


# Example implementations
if __name__ == "__main__":
    print("=" * 70)
    print("  TERNARY INTERFACES - TEST")
    print("=" * 70)
    
    # Demonstrate that any compatible organ can be connected
    print("\nInterface definitions loaded.")
    print("Any organ implementing these can connect to any other.")
    print("\nTo use:")
    print("  from ternary_interfaces import IHeart, IBrain, IStomach, IIntestine")
    print("  from ternary_interfaces import TernarySystemAssembler")
    print("")
    print("  class MyHeart(IHeart):")
    print("      def beat(self, inputs): ...")
    print("")
    print("  class MyBrain(IBrain):")  
    print("      def tick(self, inputs): ...")
    print("")
    print("  system = TernarySystemAssembler()")
    print("  system.connect_heart(MyHeart())")
    print("  system.connect_brain(MyBrain())")
    print("  system.run()")
