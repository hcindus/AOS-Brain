#!/usr/bin/env python3
"""
AOS Brain Curriculum Feeder v4.3
Feed educational content to stimulate the brain and trigger OLLAMA mode
"""

import json
import socket
import time
import random
import sys
import os
from datetime import datetime, timedelta

# Waste-derived curriculum auto-expiry (days)
WASTE_LESSON_TTL_DAYS = 7
WASTE_QUEUE_PATH = '/var/lib/aos/brain_state/waste_queue.json'

# Curriculum items - mix of basic facts and complex reasoning
CURRICULUM = [
    {"type": "fact", "content": "The human brain contains approximately 86 billion neurons.", "importance": 0.5},
    {"type": "fact", "content": "Light travels at 299,792,458 meters per second in a vacuum.", "importance": 0.4},
    {"type": "concept", "content": "Neural networks process information through weighted connections between nodes, similar to biological synapses.", "importance": 0.8},
    {"type": "logic", "content": "If all A are B, and all B are C, then all A are C. This is syllogistic reasoning.", "importance": 0.7},
    {"type": "philosophy", "content": "The Ship of Theseus paradox questions whether an object that has had all its components replaced remains fundamentally the same object.", "importance": 0.9},
    {"type": "science", "content": "Quantum entanglement occurs when two particles remain connected such that the state of one instantly affects the other, regardless of distance.", "importance": 0.85},
    {"type": "math", "content": "Euler's identity: e^(iπ) + 1 = 0 connects five fundamental mathematical constants.", "importance": 0.75},
    {"type": "ethics", "content": "The trolley problem asks whether it's morally justified to actively cause one death to passively save five others.", "importance": 0.9},
    {"type": "systems", "content": "Emergence is when complex systems exhibit behaviors that cannot be predicted from studying individual components.", "importance": 0.8},
    {"type": "ai", "content": "Transformer architectures use self-attention mechanisms to process sequences in parallel rather than sequentially.", "importance": 0.85},
]


# ========== v1.1: FEEDBACK-TO-CURRICULUM FUNCTIONS ==========

def ingest_from_waste(waste_event: dict) -> dict:
    """
    Convert Kidneys WasteEvent into curriculum item
    
    Called by the metabolic loop - waste becomes nourishment
    """
    curriculum_item = {
        "type": "waste_lesson",
        "content": waste_event.get("suggested_lesson", "Review and improve output quality."),
        "importance": min(waste_event.get("severity", 0.5) + 0.2, 1.0),  # Boost priority
        "source": "waste_loop",
        "waste_event_id": waste_event.get("event_id", "unknown"),
        "error_category": waste_event.get("error_category", "general"),
        "kidneys_state": waste_event.get("kidneys_state", "UNKNOWN"),
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(days=WASTE_LESSON_TTL_DAYS)).isoformat(),
        "priority_boost": True,
        "reinforcement_type": "correction" if waste_event.get("kidneys_state") == "EXCRETE" else "reinforcement"
    }
    
    return curriculum_item


def load_waste_queue() -> list:
    """
    Load pending waste events from Kidneys
    
    Returns list of WasteEvents ready for curriculum conversion
    """
    if not os.path.exists(WASTE_QUEUE_PATH):
        return []
    
    try:
        with open(WASTE_QUEUE_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Could not load waste queue: {e}")
        return []


def clear_waste_queue():
    """Clear processed waste events from queue"""
    if os.path.exists(WASTE_QUEUE_PATH):
        try:
            os.remove(WASTE_QUEUE_PATH)
        except Exception as e:
            print(f"⚠️  Could not clear waste queue: {e}")


def get_waste_derived_curriculum() -> list:
    """
    Get curriculum items from Kidneys waste queue
    
    This is the metabolic loop - excretion becomes nutrition
    """
    waste_events = load_waste_queue()
    
    if not waste_events:
        return []
    
    # Convert waste events to curriculum
    lessons = [ingest_from_waste(event) for event in waste_events]
    
    print(f"🔄 Loaded {len(lessons)} waste-derived lessons from Kidneys")
    
    # Clear the queue (consumed)
    clear_waste_queue()
    
    return lessons


def is_lesson_expired(lesson: dict) -> bool:
    """Check if waste-derived lesson has expired"""
    if lesson.get("source") != "waste_loop":
        return False  # Manual lessons never expire
    
    expires_at = lesson.get("expires_at")
    if not expires_at:
        return False
    
    try:
        expiry = datetime.fromisoformat(expires_at)
        return datetime.utcnow() > expiry
    except:
        return False


def filter_expired_lessons(curriculum: list) -> list:
    """Remove expired waste-derived lessons"""
    valid = [item for item in curriculum if not is_lesson_expired(item)]
    expired_count = len(curriculum) - len(valid)
    
    if expired_count > 0:
        print(f"🗑️  Expired {expired_count} old waste-derived lessons")
    
    return valid

FEED_INTERVAL = 8  # seconds between feeds

def send_to_brain(cmd, params=None):
    """Send command to brain via socket"""
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect('/tmp/aos_brain.sock')
        
        request = {"cmd": cmd}
        if params:
            request["params"] = params
        
        sock.sendall(json.dumps(request).encode() + b'\n')
        
        response = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
        
        sock.close()
        return json.loads(response.decode())
    except Exception as e:
        return {"error": str(e)}

def feed_curriculum_item(item, index):
    """Feed a single curriculum item to the brain"""
    print(f"\n[{index+1}] Feeding: {item['type'].upper()}")
    print(f"    Content: {item['content'][:60]}...")
    print(f"    Importance: {item['importance']}")
    
    # Stimulate thyroid with importance level
    if item['importance'] >= 0.7:
        result = send_to_brain("stimulate", {"importance": item['importance']})
        if result.get('stimulated'):
            print(f"    🫁 THYROID STIMULATED → OLLAMA mode!")
        else:
            print(f"    🫁 Thyroid: staying BASELINE")
    
    # Get current status
    status = send_to_brain("status")
    thyroid = status.get('thyroid', {})
    
    print(f"    Status: {thyroid.get('state', 'unknown')} | "
          f"Ollama: {thyroid.get('ollama_level', 0):.2f} | "
          f"Tick: {status.get('tick', 0)}")

def main():
    print("=" * 70)
    print("  📚 AOS BRAIN CURRICULUM FEEDER v4.4")
    print("  Feeding knowledge to stimulate endocrine response")
    print("  ♻️  METABOLIC LOOP: Waste → Curriculum (v1.1)")
    print("=" * 70)
    
    # Check brain is alive
    ping = send_to_brain("ping")
    if ping.get('error'):
        print(f"\n❌ Brain not responding: {ping['error']}")
        sys.exit(1)
    
    # Load waste-derived curriculum (metabolic loop)
    print("\n🔄 Checking for waste-derived lessons from Kidneys...")
    waste_curriculum = get_waste_derived_curriculum()
    
    # Filter expired lessons
    all_curriculum = CURRICULUM + waste_curriculum
    all_curriculum = filter_expired_lessons(all_curriculum)
    
    print(f"\n✅ Brain connected (tick: {ping.get('tick', 0)})")
    print(f"⏱️  Feed interval: {FEED_INTERVAL}s")
    print(f"📖 Manual curriculum items: {len(CURRICULUM)}")
    print(f"♻️  Waste-derived lessons: {len(waste_curriculum)}")
    print(f"📊 Total active curriculum: {len(all_curriculum)}")
    print("\nStarting feed loop... (Ctrl+C to stop)\n")
    
    try:
        for i, item in enumerate(all_curriculum):
            feed_curriculum_item(item, i)
            time.sleep(FEED_INTERVAL)
        
        print("\n" + "=" * 70)
        print("  ✅ Curriculum feed complete!")
        print("=" * 70)
        
        # Final status
        final = send_to_brain("status")
        thyroid = final.get('thyroid', {})
        print(f"\nFinal Thyroid State:")
        print(f"  State: {thyroid.get('state', 'unknown')}")
        print(f"  Ollama hormone level: {thyroid.get('ollama_level', 0):.2f}")
        print(f"  Secretions today: {thyroid.get('secretions_today', 0)}")
        print(f"  Total ticks: {final.get('tick', 0)}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Feeder stopped by user")

if __name__ == "__main__":
    main()
