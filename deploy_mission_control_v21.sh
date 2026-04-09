#!/bin/bash
# Deploy Mission Control v2.1

echo "======================================================================="
echo "  🎛️  MISSION CONTROL v2.1 DEPLOYMENT"
echo "======================================================================="

# Stop existing
echo ""
echo "[Step 1/2] Stopping Mission Control..."
if systemctl is-active --quiet aos-mission-control; then
    systemctl stop aos-mission-control
    echo "  ✅ Stopped"
fi
sleep 2

# Deploy new version
echo ""
echo "[Step 2/2] Deploying v2.1..."
cp /root/.openclaw/workspace/aocros/mission_control/server_v21.py \
   /root/.openclaw/workspace/aocros/mission_control/server_v2.py

echo "  ✅ Deployed server_v2.py (v2.1)"

# Update systemd if needed
cat > /etc/systemd/system/aos-mission-control.service << 'EOF'
[Unit]
Description=AOS Mission Control v2.1 (Brain v4.2 Compatible)
After=aos-brain-v4.service
Wants=aos-brain-v4.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace/aocros/mission_control
Environment=PYTHONPATH=/root/.aos/aos
ExecStart=/usr/bin/python3 /root/.openclaw/workspace/aocros/mission_control/server_v2.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl start aos-mission-control
sleep 2

if systemctl is-active --quiet aos-mission-control; then
    echo "  ✅ Mission Control: RUNNING"
else
    echo "  ❌ Mission Control: FAILED"
    exit 1
fi

echo ""
echo "======================================================================="
echo "  🎉 MISSION CONTROL v2.1 DEPLOYED"
echo "======================================================================="
echo ""
echo "New endpoints:"
echo "  GET  /api/thyroid     - Thyroid status"
echo "  GET  /api/router      - Router status"  
echo "  POST /api/decide      - Make decision"
echo "  POST /api/speak       - Generate voice"
echo ""
echo "Test: curl http://localhost:8080/api/status"
