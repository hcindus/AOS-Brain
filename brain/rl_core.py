"""
Reinforcement Core - Lightweight Symbolic RL for Agents
Fits modular, memory-driven agent architecture

Usage:
    rl = ReinforcementCore(alpha=0.2, gamma=0.9)
    rl.update("attack", reward=1.0, next_action="defend")
    action = rl.choose_action(["attack", "defend", "flee"])
"""

import math
import random
from collections import defaultdict
from datetime import datetime


class ReinforcementCore:
    """
    Lightweight temporal-difference RL for symbolic agents.
    Updates action utilities based on rewards.
    """
    
    def __init__(self, alpha=0.2, gamma=0.9):
        self.alpha = alpha      # Learning rate
        self.gamma = gamma      # Discount factor
        self.utilities = {}     # action -> utility score
        self.history = []      # For debugging/visualization
    
    def get_utility(self, action):
        """Get utility of an action (default 0.0)"""
        return self.utilities.get(action, 0.0)
    
    def update(self, action, reward, next_action=None):
        """
        Temporal-difference update:
        U(a) <- U(a) + alpha * (r + gamma * U(a') - U(a))
        """
        u = self.get_utility(action)
        u_next = self.get_utility(next_action) if next_action else 0.0
        
        td_error = reward + self.gamma * u_next - u
        self.utilities[action] = u + self.alpha * td_error
        
        # Log for memory
        self.history.append({
            "action": action,
            "reward": reward,
            "utility": self.utilities[action],
            "td_error": td_error,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep last 1000 updates
        if len(self.history) > 1000:
            self.history = self.history[-1000:]
        
        return self.utilities[action]
    
    def choose_action(self, actions, explore_rate=0.1):
        """
        Choose action using softmax exploration.
        Higher utility = higher probability.
        """
        if not actions:
            return None
        
        # If exploring (random chance)
        if random.random() < explore_rate:
            return random.choice(actions)
        
        # Softmax: exp(utility) / sum(exp(utilities))
        scores = {}
        for a in actions:
            scores[a] = math.exp(self.get_utility(a))
        
        total = sum(scores.values())
        if total == 0:
            return random.choice(actions)
        
        probs = {a: s/total for a, s in scores.items()}
        
        # Weighted random choice
        r = random.random()
        cumulative = 0.0
        for a, p in probs.items():
            cumulative += p
            if r <= cumulative:
                return a
        
        return list(probs.keys())[-1]
    
    def get_stats(self):
        """Get RL stats"""
        return {
            "actions_learned": len(self.utilities),
            "total_updates": len(self.history),
            "utilities": dict(self.utilities),
            "avg_reward": sum(h["reward"] for h in self.history) / len(self.history) if self.history else 0
        }


class CuriosityCore:
    """
    Curiosity-driven exploration.
    Rewards novelty in the semantic graph.
    """
    
    def __init__(self, beta=0.3):
        self.beta = beta       # Curiosity strength
        self.last_state = None
    
    def compute_reward(self, state, new_nodes=0, new_edges=0):
        """
        Compute curiosity reward based on novelty.
        r = beta * (new_nodes + new_edges)
        """
        novelty = new_nodes + new_edges
        reward = self.beta * novelty
        self.last_state = state
        return reward


class DevelopmentalStages:
    """
    Developmental stages that affect learning rate and curiosity.
    Gives agents personality arcs over time.
    """
    
    STAGES = {
        "infant":    {"alpha": 0.5, "beta": 0.8, "description": "chaotic exploration"},
        "juvenile":  {"alpha": 0.3, "beta": 0.5, "description": "skill acquisition"},
        "adult":     {"alpha": 0.2, "beta": 0.3, "description": "stable habits"},
        "elder":     {"alpha": 0.1, "beta": 0.1, "description": "conservative, wise"},
    }
    
    def __init__(self, age_ticks=0):
        self.age_ticks = age_ticks
        self.stage = self._determine_stage(age_ticks)
    
    def _determine_stage(self, ticks):
        """Determine stage based on age"""
        if ticks < 1000:
            return "infant"
        elif ticks < 10000:
            return "juvenile"
        elif ticks < 100000:
            return "adult"
        else:
            return "elder"
    
    def get_params(self):
        """Get alpha and beta for current stage"""
        return self.STAGES[self.stage]["alpha"], self.STAGES[self.stage]["beta"]
    
    def tick(self):
        """Age the agent"""
        self.age_ticks += 1
        old_stage = self.stage
        self.stage = self._determine_stage(self.age_ticks)
        
        if old_stage != self.stage:
            return f"Stage change: {old_stage} -> {self.stage}"
        return None


class RewardSignal:
    """
    Computes rewards from environment, memory, and social signals.
    """
    
    def __init__(self):
        self.weights = {
            "action_success": 1.0,
            "resource_gain": 0.5,
            "damage_taken": -1.0,
            "danger_avoided": 0.3,
            "social_approval": 0.4,
            "novelty": 0.2,
            "task_complete": 2.0,
            "goal_achieved": 5.0,
        }
    
    def compute(self, event_type, value):
        """
        Compute reward for an event.
        event_type: one of the keys above
        value: magnitude
        """
        weight = self.weights.get(event_type, 0.0)
        return weight * value
    
    def compute_composite(self, events):
        """
        Compute composite reward from multiple events.
        events: list of (event_type, value) tuples
        """
        total = 0.0
        for event_type, value in events:
            total += self.compute(event_type, value)
        return total


# ═══════════════════════════════════════════════════════════════════
# INTEGRATION INTO AGENT LOOP
# ═══════════════════════════════════════════════════════════════════

class AgentRL:
    """
    Full RL integration for agents.
    Combines ReinforcementCore + CuriosityCore + DevelopmentalStages + RewardSignal
    """
    
    def __init__(self, agent_id="agent"):
        self.agent_id = agent_id
        self.rl = ReinforcementCore(alpha=0.2, gamma=0.9)
        self.curiosity = CuriosityCore(beta=0.3)
        self.development = DevelopmentalStages(age_ticks=0)
        self.rewards = RewardSignal()
        
        self.last_action = None
        self.last_state = None
    
    def tick(self, state, available_actions, environment_reward=0.0, novelty=0):
        """
        Full RL tick: perception -> cognition -> action -> reward -> update
        """
        # 1. Age the agent
        stage_change = self.development.tick()
        
        # 2. Adjust params based on development
        alpha, beta = self.development.get_params()
        self.rl.alpha = alpha
        self.curiosity.beta = beta
        
        # 3. Compute total reward
        reward = environment_reward
        if novelty > 0:
            reward += self.curiosity.compute_reward(state, new_nodes=novelty)
        
        # 4. Update RL with last action (if any)
        if self.last_action:
            self.rl.update(self.last_action, reward, None)
        
        # 5. Choose new action
        action = self.rl.choose_action(available_actions)
        
        # 6. Store for next tick
        self.last_action = action
        self.last_state = state
        
        return {
            "action": action,
            "reward": reward,
            "stage": self.development.stage,
            "alpha": alpha,
            "beta": beta,
            "stage_change": stage_change,
            "utilities": self.rl.utilities.copy()
        }
    
    def receive_feedback(self, feedback_type, value):
        """
        Receive explicit feedback to learn from.
        feedback_type: "success", "failure", "praise", "criticism", etc.
        """
        feedback_rewards = {
            "success": 1.0,
            "failure": -0.5,
            "praise": 0.8,
            "criticism": -0.3,
            "goal_complete": 2.0,
            "mistake": -0.4,
        }
        
        reward = feedback_rewards.get(feedback_type, 0.0) * value
        if self.last_action:
            self.rl.update(self.last_action, reward, None)
        
        return reward


# Quick test
if __name__ == "__main__":
    print("🧪 Testing Reinforcement Core...")
    
    # Create agent RL
    agent = AgentRL("doom_player")
    
    print("\n1. Infant stage (high curiosity, high learning):")
    for i in range(5):
        result = agent.tick(
            state={"step": i},
            available_actions=["attack", "defend", "flee"],
            environment_reward=random.choice([-0.1, 0.1, 0.5]),
            novelty=random.randint(0, 3)
        )
        print(f"   Step {i}: action={result['action']}, reward={result['reward']:.2f}, stage={result['stage']}")
    
    print("\n2. Getting stats:")
    stats = agent.rl.get_stats()
    print(f"   Actions learned: {stats['actions_learned']}")
    print(f"   Utilities: {stats['utilities']}")
    
    print("\n3. Explicit feedback:")
    feedback_reward = agent.receive_feedback("success", 1.0)
    print(f"   Received praise: {feedback_reward}")
    
    print("\n✅ RL Core ready for agent integration!")