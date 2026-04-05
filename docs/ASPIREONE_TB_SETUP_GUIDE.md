# LOCAL MODEL SETUP - ASUS ASPIREONE + SUSE LINUX + 1TB DRIVE
**For:** Captain's Old PC Setup  
**Date:** April 5, 2026  
**Status:** READY TO DEPLOY

---

## HARDWARE SPECIFICATIONS

**Asus AspireOne (Netbook):**
- **CPU:** Intel Atom (low power)
- **RAM:** 2-4GB (upgradeable to 2GB max typically)
- **Storage:** Internal SSD/HDD (small)
- **Display:** 10.1" (sufficient for headless operation)
- **Network:** WiFi + Ethernet
- **USB:** Multiple ports for external drive

**1TB External Drive:**
- **Connection:** USB 3.0 (or USB 2.0)
- **Format:** ext4 (Linux native)
- **Mount Point:** /mnt/tb-drive

---

## SUSE LINUX ISO

**From Repository:**
- Location: Similar to V3 Cosmic Engine specs
- Version: openSUSE Leap or Tumbleweed
- Architecture: x86_64 (Atom compatible)

**Installation Steps:**
1. Download SUSE Linux ISO
2. Create bootable USB: `dd if=openSUSE.iso of=/dev/sdX bs=4M`
3. Boot AspireOne from USB
4. Install to internal drive (minimal installation)
5. Configure network (WiFi/Ethernet)

---

## SYSTEM REQUIREMENTS CHECK

**AspireOne Limitations:**
- ⚠️ **Low RAM (2-4GB)** - Cannot run 70B models
- ✅ **Can run 8B models** - Perfect for specialized agents
- ✅ **Headless mode** - No GUI needed
- ✅ **USB boot** - Can boot from external drive

**Recommended Approach:**
- **Small models (7B-8B)** on AspireOne
- **Distributed setup** - AspireOne as agent node
- **Connect to main VPS** - Agent federation

---

## INSTALLATION GUIDE

### Step 1: Prepare TB Drive

```bash
# Connect 1TB drive to AspireOne
# Boot into SUSE Linux

# Format drive (if new)
sudo mkfs.ext4 /dev/sdX1  # Replace sdX with your drive

# Create mount point
sudo mkdir /mnt/tb-drive
sudo mount /dev/sdX1 /mnt/tb-drive

# Make permanent in /etc/fstab
echo "/dev/sdX1 /mnt/tb-drive ext4 defaults,noatime 0 2" | sudo tee -a /etc/fstab
```

### Step 2: Install Ollama

```bash
# Download Ollama for Linux
curl -fsSL https://ollama.com/install.sh | sh

# Configure to use TB drive
sudo mkdir -p /mnt/tb-drive/ollama
sudo chown $USER:$USER /mnt/tb-drive/ollama

# Set environment variable
export OLLAMA_MODELS=/mnt/tb-drive/ollama/models
export OLLAMA_HOST=0.0.0.0  # Allow remote connections

# Make permanent
echo 'export OLLAMA_MODELS=/mnt/tb-drive/ollama/models' >> ~/.bashrc
echo 'export OLLAMA_HOST=0.0.0.0' >> ~/.bashrc
```

### Step 3: Download Models (8B for AspireOne)

```bash
# Pull smaller models (8B parameters ~ 4.5GB each)
ollama pull llama3:8b
ollama pull phi3:3.8b
ollama pull mistral:7b
ollama pull neural-chat:7b

# Can fit ~20 different 8B models on 1TB drive!
```

### Step 4: Configure as Agent Node

```bash
# Install Python dependencies
sudo zypper install python3 python3-pip
pip3 install requests websockets

# Create agent node script
cat > ~/agent_node.py << 'EOF'
#!/usr/bin/env python3
"""AspireOne Agent Node - Connects to Miles VPS"""

import requests
import time
import json
import subprocess

# Configuration
VPS_URL = "http://miles.cloud:8080"  # Your VPS
LOCAL_OLLAMA = "http://localhost:11434"
AGENT_ID = "aspireone-node-01"

class AspireOneAgent:
    def __init__(self):
        self.models = ["llama3:8b", "phi3:3.8b", "mistral:7b"]
        self.current_model = "llama3:8b"
        
    def check_health(self):
        """Check if Ollama is running"""
        try:
            r = requests.get(f"{LOCAL_OLLAMA}/api/tags")
            return r.status_code == 200
        except:
            return False
    
    def process_task(self, task):
        """Process task using local model"""
        prompt = task.get('prompt', '')
        model = task.get('model', self.current_model)
        
        # Query Ollama
        response = requests.post(
            f"{LOCAL_OLLAMA}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        
        return response.json().get('response', '')
    
    def register_with_vps(self):
        """Register this node with main VPS"""
        try:
            r = requests.post(
                f"{VPS_URL}/api/agents/register",
                json={
                    "agent_id": AGENT_ID,
                    "type": "aspireone_local",
                    "models": self.models,
                    "capacity": "8B_max",
                    "status": "active"
                }
            )
            return r.status_code == 200
        except:
            return False
    
    def run(self):
        """Main loop"""
        print("🚀 AspireOne Agent Node Starting...")
        
        if not self.check_health():
            print("❌ Ollama not running. Start with: ollama serve")
            return
        
        print(f"✅ Ollama healthy. Models: {self.models}")
        
        if self.register_with_vps():
            print(f"✅ Registered with VPS as {AGENT_ID}")
        else:
            print("⚠️ Could not register with VPS (running standalone)")
        
        print("\n📡 Waiting for tasks...")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")

if __name__ == "__main__":
    agent = AspireOneAgent()
    agent.run()
EOF

chmod +x ~/agent_node.py
```

### Step 5: Create Systemd Service

```bash
# Create service for auto-start
sudo tee /etc/systemd/system/aspireone-agent.service << 'EOF'
[Unit]
Description=AspireOne Local Model Agent Node
After=network.target ollama.service

[Service]
Type=simple
User=root
WorkingDirectory=/root
ExecStart=/usr/bin/python3 /root/agent_node.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable aspireone-agent
sudo systemctl start aspireone-agent
```

### Step 6: Network Configuration

```bash
# Get AspireOne IP
ip addr show | grep "inet " | head -2

# Open firewall for Ollama (port 11434)
sudo firewall-cmd --add-port=11434/tcp --permanent
sudo firewall-cmd --reload

# Or using iptables
sudo iptables -A INPUT -p tcp --dport 11434 -j ACCEPT
```

---

## DISTRIBUTED SETUP

### From VPS (Miles)

```python
# In your main agents, add AspireOne as endpoint

ASPIREONE_NODES = [
    "http://192.168.1.100:11434",  # AspireOne IP
]

def query_aspireone(prompt, model="llama3:8b"):
    """Send task to AspireOne node"""
    for node in ASPIREONE_NODES:
        try:
            response = requests.post(
                f"{node}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=60
            )
            if response.status_code == 200:
                return response.json().get('response')
        except:
            continue
    return None  # Fallback to VPS models
```

---

## TROUBLESHOOTING

### Low Memory Issues
```bash
# Create swap file on TB drive
sudo dd if=/dev/zero of=/mnt/tb-drive/swapfile bs=1G count=4
sudo mkswap /mnt/tb-drive/swapfile
sudo swapon /mnt/tb-drive/swapfile
```

### Slow USB 2.0
```bash
# Use lighter models
ollama pull phi3:3.8b  # Only 2.3GB
```

### Network Issues
```bash
# Test connection to VPS
ping miles.cloud
curl http://miles.cloud:8080/api/status
```

---

## CAPACITY PLANNING

**With 1TB Drive + 2-4GB RAM:**

| Model | Size | Quantity | Total |
|-------|------|----------|-------|
| Llama 3 8B | 4.5GB | 50x | 225GB |
| Phi 3 3.8B | 2.3GB | 100x | 230GB |
| Mistral 7B | 4.1GB | 50x | 205GB |
| Custom 7B | 4GB | 75x | 300GB |

**Total:** ~200 different 8B models on 1TB!

---

## USE CASES

1. **Specialized Agent Node**
   - Each AspireOne runs specific agent type
   - Distributed agent society

2. **Backup/Failover**
   - If VPS down, AspireOne takes over
   - Local processing continuity

3. **Offline Operation**
   - No internet required
   - Self-contained agent

4. **Cost Savings**
   - $0 cloud inference costs
   - One-time hardware cost

---

## COST COMPARISON

| Option | Setup Cost | Monthly Cost | 70B Model |
|--------|-----------|--------------|-----------|
| Cloud API | $0 | $50-200 | ✅ Available |
| VPS + TB | $200 | $20-50 | ❌ VPS only |
| AspireOne + TB | $300 | $0 | ✅ Local 8B |
| **AspireOne Fleet (5x)** | $1,500 | $0 | ✅ Distributed |

---

## NEXT STEPS

1. [ ] Flash SUSE Linux ISO to USB
2. [ ] Install on AspireOne
3. [ ] Connect and format 1TB drive
4. [ ] Install Ollama
5. [ ] Download first model (llama3:8b)
6. [ ] Test local inference
7. [ ] Configure agent node script
8. [ ] Connect to Miles VPS
9. [ ] Deploy to agent society

---

**Document ID:** ASPIREONE-TB-SETUP-2026-04-05  
**Compatible With:** V3 Cosmic Engine specifications  
**Status:** READY TO DEPLOY

---

*"From netbook to neural node."* - Miles