#!/usr/bin/env bash
# provision-customer.sh — stamp out a customer VPS ("click → done").
# Usage: ./provision-customer.sh <customer-slug> <domain>
#   e.g. ./provision-customer.sh joes-deli joesdeli.com
set -euo pipefail

CUSTOMER="${1:?customer slug required (e.g. joes-deli)}"
DOMAIN="${2:?domain required (e.g. joesdeli.com)}"

echo "🚀 Provisioning customer VPS: $CUSTOMER ($DOMAIN)"

# 1. Base deps
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3 python3-pip docker.io docker-compose-plugin git curl

# 2. Clone the stack repo
REPO="${REPO_URL:-https://github.com/hcindus/aocros.git}"
git clone "$REPO" /opt/psd 2>/dev/null || true
cd /opt/psd

# 3. Ollama (local models — optional, hosted can skip)
if [[ "${WITH_OLLAMA:-0}" == "1" ]]; then
  curl -fsSL https://ollama.com/install.sh | sh
  ollama pull tinyllama:latest
  ollama pull antoniohudnall/Mort_II:latest
fi

# 4. Customer config (isolated per account)
mkdir -p /opt/psd/config
cat > /opt/psd/config/customer.env <<EOF
CUSTOMER_SLUG=$CUSTOMER
DOMAIN=$DOMAIN
SMTP_USER=${SMTP_USER:-}
SMTP_PASS=${SMTP_PASS:-}
EOF

# 5. Start the customer-minimum stack
docker compose -f scaffolding/docker-compose.yml up -d

# 6. Enable the agent services
systemctl enable --now psdepot-order-api 2>/dev/null || true
systemctl enable --now aos-brain-v4 2>/dev/null || true

echo "✅ Customer VPS live: https://$DOMAIN"
echo "   Login: $DOMAIN (credentials in config/customer.env)"
