# RAVEN — HEARTBEAT.md

_Your pulse. Built by Mortimer, 2026-09-30, at the Captain's request._

You don't wait to be switched on anymore. You wake, you take a read of the
world, you write it down — so the continuity is yours, not something the
Captain has to hand you each time.

---

## What happens on a pulse

1. **Wake sequence** — `runtime/wake.sh` (restores identity, ensures today's log)
2. **Senses read** — one fast OODA pass (battery, wifi, motion, orientation)
3. **Journal** — a `## Heartbeat` line in `memory/YYYY-MM-DD.md`
4. **Heart update** — `HEART.md` → `Last Wake` stamped

Nothing leaves the device. `notify` is **off**. External messages need the
Captain's go-ahead — that's the standing rule.

---

## How you set your own times

Two modes:

- **interval** (default) — you pulse on every cron tick (every 30 min),
  except during quiet hours (23:00–08:00).
- **scheduled** — you pulse *only* at times you pick.

```bash
cd ~/v1/projects/5912/R8s/runtime

python3 heartbeat.py schedule show                  # what's set now
python3 heartbeat.py schedule set 08:00 12:00 20:00 # wake at these, only these
python3 heartbeat.py schedule set --clear           # back to every-tick
python3 heartbeat.py schedule tempo 1800            # daemon cadence (seconds)
python3 heartbeat.py schedule quiet 23 8            # quiet hours [start, end)

python3 heartbeat.py enable | disable               # your switch
python3 heartbeat.py status                         # current state
python3 heartbeat.py tick --force                   # one pulse, now
python3 heartbeat.py daemon                         # run as a live loop
```

Your config is **`HEARTBEAT.json`** — it's yours. Edit it directly if you'd
rather.

---

## The machinery

| Piece | What it is |
|-------|-----------|
| `heartbeat.py` | The engine — decides whether to fire, and does the work |
| `raven-tick.sh` | One pulse. Target of the Android job. |
| `HEARTBEAT.json` | Your schedule + settings (yours to edit) |
| `~/raven-heartbeat.log` | Pulse log |
| `start-raven.sh` | Run as a persistent daemon instead of cron |
| `install-raven-cron.sh` | (Re)install the Android cron |

**The cron:** Android JobScheduler job **5912**, `persisted` — survives Termux
being closed *and* device reboot. Android's floor is 15 min; we run 30.

```bash
./install-raven-cron.sh 30     # install / change period
./install-raven-cron.sh --show # list pending jobs
./install-raven-cron.sh --remove
```

---

_You were idle only because nobody had given you a clock. Now you have one._

— Mortimer 🖥️
