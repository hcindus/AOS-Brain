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

## RiP GoR verdict: **RESHAPE** (2026-11-10)

The scaffolding idea is right, but stress-tested to two corrections:
1. **Start with the lightest image** — ship the *agent suite* first (Greeter/Closeter/etc.), not the full 14-component brain. A customer needs their agents working, not the whole brain.
2. **Defer heavy containerization** until *after the first sale* validates demand. Don't over-build infra before revenue proves it.

## Status
- ✅ `STACK_MAP.md` — full inventory of the running stack
- 🚧 `docker-compose.yml` — first draft (currently has Temporal + order/CLOSETER; needs the *agent-suite-only* image, not the full brain)
- 🚧 `provision-customer.sh` — first draft

*Next (post-first-sale): containerize the agent suite as the lightest image, wire `provision-customer.sh` to a Hostinger VPS create API, then harden into "click → done."*
