# Customer VPS Scaffolding

**Goal:** "click → done" — one command stamps out an isolated customer VPS running the agent suite.

## What ships (customer minimum)
- **Temporal** (durable workflows) + UI
- **Order API** (`psdepot.com/api/order`) + CLOSETER inbox/reply handlers
- **Brain + agents** (via the AOCROS repo, per-customer config)
- **Per-customer secrets** (isolated in `config/customer.env`)

## What does NOT ship (PSD-internal)
DepotChaos CRM, collections (Go), legal/media workers, game bridges, n8n, overpass, scraper-mechanic.

## Usage
```bash
./provision-customer.sh joes-deli joesdeli.com
```

## Status
- ✅ `STACK_MAP.md` — full inventory of the running stack
- 🚧 `docker-compose.yml` — first draft of the containerized minimum
- 🚧 `provision-customer.sh` — first draft of the one-command provisioner

*Next: containerize the brain + agents (currently systemd/Python, not yet Docker images), then wire `provision-customer.sh` to a Hostinger VPS create API.*
