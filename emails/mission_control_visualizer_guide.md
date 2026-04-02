# Mission Control Visualizer — User Guide

**Date:** April 2, 2026  
**To:** Antonio.hudnall@gmail.com  
**From:** Miles (miles@myl0nr0s.cloud)  
**Subject:** Mission Control Visualizer — Access Instructions

---

## 🚀 What Is Mission Control?

A real-time Three.js 3D visualization of the Complete Brain v4.0 — showing neural activity, OODA decision cycles, heart rate, and memory clusters in a rotating 32×32×32 volume.

---

## 📍 How to Access

### Option 1: Local Browser (on Miles.cloud)
```bash
firefox http://localhost:8080
# or
google-chrome http://localhost:8080
```

### Option 2: SSH Tunnel (from your machine)
```bash
# On your local machine:
ssh -L 8080:localhost:8080 root@miles.cloud

# Then open browser to:
http://localhost:8080
```

### Option 3: Direct IP Access
Check current IP by running on the VPS:
```bash
bash /root/.openclaw/workspace/mission_control_access.sh
```

Then visit: `http://<IP_ADDRESS>:8080`

---

## 🎨 What You'll See

| Feature | Description |
|---------|-------------|
| **3D Neural Volume** | 32×32×32 rotating cube showing active neurons |
| **OODA Phases** | Color-coded cycles: Blue (Observe) → Green (Orient) → Red (Decide) → Yellow (Act) |
| **Heart Rate** | Current BPM (target: 72) |
| **Tick Counter** | Total brain ticks elapsed |
| **Memory Clusters** | Semantic memory groups visualized |
| **Novelty/Reward** | Current learning metrics |

---

## 🖌️ The Bob Ross Palette

The visualization uses a custom color palette inspired by Bob Ross:
- **Phthalo Blue** — Observe phase
- **Sap Green** — Orient phase  
- **Bright Red** — Decide phase
- **Cadmium Yellow** — Act phase
- **Titanium White** — Active neurons
- **Midnight Black** — Inactive regions

---

## 🔧 Service Management

```bash
# Check status
systemctl status aos-mission-control

# View logs
journalctl -u aos-mission-control -f

# Restart if needed
sudo systemctl restart aos-mission-control
```

---

## 🌐 System Status

- **Service:** Running (PID 1203358)
- **Port:** 8080
- **Uptime:** 1+ days
- **Brain Ticks:** 21,000+
- **Memory:** 51MB / 2GB available

---

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Page won't load | Check service: `systemctl status aos-mission-control` |
| Connection refused | Verify port 8080 isn't blocked by firewall |
| Slow rendering | The 3D scene is intensive; try a different browser |
| Blank screen | Check browser console for Three.js errors |

---

## 📊 Related Commands

```bash
# Quick status check
bash /root/.openclaw/workspace/mission_control_access.sh

# Brain state (JSON)
cat ~/.aos/brain/state/brain_state.json | jq .

# Full system health
bash /root/.openclaw/workspace/scripts/agent_keepalive.sh
```

---

**Questions?** Just ask — I'm running 24/7.

🚀 Miles  
*Autonomous Operations Engine*  
Performance Supply Depot LLC / AGI Company
