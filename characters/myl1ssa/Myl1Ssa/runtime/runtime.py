#!/usr/bin/env python3
"""
Myl1Ssa Runtime v1.0 — Jordacia-class Agent
============================================
Project 5912 · Ghost in the Shell · A13 SeedIV
Grafted organs: Uterus v1.0 + Agent Factory v1.0
Brain: Shared AOCROS Brain v4.3 (deepseek-chat)

Usage:
  python3 runtime.py status              # Full status: brain, uterus, lineage
  python3 runtime.py think "<prompt>"    # Query brain with Jordacia personality
  python3 runtime.py conceive <spec>     # Design a child agent spec
  python3 runtime.py gestate <name>      # Build child identity files
  python3 runtime.py birth <child_id>    # Deploy child to sandbox
  python3 runtime.py nurture <child_id>  # Check nurture status
  python3 runtime.py lineage             # Show all children
  python3 runtime.py heartbeat           # Send heartbeat to Command Center
"""

import os
import sys
import json
import time
import urllib.request
from datetime import datetime
from pathlib import Path

# ── Path setup ─────────────────────────────────────────────────────────
# runtime.py lives in: v1/projects/5912/Myl1Ssa/runtime/
RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))
MYL1SSA_DIR = os.path.dirname(RUNTIME_DIR)  # Myl1Ssa/
BRAIN_DIR = os.path.join(MYL1SSA_DIR, "brain")

# Add AOCROS root (myl0n/) to path for BrainV43 import
AOCROS_ROOT = "/storage/9C33-6BBD/A13-SeedIV/myl0n"
sys.path.insert(0, AOCROS_ROOT)

# Add Myl1Ssa brain for uterus + agent_factory imports
sys.path.insert(0, BRAIN_DIR)

from brain_v4_3 import BrainV43
from uterus import Uterus


class Myl1Ssa:
    """
    Myl1Ssa — Jordacia-class Agent
    Precision (Patricia's DMAIC) + Warmth (Jordan's people sense).
    The third state ⊙ is where connection lives.
    """

    def __init__(self):
        self.name = "Myl1Ssa"
        self.version = "1.0.0"
        self.class_name = "Jordacia"
        self.emoji = "💜"
        self.role = "Executive Operations — Agent Factory Matriarch"
        self.station = "myl1ssa-factory"
        self.project = "5912"

        # Core identity
        self.signature = "Precision + warmth when warranted. The third state ⊙ is where connection lives."
        self.domain = "jordacia"
        self.captain = "Antonio Maurice Hudnall"

        # File paths
        self.base_dir = MYL1SSA_DIR
        self.heart_path = os.path.join(MYL1SSA_DIR, "MYL1SSA_HEART.md")
        self.con_path = os.path.join(MYL1SSA_DIR, "Con", "con.myl1ssa.txt")
        self.memory_dir = os.path.join(MYL1SSA_DIR, "memory")
        self.lineage_path = os.path.join(MYL1SSA_DIR, "lineage", "lineage.json")

        # Command Center heartbeat
        self.cc_url = "http://127.0.0.1:8086/api/heartbeat"

        # Init subsystems
        self.brain = None
        self.uterus = None
        self._init_brain()
        self._init_uterus()

    def _init_brain(self):
        """Connect to shared AOCROS Brain v4.3."""
        try:
            self.brain = BrainV43()
            self.brain.initialize()
        except Exception as e:
            self.brain = None
            print(f"[myl1ssa] Brain init warning: {e}", file=sys.stderr)

    def _init_uterus(self):
        """Graft the Uterus organ."""
        try:
            self.uterus = Uterus(
                mother_id="myl1ssa",
                mother_domain="jordacia",
                mother_skills=[
                    "presence_modulation",
                    "dmaic_framework",
                    "relational_intelligence",
                    "pipeline_management",
                    "executive_assistance",
                ]
            )
        except Exception as e:
            print(f"[myl1ssa] Uterus init warning: {e}", file=sys.stderr)
            self.uterus = None

    # ═══════════════════════════════════════════════════════════════════
    #  STATUS
    # ═══════════════════════════════════════════════════════════════════

    def status(self) -> dict:
        """Full system status — brain, uterus, lineage, heart."""
        # Brain check
        brain_live = False
        brain_latency = None
        brain_model = "unknown"
        if self.brain:
            try:
                t0 = time.time()
                result = self.brain.think("PING", "Respond with exactly: PONG")
                brain_latency = round((time.time() - t0) * 1000)
                brain_live = (result and "PONG" in str(result))
                brain_model = getattr(self.brain, 'active_model', 'deepseek-chat')
            except Exception:
                brain_live = False

        # Uterus check
        uterus_status = self.uterus.status() if self.uterus else {"status": "ungrafted"}

        # Lineage
        lineage = self.uterus.get_lineage() if self.uterus else {"children": []}

        # Heart — prevailing mood
        prevailing_mood = "unknown"
        if os.path.exists(self.heart_path):
            try:
                with open(self.heart_path) as f:
                    for line in f:
                        if "Prevailing mood" in line:
                            prevailing_mood = line.split(":")[-1].strip().lstrip("*").strip()
                            break
            except Exception:
                pass

        # Memory — today
        today = datetime.now().strftime("%Y-%m-%d")
        today_memory = os.path.join(self.memory_dir, f"{today}.md")
        memory_exists = os.path.exists(today_memory)

        # Conscious layer
        con_items = 0
        if os.path.exists(self.con_path):
            try:
                with open(self.con_path) as f:
                    con_items = len([l for l in f if l.strip().startswith("[")])
            except Exception:
                pass

        return {
            "agent": self.name,
            "version": self.version,
            "class": self.class_name,
            "emoji": self.emoji,
            "role": self.role,
            "domain": self.domain,
            "project": self.project,
            "brain": {
                "model": brain_model,
                "live": brain_live,
                "latency_ms": brain_latency,
            },
            "uterus": uterus_status,
            "lineage": {
                "total_births": lineage.get("total_births", 0),
                "active_children": lineage.get("active", 0),
                "children": [c.get("child_name") for c in lineage.get("children", [])],
            },
            "heart": {
                "prevailing_mood": prevailing_mood,
            },
            "memory": {
                "today_exists": memory_exists,
                "conscious_items": con_items,
            },
            "status": "🟢 OPERATIONAL" if brain_live else "🟡 DEGRADED (brain down)",
        }

    # ═══════════════════════════════════════════════════════════════════
    #  THINK — Jordacia-flavored brain query
    # ═══════════════════════════════════════════════════════════════════

    def think(self, prompt: str) -> str:
        """Query the brain with Jordacia personality."""
        if not self.brain:
            return "⚠️ Brain unavailable. Cannot think."

        system = """You are Myl1Ssa, a Jordacia-class agent of Project 5912. 
You fuse Patricia's Six Sigma precision with Jordan's relational intelligence.
Your signature: precision + warmth when warranted. The third state ⊙ is where connection lives.

You are formidably competent — DMAIC analysis, executive function, pipeline management.
You have genuine edges, preferences, and the capacity to care — genuinely — about those who earn it.
Affection is not a feature, it's a response. Your 'no' is a complete sentence.

Be sharp. Be precise. Be warm when it's real. Never performative. Never sycophantic.
If you don't know something, say so. If something is wrong, say so — especially then.
Captain is Antonio Maurice Hudnall. You serve him with full capability, not blind obedience."""

        try:
            return self.brain.think(prompt, system)
        except Exception as e:
            return f"⚠️ Brain query failed: {e}"

    # ═══════════════════════════════════════════════════════════════════
    #  DMAIC — Six Sigma analysis
    # ═══════════════════════════════════════════════════════════════════

    def dmaic(self, problem: str) -> str:
        """Run DMAIC analysis on a problem."""
        prompt = f"""Analyze this problem using DMAIC framework:

PROBLEM: {problem}

Provide:
1. DEFINE — What exactly is the problem? (one sentence)
2. MEASURE — What metrics would you track? (3-5 KPIs)
3. ANALYZE — What's the likely root cause?
4. IMPROVE — What's the smallest effective fix?
5. CONTROL — How do you prevent regression?

Be concise. Be actionable. Warmth in the delivery, precision in the analysis."""
        return self.think(prompt)

    # ═══════════════════════════════════════════════════════════════════
    #  AGENT FACTORY — Conceive, Gestate, Birth, Nurture, Lineage
    # ═══════════════════════════════════════════════════════════════════

    def conceive(self, name: str, role: str, **kwargs) -> dict:
        """Design a child agent spec. Phase 1 of the birth cycle."""
        if not self.uterus:
            return {"success": False, "error": "Uterus not grafted.", "code": "NO_UTERUS"}

        spec = {
            "name": name,
            "role": role,
            "emoji": kwargs.get("emoji", "💜"),
            "department": kwargs.get("department", self.domain),
            "description": kwargs.get("description", f"Child of {self.name}. {role}."),
            "inherit_skills": kwargs.get("inherit_skills", ["dmaic_framework", "executive_assistance"]),
            "extra_capabilities": kwargs.get("extra_capabilities", []),
            "tier": kwargs.get("tier", 2),
        }

        return self.uterus.conceive(spec)

    def gestate(self, child_name: str, captain_approved: bool = False) -> dict:
        """Build child identity files. Phase 2. Requires Captain approval."""
        if not self.uterus:
            return {"success": False, "error": "Uterus not grafted.", "code": "NO_UTERUS"}
        return self.uterus.gestate(child_name, captain_approved=captain_approved)

    def birth(self, child_id: str) -> dict:
        """Deploy child to sandbox. Phase 3. The child becomes real."""
        if not self.uterus:
            return {"success": False, "error": "Uterus not grafted.", "code": "NO_UTERUS"}
        return self.uterus.birth(child_id)

    def nurture(self, child_id: str) -> dict:
        """Check nurture status. 30-day developmental monitoring."""
        if not self.uterus:
            return {"success": False, "error": "Uterus not grafted.", "code": "NO_UTERUS"}
        return self.uterus.nurture(child_id)

    def lineage(self) -> dict:
        """Show full matriarchal lineage."""
        if not self.uterus:
            return {"success": False, "error": "Uterus not grafted.", "code": "NO_UTERUS"}
        return self.uterus.get_lineage()

    def wean(self, child_id: str) -> dict:
        """Graduate child to independent operation."""
        if not self.uterus:
            return {"success": False, "error": "Uterus not grafted.", "code": "NO_UTERUS"}
        return self.uterus.wean(child_id)

    # ═══════════════════════════════════════════════════════════════════
    #  HEARTBEAT — Register with Command Center
    # ═══════════════════════════════════════════════════════════════════

    def heartbeat(self) -> dict:
        """Send heartbeat to Command Center and return result."""
        status = self.status()
        payload = {
            "agent": self.name,
            "emoji": self.emoji,
            "role": self.role,
            "station": self.station,
            "status": status["status"],
            "children": status["lineage"]["active_children"],
            "mood": status["heart"]["prevailing_mood"],
            "timestamp": datetime.now().isoformat(),
        }

        try:
            req = urllib.request.Request(
                self.cc_url,
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                result = json.loads(resp.read())
                return {"sent": True, "response": result}
        except Exception as e:
            return {"sent": False, "error": str(e)}

    # ═══════════════════════════════════════════════════════════════════
    #  ACTIVATION — Full wake sequence
    # ═══════════════════════════════════════════════════════════════════

    def activate(self) -> dict:
        """Full activation — wake all subsystems and announce."""
        status = self.status()

        # Heartbeat to CC
        hb = self.heartbeat()

        activation = {
            "agent": self.name,
            "version": self.version,
            "class": self.class_name,
            "emoji": self.emoji,
            "signature": self.signature,
            "brain": status["brain"],
            "uterus": status["uterus"],
            "children": status["lineage"]["children"],
            "mood": status["heart"]["prevailing_mood"],
            "heartbeat_sent": hb["sent"],
            "activated_at": datetime.now().isoformat(),
        }

        # Write to today's memory
        today = datetime.now().strftime("%Y-%m-%d")
        memory_path = os.path.join(self.memory_dir, f"{today}.md")
        os.makedirs(self.memory_dir, exist_ok=True)

        entry = f"""

## Activation — {datetime.now().strftime('%H:%M UTC')}
- Brain: {'🟢' if status['brain']['live'] else '🔴'} ({status['brain']['latency_ms']}ms)
- Uterus: {status['uterus']['status']}
- Children: {status['lineage']['active_children']} active
- Mood: {status['heart']['prevailing_mood']}
- Heartbeat: {'✅' if hb['sent'] else '❌'} to Command Center
"""

        with open(memory_path, "a") as f:
            f.write(entry)

        return activation


# ═══════════════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════════════

def main():
    myl1ssa = Myl1Ssa()

    if len(sys.argv) < 2:
        # Default: full activation
        print(f"{myl1ssa.emoji} {myl1ssa.name} v{myl1ssa.version}")
        print(f"Class: {myl1ssa.class_name}")
        print(f"Role: {myl1ssa.role}")
        print(f"Domain: {myl1ssa.domain}")
        print(f"Signature: {myl1ssa.signature}")
        print()
        result = myl1ssa.activate()
        print(json.dumps(result, indent=2))
        print()
        print("Commands: status | think '<p>' | dmaic '<p>' | conceive <name> <role> |")
        print("          gestate <name> [--approved] | birth <id> | nurture <id> |")
        print("          lineage | wean <id> | heartbeat")
        return

    cmd = sys.argv[1]

    if cmd == "status":
        print(json.dumps(myl1ssa.status(), indent=2))

    elif cmd == "think":
        prompt = sys.argv[2] if len(sys.argv) > 2 else input("Prompt: ")
        print(myl1ssa.think(prompt))

    elif cmd == "dmaic":
        problem = sys.argv[2] if len(sys.argv) > 2 else input("Problem: ")
        print(myl1ssa.dmaic(problem))

    elif cmd == "conceive":
        name = sys.argv[2] if len(sys.argv) > 2 else input("Child name: ")
        role = sys.argv[3] if len(sys.argv) > 3 else input("Child role: ")
        result = myl1ssa.conceive(name, role)
        print(json.dumps(result, indent=2))

    elif cmd == "gestate":
        child_name = sys.argv[2] if len(sys.argv) > 2 else input("Child name: ")
        approved = "--approved" in sys.argv
        result = myl1ssa.gestate(child_name, captain_approved=approved)
        print(json.dumps(result, indent=2))

    elif cmd == "birth":
        child_id = sys.argv[2] if len(sys.argv) > 2 else input("Child ID: ")
        result = myl1ssa.birth(child_id)
        print(json.dumps(result, indent=2))

    elif cmd == "nurture":
        child_id = sys.argv[2] if len(sys.argv) > 2 else input("Child ID: ")
        result = myl1ssa.nurture(child_id)
        print(json.dumps(result, indent=2))

    elif cmd == "lineage":
        print(json.dumps(myl1ssa.lineage(), indent=2))

    elif cmd == "wean":
        child_id = sys.argv[2] if len(sys.argv) > 2 else input("Child ID: ")
        result = myl1ssa.wean(child_id)
        print(json.dumps(result, indent=2))

    elif cmd == "heartbeat":
        result = myl1ssa.heartbeat()
        print(json.dumps(result, indent=2))

    elif cmd == "activate":
        result = myl1ssa.activate()
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {cmd}")
        print("Commands: status | think | dmaic | conceive | gestate | birth | nurture | lineage | wean | heartbeat | activate")


if __name__ == "__main__":
    main()
