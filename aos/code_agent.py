#!/usr/bin/env python3
"""
CODE AGENT v1.0 - Autonomous code generation with brain integration

OODA Loop on code:
  OBSERVE → Read repo, analyze structure, check CI status
  ORIENT  → Query brain: "similar patterns? past failures? current priorities?"
  DECIDE  → Plan changes, select files, generate code
  ACT     → Write files, commit, push PR
  LEARN   → Feedback from CI/tests to cortex

Uses brain for:
  - Persistent memory across sessions
  - Coordination with other agents
  - Temporal reasoning ("last time we touched this file...")
"""

import os
import re
import json
import time
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from agent_sdk import AOSBrainClient

@dataclass
class CodeTask:
    """A code change task"""
    task_id: str
    description: str
    repo_path: str
    target_files: List[str]
    generated_code: Dict[str, str]
    status: str  # pending, in_progress, completed, failed
    test_results: Optional[Dict] = None

class CodeAgent:
    """
    Autonomous code agent with brain-backed memory
    
    Agent ID convention: code_agent_<name>
    Example: code_agent_frontend, code_agent_api
    """
    
    def __init__(self, agent_id: str = "code_agent_main", 
                 workspace: str = "/root/.code_workspace",
                 llm_model: str = "ollama/kimi-k2.5:cloud"):
        self.agent_id = agent_id
        self.workspace = Path(workspace)
        self.workspace.mkdir(exist_ok=True)
        
        # Connect to brain
        self.brain = AOSBrainClient(agent_id=agent_id)
        self.brain.register()
        
        self.llm_model = llm_model
        self.current_task: Optional[CodeTask] = None
        self.repo_cache: Dict[str, Dict] = {}
        
        print(f"[CodeAgent:{agent_id}] Initialized")
        print(f"  Workspace: {self.workspace}")
        print(f"  Brain: Connected")
    
    def observe_repo(self, repo_path: str) -> Dict:
        """
        OBSERVE: Analyze repository structure
        
        Returns repo metadata + file tree
        """
        if not os.path.exists(repo_path):
            return {"error": f"Repo not found: {repo_path}"}
        
        repo_path = Path(repo_path)
        
        # Get structure
        files = []
        for f in repo_path.rglob("*"):
            if f.is_file() and '.git' not in str(f):
                rel_path = f.relative_to(repo_path)
                files.append({
                    "path": str(rel_path),
                    "size": f.stat().st_size,
                    "modified": f.stat().st_mtime
                })
        
        # Get recent commits
        git_log = self._run_git(repo_path, ["log", "--oneline", "-10"])
        
        # Check CI status
        ci_status = self._check_ci_status(repo_path)
        
        observation = {
            "repo": str(repo_path),
            "file_count": len(files),
            "languages": self._detect_languages(files),
            "recent_commits": git_log.split("\n") if git_log else [],
            "ci_status": ci_status,
            "timestamp": time.time()
        }
        
        # Write to brain: "I observed this repo"
        self._write_observation_to_cortex(f"repo:{repo_path}", observation)
        
        return observation
    
    def orient_with_brain(self, repo_path: str, task_description: str) -> Dict:
        """
        ORIENT: Query brain for context
        
        Ask:
        - Have I worked on this repo before?
        - Similar past tasks?
        - Current system state (coordination with other agents)
        """
        # Read cortical state for this repo
        cortex_state = self.brain.read_cortex(
            regions=[0, 1, 2],  # Code-related regions
            max_hotspots=32
        )
        
        # Query temporal memory (via cortex_stats or direct read)
        temporal = cortex_state.temporal_context if cortex_state else []
        
        # Get brain status
        brain_status = self.brain.get_brain_status()
        
        orientation = {
            "task": task_description,
            "repo": repo_path,
            "cortex_coherence": cortex_state.coherence if cortex_state else 0,
            "temporal_depth": len(temporal),
            "brain_tick": brain_status.tick if brain_status else 0,
            "brain_phase": brain_status.phase if brain_status else "unknown",
            "past_similar_work": self._find_similar_tasks(repo_path)
        }
        
        return orientation
    
    def decide_changes(self, observation: Dict, orientation: Dict) -> CodeTask:
        """
        DECIDE: Plan code changes
        
        Uses LLM + brain context to decide what to do
        """
        task_id = f"task_{int(time.time())}"
        
        # Build context for LLM
        context = {
            "observation": observation,
            "orientation": orientation,
            "brain_coherence": orientation.get("cortex_coherence", 0)
        }
        
        # In real implementation: call LLM
        # For demo: simulate decision
        print(f"[CodeAgent] Deciding changes for: {context['orientation']['task']}")
        
        # Simple heuristic: if coherence high, be conservative
        # if coherence low, be aggressive (fresh start)
        coherence = orientation.get("cortex_coherence", 0)
        
        if coherence > 0.5:
            strategy = "conservative"  # Similar to past work
        else:
            strategy = "exploratory"   # New territory
        
        # Create task
        task = CodeTask(
            task_id=task_id,
            description=context['orientation']['task'],
            repo_path=observation['repo'],
            target_files=[],  # To be filled
            generated_code={},
            status="pending"
        )
        
        # Write decision to brain
        self.brain.write_thought(
            f"Decided strategy {strategy} for task {task_id}",
            priority=0.8
        )
        
        self.current_task = task
        return task
    
    def act_generate_code(self, task: CodeTask, files_to_modify: List[str]) -> bool:
        """
        ACT: Generate and write code
        """
        task.status = "in_progress"
        
        for file_path in files_to_modify:
            # Read existing content
            full_path = Path(task.repo_path) / file_path
            
            if full_path.exists():
                with open(full_path, 'r') as f:
                    existing = f.read()
            else:
                existing = ""
            
            # In real: LLM generates code
            # For demo: simulate
            generated = self._simulate_code_generation(
                task.description,
                file_path,
                existing
            )
            
            task.generated_code[file_path] = generated
            
            # Write to disk
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(generated)
            
            print(f"[CodeAgent] Generated: {file_path}")
        
        task.status = "completed"
        
        # Write to brain: "I did this work"
        self._write_completion_to_cortex(task)
        
        return True
    
    def learn_from_feedback(self, task: CodeTask, test_results: Dict):
        """
        LEARN: Update brain with results
        
        Writes success/failure patterns to cortex for future reference
        """
        task.test_results = test_results
        
        success = test_results.get("success", False)
        
        if success:
            # Reinforce: this pattern worked
            self.brain.write_thought(
                f"Task {task.task_id} succeeded. Pattern validated.",
                priority=1.0
            )
        else:
            # Mark: avoid this pattern
            self.brain.write_thought(
                f"Task {task.task_id} failed: {test_results.get('error', 'unknown')}",
                priority=0.9
            )
        
        # Persist task to brain's long-term memory
        self.brain.ingest(
            content=json.dumps(asdict(task)),
            source="code_agent",
            priority=0.7
        )
    
    def resume_from_brain(self) -> Optional[CodeTask]:
        """
        Resume interrupted work from brain state
        
        Called on startup to check if there was pending work
        """
        # Read last known state
        snapshot = self.brain.read_cortex(max_hotspots=64)
        
        if snapshot.coherence > 0.1:
            print(f"[CodeAgent] Resuming from tick {snapshot.tick}")
            
            # Query for incomplete tasks
            # In real: would read from persistence
            # For demo: return None
            return None
        
        return None
    
    # === Helper methods ===
    
    def _run_git(self, repo_path: Path, args: List[str]) -> str:
        """Run git command"""
        try:
            result = subprocess.run(
                ["git", "-C", str(repo_path)] + args,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout
        except:
            return ""
    
    def _check_ci_status(self, repo_path: Path) -> str:
        """Check CI status (placeholder)"""
        # Would check GitHub Actions, etc.
        return "unknown"
    
    def _detect_languages(self, files: List[Dict]) -> Dict[str, int]:
        """Detect programming languages by extension"""
        exts = {}
        for f in files:
            ext = Path(f['path']).suffix
            exts[ext] = exts.get(ext, 0) + 1
        return exts
    
    def _write_observation_to_cortex(self, key: str, data: Dict):
        """Write observation to brain cortex"""
        # Encode to simple representation
        text = f"observed:{key} files:{data.get('file_count', 0)}"
        self.brain.write_thought(text, priority=0.6)
    
    def _find_similar_tasks(self, repo_path: str) -> List[Dict]:
        """Find similar past tasks from brain memory"""
        # Read cortex state and check temporal context
        snapshot = self.brain.read_cortex(regions=list(range(8)), max_hotspots=32)
        
        # Filter for code-related patterns from temporal context
        similar = []
        if snapshot:
            for ctx in snapshot.temporal_context:
                if isinstance(ctx, dict) and ctx.get('pattern_hash', '').startswith('code'):
                    similar.append(ctx)
        
        return similar
    
    def _simulate_code_generation(self, description: str, file_path: str, existing: str) -> str:
        """Simulate code generation (placeholder for LLM)"""
        return f"""# Generated by {self.agent_id}
# Task: {description}
# File: {file_path}

# TODO: Implement actual code generation with LLM
# This is a placeholder

def placeholder_function():
    \"\"\"Placeholder implementation\"\"\""
    return "Code would be generated here"

if __name__ == "__main__":
    result = placeholder_function()
    print(result)
"""
    
    def _write_completion_to_cortex(self, task: CodeTask):
        """Write completion to cortex"""
        summary = f"completed:{task.task_id} files:{len(task.generated_code)}"
        self.brain.write_thought(summary, priority=0.8)


def demo_code_agent():
    """Demonstrate code agent"""
    print("=" * 70)
    print("  CODE AGENT DEMO")
    print("  OODA Loop with Brain Integration")
    print("=" * 70)
    
    # Create agent
    agent = CodeAgent(agent_id="code_agent_demo")
    
    # Check for existing work
    print("\n[1] Checking brain for interrupted work...")
    pending = agent.resume_from_brain()
    if pending:
        print(f"   Resuming task: {pending.task_id}")
    else:
        print("   No pending work found")
    
    # Create test repo
    test_repo = Path("/tmp/test_repo")
    test_repo.mkdir(exist_ok=True)
    (test_repo / "main.py").write_text("# Initial code\nprint('hello')\n")
    
    # OODA Loop
    print("\n[2] OBSERVE: Analyze repository")
    obs = agent.observe_repo(str(test_repo))
    print(f"   Files: {obs['file_count']}")
    print(f"   Languages: {obs['languages']}")
    
    print("\n[3] ORIENT: Query brain context")
    orientation = agent.orient_with_brain(
        str(test_repo),
        "Add error handling and logging"
    )
    print(f"   Cortex coherence: {orientation['cortex_coherence']:.3f}")
    print(f"   Brain phase: {orientation['brain_phase']}")
    print(f"   Past similar work: {len(orientation['past_similar_work'])} items")
    
    print("\n[4] DECIDE: Plan changes")
    task = agent.decide_changes(obs, orientation)
    print(f"   Task ID: {task.task_id}")
    print(f"   Description: {task.description}")
    
    print("\n[5] ACT: Generate code")
    agent.act_generate_code(task, ["main.py", "utils.py"])
    print(f"   Generated {len(task.generated_code)} files")
    
    print("\n[6] LEARN: Store results")
    test_results = {"success": True, "tests_passed": 5, "tests_failed": 0}
    agent.learn_from_feedback(task, test_results)
    print("   Feedback stored in brain")
    
    print("\n[7] Verify persistence")
    stats = agent.brain.get_cortex_stats()
    if stats:
        print(f"   Agents registered: {len(stats.get('agents', {}))}")
    
    print("\n" + "=" * 70)
    print("  CODE AGENT DEMO COMPLETE")
    print("=" * 70)
    print("\nOODA Loop with brain integration:")
    print("  Observe → Orient (brain query) → Decide → Act → Learn (brain store)")
    print("\nThe code agent now has:")
    print("  - Persistent memory across sessions")
    print("  - Coordination with other agents via brain")
    print("  - Temporal reasoning about past work")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_code_agent()
    else:
        print("Usage: python3 code_agent.py --demo")
