### TTS
- Preferred voice: "Adam" (deep, energetic, professional, consultative—perfect for a sales agent).
- Default provider: ElevenLabs

### Backup Models
- Primary: `ollama/antoniohudnall/Mort_II:latest`
- Fallback 1: `google/gemini-3.1-pro-preview`
- Fallback 2: `ollama/minimax.cloud`
- Fallback 3: `ollama/kimi2.5.cloud`

### Crypto/Trading
- Portfolio Manager: Linked to `hcindus/the-great-cryptonio-active` and the Binance API endpoints in `aocros`.

### DeepSeek API
- **API Key:** Stored in `/root/.deepseek_env`
- **Base URL:** https://api.deepseek.com
- **Models:** deepseek-chat (V3), deepseek-reasoner (R1)
- **Load:** `source /root/.deepseek_env`

### Jordan's Local Models
| Model | Size | Best For | Command |
|-------|------|----------|---------|
| **Qwen2.5:14b** | 9GB | Coding, reasoning, text | `ollama run qwen2.5:14b` |
| **Qwen3.5** | 6.6GB | Vision + text (multimodal) | `ollama run qwen3.5` |
| Llama3.1 | 4.9GB | General purpose | `ollama run llama3.1` |
| Mistral | 4.4GB | Fast responses | `ollama run mistral` |

### AGI Company Model Registry (v2026-07-23)
**Updated:** 2026-07-23 23:09 UTC

| Model | Status | Size | Best For | Assigned Agents |
|-------|--------|------|----------|-----------------|
| `qwen3.5:latest` | ✅ Active | 6.6GB | Vision + text, multimodal | Forge (infrastructure), Pixel (web) |
| `gemma2:2b` | ✅ Active | 1.6GB | Fast inference, lightweight | GREET (front desk), Clerk (documentation) |
| `nous-hermes2:latest` | ✅ Active | 6.1GB | General purpose, roleplay | Jane (sales), Hume (regional) |
| `antoniohudnall/Mort_II:latest` | ✅ Active | 2.0GB | Sales, voice, consultative | Miles (sales consultant) |
| `qwen2.5:14b` | ✅ Active | 9.0GB | Deep reasoning, coding | Dusty (research), Stacktrace (debugging) |
| `tinyllama:latest` | ✅ Active | 637MB | Fast decisions, routing | Spindle (scheduler), TAPTAP (reviewer) |
| `nomic-embed-text:latest` | ✅ Active | 274MB | Embeddings, search | QORA (query optimization) |

### Model Assignment Matrix

**C-Suite Models:**
- **Patricia:** Cloud-routed (current) with local `gemma2:2b` fallback
- **Chelios:** `qwen2.5:14b` (security analysis)
- **Sentinel:** `nous-hermes2` (threat detection)
- **Dusty:** `qwen2.5:14b` (deep research)
- **Pulp:** `nous-hermes2` (sales strategy)
- **Forge:** `qwen3.5` (infrastructure + vision)
- **Aurora:** `qwen3.5` (design + multimodal)

**Sales Team Models:**
- **Jane:** `nous-hermes2` (enterprise sales)
- **Hume:** `nous-hermes2` (regional management)
- **Clippy-42:** `gemma2:2b` (assistant tasks)
- **Jordan:** `qwen3.5` (operations analysis)
- **GREET:** `gemma2:2b` (24/7 fast response)
- **CLOSETER:** `nous-hermes2` (conversion optimization)

**Technical Models:**
- **Pipeline:** `qwen2.5:14b` (CI/CD automation)
- **TAPTAP:** `tinyllama` (quick code review)
- **BUGCATCHER:** `qwen2.5:14b` (deep debugging)
- **Spindle:** `tinyllama` (fast scheduling)
- **Stacktrace:** `qwen2.5:14b` (error analysis)
- **Pixel:** `qwen3.5` (web dev + vision)
- **Harper:** `qwen2.5:14b` (systems analysis)
- **Mill:** `qwen3.5` (process optimization)
- **Boxtron:** `tinyllama` (package management)

**Creative Models:**
- **Blender-Expert:** `qwen3.5` (3D + vision)
- **Unity-Expert:** `qwen3.5` (game dev)
- **Unreal-Expert:** `qwen3.5` (game dev)
- **SFX:** `qwen3.5` (audio design)
- **Scribble:** `nous-hermes2` (concept art direction)
- **Feelix:** `nous-hermes2` (emotional UX)

**Myl Family Models:**
- All 7 children: `gemma2:2b` (efficient for teaching)

**Finance Models:**
- **Cryptonio:** `qwen2.5:14b` (trading analysis)
- **Ledger:** `gemma2:2b` (bookkeeping)
- **Ledger-9:** `qwen2.5:14b` (complex accounting)
- **Redactor:** `qwen2.5:14b` (compliance analysis)
- **Velum:** `nous-hermes2` (privacy/GDPR)

**Specialized Models:**
- **Miles:** `antoniohudnall/Mort_II:latest` (voice/sales)
- **Milkman:** `gemma2:2b` (logistics)
- **R2-C4:** `tinyllama` (calculator)
- **QORA:** `nomic-embed-text:latest` (embeddings)
- **Fiber:** `qwen3.5` (network engineering)
- **Mortimer:** `antoniohudnall/Mort_II:latest` (model hosting)

### Cloud API Models (External Access)
- **minimax-m2.5:cloud** - High-performance Chinese LLM (API key required)
- **kimi-k2.5:cloud** - Long context model (API key required)
- **gemini-3.1-pro-preview** - Google multimodal (API key in `.env`)

### Model Selection Guidelines
1. **Vision tasks:** Always use `qwen3.5`
2. **Fast responses:** Use `gemma2:2b` or `tinyllama`
3. **Deep reasoning:** Use `qwen2.5:14b`
4. **Sales/voice:** Use `Mort_II`
5. **Embeddings:** Use `nomic-embed-text`
6. **General purpose:** Use `nous-hermes2`
