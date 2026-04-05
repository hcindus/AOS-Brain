#!/usr/bin/env python3
"""
Learning Engine - User Style and Company Knowledge.

Learns:
- User communication patterns
- Work habits and preferences
- Company knowledge from GitHub
- Task success/failure patterns
"""

import os
import sys
import json
import time
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from collections import Counter


class UserStyleLearner:
    """
    Learns user's communication style and preferences.
    """
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.data_file = Path.home() / ".aos" / "brain" / f"user_style_{user_id}.json"
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Style patterns
        self.patterns = {
            "greeting_style": [],
            "response_length": [],
            "formality": "casual",  # formal, casual, mixed
            "emoji_usage": 0.0,
            "questions_vs_statements": 0.5,
            "preferred_times": [],
            "common_phrases": Counter(),
            "urgency_indicators": [],
        }
        
        self._load()
    
    def learn_from_interaction(self, user_input: str, agent_response: str):
        """Learn from each interaction."""
        # Analyze user input
        words = user_input.lower().split()
        
        # Formality
        if any(w in words for w in ["please", "thank you", "would you"]):
            self.patterns["formality"] = "polite"
        
        # Emoji usage
        emoji_count = len(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', user_input))
        if emoji_count > 0:
            self.patterns["emoji_usage"] = min(1.0, self.patterns["emoji_usage"] + 0.1)
        
        # Common phrases
        for phrase in self._extract_phrases(user_input):
            self.patterns["common_phrases"][phrase] += 1
        
        # Save periodically
        if sum(self.patterns["common_phrases"].values()) % 10 == 0:
            self._save()
    
    def _extract_phrases(self, text: str) -> List[str]:
        """Extract meaningful phrases."""
        # Simple extraction
        words = text.lower().split()
        return [" ".join(words[i:i+2]) for i in range(len(words)-1)]
    
    def get_style_recommendation(self) -> Dict:
        """Get style recommendations for agent."""
        return {
            "formality": self.patterns["formality"],
            "use_emojis": self.patterns["emoji_usage"] > 0.3,
            "response_length": "medium",  # short, medium, long
            "common_phrases": list(self.patterns["common_phrases"].keys())[:5]
        }
    
    def _load(self):
        if self.data_file.exists():
            try:
                with open(self.data_file) as f:
                    data = json.load(f)
                    self.patterns.update(data.get("patterns", {}))
            except:
                pass
    
    def _save(self):
        with open(self.data_file, 'w') as f:
            json.dump({"patterns": dict(self.patterns)}, f, indent=2)


class CompanyKnowledgeLearner:
    """
    Learns company knowledge from GitHub repositories.
    """
    
    def __init__(self, org: str = "hcindus"):
        self.org = org
        self.knowledge_file = Path.home() / ".aos" / "brain" / f"company_knowledge_{org}.json"
        self.knowledge_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.knowledge = {
            "repositories": {},
            "technologies": Counter(),
            "contributors": {},
            "code_patterns": [],
            "documentation": []
        }
        
        self._load()
    
    def learn_from_github(self, repo_path: Optional[str] = None):
        """Learn from GitHub repos."""
        if repo_path and os.path.exists(repo_path):
            self._scan_local_repo(repo_path)
        
        # Try to get GitHub data via gh CLI
        self._fetch_github_data()
    
    def _scan_local_repo(self, repo_path: str):
        """Scan a local git repository."""
        repo_name = os.path.basename(repo_path)
        
        print(f"[CompanyLearner] Scanning {repo_name}...")
        
        # Count file types
        file_types = Counter()
        for root, dirs, files in os.walk(repo_path):
            if '.git' in root:
                continue
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext:
                    file_types[ext] += 1
        
        self.knowledge["repositories"][repo_name] = {
            "file_types": dict(file_types),
            "last_scanned": time.time()
        }
        
        # Update technologies
        tech_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.cpp': 'C++',
            '.hpp': 'C++',
            '.h': 'C/C++',
            '.go': 'Go',
            '.rs': 'Rust',
            '.java': 'Java',
        }
        
        for ext, count in file_types.items():
            if ext in tech_map:
                self.knowledge["technologies"][tech_map[ext]] += count
    
    def _fetch_github_data(self):
        """Fetch data from GitHub API."""
        try:
            # Try to use gh CLI
            result = subprocess.run(
                ["gh", "repo", "list", self.org, "--json", "name,description,language"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                repos = json.loads(result.stdout)
                for repo in repos:
                    name = repo.get("name")
                    self.knowledge["repositories"][name] = {
                        "description": repo.get("description", ""),
                        "language": repo.get("language", "Unknown"),
                        "fetched": time.time()
                    }
                    
                    if repo.get("language"):
                        self.knowledge["technologies"][repo["language"]] += 1
                        
        except Exception as e:
            print(f"[CompanyLearner] Could not fetch GitHub data: {e}")
    
    def get_company_summary(self) -> str:
        """Generate company knowledge summary."""
        lines = [f"Company: {self.org}", ""]
        
        lines.append(f"Repositories: {len(self.knowledge['repositories'])}")
        lines.append("")
        
        lines.append("Technologies:")
        for tech, count in self.knowledge["technologies"].most_common(10):
            lines.append(f"  - {tech}: {count} files/repos")
        
        return "\n".join(lines)
    
    def _load(self):
        if self.knowledge_file.exists():
            try:
                with open(self.knowledge_file) as f:
                    self.knowledge = json.load(f)
            except:
                pass
    
    def _save(self):
        with open(self.knowledge_file, 'w') as f:
            json.dump(self.knowledge, f, indent=2, default=str)


class PatternLearner:
    """
    Learns task execution patterns and resource usage.
    """
    
    def __init__(self):
        self.patterns_file = Path.home() / ".aos" / "brain" / "task_patterns.json"
        self.patterns_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.patterns = {
            "task_times": {},  # Best times for each task
            "resource_correlation": {},  # Resource usage patterns
            "success_predictors": {},  # What leads to success
            "failure_signatures": {}  # Early warning signs
        }
        
        self._load()
    
    def record_execution(self, task_name: str, success: bool, 
                        duration: float, resources: Dict):
        """Record task execution data."""
        hour = datetime.now().hour
        
        if task_name not in self.patterns["task_times"]:
            self.patterns["task_times"][task_name] = {"success_by_hour": {}, "total_by_hour": {}}
        
        task_data = self.patterns["task_times"][task_name]
        
        if hour not in task_data["success_by_hour"]:
            task_data["success_by_hour"][hour] = 0
            task_data["total_by_hour"][hour] = 0
        
        task_data["total_by_hour"][hour] += 1
        if success:
            task_data["success_by_hour"][hour] += 1
        
        # Save periodically
        if sum(task_data["total_by_hour"].values()) % 5 == 0:
            self._save()
    
    def get_optimal_time(self, task_name: str) -> Optional[int]:
        """Get optimal hour for task execution."""
        if task_name not in self.patterns["task_times"]:
            return None
        
        task_data = self.patterns["task_times"][task_name]
        best_hour = None
        best_rate = 0
        
        for hour, total in task_data["total_by_hour"].items():
            if total >= 3:  # Need sufficient data
                success = task_data["success_by_hour"].get(hour, 0)
                rate = success / total
                if rate > best_rate:
                    best_rate = rate
                    best_hour = hour
        
        return best_hour
    
    def _load(self):
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file) as f:
                    self.patterns = json.load(f)
            except:
                pass
    
    def _save(self):
        with open(self.patterns_file, 'w') as f:
            json.dump(self.patterns, f, indent=2)


if __name__ == "__main__":
    print("Learning Engine Demo")
    print("=" * 50)
    
    # User style
    user_learner = UserStyleLearner()
    user_learner.learn_from_interaction("Hey, can you help with this?", "Sure!")
    print("User style learned")
    
    # Company knowledge
    company_learner = CompanyKnowledgeLearner("hcindus")
    company_learner._scan_local_repo("/root/.openclaw/workspace/aos_brain_py")
    print(company_learner.get_company_summary())
    
    # Patterns
    pattern_learner = PatternLearner()
    pattern_learner.record_execution("test_task", True, 1.5, {"cpu": 10})
    print("Pattern recorded")
