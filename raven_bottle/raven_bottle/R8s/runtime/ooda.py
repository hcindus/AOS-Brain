#!/usr/bin/env python3
"""ooda.py — Raven's OODA loop, wired to her real senses.

Boyd's Observe-Orient-Decide-Act cycle, done properly:
  1. It's an actual LOOP (tempo clock, not a single pass)
  2. Act's result FEEDS BACK into the next Observe
  3. TERNARY states (true/false/unknown) — matches BRAIN_CONFIG gate weights
  4. CORRELATION — every entry shares a cycleId + timestamp
  5. REAL SENSES — Observe samples the senses.py bridge (location, battery, etc.)

Run standalone:  python3 ooda.py [--cycles N] [--tempo SECONDS]
Import:          from ooda import OODALoop
"""

import json
import os
import sys
import time

# Import Raven's senses bridge (same directory).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import senses  # noqa: E402

HOME = os.path.expanduser("~/v1/projects/5912/R8s")

# --- Ternary state ---------------------------------------------------------
TRUE = "true"
FALSE = "false"
UNKNOWN = "unknown"


# --- OODA loop -------------------------------------------------------------
class OODALoop:
    def __init__(self, tempo=5.0, max_cycles=None, location_timeout=15):
        self.tempo = tempo            # seconds per cycle (the "tempo")
        self.max_cycles = max_cycles  # None = run forever
        self.location_timeout = location_timeout  # GPS fix timeout (slow sense)
        self.cycle = 0
        self.subcon = []              # Observe + Act (automatic)
        self.uncon = []               # Orient (deep memory / mental models)
        self.con = []                 # Decide (deliberate)
        self.state = {}               # carries forward between cycles (feedback)
        self.running = False

    # --- The four steps (each returns a payload with a ternary `state`) ----

    def observe(self, fast=False):
        """Sample the senses. Never pretend — return real data or None.

        fast=True (used by perceive, the pre-response pass) samples the quick
        senses: battery + wifi + motion (~1s). It skips location and raw
        sensors — both are slow AND leave the termux-api app in a degraded
        state that makes every later call hang. Location stays available
        on-demand via senses.location()."""
        obs = {
            "battery": senses.battery(),
            "wifi": senses.wifi(),
            "motion": senses.motion(),
        }
        if not fast:
            obs["location"] = senses.location(timeout=self.location_timeout)
            obs["sensors"] = senses.sensors()
        # Observe confidence: true if we have a GPS fix, unknown if partial,
        # false if the world is dark to us.
        if obs.get("location"):
            obs["state"] = TRUE
        elif obs.get("battery") or obs.get("wifi"):
            obs["state"] = UNKNOWN
        else:
            obs["state"] = FALSE
        return obs

    def orient(self, observations):
        """Build context from observations + prior state."""
        loc = observations.get("location")
        bat = observations.get("battery")
        motion = observations.get("motion")
        orientation = "unknown"
        if motion and motion.get("z") is not None:
            z = motion["z"]
            if z > 7:
                orientation = "flat (face up)"
            elif z < -7:
                orientation = "flat (face down)"
            else:
                orientation = "tilted/upright"
        context = {
            "summary": (
                f"at {loc.get('latitude')},{loc.get('longitude')}"
                if loc else "no position fix"
            ),
            "battery_pct": bat.get("percentage") if bat else None,
            "orientation": orientation,
            "prior_result": self.state.get("last_result", {}).get("state", UNKNOWN),
        }
        # Clear picture = true, contradictory = false, partial = unknown.
        if loc and bat:
            context["state"] = TRUE
        elif loc or bat:
            context["state"] = UNKNOWN
        else:
            context["state"] = FALSE
        return context

    def decide(self, situation):
        """The one deliberate step."""
        decision = {
            "action": "hold" if situation["state"] == TRUE else "re-orient",
            "confidence": situation["state"],
        }
        decision["state"] = TRUE if situation["state"] == TRUE else UNKNOWN
        return decision

    def act(self, decision):
        """Execute. Outcome is genuinely uncertain until observed."""
        action = decision.get("action")
        success = False
        if action == "hold":
            # A quiet, real action: confirm presence via a toast.
            success = senses.toast("🐦‍⬛ holding position")
        else:
            success = senses.toast("🐦‍⬛ re-orienting")
        return {
            "executed": action,
            "state": TRUE if success else FALSE,
        }

    # --- The loop ----------------------------------------------------------

    def step(self):
        cycle_id = self.cycle
        self.cycle += 1
        ts = time.time()
        cid = f"{cycle_id}@{int(ts * 1000)}"

        observations = self.observe()
        self.subcon.append({"cycleId": cid, "step": "Observe",
                            "data": observations, "state": observations.get("state", UNKNOWN)})

        situation = self.orient(observations)
        self.uncon.append({"cycleId": cid, "step": "Orient",
                           "context": situation, "state": situation.get("state", UNKNOWN)})

        decision = self.decide(situation)
        self.con.append({"cycleId": cid, "step": "Decide",
                         "decision": decision, "state": decision.get("state", UNKNOWN)})

        result = self.act(decision)
        self.subcon.append({"cycleId": cid, "step": "Act",
                            "action": decision, "state": result.get("state", UNKNOWN)})

        # FEEDBACK: fold the outcome into state for the next cycle.
        self.state["last_result"] = result
        self.state["last_cycle"] = cid

        return {"cycleId": cid, "observations": observations,
                "situation": situation, "decision": decision, "result": result}

    def perceive(self):
        """Observe -> Orient -> Decide, WITHOUT acting.

        A single cognitive pass — used to give Raven a live read of her
        state before she responds. The 'act' is her actual reply.
        Uses fast observe (skips slow raw sensors) to stay snappy.
        Returns a compact dict for injection into a prompt.
        """
        observations = self.observe(fast=True)
        situation = self.orient(observations)
        decision = self.decide(situation)
        return {
            "observations": observations,
            "situation": situation,
            "decision": decision,
        }

    def run(self):
        self.running = True
        while self.running and (self.max_cycles is None or self.cycle < self.max_cycles):
            t0 = time.time()
            self.step()
            elapsed = time.time() - t0
            wait = max(0.0, self.tempo - elapsed)
            if wait:
                time.sleep(wait)

    def stop(self):
        self.running = False

    # --- Persistence (Con / Subcon / Uncon) ---------------------------------

    def save(self):
        """Write the three histories to Raven's Con/Subcon/Uncon dirs."""
        for name, hist in (("Subcon", self.subcon), ("Uncon", self.uncon), ("Con", self.con)):
            path = os.path.join(HOME, name, "ooda_history.json")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                json.dump(hist, f, indent=2, default=str)
        return True

    def cycles(self):
        """Reconstruct full cycles from the three histories."""
        by_id = {}
        for e in self.subcon + self.uncon + self.con:
            by_id.setdefault(e["cycleId"], {"cycleId": e["cycleId"], "steps": []})
            by_id[e["cycleId"]]["steps"].append(e)
        return list(by_id.values())


if __name__ == "__main__":
    args = sys.argv[1:]
    tempo = 5.0
    cycles = 3
    if "--tempo" in args:
        tempo = float(args[args.index("--tempo") + 1])
    if "--cycles" in args:
        cycles = int(args[args.index("--cycles") + 1])

    loop = OODALoop(tempo=tempo, max_cycles=cycles)
    print(f"🐦‍⬛ OODA loop — {cycles} cycles @ {tempo}s tempo")
    loop.run()
    loop.save()
    print("Subconscious:", json.dumps(loop.subcon, indent=2, default=str))
    print("Unconscious:", json.dumps(loop.uncon, indent=2, default=str))
    print("Conscious:", json.dumps(loop.con, indent=2, default=str))
    print("Reconstructed cycles:", len(loop.cycles()))
