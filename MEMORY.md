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
