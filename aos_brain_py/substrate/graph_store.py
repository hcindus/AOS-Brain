# substrate/graph_store.py
"""
Semantic graph store for neural substrate.
Nodes = concepts/thoughts
Edges = relationships
"""

import uuid
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class Node:
    """A concept/thought node in the semantic graph."""
    label: str
    embedding: List[float]
    ternary: List[int]  # [-1, 0, 1] signature
    value: float = 0.5
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    usage: int = 1
    tags: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=lambda: __import__('time').time())
    
    def strengthen(self, amount: float = 0.1):
        """Strengthen this node (Hebbian)."""
        self.usage += 1
        self.value = min(1.0, self.value + amount)


@dataclass 
class Edge:
    """Relationship between nodes."""
    source_id: str
    target_id: str
    relation: str = "assoc"  # association, causation, similarity, etc.
    weight: float = 0.1


class GraphStore:
    """
    Semantic graph for storing and growing concepts.
    
    Features:
    - Node creation with ternary signatures
    - Edge linking based on context
    - Similarity-based merging
    - Usage-based pruning
    """
    
    def __init__(self, merge_threshold: float = 0.85, prune_threshold: int = 2):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[Tuple[str, str], Edge] = {}
        self.merge_threshold = merge_threshold
        self.prune_threshold = prune_threshold
    
    def add_thought(self, thought: dict) -> Node:
        """
        Add a thought to the graph.
        
        If similar node exists, strengthen it.
        Otherwise create new node.
        """
        text = thought.get("language", "")
        emb = thought.get("embedding", [])
        tern = thought.get("ternary_code", [0, 0, 0, 0, 0])
        val = thought.get("value", {}).get("importance", 0.5)
        
        # Find similar existing node
        similar = self._find_similar_node(emb)
        
        if similar:
            # Strengthen existing node
            similar.strengthen()
            self._link_to_context(similar, thought)
            return similar
        else:
            # Create new node
            return self._create_node(text, emb, tern, val, thought)
    
    def _create_node(self, label: str, embedding: List[float], 
                     ternary: List[int], value: float, thought: dict) -> Node:
        """Create a new node and link to context."""
        node = Node(label=label[:100], embedding=embedding, 
                   ternary=ternary, value=value)
        
        # Tag based on ternary
        if ternary[1] == 1:  # positive value
            node.tags.append("salient")
        if ternary[0] == 1:  # novelty
            node.tags.append("novel")
        if ternary[4] == 1:  # growth
            node.tags.append("growing")
        
        self.nodes[node.id] = node
        self._link_to_context(node, thought)
        return node
    
    def _find_similar_node(self, embedding: List[float]) -> Optional[Node]:
        """Find most similar node above threshold."""
        if not embedding or not self.nodes:
            return None
        
        best_sim = 0.0
        best_node = None
        
        for node in self.nodes.values():
            if node.embedding:
                sim = self._cosine_similarity(node.embedding, embedding)
                if sim > best_sim:
                    best_sim, best_node = sim, node
        
        return best_node if best_sim >= self.merge_threshold else None
    
    def _link_to_context(self, node: Node, thought: dict):
        """Create edges to contextual nodes."""
        memories = thought.get("memories_used", [])
        
        for mem_id in memories:
            if mem_id in self.nodes:
                self._add_edge(mem_id, node.id, "context", 0.2)
    
    def _add_edge(self, source_id: str, target_id: str, 
                  relation: str = "assoc", weight: float = 0.1):
        """Add or strengthen edge between nodes."""
        key = (source_id, target_id)
        
        if key in self.edges:
            self.edges[key].weight = min(1.0, self.edges[key].weight + weight)
        else:
            self.edges[key] = Edge(source_id, target_id, relation, weight)
    
    def grow(self, thought: dict):
        """
        Apply growth rules based on ternary signals.
        
        Rules:
        - Novelty + Value = create/merge nodes
        - High usage = strengthen edges
        - Low usage + negative = prune
        """
        ternary = thought.get("ternary_code", [0, 0, 0, 0, 0])
        
        # Growth rule: novelty + value
        if ternary[0] == 1 and ternary[1] == 1:
            self._explore_new_connections(thought)
        
        # Pruning rule: negative growth signal
        if ternary[4] == -1:
            self._prune_weak_nodes()
    
    def _explore_new_connections(self, thought: dict):
        """Explore and create new connections based on thought."""
        # Find nodes with similar ternary signatures
        target_ternary = thought.get("ternary_code", [])
        
        for node in self.nodes.values():
            if node.ternary == target_ternary:
                # Potential connection
                pass  # Could create edges here
    
    def _prune_weak_nodes(self):
        """Remove nodes with low usage and low value."""
        to_remove = []
        
        for node_id, node in self.nodes.items():
            if node.usage < self.prune_threshold and node.value < 0.3:
                to_remove.append(node_id)
        
        for node_id in to_remove:
            del self.nodes[node_id]
            # Remove connected edges
            self.edges = {k: v for k, v in self.edges.items() 
                         if k[0] != node_id and k[1] != node_id}
    
    def get_stats(self) -> dict:
        """Get graph statistics."""
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "avg_node_value": sum(n.value for n in self.nodes.values()) / max(1, len(self.nodes)),
            "avg_edge_weight": sum(e.weight for e in self.edges.values()) / max(1, len(self.edges)),
        }
    
    def get_nodes_by_tag(self, tag: str) -> List[Node]:
        """Get all nodes with given tag."""
        return [n for n in self.nodes.values() if tag in n.tags]
    
    @staticmethod
    def _cosine_similarity(a: List[float], b: List[float]) -> float:
        """Compute cosine similarity between two vectors."""
        if not a or not b:
            return 0.0
        
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot / (norm_a * norm_b)


class GrowthRules:
    """
    Biologically-inspired growth rules for the neural substrate.
    """
    
    @staticmethod
    def should_create_node(ternary: List[int]) -> bool:
        """Create node only if novelty AND value are positive."""
        return ternary[0] == 1 and ternary[1] == 1
    
    @staticmethod
    def should_strengthen_edge(usage: int, recency: float) -> float:
        """Calculate edge strengthening amount."""
        return 0.1 * (1 + usage * 0.1) * recency
    
    @staticmethod
    def should_prune_node(node: Node) -> bool:
        """Prune if low usage AND low value."""
        return node.usage < 2 and node.value < 0.2
