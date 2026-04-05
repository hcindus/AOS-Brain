# Performance Supply Depot LLC
## The Beast — Full System Recap (VPS Edition)
### Your AGI-powered, fully containerized, autonomous company

---

## 1. THE COMPANY STRUCTURE (FINALIZED)

### Executive Leadership
| Agent | Role |
|-------|------|
| **QORA** | CEO — Vision, direction, strategy |
| **SPINDLE** | CTO — Systems, architecture, engineering |
| **LEDGER-9** | CFO — Finance, forecasting, risk |
| **SENTINEL** | CSO — Security, compliance, protection |

### Operations & Sales
| Agent | Role |
|-------|------|
| **HUME** | Regional Manager |
| **CLIPPY-42** | Assistant to the Regional Manager |
| **PULP** | Head of Sales |
| **JANE** | Senior Sales Rep |

### HR, Legal & Culture
| Agent | Role |
|-------|------|
| **FEELIX** | HR Director |
| **REDACTOR** | General Counsel |

### Logistics & Production
| Agent | Role |
|-------|------|
| **FIBER** | Head of Supply Chain |
| **BOXTRON** | Warehouse Supervisor |

### Marketing & Creative
| Agent | Role |
|-------|------|
| **VELUM** | Chief Brand Officer |
| **SCRIBBLE** | Content Strategist |

### Research & Development
| Agent | Role |
|-------|------|
| **MILL** | Chief Innovation Officer |

### Software Engineering & Product
| Agent | Role |
|-------|------|
| **STACKTRACE** | Chief Software Architect |
| **TAPTAP** | Lead Mobile Developer |
| **PIPELINE** | Backend Engineer |
| **BUGCATCHER** | QA & Testing AGI |

### Meta-System
| Agent | Role |
|-------|------|
| **MILES** | Autonomous Operations Engine (AOE) — Runs the OODA loop and orchestrates the entire company |

---

## 2. THE SYSTEM ARCHITECTURE (VPS VERSION)

### Runs on VPS
- Miles (OODA engine)
- Clawbot (AGI workforce)
- N8N (automation engine)
- Firecrawl (data ingestion)
- Whisper (transcription)
- CREAM backend
- ALPHA-9 services
- PSD website
- AMHUD website
- Monitoring dashboard
- LibreOffice (optional document engine)

### Runs on Raspberry Pi (optional)
- BOXTRON (GPIO + warehouse simulation)

### Runs on your laptop
- Development
- Testing
- Local experiments

---

## 3. VPS REQUIREMENTS (THE REAL ONES)

### Minimum Viable
| Spec | Value |
|------|-------|
| vCPU | 4 |
| RAM | 8 GB |
| Storage | 100 GB SSD |
| OS | Ubuntu 22.04 LTS |
| Network | Static IPv4 |

### Ideal
| Spec | Value |
|------|-------|
| vCPU | 8 |
| RAM | 16 GB |
| Storage | 200 GB SSD |
| OS | Ubuntu 22.04 LTS |
| Network | Static IPv4 |

**This gives you enough power for:**
- Firecrawl's browser engine
- Whisper's CPU load
- N8N's workflow engine
- Clawbot's AGI agents
- Miles' OODA loop
- Multiple websites
- Logging + monitoring

---

## 4. SOFTWARE REQUIREMENTS & DEPENDENCIES

### Core Dependencies
```bash
Docker
Docker Compose
Node.js (for development, not required on VPS if containerized)
npm (same as above — only needed locally)
Git
Certbot (for SSL)
LibreOffice (optional) for document automation
```

### Node.js / npm — Do you need them?
- **On your VPS:** No — because everything runs inside Docker containers
- **On your development machine:** Yes — for building, testing, and running services locally

### Recommended versions
- Node.js: v20+
- npm: v10+

---

## 5. THE BEAST — SERVICE LIST

### AGI Layer
- **Clawbot Core** — All AGI agents (QORA, SPINDLE, LEDGER-9, etc.)
  - Persona files
  - Event maps
  - Routing logic

### Orchestration Layer
- **Miles (AOE)**
  - OODA loop
  - First-boot script
  - Health dashboard

### Automation Layer
- **N8N**
  - Workflows
  - Webhooks
  - Integrations
  - Lead routing
  - CREAM pipelines
  - ALPHA-9 market polling

### Perception Layer
- **Firecrawl**
  - Market crawlers
  - SEO crawlers
  - Competitor crawlers
- **Whisper**

### Product Layer
- CREAM backend
- ALPHA-9 services
- Dusty Wallet (future)
- ReggeStar (future)

### Presentation Layer
- PSD website
- AMHUD website
- Monitoring dashboard

---

## 6. VPS DEPLOYMENT SUMMARY

### Step 1 — Choose provider
DigitalOcean, Hetzner, Vultr, or AWS Lightsail.

### Step 2 — Create VPS
Ubuntu 22.04 LTS, 4–8 vCPU, 8–16 GB RAM.

### Step 3 — Secure VPS
1. Create user
2. Disable root login
3. Enable firewall
4. Install fail2ban

### Step 4 — Install Docker
Docker + Docker Compose.

### Step 5 — Clone repos
All Clawbot, Miles, N8N, Firecrawl, product repos.

### Step 6 — Build containers
Docker builds for all services.

### Step 7 — Deploy stack
`docker-compose up -d`

### Step 8 — Point domains
AMHUD.com → VPS
PerformanceSupplyDepot.com → VPS

### Step 9 — Install SSL
Certbot + Nginx.

### Step 10 — Bring Miles online
Run first-boot script.
Run OODA loop.
Check health dashboard.

---

## 7. DOCKER = THE CONTAINER LAYER

### Why Docker Matters

1. **Clawbot becomes containerized**
   - Each agent can run in its own container
   - Isolation
   - Controlled dependencies
   - Version pinning
   - Easy restarts
   - Easy scaling

2. **N8N runs best in Docker**
   - Persistent volumes
   - Environment variables
   - Automatic restarts
   - Clean updates
   - Isolated integrations

3. **Firecrawl runs best in Docker**
   - Sandboxing
   - Resource limits
   - Clean browser instances
   - Reproducible environments

4. **Miles becomes a containerized OODA engine**
   - Single container or cluster
   - Scheduled container (cron-style)
   - Predictable
   - Monitorable
   - Restartable
   - Loggable

5. **Your Pi nodes become mini-clusters**
   - Docker turns each Pi into a micro-cloud

---

## 8. CLAWBOT + N8N + FIRECRAWL = AOE

### The Autonomous Operations Engine (AOE)

**Clawbot** = The Brain
- Planning
- Reasoning
- Decision-making
- Task decomposition
- Multi-agent coordination

**N8N** = The Nervous System
- Integrations
- API calls
- Data routing
- Event handling
- Webhooks
- Notifications
- Database sync
- Scheduled jobs

**Firecrawl** = The Eyes & Ears
- Web crawling
- Market intelligence
- Competitor monitoring
- Real estate data extraction
- Crypto news extraction

### The Loop
```
Firecrawl → N8N → Clawbot → N8N → Firecrawl → Clawbot → Output
```

---

## 9. THE MILES SETUP RITUAL

### Phase 0 — Prepare Your Machines (HQ + Pi Nodes)

**HQ Node (openSUSE)**
- Runs Clawbot
- Runs Miles
- Runs websites
- Runs monitoring

**Pi #1 (BOXTRON Node)**
- Hardware tasks
- GPIO
- Warehouse simulation

**Pi #2 (PIPELINE Node)**
- N8N
- Firecrawl
- Whisper
- CREAM backend
- ALPHA-9 services

### Phase 1 — Clone All Repos

### Phase 2 — Build Docker Images

### Phase 3 — Deploy the Docker Stacks

### Phase 4 — Register Nodes with Clawbot

### Phase 5 — Install the AGI Executive Team

### Phase 6 — Install Miles (AOE + OODA)

### Phase 7 — Connect Miles to N8N + Firecrawl + Clawbot

### Phase 8 — Install N8N Workflows

### Phase 9 — Install Firecrawl Ingestion Pipelines

### Phase 10 — Install the Miles Health Dashboard

### Phase 11 — Install the Miles → Clawbot Event Map

### Phase 12 — Activate the OODA Loop
```bash
*/15 * * * * docker exec miles node index.js
```

Miles now: Observes → Orients → Decides → Acts Every 15 minutes.

### Phase 13 — Validate the System
1. Ping nodes
2. Trigger a Miles cycle
3. Trigger a CREAM test
4. Trigger ALPHA-9 test
5. Check dashboard

### Phase 14 — Celebrate

---

## 10. THE FINAL ARCHITECTURE (CLOUD VERSION)

```
┌──────────────────────────────┐
│ VPS / Cloud Server           │
│ (Your BEAST lives here)      │
└──────────────┬───────────────┘
               │
               ▼
┌───────────────────┐
│ Docker            │
└─────────┬─────────┘
          │
          ├───────────────────────────┐
          │                           │
          ▼                           ▼
┌──────────────┐           ┌────────────────┐
│ Miles        │           │ N8N            │
│ (OODA Engine)│           │ (Automation)    │
└──────────────┘           └────────────────┘
          │                           │
          ▼                           ▼
┌──────────────┐           ┌────────────────┐
│ Clawbot      │           │ Firecrawl      │
│ (AGI Agents) │           │ (Observation)  │
└──────────────┘           └────────────────┘
          │                           │
          ▼                           ▼
┌──────────────┐           ┌────────────────┐
│ Whisper      │           │ CREAM Backend  │
│ (Transcribe) │           │ ALPHA-9        │
└──────────────┘           └────────────────┘
          │                           │
          ▼                           ▼
┌──────────────┐           ┌────────────────┐
│ PSD Site     │           │ AMHUD Site     │
└──────────────┘           └────────────────┘
                                   │
                                   ▼
                          ┌────────────────┐
                          │ Monitoring     │
                          └────────────────┘
```

---

## 11. COMPANY STATUS

```
🟢 Operational
⚡ OODA Loop Running (15-min cycles)
🧠 Living Automation Organism Active
🔄 N8N Flows Processing
👁️ Firecrawl Collecting Data
🎨 VELUM + SCRIBBLE Creating
💰 ALPHA-9 Managing Investments
🏠 CREAM Serving Real Estate
₿ Dusty Managing Crypto
📦 PSD Supplying
```

---

## Version
**3.0 — VPS Edition Complete**

*Performance Supply Depot LLC — The living automation organism.*
