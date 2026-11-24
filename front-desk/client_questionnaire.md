# Frontline SOA — Client Setup Questionnaire

**Performance Supply Depot · Service Oriented Assistant**

Complete this when provisioning a Frontline SOA for a new client. Each answer maps
directly to a field in the client's `client_config.yaml` (see
`client_config.example.yaml`). The receptionist is built from these answers — the
tone, the greeting, the escalation path, and the notification routing.

> **Who is filling this out:** ______ &nbsp;·&nbsp; **Date:** ______ &nbsp;·&nbsp; **Sales rep:** ______

---

## 1 · Who the system is for (company information)

**Business name** *(exactly as it should be spoken on the phone)*
```
________________________________________
```

**Doing business as / legal name** *(if different)*
```
________________________________________
```

**Industry / type of business**
```
________________________________________
```

**Physical address** — street, city, state, ZIP
```
________________________________________
```

**Main phone line** *(the number the receptionist answers for)*
```
________________________________________
```

**Hours of operation**
```
Mon–Fri: ________    Sat: ________    Sun: ________
```

**Website**
```
________________________________________
```

---

## 2 · Primary contact (who owns the account)

**Name** `____________________` &nbsp; **Role / title** `____________________`

**Phone** `____________________` &nbsp; **Email** `____________________`

---

## 3 · Tone of greeting

**How should the receptionist greet callers?** *(pick one)*
- ☐ Warm & friendly — "Hey there, thanks for calling!"
- ☐ Professional — "Thank you for calling [Business], how may I help you?"
- ☐ Formal — "Good [morning/afternoon], you've reached [Business]."
- ☐ Casual — first-name basis, relaxed

**Custom greeting** *(optional — paste the exact opening line, or leave blank for default)*
```
________________________________________
________________________________________
```

**Business name pronunciation note** *(if it's unusual / easily misread)*
```
________________________________________
```

---

## 4 · Tone of receptionist

**Voice** *(text-to-speech voice the receptionist uses)*
- ☐ Polly.Matthew (default — warm, masculine)
- ☐ Polly.Joanna (feminine)
- ☐ Polly.Amy (British feminine)
- ☐ Other: _______________

**Personality** *(check all that apply)*
- ☐ Warm & empathetic  ☐ Energetic  ☐ Calm & steady  ☐ Professional
- ☐ Playful  ☐ Direct / no-nonsense

**Language**
- ☐ English  ☐ Spanish  ☐ Bilingual (English + Spanish)  ☐ Other: _______________

**Formality** *(1 = very casual, 5 = very formal)*
```
1 — 2 — 3 — 4 — 5
```

---

## 5 · Emergency contact (who to reach in an emergency)

**Name** `____________________` &nbsp; **Relationship** `____________________`

**Emergency phone (24/7)** `____________________`

**Escalation email** `____________________`

**What counts as an emergency?** *(check all that apply)*
- ☐ System outage / receptionist down
- ☐ Security / threat / breach
- ☐ Unhappy or irate customer
- ☐ Anything outside normal hours
- ☐ Other: _______________

---

## 6 · Emails (where notifications route)

**Primary notification email** *(transcripts, missed calls, after-hours)*
```
________________________________________
```

**Secondary / CC** `________________________________________`

**Orders & invoices** `________________________________________`

**Daily/weekly summary** `________________________________________`

---

## 7 · Cadence (how often the system follows up)

**Follow-up cadence on leads**
- ☐ Immediate only (respond, then hand off)
- ☐ Day 0 + 1 + 3 (standard)
- ☐ Aggressive (daily for a week)
- ☐ Custom: _______________

**Summary report frequency**
- ☐ Real-time / on-event  ☐ Daily digest  ☐ Weekly  ☐ None

**Quiet hours** *(do NOT contact between)*
```
From ________ to ________
```

**Preferred follow-up channel**
- ☐ Email  ☐ Phone  ☐ SMS  ☐ Any

---

## 8 · Suite (SOA routing)

**Which suite is this client on?**
- ☐ Front office ($149/mo) — greeter · missed-call · review · ping
- ☐ Growth ($349/mo) — closeter · concierge
- ☐ Full office ($749/mo) — clerk · ea · miles
- ☐ Security add-on ($99/mo) — chelios

**Special routing rules** *(optional — e.g. "route all Spanish calls to X", "route invoices to Y")*
```
________________________________________
________________________________________
```

---

**Thank you.** The answers above are used to provision the client's Frontline SOA —
greeting, voice, escalation, routing, and notifications — before the first live call.
