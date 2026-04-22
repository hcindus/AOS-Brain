# Bonsai Quantization Lab
**Project Lead:** Patricia/Patricia2 (Oversight)  
**Lab:** Factory Research Division  
**Objective:** Solve Ternary-Bonsai Q2 → Standard Q4/Q8 quantization for Ollama compatibility

## The Problem
- `ternary-bonsai-q2:8b` (1.58-bit weights) segfaults in Ollama 0.18.0
- Root cause: Ternary quantization is not supported in standard llama.cpp
- Need: Convert to standard GGUF (Q4_K_M, Q8_0) without original FP16 weights

## Lab Structure

### /experiments/
Active quantization experiments and test scripts

### /models/
Downloaded model files, converted GGUFs, test builds

### /logs/
Conversion logs, test results, benchmark data

### /team/
Agent assignments, task tracking, progress reports

### /docs/
Research notes, compatibility matrices, findings

## Team Assignments

| Agent | Role | Focus |
|-------|------|-------|
| Patricia/Patricia2 | Project Lead | Oversight, architecture decisions |
| TBD | Quant Engineer | GGUF conversion pipeline |
| TBD | Test Engineer | Ollama integration testing |
| TBD | Research Analyst | Alternative model evaluation |

## Current Status
🔴 **BLOCKED** — Awaiting source weights or alternative approach

## Possible Approaches

1. **Reverse-engineer 1.58-bit → FP16** (ambitious)
2. **Use Qwen3.5 as Bonsai replacement** (fallback)
3. **Patch llama.cpp for ternary support** (upstream contribution)
4. **Build custom runner** (isolated)

## Resources
- Original Model: `hf.co/prism-ml/Ternary-Bonsai-8B-gguf`
- Current Ollama: v0.18.0
- Target Quant: Q4_K_M or Q8_0
- Test System: Miles VPS (15GB RAM, no GPU)

---
*Lab opened: 2026-04-22 01:55 UTC*
