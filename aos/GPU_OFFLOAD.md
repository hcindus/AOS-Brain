# Cortex v2.5 GPU Offload Guide

## Current State

### Python (CuPy)
```python
import cupy as cp

# GPU convolution for propagation
kernel = cp.ones((3, 3, 3), dtype=cp.float32) / 27.0
convolved = cp.signal.convolve(gpu_volume, kernel, mode='same')

# Quantize back to ternary
gpu_volume = cp.where(convolved > 0.3, TERNARY_POS,
              cp.where(convolved < -0.3, TERNARY_NEG, TERNARY_NULL))
```

**When GPU is used:**
- Every 10th tick (configurable)
- Large batch operations
- Sync results back to CPU regions

### Future: Vulkan Compute

For non-CUDA GPUs (AMD, Intel):

```python
import ctypes
vulkan_lib = ctypes.CDLL('./vulkan_cortex.so')

# Launch compute shader
vulkan_lib.propagate_ternary(
    buffer_in, buffer_out, size, workgroup_size
)
```

## Performance Targets

| Implementation | Tick Time | Speedup |
|----------------|-----------|---------|
| Python v1 (dense) | 2-5ms | 1x |
| Python v2.5 (sparse) | 0.7-1.0ms | 3-5x |
| Python + GPU (every 10th) | 0.5-0.8ms | 4-7x |
| Rust (CPU) | 0.1-0.2ms | 15-25x |
| Rust + GPU | 0.05-0.1ms | 30-50x |

## SIMD Strategy

### x86_64 (AVX2)
```rust
// Process 32 ternary values at once (16 bytes)
use std::simd::*;

let chunk: u8x32 = u8x32::from_slice(&data[i..]);
let mask = chunk & u8x32::splat(0b11);
// Parallel ternary operations
```

### ARM NEON
```rust
#[cfg(target_arch = "aarch64")]
use std::arch::aarch64::*;

let mut vec = vld1q_u8(data.as_ptr());
vec = vandq_u8(vec, vdupq_n_u8(0b11));
```

## Agent API

Agents can request GPU-accelerated operations:

```python
# Agent requests large-scale pattern search
read_req = AgentReadRequest(
    agent_id="search_agent",
    region_indices=[0,1,2,3,4,5,6,7],  # All regions
    use_gpu=True,  # Use GPU for aggregation
    max_hotspots=1024
)
```