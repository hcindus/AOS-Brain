# Agent Alpha — Quant Engineer
## Assignment: BQL-001 through BQL-003

**Agent ID:** Alpha  
**Specialty:** GGUF conversion, quantization pipelines  
**Reports to:** Patricia/Patricia2  

### Mission
Solve the ternary → standard quantization conversion problem.

### Tasks

#### BQL-001: Source Weight Investigation
- [ ] Check if prism-ml released FP16/BF16 source weights
- [ ] Examine HF repo: https://huggingface.co/prism-ml/Ternary-Bonsai-8B-gguf
- [ ] Contact model authors if needed
- [ ] Document weight availability status

#### BQL-002: De-ternary Conversion
**Hypothesis:** Can we approximate FP16 from 1.58-bit weights?

Approach:
```python
# Conceptual: Map ternary {-1, 0, +1} → approximate FP16
# Then quantize to Q4_K_M

import numpy as np

ternary_weights = load_gguf("ternary-bonsai-q2.gguf")
# Map: -1 → -scale, 0 → 0, +1 → +scale
scale = estimate_scale(ternary_weights)
approx_fp16 = ternary_weights.astype(np.float16) * scale

# Then standard quantization
quantize_to_q4_km(approx_fp16, output="bonsai-q4.gguf")
```

**Challenges:**
- Scale estimation per layer?
- Precision loss from ternary→FP16→Q4?
- llama.cpp quantization expects specific format

#### BQL-003: Alternative: Direct Ternary Runner
- [ ] Research if llama.cpp has experimental ternary support
- [ ] Check if custom runner can be built
- [ ] Document complexity vs benefit

### Deliverables
1. `report-001.md` — Weight availability findings
2. `report-002.md` — Conversion attempt results
3. `report-003.md` — Custom runner feasibility

### Weekly Standup
Report to Patricia/Patricia2 every Wednesday with:
- Progress on active task
- Blockers encountered
- Next week's plan

### Success Criteria
✅ Produce working Q4_K_M GGUF OR  
✅ Document why conversion is impossible OR  
✅ Propose viable alternative approach

---
*Assigned: 2026-04-22 01:57 UTC*
