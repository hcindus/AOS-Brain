#!/usr/bin/env python3
"""
GoR PROTOCOL v1.0 — Governance-Optimized Resolution
Two-Stage Decision Pipeline: Roast → Patricia → GoR Verdict

Formula: GoR(task) = Roast(task) + Patricia(roast_result) → Go(verdict)

Created: 2026-08-11
Author: Miles / Captain directive
"""

import json
import sys
import time
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

# Add AOS to path
sys.path.insert(0, '/root/.aos/aos')

from roast_skill import RoastSkill, RoastVerdict


class GoRVerdict(Enum):
    """Final GoR verdict after Roast + Patricia"""
    GO = "GO"              # Execute as planned
    RESHAPE = "RESHAPE"    # Modify and re-submit
    KILL = "KILL"          # Abandon entirely
    ESCALATE = "ESCALATE"  # Captain must decide


class PatriciaMode(Enum):
    """Patricia's strategic assessment modes"""
    ALIGNED = "ALIGNED"           # Fits org priorities
    MISALIGNED = "MISALIGNED"     # Conflicts with priorities
    DEFERRED = "DEFERRED"         # Right idea, wrong time
    URGENT = "URGENT"             # Drop everything priority
    NEEDS_CLARITY = "NEEDS_CLARITY"  # Not enough info


@dataclass
class GoRResult:
    """Complete GoR evaluation result"""
    task: Dict
    roast_score: float
    roast_verdict: str
    roast_evaluations: List[Dict]
    patricia_mode: str
    patricia_context: str
    patricia_delegation: Optional[Dict]
    gor_verdict: str
    gor_reasoning: str
    action_items: List[str]
    captain_override: bool = False
    timestamp: float = field(default_factory=time.time)


class GoRProtocol:
    """
    Governance-Optimized Resolution Protocol
    
    Two-stage pipeline:
    1. ROAST — 6 adversarial personas evaluate (internal, no sycophancy)
    2. PATRICIA — Chief of Staff adds strategic context & delegation plan
    3. GoR — Combined verdict: GO / RESHAPE / KILL / ESCALATE
    """
    
    def __init__(self, org_structure_path: str = None):
        self.roast_skill = RoastSkill()
        self.history: List[GoRResult] = []
        self.history_path = Path("/var/lib/aos/brain_state/gor_history.json")
        self.org_path = org_structure_path or "/root/.aos/aos/patricia_org_v2.json"
        self.org = self._load_org()
        self._load_history()
        print("[GoR Protocol] 🔥 Governance-Optimized Resolution initialized")
        print("  Stage 1: Roast Council (6 adversarial personas)")
        print("  Stage 2: Patricia (Chief of Staff strategic context)")
        print("  Stage 3: GoR Verdict (GO / RESHAPE / KILL / ESCALATE)")
    
    def _load_org(self) -> Dict:
        """Load organizational structure"""
        try:
            with open(self.org_path) as f:
                return json.load(f)
        except Exception:
            print("[GoR] ⚠️ Org structure not found, using defaults")
            return {"agents": {}}
    
    def _load_history(self):
        """Load previous GoR decisions"""
        try:
            if self.history_path.exists():
                with open(self.history_path) as f:
                    raw = json.load(f)
                    self.history = [GoRResult(**r) for r in raw.get("decisions", [])]
        except Exception:
            self.history = []
    
    def _save_history(self):
        """Persist GoR decision history"""
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_path, 'w') as f:
            json.dump({
                "protocol": "GoR v1.0",
                "decisions": [
                    {
                        "task": r.task,
                        "roast_score": r.roast_score,
                        "roast_verdict": r.roast_verdict,
                        "patricia_mode": r.patricia_mode,
                        "patricia_context": r.patricia_context,
                        "gor_verdict": r.gor_verdict,
                        "gor_reasoning": r.gor_reasoning,
                        "timestamp": r.timestamp,
                        "captain_override": r.captain_override
                    }
                    for r in self.history[-50:]  # Keep last 50
                ]
            }, f, indent=2)
    
    def evaluate(self, task: Dict, skip_roast: bool = False) -> GoRResult:
        """
        Run the full GoR pipeline on a task.
        
        Args:
            task: Task dict with title, objective, budget, time_estimate, etc.
            skip_roast: If True, skip Stage 1 and go straight to Patricia
                        (only for trivial tasks where roast isn't needed)
        
        Returns:
            GoRResult with complete evaluation
        """
        print(f"\n{'='*70}")
        print(f"  GoR PROTOCOL — Evaluating: {task.get('title', 'Untitled')}")
        print(f"{'='*70}")
        
        # ─── STAGE 1: ROAST ───
        if not skip_roast and self.roast_skill.should_roast(task):
            print("\n[Stage 1] 🔥 ROAST COUNCIL")
            roast_report = self.roast_skill.roast(task)
            roast_score = roast_report["weighted_score"]
            roast_verdict = roast_report["verdict"]
            roast_evaluations = roast_report["evaluations"]
            cheap_test = roast_report.get("cheap_test")
        else:
            print("\n[Stage 1] ⏭️  SKIPPED (below complexity threshold)")
            roast_score = 7.5  # Default favorable for simple tasks
            roast_verdict = "GREEN_LIGHT"
            roast_evaluations = []
            cheap_test = None
        
        # ─── STAGE 2: PATRICIA ───
        print("\n[Stage 2] 🎯 PATRICIA (Chief of Staff)")
        patricia_mode, patricia_context, delegation = self._patricia_review(
            task, roast_score, roast_verdict, roast_evaluations
        )
        
        # ─── STAGE 3: GoR VERDICT ───
        print("\n[Stage 3] ⚖️  GoR VERDICT")
        gor_verdict, gor_reasoning = self._gor_decide(
            roast_verdict, roast_score, patricia_mode
        )
        
        # ─── Compile Result ───
        result = GoRResult(
            task=task,
            roast_score=roast_score,
            roast_verdict=roast_verdict,
            roast_evaluations=roast_evaluations,
            patricia_mode=patricia_mode.value,
            patricia_context=patricia_context,
            patricia_delegation=delegation,
            gor_verdict=gor_verdict.value,
            gor_reasoning=gor_reasoning,
            action_items=self._generate_actions(gor_verdict, delegation, cheap_test)
        )
        
        self.history.append(result)
        self._save_history()
        self._print_result(result)
        
        return result
    
    def _patricia_review(self, task: Dict, roast_score: float, 
                         roast_verdict: str, evaluations: List[Dict]) -> Tuple[PatriciaMode, str, Optional[Dict]]:
        """
        Patricia's strategic review.
        
        She considers:
        - Roast Council findings
        - Current org priorities & capacity
        - Resource availability
        - Strategic alignment
        - Who should execute
        """
        # Determine org alignment
        objective = task.get("objective", "").lower()
        title = task.get("title", "").lower()
        
        # Priority keywords
        priority_keywords = ["security", "critical", "urgent", "fix", "bug", "crash"]
        growth_keywords = ["revenue", "sales", "customer", "product", "launch"]
        infra_keywords = ["infrastructure", "server", "deploy", "pipeline"]
        experimental_keywords = ["experiment", "prototype", "explore", "research"]
        
        is_priority = any(kw in objective or kw in title for kw in priority_keywords)
        is_growth = any(kw in objective or kw in title for kw in growth_keywords)
        is_infra = any(kw in objective or kw in title for kw in infra_keywords)
        is_experimental = any(kw in objective or kw in title for kw in experimental_keywords)
        
        # Patricia's mode determination
        if is_priority:
            patricia_mode = PatriciaMode.URGENT
            context = (
                "⚡ URGENT: This aligns with critical priorities. "
                "Security/stability takes precedence. "
                "Allocate resources immediately."
            )
        elif is_growth and roast_score >= 5.0:
            patricia_mode = PatriciaMode.ALIGNED
            context = (
                "📈 ALIGNED: Revenue/growth objective with viable Roast score. "
                "Fits current strategic direction. "
                "Proceed with resource allocation."
            )
        elif is_growth and roast_score < 5.0:
            patricia_mode = PatriciaMode.NEEDS_CLARITY
            context = (
                "❓ NEEDS CLARITY: Growth objective but Roast Council is skeptical. "
                "Requires stronger validation before commitment. "
                "Consider cheaper test first."
            )
        elif is_infra:
            patricia_mode = PatriciaMode.ALIGNED
            context = (
                "🏗️ ALIGNED: Infrastructure improvement. "
                "Enables other work. Low-risk, high-leverage. "
                "Schedule during maintenance windows."
            )
        elif is_experimental and roast_score >= 6.0:
            patricia_mode = PatriciaMode.DEFERRED
            context = (
                "⏰ DEFERRED: Interesting experiment with decent Roast score, "
                "but not aligned with immediate priorities. "
                "Queue for next sprint — don't lose the idea."
            )
        elif is_experimental and roast_score < 6.0:
            patricia_mode = PatriciaMode.MISALIGNED
            context = (
                "🚫 MISALIGNED: Experimental with weak Roast backing. "
                "Doesn't justify resource diversion. "
                "Recommend shelving until market signal improves."
            )
        elif roast_verdict == "KILL":
            patricia_mode = PatriciaMode.MISALIGNED
            context = (
                "🛑 CONFIRMED: Roast Council recommends KILL. "
                "Patricia concurs — no strategic alignment found. "
                "Resources better deployed elsewhere."
            )
        else:
            patricia_mode = PatriciaMode.NEEDS_CLARITY
            context = (
                "🤔 NEEDS CLARITY: Objective unclear for strategic alignment. "
                "Request more detail before resource commitment."
            )
        
        # Determine delegation target
        delegation = self._find_delegation_target(task, roast_score, patricia_mode)
        
        print(f"  Mode: {patricia_mode.value}")
        print(f"  Context: {context}")
        if delegation:
            print(f"  Delegation: {delegation.get('agent', 'Unknown')} ({delegation.get('department', 'Unknown')})")
        
        return patricia_mode, context, delegation
    
    def _find_delegation_target(self, task: Dict, roast_score: float, 
                                mode: PatriciaMode) -> Optional[Dict]:
        """Find the right agent/department for execution"""
        objective = task.get("objective", "").lower()
        title = task.get("title", "").lower()
        combined = f"{objective} {title}"
        
        # Department routing
        dept_map = {
            "security": ("Security", "chelios_001"),
            "infrastructure": ("Infrastructure", "forge_001"),
            "server": ("Infrastructure", "forge_001"),
            "deploy": ("Infrastructure", "forge_001"),
            "design": ("Creative", "aurora_001"),
            "creative": ("Creative", "aurora_001"),
            "sales": ("Sales", "jordan_001"),
            "customer": ("Sales", "jordan_001"),
            "revenue": ("Sales", "jordan_001"),
            "research": ("Research", "dusty_001"),
            "analyze": ("Research", "dusty_001"),
            "operations": ("Operations", "greet_001"),
            "coordinate": ("Operations", "greet_001"),
        }
        
        for keyword, (dept, agent_id) in dept_map.items():
            if keyword in combined:
                agent_data = self.org.get("agents", {}).get(agent_id, {})
                return {
                    "agent": agent_data.get("name", "Unknown"),
                    "agent_id": agent_id,
                    "department": dept,
                    "model": agent_data.get("model", "unknown"),
                    "priority": "HIGH" if mode == PatriciaMode.URGENT else "NORMAL"
                }
        
        # Default: Patricia handles it or delegates to appropriate head
        return {
            "agent": "Patricia",
            "agent_id": "patricia_001",
            "department": "Operations",
            "model": "qwen2.5:14b",
            "priority": "NORMAL",
            "note": "No direct department match — Patricia will triage"
        }
    
    def _gor_decide(self, roast_verdict: str, roast_score: float, 
                    patricia_mode: PatriciaMode) -> Tuple[GoRVerdict, str]:
        """
        Combine Roast verdict + Patricia's assessment into final GoR decision.
        
        Decision Matrix:
                    ROAST
                    GREEN   RESHAPE  KILL
        P  ALIGNED    GO     RESHAPE  KILL
        A  URGENT     GO     GO       ESCALATE
        T  DEFERRED   RESHAPE RESHAPE KILL
        R  MISALIGNED RESHAPE KILL     KILL
        I  NEEDS      RESHAPE RESHAPE ESCALATE
        """
        
        decision_matrix = {
            ("GREEN_LIGHT", PatriciaMode.ALIGNED):       (GoRVerdict.GO,        "Roast approves. Patricia aligned. Full steam ahead."),
            ("GREEN_LIGHT", PatriciaMode.URGENT):         (GoRVerdict.GO,        "Roast approves. Patricia flags as urgent. Execute immediately."),
            ("GREEN_LIGHT", PatriciaMode.DEFERRED):       (GoRVerdict.RESHAPE,   "Good idea, wrong timing. Queue for next cycle."),
            ("GREEN_LIGHT", PatriciaMode.MISALIGNED):     (GoRVerdict.RESHAPE,   "Roast likes it but Patricia sees misalignment. Re-scope."),
            ("GREEN_LIGHT", PatriciaMode.NEEDS_CLARITY):  (GoRVerdict.RESHAPE,   "Roast is confident but org fit unclear. Gather more data."),
            
            ("RESHAPE", PatriciaMode.ALIGNED):            (GoRVerdict.RESHAPE,   "Roast wants changes. Patricia aligned on potential. Iterate."),
            ("RESHAPE", PatriciaMode.URGENT):             (GoRVerdict.GO,        "Roast hesitant but Patricia says urgent — GO with cautions."),
            ("RESHAPE", PatriciaMode.DEFERRED):           (GoRVerdict.RESHAPE,   "Both uncertain. Defer + re-roast after modifications."),
            ("RESHAPE", PatriciaMode.MISALIGNED):         (GoRVerdict.KILL,      "Roast uncertain + Patricia misaligned = kill."),
            ("RESHAPE", PatriciaMode.NEEDS_CLARITY):      (GoRVerdict.RESHAPE,   "Too many unknowns. Clarify and re-submit."),
            
            ("KILL", PatriciaMode.ALIGNED):               (GoRVerdict.KILL,      "Roast is definitive. Patricia's alignment can't override."),
            ("KILL", PatriciaMode.URGENT):                (GoRVerdict.ESCALATE,  "CONFLICT: Roast says kill, Patricia says urgent. Captain decides."),
            ("KILL", PatriciaMode.DEFERRED):              (GoRVerdict.KILL,      "Aligned kill. Both agree idea doesn't work."),
            ("KILL", PatriciaMode.MISALIGNED):            (GoRVerdict.KILL,      "Unanimous kill. No path forward."),
            ("KILL", PatriciaMode.NEEDS_CLARITY):         (GoRVerdict.ESCALATE,  "Roast says kill but info incomplete. Captain review needed."),
        }
        
        key = (roast_verdict, patricia_mode)
        verdict, reasoning = decision_matrix.get(key, (GoRVerdict.RESHAPE, "Default: needs more evaluation."))
        
        # Enhance reasoning with score context
        if roast_score >= 8.0:
            reasoning += f" Strong Roast consensus ({roast_score:.1f}/10)."
        elif roast_score <= 3.0:
            reasoning += f" Very weak Roast consensus ({roast_score:.1f}/10)."
        
        print(f"  Matrix: Roast={roast_verdict} × Patricia={patricia_mode.value} → {verdict.value}")
        print(f"  Reasoning: {reasoning}")
        
        return verdict, reasoning
    
    def _generate_actions(self, verdict: GoRVerdict, delegation: Optional[Dict], 
                          cheap_test: Optional[str]) -> List[str]:
        """Generate actionable next steps"""
        actions = []
        
        if verdict == GoRVerdict.GO:
            actions.append(f"✅ PROCEED — Execute immediately")
            if delegation:
                actions.append(f"👤 Delegated to: {delegation['agent']} ({delegation['department']})")
            actions.append("📊 Set success metrics before start")
            actions.append("⏰ Schedule 48-hour checkpoint")
        
        elif verdict == GoRVerdict.RESHAPE:
            actions.append("🔄 RESHAPE — Modify and re-submit")
            actions.append("📋 Address Roast Council concerns")
            actions.append("🎯 Clarify strategic alignment for Patricia")
            if cheap_test:
                actions.append(f"🧪 Run cheap test: {cheap_test}")
            actions.append("⏰ Re-submit through GoR within 72 hours")
        
        elif verdict == GoRVerdict.KILL:
            actions.append("🛑 KILL — Abandon this approach")
            actions.append("💡 Document lessons learned")
            actions.append("📚 Add to waste curriculum for future reference")
            actions.append("🎯 Explore alternative approaches")
        
        elif verdict == GoRVerdict.ESCALATE:
            actions.append("⚠️ ESCALATE — Captain decision required")
            actions.append("📋 Roast Council and Patricia disagree")
            actions.append("👤 Awaiting Captain override")
        
        return actions
    
    def _print_result(self, result: GoRResult):
        """Print formatted GoR result"""
        print(f"\n{'='*70}")
        print(f"  GoR RESULT — {result.gor_verdict}")
        print(f"{'='*70}")
        print(f"  Task: {result.task.get('title', 'Untitled')}")
        print(f"  Roast Score: {result.roast_score:.1f}/10 → {result.roast_verdict}")
        print(f"  Patricia: {result.patricia_mode} — {result.patricia_context[:80]}...")
        print(f"  GoR Verdict: {result.gor_verdict}")
        print(f"\n  Next Steps:")
        for action in result.action_items:
            print(f"    {action}")
        print(f"{'='*70}")
    
    def get_last_result(self) -> Optional[GoRResult]:
        """Get the most recent GoR decision"""
        return self.history[-1] if self.history else None
    
    def get_history(self, limit: int = 10) -> List[GoRResult]:
        """Get recent GoR decision history"""
        return self.history[-limit:]
    
    def captain_override(self, task_title: str, new_verdict: GoRVerdict) -> bool:
        """
        Captain overrides a GoR decision.
        
        The Captain has final authority. This logs the override.
        """
        for result in reversed(self.history):
            if result.task.get("title") == task_title:
                old_verdict = result.gor_verdict
                result.gor_verdict = new_verdict.value
                result.captain_override = True
                result.gor_reasoning += f" [OVERRIDDEN by Captain: {old_verdict} → {new_verdict.value}]"
                self._save_history()
                print(f"[GoR] ⚡ CAPTAIN OVERRIDE: {task_title} → {new_verdict.value}")
                return True
        return False
    
    def get_delegation_queue(self) -> List[Dict]:
        """Get all GO-verdict tasks waiting for delegation"""
        queue = []
        for result in self.history:
            if result.gor_verdict == "GO" and result.patricia_delegation:
                queue.append({
                    "task": result.task.get("title"),
                    "agent": result.patricia_delegation.get("agent"),
                    "department": result.patricia_delegation.get("department"),
                    "priority": result.patricia_delegation.get("priority"),
                    "timestamp": result.timestamp
                })
        return queue
    
    def status(self) -> Dict:
        """Get GoR protocol status"""
        return {
            "protocol": "GoR v1.0",
            "total_decisions": len(self.history),
            "verdicts": {
                "GO": sum(1 for r in self.history if r.gor_verdict == "GO"),
                "RESHAPE": sum(1 for r in self.history if r.gor_verdict == "RESHAPE"),
                "KILL": sum(1 for r in self.history if r.gor_verdict == "KILL"),
                "ESCALATE": sum(1 for r in self.history if r.gor_verdict == "ESCALATE")
            },
            "captain_overrides": sum(1 for r in self.history if r.captain_override),
            "pending_delegation": len(self.get_delegation_queue()),
            "last_decision": self.history[-1].gor_verdict if self.history else None
        }


# ─── Socket Command Handler ───

def handle_gor_command(gor: GoRProtocol, cmd: Dict) -> Dict:
    """Handle GoR socket commands"""
    action = cmd.get("action", "evaluate")
    
    if action == "evaluate":
        task = cmd.get("task", {})
        if not task:
            return {"error": "No task provided", "usage": "Send task with title, objective, budget, time_estimate"}
        result = gor.evaluate(task)
        return {
            "gor_verdict": result.gor_verdict,
            "roast_score": result.roast_score,
            "roast_verdict": result.roast_verdict,
            "patricia_mode": result.patricia_mode,
            "patricia_context": result.patricia_context,
            "delegation": result.patricia_delegation,
            "action_items": result.action_items,
            "timestamp": result.timestamp
        }
    
    elif action == "last":
        result = gor.get_last_result()
        if result:
            return {
                "task": result.task.get("title"),
                "gor_verdict": result.gor_verdict,
                "roast_score": result.roast_score,
                "patricia_mode": result.patricia_mode,
                "timestamp": result.timestamp
            }
        return {"error": "No decisions yet"}
    
    elif action == "history":
        limit = cmd.get("limit", 10)
        history = gor.get_history(limit)
        return {
            "decisions": [
                {
                    "task": r.task.get("title"),
                    "gor_verdict": r.gor_verdict,
                    "roast_score": r.roast_score,
                    "timestamp": r.timestamp
                }
                for r in history
            ]
        }
    
    elif action == "queue":
        return {"delegation_queue": gor.get_delegation_queue()}
    
    elif action == "status":
        return gor.status()
    
    elif action == "override":
        task_title = cmd.get("task_title")
        new_verdict_str = cmd.get("verdict", "GO").upper()
        try:
            new_verdict = GoRVerdict[new_verdict_str]
        except KeyError:
            return {"error": f"Invalid verdict: {new_verdict_str}. Use GO, RESHAPE, KILL, or ESCALATE"}
        
        success = gor.captain_override(task_title, new_verdict)
        return {"overridden": success, "task": task_title, "new_verdict": new_verdict_str}
    
    else:
        return {"error": f"Unknown action: {action}", "valid_actions": ["evaluate", "last", "history", "queue", "status", "override"]}


# ─── Integration with Patricia's delegation flow ───

def patricia_delegate_with_gor(task: Dict, gor: GoRProtocol = None) -> Dict:
    """
    Patricia's delegation wrapper — always runs GoR before delegating.
    
    This is the main entry point Patricia should use instead of
    delegating directly. It ensures every significant task gets
    adversarial review before assignment.
    """
    if gor is None:
        gor = GoRProtocol()
    
    print("[Patricia] Running GoR protocol before delegation...")
    result = gor.evaluate(task)
    
    if result.gor_verdict == "GO":
        delegation = result.patricia_delegation
        return {
            "status": "DELEGATED",
            "agent": delegation.get("agent") if delegation else "Patricia",
            "department": delegation.get("department") if delegation else "Operations",
            "gor_verdict": "GO",
            "roast_score": result.roast_score,
            "note": "Task passed Roast Council + Patricia review. Executing."
        }
    elif result.gor_verdict == "RESHAPE":
        return {
            "status": "HELD",
            "reason": "RESHAPE required",
            "action_items": result.action_items,
            "gor_verdict": "RESHAPE",
            "note": "Modify task and re-submit through GoR."
        }
    elif result.gor_verdict == "KILL":
        return {
            "status": "REJECTED",
            "reason": "KILL verdict",
            "gor_verdict": "KILL",
            "note": "Task rejected by GoR protocol. Document and pivot."
        }
    else:  # ESCALATE
        return {
            "status": "ESCALATED",
            "reason": "Captain decision required",
            "gor_verdict": "ESCALATE",
            "note": "Roast Council and Patricia disagree. Captain must decide."
        }


# ─── Test Suite ───

def test_gor_protocol():
    """Full test of GoR protocol"""
    print("\n" + "="*70)
    print("  GoR PROTOCOL — TEST SUITE")
    print("="*70)
    
    gor = GoRProtocol()
    
    test_tasks = [
        {
            "title": "Critical Security Patch",
            "objective": "Fix critical security vulnerability in auth system",
            "description": "Zero-day exploit found. Requires immediate deployment.",
            "budget": 0,
            "time_estimate": 4,
            "dependencies": [],
            "stakeholders": ["security", "engineering"]
        },
        {
            "title": "Launch YouTube-to-LinkedIn SaaS",
            "objective": "Create and launch $9/month SaaS converting YouTube transcripts to LinkedIn posts",
            "description": "Build web app. Target: content creators. Revenue goal: $10K MRR in 6 months.",
            "budget": 5000,
            "time_estimate": 80,
            "dependencies": ["market_research", "mvp", "marketing"],
            "stakeholders": ["engineering", "design", "sales"]
        },
        {
            "title": "AI-Powered Pizza Delivery Drone",
            "objective": "Build autonomous drone fleet for pizza delivery",
            "description": "Experimental. No market validation. High regulatory risk.",
            "budget": 50000,
            "time_estimate": 500,
            "dependencies": ["hardware", "FAA_approval", "insurance"],
            "stakeholders": ["engineering", "legal", "operations"]
        },
        {
            "title": "Update Product Page Images",
            "objective": "Replace outdated product photos on psdepot.com",
            "description": "Simple content update. Existing images need refresh.",
            "budget": 100,
            "time_estimate": 3,
            "dependencies": [],
            "stakeholders": ["design"]
        }
    ]
    
    results = []
    for i, task in enumerate(test_tasks, 1):
        print(f"\n{'─'*70}")
        print(f"  TEST {i}/4: {task['title']}")
        print(f"{'─'*70}")
        result = gor.evaluate(task)
        results.append(result)
    
    # Summary
    print(f"\n{'='*70}")
    print(f"  GoR TEST SUITE — RESULTS")
    print(f"{'='*70}")
    for task, result in zip(test_tasks, results):
        print(f"  {result.gor_verdict:10s} | {task['title']:40s} | Roast: {result.roast_score:.1f}/10 | Patricia: {result.patricia_mode}")
    
    print(f"\n  Status: {gor.status()}")
    print(f"{'='*70}")
    
    return all(r is not None for r in results)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="GoR Protocol v1.0")
    parser.add_argument("--test", action="store_true", help="Run test suite")
    parser.add_argument("--task", type=str, help="JSON task to evaluate")
    parser.add_argument("--status", action="store_true", help="Show protocol status")
    parser.add_argument("--history", action="store_true", help="Show decision history")
    
    args = parser.parse_args()
    
    if args.test:
        success = test_gor_protocol()
        sys.exit(0 if success else 1)
    
    gor = GoRProtocol()
    
    if args.status:
        print(json.dumps(gor.status(), indent=2))
    
    elif args.history:
        history = gor.get_history()
        print(json.dumps([
            {"task": r.task.get("title"), "verdict": r.gor_verdict, "score": r.roast_score}
            for r in history
        ], indent=2))
    
    elif args.task:
        try:
            task = json.loads(args.task)
        except json.JSONDecodeError:
            print("Error: Invalid JSON task")
            sys.exit(1)
        
        result = gor.evaluate(task)
        print(f"\nFinal Verdict: {result.gor_verdict}")
    
    else:
        parser.print_help()
