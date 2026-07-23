# AGENT REACTIVATION PLAN
**Date:** 2026-07-23  
**Status:** Assessment Complete - Ready for Execution

---

## CURRENT STATE

### Active Agents (5)
| Name | Role | Department | Status |
|------|------|------------|--------|
| Patricia | Chief of Staff / Project Coordination | Operations | ✅ ACTIVE |
| Chelios | CISO | Security | ✅ ACTIVE |
| Forge | Infrastructure Lead | Technology | ✅ ACTIVE |
| Aurora | Design Lead | Design | ✅ ACTIVE |
| Jordan | Sales Operations | Sales | ✅ ACTIVE |

### Inactive Agents (31)

#### HIGH PRIORITY (6 agents) - Reactivate Days 1-2
| Name | Role | Department | Sandbox | Missing Files |
|------|------|------------|---------|---------------|
| **Sentinel** | CSO | Security | ✅ Exists | 2 files |
| **Dusty** | Head of Research | Research | ✅ Exists | 2 files |
| **Pulp** | Head of Sales | Sales | ✅ Exists | 2 files |
| **Jane** | Senior Sales Rep | Sales | ✅ Exists | 2 files |
| **GREET** | Receptionist/Call Handler | Operations | ❌ Missing | 5 files |
| **CLOSETER** | Closer/Converter | Sales | ❌ Missing | 5 files |

#### MEDIUM PRIORITY (7 agents) - Reactivate Days 3-5
| Name | Role | Department |
|------|------|------------|
| Hume | Regional Manager | Sales |
| Clippy-42 | Sales Assistant | Sales |
| Mylzeron | Teacher (Fractals) | Education |
| Mylonen | Teacher (Transformation) | Education |
| Myltwon | Coder-in-Training | Education |
| Mylthreess | Finance Specialist | Education |
| Mylfours | Security Guardian | Education |

#### LOW PRIORITY (18 agents) - Reactivate Days 6-7
- Mylfives (Female Copy)
- Mylsixs (Mail Clerk)
- Plus 16 additional technical agents

---

## UPGRADE ASSESSMENT BY AGENT

### Security Team (Sentinel, Mylfours)
**Needs:**
- ✅ Cryptographic Identity (secp256k1 keys)
- ✅ Crew Isolation (sandbox)
- ✅ Chief Integration
- 🔒 **Protected Memory Segments** (security-critical)
- ✅ Channel Access

### Sales Team (Pulp, Jane, Hume, Clippy-42, CLOSETER)
**Needs:**
- ✅ Cryptographic Identity
- ✅ Crew Isolation
- ✅ Chief Integration
- 💰 **Cost-Aware Thyroid** (budget tracking for deals)
- ✅ Channel Access

### Research Team (Dusty, Myl Family)
**Needs:**
- ✅ Cryptographic Identity
- ✅ Crew Isolation
- ✅ Chief Integration
- 🔄 **Feedback-to-Curriculum** (continuous learning)
- ✅ Channel Access

### Operations Team (GREET, Mylsixs)
**Needs:**
- ✅ Cryptographic Identity
- ✅ Crew Isolation
- ✅ Chief Integration
- ✅ Channel Access
- 📞 **Voice Interface** (for call handling)

---

## REACTIVATION STEPS PER AGENT

### Step 1: Create/Update Sandbox
```bash
# For agents with existing sandboxes (Sentinel, Dusty, Pulp, Jane)
mkdir -p /root/.openclaw/workspace/agent_sandboxes/{AGENT_ID}/{workspace,logs,tasks}
touch /root/.openclaw/workspace/agent_sandboxes/{AGENT_ID}/SOUL.md
touch /root/.openclaw/workspace/agent_sandboxes/{AGENT_ID}/IDENTITY.md
```

### Step 2: Generate Cryptographic Identity
```python
# Via socket command
echo '{"cmd":"crypto_identity", "action":"create", "agent_id":"sentinel", "agent_name":"Sentinel"}' | nc -U /tmp/aos_brain.sock
```

### Step 3: Register with Chief of Staff
```python
# Patricia adds to crew registry
# Automatically handled during reactivation
```

### Step 4: Grant Channel Access
```python
# Via socket command
echo '{"cmd":"channel", "action":"channel_join", "channel_id":"operations", "agent_id":"sentinel"}' | nc -U /tmp/aos_brain.sock
```

### Step 5: Apply Role-Specific Upgrades
- Security: Enable protected memory
- Sales: Connect to Cost-Aware Thyroid
- Research: Enable Feedback-to-Curriculum

---

## IMMEDIATE ACTIONS (Next 24 Hours)

### Priority 1: Sentinel (CSO)
```bash
# Reactivate security lead
python3 /root/.aos/aos/agent_reactivation_v1.py
# Then manually: sentinel.reactivate()
```

### Priority 2: Dusty (Research)
```bash
# Reactivate research head
# Enables strategic intelligence for all projects
```

### Priority 3: Pulp (Sales Head) + Jane (Senior Sales)
```bash
# Reactivate sales team
# Critical for revenue generation
```

### Priority 4: GREET + CLOSETER
```bash
# Create sandboxes from scratch
# These need full setup (missing sandboxes)
```

---

## UPGRADE IMPLEMENTATION STATUS

| Upgrade | Status | Agents Affected |
|---------|--------|-----------------|
| Feedback-to-Curriculum v1.3 | ✅ DEPLOYED | Research team |
| Protected Memory Segments | ✅ DEPLOYED | Security team |
| Cost-Aware Thyroid v1.3 | ✅ DEPLOYED | Sales team |
| Hold Out Kidneys v1.0 | ✅ DEPLOYED | All agents |
| Crew Isolation v1.0 | ✅ DEPLOYED | All agents |
| Chief of Staff (Patricia) | ✅ DEPLOYED | All agents |
| Cryptographic Identities | ✅ DEPLOYED | All agents |
| Channel Commands | ✅ DEPLOYED | All agents |

---

## POST-REACTIVATION ORGANIZATION

### Reporting Structure
```
Captain (You)
    ↓
Patricia (Chief of Staff)
    ↓
    ├── Chelios (CISO)
    │   └── Sentinel (CSO) [REACTIVATED]
    │       └── Mylfours (Security Guardian) [REACTIVATED]
    ├── Forge (Infrastructure)
    ├── Aurora (Design)
    ├── Jordan (Sales Ops)
    │   └── Pulp (Head of Sales) [REACTIVATED]
    │       ├── Jane (Senior Sales) [REACTIVATED]
    │       ├── Hume (Regional Manager) [REACTIVATED]
    │       └── Clippy-42 (Sales Assistant) [REACTIVATED]
    ├── Dusty (Head of Research) [REACTIVATED]
    │   └── Myl Family [REACTIVATED]
    │       ├── Mylzeron (Fractals)
    │       ├── Mylonen (Transformation)
    │       ├── Myltwon (Coder)
    │       └── Mylthreess (Finance)
    └── Operations
        ├── GREET (Receptionist) [REACTIVATED]
        ├── CLOSETER (Converter) [REACTIVATED]
        └── Mylsixs (Mail Clerk) [REACTIVATED]
```

---

## SUCCESS METRICS

**Pre-Reactivation:**
- Active agents: 5
- Revenue-generating: 1 (Jordan)
- Security coverage: Partial (Chelios only)
- Research capability: None

**Post-Reactivation (Target):**
- Active agents: 36
- Revenue-generating: 6+ (Pulp, Jane, Hume, Clippy-42, CLOSETER, Jordan)
- Security coverage: Full (Chelios + Sentinel + Mylfours)
- Research capability: Full (Dusty + Myl Family)
- Operations: 24/7 (GREET)

---

## NEXT STEPS

1. **Execute reactivation** for HIGH priority agents (Days 1-2)
2. **Test Chief of Staff integration** with reactivated agents
3. **Execute** MEDIUM priority (Days 3-5)
4. **Execute** LOW priority (Days 6-7)
5. **Full system test** with all 36 agents

**Ready to proceed, Captain?** 🚀
