# Griffin / HIM Rollout Plan — AGI Company

**Created:** 2026-10-03 (Captain directive)
**Trigger:** Tavus Griffin — "first Human Interaction Model" (full-duplex, video-to-video, passes video Turing test at 48%).

## North Star (Captain)
> "Setup the best order, get our SOPs so we know the basics, assemble the team list first. I would love Raven as our spokesmodel."

---

## 1. Team Roster (who's on the list)

### Flagship / Public Face
| Agent | Role | Notes |
|-------|------|-------|
| **Raven** (Myl1Ssa.R8s) | **Spokesmodel** | Jordacia-class. Already built: `characters/myl1ssa/`, RAVEN_MANIFEST.md (face+brain+presence+voice+body), HAL (digital_world/blender/unitree g1+h1). Embodied face of the company. |

### Sales
| Agent | Role | Model |
|-------|------|-------|
| **Miles** | Sales Consultant | Mort_II |
| **Mortimer** | Model hosting / sales engine | Mort_II |
| Pulp | Head of Sales | Mort_II |
| Jane | Senior/Enterprise Sales | nous-hermes2 |
| Hume | Regional Manager | nous-hermes2 |
| CLOSETER | Closer | nous-hermes2 |
| Clippy-42 | Assistant | gemma2:2b |

### Customer Service / Secretarial Pool (post-roast KEPT)
| Agent | Role | Notes |
|-------|------|-------|
| **GREET** | Receptionist / Dispatcher | Front desk, 24/7 |
| **R2-D2** | Technical Support | "Hold it up to the camera" use case |
| **Clerk** | Records | Documentation |
| **Executive** | C-Suite Support | High-value |

### Strategy / C-Suite (context)
| Agent | Role |
|-------|------|
| Patricia | DMCIA specialist — org alignment |

---

## 2. SOP Foundation (the "basics")

Existing SOP skill library = the playbook every HIM agent runs. Lock these first.

**Customer service:**
- `sop-order-status` — "where's my order" within 60s, 80% first-contact resolution (highest automation potential)
- `sop-resale-certificate` — reseller tax-exemption management
- `sop-database-operations` — safe data handling

**Sales (lead → close):**
- `sop-lead-response` — inbound within 5 min, 40%+ to qualified
- `sop-ai-prospecting` → `sop-ai-qualifying` → `sop-ai-presenting` → `sop-ai-objection-handling` (Feel-Felt-Found) → `sop-ai-closing-delivery`
- `sop-quote-followup` — quote within 2h, 35%+ close

**Cross-cutting:**
- `consultative-approach` — partner not vendor
- Disclosure SOP (NEW — required before any Turing-passing agent goes live)

---

## 3. Best Rollout Order

### Phase 0 — Lock the SOPs (foundation, ~already done)
Confirm each agent's playbook. Every HIM agent runs a documented SOP, no ad-hoc behavior.

### Phase 1 — Raven, the Spokesmodel (flagship, build now)
Embody Raven as the public face: Griffin-class face + voice + presence on top of her existing manifest/HAL.
- She's the demo — "living proof" (same logic as GREET/CLOSETER being "the product is the employee").
- Front-facing on the site, pitches, and video presence.
- Disclosure is easy here: she *announces* she's AI. No deception burden.

### Phase 2 — Customer Service (fastest ROI, lowest risk)
GREET, R2-D2, Clerk, Executive.
- "Hold a broken printer / wrong label roll up to the camera" — visual support = our POS supplies business.
- Clean disclosure ("I'm your support agent"), no closing pressure.

### Phase 3 — Sales (highest value, deploy last)
Miles, Mortimer, Pulp, Jane, Hume, CLOSETER.
- Full-duplex video closers: backchannel, read hesitation, stop when cut off.
- Highest disclosure/safety burden — deploy only after Phases 1–2 harden the disclosure SOP.

---

## 4. Open Questions / Blockers
- **Tavus access** — Griffin is research-preview only, select testers. No customer API yet. Need to request access.
- **Disclosure SOP** — RESOLVED (Captain, 2026-10-03): agents only need to state they are AI. One clear "I'm an AI assistant" beat — no elaborate script. (SOUL.md's "don't mention you're AI unless asked" flips to: always disclose for customer-facing Turing-passing agents.)
- **Voice cloning policy** — Griffin clones voice from ~10s audio. Guardrails needed.

*Status: plan drafted, awaiting Captain confirmation on Phase 1 start.*
