# M715q Two-Node Homelab — Build Plan & Parts List

**Date:** 2026-08-24
**Prepared by:** Miles

---

## The Goal

Two Lenovo ThinkCentre M715q Gen 1 (Type 10M3) Tiny PCs, each running **Omarchy** (DHH's Arch-based Linux), connected over **Tailscale** so they can talk to each other, each running **Pi agents** independently.

---

## Hardware Inventory (what you have)

| Item | Spec | Notes |
|------|------|-------|
| Machine | Lenovo ThinkCentre M715q Gen 1 (10M3) | ×2 |
| CPU | AMD Ryzen 3 Pro 2200GE or Ryzen 5 Pro 2400GE | socketed AM4, 35W |
| Storage | Netac NS100 128GB SATA SSD (2.5") | ×2, one per node |
| Video | Full-size DisplayPort (rear) | needs DP→HDMI cable |

**GPU upgrade: NOT possible.** The M715q Gen 1 has no PCIe expansion slot (unlike the M920X / P330 Tiny). It uses the integrated AMD APU graphics. This is a headless/agent node, so that's fine.

---

## Parts to Order

### 1. RAM — 32GB per node (CONFIRMED)

- **2× 16GB DDR4-2666 SODIMM** (260-pin, non-ECC) **per machine**
- **Total: 4× 16GB** sticks for both nodes
- Buy **matched 2×16GB kits** (two kits), not mixed single sticks
- DDR4-2666 is the sweet spot; 3200 will just downclock, don't pay extra

### 2. Thermal paste

- **Arctic MX-4** or **Noctua NT-H1** (non-conductive)
- One 4g tube is more than enough for both APUs
- Skip liquid metal (overkill + risky for 35W APUs)

### 3. Video cable

- **DisplayPort → HDMI** cable (full-size DP, confirmed from photo)
- Standard cable, no Lenovo dongle needed
- Only needed for the install; can go headless after

---

## The Build (per node)

1. Open the case, clean old paste (isopropyl + lint-free cloth)
2. Apply a small dot of fresh paste, re-seat the cooler
3. Install 2× 16GB SODIMM
4. Seat the Netac NS100 128GB SATA SSD
5. Connect DP→HDMI to a monitor + wired USB keyboard

---

## OS Install

**⚠️ Use the OFFICIAL Omarchy, not omarchy.net**

- **Official site / ISO:** https://omarchy.org
- **Repo:** https://github.com/basecamp/omarchy (branch `quattro`)
- **Manual:** https://learn.omacom.io

### Steps

1. Download the ISO from omarchy.org
2. Flash to USB (balenaEtcher on Mac/Win, or `caligula` on Linux)
3. **In BIOS: disable Secure Boot + TPM** (required)
4. Boot from USB, run the install wizard
5. **At the disk-format confirmation, hit `Ctrl+C` to install WITHOUT encryption**
   - Rationale: headless always-on node, no boot-time password needed
6. Set hostname `m715q-1` (node 1) / `m715q-2` (node 2)

---

## Networking (Tailscale mesh)

On each node:

```bash
sudo pacman -S tailscale
sudo systemctl enable --now tailscaled
sudo tailscale up
```

Authenticate each. Confirm they see each other:

```bash
tailscale ping m715q-2   # from node 1
tailscale ping m715q-1   # from node 2
```

Now they can SSH to each other over the tailnet from anywhere.

---

## Pi Agents

Install the agent stack (mise + Pi/Claude Code/Codex) on each node, point them at their task queues. Two independent nodes on one shared tailnet.

---

## Quick Summary — Order This

| Qty | Item |
|-----|------|
| 4 | 16GB DDR4-2666 SODIMM (as two 2×16GB matched kits) |
| 1 | Arctic MX-4 or Noctua NT-H1 thermal paste (4g) |
| 1 | DisplayPort → HDMI cable |
| — | (ISO downloaded from omarchy.org, no purchase) |
