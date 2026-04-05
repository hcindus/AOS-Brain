#!/usr/bin/env python3
"""Agent Learning System - Agents learn from experiences and share knowledge"""

import json
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class Experience:
    """Single learning experience"""
    agent_id: str
    action: str
    result: str
    reward: float
    context: Dict
    timestamp: str

class AgentLearning:
    """Distributed learning system for all agents"""
    
    def __init__(self):
        self.experiences: List[Experience] = []
        self.skill_matrix: Dict[str, Dict] = {}
        self.knowledge_pool: Dict[str, any] = {}
        
    def record_experience(self, agent_id: str, action: str, result: str, reward: float, context: Dict):
        """Record an agent's experience"""
        from datetime import datetime
        exp = Experience(agent_id, action, result, reward, context, datetime.now().isoformat())
        self.experiences.append(exp)
        
        # Update skill matrix
        if agent_id not in self.skill_matrix:
            self.skill_matrix[agent_id] = {}
        if action not in self.skill_matrix[agent_id]:
            self.skill_matrix[agent_id][action] = {"attempts": 0, "success": 0, "avg_reward": 0.0}
        
        self.skill_matrix[agent_id][action]["attempts"] += 1
        if reward > 0:
            self.skill_matrix[agent_id][action]["success"] += 1
        
        # Update average reward
        old_avg = self.skill_matrix[agent_id][action]["avg_reward"]
        new_avg = old_avg + 0.1 * (reward - old_avg)
        self.skill_matrix[agent_id][action]["avg_reward"] = new_avg
        
    def share_knowledge(self, from_agent: str, to_agent: str, skill: str):
        """Transfer learned skills between agents"""
        if from_agent in self.skill_matrix and skill in self.skill_matrix[from_agent]:
            skill_data = self.skill_matrix[from_agent][skill]
            
            if to_agent not in self.skill_matrix:
                self.skill_matrix[to_agent] = {}
            
            # Transfer with some degradation (learning isn't perfect)
            self.skill_matrix[to_agent][skill] = {
                "attempts": skill_data["attempts"] * 0.5,
                "success": skill_data["success"] * 0.5,
                "avg_reward": skill_data["avg_reward"] * 0.8,
                "learned_from": from_agent
            }
            return True
        return False
    
    def get_best_practice(self, skill: str) -> Tuple[str, float]:
        """Find which agent is best at a skill"""
        best_agent = None
        best_score = -float('inf')
        
        for agent, skills in self.skill_matrix.items():
            if skill in skills:
                score = skills[skill]["avg_reward"] * (skills[skill]["success"] / max(1, skills[skill]["attempts"]))
                if score > best_score:
                    best_score = score
                    best_agent = agent
        
        return best_agent, best_score
    
    def teach_all(self, skill: str, teacher: str = None):
        """Best agent teaches skill to everyone"""
        if teacher is None:
            teacher, _ = self.get_best_practice(skill)
        
        if teacher:
            for agent in self.skill_matrix.keys():
                if agent != teacher:
                    self.share_knowledge(teacher, agent, skill)
            return True
        return False
