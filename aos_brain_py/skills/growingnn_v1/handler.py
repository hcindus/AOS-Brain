#!/usr/bin/env python3
"""
GrowingNN Skill - Dynamic Neural Network Growth

Implements adaptive network growth:
- Add nodes when novelty > threshold
- Add layers when complexity > threshold  
- Prune when error rates drop

Ternary growth signals:
- Novelty: 1 = new pattern → grow
- Error: -1 = high error → grow
- Complexity: 0.9+ → add layer
"""

import math
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class GrowingNN:
    """Self-growing neural network."""
    
    # Architecture
    layers: List[int] = field(default_factory=lambda: [8, 12, 40])
    nodes: int = 60
    max_nodes: int = 10000
    max_layers: int = 7
    
    # Growth thresholds
    add_node_threshold: Dict = field(default_factory=lambda: {'novelty': 0.8, 'error': 0.6})
    add_layer_threshold: float = 0.9
    
    # State
    novelty_history: List[float] = field(default_factory=list)
    error_history: List[float] = field(default_factory=list)
    growth_events: int = 0
    last_growth: float = 0.0
    
    def compute_complexity(self) -> float:
        """Compute network complexity score."""
        if not self.novelty_history:
            return 0.0
        
        # Complexity = variance in novelty + error rate
        avg_novelty = sum(self.novelty_history) / len(self.novelty_history)
        variance = sum((n - avg_novelty) ** 2 for n in self.novelty_history) / len(self.novelty_history)
        
        avg_error = sum(self.error_history) / len(self.error_history) if self.error_history else 0.0
        
        complexity = (variance * 0.7) + (avg_error * 0.3)
        return min(1.0, complexity)
    
    def should_add_node(self, novelty: float, error: float) -> bool:
        """Check if should add node."""
        if self.nodes >= self.max_nodes:
            return False
        
        # Trigger on high novelty OR high error
        if novelty > self.add_node_threshold['novelty']:
            return True
        if error > self.add_node_threshold['error']:
            return True
        
        return False
    
    def should_add_layer(self) -> bool:
        """Check if should add layer."""
        if len(self.layers) >= self.max_layers:
            return False
        
        complexity = self.compute_complexity()
        return complexity > self.add_layer_threshold
    
    def add_node(self) -> Dict:
        """Add a node to the network."""
        # Add to last layer
        self.layers[-1] += 1
        self.nodes += 1
        self.growth_events += 1
        self.last_growth = time.time()
        
        return {
            'action': 'add_node',
            'layers': self.layers.copy(),
            'total_nodes': self.nodes,
            'growth_event': self.growth_events
        }
    
    def add_layer(self) -> Dict:
        """Add a new layer."""
        if len(self.layers) >= self.max_layers:
            return {'error': 'Max layers reached'}
        
        # New layer size = average of last two
        new_size = (self.layers[-1] + self.layers[-2]) // 2
        self.layers.append(max(new_size, 10))  # Minimum 10 nodes
        self.nodes += self.layers[-1]
        self.growth_events += 1
        self.last_growth = time.time()
        
        return {
            'action': 'add_layer',
            'layers': self.layers.copy(),
            'total_nodes': self.nodes,
            'growth_event': self.growth_events
        }
    
    def update(self, novelty: float, error: float) -> Optional[Dict]:
        """Update GrowingNN and trigger growth if needed."""
        # Track history
        self.novelty_history.append(novelty)
        self.error_history.append(error)
        
        # Keep last 100
        self.novelty_history = self.novelty_history[-100:]
        self.error_history = self.error_history[-100:]
        
        # Check growth triggers
        if self.should_add_layer():
            return self.add_layer()
        
        if self.should_add_node(novelty, error):
            return self.add_node()
        
        return None
    
    def get_status(self) -> Dict:
        """Get GrowingNN status."""
        return {
            'layers': self.layers.copy(),
            'total_nodes': self.nodes,
            'growth_events': self.growth_events,
            'complexity': self.compute_complexity(),
            'last_growth': self.last_growth
        }


# Skill handler
def growingnn_handler(input_data: Dict) -> Dict:
    """
    GrowingNN skill - dynamic network growth.
    
    Input:
        action: 'update' | 'status' | 'force_grow'
        novelty: float (0-1)
        error: float (0-1)
        
    Output:
        status: Current network state
        growth: Growth event if triggered
    """
    if not hasattr(growingnn_handler, '_growingnn'):
        growingnn_handler._growingnn = GrowingNN()
    
    gnn = growingnn_handler._growingnn
    action = input_data.get('action', 'status')
    
    if action == 'update':
        novelty = input_data.get('novelty', 0.0)
        error = input_data.get('error', 0.0)
        
        growth = gnn.update(novelty, error)
        
        return {
            'status': gnn.get_status(),
            'growth_triggered': growth is not None,
            'growth': growth
        }
    
    elif action == 'force_grow':
        # Force a growth event
        if input_data.get('type') == 'layer' and len(gnn.layers) < gnn.max_layers:
            growth = gnn.add_layer()
        else:
            growth = gnn.add_node()
        
        return {
            'status': gnn.get_status(),
            'growth': growth,
            'forced': True
        }
    
    else:  # status
        return {'status': gnn.get_status()}


if __name__ == '__main__':
    # Demo growth
    print("🌱 GrowingNN - Dynamic Neural Growth")
    print("=" * 50)
    
    gnn = GrowingNN()
    print(f"Initial: {gnn.layers} = {gnn.nodes} nodes")
    
    # Simulate high novelty
    for i in range(10):
        result = gnn.update(novelty=0.9, error=0.2)
        if result:
            print(f"Growth event: {result['action']}")
            print(f"  Now: {gnn.layers} = {gnn.nodes} nodes")
    
    print(f"\nFinal: {gnn.layers} = {gnn.nodes} nodes")
    print(f"Growth events: {gnn.growth_events}")
