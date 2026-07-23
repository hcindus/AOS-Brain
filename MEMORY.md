# MEMORY.md - Curated Knowledge

## Game Creation Skill v1.0
**Created:** 2026-04-07
**Location:** `/root/.openclaw/workspace/skills/game-creator/SKILL.md`

### Capability
I can now create browser-based 3D games using Three.js with:
- Procedural voxel universe generation
- Real physics (gravity, orbits)
- Multi-platform controls (keyboard/mouse/touch)
- Spatial audio
- Canvas HUDs and mini-maps

### First Creation
**N'og nog: Universal Explorer** (2026-04-07)
- Deployed to myl0nr0s.cloud/nog & tappylewis.cloud/nog
- 100x100x100 voxel universe with 6 universe types
- GitHub: hcindus/AOS-Brain/nognog/
- Tech: Three.js r128, Simplex Noise, Web Audio API

### Architecture Pattern
```
game/
├── index.html, nognog-pro.html
├── css/styles.css
├── js/{core,universe,player,render}/
└── assets/audio/
```

---

## Quick Reference

### Brain Status Commands
```bash
# Full brain status
echo '{"cmd":"status"}' | nc -U /tmp/aos_brain.sock

# Service status
systemctl status aos-brain-v4
systemctl status aos-mission-control
```

### Keepalive Scripts
- `/root/.openclaw/workspace/scripts/agent_keepalive.sh`
- `/root/.openclaw/workspace/scripts/aos_keepalive.sh`
- `/root/.openclaw/workspace/scripts/minecraft_keepalive.sh`

### Deployed Systems
- Mission Control v2.1 (port 8080)
- Complete Brain v4.4 (Liver + Kidneys + Thyroid)
- N'og nog game (myl0nr0s.cloud/nog)
- Roblox Bridge
- Minecraft Server + 4 Mineflayer agents

---

## Capton Pouring Systems Pages
**Created:** 2026-07-21
**Status:** DEPLOYED

### Category Page
- **URL:** `https://psdepot.com/products/capton-pouring-systems.html`
- **Description:** Main landing page for Capton beverage portion control systems

### Product Pages Created
| Product | SKU | Price | URL |
|---------|-----|-------|-----|
| Capton 1 oz Bottle Top Pourer | CAP-100-1OZ | $24.99 | `/products/capton-1oz-pourer.html` |
| Capton 1.5 oz Bottle Top Pourer | CAP-150-15OZ | $24.99 | `/products/capton-1.5oz-pourer.html` |
| Capton 2 oz Bottle Top Pourer | CAP-200-2OZ | $26.99 | `/products/capton-2oz-pourer.html` |
| Capton Wine Pourer (5 oz) | CAP-WINE-5OZ | $29.99 | `/products/capton-wine-pourer.html` |
| Capton Variety Pack (12-Pack) | CAP-VARY-12PK | $279.99 | `/products/capton-variety-pack.html` |
| Capton Pourer Cleaning Kit | CAP-CLEAN-KIT | $34.99 | `/products/capton-cleaning-kit.html` |

### Features
- Schema.org Product markup on all pages
- Responsive design matching existing PSD template
- SEO optimized with proper meta tags
- Linked from `/products/index.html` in categories

---

## Feedback-to-Curriculum v1.1 - DEPLOYED
**Created:** 2026-07-23
**Status:** Phase 1.1 + 1.2 Complete

### Implementation
- **Kidneys v1.1**: Extended with `WasteEvent` data structure and `process_for_recycling()` method
- **Auto-categorization**: syntax/logic/security/efficiency/alignment errors
- **Auto-lesson generation**: Converts waste into curriculum items
- **Liver v1.1**: Priority queue routing for waste-derived curriculum (HIGH priority)
- **Socket commands**: `waste_loop`, `waste_queue`, `priority_curriculum`
- **Persistence**: Waste queue saved to `/var/lib/aos/brain_state/waste_queue.json`

### Metabolic Loop
```
Brain Output → Kidneys (process_for_recycling)
    ↓
    REABSORB/EXCRETE detected
    ↓
WasteEvent created → Queued for curriculum
    ↓
Curriculum Feeder (ingest_from_waste)
    ↓
Priority curriculum item → Brain (next tick)
```

### Test Results
- All 4 test scenarios passed
- Waste events generating correctly (REABSORB mode)
- Curriculum conversion working with priority boosting
- Deduplication preventing duplicate lessons

---

## Performance Supply Depot SOPs v1.0
**Created:** 2026-07-23
**Status:** Ready for Review
**Location:** `/root/.openclaw/workspace/psd/sops/`

### SOPs Created
1. **SOP-001: Lead Response & Qualification**
   - Target: 5-minute response, 40%+ conversion
   - Lead scoring (Hot/Warm/Cold)
   - Ghosted lead recovery sequence

2. **SOP-002: Quote Generation & Follow-Up**
   - Target: 2-hour turnaround, 35%+ close rate
   - Pricing rules and discounts
   - 30-day follow-up sequence

3. **SOP-003: Order Status & Customer Inquiry**
   - Target: 60-second response, 80%+ first-contact resolution
   - Status definitions and scripts
   - **Highest automation potential**

### Implementation Package
- 4-week rollout timeline
- Daily metrics tracking sheet
- Risk mitigation plan
- Real-world test results (4/4 passed per SOP)
- Automation notes for AI agent deployment

---

*Last Updated: 2026-07-23

---

## N'og nog Crew Expansion v1.0
**Deployed:** 2026-04-07 08:24 UTC
**Location:** `/root/.openclaw/workspace/nognog/crew-lite.js`

### Current Crew (Active)
| Name | Role | Level | Status |
|------|------|-------|--------|
| Vex | PILOT | Rookie | ACTIVE |
| Nyx | ENGINEER | Rookie | ACTIVE |
| Jax | SCIENTIST | Rookie | ACTIVE |
| Luna | COMBAT | Rookie | ACTIVE |
| Aria | MEDIC | Rookie | ACTIVE |

### Features
- ✅ **Persistence** - JSON storage in `/storage/crew/`
- ✅ **Tick System** - 30s automation, hourly reports
- ✅ **XP/Leveling** - 6 tiers: Rookie → Legend
- ✅ **Discovery System** - 1% chance per tick
- ✅ **Service** - `nognog-crew` systemd service running

### Coming Next
- 🔄 AOS Brain decision integration
- 🔄 Roblox/Minecraft bridge connections
- 🔄 Email/Telegram notifications
- 🔄 Photo handling from crew

---

## SendGrid Integration for DepotChaos ✅ DEPLOYED
**Deployed:** 2026-07-03
**Status:** ACTIVE (pending SENDGRID_API_KEY)

### What's New
- ✅ SendGrid sender module: `/datadepot/web/sendgrid_sender.py`
- ✅ FastAPI integration with rate limiting (15min between sends)
- ✅ Queue processor cron job: every 15 minutes
- ✅ API endpoint: `/api/sendgrid/status` for health checks
- ✅ 96 emails/day capacity (stays under SendGrid free limit)

### Configuration Required
Set the SendGrid API key:
```bash
# Add to environment
export SENDGRID_API_KEY=SG.xxxxxxx

# Or edit systemd service
systemctl edit depotchaos
# Add: Environment=SENDGRID_API_KEY=your_key_here
systemctl daemon-reload
systemctl restart depotchaos
```

### DNS Configuration (REQUIRED for deliverability)
Add these DNS records to psdepot.com in Hostinger:

| Type | Host | Value |
|------|------|-------|
| CNAME | em8873.psdepot.com | u109143135.wl136.sendgrid.net |
| CNAME | s1._domainkey.psdepot.com | s1.domainkey.u109143135.wl136.sendgrid.net |
| CNAME | s2._domainkey.psdepot.com | s2.domainkey.u109143135.wl136.sendgrid.net |
| TXT | _dmarc.psdepot.com | v=DMARC1; p=none |

### API Endpoints
```bash
# Check queue status
curl http://localhost:8082/api/queue | python3 -m json.tool

# Check SendGrid status
curl http://localhost:8082/api/sendgrid/status | python3 -m json.tool

# Send single email
curl -X POST http://localhost:8082/api/queue/{email_id}/send
```

### Files
- Sender: `/datadepot/web/sendgrid_sender.py`
- Cron: `/datadepot/cron/process_email_queue.py`
- Service: `/etc/systemd/system/depotchaos.service`

---
*Last Updated: 2026-06-11*
