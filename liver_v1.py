#!/usr/bin/env python3
"""
AOS LIVER v1.0 - Ternary Blood Filtration
Biological analogy: Filters blood, processes toxins, produces bile for digestion

Ternary States:
- CLEAN: Input is pure signal, pass through unchanged
- PURIFY: Input has noise, filter and enhance signal
- TOXIC: Input is garbage/corrupted, neutralize and discard
"""

import time
import re
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum, auto


class LiverState(Enum):
    CLEAN = auto()    # Signal is clear, no filtering needed
    PURIFY = auto() # Signal mixed with noise, filtering required
    TOXIC = auto()   # Input is garbage, neutralize and discard


@dataclass
class BloodSample:
    """A unit of information flowing through the system (like blood)"""
    source: str           # Where it came from
    content: str          # The actual content
    timestamp: float      # When received
    flow_rate: float     # How fast it's coming (data velocity)
    
    @property
    def toxicity(self) -> float:
        """Calculate toxicity score (0.0 = pure signal, 1.0 = pure noise)"""
        score = 0.0
        
        # Check for repetitive patterns (noise indicator)
        if len(self.content) > 0:
            unique_chars = len(set(self.content.lower()))
            repetition = 1 - (unique_chars / max(len(self.content), 1))
            score += repetition * 0.3
        
        # Check for random/gibberish content
        words = self.content.split()
        if len(words) > 0:
            avg_word_len = sum(len(w) for w in words) / len(words)
            if avg_word_len > 15 or avg_word_len < 2:
                score += 0.2
        
        # Check for excessive punctuation/special chars
        special_chars = sum(1 for c in self.content if not c.isalnum() and not c.isspace())
        if len(self.content) > 0:
            special_ratio = special_chars / len(self.content)
            if special_ratio > 0.3:
                score += 0.25
        
        # High flow rate = potential spam/noise
        if self.flow_rate > 10.0:
            score += 0.25
        
        return min(1.0, score)
    
    @property
    def information_density(self) -> float:
        """Measure of signal per unit of content (0.0-1.0)"""
        if not self.content:
            return 0.0
        
        # Count meaningful tokens (words, numbers, structured data)
        words = len([w for w in self.content.split() if len(w) > 2])
        sentences = self.content.count('.') + self.content.count('!') + self.content.count('?')
        numbers = len(re.findall(r'\d+', self.content))
        
        # Information units per character
        total_units = words + sentences + numbers
        density = total_units / max(len(self.content) / 10, 1)
        
        return min(1.0, density / 5)  # Normalize


class AOSLiverV1:
    """
    Ternary Liver - Filters incoming data before it reaches the brain
    
    Like a biological liver:
    - CLEAN: Pure signal flows to brain immediately
    - PURIFY: Mixed signal gets filtered, enhanced, then passed
    - TOXIC: Garbage is neutralized and stored as bile (waste log)
    """
    
    def __init__(self, 
                 toxic_threshold: float = 0.7,
                 purify_threshold: float = 0.3,
                 bile_capacity: int = 1000):
        
        self.toxic_threshold = toxic_threshold    # Above this = TOXIC
        self.purify_threshold = purify_threshold  # Above this = PURIFY
        self.bile_capacity = bile_capacity        # Waste storage
        
        self.state = LiverState.CLEAN
        self.bile = []  # Waste log (like bile storage)
        self.filtered_count = 0
        self.toxic_count = 0
        
        print(f"[Liver v1.0] Initialized - ternary filtration")
        print(f"  CLEAN (<{purify_threshold}) → Pass through")
        print(f"  PURIFY ({purify_threshold}-{toxic_threshold}) → Filter & enhance")
        print(f"  TOXIC (>{toxic_threshold}) → Neutralize & discard")
    
    def process(self, sample: BloodSample) -> Tuple[LiverState, Optional[str], dict]:
        """
        Process a blood sample through the liver
        
        Returns:
            (state, filtered_content, metadata)
        """
        toxicity = sample.toxicity
        density = sample.information_density
        
        # Determine state
        if toxicity >= self.toxic_threshold:
            self.state = LiverState.TOXIC
            result = self._neutralize(sample)
            
        elif toxicity >= self.purify_threshold:
            self.state = LiverState.PURIFY
            result = self._purify(sample)
            
        else:
            self.state = LiverState.CLEAN
            result = self._pass_through(sample)
        
        self.filtered_count += 1
        
        metadata = {
            "original_toxicity": toxicity,
            "original_density": density,
            "processing_time": time.time() - sample.timestamp,
            "action": self.state.name
        }
        
        return self.state, result, metadata
    
    def _pass_through(self, sample: BloodSample) -> str:
        """CLEAN: Signal is clear, pass unchanged"""
        return sample.content
    
    def _purify(self, sample: BloodSample) -> str:
        """PURIFY: Filter noise, enhance signal"""
        content = sample.content
        
        # Remove excessive whitespace
        content = ' '.join(content.split())
        
        # Remove repetitive characters
        content = re.sub(r'(.)\1{3,}', r'\1\1', content)
        
        # Extract key sentences (those with numbers or specific keywords)
        sentences = content.split('.')
        important = [s for s in sentences if any(
            keyword in s.lower() for keyword in 
            ['error', 'warning', 'success', 'fail', 'complete', 'critical', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        )]
        
        if important:
            return '. '.join(important[:3]) + '.'
        return content[:200]  # Truncate if no clear signal found
    
    def _neutralize(self, sample: BloodSample) -> None:
        """TOXIC: Store as bile (waste), return nothing"""
        self.toxic_count += 1
        
        bile_entry = {
            "timestamp": time.time(),
            "source": sample.source,
            "toxicity": sample.toxicity,
            "preview": sample.content[:50] + "..." if len(sample.content) > 50 else sample.content
        }
        
        self.bile.append(bile_entry)
        
        # Prune old bile if at capacity
        if len(self.bile) > self.bile_capacity:
            self.bile.pop(0)
        
        return None
    
    def get_status(self) -> dict:
        """Current liver status"""
        return {
            "state": self.state.name,
            "filtered_total": self.filtered_count,
            "toxic_neutralized": self.toxic_count,
            "bile_stored": len(self.bile),
            "bile_capacity": self.bile_capacity,
            "purify_threshold": self.purify_threshold,
            "toxic_threshold": self.toxic_threshold
        }
    
    def analyze_bile(self) -> dict:
        """Analyze waste patterns"""
        if not self.bile:
            return {"message": "No waste recorded"}
        
        sources = {}
        for entry in self.bile:
            src = entry.get('source', 'unknown')
            sources[src] = sources.get(src, 0) + 1
        
        return {
            "total_waste": len(self.bile),
            "sources": sources,
            "avg_toxicity": sum(e.get('toxicity', 0) for e in self.bile) / len(self.bile),
            "recent_pattern": "High noise from: " + max(sources.items(), key=lambda x: x[1])[0] if sources else "None"
        }


# Test
if __name__ == "__main__":
    print("=" * 70)
    print("  🫘 LIVER v1.0 - Ternary Filtration Test")
    print("=" * 70)
    
    liver = AOSLiverV1()
    
    test_samples = [
        BloodSample("user", "Hello, this is a clear message with information.", time.time(), 1.0),
        BloodSample("sensor", "asdfjk lasdf lkasdf lkasdfl kasdfl kasdfl kasdfl", time.time(), 5.0),
        BloodSample("log", "ERROR: Connection failed at 2026-04-05 07:40:12. Code: 503", time.time(), 2.0),
        BloodSample("spam", "!!!!!! BUY NOW !!!!!!! CLICK HERE !!!!!!!", time.time(), 15.0),
        BloodSample("chat", "The weather is nice today, temperature is 72 degrees.", time.time(), 1.5),
    ]
    
    print("\nProcessing samples...\n")
    for sample in test_samples:
        state, result, meta = liver.process(sample)
        print(f"  Source: {sample.source:10s}")
        print(f"    Input:  {sample.content[:50]}...")
        print(f"    Toxicity: {meta['original_toxicity']:.2f} | Density: {meta['original_density']:.2f}")
        print(f"    State: {state.name:8s} | Action: {meta['action']}")
        if result:
            print(f"    Output: {result[:50]}...")
        else:
            print(f"    Output: [NEUTRALIZED → BILE]")
        print()
    
    print("=" * 70)
    print("  Liver Status:")
    for k, v in liver.get_status().items():
        print(f"    {k}: {v}")
    print("=" * 70)
