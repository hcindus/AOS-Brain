# Bonsai Model Matrix
## Complete Model Availability & Status Reference

**Document ID:** BQL-DOC-002  
**Version:** 1.0  
**Updated:** 2026-04-22  
**Status:** Complete

---

## Executive Summary

This matrix documents all Bonsai model variants, their availability, quantization formats, and deployment status based on PrismML repository research.

---

## 1. Bonsai-8B (1-bit) - Q1_0 Format

### Model Information

| Property | Value |
|----------|-------|
| **Model ID** | Bonsai-8B-Q1_0 |
| **Architecture** | Qwen3-8B based |
| **Quantization** | Q1_0 (1-bit) |
| **Size** | ~1.15 GB |
| **Parameters** | 8.06B |
| **Context length** | 65,536 tokens |
| **License** | Apache 2.0 |

### Status

| Aspect | Status |
|--------|--------|
| **HuggingFace Availability** | ✅ Available |
| **GGUF Download** | ✅ Yes |
| **Upstream llama.cpp** | ✅ **MERGED** |
| **Ollama Compatible** | ✅ **YES** |
| **Ready for Production** | ✅ **YES** |

### HuggingFace Location
- **Repository:** `prism-ml/Bonsai-8B-gguf`
- **Files:** `bonsai-8b-q1_0.gguf`, `bonsai-8b-q1_0-Im.gguf`
- **URL:** https://huggingface.co/prism-ml/Bonsai-8B-gguf

### Performance Benchmarks

| Metric | Value | vs Qwen3 8B |
|--------|-------|-------------|
| **Avg Score** | 70.5 | -8.8 |
| **Intelligence Density** | 1.062 | 11× higher |
| **MMLU** | 69.2 | - |
| **HumanEval** | 38.5 | - |
| **GSM8K** | 58.1 | - |

### Deployment Command (Ollama)
```bash
# Download from HuggingFace first, then:
ollama create bonsai-8b-q1_0 -f Modelfile

# Modelfile content:
FROM ./bonsai-8b-q1_0.gguf
PARAMETER temperature 0.5
PARAMETER top_k 20
PARAMETER top_p 0.85
SYSTEM "You are a helpful AI assistant."
```

---

## 2. Ternary-Bonsai-8B (1.58-bit) - Q2_0 Format

### Model Information

| Property | Value |
|----------|-------|
| **Model ID** | Ternary-Bonsai-8B-Q2_0 |
| **Architecture** | Qwen3-8B based |
| **Quantization** | Q2_0 (ternary / 1.58-bit) |
| **Size** | 2.03 GB |
| **Parameters** | 8.06B |
| **Context length** | 65,536 tokens |
| **License** | Apache 2.0 |

### Status

| Aspect | Status |
|--------|--------|
| **HuggingFace Availability** | ✅ Available |
| **GGUF Download** | ✅ Yes |
| **Upstream llama.cpp** | ❌ **NOT MERGED** |
| **Ollama Compatible** | ❌ **NO (segfault)** |
| **Ready for Production** | ⚠️ **Requires Fork** |

### HuggingFace Location
- **Repository:** `prism-ml/Ternary-Bonsai-8B-gguf`
- **Files:** `Ternary-Bonsai-8B-q2_0.gguf`
- **URL:** https://huggingface.co/prism-ml/Ternary-Bonsai-8B-gguf

### Performance Benchmarks

| Metric | Value | vs Qwen3 8B | vs Bonsai-8B 1-bit |
|--------|-------|-------------|------------------|
| **Avg Score** | 75.5 | -3.8 | +5.0 |
| **Intelligence Density** | 0.645 | 6.7× higher | - |
| **MMLU** | 73.8 | - | +4.6 |
| **HumanEval** | 43.2 | - | +4.7 |
| **GSM8K** | 65.4 | - | +7.3 |

### Deployment Options

#### Option A: PrismML Fork (Recommended for Ternary)
```bash
# Clone PrismML fork with Q2_0 support
git clone -b prism https://github.com/PrismML-Eng/llama.cpp.git
cd llama.cpp

# Build with Metal (macOS) or CUDA (Linux)
cmake -B build -DGGML_METAL=ON
cmake --build build -j$(nproc)

# Run model
./build/bin/llama-cli \
  -m models/Ternary-Bonsai-8B-q2_0.gguf \
  -p "Your prompt here" \
  -n 256
```

#### Option B: Wait for Upstream
- PrismML states: "upstream PRs are coming next"
- No timeline specified
- Risk: May never merge

---

## 3. Ternary-Bonsai-8B-F16 (Source Weights)

### Model Information

| Property | Value |
|----------|-------|
| **Model ID** | Ternary-Bonsai-8B (FP16 source) |
| **Format** | PyTorch / HuggingFace native |
| **Purpose** | Source weights for conversion |
| **Size** | ~16 GB (FP16) |
| **Base Architecture** | Qwen3-8B |

### Status

| Aspect | Status |
|--------|--------|
| **HuggingFace Availability** | ✅ Available |
| **Format** | SafeTensors / PyTorch |
| **Quantized GGUF** | ✅ Available (Q2_0) |
| **1-bit Variant** | ❌ Not published |

### HuggingFace Location
- **Base Model:** `prism-ml/Ternary-Bonsai-8B`
- **URL:** https://huggingface.co/prism-ml/Ternary-Bonsai-8B

### Conversion Possibilities

#### Q2_0 → Q4_K_M (Theoretical)
```
Ternary (Q2_0) → Dequantize → FP16 → Quantize → Q4_K_M
```

**Challenges:**
- ❌ No standard tool exists for Q2_0 dequantization
- ❌ Custom decoder required
- ⚠️ Compound quality loss (ternary → FP16 → Q4)

#### Using Source Weights
If FP16 source is available:
```bash
# Use llama.cpp convert script
python convert_hf_to_gguf.py ./Ternary-Bonsai-8B \
  --outfile ternary-bonsai-8b-f16.gguf

# Then quantize to Q4_K_M
./llama-quantize \
  ternary-bonsai-8b-f16.gguf \
  ternary-bonsai-8b-q4_k_m.gguf \
  Q4_K_M
```

**Current Status:** ❌ Source weights are ternary-quantized, not FP16. The "FP16" source is actually the ternary model stored in HF format.

---

## 4. Complete Model Family Matrix

### 1-bit Bonsai Family (Q1_0)

| Model | Params | Size | Ollama Ready | Notes |
|-------|--------|------|--------------|-------|
| Bonsai-1.7B | 1.7B | ~0.24 GB | ✅ Yes | Smallest |
| Bonsai-4B | 4B | ~0.5 GB | ✅ Yes | Mid-size |
| **Bonsai-8B** | **8.06B** | **~1.15 GB** | **✅ Yes** | **Recommended** |

### Ternary Bonsai Family (Q2_0)

| Model | Params | Size | Ollama Ready | Notes |
|-------|--------|------|--------------|-------|
| Ternary-Bonsai-1.7B | 1.7B | ~0.5 GB | ❌ Fork required | Smallest ternary |
| Ternary-Bonsai-4B | 4B | ~1.0 GB | ❌ Fork required | Mid-size |
| **Ternary-Bonsai-8B** | **8.06B** | **2.03 GB** | **❌ Fork required** | **Best quality** |

---

## 5. Model Comparison Summary

### For Ollama Deployment (Stock)

| Model | Format | Size | Quality | Recommendation |
|-------|--------|------|---------|----------------|
| Bonsai-8B | Q1_0 | 1.15 GB | ⭐⭐⭐ | **Use this** |
| Qwen3:8b | Q4_K_M | 5.5 GB | ⭐⭐⭐⭐⭐ | Fallback option |
| Ternary-Bonsai-8B | Q2_0 | 2.03 GB | ⭐⭐⭐⭐ | ❌ Not compatible |

### For Custom Fork Deployment

| Model | Format | Size | Quality | Recommendation |
|-------|--------|------|---------|----------------|
| Ternary-Bonsai-8B | Q2_0 | 2.03 GB | ⭐⭐⭐⭐ | **Best quality** |
| Bonsai-8B | Q1_0 | 1.15 GB | ⭐⭐⭐ | Ultra-constrained |

---

## 6. Availability Quick Reference

### Download Links

| Model | HF Repository | Direct GGUF | MLX |
|-------|---------------|-------------|-----|
| Bonsai-8B (1-bit) | prism-ml/Bonsai-8B-gguf | ✅ | ✅ |
| Ternary-Bonsai-8B | prism-ml/Ternary-Bonsai-8B-gguf | ✅ | ✅ |
| Bonsai-4B | prism-ml/Bonsai-4B-gguf | ✅ | ✅ |
| Ternary-Bonsai-4B | prism-ml/Ternary-Bonsai-4B-gguf | ✅ | ✅ |
| Bonsai-1.7B | prism-ml/Bonsai-1.7B-gguf | ✅ | ✅ |
| Ternary-Bonsai-1.7B | prism-ml/Ternary-Bonsai-1.7B-gguf | ✅ | ✅ |

### MLX Format Availability

| Model | MLX Format | URL |
|-------|------------|-----|
| Ternary-Bonsai-8B | ✅ | `prism-ml/Ternary-Bonsai-8B-mlx` |
| All variants | ✅ | Check HF for `-mlx` suffix |

---

## 7. Key Findings from Research

### Critical Discovery
> "1-bit Bonsai (Q1_0) IS merged upstream. Ternary (Q2_0) requires PrismML fork."

### Why Ternary-Bonsai-8B Segfaults
- Ollama 0.18.0 uses standard llama.cpp
- Standard llama.cpp lacks Q2_0 kernel implementation
- GGUF loader doesn't recognize Q2_0 quantization type
- Result: Undefined behavior → segfault

### The Group Size Problem
- llama.cpp has TQ1_0/TQ2_0 formats
- BUT they use group size 256
- Bonsai uses group size 128
- Result: Incompatible, cannot reuse existing ternary kernels

---

## 8. Action Items

### Immediate
- [ ] Download Bonsai-8B-Q1_0 for Ollama testing
- [ ] Verify Q1_0 works in stock Ollama 0.18.0

### Short-term
- [ ] Build PrismML fork for Ternary-Bonsai testing
- [ ] Benchmark Q1_0 vs Ternary quality difference
- [ ] Evaluate if Q1_0 quality meets requirements

### Long-term
- [ ] Monitor PrismML fork for upstream PR
- [ ] Track llama.cpp releases for Q2_0 merge
- [ ] Consider custom conversion if tools emerge

---

## References

1. [PrismML Bonsai 8B](https://huggingface.co/prism-ml/Bonsai-8B-gguf)
2. [PrismML Ternary Bonsai 8B](https://huggingface.co/prism-ml/Ternary-Bonsai-8B-gguf)
3. [PrismML Fork](https://github.com/PrismML-Eng/llama.cpp)
4. [Bonsai Technical Report](https://github.com/PrismML-Eng/Bonsai-demo)

---

*Document: BQL-DOC-002 | Status: Complete | Classification: Lab Reference*