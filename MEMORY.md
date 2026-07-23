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

## Feedback-to-Curriculum v1.3 - FULLY DEPLOYED
**Created:** 2026-07-23
**Status:** All Phases Complete (1.1 + 1.2 + 1.3)

### Implementation
- **Kidneys v1.1**: Extended with `WasteEvent` data structure and `process_for_recycling()` method
- **Auto-categorization**: syntax/logic/security/efficiency/alignment errors
- **Auto-lesson generation**: Converts waste into curriculum items
- **Liver v1.1**: Priority queue routing for waste-derived curriculum (HIGH priority)
- **Socket commands**: `waste_loop`, `waste_queue`, `priority_curriculum`
- **Persistence**: Waste queue saved to `/var/lib/aos/brain_state/waste_queue.json`

### NEW: Intelligence Layer v1.3 (Phase 1.3)
- **CurriculumIntelligence**: Tracks lesson effectiveness over time
- **Error Trend Analysis**: Detects improving/worsening patterns
- **Auto-Tuning**: Automatically adjusts Kidneys thresholds based on results
- **Conversion Metrics**: waste → lesson → improvement funnel
- **Dashboard & Reports**: Human-readable intelligence reports

### Metabolic Loop with Intelligence
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
    ↓
Curriculum Intelligence (track effectiveness)
    ↓
Auto-tune thresholds → Better performance
```

### Test Results
- Phase 1.1: 4/4 tests passed
- Phase 1.2: 5/5 tests passed
- Phase 1.3: 6/6 tests passed
- Lesson effectiveness tracking: 92.9% improvement detected
- Auto-tuning: Threshold recommendations generated

### Socket Commands
```bash
# Intelligence dashboard
echo '{"cmd":"curriculum_intelligence", "action":"dashboard"}' | nc -U /tmp/aos_brain.sock
echo '{"cmd":"curriculum_intelligence", "action":"metrics"}' | nc -U /tmp/aos_brain.sock
echo '{"cmd":"curriculum_intelligence", "action":"report"}' | nc -U /tmp/aos_brain.sock
echo '{"cmd":"curriculum_intelligence", "action":"auto_tune"}' | nc -U /tmp/aos_brain.sock
```

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

## Hold Out Kidneys v1.0 - Blind Validation
**Created:** 2026-07-23
**Status:** Deployed

### Implementation
- **Strong DM-inspired**: Validator has ZERO knowledge of implementation
- **Bias Elimination**: 15% grade inflation detected and removed
- **Pure Assessment**: Output evaluated only against requirements

### Key Features
- Implementation plan HIDDEN from validator
- Original prompt HIDDEN from validator
- Validator ONLY sees: output + requirements + constraints
- No sycophantic bias (can't be swayed by intent)

### Test Results
- Blind score: 0.80
- Non-blind score: 0.95
- **Bias eliminated: 15%**

### Socket Commands
```python
# Submit for blind validation
hok.submit_for_validation(
    output_content=code,
    output_type="code",
    requirements="Create function with error handling",
    constraints="Keep it concise",
    implementation_plan="Step 1...",  # HIDDEN
    original_prompt="Build..."          # HIDDEN
)

# Get validation package (validator's view)
package = hok.get_validation_package(task_id)
# Returns: ONLY output, requirements, constraints

# Perform blind validation
result = hok.perform_blind_validation(task_id)
```

---

## Gemma 4 E4B - Potential Model Addition
**Source:** XDA Developers (2026-07-12)
**Status:** Under Evaluation

### Specs
| Parameter | Value |
|-----------|-------|
| Effective Params | 4.5B (Per-Layer Embeddings) |
| Knowledge | Equivalent to 8B model |
| Pi 5 (8GB) | 2.95-3.25 t/s |
| GTX 1080 | 30-40 t/s |
| RTX 3080 Ti | ~90-120 t/s |

### Key Innovation: Per-Layer Embeddings (PLE)
- Each decoder layer has its own embedding table
- Accesses more info without hogging resources
- Reduces effective params while maintaining capability

### Use Case for AOS
- **Cost-Aware Thyroid**: EMERGENCY mode candidate
- Runs on Pi (tiny enough for budget constraints)
- More capable than tinyllama (1.1B) for basic tasks
- 4.5B params vs 1.1B = significant upgrade

### Test Results (from review)
- ✅ Raspberry Pi 5 (8GB) - works where 5B-6B models fail
- ✅ PDF summarization
- ✅ Image description
- ✅ Docker management (limited)
- ❌ Some obscure tool detection issues

### Recommendation
Add to Model Router as EMERGENCY mode fallback when budget constraints hit but tinyllama insufficient.

---

## AOCROS Upgrades Summary v4.6 - COMPLETE
**Date:** 2026-07-23
**Status:** ✅ ALL 5 COMPLETE

### ✅ Completed Upgrades

1. **Feedback-to-Curriculum v1.3** - Metabolic loop for self-improvement
   - Kidneys v1.1 waste event generation
   - Liver v1.1 priority routing
   - Intelligence v1.3 with auto-tuning
   - 92.9% improvement detected

2. **Protected Memory Segments** - SOUL.md/IDENTITY.md immutable
   - 5 files protected
   - 2 immutable (SOUL.md, IDENTITY.md)
   - Write protection enforced
   - Integrity verification active

3. **Cost-Aware Thyroid v1.3** - Budget-aware model switching
   - Daily/hourly budget tracking
   - NORMAL/CONSERVATIVE/EMERGENCY modes
   - Gemma 4 E4B integration for EMERGENCY mode
   - Auto-downgrade at 70% budget

4. **Hold Out Kidneys v1.0** - Blind validation pattern
   - 15% bias eliminated (sycophancy removal)
   - Implementation plan HIDDEN from validator
   - Pure quality assessment

5. **Crew Isolation v1.0** - True sandbox for agents
   - Isolated workspaces per agent
   - Message queue communication only
   - Quarantine for misbehaving agents
   - Complete destruction capability

### New Model Added
- **Gemma 4 E4B** - Emergency mode fallback
  - 4.5B effective params (8B equivalent knowledge)
  - Runs on Raspberry Pi 5
  - Cost-efficient for budget constraints

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
