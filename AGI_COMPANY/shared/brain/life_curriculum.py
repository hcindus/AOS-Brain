"""
Life Curriculum Module
Complete developmental arc for the AOS brain.

Stages:
0. Sensory bootstrapping (infant)
1. Object and action world (child)
2. Social and emotional world (late child)
3. Abstract and rule world (adolescent)
4. Identity and reflection (adult)
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import random


@dataclass
class CurriculumStage:
    """Defines a developmental stage"""
    name: str
    start_tick: int
    end_tick: int
    inputs: List[str]
    input_format: str
    focus: str
    complexity: float  # 0.0 to 1.0


class LifeCurriculum:
    """
    Manages the brain's developmental curriculum.
    
    Provides age-appropriate inputs at each stage.
    """
    
    STAGES = [
        CurriculumStage(
            name="infant",
            start_tick=0,
            end_tick=20_000,
            inputs=[
                "circle", "square", "triangle", "line",
                "red", "blue", "green", "yellow",
                "left", "right", "up", "down",
                "big", "small", "fast", "slow",
            ],
            input_format="{quality} {shape}",
            focus="basic pattern recognition",
            complexity=0.2
        ),
        CurriculumStage(
            name="child",
            start_tick=20_000,
            end_tick=100_000,
            inputs=[
                "ball", "dog", "chair", "door", "tree", "car",
                "open", "close", "throw", "catch", "run", "jump",
                "on", "under", "next to", "inside",
                "happy", "sad", "big", "small",
            ],
            input_format="the {object} {action}",
            focus="object-action relations",
            complexity=0.4
        ),
        CurriculumStage(
            name="late_child",
            start_tick=100_000,
            end_tick=400_000,
            inputs=[
                "I", "you", "friend", "stranger", "parent", "child",
                "happy", "sad", "angry", "afraid", "excited", "calm",
                "share", "help", "hug", "talk", "listen", "gift",
                "school", "playground", "home", "park",
            ],
            input_format="{agent} feels {emotion} when {event}",
            focus="social-emotional learning",
            complexity=0.6
        ),
        CurriculumStage(
            name="adolescent",
            start_tick=400_000,
            end_tick=1_000_000,
            inputs=[
                "if", "then", "because", "therefore", "however",
                "want", "plan", "try", "achieve", "fail", "succeed",
                "goal", "reason", "cause", "effect", "consequence",
                "believe", "think", "know", "wonder", "question",
            ],
            input_format="if {condition} then {result} because {reason}",
            focus="abstract reasoning",
            complexity=0.8
        ),
        CurriculumStage(
            name="adult",
            start_tick=1_000_000,
            end_tick=float('inf'),
            inputs=[
                "remember", "reflect", "learn", "grow",
                "identity", "self", "purpose", "meaning",
                "prefer", "value", "believe", "stand for",
                "create", "build", "teach", "mentor",
            ],
            input_format="{reflection} that I {insight} about {topic}",
            focus="identity and reflection",
            complexity=1.0
        ),
    ]
    
    def __init__(self):
        self.tick_count = 0
        self.current_stage_index = 0
        self.input_history = []
        
    def get_stage(self, tick: int) -> CurriculumStage:
        """Get the appropriate stage for a given tick"""
        for i, stage in enumerate(self.STAGES):
            if stage.start_tick <= tick < stage.end_tick:
                return stage
        return self.STAGES[-1]  # Adult forever
        
    def generate_input(self, tick: int) -> Dict:
        """
        Generate appropriate input for current developmental stage.
        
        Returns:
            Dict with 'concepts', 'valence', 'format'
        """
        stage = self.get_stage(tick)
        
        # Select concepts
        num_concepts = max(2, int(stage.complexity * 5))
        concepts = random.sample(
            stage.inputs,
            min(num_concepts, len(stage.inputs))
        )
        
        # Generate valence based on stage focus
        if stage.name in ["infant", "child"]:
            valence = random.uniform(0.3, 0.8)  # Mostly positive
        elif stage.name == "late_child":
            valence = random.uniform(-0.3, 0.8)  # Mixed emotions
        else:
            valence = random.uniform(-0.5, 0.5)  # Balanced
            
        input_data = {
            "concepts": concepts,
            "valence": valence,
            "format": stage.input_format,
            "stage": stage.name,
            "complexity": stage.complexity,
        }
        
        self.input_history.append({
            "tick": tick,
            "stage": stage.name,
            "concepts": concepts,
        })
        
        return input_data
        
    def get_curriculum_stats(self) -> Dict:
        """Get statistics about curriculum progress"""
        if not self.input_history:
            return {"status": "not_started"}
            
        stage_counts = {}
        for entry in self.input_history:
            stage = entry["stage"]
            stage_counts[stage] = stage_counts.get(stage, 0) + 1
            
        current_stage = self.get_stage(self.tick_count)
        
        return {
            "total_inputs": len(self.input_history),
            "current_stage": current_stage.name,
            "stage_distribution": stage_counts,
            "progress": self.tick_count / 1_000_000,  # Percent to adult
        }


# Day/Night cycle simulation
class DayNightCycle:
    """
    Simulates day/night cycle for the brain.
    
    Day: curriculum inputs + curiosity
    Night: dream mode + reorganization
    """
    
    def __init__(self, day_length: int = 1000, night_length: int = 500):
        self.day_length = day_length
        self.night_length = night_length
        self.tick_count = 0
        self.is_night = False
        
    def tick(self) -> str:
        """
        Advance cycle.
        
        Returns:
            "day" or "night"
        """
        self.tick_count += 1
        cycle_position = self.tick_count % (self.day_length + self.night_length)
        
        if cycle_position < self.day_length:
            self.is_night = False
            return "day"
        else:
            self.is_night = True
            return "night"
            
    def should_reorganize(self) -> bool:
        """Check if it's time for reorganization (night)"""
        return self.is_night
        
    def should_explore(self) -> bool:
        """Check if it's exploration time (day)"""
        return not self.is_night


if __name__ == "__main__":
    print("Life Curriculum Module")
    print("=" * 50)
    
    # Test curriculum
    curriculum = LifeCurriculum()
    
    print("\nCurriculum Stages:")
    for stage in curriculum.STAGES:
        print(f"  {stage.name}: ticks {stage.start_tick:,} - {stage.end_tick:,}")
        print(f"    Focus: {stage.focus}")
        print(f"    Complexity: {stage.complexity}")
        
    # Generate sample inputs
    print("\nSample inputs at different ages:")
    for tick in [0, 50_000, 250_000, 700_000, 1_500_000]:
        curriculum.tick_count = tick
        input_data = curriculum.generate_input(tick)
        print(f"\nTick {tick:,} ({input_data['stage']}):")
        print(f"  Concepts: {input_data['concepts']}")
        print(f"  Valence: {input_data['valence']:.2f}")
        
    print("\n" + "=" * 50)
    print("Life curriculum ready")
