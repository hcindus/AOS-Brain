# Quantization Types Reference
## Bonsai Quantization Lab Technical Documentation

**Purpose:** Understand quantization formats for model conversion

---

## Overview

Quantization reduces model size by using fewer bits per weight. Different formats trade off size, speed, and quality.

---

## Standard GGUF Quantization Types

### Floating Point

| Format | Bits | Use Case | Notes |
|--------|------|----------|-------|
| **F32** | 32-bit | Training reference | Too large for inference |
| **F16** | 16-bit | Baseline quality | 2× memory vs Q8 |
| **BF16** | 16-bit | Training stability | Similar to F16 |

### Integer Quantization (Standard)

| Format | Bits/Weight | Description | Quality | Size |
|--------|-------------|-------------|---------|------|
| **Q8_0** | 8-bit | Block-wise 8-bit | ⭐⭐⭐⭐⭐ | 50% of F16 |
| **Q6_K** | 6-bit | K-quant variant | ⭐⭐⭐⭐ | ~38% of F16 |
| **Q5_K_M** | 5-bit | Mixed K-quant | ⭐⭐⭐⭐ | ~31% of F16 |
| **Q5_K_S** | 5-bit | Small K-quant | ⭐⭐⭐ | ~31% of F16 |
| **Q4_K_M** | 4-bit | **Recommended** | ⭐⭐⭐ | ~25% of F16 |
| **Q4_K_S** | 4-bit | Small variant | ⭐⭐⭐ | ~25% of F16 |
| **Q4_0** | 4-bit | Legacy 4-bit | ⭐⭐ | ~25% of F16 |
| **Q3_K_M** | 3-bit | K-quant medium | ⭐⭐ | ~19% of F16 |
| **Q3_K_S** | 3-bit | K-quant small | ⭐⭐ | ~19% of F16 |
| **Q2_K** | 2-bit | K-quant | ⭐ | ~13% of F16 |

### Key Distinction
- **K-quants:** Mixed-precision per layer (better quality)
- **Legacy (Q4_0, Q8_0):** Uniform quantization

---

## Ternary Quantization (1.58-bit)

### What is 1.58-bit?

Ternary weights use only **3 values**: {-1, 0, +1}

Information theory:
- 3 states = log₂(3) ≈ **1.58 bits**
- Named "1.58-bit" or "ternary"

### Bonsai Q2_0 Format

| Property | Value |
|----------|-------|
| **Values** | {-1, 0, +1} |
| **Encoding** | 2-bit codes {0,1,2,3} |
| **Block size** | 128 weights |
| **Block storage** | 34 bytes |
| **Effective bits** | 2.125 bits/weight |
| **Scale per block** | FP16 |

### Dequantization Formula
```
q = 2-bit code ∈ {0, 1, 2, 3}
t = q - 1 ∈ {-1, 0, +1}  (ternary value)
w = t × scale            (final weight)
```

Note: Code `3` (+2) is reserved for future extensions.

---

## Comparison: 8B Model Sizes

| Format | Size | vs FP16 | Quality Loss |
|--------|------|---------|--------------|
| F16 | 16.38 GB | 1.0x | 0% (baseline) |
| Q8_0 | ~8.2 GB | 2.0x | ~1% |
| Q4_K_M | ~4.5 GB | 3.6x | ~3-5% |
| **Q2_0 (Ternary)** | **2.03 GB** | **8.1x** | **~5-10%** |
| Q2_K | ~2.1 GB | 7.8x | ~15-20% |

---

## Microsoft BitNet Formats

| Format | Description | Status |
|--------|-------------|--------|
| **i2_s** | 2-bit signed | Supported (CPU) |
| **tl1** | Ternary lookup table | Supported (ARM) |
| **tl2** | Ternary lookup v2 | Experimental |

BitNet uses different encoding than Q2_0:
- Lookup table methodology
- Optimized for {-1, 0, +1} specifically
- Part of T-MAC framework

---

## Conversion Possibilities

### Can Ternary → FP16 → Q4?

**Yes, theoretically:**
1. Dequantize Q2_0: w = (q - 1) × scale
2. Results in approximate FP16 values
3. Requantize to Q4_K_M

**Challenges:**
- Requires decoding Q2_0 format
- Quality loss: compound (ternary + Q4)
- No standard tool exists

### Tools Required

| Task | Tool Status |
|------|-------------|
| Q2_0 → GGUF | ❌ Not available |
| BitNet → GGUF | ⚠️ Custom BitNet only |
| Generic ternary convert | ❌ None found |

---

## Recommendation Matrix

| Goal | Recommended Format | Reason |
|------|-------------------|--------|
| Maximum quality | Q8_0 or F16 | Minimal loss |
| Best balance | Q4_K_M | Good quality, 4× smaller |
| Edge deployment | Q4_K_M | Broad support |
| Research/Experiment | Q2_0 | Cutting edge size |
| Production (Ollama) | Q4_K_M or Q8_0 | Stable, supported |

---

## Format Support Summary

| Framework | Q2_0 | Q4_K_M | Q8_0 | F16 |
|-----------|------|--------|------|-----|
| llama.cpp | ❌ | ✅ | ✅ | ✅ |
| PrismML fork | ✅ | ✅ | ✅ | ✅ |
| Microsoft BitNet | ❌ | ❌ | ❌ | ⚠️ Partial |
| Ollama | ❌ | ✅ | ✅ | ✅ |
| MLX (Apple) | ⚠️ Via MLX format | ✅ | ✅ | ✅ |

---

## References

- [GGUF Spec](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)
- [llama.cpp Quantization](https://github.com/ggml-org/llama.cpp/blob/master/gguf-py/README.md)
- [BitNet Paper](https://arxiv.org/abs/2402.17764)
- [T-MAC Framework](https://github.com/microsoft/T-MAC/)

---

*Document: BQL-008.1 | Status: Draft | Updated: 2026-04-22*
