#!/usr/bin/env python3
"""
AOS COMPLETE MULTI-SENSE ORCHESTRATOR v2.0
Coordinates: Vision + Audio + Market + Cross-Modal + Sensory Memory
"""

import sys
import time
import threading
from pathlib import Path

sys.path.insert(0, '/root/.aos/aos')

from camera_vision_daemon import CameraVisionDaemon
from audio_sense import AudioSense
from market_sense import MarketSense
from cross_modal_triggers import CrossModalIntegrator, SensoryEvent
from sensory_memory import SensoryMemory
from gutenberg_feeder import GutenbergFeeder

class CompleteMultisenseOrchestrator:
    """
    Full sensory orchestration with cross-modal integration
    """
    
    def __init__(self):
        print("="*70)
        print("  AOS COMPLETE MULTI-SENSE ORCHESTRATOR v2.0")
        print("="*70)
        print()
        
        # Initialize all senses
        self.vision = CameraVisionDaemon(capture_interval=2.0)
        self.audio = AudioSense()
        self.market = MarketSense()
        self.cross_modal = CrossModalIntegrator()
        self.memory = SensoryMemory()
        self.gutenberg = GutenbergFeeder()
        
        # Threads
        self.threads = []
        self.running = False
        
        print("All senses initialized")
        print()
    
    def start_vision(self):
        """Start vision with memory integration"""
        print("[1] Starting Vision...")
        
        # Patch vision to store patterns
        original_capture = self.vision._capture_and_feed
        
        def vision_with_memory():
            original_capture()
            # Store in memory if important
            if self.vision.stats['captures'] % 5 == 0:
                # Create dummy features for demo
                features = {
                    'edge_complexity': 0.5 + 0.3 * (self.vision.tick_count % 3),
                    'triggered_actions': []
                }
                self.memory.store_pattern('vision', features, [])
        
        self.vision._capture_and_feed = vision_with_memory
        self.vision.start()
        
        # Cross-modal hook
        def vision_event_hook():
            while self.running:
                if self.vision.stats['captures'] % 10 == 0:
                    event = SensoryEvent(
                        'vision', 'motion', 0.6, {}, time.time()
                    )
                    self.cross_modal.receive_event(event)
                time.sleep(2)
        
        t = threading.Thread(target=vision_event_hook, daemon=True)
        t.start()
        self.threads.append(t)
        
        print("    ✓ Vision active")
    
    def start_audio(self):
        """Start audio sense"""
        print("[2] Starting Audio...")
        
        def audio_with_events():
            tick = 0
            while self.running:
                self.audio.capture()
                
                # Fire cross-modal event periodically
                if tick % 20 == 0:
                    event = SensoryEvent(
                        'audio', 'loud', 0.7, {}, time.time()
                    )
                    self.cross_modal.receive_event(event)
                
                tick += 1
                time.sleep(0.5)
        
        t = threading.Thread(target=audio_with_events, daemon=True)
        t.start()
        self.threads.append(t)
        
        print("    ✓ Audio active")
    
    def start_market(self):
        """Start market sense"""
        print("[3] Starting Market Sense...")
        
        def market_with_events():
            tick = 0
            while self.running:
                self.market.capture()
                
                # Fire events on volatility
                if tick % 15 == 0:
                    event = SensoryEvent(
                        'market', 'volatile', 0.8, {}, time.time()
                    )
                    self.cross_modal.receive_event(event)
                
                tick += 1
                time.sleep(2.0)
        
        t = threading.Thread(target=market_with_events, daemon=True)
        t.start()
        self.threads.append(t)
        
        print("    ✓ Market active")
    
    def start_cross_modal(self):
        """Start cross-modal monitor"""
        print("[4] Starting Cross-Modal Integration...")
        
        def monitor_loop():
            while self.running:
                self.cross_modal._detect_synchrony()
                time.sleep(1.0)
        
        t = threading.Thread(target=monitor_loop, daemon=True)
        t.start()
        self.threads.append(t)
        
        print("    ✓ Cross-modal active")
    
    def start_gutenberg(self):
        """Start literature feed"""
        print("[5] Starting Gutenberg Literature...")
        
        def gutenberg_loop():
            # Feed one book every 60 seconds
            books = ['pride_prejudice', 'alice_wonderland']
            idx = 0
            
            while self.running:
                try:
                    book = books[idx % len(books)]
                    self.gutenberg.feed_book(book, chunks=3)
                    idx += 1
                except:
                    pass
                time.sleep(60)
        
        t = threading.Thread(target=gutenberg_loop, daemon=True)
        t.start()
        self.threads.append(t)
        
        print("    ✓ Literature active")
    
    def start_all(self):
        """Start complete sensory system"""
        self.running = True
        
        # Replay previous sensory memories
        print("[0] Loading sensory memories...")
        self.memory.replay_memory(count=min(5, len(self.memory.patterns)))
        print()
        
        # Start all senses
        self.start_vision()
        self.start_audio()
        self.start_market()
        self.start_cross_modal()
        self.start_gutenberg()
        
        print()
        print("="*70)
        print("  ALL SYSTEMS ACTIVE")
        print("="*70)
        print()
        print("  Running:")
        print("    • Vision (camera/simulated) - 2s interval")
        print("    • Audio (5-band spectrum) - 0.5s interval")
        print("    • Market (BTC/ETH/SOL/XRP/DOGE) - 2s interval")
        print("    • Cross-Modal (5 trigger mappings)")
        print("    • Sensory Memory (persistent storage)")
        print("    • Literature (Gutenberg classics)")
        print()
        print("  Cross-Modal Mappings:")
        print("    • audio_loud → vision:bright_flash")
        print("    • vision_bright → audio:high_tone")
        print("    • market_volatile → vision:red_pulsing")
        print("    • market_breakout → vision:green_flash")
        print("    • vision_motion → audio:spatial_sound")
        print()
        print("  Press Ctrl+C to stop")
        print("="*70)
        print()
    
    def stop_all(self):
        """Stop all systems"""
        print("\n[Shutting down...]")
        self.running = False
        
        # Save memory
        print("  Saving sensory memories...")
        self.memory._save_memory()
        
        # Stop vision
        if hasattr(self.vision, 'stop'):
            self.vision.stop()
        
        print("\nAll systems offline.")
        print(f"  Vision captures: {self.vision.stats.get('captures', 0)}")
        print(f"  Audio captures: {self.audio.stats.get('captures', 0)}")
        print(f"  Market feeds: {self.market.stats.get('feeds', 0)}")
        print(f"  Cross-modal activations: {self.cross_modal.cross_activations}")
        print(f"  Memory patterns: {len(self.memory.patterns)}")
    
    def run(self):
        """Main run loop"""
        self.start_all()
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_all()

def main():
    orchestrator = CompleteMultisenseOrchestrator()
    orchestrator.run()

if __name__ == "__main__":
    main()
