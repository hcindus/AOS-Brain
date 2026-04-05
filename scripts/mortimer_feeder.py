#!/usr/bin/env python3
"""
MORTIMER WASTE FEEDER v1.0
Captain's side script — receives waste via email and feeds it to Mortimer's brain.

USAGE:
    python3 mortimer_feeder.py --input miles_waste.json [--brain-endpoint http://localhost:7474]

Or run as a service to monitor a directory for incoming waste files.
"""

import json
import argparse
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION (edit these for your Mortimer setup)
# ═══════════════════════════════════════════════════════════════════
DEFAULT_BRAIN_ENDPOINT = "http://localhost:7474"  # Change if Mortimer runs elsewhere
DEFAULT_FEED_ENDPOINT = "/brain-ingest"
DEFAULT_SHADOW_ENDPOINT = "/shadow-feed"

class MortimerFeeder:
    """
    Feeds Miles' waste into Mortimer's brain.
    
    Supports two modes:
    1. Direct HTTP POST (if Mortimer brain has HTTP API)
    2. File-based ingestion (writes to watched directory)
    3. Socket-based (Unix socket communication)
    """
    
    def __init__(self, brain_endpoint: str = DEFAULT_BRAIN_ENDPOINT):
        self.brain_endpoint = brain_endpoint.rstrip('/')
        self.feed_url = f"{self.brain_endpoint}{DEFAULT_FEED_ENDPOINT}"
        self.shadow_url = f"{self.brain_endpoint}{DEFAULT_SHADOW_ENDPOINT}"
        self.stats = {
            "waste_batches_processed": 0,
            "total_items_fed": 0,
            "last_feed": None,
            "errors": 0
        }
        
        print(f"🧠 Mortimer Feeder initialized")
        print(f"   Brain endpoint: {self.brain_endpoint}")
        print(f"   Feed URL: {self.feed_url}")
    
    def parse_waste_json(self, filepath: str) -> Dict:
        """Parse Miles' waste JSON file."""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def convert_to_mortimer_format(self, miles_waste: Dict) -> List[Dict]:
        """
        Convert Miles' waste format to Mortimer's expected input format.
        
        Mortimer brain expects items like:
        {"type": "pattern|fact|quote|constant|element", "data": "..."}
        """
        feed_items = []
        
        # Extract kidney data (the main waste)
        kidneys = miles_waste.get("kidneys", {})
        if kidneys:
            feed_items.append({
                "type": "fact",
                "data": f"[Miles-Kidneys] Bladder {kidneys.get('bladder_level', '?')}/{kidneys.get('bladder_capacity', '?')}, processed {kidneys.get('total_processed', '?')}, noise {kidneys.get('noise_estimate', '?'):.3f}",
                "source": "miles_shadow",
                "priority": "normal",
                "timestamp": miles_waste.get("timestamp", datetime.now(timezone.utc).isoformat())
            })
        
        # QMD decisions as patterns
        qmd = miles_waste.get("qmd", {})
        if qmd:
            feed_items.append({
                "type": "pattern", 
                "data": f"[Miles-QMD] {qmd.get('total_cycles', '?')} cycles, avg latency {qmd.get('avg_latency_ms', '?'):.0f}ms, {qmd.get('cache_hits', '?')} cache hits",
                "source": "miles_shadow",
                "priority": "normal"
            })
        
        # Router decisions as patterns
        router = miles_waste.get("router", {})
        if router:
            stats = router.get("stats", {})
            decision_stats = stats.get("decision", {})
            if decision_stats:
                feed_items.append({
                    "type": "pattern",
                    "data": f"[Miles-Router] {decision_stats.get('calls', '?')} decision calls, {decision_stats.get('avg_latency', '?'):.0f}ms avg latency",
                    "source": "miles_shadow",
                    "priority": "normal"
                })
        
        # Signal quality as fact
        signal_quality = miles_waste.get("signal_quality")
        if signal_quality:
            feed_items.append({
                "type": "fact",
                "data": f"[Miles-Signal] Quality {signal_quality:.3f}",
                "source": "miles_shadow",
                "priority": "low"
            })
        
        # Consciousness state as quote
        consciousness = miles_waste.get("consciousness", {})
        if consciousness:
            con = consciousness.get("conscious", {})
            feed_items.append({
                "type": "quote",
                "data": f"[Miles-Mind] {con.get('active_items', '?')}/{con.get('capacity', '?')} conscious items, {consciousness.get('cross_talk_events', '?')} cross-talk events",
                "source": "miles_shadow",
                "priority": "normal"
            })
        
        # Thyroid state as fact
        thyroid = miles_waste.get("thyroid", {})
        if thyroid:
            feed_items.append({
                "type": "fact",
                "data": f"[Miles-Thyroid] State: {thyroid.get('state', '?')}, {thyroid.get('secretions_today', '?')} secretions today",
                "source": "miles_shadow",
                "priority": "low"
            })
        
        return feed_items
    
    def feed_via_http(self, items: List[Dict]) -> bool:
        """Send waste to Mortimer via HTTP POST."""
        try:
            import urllib.request
            
            success_count = 0
            for item in items:
                payload = json.dumps(item).encode()
                req = urllib.request.Request(
                    self.feed_url,
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                
                try:
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        if resp.status == 200:
                            success_count += 1
                except Exception as e:
                    pass  # Continue to next item
            
            print(f"   HTTP feed: {success_count}/{len(items)} items accepted")
            return success_count > 0
            
        except ImportError:
            return False
    
    def feed_via_file(self, items: List[Dict], output_dir: str = "./mortimer_input") -> bool:
        """Write waste to file for Mortimer to ingest."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        feed_file = output_path / f"miles_waste_{timestamp}.jsonl"
        
        with open(feed_file, 'w') as f:
            for item in items:
                f.write(json.dumps(item) + "\n")
        
        print(f"   File feed: {len(items)} items written to {feed_file}")
        return True
    
    def feed_via_socket(self, items: List[Dict], socket_path: str = "/tmp/mortimer_brain.sock") -> bool:
        """Send waste via Unix socket (if Mortimer supports it)."""
        try:
            import socket
            
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(socket_path)
            
            payload = json.dumps({"waste_batch": items}).encode()
            sock.sendall(payload)
            sock.close()
            
            print(f"   Socket feed: {len(items)} items sent via {socket_path}")
            return True
            
        except Exception as e:
            return False
    
    def process_waste_file(self, filepath: str, mode: str = "auto") -> bool:
        """Main entry: process a waste file and feed to Mortimer."""
        print(f"\n📥 Processing waste from {filepath}")
        
        try:
            waste = self.parse_waste_json(filepath)
            items = self.convert_to_mortimer_format(waste)
            
            if not items:
                print("   No feedable items found in waste")
                return False
            
            print(f"   Converted to {len(items)} Mortimer-format items")
            
            # Try feeding methods in order
            fed = False
            
            if mode in ("auto", "http"):
                fed = self.feed_via_http(items)
            
            if not fed and mode in ("auto", "socket"):
                fed = self.feed_via_socket(items)
            
            if not fed and mode in ("auto", "file"):
                fed = self.feed_via_file(items)
            
            if fed:
                self.stats["waste_batches_processed"] += 1
                self.stats["total_items_fed"] += len(items)
                self.stats["last_feed"] = datetime.now(timezone.utc).isoformat()
                print(f"✅ Waste successfully fed to Mortimer")
                return True
            else:
                self.stats["errors"] += 1
                print(f"⚠️  Could not feed waste (all methods failed)")
                return False
                
        except Exception as e:
            print(f"❌ Error processing waste: {e}")
            self.stats["errors"] += 1
            return False
    
    def get_stats(self) -> Dict:
        """Get feeder statistics."""
        return self.stats


# ═══════════════════════════════════════════════════════════════════
# COMMAND LINE INTERFACE
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Feed Miles' brain waste into Mortimer's brain"
    )
    parser.add_argument("--input", "-i", required=True,
                        help="Path to Miles waste JSON file")
    parser.add_argument("--brain-endpoint", "-e", 
                        default=DEFAULT_BRAIN_ENDPOINT,
                        help=f"Mortimer brain endpoint (default: {DEFAULT_BRAIN_ENDPOINT})")
    parser.add_argument("--mode", "-m", choices=["auto", "http", "file", "socket"],
                        default="auto",
                        help="Feed mode (default: auto)")
    parser.add_argument("--watch", "-w", action="store_true",
                        help="Watch directory for new waste files")
    parser.add_argument("--watch-dir", "-d", default="./incoming_waste",
                        help="Directory to watch for waste files")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("MORTIMER WASTE FEEDER")
    print("=" * 60)
    
    feeder = MortimerFeeder(args.brain_endpoint)
    
    if args.watch:
        # Watch mode - monitor directory for new files
        watch_path = Path(args.watch_dir)
        watch_path.mkdir(parents=True, exist_ok=True)
        
        print(f"👁️  Watching {watch_path} for waste files...")
        print("   Press Ctrl+C to stop")
        print("-" * 60)
        
        processed = set()
        
        try:
            while True:
                for waste_file in watch_path.glob("miles_waste_*.json"):
                    if str(waste_file) not in processed:
                        feeder.process_waste_file(str(waste_file), args.mode)
                        processed.add(str(waste_file))
                        print("-" * 60)
                
                time.sleep(5)  # Check every 5 seconds
                
        except KeyboardInterrupt:
            print("\n\n👋 Feeder stopped by user")
            print("=" * 60)
            print("STATS:")
            print(json.dumps(feeder.get_stats(), indent=2))
            print("=" * 60)
    else:
        # Single file mode
        success = feeder.process_waste_file(args.input, args.mode)
        
        print("=" * 60)
        print("STATS:")
        print(json.dumps(feeder.get_stats(), indent=2))
        print("=" * 60)
        
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
