# 1977 F150 — Wiring Diagram + Build Phases
*Finalized: Pi 5 brain + Starlink Mini connectivity. Miles + Beets — 2026-08-24.*

---

## MASTER WIRING DIAGRAM (ASCII)

```
                          [ SOLAR PANEL 100W ]
                                   │  (MC4 → controller PV input)
                                   ▼
┌─────────────────────────────────────────────────────────────┐
│              RENOGY RBC2125DS (DC-DC + Solar MPPT)          │
│  (single box: isolates aux battery, charges from alt + sun) │
└──────┬──────────────────┬───────────────────────────────────┘
       │                  │
       │ (B+ from alt)    │ (charge out to aux battery)
       ▼                  ▼
 ┌──────────┐      ┌──────────────────┐
 │ ALTERNATOR│      │ LiFePO4 50Ah     │  ◄── SECONDARY / HOUSE BATTERY
 │ (~100A 3G)│      │ (Renogy RBT1250) │      (your "never stranded" reserve)
 └────┬─────┘      └────────┬─────────┘
      │                     │
      ▼                     │ 12V DISTRIBUTION (fused)
 ┌──────────┐               │
 │ START     │               ├──► Starlink Mini (12V/DC or PoE adapter)
 │ BATTERY   │               ├──► Raspberry Pi 5 (via 12V→5V/3A buck)
 │ Group 65  │               ├──► Cellular? NO — Starlink replaces it
 │ AGM       │               ├──► ESP32 sensor hub (12V→5V buck)
 │ (main)    │               ├──► 12V relay board (ignition/starter control)
 └──────────┘               ├──► USB speaker amp + mic (5V)
                             ├──► Viper 4105V remote-start module
                             └──► (spare fused 12V for future)

  MANUAL BATTERY SWITCH (Blue Sea 9001e)
  ┌─────────────────────────────────────────────┐
  │  OFF | 1 (start) | 2 (aux) | BOTH (jump)    │
  └─────────────────────────────────────────────┘
        Position "BOTH" = self-jump: aux LiFePO4
        jumps the dead starter battery. ← your goal
```

### Key isolation rule (don't skip this)
The **RBC2125DS (or Orion-Tr)** sits between the alternator and the aux battery. That's what keeps the Pi/Starlink/solar from ever draining your **starter** battery. Without it, a dead aux battery = stranded. With it, the truck always starts and the aux always has juice.

### Jump-start procedure (your "never stranded" moment)
1. Flip manual switch to **BOTH**.
2. Crank — the LiFePO4 aux battery joins the starter battery.
3. Once running, flip back to **1 (start)** so the alternator recharges the main, and the DC-DC recharges the aux while you drive.

---

## PHASE-BY-PHASE BUILD CHECKLIST

### Phase 1 — Get it running (mechanical)
- [ ] Confirm engine (VIN 8th digit / block casting): 300 I6 or 302 V8
- [ ] Install Pertronix Ignitor + Flame-Thrower coil
- [ ] Rebuild/adjust carburetor
- [ ] New cap + rotor, plugs, wires
- [ ] Replace grounds + battery cables (2/0)
- [ ] New Group 65 AGM main battery
- [ ] (Optional) 3G 100A alternator upgrade
- ✅ *Goal: fires on first key, every time.*

### Phase 2 — Secondary battery + solar (never stranded)
- [ ] Mount LiFePO4 50Ah (under hood or in-cab, vented box)
- [ ] Install RBC2125DS DC-DC charger (alt in → aux out, solar in)
- [ ] Wire Blue Sea 9001e manual switch
- [ ] Mount 100W solar panel (roof rack or hood)
- [ ] Add fuse block + SmartShunt/RBM500 monitor
- ✅ *Goal: aux battery always charged, can self-jump the truck.*

### Phase 3 — AI brain (Pi 5)
- [ ] Pi 5 + active cooler + case + NVMe SSD
- [ ] USB mic + speaker amp
- [ ] 12V→5V/3A buck converter (clean power, no USB brownout)
- [ ] Install OS + voice assistant (see below)
- ✅ *Goal: truck talks to you, monitors battery/telemetry.*

### Phase 4 — Connectivity (Starlink Mini)
- [ ] Roof-mount Starlink Mini (clear sky view)
- [ ] Power via 12V (DC) — it can run straight off the aux battery
- [ ] Wire Starlink → Pi (Ethernet or Wi-Fi)
- ✅ *Goal: truck online anywhere, remote access from your phone.*

### Phase 5 — Sensors + remote start
- [ ] ESP32 + DS18B20 (coolant + cabin temp) + voltage sense
- [ ] 8ch relay board (ignition, starter, accessories)
- [ ] Viper 4105V remote start
- [ ] Door/hood/tilt sensors (security)
- ✅ *Goal: remote start + full telemetry + anti-theft.*

### Phase 6 — Enclosure + cleanup
- [ ] Weatherproof enclosure (sealed, vented, fan)
- [ ] Marine tinned wire + heat-shrink + fusing everywhere
- [ ] Label every wire + draw the final as-built
- ✅ *Goal: durable, weatherproof, documented.*

---

## SOFTWARE STACK (for the Pi 5)

| Layer | Choice |
|---|---|
| OS | Raspberry Pi OS Lite (headless, low power) |
| Voice assistant | Mycroft / Home Assistant / OpenAI-compatible local |
| Telemetry | Node-RED or Python + MQTT |
| Remote access | Starlink + Tailscale (free, encrypted) |
| Local AI (optional) | Ollama running a small model (but Pi 5 is limited — use cloud/Starlink for heavy lifting) |

> The Pi 5 + Starlink means you can lean on **cloud AI over the satellite link** rather than trying to run a big model locally. That keeps the power draw tiny.

---

## FINAL COST (Pi 5 + Starlink Mini)

| Category | Cost |
|---|---|
| Mechanical | ~$720–1,175 |
| Power + solar | ~$620–1,010 |
| Pi 5 brain | ~$210–275 |
| Starlink Mini | $599 + $50/mo |
| Sensors + control | ~$80–115 |
| Enclosure + wiring | ~$125–205 |
| **TOTAL** | **~$2,350–3,375** + $50/mo |

*(Hire the welding instead of buying a welder and it drops to ~$1,850–2,870.)*

---

## My recommendation on order

1. **Phase 1** first — a running truck is the whole point.
2. **Phase 2** second — the secondary battery is your "never stranded" goal, independent of the AI.
3. **Phase 3+4** together — Pi + Starlink turn it into an AI truck.
4. **Phase 5+6** last — polish, sensors, enclosure.

You can pause after Phase 2 and still have exactly what you asked for (reliable start + never stranded). Phases 3–6 are where the "AI" actually lives.
