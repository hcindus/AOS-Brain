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

*Last Updated: 2026-04-07*

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

## PENDING: SendGrid DNS Configuration for DepotChaos
**Created:** 2026-06-11
**Status:** AWAITING ACTION (Captain)

### What Needs to Be Done
Add these DNS records to psdepot.com in Hostinger:

| Type | Host | Value |
|------|------|-------|
| CNAME | em8873.psdepot.com | u109143135.wl136.sendgrid.net |
| CNAME | s1._domainkey.psdepot.com | s1.domainkey.u109143135.wl136.sendgrid.net |
| CNAME | s2._domainkey.psdepot.com | s2.domainkey.u109143135.wl136.sendgrid.net |
| TXT | _dmarc.psdepot.com | v=DMARC1; p=none |

### Steps
1. Go to Hostinger Dashboard → Domains → psdepot.com → DNS Zone
2. Add the 4 records above
3. Wait 5-30 minutes for propagation
4. Verify in SendGrid domain authentication page
5. Create SendGrid API key (Settings → API Keys)
6. Provide API key to Miles for DepotChaos configuration

### Why This Matters
- Enables SendGrid email delivery for DepotChaos CRM
- Bypasses Hostinger SMTP rate limits
- Allows sending 100 emails/day free
- Fixes current email queue blockage (106 emails pending)

### Reference
Source: Telegram conversation 2026-06-11

---
*Last Updated: 2026-06-11*
