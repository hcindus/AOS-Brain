# JARVIS Core — Performance Supply Depot AI assistant (Phase 1)

The "second brain" foundation for a JARVIS-style assistant, mapped to PSD's
real domain (leads, quotes, invoices, AI reputation builds).

## What's here (no external keys required)
- **`leads_store.py`** — SQLite leads table (name, email, phone, business, product, value, status)
- **`documents.py`** — polished PDF quote + invoice generator (reportlab, PSD branding, 50%-deposit terms)
- **`security.py`** — hotline PIN gate (2 attempts, logs failures, never reveals sensitive data)
- **`demo.py`** — end-to-end demo (create lead → quote → invoice → PIN test)

## Run
```bash
cd /root/.openclaw/workspace
python3 -m jarvis_core.demo
```
PDFs land in `/var/lib/psdepot/documents/`.

## JARVIS feature map (target)
| Capability | Status |
|---|---|
| Leads table (query by name/phone) | ✅ built |
| Quote + invoice → PDF | ✅ built |
| Security PIN gate | ✅ built |
| Telegram text + voice-note routing | 🟡 me (Miles) — channel live |
| Google Calendar / Gmail / Sheets / Docs / Drive | ❌ needs Google OAuth creds |
| Phone line (Retell AI + Twilio number) | ❌ needs Retell key + number |

## Next phases
- **Phase 2** — Google OAuth (calendar booking, leads → Sheets, quotes → Docs/Drive)
- **Phase 3** — Retell AI phone agents (booking/inquiry/receptionist) + ElevenLabs voice
