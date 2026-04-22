# Bonsai Deployment Recommendations
## Strategic Guide for Model Selection & Migration

**Document ID:** BQL-DOC-003  
**Version:** 1.0  
**Updated:** 2026-04-22  
**Status:** Complete

---

## Executive Summary

Based on comprehensive PrismML repository research, this document provides actionable recommendations for deploying Bonsai models, including which model to use today, migration paths, and fallback options.

---

## 1. Which Model to Use Today

### Recommendation: Bonsai-8B Q1_0 (1-bit)

**Primary Recommendation for Immediate Deployment**

```
Model: Bonsai-8B-Q1_0
Format: 1-bit quantization (Q1_0)
Size: ~1.15 GB
Status: ✅ Ready for production in Ollama
```

### Why This Model?

| Criterion | Status |
|-----------|--------|
| **Works in stock Ollama** | ✅ Yes (v0.18.0+) |
| **No custom builds needed** | ✅ True |
| **Smallest footprint** | ✅ 1.15 GB for 8B params |
| **Upstream merged** | ✅ In llama.cpp mainline |
| **Available now** | ✅ HF: prism-ml/Bonsai-8B-gguf |

### Quality Assessment

| Metric | Value | Verdict |
|--------|-------|---------|
| **Benchmark Score** | 70.5 | Good for size |
| **vs Qwen3 8B** | -8.8 points | Acceptable tradeoff |
| **Intelligence Density** | 1.062 | **Best in class** |

**Verdict:** Quality is sufficient for most applications given the 14× size reduction.

---

## 2. Deployment Instructions

### Quick Start (Ollama)

```bash
# Step 1: Download the model
huggingface-cli download prism-ml/Bonsai-8B-gguf \
  bonsai-8b-q1_0.gguf \
  --local-dir ./models

# Step 2: Create Modelfile
cat > Modelfile << 'EOF'
FROM ./models/bonsai-8b-q1_0.gguf

PARAMETER temperature 0.5
PARAMETER top_p 0.85
PARAMETER top_k 20
PARAMETER num_ctx 4096

SYSTEM """You are a helpful AI assistant optimized for efficiency."""
EOF

# Step 3: Create Ollama model
ollama create bonsai-8b -f Modelfile

# Step 4: Test
ollama run bonsai-8b "Hello, explain your capabilities."
```

### Verification Checklist

- [ ] Model loads without errors
- [ ] Inference runs successfully
- [ ] Output quality is acceptable
- [ ] Performance meets requirements
- [ ] Memory usage is as expected (~1.2 GB)

---

## 3. Migration Path

### Current State → Target State

```
TODAY                          FUTURE
─────────────────────────────────────────────────
tinyllama (1.1B)      →        Bonsai-8B-Q1_0 (8B)
~1 GB, lower quality           ~1.15 GB, higher quality
─────────────────────────────────────────────────
```

### Migration Steps

#### Phase 1: Immediate (This Week)

1. **Download and Test**
   ```bash
   # Download Bonsai-8B-Q1_0
   huggingface-cli download prism-ml/Bonsai-8B-gguf \
     bonsai-8b-q1_0.gguf --local-dir ./models
   
   # Test with Ollama
   ollama create bonsai-test -f Modelfile
   ollama run bonsai-test
   ```

2. **Benchmark vs tinyllama**
   - Run side-by-side comparisons
   - Document quality differences
   - Measure inference speed

3. **Decision Point**
   - ✅ If quality acceptable: Proceed to Phase 2
   - ❌ If quality insufficient: See Fallback Options (Section 4)

#### Phase 2: Validation (Next 2 Weeks)

1. **Extended Testing**
   - Production-like workload testing
   - Stress test with concurrent requests
   - Memory profiling under load

2. **Integration**
   - Replace tinyllama in deployment scripts
   - Update documentation
   - Train team on new model

3. **Rollback Plan**
   - Keep tinyllama config available
   - Document quick rollback procedure

#### Phase 3: Production (Month 1)

1. **Gradual Rollout**
   - Deploy to staging first
   - Canary deployment to 10% traffic
   - Monitor for issues

2. **Full Migration**
   - Complete cutover when validated
   - Retire tinyllama from active use
   - Archive old configurations

#### Phase 4: Future-Proofing (Ongoing)

1. **Monitor Ternary Support**
   - Track PrismML fork for upstream merge
   - Watch llama.cpp releases
   - Evaluate Q2_0 when available

2. **Evaluate Q2_0 Migration**
   - When Q2_0 hits upstream:
     ```
     Bonsai-8B-Q1_0 → Ternary-Bonsai-8B-Q2_0
     1.15 GB → 2.03 GB (+76% size)
     70.5 → 75.5 score (+5 points quality)
     ```

3. **Decision Matrix for Future Migration**

| Scenario | Action |
|----------|--------|
| Q2_0 merges upstream | Evaluate upgrade to ternary |
| Q1_0 quality sufficient | Stay on 1-bit |
| Need higher quality now | See Fallback Options |

---

## 4. Fallback Options

### If Bonsai-8B-Q1_0 Quality is Insufficient

#### Option A: Qwen3 Family (Immediate, Ollama Native)

| Model | Size | Quality | Best For |
|-------|------|---------|----------|
| `qwen3:8b` | 5.5 GB | ⭐⭐⭐⭐⭐ | Full quality |
| `qwen3:4b` | 2.8 GB | ⭐⭐⭐⭐ | Balanced |
| `qwen3:1.7b` | 1.2 GB | ⭐⭐⭐ | Similar size to Bonsai |

**Deployment:**
```bash
# Immediate availability
ollama pull qwen3:8b
ollama run qwen3:8b
```

**Pros:**
- ✅ Works in Ollama today
- ✅ Higher quality than Bonsai
- ✅ Same architecture (Qwen3-based)

**Cons:**
- ❌ Larger size (5-6× Bonsai)
- ❌ Lower intelligence density

#### Option B: Build PrismML Fork (Medium Effort)

**For when Ternary quality is required:**

```bash
# Clone and build
# (See bonsai-model-matrix.md Section 2 for full instructions)
```

**Pros:**
- ✅ Ternary quality (75.5 score)
- ✅ 2.03 GB (still compact)

**Cons:**
- ❌ Custom build required
- ❌ No Ollama integration
- ❌ Maintenance burden

#### Option C: Falcon3 1.58-bit (Experimental)

| Model | Size | Ollama Status |
|-------|------|---------------|
| `falcon3-7b-instruct-1.58bit-gguf` | ~2 GB | ⚠️ Needs testing |

**Status:** Uncertain if GGUF works in Ollama. Requires validation.

#### Option D: Hybrid Approach (Recommended for Production)

**Tiered Model Strategy:**

```
┌─────────────────────────────────────────────────────────┐
│  Tier 1: Simple Queries → Bonsai-8B-Q1_0 (1.15 GB)     │
│           80% of traffic, ultra-low latency               │
├─────────────────────────────────────────────────────────┤
│  Tier 2: Complex Queries → Qwen3:4b (2.8 GB)           │
│           15% of traffic, higher quality                  │
├─────────────────────────────────────────────────────────┤
│  Tier 3: Critical Tasks → Qwen3:8b (5.5 GB)              │
│           5% of traffic, maximum quality                  │
└─────────────────────────────────────────────────────────┘
```

**Implementation:**
```python
# Example routing logic
def select_model(query_complexity):
    if query_complexity < 0.3:
        return "bonsai-8b-q1_0"  # Fast, efficient
    elif query_complexity < 0.8:
        return "qwen3:4b"         # Balanced
    else:
        return "qwen3:8b"         # Quality first
```

---

## 5. Decision Flowchart

```
START
  │
  ▼
Need ultra-small model (< 1.5 GB)?
  │
  ├── YES ──→ Use Bonsai-8B-Q1_0
  │              (1.15 GB, ready now)
  │
  └── NO ───→ Can use custom build?
                 │
                 ├── YES ──→ Build PrismML fork
                 │              (Ternary, 2.03 GB)
                 │
                 └── NO ───→ Use Qwen3:8b
                                (5.5 GB, native Ollama)
```

---

## 6. Key Findings Summary

### From PrismML Research

1. **Q1_0 is merged upstream** ✅
   - Bonsai-8B 1-bit works in stock Ollama
   - Available: prism-ml/Bonsai-8B-gguf

2. **Q2_0 requires fork** ❌
   - Ternary-Bonsai-8B segfaults in Ollama
   - Need PrismML-Eng/llama.cpp fork
   - No upstream timeline

3. **Group size incompatibility**
   - llama.cpp TQ formats: g256
   - Bonsai: g128
   - Result: Cannot reuse existing kernels

4. **Quality vs Size Tradeoff**
   - Q1_0: 70.5 score, 1.15 GB (best density)
   - Q2_0: 75.5 score, 2.03 GB (best quality/size)
   - Qwen3:8b: 79.3 score, 5.5 GB (best quality)

---

## 7. Monitoring Checklist

### Weekly Checks

- [ ] Check llama.cpp releases for Q2_0 merge
- [ ] Monitor PrismML fork for upstream PR
- [ ] Track Ollama releases for new quant support

### Monthly Reviews

- [ ] Re-evaluate if Q1_0 quality still sufficient
- [ ] Benchmark against new model releases
- [ ] Review resource utilization metrics

### Triggers for Re-evaluation

| Trigger | Action |
|---------|--------|
| Q2_0 merges upstream | Evaluate migration |
| Quality complaints spike | Consider fallback |
| New Qwen3 version released | Benchmark comparison |
| Storage costs increase | Reaffirm Q1_0 value |

---

## 8. References

1. [Bonsai-8B-gguf (1-bit)](https://huggingface.co/prism-ml/Bonsai-8B-gguf)
2. [Ternary-Bonsai-8B-gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-8B-gguf)
3. [PrismML Fork](https://github.com/PrismML-Eng/llama.cpp)
4. [Ollama Qwen3](https://ollama.com/library/qwen3)
5. [quantization-types.md](./quantization-types.md)
6. [bonsai-model-matrix.md](./bonsai-model-matrix.md)

---

## 9. Summary Table

| Model | Format | Size | Ollama | Quality | Recommendation |
|-------|--------|------|--------|---------|----------------|
| **Bonsai-8B** | **Q1_0** | **1.15 GB** | **✅** | **70.5** | **⭐ USE TODAY** |
| Ternary-Bonsai-8B | Q2_0 | 2.03 GB | ❌ | 75.5 | Future upgrade |
| Qwen3:8b | Q4_K_M | 5.5 GB | ✅ | 79.3 | Quality fallback |
| Qwen3:4b | Q4_K_M | 2.8 GB | ✅ | ~72 | Balanced fallback |

---

*Document: BQL-DOC-003 | Status: Complete | Classification: Strategic Guide*