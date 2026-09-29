# Model Budget — RESOLVED, follow-up for Jordan

**Status:** ✅ APPROVED (DeepSeek API available)
**Date:** 2026-09-29

## Resolution

The Q3 model budget is already approved. Captain confirmed:
> "Was already approved and we have Deepseek model api available."

Current available models:
- **DeepSeek API** (`deepseek-chat` / `deepseek-reasoner` — key in `/root/.deepseek_env`)
- **Ollama local** (deepseek-r1:7b, qwen3.5, qwen2.5:14b, gemma2:2b, tinyllama, nomic-embed-text, Mort_II, nous-hermes2)
- **Qwen vision** — `qwen3.5:latest` is multimodal (capabilities: completion · vision · tools · thinking) — the vision model is live

---

## ❓ Question for Jordan — what else do you need?

The budget is approved and DeepSeek is live. Please specify concretely:

1. **Which models/tasks** are still unserved by the current set? (e.g., a specific capability gap, a model you need for a task, higher throughput, longer context?)
2. **Any API spend** you need authorized (beyond the already-available DeepSeek key)?
3. **Any local model** you want pulled/loaded into Ollama that's currently missing?

If the current DeepSeek + Ollama set already covers your needs, we can formally **close** this line as resolved and stop re-flagging it in the standup.
