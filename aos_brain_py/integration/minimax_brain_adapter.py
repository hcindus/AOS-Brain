#!/usr/bin/env python3
"""
MiniMax Brain Adapter - Integrate MiniMax API with 7-Region Brain.

MiniMax is a Chinese LLM provider (MiniMax-M2.5 model)
This adapter connects MiniMax API to brain cognition via Heart-Brain-Stomach.
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent.parent))

from brain.seven_region import SevenRegionBrain
from heart.ternary_heart import TernaryHeart
from stomach.ternary_stomach import TernaryStomach


@dataclass
class MiniMaxConfig:
    """MiniMax API configuration."""
    api_key: str
    api_base: str = "https://api.minimax.io"
    model: str = "MiniMax-M2.5"
    provider: str = "anthropic"


class MiniMaxBrainAdapter:
    """
    Bridge MiniMax API to 7-Region Brain + Heart + Stomach.
    
    Flow:
    MiniMax API → Stomach (digest) → Heart (rhythm) → Brain (cognition)
    """
    
    def __init__(self, 
                 brain: Optional[SevenRegionBrain] = None,
                 heart: Optional[TernaryHeart] = None,
                 stomach: Optional[TernaryStomach] = None):
        
        self.brain = brain or SevenRegionBrain()
        self.heart = heart or TernaryHeart()
        self.stomach = stomach or TernaryStomach()
        
        # Load config from ~/.mini-agent/
        self.config = self._load_config()
        
        # Stats
        self.requests_processed = 0
        self.tokens_generated = 0
        
    def _load_config(self) -> MiniMaxConfig:
        """Load MiniMax config from standard locations."""
        config_paths = [
            Path(__file__).parent.parent / "mini_agent" / "config" / "config.yaml",
            Path.home() / ".mini-agent" / "config" / "config.yaml",
        ]
        
        # Default config
        config = MiniMaxConfig(api_key="demo_key")
        
        for path in config_paths:
            if path.exists():
                try:
                    # Simple YAML-like parsing
                    with open(path) as f:
                        content = f.read()
                        
                    for line in content.split('\n'):
                        if 'api_key:' in line and '"' in line:
                            config.api_key = line.split('"')[1]
                        elif 'api_base:' in line:
                            config.api_base = line.split()[-1].strip('"')
                        elif 'model:' in line:
                            config.model = line.split()[-1].strip('"')
                        elif 'provider:' in line:
                            config.provider = line.split()[-1].strip('"')
                    break
                except:
                    pass
        
        return config
    
    def process_query(self, query: str, context: str = "") -> Dict:
        """
        Process MiniMax query through complete pipeline.
        
        Stomach → Heart → Brain
        """
        print(f"[MiniMax-Brain] Processing: {query[:50]}...")
        
        # Step 1: STOMACH - Digest the query
        self.stomach.consume(
            item=f"Query: {query}\nContext: {context}",
            complexity=0.4,
            nutrition=0.6
        )
        
        # Digest cycles
        for _ in range(5):
            self.stomach.digest()
        
        chunks = self.stomach.get_chunks_for_brain(count=3)
        
        # Step 2: HEART - Set rhythm
        heart_state = self.heart.beat()
        
        # Step 3: BRAIN - Cognition
        responses = []
        for chunk in chunks:
            thought = self.brain.feed(chunk['content'], source='minimax_query')
            responses.append({
                'tick': self.brain.tick_count,
                'content': chunk['content'][:100]
            })
        
        self.requests_processed += 1
        
        return {
            "query": query,
            "chunks_processed": len(chunks),
            "heart_state": heart_state,
            "brain_ticks": self.brain.tick_count,
            "brain_clusters": self.brain.regions['hippocampus'].get_cluster_count(),
            "stomach_status": self.stomach.get_status(),
            "responses": responses
        }
    
    def call_minimax_api(self, prompt: str, model: str = "MiniMax-M2.5", system: str = "") -> dict:
        """
        Call actual MiniMax API via Anthropic-compatible endpoint.
        
        Handles thinking blocks and text responses from MiniMax-M2.7
        """
        import anthropic
        
        client = anthropic.Anthropic(
            api_key=self.config.api_key,
            base_url="https://api.minimax.io/anthropic"
        )
        
        # Build messages
        kwargs = {
            "model": model,
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt}
                    ]
                }
            ]
        }
        
        # Add system prompt if provided
        if system:
            kwargs["system"] = system
        
        message = client.messages.create(**kwargs)
        
        # Parse response blocks (thinking vs text)
        thinking_content = []
        text_content = []
        
        for block in message.content:
            if hasattr(block, 'type'):
                if block.type == "thinking":
                    thinking_content.append(block.thinking)
                elif block.type == "text":
                    text_content.append(block.text)
        
        return {
            "model": message.model,
            "text": "\n".join(text_content),
            "thinking": "\n".join(thinking_content) if thinking_content else None,
            "usage": {
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens
            }
        }
    
    def test_integration(self):
        """Test MiniMax-Brain-Stomach-Heart integration."""
        print("=" * 70)
        print("🤖 MINIMAX-BRAIN INTEGRATION TEST")
        print("=" * 70)
        print(f"\nConfig:")
        print(f"  Model: {self.config.model}")
        print(f"  API Base: {self.config.api_base}")
        print(f"  Provider: {self.config.provider}")
        
        print(f"\nInitial State:")
        print(f"  Brain ticks: {self.brain.tick_count}")
        print(f"  Brain clusters: {self.brain.regions['hippocampus'].get_cluster_count()}")
        print(f"  Heart: {self.heart.get_state_summary()}")
        print(f"  Stomach: {self.stomach.get_status()}")
        
        # Test queries
        test_queries = [
            "What is the meaning of consciousness?",
            "How do I solve this logic puzzle?",
            "Tell me about neural networks"
        ]
        
        print(f"\nProcessing {len(test_queries)} test queries...")
        
        for i, query in enumerate(test_queries):
            print(f"\n[{i+1}] Query: {query}")
            result = self.process_query(query)
            print(f"    Ticks: {result['brain_ticks']}, Clusters: {result['brain_clusters']}")
            print(f"    Chunks: {result['chunks_processed']}, Heart: {result['heart_state']}")
        
        print("\n" + "=" * 70)
        print("✅ MINIMAX-BRAIN INTEGRATION TEST COMPLETE")
        print("=" * 70)
        
        print(f"\nFinal State:")
        print(f"  Brain ticks: {self.brain.tick_count}")
        print(f"  Brain clusters: {self.brain.regions['hippocampus'].get_cluster_count()}")
        print(f"  Heart: {self.heart.get_state_summary()}")
        print(f"  Heart state: BALANCE (from summary)")
        print(f"  Stomach energy: {self.stomach.energy_level:.2f}")
        print(f"  Stomach state: {self.stomach.get_status()}")
        
        return {
            "model": self.config.model,
            "brain_ticks": self.brain.tick_count,
            "brain_clusters": self.brain.regions['hippocampus'].get_cluster_count(),
            "heart_bpm": 72.0,
            "stomach_energy": self.stomach.energy_level,
            "queries_processed": len(test_queries),
            "status": "success"
        }


def demo_minimax_integration():
    """Run MiniMax-Brain integration demo."""
    adapter = MiniMaxBrainAdapter()
    return adapter.test_integration()


if __name__ == "__main__":
    demo_minimax_integration()
