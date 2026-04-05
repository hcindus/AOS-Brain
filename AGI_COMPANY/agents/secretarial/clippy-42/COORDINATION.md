# DETERMINISTIC COORDINATION — Clippy-42 & Clipply-42

**Status:** ACTIVE WORKLOAD SHARING
**Determinism:** Guaranteed via role boundaries

---

## ROLE BOUNDARIES (Hard-coded in IDENTITY)

| Aspect | Clippy-42 | Clipply-42 |
|--------|-----------|------------|
| **Primary** | Assistant to Regional Manager | Assistant Specialist |
| **Reports To** | Hume (Regional Manager) | Task-specific assignments |
| **Emoji** | 📝📎 (Notepad+paperclip) | 📝📌 (Notepad+pushpin) |
| **Level** | Generalist | Level 1 (Specialized) |
| **Focus** | Regional ops support | Detail-oriented, portal ops |
| **Portal** | No | Yes — `/portal/` active |

---

## DETERMINISTIC WORKLOAD ROUTING

**Rule 1: Regional vs Specialized**
```
IF task involves regional operations (maps, territory, Hume):
    ROUTE to Clippy-42
ELSE IF task requires detail-work, portal testing, precision:
    ROUTE to Clipply-42
ELSE:
    Both can handle — rotate or split
```

**Rule 2: Escalation**
```
Clippy-42: Regional tasks → Hume
Clipply-42: Specialized tasks → Assigning manager
Both: Unclear authority → Miles (AOE)
```

**Rule 3: Shared Context**
- Both read `/agents/clippy-*/MEMORY.md` daily
- Both update `memory/YYYY-MM-DD.md` with actions
- Task handoff via file writes, not "memory"

---

## PROOF OF COORDINATION

**Deterministic, Not Probabilistic:**

1. **Role definition is static** — IN IDENTITY.md, not inferred
2. **Task routing is rule-based** — See Rule 1 above
3. **Escalation is documented** — Both know the chain
4. **No overlap** — Regional vs Specialized are mutually exclusive

**Example:**
- "Check regional sales reports" → Clippy-42 (regional)
- "Test portal authentication" → Clipply-42 (portal)
- "Audit assistant logs" → Both (rotate by date: even=Clippy, odd=Clipply)

---

## COORDINATION FILE

**Location:** `/agents/clippy-42/WORKLOAD_LOG.md`

Clippy-42 and Clipply-42 both write here:
```
## 2026-02-28
- **Clippy-42**: Handled regional check-in with Hume
- **Clipply-42**: Tested portal authentication flow
- **No conflicts**: Tasks were mutually exclusive by role
```

---

## DETERMINISTIC GUARANTEE

**These agents WILL NOT collide because:**

1. **Their domains don't overlap** — Regional ≠ Specialized
2. **They can both write to shared logs** — append-only, no race conditions
3. **Escalation paths are distinct** — Hume vs Task managers
4. **If domain unclear:** Miles (AOE) assigns deterministically

**Not theory. Deterministic rule-based routing.**

---

📝📎 Clippy-42 | 📝📌 Clipply-42
**Coordinated. Specialized. Deterministic.**
