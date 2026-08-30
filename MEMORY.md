# MEMORY.md - Curated Knowledge

## Vendor Outreach Authority (Captain, 2026-08-30)
**Phased email escalation — durable policy.**
- **Now active:** Miles may reach out to **vendors** on Captain's behalf, place orders as Captain shares them, and report back any vendor replies.
- **NOT yet:** **customers** — separate, later gate. Do NOT email customers until explicitly authorized.
- **Tooling:** `scripts/vendor_comms.py` (`check` / `send` / `orders` / `add-vendor`). Creds from `.env` (single source). Inbound watch = OpenClaw cron `agentTurn` every 15 min → announces new email to Captain on Telegram. State: `data/vendor_comms_state.json` (seen UIDs), `data/vendor_contacts.json` (vendor directory), `data/email_inbox/` (saved copies).
- **Existing vendor:** Labels Direct (Brandon Chilcoat) — trusted, "always fair." Respectful negotiation posture; don't squeeze a fair vendor. Matte LD46TTBOPP15PWI $446/case, gloss LD46TTGBOPP15PWI $420/case.

## Strategic Enrichment — Steve Jobs @ NeXT (Stanford GSB talk) — 2026-08-25
Captain shared transcript → distilled into North Star for AGI Company positioning.

**Core frame: management vs. operational productivity.** PCs/Macs only ever attacked *management* productivity (shrink-wrapped apps). Real moat + money = *operational* apps — custom mission-critical tools that ARE the product ("an idea, a sales force, and a custom app to bang on databases"). No app → no product. **This is literally our Dark Factory value prop: custom agents as the "custom app" that makes a client's product real.**

**Three pullable principles:**
1. **Software > hardware as durable moat** (hardware churns 18mo; software takes 8-9yrs to catch up). Our edge = agents/manifests/orchestration, not boxes.
2. **"20% of the code" = reusable objects.** NeXTSTEP won by writing ~20% of competitor code. Our skill library + Temporal + Hold-Out/Kidneys = same leverage. Don't re-plumb.
3. **Direct sales creates demand; channels only fulfill it.** Revolutionary product can't ride a channel that can't demo it. Ties to consultative, demo-first agent selling.

**Secondary notes:** "code you don't write is fastest/easiest to maintain"; technology windows ≈5yrs to open + 5yrs to exploit; JIT/manufacturing-as-software; policy-team consensus on ~25 truly-important decisions/yr.
*Full note: `memory/2026-08-25.md`*

## Temporal Dark Factory — LIVE (2026-08-18)
**Status:** ✅ DEPLOYED on Miles VPS (this host). Server + worker running.

### What's running
- **Temporal server** — Docker Compose at `/opt/temporal/docker-compose.yml` (postgres + auto-setup + UI)
  - gRPC `localhost:7233`, UI `http://localhost:8233`
  - Containers: `temporal`, `temporal-postgresql`, `temporal-ui` (`restart: unless-stopped`)
- **Worker** — systemd service `darkfactory-worker` (auto-restart + boot)
  - `/root/.openclaw/workspace/temporal/darkfactory/worker.py` (Python, venv `.venv`)
  - Task queue: `darkfactory-queue`
- **Pipeline (Level 3 autonomy):** validate SDK → allocate → build → verify → **blind hold-out validate** → notify, with a 30-min durable watchdog + escalation.

### Key fixes made
- `workflow.start_timer` / `cancel_timer` don't exist in temporalio 1.31 — replaced with durable `asyncio.wait_for` watchdog.
- Activity args are JSON-serialized to dicts at the boundary — `execute_build` made dict-safe.
- Hold-out scenarios use `artifact_present` (relative globs) so they work on any build output.

### CLI usage
```bash
cd /root/.openclaw/workspace/temporal/darkfactory && source .venv/bin/activate
export TEMPORAL_HOST=localhost:7233
python3 cli.py start CREAM --type web --source /root/.openclaw/workspace/Cream/web/ --wait
python3 cli.py list
```

### Level 5 (full autonomy) — added 2026-08-18
- **Auto-triage loop** — `triage_loop.py` scans `specs/inbox/*.json`, accepts/rejects vs mission.md, auto-submits to Temporal. Run every 30 min via `darkfactory-triage.timer`.
- **Blue-green deploy** — `deploy_blue_green` activity deploys to `/var/www/darkfactory-deploy/{project}/` with atomic `current` symlink flip.
- **The "console"** = drop a spec JSON into `specs/inbox/`. Everything else is autonomous.
- Full pipeline: validate → allocate → build → verify → blind hold-out → **blue-green deploy** → notify.
- Deployment docs + infra config: `temporal/darkfactory/DEPLOYMENT.md`, `deploy/` (docker-compose + systemd units).

### Dark Factory upgrades (RiP GoR Council directive)
- `AGI_COMPANY/subsidiaries/DARK_FACTORY/mission.md` — goals + non-goals + accept/reject triage
- `.../DARK_FACTORY/validation/hold_out_scenarios.{py,json}` — blind hold-out validator
- `.../DARK_FACTORY/factory.py` — back-ported `triage_order()` (accept/reject) + `run_qc()` (blind hold-out QC gate at phase 4→5)

### Temporal consolidation (2026-08-18)
One Temporal server (Miles VPS `localhost:7233`), all workflows on it:
- **Dark Factory** (Python) — `darkfactory-worker.service`, queue `darkfactory-queue`
- **Collections** (Go, compiled `collections-worker` binary) — `collections-worker.service`, queue `collections-queue`
- **DepotChaos MS-Connect** (Python) — available, not yet registered (its `depotchaos-tasks.service` is dead; CRM services are active but non-Temporal)
- **Mortimer sales engine** — deprecated (was a mock "Temporal-like" engine, not real Temporal)
- See `temporal/CONSOLIDATION.md` for full map.

---

## Partner Leads Portal (PSD × Chipp × WitzEnd) v1.0
**Created:** 2026-08-18
**Live URLs:**
- Portal: `https://psdepot.com/leads-portal/` (was `/chipp-portal/`)
- Dashboard: `https://psdepot.com/leads-dashboard/` (was `/chipp-dashboard/`)
- Old `chipp-*` URLs now 301-redirect to new names

### Architecture
- **Backend:** `chipp_leads_api.py` (FastAPI, port 8086) — JSON store at `/var/lib/psdepot/chipp_leads.json`
  - Service: `chipp-leads-api.service` (`/root/.openclaw/workspace/datadepot/web/chipp_leads_api.py`)
  - nginx: `/api/leads` → `127.0.0.1:8086/api/leads`
- **Frontend:** static HTML in `/var/www/psdepot.com/leads-portal/` + `leads-dashboard/`
- **Files:** `/var/www/psdepot.com/leads-portal/index.html`, `leads-dashboard/index.html`

### Three Destinations (routing partners)
| Destination | Key | Notify email | Accent |
|---|---|---|---|
| PSDepot | `psd` | info@psdepot.com | blue `#58a6ff` |
| Chipp | `chipp` | steven@chipp.cc | green `#3fb950` |
| WitzEnd Beverages | `witzend` | lisa@witzendbeverages.com | pink `#f778ba` |

### WitzEnd Beverages (new partner, 2026-08-18)
- Shopify mocktail brand: `witzendbeverages.com` (`7a7896-52.myshopify.com`)
- Contact: Lisa Ikeda — lisa@witzendbeverages.com
- 6 mocktail flavors: Hugo Spritz, The Maitai, The Mule, The Paloma, Ranch Water, Sea Breeze + Variety 12-Pack + merch
- Bay Area. Product list mapped in portal: Mocktails (Wholesale), 6 flavors, Variety 12-Pack, Merch/Apparel, Multiple/Not Sure

### Email notifications (on new lead only)
- Fires ONLY on `POST /api/leads` (new lead), never bulk sync/update
- Hostinger SMTP: `smtp.hostinger.com:587`, auth `miles@myl0nr0s.cloud` / pass in `workspace/.env` (`HOSTINGER_SMTP_PASS`)
- From: `Performance Supply Depot — Lead Portal <miles@myl0nr0s.cloud>`
- SendGrid + Mailgun keys are placeholders (NOT configured) — Hostinger SMTP is the live path
- Function: `notify_new_lead()` in `chipp_leads_api.py`, mapping `DESTINATION_EMAILS`

### Lead schema (fields)
`id, source, destination, businessName, contactName, email, phone, city, state, address, zip, product, notes, createdAt, status, dateContacted, otherReason`
- Form field order: Street Address → City → State → ZIP (above ZIP)

### Known bug fixed (2026-08-18)
- Old dashboard had binary `'PSD' : 'Chipp'` dest fallback → new `witzend` value displayed as "Chipp". Fixed with `destText()` helper handling all 3.

### Test lead
- Star Grocery, Nick, stargrocery@sbcglobal.net, Berkeley CA, 3068 Claremont Ave (still in notes — address migration optional)

---

## RiP GoR Protocol v1.0 — Governance-Optimized Resolution
**Created:** 2026-08-11
**Location:** `/root/.aos/aos/gor_protocol.py`
**Skill:** `/root/.openclaw/workspace/skills/gor-protocol/SKILL.md`

### Acronym (Captain, 2026-08-18)
**RiP GoR** =
- **R** = Roast — 6-persona adversarial council (`roast_skill.py`)
- **i** (int) = the topic / input
- **P** = Patricia — DMCIA specialist (was "Chief of Staff")
- **Go** = go with the **(R)esult** (verdict)

### The RiP GoR Council (named by Captain, 2026-08-18)
The governing body that runs `RiP GoR(int) = Roast(int) + Patricia → Go with Result`.

**Roster:**
| Seat | Member | Role |
|------|--------|------|
| Roast Council | Contrarian (25%) | Fatal Flaw Finder |
| Roast Council | Expansionist (15%) | Upside Maximizer |
| Roast Council | FirstPrinciples (20%) | Logic Purist |
| Roast Council | Researcher (20%) | Market Intelligence |
| Roast Council | Buyer (20%) | Customer Proxy |
| Roast Council | Judge (—) | Final Arbiter → verdict |
| Strategic | Patricia | DMCIA specialist — org alignment, delegation |
| Authority | Captain | Final override (override / escalate) |

**First Council ruling (2026-08-18):** DarkFactory → **RESHAPE** (5.5 × ALIGNED-with-caution). Build sandboxed Level-3+ harness, not full Level-5, pointed at a safe workload; wire from existing `coding-agent` skill + Hold Out Kidneys + cron.

### Formula
```
RiP GoR(int) = Roast(int) + Patricia(roast_result) → Go with Result
```

### Pipeline
1. **Stage 1 — ROAST:** 6 adversarial personas evaluate (Contrarian, Expansionist, FirstPrinciples, Researcher, Buyer → Judge)
2. **Stage 2 — PATRICIA:** DMCIA specialist adds strategic context, org alignment, delegation target
3. **Stage 3 — GoR:** Combined verdict via decision matrix → GO / RESHAPE / KILL / ESCALATE

### Decision Matrix
| Roast ↓ × Patricia → | ALIGNED | URGENT | DEFERRED | MISALIGNED | NEEDS_CLARITY |
|----------------------|---------|--------|----------|------------|---------------|
| GREEN_LIGHT | GO | GO | RESHAPE | RESHAPE | RESHAPE |
| RESHAPE | RESHAPE | **GO** | RESHAPE | KILL | RESHAPE |
| KILL | KILL | **ESCALATE** | KILL | KILL | **ESCALATE** |

**Key rules:**
- RESHAPE + URGENT = GO (Patricia can override Roast hesitation when urgent)
- KILL + URGENT = ESCALATE (Captain must resolve conflict)
- KILL + ALIGNED = KILL (Patricia cannot override Roast KILL verdict)
- Simple tasks (under complexity threshold) skip Roast, go straight to Patricia

### Socket Commands
```bash
# Evaluate a task through GoR
echo '{"cmd":"gor","task":{"title":"Launch X","objective":"Build Y","budget":5000,"time_estimate":80}}' | nc -U /tmp/aos_brain.sock

# Get last decision
echo '{"cmd":"gor","action":"last"}' | nc -U /tmp/aos_brain.sock

# Decision history
echo '{"cmd":"gor","action":"history","limit":10}' | nc -U /tmp/aos_brain.sock

# Delegation queue
echo '{"cmd":"gor","action":"queue"}' | nc -U /tmp/aos_brain.sock

# Protocol status
echo '{"cmd":"gor","action":"status"}' | nc -U /tmp/aos_brain.sock

# Captain override
echo '{"cmd":"gor","action":"override","task_title":"Launch X","verdict":"GO"}' | nc -U /tmp/aos_brain.sock
```

### Integration
- Patricia must use `patricia_delegate_with_gor()` instead of delegating directly
- All GoR decisions logged to `/var/lib/aos/brain_state/gor_history.json`
- Captain has final override authority via socket command

### Test Results (4/4 passed)
| Task | Roast | Patricia | GoR |
|------|-------|----------|-----|
| Critical Security Patch | 5.5 RESHAPE | URGENT | **GO** |
| YouTube-to-LinkedIn SaaS | 5.5 RESHAPE | ALIGNED | RESHAPE |
| Pizza Delivery Drones | 5.5 RESHAPE | NEEDS_CLARITY | RESHAPE |
| Update Product Images | 7.5 SKIPPED | ALIGNED | **GO** |

---

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

## psdepot.com Cart localStorage Issue - 2026-07-28
**Problem:** Cart items from main page not appearing in checkout

**Root Cause:** Inconsistent localStorage keys across pages
- Product pages (72-100-cash-drawer.html, etc.): Used `psdepot.com:psdepot_cart`
- Checkout/index pages: Used `psdepot_cart`
- This caused carts to appear empty or items to not sync

**Solution:** Standardize ALL pages to use `psdepot_cart`
- Updated ~30+ HTML files site-wide
- Keys must match exactly: `psdepot_cart` (not `psdepot.com:psdepot_cart`)
- Data structure: `{sku, name, price, quantity}` minimum fields

**Files to check if issue recurs:**
- `/var/www/psdepot.com/index.html` — main page cart functions
- `/var/www/psdepot.com/checkout.html` — checkout getCart/saveCart
- `/var/www/psdepot.com/products/*.html` — product addToCart functions

**Diagnostic:** Visit `https://psdepot.com/cart-test.html` to inspect localStorage contents

**Command to verify consistency:**
```bash
grep -r "localStorage.*psdepot_cart" /var/www/psdepot.com --include="*.html" | grep -v ".backups"
# All should show: psdepot_cart (NOT psdepot.com:psdepot_cart)
```

---

## Omarchy Manual (2026-08-24)
- **Omarchy** = DHH's omakase Linux distro (Arch + Hyprland tiling WM + Quickshell). Keyboard-first, TUI-heavy, full-disk encryption mandatory.
- **Manual** (condensed field guide, with Miles's notes) at `workspace/manuals/omarchy-manual.md` — emailed to Antonio.hudnall@gmail.com.
- **Key facts to remember:**
  - `Super + K` = show all hotkeys (the one to memorize).
  - `Super + Space` = Omarchy menu (everything). `Super + Return` = terminal. `Super + W` = close.
  - Unified clipboard: `Super+C/X/V` (works in terminal too).
  - **Never `pacman -Syu`** — use `omarchy update` (does snapshots + migrations + config).
  - **`omarchy` CLI = agent hook** — exposes all internal tooling; use it to let agents (Beets, etc.) customize the system.
  - **`omarchy reinstall` wipes user config changes** (unlike snapshots which preserve /home + ~/.config). Reach for it carefully.
  - Tmux prefix = `Ctrl+Space`. AI-agent layouts: `tdl [agent]`, `tds`, `tdlm`, `tsl N [cmd]`.
  - Neovim (LazyVim-based, leader = Space). Snapshots via Limine bootloader (auto on update, rollback from boot menu).
  - Full-disk install WIPES the drive — backup first. Wired/2.4GHz keyboard required (BT can't enter encryption pw at boot).
  - 22 themes. Security: firewall on by default, SSH off until enabled, ufw-docker locks Docker.

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
| Capton 1 oz Bottle Top Pourer | CAP-100-1OZ | $49.00 | `/products/capton-1oz-pourer.html` |
| Capton 1.5 oz Bottle Top Pourer | CAP-150-15OZ | $49.00 | `/products/capton-1.5oz-pourer.html` |
| Capton 2 oz Bottle Top Pourer | CAP-200-2OZ | $49.00 | `/products/capton-2oz-pourer.html` |
| Capton Wine Pourer (5 oz) | CAP-WINE-5OZ | $49.00 | `/products/capton-wine-pourer.html` |
| Capton Variety Pack (12-Pack) | CAP-VARY-12PK | $558.00 | `/products/capton-variety-pack.html` |
| Capton Pourer Cleaning Kit | CAP-CLEAN-KIT | $34.99 | `/products/capton-cleaning-kit.html` |
| Capton PourLink Analytics | POUR-ANALYTICS | $3,000.00 | `/products/capton-pourlink-analytics.html` |
| Capton PourLink Receiver | POUR-RECV | $2,200.00 | `/products/capton-pourlink-receiver.html` |

### Features
- Schema.org Product markup on all pages
- Responsive design matching existing PSD template
- SEO optimized with proper meta tags
- Linked from `/products/index.html` in categories

---

## Agent Readiness — llms.txt + products.json Deployed
**Deployed:** 2026-08-11 00:37 UTC
**Status:** ✅ LIVE

### What's New
- **`https://psdepot.com/llms.txt`** — Agent-readable site index listing all categories, services, shipping, contact, and crawling policy. First POS supply site with agent-native discovery.
- **`https://psdepot.com/products.json`** — Machine-readable product catalog with 24 products across 6 categories. Each product has SKU, name, price, brand, category, description, URL, availability, and specs.

### Agent Readiness Audit Results
- ✅ Schema.org markup: B+ (LocalBusiness, FAQPage, Product schemas)
- ✅ llms.txt deployed
- ✅ products.json deployed
- ⚠️ 6 product pages still need Product schema added (15-741, 30-150, 54-230, 62245, 67240, CC-235)
- ⚠️ No MCP endpoint / agent checkout yet
- ⚠️ No review/rating schema

### Competitive Position
- **pospaper.com**: Only competitor with llms.txt (Shopify store, basic)
- **Staples, Uline, POSSupply, ReceiptPaper**: All 404 on llms.txt
- **psdepot.com**: First POS supply site with both llms.txt + products.json

### Price Bug Fixed
- Capton prices in MEMORY.md corrected to match live site ($24.99→$49.00 etc.)

### Files
- `/var/www/psdepot.com/llms.txt`
- `/var/www/psdepot.com/products.json`

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

---

## TODO: Auth System SendGrid Setup
**Added:** 2026-08-05
**Status:** DOWNGRADED to OPTIONAL (SMTP fallback verified working) — 2026-08-19

### Finding (2026-08-19)
Auth system email is NOT actually broken. `backend/utils/email.js` has a full transport priority chain (SendGrid → AWS SES → Mailgun → SMTP → Ethereal), and the Hostinger SMTP fallback is fully configured in `.env` and **verified working** (`nodemailer.verify()` → OK, 2026-08-19). So verification + password-reset emails already deliver via SMTP.

### Remaining SendGrid work (optional, better deliverability only — requires Captain's credentials)
1. Get a SendGrid API key (blocked on Captain — needs a SendGrid account/API key; none stored)
2. Add DNS records (CNAME + DKIM + DMARC) — Captain action on DNS provider
3. Add `SENDGRID_API_KEY` to `.env` (currently commented out)
4. Test delivery

### Reference
- DepotChaos SendGrid: `/datadepot/web/sendgrid_sender.py`, `/datadepot/cron/process_email_queue.py`
- Auth email logic: `/root/.openclaw/workspace/auth-system/backend/utils/email.js`

### Files
- `/root/.openclaw/workspace/auth-system/.env` (SMTP Hostinger configured; SENDGRID_API_KEY commented)
- `/root/.openclaw/workspace/auth-system/backend/`

### Reminder
Cron job `auth-system-sendgrid-setup` — daily. (Downgraded; no longer blocking login.)
