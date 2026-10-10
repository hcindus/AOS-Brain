# Cyberdeck Agent Startup — systemd + health check

*Auto-register the Pi agent on boot and report node status over the tailnet. Per-node, drop these two files on each M715q.*

---

## 1. systemd service — `/etc/systemd/system/pi-agent.service`

```ini
[Unit]
Description=Pi coding agent (auto-register + health check)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
ExecStartPre=/usr/local/bin/pi-agent-healthcheck.sh pre
ExecStart=/usr/bin/pi --print --no-session "Register with the task queue and wait for work."
ExecStartPost=/usr/local/bin/pi-agent-healthcheck.sh check
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable it:
```bash
sudo systemctl enable --now pi-agent.service
```

---

## 2. Health check — `/usr/local/bin/pi-agent-healthcheck.sh`

```bash
#!/bin/bash
# Health check + status report for the Pi agent. Writes JSON status to a local
# file, and (optionally) pushes it to a shared node over Tailscale.
set -u
NODE="$(hostname)"
STATUS_DIR="/var/lib/pi-agent"
STATUS_FILE="$STATUS_DIR/status.json"
REMOTE_NODE="${1:-}"          # optional peer to scp status to (Tailscale hostname)

mkdir -p "$STATUS_DIR"

case "${MODE:-check}" in
  pre)
    printf '{"node":"%s","state":"starting","boot":"%s"}\n' "$NODE" "$(date -Is)" > "$STATUS_FILE"
    ;;
  check)
    if pgrep -f "pi --print" >/dev/null 2>&1; then
      printf '{"node":"%s","state":"running","ts":"%s"}\n' "$NODE" "$(date -Is)" > "$STATUS_FILE"
      rc=0
    else
      printf '{"node":"%s","state":"down","ts":"%s"}\n' "$NODE" "$(date -Is)" > "$STATUS_FILE"
      rc=1
    fi
    # optionally report to a peer node over the tailnet
    if [ -n "$REMOTE_NODE" ]; then
      scp "$STATUS_FILE" "root@$REMOTE_NODE:/var/lib/pi-agent/peers/$NODE.json" >/dev/null 2>&1 || true
    fi
    exit $rc
    ;;
esac
```

Make it executable:
```bash
sudo chmod +x /usr/local/bin/pi-agent-healthcheck.sh
```

---

## 3. Periodic check (so "down" is noticed)

A small systemd timer runs the check every minute and, on failure, restarts the service:

```ini
# /etc/systemd/system/pi-agent-healthcheck.timer
[Unit]
Description=Run pi-agent health check every minute

[Timer]
OnBootSec=1min
OnUnitActiveSec=1min

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/pi-agent-healthcheck.service
[Unit]
Description=Pi agent health check

[Service]
Type=oneshot
Environment=MODE=check
ExecStart=/usr/local/bin/pi-agent-healthcheck.sh
```

```bash
sudo systemctl enable --now pi-agent-healthcheck.timer
```

---

## What this gives you

- **Boot → auto-register** — the agent starts on boot, registers with the task queue, no manual step.
- **Restart on crash** — `Restart=on-failure` keeps it alive.
- **Visible status** — each node writes `status.json`; the timer catches "down" and restarts.
- **Tailnet awareness** — optionally `scp` status to a peer so one node knows the health of the other.

---

## 4. Auto-update (weekly, from Copilot's suggestion)

A weekly systemd timer pulls the latest agent so nodes self-update:

```ini
# /etc/systemd/system/pi-agent-update.timer
[Unit]
Description=Weekly Pi agent update

[Timer]
OnCalendar=Mon *-*-* 03:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/pi-agent-update.service
[Unit]
Description=Update the Pi agent
After=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/pi update self
# or, if you version the agent config in git:
# ExecStart=/usr/bin/git -C /opt/pi-agent pull

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now pi-agent-update.timer
```

**Note on the agent binary:** Copilot's draft referenced `/usr/local/bin/pi-agent --config /etc/pi-agent/config.yaml`. Our real agent is the **`pi` CLI** (`/usr/bin/pi --print`), and we don't yet have a monitoring endpoint — so the health "heartbeat" is local `status.json` + optional peer `scp` over the tailnet (no external `curl` endpoint needed). If we later stand up a monitoring service, swap the local file for a `curl` POST.

*Two nodes, one tailnet, self-healing, self-updating, reporting. A proper little fleet.*
