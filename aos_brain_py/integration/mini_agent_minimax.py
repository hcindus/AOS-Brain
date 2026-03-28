#!/usr/bin/env python3
"""
Mini-Agent + MiniMax-M2.7 Integration
Direct MiniMax API usage for Mini-Agent with rationed calls
"""

import os
import sys
import anthropic
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.rationed_api_manager import get_ration_manager


class MiniAgentMiniMax:
    """
    Mini-Agent using MiniMax-M2.7 via Anthropic-compatible API.
    
    Features:
    - Direct MiniMax API calls
    - Rationed usage (100/day limit)
    - Thinking block handling
    - Automatic fallback to local brain
    """
    
    def __init__(self, daily_limit: int = 100):
        self.ration = get_ration_manager(daily_limit)
        
        # MiniMax API via Anthropic SDK
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY", 
                "sk-api-AiDiIM7K52eyXaxwrW4nhu2bakhQ0xoa5yWV8avoLFGBIRpeIeEpcC0HjR2wUixnqfni4O-xdWK5hwFkTt8h9JtasU6-nbLUT5iMn5vaWWRNHQpNJKifK1w"),
            base_url="https://api.minimax.io/anthropic"
        )
        
        # Default model
        self.model = "MiniMax-M2.7"  # Use M2.7 for reasoning
        
        print("=" * 70)
        print("🤖 MINI-AGENT + MINIMAX-M2.7")
        print("=" * 70)
        print()
        
    def process(self, query: str, system: str = "You are a helpful assistant.") -> Dict:
        """
        Process query via MiniMax API with rationing.
        
        Args:
            query: User query
            system: System prompt (optional)
            
        Returns:
            Dict with text, thinking, usage info
        """
        agent_name = "Mini-Agent"
        
        # Check ration
        if not self.ration.can_make_call(agent_name):
            return {
                "text": "Daily API limit reached. Using local brain fallback.",
                "thinking": None,
                "model": "local_brain",
                "source": "fallback"
            }
        
        print(f"[Mini-Agent] Query: {query[:50]}...")
        print(f"[Mini-Agent] Routing to MiniMax-{self.model}")
        
        try:
            # Build kwargs
            kwargs = {
                "model": self.model,
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": query}]
                    }
                ]
            }
            
            # Add system prompt if provided
            if system:
                kwargs["system"] = system
            
            # Call MiniMax API
            response = self.client.messages.create(**kwargs)
            
            # Parse blocks
            text_content = []
            thinking_content = []
            
            for block in response.content:
                if hasattr(block, 'type'):
                    if block.type == "thinking":
                        thinking_content.append(block.thinking)
                    elif block.type == "text":
                        text_content.append(block.text)
            
            # Record usage
            tokens = response.usage.output_tokens if hasattr(response, 'usage') else 100
            self.ration.record_call(agent_name, tokens)
            
            result = {
                "text": "\n".join(text_content),
                "thinking": "\n".join(thinking_content) if thinking_content else None,
                "model": response.model,
                "tokens": tokens,
                "source": "minimax_api"
            }
            
            print(f"[Mini-Agent] ✓ Response received")
            print(f"[Mini-Agent] Tokens: {tokens}")
            if thinking_content:
                print(f"[Mini-Agent] Thinking: {len(thinking_content)} blocks")
            
            return result
            
        except Exception as e:
            print(f"[Mini-Agent] ❌ API Error: {e}")
            return {
                "text": f"Error calling MiniMax: {e}",
                "thinking": None,
                "model": "error",
                "source": "error"
            }
    
    def test(self):
        """Test Mini-Agent with MiniMax."""
        print("\n" + "=" * 70)
        print("🧪 Testing Mini-Agent + MiniMax-M2.7")
        print("=" * 70)
        print()
        
        test_queries = [
            "What is 2+2?",
            "Explain recursion in programming",
            "How do I debug a memory leak?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n[{i}] Query: {query}")
            result = self.process(query)
            print(f"   Model: {result['model']}")
            print(f"   Response: {result['text'][:80]}...")
            if result['thinking']:
                print(f"   Thinking: {result['thinking'][:80]}...")
        
        print("\n" + "=" * 70)
        self.ration.print_status()
        print("=" * 70)


def main():
    """Run Mini-Agent with MiniMax."""
    agent = MiniAgentMiniMax(daily_limit=100)
    agent.test()


if __name__ == "__main__":
    main()
