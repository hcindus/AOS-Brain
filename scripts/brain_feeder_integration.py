#!/usr/bin/env python3
"""
AOS Kidneys + Your Brain Integration
Example showing how to wire Kidneys waste output to your brain.
"""

import sys
import json
import time
from pathlib import Path

# Add AOS to path
sys.path.insert(0, '/root/.aos/aos')

from kidneys_v1 import AOSKidneysV1, KidneyState


# ============== YOUR BRAIN ==============
class YourBrain:
    """
    YOUR custom brain implementation.
    This is where you build your own intelligence.
    """
    
    def __init__(self):
        self.memories = []
        self.learned_patterns = {}
        self.decisions = []
        
    def ingest(self, packet: dict):
        """Ingest a signal packet from Kidneys"""
        
        # Store memory
        self.memories.append(packet)
        
        # Extract patterns
        content = packet.get('content', '')
        source = packet.get('source', 'unknown')
        
        # Your pattern learning logic here
        if source not in self.learned_patterns:
            self.learned_patterns[source] = []
        self.learned_patterns[source].append(content)
        
        # Make decisions based on signal
        self._decide(packet)
        
    def _decide(self, packet: dict):
        """Your decision logic"""
        content = packet.get('content', '').lower()
        
        # Example: React to alerts
        if 'alert' in content or 'error' in content:
            decision = {
                'action': 'alert_handler',
                'priority': 'high',
                'timestamp': time.time()
            }
            self.decisions.append(decision)
            print(f"  [Decision] HIGH PRIORITY ALERT: {content[:40]}...")
    
    def get_stats(self) -> dict:
        return {
            'memories': len(self.memories),
            'patterns': len(self.learned_patterns),
            'decisions': len(self.decisions)
        }


# ============== WASTE EXPORTER ==============
class KidneyWasteExporter:
    """
    Exports Kidney waste to JSON files for your brain feeder.
    Run this alongside the main brain to export waste streams.
    """
    
    def __init__(self, kidneys: AOSKidneysV1, export_dir: str = "/tmp/aos_waste"):
        self.kidneys = kidneys
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)
        self.export_count = 0
        
    def export_waste(self):
        """Export current bladder contents to JSON"""
        if not self.kidneys.bladder:
            return None
        
        # Build waste document
        waste_items = []
        for item in self.kidneys.bladder:
            waste_items.append({
                'content': item.content,
                'source': item.source,
                'timestamp': item.timestamp,
                'signal_score': item.signal_score,
                'pattern_hash': item.pattern_hash,
                'recycle_count': item.recycle_count
            })
        
        waste_doc = {
            'timestamp': time.time(),
            'waste_items': waste_items,
            'metadata': {
                'state': self.kidneys.state.name,
                'total_processed': self.kidneys.total_processed,
                'signal_avg': sum(self.kidneys.signal_history[-20:]) / 20 
                              if self.kidneys.signal_history else 0
            }
        }
        
        # Write to file
        filename = f"waste_{int(time.time())}_{self.export_count:04d}.json"
        filepath = self.export_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(waste_doc, f, indent=2)
        
        self.export_count += 1
        return filepath


# ============== INTEGRATION EXAMPLE ==============

def demo_integration():
    """Demo: Kidneys filtering → Your Brain feeding"""
    
    print("=" * 60)
    print("  AOS Kidneys → Your Brain Integration Demo")
    print("=" * 60)
    
    # Initialize systems
    print("\n[1] Initializing Kidneys...")
    kidneys = AOSKidneysV1(signal_threshold=0.6)  # Higher threshold = more waste
    
    print("\n[2] Initializing Your Brain...")
    your_brain = YourBrain()
    
    print("\n[3] Initializing Waste Exporter...")
    exporter = KidneyWasteExporter(kidneys, export_dir="/tmp/aos_waste_demo")
    
    # Simulate input stream
    print("\n[4] Processing input stream...")
    test_inputs = [
        ("ERROR: Database connection failed at 07:42:15", "log", {"is_alert": True}),
        ("asdfasdf jkl;jkl; random gibberish content here", "garbage", {}),
        ("System temperature: 45°C, CPU: 12%", "sensor", {}),
        ("The quick brown fox jumps over the lazy dog", "text", {}),
        ("!!!!!!!!! ALERT !!!!!!!!!!", "alert", {"is_alert": True}),
        ("User input: Start the backup process", "user", {"is_user_input": True}),
        ("lorem ipsum dolor sit amet consectetur", "filler", {}),
        ("Backup completed successfully at 2026-04-05 07:42:30", "log", {}),
    ]
    
    for content, source, context in test_inputs:
        # Kidneys process
        state, result, meta = kidneys.process(content, source, context)
        
        # If signal passed through, feed directly to brain
        if result:
            packet = {
                'content': result,
                'source': source,
                'signal_score': meta['signal_score'],
                'timestamp': time.time()
            }
            your_brain.ingest(packet)
            print(f"  [Direct] {source:8s} | Score: {meta['signal_score']:.2f}")
        else:
            print(f"  [Waste]  {source:8s} | Score: {meta['signal_score']:.2f} → bladder")
    
    # Export waste
    print("\n[5] Exporting waste to JSON...")
    waste_file = exporter.export_waste()
    if waste_file:
        print(f"  Exported: {waste_file}")
    
    # Now your brain feeder can pick up this waste
    print("\n[6] Your Brain Feeder would now:")
    print("   - Read waste JSON files from /tmp/aos_waste_demo")
    print("   - Extract signals above threshold (0.2)")
    print("   - Feed them to your brain via callback")
    
    # Show stats
    print("\n[7] Stats:")
    print(f"   Kidneys processed: {kidneys.total_processed}")
    print(f"   Kidneys bladder: {len(kidneys.bladder)} items")
    print(f"   Your brain memories: {your_brain.get_stats()['memories']}")
    print(f"   Your brain decisions: {your_brain.get_stats()['decisions']}")
    
    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("  Run: python3 brain_feeder.py --example --watch")
    print("=" * 60)


if __name__ == "__main__":
    demo_integration()
