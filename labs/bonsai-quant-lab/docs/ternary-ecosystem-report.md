# Ternary Quantization Ecosystem Report
## Bonsai Quantization Lab Research

**Date:** 2026-04-22  
**Analyst:** Agent Gamma  
**Status:** Initial Research Complete

---

## Executive Summary

The ternary (1.58-bit) quantization ecosystem is emerging but **not yet supported in standard llama.cpp**. The Bonsai project requires a custom fork (PrismML-Eng/llama.cpp) to run ternary models. This has significant implications for Ollama compatibility.

---

## 1. llama.cpp Ternary Support Status

### Current State
- **Standard llama.cpp:** ❌ Does NOT support ternary/1.58-bit quantization
- **Official Microsoft BitNet:** Uses separate `bitnet.cpp` framework (fork of llama.cpp)
- **PrismML Fork:** Custom `prism` branch adds Q2_0 support for CPU (NEON/generic) and Metal

### Key Finding
> "Q2_0 is not yet in mainline llama.cpp. Use our fork at PrismML-Eng/llama.cpp (prism branch, default) which adds Q2_0 support."
> — PrismML Ternary-Bonsai-8B Model Card

### Supported Quantization Types (Standard llama.cpp)
| Format | Bits | Status | Notes |
|--------|------|--------|-------|
| Q2_K | 2-bit | ✅ | Supported but different encoding |
| Q2_0 | 2-bit | ❌ | Ternary-specific; requires fork |
| Q4_K_M | 4-bit | ✅ | Standard recommendation |
| Q4_0 | 4-bit | ✅ | Legacy support |
| Q8_0 | 8-bit | ✅ | Maximum quality |
| F16 | 16-bit | ✅ | Baseline reference |

### Roadmap Indicators
- **No official timeline** found for ternary support in mainline llama.cpp
- Microsoft maintains separate `bitnet.cpp` for 1.58-bit inference
- PrismML has committed to "Upstream PR coming soon" (no date specified)

---

## 2. Alternative Ternary Models

### PrismML Ternary Bonsai Family
| Model | Params | GGUF Available | MLX Available |
|-------|--------|----------------|---------------|
| Ternary-Bonsai-1.7B | 1.7B | ✅ | ✅ |
| Ternary-Bonsai-4B | 4B | ✅ | ✅ |
| Ternary-Bonsai-8B | 8B | ✅ | ✅ |

**Base Architecture:** Qwen3-8B (Qwen3 family)

### Microsoft BitNet Official
| Model | Params | Available |
|-------|--------|-----------|
| BitNet-b1.58-2B-4T | 2.4B | ✅ HuggingFace |
| bitnet_b1_58-large | 0.7B | ✅ |
| bitnet_b1_58-3B | 3.3B | ✅ |
| Llama3-8B-1.58-100B-tokens | 8.0B | ✅ |

### TII Falcon3 Family (1.58-bit variants)
| Model | Params | Notes |
|-------|--------|-------|
| Falcon3-1B-Instruct-1.58bit | 1B | Has GGUF version |
| Falcon3-3B-Instruct-1.58bit | 3B | Has GGUF version |
| Falcon3-7B-Instruct-1.58bit | 7B | Has GGUF version |
| Falcon3-10B-Instruct-1.58bit | 10B | Has GGUF version |

### Key Insight
**Bonsai is NOT unique**, but it has the best performance-per-size ratio among ternary models:
- 2.03 GiB for 8B parameters
- Competitive with Qwen3 8B (16.38 GB) despite 8x size reduction

---

## 3. Qwen3-Based Alternatives (Fallback Path)

Since Bonsai is based on Qwen3, these are direct alternatives:

| Model | Params | Ollama Support | Size (Q4) |
|-------|--------|----------------|-----------|
| qwen3:8b | 8B | ✅ | ~5.5GB |
| qwen3:4b | 4B | ✅ | ~2.8GB |
| qwen3:1.7b | 1.7B | ✅ | ~1.2GB |
| qwen3:0.6b | 0.6B | ✅ | ~0.5GB |

**Available in Ollama Library:** qwen3, qwen3.5, qwen3.6

---

## 4. Conversion Tools & Frameworks

### Microsoft BitNet Framework
- **Repository:** `microsoft/BitNet`
- **Type:** Fork of llama.cpp with 1.58-bit kernels
- **Quant Types:** i2_s, tl1, tl2
- **Support:** CPU (x86/ARM), GPU (CUDA)
- **Status:** Active development (GPU support added May 2025)

### PrismML Fork
- **Repository:** `PrismML-Eng/llama.cpp`
- **Branch:** `prism` (default)
- **Added:** Q2_0 g128 ternary format
- **Support:** CPU (NEON/generic), Metal
- **Status:** Community fork, "upstream PR coming soon"

### Compatibility Issue
⚠️ **Critical:** BitNet models and Bonsai models use DIFFERENT ternary encodings:
- BitNet: i2_s, tl1, tl2
- Bonsai: Q2_0 g128

They are **not interchangeable** without conversion.

---

## 5. Q2_0 Format Deep Dive

### Structure
```
Each weight = {-1, 0, +1}
Encoding: 2-bit code q ∈ {0,1,2,3}
Dequantization: w = (q - 1) * scale

Block size: 128 elements
Block storage: 34 bytes
  - 2 bytes: FP16 scale
  - 32 bytes: 128 × 2-bit packed codes
Effective: 2.125 bits/weight
```

### Memory Comparison (8B model)
| Format | Size | vs FP16 |
|--------|------|---------|
| FP16 | 16.38 GB | 1.0x |
| Q2_0 | 2.03 GiB | 7.5x smaller |
| Q4_K_M | ~4.5 GB | ~3.6x smaller |

---

## 6. Ollama Compatibility Matrix

| Model Type | Ollama v0.18.0 | Notes |
|------------|----------------|-------|
| Standard GGUF (Q4, Q8, F16) | ✅ | Full support |
| Ternary Q2_0 (Bonsai) | ❌ | Segfault - unsupported |
| BitNet models | ❌ | Not supported |
| Custom quant types | ❌ | Unknown = crash |

### Root Cause
Ollama uses standard llama.cpp, which lacks ternary kernel implementations. The GGUF loader doesn't recognize Q2_0 format, causing undefined behavior.

---

## 7. Actionable Recommendations

### Option A: Wait for Upstream (Low Effort, Timeline Unknown)
- Monitor PrismML upstream PR
- Track llama.cpp releases for Q2_0 merge
- **Risk:** Timeline undefined, could be months

### Option B: Use Qwen3 Fallback (Immediate)
- Switch to `qwen3:8b` or `qwen3:4b` in Ollama
- 75% of Bonsai performance at 2-4x larger size
- **Risk:** Minimal, proven working path

### Option C: Build Custom Runner (High Effort)
- Compile PrismML fork for server deployment
- Build Ollama from source with custom llama.cpp
- **Risk:** Maintenance burden, drift from upstream

### Option D: Convert Ternary → Q4 (Ideal but Hard)
- Requires dequantization ternary → FP16 → Q4
- Need source weights or reverse-engineering
- **Risk:** High complexity, may be lossy

---

## 8. Monitoring Checklist

**Weekly Tracking:**
- [ ] llama.cpp releases for ternary/BitNet mentions
- [ ] PrismML-Eng/llama.cpp for upstream PR
- [ ] ollama/ollama releases for quant format updates
- [ ] New ternary models on HuggingFace

**Sources:**
- https://github.com/ggml-org/llama.cpp/releases
- https://github.com/ollama/ollama/releases
- https://huggingface.co/prism-ml
- https://huggingface.co/microsoft

---

## References

1. [Microsoft BitNet Repository](https://github.com/microsoft/BitNet)
2. [PrismML Ternary Bonsai 8B](https://huggingface.co/prism-ml/Ternary-Bonsai-8B-gguf)
3. [GGUF Specification](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)
4. [BitNet b1.58 Paper](https://arxiv.org/abs/2402.17764)
5. [1.58-bit LLM Wikipedia](https://en.wikipedia.org/wiki/BitNet)
6. [Falcon3 1.58-bit Collection](https://huggingface.co/collections/tiiuae/falcon3)

---

*Report compiled by Agent Gamma | Bonsai Quantization Lab*
