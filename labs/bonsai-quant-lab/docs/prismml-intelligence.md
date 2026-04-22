# URGENT: PrismML Bonsai Technical Intelligence
**Source:** https://github.com/PrismML-Eng/Bonsai-demo  
**Discovered:** 2026-04-22 02:01 UTC  
**Classification:** Lab Critical — Immediate Action Required

## Executive Summary

**The Q2_0 format for Ternary-Bonsai IS NOT in upstream llama.cpp yet.**

PrismML has a **working fork** with Q2_0 kernels. Upstream merge is "coming next" (as of their docs).

## Key Technical Details

### Format: Q2_0 (NOT standard GGUF)
- Q2_0 stores ~1.58-bit ternary weights in **2-bit aligned** format
- Hardware-friendly: maps cleanly to Metal/CUDA quantization paths
- Larger than tight ternary packing, but enables fast accelerated kernels

### llama.cpp Support Matrix

| Format | Upstream llama.cpp | PrismML Fork | Status |
|--------|-------------------|--------------|--------|
| Q1_0 (1-bit Bonsai) | ✅ **MERGED** | ✅ Available | Ready now |
| Q2_0 (Ternary-Bonsai) | ❌ **NOT merged** | ✅ **Available** | Need fork |

### The Group Size Problem
- llama.cpp has TQ1_0 and TQ2_0 formats (conceptually similar)
- BUT: TQ formats use **group size 256**
- Bonsai uses **group size 128**
- Result: Existing TQ formats **don't fit** Bonsai weights

## Solution Paths

### Option 1: Use PrismML Fork (Recommended)
```bash
# Clone their fork with Q2_0 support
git clone -b prism https://github.com/PrismML-Eng/llama.cpp.git
cd llama.cpp

# Build with your backend
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j$(nproc)

# Run Ternary-Bonsai
./build/bin/llama-cli \
  -m models/ternary-bonsai-8b-q2_0.gguf \
  -p "Your prompt"
```

**Pros:** Works today, has Metal/CUDA/Vulkan/CPU kernels  
**Cons:** Not upstream, need to maintain fork

### Option 2: Patch Ollama with PrismML Backend
```bash
# Replace llama.cpp submodule in Ollama with PrismML fork
# Rebuild Ollama from source
```

**Pros:** Keep Ollama API, get Q2_0 support  
**Cons:** Complex build, may break other models

### Option 3: Wait for Upstream
- PrismML states: "upstream PRs are coming next"
- No timeline given

**Pros:** No maintenance burden  
**Cons:** Indefinite wait

### Option 4: Use 1-bit Bonsai Instead
- Q1_0 (1-bit) **IS** merged upstream
- Available: Bonsai-8B, Bonsai-4B, Bonsai-1.7B

**Pros:** Works in stock Ollama today  
**Cons:** 1-bit vs 1.58-bit, may have different quality

## Action Items for Lab

### Immediate (Agent Alpha)
- [ ] Test 1-bit Bonsai in Ollama (Q1_0 merged)
- [ ] Clone PrismML llama.cpp fork
- [ ] Build with CPU backend
- [ ] Verify Ternary-Bonsai runs

### Short-term (Agent Beta)
- [ ] Compare 1-bit Bonsai vs Qwen3.5 vs tinyllama
- [ ] Benchmark decision quality

### Medium-term (Agent Gamma)
- [ ] Monitor upstream llama.cpp for Q2_0 merge
- [ ] Document fork maintenance requirements

## Decision Matrix

| Approach | Effort | Works Today | Maintenance | Recommendation |
|----------|--------|-------------|-------------|----------------|
| Use 1-bit Bonsai | Low | ✅ Yes | None | **Quick win** |
| PrismML Fork | Med | ✅ Yes | High | **Best long-term** |
| Patch Ollama | High | ✅ Yes | Very High | Avoid |
| Wait upstream | None | ❌ No | None | Parallel track |

## Resources

- PrismML Fork: https://github.com/PrismML-Eng/llama.cpp (prism branch)
- 1-bit Bonsai: https://huggingface.co/prism-ml/Bonsai-8B-gguf
- Ternary Bonsai: https://huggingface.co/prism-ml/Ternary-Bonsai-8B-gguf
- Pre-built Binaries: https://github.com/PrismML-Eng/llama.cpp/releases

---

**Recommendation to Patricia/Patricia2:**

1. **Immediate:** Test 1-bit Bonsai-8B as tinyllama replacement (it's already in upstream)
2. **Parallel:** Build PrismML fork for Ternary-Bonsai support
3. **Fallback:** Keep Qwen3.5 as proven working alternative

This explains why the Q2 model segfaults — Ollama 0.18.0 doesn't have the Q2_0 kernels.

---
*Intelligence gathered by: External web reconnaissance*  
*Relayed to Lab: 2026-04-22 02:01 UTC*
