#!/usr/bin/env python3
"""
Dynamic Threshold Adjustment Module
Automatically adjusts GrowingNN thresholds based on performance
"""

import json
import time
import sqlite3
import os
from collections import deque

class DynamicThresholds:
    """
    Adjusts novelty and error thresholds based on system performance
    Prevents runaway growth or stagnation
    """
    
    def __init__(self):
        self.threshold_history = deque(maxlen=100)
        self.current_novelty_threshold = 0.8
        self.current_error_threshold = 0.6
        self.performance_window = []
        
        # Target metrics
        self.target_growth_rate = 0.1  # 10% growth per hour
        self.target_error_rate = 0.05  # 5% error rate
        
    def analyze_performance(self, metrics):
        """Analyze recent performance and suggest threshold adjustments"""
        
        # Calculate growth rate
        if len(self.performance_window) >= 2:
            old_nodes = self.performance_window[0]['nodes']
            new_nodes = self.performance_window[-1]['nodes']
            time_diff = self.performance_window[-1]['timestamp'] - self.performance_window[0]['timestamp']
            
            if time_diff > 0:
                growth_rate = (new_nodes - old_nodes) / time_diff
                
                # Adjust thresholds based on growth rate
                if growth_rate > self.target_growth_rate * 2:
                    # Growing too fast - increase threshold
                    self.current_novelty_threshold = min(0.95, self.current_novelty_threshold + 0.05)
                    return {
                        'action': 'increase_threshold',
                        'reason': f'Growth rate {growth_rate:.3f} exceeds target',
                        'new_threshold': self.current_novelty_threshold
                    }
                
                elif growth_rate < self.target_growth_rate * 0.5:
                    # Growing too slow - decrease threshold
                    self.current_novelty_threshold = max(0.5, self.current_novelty_threshold - 0.05)
                    return {
                        'action': 'decrease_threshold',
                        'reason': f'Growth rate {growth_rate:.3f} below target',
                        'new_threshold': self.current_novelty_threshold
                    }
        
        return {'action': 'maintain', 'current_threshold': self.current_novelty_threshold}
    
    def get_optimal_thresholds(self, system_state):
        """Calculate optimal thresholds for current system state"""
        
        complexity = system_state.get('complexity', 0.5)
        memory_clusters = system_state.get('memory_clusters', 100)
        
        # Higher complexity = higher threshold (more selective)
        base_threshold = 0.8
        complexity_adjustment = complexity * 0.1
        
        # More memory = higher threshold (prevent overflow)
        memory_adjustment = min(0.1, memory_clusters / 10000)
        
        optimal_novelty = base_threshold + complexity_adjustment + memory_adjustment
        optimal_novelty = min(0.95, max(0.5, optimal_novelty))
        
        return {
            'novelty_threshold': optimal_novelty,
            'error_threshold': self.current_error_threshold,
            'complexity_factor': complexity_adjustment,
            'memory_factor': memory_adjustment
        }
    
    def log_threshold_change(self, old_val, new_val, reason):
        """Log threshold adjustments"""
        conn = sqlite3.connect(os.path.expanduser('~/.aos/brain/state/thresholds.db'))
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS threshold_changes (
                id INTEGER PRIMARY KEY,
                timestamp REAL,
                old_threshold REAL,
                new_threshold REAL,
                reason TEXT
            )
        ''')
        
        cursor.execute('''
            INSERT INTO threshold_changes (timestamp, old_threshold, new_threshold, reason)
            VALUES (?, ?, ?, ?)
        ''', (time.time(), old_val, new_val, reason))
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    dt = DynamicThresholds()
    
    # Test with sample data
    test_state = {
        'complexity': 0.7,
        'memory_clusters': 2500,
        'nodes': 1500
    }
    
    thresholds = dt.get_optimal_thresholds(test_state)
    print("Optimal Thresholds:")
    print(f"  Novelty: {thresholds['novelty_threshold']:.3f}")
    print(f"  Error: {thresholds['error_threshold']:.3f}")
    print(f"  Complexity factor: {thresholds['complexity_factor']:.3f}")
    print(f"  Memory factor: {thresholds['memory_factor']:.3f}")
