#!/usr/bin/env bash
# Download Ubuntu Server LTS ISO + verify its SHA256 checksum.
# Run from any Linux box (or the machine you'll flash the USB from).
set -euo pipefail

VERSION="${VERSION:-24.04.1}"          # LTS; bump to 26.04.x if you prefer newer
BASE="https://releases.ubuntu.com/${VERSION}"
ISO="ubuntu-${VERSION}-live-server-amd64.iso"

cd "$(dirname "$0")"

echo "==> Downloading ${ISO} ..."
curl -fL -O "${BASE}/${ISO}"

echo "==> Downloading SHA256SUMS ..."
curl -fL -O "${BASE}/SHA256SUMS"

echo "==> Verifying checksum (only checks files present here) ..."
sha256sum -c SHA256SUMS --ignore-missing

echo ""
echo "✅ ${ISO} downloaded and verified."
echo "   Next: ./02-flash-usb.sh ${ISO} /dev/sdX   (replace sdX with your USB stick)"
