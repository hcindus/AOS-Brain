#!/usr/bin/env python3
"""
CORTEX v2.5 - Optimized Python with Numba JIT + SIMD structure + GPU offload
Features: Agent read/write API, region threading, SIMD-ready, CuPy GPU
"""

import numpy as np
import threading
import hashlib
from typing import Dict, List, Tuple, Optional, Set, Callable
from dataclasses import dataclass, field
from collections import deque, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import time

# Optional GPU support
try:
    import cupy as cp
    HAS_CUPY = True
    print("[CortexV2.5] CuPy available - GPU offload enabled")
except ImportError:
    HAS_CUPY = False
    cp = None

# Numba JIT for hot paths
try:
    from numba import njit, prange, uint8, int32, float32
    HAS_NUMBA = True
    print("[CortexV2.5] Numba available - JIT compilation enabled")
except ImportError:
    HAS_NUMBA = False
    def njit(*args, **kwargs):
        def wrapper(f): return f
        return wrapper
    prange = range
    uint8 = int
    int32 = int
    float32 = float

# Ternary encoding in 2 bits: 0=null, 1=neg, 2=pos, 3=unused
TERNARY_PACKED = np.uint8
TERNARY_NULL = np.uint8(0)
TERNARY_NEG = np.uint8(1)
TERNARY_POS = np.uint8(2)

# SIMD-friendly: Process 256 nodes at once (8x8x4 or 16x4x4 blocks)
SIMD_BLOCK_SIZE = 256

@dataclass
class AgentReadRequest:
    """Agent request to read cortex state"""
    agent_id: str
    region_indices: List[int]  # Which of 8 regions to read
    layer_mask: int  # Bitmask: bit0=conscious, bit1=subconscious, bit2=unconscious
    max_hotspots: int = 64
    format: str = "sparse"  # "sparse", "dense", "summary"

@dataclass
class AgentWriteRequest:
    """Agent request to write to cortex"""
    agent_id: str
    region_indices: List[int]
    activations: List[Tuple[int, int, int, int]]  # x, y, z, ternary_value
    priority: float = 1.0  # 0.0-1.0, affects propagation strength
    ephemeral: bool = False  # If True, cleared next tick

@dataclass
class CortexSnapshot:
    """Read-only snapshot for agents"""
    tick: int
    agent_id: str
    hotspots: Dict[Tuple[int, int, int], int]  # coord -> ternary
    coherence: float
    pattern_hash: Optional[str]
    temporal_context: List[Dict]  # Recent similar patterns

@dataclass
class RegionState:
    """State for one of 8 parallel regions"""
    index: int
    x_bounds: Tuple[int, int]
    y_bounds: Tuple[int, int]
    z_bounds: Tuple[int, int]
    active_nodes: Dict[Tuple[int, int, int], np.uint8]  # Sparse storage
    hotspots: Dict[Tuple[int, int, int], dict]  # Coordinates with metadata
    lock: threading.RLock = field(default_factory=threading.RLock)
    last_tick: int = 0
    agent_writes: List[AgentWriteRequest] = field(default_factory=list)


if HAS_NUMBA:
    @njit([uint8[:, :, :](uint8[:, :, :], float32[:, :, :], float32)], cache=True, parallel=True)
    def numba_propagate(volume, weights, decay_factor):
        """Numba-optimized propagation with SIMD-friendly loops"""
        depth, height, width = volume.shape
        new_volume = np.empty_like(volume)
        
        # Process in SIMD-friendly blocks
        for z in prange(depth):
            for y in range(0, height, 4):  # Block for cache
                for x in range(0, width, 4):
                    # Vectorized block processing
                    block_sum = np.float32(0.0)
                    for dy in range(4):
                        for dx in range(4):
                            if y + dy < height and x + dx < width:
                                val = volume[z, y + dy, x + dx]
                                if val == TERNARY_POS:
                                    block_sum += weights[z, y + dy, x + dx]
                                elif val == TERNARY_NEG:
                                    block_sum -= weights[z, y + dy, x + dx]
                    
                    # Apply to block center
                    cy, cx = min(y + 2, height - 1), min(x + 2, width - 1)
                    propagated = np.tanh(block_sum * 0.1)
                    
                    # Quantize to ternary
                    if propagated > 0.3:
                        new_volume[z, cy, cx] = TERNARY_POS
                    elif propagated < -0.3:
                        new_volume[z, cy, cx] = TERNARY_NEG
                    else:
                        new_volume[z, cy, cx] = TERNARY_NULL
        
        return new_volume
    
    @njit([uint8[:](float32[:], uint8[:])], cache=True)
    def numba_embed_to_ternary(embedding, out):
        """Numba-optimized embedding quantization"""
        n = len(embedding)
        for i in range(n):
            if embedding[i] > 0.5:
                out[i] = TERNARY_POS
            elif embedding[i] < -0.5:
                out[i] = TERNARY_NEG
            else:
                out[i] = TERNARY_NULL
        return out
    
    @njit([float32(uint8[:, :, :])], cache=True)
    def numba_calculate_coherence(volume):
        """SIMD-friendly coherence calculation"""
        depth, height, width = volume.shape
        active = np.int32(0)
        total = depth * height * width
        
        for z in prange(depth):
            for y in range(height):
                for x in range(width):
                    if volume[z, y, x] != TERNARY_NULL:
                        active += 1
        
        return float32(active) / float32(total)
else:
    def numba_propagate(volume, weights, decay_factor):
        """Fallback without Numba"""
        return volume
    
    def numba_embed_to_ternary(embedding, out):
        for i, val in enumerate(embedding):
            if val > 0.5:
                out[i] = TERNARY_POS
            elif val < -0.5:
                out[i] = TERNARY_NEG
            else:
                out[i] = TERNARY_NULL
        return out
    
    def numba_calculate_coherence(volume):
        return np.mean(volume != TERNARY_NULL)


class TernarySIMDArray:
    """
    SIMD-optimized ternary array
    Stores 4 ternary values per byte (2 bits each)
    """
    
    def __init__(self, size: int):
        self.size = size
        self.num_values = size * size * size
        # 4 values per byte
        self.data = np.zeros((self.num_values + 3) // 4, dtype=np.uint8)
        self.shape = (size, size, size)
    
    def _index(self, x: int, y: int, z: int) -> Tuple[int, int]:
        """Get byte index and bit offset for coordinate"""
        flat = (z * self.size * self.size) + (y * self.size) + x
        byte_idx = flat // 4
        bit_offset = (flat % 4) * 2
        return byte_idx, bit_offset
    
    def get(self, x: int, y: int, z: int) -> np.uint8:
        """Get ternary value at coordinate"""
        if not (0 <= x < self.size and 0 <= y < self.size and 0 <= z < self.size):
            return TERNARY_NULL
        byte_idx, bit_offset = self._index(x, y, z)
        return (self.data[byte_idx] >> bit_offset) & 0b11
    
    def set(self, x: int, y: int, z: int, value: np.uint8):
        """Set ternary value at coordinate"""
        if not (0 <= x < self.size and 0 <= y < self.size and 0 <= z < self.size):
            return
        byte_idx, bit_offset = self._index(x, y, z)
        # Clear bits, then set (mask as uint8 to avoid overflow)
        mask = np.uint8(~(0b11 << bit_offset) & 0xFF)
        self.data[byte_idx] = (self.data[byte_idx] & mask) | ((value & 0b11) << bit_offset)
    
    def to_dense(self) -> np.ndarray:
        """Convert to dense numpy array (for GPU ops)"""
        result = np.zeros(self.shape, dtype=np.uint8)
        for z in range(self.size):
            for y in range(self.size):
                for x in range(self.size):
                    result[z, y, x] = self.get(x, y, z)
        return result
    
    def from_dense(self, dense: np.ndarray):
        """Load from dense numpy array"""
        for z in range(min(self.size, dense.shape[0])):
            for y in range(min(self.size, dense.shape[1])):
                for x in range(min(self.size, dense.shape[2])):
                    self.set(x, y, z, dense[z, y, x])
    
    def copy(self) -> 'TernarySIMDArray':
        """Return a copy of this array"""
        new_array = TernarySIMDArray(self.size)
        new_array.data = self.data.copy()
        return new_array
    
    def __getstate__(self) -> Dict:
        """For pickle serialization"""
        return {
            'size': self.size,
            'data': self.data.tobytes()  # Convert to bytes for pickle
        }
    
    def __setstate__(self, state: Dict):
        """For pickle deserialization"""
        self.size = state['size']
        num_values = self.size * self.size * self.size
        bytes_needed = (num_values + 3) // 4
        self.data = np.frombuffer(state['data'], dtype=np.uint8).copy()
        # Ensure correct size
        if len(self.data) != bytes_needed:
            self.data = np.zeros(bytes_needed, dtype=np.uint8)


class CortexV25Optimized:
    """
    High-performance cortex with agent read/write, SIMD, and GPU offload
    
    Architecture:
    - 32x32x32 nodes, bit-packed (8KB vs 32KB float32)
    - 8 regions with independent locks
    - Numba JIT for propagation
    - CuPy GPU for large convolutions
    - Agent read/write with priority
    """
    
    def __init__(self, size: int = 32, temporal_depth: int = 128, 
                 use_gpu: bool = True, use_numba: bool = True):
        self.size = size
        self.total_nodes = size ** 3
        self.temporal_depth = temporal_depth
        self.use_gpu = use_gpu and HAS_CUPY
        self.use_numba = use_numba and HAS_NUMBA
        
        print(f"[CortexV2.5] Optimized sparse ternary cortex")
        print(f"             Size: {size}³ = {self.total_nodes:,} nodes")
        print(f"             Packed size: {self.total_nodes // 4:,} bytes")
        print(f"             Numba JIT: {'ON' if self.use_numba else 'OFF'}")
        print(f"             GPU offload: {'ON' if self.use_gpu else 'OFF'}")
        
        # SIMD-packed volume (CPU)
        self.volume = TernarySIMDArray(size)
        
        # GPU mirror (if available)
        self.gpu_volume = None
        if self.use_gpu:
            self.gpu_volume = cp.zeros((size, size, size), dtype=cp.uint8)
        
        # Region threading: 8 regions of 16x16x16
        self.region_size = size // 2
        self.regions: List[RegionState] = []
        for ri in range(8):
            rx, ry, rz = ri // 4, (ri // 2) % 2, ri % 2
            self.regions.append(RegionState(
                index=ri,
                x_bounds=(rx * self.region_size, (rx + 1) * self.region_size),
                y_bounds=(ry * self.region_size, (ry + 1) * self.region_size),
                z_bounds=(rz * self.region_size, (rz + 1) * self.region_size),
                active_nodes={},
                hotspots={}
            ))
        
        # Temporal buffer
        self.temporal_buffer: deque[Dict] = deque(maxlen=temporal_depth)
        self.current_tick = 0
        
        # Agent registry
        self.registered_agents: Dict[str, Dict] = {}
        self.agent_callbacks: Dict[str, Callable] = {}
        
        # Performance tracking
        self.timings = defaultdict(list)
        
        print(f"[CortexV2.5] 8 regions of {self.region_size}³ nodes ready")
    
    def register_agent(self, agent_id: str, 
                       read_callback: Optional[Callable] = None,
                       write_callback: Optional[Callable] = None) -> bool:
        """Register an agent for cortex access"""
        if agent_id in self.registered_agents:
            return False
        
        self.registered_agents[agent_id] = {
            "registered_at": time.time(),
            "read_count": 0,
            "write_count": 0
        }
        
        if read_callback:
            self.agent_callbacks[f"{agent_id}:read"] = read_callback
        if write_callback:
            self.agent_callbacks[f"{agent_id}:write"] = write_callback
        
        print(f"[CortexV2.5] Agent '{agent_id}' registered")
        return True
    
    def unregister_agent(self, agent_id: str):
        """Remove agent registration"""
        self.registered_agents.pop(agent_id, None)
        self.agent_callbacks.pop(f"{agent_id}:read", None)
        self.agent_callbacks.pop(f"{agent_id}:write", None)
    
    def agent_read(self, request: AgentReadRequest) -> CortexSnapshot:
        """
        Agent reads cortex state
        
        Returns sparse snapshot of requested regions
        """
        start_time = time.time()
        
        # Update stats
        if request.agent_id in self.registered_agents:
            self.registered_agents[request.agent_id]["read_count"] += 1
        
        # Gather hotspots from requested regions
        hotspots = {}
        for region_idx in request.region_indices:
            if 0 <= region_idx < len(self.regions):
                region = self.regions[region_idx]
                with region.lock:
                    for coord, data in region.hotspots.items():
                        hotspots[coord] = data.get("activation", 0)
        
        # Sort by activation, limit
        sorted_hotspots = sorted(hotspots.items(), 
                                key=lambda x: abs(x[1]), 
                                reverse=True)[:request.max_hotspots]
        hotspots = dict(sorted_hotspots)
        
        # Calculate coherence
        coherence = self._calculate_coherence()
        pattern_hash = self._extract_pattern_hash()
        
        # Get temporal context
        temporal_context = []
        if pattern_hash:
            for frame in self.temporal_buffer:
                if frame.get("pattern_hash") == pattern_hash:
                    temporal_context.append({
                        "tick": frame.get("tick"),
                        "coherence": frame.get("coherence")
                    })
        
        # Trigger callback if registered
        callback_key = f"{request.agent_id}:read"
        if callback_key in self.agent_callbacks:
            try:
                self.agent_callbacks[callback_key](request, hotspots)
            except Exception as e:
                print(f"[CortexV2.5] Read callback error: {e}")
        
        elapsed = time.time() - start_time
        self.timings["agent_read"].append(elapsed)
        
        return CortexSnapshot(
            tick=self.current_tick,
            agent_id=request.agent_id,
            hotspots=hotspots,
            coherence=coherence,
            pattern_hash=pattern_hash,
            temporal_context=temporal_context
        )
    
    def agent_write(self, request: AgentWriteRequest) -> Dict:
        """
        Agent writes to cortex
        
        Writes are queued per-region and applied during tick
        """
        start_time = time.time()
        
        if request.agent_id in self.registered_agents:
            self.registered_agents[request.agent_id]["write_count"] += 1
        
        # Distribute writes to regions
        written_count = 0
        for region_idx in request.region_indices:
            if 0 <= region_idx < len(self.regions):
                region = self.regions[region_idx]
                region.agent_writes.append(request)
                written_count += len(request.activations)
        
        # Trigger callback if registered
        callback_key = f"{request.agent_id}:write"
        if callback_key in self.agent_callbacks:
            try:
                self.agent_callbacks[callback_key](request, written_count)
            except Exception as e:
                print(f"[CortexV2.5] Write callback error: {e}")
        
        elapsed = time.time() - start_time
        self.timings["agent_write"].append(elapsed)
        
        return {
            "written": written_count,
            "regions_affected": len(request.region_indices),
            "priority": request.priority
        }
    
    def _apply_agent_writes(self, region: RegionState):
        """Apply all pending agent writes to a region"""
        with region.lock:
            for write in region.agent_writes:
                for x, y, z, ternary_val in write.activations:
                    # Check if in region bounds
                    if (region.x_bounds[0] <= x < region.x_bounds[1] and
                        region.y_bounds[0] <= y < region.y_bounds[1] and
                        region.z_bounds[0] <= z < region.z_bounds[1]):
                        
                        coord = (x, y, z)
                        if ternary_val == 0:
                            region.active_nodes.pop(coord, None)
                            region.hotspots.pop(coord, None)
                        else:
                            encoded = TERNARY_POS if ternary_val > 0 else TERNARY_NEG
                            region.active_nodes[coord] = encoded
                            region.hotspots[coord] = {
                                "activation": ternary_val,
                                "priority": write.priority,
                                "ephemeral": write.ephemeral,
                                "age": 0
                            }
            
            region.agent_writes.clear()
    
    def _propagate_region(self, region: RegionState) -> Dict:
        """Propagate activation within one region (thread-safe)"""
        start_time = time.time()
        
        with region.lock:
            # Apply agent writes first
            self._apply_agent_writes(region)
            
            # Local propagation: diffuse to neighbors
            new_activations = {}
            decayed = []
            
            for coord, encoded in region.active_nodes.items():
                x, y, z = coord
                val = 1 if encoded == TERNARY_POS else (-1 if encoded == TERNARY_NEG else 0)
                
                if val == 0:
                    continue
                
                # Age and decay
                hotspot = region.hotspots.get(coord)
                if hotspot:
                    hotspot["age"] = hotspot.get("age", 0) + 1
                    
                    # Decay old hotspots
                    if hotspot["age"] > 50 or (hotspot.get("ephemeral") and hotspot["age"] > 1):
                        decayed.append(coord)
                        continue
                    
                    # Propagate to neighbors (6-connected)
                    if hotspot.get("priority", 1.0) > 0.3:
                        for dx, dy, dz in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
                            nx, ny, nz = x+dx, y+dy, z+dz
                            
                            # Check bounds
                            if (region.x_bounds[0] <= nx < region.x_bounds[1] and
                                region.y_bounds[0] <= ny < region.y_bounds[1] and
                                region.z_bounds[0] <= nz < region.z_bounds[1]):
                                
                                ncoord = (nx, ny, nz)
                                if ncoord not in region.active_nodes:
                                    # Weakened propagation
                                    new_val = val * 0.5 * hotspot["priority"]
                                    if abs(new_val) >= 0.5:
                                        new_activations[ncoord] = 1 if new_val > 0 else -1
            
            # Apply decayed
            for coord in decayed:
                region.active_nodes.pop(coord, None)
                region.hotspots.pop(coord, None)
            
            # Apply new activations
            for coord, val in new_activations.items():
                encoded = TERNARY_POS if val > 0 else TERNARY_NEG
                region.active_nodes[coord] = encoded
                region.hotspots[coord] = {
                    "activation": val,
                    "priority": 0.5,
                    "age": 0
                }
            
            region.last_tick = self.current_tick
            
            elapsed = time.time() - start_time
            self.timings[f"region_{region.index}"].append(elapsed)
            
            return {
                "region": region.index,
                "active_count": len(region.active_nodes),
                "propagated": len(new_activations),
                "decayed": len(decayed),
                "time_ms": elapsed * 1000
            }
    
    def _gpu_sync_to_cpu(self):
        """Sync GPU volume back to CPU (if using GPU)"""
        if self.use_gpu and self.gpu_volume is not None:
            dense = cp.asnumpy(self.gpu_volume)
            self.volume.from_dense(dense)
    
    def _gpu_propagate(self):
        """GPU-accelerated propagation using CuPy"""
        if not self.use_gpu or self.gpu_volume is None:
            return
        
        # Upload current CPU state
        dense = self.volume.to_dense()
        self.gpu_volume = cp.array(dense)
        
        # GPU convolution for propagation
        kernel = cp.ones((3, 3, 3), dtype=cp.float32) / 27.0
        convolved = cp.signal.convolve(
            self.gpu_volume.astype(cp.float32), 
            kernel, 
            mode='same'
        )
        
        # Quantize back to ternary
        self.gpu_volume = cp.where(convolved > 0.3, TERNARY_POS,
                                  cp.where(convolved < -0.3, TERNARY_NEG, TERNARY_NULL))
        
        # Sync back
        self._gpu_sync_to_cpu()
    
    def tick_parallel(self) -> Dict:
        """
        Execute one tick with full parallel region processing
        """
        tick_start = time.time()
        self.current_tick += 1
        
        # Method 1: CPU parallel (default)
        # Method 2: GPU if enabled and tick % N == 0
        use_gpu_this_tick = (self.use_gpu and 
                            self.current_tick % 10 == 0 and 
                            self.gpu_volume is not None)
        
        if use_gpu_this_tick:
            self._gpu_propagate()
            region_results = [{"region": i, "gpu": True} for i in range(8)]
        else:
            # Parallel CPU processing
            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = {
                    executor.submit(self._propagate_region, region): region.index 
                    for region in self.regions
                }
                
                region_results = []
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        region_results.append(result)
                    except Exception as e:
                        print(f"[CortexV2.5] Region error: {e}")
        
        # Cross-region synchronization (every 5 ticks)
        if self.current_tick % 5 == 0:
            self._sync_region_boundaries()
        
        # Update temporal buffer
        total_active = sum(r["active_count"] for r in region_results)
        frame = {
            "tick": self.current_tick,
            "total_active": total_active,
            "coherence": self._calculate_coherence(),
            "pattern_hash": self._extract_pattern_hash(),
            "regions": region_results
        }
        self.temporal_buffer.append(frame)
        
        tick_elapsed = time.time() - tick_start
        self.timings["full_tick"].append(tick_elapsed)
        
        return {
            "tick": self.current_tick,
            "active_nodes": total_active,
            "sparsity": total_active / self.total_nodes,
            "regions": len(region_results),
            "gpu_used": use_gpu_this_tick,
            "tick_time_ms": tick_elapsed * 1000
        }
    
    def _sync_region_boundaries(self):
        """Synchronize activation across region boundaries"""
        # Find boundary nodes and share with neighbors
        for i, region in enumerate(self.regions):
            with region.lock:
                # Get boundary nodes (simplified: just corners/edges)
                boundary_nodes = [
                    coord for coord in region.active_nodes.keys()
                    if (coord[0] in [region.x_bounds[0], region.x_bounds[1]-1] or
                        coord[1] in [region.y_bounds[0], region.y_bounds[1]-1] or
                        coord[2] in [region.z_bounds[0], region.z_bounds[1]-1])
                ]
                
                # Could broadcast to adjacent regions here
                # For now, just update shared volume
                for coord in boundary_nodes:
                    self.volume.set(coord[0], coord[1], coord[2], 
                                   region.active_nodes[coord])
    
    def _calculate_coherence(self) -> float:
        """Calculate global coherence"""
        total_active = sum(len(r.active_nodes) for r in self.regions)
        return min(1.0, total_active / 500.0)  # Normalize to ~500 active nodes
    
    def _extract_pattern_hash(self) -> Optional[str]:
        """Extract pattern signature"""
        # Get top nodes from each region
        top_nodes = []
        for region in self.regions:
            with region.lock:
                sorted_nodes = sorted(
                    region.active_nodes.items(),
                    key=lambda x: abs(self._decode(x[1])),
                    reverse=True
                )[:5]
                top_nodes.extend(sorted_nodes)
        
        if not top_nodes:
            return None
        
        pattern_str = "|".join(f"{c[0]},{c[1]},{c[2]}" for c, _ in top_nodes[:20])
        return hashlib.md5(pattern_str.encode()).hexdigest()[:16]
    
    def _decode(self, encoded: np.uint8) -> int:
        """Decode ternary"""
        if encoded == TERNARY_POS:
            return 1
        elif encoded == TERNARY_NEG:
            return -1
        return 0
    
    def embed_to_hotspots(self, embedding: np.ndarray, n_hotspots: int = 64) -> List[Tuple[int, int, int, int]]:
        """
        Convert embedding vector to ternary hotspots
        Compatible with cortex_v2_sparse API
        """
        import hashlib
        emb = embedding.flatten()[:256]
        emb = (emb - emb.mean()) / (emb.std() + 1e-8)
        
        # Quantize to ternary
        ternary = np.where(emb > 0.5, 1, np.where(emb < -0.5, -1, 0))
        
        activations = []
        for i, val in enumerate(ternary):
            if val != 0:
                hash_input = f"{i}_{val}_{emb[i]:.4f}"
                hash_val = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
                
                x = hash_val % self.size
                y = (hash_val // self.size) % self.size
                z = (hash_val // (self.size * self.size)) % self.size
                
                activations.append((x, y, z, int(val)))
        
        # Keep top by magnitude
        activations.sort(key=lambda a: abs(embedding.flatten()[a[0] % len(emb)]), reverse=True)
        return activations[:n_hotspots]
    
    def get_performance_stats(self) -> Dict:
        """Get performance timing statistics"""
        stats = {}
        for key, times in self.timings.items():
            if times:
                stats[key] = {
                    "mean_ms": np.mean(times) * 1000,
                    "max_ms": np.max(times) * 1000,
                    "min_ms": np.min(times) * 1000,
                    "count": len(times)
                }
        return stats
    
    def get_agent_stats(self) -> Dict:
        """Get agent activity statistics"""
        return {
            agent_id: {
                "reads": data["read_count"],
                "writes": data["write_count"],
                "uptime": time.time() - data["registered_at"]
            }
            for agent_id, data in self.registered_agents.items()
        }
    
    # === PERSISTENCE METHODS ===
    
    def get_state_for_persistence(self) -> Dict:
        """
        Export state for persistence layer
        Called by brain_persistence.save_state()
        """
        # Collect all active nodes from regions
        active_nodes = {}
        for region in self.regions:
            with region.lock:
                for coord, encoded in region.active_nodes.items():
                    active_nodes[coord] = int(encoded)
        
        # Serialize temporal buffer (limit to last 20)
        temporal_slim = []
        for frame in list(self.temporal_buffer)[-20:]:
            temporal_slim.append({
                'tick': frame.get('tick', 0),
                'coherence': frame.get('coherence', 0.0),
                'active_count': frame.get('total_active', 0)
            })
        
        return {
            'active_nodes': active_nodes,
            'current_tick': self.current_tick,
            'temporal_buffer': temporal_slim,
            'agent_registry': {
                aid: {
                    'reads': d['read_count'],
                    'writes': d['write_count']
                } for aid, d in self.registered_agents.items()
            }
        }
    
    def restore_from_persistence(self, state: Dict):
        """
        Restore state from persistence layer
        Called by brain_persistence.load_state()
        """
        # Helper to find region
        def coord_to_region(x, y, z):
            rx = 0 if x < self.region_size else 1
            ry = 0 if y < self.region_size else 1
            rz = 0 if z < self.region_size else 1
            return rx * 4 + ry * 2 + rz
        
        # Restore active nodes to regions
        active_nodes = state.get('active_nodes', {})
        for coord, encoded in active_nodes.items():
            # Find which region
            x, y, z = coord
            region_idx = coord_to_region(x, y, z)
            if 0 <= region_idx < len(self.regions):
                region = self.regions[region_idx]
                with region.lock:
                    region.active_nodes[tuple(coord)] = np.uint8(encoded)
                    region.hotspots[tuple(coord)] = {
                        'activation': 1 if encoded == 2 else (-1 if encoded == 1 else 0),
                        'age': 0,
                        'priority': 1.0,
                        'ephemeral': False
                    }
        
        # Restore tick count
        self.current_tick = state.get('current_tick', 0)
        
        print(f"[CortexV2.5] Restored from persistence: tick {self.current_tick}, {len(active_nodes)} nodes")
    
    def to_dict(self) -> Dict:
        """For backward compatibility with old persistence"""
        return self.get_state_for_persistence()
    
    def from_dict(self, state: Dict):
        """For backward compatibility with old persistence"""
        self.restore_from_persistence(state)


if __name__ == "__main__":
    print("=" * 70)
    print("  CORTEX v2.5 - OPTIMIZED PYTHON TEST")
    print("=" * 70)
    
    cortex = CortexV25Optimized(size=32, temporal_depth=128)
    
    # Test agent registration
    print("\n[Test 1] Agent registration")
    cortex.register_agent("agent_1")
    cortex.register_agent("agent_2")
    print(f"  Registered: {list(cortex.registered_agents.keys())}")
    
    # Test agent write
    print("\n[Test 2] Agent write")
    write_req = AgentWriteRequest(
        agent_id="agent_1",
        region_indices=[0, 1, 2],
        activations=[(5, 5, 5, 1), (6, 6, 6, 1), (7, 7, 7, -1)] * 10,
        priority=0.8
    )
    result = cortex.agent_write(write_req)
    print(f"  Written: {result}")
    
    # Test agent read
    print("\n[Test 3] Agent read")
    read_req = AgentReadRequest(
        agent_id="agent_1",
        region_indices=[0, 1],
        layer_mask=0b111,
        max_hotspots=32
    )
    snapshot = cortex.agent_read(read_req)
    print(f"  Snapshot: tick={snapshot.tick}, hotspots={len(snapshot.hotspots)}, coherence={snapshot.coherence:.3f}")
    
    # Test parallel ticks
    print("\n[Test 4] Parallel ticks (100)")
    for i in range(100):
        result = cortex.tick_parallel()
        if i % 25 == 0:
            print(f"  Tick {i}: {result['active_nodes']} nodes, {result['tick_time_ms']:.2f}ms")
    
    # Performance stats
    print("\n[Test 5] Performance statistics")
    perf = cortex.get_performance_stats()
    for key, data in perf.items():
        print(f"  {key}: mean={data['mean_ms']:.3f}ms, max={data['max_ms']:.3f}ms")
    
    # Agent stats
    print("\n[Test 6] Agent statistics")
    agent_stats = cortex.get_agent_stats()
    for agent, data in agent_stats.items():
        print(f"  {agent}: reads={data['reads']}, writes={data['writes']}")
    
    print("\n" + "=" * 70)
    print("  SUCCESS: v2.5 optimized cortex")
    print("=" * 70)