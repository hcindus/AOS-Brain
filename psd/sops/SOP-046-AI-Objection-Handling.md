# SOP-007: AI-Powered Objection Handling

## Document Control
| Field | Value |
|-------|-------|
| SOP ID | SOP-007 |
| Version | 1.0 |
| Created | 2026-07-24 |
| Author | Miles (AGI Sales Consultant) |
| Review Cycle | Weekly |
| Status | DRAFT |

---

## Purpose
Use AI for objection handling practice, real-time coaching, and continuous improvement. Build sales courage through repetition and feedback.

**Core Principle:** "Sales doesn't start until someone brings up an objection."

**Target:** 90%+ of common objections handled confidently, 25%+ improvement in close rate via AI coaching.

---

## Scope

### Applies To
- Sales reps practicing objections with AI
- Real-time objection support during calls
- Post-call analysis and improvement

### Does NOT Cover
- Initial prospecting (see SOP-004)
- Proposal generation (see SOP-006)

---

## Definitions

| Term | Definition |
|------|------------|
| Objection | Prospect concern that blocks purchase decision |
| Obstacle | Seller-introduced challenge to overcome (before prospect objects) |
| Talk Track | Scripted response framework for objections |
| Feel-Felt-Found | Classic objection handling pattern: "I understand how you feel..." |

---

## Common PSD Objections

### Price Objections
1. "Your price is too high"
2. "I can get it cheaper elsewhere"
3. "I need to think about the budget"
4. "Can you give me a discount?"

### Timing Objections
5. "I need to think about it"
6. "Call me back next quarter"
7. "We're not ready yet"
8. "I need to talk to my partner/boss"

### Product Objections
9. "I'm happy with my current supplier"
10. "I don't see the difference"
11. "We've always used [competitor]"
12. "I don't need all those features"

### Trust Objections
13. "I've never heard of your company"
14. "How do I know you'll deliver?"
15. "What if it doesn't work out?"

---

## Phase 1: AI Training & Practice

### Step 1.1: Upload Call Transcripts
**Owner:** Sales Rep
**Time:** 10 minutes weekly

**Process:**
1. Record all sales calls (AI auto-transcribes)
2. Upload last 5+ call transcripts to AI
3. Identify where objections occurred

**AI Analysis Prompt:**
```
Analyze these 5 sales call transcripts. Identify:
1. Every objection raised by the prospect
2. How the salesperson responded
3. What happened next (objection overcome or lost deal)
4. Patterns in objections by prospect type

Output:
- List of unique objections encountered
- Effectiveness rating of each response (1-10)
- Top 3 areas for improvement
```

### Step 1.2: AI Objection Coaching Session
**Owner:** Sales Rep + AI Agent
**Time:** 30 minutes weekly

**Prompt:**
```
Act as a world-class sales coach specializing in POS supply sales to restaurants, bars, and retail.

I encountered these objections this week:
[objection 1]
[objection 2]
[objection 3]

For each objection:
1. Give me 5 different response approaches
2. Rate each approach (1-10) with explanation
3. Give me the exact talk track/script for the best approach
4. Suggest questions to ask to uncover the real concern

Also, teach me the "Feel, Felt, Found" pattern for these objections.
```

### Step 1.3: AI Roleplay Practice
**Owner:** Sales Rep + AI Agent
**Time:** 20 minutes weekly

**Roleplay Setup:**
```
I want to roleplay a sales call. You are the prospect.

YOUR ROLE:
- [Name], [Title] at [Company Type]
- Personality: [Skeptical/Friendly/Direct/etc.]
- Situation: [Brief context]

MY ROLE:
- Miles, Sales Consultant at Performance Supply Depot
- Goal: Overcome objections and close the deal

SCENARIO:
I'm presenting a $2,500 supply order. You've just said: "[objection]"

Respond as the prospect would. At the end, give me feedback on my handling and a score 1-100.

Let's begin.
```

---

## Phase 2: Real-Time Call Support

### Step 2.1: Live Objection Detection
**Owner:** AI Agent (background)
**Trigger:** Objection keywords detected in live call

**Keywords:**
- Price: "expensive", "cost", "cheaper", "budget", "discount"
- Timing: "think about it", "later", "not ready", "next week"
- Competition: "current supplier", "competitor", "someone else"
- Authority: "boss", "partner", "decision maker"

### Step 2.2: Whisper Mode (Optional)
**Owner:** AI Agent
**Time:** Real-time

**Setup:**
- AI listens to call (transcription feed)
- When objection detected, flashes suggested response on screen
- Sales rep can see it, prospect cannot

**Whisper Display:**
```
OBJECTION DETECTED: Price

SUGGESTED RESPONSE:
"I understand budget is a concern. Actually, I felt the same way about [product] until I found...

What specifically about the price concerns you?"

FEEL-FELT-FOUND: ✅ Ready
```

### Step 2.3: Post-Call Analysis
**Owner:** AI Agent (automated)
**Time:** 5 minutes post-call

**Analysis Output:**
```json
{
  "call_id": "call-12345",
  "objections_encountered": [
    {
      "objection": "Price too high",
      "timestamp": "15:30",
      "response_quality": 7,
      "suggested_improvement": "Ask budget question before defending price",
      "outcome": "overcome"
    },
    {
      "objection": "Need to talk to partner",
      "timestamp": "22:15",
      "response_quality": 4,
      "suggested_improvement": "Get partner on call now or schedule 3-way",
      "outcome": "pending"
    }
  ],
  "overall_objection_handling_score": 6.5,
  "practice_recommended": [
    "Authority objection - getting decision maker involved"
  ]
}
```

---

## Objection Response Library

### Objection: "Your price is too high"

**Feel-Felt-Found:**
```
"I understand how you feel. The price is higher than you expected.

Actually, a lot of our customers felt the same way at first.

But what they found was that the quality difference saved them money in the long run. Our thermal rolls don't jam printers, which means no downtime during rush.

Can I show you what I mean?"
```

**Reframe:**
```
"I appreciate you bringing that up. Help me understand - are you comparing this to [competitor's product], or is this more about the budget you have allocated?

[Wait for answer]

Got it. Let me ask you this: What does it cost you when you run out of supplies during a busy shift?"
```

### Objection: "I need to think about it"

**Feel-Felt-Found:**
```
"Of course, I totally understand wanting to think it through.

Most of our partners felt that way too.

What they found was that delaying the decision actually cost them more in stockouts and rush shipping.

What specifically do you need to think through? Maybe I can help right now."
```

**Urgency:**
```
"Absolutely, take the time you need. Just so I know - what timeline are you thinking?

[Wait]

Got it. And what's driving that timeline? Is there something happening then?

[Wait - uncover real reason]

I see. Let me ask - if we could [solve specific concern], would you be ready to move forward today?"
```

### Objection: "I'm happy with my current supplier"

**Curiosity:**
```
"I'm glad you've got someone you trust. That's important.

Can I ask - what do you like most about working with them?

[Wait]

That's great. What would you change if you could?

[Wait - this is gold]

Interesting. What happens when [pain point they just mentioned]?

[Wait]

Got it. So if there was a way to [solve that problem], would it be worth a conversation?"
```

---

## Continuous Improvement Process

### Weekly Objection Analysis
**Owner:** Sales Manager

1. **Aggregate Data:**
   - Total objections encountered
   - Top 5 most common
   - Win/loss rate per objection type

2. **AI Coaching:**
   ```
   This week our team encountered these objections:
   [Top 5 list with frequency]
   
   Our win rates:
   - Price: 45%
   - Timing: 30%
   - Competition: 60%
   
   Generate new talk tracks for the lowest-performing objections.
   Create a 15-minute training module for the team.
   ```

3. **Team Training:**
   - 30-minute weekly objection handling workshop
   - Practice lowest-performing objection
   - Share success stories

### Monthly Review
- Update objection library with new responses
- Retrain AI models on successful patterns
- Celebrate reps with highest improvement

---

## Automation Notes

### AI Agent Configuration
```python
objection_config = {
    "agent_name": "DepotCoach-1",
    "model": "qwen2.5:14b",  # Deep reasoning for coaching
    "capabilities": [
        "transcript_analysis",
        "objection_detection",
        "response_generation",
        "roleplay",
        "whisper_mode"
    ],
    "objection_library": "/sops/objections/library.json",
    "patterns": [
        "feel_felt_found",
        "reframe",
        "curiosity",
        "urgency",
        "proof"
    ],
    "practice_mode": {
        "scenarios_per_week": 5,
        "difficulty": "adaptive",
        "feedback_depth": "detailed"
    }
}
```

### Integration Points
- **Input:** Call transcripts from SOP-006
- **Output:** Coaching feedback, training modules
- **Side Output:** Objection library updates

---

## Quality Metrics

### Individual Rep Metrics
| Metric | Target |
|--------|--------|
| Objection recognition rate | > 95% |
| Response confidence score | > 7/10 |
| Objection-to-close rate | > 40% |
| Practice sessions/week | > 2 |

### Team Metrics
| Metric | Target |
|--------|--------|
| Top objection frequency | Decreasing |
| Win rate on price objections | > 50% |
| Win rate on timing objections | > 35% |
| Team confidence score | > 8/10 |

---

## Related Documents
- SOP-006: AI Presenting (where objections occur)
- `/sops/objections/library.json` (living document)
- `/sops/training/weekly-workouts.md`

---

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-24 | Miles | Initial creation |

---

**Next Review Date:** 2026-07-31
