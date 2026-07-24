# PSD Sales Automation System
## Dan Martell 5-Phase AI Sales Framework Implementation

**SOPs:** 004, 005, 006, 007, 008
**Status:** DEPLOYED

---

## Overview

This system implements Dan Martell's 5-phase AI sales pipeline for Performance Supply Depot:

1. **Prospecting** (SOP-004) → 10,000+ leads/quarter
2. **Qualifying** (SOP-005) → 95% reduction in unqualified calls  
3. **Presenting** (SOP-006) → Custom proposals <10 min
4. **Objection Handling** (SOP-007) → AI coaching & roleplay
5. **Closing/Delivery** (SOP-008) → 90%+ onboarding completion

---

## Architecture

```
Company List → Prospector → Qualifier → Presenter → [Human Call + Coach Whisper] → Closer
     │              │            │            │                    │                   │
     │              │            │            │                    │                   │
  SOP-004       SOP-004      SOP-005      SOP-006              SOP-007             SOP-008
```

---

## Quick Start

### Start the Service
```bash
sudo systemctl start psd-sales-automation
sudo systemctl enable psd-sales-automation
```

### Check Status
```bash
curl http://localhost:8085/health
```

### Run Full Pipeline
```bash
curl -X POST http://localhost:8085/pipeline/full \
  -H "Content-Type: application/json" \
  -d '{"companies": ["Downtown Grill", "Metro Cafe", "Corner Bar"]}'
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Service health check |
| `/phase1/prospect` | POST | Run prospecting on company list |
| `/phase2/qualify` | POST | Run qualification on leads |
| `/phase3/generate-proposal` | POST | Generate proposal for appointment |
| `/phase4/analyze-objection` | POST | Real-time objection detection |
| `/phase5/close` | POST | Process deal close |
| `/pipeline/full` | POST | Run complete 5-phase pipeline |
| `/status/{phase}` | GET | Get phase output status |

---

## File Structure

```
psd/sales-automation/
├── agents/
│   ├── prospector/        # SOP-004
│   ├── qualifier/         # SOP-005
│   ├── presenter/         # SOP-006
│   ├── coach/             # SOP-007
│   └── closer/            # SOP-008
├── orchestrator.py        # Pipeline coordination
├── service.py            # HTTP service
├── requirements.txt
└── state/                # Pipeline state storage
    ├── phase_1_output.json
    ├── phase_2_output.json
    └── ...
```

---

## Configuration

### Models Used
- **Prospector:** `Mort_II:latest` (social analysis)
- **Qualifier:** `Mort_II:latest` + Adam voice (TTS)
- **Presenter:** `qwen2.5:14b` (deep reasoning)
- **Coach:** `qwen2.5:14b` (coaching)
- **Closer:** `nous-hermes2:latest` (warm, personable)

### Environment Variables
```bash
OLLAMA_HOST=http://localhost:11434
PYTHONPATH=/root/.openclaw/workspace/psd/sales-automation
```

---

## Integration with PSD

### CRM Integration
- Reads from: Lead database, customer records
- Writes to: Qualified appointments, proposals, customer onboarding

### Voice Integration (Future)
- Twilio for call initiation
- Real-time TTS with Mort_II + Adam voice
- Speech-to-text for prospect responses

### Calendar Integration (Future)
- Calendly/Acuity for booking
- Buffer time management
- Auto-assignment based on score

---

## Metrics

### Phase Targets
| Phase | Metric | Target |
|-------|--------|--------|
| 1 | ICP accuracy | 80%+ |
| 2 | Qualification rate | 60%+ |
| 3 | Proposal quality | 8/10+ |
| 4 | Objection handling | 90%+ confident |
| 5 | Onboarding completion | 90%+ |

### Overall Pipeline
- Leads → Qualified: 20%+
- Qualified → Proposal: 80%+
- Proposal → Close: 35%+

---

## Logs

```bash
# Service logs
sudo journalctl -u psd-sales-automation -f

# Application logs
tail -f /root/.openclaw/workspace/psd/sales-automation/logs/*.log
```

---

## Next Steps

1. [ ] Connect to live lead sources (LinkedIn, databases)
2. [ ] Implement voice calling with Twilio
3. [ ] Add real-time whisper mode UI
4. [ ] Integrate with PSD CRM
5. [ ] Deploy production monitoring

---

## Contact

**Owner:** Miles (AGI Sales Consultant)  
**System:** PSD Sales Automation  
**Version:** 1.0.0
