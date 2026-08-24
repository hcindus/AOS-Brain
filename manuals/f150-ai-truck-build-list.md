# 1977 F150 — "AI in the Truck" Priced Build List
*Prepared by Miles for the Captain — 2026-08-24*

## ⚠️ About these prices
Amazon/retailer pages block automated price checks, so these are **real model numbers with honest market ranges** (not live-scraped). Treat every price as "verify at checkout" — they drift a few dollars week to week. Where it matters I gave you the exact search term to paste into Amazon.

---

## YOUR GOAL, CLARIFIED: Secondary battery (jump-start reserve)

You mentioned the secondary battery is really about *not getting stranded* — a reserve you can use to jump/charge the main battery when you're out somewhere. That's a **dual-battery / jump-start setup**, and it's actually *simpler and cheaper* than the full "AI house battery" I first spec'd. Here's how they connect:

- **Secondary battery (AGM, deep-cycle)** — charges off the alternator while you drive via an **isolator** (so the AI/accessories never drain the starter battery).
- When the main battery dies out in the field, you **jump the truck off the secondary battery** — no cables-from-a-stranger needed.
- The **solar panel** then tops off *both* batteries when parked, which is your "self-sustaining" piece.

So your instinct and the AI project share one battery system. Good news: one set of purchases covers both.

---

## LAYER 1 — Mechanical: "starts every time"

| Item | Model / SKU (search term) | Price |
|---|---|---|
| Electronic ignition (kills the "work-it-to-start" points problem) | **Pertronix Ignitor** (or 1481 Ignitor II) for 300 I6 / 302 V8 | $90–130 |
| Ignition coil | Pertronix Flame-Thrower coil | $40–55 |
| Distributor cap + rotor | Motorcraft / ACDelco for your engine | $25–40 |
| Carburetor rebuild kit | Holley or Motorcraft rebuild kit | $30–60 |
| Starter motor | Reman, e.g. ACDelco or Duralast | $70–140 |
| Alternator (100A+ upgrade) | ACDelco / Duralast Gold | $120–180 |
| Battery — Group 65 AGM | Odyssey 65-PC1750 or Optima RedTop | $220–320 |
| Fuel pump (mechanical) | Carter / Airtex | $30–50 |
| Fuel filter | inline, $10 | $10 |
| Tune-up kit (plugs, wires, belts, hoses) | Motorcraft / NGK | $60–120 |
| Battery cables + ground straps | 2/0 or 4 AWG kit | $40–70 |

**Layer 1 subtotal: ~$735–1,175**

> The hard-start fix is almost entirely the Pertronix + carb kit + fresh grounds. If you only buy three things, buy those.

---

## LAYER 1b — Welding gear (body holes)

| Item | Model / SKU | Price |
|---|---|---|
| MIG welder (110V) | **Hobart Handler 140** or **Lincoln Electric PowerMIG 140** | $550–750 |
| C25 gas + regulator | (rent or buy; 20–40 cf tank) | $150–250 (tank) |
| Auto-darkening helmet | Lincoln / YESWELDER | $40–90 |
| Welding gloves + jacket | any | $30–60 |
| 4.5" angle grinder | DeWalt / Makita | $60–90 |
| Cutting/grinding/flap discs | pack | $20–35 |
| Patch panels / sheet steel | 18–20 ga | $40–100 |
| Rust converter | **POR-15** kit | $30–50 |

**Layer 1b subtotal: ~$920–1,425** (or ~$200–400 if you hire the welder and only buy grinder + panels + POR-15)

---

## LAYER 2 — Sensors + remote start (nervous system)

| Item | Model / SKU | Price |
|---|---|---|
| ESP32 dev board | ESP32-WROOM-32 | $10–15 |
| Relay board (for ignition/starter control) | 4/8-ch 12V relay module | $12–20 |
| Voltage sensor | INA219 or voltage divider | $8–12 |
| Temp sensors | DS18B20 (coolant + cabin) | $10–15 |
| Fuel-level / oil-pressure tap | (reuse stock senders) | $0–20 |
| Remote-start module (universal 12V) | Crimestopper / Viper 4105V | $60–120 |
| Door/hood/tilt sensors | reed + tilt switch | $10–20 |
| 12V→5V buck converter | LM2596 | $8 |

**Layer 2 subtotal: ~$120–210**

---

## LAYER 3 — Power (solar + secondary battery = your goal)

| Item | Model / SKU | Price |
|---|---|---|
| **Secondary battery — 12V LiFePO4 50Ah** | Renogy / LiTime / Redodo 50Ah | $180–260 |
| **Battery isolator / DC-DC charger** | Renogy DCC50S or Victron Orion-Tr 12/12-18 | $150–220 |
| **Solar panel 100W** | Renogy 100W rigid (or flexible) | $90–130 |
| **MPPT charge controller** | Victron SmartSolar 75/15 | $100–120 |
| Fuse block + inline fuses | Blue Sea 6-circuit | $40–60 |
| Battery monitor/shunt | Victron SmartShunt | $130–150 |
| Wiring (marine tinned + heat shrink) | assorted | $50–80 |
| **Jump cable / self-jump switch** | (manual battery switch, e.g. Blue Sea 9001e) | $35–60 |

**Layer 3 subtotal: ~$775–1,080**

> This layer IS your "secondary battery so I never get stranded." The solar + LiFePO4 + isolator + a manual battery switch gives you exactly the jump-start reserve you wanted, plus it runs the AI. One system, two wins.

---

## LAYER 4 — Connectivity (signal)

| Item | Model / SKU | Price |
|---|---|---|
| Cellular router | **GL.iNet Spitz AX (GL-X3000)** or Teltonika RUTX50 | $150–300 |
| Data-only SIM | prepaid (T-Mobile/Visible/etc.) | $10–30/mo |
| High-gain LTE antenna (mag roof) | Proxicast / Bingfu | $20–40 |
| GPS module | (built into many routers; else u-blox NEO-6M) | $0–15 |
| *(optional)* Starlink Mini | Starlink Mini kit | $599 + $50/mo |

**Layer 4 subtotal: ~$170–355** (+Starlink if desired)

---

## LAYER 5 — AI Brain

### Option A — Raspberry Pi 5 (recommended: voice + telemetry + remote control)

| Item | Model / SKU | Price |
|---|---|---|
| Raspberry Pi 5 (8GB) | Pi 5 8GB | $80 |
| Case + cooling | active cooler + case | $20–30 |
| NVMe hat + 256GB NVMe | Pimoroni NVMe Base + drive | $50–70 |
| USB mic | (any) | $15–25 |
| Speaker + small amp | USB or 2×5W amp | $15–30 |
| Camera (optional, for vision) | Pi Camera Module 3 | $30–40 |

**Option A subtotal: ~$210–275**

### Option B — Jetson Orin Nano (real local LLM / offline vision)

| Item | Model / SKU | Price |
|---|---|---|
| Jetson Orin Nano Dev Kit (8GB) | NVIDIA | $250 |
| NVMe SSD 512GB | Samsung/Crucial | $45–60 |
| USB mic + speaker + camera | (as above) | $60–95 |

**Option B subtotal: ~$355–405**

---

## LAYER 6 — Enclosure & wiring

| Item | Model / SKU | Price |
|---|---|---|
| Weatherproof enclosure | NEMA box / sealed ammo can | $30–50 |
| 12V fan + vent | (any) | $15–25 |
| Distribution + relays + terminals | assorted | $40–70 |
| Marine-grade wiring + connectors | assorted | $40–60 |

**Layer 6 subtotal: ~$125–205**

---

## GRAND TOTAL (with your dual-battery setup, Pi 5 brain, no Starlink)

| Layer | Cost |
|---|---|
| 1 — Mechanical | $735–1,175 |
| 1b — Welding | $920–1,425 |
| 2 — Sensors + remote start | $120–210 |
| 3 — Power (solar + secondary battery) | $775–1,080 |
| 4 — Connectivity | $170–355 |
| 5 — AI brain (Pi 5) | $210–275 |
| 6 — Enclosure/wiring | $125–205 |
| **TOTAL** | **~$3,055–4,725** |

*(If you hire the welder instead of buying one, subtract ~$500–700 → **~$2,550–4,000**.)*

---

## What I'd actually buy first (priority order)

1. **Pertronix Ignitor + carb rebuild kit + new grounds** (~$150) — fixes the "work it to start" problem. Do this weekend.
2. **Secondary LiFePO4 battery + isolator + manual switch** (~$400) — your never-stranded jump-start goal, done right.
3. **100W solar + MPPT** (~$220) — makes the secondary battery self-sustaining.
4. **Raspberry Pi 5 + mic + speaker** (~$150) — the AI brain.
5. **Cellular router + SIM** (~$200) — gives it signal.
6. **Welder + grinder + panels** — tackle the holes whenever you're ready (this is independent).

---

## My honest take

Your **secondary-battery instinct is the backbone of the whole build** — it's the jump-start reserve you wanted *and* the power source for the AI. Buy that first after the mechanical fix, and everything else hangs off it.

The only open question left: **Pi 5 vs Jetson**, and **Starlink or cellular**. Once you lock those two, I can write the exact Amazon cart links and a phase-by-phase wiring checklist.

*Want me to draft that wiring diagram (how the isolator + solar + house battery + ESP32 + Pi all connect) as a next step?*
