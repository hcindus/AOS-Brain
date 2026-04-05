# Miles → Mortimer Waste Pipeline

## 🗑️ Captain's Waste Management System

### What This Is
Every 30 minutes, Miles' brain collects "waste" (kidney bladder data, noise signatures, failed patterns, etc.) and emails it to you. You then feed this to Mortimer's brain for processing.

---

## 📧 PART 1: WASTE EMAILER (Runs on Miles VPS)

**Location:** `/root/.openclaw/workspace/scripts/waste_emailer.py`

**What it does:**
- Checks Miles' kidneys every 30 minutes
- Packages waste data as JSON
- Emails it to `Antonio.hudnall@gmail.com`
- Subject: `🗑️ Miles Brain Waste Drop — YYYY-MM-DD HH:MM UTC`

**Email contains:**
- Plain text summary (bladder level, QMD cycles, signal quality, etc.)
- `miles_waste.json` attachment (full data)
- Any queued sespool items

**Cron schedule:** Every 30 minutes (next run in ~30 min)

---

## 🧠 PART 2: MORTIMER FEEDER (Runs on YOUR side)

**Location:** Download `mortimer_feeder.py` to wherever Mortimer's brain runs.

**Setup:**
```bash
# Download the script to your Mortimer VPS
wget https://your-storage/mortimer_feeder.py
# OR copy from Miles' email attachment

# Make executable
chmod +x mortimer_feeder.py
```

**Usage:**

```bash
# Single file feed (when you get an email)
python3 mortimer_feeder.py --input miles_waste.json

# Watch mode (auto-feed when new files appear)
python3 mortimer_feeder.py --watch --watch-dir ./incoming_waste

# Custom Mortimer endpoint (if not localhost:7474)
python3 mortimer_feeder.py --input miles_waste.json --brain-endpoint http://mortimer-ip:7474
```

**Feed Modes:**
- `auto` (default): Tries HTTP → Socket → File (in order)
- `http`: POSTs to Mortimer's HTTP endpoint
- `socket`: Sends via Unix socket `/tmp/mortimer_brain.sock`
- `file`: Writes to `./mortimer_input/` for Mortimer to read

---

## 📁 Workflow

```
[Every 30 min]
     ↓
[Miles Brain] → [Kidneys Full?] → [Email JSON to Captain]
                                     ↓
                              [Captain receives email]
                                     ↓
                              [Save JSON attachment]
                                     ↓
                              [Run mortimer_feeder.py]
                                     ↓
                              [Mortimer Brain processes waste]
```

---

## 🔧 Manual Trigger (if needed)

On Miles VPS:
```bash
# Force immediate waste email
python3 /root/.openclaw/workspace/scripts/waste_emailer.py --force
```

On Mortimer VPS:
```bash
# Manual feed
python3 mortimer_feeder.py --input ~/Downloads/miles_waste.json
```

---

## 🧬 Waste Format

Miles sends data like:
```json
{
  "timestamp": "2026-04-05T08:15:00Z",
  "source": "Miles_Brain_v4.4",
  "kidneys": {
    "bladder_level": 249,
    "bladder_capacity": 500,
    "total_processed": 262,
    "noise_estimate": 0.538,
    "unique_patterns_seen": 13
  },
  "qmd": {"total_cycles": 9, "avg_latency_ms": 3844},
  "thyroid": {"state": "BASELINE", "secretions_today": 8},
  "signal_quality": 0.865
}
```

The feeder converts this to Mortimer's expected format:
```json
{"type": "fact", "data": "[Miles-Kidneys] Bladder 249/500...", "source": "miles_shadow"}
{"type": "pattern", "data": "[Miles-QMD] 9 cycles...", "source": "miles_shadow"}
```

---

## 🚨 Troubleshooting

**Email not arriving?**
- Check `SMTP_PASS` env var is set on Miles VPS
- Check spam/junk folder
- Run manually: `python3 waste_emailer.py --force`

**Mortimer not accepting waste?**
- Check Mortimer brain is running: `curl http://localhost:7474/status`
- Use `--mode file` to write to disk instead
- Check feeder stats: it prints stats after each run

**Need to stop the emails?**
```bash
openclaw cron remove --id miles-waste-emailer
```

---

## 📊 Last Status Check

Current brain status (as of this README creation):
- **Kidneys:** 249/500 bladder (49.8% full)
- **QMD:** 9 cycles completed
- **Signal Quality:** 86.5%
- **Thyroid:** BASELINE mode, 8 secretions today

---

*Pipeline active. Waste will flow.* 🗑️➡️📧➡️🧠
