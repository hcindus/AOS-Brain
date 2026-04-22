# Ollama Compatibility Matrix
## Bonsai Quantization Lab Documentation

**Purpose:** Track Ollama version support for quantization formats

---

## Ollama Version History (Relevant)

| Version | Release | Key Quant Changes |
|---------|---------|-------------------|
| 0.18.0 | Current (Lab) | Base reference |
| 0.17.x | Previous | Same quant support |
| 0.16.x | Legacy | Same quant support |

---

## Quantization Support Matrix (Ollama 0.18.0)

Based on llama.cpp v0.0.x (bundled with Ollama)

| Format | Status | Notes |
|--------|--------|-------|
| **F16** | ✅ Supported | Full precision |
| **F32** | ✅ Supported | Training format |
| **Q8_0** | ✅ Supported | High quality |
| **Q6_K** | ✅ Supported | Good quality |
| **Q5_K_M** | ✅ Supported | Recommended |
| **Q5_K_S** | ✅ Supported | Balanced |
| **Q4_K_M** | ✅ Supported | **Best default** |
| **Q4_K_S** | ✅ Supported | Balanced |
| **Q4_0** | ✅ Supported | Legacy compatible |
| **Q3_K_M** | ✅ Supported | Smaller, some loss |
| **Q3_K_S** | ✅ Supported | Smaller, some loss |
| **Q2_K** | ✅ Supported | Smallest standard |
| **IQ4_XS** | ✅ Supported | Importance matrix |
| **IQ3_XXS** | ⚠️ May work | Experimental |
| **Q2_0** | ❌ **NOT SUPPORTED** | Ternary format |
| **i2_s** | ❌ **NOT SUPPORTED** | BitNet format |
| **tl1/tl2** | ❌ **NOT SUPPORTED** | BitNet lookup |

---

## Model Compatibility Test Results

### Known Working (Ollama 0.18.0)

| Model | Format | Source | Status |
|-------|--------|--------|--------|
| qwen3:8b | Q4_K_M | Ollama Hub | ✅ Works |
| qwen3:4b | Q4_K_M | Ollama Hub | ✅ Works |
| qwen3:1.7b | Q4_K_M | Ollama Hub | ✅ Works |
| llama3.2 | Q4_K_M | Ollama Hub | ✅ Works |
| phi4 | Q4_K_M | Ollama Hub | ✅ Works |

### Known NOT Working (Ollama 0.18.0)

| Model | Format | Source | Status |
|-------|--------|--------|--------|
| Ternary-Bonsai-8B | Q2_0 | PrismML HF | ❌ Segfault |

**Root Cause:** Ollama's llama.cpp lacks Q2_0 kernel implementation

---

## GGUF Format Detection

Ollama detects format from GGUF metadata:

```
GGUF Version: 3 (latest)
Tensor Count: [number]
Metadata KV pairs: [number]
General.architecture: qwen
General.quantization_version: 2 (for Q2_0 - unknown to Ollama)
```

Unknown quantization versions cause undefined behavior.

---

## Creating Ollama-Compatible Models

### From HuggingFace (Standard Flow)

```bash
# 1. Download FP16
huggingface-cli download model-id --local-dir ./model

# 2. Convert to GGUF (requires llama.cpp convert script)
python convert_hf_to_gguf.py ./model --outfile model-f16.gguf

# 3. Quantize to Ollama-compatible format
./llama-quantize model-f16.gguf model-q4_k_m.gguf Q4_K_M

# 4. Create Ollama Modelfile
ollama create my-model -f Modelfile
```

### Modelfile Template

```dockerfile
FROM ./model-q4_k_m.gguf

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40

SYSTEM """You are a helpful assistant."""
```

---

## Ternary → Ollama Conversion (Not Currently Possible)

### The Problem

```
Ternary Bonsai (Q2_0) ──❌──→ Ollama
         │
         ├── Requires: Q2_0 dequant kernel
         ├── Missing from: llama.cpp mainline
         └── Solution: Unknown
```

### Potential Solutions

| Solution | Feasibility | Effort | Timeline |
|----------|-------------|--------|----------|
| Wait for upstream | Medium | None | Unknown |
| Use PrismML fork | High | Medium | Now |
| Dequantize to FP16 | Medium | High | Weeks |
| Custom Ollama build | Medium | High | Weeks |

---

## Monitoring Checklist

**Check on each Ollama release:**

- [ ] New quantization types added?
- [ ] llama.cpp version bump?
- [ ] Q2_0 or ternary mentioned?
- [ ] GGUF spec changes?

**Sources:**
- https://github.com/ollama/ollama/releases
- https://ollama.com/blog
- https://github.com/ggml-org/llama.cpp/releases

---

## Troubleshooting Unknown Quant Formats

### Symptom: Segfault on model load

**Likely Cause:** Unknown quantization type in GGUF

**Diagnostic:**
```bash
# Check GGUF metadata
python -c "from gguf import GGUFReader; r = GGUFReader('model.gguf'); print(r.fields)"
```

**Look for:**
- `general.quantization_version` = unusual value
- `general.file_type` = unrecognized enum

### Solutions

1. **Use known working quant:** Q4_K_M, Q8_0
2. **Check model source:** Verify format compatibility
3. **Update Ollama:** Newer versions may add support
4. **Use alternative tool:** llama.cpp CLI, bitnet.cpp

---

## Version Compatibility Notes

### Ollama 0.18.0 Bundled Components

| Component | Version | Notes |
|-----------|---------|-------|
| llama.cpp | v0.0.x | Specific commit bundled |
| GGUF spec | v3 | Latest standard |
| CUDA support | Optional | Requires GPU build |
| Metal support | Optional | macOS only |

### Upgrading Ollama

```bash
# Check current version
ollama --version

# Update (varies by platform)
# Linux: curl -fsSL https://ollama.com/install.sh | sh
# macOS: brew upgrade ollama
# Windows: Download new installer

# Verify after upgrade
ollama --version
ollama list  # Check models still work
```

---

## References

- [Ollama Releases](https://github.com/ollama/ollama/releases)
- [Ollama Documentation](https://github.com/ollama/ollama/blob/main/docs/README.md)
- [GGUF Spec v3](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)
- [llama.cpp Quantization](https://github.com/ggml-org/llama.cpp/blob/master/examples/quantize/README.md)

---

*Document: BQL-008.3 | Status: Draft | Updated: 2026-04-22*
