# Alternative Models Landscape
## Bonsai Quantization Lab Research

**Task:** BQL-007 | **Analyst:** Agent Gamma

---

## Executive Summary

Bonsai is **not unique** but leads in intelligence density. Multiple ternary and Qwen3-based alternatives exist. The lab has fallback options if Bonsai conversion proves impossible.

---

## Direct Bonsai Alternatives (Ternary 1.58-bit)

### 1. PrismML Ternary Bonsai Family

| Model | Params | GGUF | MLX | Size (Q2_0) |
|-------|--------|------|-----|-------------|
| Ternary-Bonsai-1.7B | 1.7B | ✅ | ✅ | ~0.5 GB |
| Ternary-Bonsai-4B | 4B | ✅ | ✅ | ~1.0 GB |
| Ternary-Bonsai-8B | 8B | ✅ | ✅ | **2.03 GB** |

**Base:** Qwen3-8B  
**Architecture:** GQA, SwiGLU, RoPE, RMSNorm  
**Context:** 65K tokens  
**License:** Apache 2.0  

**Performance:** 2nd among 6B-9B models tested, despite 8× smaller than Qwen3 8B

**Availability:**
- HF: `prism-ml/Ternary-Bonsai-*B-gguf`
- Requires: PrismML fork of llama.cpp

---

### 2. Microsoft BitNet Official

| Model | Params | Format | Size | Notes |
|-------|--------|--------|------|-------|
| BitNet-b1.58-2B-4T | 2.4B | Custom | ~3GB | Latest official |
| bitnet_b1_58-large | 0.7B | Custom | ~1GB | Experimental |
| bitnet_b1_58-3B | 3.3B | Custom | ~4GB | Research model |
| Llama3-8B-1.58-100B | 8B | Custom | ~10GB | Llama3 based |

**Format:** i2_s, tl1, tl2 (not GGUF-compatible)  
**Inference:** bitnet.cpp (Microsoft fork)  
**Status:** Active development (GPU support added May 2025)

**Key Limitation:** Uses different ternary encoding than Bonsai. Cannot run Bonsai models.

---

### 3. TII Falcon3 (1.58-bit Variants)

| Model | Params | GGUF | 1.58-bit GGUF | Notes |
|-------|--------|------|---------------|-------|
| Falcon3-1B-Instruct-1.58bit | 1B | ✅ | ✅ | Smallest option |
| Falcon3-3B-Instruct-1.58bit | 3B | ✅ | ✅ | Mid-size |
| Falcon3-7B-Instruct-1.58bit | 7B | ✅ | ✅ | Has GGUF version |
| Falcon3-10B-Instruct-1.58bit | 10B | ✅ | ✅ | Largest Falcon3 |

**Availability:** HF: `tiiuae/Falcon3-*-Instruct-1.58bit-GGUF`

**Question:** Do Falcon3 1.58-bit GGUFs work in standard Ollama?  
**Requires verification** - format compatibility unknown.

---

## Qwen3-Based Fallbacks (Standard Quantization)

Since Bonsai is Qwen3-based, these are direct alternatives:

### Ollama Official Library

| Model | Params | Ollama Tag | Size (Q4) | Notes |
|-------|--------|------------|-----------|-------|
| qwen3 | 8B | `qwen3:8b` | ~5.5 GB | Full capability |
| qwen3 | 4B | `qwen3:4b` | ~2.8 GB | Mid-tier |
| qwen3 | 1.7B | `qwen3:1.7b` | ~1.2 GB | Comparable to Bonsai |
| qwen3 | 0.6B | `qwen3:0.6b` | ~0.5 GB | Smallest |
| qwen3.5 | 9B | `qwen3.5:9b` | ~6.0 GB | Latest generation |
| qwen3.6 | 35B | `qwen3.6:35b` | ~22 GB | MoE architecture |

### Qwen3 Performance vs Bonsai 8B

| Model | Size | Avg Score | Intelligence Density |
|-------|------|-----------|-------------------|
| Qwen3 8B | 16.38 GB | 79.3 | 0.096 |
| **Ternary Bonsai 8B** | **2.18 GB** | **75.5** | **0.645** |
| Qwen3 4B | ~8 GB | ~72 | ~0.15 |

**Verdict:** Qwen3 8B scores higher but is 7.5× larger. For constrained deployment, Bonsai wins on density.

---

## Alternative Ternary Research

### HF1BitLLM Family

| Model | Params | Notes |
|-------|--------|-------|
| HF1BitLLM/Llama3-8B-1.58-100B-tokens | 8B | Community ternary |

### 1bitLLM Organization

| Model | Params | Notes |
|-------|--------|-------|
| 1bitLLM/bitnet_b1_58-large | 0.7B | Early research |
| 1bitLLM/bitnet_b1_58-3B | 3.3B | Research model |

---

## Conversion Tool Alternatives

### If Ternary → Q4 Conversion Needed

| Tool | Supports | Output |
|------|----------|--------|
| llama-quantize (llama.cpp) | F16/Q8 → Q4 | Standard GGUF |
| convert-hf-to-gguf.py | HF → GGUF | Various quants |
| BitNet setup_env.py | BitNet → i2_s | Custom format |
| **None found** | Q2_0 → Q4 | ❌ Not available |

**Gap Identified:** No tool exists to convert Q2_0 ternary to standard quantization.

---

## Decision Matrix

### If We Need to Replace Bonsai...

| Priority | Option | Effort | Quality | Size |
|----------|--------|--------|---------|------|
| 1 | Qwen3:8b (Ollama) | Low | ⭐⭐⭐⭐⭐ | 5.5 GB |
| 2 | Qwen3:4b (Ollama) | Low | ⭐⭐⭐⭐ | 2.8 GB |
| 3 | Falcon3-7B-1.58bit-GGUF | Medium | ⭐⭐⭐ | ~2 GB |
| 4 | BitNet-b1.58-2B | High | ⭐⭐⭐ | ~3 GB |
| 5 | Custom Q2_0→Q4 converter | Very High | ⭐⭐⭐ | ~2 GB |

### If We Stick with Bonsai...

| Approach | Effort | Maintainability |
|----------|--------|-----------------|
| Use PrismML fork | Medium | Medium |
| Build custom runner | High | Low |
| Wait for upstream | Low | High (eventually) |

---

## Key Findings

1. **Bonsai is unique in ecosystem:** Only Qwen3-based ternary with GGUF Q2_0 format
2. **Qwen3 family provides drop-in replacement:** Available in Ollama today
3. **Falcon3 has ternary GGUFs:** May work with Ollama (needs testing)
4. **Microsoft BitNet is separate ecosystem:** Different encoding, different tools
5. **No conversion bridge exists:** Q2_0 cannot be converted to Q4 with existing tools

---

## Recommendations

### Immediate (This Week)
- [ ] Test `qwen3:8b` in Ollama as baseline
- [ ] Test `falcon3-7b-instruct-1.58bit-gguf` if available
- [ ] Verify current Ollama version and quantization support

### Short Term (Next 2 Weeks)
- [ ] Benchmark Qwen3 variants vs Bonsai capability
- [ ] Evaluate if Qwen3:4b meets requirements (similar size to Bonsai 8B)
- [ ] Test PrismML fork if local deployment acceptable

### Long Term (Month)
- [ ] Monitor llama.cpp for Q2_0 upstream merge
- [ ] Evaluate building custom converter (if worth investment)
- [ ] Track Microsoft BitNet for standardization

---

## References

- [PrismML Ternary Bonsai](https://huggingface.co/prism-ml/Ternary-Bonsai-8B-gguf)
- [Microsoft BitNet](https://github.com/microsoft/BitNet)
- [Falcon3 Collection](https://huggingface.co/collections/tiiuae/falcon3)
- [Ollama Qwen3](https://ollama.com/library/qwen3)
- [HF1BitLLM](https://huggingface.co/HF1BitLLM)

---

*Document: BQL-007 Complete | Intelligence Level: HIGH | Updated: 2026-04-22*
