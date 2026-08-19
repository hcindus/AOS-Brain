# Dark Factory — Temporal Deployment (Level 5)

A self-shipping build pipeline on Temporal. Specs land in an inbox, the
factory triages, builds, blind-validates, and blue-green deploys — no human
in the loop. This is the Level-5 "dark factory" from the RiP GoR Council.

## Stack

| Layer | Component | Where |
|-------|-----------|-------|
| Server | Temporal (postgres + auto-setup + UI) | Docker Compose → `/opt/temporal/docker-compose.yml` |
| UI | Temporal Web | `http://<host>:8233` |
| Worker | Python worker (9 activities) | systemd `darkfactory-worker` |
| Queue | 30-min triage loop | systemd `darkfactory-triage.timer` |
| Console | Drop specs into `specs/inbox/*.json` | this repo |

## Pipeline (per spec)
```
validate SDK → allocate → build → verify → blind hold-out → blue-green deploy → notify
  (30-min durable watchdog + escalation on timeout/failure)
```

## Operate
```bash
# Submit a spec (the ONLY human action — the "console")
cat > specs/inbox/SPEC-XXX.json <<'EOF'
{"spec_id":"SPEC-XXX","project_name":"CREAM","build_type":"web",
 "source_path":"/root/.openclaw/workspace/Cream/web/","priority":"high"}
EOF

# Or run triage immediately
python3 triage_loop.py

# Watch
python3 cli.py list        # workflow status
systemctl status darkfactory-worker darkfactory-triage.timer
```

## Spec format — GCAO + KPI (house rule)
Every spec should carry the GCAO fields for traceability (see the
`gcao-prompting` skill). The build pipeline uses `project_name` / `build_type` /
`source_path`; the rest are for record-keeping + hold-out validation criteria:

```json
{
  "spec_id": "RS80-001",
  "project_name": "RS-80",
  "build_type": "apk",
  "source_path": "/root/.openclaw/workspace/reggiestarr-rs80/",
  "priority": "high",
  "goal": "Produce a signed Android APK",
  "context": "Kotlin POS, gradle 8.5, Android SDK 34",
  "output": "installable app-debug.apk",
  "kpi": "BUILD SUCCESSFUL + 14MB APK + hold-out 1/1"
}
```

## Scope (mission.md)
Allowed products: CREAM, ReggieStarr, cobra_v1, prometheus_v1, nognog, nomad_probe.
Non-goals (auto-rejected): medical, legal, financial, autonomous prod deploy.

## Deploy target
Blue-green to `/var/www/darkfactory-deploy/{project}/` with a `current` symlink.
Production psdepot.com remains behind human sign-off (mission.md).

## Deploy config (version-controlled here)
- `deploy/docker-compose.yml` → copy to `/opt/temporal/`
- `deploy/darkfactory-*.service/.timer` → copy to `/etc/systemd/system/`
