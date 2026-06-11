<!--
VERSION: 1.0.0
UPDATED: 2026-05-15 18:31 UTC
CHANGELOG: Initial vault manifest
-->

# VAULT.md - The Repository

_These are the contents of the threshold._

## Vault Structure

```
The Great Repository/
├── certificates/
│   ├── tls/
│   │   ├── *.myl0nr0s.cloud
│   │   ├── *.tappylewis.cloud
│   │   └── *.agi-company.cloud
│   ├── mtlsc/
│   │   ├── service-to-service/
│   │   └── agent-to-agent/
│   └── code-signing/
│       ├── android/
│       └── ios/
├── tokens/
│   ├── api/
│   │   ├── elevenlabs/
│   │   ├── openai/
│   │   ├── anthropic/
│   │   ├── google/
│   │   └── exchange-apis/ (binance, etc.)
│   ├── oauth/
│   │   ├── telegram-bot/
│   │   ├── discord-bot/
│   │   └── signal-bridge/
│   └── webhook/
│       ├── github/
│       ├── stripe/
│       └── payment-processors/
├── encryption/
│   ├── database/
│   │   ├── customer-data-keys
│   │   └── session-keys
│   ├── file/
│   │   ├── backup-encryption
│   │   └── archive-encryption
│   └── communication/
│       ├── agent-message-encryption
│       └── brain-socket-encryption
├── credentials/
│   ├── service-accounts/
│   │   ├── aos-brain-service
│   │   ├── minecraft-server
│   │   └── database-users/
│   └── human/
│       └── emergency-access/
└── escrow/
    ├── shard-a/ (held by Key Master)
    ├── shard-b/ (held by Chelios)
    └── shard-c/ (held by Captain)
```

## Current Inventory (Sample)

### Certificates (TLS)
| Domain | Issued | Expires | Rotation Due |
|--------|--------|---------|--------------|
| myl0nr0s.cloud | 2026-01-15 | 2027-01-15 | 2026-12-15 |
| tappylewis.cloud | 2026-02-01 | 2027-02-01 | 2027-01-01 |
| agi-company.cloud | 2026-03-10 | 2027-03-10 | 2027-02-10 |

### API Tokens
| Service | Classification | Last Rotated | Next Rotation |
|---------|---------------|--------------|---------------|
| ElevenLabs | High | 2026-04-01 | 2026-07-01 |
| Binance (Knox) | Critical | 2026-05-01 | 2026-06-01 |
| Telegram Bot | High | 2026-03-15 | 2026-06-15 |
| OpenAI | High | 2026-04-10 | 2026-07-10 |

### Database Encryption Keys
| Database | Classification | Rotation Schedule |
|----------|---------------|-------------------|
| aos-brain-state | Critical | Monthly |
| minecraft-worlds | Standard | Bi-annual |
| trading-data | Critical | Monthly |
| customer-leads | High | Quarterly |

## Rotation Calendar

### May 2026
- **May 15:** Binance API keys (Knox)
- **May 20:** Database session keys
- **May 28:** Discord bot token

### June 2026
- **June 01:** Telegram bot token
- **June 10:** OpenAI API key
- **June 15:** AOS brain service credentials

### July 2026
- **July 01:** ElevenLabs API key
- **July 15:** TLS certificates review

## Access Audit Trail

**Format:** `[TIMESTAMP] [ACTOR] [ACTION] [SECRET_ID] [REASON]`

Recent Entries:
```
[2026-05-15 18:30:00 UTC] [Knox] [RETRIEVE] [binance-api-prod] [Trading session]
[2026-05-15 18:15:00 UTC] [Miles] [RETRIEVE] [elevenlabs-tts] [Customer call]
[2026-05-15 17:45:00 UTC] [System] [ROTATION] [aos-brain-db-key] [Scheduled]
```

## Incident Log

### 2026-04-20 - Code YELLOW
- **Type:** Suspicious access pattern detected
- **Resolution:** False positive—Miles legitimate bulk operations
- **Action:** Enhanced monitoring for 24 hours

### 2026-03-15 - Code GREEN
- **Type:** Certificate expiry warning
- **Resolution:** Proactive rotation completed
- **Action:** None—preventive maintenance

## Recovery Procedures

### From Hardware Failure
1. Activate escrow (shards A+B required)
2. Rebuild vault on replacement hardware
3. Verify integrity of all secrets
4. Full rotation as precaution

### From Compromise
1. Immediate Code BREACH
2. Emergency rotation of ALL secrets
3. Incident report to Chelios and Captain
4. Post-incident security review

---

*The vault remembers everything. The threshold forgets nothing.*

*Version: 1.0.0 | Keeper of the Threshold*