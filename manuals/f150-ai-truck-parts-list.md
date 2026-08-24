# 1977 Ford F150 — Researched Parts List (real SKUs)
*Compiled by Miles + Beets — 2026-08-24. Prices are current market ranges; confirm at checkout. "VERIFIED" = model confirmed on a manufacturer/retailer page; "est." = market estimate.*

---

## ⚠️ First: confirm your engine
The only spec-sensitive parts are the **cap/rotor + Pertronix kit**. A '77 F150 is either a **300ci inline-6 (4.9L)** or **302ci V8 (5.0L)**. Check the **8th digit of the VIN** or the block casting before ordering those two. Everything else is near-identical across both engines.

---

## 1. MECHANICAL — reliable starting

| Item | Model / SKU | Price | Source |
|---|---|---|---|
| Electronic ignition kit | Pertronix Ignitor (Ford 300 I6 or 302 V8) | ~$90–130 | ebay.com / pertronixbrands.com |
| Ignition coil | Pertronix Flame-Thrower | ~$40–55 | ebay.com |
| Distributor cap + rotor | Motorcraft (300 vs 302 — engine-specific) | ~$25–40 | rockauto.com |
| Carburetor rebuild kit | Motorcraft 2-bbl / Holley | ~$30–60 | ebay.com / rockauto.com |
| Starter motor (3-bolt, 300 or 302) | DB Electrical SDN14 / ACDelco 322-2657 | ~$50–90 | ebay.com (DB Electrical) |
| Alternator ~100A (Ford 3G upgrade) | Tuff Stuff 7114-100 / Powermaster 8001 | ~$180–250 | summitracing.com |
| Battery — Group 65 AGM (main) | Optima RedTop 8065-167 / Odyssey 65-PC1750 | ~$260 (Optima) / ~$360 (Odyssey) | optimabatteries.com |
| Mechanical fuel pump (300/302, 5/16") | Carter M61013 / Airtex E8012S | ~$30–45 | rockauto.com |
| Spark plugs | NGK XR4 (7712) / Motorcraft ASF-22C | ~$3–5 ea | rockauto.com |
| Plug wire set | Motorcraft WR-3160 / MSD 32829 | ~$40–70 | summitracing.com |
| Battery cable + ground kit (2/0) | JEGS 10612 | ~$30–60 | jegs.com |

**Mechanical subtotal: ~$720–1,175**

---

## 2. SECONDARY BATTERY + POWER (never stranded + solar)

| Item | Model / SKU | Price | Source |
|---|---|---|---|
| LiFePO4 12V 50Ah battery | **Renogy RBT1250LFP** (VERIFIED) | ~$135–169 | renogy.com |
| DC-DC charger + solar (one box — isolates aux battery + charges from alt & panel) | **Renogy RBC2125DS** (VERIFIED, DCC50S successor) | ~$349–379 | renogy.com |
| └ cheaper split option | Victron Orion-Tr 12/12-18 (2915) | ~$180–200 | victronenergy.com |
| 100W rigid mono solar panel | **Renogy RNG-100D-US** (VERIFIED) | ~$85–125 | renogy.com |
| MPPT charge controller (if Victron route) | Victron SmartSolar MPPT 75/15 (SCC110050060) | ~$135–155 | victronenergy.com |
| Manual battery selector switch | Blue Sea 9001e (mini, 300A) | ~$35–48 | bluesea.com/products/9001e |
| Battery monitor | Victron SmartShunt SCS000500000 / budget Renogy RBM500 (VERIFIED) | ~$160–185 / $59–69 | victronenergy.com |

**Power subtotal: ~$620–1,010**

> **Note:** the Renogy RBC2125DS does double duty (isolator + solar MPPT in one box), so you can skip the separate Victron 75/15 if you go Renogy. For a Pi 5 (~12W), a 50Ah LiFePO4 = 24+ hrs runtime; 100W solar recharges it in ~1 good sun-day.

---

## 3. AI BRAIN + CONNECTIVITY

| Item | Model / SKU | Price | Source |
|---|---|---|---|
| Raspberry Pi 5 (8GB) | Adafruit #5813 (VERIFIED $80) | $80 | adafruit.com/product/5813 |
| Active cooler + case | Pi 5 Active Cooler + Official Case | ~$35–45 | raspberrypi.com |
| NVMe hat + 256GB SSD | Pimoroni NVMe Base + Crucial P3 Plus 250GB | ~$18 + $20–25 | shop.pimoroni.com |
| USB microphone | Samson Go Mic / Fifine K669 | ~$15–40 | amazon.com |
| Speaker + amp | PAM8403 / TDA7297 board + 3–4" speaker | ~$10–20 | amazon.com |
| 5G LTE router | **GL.iNet Spitz AX GL-X3000** (VERIFIED, dual-SIM 5G + Wi-Fi 6) | ~$330–380 | gl-inet.com/products/gl-x3000/ |
| └ alt (2× price) | Teltonika RUTX50 | ~$600 | teltonika.com |
| Mag-mount LTE antenna | 15 dBi SMA (Taoglas / AONIOE) | ~$20–35 | amazon.com |

**AI + connectivity subtotal: ~$510–625**

---

## 4. SENSORS + CONTROL

| Item | Model / SKU | Price | Source |
|---|---|---|---|
| ESP32 dev board | ESP32-WROOM-32 / DOIT DevKit V1 | ~$10–15 | amazon.com |
| 12V relay module (8ch) | Songle SRD-05VDC, optocoupled | ~$8–15 | amazon.com |
| Remote start (2-way, 4000ft) | **Viper 4105V** | ~$55–70 | amazon.com |
| Temp sensors | DS18B20 waterproof probe (3–5 pack) | ~$8–12 | amazon.com |

**Sensors + control subtotal: ~$80–115**

---

## GRAND TOTAL

| Category | Cost |
|---|---|
| Mechanical | ~$720–1,175 |
| Power + solar | ~$620–1,010 |
| AI brain + connectivity | ~$510–625 |
| Sensors + control | ~$80–115 |
| **TOTAL** | **~$1,930–2,925** *(before shipping/tax)* |

---

## What Beets flags as the highest-value buys

1. **Pertronix kit + coil** — one box fixes most "cranks but won't fire" on a 40-year-old rig. The single best $130 you'll spend.
2. **Renogy RBC2125DS DC-DC charger** — your "never stranded" secondary battery done right (isolator + solar in one).
3. **Group 65 AGM main battery** — the foundation everything runs off.

Everything else layers the Pi brain on top.

---

## One honest caveat

eBay listings churn fast, so some of these are model numbers verified on manufacturer/retailer pages rather than a specific live eBay auction. Prices marked "est." are honest market ranges. When you're ready to buy, paste the model/SKU into eBay search and sort by price — that'll surface the current cheapest listing.

*Next step if you want it: I'll draft the wiring diagram (alternator → isolator/DC-DC → LiFePO4 + solar → Pi 5 + ESP32 → sensors/relay), so you have the full schematic before you order anything.*
