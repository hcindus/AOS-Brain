# M715q Tiny — Local LLM Build

Two identical, independent Lenovo M715q Tiny boxes (Ryzen APU, 32GB RAM each),
each running llama.cpp. CPU-only inference — the RAM is the "VRAM."

## Hardware
- 2× M715q Tiny (Ryzen 2200GE / 2400GE, Zen/Zen+, AVX2)
- 2× 500GB NVMe (one per box, boot/OS drive)
- 1× 250GB SATA (scratch)
- 2× 16GB DDR4 SODIMM per box (dual-channel — do NOT run single stick)

## Step-by-step (it's been a while — quick refresh)

### 1. Make the USB installer
```bash
./01-download-ubuntu.sh          # downloads + verifies the ISO
./02-flash-usb.sh ubuntu-24.04.1-live-server-amd64.iso /dev/sdX
```
- Identify your stick with `lsblk` (look at SIZE/MODEL). It's usually `/dev/sdb`.
- `dd` writes the ISO directly; Ubuntu ISOs are hybrid (boot BIOS *and* UEFI), so no Rufus/UNetbootin needed.

### 2. Install Ubuntu (the SATA dance)
1. Boot the M715q, mash **F12** for the boot menu → pick the USB stick.
2. **Disable/unplug the SATA drive first** (BIOS or pop it out) so the installer targets the NVMe cleanly.
3. Install **Ubuntu Server 24.04 LTS** to the NVMe (use whole disk, let it set up UEFI/GRUB).
4. Reboot, confirm it boots from NVMe alone.
5. Re-enable SATA → set boot order NVMe-first. Wipe old SUSE off the SATA later (or keep it as scratch).

### 3. Install llama.cpp (on each box)
```bash
./03-install-llama.cpp.sh
```

### 4. Pull a model + serve
```bash
./04-pull-model.sh
```
Serves an OpenAI-compatible API at `http://<ip>:8080/v1`.

### 5. Network + identity (run on each box, with the right hostname)
```bash
HOSTNAME=miles  ./05-network.sh     # garage box
HOSTNAME=mortimer ./05-network.sh   # bedroom box
```
Sets hostname, SSH keys, optional static IP, and installs Tailscale so:
- `miles` ↔ `mortimer` (counterpart, direct)
- `miles` ↔ Miles VPS, `mortimer` ↔ Mortimer VPS (respective VPS)
- SSH into any node from anywhere via its tailnet name.

After running, join the VPSes to the same tailnet too (`tailscale up` on each VPS).

**Naming convention (keep clean):** `.lan` / tailnet name = physical home box, `.cloud` = VPS.

## Model sizing (32GB RAM, CPU inference)
| Model | Quant | Speed (approx) | Notes |
|-------|-------|----------------|-------|
| Qwen2.5 / Llama-3.1 **7-8B** | Q4_K_M | ~4-6 tok/s | Daily driver |
| Qwen2.5 **14B** | Q4_K_M | ~2-4 tok/s | Slower, higher quality |
| 30B+ | — | too slow | Only via RPC split (see below) |

## Keep them identical
Same OS, same llama.cpp commit, same build flags, same models, same launch
command. Pin a `setup.sh` in git/workspace so drift doesn't creep in.

## Later: cluster (optional, currently NOT doing this)
llama.cpp's RPC backend can split one big model across both boxes' RAM (64GB total),
but over 1GbE the interconnect bottlenecks it to slower-than-single-box speed.
Only worth revisiting if you specifically need a 30B+ model.
