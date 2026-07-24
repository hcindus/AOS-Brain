# PSD Sales Automation - Integration Specification
## Complete 5-Phase AI Sales Pipeline

**Version:** 1.0.0  
**Status:** Ready for Deployment  
**Owner:** Miles (AGI Sales Consultant)

---

## Overview

This document specifies the complete integration architecture for Performance Supply Depot's AI-powered sales pipeline based on Dan Martell's 5-phase framework.

---

## SOP Mapping

| SOP | Phase | Description | File |
|-----|-------|-------------|------|
| SOP-043 | 1 | AI Prospecting | `sops/SOP-043-AI-Prospecting.md` |
| SOP-044 | 2 | AI Qualifying | `sops/SOP-044-AI-Qualifying.md` |
| SOP-045 | 3 | AI Presenting | `sops/SOP-045-AI-Presenting.md` |
| SOP-046 | 4 | AI Objection Handling | `sops/SOP-046-AI-Objection-Handling.md` |
| SOP-047 | 5 | AI Closing/Delivery | `sops/SOP-047-AI-Closing-Delivery.md` |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    LEAD SOURCES                                  │
│  LinkedIn │ Yelp │ Google Maps │ Chamber │ Industry DBs         │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: PROSPECTING (SOP-043)                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Prospector Agent                                           │ │
│  │ - ICP matching (80%+ accuracy)                             │ │
│  │ - Lead scoring (1-10)                                      │ │
│  │ - Contact enrichment                                       │ │
│  └────────────────────┬───────────────────────────────────────┘ │
└──────────────────────┼────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  CRM (DepotChaos)                                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Hot Lead Queue                                             │ │
│  │ - Score 7+ leads prioritized                               │ │
│  │ - Daily 50 lead quota                                      │ │
│  └────────────────────┬───────────────────────────────────────┘ │
└──────────────────────┼────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 2: QUALIFYING (SOP-044)                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Qualifier Agent + Twilio Voice                             │ │
│  │ - Voice calls with Adam TTS                                │ │
│  │ - BANT qualification (Budget, Authority, Need, Timeline)   │ │
│  │ - Calendar booking (score 60+)                             │ │
│  │ - Ghosted lead recovery sequence                           │ │
│  └────────────────────┬───────────────────────────────────────┘ │
└──────────────────────┼────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 3: PRESENTING (SOP-045)                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Presenter Agent                                            │ │
│  │ - AI intelligence gathering                                  │ │
│  │ - Custom proposal generation (<10 min)                       │ │
│  │ - Talk track creation                                        │ │
│  │ - PDF export                                                   │ │
│  └────────────────────┬───────────────────────────────────────┘ │
└──────────────────────┼────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 4: OBJECTION HANDLING (SOP-046)                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Coach Agent + Whisper Mode UI                              │ │
│  │ - Real-time objection detection                              │ │
│  │ - Feel-Felt-Found scripts                                    │ │
│  │ - Alternative responses                                      │ │
│  │ - Roleplay practice mode                                     │ │
│  └────────────────────┬───────────────────────────────────────┘ │
└──────────────────────┼────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 5: CLOSING/DELIVERY (SOP-047)                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Closer Agent                                               │ │
│  │ - Order processing automation                                │ │
│  │ - Welcome sequences (hour 0, 4, day 1, 3, 7, 30)             │ │
│  │ - Win detection                                              │ │
│  │ - Case study collection                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## Integration Points

### 1. Lead Sources → Prospector

**File:** `integrations/lead_sources/linkedin_scraper.py`

**Inputs:**
- LinkedIn Sales Navigator
- Yelp Fusion API
- Google Places API
- Chamber of Commerce directories

**Output Format:**
```json
{
  "lead_id": "LI-20250724-0001",
  "company_name": "Downtown Grill",
  "source": "linkedin",
  "icp_score": 9,
  "status": "hot",
  "contacts": [...]
}
```

**Configuration:**
```python
# Target criteria
industries = ["Restaurant", "Bar", "Retail", "Cafe"]
titles = ["Owner", "Manager", "Director"]
company_size = "10-500 employees"
geography = ["US", "Canada"]
```

---

### 2. Prospector → CRM

**File:** `integrations/crm/depotchaos_client.py`

**Database Schema:**
- `leads` table: Lead records with ICP scores
- `customers` table: Converted customers
- `activities` table: Call logs, emails, notes

**API Methods:**
```python
client.create_lead(lead_data)
client.get_hot_leads(min_score=7)
client.update_lead_status(lead_id, "qualified")
client.create_customer(deal_data)
```

---

### 3. CRM → Qualifier

**Trigger:** New hot lead (ICP score 7+)

**Action:** Initiate voice call via Twilio

**File:** `integrations/voice/twilio_integration.py`

**Environment Variables:**
```bash
TWILIO_ACCOUNT_SID=xxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_FROM_NUMBER=+1xxxxxxxxxx
```

**Call Flow:**
1. Opening: "Hi, this is Miles from Performance Supply Depot..."
2. Permission: "Do you have 2 minutes...?"
3. Discovery: BANT questions
4. Qualification: Score and route
5. Booking: Calendar integration

---

### 4. Qualifier → CRM

**Updates:**
- Qualification scores
- Transcripts
- Booking confirmations
- BANT data

---

### 5. CRM → Presenter

**Trigger:** Qualified appointment booked

**File:** `agents/presenter/agent.py`

**Process:**
1. Gather intelligence (lead data + research)
2. Generate custom proposal
3. Create talk track
4. Export PDF

---

### 6. Presenter → Human Rep

**Deliverables:**
- `Proposal-[COMPANY]-[DATE].pdf`
- `TalkTrack-[COMPANY]-[DATE].md`
- Pre-call briefing

---

### 7. Human Call → Whisper Mode

**File:** `web/whisper_mode_ui.html`

**Real-time Flow:**
```
Twilio Stream → Transcription → Objection Detection → UI Display
```

**UI Features:**
- Live transcript
- Objection badge (PRICE, TIMING, COMPETITION)
- Suggested responses (Feel-Felt-Found)
- Copy-to-clipboard
- Confidence scores

---

### 8. Call → CRM

**Storage:**
- Full transcript
- Recording URL
- Objections encountered
- Outcome

---

### 9. Close → Closer Agent

**Trigger:** Deal won

**File:** `agents/closer/agent.py`

**Actions:**
1. Create customer record
2. Trigger onboarding sequence
3. Schedule welcome emails
4. Set up win detection

---

### 10. Closer → CRM

**Updates:**
- Customer record
- Order status
- Onboarding progress
- Win tracking

---

## Service Architecture

### Main Service
**File:** `service.py`  
**Port:** 8085  
**Endpoints:**
- `/health` - Health check
- `/phase1/prospect` - Run prospecting
- `/phase2/qualify` - Run qualification
- `/phase3/generate-proposal` - Generate proposal
- `/phase4/analyze-objection` - Objection detection
- `/phase5/close` - Process close
- `/pipeline/full` - Complete pipeline

### Voice Webhook Server
**File:** `integrations/voice/twilio_integration.py`  
**Port:** 8086  
**Routes:**
- `/voice/incoming` - Call connected
- `/voice/process-speech` - Speech input
- `/voice/status` - Status callbacks

### Whisper Mode UI
**File:** `web/whisper_mode_ui.html`  
**Port:** Served via nginx (80/443)

---

## Configuration

### Models
| Agent | Model | Purpose |
|-------|-------|---------|
| Prospector | Mort_II:latest | Social analysis |
| Qualifier | Mort_II:latest + Adam TTS | Voice calls |
| Presenter | qwen2.5:14b | Deep reasoning |
| Coach | qwen2.5:14b | Coaching |
| Closer | nous-hermes2:latest | Warm, personable |

### Systemd Services
```bash
# Main automation service
psd-sales-automation.service → port 8085

# Voice webhook service
psd-voice-webhook.service → port 8086

# Both auto-start on boot
```

---

## Deployment Checklist

### Pre-deployment
- [ ] Set environment variables
- [ ] Configure Twilio credentials
- [ ] Link to DepotChaos database
- [ ] Set up LinkedIn API access
- [ ] Configure calendar integration

### Deployment
- [ ] Start systemd services
- [ ] Verify health endpoints
- [ ] Test voice webhooks
- [ ] Verify CRM writes
- [ ] Test Whisper Mode UI

### Post-deployment
- [ ] Monitor lead flow
- [ ] Check qualification rates
- [ ] Review proposal quality
- [ ] Track objection handling
- [ ] Measure onboarding completion

---

## Metrics & Monitoring

### Phase Targets
| Phase | Metric | Target |
|-------|--------|--------|
| 1 | ICP accuracy | 80%+ |
| 1 | Leads/quarter | 10,000+ |
| 2 | Qualification rate | 60%+ |
| 2 | Unqualified reduction | 95% |
| 3 | Proposal time | <10 min |
| 3 | Proposal quality | 8/10+ |
| 4 | Objection handling | 90%+ confident |
| 4 | Close rate improvement | 25%+ |
| 5 | Onboarding completion | 90%+ |
| 5 | First win time | <48 hours |

### Pipeline Funnel
- Companies → Hot Leads: 20%+
- Hot Leads → Qualified: 40%+
- Qualified → Proposals: 80%+
- Proposals → Closes: 35%+

---

## File Structure

```
psd/sales-automation/
├── agents/
│   ├── __init__.py
│   ├── prospector/
│   │   ├── __init__.py
│   │   └── agent.py          # SOP-043
│   ├── qualifier/
│   │   ├── __init__.py
│   │   └── agent.py          # SOP-044
│   ├── presenter/
│   │   ├── __init__.py
│   │   └── agent.py          # SOP-045
│   ├── coach/
│   │   ├── __init__.py
│   │   └── agent.py          # SOP-046
│   └── closer/
│       ├── __init__.py
│       └── agent.py          # SOP-047
├── integrations/
│   ├── lead_sources/
│   │   └── linkedin_scraper.py
│   ├── voice/
│   │   └── twilio_integration.py
│   └── crm/
│       └── depotchaos_client.py
├── web/
│   └── whisper_mode_ui.html
├── orchestrator.py
├── service.py
├── requirements.txt
├── INTEGRATION-SPEC.md
└── README.md
```

---

## Next Steps

1. **Environment Setup**
   - Set all environment variables
   - Configure API keys
   - Test database connections

2. **Service Deployment**
   - Enable systemd services
   - Configure nginx for Whisper UI
   - Set up SSL certificates

3. **Integration Testing**
   - End-to-end pipeline test
   - Voice call test
   - CRM write verification

4. **Production Monitoring**
   - Deploy monitoring dashboard
   - Set up alerting
   - Track conversion metrics

---

**Ready for deployment on your command.**
