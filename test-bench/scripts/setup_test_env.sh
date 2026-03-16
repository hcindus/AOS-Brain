#!/bin/bash
# Test-Bench Environment Setup Script
# Creates isolated test environment for AOS Brain testing

set -e

TEST_DIR="/root/.openclaw/workspace/test-bench"
ENV_DIR="$TEST_DIR/environments/aos-brain-test"
LOG_FILE="$TEST_DIR/logs/setup_$(date +%Y%m%d_%H%M%S).log"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     AOS BRAIN TEST-BENCH SETUP                           ║"
echo "║     Creating Isolated Test Environment                   ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Create log file
mkdir -p "$TEST_DIR/logs"
exec 1>>"$LOG_FILE" 2>>"$LOG_FILE"

echo "[$(date)] Starting Test-Bench setup..."

# Create environment structure
echo "[$(date)] Creating directory structure..."
mkdir -p "$ENV_DIR"/{brain,config,state,input,output,logs}

# Copy brain source
echo "[$(date)] Copying brain source code..."
cp -r /root/.openclaw/workspace/AOS/brain/*.py "$ENV_DIR/brain/"
cp -r /root/.openclaw/workspace/AOS/brain/agents "$ENV_DIR/brain/"

# Copy config
echo "[$(date)] Copying configuration..."
cp /root/.openclaw/workspace/AOS/config/brain.yaml "$ENV_DIR/config/"

# Modify config for test environment
echo "[$(date)] Modifying config for test environment..."
sed -i "s|~/.aos|$ENV_DIR/.aos|g" "$ENV_DIR/config/brain.yaml"

# Create test input queue
echo "[$(date)] Setting up input queue..."
mkdir -p "$ENV_DIR/.aos/brain/input"
touch "$ENV_DIR/.aos/brain/input/queue.jsonl"

# Create state directory
echo "[$(date)] Setting up state directory..."
mkdir -p "$ENV_DIR/.aos/brain/state"

# Create test scripts
echo "[$(date)] Creating test scripts..."

cat > "$ENV_DIR/scripts/run_brain.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/../brain"
python3 brain.py &
echo $! > ../brain.pid
echo "Brain started with PID: $(cat ../brain.pid)"
EOF

cat > "$ENV_DIR/scripts/stop_brain.sh" << 'EOF'
#!/bin/bash
if [ -f "$(dirname "$0")/../brain.pid" ]; then
    kill $(cat "$(dirname "$0")/../brain.pid") 2>/dev/null
    rm "$(dirname "$0")/../brain.pid"
    echo "Brain stopped"
else
    echo "Brain not running"
fi
EOF

cat > "$ENV_DIR/scripts/feed_input.sh" << 'EOF'
#!/bin/bash
INPUT="$1"
QUEUE_FILE="$(dirname "$0")/../.aos/brain/input/queue.jsonl"

if [ -z "$INPUT" ]; then
    echo "Usage: ./feed_input.sh 'Your input here'"
    exit 1
fi

echo '{"text": "'"$INPUT"'", "source": "test", "timestamp": '$(date +%s)', "type": "user_input"}' >> "$QUEUE_FILE"
echo "✓ Fed to brain: $INPUT"
EOF

cat > "$ENV_DIR/scripts/check_status.sh" << 'EOF'
#!/bin/bash
STATE_FILE="$(dirname "$0")/../.aos/brain/state/brain_state.json"

if [ -f "$STATE_FILE" ]; then
    echo "=== BRAIN STATUS ==="
    python3 -c "
import json
with open('$STATE_FILE', 'r') as f:
    d = json.load(f)
    print(f\"Tick: {d.get('tick', 'N/A')}\")
    print(f\"Phase: {d.get('phase', 'N/A')}\")
    print(f\"Nodes: {d.get('policy_nn', {}).get('total_nodes', 'N/A')}\")
    print(f\"Novelty: {d.get('growingnn', {}).get('novelty', 'N/A')}\")
    print(f\"Memory: {d.get('memory_nn', {}).get('clusters', 'N/A')} clusters\")
"
else
    echo "No state file found"
fi
EOF

chmod +x "$ENV_DIR/scripts/"*.sh

echo "[$(date)] Test-Bench setup complete!"
echo ""
echo "Environment location: $ENV_DIR"
echo "Scripts available:"
echo "  - run_brain.sh: Start brain"
echo "  - stop_brain.sh: Stop brain"
echo "  - feed_input.sh: Feed input to brain"
echo "  - check_status.sh: Check brain status"
echo ""
echo "Log file: $LOG_FILE"
