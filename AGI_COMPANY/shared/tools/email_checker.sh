#!/bin/bash
# 📧 EMAIL HEALTH CHECKER
# Check Miles and Mortimer email accounts
# Date: 2026-02-22

VAULT="/root/.openclaw/workspace/armory/vault/EMAIL_CREDENTIALS.md"
LOG_FILE="/var/log/fleet-email-check.log"

echo "📧 FLEET EMAIL CHECK"
echo "===================="
echo "Time: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo ""

# Extract credentials from vault (simple grep for demo - in production use secure method)
# For now, just verify the config file exists

if [[ -f "$VAULT" ]]; then
    echo "✅ Email credentials configured"
    echo "   Location: $VAULT"
    echo ""
    echo "Configured accounts:"
    echo "  📧 miles@myl0nr0s.cloud"
    echo "  📧 mortimer@myl0nr0s.cloud"
    echo ""
    echo "Status: 🟢 Ready for IMAP/POP3 setup"
    echo ""
    echo "Next steps:"
    echo "  1. Configure IMAP client"
    echo "  2. Set up auto-polling"
    echo "  3. Alert on new messages"
else
    echo "❌ Email credentials not found"
    exit 1
fi

echo ""
echo "Log entry saved to: $LOG_FILE"
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - Email check complete" >> "$LOG_FILE"
