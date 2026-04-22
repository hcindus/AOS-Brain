# Agent Gamma — Research Analyst
## Assignment: BQL-006 through BQL-008

**Agent ID:** Gamma  
**Specialty:** Upstream monitoring, technical research, documentation  
**Reports to:** Patricia/Patricia2  

### Mission
Track ternary quantization ecosystem and document all findings.

### Tasks

#### BQL-006: llama.cpp Ternary Support Tracking

**Monitoring Targets:**
- [ ] GitHub: ggerganov/llama.cpp — issues mentioning "ternary", "1.58-bit", "BitNet"
- [ ] GitHub: ollama/ollama — PRs mentioning quantization support
- [ ] arXiv: Papers citing BitNet b1.58

**Key Questions:**
1. Is ternary support on llama.cpp roadmap?
2. Any experimental branches with ternary kernels?
3. Estimated timeline for mainstream support?

**Deliverable:** `ternary-roadmap-report.md` updated weekly

#### BQL-007: Alternative Model Research

**Research Targets:**
- [ ] Other Qwen3-based models (32B, 72B variants)
- [ ] Other ternary models (if any)
- [ ] Models with native ternary → Q4 conversion tools

**Key Question:**  
Is Bonsai unique, or are there drop-in alternatives?

**Deliverable:** `alternative-models-landscape.md`

#### BQL-008: Knowledge Base Documentation

**Create Comprehensive Docs:**
- [ ] `quantization-types.md` — Q2 vs Q4 vs Q8 vs ternary
- [ ] `gguf-format-guide.md` — Internal structure
- [ ] `ollama-compatibility-matrix.md` — Version vs quant support
- [ ] `troubleshooting-guide.md` — Common conversion failures

### Weekly Research Summary
Every Friday, post to lab channel:
```
# Research Update — Week of YYYY-MM-DD

## llama.cpp upstream
- [What changed this week]

## Ollama releases
- [Any new versions, features]

## Community developments
- [Discussions, papers, tools]

## Action items for next week
- [What Gamma will investigate]
```

### Success Criteria
✅ Patricia/Patricia2 never surprised by upstream changes  
✅ Lab has definitive reference documentation  
✅ Alternative options documented before needed

---
*Assigned: 2026-04-22 01:57 UTC*
