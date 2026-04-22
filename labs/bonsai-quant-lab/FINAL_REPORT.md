# Bonsai Quantization Lab - v1.1 Release

## Summary
Successfully integrated 1-bit Bonsai (Q1_0) as Brain's decision model via Ollama-Bonsai Bridge.

## Changes

### 1. Ollama-Bonsai Bridge (NEW)
- **File:** `labs/bonsai-quant-lab/ollama_bonsai_bridge.py`
- **Port:** 11435
- **Function:** Routes Bonsai models to PrismML fork, others to standard Ollama
- **Service:** `/etc/systemd/system/ollama-bonsai-bridge.service`

### 2. Model Router v1.1 (UPDATED)
- **File:** `/root/.aos/aos/model_router.py`
- **Decision Model:** `bonsai-8b-q1_0` (via bridge)
- **Fallback:** `tinyllama:latest`
- **Endpoint:** Port 11435

### 3. Brain Monitor Page (UPDATED)
- **File:** `brain.html`
- **Changes:**
  - Added Brain v4.5 Pipeline visualization (Lungs → Liver → Brain → Kidneys)
  - Live metrics from Mission Control API
  - Real-time tick, phase, thyroid state

### 4. Documentation (NEW)
- `labs/bonsai-quant-lab/docs/quantization-types.md`
- `labs/bonsai-quant-lab/docs/bonsai-model-matrix.md`
- `labs/bonsai-quant-lab/docs/prismml-intelligence.md`
- `labs/bonsai-quant-lab/SOLUTION_PROPOSAL.md`

## Technical Details

### Why This Works
- Ollama 0.18.0 lacks Q1_0/Q2_0 tensor support
- PrismML fork has working Q1_0/Q2_0 kernels
- Bridge acts as intelligent router between APIs

### Performance
- 1-bit Bonsai: 1.1GB, 70.5 benchmark score
- Latency: ~3-5s first load, then cached
- Memory: ~10GB resident

### Team
- Patricia/Patricia2: Project oversight
- Agent Alpha: Quant Engineer
- Agent Beta: Integration Tester
- Agent Gamma: Research Analyst

## Testing
- ✅ Bridge operational on port 11435
- ✅ Brain v4.5 restarted with new router
- ✅ Curriculum fed successfully
- ✅ First TracRay episode recorded

## Deployment
```bash
systemctl enable ollama-bonsai-bridge
systemctl restart aos-brain-v4
```

---
Deployed: 2026-04-22 02:33 UTC
