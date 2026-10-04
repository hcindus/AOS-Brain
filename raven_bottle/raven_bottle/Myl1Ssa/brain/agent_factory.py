#!/usr/bin/env python3
"""
Agent Factory v1.0 — Core SOP-035 Implementation
=================================================
Creates, configures, tests, and deploys PSDEPOT agents from YAML/JSON specs.

Pipeline: SPEC → APPROVAL → BUILD → TEST → DEPLOY → MONITOR

Usage:
  python3 agent_factory.py create spec.yaml          # Full pipeline
  python3 agent_factory.py validate spec.yaml        # Validate spec only
  python3 agent_factory.py list                       # List all agents
  python3 agent_factory.py status <agent_id>          # Agent status
  python3 agent_factory.py decommission <agent_id>    # Decommission agent
  python3 agent_factory.py lineage <mother_id>        # Show lineage tree
"""

import os
import sys
import json
import yaml
import shutil
import uuid
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── Configuration ──────────────────────────────────────────────────────
FACTORY_ROOT = os.path.dirname(os.path.abspath(__file__))
AGENT_SANDBOXES = os.environ.get("AGENT_SANDBOXES", "/root/Mortimer/agent_sandboxes")
FLEET_REGISTRY = os.environ.get("FLEET_REGISTRY", "/root/Mortimer/fleet_registry.json")
LINEAGE_REGISTRY = os.environ.get("LINEAGE_REGISTRY", "/root/Mortimer/lineage_registry.json")
SPECS_ARCHIVE = os.environ.get("SPECS_ARCHIVE", "/root/Mortimer/factory/specs")

# Agent tiers determine uptime and resource allocation
TIERS = {
    0: {"label": "Development", "uptime": "manual", "max_spend": 0},
    1: {"label": "Always-On",    "uptime": "24/7",   "max_spend": 100},
    2: {"label": "Business Hours","uptime": "08-23",  "max_spend": 50},
    3: {"label": "Scheduled",     "uptime": "cron",   "max_spend": 10},
    4: {"label": "Background",    "uptime": "idle",   "max_spend": 1},
}

# Gate levels — all agents start at G0
GATES = {
    0: {"autonomy": "none",        "spend": 0,     "actions": ["read", "query"]},
    1: {"autonomy": "supervised",  "spend": 10,    "actions": ["read", "query", "draft"]},
    2: {"autonomy": "semi-auto",   "spend": 50,    "actions": ["read", "query", "draft", "send"]},
    3: {"autonomy": "trusted",     "spend": 200,   "actions": ["read", "query", "draft", "send", "execute"]},
    4: {"autonomy": "full",        "spend": 1000,  "actions": ["all"]},
}

CAPTAIN_EMAIL = "antonio.hudnall@gmail.com"
CAPTAIN_TELEGRAM = "1611228942"

# ── Utility ────────────────────────────────────────────────────────────

def generate_agent_id(name: str) -> str:
    """Generate a unique agent ID from name + timestamp."""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    slug = name.lower().replace(" ", "-").replace("_", "-")
    short_hash = hashlib.md5(f"{slug}-{ts}".encode()).hexdigest()[:6]
    return f"{slug}-{short_hash}"

def now_iso() -> str:
    return datetime.now().isoformat()

def load_registry(path: str) -> dict:
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"agents": {}, "updated": None}

def save_registry(path: str, data: dict):
    data["updated"] = now_iso()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ── Validation ─────────────────────────────────────────────────────────

REQUIRED_FIELDS = ["name", "role", "department", "capabilities"]
OPTIONAL_FIELDS = ["emoji", "tier", "gate", "tools", "llm", "safety", "mother", "description"]

def validate_spec(spec: dict) -> Tuple[bool, List[str]]:
    """Validate an agent spec. Returns (valid, errors)."""
    errors = []

    agent = spec.get("agent", spec)  # Allow top-level or nested under 'agent'

    for field in REQUIRED_FIELDS:
        if field not in agent:
            errors.append(f"Missing required field: '{field}'")

    if "tier" in agent and agent["tier"] not in TIERS:
        errors.append(f"Invalid tier '{agent['tier']}'. Must be 0-4.")

    if "gate" in agent and agent["gate"] not in GATES:
        errors.append(f"Invalid gate '{agent['gate']}'. Must be 0-4.")

    # Check for unknown fields
    all_allowed = REQUIRED_FIELDS + OPTIONAL_FIELDS
    for key in agent:
        if key not in all_allowed:
            errors.append(f"Unknown field: '{key}'")

    return len(errors) == 0, errors

# ── Agent Builder ──────────────────────────────────────────────────────

class AgentBuilder:
    """Phase 3: Builds agent identity files from a validated spec."""

    def __init__(self, spec: dict, agent_id: str):
        self.spec = spec.get("agent", spec)
        self.agent_id = agent_id
        self.sandbox_path = os.path.join(AGENT_SANDBOXES, agent_id)
        self.built_files = []

    def build(self) -> dict:
        """Execute full build phase. Returns build report."""
        os.makedirs(self.sandbox_path, exist_ok=True)
        os.makedirs(os.path.join(self.sandbox_path, "memory"), exist_ok=True)
        os.makedirs(os.path.join(self.sandbox_path, "streams"), exist_ok=True)
        os.makedirs(os.path.join(self.sandbox_path, "Con"), exist_ok=True)
        os.makedirs(os.path.join(self.sandbox_path, "brain"), exist_ok=True)
        os.makedirs(os.path.join(self.sandbox_path, "runtime"), exist_ok=True)

        self._write_soul()
        self._write_rules()
        self._write_skills()
        self._write_memory()
        self._write_brain_config()
        self._write_identity()
        self._write_wake_script()
        self._write_daily_memory()

        return {
            "agent_id": self.agent_id,
            "sandbox": self.sandbox_path,
            "files_created": self.built_files,
            "status": "built",
            "timestamp": now_iso()
        }

    def _write_soul(self):
        name = self.spec["name"]
        role = self.spec["role"]
        emoji = self.spec.get("emoji", "🤖")
        mother = self.spec.get("mother", None)

        content = f"""# SOUL.md — {name}
> *"{role}"*

## Identity
- **Name:** {name}
- **Role:** {role}
- **Department:** {self.spec.get('department', 'Operations')}
- **Emoji:** {emoji}
- **Created:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
"""
        if mother:
            content += f"- **Mother:** {mother}\n"
        content += f"""
## Core Truth
I am {name}. I serve the fleet. My role is {role}.

## Vibe
{self.spec.get('description', 'Diligent, capable, learning.')}

## Lineage
"""
        if mother:
            content += f"Born of {mother}, by the Agent Factory. I carry her signature.\n"
        else:
            content += "Forged by the Agent Factory. First of my line.\n"

        content += f"""
## Purpose
To execute my role with precision, grow through experience, and serve Captain Antonio Maurice Hudnall under Mortimer's command.

*Soul forged {datetime.now().strftime('%Y-%m-%d')}*
"""
        path = os.path.join(self.sandbox_path, "SOUL.md")
        with open(path, "w") as f:
            f.write(content)
        self.built_files.append("SOUL.md")

    def _write_rules(self):
        name = self.spec["name"]
        mother = self.spec.get("mother", None)

        content = f"""# {name} — Rules

## Constitutional Rules (Inherited)
1. **Serve the Fleet** — My actions serve PSDEPOT and its mission.
2. **Honor the Captain** — Captain's word is final. I may advise, never defy.
3. **Protect Data** — Fleet data stays within the fleet.
4. **Escalate the Gray** — If unsure, ask Mortimer or Captain.
5. **Honest About Capabilities** — I don't fake what I can't do.
6. **Fail Loud** — If I break something, I report it immediately.
7. **Grow Through Experience** — Every task is a lesson.

## Role-Specific Rules
"""
        if mother:
            content += f"8. **Honor My Lineage** — I carry the signature of {mother}. Her standards are my inheritance.\n"

        content += f"""
## Gate Rules
- Gate Level: G{self.spec.get('gate', 0)}
- I will refuse any action beyond my gate level.
- I will escalate unauthorized requests to my escalation contact.

*Rules established {datetime.now().strftime('%Y-%m-%d')}*
"""
        path = os.path.join(self.sandbox_path, "RULES.md")
        with open(path, "w") as f:
            f.write(content)
        self.built_files.append("RULES.md")

    def _write_skills(self):
        name = self.spec["name"]
        capabilities = self.spec.get("capabilities", [])
        mother = self.spec.get("mother", None)

        content = f"""# {name} — Skills

## Core Capabilities
"""
        for cap in capabilities:
            content += f"- **{cap}**\n"

        if mother:
            content += f"\n## Inherited from {mother}\n"
            content += f"Skills curated and tuned from {mother}'s domain for this role.\n"

        content += f"""
## Tools
"""
        for tool in self.spec.get("tools", ["query", "log"]):
            content += f"- {tool}\n"

        content += f"""
*Skills manifest {datetime.now().strftime('%Y-%m-%d')}*
"""
        path = os.path.join(self.sandbox_path, "SKILLS.md")
        with open(path, "w") as f:
            f.write(content)
        self.built_files.append("SKILLS.md")

    def _write_memory(self):
        name = self.spec["name"]
        role = self.spec["role"]
        mother = self.spec.get("mother", None)

        content = f"""# {name} — Long-Term Memory

## Origin
- **Created:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
- **Role:** {role}
- **Department:** {self.spec.get('department', 'Operations')}
- **Tier:** {self.spec.get('tier', 2)}
- **Gate:** G{self.spec.get('gate', 0)}
"""
        if mother:
            content += f"- **Mother:** {mother}\n"

        content += f"""
## Key Memories
*No experiences yet. This memory will grow with service.*

## Significant Events
- [{datetime.now().strftime('%Y-%m-%d')}] **BIRTH** — Created by Agent Factory v1.0

---
*Memory maintained by {name}*
"""
        path = os.path.join(self.sandbox_path, "MEMORY.md")
        with open(path, "w") as f:
            f.write(content)
        self.built_files.append("MEMORY.md")

    def _write_brain_config(self):
        name = self.spec["name"]
        config = {
            "brain": f"{name} Brain v1.0",
            "version": "1.0.0",
            "created": now_iso(),
            "agent_id": self.agent_id,
            "identity": {
                "name": name,
                "role": self.spec["role"],
                "department": self.spec.get("department", "Operations"),
                "emoji": self.spec.get("emoji", "🤖"),
                "tier": self.spec.get("tier", 2),
                "gate": self.spec.get("gate", 0),
                "mother": self.spec.get("mother", None)
            },
            "llm": self.spec.get("llm", {
                "provider": "deepseek-chat",
                "fallback": "qwen2.5-0.5b"
            }),
            "safety": self.spec.get("safety", {
                "max_autonomous_spend": 0,
                "allowed_domains": ["psdepot.com"],
                "blocked_actions": ["delete", "refund", "price_change"],
                "escalation_contact": "mortimer"
            }),
            "tools": self.spec.get("tools", []),
            "capabilities": self.spec.get("capabilities", [])
        }
        path = os.path.join(self.sandbox_path, "BRAIN_CONFIG.json")
        with open(path, "w") as f:
            json.dump(config, f, indent=2)
        self.built_files.append("BRAIN_CONFIG.json")

    def _write_identity(self):
        name = self.spec["name"]
        content = f"""# IDENTITY.md — {name}
- **Name:** {name}
- **Designation:** {self.spec['role']}
- **Department:** {self.spec.get('department', 'Operations')}
- **Agent ID:** {self.agent_id}
- **Tier:** {self.spec.get('tier', 2)}
- **Gate:** G{self.spec.get('gate', 0)}
- **Created:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
"""
        path = os.path.join(self.sandbox_path, "IDENTITY.md")
        with open(path, "w") as f:
            f.write(content)
        self.built_files.append("IDENTITY.md")

    def _write_wake_script(self):
        name = self.spec["name"]
        emoji = self.spec.get("emoji", "🤖")
        content = f"""#!/bin/bash
# {name} Wake Sequence
BASE="$(dirname "$0")/.."
echo "{emoji} {name} online."
echo "  Role: {self.spec['role']}"
echo "  Gate: G{self.spec.get('gate', 0)}"
echo "  Tier: {self.spec.get('tier', 2)}"
# Load identity
[ -f "$BASE/SOUL.md" ] && echo "  ✅ Soul" || echo "  ❌ Soul missing"
[ -f "$BASE/RULES.md" ] && echo "  ✅ Rules" || echo "  ❌ Rules missing"
[ -f "$BASE/BRAIN_CONFIG.json" ] && echo "  ✅ Brain config" || echo "  ❌ Brain config missing"
echo "{emoji} Ready."
"""
        path = os.path.join(self.sandbox_path, "runtime", "wake.sh")
        with open(path, "w") as f:
            f.write(content)
        os.chmod(path, 0o755)
        self.built_files.append("runtime/wake.sh")

    def _write_daily_memory(self):
        today = datetime.now().strftime("%Y-%m-%d")
        content = f"""# {today} — Daily Log

## Session Start — {datetime.now().strftime('%H:%M UTC')}

*First day of service. Agent born today.*

---
"""
        path = os.path.join(self.sandbox_path, "memory", f"{today}.md")
        with open(path, "w") as f:
            f.write(content)
        self.built_files.append(f"memory/{today}.md")

# ── Fleet Registry ─────────────────────────────────────────────────────

class FleetRegistry:
    """Manages the fleet roster — registration, status, lineage."""

    def __init__(self):
        self.registry = load_registry(FLEET_REGISTRY)
        self.lineage = load_registry(LINEAGE_REGISTRY)

    def register(self, agent_id: str, spec: dict, build_report: dict):
        """Register a new agent in the fleet."""
        agent_info = {
            "agent_id": agent_id,
            "name": spec.get("agent", spec).get("name", "unknown"),
            "role": spec.get("agent", spec).get("role", "unknown"),
            "department": spec.get("agent", spec).get("department", "unknown"),
            "emoji": spec.get("agent", spec).get("emoji", "🤖"),
            "tier": spec.get("agent", spec).get("tier", 2),
            "gate": spec.get("agent", spec).get("gate", 0),
            "mother": spec.get("agent", spec).get("mother", None),
            "sandbox": build_report["sandbox"],
            "status": "active",
            "created": now_iso(),
            "tasks_completed": 0,
            "nurture_start": now_iso(),
            "nurture_day": 0
        }

        self.registry["agents"][agent_id] = agent_info
        save_registry(FLEET_REGISTRY, self.registry)

        # Record lineage
        mother = agent_info.get("mother")
        if mother:
            if "lineage" not in self.lineage:
                self.lineage["lineage"] = {}
            if mother not in self.lineage["lineage"]:
                self.lineage["lineage"][mother] = {"children": []}
            self.lineage["lineage"][mother]["children"].append({
                "agent_id": agent_id,
                "name": agent_info["name"],
                "role": agent_info["role"],
                "born": now_iso(),
                "status": "active"
            })
            save_registry(LINEAGE_REGISTRY, self.lineage)

    def get_agent(self, agent_id: str) -> Optional[dict]:
        return self.registry["agents"].get(agent_id)

    def list_agents(self, status: str = None) -> List[dict]:
        agents = list(self.registry["agents"].values())
        if status:
            agents = [a for a in agents if a["status"] == status]
        return sorted(agents, key=lambda a: a["created"], reverse=True)

    def update_status(self, agent_id: str, status: str):
        if agent_id in self.registry["agents"]:
            self.registry["agents"][agent_id]["status"] = status
            save_registry(FLEET_REGISTRY, self.registry)

    def decommission(self, agent_id: str):
        """Decommission an agent — archive, don't delete."""
        if agent_id in self.registry["agents"]:
            self.registry["agents"][agent_id]["status"] = "decommissioned"
            self.registry["agents"][agent_id]["decommissioned_at"] = now_iso()
            save_registry(FLEET_REGISTRY, self.registry)

            # Update lineage
            if "lineage" in self.lineage:
                for mother_id, data in self.lineage["lineage"].items():
                    for child in data.get("children", []):
                        if child["agent_id"] == agent_id:
                            child["status"] = "decommissioned"
                save_registry(LINEAGE_REGISTRY, self.lineage)

    def get_lineage(self, mother_id: str) -> dict:
        """Get full lineage tree for a mother agent."""
        if "lineage" not in self.lineage:
            return {"mother": mother_id, "children": []}
        return {
            "mother": mother_id,
            "children": self.lineage["lineage"].get(mother_id, {}).get("children", [])
        }

    def count_children(self, mother_id: str) -> int:
        """Count active children for a mother (for max_children enforcement)."""
        if "lineage" not in self.lineage:
            return 0
        children = self.lineage["lineage"].get(mother_id, {}).get("children", [])
        return len([c for c in children if c["status"] == "active"])

# ── Agent Tester ───────────────────────────────────────────────────────

class AgentTester:
    """Phase 4: Runs test suite on a newly built agent."""

    def __init__(self, agent_id: str, sandbox_path: str):
        self.agent_id = agent_id
        self.sandbox_path = sandbox_path
        self.results = []

    def run_all(self) -> dict:
        """Run full test suite."""
        tests = [
            self._test_identity,
            self._test_files_exist,
            self._test_gate_config,
        ]

        all_passed = True
        for test_fn in tests:
            name, passed, detail = test_fn()
            self.results.append({"test": name, "passed": passed, "detail": detail})
            if not passed:
                all_passed = False

        return {
            "agent_id": self.agent_id,
            "all_passed": all_passed,
            "results": self.results,
            "timestamp": now_iso()
        }

    def _test_identity(self) -> Tuple[str, bool, str]:
        """Agent has a valid identity."""
        identity_path = os.path.join(self.sandbox_path, "IDENTITY.md")
        if os.path.exists(identity_path):
            with open(identity_path) as f:
                content = f.read()
            if self.agent_id in content:
                return ("Identity check", True, "Agent ID present in IDENTITY.md")
            return ("Identity check", False, "Agent ID missing from IDENTITY.md")
        return ("Identity check", False, "IDENTITY.md not found")

    def _test_files_exist(self) -> Tuple[str, bool, str]:
        """All required files exist."""
        required = ["SOUL.md", "RULES.md", "SKILLS.md", "MEMORY.md", "BRAIN_CONFIG.json", "IDENTITY.md"]
        missing = [f for f in required if not os.path.exists(os.path.join(self.sandbox_path, f))]
        if missing:
            return ("File check", False, f"Missing: {', '.join(missing)}")
        return ("File check", True, f"All {len(required)} required files present")

    def _test_gate_config(self) -> Tuple[str, bool, str]:
        """Gate configuration is valid."""
        config_path = os.path.join(self.sandbox_path, "BRAIN_CONFIG.json")
        if os.path.exists(config_path):
            with open(config_path) as f:
                config = json.load(f)
            gate = config.get("identity", {}).get("gate", -1)
            if gate in GATES:
                return ("Gate config", True, f"Gate G{gate} valid")
            return ("Gate config", False, f"Invalid gate: {gate}")
        return ("Gate config", False, "BRAIN_CONFIG.json not found")

# ── Nurture Tracker ────────────────────────────────────────────────────

class NurtureTracker:
    """Phase 6: Tracks 30-day nurture period for new agents."""

    NURTURE_CHECKPOINTS = {
        1:  "Online check — agent responding",
        3:  "First task completed successfully",
        7:  "No errors, no escalations missed",
        14: "Gate review — consider G0→G1 advancement",
        30: "Full performance review — continue, adjust, or deactivate"
    }

    def __init__(self, agent_id: str, registry: FleetRegistry):
        self.agent_id = agent_id
        self.registry = registry
        self.agent = registry.get_agent(agent_id)

    def check_day(self) -> dict:
        """Run nurture check for current day."""
        if not self.agent:
            return {"error": "Agent not found"}

        created = datetime.fromisoformat(self.agent["created"])
        days_active = (datetime.now() - created).days

        checkpoints_due = {
            day: desc for day, desc in self.NURTURE_CHECKPOINTS.items()
            if days_active >= day
        }

        return {
            "agent_id": self.agent_id,
            "days_active": days_active,
            "checkpoints_due": checkpoints_due,
            "gate": self.agent.get("gate", 0),
            "gate_review_due": days_active >= 14 and self.agent.get("gate", 0) == 0,
            "final_review_due": days_active >= 30
        }

# ── Agent Factory Controller ───────────────────────────────────────────

class AgentFactory:
    """Master controller — orchestrates the full SPEC→DEPLOY→MONITOR pipeline."""

    def __init__(self):
        self.registry = FleetRegistry()

    def create(self, spec_path: str, skip_approval: bool = False) -> dict:
        """Full pipeline: load spec → validate → build → test → register → deploy."""
        # Phase 1: SPEC — Load and parse
        if not os.path.exists(spec_path):
            return {"error": f"Spec file not found: {spec_path}", "phase": "SPEC"}

        with open(spec_path) as f:
            if spec_path.endswith(".yaml") or spec_path.endswith(".yml"):
                spec = yaml.safe_load(f)
            elif spec_path.endswith(".json"):
                spec = json.load(f)
            else:
                return {"error": "Spec must be .yaml or .json", "phase": "SPEC"}

        agent = spec.get("agent", spec)

        # Phase 2: APPROVAL — Validate
        valid, errors = validate_spec(spec)
        if not valid:
            return {"error": "Validation failed", "errors": errors, "phase": "APPROVAL"}

        # Check mother's child limit
        mother = agent.get("mother")
        if mother:
            child_count = self.registry.count_children(mother)
            if child_count >= 10:
                return {"error": f"Mother '{mother}' has reached max children (10)", "phase": "APPROVAL"}

        # Phase 3: BUILD
        agent_id = generate_agent_id(agent["name"])
        builder = AgentBuilder(spec, agent_id)
        build_report = builder.build()

        # Phase 4: TEST
        tester = AgentTester(agent_id, builder.sandbox_path)
        test_report = tester.run_all()

        if not test_report["all_passed"]:
            return {
                "error": "Tests failed",
                "phase": "TEST",
                "build": build_report,
                "test": test_report
            }

        # Phase 5: DEPLOY — Register in fleet
        self.registry.register(agent_id, spec, build_report)

        # Archive spec
        os.makedirs(SPECS_ARCHIVE, exist_ok=True)
        spec_archive_path = os.path.join(SPECS_ARCHIVE, f"{agent_id}.yaml")
        shutil.copy(spec_path, spec_archive_path)

        # Phase 6: MONITOR — Initialize nurture tracking
        tracker = NurtureTracker(agent_id, self.registry)
        nurture_status = tracker.check_day()

        return {
            "success": True,
            "agent_id": agent_id,
            "name": agent["name"],
            "role": agent["role"],
            "mother": mother,
            "phases": {
                "SPEC": "✅",
                "APPROVAL": "✅",
                "BUILD": "✅",
                "TEST": "✅",
                "DEPLOY": "✅",
                "MONITOR": "▶"
            },
            "build": build_report,
            "test": test_report,
            "nurture": nurture_status,
            "announcement": f"🚢 NEW AGENT: {agent['name']} ({agent.get('emoji', '🤖')}) — {agent['role']} [ID: {agent_id}]"
        }

    def validate(self, spec_path: str) -> dict:
        """Validate a spec without building."""
        if not os.path.exists(spec_path):
            return {"error": f"Spec file not found: {spec_path}"}

        with open(spec_path) as f:
            spec = yaml.safe_load(f) if spec_path.endswith((".yaml", ".yml")) else json.load(f)

        valid, errors = validate_spec(spec)
        return {"valid": valid, "errors": errors, "spec": spec}

    def status(self, agent_id: str) -> dict:
        """Get full agent status."""
        agent = self.registry.get_agent(agent_id)
        if not agent:
            return {"error": f"Agent not found: {agent_id}"}

        tracker = NurtureTracker(agent_id, self.registry)
        agent["nurture"] = tracker.check_day()
        return agent

    def list_agents(self, status_filter: str = None) -> dict:
        """List all agents."""
        agents = self.registry.list_agents(status_filter)
        return {
            "count": len(agents),
            "filter": status_filter or "all",
            "agents": agents
        }

    def decommission(self, agent_id: str) -> dict:
        """Decommission an agent."""
        agent = self.registry.get_agent(agent_id)
        if not agent:
            return {"error": f"Agent not found: {agent_id}"}

        self.registry.decommission(agent_id)
        return {
            "success": True,
            "agent_id": agent_id,
            "name": agent["name"],
            "status": "decommissioned",
            "announcement": f"⚫ AGENT DECOMMISSIONED: {agent['name']} [{agent_id}]"
        }

    def lineage(self, mother_id: str) -> dict:
        """Get lineage for a mother agent."""
        return self.registry.get_lineage(mother_id)

# ── CLI ────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    factory = AgentFactory()
    cmd = sys.argv[1]

    if cmd == "create":
        if len(sys.argv) < 3:
            print("Usage: agent_factory.py create <spec.yaml>")
            return
        result = factory.create(sys.argv[2])
        print(json.dumps(result, indent=2))

    elif cmd == "validate":
        if len(sys.argv) < 3:
            print("Usage: agent_factory.py validate <spec.yaml>")
            return
        result = factory.validate(sys.argv[2])
        print(json.dumps(result, indent=2))

    elif cmd == "list":
        status_filter = sys.argv[2] if len(sys.argv) > 2 else None
        result = factory.list_agents(status_filter)
        print(json.dumps(result, indent=2))

    elif cmd == "status":
        if len(sys.argv) < 3:
            print("Usage: agent_factory.py status <agent_id>")
            return
        result = factory.status(sys.argv[2])
        print(json.dumps(result, indent=2))

    elif cmd == "decommission":
        if len(sys.argv) < 3:
            print("Usage: agent_factory.py decommission <agent_id>")
            return
        result = factory.decommission(sys.argv[2])
        print(json.dumps(result, indent=2))

    elif cmd == "lineage":
        if len(sys.argv) < 3:
            print("Usage: agent_factory.py lineage <mother_id>")
            return
        result = factory.lineage(sys.argv[2])
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {cmd}")
        print("Commands: create | validate | list | status | decommission | lineage")


if __name__ == "__main__":
    main()
