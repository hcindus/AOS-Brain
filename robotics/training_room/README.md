# RP1 Training Room

A sandbox where our agents learn to drive the RoboParty RP1 humanoid in
simulation **before they ever touch a real robot**. CPU-first on this host
(MuJoCo runs fine without a GPU); GPU training is a plug-in socket.

## Layout

```
training_room/
  gym/            RP1GymEnv — MuJoCo sandbox (reset / step / observe / reward)
  pilots/         Pilot interface + baselines (zero, random, hold) + OllamaPilot
  agents/         roster.json — our Ollama models mapped as pilots
  graduation/     blind hold-out scoring + graduation gate (GoR council)
  dispatch/       backends — local_cpu now, gpu as a socket
  train.py        CLI (eval / graduate / roster)
```

## Quick start

```bash
cd robotics/training_room
source .venv/bin/activate

python3 train.py roster                       # who's in the gym
python3 train.py eval hold                    # naive PD-stand baseline
python3 train.py eval mort_ii                 # drive it with Mort_II
python3 train.py graduate hold                # blind hold-out -> GoR verdict
```

## How "graduate" works

1. `graduation/holdout.py` runs three **blind** scenarios (stand / walk /
   push-recovery) and scores the pilot 0..1.
2. `graduation/gate.py` passes the score to the **RiP GoR council** via the
   AOS brain socket (`/tmp/aos_brain.sock`) when it's up — a real
   GO / RESHAPE / KILL / ESCALATE verdict. Otherwise it falls back to a
   deterministic score threshold.
3. Every verdict is appended to `runs/graduation_log.jsonl`.

This is the same "blind hold-out" discipline we run on the Dark Factory:
no agent graduates on vibes.

## GPU socket

`dispatch/backend.py` defines a `TrainingBackend` with `eval` + `train`.
`LocalCPUBackend` runs here. `GPUBackend` is the interface we point at a
cloud GPU (RunPod/Lambda) or a dedicated box later — same queue, same
scoring, no re-plumbing of the gym or gate.

## Roster → models

| Pilot | Model | Role |
|-------|-------|------|
| mort_ii | antoniohudnall/Mort_II:latest | voice / sales |
| qwen35 | qwen3.5:latest | vision / multimodal |
| qwen25 | qwen2.5:14b | reasoning / control |
| deepseek | deepseek-r1:7b | reasoning |
| hermes2 | nous-hermes2:latest | general |
| tinyllama | tinyllama:latest | fast decisions |
| hold / random / zero | (baselines) | control references |
