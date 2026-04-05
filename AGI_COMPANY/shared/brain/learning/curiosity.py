"""
Curiosity Module
Curiosity-driven exploration.
"""

import math
import random
from collections import defaultdict

# Global visit tracking
visit_count = defaultdict(int)


def register_concept_use(concepts):
    """Track concept usage"""
    for c in concepts:
        visit_count[c] += 1


def curiosity_score(concept):
    """
    Calculate curiosity score.
    
    Higher score = more novel/less familiar
    """
    v = visit_count[concept]
    if v == 0:
        return 1.0
    return 1.0 / (1.0 + math.log(1 + v))


def pick_curiosity_target(TRACRAY, top_k=10):
    """
    Pick a concept to explore based on curiosity.
    
    Args:
        TRACRAY: Tracray lexicon
        top_k: Number of top candidates to choose from
    """
    scores = []
    for name in TRACRAY.get("concepts", {}).keys():
        scores.append((curiosity_score(name), name))
        
    if not scores:
        return None
        
    scores.sort(reverse=True)
    top = scores[:min(top_k, len(scores))]
    return random.choice(top)[1]


class CuriosityAgent:
    """
    Curiosity-driven exploration agent.
    """
    
    def __init__(self, tracray, sheet, novelty_threshold=0.7, exploration_rate=0.1):
        self.tracray = tracray
        self.sheet = sheet
        self.novelty_threshold = novelty_threshold
        self.exploration_rate = exploration_rate
        
    def act(self):
        """
        Execute curiosity-driven action.
        
        Returns:
            Name of concept explored, or None
        """
        target_name = pick_curiosity_target(self.tracray)
        
        if not target_name:
            return None
            
        if target_name not in self.tracray.get("concepts", {}):
            return None
            
        spec = self.tracray["concepts"][target_name]
        if "coord" not in spec:
            return None
            
        x, y, z = spec["coord"]
        self.sheet.excite_region(int(x), int(y), int(z), radius=2)
        
        return target_name
        
    def should_explore(self, current_novelty):
        """
        Decide whether to explore vs exploit.
        
        Args:
            current_novelty: Current novelty level (0.0 to 1.0)
        """
        return current_novelty > self.novelty_threshold or random.random() < self.exploration_rate
