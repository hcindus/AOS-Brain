#!/usr/bin/env python3
"""
Stomach-Heart-Brain Pipeline - Complete AGI Digestion System.

Data Flow:
  1. STOMACH: Consumes large data, chunks it, digests
  2. HEART: Provides rhythm and emotional context
  3. BRAIN: Processes chunks into cognition
  
This creates a complete metabolic cycle for the AGI system.
"""

import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from stomach.ternary_stomach import TernaryStomach
from heart.ternary_heart import TernaryHeart
from brain.seven_region import SevenRegionBrain


class StomachHeartBrainPipeline:
    """
    Complete pipeline: Stomach → Heart → Brain
    
    Processes large data through digestion pipeline:
    - Stomach chunks and digests
    - Heart provides rhythm/emotion
    - Brain thinks and learns
    """
    
    def __init__(self):
        print("=" * 70)
        print("🍽️🫀🧠 STOMACH-HEART-BRAIN PIPELINE")
        print("=" * 70)
        print()
        
        self.stomach = TernaryStomach()
        self.heart = TernaryHeart()
        self.brain = SevenRegionBrain()
        
        # Pipeline state
        self.processed_chunks = 0
        self.total_nutrition = 0.0
        
        print("✅ Pipeline initialized")
        print("  Stomach: Chunks and digests data")
        print("  Heart: Provides rhythm and emotion")
        print("  Brain: Cognition and learning")
        print()
    
    def process_large_data(self, data: str, data_type: str = "text") -> Dict:
        """
        Process large data through complete pipeline.
        
        Args:
            data: Large data to process
            data_type: Type of data (text, json, csv)
            
        Returns:
            Processing results
        """
        print(f"\n--- Processing {len(data)} chars of {data_type} data ---")
        
        # 1. STOMACH: Chunk and digest
        print("[1] STOMACH: Chunking data...")
        stomach_result = self.stomach.consume_large_data(data, data_type)
        print(f"    Created {stomach_result['total_chunks']} chunks")
        
        # Digest cycles to process chunks
        for _ in range(min(5, stomach_result['total_chunks'])):
            self.stomach.digest()
        
        # 2. GET READY CHUNKS
        brain_chunks = self.stomach.get_chunks_for_brain(count=3)
        print(f"    {len(brain_chunks)} chunks ready for brain")
        
        # 3. HEART: Prepare rhythm
        print("[2] HEART: Preparing rhythm...")
        
        # Get energy from stomach
        stomach_outputs = self.stomach.get_outputs()
        heart_energy = stomach_outputs['heart_energy']
        
        # Feed energy context to heart
        heart_inputs = {
            "brain_arousal": min(1.0, len(brain_chunks) / 3),
            "safety": 0.8,
            "connection": 0.6,
            "stress": 0.1 if stomach_outputs['hunger_level'] < 0.5 else 0.4,
        }
        
        heart_outputs = self.heart.beat(heart_inputs)
        print(f"    Heart: {heart_outputs['heart_state']} | "
              f"Emotion: {heart_outputs['heart_emotional_tone']}")
        
        # 4. BRAIN: Process chunks
        print("[3] BRAIN: Processing chunks...")
        thoughts = []
        
        for i, chunk in enumerate(brain_chunks, 1):
            # Prepare brain input with heart influence
            brain_input = {
                "text": chunk['content'],
                "source": "stomach_chunk",
                "arousal": heart_outputs['heart_arousal'],
                "coherence": heart_outputs['heart_coherence'],
                "nutrition": chunk['nutrition'],
            }
            
            # Brain thinks
            thought = self.brain.feed(
                f"[CHUNK {i}] {chunk['content'][:100]}",
                source="stomach_pipeline"
            )
            
            thoughts.append({
                "chunk_id": i,
                "mode": thought.get('mode', 'Unknown'),
                "nutrition_consumed": chunk['nutrition'],
            })
            
            print(f"    Chunk {i}: Brain mode {thought.get('mode')}")
            time.sleep(0.1)
        
        # 5. SUMMARY
        self.processed_chunks += len(brain_chunks)
        self.total_nutrition += sum(c['nutrition'] for c in brain_chunks)
        
        return {
            "chunks_created": stomach_result['total_chunks'],
            "chunks_processed": len(brain_chunks),
            "heart_state": heart_outputs['heart_state'],
            "heart_emotion": heart_outputs['heart_emotional_tone'],
            "brain_modes": [t['mode'] for t in thoughts],
            "total_nutrition": self.total_nutrition,
            "stomach_status": self.stomach.get_status(),
        }
    
    def run_pipeline_cycle(self):
        """Run one complete pipeline cycle."""
        # Stomach digests
        stomach_result = self.stomach.digest()
        
        # Heart beats
        heart_inputs = {
            "brain_arousal": 0.5,
            "safety": 0.7,
            "connection": 0.6,
            "stress": 0.2,
        }
        heart_outputs = self.heart.beat(heart_inputs)
        
        # Get chunks for brain
        chunks = self.stomach.get_chunks_for_brain(count=2)
        
        # Brain processes
        for chunk in chunks:
            self.brain.feed(chunk['content'], source="pipeline")
        
        return {
            "stomach": stomach_result,
            "heart": heart_outputs,
            "brain_ticks": self.brain.tick_count,
        }
    
    def get_pipeline_status(self) -> str:
        """Get complete pipeline status."""
        stomach_status = self.stomach.get_status()
        heart_status = self.heart.get_state_summary()
        
        lines = [
            "=" * 70,
            "🍽️🫀🧠 PIPELINE STATUS",
            "=" * 70,
            stomach_status,
            heart_status,
            f"Brain: {self.brain.tick_count} ticks | Mode: {self.brain.current_mode}",
            f"Processed chunks: {self.processed_chunks}",
            f"Total nutrition: {self.total_nutrition:.2f}",
            "=" * 70,
        ]
        
        return "\n".join(lines)


def demo_pipeline():
    """Demo complete stomach-heart-brain pipeline."""
    print("\n" + "=" * 70)
    print("🍽️🫀🧠 COMPLETE PIPELINE DEMO")
    print("=" * 70)
    print()
    print("Processing large data through complete AGI system:")
    print("  1. STOMACH: Chunks and digests")
    print("  2. HEART: Provides rhythm/emotion")  
    print("  3. BRAIN: Cognition and learning")
    print()
    
    pipeline = StomachHeartBrainPipeline()
    
    # Process large text
    large_document = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, 
    as opposed to natural intelligence displayed by animals including humans.
    AI research has been defined as the field of study of intelligent agents, 
    which refers to any system that perceives its environment and takes actions 
    that maximize its chance of achieving its goals.
    
    The term "artificial intelligence" had previously been used to describe machines 
    that mimic and display "human" cognitive skills that are associated with the human 
    mind, such as "learning" and "problem-solving". This definition has since been 
    rejected by major AI researchers who now describe AI in terms of rationality and 
    acting rationally, which does not limit how intelligence can be articulated.
    
    AI applications include advanced web search engines, recommendation systems, 
    understanding natural speech, self-driving cars, automated decision-making, 
    and competing at the highest level in strategic game systems.
    
    As machines become increasingly capable, tasks considered to require "intelligence" 
    are often removed from the definition of AI, a phenomenon known as the AI effect. 
    For instance, optical character recognition is frequently excluded from things 
    considered to be AI, having become a routine technology.
    """
    
    result = pipeline.process_large_data(large_document, "text")
    
    print("\n" + "=" * 70)
    print("PROCESSING RESULTS")
    print("=" * 70)
    print(f"Chunks created: {result['chunks_created']}")
    print(f"Chunks processed: {result['chunks_processed']}")
    print(f"Heart state: {result['heart_state']} ({result['heart_emotion']})")
    print(f"Brain modes: {', '.join(result['brain_modes'])}")
    print(f"Total nutrition: {result['total_nutrition']:.2f}")
    print()
    print(result['stomach_status'])
    
    print("\n" + "=" * 70)
    print("✅ Pipeline Demo Complete!")
    print("=" * 70)
    print("\nThe AGI digestion system:")
    print("  - Stomach chunks large data")
    print("  - Heart provides emotional context")
    print("  - Brain processes into cognition")
    print("  - Complete metabolic cycle achieved")
    print("=" * 70)


if __name__ == "__main__":
    demo_pipeline()
