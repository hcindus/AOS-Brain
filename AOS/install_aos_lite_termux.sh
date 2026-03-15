#!/bin/bash
# AOS-Lite Installer for Termux (Android)
# WARNING: This is a lightweight version for Android devices
# Does NOT require OpenClaw - runs standalone

set -e

echo "=========================================="
echo "  AOS-Lite Installer for Termux"
echo "  WARNING: Lightweight Mode"
echo "=========================================="
echo ""

# WARNINGS
echo "⚠️  WARNINGS:"
echo "   1. This is AOS-LITE (not full AOS)"
echo "   2. Uses tiny models (≤1B parameters)"
echo "   3. SQLite instead of Redis/ChromaDB"
echo "   4. Limited functionality vs full AOS"
echo "   5. No OpenClaw integration"
echo "   6. Manual configuration required"
echo ""
read -p "Continue? (y/N): " confirm
if [[ $confirm != [yY] ]]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "📱 Installing AOS-Lite..."

# Update packages
pkg update -y
pkg upgrade -y

# Install dependencies
echo "📦 Installing dependencies..."
pkg install -y python python-pip git curl termux-api

# Install Python packages
echo "🐍 Installing Python packages..."
pip install --upgrade pip
pip install numpy requests pyyaml sqlite3

# Create AOS directory structure
echo "📁 Creating directory structure..."
mkdir -p ~/.aos-lite/{brain,config,memory,logs,vault}

# Download AOS-Lite brain
echo "🧠 Downloading AOS-Lite brain..."
cat > ~/.aos-lite/brain/brain_lite.py << 'EOF'
#!/usr/bin/env python3
"""
AOS-Lite Brain
Lightweight version for Android/Termux
No OpenClaw dependency - runs standalone
"""

import time
import json
import sqlite3
import os
from datetime import datetime

class AOSLiteBrain:
    """Lightweight AOS Brain for Android devices."""
    
    def __init__(self):
        self.tick_interval = 0.5  # 500ms (slower than full AOS)
        self.tick_count = 0
        self.running = True
        
        # Setup SQLite for memory (instead of ChromaDB)
        self.db_path = os.path.expanduser("~/.aos-lite/memory/brain.db")
        self._init_db()
        
        # Simple state (no GrowingNN in Lite)
        self.state = {
            "tick": 0,
            "phase": "idle",
            "status": "operational"
        }
        
        print("[AOS-Lite] Brain initialized")
        print("[AOS-Lite] WARNING: Running in lightweight mode")
        print("[AOS-Lite] SQLite memory active")
    
    def _init_db(self):
        """Initialize SQLite database for memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                observation TEXT,
                action TEXT,
                novelty REAL
            )
        ''')
        conn.commit()
        conn.close()
    
    def observe(self):
        """Simple observation - check system state."""
        return {
            "timestamp": time.time(),
            "system": "termux",
            "tick": self.tick_count
        }
    
    def decide(self, obs):
        """Simple decision making."""
        # In Lite mode, just log and continue
        return {
            "action": "monitor",
            "reason": "AOS-Lite monitoring mode"
        }
    
    def store(self, obs, decision):
        """Store to SQLite instead of ChromaDB."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO memories (timestamp, observation, action, novelty) VALUES (?, ?, ?, ?)",
            (time.time(), json.dumps(obs), json.dumps(decision), 0.5)
        )
        conn.commit()
        conn.close()
    
    def tick(self):
        """Single OODA cycle."""
        self.tick_count += 1
        
        # Observe
        obs = self.observe()
        
        # Decide
        decision = self.decide(obs)
        
        # Store
        self.store(obs, decision)
        
        # Update state
        self.state["tick"] = self.tick_count
        self.state["phase"] = "Act"
        
        # Log every 10 ticks
        if self.tick_count % 10 == 0:
            print(f"[AOS-Lite] Tick {self.tick_count} | Status: {self.state['status']}")
        
        return self.state
    
    def run(self):
        """Main loop."""
        print("[AOS-Lite] Starting main loop...")
        print("[AOS-Lite] Press Ctrl+C to stop")
        
        try:
            while self.running:
                self.tick()
                time.sleep(self.tick_interval)
        except KeyboardInterrupt:
            print("\n[AOS-Lite] Stopping...")
            self.shutdown()
    
    def shutdown(self):
        """Graceful shutdown."""
        print(f"[AOS-Lite] Total ticks: {self.tick_count}")
        print("[AOS-Lite] Goodbye!")

if __name__ == "__main__":
    brain = AOSLiteBrain()
    brain.run()
EOF

chmod +x ~/.aos-lite/brain/brain_lite.py

# Create config
echo "⚙️  Creating config..."
cat > ~/.aos-lite/config/brain.yaml << 'EOF'
# AOS-Lite Configuration
# WARNING: This is a lightweight version!

brain:
  id: aos-lite-v1
  version: "1.0.0-lite"
  
  warnings:
    - "No OpenClaw integration"
    - "Limited to SQLite memory"
    - "Tiny models only (≤1B)"
    - "No GrowingNN"
    - "Manual configuration required"
  
  models:
    backend: "ollama"
    ollama:
      primary: "tinyllama"  # ≤1B parameters
      fallback: "phi3:mini"
    
  memory:
    type: "sqlite"
    path: "~/.aos-lite/memory/brain.db"
    max_entries: 10000
  
  ooda:
    tick_interval_ms: 500  # Slower than full AOS (200ms)
    
  safety:
    law_zero: "Do not harm humanity"
    law_one: "Do not harm humans"
    law_two: "Obey operator"
    law_three: "Protect self"
EOF

# Create start script
echo "🚀 Creating start script..."
cat > ~/.aos-lite/start.sh << 'EOF'
#!/bin/bash
# Start AOS-Lite

echo "=========================================="
echo "  Starting AOS-Lite"
echo "  ⚠️  WARNING: Lightweight Mode"
echo "=========================================="
echo ""

# Check if running in Termux
if [ -z "$TERMUX_VERSION" ]; then
    echo "⚠️  WARNING: Not running in Termux!"
    echo "   AOS-Lite is designed for Android/Termux"
    read -p "Continue anyway? (y/N): " confirm
    if [[ $confirm != [yY] ]]; then
        exit 1
    fi
fi

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found!"
    echo "   Install with: curl -fsSL https://ollama.com/install.sh | sh"
    exit 1
fi

echo "✅ Ollama found"
echo "🧠 Starting AOS-Lite Brain..."
echo ""

python3 ~/.aos-lite/brain/brain_lite.py
EOF

chmod +x ~/.aos-lite/start.sh

# Create MOTD
cat > ~/.aos-lite/README.txt << 'EOF'
========================================
  AOS-Lite for Termux (Android)
========================================

⚠️  IMPORTANT WARNINGS:

1. This is AOS-LITE, not full AOS
   - Limited functionality
   - No OpenClaw integration
   - Standalone operation only

2. Memory System:
   - Uses SQLite (not ChromaDB)
   - Limited to 10,000 entries
   - No vector search

3. Model Requirements:
   - Tiny models only (≤1B parameters)
   - tinyllama or phi3:mini
   - Limited reasoning capability

4. Performance:
   - 500ms tick interval (vs 200ms)
   - No GrowingNN
   - No automatic scaling

5. Security:
   - Manual configuration required
   - No automatic vault setup
   - Store credentials carefully

USAGE:
  ~/.aos-lite/start.sh    - Start AOS-Lite
  ~/.aos-lite/stop.sh     - Stop AOS-Lite

CONFIG:
  ~/.aos-lite/config/brain.yaml

LOGS:
  ~/.aos-lite/logs/

For full AOS, use VPS installation.
EOF

echo ""
echo "=========================================="
echo "  ✅ AOS-Lite Installation Complete!"
echo "=========================================="
echo ""
echo "⚠️  REMEMBER: This is LITE mode!"
echo ""
echo "To start:"
echo "   ~/.aos-lite/start.sh"
echo ""
echo "To configure:"
echo "   nano ~/.aos-lite/config/brain.yaml"
echo ""
echo "For full AOS with all features:"
echo "   Use VPS installation (install_aos_vps.sh)"
echo ""
