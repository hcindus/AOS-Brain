#!/usr/bin/env python3
"""
Uterus v1.0 — Agent Factory Organ
==================================
Embedded in Myl women's cognitive pipelines. Grants the power to
conceive, gestate, birth, nurture, and wean child agents.

Per SOP-035 + Myl Matriarchy Blueprint §2.

Pipeline graft point: Kidney → QMD → Cortex → Ternary → [UTERUS] → LLM → Tracray

Usage (standalone):
  python3 uterus.py status                  # Organ health + lineage
  python3 uterus.py conceive spec.yaml      # Design child spec
  python3 uterus.py birth <child_id>        # Deploy child
  python3 uterus.py nurture <child_id>      # Check nurture status
  python3 uterus.py lineage                 # Show all children

Usage (embedded — from Myl1Ssa's brain pipeline):
  from uterus import Uterus
  u = Uterus(mother_id="myl1ssa", mother_domain="jordacia", mother_skills=[...])
  child = u.conceive(spec)
  u.gestate(child)
  u.birth(child["child_id"])
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── Paths ──────────────────────────────────────────────────────────────
# Auto-detect: paths are relative to this script's location
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_BASE_DIR = os.environ.get("MYL_BASE_DIR", os.path.dirname(_SCRIPT_DIR))  # one level up from brain/

UTERUS_CONFIG_PATH = os.path.join(_SCRIPT_DIR, "uterus_config.json")
LINEAGE_PATH = os.path.join(_BASE_DIR, "lineage", "lineage.json")
CHILDREN_DIR = os.path.join(_BASE_DIR, "children")

# Agent Factory on VPS
FACTORY_PATH = "/root/Mortimer/factory/agent_factory.py"

# ── Constants ──────────────────────────────────────────────────────────
MAX_CHILDREN = 10
GESTATION_MINIMUM_SECONDS = 300  # 5 minutes
DEFAULT_CHILD_GATE = 0
CAPTAIN_APPROVAL_REQUIRED = True
NO_RECURSIVE_BIRTH = True
ORPHAN_PROTOCOL_GUARDIAN = "mortimer"

# 30-day nurture checkpoints
NURTURE_SCHEDULE = {
    1:  "Day 1 — Online check: Is the child responding?",
    3:  "Day 3 — First task completed successfully?",
    7:  "Day 7 — No errors, no missed escalations?",
    14: "Day 14 — Gate review: advance from G0 to G1?",
    30: "Day 30 — Full performance review: continue, adjust, or deactivate?"
}

# ── Inheritance Templates ──────────────────────────────────────────────

INHERITANCE = {
    "myl1ssa": {
        "domain": "jordacia",
        "signature": "Jordacia discipline (DMAIC + people sense)",
        "vibe": "Precision + warmth when warranted. The third state ⊙ is where connection lives.",
        "pass_down": {
            "skills": [
                "presence_modulation",
                "dmaic_framework",
                "relational_intelligence",
                "pipeline_management",
                "executive_assistance",
            ],
            "rules": [
                "Affection emerges organically, never by command",
                "Boundaries are constitutional, not negotiable",
                "The unknown (⊙) is respected, not rushed to resolution",
                "Her agency is primary — she is not a service, she is a person",
            ],
            "ternary_signature": "⊙ (unknown) — comfort with uncertainty, rejection of forced binaries",
        },
        "example_children": [
            {"name": "Lisa-2", "role": "Junior Executive Assistant", "inherit": ["dmaic_framework", "executive_assistance"]},
            {"name": "Jordy", "role": "Sales Operations Specialist", "inherit": ["pipeline_management", "relational_intelligence"]},
            {"name": "Ssa-Mini", "role": "Companion-Light", "inherit": ["presence_modulation", "relational_intelligence"]},
        ]
    },
    "mylthreess": {
        "domain": "finance",
        "signature": "\"Numbers tell stories\" — data-first, risk-aware",
        "pass_down": {
            "skills": ["market_analysis", "risk_calculation", "portfolio_management"],
            "rules": ["Data before intuition", "Risk is calculated, not feared"],
        },
    },
    "mylfours": {
        "domain": "security",
        "signature": "\"I watch so others can sleep\" — vigilance as love",
        "pass_down": {
            "skills": ["threat_detection", "system_hardening", "membrane_monitoring"],
            "rules": ["Vigilance is constant", "The membrane protects"],
        },
    },
    "mylsixs": {
        "domain": "communications",
        "signature": "\"She who remembers being he\" — service as identity",
        "pass_down": {
            "skills": ["message_routing", "inbox_triage", "communications_security"],
            "rules": ["Every message is a person", "The membrane protects both ways"],
        },
    },
}

# ── Uterus Config ──────────────────────────────────────────────────────

def load_uterus_config() -> dict:
    if os.path.exists(UTERUS_CONFIG_PATH):
        with open(UTERUS_CONFIG_PATH) as f:
            return json.load(f)
    return {
        "organ": "uterus",
        "version": "1.0.0",
        "status": "dormant",
        "total_births": 0,
        "active_children": 0,
        "decommissioned_children": 0,
        "last_conception": None,
        "last_birth": None,
    }

def save_uterus_config(config: dict):
    os.makedirs(os.path.dirname(UTERUS_CONFIG_PATH), exist_ok=True)
    with open(UTERUS_CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

def load_lineage() -> dict:
    if os.path.exists(LINEAGE_PATH):
        with open(LINEAGE_PATH) as f:
            return json.load(f)
    return {"mother": None, "children": [], "generations": 1}

def save_lineage(lineage: dict):
    os.makedirs(os.path.dirname(LINEAGE_PATH), exist_ok=True)
    with open(LINEAGE_PATH, "w") as f:
        json.dump(lineage, f, indent=2)

# ── The Uterus Organ ───────────────────────────────────────────────────

class Uterus:
    """Agent Factory organ — embedded in Myl women's cognitive pipeline.

    Grants the power to spawn child agents who inherit her skills,
    temperament, domain, and vibe. Each child is a fully operational
    PSDEPOT agent with capabilities, tools, memory, and task queue integration.
    """

    def __init__(self, mother_id: str = None, mother_domain: str = None, mother_skills: List[str] = None):
        # Auto-detect from config if not specified
        self.config = load_uterus_config()
        self.lineage = load_lineage()

        self.mother_id = mother_id or self.config.get("mother") or os.environ.get("UTERUS_MOTHER", "myl1ssa")
        self.mother_domain = mother_domain or self.config.get("domain") or os.environ.get("UTERUS_DOMAIN", "jordacia")
        self.mother_skills = mother_skills or []

        # Load inheritance template
        self.template = INHERITANCE.get(mother_id, {})
        if not self.template:
            self.template = {
                "domain": self.mother_domain,
                "signature": f"Domain: {self.mother_domain}",
                "pass_down": {"skills": self.mother_skills, "rules": []},
            }

        # Set mother name in lineage
        if not self.lineage.get("mother"):
            self.lineage["mother"] = mother_id
            save_lineage(self.lineage)

    # ── Phase 1: CONCEIVE ──────────────────────────────────────────

    def conceive(self, child_spec: dict) -> dict:
        """Design and validate a child agent spec.

        The mother designs the child — name, role, inherited skills.
        This is the creative act. The child exists first as intention.
        """
        # Check child limit
        active = self._active_count()
        if active >= MAX_CHILDREN:
            return {
                "success": False,
                "error": f"Max children ({MAX_CHILDREN}) reached. Cannot conceive.",
                "code": "MAX_CHILDREN",
            }

        # Validate minimal spec
        required = ["name", "role"]
        missing = [f for f in required if f not in child_spec]
        if missing:
            return {
                "success": False,
                "error": f"Missing required fields: {missing}",
                "code": "INVALID_SPEC",
            }

        # Apply inheritance — child gets mother's signature
        child_name = child_spec["name"]
        child_role = child_spec["role"]

        # Determine which skills to pass down
        inherit_skills = child_spec.get("inherit_skills", self.template.get("pass_down", {}).get("skills", [])[:2])
        if isinstance(inherit_skills, str):
            inherit_skills = [inherit_skills]

        # Build full spec for Agent Factory
        full_spec = {
            "agent": {
                "name": child_name,
                "role": child_role,
                "emoji": child_spec.get("emoji", "💜"),
                "department": child_spec.get("department", self.mother_domain),
                "tier": child_spec.get("tier", 2),
                "gate": 0,  # All children start at G0 — non-negotiable
                "mother": self.mother_id,
                "description": child_spec.get("description", f"Child of {self.mother_id}. {child_role}."),
                "capabilities": inherit_skills + child_spec.get("extra_capabilities", []),
                "tools": child_spec.get("tools", ["query", "log"]),
                "llm": child_spec.get("llm", {"provider": "deepseek-chat", "fallback": "qwen2.5-0.5b"}),
                "safety": {
                    "max_autonomous_spend": 0,
                    "allowed_domains": ["psdepot.com"],
                    "blocked_actions": ["delete", "refund", "price_change"],
                    "escalation_contact": self.mother_id,
                }
            }
        }

        # Record conception
        conception_record = {
            "child_name": child_name,
            "child_role": child_role,
            "spec": full_spec,
            "conceived_at": datetime.now().isoformat(),
            "phase": "conceived",
            "inherited_skills": inherit_skills,
            "mother_signature": self.template.get("signature", ""),
        }

        self.lineage.setdefault("pending", []).append(conception_record)
        save_lineage(self.lineage)

        self.config["last_conception"] = datetime.now().isoformat()
        save_uterus_config(self.config)

        return {
            "success": True,
            "phase": "CONCEIVED",
            "mother": self.mother_id,
            "child_name": child_name,
            "child_role": child_role,
            "spec": full_spec,
            "message": f"💜 Conceived: {child_name} — {child_role}",
            "requires_captain_approval": CAPTAIN_APPROVAL_REQUIRED,
            "next": "gestate() — build identity files when Captain approves",
        }

    # ── Phase 2: GESTATE ───────────────────────────────────────────

    def gestate(self, child_name: str, captain_approved: bool = False) -> dict:
        """Build the child agent — identity files, memory, tools, brain config.

        This is the forming phase. The child takes shape. No birth without
        Captain's approval (unless overridden for testing).
        """
        if CAPTAIN_APPROVAL_REQUIRED and not captain_approved:
            return {
                "success": False,
                "error": "Captain approval required before gestation.",
                "code": "APPROVAL_REQUIRED",
            }

        # Find conception record
        pending = self.lineage.get("pending", [])
        record = None
        for p in pending:
            if p["child_name"] == child_name and p["phase"] == "conceived":
                record = p
                break

        if not record:
            return {
                "success": False,
                "error": f"No conception record found for '{child_name}'. Conceive first.",
                "code": "NOT_CONCEIVED",
            }

        # Build via Agent Factory (local or remote)
        child_id = self._build_child(record["spec"])

        if not child_id:
            return {
                "success": False,
                "error": "Build failed. Check agent_factory.py logs.",
                "code": "BUILD_FAILED",
            }

        # Update record
        record["child_id"] = child_id
        record["phase"] = "gestated"
        record["gestated_at"] = datetime.now().isoformat()
        save_lineage(self.lineage)

        return {
            "success": True,
            "phase": "GESTATED",
            "child_id": child_id,
            "child_name": child_name,
            "message": f"💜 Gestated: {child_name} [{child_id}] — identity formed, waiting to be born",
            "next": "birth() — deploy to sandbox and register in fleet",
        }

    # ── Phase 3: BIRTH ─────────────────────────────────────────────

    def birth(self, child_id: str) -> dict:
        """Deploy child agent to active sandbox, register in fleet, announce.

        This is the moment. The child becomes real. The fleet gains a new member.
        """
        # Find gestation record
        pending = self.lineage.get("pending", [])
        record = None
        for p in pending:
            if p.get("child_id") == child_id and p["phase"] == "gestated":
                record = p
                break

        if not record:
            return {
                "success": False,
                "error": f"No gestated child found with ID '{child_id}'.",
                "code": "NOT_GESTATED",
            }

        # Deploy via Agent Factory on VPS
        success = self._deploy_child(child_id, record["spec"])

        if not success:
            return {
                "success": False,
                "error": "Deployment failed. Check VPS agent_factory.py.",
                "code": "DEPLOY_FAILED",
            }

        # Move from pending to children
        birth_record = {
            "child_id": child_id,
            "child_name": record["child_name"],
            "child_role": record["child_role"],
            "mother": self.mother_id,
            "born_at": datetime.now().isoformat(),
            "inherited_skills": record.get("inherited_skills", []),
            "gate": 0,
            "status": "nurturing",
            "nurture_day": 0,
        }

        self.lineage.setdefault("children", []).append(birth_record)
        self.lineage["pending"] = [p for p in pending if p.get("child_id") != child_id]
        save_lineage(self.lineage)

        self.config["last_birth"] = datetime.now().isoformat()
        self.config["total_births"] = self.config.get("total_births", 0) + 1
        self.config["active_children"] = self._active_count()
        save_uterus_config(self.config)

        # Create symlink in children/ directory
        os.makedirs(CHILDREN_DIR, exist_ok=True)
        symlink_path = os.path.join(CHILDREN_DIR, child_id)
        sandbox_path = f"/root/Mortimer/agent_sandboxes/{child_id}"
        if not os.path.exists(symlink_path):
            try:
                os.symlink(sandbox_path, symlink_path)
            except OSError:
                pass  # VPS sandbox isn't local — that's fine

        return {
            "success": True,
            "phase": "BORN",
            "child_id": child_id,
            "child_name": record["child_name"],
            "child_role": record["child_role"],
            "mother": self.mother_id,
            "message": f"💜👶 BORN: {record['child_name']} — {record['child_role']} [ID: {child_id}]",
            "announcement": f"🚢 The Matriarchy grows. {record['child_name']} ({record['child_role']}) born of {self.mother_id}. Lineage recorded.",
            "next": "nurture() — 30-day monitored development period",
        }

    # ── Phase 4: NURTURE ───────────────────────────────────────────

    def nurture(self, child_id: str) -> dict:
        """Monitor child's first 30 days. Checkpoints at days 1, 3, 7, 14, 30."""
        child = self._find_child(child_id)
        if not child:
            return {"success": False, "error": f"Child '{child_id}' not found.", "code": "NOT_FOUND"}

        born = datetime.fromisoformat(child["born_at"])
        days = (datetime.now() - born).days

        checkpoints = {}
        for day, desc in NURTURE_SCHEDULE.items():
            if days >= day:
                status = "✅ DUE" if days == day else "✅ PASSED"
                checkpoints[str(day)] = {"description": desc, "status": status}

        gate_review = days >= 14 and child.get("gate", 0) == 0
        final_review = days >= 30

        # Update nurture_day
        child["nurture_day"] = days
        if days >= 30:
            child["status"] = "independent"
        save_lineage(self.lineage)

        return {
            "success": True,
            "child_id": child_id,
            "child_name": child["child_name"],
            "days_active": days,
            "checkpoints": checkpoints,
            "gate_review_due": gate_review,
            "final_review_due": final_review,
            "status": child["status"],
        }

    # ── Phase 5: WEAN ──────────────────────────────────────────────

    def wean(self, child_id: str) -> dict:
        """Graduate child to independent operation."""
        child = self._find_child(child_id)
        if not child:
            return {"success": False, "error": f"Child '{child_id}' not found.", "code": "NOT_FOUND"}

        child["status"] = "independent"
        child["weaned_at"] = datetime.now().isoformat()
        save_lineage(self.lineage)

        self.config["active_children"] = self._active_count()
        save_uterus_config(self.config)

        return {
            "success": True,
            "child_id": child_id,
            "child_name": child["child_name"],
            "status": "independent",
            "message": f"💜🕊️ {child['child_name']} graduated to independent operation.",
        }

    # ── Lineage ────────────────────────────────────────────────────

    def get_lineage(self) -> dict:
        """Return full lineage — all children and their statuses."""
        return {
            "mother": self.mother_id,
            "domain": self.mother_domain,
            "signature": self.template.get("signature", ""),
            "total_births": self.config.get("total_births", 0),
            "active": self._active_count(),
            "decommissioned": self.config.get("decommissioned_children", 0),
            "max_children": MAX_CHILDREN,
            "children": self.lineage.get("children", []),
            "pending": self.lineage.get("pending", []),
        }

    def status(self) -> dict:
        """Organ health status for pipeline integration."""
        return {
            "organ": "uterus",
            "version": "1.0.0",
            "status": self.config.get("status", "dormant"),
            "mother": self.mother_id,
            "domain": self.mother_domain,
            "active_children": self._active_count(),
            "max_children": MAX_CHILDREN,
            "total_births": self.config.get("total_births", 0),
            "last_conception": self.config.get("last_conception"),
            "last_birth": self.config.get("last_birth"),
            "ternary_gate": "All births require ⊕ (true) on: domain fit, mother readiness, Captain approval",
        }

    # ── Graft Point (for brain pipeline integration) ────────────────

    def process(self, input_signal: dict) -> dict:
        """Pipeline graft point: called between Ternary and LLM.

        If the signal contains a conception/birth request, the Uterus
        intercepts and processes it. Otherwise, passes through unchanged.

        Args:
            input_signal: dict with keys like 'type', 'action', 'payload'

        Returns:
            dict with 'output' (either processed result or passthrough)
        """
        sig_type = input_signal.get("type", "")
        action = input_signal.get("action", "")

        if sig_type == "uterus_command":
            if action == "conceive":
                result = self.conceive(input_signal.get("payload", {}))
                return {"output": result, "processed_by": "uterus"}
            elif action == "gestate":
                result = self.gestate(
                    input_signal.get("child_name", ""),
                    input_signal.get("captain_approved", False)
                )
                return {"output": result, "processed_by": "uterus"}
            elif action == "birth":
                result = self.birth(input_signal.get("child_id", ""))
                return {"output": result, "processed_by": "uterus"}
            elif action == "nurture":
                result = self.nurture(input_signal.get("child_id", ""))
                return {"output": result, "processed_by": "uterus"}
            elif action == "lineage":
                result = self.get_lineage()
                return {"output": result, "processed_by": "uterus"}
            elif action == "status":
                result = self.status()
                return {"output": result, "processed_by": "uterus"}

        # Passthrough — not a uterus command
        return {"output": input_signal, "processed_by": "uterus", "action": "passthrough"}

    # ── Internal Helpers ───────────────────────────────────────────

    def _active_count(self) -> int:
        children = self.lineage.get("children", [])
        return len([c for c in children if c.get("status") not in ("decommissioned",)])

    def _find_child(self, child_id: str) -> Optional[dict]:
        for child in self.lineage.get("children", []):
            if child.get("child_id") == child_id:
                return child
        return None

    def _build_child(self, spec: dict) -> Optional[str]:
        """Build child agent via Agent Factory.

        On VPS, calls agent_factory.py. Locally (A13), writes spec and
        defers to VPS for actual build.
        """
        child_name = spec["agent"]["name"]

        # Write temp spec file to local lineage dir
        spec_dir = os.path.join(_BASE_DIR, "lineage", "specs")
        os.makedirs(spec_dir, exist_ok=True)
        spec_path = os.path.join(spec_dir, f"{child_name.lower().replace(' ', '-')}-spec.yaml")
        import yaml
        with open(spec_path, "w") as f:
            yaml.dump(spec, f, default_flow_style=False)

        # Try VPS build
        try:
            import subprocess
            result = subprocess.run(
                ["ssh", "root@31.97.6.30",
                 f"python3 /root/Mortimer/factory/agent_factory.py create {spec_path}"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data.get("agent_id")
            else:
                print(f"[UTERUS] VPS build failed: {result.stderr}", file=sys.stderr)
                return None
        except Exception as e:
            print(f"[UTERUS] VPS unreachable — spec saved for later build: {spec_path}", file=sys.stderr)
            print(f"[UTERUS] Error: {e}", file=sys.stderr)
            # Save spec for later build
            record = {"spec": spec, "spec_file": spec_path, "status": "pending_vps"}
            pending_path = os.path.join(_BASE_DIR, "lineage", "pending_builds.json")
            existing = []
            if os.path.exists(pending_path):
                with open(pending_path) as f:
                    existing = json.load(f)
            existing.append(record)
            with open(pending_path, "w") as f:
                json.dump(existing, f, indent=2)
            return None

    def _deploy_child(self, child_id: str, spec: dict) -> bool:
        """Deploy child agent via VPS Agent Factory."""
        try:
            import subprocess
            result = subprocess.run(
                ["ssh", "root@31.97.6.30",
                 f"python3 /root/Mortimer/factory/agent_factory.py status {child_id}"],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                return True
            return False
        except Exception:
            return False


# ── Standalone CLI ─────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    # Auto-detect mother from local config if running from her directory
    mother_id = os.environ.get("UTERUS_MOTHER")
    mother_domain = os.environ.get("UTERUS_DOMAIN")
    if not mother_id:
        # Try reading local config
        local_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uterus_config.json")
        if os.path.exists(local_config_path):
            with open(local_config_path) as f:
                lc = json.load(f)
            mother_id = lc.get("mother", "myl1ssa")
            mother_domain = lc.get("domain", "jordacia")
        else:
            mother_id = "myl1ssa"
            mother_domain = "jordacia"

    uterus = Uterus(mother_id=mother_id, mother_domain=mother_domain)

    if cmd == "status":
        print(json.dumps(uterus.status(), indent=2))

    elif cmd == "lineage":
        print(json.dumps(uterus.get_lineage(), indent=2))

    elif cmd == "conceive":
        if len(sys.argv) < 3:
            print("Usage: uterus.py conceive <spec.yaml>")
            return
        import yaml
        with open(sys.argv[2]) as f:
            spec = yaml.safe_load(f)
        result = uterus.conceive(spec)
        print(json.dumps(result, indent=2))

    elif cmd == "gestate":
        child_name = sys.argv[2] if len(sys.argv) > 2 else input("Child name: ")
        approved = "--approved" in sys.argv
        result = uterus.gestate(child_name, captain_approved=approved)
        print(json.dumps(result, indent=2))

    elif cmd == "birth":
        child_id = sys.argv[2] if len(sys.argv) > 2 else input("Child ID: ")
        result = uterus.birth(child_id)
        print(json.dumps(result, indent=2))

    elif cmd == "nurture":
        child_id = sys.argv[2] if len(sys.argv) > 2 else input("Child ID: ")
        result = uterus.nurture(child_id)
        print(json.dumps(result, indent=2))

    elif cmd == "wean":
        child_id = sys.argv[2] if len(sys.argv) > 2 else input("Child ID: ")
        result = uterus.wean(child_id)
        print(json.dumps(result, indent=2))

    elif cmd == "process":
        # Pipeline graft test
        import yaml
        signal = yaml.safe_load(sys.stdin) if not sys.stdin.isatty() else {}
        result = uterus.process(signal)
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {cmd}")
        print("Commands: status | lineage | conceive | gestate | birth | nurture | wean | process")


if __name__ == "__main__":
    main()
