---
name: gcao-prompting
description: House prompting framework for every task, spec, and agent instruction. Structure any request as Goal (with a clear, measurable KPI), Context, Action, and Output format. Use before writing Dark Factory specs, skills, sales scripts, or any agent prompt — vague asks produce generic output; structured asks produce working output.
---

# GCAO Prompting (with KPI)

The house standard for writing prompts, specs, and agent instructions.
If you do it twice, write it in GCAO once and reuse it.

## The framework — GCAO + KPI

| Element | Question it answers | Required? |
|---|---|---|
| **G**oal | What outcome am I trying to achieve? | ✅ — with a **measurable KPI** |
| **C**ontext | Who/what is this for? What's the situation, constraints, prior attempts? | ✅ |
| **A**ction | The specific task/instruction. | ✅ |
| **O**utput | The exact format, length, structure expected. | ✅ |
| **KPI** | How will I know it worked? (a number + a deadline) | ✅ — always |

## The KPI rule

Every Goal must carry a **clear, measurable KPI** — a number you can check
later, not a vibe. Vague goals ("get more sales") become measurable ones
("5 qualified leads/week · 40% conversion · tracked in the lead portal").

Good KPI shape: **<metric> <target> <timeframe>** — e.g. "5-min lead response,
40%+ conversion, this week."

## Template

```
GOAL:  <what you want, with a measurable KPI>
CTX:   <who/what/why, constraints, what's already been tried>
ACT:   <the specific thing to do>
OUT:   <exact format/length/structure>
KPI:   <metric + target + timeframe>
```

## Example (bad → good)

**Bad:** "Write me a follow-up email."

**Good:**
```
GOAL:  Re-engage a ghosted lead and book a call (KPI: 1 reply, 1 booked call)
CTX:   Lead = Nick, AI-reputation build, quoted $3,400, went quiet 7 days ago,
       direct tone, no fluff
ACT:   Write a short follow-up email
OUT:   3 sentences, one clear CTA ("want to grab 15 min this week?"), no emojis
KPI:   >= 30% reply rate this week
```

## Where this applies
- Dark Factory specs (`specs/inbox/*.json`)
- New AgentSkills
- Sales scripts and follow-up sequences
- Any agent/system prompt

When in doubt, fill all five — the KPI is what separates "did it" from "did it well."
