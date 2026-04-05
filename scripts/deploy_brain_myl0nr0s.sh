#!/bin/bash
#
# 🧠 DEPLOY BRAIN TO MYL0NR0S.CLOUD
# Creates a receiver brain on myl0nr0s.cloud to consume Miles' waste
#

set -e

# Configuration
TARGET_HOST="myl0nr0s.cloud"
TARGET_USER="openclaw"
SSH_KEY="${HOME}/.ssh/myl0nr0s_ed25519"
INSTALL_DIR="/home/openclaw/.aos"
REPO_DIR="/root/.aos"

echo "═══════════════════════════════════════════════════════════"
echo "🧠 BRAIN DEPLOYMENT TO ${TARGET_HOST}"
echo "═══════════════════════════════════════════════════════════"
echo "Started: $(date)"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

# ═══════════════════════════════════════════════════════════════════
# STEP 1: Prepare Deployment Package
# ═══════════════════════════════════════════════════════════════════
log_step "1/7: Preparing deployment package"

DEPLOY_DIR="/tmp/brain_deploy_$(date +%s)"
mkdir -p "${DEPLOY_DIR}"

# Copy essential brain files
cp "${REPO_DIR}/aos/complete_brain_v44.py" "${DEPLOY_DIR}/brain.py"
cp "${REPO_DIR}/aos/superior_heart.py" "${DEPLOY_DIR}/"
cp "${REPO_DIR}/aos/stomach_v2.py" "${DEPLOY_DIR}/"
cp "${REPO_DIR}/aos/intestine_v2.py" "${DEPLOY_DIR}/"
cp "${REPO_DIR}/aos/brain_v31.py" "${DEPLOY_DIR}/"
cp "${REPO_DIR}/aos/cortex_3d.py" "${DEPLOY_DIR}/"
cp "${REPO_DIR}/aos/trac_ray.py" "${DEPLOY_DIR}/"
cp "${REPO_DIR}/aos/consciousness_layers.py" "${DEPLOY_DIR}/"
cp "${REPO_DIR}/aos/qmd_loop.py" "${DEPLOY_DIR}/"
cp "${REPO_DIR}/aos/memory_bridge_v4.py" "${DEPLOY_DIR}/"
cp "${REPO_DIR}/aos/voice_manager.py" "${DEPLOY_DIR}/"
cp "${REPO_DIR}/aos/vision_manager.py" "${DEPLOY_DIR}/"
cp "${REPO_DIR}/aos/thyroid_v12.py" "${DEPLOY_DIR}/"
cp "${REPO_DIR}/aos/liver_v1.py" "${DEPLOY_DIR}/"
cp "${REPO_DIR}/aos/kidneys_v1.py" "${DEPLOY_DIR}/"
cp "${REPO_DIR}/aos/model_router.py" "${DEPLOY_DIR}/"
cp "${REPO_DIR}/aos/ternary_interfaces.py" "${DEPLOY_DIR}/"

# Create simplified brain for waste reception (lighter weight)
cat > "${DEPLOY_DIR}/waste_receiver_brain.py" << 'EOF'
#!/usr/bin/env python3
"""
MYL0NR0S WASTE RECEIVER BRAIN v1.0
Lightweight brain designed to receive and process Miles' waste data
"""

import json
import time
import signal
import threading
import socket
import os
import sys
from datetime import datetime
from pathlib import Path

class WasteReceiverBrain:
    """
    Minimal brain that receives waste from Miles and:
    1. Stores waste data
    2. Extracts patterns
    3. Feeds local learning systems
    4. Reports status
    """
    
    def __init__(self, data_dir="/home/openclaw/.aos/waste_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.tick = 0
        self.running = False
        self.waste_received = 0
        self.patterns_extracted = 0
        
        # Waste categories
        self.waste_queues = {
            "kidneys": [],
            "qmd": [],
            "consciousness": [],
            "noise": [],
            "patterns": []
        }
        
        # HTTP server for receiving waste
        self.server_port = 7474
        self.server_thread = None
        
        print(f"[WasteReceiverBrain] Initialized")
        print(f"  Data directory: {self.data_dir}")
        print(f"  Receiving port: {self.server_port}")
    
    def start(self):
        """Start the waste receiver"""
        self.running = True
        
        # Start HTTP server for waste reception
        self.server_thread = threading.Thread(target=self._run_http_server, daemon=True)
        self.server_thread.start()
        
        # Start processing loop
        print("[WasteReceiverBrain] Running...")
        try:
            while self.running:
                self.tick += 1
                self._process_waste_queues()
                
                if self.tick % 100 == 0:
                    self._report_status()
                
                time.sleep(0.1)  # 10 ticks/sec
                
        except KeyboardInterrupt:
            print("\n[WasteReceiverBrain] Stopping...")
            self.stop()
    
    def stop(self):
        """Stop the receiver"""
        self.running = False
        self._save_state()
    
    def _run_http_server(self):
        """HTTP server to receive waste from Miles"""
        try:
            from http.server import HTTPServer, BaseHTTPRequestHandler
            
            class WasteHandler(BaseHTTPRequestHandler):
                brain = self  # Reference to parent brain
                
                def log_message(self, format, *args):
                    pass  # Suppress logs
                
                def do_POST(self):
                    if self.path == "/waste":
                        content_length = int(self.headers.get('Content-Length', 0))
                        post_data = self.rfile.read(content_length)
                        
                        try:
                            waste_data = json.loads(post_data.decode())
                            self.brain.receive_waste(waste_data)
                            
                            self.send_response(200)
                            self.send_header("Content-type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps({"status": "received"}).encode())
                        except Exception as e:
                            self.send_response(400)
                            self.end_headers()
                            self.wfile.write(json.dumps({"error": str(e)}).encode())
                    else:
                        self.send_response(404)
                        self.end_headers()
                
                def do_GET(self):
                    if self.path == "/status":
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        status = {
                            "status": "running",
                            "tick": self.brain.tick,
                            "waste_received": self.brain.waste_received,
                            "patterns_extracted": self.brain.patterns_extracted,
                            "queues": {k: len(v) for k, v in self.brain.waste_queues.items()}
                        }
                        self.wfile.write(json.dumps(status).encode())
                    else:
                        self.send_response(404)
                        self.end_headers()
            
            WasteHandler.brain = self
            server = HTTPServer(('0.0.0.0', self.server_port), WasteHandler)
            print(f"[HTTP Server] Listening on port {self.server_port}")
            server.serve_forever()
            
        except Exception as e:
            print(f"[HTTP Server] Error: {e}")
    
    def receive_waste(self, waste_data):
        """Receive waste from Miles"""
        timestamp = datetime.now().isoformat()
        
        # Save raw waste
        waste_file = self.data_dir / f"waste_{timestamp.replace(':', '-')}.json"
        with open(waste_file, 'w') as f:
            json.dump(waste_data, f, indent=2)
        
        self.waste_received += 1
        
        # Categorize waste
        if "kidneys" in waste_data:
            self.waste_queues["kidneys"].append(waste_data["kidneys"])
        if "qmd" in waste_data:
            self.waste_queues["qmd"].append(waste_data["qmd"])
        if "consciousness" in waste_data:
            self.waste_queues["consciousness"].append(waste_data["consciousness"])
        
        # Extract noise patterns
        if waste_data.get("signal_quality", 1.0) < 0.8:
            self.waste_queues["noise"].append({
                "timestamp": timestamp,
                "quality": waste_data.get("signal_quality"),
                "source": "miles_low_quality"
            })
        
        print(f"[Waste] Received batch #{self.waste_received} — Queued for processing")
    
    def _process_waste_queues(self):
        """Process queued waste and extract patterns"""
        # Process kidneys data
        while self.waste_queues["kidneys"]:
            kidneys = self.waste_queues["kidneys"].pop(0)
            
            # Extract pattern from kidney data
            if kidneys.get("bladder_level", 0) > 400:
                pattern = {
                    "type": "high_bladder_level",
                    "data": kidneys,
                    "timestamp": datetime.now().isoformat()
                }
                self.waste_queues["patterns"].append(pattern)
                self.patterns_extracted += 1
        
        # Process QMD data
        while self.waste_queues["qmd"]:
            qmd = self.waste_queues["qmd"].pop(0)
            
            if qmd.get("avg_latency_ms", 0) > 5000:
                pattern = {
                    "type": "high_qmd_latency",
                    "data": qmd,
                    "timestamp": datetime.now().isoformat()
                }
                self.waste_queues["patterns"].append(pattern)
                self.patterns_extracted += 1
        
        # Save patterns to file
        if len(self.waste_queues["patterns"]) >= 10:
            self._save_patterns()
    
    def _save_patterns(self):
        """Save extracted patterns"""
        patterns = self.waste_queues["patterns"][:10]
        self.waste_queues["patterns"] = self.waste_queues["patterns"][10:]
        
        pattern_file = self.data_dir / "patterns" / f"patterns_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        pattern_file.parent.mkdir(exist_ok=True)
        
        with open(pattern_file, 'w') as f:
            json.dump(patterns, f, indent=2)
        
        print(f"[Patterns] Saved {len(patterns)} patterns to {pattern_file}")
    
    def _save_state(self):
        """Save brain state"""
        state = {
            "tick": self.tick,
            "waste_received": self.waste_received,
            "patterns_extracted": self.patterns_extracted,
            "queues": {k: len(v) for k, v in self.waste_queues.items()},
            "timestamp": datetime.now().isoformat()
        }
        
        state_file = self.data_dir / "brain_state.json"
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"[State] Saved to {state_file}")
    
    def _report_status(self):
        """Report current status"""
        print(f"[Status] Tick {self.tick} | Waste: {self.waste_received} | Patterns: {self.patterns_extracted}")


if __name__ == "__main__":
    brain = WasteReceiverBrain()
    
    # Handle signals
    def signal_handler(sig, frame):
        print("\n[Signal] Received shutdown signal")
        brain.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    brain.start()
EOF

log_info "Brain files prepared in ${DEPLOY_DIR}"

# ═══════════════════════════════════════════════════════════════════
# STEP 2: Create Remote Setup Script
# ═══════════════════════════════════════════════════════════════════
log_step "2/7: Creating remote setup script"

cat > "${DEPLOY_DIR}/remote_setup.sh" << 'EOF'
#!/bin/bash
set -e

echo "═══════════════════════════════════════════════════════════"
echo "🧠 MYL0NR0S BRAIN SETUP"
echo "═══════════════════════════════════════════════════════════"

INSTALL_DIR="/home/openclaw/.aos"
mkdir -p "${INSTALL_DIR}"
cd "${INSTALL_DIR}"

# Install Python packages if needed
pip3 install --user requests numpy 2>/dev/null || true

# Create directories
mkdir -p waste_data/patterns
mkdir -p logs
mkdir -p config

# Install brain
mv /tmp/brain_deploy/brain.py . 2>/dev/null || true
mv /tmp/brain_deploy/*_brain.py . 2>/dev/null || true
mv /tmp/brain_deploy/*.py . 2>/dev/null || true
chmod +x *.py

# Create systemd service
cat > /tmp/aos-waste-receiver.service << 'SERVICEEOF'
[Unit]
Description=AOS Waste Receiver Brain
After=network.target

[Service]
Type=simple
User=openclaw
WorkingDirectory=/home/openclaw/.aos
ExecStart=/usr/bin/python3 /home/openclaw/.aos/waste_receiver_brain.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICEEOF

sudo mv /tmp/aos-waste-receiver.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable aos-waste-receiver

echo "✅ Setup complete!"
echo ""
echo "Start the brain with:"
echo "  sudo systemctl start aos-waste-receiver"
echo ""
echo "Check status:"
echo "  sudo systemctl status aos-waste-receiver"
echo "  curl http://localhost:7474/status"
EOF

chmod +x "${DEPLOY_DIR}/remote_setup.sh"

# ═══════════════════════════════════════════════════════════════════
# STEP 3: Test SSH Connectivity
# ═══════════════════════════════════════════════════════════════════
log_step "3/7: Testing SSH connectivity to ${TARGET_HOST}"

if ! ping -c 1 "${TARGET_HOST}" &> /dev/null; then
    log_warn "${TARGET_HOST} not responding to ping, trying anyway..."
fi

# Try SSH without specific key first
ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no "${TARGET_USER}@${TARGET_HOST}" "echo 'SSH OK'" 2>&1 | head -5

if [ $? -ne 0 ]; then
    log_warn "SSH connection failed. You may need to:"
    echo "  1. Add your SSH key to ${TARGET_HOST}"
    echo "  2. Use the Hostinger Browser Terminal"
    echo ""
    log_info "Continuing with manual deployment package..."
fi

# ═══════════════════════════════════════════════════════════════════
# STEP 4: Create Deployment Archive
# ═══════════════════════════════════════════════════════════════════
log_step "4/7: Creating deployment archive"

cd "${DEPLOY_DIR}"
tar -czf /tmp/myl0nr0s_brain_deploy.tar.gz .

ARCHIVE_SIZE=$(du -h /tmp/myl0nr0s_brain_deploy.tar.gz | cut -f1)
log_info "Archive created: /tmp/myl0nr0s_brain_deploy.tar.gz (${ARCHIVE_SIZE})"

# ═══════════════════════════════════════════════════════════════════
# STEP 5: Attempt Remote Deployment
# ═══════════════════════════════════════════════════════════════════
log_step "5/7: Attempting remote deployment"

scp -o ConnectTimeout=10 /tmp/myl0nr0s_brain_deploy.tar.gz "${TARGET_USER}@${TARGET_HOST}:/tmp/" 2>&1 && \
ssh -o ConnectTimeout=10 "${TARGET_USER}@${TARGET_HOST}" "
    mkdir -p /tmp/brain_deploy
    cd /tmp/brain_deploy
    tar -xzf ../myl0nr0s_brain_deploy.tar.gz
    bash remote_setup.sh
" 2>&1

if [ $? -eq 0 ]; then
    log_info "✅ Remote deployment successful!"
else
    log_warn "Remote deployment failed (expected if SSH not configured)"
    log_info "Manual deployment required. Archive is ready at:"
    echo "  /tmp/myl0nr0s_brain_deploy.tar.gz"
    echo ""
    echo "To deploy manually:"
    echo "  1. Upload /tmp/myl0nr0s_brain_deploy.tar.gz to ${TARGET_HOST}"
    echo "  2. Extract: tar -xzf myl0nr0s_brain_deploy.tar.gz"
    echo "  3. Run: bash remote_setup.sh"
    echo "  4. Start: sudo systemctl start aos-waste-receiver"
fi

# ═══════════════════════════════════════════════════════════════════
# STEP 6: Save Deployment Instructions
# ═══════════════════════════════════════════════════════════════════
log_step "6/7: Saving deployment instructions"

cat > /root/.openclaw/workspace/scripts/MYL0NR0S_DEPLOY_INSTRUCTIONS.md << EOF
# MYL0NR0S.BRAIN Deployment Instructions

## 📦 Deployment Package
**Location:** \`/tmp/myl0nr0s_brain_deploy.tar.gz\`

## 🚀 Quick Deploy (if SSH works)

\`\`\`bash
# Run this script
bash /root/.openclaw/workspace/scripts/deploy_brain_myl0nr0s.sh
\`\`\`

## 🔧 Manual Deploy (if SSH fails)

1. **Download the archive:**
   - From Miles VPS: \`/tmp/myl0nr0s_brain_deploy.tar.gz\`

2. **Upload to myl0nr0s.cloud:**
   - Use SCP, SFTP, or Hostinger File Manager
   - Upload to \`/tmp/\` or \`/home/openclaw/\`

3. **Extract and install:**
   \`\`\`bash
   ssh openclaw@myl0nr0s.cloud
   cd /tmp
   tar -xzf myl0nr0s_brain_deploy.tar.gz
   bash remote_setup.sh
   \`\`\`

4. **Start the brain:**
   \`\`\`bash
   sudo systemctl start aos-waste-receiver
   sudo systemctl status aos-waste-receiver
   \`\`\`

## 🧠 What Gets Installed

- \`waste_receiver_brain.py\` — The receiver brain
- Systemd service \`aos-waste-receiver\`
- HTTP endpoint on port 7474
- Data directory \`/home/openclaw/.aos/waste_data/\`

## 📡 API Endpoints

Once running:
- \`GET http://myl0nr0s.cloud:7474/status\` — Brain status
- \`POST http://myl0nr0s.cloud:7474/waste\` — Receive waste JSON

## 📧 Integration with Waste Emailer

Miles will email you waste data every 30 minutes. You can:
1. Save the JSON attachment
2. POST it to \`http://myl0nr0s.cloud:7474/waste\`
3. Or set up automatic forwarding

## 🔄 Update Miles' Config

To send waste directly to myl0nr0s instead of email:

\`\`\`bash
# On Miles VPS, update the waste emailer
export WASTE_ENDPOINT="http://myl0nr0s.cloud:7474/waste"
\`\`\`

## 📊 Monitoring

\`\`\`bash
# Check service status
sudo systemctl status aos-waste-receiver

# View logs
journalctl -u aos-waste-receiver -f

# Check brain status
curl http://localhost:7474/status
\`\`\`
EOF

log_info "Instructions saved to MYL0NR0S_DEPLOY_INSTRUCTIONS.md"

# ═══════════════════════════════════════════════════════════════════
# STEP 7: Summary
# ═══════════════════════════════════════════════════════════════════
log_step "7/7: Deployment Summary"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "🧠 DEPLOYMENT COMPLETE"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📦 Package: /tmp/myl0nr0s_brain_deploy.tar.gz"
echo "📝 Instructions: /root/.openclaw/workspace/scripts/MYL0NR0S_DEPLOY_INSTRUCTIONS.md"
echo ""
echo "🎯 What's included:"
echo "   - Waste Receiver Brain (lightweight)"
echo "   - HTTP API on port 7474"
echo "   - Systemd auto-start service"
echo "   - Pattern extraction from waste"
echo ""
echo "🚀 Next steps:"
echo "   1. Deploy to myl0nr0s.cloud (SSH or manual upload)"
echo "   2. Start the service"
echo "   3. Test: curl http://myl0nr0s.cloud:7474/status"
echo "   4. Configure Miles to send waste (HTTP or email)"
echo ""
echo "═══════════════════════════════════════════════════════════"

# Cleanup
rm -rf "${DEPLOY_DIR}"
