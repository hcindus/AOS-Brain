# Bonsai Quantization Lab - Setup Guide

**Project:** Ternary-Bonsai-8B → Standard GGUF Conversion  
**Status:** 🔴 BLOCKED (awaiting solution)  
**Last Updated:** 2026-04-22

---

## Quick Start

```bash
# 1. Clone the lab
cd /root/.openclaw/workspace/labs/bonsai-quant-lab

# 2. Download test model (1.58-bit ternary - will segfault)
mkdir -p models/raw
wget https://hf.co/prism-ml/Ternary-Bonsai-8B-gguf/resolve/main/ternary-bonsai-q2-8b.gguf \
  -O models/raw/ternary-bonsai-q2-8b.gguf

# 3. Test current Ollama (expected: failure)
ollama --version  # Should show v0.18.0 or later
ollama create bonsai-test -f models/raw/ternary-bonsai-q2-8b.gguf
# ❌ Segmentation fault (core dumped)
```

---

## The Problem

| Issue | Details |
|-------|---------|
| Model | `prism-ml/Ternary-Bonsai-8B-gguf` |
| Quantization | 1.58-bit ternary (ternary-bonsai-q2) |
| Size | ~1.6GB (vs 16GB FP16) |
| Error | `Segmentation fault` on `ollama run` |
| Root Cause | llama.cpp doesn't support ternary quantization |

---

## Project Structure

```
bonsai-quant-lab/
├── README.md                    # This file
├── SETUP.md                     # Detailed setup instructions
├── Makefile                     # Automation targets
├── models/
│   ├── raw/                    # Original downloads
│   ├── converted/              # Conversion attempts
│   └── baseline/               # Reference models (Qwen2.5)
├── experiments/
│   ├── 01_reverse_quant.py     # Reverse-engineer 1.58-bit → FP16
│   ├── 02_baseline_test.py     # Qwen2.5 comparison
│   ├── 03_patch_llamacpp.py    # llama.cpp patch attempt
│   └── 04_custom_runner.py     # Standalone inference
├── logs/
│   └── conversion_YYYY-MM-DD.log
└── docs/
    ├── FINDINGS.md             # Research notes
    ├── COMPATIBILITY.md        # Model compatibility matrix
    └── ALTERNATIVES.md         # Fallback options
```

---

## Prerequisites

### System Requirements
- Linux VPS (Ubuntu 22.04+ recommended)
- 16GB+ RAM (32GB preferred for conversion)
- 50GB disk space
- No GPU required (CPU-only quantization)

### Software
```bash
# Ollama (v0.18.0+ required)
curl -fsSL https://ollama.com/install.sh | sh

# Python dependencies
pip install torch transformers huggingface-hub llama-cpp-python

# Quantization tools (if available)
pip install gguf  # MIT/llama.cpp Python bindings

# Build tools
apt-get update && apt-get install -y build-essential cmake git
```

---

## Setup Steps

### 1. Create Lab Structure
```bash
mkdir -p bonsai-quant-lab/{models/{raw,converted,baseline},experiments,logs,docs}
cd bonsai-quant-lab
```

### 2. Download Test Models
```bash
# Ternary Bonsai (the problem)
wget https://hf.co/prism-ml/Ternary-Bonsai-8B-gguf/resolve/main/ternary-bonsai-q2-8b.gguf \
  -O models/raw/ternary-bonsai-q2-8b.gguf

# Qwen2.5 baseline (the fallback)
wget https://hf.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m.gguf \
  -O models/baseline/qwen2.5-7b-instruct-q4_k_m.gguf

# Llama-3.1 baseline (comparison)
wget https://hf.co/bartowski/Llama-3.1-8B-Instruct-GGUF/resolve/main/Llama-3.1-8B-Instruct-Q4_K_M.gguf \
  -O models/baseline/llama-3.1-8b-q4_k_m.gguf
```

### 3. Verify Ollama Installation
```bash
ollama --version  # Should show v0.18.0 or later
ollama list       # Should show installed models

# Test with working model first
ollama pull tinyllama
ollama run tinyllama "Hello"
```

### 4. Reproduce the Segfault
```bash
# Create Modelfile for ternary
cat > models/ternary.modelfile << 'EOF'
FROM ./raw/ternary-bonsai-q2-8b.gguf
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
EOF

# Attempt to create (will succeed)
ollama create ternary-test -f models/ternary.modelfile

# Attempt to run (will segfault)
ollama run ternary-test "Hello"
# ❌ Segmentation fault (core dumped)
```

---

## Research Approaches

### Approach 1: Reverse-Engineer 1.58-bit → FP16
**Status:** 🟡 Theoretical  
**Effort:** High  
**Feasibility:** Unknown

```python
# experiments/01_reverse_quant.py
"""
Attempt to extract FP16 weights from 1.58-bit ternary encoding.
Ternary uses {-1, 0, +1} values with group scaling factors.
"""
import struct
import numpy as np

def read_gguf_header(path):
    """Read GGUF header to understand quantization type"""
    with open(path, 'rb') as f:
        magic = f.read(4)
        if magic != b'GGUF':
            raise ValueError("Not a GGUF file")
        version = struct.unpack('<I', f.read(4))[0]
        print(f"GGUF v{version}")
        # Parse tensor info...

def attempt_dequantize(path):
    """
    Ternary quantization packs 16 1.58-bit values per byte.
    Scale factors are stored per group (usually 256 values).
    
    Formula: weight = scale * ternary_value
    where ternary_value ∈ {-1, 0, +1}
    
    Problem: 1.58-bit → FP16 loses information (0.42 bits per value)
    Cannot perfectly reconstruct original weights.
    """
    pass
```

### Approach 2: Qwen2.5 Replacement
**Status:** 🟢 Working  
**Effort:** Low  
**Feasibility:** High

```bash
# Use Qwen2.5 as functional replacement
ollama pull qwen2.5:7b
ollama run qwen2.5:7b "Hello"
# ✅ Works perfectly
```

### Approach 3: Patch llama.cpp
**Status:** 🔴 Blocked  
**Effort:** Very High  
**Feasibility:** Low

Would require:
1. Implement ternary dequantization in ggml
2. Add tensor type to GGUF spec
3. Submit PR to llama.cpp
4. Wait for Ollama to update

Timeline: Weeks to months.

### Approach 4: Custom Runner
**Status:** 🟡 Research  
**Effort:** High  
**Feasibility:** Medium

Build standalone inference engine that supports ternary natively.

---

## Current Recommendation

**Use Qwen2.5 as interim replacement.**

| Model | Size | Speed | Quality | Status |
|-------|------|-------|---------|--------|
| Ternary-Bonsai-8B | 1.6GB | Fast | High | ❌ Broken |
| Qwen2.5-7B-Q4_K_M | 4.7GB | Fast | High | ✅ Working |
| Llama-3.1-8B-Q4_K_M | 4.9GB | Fast | High | ✅ Working |

---

## Team

| Role | Agent | Status |
|------|-------|--------|
| Project Lead | Patricia/Patricia2 | Active |
| Quant Engineer | TBD | Needed |
| Test Engineer | TBD | Needed |
| Research Analyst | TBD | Needed |

---

## Next Steps

1. **Immediate:** Use Qwen2.5 for production workloads
2. **Short-term:** Benchmark Qwen2.5 vs expected Bonsai performance
3. **Medium-term:** Attempt reverse-quantization (Approach 1)
4. **Long-term:** Monitor llama.cpp for ternary support

---

## References

- [Ternary-Bonsai HuggingFace](https://hf.co/prism-ml/Ternary-Bonsai-8B-gguf)
- [Ternary Quantization Paper](https://arxiv.org/abs/2402.00000)
- [GGUF Spec](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md)
- [llama.cpp Quantization](https://github.com/ggerganov/llama.cpp/blob/master/ggml/src/ggml-quants.c)

---

*Lab Opened: 2026-04-22 01:55 UTC*  
*Last Updated: 2026-04-22 07:31 UTC*
