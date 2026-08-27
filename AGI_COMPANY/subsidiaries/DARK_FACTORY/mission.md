# DARK FACTORY — MISSION.md
**Guidance Layer · Goals & Non-Goals**
**Authored:** 2026-08-18 (RiP GoR Council directive)
**Owner:** Patricia (DMCIA) · **Enforcer:** Factory Triage

> This file is the single source of truth for what the Dark Factory is *allowed* to build.
> Every incoming spec/order is triaged against this file first. If a spec is **out of scope**,
> the factory REJECTS it — it corrects the requester, not the other way around.

---

## 🎯 GOALS (in scope)

1. **Robotics production** — cobra_v1, prometheus_v1, and their BOMs, design files (OpenSCAD/STL), and kits.
2. **Digital products** — Cream, ReggieStarr (web + PWA), N'og nog.
3. **Durable build orchestration** — Temporal workflows (validate → allocate → build → verify → notify → cleanup).
4. **Vendor sourcing & procurement** — outsourced manufacturing, vendor onboarding.
5. **Agent training** — Myl training system, curriculum, progression gates.
6. **Simulation** — physics/cobra simulation environments for pre-build validation.
7. **Agentic software & agent infrastructure** — browser/scraper agents, intelligence-collection tools (e.g. IC Browser), and fleet infrastructure that other agents use to operate. Captain directive 2026-08-27.

## 🚫 NON-GOALS (out of scope → REJECT)

1. **Autonomous deploy to production psdepot.com** — no auto-merge/auto-deploy to the live store. Human sign-off required (blue-green flip only on approval).
2. **Medical, legal, or financial advice** — anything touching health, law, or autonomous money movement.
3. **Autonomous model/system-prompt changes** — the factory never edits its own safety rules, SOUL, or guardrails.
4. **Anything not in a declared product line** — a spec for a random/undefined product gets rejected, not silently built.
5. **Security-sensitive changes** — pentest/security posture changes require Captain + Chelios sign-off.

## ⚖️ ACCEPT / REJECT TRIAGE RULES

| Signal | Decision |
|--------|----------|
| Spec maps to a declared GOAL product line | ✅ ACCEPT → queue |
| Spec conflicts with a NON-GOAL | ❌ REJECT (correct requester) |
| Spec is ambiguous / no clear product | 🔄 ASK for clarity |
| Spec too large / risky | ✂️ SPLIT into bite-size orders (one task at a time) |
| Spec touches production deploy | ⏸️ HOLD for human sign-off |

## 🔐 BOUNDARIES (factory rules — stricter than global rules)

- One order = one bite-size task. No multi-feature mega-builds.
- The builder NEVER sees hold-out scenarios. The validator NEVER sees the plan.
- Every build is verified before "complete" is reported.
- Escalate (don't loop) if stuck > 30 minutes.
- Never report success without an output artifact that exists and has size.

---

*"The factory that builds the agents — and corrects the specs."*
