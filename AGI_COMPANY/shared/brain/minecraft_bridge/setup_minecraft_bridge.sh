#!/bin/bash
# Setup Minecraft Bridge for AOS Brain
# Makes the bridge persistent and starts services

echo "Setting up Minecraft Bridge..."

# Create systemd service for bridge
cat > /etc/systemd/system/minecraft-bridge.service << 'EOF'
[Unit]
Description=Minecraft Bridge for AOS Brain
After=minecraft.service
Requires=minecraft.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace/AGI_COMPANY/shared/brain/minecraft_bridge
ExecStart=/usr/bin/python3 /root/.openclaw/workspace/AGI_COMPANY/shared/brain/minecraft_bridge/minecraft_bridge_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for game training
cat > /etc/systemd/system/myl-game-trainer.service << 'EOF'
[Unit]
Description=MYL Agent Game Training Service
After=minecraft-bridge.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/training
ExecStart=/usr/bin/python3 -c "from myl_game_trainer import run_training; run_training()"
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
systemctl daemon-reload

# Enable services
systemctl enable minecraft-bridge.service
systemctl enable myl-game-trainer.service

echo "Services created. Starting..."

# Start services
systemctl start minecraft-bridge.service
systemctl start myl-game-trainer.service

echo ""
echo "Minecraft Bridge Status:"
systemctl status minecraft-bridge.service --no-pager -l

echo ""
echo "Game Trainer Status:"
systemctl status myl-game-trainer.service --no-pager -l

echo ""
echo "Setup complete!"
echo "Bridge: localhost:8765 (observer), localhost:8766 (actor)"
