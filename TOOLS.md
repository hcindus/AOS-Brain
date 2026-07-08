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
