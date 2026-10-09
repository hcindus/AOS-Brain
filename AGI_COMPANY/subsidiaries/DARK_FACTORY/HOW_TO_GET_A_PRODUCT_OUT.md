# Dark Factory — How to Get a Product Out

*The Dark Factory turns a spec into a built, verified, deployed product — autonomously. This is what you need to provide, and what the factory does with it.*

---

## The pipeline (what happens)

```
spec → triage → validate SDK → allocate → BUILD → verify → blind hold-out → blue-green deploy → notify
```

Six stages, no human in the loop. You provide the **spec** + the **hold-out scenarios** (written *before* the build). Everything else is autonomous.

---

## 1. The spec (what you must provide)

Drop a JSON file into `temporal/darkfactory/specs/inbox/`. Required fields:

| Field | Required | Example | Notes |
|---|---|---|---|
| `project_name` | ✅ | `"agentic-software"` | Must be in the ALLOWED_PRODUCTS list |
| `build_type` | ✅ | `"codegen"` | `apk` / `web` / `docker` / `codegen` |
| `source_path` | ✅ | `"/path/to/source"` | Existing code (or context for codegen) |
| `objective` | codegen only | `"write a loader that…"` | What to generate |
| `title` | no | `"Raven Character Loader"` | human-readable |
| `spec_id` | no | `"SPEC-XXX-001"` | auto-generated if absent |
| `priority` | no | `"high"` | low / normal / high / critical |
| `max_duration_minutes` | no | `90` | build timeout |

**Example (codegen):**
```json
{
  "project_name": "agentic-software",
  "build_type": "codegen",
  "source_path": "/root/.openclaw/workspace/characters/myl1ssa/Myl1Ssa/",
  "objective": "Write a runnable Python module that…",
  "priority": "high",
  "max_duration_minutes": 90
}
```

---

## 2. Build types

| Type | What it does | SDK check |
|---|---|---|
| `apk` | Gradle Android build (PWA/Bubblewrap fallback) | Android SDK |
| `web` | `npm ci && npm run build` (static-copy fallback) | Node.js |
| `docker` | `docker build` + tag | Docker |
| `codegen` | hands the `objective` to `pi` (coding agent), which writes the code | `pi` CLI |

---

## 3. The allowed product line (triage)

A spec's `project_name` must be one of these 13 (else triage rejects it):

`cobra_v1, prometheus_v1, CREAM, ReggieStarr, nognog, nomad_probe, RS-80, neon-courier, quantum-defender, laser-pistol, IC-Browser, IC-Browser-v1, agentic-software`

Rejected on keywords: `medical`, `legal`, `financial`, `autonomous deploy`, `production deploy`.

---

## 4. Hold-out scenarios (the "acceptable" gate)

For the build to pass, **every product must have pre-authored hold-out scenarios** — a blind validator checks the output against them (the builder never sees them). **All 13 products now have scenarios** in `AGI_COMPANY/subsidiaries/DARK_FACTORY/validation/hold_out_scenarios.json`.

Scenario check types:
- `artifact_present` — a glob (`*.stl`, `*.py`, `index.html`) exists in the output
- `file_exists` / `file_nonempty` / `dir_contains` / `log_contains`

**Pass = 80% weighted score.**

| Product class | Scenario pattern |
|---|---|
| Hardware (STL) | `BOM*.md` + `*.stl` |
| Web / game | `index.html` + `*.js` |
| Android app | `*.apk` |
| Python / agentic | `*.py` + a named module (`*load*.py`, `*collect*.py`) |

---

## 5. Adding a NEW product

1. Add `project_name` to `ALLOWED_PRODUCTS` in `triage_loop.py`.
2. Add hold-out scenarios to `hold_out_scenarios.json`.
3. (If codegen) ensure `objective` flows through `make_order` + `DarkFactoryOrder`.
4. Drop the spec in `specs/inbox/`.

The triage loop picks it up (cron every 30 min, or run `python3 triage_loop.py` manually).

---

## 6. Monitoring

- **Workflow status:** `python3 cli.py list` (in `temporal/darkfactory/`, with the venv).
- **Temporal UI:** `http://localhost:8233`.
- **Worker logs:** `journalctl -u darkfactory-worker`.

---

*Last updated 2026-10-09 — codegen build type + hold-out coverage for all 13 products.*
