#!/usr/bin/env python3
"""
Mortimer Waste Auto-Feeder
Transfers noise/waste data from Miles' sespool to Mortimer's brain input queue
"""

import json
import os
import sys
import subprocess
import time
import random
from datetime import datetime, timezone
from pathlib import Path

# Configuration
SESPOOL_DIR = Path("/root/.openclaw/workspace/memory/sespool")
MANIFEST_FILE = SESPOOL_DIR / "sespool-manifest.json"
LOG_FILE = SESPOOL_DIR / "feeder.log"

# Mortimer VPS configuration (to be filled)
MORTIMER_HOST = os.getenv("MORTIMER_HOST", "mortimer-vps.example.com")
MORTIMER_USER = os.getenv("MORTIMER_USER", "openclaw")
MORTIMER_BRAIN_PATH = os.getenv("MORTIMER_BRAIN_PATH", "/home/openclaw/.aos/brain/waste-input/")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "50"))  # Items per feed
FEED_INTERVAL_MIN = int(os.getenv("FEED_INTERVAL_MIN", "3"))  # Minutes between feeds
FEED_INTERVAL_MAX = int(os.getenv("FEED_INTERVAL_MAX", "7"))  # Randomize to prevent lockstep

def log(message):
    timestamp = datetime.now(timezone.utc).isoformat()
    entry = f"[{timestamp}] {message}"
    print(entry)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def load_manifest():
    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE) as f:
            return json.load(f)
    return {"batches": [], "total_waste_items": 0}

def save_manifest(manifest):
    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, indent=2)

def collect_waste():
    """Collect waste files from all sespool directories"""
    waste_dirs = [
        SESPOOL_DIR / "periodic-waste",
        SESPOOL_DIR / "urban-waste", 
        SESPOOL_DIR / "webster-waste",
        SESPOOL_DIR / "thesaurus-waste"
    ]
    
    waste_items = []
    for waste_dir in waste_dirs:
        if waste_dir.exists():
            for waste_file in waste_dir.glob("*.json"):
                if "transferred" not in waste_file.name:
                    try:
                        with open(waste_file) as f:
                            data = json.load(f)
                            waste_items.append({
                                "file": str(waste_file),
                                "data": data,
                                "source": waste_dir.name
                            })
                    except Exception as e:
                        log(f"Error loading {waste_file}: {e}")
    
    return waste_items

def package_batch(waste_items):
    """Package waste items into a batch for Mortimer"""
    batch_id = f"batch_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{random.randint(1000,9999)}"
    batch = {
        "batch_id": batch_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "miles-sespool",
        "item_count": len(waste_items),
        "waste_type_distribution": {},
        "items": waste_items
    }
    
    # Count waste types
    for item in waste_items:
        wt = item.get("source", "unknown")
        batch["waste_type_distribution"][wt] = batch["waste_type_distribution"].get(wt, 0) + 1
    
    return batch

def transfer_to_mortimer(batch):
    """Transfer batch to Mortimer's VPS"""
    batch_file = SESPOOL_DIR / f"{batch['batch_id']}.json"
    
    # Save batch locally first
    with open(batch_file, "w") as f:
        json.dump(batch, f, indent=2)
    
    # Transfer via scp
    remote_path = f"{MORTIMER_USER}@{MORTIMER_HOST}:{MORTIMER_BRAIN_PATH}"
    
    try:
        result = subprocess.run(
            ["scp", str(batch_file), remote_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            log(f"✅ Transferred {batch['batch_id']} ({batch['item_count']} items) to Mortimer")
            
            # Mark original waste files as transferred
            for item in batch["items"]:
                original = Path(item["file"])
                if original.exists():
                    transferred_name = original.parent / f"{original.stem}.transferred.json"
                    original.rename(transferred_name)
            
            # Archive batch
            archive_dir = SESPOOL_DIR / "archive"
            archive_dir.mkdir(exist_ok=True)
            batch_file.rename(archive_dir / batch_file.name)
            
            return True
        else:
            log(f"❌ Transfer failed: {result.stderr}")
            return False
            
    except Exception as e:
        log(f"❌ Transfer error: {e}")
        return False

def simulate_transfer(batch):
    """Simulate transfer for testing (when Mortimer VPS not available)"""
    log(f"🔵 SIMULATED: Would transfer {batch['batch_id']} ({batch['item_count']} items) to Mortimer")
    log(f"   Waste types: {batch['waste_type_distribution']}")
    
    # Save to pending queue
    pending_dir = SESPOOL_DIR / "pending"
    pending_dir.mkdir(exist_ok=True)
    batch_file = pending_dir / f"{batch['batch_id']}.json"
    
    with open(batch_file, "w") as f:
        json.dump(batch, f, indent=2)
    
    # Mark originals
    for item in batch["items"]:
        original = Path(item["file"])
        if original.exists():
            transferred_name = original.parent / f"{original.stem}.transferred.json"
            original.rename(transferred_name)
    
    return True

def feed_cycle():
    """One feeding cycle"""
    waste_items = collect_waste()
    
    if len(waste_items) == 0:
        log("No waste available for feeding")
        return False
    
    # Take batch_size items
    batch_items = waste_items[:BATCH_SIZE]
    batch = package_batch(batch_items)
    
    # Update manifest
    manifest = load_manifest()
    manifest["batches"].append({
        "batch_id": batch["batch_id"],
        "timestamp": batch["timestamp"],
        "item_count": batch["item_count"],
        "status": "transferring"
    })
    manifest["total_waste_items"] += batch["item_count"]
    save_manifest(manifest)
    
    # Attempt transfer (or simulation)
    if os.getenv("SIMULATE_TRANSFER", "true").lower() == "true":
        success = simulate_transfer(batch)
    else:
        success = transfer_to_mortimer(batch)
    
    if success:
        manifest = load_manifest()
        for b in manifest["batches"]:
            if b["batch_id"] == batch["batch_id"]:
                b["status"] = "transferred"
        save_manifest(manifest)
    
    return success

def main():
    log("=" * 50)
    log("Mortimer Waste Auto-Feeder Starting")
    log(f"Sespool dir: {SESPOOL_DIR}")
    log(f"Target: {MORTIMER_USER}@{MORTIMER_HOST}:{MORTIMER_BRAIN_PATH}")
    log(f"Batch size: {BATCH_SIZE}")
    log(f"Feed interval: {FEED_INTERVAL_MIN}-{FEED_INTERVAL_MAX} minutes")
    log("=" * 50)
    
    while True:
        try:
            fed = feed_cycle()
            
            # Calculate next feed time (with jitter)
            interval = random.randint(FEED_INTERVAL_MIN, FEED_INTERVAL_MAX)
            next_feed = datetime.now(timezone.utc + timedelta(minutes=interval))
            
            if fed:
                log(f"Next feed in {interval} minutes (at {next_feed.strftime('%H:%M')})")
            else:
                log(f"Waiting {interval} minutes for more waste...")
            
            time.sleep(interval * 60)
            
        except KeyboardInterrupt:
            log("Feeder stopped by user")
            break
        except Exception as e:
            log(f"Error in feed cycle: {e}")
            time.sleep(60)  # Wait a minute before retry

if __name__ == "__main__":
    from datetime import timedelta  # Import here to avoid NameError
    main()
