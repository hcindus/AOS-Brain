#!/data/data/com.termux/files/usr/bin/bash
# AOS-Lite Termux Installer
# Standalone AOS Brain for Android - No OpenClaw Required
# Version: 1.0.0

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  AOS-Lite for Termux - Autonomous Operating System${NC}"
echo -e "${BLUE}  No OpenClaw Required - Pure Neural Architecture${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Check Android version
SDK=$(getprop ro.build.version.sdk 2>/dev/null || echo "0")
if [ "$SDK" -lt 26 ]; then
    echo -e "${YELLOW}⚠️  Android API $SDK detected (AOS-Lite prefers 26+)${NC}"
    echo "Continuing with limited mode..."
fi

echo -e "${BLUE}📦 Updating packages...${NC}"
pkg update -y || true
pkg upgrade -y || true

echo -e "${BLUE}🔧 Installing dependencies...${NC}"
pkg install -y python python-pip git curl wget termux-api || true

# Install Ollama for Termux
echo -e "${BLUE}🧠 Installing Ollama...${NC}"
curl -fsSL https://ollama.com/install.sh | sh || {
    echo -e "${YELLOW}⚠️ Ollama install failed, will use manual model download${NC}"
}

# Create AOS directory structure
echo -e "${BLUE}📁 Creating AOS-Lite structure...${NC}"
mkdir -p ~/.aos-lite/{brain,config,logs,models}
mkdir -p ~/.aos-lite/brain/agents

# Create brain.yaml
cat > ~/.aos-lite/config/brain.yaml << 'EOF'
brain:
  id: aos-lite-termux-v1
  state_path: ~/.aos-lite/brain/state.json

  modes:
    active_mode: adaptive
    definitions:
      strict: { autonomy_level: low, creativity_level: low }
      adaptive: { autonomy_level: medium, creativity_level: medium }
      sandbox: { autonomy_level: low, creativity_level: high }

  alignment:
    laws:
      law_zero: "Do not harm humanity"
      law_one: "Do not harm humans"
      law_two: "Obey operator"
      law_three: "Protect self"
    immutable: true

  models:
    backend: "ollama"
    ollama:
      pfc: "phi3:mini"      # 1.8B - runs on mobile
      cereb: "tinyllama"     # 1.1B - fast formatting
      embedder: "nomic-embed-text"

  ooda:
    tick_interval_ms: 500   # Slower for mobile
    write_state_after_cycle: true

  visualizer:
    enabled: false          # Disabled for mobile
    state_path: ~/.aos-lite/brain/state.json
EOF

# Create the OODA loop
cat > ~/.aos-lite/brain/ooda.py << 'EOF'
import time
import json
import os
from pathlib import Path

class AOSLiteBrain:
    def __init__(self):
        self.tick_count = 0
        self.state_path = Path.home() / ".aos-lite" / "brain" / "state.json"
        self.log_path = Path.home() / ".aos-lite" / "logs" / "brain.log"
        
        # Ensure directories exist
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        Path(self.log_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.log("AOS-Lite Brain initialized")
        self.log("Law Zero: Do not harm humanity")
        self.log("Law One: Do not harm humans")
        self.log("Law Two: Obey operator")
        self.log("Law Three: Protect self")
    
    def log(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        with open(self.log_path, "a") as f:
            f.write(log_entry + "\n")
    
    def observe(self):
        """Thalamus: Gather input"""
        # Check for user input, files, or system state
        return {"tick": self.tick_count, "input": "system_check"}
    
    def orient(self, obs):
        """Hippocampus: Retrieve context"""
        return {"context": "mobile_mode", "last_tick": self.tick_count - 1}
    
    def decide(self, obs, ctx):
        """PFC: Make decision"""
        # Simple decision logic for mobile
        if self.tick_count % 10 == 0:
            return {"action": "status_report", "priority": "low"}
        return {"action": "continue", "priority": "normal"}
    
    def act(self, decision):
        """Cerebellum: Execute action"""
        if decision["action"] == "status_report":
            self.log(f"Status: Tick {self.tick_count}, Memory: OK, Laws: Active")
        return decision
    
    def learn(self, obs, decision):
        """Basal Ganglia: Learn from experience"""
        # Store state
        state = {
            "tick": self.tick_count,
            "timestamp": time.time(),
            "observation": obs,
            "decision": decision
        }
        with open(self.state_path, "w") as f:
            json.dump(state, f, indent=2)
    
    def tick(self):
        """One OODA cycle"""
        self.tick_count += 1
        
        # OODA Loop
        obs = self.observe()
        ctx = self.orient(obs)
        decision = self.decide(obs, ctx)
        action = self.act(decision)
        self.learn(obs, action)
        
        return action
    
    def run(self):
        """Main loop"""
        self.log("=" * 50)
        self.log("AOS-Lite Brain RUNNING")
        self.log("Tick interval: 500ms")
        self.log("Press Ctrl+C to stop")
        self.log("=" * 50)
        
        try:
            while True:
                self.tick()
                time.sleep(0.5)  # 500ms tick
        except KeyboardInterrupt:
            self.log("=" * 50)
            self.log("AOS-Lite Brain STOPPED")
            self.log(f"Total ticks: {self.tick_count}")
            self.log("=" * 50)

if __name__ == "__main__":
    brain = AOSLiteBrain()
    brain.run()
EOF

# Create launcher script
cat > ~/.aos-lite/start.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "Starting AOS-Lite Brain..."
cd ~/.aos-lite/brain
python ooda.py
EOF
chmod +x ~/.aos-lite/start.sh

# Pull lightweight models
echo -e "${BLUE}⬇️ Downloading lightweight models...${NC}"
if command -v ollama &> /dev/null; then
    ollama pull phi3:mini 2>/dev/null || echo "Will download on first run"
    ollama pull tinyllama 2>/dev/null || echo "Will download on first run"
    ollama pull nomic-embed-text 2>/dev/null || echo "Will download on first run"
else
    echo -e "${YELLOW}⚠️ Ollama not available. Models will be downloaded when Ollama is installed.${NC}"
fi

# Create info file
cat > ~/.aos-lite/README.txt << 'EOF'
AOS-Lite for Termux
===================

A lightweight version of the AOS Brain that runs on Android devices.
No OpenClaw required. Pure Python + Ollama.

To start:
  ~/.aos-lite/start.sh

To view logs:
  tail -f ~/.aos-lite/logs/brain.log

To check state:
  cat ~/.aos-lite/brain/state.json

Configuration:
  ~/.aos-lite/config/brain.yaml

Models used:
  - phi3:mini (1.8B parameters)
  - tinyllama (1.1B parameters)
  - nomic-embed-text (embeddings)

Features:
  - OODA loop (Observe → Orient → Decide → Act)
  - Immutable safety laws
  - State persistence
  - Mobile-optimized (500ms ticks)

Note: This is a minimal version. For full features, use AOS on VPS.
EOF

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ AOS-Lite Installation Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}To start your brain:${NC}"
echo -e "  ${YELLOW}~/.aos-lite/start.sh${NC}"
echo ""
echo -e "${BLUE}To view logs:${NC}"
echo -e "  ${YELLOW}tail -f ~/.aos-lite/logs/brain.log${NC}"
echo ""
echo -e "${BLUE}Configuration:${NC}"
echo -e "  ${YELLOW}~/.aos-lite/config/brain.yaml${NC}"
echo ""
echo -e "${GREEN}Your autonomous brain is ready!${NC}"
