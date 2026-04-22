# Team Assignments — Bonsai Quantization Lab

## Project Oversight
**Lead:** Patricia/Patricia2  
**Role:** Architecture review, final decisions, cross-project coordination
**Scope:** All quantization experiments, fallback strategies

## Research Team

### Agent Alpha — Quant Engineer
**Status:** OPEN  
**Responsibility:** 
- Investigate GGUF conversion pipelines
- Test llama.cpp quantize scripts
- Document conversion failures

**Deliverables:**
- [ ] Attempt conversion from ternary → Q4_K_M
- [ ] Test with llama-quantize (llama.cpp)
- [ ] Report on precision loss

### Agent Beta — Integration Tester
**Status:** OPEN  
**Responsibility:**
- Ollama compatibility testing
- Benchmark decision latency
- Validate output quality

**Deliverables:**
- [ ] Load test converted models in Ollama
- [ ] Compare decision quality vs tinyllama
- [ ] Document memory/speed tradeoffs

### Agent Gamma — Research Analyst
**Status:** OPEN  
**Responsibility:**
- Evaluate alternative models
- Track llama.cpp/ollama upstream changes
- Assess Qwen3.5 viability as fallback

**Deliverables:**
- [ ] Benchmark Qwen3.5 vs tinyllama
- [ ] Monitor ternary support in llama.cpp
- [ ] Weekly research summary

## Task Board

| ID | Task | Owner | Priority | Status |
|----|------|-------|----------|--------|
| BQL-001 | Download Bonsai source weights | Alpha | HIGH | TODO |
| BQL-002 | Attempt de-ternary conversion | Alpha | HIGH | TODO |
| BQL-003 | Test Q4_K_M in Ollama | Beta | HIGH | TODO |
| BQL-004 | Benchmark Qwen3.5 fallback | Gamma | MED | TODO |
| BQL-005 | Research llama.cpp ternary support | Gamma | LOW | TODO |
| BQL-006 | Document findings for Patricia | All | MED | TODO |

## Meeting Cadence
- **Daily standup:** Async progress updates
- **Weekly review:** Patricia/Patricia2 oversight
- **Milestone:** Go/no-go on ternary conversion

## Success Criteria
1. ✅ Q4/Q8 GGUF loads without segfault
2. ✅ Decision quality matches or exceeds tinyllama
3. ✅ Latency under 2 seconds
4. ✅ Memory usage under 4GB

**Fallback:** Adopt Qwen3.5 as primary decision model

---
*Updated: 2026-04-22 01:55 UTC*
