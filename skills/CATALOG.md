# Skill Catalog — AGI Company / Performance Supply Depot

A registry of **every** AgentSkill in the repo. Each entry: name · purpose · KPI.

> **Total: ~210 distinct skills across 9 collections.** The house rule:
> *if you do a process twice, it becomes a skill with a clear KPI.*

---

## Collections (all locations)

| Collection | Count | What it holds |
|---|---|---|
| `mortimer-build/skills/hermes/` | 94 | Hermes agent — mlops (vllm, unsloth, peft), github, research (arxiv, duckduckgo), apple, media, productivity, gaming |
| `MetaClaw/memory_data/skills/` | 36 | Agent best-practices — secure-code-review, git-workflow, sql, secrets, debugging, task-decomposition |
| `AGI_COMPANY/shared/skills/` | 34 | AGI Company agents — crypto, finance, sales-consultant, security-officer, portfolio-manager, technical-architect |
| `skills/` | 23 | Working set — SOPs, `gcao-prompting`, `gor-protocol`, `jarvis-audit`, tooling |
| `aos_brain_py/skills/` | 12 | AOS Brain — brain-health-check, memory-consolidation, stomach-v1, thalamus-v1, pfc-v2 |
| `AGI_COMPANY/agents/technical/` | 3 | blender-expert, unity-expert, unreal-expert |
| `AGI_COMPANY/skills/` | 1 | script-generation |
| `mortimer-build/skills/aosbrain/` | 6 | mirror of `skills/` |
| `mortimer-build/skills/myl0n-ros/` | 1 | — |

**Mirror dirs (duplicates, not counted twice):** `aocros/skills/` (= AGI_COMPANY), `.sync/skills/` (= `skills/`), `aocros/agent_sandboxes/` (= technical agents).

---

## Working set (`skills/`) — actively used

### 🎯 Framework
| Skill | KPI |
|---|---|
| `gcao-prompting` | every prompt structured (Goal·Ctx·Act·Out·KPI) |

### 🧭 Governance
| Skill | KPI |
|---|---|
| `gor-protocol` | every decision stress-tested |

### 💰 Sales pipeline
| Skill | KPI |
|---|---|
| `sop-ai-prospecting` | 10k/qtr · 80% ICP |
| `sop-ai-qualifying` | 95% fewer unqualified calls |
| `sop-lead-response` | 5-min · 40% conversion |
| `sop-ai-presenting` | <10 min · 35% close |
| `sop-quote-followup` | 2h · 35% close |
| `sop-ai-objection-handling` | 90% handled · 25% lift |
| `sop-ai-closing-delivery` | 90% onboarding · win in 48h |
| `sop-order-status` | 60-sec · 80% FCR |

### 🗄️ Ops & Data
| Skill | KPI |
|---|---|
| `sop-resale-certificate` | 100% valid · 30-day flag |
| `sop-database-operations` | 0 data loss |

### 🔍 Audit
| Skill | KPI |
|---|---|
| `jarvis-audit` | PASS / WARN / FAIL |
| `agent-readiness-audit` | — |

### 🛠️ Tooling
`email-sender`, `game-creator`, `browser-agent`, `browser-automation`, `agent-browser-clawdbot`, `cmp`, `depotchaos`, `skill-builder`, `audit`

### 🌐 Web / Demo
`restaurant-landing-page` — build a single-page demo landing site for a local restaurant from a Yelp listing (menu + photos + contact) · KPI: live in <10 min

---

## Proposed (to codify next)
`dark-factory`, `deployment`, `lead-enrichment`, `lead-scraping`, `email-campaign`, `system-monitoring`

---

*Maintained at `skills/CATALOG.md`. The 210-skill full inventory spans 9 collections — consolidation into the dedicated `hcindus/skills` repo is the open task.*
