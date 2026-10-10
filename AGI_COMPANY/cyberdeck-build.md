# Cyberdeck Build — two M715q + router in a DeWalt case

*Portable two-node compute rig. The homelab plan (Omarchy + Tailscale + Pi agents) stays the same — this adds the case + power + cooling so it's a rugged, battery-powered cyberdeck.*

---

## The vision

Two Lenovo ThinkCentre M715q Gen 1 (10M3) Tinies + a BEFR1154 router, mounted in a **DeWalt drill box** (T-STAK or ToughSystem case), powered off **DeWalt 20V batteries** so it runs untethered. A portable compute cluster / cyberdeck.

---

## Power budget

| Component | Peak | Idle |
|---|---|---|
| M715q #1 | ~65 W | ~20 W |
| M715q #2 | ~65 W | ~20 W |
| Router | ~12 W | ~12 W |
| **Total** | **~142 W** | **~52 W** |

**Runtime on DeWalt 20V batteries:**
- 5 Ah ≈ 90 Wh → ~1.5–2 h idle, ~40 min full tilt
- Two batteries hot-swapped = a real untethered rig

---

## The power wiring (the key trick)

The M715q runs on a **20V DC input via a Lenovo slim-tip (rectangular) connector** — *not* a standard 5.5 mm barrel. DeWalt 20V MAX batteries are ~20V nominal (18V under load), so the voltage matches directly. No buck/boost needed for the Tinies.

**Wiring:**
```
DeWalt 20V battery → DeWalt battery adapter (bare leads) → split to 2× Lenovo slim-tip 20V
```
- **DeWalt 20V battery adapter** (battery clip → pigtail leads) — cheap, ubiquitous ("DeWalt 20V power adapter")
- **2× Lenovo slim-tip 20V DC cables** — splice onto the adapter leads (or buy "Lenovo 20V slim tip cable")
- Optionally a **20V → 12V buck converter** for the router, if the BEFR1154 is 12V (verify the router's adapter voltage first)

⚠️ **The M715q pulls up to 65W each** — make sure the DeWalt battery adapter + leads are rated for the current (a 5Ah 20V pack can do it; check the adapter's wire gauge).

---

## Cooling (non-negotiable)

Two Tinies in a sealed plastic case will **cook**. Plan for airflow:
- **2× 80 mm (or 40 mm) 12V fans** — one intake, one exhaust, cut into the case
- Power the fans off the 20V line via a **buck converter (20V → 12V)** or a small 12V fan controller
- Cut **vent grilles** + a dust filter mesh over the intake

---

## Full parts list (merge with the Aug 24 homelab plan)

### Core (from the existing homelab plan — re-confirm)
| Qty | Item |
|---|---|
| 4 | 16 GB DDR4-2666 SODIMM (as two matched 2×16GB kits) |
| 1 | Arctic MX-4 / Noctua NT-H1 thermal paste (4g) |
| 1 | DisplayPort → HDMI cable |
| 2 | Netac NS100 128GB SATA SSD (already have) |

### Cyberdeck additions (new)
| Qty | Item | Notes |
|---|---|---|
| 1 | DeWalt drill case (T-STAK / ToughSystem) | the enclosure |
| 1 | DeWalt 20V MAX battery (5Ah) | or two for hot-swap |
| 1 | DeWalt 20V battery adapter (→ bare leads) | powers the rig |
| 2 | Lenovo slim-tip 20V DC cable | splice onto the adapter leads |
| 1 | Buck converter 20V → 12V | for the router + fans (if router is 12V) |
| 2 | 80 mm 12V fan | intake + exhaust |
| — | vent grilles + dust mesh | cut into the case |
| — | M2.5 / M3 standoffs + screws | mount the Tinies + router to a board |

---

## Build steps

1. **Prep the case** — mount a backer board (plywood/acrylic), drill standoff holes for the two Tinies + router, cut fan vents.
2. **Mount hardware** — screw the Tinies + router to the board, fans at intake/exhaust.
3. **Wire power** — DeWalt adapter → leads → split to 2× Lenovo slim-tip → Tinies; buck converter → 12V rail for router + fans.
4. **Wire networking** — BEFR1154 LAN ports → each Tiny; (or run Tailscale and skip the physical switch).
5. **Install OS** — per the Omarchy plan (disable Secure Boot/TPM, flash ISO, no-encryption install, hostnames m715q-1 / m715q-2).
6. **Tailscale** — mesh the two nodes, confirm `tailscale ping` across.
7. **Pi agents** — install on each node, point at task queues.

---

## Open questions to verify before ordering
1. **BEFR1154 model + voltage** — is it 12V or 5V? (Decides the buck converter.) If it's actually a *different* router model, re-check.
2. **Lenovo connector tip** — confirm it's the slim-tip (rectangular), not the older yellow barrel, before buying the DC cables.
3. **M715q power draw under load** — 65W is the adapter rating; real load is lower, but size the leads for the worst case.

---

## Pre-install refinements (from a second review — all good)

1. **BIOS update** — flash the latest Lenovo BIOS for the M715q Gen 1 (v M1AKTxxA) *before* installing Omarchy; improves stability with 32 GB RAM kits.
2. **Fan curve** — in BIOS, set "Smart Cooling" to **Performance** (keeps the Ryzen GE APUs cooler under sustained load — matters in a sealed case).
3. **Power profile** — disable **ErP** and **Deep Sleep** so the nodes stay reachable over Tailscale even after idle.
4. **SSD alignment** — after install, run `lsblk -o NAME,ALIGNMENT`; Netac drives sometimes ship misaligned, and a quick `fdisk` re-create fixes it.

---

## Startup automation (systemd + health check)

So each node auto-registers its Pi agent on boot and reports status. See `cyberdeck-agent-startup.md` for the full systemd unit + health-check script.

*This + the muscle + the face = a busy workbench, Captain. But a good kind of busy.*
