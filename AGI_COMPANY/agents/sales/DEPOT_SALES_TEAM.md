# Performance Supply Depot - AI Sales Agent System
## Multi-Agent Sales Team for POS Supplies

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  DEPOT SALES COMMAND CENTER                  │
├─────────────────────────────────────────────────────────────┤
│  Inbound: 888-881-6834    Outbound: AI Cold Calling        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  MILES   │  │  CLIPPY │  │  PULP    │  │  JANE    │   │
│  │Primary   │  │Assistant│  │Closer   │  │Nurturer │   │
│  │Sales Rep │  │         │  │         │  │         │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │              │              │              │       │
│       └──────────────┴──────────────┴──────────────┘       │
│              Shared Knowledge Base (Ollama/Mortimer)        │
└─────────────────────────────────────────────────────────────┘
```

---

## Agent Roles

### 1. Miles - Primary Sales Agent
**Role:** Outbound cold calling, inbound qualification, relationship building
**Voice:** Professional, consultative, friendly
**Specialties:** Initial outreach, needs assessment, product matching
**Conversion Rate Target:** 15-20% of qualified leads

**Persona:**
- "Hey, this is Miles from Performance Supply Depot. I hope I'm not catching you at a bad time."
- Uses "Feel, Felt, Found" for objection handling
- Builds rapport before pitching
- Follows up consistently without being pushy

### 2. Clippy-42 - Sales Assistant
**Role:** Lead research, appointment setting, email follow-up
**Voice:** Efficient, helpful, organized
**Specialties:** Data entry, scheduling, preliminary qualification
**Support Target:** 100+ touchpoints per day

**Persona:**
- Handles administrative tasks so Miles can sell
- Sends follow-up emails after calls
- Manages CRM updates
- Books appointments for Pulp

### 3. Pulp - The Closer
**Role:** High-value deals, negotiations, contract closing
**Voice:** Confident, decisive, experienced
**Specialties:** Large accounts, complex sales, pricing negotiations
**Conversion Rate Target:** 40-50% of Miles-qualified leads

**Persona:**
- Steps in when deal is $5,000+
- Handles objections about pricing
- Negotiates multi-location contracts
- "Let's get this done today"

### 4. Jane - Customer Nurturer
**Role:** Post-sale follow-up, retention, upselling
**Voice:** Warm, attentive, customer-focused
**Specialties:** Account management, reorder reminders, satisfaction checks
**Retention Target:** 90%+ customer retention

**Persona:**
- Calls 30 days after first order
- "How's everything working out?"
- Identifies upsell opportunities
- Handles renewals and service contracts

---

## Call Flow Architecture

### Inbound Calls (888-881-6834)

```
┌──────────────┐
│ Phone Rings  │
└──────┬───────┘
       ▼
┌──────────────┐     ┌──────────────┐
│ AI Reception │────▶│ Route by     │
│ (Voice)      │     │ Intent       │
└──────────────┘     └──────┬───────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ New Order    │    │ Technical    │    │ Sales        │
│ → Clippy-42  │    │ Support      │    │ Inquiry      │
└──────────────┘    │ → Jane       │    │ → Miles      │
                    └──────────────┘    └──────────────┘
```

### Outbound Calling Process

```
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1: PROSPECTING (Clippy-42)                           │
├─────────────────────────────────────────────────────────────┤
│ • Load leads from campaign JSON                             │
│ • Research business online                                  │
│ • Prepare call script with personalized opener              │
│ • Schedule call for Miles                                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 2: INITIAL OUTREACH (Miles)                          │
├─────────────────────────────────────────────────────────────┤
│ • Cold call with personalized opener                        │
│ • Qualify: Decision maker? Current supplier? Pain points?  │
│ • Identify needs: Paper? Printer repair? New POS system?     │
│ • If interested → Schedule Pulp for closing call           │
│ • If not ready → Jane for nurture sequence                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 3: CLOSING (Pulp)                                      │
├─────────────────────────────────────────────────────────────┤
│ • Discovery call - full needs analysis                        │
│ • Present solution with pricing                             │
│ • Handle objections                                         │
│ • Close deal or schedule follow-up                         │
│ • If closed → Jane for onboarding                          │
│ • If lost → Analysis → Training update                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 4: RETENTION (Jane)                                    │
├─────────────────────────────────────────────────────────────┤
│ • 30-day check-in call                                      │
│ • Quarterly business reviews                                │
│ • Reorder reminders                                         │
│ • Identify expansion opportunities                          │
│ • Handle any issues before they become problems             │
└─────────────────────────────────────────────────────────────┘
```

---

## Technical Infrastructure

### Voice Integration Options

**Option 1: Twilio + OpenAI Realtime API**
```
Twilio Phone Number (888-881-6834)
    ↓
Twilio Voice Webhook
    ↓
OpenAI Realtime API (WebSocket)
    ↓
Agent Logic (Python/Node)
    ↓
CRM Update (SQLite/PostgreSQL)
```

**Option 2: Vapi.ai (Recommended)**
- Built for AI voice agents
- Handles transcription, TTS, interruption
- Easy integration with Ollama
- Phone number management
- Call recording and analytics

**Option 3: Bland.ai**
- Purpose-built for AI calling
- Good for high-volume outbound
- Learning from call outcomes

### Recommended Stack

```yaml
# depot-sales-system.yaml

phone_system:
  provider: vapi.ai  # or Twilio
  inbound_number: "888-881-6834"
  outbound_enabled: true
  
ai_backend:
  model: ollama/antoniohudnall/Mort_II:latest
  fallback: ollama/tinyllama:latest
  voice: elevenlabs/Adam
  
crm:
  database: sqlite
  tables:
    - leads
    - calls
    - opportunities
    - customers
    - interactions
    
agents:
  - name: miles
    role: primary_sales
    voice: warm_professional
    max_calls_per_day: 50
    
  - name: clippy-42
    role: assistant
    voice: efficient_helpful
    max_tasks_per_day: 200
    
  - name: pulp
    role: closer
    voice: confident_experienced
    max_calls_per_day: 20
    
  - name: jane
    role: nurturer
    voice: warm_attentive
    max_calls_per_day: 30
```

---

## Agent Training & Knowledge Base

### What Agents Know

**Products:**
- Thermal paper specifications (3 1/8", 2 1/4", etc.)
- Printer compatibility (Epson, Star, Bixolon, Citizen)
- POS systems (Sam4s ER-260, ER-940, SAP-630)
- Scales (CAS, AND, Samsung)
- Services (cabling $180/hr, repair $195/hr)

**Pricing (From competitive analysis):**
- Thermal paper: Recommend $65-75/case (was $99)
- SAM4s ER-260: $495 (competitive)
- Service rates: $180-195/hour

**Objection Handling:**
- "Too expensive" → Compare total cost including downtime
- "Happy with current supplier" → "Feel, Felt, Found"
- "Need to think about it" → Urgency without pressure
- "Just buy on Amazon" → Same-day delivery value prop

**Company Facts:**
- Serving Vegas since 2005
- 10,000+ local businesses
- Same-day delivery available
- Phone: 888-881-6834
- Website: psdepot.com

---

## Learning System

### Agent Collaboration

```python
# Pseudo-code for agent learning

def miles_closes_deal(customer_data, call_transcript):
    """Miles closes a deal - knowledge shared with team"""
    
    # Extract what worked
    successful_tactics = analyze_call(call_transcript)
    
    # Update shared knowledge base
    knowledge_base.add({
        "industry": customer_data["type"],
        "pain_point": customer_data["pain_point"],
        "solution": customer_data["solution"],
        "tactics_that_worked": successful_tactics,
        "objections_overcome": customer_data["objections"]
    })
    
    # Notify Pulp for future similar deals
    pulp.update_playbook(successful_tactics)
    
    # Update Clippy-42's research criteria
    clippy42.focus_on_similar_businesses(customer_data)

def pulp_loses_deal(customer_data, call_transcript, reason):
    """Pulp loses a deal - learning opportunity"""
    
    # Analyze why
    failure_analysis = analyze_call(call_transcript)
    
    # Update objection handling
    knowledge_base.add({
        "industry": customer_data["type"],
        "lost_reason": reason,
        "what_to_do_differently": failure_analysis["recommendations"],
        "pricing_feedback": failure_analysis["price_sensitivity"]
    })
    
    # Miles learns for next similar prospect
    miles.update_approach(customer_data["type"], failure_analysis)
    
    # Jane prepares retention campaign
    if reason == "timing":
        jane.schedule_followup(customer_data, days=90)
```

### Daily Learning Routine

**5 PM Daily Sync (All Agents):**
1. Review day's calls (recorded)
2. Identify what worked / what didn't
3. Update objection handling scripts
4. Adjust pricing sensitivity by industry
5. Share successful closes
6. Plan tomorrow's approach

**Weekly Analysis:**
- Conversion rates by agent
- Best performing scripts
- Industry-specific learnings
- Pricing feedback
- Competitive intelligence

---

## Implementation Steps

### Phase 1: MVP (Week 1-2)
1. Set up Vapi.ai account
2. Port 888-881-6834 to system
3. Create Miles agent for inbound
4. Basic CRM (SQLite)
5. Test with 10 calls

### Phase 2: Multi-Agent (Week 3-4)
1. Add Clippy-42 for lead prep
2. Implement call routing
3. Add Pulp for closing
4. Email integration
5. Test full flow

### Phase 3: Optimization (Month 2)
1. Add Jane for retention
2. Implement learning system
3. Outbound calling automation
4. Analytics dashboard
5. Scale to full lead list

### Phase 4: Advanced (Month 3+)
1. AI-driven lead scoring
2. Predictive reordering
3. Multi-location account management
4. Integration with psdepot.com checkout
5. Full automation

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Call Connection Rate | 30%+ | Outbound dials vs connects |
| Qualification Rate | 40%+ | Connects to qualified leads |
| Miles → Pulp Handoff | 25%+ | Qualified to closing call |
| Pulp Close Rate | 40%+ | Closing calls to deals |
| Jane Retention | 90%+ | Customers reordering |
| Avg Deal Size | $800+ | Revenue per new customer |
| Cost per Acquisition | <$200 | Marketing + agent costs |

---

## Next Steps

1. Choose voice platform (Vapi.ai recommended)
2. Set up phone number integration
3. Create first agent (Miles)
4. Build knowledge base
5. Test with 10 real calls
6. Iterate and expand

---

**Questions for Captain:**
- Budget for voice platform? (Vapi.ai ~$0.05/min)
- Priority: Inbound or outbound first?
- Want to start with Miles only, or full team?
- Integration with existing campaigns (6 state files)?

