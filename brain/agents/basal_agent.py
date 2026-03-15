import numpy as np
import time

class BasalAgent:
    def __init__(self, cfg):
        self.cfg = cfg
        
        # Error tracking for GrowingNN
        self.prediction_history = []
        self.error_rate = 0.0
        self.max_history = 100
        
        # GrowingNN Configuration
        self.growing_config = cfg.get("growingnn", {})
        self.node_threshold = self.growing_config.get("add_node_threshold", {"novelty": 0.8, "error": 0.6})
        self.layer_threshold = self.growing_config.get("add_layer_threshold", {"complexity": 0.9})
        
        # Neural Network State
        self.policy_nn = {
            "layers": 3,
            "nodes": [8, 12, 16],
            "activations": [[0.8]*8, [0.5]*12, [0.9]*16],
            "growth_history": []
        }
        
        # Complexity tracking
        self.complexity_scores = []
        
    def execute(self, action, affect):
        """Execute action and track outcomes for error calculation."""
        # Store action for later outcome comparison
        self.last_action = action
        self.last_affect = affect
        
        # Log execution
        print(f"[Basal] Executing: {action.get('type', 'unknown')}")
        
        return {"status": "executed", "action": action}

    def track_error(self, predicted_outcome, actual_outcome):
        """
        Calculate error between predicted and actual outcomes.
        Returns error rate 0.0-1.0.
        """
        if predicted_outcome is None or actual_outcome is None:
            return 0.0
        
        try:
            # Simple error calculation - can be enhanced
            if isinstance(predicted_outcome, (int, float)) and isinstance(actual_outcome, (int, float)):
                error = abs(predicted_outcome - actual_outcome) / max(abs(predicted_outcome), 0.001)
            else:
                # String similarity for non-numeric outcomes
                pred_str = str(predicted_outcome)
                actual_str = str(actual_outcome)
                # Simple Levenshtein-inspired distance
                error = self._string_distance(pred_str, actual_str)
            
            error = min(error, 1.0)  # Cap at 1.0
            self.prediction_history.append(error)
            
            # Keep only recent history
            if len(self.prediction_history) > self.max_history:
                self.prediction_history = self.prediction_history[-self.max_history:]
            
            # Calculate rolling average
            self.error_rate = np.mean(self.prediction_history)
            
            return self.error_rate
        except Exception as e:
            print(f"[Basal] Error calculation failed: {e}")
            return 0.0

    def _string_distance(self, s1, s2):
        """Calculate normalized string distance."""
        if len(s1) == 0 and len(s2) == 0:
            return 0.0
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 0.0
        
        # Simple character difference ratio
        matches = sum(c1 == c2 for c1, c2 in zip(s1, s2))
        return 1.0 - (matches / max_len)

    def calculate_complexity(self, obs, ctx):
        """
        Calculate task complexity based on observation and context.
        Returns 0.0-1.0.
        """
        complexity = 0.0
        
        # Factor 1: Context size
        if ctx and isinstance(ctx, dict):
            ctx_str = str(ctx.get("context", ""))
            complexity += min(len(ctx_str) / 1000, 0.3)  # Up to 0.3
        
        # Factor 2: Observation complexity
        if obs and isinstance(obs, dict):
            obs_str = str(obs)
            complexity += min(len(obs_str) / 500, 0.3)  # Up to 0.3
        
        # Factor 3: Historical complexity trend
        if self.complexity_scores:
            avg_complexity = np.mean(self.complexity_scores[-50:])
            complexity += avg_complexity * 0.4  # Up to 0.4
        
        complexity = min(complexity, 1.0)
        self.complexity_scores.append(complexity)
        
        if len(self.complexity_scores) > 100:
            self.complexity_scores = self.complexity_scores[-100:]
        
        return complexity

    def should_add_node(self, novelty, error):
        """Determine if network should grow by adding a node."""
        novelty_trigger = novelty >= self.node_threshold["novelty"]
        error_trigger = error >= self.node_threshold["error"]
        
        return novelty_trigger or error_trigger

    def should_add_layer(self, complexity):
        """Determine if network should grow by adding a layer."""
        return complexity >= self.layer_threshold["complexity"]

    def add_node(self):
        """Add a node to the last layer."""
        if not self.policy_nn["nodes"]:
            return
        
        last_layer_idx = len(self.policy_nn["nodes"]) - 1
        self.policy_nn["nodes"][last_layer_idx] += 1
        
        # Add activation for new node
        self.policy_nn["activations"][last_layer_idx].append(0.5)
        
        # Log growth
        growth_event = {
            "timestamp": time.time(),
            "type": "add_node",
            "layer": last_layer_idx,
            "new_size": self.policy_nn["nodes"][last_layer_idx]
        }
        self.policy_nn["growth_history"].append(growth_event)
        
        print(f"[GrowingNN] Added node to layer {last_layer_idx}. Total nodes: {sum(self.policy_nn['nodes'])}")

    def add_layer(self):
        """Add a new layer to the network."""
        self.policy_nn["layers"] += 1
        self.policy_nn["nodes"].append(8)  # Start with 8 nodes
        self.policy_nn["activations"].append([0.5] * 8)
        
        # Log growth
        growth_event = {
            "timestamp": time.time(),
            "type": "add_layer",
            "new_layer": self.policy_nn["layers"],
            "total_nodes": sum(self.policy_nn["nodes"])
        }
        self.policy_nn["growth_history"].append(growth_event)
        
        print(f"[GrowingNN] Added layer. Total layers: {self.policy_nn['layers']}, Total nodes: {sum(self.policy_nn['nodes'])}")

    def get_nn_state(self):
        """Return current neural network state."""
        return {
            "layers": self.policy_nn["layers"],
            "nodes": self.policy_nn["nodes"],
            "activations": self.policy_nn["activations"],
            "total_nodes": sum(self.policy_nn["nodes"]),
            "growth_events": len(self.policy_nn["growth_history"]),
            "error_rate": self.error_rate,
            "avg_complexity": np.mean(self.complexity_scores) if self.complexity_scores else 0.0
        }

    def get_stats(self):
        """Return comprehensive stats for state writer."""
        return {
            "error_rate": self.error_rate,
            "prediction_count": len(self.prediction_history),
            "complexity_current": self.complexity_scores[-1] if self.complexity_scores else 0.0,
            "complexity_avg": np.mean(self.complexity_scores[-50:]) if self.complexity_scores else 0.0,
            "nn_state": self.get_nn_state()
        }
