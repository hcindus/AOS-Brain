import time

class LimbicAgent:
    def __init__(self, cfg, hippocampus=None):
        self.cfg = cfg
        self.hippo = hippocampus
        self.novelty_history = []
        self.reward_history = []
        
    def evaluate(self, obs, ctx):
        """
        Evaluate affect (reward/novelty) based on observation and context.
        Connects to hippocampus for novelty calculation.
        """
        # Calculate novelty from hippocampus if available
        novelty = 0.0
        if self.hippo and hasattr(self.hippo, 'calculate_novelty'):
            try:
                trace = {"obs": obs, "ctx": ctx, "timestamp": time.time()}
                novelty = self.hippo.calculate_novelty(trace)
            except Exception as e:
                novelty = 0.5  # Default on error
        else:
            # Fallback: estimate novelty from context size
            if ctx and isinstance(ctx, dict):
                ctx_str = str(ctx.get("context", ""))
                novelty = min(len(ctx_str) / 1000, 1.0)
            else:
                novelty = 0.5
        
        self.novelty_history.append(novelty)
        if len(self.novelty_history) > 100:
            self.novelty_history = self.novelty_history[-100:]
        
        # Calculate reward based on action success (simplified)
        # In real implementation, this would compare predicted vs actual outcomes
        reward = self._calculate_reward(obs, ctx)
        self.reward_history.append(reward)
        if len(self.reward_history) > 100:
            self.reward_history = self.reward_history[-100:]
        
        return {
            "reward": reward, 
            "novelty": novelty, 
            "mode": self.cfg.get("modes", {}).get("active_mode", "adaptive"),
            "novelty_avg": sum(self.novelty_history) / len(self.novelty_history) if self.novelty_history else 0.0,
            "reward_avg": sum(self.reward_history) / len(self.reward_history) if self.reward_history else 0.0
        }
    
    def _calculate_reward(self, obs, ctx):
        """
        Calculate reward signal based on observation.
        Higher reward for successful actions, lower for errors.
        """
        # Check for error indicators in observation
        obs_str = str(obs)
        
        if "error" in obs_str.lower() or "fail" in obs_str.lower():
            return -0.5
        elif "success" in obs_str.lower() or "complete" in obs_str.lower():
            return 0.8
        elif "noop" in obs_str.lower():
            return 0.1  # Neutral for no-ops
        else:
            return 0.3  # Slight positive for normal operation
