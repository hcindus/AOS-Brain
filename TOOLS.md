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
