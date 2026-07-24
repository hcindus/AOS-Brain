#!/usr/bin/env python3
"""
CONTEXT MANAGER v1.0 - Session Handoff & Context Window Monitoring
Based on Nate Herk's "Stop Context Rot" pattern

Features:
- Real-time context window tracking
- State summary generation before reset
- Pick-up instructions for next turn
- Auto-handoff at ~200K tokens (safety margin before 250K)
"""

import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class ContextStatus(Enum):
    HEALTHY = "healthy"           # < 150K tokens
    WARNING = "warning"          # 150K - 200K tokens
    CRITICAL = "critical"        # 200K - 250K tokens
    OVERFLOW = "overflow"        # > 250K tokens


@dataclass
class StateSnapshot:
    """Complete state snapshot for session handoff"""
    timestamp: float
    token_count: int
    context_status: str
    
    # Current objectives
    active_objectives: List[str]
    completed_objectives: List[str]
    blocked_objectives: List[str]
    
    # Key decisions made
    recent_decisions: List[Dict]
    
    # Open questions
    pending_questions: List[str]
    
    # Critical context
    key_files_modified: List[str]
    external_dependencies: List[str]
    
    # Next turn instructions
    pickup_instructions: str
    priority_actions: List[str]
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_markdown(self) -> str:
        """Generate markdown summary for human readability"""
        md = f"""# Session Handoff Summary

**Generated:** {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime(self.timestamp))}
**Token Count:** {self.token_count:,} / 250,000 ({(self.token_count/250000)*100:.1f}%)
**Status:** {self.context_status.upper()}

---

## 🎯 Active Objectives
"""
        for obj in self.active_objectives:
            md += f"- [ ] {obj}\n"
        
        if self.completed_objectives:
            md += "\n## ✅ Recently Completed\n"
            for obj in self.completed_objectives[-5:]:  # Last 5
                md += f"- {obj}\n"
        
        if self.blocked_objectives:
            md += "\n## 🚧 Blocked\n"
            for obj in self.blocked_objectives:
                md += f"- {obj}\n"
        
        if self.recent_decisions:
            md += "\n## 📝 Key Decisions\n"
            for decision in self.recent_decisions[-3:]:
                md += f"- **{decision.get('topic', 'Unknown')}**: {decision.get('decision', 'N/A')}\n"
        
        if self.pending_questions:
            md += "\n## ❓ Open Questions\n"
            for question in self.pending_questions:
                md += f"- {question}\n"
        
        if self.key_files_modified:
            md += "\n## 📁 Files Modified\n"
            for f in self.key_files_modified[-10:]:
                md += f"- `{f}`\n"
        
        md += f"""
---

## 🚀 Next Turn Instructions

{self.pickup_instructions}

### Priority Actions
"""
        for action in self.priority_actions:
            md += f"1. {action}\n"
        
        md += """
---

*This summary was auto-generated before context reset*
"""
        return md


class ContextManager:
    """
    Manages AOS context window and session handoffs
    
    Monitors token usage, generates state summaries,
    and orchestrates graceful handoffs.
    """
    
    # Token thresholds
    WARNING_THRESHOLD = 150000   # Start monitoring
    HANDOFF_THRESHOLD = 200000  # Prepare handoff
    CRITICAL_THRESHOLD = 240000 # Emergency handoff
    MAX_TOKENS = 250000         # Hard limit
    
    def __init__(self):
        self.current_tokens = 0
        self.session_history: List[StateSnapshot] = []
        self.objectives_log: List[Dict] = []
        self.decisions_log: List[Dict] = []
        
        print("[Context Manager] 📊 Context monitoring initialized")
        print(f"  Warning: {self.WARNING_THRESHOLD:,} tokens")
        print(f"  Handoff: {self.HANDOFF_THRESHOLD:,} tokens")
        print(f"  Critical: {self.CRITICAL_THRESHOLD:,} tokens")
    
    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (1 token ≈ 4 chars)"""
        return len(text) // 4
    
    def add_conversation(self, role: str, content: str) -> None:
        """Track conversation token usage"""
        tokens = self.estimate_tokens(f"{role}: {content}")
        self.current_tokens += tokens
    
    def get_status(self) -> ContextStatus:
        """Get current context status"""
        if self.current_tokens >= self.MAX_TOKENS:
            return ContextStatus.OVERFLOW
        elif self.current_tokens >= self.CRITICAL_THRESHOLD:
            return ContextStatus.CRITICAL
        elif self.current_tokens >= self.HANDOFF_THRESHOLD:
            return ContextStatus.WARNING
        return ContextStatus.HEALTHY
    
    def should_handoff(self) -> bool:
        """Check if handoff needed"""
        return self.current_tokens >= self.HANDOFF_THRESHOLD
    
    def create_handoff_summary(self, 
                               active_objectives: List[str],
                               completed: List[str] = None,
                               blocked: List[str] = None,
                               files_modified: List[str] = None) -> StateSnapshot:
        """Create comprehensive handoff summary"""
        
        status = self.get_status()
        
        # Generate pickup instructions based on context
        pickup = self._generate_pickup_instructions(active_objectives, status)
        
        # Generate priority actions
        priorities = self._generate_priority_actions(active_objectives, blocked or [])
        
        snapshot = StateSnapshot(
            timestamp=time.time(),
            token_count=self.current_tokens,
            context_status=status.value,
            active_objectives=active_objectives,
            completed_objectives=completed or [],
            blocked_objectives=blocked or [],
            recent_decisions=self.decisions_log[-5:] if self.decisions_log else [],
            pending_questions=[],
            key_files_modified=files_modified or [],
            external_dependencies=[],
            pickup_instructions=pickup,
            priority_actions=priorities
        )
        
        self.session_history.append(snapshot)
        return snapshot
    
    def _generate_pickup_instructions(self, 
                                    objectives: List[str], 
                                    status: ContextStatus) -> str:
        """Generate context-appropriate pickup instructions"""
        
        if status == ContextStatus.CRITICAL or status == ContextStatus.OVERFLOW:
            return (
                "⚠️ **CRITICAL HANDOFF** - Context window near limit.\n\n"
                "Focus on completing ONE objective from the active list.\n"
                "Do NOT start new work. Verify all changes are saved.\n"
                "Next session will start fresh context."
            )
        
        if len(objectives) == 0:
            return "No active objectives. Ready for new tasks."
        
        if len(objectives) == 1:
            return f"Continue work on: {objectives[0]}"
        
        primary = objectives[0]
        return (
            f"Primary objective: {primary}\n"
            f"Secondary objectives: {', '.join(objectives[1:])}\n\n"
            "Complete primary before moving to secondary."
        )
    
    def _generate_priority_actions(self, 
                                 objectives: List[str], 
                                 blocked: List[str]) -> List[str]:
        """Generate prioritized action list"""
        actions = []
        
        if objectives:
            actions.append(f"Resume: {objectives[0]}")
        
        if len(objectives) > 1:
            actions.append(f"Queue: {objectives[1]}")
        
        if blocked:
            actions.append(f"Unblock: {blocked[0]}")
        
        actions.append("Check MEMORY.md for context")
        actions.append("Verify recent file changes")
        
        return actions
    
    def log_objective(self, objective: str, status: str = "started") -> None:
        """Log objective state change"""
        self.objectives_log.append({
            "objective": objective,
            "status": status,
            "timestamp": time.time()
        })
    
    def log_decision(self, topic: str, decision: str, rationale: str = "") -> None:
        """Log important decision"""
        self.decisions_log.append({
            "topic": topic,
            "decision": decision,
            "rationale": rationale,
            "timestamp": time.time()
        })
    
    def reset_context(self) -> StateSnapshot:
        """Reset context and return handoff summary"""
        print(f"\n[Context Manager] 🔄 Context reset triggered")
        print(f"  Tokens used: {self.current_tokens:,}")
        
        # Get current objectives
        active = [o["objective"] for o in self.objectives_log 
                  if o["status"] == "started"][-5:]
        completed = [o["objective"] for o in self.objectives_log 
                     if o["status"] == "completed"][-5:]
        
        # Create handoff summary
        snapshot = self.create_handoff_summary(active, completed)
        
        # Save to file
        self._save_handoff_file(snapshot)
        
        # Reset token counter
        self.current_tokens = 0
        
        print(f"  Handoff saved. Ready for new session.")
        
        return snapshot
    
    def _save_handoff_file(self, snapshot: StateSnapshot) -> None:
        """Save handoff summary to file"""
        filename = f"/root/.openclaw/workspace/memory/handoff_{int(snapshot.timestamp)}.md"
        with open(filename, 'w') as f:
            f.write(snapshot.to_markdown())
    
    def get_session_stats(self) -> Dict:
        """Get session statistics"""
        return {
            "current_tokens": self.current_tokens,
            "max_tokens": self.MAX_TOKENS,
            "usage_percent": (self.current_tokens / self.MAX_TOKENS) * 100,
            "status": self.get_status().value,
            "total_objectives": len(self.objectives_log),
            "total_decisions": len(self.decisions_log),
            "handoffs": len(self.session_history)
        }


# Global instance
context_manager = ContextManager()


# Utility functions for integration
def check_context_status() -> Dict:
    """Quick check of context status"""
    return {
        "tokens": context_manager.current_tokens,
        "threshold": context_manager.HANDOFF_THRESHOLD,
        "status": context_manager.get_status().value,
        "should_handoff": context_manager.should_handoff()
    }


def handoff_if_needed(active_objectives: List[str]) -> Optional[StateSnapshot]:
    """Auto-handoff if context threshold reached"""
    if context_manager.should_handoff():
        return context_manager.reset_context()
    return None


# Test function
def test_context_manager():
    """Test context manager"""
    print("\n" + "=" * 70)
    print("  CONTEXT MANAGER - TEST")
    print("=" * 70)
    
    cm = ContextManager()
    
    # Simulate conversation
    print("\n[Test 1] Simulate conversation buildup")
    messages = [
        ("user", "I need to build a web application with authentication and database. It should handle user registration, login, and profile management."),
        ("assistant", "I'll help you build that. Let me start by creating the project structure..." * 50),  # Long response
    ] * 100  # 100 exchanges
    
    for role, content in messages[:50]:  # Add 50 messages
        cm.add_conversation(role, content)
    
    print(f"  Tokens: {cm.current_tokens:,}")
    print(f"  Status: {cm.get_status().value}")
    print(f"  Should handoff: {cm.should_handoff()}")
    
    # Add more to trigger handoff
    print("\n[Test 2] Add more to trigger handoff threshold")
    for role, content in messages[50:100]:
        cm.add_conversation(role, content)
    
    print(f"  Tokens: {cm.current_tokens:,}")
    print(f"  Status: {cm.get_status().value}")
    print(f"  Should handoff: {cm.should_handoff()}")
    
    if cm.should_handoff():
        print("\n[Test 3] Generate handoff summary")
        
        # Log some objectives
        cm.log_objective("Build web application", "started")
        cm.log_objective("Create authentication system", "started")
        cm.log_decision("Framework", "Use FastAPI", "Performance + async support")
        cm.log_decision("Database", "PostgreSQL", "Production proven")
        
        snapshot = cm.create_handoff_summary(
            active_objectives=["Build web application", "Create authentication system"],
            completed=["Project setup"],
            files_modified=["main.py", "auth.py", "config.py"]
        )
        
        print(f"  Summary created: {len(snapshot.to_markdown())} chars")
        print(f"  Status in summary: {snapshot.context_status}")
        print(f"  Pickup instructions:\n    {snapshot.pickup_instructions[:100]}...")
    
    print("\n" + "=" * 70)
    print("  ✅ Context Manager Test Complete")
    print("=" * 70)


if __name__ == "__main__":
    test_context_manager()
