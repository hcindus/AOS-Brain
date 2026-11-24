#!/usr/bin/env bash
# Frontline SOA — install + start as a systemd service.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SVC="frontline-soa"

echo "== Frontline SOA installer =="
echo "  dir: $DIR"

# 1. deps (system python3)
echo ">> installing python deps"
python3 -m pip install --quiet -r "$DIR/requirements.txt" || {
  echo "!! pip install failed — may need --break-system-packages on this distro"
}

# 2. service unit (uses EnvironmentFile=aocros/secrets/telegram.env)
echo ">> writing systemd unit"
install -m 0644 "$DIR/setup/frontline-soa.service" "/etc/systemd/system/${SVC}.service"

systemctl daemon-reload
systemctl enable --now "${SVC}"

echo ">> status:"
systemctl --no-pager status "${SVC}" --lines 6 || true

echo ""
echo "== done =="
echo "  dashboard:  http://127.0.0.1:8120/"
echo "  health:     http://127.0.0.1:8120/health"
echo "  public:     https://psdepot.com/frontline/   (after nginx reload)"
