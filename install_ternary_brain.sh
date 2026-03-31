#!/bin/bash
#
# 🧠 TERNARY BRAIN SYSTEM v2.0 - INSTALLER
# For: Mortimer.cloud VPS (or any Ubuntu/Debian system)
# Author: Miles (AOE)
# Date: 2026-03-31
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║           🧠 TERNARY BRAIN SYSTEM v2.0 INSTALLER               ║"
echo "║                                                               ║"
echo "║              Heart + Brain + Stomach = ALIVE                 ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

INSTALL_DIR="${HOME}/.aos"
REPO_URL="https://github.com/hcindus/AOS-Brain.git"

echo -e "${BLUE}[INFO]${NC} Installing to: $INSTALL_DIR"
echo -e "${BLUE}[INFO]${NC} Repository: $REPO_URL"
echo ""

# Check dependencies
echo -e "${YELLOW}[CHECK]${NC} Verifying dependencies..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3 not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv
fi

if ! command -v sqlite3 &> /dev/null; then
    echo -e "${YELLOW}[WARN]${NC} SQLite3 not found. Installing..."
    sudo apt-get install -y sqlite3
fi

if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}[WARN]${NC} Git not found. Installing..."
    sudo apt-get install -y git
fi

echo -e "${GREEN}[OK]${NC} Dependencies verified"
echo ""

# Create directories
echo -e "${YELLOW}[SETUP]${NC} Creating directory structure..."
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"
mkdir -p {brain,memory,config,logs,models,scripts,backups}
echo -e "${GREEN}[OK]${NC} Directories created"
echo ""

# Clone repository
echo -e "${YELLOW}[CLONE]${NC} Fetching Ternary Brain..."
if [ -d "$INSTALL_DIR/aos" ]; then
    cd "$INSTALL_DIR/aos"
    git pull origin master
else
    git clone "$REPO_URL" "$INSTALL_DIR/aos"
fi
echo -e "${GREEN}[OK]${NC} Repository cloned"
echo ""

# Set up Python environment
echo -e "${YELLOW}[PYTHON]${NC} Setting up virtual environment..."
cd "$INSTALL_DIR"
python3 -m venv venv
source venv/bin/activate

echo -e "${YELLOW}[PIP]${NC} Installing Python packages..."
pip install --upgrade pip
pip install requests numpy sqlite3

echo -e "${GREEN}[OK]${NC} Python environment ready"
echo ""

# Copy brain files
echo -e "${YELLOW}[COPY]${NC} Installing brain modules..."
cp -r "$INSTALL_DIR/aos/AOS/brain"/* "$INSTALL_DIR/brain/" 2>/dev/null || true
cp -r "$INSTALL_DIR/aos/AOS/scripts"/* "$INSTALL_DIR/scripts/" 2>/dev/null || true

# Make scripts executable
chmod +x "$INSTALL_DIR/scripts"/*.sh 2>/dev/null || true
echo -e "${GREEN}[OK]${NC} Brain modules installed"
echo ""

# Create launcher script
echo -e "${YELLOW}[CREATE]${NC} Creating launcher..."
cat > "$INSTALL_DIR/start_brain.sh" << 'EOF'
#!/bin/bash
# Ternary Brain Launcher

INSTALL_DIR="${HOME}/.aos"
LOG_FILE="$INSTALL_DIR/logs/brain.log"
PID_FILE="$INSTALL_DIR/brain/daemon.pid"

echo "🧠 Starting Ternary Brain..."
echo "Log: $LOG_FILE"

# Check if already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "Brain already running (PID: $OLD_PID)"
        exit 0
    fi
fi

# Start brain
cd "$INSTALL_DIR"
source venv/bin/activate

nohup python3 -c "
import sys
sys.path.insert(0, '$INSTALL_DIR/brain')
from brain_complete import MortimerBrainComplete, get_state
import time

brain = MortimerBrainComplete()
print('🧠 Ternary Brain initialized')
print(f'Tick: {brain.ooda.tick_count}')
print(f'Nodes: {sum(brain.ooda.basal.policy_nn[\"nodes\"])}')

# Run main loop
try:
    while True:
        time.sleep(1)
        state = get_state()
        if state:
            print(f'[TICK {state.get(\"tick_count\", 0)}] Nodes: {state.get(\"nodes\", 0)} | Hunger: {state.get(\"hunger\", 0):.2f}')
except KeyboardInterrupt:
    print('Shutting down...')
" > "$LOG_FILE" 2>&1 &

PID=$!
echo $PID > "$PID_FILE"

echo "✅ Brain started (PID: $PID)"
echo "View logs: tail -f $LOG_FILE"
EOF

chmod +x "$INSTALL_DIR/start_brain.sh"

# Create status checker
cat > "$INSTALL_DIR/status.sh" << 'EOF'
#!/bin/bash
INSTALL_DIR="${HOME}/.aos"
STATE_FILE="$INSTALL_DIR/brain/state/brain_state.json"
PID_FILE="$INSTALL_DIR/brain/daemon.pid"

echo "🧠 TERNARY BRAIN STATUS"
echo "═══════════════════════════════════════════════════"

# Check if running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "Status: \033[0;32m● RUNNING\033[0m (PID: $PID)"
    else
        echo -e "Status: \033[0;31m● STOPPED\033[0m (PID file exists but process dead)"
    fi
else
    echo -e "Status: \033[0;31m● NOT RUNNING\033[0m"
fi

# Show state if available
if [ -f "$STATE_FILE" ]; then
    echo ""
    echo "Last State:"
    cat "$STATE_FILE" | python3 -m json.tool 2>/dev/null | head -30
fi

echo ""
echo "Commands:"
echo "  start:  $INSTALL_DIR/start_brain.sh"
echo "  stop:   kill \$(cat $PID_FILE)"
echo "  logs:   tail -f $INSTALL_DIR/logs/brain.log"
EOF

chmod +x "$INSTALL_DIR/status.sh"
echo -e "${GREEN}[OK]${NC} Launcher scripts created"
echo ""

# Create systemd service (optional)
echo -e "${YELLOW}[SERVICE]${NC} Creating systemd service..."
cat > /tmp/ternary-brain.service << EOF
[Unit]
Description=Ternary Brain System
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/start_brain.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo -e "${CYAN}To install as systemd service:${NC}"
echo "  sudo cp /tmp/ternary-brain.service /etc/systemd/system/"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl enable ternary-brain"
echo "  sudo systemctl start ternary-brain"
echo ""

# Final summary
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}    ✅ TERNARY BRAIN v2.0 INSTALLATION COMPLETE${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}Installation Directory:${NC} $INSTALL_DIR"
echo -e "${CYAN}Brain Modules:${NC} $INSTALL_DIR/brain"
echo -e "${CYAN}Memory:${NC} $INSTALL_DIR/memory"
echo -e "${CYAN}Logs:${NC} $INSTALL_DIR/logs"
echo ""
echo -e "${CYAN}Commands:${NC}"
echo "  Start:   $INSTALL_DIR/start_brain.sh"
echo "  Status:  $INSTALL_DIR/status.sh"
echo "  Logs:    tail -f $INSTALL_DIR/logs/brain.log"
echo ""
echo -e "${CYAN}Next Steps:${NC}"
echo "  1. Start the brain: ~/.aos/start_brain.sh"
echo "  2. Check status: ~/.aos/status.sh"
echo "  3. Feed data via the web interface (port 8766)"
echo ""
echo -e "${YELLOW}🏴󠁧󠁢󠁳󠁣󠁴󠁿 The brain awakens!${NC}"
echo ""
