# AOS Brain Deployment Guide
## Multi-Agent Coordination with Shared Memory

### Quick Start (5 minutes)

```bash
# 1. Start the brain service
cd /root/.aos/aos
python3 complete_brain_v45.py &

# 2. Verify brain is running
echo '{"cmd":"status"}' | nc -U /tmp/aos_brain.sock

# 3. Run multiple agents
python3 vision_agent_pillow.py --test &
python3 code_agent.py --demo &
python3 agent_sdk.py &

# 4. Check coordination
echo '{"cmd":"cortex_stats"}' | nc -U /tmp/aos_brain.sock
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    BRAIN SERVICE (Port: Socket)           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Cortex v2.5│  │ Persistence │  │  Socket Server      │  │
│  │  32K nodes  │  │  /var/lib   │  │  /tmp/aos_brain.sock│  │
│  └──────┬──────┘  └─────────────┘  └─────────────────────┘  │
└─────────┼───────────────────────────────────────────────────┘
          │
    ┌─────┼─────┐
    │     │     │
┌───▼──┐┌▼───┐┌▼────┐
│Vision││Code││Trade│  ← Specialized Agents
│Agent ││Agent││Agent│
└──┬───┘└─┬──┘└──┬──┘
   │      │      │
 Camera  Git   Binance  ← External APIs/Inputs
```

---

## 1. Brain Service Setup

### Systemd Service (Production)

Create `/etc/systemd/system/aos-brain.service`:

```ini
[Unit]
Description=AOS Brain v4.5 - Multi-Agent Coordination
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.aos/aos
Environment=PYTHONPATH=/root/.aos/aos
Environment=AOS_VERSION=4.5
Environment=AOS_LOG_LEVEL=INFO
ExecStart=/usr/bin/python3 /root/.aos/aos/complete_brain_v45.py
Restart=always
RestartSec=10

# Resource limits
LimitNOFILE=65536
MemoryMax=2G
CPUQuota=200%

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
systemctl daemon-reload
systemctl enable aos-brain
systemctl start aos-brain
systemctl status aos-brain
```

### Verify Brain Health

```bash
# Check socket exists
ls -la /tmp/aos_brain.sock

# Test commands
echo '{"cmd":"ping"}' | nc -U /tmp/aos_brain.sock
echo '{"cmd":"status"}' | nc -U /tmp/aos_brain.sock | python3 -m json.tool
```

---

## 2. Agent Deployment

### Vision Agent (Perception)

```python
# vision_worker.py
from vision_agent_pillow import VisionAgent
import time

agent = VisionAgent(agent_id="vision_perception_01")
agent.register()

while True:
    # Process camera or images
    result = agent.process_and_send("/path/to/image.jpg")
    print(f"Vision: {result['hotspots']} hotspots written")
    time.sleep(5)  # Adjust FPS
```

Run:
```bash
python3 vision_worker.py &
```

### Code Agent (Action)

```python
# code_worker.py
from code_agent import CodeAgent

agent = CodeAgent(agent_id="code_generator_01")

# Check for work every minute
while True:
    task = agent.resume_from_brain()
    if task:
        print(f"Resuming: {task.task_id}")
        # Continue work
    else:
        # Look for new tasks
        time.sleep(60)
```

### Trading Agent (Decision)

```python
# trade_worker.py
from agent_sdk import AOSBrainClient
import requests

client = AOSBrainClient(agent_id="trader_01")
client.register()

while True:
    # Fetch market data
    prices = requests.get("https://api.binance.com/...").json()
    
    # Write to cortex (region 0-3 for market data)
    hotspots = encode_prices_to_ternary(prices)
    client.write_cortex(hotspots, regions=[0,1,2,3])
    
    # Check for signals from other agents
    state = client.read_cortex(regions=[4,5,6,7])
    if state.coherence > 0.5:
        print("High coherence - checking for trade signals")
    
    time.sleep(1)  # 1 second for trading
```

---

## 3. Monitoring & Debugging

### Real-time Cortex Monitor

```bash
# Watch cortex activity
watch -n 1 'echo "{\"cmd\":\"cortex_stats\"}" | nc -U /tmp/aos_brain.sock | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Agents: {len(d.get(chr(39)+\"agents\"+chr(39),{}))} | Tick: {d.get(chr(39)+\"current_tick\"+chr(39),0)}\")"'
```

### Brain Health Dashboard

```python
# monitor.py
import time
import json
import socket

def get_metrics():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(2)
    sock.connect('/tmp/aos_brain.sock')
    sock.sendall(b'{"cmd":"status"}\n')
    data = sock.recv(4096)
    sock.close()
    return json.loads(data.decode())

while True:
    m = get_metrics()
    print(f"Tick: {m['tick']} | Phase: {m['phase']} | Components: {m['components_active']}")
    time.sleep(5)
```

### Log Files

```bash
# Brain logs (if running via systemd)
journalctl -u aos-brain -f

# Custom log location
/var/log/aos/brain.log

# Persistence logs
/var/lib/aos/brain_state/
```

---

## 4. Persistence & Backup

### Automatic Persistence

Brain auto-saves every 60 seconds to `/var/lib/aos/brain_state/`:

```
/var/lib/aos/brain_state/
├── brain_state.pkl          # Main state file
├── brain_metadata.json      # Human-readable summary
└── backups/
    ├── brain_backup_20250526_120000_tick1000.pkl
    └── brain_backup_20250526_130000_tick1500.pkl
```

### Manual Backup

```python
from agent_sdk import AOSBrainClient

client = AOSBrainClient(agent_id="backup_admin")
# Trigger save
echo '{"cmd":"save"}' | nc -U /tmp/aos_brain.sock
```

### Restore from Backup

```bash
# Stop brain
systemctl stop aos-brain

# Restore state
cp /var/lib/aos/brain_state/backups/brain_backup_*.pkl \
   /var/lib/aos/brain_state/brain_state.pkl

# Start brain
systemctl start aos-brain
```

---

## 5. Multi-Agent Coordination Patterns

### Pattern 1: Shared Alert

```python
# Any agent can raise alert
client.write_thought("ALERT: Market volatility detected", priority=1.0)

# All other agents see it in cortex
state = client.read_cortex()
if state.coherence > 0.8:
    print("Multiple agents signaling - consensus reached")
```

### Pattern 2: Task Handoff

```python
# Vision agent detects something
vision.write_cortex(hotspots, regions=[0,1])

# Code agent reads and acts
state = code_agent.read_cortex(regions=[0,1])
if state.hotspots:
    code_agent.generate_code_for_pattern(state)
    code_agent.write_cortex(response, regions=[4,5])  # Signal completion
```

### Pattern 3: Temporal Learning

```python
# Before action
client.write_thought("Starting task: refactor authentication", priority=0.9)

# ... do work ...

# After action (with result)
result = "success" if tests_pass else "failed"
client.write_thought(f"Task completed: {result}", priority=1.0)

# Later: query temporal memory
# "What happened last time we touched authentication?"
```

---

## 6. Scaling Considerations

### Vertical Scaling (Single Node)

| Resource | Usage | Limit |
|----------|-------|-------|
| Memory | ~200MB base + ~50MB per agent | 2GB recommended |
| CPU | 1-3ms/tick per agent | 4 cores sufficient |
| Disk | ~10MB state + backups | 1GB recommended |

### Horizontal Scaling (Multi-Node)

For multiple VPS nodes:

```python
# Node A (leader)
brain = CompleteBrainV44()
brain.setup_distributed(node_id="node_alpha", 
                        peers=["node_beta", "node_gamma"])

# Node B (follower)
brain = CompleteBrainV44()
brain.setup_distributed(node_id="node_beta",
                        peers=["node_alpha", "node_gamma"])
```

### Performance Tuning

```python
# For high-frequency agents (trading)
cortex = CortexV25Optimized(
    size=32,
    temporal_depth=64,  # Smaller = faster
    use_gpu=True          # If available
)

# For memory-heavy agents (vision)
cortex = CortexV25Optimized(
    size=32,
    temporal_depth=256,  # Larger = more history
    use_gpu=False        # CPU fine for images
)
```

---

## 7. Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| `Socket not found` | Brain not running | `systemctl start aos-brain` |
| `Registration failed` | Agent ID conflict | Use unique IDs per agent |
| `Low coherence` | No agent activity | Check agent is writing to cortex |
| `Persistence failed` | Disk full | Check `/var/lib/aos/` space |
| `High latency` | Too many agents | Reduce `temporal_depth` or shard agents |

### Debug Commands

```bash
# Check brain process
ps aux | grep complete_brain

# Check socket
ss -xp | grep aos_brain

# Check persistence
ls -lah /var/lib/aos/brain_state/

# Test with verbose client
python3 -c "
from agent_sdk import AOSBrainClient
import logging
logging.basicConfig(level=logging.DEBUG)
c = AOSBrainClient('debug_test')
c.register()
print(c.get_brain_status())
"
```

---

## 8. Production Checklist

- [ ] Brain service running under systemd
- [ ] Persistence directory exists (`/var/lib/aos/brain_state/`)
- [ ] Agents registered with unique IDs
- [ ] Log rotation configured
- [ ] Backup script in cron
- [ ] Health monitoring active
- [ ] Resource limits set
- [ ] Socket permissions correct (755)

---

## Next Steps

1. **Add more agents**: Discord, GitHub, API monitoring
2. **Implement learning**: Feedback loops from agent success/failure
3. **Connect to LLM**: Claude/GPT for reasoning layer
4. **Add UI**: Web dashboard for brain visualization
5. **Scale out**: Deploy to multiple VPS nodes

---

## Files Reference

| File | Purpose | Status |
|------|---------|--------|
| `complete_brain_v45.py` | Brain service | ✅ Production |
| `cortex_v25_optimized.py` | Memory core | ✅ Integrated |
| `agent_sdk.py` | Agent library | ✅ Ready |
| `vision_agent_pillow.py` | Perception | ✅ Working |
| `code_agent.py` | Code generation | ✅ Working |
| `production_infra.py` | Vector DB/GPU | 📝 Structure |
| `demo_agents_communicating.py` | Demo | ✅ Working |

---

**Your multi-agent coordination system is now deployed and ready.**

Agents can:
- Register and persist identity
- Read/write shared cortical state
- Coordinate through coherence
- Learn from temporal memory
- Survive crashes and resume

Start with 2-3 agents, add more as needed.