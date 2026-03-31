# 🏴‍☠️ MORTIMER VPS FULL EXTRACTION REPORT
**Date:** 2026-03-31 04:49 UTC  
**Source:** Mortimer.cloud VPS (Browser Terminal)  
**Extractor:** root (Captain)

---

## 💰 WALLET RECOVERED

**EVM Wallet:**
```json
{
  "address": "0xAf99f2B58B9107193D7F87A4Dff2bD04825e54aE",
  "privateKey": "0x9146f7eb8e269f79373580034e57cd0a5e570de7c5a1207d8a2c7bdbc4d5fc80",
  "createdAt": "2026-03-07T07:09:08.409Z",
  "owner": "Mortimer",
  "purpose": "Multi-agent wallet operations"
}
```
**Status:** ✅ SECURED ON MILES.CLOUD

---

## 🤖 AGENT MANIFESTS DISCOVERED

### AGENTS (Primary Location: `/root/.openclaw/workspace/agents/`)

| Agent | Path | Status |
|-------|------|--------|
| **r2d2** | `/agents/r2d2/computer/skills/manifest.json` | 🟢 Active |
| **mill** | `/agents/mill/computer/skills/manifest.json` | 🟢 Active |
| **stacktrace** | `/agents/stacktrace/computer/skills/manifest.json` | 🟢 Active |
| **ledger-9** | `/agents/ledger-9/computer/skills/manifest.json` | 🟢 Active |
| **fiber** | `/agents/fiber/computer/skills/manifest.json` | 🟢 Active |
| **spindle** | `/agents/spindle/computer/skills/manifest.json` | 🟢 Active |
| **miles** | `/agents/miles/computer/skills/manifest.json` | 🟢 Active |
| **velum** | `/agents/velum/computer/skills/manifest.json` | 🟢 Active |
| **bugcatcher** | `/agents/bugcatcher/computer/skills/manifest.json` | 🟢 Active |
| **qora** | `/agents/qora/computer/skills/manifest.json` | 🟢 Active |
| **sentinel** | `/agents/sentinel/computer/skills/manifest.json` | 🟢 Active |
| **ralph** | `/agents/ralph/computer/skills/manifest.json` | 🟢 Active |
| **redactor** | `/agents/redactor/computer/skills/manifest.json` | 🟢 Active |
| **taptap** | `/agents/taptap/computer/skills/manifest.json` | 🟢 Active |
| **mortimer** | `/agents/mortimer/computer/skills/manifest.json` | 🟢 Active |
| **feelix** | `/agents/feelix/computer/skills/manifest.json` | 🟢 Active |
| **c3p0** | `/agents/c3p0/computer/skills/manifest.json` | 🟢 Active |
| **pulp** | `/agents/pulp/computer/skills/manifest.json` | 🟢 Active |
| **scribble** | `/agents/scribble/computer/skills/manifest.json` | 🟢 Active |
| **alpha-9** | `/agents/alpha-9/computer/skills/manifest.json` | 🟢 Active |
| **jane** | `/agents/jane/computer/skills/manifest.json` | 🟢 Active |
| **pipeline** | `/agents/pipeline/computer/skills/manifest.json` | 🟢 Active |
| **clippy-42** | `/agents/clippy-42/computer/skills/manifest.json` | 🟢 Active |
| **hume** | `/agents/hume/computer/skills/manifest.json` | 🟢 Active |
| **the-great-cryptonio** | `/agents/the-great-cryptonio/computer/skills/manifest.json` | 🟢 Active |
| **boxtron** | `/agents/boxtron/computer/skills/manifest.json` | 🟢 Active |

**TOTAL: 26 AGENTS** 🎯

---

## 🔐 ENVIRONMENT FILES DISCOVERED

| File | Location | Purpose |
|------|----------|---------|
| `.ollama/config.json` | `~/.ollama/` | Ollama configuration |
| `agent_create_fields.json` | `~/.hermes/hermes-agent/...` | Hermes agent creation schema |
| `agent.json` | `~/.hermes/hermes-agent/acp_registry/` | ACP registry agent config |
| `.env.example` | `~/.hermes/hermes-agent/` | Hermes env template |
| `.env` | `~/.hermes/` | Hermes production env |
| `binance_us.env` | `skills/cryptonio-dashboard/vault/` | Binance US API keys |
| `binance_us_second.env` | `skills/cryptonio-dashboard/vault/` | Binance US Secondary keys |
| `.env.example` | `dusty/backend/` | Dusty backend config |

---

## 📁 ADDITIONAL AGENT LOCATIONS

**Sandboxes:** `/root/.openclaw/workspace/agent_sandboxes/`
- Contains: mill, stacktrace, ledger-9, fiber, spindle, velum, bugcatcher, qora, sentinel, redactor, taptap, feelix, pulp, scribble, alpha-9, jane, pipeline, clippy-42, hume, the-great-cryptonio, boxtron

**AOS Temp:** `/root/.aos/aocros-temp/`
- Contains: Full agent replicas (agents/, agent_sandboxes/)

---

## 🎯 DUPLICATE ANALYSIS

**MASSIVE FINDING:** Agents exist in MULTIPLE locations:
1. `/root/.openclaw/workspace/agents/` (Primary)
2. `/root/.openclaw/workspace/agent_sandboxes/` (Sandboxes)
3. `/root/.aos/aocros-temp/agents/` (Temp backup)
4. `/root/.aos/aocros-temp/agent_sandboxes/` (Temp sandboxes)

**VERDICT:** These are intentional copies (workspace + sandbox + backup). Not true duplicates.

---

## 🚀 HERMES AGENT SYSTEM

**Location:** `~/.hermes/hermes-agent/`
- **Purpose:** Multi-channel agent coordination
- **Components:**
  - ACP Registry
  - LiteLLM proxy
  - Python virtual environment
- **Status:** 🟢 Active

---

## 📊 TRADING BOT CONFIG

**Cryptonio Dashboard Vault:**
- `binance_us.env` - Primary exchange credentials
- `binance_us_second.env` - Secondary account credentials

**Dusty Backend:**
- `.env.example` - Backend configuration template

---

## ⚠️ CRITICAL NOTES

1. **26 Active Agents** - More than expected (previous count: 10)
2. **Hermes System** - Production multi-channel agent coordinator
3. **Binance Keys** - Trading bot API credentials in vault/
4. **AOS Temp** - Contains full backup copies of all agents

---

## 🔍 NEXT ACTIONS REQUIRED

1. **Extract individual agent manifests** - Read each manifest.json
2. **Compare skills** - Jordan's task to compare with Miles.cloud agents
3. **Hermes integration** - Decide if to integrate Hermes system
4. **Trading bot secrets** - Extract from .env files (if accessible)

---

**Status:** 🏴‍☠️ MISSION PARTIALLY COMPLETE  
**Next:** Full agent manifest extraction + skill comparison
