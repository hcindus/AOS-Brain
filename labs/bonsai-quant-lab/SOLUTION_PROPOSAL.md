# SOLUTION PROPOSAL — Bonsai Integration

## Executive Summary

**Problem:** Ollama 0.18.0 lacks Q1_0 and Q2_0 tensor support despite format recognition.
**Root Cause:** Ollama bundles llama.cpp — it's behind upstream.
**Solution:** Use PrismML fork directly or patch Ollama.

---

## Option 1: Use PrismML Fork (RECOMMENDED — Immediate)

**Status:** ✅ Already working on your system

```bash
# PrismML fork is already built at:
/tmp/prism-llama.cpp/build/bin/llama-cli

# Working command:
/tmp/prism-llama.cpp/build/bin/llama-cli \
  -m /root/Ternary-Bonsai-8B-Q2_0.gguf \
  -p "Your prompt" \
  -n 100 \
  --temp 0.7
```

**Pros:**
- ✅ Works today
- ✅ Supports both Q1_0 and Q2_0
- ✅ No Ollama modifications needed

**Cons:**
- ❌ Different API (not Ollama-compatible)
- ❌ Requires wrapper for Brain integration

---

## Option 2: Build Ollama with PrismML llama.cpp

**Steps:**
```bash
# 1. Clone Ollama
git clone https://github.com/ollama/ollama.git
cd ollama

# 2. Replace llama.cpp submodule with PrismML fork
git submodule deinit llm/llama.cpp
rm -rf .git/modules/llm/llama.cpp
rm -rf llm/llama.cpp
git submodule add -b prism https://github.com/PrismML-Eng/llama.cpp.git llm/llama.cpp

# 3. Build Ollama from source
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build

# 4. Install
sudo cp build/ollama /usr/local/bin/ollama
```

**Pros:**
- ✅ Full Ollama API with Bonsai support
- ✅ Single binary solution

**Cons:**
- ⚠️ Complex build process
- ⚠️ May break other models
- ⚠️ Maintenance burden

---

## Option 3: Create Ollama-Compatible Wrapper

**Architecture:**
```
Brain → Ollama API → Wrapper → PrismML llama-cli → Bonsai
                    ↓
              Other models → Standard Ollama
```

**Implementation:**
```python
# /root/.openclaw/workspace/labs/bonsai-quant-lab/ollama_bonsai_bridge.py

import subprocess
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class BonsaiBridgeHandler(BaseHTTPRequestHandler):
    def do_post(self):
        if '/api/generate' in self.path:
            data = json.loads(self.rfile.read())
            model = data['model']
            prompt = data['prompt']
            
            if 'bonsai' in model.lower():
                # Use PrismML fork
                result = subprocess.run([
                    '/tmp/prism-llama.cpp/build/bin/llama-cli',
                    '-m', f'/root/{model}.gguf',
                    '-p', prompt,
                    '-n', str(data.get('options', {}).get('num_predict', 100)),
                    '--temp', str(data.get('options', {}).get('temperature', 0.7)),
                    '--no-display-prompt'
                ], capture_output=True, text=True)
                response = result.stdout
            else:
                # Forward to real Ollama
                ...
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"response": response}).encode())

# Run on port 11435, configure Brain to use this instead
```

**Pros:**
- ✅ Clean separation
- ✅ No Ollama modification
- ✅ Can add special handling

**Cons:**
- ⚠️ More components to maintain
- ⚠️ Latency overhead

---

## Option 4: Wait for Official Ollama Update

**Timeline:** Unknown

**Monitoring:**
- Watch: https://github.com/ollama/ollama/releases
- Check for: "Added Q1_0/Q2_0 support" or "Updated llama.cpp"

**Pros:**
- ✅ Zero effort
- ✅ Official support

**Cons:**
- ❌ Timeline unknown
- ❌ May never happen (PrismML formats are niche)

---

## Recommendation

**IMMEDIATE (Today):**
Use Option 1 — PrismML fork is already working. Create a simple wrapper script for Brain integration.

**SHORT-TERM (This Week):**
Implement Option 3 — Ollama-compatible bridge. This gives you:
- Clean API for Brain
- Fallback to standard Ollama for other models
- No build complexity

**LONG-TERM:**
Monitor Option 4. If Ollama updates with native support, migrate away from bridge.

---

## Test Results Summary

| Model | Format | Ollama 0.18.0 | PrismML Fork | Status |
|-------|--------|---------------|--------------|--------|
| tinyllama | Q4 | ✅ Works | ✅ Works | Ready |
| qwen3.5 | Q4_K_M | ✅ Works | ✅ Works | Ready |
| Bonsai-8B | Q1_0 | ❌ GGML_ASSERT | ✅ Works | Needs bridge |
| Ternary-Bonsai-8B | Q2_0 | ❌ Segfault | ✅ Works | Needs bridge |

---

*Analysis complete: 2026-04-22 02:20 UTC*
