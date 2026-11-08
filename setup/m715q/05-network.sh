#!/usr/bin/env bash
# Network + identity setup for one M715q node (Miles OR Mortimer).
# Run ONCE per box, AFTER Ubuntu Server is installed.
# Covers: hostname, optional static IP, SSH keys, Tailscale (mesh to VPS + counterpart).
set -euo pipefail

# ==== EDIT THESE PER BOX ====================================================
HOSTNAME="${HOSTNAME:-miles}"       # "miles" or "mortimer" (keep it lowercase)

# Static IP is OPTIONAL. The SIMPLER path is a DHCP reservation on your router,
# then leave these empty. Only fill these if you want a hardcoded static IP.
STATIC_IP=""                        # e.g. "192.168.1.10"
GATEWAY=""                          # e.g. "192.168.1.1"  (your router)
DNS="192.168.1.1"                   # usually your router
CIDR="24"                           # subnet mask — /24 is standard for home
# =============================================================================

echo "==> Setting hostname to '${HOSTNAME}' ..."
sudo hostnamectl set-hostname "${HOSTNAME}"

# --- Optional static IP (via netplan) ---
if [[ -n "$STATIC_IP" ]]; then
  IFACE="$(ip -o -4 route show default | awk '{print $5}')"
  echo "==> Configuring static IP ${STATIC_IP}/${CIDR} on ${IFACE} ..."
  sudo tee /etc/netplan/99-static.yaml >/dev/null <<EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    ${IFACE}:
      dhcp4: no
      addresses: [${STATIC_IP}/${CIDR}]
      routes:
        - to: default
          via: ${GATEWAY}
      nameservers:
        addresses: [${DNS}]
EOF
  sudo netplan apply
else
  echo "==> Skipping static IP (using DHCP). Tip: reserve this box's IP on your router for a stable .lan address."
fi

# --- SSH keys ---
echo "==> Generating SSH key (if absent) ..."
if [[ ! -f ~/.ssh/id_ed25519 ]]; then
  ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519
fi
echo ""
echo "── Your public key (distribute to counterpart + respective VPS): ──"
cat ~/.ssh/id_ed25519.pub
echo "──────────────────────────────────────────────────────────────────────"
echo ""
echo "Copy it to the OTHER box and to this box's VPS:"
echo "  ssh-copy-id -i ~/.ssh/id_ed25519.pub <user>@<counterpart-or-vps>"
echo ""

# --- Tailscale (mesh: this box <-> counterpart <-> VPS <-> remote access) ---
echo "==> Installing Tailscale ..."
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

echo ""
echo "✅ ${HOSTNAME} network setup done."
echo "   After 'tailscale up', open the printed login URL and authenticate."
echo "   Then this box is reachable from anywhere by its tailnet name."
echo ""
echo "   Next on the counterpart box: run this same script with HOSTNAME= the other name."
echo "   And on the VPSes: run 'tailscale up' too so they join the same tailnet."
