# Dark Factory Temporal System

Makes the pipeline indestructible. Jobs survive crashes. No more "44 done, 0 files."

## Quick Start

### 1. Install Dependencies

```bash
cd /root/.openclaw/workspace/temporal/darkfactory
pip install -r requirements.txt
```

### 2. Start Temporal Server (if not already running)

On Miles.cloud:
```bash
# Option A: Quick dev server
temporal server start-dev --ui-port 8233

# Option B: Docker compose (production)
# See https://github.com/temporalio/docker-compose
```

### 3. Start the Dark Factory Worker

```bash
export TEMPORAL_HOST=localhost:7233  # or miles.cloud:7233
python worker.py
```

### 4. Submit a Build Job

```bash
# Single order
python cli.py start CREAM --type web --source /root/.openclaw/workspace/Cream/web/ --priority high --wait

# Batch from file
python cli.py batch --file orders.json

# Start health check
python cli.py health --types apk,web,docker
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      DARK FACTORY SYSTEM                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐    ┌──────────────────┐    ┌──────────────┐ │
│   │   Client     │───▶│  Temporal Server │───▶│   Worker     │ │
│   │   (CLI/API)  │    │  (miles.cloud)   │    │   (Python)   │ │
│   └──────────────┘    └──────────────────┘    └──────────────┘ │
│                              │                          │       │
│                    ┌─────────▼────────┐          ┌──────▼──────┐│
│                    │   UI (8233)      │          │  Activities ││
│                    │   Visibility     │          │  - validate ││
│                    └──────────────────┘          │  - build    ││
│                                                  │  - verify   ││
│                                                  └─────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Workflows

| Workflow | Purpose |
|----------|---------|
| `DarkFactoryWorkflow` | Single build job with full lifecycle |
| `DarkFactoryBatchWorkflow` | Process multiple jobs |
| `DarkFactoryHealthCheck` | Daily SDK validation |

## Activities

| Activity | Purpose |
|----------|---------|
| `validate_sdk_health` | Check SDK installed & functional |
| `allocate_build_resources` | Create workspace |
| `execute_build` | Actually run the build (with heartbeats) |
| `verify_build_output` | Patricia's rule: must exist & have size |
| `notify_completion` | Success notification |
| `notify_escalation` | Stuck/failed alert |
| `cleanup_resources` | Remove temp files |

## Resilience Features

- ✅ **Durable state** - survives crashes, resumes exactly where it left off
- ✅ **Automatic retries** - exponential backoff, configurable per-activity
- ✅ **Heartbeats** - long builds must check in or get restarted
- ✅ **Escalation timer** - auto-alert if stuck >30 minutes
- ✅ **Output verification** - "44 done, 0 files" is impossible
- ✅ **UI visibility** - see every running/failed/completed job at `:8233`

## Example Orders JSON

```json
[
  {
    "order_id": "DF-001",
    "project_name": "CREAM",
    "build_type": "web",
    "source_path": "/workspace/Cream/web/",
    "priority": "high"
  },
  {
    "order_id": "DF-002", 
    "project_name": "ReggieStarr",
    "build_type": "apk",
    "source_path": "/workspace/ReggieStarr/mobile/",
    "priority": "normal"
  }
]
```

## Files

```
darkfactory/
├── requirements.txt          # Python deps
├── worker.py                 # Temporal worker
├── cli.py                    # Command line interface
├── workflows/
│   ├── __init__.py
│   └── dark_factory.py       # Workflow definitions
└── activities/
    ├── __init__.py
    └── build_activities.py   # Activity implementations
```

## Patricia's Rules (Now Enforced)

1. ✅ Validate SDK before accepting job
2. ✅ Build with heartbeats every 60s
3. ✅ Verify output file exists & has size
4. ✅ Escalate if stuck >30 minutes
5. ✅ Health check SDK daily
6. ✅ Never report "complete" without verification

---

*Built with Temporal. Resilient by design.*