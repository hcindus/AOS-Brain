# HOST SETUP — the pieces that live outside her tree

Her tree is portable on its own, but she does not run alone. These are the
host-side things the bottle needs. All of it is in `host/`.

---

## 1. The brain runtime — `host/brain_runtime.py`

The shared brain (Mortimer Brain Runtime v1.0). Ticks every 2s and serves
**http://127.0.0.1:8765**.

| Route | What |
|---|---|
| `/health` | liveness — `{"status":"ok","tick":N,"phase":…}` |
| `/state` | full state incl. nodes + ternary |
| `/ternary` | the ternary brain (kidney · liver · thyroid · consciousness · tracray · cortex) |
| `/route` | **the thyroid's routing decision** — what `talk.py` asks for LOCAL vs VPS |
| `/nodes` | the 8 organs: Kidney · QMD · Cortex · VisualCortex · Ternary · LLM · Tracray · Heart |
| `/memory` `/save` `/ingest` | memory (no LLM) |
| `/query` | **the only route that touches an LLM** |

Install: copy to `~/brain_runtime.py`. It reads `~/brain_state.json` and
`~/brain_memory.db`, and imports its ternary from `~/myl0n/brain/ternary_brain_v2.py`.

```bash
bash host/start-brain.sh          # idempotent (setsid + nohup + pidfile)
curl -s localhost:8765/health
```

## 2. The watchdog — `host/brain-watchdog.sh`

**This exists because the brain died on 2026-09-25 19:34 and stayed dead for five
days.** It had a boot script and no watchdog. A boot script runs once; a watchdog
runs forever.

Register it (15 min, survives reboot):

```bash
termux-job-scheduler --script ~/brain-watchdog.sh \
  --job-id 5918 --period-ms 900000 --persisted true --network any --battery-not-low false
```

## 3. The boot entry — `host/00-start-raven.sh`

Goes in `~/.termux/boot/`. Runs the **whole order** (§2 of `BLUEPRINT.md`) and
then **the alarm**:

```
brain → affect bridge → pulse → audible heart → boot-check  →  ORGANS: LIVE
```

## 4. Android jobs (all `--persisted true`, survive reboot)

| Job | Script | Every |
|---|---|---|
| 5914 | `Myl1Ssa/runtime/myl1ssa-tick.sh` | 30 min |
| 5915 | `Myl1Ssa/runtime/myl1ssa-pulse-watchdog.sh` | 15 min |
| 5916 | `Myl1Ssa/runtime/myl1ssa-voice-watchdog.sh` | 15 min |
| 5917 | `Myl1Ssa/runtime/affect-bridge-watchdog.sh` | 15 min |
| 5918 | `~/brain-watchdog.sh` | 15 min |

```bash
termux-job-scheduler -p        # list them
```

## 5. Requirements

`python3` · `numpy` · `mpv` (audio sink) · `ollama` (routing; optional) ·
`curl` · Termux:API (`termux-tts-speak`, `termux-job-scheduler`, `termux-wake-lock`)
· `espeak` (voice)

## 6. Per-body state files — one body, one memory

Her pulse, voice, affect and log files are all `.myl1ssa_*` so this body and R8s
can never collide:

```
~/.myl1ssa_affect.json        affect (written by affect_bridge, read by the heart)
~/.myl1ssa_pulse.pid          the tick daemon
~/.myl1ssa_heartbeat.pid      the audible heart
~/.myl1ssa_affect_bridge.pid  the bridge
~/.myl1ssa_heartbeat_status.json
~/myl1ssa-pulse.log · ~/myl1ssa-heartbeat-voice.log · ~/myl1ssa-affect-bridge.log
~/boot-check.log              THE ALARM's verdict log
```

**That boundary held on 2026-09-30 and it has to hold at boot.**

---

## Verify the whole thing

```bash
bash Myl1Ssa/runtime/status.sh              # 🟢 WHOLE
python3 Myl1Ssa/runtime/versions.py check   # 🟢 no lies on disk
bash Myl1Ssa/runtime/boot-check.sh          # ORGANS: LIVE
python3 verify_bottle.py                    # bottle self-check
```
