#!/usr/bin/env bash
# Write an ISO to a USB stick with dd.
# Usage: ./02-flash-usb.sh <iso> <device>
#   e.g.  ./02-flash-usb.sh ubuntu-24.04.1-live-server-amd64.iso /dev/sdb
set -euo pipefail

ISO="${1:-}"
DEV="${2:-}"

if [[ -z "$ISO" || -z "$DEV" ]]; then
  echo "Usage: $0 <iso> <device>"
  echo ""
  echo "Here are your block devices — pick the USB stick (look at SIZE/MODEL):"
  lsblk -o NAME,SIZE,MODEL,TRAN,TYPE,MOUNTPOINT
  exit 1
fi

if [[ ! -f "$ISO" ]]; then
  echo "Error: ISO not found: $ISO"
  exit 1
fi

if [[ ! -b "$DEV" ]]; then
  echo "Error: $DEV is not a block device. Check with: lsblk"
  exit 1
fi

# Safety: refuse if anything on that device is mounted
if mount | grep -q "^${DEV}"; then
  echo "Error: $DEV has mounted partitions. Unmount them first (umount /dev/sdX1 etc.)."
  exit 1
fi

echo "⚠️  THIS WILL DESTROY ALL DATA ON $DEV"
echo "    Target: $(lsblk -o NAME,SIZE,MODEL "$DEV" | tail -n +2)"
read -r -p "    Type 'yes' to continue: " ans
[[ "$ans" == "yes" ]] || { echo "Aborted."; exit 1; }

echo "==> Writing ${ISO} -> ${DEV} (this can take several minutes) ..."
sudo dd if="$ISO" of="$DEV" bs=4M status=progress conv=fsync

sync
echo "✅ Done. Safe to unplug. Boot the M715q from USB (F12 boot menu) and install."
