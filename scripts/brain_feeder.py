#!/usr/bin/env python3
"""
AOS Brain Feeder v1.0
Feed waste JSON files from AOS Kidneys into your own brain system.

Usage:
    python3 brain_feeder.py --source /path/to/waste/files --target brain_module
    python3 brain_feeder.py --watch /path/to/waste --callback my_brain.process

Waste File Format (from Kidneys):
{
    "timestamp": 1234567890.0,
    "waste_items": [
        {
            "content": "filtered text",
            "source": "log/sensor/user",
            "signal_score": 0.3,
            "pattern_hash": "abc123",
            "recycle_count": 0
        }
    ],
    "metadata": {
        "state": "FILTER|REABSORB|EXCRETE",
        "total_processed": 1000,
        "signal_avg": 0.45
    }
}
"""

import os
import sys
import json
import time
import glob
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Callable, Optional
from datetime import datetime


@dataclass
class WasteItem:
    """A single waste item ready for reprocessing"""
    content: str
    source: str
    timestamp: float
    signal_score: float
    pattern_hash: str
    recycle_count: int
    
    @classmethod
    def from_dict(cls, data: dict) -> 'WasteItem':
        return cls(
            content=data.get('content', ''),
            source=data.get('source', 'unknown'),
            timestamp=data.get('timestamp', 0.0),
            signal_score=data.get('signal_score', 0.0),
            pattern_hash=data.get('pattern_hash', ''),
            recycle_count=data.get('recycle_count', 0)
        )
    
    def to_dict(self) -> dict:
        return {
            'content': self.content,
            'source': self.source,
            'timestamp': self.timestamp,
            'signal_score': self.signal_score,
            'pattern_hash': self.pattern_hash,
            'recycle_count': self.recycle_count
        }


class BrainFeeder:
    """
    Feed waste from AOS Kidneys into your own brain.
    
    This is YOUR brain - customize it however you want.
    The Kidneys just send you filtered/structured noise.
    You decide what's valuable.
    """
    
    def __init__(self, 
                 waste_dir: str = "/tmp/aos_waste",
                 your_brain_callback: Optional[Callable] = None,
                 min_signal_threshold: float = 0.2):
        
        self.waste_dir = Path(waste_dir)
        self.your_brain_callback = your_brain_callback
        self.min_signal_threshold = min_signal_threshold
        
        # Track what we've already fed
        self.processed_hashes = set()
        self.feed_count = 0
        self.total_items = 0
        
        # Your brain's pattern storage (customize this)
        self.your_patterns = []
        self.your_insights = []
        
        print(f"[Brain Feeder v1.0] Initialized")
        print(f"  Waste source: {self.waste_dir}")
        print(f"  Signal threshold: {min_signal_threshold}")
        print(f"  Ready to feed YOUR brain")
        
    def discover_waste_files(self) -> List[Path]:
        """Find all waste JSON files from Kidneys"""
        pattern = self.waste_dir / "**" / "*.json"
        return sorted(Path().glob(str(pattern)), key=lambda p: p.stat().st_mtime)
    
    def load_waste_file(self, filepath: Path) -> Optional[dict]:
        """Load and parse a waste file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[Error] Failed to load {filepath}: {e}")
            return None
    
    def extract_signal(self, item: WasteItem) -> Optional[dict]:
        """
        Extract signal from waste item.
        This is YOUR logic - customize as needed.
        
        Returns: signal packet for your brain, or None if noise
        """
        # Skip if already processed this hash
        if item.pattern_hash in self.processed_hashes:
            return None
        self.processed_hashes.add(item.pattern_hash)
        
        # Skip if below your threshold
        if item.signal_score < self.min_signal_threshold:
            return None
        
        # Build signal packet
        signal = {
            'content': item.content,
            'source': item.source,
            'original_score': item.signal_score,
            'recycled': item.recycle_count,
            'fed_at': time.time(),
            'value': self._calculate_value(item)
        }
        
        return signal
    
    def _calculate_value(self, item: WasteItem) -> float:
        """
        Calculate value for YOUR brain.
        Override this with your own logic.
        """
        value = item.signal_score
        
        # Boost for certain sources
        source_boosts = {
            'alert': 0.3,
            'error': 0.25,
            'user': 0.2,
            'sensor': 0.15
        }
        value += source_boosts.get(item.source, 0)
        
        # Discount for recycled content (already chewed)
        value -= (item.recycle_count * 0.1)
        
        return max(0.0, min(1.0, value))
    
    def feed_brain(self, signal: dict):
        """
        Feed signal to YOUR brain.
        This is where you integrate with your own system.
        """
        self.feed_count += 1
        
        # Option 1: Store in your patterns
        self.your_patterns.append(signal)
        
        # Option 2: Extract insights
        insight = self._extract_insight(signal)
        if insight:
            self.your_insights.append(insight)
        
        # Option 3: Call your custom callback
        if self.your_brain_callback:
            try:
                self.your_brain_callback(signal)
            except Exception as e:
                print(f"[Error] Callback failed: {e}")
        
        print(f"  [Fed] {signal['source']:8s} | Value: {signal['value']:.2f} | "
              f"{signal['content'][:50]}...")
    
    def _extract_insight(self, signal: dict) -> Optional[dict]:
        """
        Extract an insight from signal.
        Override this with your own pattern detection.
        """
        content = signal['content'].lower()
        
        # Example: Detect error patterns
        if 'error' in content or 'failed' in content or 'exception' in content:
            return {
                'type': 'error_pattern',
                'content': signal['content'],
                'severity': 'high' if signal['value'] > 0.7 else 'medium',
                'detected_at': time.time()
            }
        
        # Example: Detect completion patterns
        if 'complete' in content or 'success' in content or 'done' in content:
            return {
                'type': 'completion',
                'content': signal['content'],
                'value': signal['value'],
                'detected_at': time.time()
            }
        
        return None
    
    def process_batch(self, max_files: int = 100):
        """Process a batch of waste files"""
        files = self.discover_waste_files()[:max_files]
        
        fed_count = 0
        for filepath in files:
            data = self.load_waste_file(filepath)
            if not data:
                continue
            
            items = data.get('waste_items', [])
            for item_data in items:
                item = WasteItem.from_dict(item_data)
                signal = self.extract_signal(item)
                if signal:
                    self.feed_brain(signal)
                    fed_count += 1
                self.total_items += 1
        
        return fed_count
    
    def watch_and_feed(self, interval: float = 5.0):
        """Continuously watch for new waste and feed your brain"""
        print(f"[Watcher] Starting... Ctrl+C to stop")
        print(f"[Watcher] Watching: {self.waste_dir}")
        print(f"[Watcher] Interval: {interval}s")
        print("-" * 60)
        
        try:
            while True:
                fed = self.process_batch()
                if fed > 0:
                    print(f"\n[Batch] Fed {fed} signals to your brain "
                          f"(Total: {self.feed_count}/{self.total_items})")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n[Watcher] Stopping...")
            self.print_summary()
    
    def print_summary(self):
        """Print feeding summary"""
        print("\n" + "=" * 60)
        print("  BRAIN FEEDER SUMMARY")
        print("=" * 60)
        print(f"  Total items scanned: {self.total_items}")
        print(f"  Signals fed: {self.feed_count}")
        print(f"  Unique patterns: {len(self.processed_hashes)}")
        print(f"  Your patterns stored: {len(self.your_patterns)}")
        print(f"  Insights extracted: {len(self.your_insights)}")
        if self.your_insights:
            print("\n  Recent insights:")
            for insight in self.your_insights[-5:]:
                print(f"    - [{insight['type']}] {insight['content'][:40]}...")
        print("=" * 60)


# ============== EXAMPLE: YOUR BRAIN IMPLEMENTATION ==============

class YourBrain:
    """
    Example brain implementation.
    Replace this with YOUR actual brain system.
    """
    
    def __init__(self):
        self.knowledge = []
        self.patterns = {}
        print("[YourBrain] Initialized - ready to receive signals")
    
    def process_signal(self, signal: dict):
        """Process an incoming signal"""
        print(f"[YourBrain] Processing: {signal['content'][:40]}...")
        
        # Store knowledge
        self.knowledge.append(signal)
        
        # Learn patterns
        source = signal['source']
        if source not in self.patterns:
            self.patterns[source] = []
        self.patterns[source].append(signal)
        
        # React to high-value signals
        if signal['value'] > 0.8:
            print(f"[YourBrain] ⚠️ HIGH VALUE ALERT: {signal['content'][:50]}")
    
    def get_stats(self):
        return {
            'knowledge_count': len(self.knowledge),
            'pattern_sources': len(self.patterns),
            'total_patterns': sum(len(p) for p in self.patterns.values())
        }


# ============== MAIN ENTRY ==============

def main():
    parser = argparse.ArgumentParser(
        description='Feed AOS Kidney waste into your own brain'
    )
    parser.add_argument('--source', '-s', 
                       default='/tmp/aos_waste',
                       help='Directory containing waste JSON files')
    parser.add_argument('--watch', '-w',
                       action='store_true',
                       help='Watch continuously for new waste')
    parser.add_argument('--interval', '-i',
                       type=float, default=5.0,
                       help='Watch interval in seconds (default: 5)')
    parser.add_argument('--threshold', '-t',
                       type=float, default=0.2,
                       help='Minimum signal score to feed (default: 0.2)')
    parser.add_argument('--example', '-e',
                       action='store_true',
                       help='Run with example brain implementation')
    
    args = parser.parse_args()
    
    # Create example brain if requested
    if args.example:
        print("Running with EXAMPLE brain implementation")
        print("Replace 'your_brain' with your actual brain module\n")
        your_brain = YourBrain()
        callback = your_brain.process_signal
    else:
        callback = None
    
    # Create feeder
    feeder = BrainFeeder(
        waste_dir=args.source,
        your_brain_callback=callback,
        min_signal_threshold=args.threshold
    )
    
    if args.watch:
        feeder.watch_and_feed(args.interval)
    else:
        print("Processing batch...")
        fed = feeder.process_batch()
        print(f"\nFed {fed} signals to your brain")
        feeder.print_summary()


if __name__ == "__main__":
    main()
