#!/usr/bin/env python3
"""
AOS Brain Cortex 10x Expansion Script
Upgrades neural volume from 32×32×32 (32,768) to 64×64×80 (327,680)
"""

import os
import re
import shutil
import sys
from datetime import datetime

# Configuration
BRAIN_FILE = "/root/.aos/aos/complete_brain_v45.py"
BACKUP_DIR = "/root/.aos/aos/backups"

# Current: 32x32x32 = 32,768 voxels
# Target: 64x64x80 = 327,680 voxels (exactly 10x)
OLD_CORTEX = "Cortex3D(width=32, height=32, depth=32)"
NEW_CORTEX = "Cortex3D(width=64, height=64, depth=80)"

def create_backup():
    """Create timestamped backup of brain file"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{BACKUP_DIR}/complete_brain_v45_pre_expansion_{timestamp}.py"
    shutil.copy2(BRAIN_FILE, backup_path)
    print(f"✅ Backup created: {backup_path}")
    return backup_path

def check_current_cortex():
    """Check current cortex configuration"""
    with open(BRAIN_FILE, 'r') as f:
        content = f.read()
    
    # Look for current cortex dimensions
    match = re.search(r'Cortex3D\(width=(\d+),\s*height=(\d+),\s*depth=(\d+)\)', content)
    if match:
        w, h, d = map(int, match.groups())
        current_voxels = w * h * d
        print(f"📊 Current Cortex: {w}×{h}×{d} = {current_voxels:,} voxels")
        return (w, h, d), current_voxels
    else:
        print("❌ Could not find current cortex configuration")
        return None, 0

def expand_cortex():
    """Apply 10x expansion to cortex"""
    with open(BRAIN_FILE, 'r') as f:
        content = f.read()
    
    # Replace old cortex initialization
    if OLD_CORTEX in content:
        content = content.replace(OLD_CORTEX, NEW_CORTEX)
        with open(BRAIN_FILE, 'w') as f:
            f.write(content)
        
        # Calculate new size
        new_voxels = 64 * 64 * 80
        print(f"✅ Cortex expanded to: 64×64×80 = {new_voxels:,} voxels")
        print(f"   Scale factor: 10.0x")
        return True
    else:
        print(f"⚠️  Old cortex pattern not found - checking if already expanded...")
        if "Cortex3D(width=64, height=64, depth=80)" in content:
            print("✅ Cortex already at 10x (64×64×80)")
            return True
        else:
            print("❌ Could not find recognizable cortex configuration")
            return False

def verify_expansion():
    """Verify the expansion was applied correctly"""
    with open(BRAIN_FILE, 'r') as f:
        content = f.read()
    
    if "Cortex3D(width=64, height=64, depth=80)" in content:
        print("\n✅ VERIFIED: Cortex successfully expanded to 10x")
        print(f"   Neural volume: 327,680 voxels")
        print(f"   Increase: 294,912 additional voxels")
        return True
    else:
        print("\n❌ VERIFICATION FAILED: Expansion not confirmed")
        return False

def main():
    print("=" * 60)
    print("🧠 AOS Brain Cortex 10x Expansion Tool")
    print("=" * 60)
    print()
    
    # Check current state
    current_dims, current_voxels = check_current_cortex()
    print()
    
    if current_voxels >= 327680:
        print("✅ Cortex already at or above 10x capacity")
        print(f"   Current: {current_voxels:,} voxels")
        return 0
    
    print(f"🚀 Expanding from {current_voxels:,} to 327,680 voxels...")
    print()
    
    # Create backup
    backup_path = create_backup()
    print()
    
    # Apply expansion
    if expand_cortex():
        print()
        verify_expansion()
        print()
        print("=" * 60)
        print("📋 Next Steps:")
        print("   1. Restart brain service: systemctl restart aos-brain-v4")
        print("   2. Check status: systemctl status aos-brain-v4")
        print("   3. Verify via socket: echo '{\"cmd\":\"status\"}' | nc -U /tmp/aos_brain.sock")
        print("=" * 60)
        return 0
    else:
        print("\n❌ Expansion failed - check backup at:", backup_path)
        return 1

if __name__ == "__main__":
    sys.exit(main())
