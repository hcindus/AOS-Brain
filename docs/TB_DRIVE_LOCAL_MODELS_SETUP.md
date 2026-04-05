# TB DRIVE SETUP - LOCAL MODELS FOR HERMES/OPENCLAW/PI
**Source:** Email from Captain (April 4, 2026)  
**Purpose:** Run local models on 1TB drive  
**Status:** EXTRACTED AND READY

---

## EMAIL CONTENT EXTRACTED

### 1. HERMES LOCAL SETUP

**Framework:** Agent framework (not a model)  
**Supports:** Ollama, LM Studio, OpenAI-compatible servers

**Recommended: LM Studio**
1. Install LM Studio (Windows/Linux/Mac)
2. Download model (Qwen, Llama, DeepSeek)
3. Start local server (default: http://127.0.0.1:1234/v1)
4. Hermes config:
```yaml
model:
  primary: "lmstudio/my-local-model"
providers:
  lmstudio:
    baseUrl: "http://127.0.0.1:1234/v1"
    apiKey: "lmstudio"
```

---

### 2. OPENCLAW LOCAL MODELS

**Lightweight:** OpenClaw itself is lightweight  
**Backends Supported:**
- Ollama (easiest)
- LM Studio (best for large models)
- Custom OpenAI-compatible (vLLM, llama.cpp)

**Requirements:**
- 32K-65K context
- Stable tool-calling
- Large KV cache

**Steps:**
```bash
# 1. Install OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard

# 2. Install LM Studio and load model
# 3. Enable LM Studio local server
# 4. Configure OpenClaw to use local endpoint
```

---

## KEY INSIGHT

**TB Drive Use:** Store local models on 1TB drive, run inference locally on AspireOne or other hardware.

**Models to Download:**
- Qwen 32B
- DeepSeek
- Llama 3
- Hermes models

**Benefits:**
- No cloud dependency
- Full privacy
- Cost savings
- Works offline

---

**Document ID:** TB-DRIVE-LOCAL-MODELS-2026-04-05  
**Extracted From:** Email 407 "Re: TB"  
**Status:** Ready for implementation