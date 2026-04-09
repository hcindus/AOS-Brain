#!/bin/bash
# Complete deployment script for Brain v4.2

set -e

echo "======================================================================="
echo "  🚀 BRAIN v4.2 DEPLOYMENT"
echo "  Thyroid v1.1 + Model Router"
echo "======================================================================="

# Step 1: Validate environment
echo ""
echo "[Step 1/6] Validating environment..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found"
    exit 1
fi
echo "  ✅ Python3: $(python3 --version)"

# Check Ollama
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "  ✅ Ollama: running"
    
    # Check required models
    MODELS=("tinyllama:latest" "antoniohudnall/Mort_II:latest" "nomic-embed-text:latest")
    for model in "${MODELS[@]}"; do
        if curl -s http://localhost:11434/api/tags | grep -q "$model"; then
            echo "     ✅ $model"
        else
            echo "     ⚠️  $model (will be pulled on first use)"
        fi
    done
else
    echo "  ⚠️  Ollama: not running (will start without LLM features)"
fi

# Step 2: Backup current
echo ""
echo "[Step 2/6] Creating backup..."
BACKUP_DIR="/root/.aos/backup/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

cp /root/.aos/aos/complete_brain_v4.py "$BACKUP_DIR/" 2>/dev/null || true
cp /root/.aos/aos/thyroid.py "$BACKUP_DIR/" 2>/dev/null || true
cp /etc/systemd/system/aos-brain-v4.service "$BACKUP_DIR/" 2>/dev/null || true

echo "  ✅ Backup created: $BACKUP_DIR"

# Step 3: Stop services
echo ""
echo "[Step 3/6] Stopping services..."

if systemctl is-active --quiet aos-brain-v4; then
    systemctl stop aos-brain-v4
    echo "  ✅ Stopped aos-brain-v4"
else
    echo "  ℹ️  aos-brain-v4 not running"
fi

# Wait for clean shutdown
sleep 2

# Kill any remaining processes
pkill -f "complete_brain_v4" 2>/dev/null || true
sleep 1

echo "  ✅ Services stopped"

# Step 4: Deploy new files
echo ""
echo "[Step 4/6] Deploying Brain v4.2..."

# Copy main brain
cp /root/.aos/aos/complete_brain_v42.py /root/.aos/aos/complete_brain_v4.py
echo "  ✅ Deployed: complete_brain_v4.py (v4.2)"

# Copy Thyroid v1.1
cp /root/.aos/aos/thyroid_v11.py /root/.aos/aos/thyroid.py
echo "  ✅ Deployed: thyroid.py (v1.1)"

# Copy Model Router (already in place)
echo "  ✅ Deployed: model_router.py"

# Update QMD (already has tinyllama default)
echo "  ✅ QMD already updated (tinyllama default)"

# Step 5: Update systemd
echo ""
echo "[Step 5/6] Updating systemd..."

cat > /etc/systemd/system/aos-brain-v4.service << 'EOF'
[Unit]
Description=AOS Complete Brain v4.2 (Thyroid + Model Router)
Documentation=https://docs.openclaw.ai
After=network.target ollama.service
Wants=ollama.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/.aos/aos
Environment=PYTHONPATH=/root/.aos/aos
Environment=AOS_VERSION=4.2
Environment=AOS_THYROID_ENABLED=1
Environment=AOS_ROUTER_ENABLED=1
ExecStart=/usr/bin/python3 /root/.aos/aos/complete_brain_v4.py
ExecReload=/bin/kill -HUP $MAINPID
KillMode=mixed
KillSignal=SIGTERM
TimeoutStopSec=30
Restart=always
RestartSec=5
StartLimitInterval=60s
StartLimitBurst=3

# Resource limits
MemoryMax=8G
CPUQuota=200%

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=aos-brain-v4

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
echo "  ✅ Updated: aos-brain-v4.service"

# Step 6: Start services
echo ""
echo "[Step 6/6] Starting Brain v4.2..."

systemctl start aos-brain-v4

# Wait for startup
sleep 5

# Check status
if systemctl is-active --quiet aos-brain-v4; then
    echo "  ✅ aos-brain-v4: RUNNING"
else
    echo "  ❌ aos-brain-v4: FAILED"
    echo ""
    echo "Check logs: journalctl -u aos-brain-v4 -n 50 --no-pager"
    exit 1
fi

# Check socket
if [ -S "/tmp/aos_brain.sock" ]; then
    echo "  ✅ Socket: /tmp/aos_brain.sock"
else
    echo "  ⚠️  Socket: Not ready yet (may take a moment)"
fi

echo ""
echo "======================================================================="
echo "  🎉 BRAIN v4.2 DEPLOYED SUCCESSFULLY"
echo "======================================================================="
echo ""
echo "New Features:"
echo "  • Thyroid v1.1 - Reflexive mode switching"
echo "  • Model Router - tinyllama decisions, Mort_II voice"
echo "  • Memory-aware cost budget"
echo "  • Enhanced socket API"
echo ""
echo "Quick Test:"
echo "  echo '{\"cmd\":\"status\"}' | nc -U /tmp/aos_brain.sock"
echo "  echo '{\"cmd\":\"thyroid\"}' | nc -U /tmp/aos_brain.sock"
echo "  echo '{\"cmd\":\"router\"}' | nc -U /tmp/aos_brain.sock"
echo ""
echo "Logs:"
echo "  journalctl -u aos-brain-v4 -f"
echo ""
echo "======================================================================="
