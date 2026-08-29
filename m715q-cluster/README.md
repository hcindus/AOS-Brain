# M715q Edge Cluster — README

**Date:** 2026-08-29 · **Owner:** Captain (Antonio)

A tiny 3-node edge cluster on a 5-port switch: two Lenovo ThinkCentre M715q Gen 1 + one
ASUS Eee PC 900. Together they form a **mind / worker / body** — the seed of a physical
agent fleet (the AI Cube is the next body).

---

## Topology

```
                 ┌─────────────────────────┐
                 │      5-port switch       │
                 └────┬────────┬───────┬────┘
                      │        │       │
        ┌─────────────┴──┐  ┌──┴─────┐ ┌┴──────────────┐
        │  M715q #1       │  │M715q#2 │ │  Eee PC 900    │
        │  🧠 BRAIN        │  │⚙️ WORKER│ │  🦾 BODY        │
        │  Ollama + models │  │Dark F. │ │  split_body.py │
        │  (gemma2:2b)     │  │Temporal│ │  local hands   │
        └──────────────────┘  └────────┘ └────────────────┘
```

| Node | Role | Runs | Why |
|------|------|------|-----|
| M715q #1 | **Brain** | Ollama + `gemma2:2b` / `tinyllama` | the "mind" — serves inference over the LAN |
| M715q #2 | **Worker** | Dark Factory / Temporal / failover brain | heavy compute + redundancy |
| Eee PC 900 | **Body** | `split_body.py` | the "hands" — executes code locally, borrows a brain |

---

## The Idea (in one line)

> Give it a **brain** (remote model), a **mission** (goal), and **coding skills** (a local
> shell) — and it figures out the rest. The netbook can't host a model, so the brain lives
> on the M715q and the *hands* stay on the netbook.

The minimum seed is three things: **brain + mission + `run`**. Everything else the agent
writes itself.

---

## Files

| File | What |
|------|------|
| `PLAN.md` | original M715q build plan (Omarchy install, RAM, Tailscale) |
| `MINIMAL_AGENT.md` | full spec for the no-harness local agent |
| `bareagent.py` | standalone local agent (brain + hands on ONE machine) |
| `split_body.py` | edge body — hands local, brain remote (for the Eee PC) |

---

## Setup

### 1. Brain node (M715q #1)

```bash
# install ollama + a model
curl -fsSL https://ollama.com/install.sh | sh
ollama pull gemma2:2b

# let the LAN reach it
sudo systemctl edit ollama
#   add:  [Service]  Environment=OLLAMA_HOST=0.0.0.0
sudo systemctl restart ollama
```

### 2. Worker node (M715q #2)

- Omarchy (headless) + Pi agents (see `PLAN.md`), Dark Factory + Temporal if needed.
- Or just run a second Ollama instance as a failover brain.

### 3. Body node (Eee PC 900)

```bash
# copy split_body.py over (scp or USB), then:
BRAIN_URL=http://<m715q-1-ip>:11434 ./split_body.py "your mission"
```

> **Note:** the netbook's dead browser/TLS is irrelevant — SSH and raw HTTP over the switch
> are all the agent needs. Use Ethernet (the 900 has it).

---

## The Split Architecture (brain ⇄ body)

```
  BODY (Eee PC)                    BRAIN (M715q)
  ─────────────                    ─────────────
  run/read/write (local)           Ollama model
        │                                ▲
        │  "what do I do?"               │
        ├─────────── HTTP/SSH ──────────▶│
        │◀────────── JSON action ────────┤
        │                                │
        └── execute → send observation ─▶┘
```

Same pattern as the AI Cube: **brain remote, body at the edge.** The cube is just this with
actuators (servos/tracks) instead of a shell.

---

## Next Steps

- [ ] Confirm `gemma2:2b` runs smooth on the M715q APU (~8–12 tok/s).
- [ ] Assign static LAN IPs to all three nodes.
- [ ] Wire the Eee PC onto the switch via Ethernet + SSH keys.
- [ ] (later) point the AI Cube at M715q #1 as its dock/home-base brain.
