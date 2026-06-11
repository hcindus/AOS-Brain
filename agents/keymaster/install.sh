#!/bin/bash
# Key Master Installation Script
# Sets up The Key Master vault service

set -e

echo "🗝️  The Key Master - Installation"
echo "================================"

KEYMASTER_DIR="/root/.openclaw/workspace/agents/keymaster"
VENV_DIR="$KEYMASTER_DIR/.venv"

# Check if running as root for system-wide install
if [ "$EUID" -ne 0 ]; then 
    echo "Note: Running without root. Systemd service will need manual setup."
fi

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# Install dependencies
echo "Installing dependencies..."
pip install cryptography

# Set permissions
echo "Setting permissions..."
chmod 700 "$KEYMASTER_DIR/storage/vault"
chmod +x "$KEYMASTER_DIR/src/vault_api.py"
chmod +x "$KEYMASTER_DIR/src/keymaster_cli.py"
chmod +x "$KEYMASTER_DIR/scripts/bootstrap.py"
chmod +x "$KEYMASTER_DIR/scripts/rotation_automator.py"

# Create CLI symlink
echo "Creating CLI shortcut..."
ln -sf "$KEYMASTER_DIR/src/keymaster_cli.py" /usr/local/bin/keymaster || echo "Could not create symlink (needs root)"

# Install systemd service if root
if [ "$EUID" -eq 0 ]; then
    echo "Installing systemd service..."
    cat > /etc/systemd/system/keymaster.service << 'EOF'
[Unit]
Description=The Key Master - Vault API Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace/agents/keymaster
Environment=KEYMASTER_HOST=127.0.0.1
Environment=KEYMASTER_PORT=8472
Environment=PYTHONPATH=/root/.openclaw/workspace/agents/keymaster/src
ExecStart=/root/.openclaw/workspace/agents/keymaster/.venv/bin/python /root/.openclaw/workspace/agents/keymaster/src/vault_api.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    echo "Systemd service installed. Start with: systemctl start keymaster"
fi

# Run bootstrap
echo ""
echo "Running bootstrap..."
python3 "$KEYMASTER_DIR/scripts/bootstrap.py"

echo ""
echo "================================"
echo "✅ Installation complete!"
echo ""
echo "Usage:"
echo "  keymaster status          - Show vault status"
echo "  keymaster list            - List all secrets"
echo "  keymaster store <id> <svc> --type api_key - Store a secret"
echo "  keymaster get <id> --reason 'purpose' - Retrieve a secret"
echo "  keymaster rotate <id> --reason 'why' - Rotate a secret"
echo "  keymaster revoke <id> --reason 'why' - Revoke a secret"
echo "  keymaster queue           - Show rotation queue"
echo "  keymaster audit           - View audit log"
echo ""
echo "API Endpoints (if service running):"
echo "  GET  http://localhost:8472/status"
echo "  GET  http://localhost:8472/secrets"
echo "  GET  http://localhost:8472/rotation-queue"
echo "  POST http://localhost:8472/request  - Get secret value"
echo "  POST http://localhost:8472/store    - Store new secret"
echo "  POST http://localhost:8472/rotate   - Rotate secret"
echo "  POST http://localhost:8472/revoke   - Revoke secret"
echo ""
echo "Start service: systemctl start keymaster"
echo "View logs: journalctl -u keymaster -f"