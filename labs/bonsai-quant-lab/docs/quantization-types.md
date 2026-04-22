# Quantization Types Reference
## Bonsai Quantization Lab Technical Documentation

**Document ID:** BQL-DOC-001  
**Version:** 1.0  
**Updated:** 2026-04-22  
**Status:** Complete

---

## Executive Summary

This document catalogs quantization formats relevant to the Bonsai ecosystem, with special focus on Q1_0 (1-bit), Q2_0 (ternary/1.58-bit), and standard GGUF formats. Includes upstream status, compatibility matrix, and format comparison.

---

## 1. Q1_0 (1-bit Bonsai)

### Technical Specification

| Property | Value |
|----------|-------|
| **Weight values** | {-1, +1} (binary) |
| **Bits per weight** | 1.125 (1 bit + FP16 scale/128) |
| **Group size** | 128 |
| **Block storage** | 18 bytes (1 byte overhead + weights) |
| **Upsteam llama.cpp** | ✅ **MERGED** |
| **Ollama compatible** | ✅ **YES (v0.18.0+)** |

### Upstream Status
- **Merged in llama.cpp:** YES, as of mainline releases
- **Ollama support:** Native, works in stock Ollama
- **Prerequisites:** None

### Use Cases
1. **Immediate deployment** when ternary is unavailable
2. **Ultra-constrained environments** (smallest size: ~1.15 GB for 8B)
3. **Edge devices** with limited storage
4. **Proof-of-concept** for 1-bit quantization viability

### Performance (Bonsai-8B)
- **Size:** ~1.15 GB
- **Quality Score:** ~70.5 (vs Qwen3 8B: 79.3)
- **Intelligence Density:** 1.062 (highest of any format)

---

## 2. Q2_0 (Ternary / 1.58-bit)

### Technical Specification

| Property | Value |
|----------|-------|
| **Weight values** | {-1, 0, +1} (ternary) |
| **Information content** | log₂(3) ≈ 1.58 bits |
| **Storage encoding** | 2-bit codes {0,1,2,3} |
| **Group size** | 128 |
| **Block size** | 128 weights |
| **Block storage** | 34 bytes (2 bytes FP16 scale + 32 bytes packed codes) |
| **Effective bits** | 2.125 bits/weight |

### Dequantization Formula
```
q = 2-bit code ∈ {0, 1, 2, 3}
t = q - 1 ∈ {-1, 0, +1}  (ternary value)
w = t × scale            (final weight)

Note: Code 3 (+2) reserved for future extensions
```

### Upstream Status
- **Merged in llama.cpp:** ❌ **NOT MERGED**
- **Ollama support:** ❌ **NO** (causes segfault)
- **Available via:** PrismML fork only

### Why Ternary Fails in Standard Ollama

#### The Group Size Conflict

llama.cpp has TQ1_0 and TQ2_0 formats that are conceptually similar:

| Format | Group Size | Bonsai Compatible? |
|--------|------------|-------------------|
| TQ1_0 | 256 | ❌ No - different grouping |
| TQ2_0 | 256 | ❌ No - different grouping |
| Q1_0 (Bonsai) | 128 | ✅ Yes - merged |
| Q2_0 (Bonsai) | 128 | ✅ Yes - PrismML only |

**Root cause:** Bonsai uses g128, but llama.cpp TQ formats use g256. The weights won't align, causing incompatible tensor layouts.

### Use Cases
1. **Best quality** among Bonsai variants (75.5 score)
2. **Research environments** where custom builds are acceptable
3. **Future-proofing** when upstream merges
4. **Apple Silicon** via PrismML fork Metal support

### Performance (Ternary-Bonsai-8B)
- **Size:** 2.03 GB
- **Quality Score:** 75.5 (vs Qwen3 8B: 79.3)
- **Intelligence Density:** 0.645

---

## 3. Q4_K_M (Standard 4-bit)

### Technical Specification

| Property | Value |
|----------|-------|
| **Bits per weight** | 4.5 (mixed-precision) |
| **Quantization type** | K-quant (mixed per layer) |
| **Block handling** | Variable blocks per tensor |
| **Upsteam llama.cpp** | ✅ **MERGED** |
| **Ollama support** | ✅ **YES** |

### Upstream Status
- **Standard:** Default recommendation in llama.cpp
- **Stability:** Production-ready, battle-tested
- **Compatibility:** Universal across GGUF tools

### Use Cases
1. **Default choice** for production deployments
2. **Ollama models** from official library
3. **Balanced** size vs quality tradeoff
4. **Fallback** when exotic quantizations fail

### Performance (Qwen3-8B as reference)
- **Size:** ~4.5 GB
- **Quality Score:** ~76-78 (vs FP16: 79.3, minimal loss)
- **Compatibility:** 100% with Ollama, llama.cpp, MLX

---

## 4. Q8_0 (Standard 8-bit)

### Technical Specification

| Property | Value |
|----------|-------|
| **Bits per weight** | 8.125 |
| **Block size** | 32 |
| **Upsteam llama.cpp** | ✅ **MERGED** |
| **Ollama support** | ✅ **YES** |

### Upstream Status
- **Standard:** Full upstream support
- **Use case:** Maximum quality with quantization
- **Tradeoff:** 2x larger than Q4

### Use Cases
1. **Quality-critical** applications
2. **When Q4 artifacts** are noticeable
3. **Reference baseline** for quantization studies

### Performance (Qwen3-8B as reference)
- **Size:** ~8.2 GB
- **Quality Score:** ~78-79 (vs FP16: 79.3, ~1% loss)

---

## 5. Format Comparison Table

### Size Comparison (8B Parameters)

| Format | Size | vs FP16 | Compression | Upstream Status |
|--------|------|---------|-------------|-----------------|
| F16 | 16.38 GB | 1.0x | — | ✅ Merged |
| Q8_0 | ~8.2 GB | 2.0x | 50% | ✅ Merged |
| Q4_K_M | ~4.5 GB | 3.6x | 72% | ✅ Merged |
| **Q2_0** | **2.03 GB** | **8.1x** | **88%** | ❌ PrismML fork |
| **Q1_0** | **1.15 GB** | **14.2x** | **93%** | ✅ Merged |

### Quality Comparison (Benchmark Scores)

| Format | Avg Score | vs FP16 | Notes |
|--------|-----------|---------|-------|
| F16 | 79.3 | 0% | Baseline |
| Q8_0 | ~78.5 | ~1% | Minimal loss |
| Q4_K_M | ~76.8 | ~3% | Recommended |
| **Q2_0** | **75.5** | **~5%** | **Ternary (Bonsai)** |
| **Q1_0** | **70.5** | **~11%** | **1-bit (Bonsai)** |

### Intelligence Density (Score / GB)

| Format | Density | Best For |
|--------|---------|----------|
| Q1_0 | 1.062 | Ultra-constrained edge |
| Q2_0 | 0.645 | Balanced compression |
| Q4_K_M | ~0.17 | Standard production |
| Q8_0 | ~0.10 | Quality-first |
| F16 | ~0.005 | Baseline reference |

---

## 6. Compatibility Matrix

### Framework Support

| Format | llama.cpp | PrismML Fork | Ollama | MLX | BitNet |
|--------|-----------|--------------|--------|-----|--------|
| F16 | ✅ | ✅ | ✅ | ✅ | ⚠️ Partial |
| Q8_0 | ✅ | ✅ | ✅ | ✅ | ❌ |
| Q4_K_M | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Q1_0** | ✅ | ✅ | **✅** | ⚠️ Via GGUF | ❌ |
| **Q2_0** | ❌ | **✅** | **❌** | **⚠️ Via MLX** | ❌ |
| i2_s/tl1 | ❌ | ❌ | ❌ | ❌ | ✅ |

### Ollama Version Compatibility

| Format | v0.18.0 | v0.17.x | v0.16.x | Notes |
|--------|---------|---------|---------|-------|
| F16 | ✅ | ✅ | ✅ | — |
| Q8_0 | ✅ | ✅ | ✅ | — |
| Q4_K_M | ✅ | ✅ | ✅ | — |
| **Q1_0** | **✅** | **✅** | **✅** | **Bonsai 1-bit** |
| **Q2_0** | **❌** | **❌** | **❌** | **Requires fork** |

---

## 7. Key Findings from PrismML Research

### Critical Discovery
> "Q2_0 is not yet in mainline llama.cpp. Use our fork at PrismML-Eng/llama.cpp (prism branch) which adds Q2_0 support."
> — PrismML Ternary-Bonsai-8B Model Card

### The Problem
- **Q1_0 (1-bit Bonsai):** MERGED upstream ✅
- **Q2_0 (Ternary Bonsai):** NOT merged ❌
- **TQ formats (llama.cpp):** Group size 256 (incompatible with Bonsai g128)

### Solution Paths
1. **Use 1-bit Bonsai** → Works in stock Ollama today
2. **Use PrismML fork** → Ternary works with custom build
3. **Wait for upstream** → Timeline unknown

---

## 8. References

1. [GGUF Specification v3](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)
2. [llama.cpp Quantization](https://github.com/ggml-org/llama.cpp/blob/master/gguf-py/README.md)
3. [PrismML 1-bit Model Card](https://huggingface.co/prism-ml/Bonsai-8B-gguf)
4. [PrismML Ternary Model Card](https://huggingface.co/prism-ml/Ternary-Bonsai-8B-gguf)
5. [PrismML Fork](https://github.com/PrismML-Eng/llama.cpp)
6. [BitNet Paper](https://arxiv.org/abs/2402.17764)

---

*Document: BQL-DOC-001 | Status: Complete | Classification: Lab Reference*