# Temporal Consolidation — AGI Company

**Date:** 2026-08-18
**Decision:** One Temporal server (Miles VPS), all workflows registered on it.
**Driver:** RiP GoR Council → "consolidate the dormant Temporal codebases."

---

## The unified stack (Miles VPS)

| Layer | Component | Status |
|-------|-----------|--------|
| Server | Temporal (postgres + auto-setup + UI) | ✅ Docker `/opt/temporal/`, `:7233` / `:8233` |
| Worker 1 | Dark Factory (Python, 9 activities) | ✅ `darkfactory-worker.service` |
| Worker 2 | Collections (Go, debt collection) | ✅ `collections-worker.service` |
| Queue | 30-min triage loop | ✅ `darkfactory-triage.timer` |

---

## Workflows now consolidated

### 1. Dark Factory (Python) — ✅ live
- `temporal/darkfactory/` — validate → allocate → build → verify → blind hold-out → blue-green deploy → notify.
- Queue: `darkfactory-queue`.

### 2. Collections (Go) — ✅ live (compiled binary)
- `AGI_COMPANY/operations/collections/temporal-workflow/` — debt collection (friendly → second → final → review).
- `main.go` compiled to `collections-worker` binary → runs as `collections-worker.service`.
- Queue: `collections-queue`. Connects to `127.0.0.1:7233` (this host).

### 3. DepotChaos MS-Connect follow-up (Python) — 🟡 available, not yet registered
- `depotchaos/temporal_workflow.py` — real temporalio workflow defs (with `TEMPORAL_AVAILABLE` graceful fallback).
- Intended runner: `depotchaos-tasks.service` (currently `dead`).
- Its own services (`depotchaos.service`, `depotchaos-api.service`) are ACTIVE but are NOT Temporal — they're the CRM web/API. Do not disturb.
- **Next:** register its workflow on the Python worker (or a dedicated depotchaos worker) when follow-up automation is reactivated.

### 4. Mortimer sales pipeline engine (Python) — 🚫 deprecated (was a mock)
- `mortimer-build/pipelines/workflows/temporal_engine.py` — a CUSTOM "Temporal-like" engine, NOT real Temporal.
- Marked deprecated; port to real Temporal SDK if the sales pipeline is reactivated.

---

## Note on Mortimer's VPS / phones
These codebases may also be referenced by Mortimer or the companion apps, which run on **Mortimer's VPS** (a separate host). Nothing on *this* (Miles) VPS depended on them, so consolidating here is safe and non-breaking.

---

## How to run another workflow on this server
```bash
# Any Python temporalio worker can register additional workflows on the same
# server (localhost:7233). Register new workflow types in a worker service,
# or add them to darkfactory-worker's task queue.
```
