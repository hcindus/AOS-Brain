#!/usr/bin/env python3
"""
CORTEX v2.0 - Sparse Temporal Ternary Cortex
Features: Temporal layers, sparse hotspots, associative links, parallel regions
"""

import numpy as np
import threading
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from collections import deque, defaultdict
from concurrent.futures import ThreadPoolExecutor
import hashlib

# Ternary encoding: 0b00=null, 0b01=neg, 0b10=pos, 0b11=unused
TERNARY_NULL = 0b00
TERNARY_NEG = 0b01
TERNARY_POS = 0b10

@dataclass
class HotspotRegion:
    """Active region in the cortex"""
    x: int
    y: int
    z: int
    size: int  # 1=single node, larger=region
    activation: int  # Ternary: -1, 0, 1 stored as encoded
    age: int = 0  # Ticks since activation
    
    def to_ternary(self) -> int:
        """Return -1, 0, or 1"""
        if self.activation == TERNARY_NEG:
            return -1
        elif self.activation == TERNARY_POS:
            return 1
        return 0

@dataclass
class TemporalFrame:
    """One tick of cortical history"""
    tick: int
    hotspots: Dict[Tuple[int,int,int], HotspotRegion]  # Sparse snapshot
    dominant_pattern: Optional[str] = None
    coherence: float = 0.0

@dataclass
class AssociativeLink:
    """Learned connection between cortical patterns"""
    source: Tuple[int,int,int]
    target: Tuple[int,int,int]
    strength: float  # 0.0 to 1.0
    last_fired: int = 0
    fire_count: int = 0

class TernarySparseCortex:
    """
    Sparse ternary cortex with temporal memory and associative links
    
    Architecture:
    - 32x32x32 nodes = 32,768 total (but sparsely active)
    - 8 parallel regions (16x16x16 each)
    - Temporal buffer: last N frames
    - Associative link network for pattern completion
    """
    
    def __init__(self, size: int = 32, temporal_depth: int = 64, max_hotspots: int = 1024):
        self.size = size  # 32 per dimension
        self.total_nodes = size * size * size
        self.temporal_depth = temporal_depth
        self.max_hotspots = max_hotspots
        
        print(f"[CortexV2] Initializing {size}³ sparse ternary cortex")
        print(f"           Total capacity: {self.total_nodes:,} nodes")
        print(f"           Temporal depth: {temporal_depth} frames")
        print(f"           Max hotspots: {max_hotspots}")
        
        # Parallel regions: 8 sub-cubes of 16x16x16
        self.region_size = size // 2
        self.regions = [
            (rx, ry, rz) 
            for rx in range(2) 
            for ry in range(2) 
            for rz in range(2)
        ]  # 8 regions: (0,0,0), (0,0,1), etc.
        
        # Sparse storage: only active nodes stored
        # Key: (x,y,z), Value: ternary encoded state
        self.active_nodes: Dict[Tuple[int,int,int], int] = {}
        self.hotspots: Dict[Tuple[int,int,int], HotspotRegion] = {}
        
        # Temporal buffer: rolling window of frames
        self.temporal_buffer: deque[TemporalFrame] = deque(maxlen=temporal_depth)
        self.current_tick = 0
        
        # Associative links: sparse graph
        # Key: source_coord, Value: list of links
        self.links: Dict[Tuple[int,int,int], List[AssociativeLink]] = defaultdict(list)
        self.link_strength_threshold = 0.3
        self.max_links_per_node = 8
        
        # Threading
        self.executor = ThreadPoolExecutor(max_workers=8)
        self._lock = threading.RLock()
        
        # Pattern hashes for link learning
        self.recent_patterns: deque[Set[Tuple[int,int,int]]] = deque(maxlen=10)
        
        print(f"[CortexV2] 8 parallel regions of {self.region_size}³ nodes each")
        print(f"[CortexV2] Ready")
    
    def _coord_to_region(self, x: int, y: int, z: int) -> int:
        """Get region index (0-7) for a coordinate"""
        rx = 0 if x < self.region_size else 1
        ry = 0 if y < self.region_size else 1
        rz = 0 if z < self.region_size else 1
        return rx * 4 + ry * 2 + rz
    
    def _region_bounds(self, region_idx: int) -> Tuple[Tuple[int,int], Tuple[int,int], Tuple[int,int]]:
        """Get (x_min, x_max), (y_min, y_max), (z_min, z_max) for region"""
        rx = region_idx // 4
        ry = (region_idx // 2) % 2
        rz = region_idx % 2
        
        x_bounds = (rx * self.region_size, (rx + 1) * self.region_size)
        y_bounds = (ry * self.region_size, (ry + 1) * self.region_size)
        z_bounds = (rz * self.region_size, (rz + 1) * self.region_size)
        
        return x_bounds, y_bounds, z_bounds
    
    def encode_ternary(self, value: int) -> int:
        """Encode -1, 0, 1 to ternary bits"""
        if value > 0:
            return TERNARY_POS
        elif value < 0:
            return TERNARY_NEG
        return TERNARY_NULL
    
    def decode_ternary(self, encoded: int) -> int:
        """Decode ternary bits to -1, 0, 1"""
        if encoded == TERNARY_POS:
            return 1
        elif encoded == TERNARY_NEG:
            return -1
        return 0
    
    def activate_sparse(self, activations: List[Tuple[int,int,int,int]], source: str = "external"):
        """
        Activate specific nodes with ternary values
        
        Args:
            activations: List of (x, y, z, value) where value is -1, 0, or 1
            source: Source of activation (for tracking)
        """
        with self._lock:
            new_nodes = set()
            
            for x, y, z, value in activations:
                if not (0 <= x < self.size and 0 <= y < self.size and 0 <= z < self.size):
                    continue
                
                if value == 0:
                    # Deactivate
                    self.active_nodes.pop((x,y,z), None)
                    self.hotspots.pop((x,y,z), None)
                else:
                    # Activate
                    encoded = self.encode_ternary(value)
                    self.active_nodes[(x,y,z)] = encoded
                    new_nodes.add((x,y,z))
                    
                    # Create/update hotspot
                    self.hotspots[(x,y,z)] = HotspotRegion(
                        x=x, y=y, z=z,
                        size=1,
                        activation=encoded,
                        age=0
                    )
            
            # Age existing hotspots
            for coord, hotspot in list(self.hotspots.items()):
                if coord not in new_nodes:
                    hotspot.age += 1
                    # Decay old hotspots
                    if hotspot.age > 100:
                        self.hotspots.pop(coord, None)
                        self.active_nodes.pop(coord, None)
            
            # Prune to max_hotspots (keep newest/most active)
            if len(self.hotspots) > self.max_hotspots:
                sorted_hotspots = sorted(
                    self.hotspots.items(),
                    key=lambda x: (-x[1].activation, x[1].age)
                )
                to_remove = sorted_hotspots[self.max_hotspots:]
                for coord, _ in to_remove:
                    self.hotspots.pop(coord, None)
                    self.active_nodes.pop(coord, None)
    
    def embed_to_hotspots(self, embedding: np.ndarray, n_hotspots: int = 64) -> List[Tuple[int,int,int,int]]:
        """
        Convert a dense embedding vector to sparse ternary hotspots
        
        Strategy: Hash-based mapping to ensure determinism
        """
        # Normalize embedding
        emb = embedding.flatten()[:256]  # Use first 256 dims
        emb = (emb - emb.mean()) / (emb.std() + 1e-8)
        
        # Quantize to ternary
        ternary = np.where(emb > 0.5, 1, np.where(emb < -0.5, -1, 0))
        
        activations = []
        for i, val in enumerate(ternary):
            if val != 0:
                # Deterministic hash to coordinates
                hash_input = f"{i}_{val}_{emb[i]:.4f}"
                hash_val = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
                
                x = hash_val % self.size
                y = (hash_val // self.size) % self.size
                z = (hash_val // (self.size * self.size)) % self.size
                
                activations.append((x, y, z, int(val)))
        
        # Keep top by magnitude
        activations.sort(key=lambda a: abs(embedding.flatten()[a[0] % len(emb)]), reverse=True)
        return activations[:n_hotspots]
    
    def propagate_associative(self, max_propagations: int = 100) -> Dict[Tuple[int,int,int], int]:
        """
        Fire associative links: when a pattern activates, prime connected patterns
        
        Returns: New activations from link firing
        """
        with self._lock:
            new_activations: Dict[Tuple[int,int,int], int] = {}
            fired_count = 0
            
            # Get currently active nodes (positive activation)
            active_pos = {coord for coord, enc in self.active_nodes.items() 
                         if enc == TERNARY_POS}
            
            for coord in active_pos:
                for link in self.links.get(coord, []):
                    if fired_count >= max_propagations:
                        break
                    
                    # Check if target is not already strongly active
                    target_enc = self.active_nodes.get(link.target, TERNARY_NULL)
                    if target_enc == TERNARY_NULL or self.decode_ternary(target_enc) < 1:
                        # Prime the target (weakened activation)
                        prime_val = 1 if link.strength > 0.7 else 0
                        if prime_val > 0:
                            new_activations[link.target] = prime_val
                            link.last_fired = self.current_tick
                            link.fire_count += 1
                            fired_count += 1
            
            return new_activations
    
    def learn_associations(self, pattern: Set[Tuple[int,int,int]], learning_rate: float = 0.1):
        """
        Learn associations from a co-occurring pattern
        
        Hebbian-style: nodes that fire together wire together
        """
        with self._lock:
            pattern_list = list(pattern)
            
            # Create links between co-occurring nodes
            for i, source in enumerate(pattern_list[:20]):  # Limit per pattern
                for target in pattern_list[i+1:min(i+5, len(pattern_list))]:
                    # Check if link exists
                    existing = [l for l in self.links[source] if l.target == target]
                    
                    if existing:
                        # Strengthen
                        existing[0].strength = min(1.0, existing[0].strength + learning_rate)
                    elif len(self.links[source]) < self.max_links_per_node:
                        # Create new link
                        self.links[source].append(AssociativeLink(
                            source=source,
                            target=target,
                            strength=learning_rate,
                            last_fired=self.current_tick
                        ))
    
    def _process_region_parallel(self, region_idx: int, task: str) -> Dict:
        """Process a single region in parallel (called by thread pool)"""
        x_bounds, y_bounds, z_bounds = self._region_bounds(region_idx)
        
        # Get nodes in this region
        region_nodes = {
            coord: enc for coord, enc in self.active_nodes.items()
            if x_bounds[0] <= coord[0] < x_bounds[1]
            and y_bounds[0] <= coord[1] < y_bounds[1]
            and z_bounds[0] <= coord[2] < z_bounds[1]
        }
        
        if task == "local_propagation":
            # Local diffusion within region
            new_activations = {}
            for (x,y,z), enc in region_nodes.items():
                val = self.decode_ternary(enc)
                if val != 0:
                    # Diffuse to neighbors
                    for dx, dy, dz in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
                        nx, ny, nz = x+dx, y+dy, z+dz
                        if x_bounds[0] <= nx < x_bounds[1] and y_bounds[0] <= ny < y_bounds[1] and z_bounds[0] <= nz < z_bounds[1]:
                            neighbor_coord = (nx, ny, nz)
                            if neighbor_coord not in self.active_nodes:
                                new_activations[neighbor_coord] = val * 0.5  # Weakened
            return {"region": region_idx, "new_activations": new_activations}
        
        elif task == "pattern_summary":
            # Summarize patterns in this region
            pos_count = sum(1 for enc in region_nodes.values() if enc == TERNARY_POS)
            neg_count = sum(1 for enc in region_nodes.values() if enc == TERNARY_NEG)
            return {
                "region": region_idx,
                "active_count": len(region_nodes),
                "positive": pos_count,
                "negative": neg_count
            }
        
        return {"region": region_idx, "error": "unknown_task"}
    
    def tick_parallel(self, use_links: bool = True, use_temporal: bool = True) -> Dict:
        """
        Execute one tick with parallel region processing
        
        Returns: Summary of tick activity
        """
        self.current_tick += 1
        
        # Step 1: Parallel region processing (local propagation)
        futures = [
            self.executor.submit(self._process_region_parallel, ri, "local_propagation")
            for ri in range(8)
        ]
        
        region_results = [f.result() for f in futures]
        
        # Collect new activations from regions
        with self._lock:
            for result in region_results:
                for coord, val in result.get("new_activations", {}).items():
                    if val >= 0.5 and coord not in self.active_nodes:
                        self.active_nodes[coord] = TERNARY_POS
        
        # Step 2: Associative link propagation
        link_activations = {}
        if use_links:
            link_activations = self.propagate_associative(max_propagations=200)
            with self._lock:
                for coord, val in link_activations.items():
                    if val > 0:
                        self.active_nodes[coord] = TERNARY_POS
        
        # Step 3: Learn from current pattern
        if use_temporal and self.current_tick % 10 == 0:
            current_pattern = set(self.active_nodes.keys())
            if len(current_pattern) > 5:
                self.learn_associations(current_pattern)
                self.recent_patterns.append(current_pattern)
        
        # Step 4: Store temporal frame
        if use_temporal:
            frame = TemporalFrame(
                tick=self.current_tick,
                hotspots=dict(self.hotspots),
                dominant_pattern=self._extract_dominant_pattern(),
                coherence=self._calculate_coherence()
            )
            self.temporal_buffer.append(frame)
        
        return {
            "tick": self.current_tick,
            "active_nodes": len(self.active_nodes),
            "hotspots": len(self.hotspots),
            "link_activations": len(link_activations),
            "associative_links": sum(len(links) for links in self.links.values()),
            "temporal_frames": len(self.temporal_buffer)
        }
    
    def _extract_dominant_pattern(self) -> Optional[str]:
        """Extract a hashable pattern signature from current state"""
        if not self.hotspots:
            return None
        
        # Get top 10 hotspots by activation
        top = sorted(self.hotspots.values(), 
                     key=lambda h: (-h.activation, h.age))[:10]
        
        pattern_str = "|".join(f"{h.x},{h.y},{h.z}" for h in top)
        return hashlib.md5(pattern_str.encode()).hexdigest()[:16]
    
    def _calculate_coherence(self) -> float:
        """Calculate coherence: how synchronized are active regions"""
        if len(self.hotspots) < 2:
            return 0.0
        
        # Simple coherence: ratio of hotspots to max
        return min(1.0, len(self.hotspots) / 100.0)
    
    def query_temporal(self, pattern_hash: Optional[str] = None, 
                       ticks_back: int = 10) -> List[TemporalFrame]:
        """
        Query temporal memory for similar patterns or recent history
        
        Args:
            pattern_hash: Optional pattern to search for
            ticks_back: How many frames to return
        
        Returns:
            List of matching temporal frames
        """
        frames = list(self.temporal_buffer)[-ticks_back:]
        
        if pattern_hash:
            frames = [f for f in frames if f.dominant_pattern == pattern_hash]
        
        return frames
    
    def chain_of_thought(self, initial_pattern: List[Tuple[int,int,int]], 
                         steps: int = 3) -> List[Dict]:
        """
        Traverse temporal buffer for chain-of-thought reasoning
        
        Returns trace of how patterns evolved
        """
        thought_chain = []
        current_pattern = set(initial_pattern)
        
        for step in range(steps):
            # Find frames with similar patterns
            pattern_hash = self._pattern_to_hash(current_pattern)
            similar_frames = self.query_temporal(pattern_hash, ticks_back=self.temporal_depth)
            
            if similar_frames:
                # Extract what happened next
                frame = similar_frames[-1]  # Most recent match
                thought_chain.append({
                    "step": step,
                    "pattern_hash": frame.dominant_pattern,
                    "coherence": frame.coherence,
                    "hotspot_count": len(frame.hotspots)
                })
                
                # Evolve pattern for next step
                current_pattern = set(frame.hotspots.keys())
            else:
                break
        
        return thought_chain
    
    def _pattern_to_hash(self, pattern: Set[Tuple[int,int,int]]) -> str:
        """Convert pattern set to hash string"""
        pattern_str = "|".join(f"{x},{y},{z}" for x,y,z in sorted(pattern)[:10])
        return hashlib.md5(pattern_str.encode()).hexdigest()[:16]
    
    def get_state_for_prompt(self) -> str:
        """
        Generate a compact representation for LLM system prompt
        
        This is the key bridge: cortex state -> LLM context
        """
        lines = ["[CORTEX_STATE]"]
        
        # Active regions summary
        region_activity = defaultdict(int)
        for (x,y,z), enc in self.active_nodes.items():
            region_idx = self._coord_to_region(x,y,z)
            val = self.decode_ternary(enc)
            region_activity[region_idx] += val
        
        lines.append(f"Active regions: {dict(region_activity)}")
        lines.append(f"Coherence: {self._calculate_coherence():.2f}")
        lines.append(f"Temporal depth: {len(self.temporal_buffer)}/{self.temporal_depth}")
        
        # Dominant pattern
        dom = self._extract_dominant_pattern()
        if dom:
            lines.append(f"Current pattern: {dom[:8]}...")
        
        # Recent temporal trends
        if len(self.temporal_buffer) >= 3:
            recent = list(self.temporal_buffer)[-3:]
            coherence_trend = [f.coherence for f in recent]
            lines.append(f"Coherence trend: {[f'{c:.2f}' for c in coherence_trend]}")
        
        return "\n".join(lines)
    
    def get_stats(self) -> Dict:
        """Get cortex statistics"""
        return {
            "active_nodes": len(self.active_nodes),
            "hotspots": len(self.hotspots),
            "links": sum(len(l) for l in self.links.values()),
            "temporal_frames": len(self.temporal_buffer),
            "current_tick": self.current_tick,
            "coherence": self._calculate_coherence(),
            "sparsity": len(self.active_nodes) / self.total_nodes
        }


if __name__ == "__main__":
    print("=" * 70)
    print("  CORTEX v2.0 - SPARSE TERNARY TEST")
    print("=" * 70)
    
    cortex = TernarySparseCortex(size=32, temporal_depth=64)
    
    # Test 1: Sparse activation from embedding
    print("\n[Test 1] Embedding to hotspots")
    test_emb = np.random.randn(256)
    test_emb[50:70] = 2.0  # Create some strong positives
    test_emb[100:120] = -2.0  # Some negatives
    
    hotspots = cortex.embed_to_hotspots(test_emb, n_hotspots=64)
    print(f"  Generated {len(hotspots)} hotspots from embedding")
    
    cortex.activate_sparse(hotspots)
    print(f"  Active nodes: {len(cortex.active_nodes)}")
    
    # Test 2: Parallel tick with links
    print("\n[Test 2] Parallel ticks with associative learning")
    for i in range(20):
        result = cortex.tick_parallel(use_links=True, use_temporal=True)
        if i % 5 == 0:
            print(f"  Tick {i}: {result['active_nodes']} nodes, {result['associative_links']} links")
    
    # Test 3: Temporal query
    print("\n[Test 3] Temporal memory query")
    frames = cortex.query_temporal(ticks_back=5)
    print(f"  Last 5 frames: {[f.coherence for f in frames]}")
    
    # Test 4: Chain of thought
    print("\n[Test 4] Chain of thought traversal")
    initial = list(cortex.hotspots.keys())[:5]
    chain = cortex.chain_of_thought(initial, steps=3)
    for step in chain:
        print(f"  Step {step['step']}: coherence={step['coherence']:.2f}, hotspots={step['hotspot_count']}")
    
    # Test 5: State for prompt
    print("\n[Test 5] LLM prompt state")
    prompt_state = cortex.get_state_for_prompt()
    print(prompt_state)
    
    print("\n" + "=" * 70)
    print("  Stats:", cortex.get_stats())
    print("=" * 70)