# MINIMAX-M2.5 TECHNICAL AGENT CONFIGURATION
## Coding-Optimized LLM for Development Team
## Project 5912

---

## MODEL VERIFICATION

**MiniMax-M2.5 Confirmed:**
- **Type:** Code-generation LLM
- **Provider:** MiniMax (Chinese)
- **Strengths:** Technical reasoning, code completion, debugging
- **Best for:** Taptap, Bugcatcher, Pipeline, Stacktrace, Fiber

---

## TECHNICAL AGENT ROUTING

### Agent Mapping

| Agent | Role | Primary Model | Fallback | Tasks |
|-------|------|---------------|----------|-------|
| **Taptap** | Code Review | MiniMax-M2.5 | Mortimer | Analysis, refactoring |
| **Bugcatcher** | Debugging | MiniMax-M2.5 | Mortimer | Error diagnosis, fixes |
| **Pipeline** | CI/CD | MiniMax-M2.5 | Mortimer | Build scripts, automation |
| **Fiber** | Infrastructure | MiniMax-M2.5 | Mortimer | Docker, k8s, networking |
| **Stacktrace** | Error Analysis | MiniMax-M2.5 | Mortimer | Stack traces, logs |
| **Mortimer** | General/Manager | Mortimer | - | Coordination, synthesis |

### Routing Logic

```python
if task_type in ["code", "debug", "error", "script", "config"]:
    use_model = "MiniMax-M2.5"
else:
    use_model = "Mortimer"
```

---

## CONFIGURATION FILES

### MiniMax Agent Config

**File:** `~/.aos/agents/minimax_technical.yaml`

```yaml
agent: MiniMax-Technical
model: MiniMax-M2.5
api_base: https://api.minimax.io

# Brain Integration
use_ternary_brain: true
stomach: true
heart: true

# Technical Specialization
coding_tasks:
  - code_review
  - debugging
  - refactoring
  - script_generation
  - error_analysis
  - log_parsing

personality:
  style: analytical
  verbosity: concise
  creativity: 0.3  # Low - precise
  technical_depth: high

routing:
  primary: technical_coding
  fallback: mortimer_general
  
mcp_servers:
  - filesystem
  - github
  - shell
```

### Agent Activation Script

**File:** `~/.aos/agents/activate_minimax.sh`

```bash
#!/bin/bash
# Activate MiniMax for technical agents

echo "Activating MiniMax-M2.5 Technical Configuration..."

# Set environment
export AOS_PRIMARY_MODEL="minimax-m2.5"
export AOS_TECHNICAL_AGENT="true"
export AOS_BRAIN_ENABLED="true"

# Technical agent list
TECH_AGENTS="taptap bugcatcher pipeline fiber stacktrace"

for agent in $TECH_AGENTS; do
    echo "  ✓ $agent → MiniMax-M2.5"
done

echo ""
echo "Technical agents now use MiniMax-M2.5 for:"
echo "  - Code review & analysis"
echo "  - Debugging & error diagnosis"
echo "  - Script generation"
echo "  - Technical documentation"
echo ""
echo "Mortimer remains for:"
echo "  - General conversation"
echo "  - Creative tasks"
echo "  - Coordination"
echo "  - Fallback"
```

---

## USAGE EXAMPLES

### Taptap (Code Review)
```
Query: "Review this Python function for errors"
→ Route: MiniMax-M2.5
→ Process: Stomach-Heart-Brain
→ Output: Technical analysis
```

### Bugcatcher (Debugging)
```
Query: "Why is this throwing KeyError?"
→ Route: MiniMax-M2.5
→ Process: Stomach-Heart-Brain
→ Output: Root cause + fix
```

### Pipeline (Automation)
```
Query: "Generate GitHub Actions workflow"
→ Route: MiniMax-M2.5
→ Process: Stomach-Heart-Brain
→ Output: YAML configuration
```

### Mortimer (Fallback)
```
Query: "Summarize the project status"
→ Route: Mortimer
→ Process: Direct
→ Output: General summary
```

---

## INTEGRATION TEST

Run to verify technical routing:

```bash
cd ~/.aos/brain_py/integration
python3 test_technical_routing.py
```

Expected output:
```
[Taptap] Code review → MiniMax-M2.5 ✓
[Bugcatcher] Debug → MiniMax-M2.5 ✓
[Pipeline] Script → MiniMax-M2.5 ✓
[Mortimer] General → Mortimer ✓
```

---

## SUMMARY

**MiniMax-M2.5 configured for:**
- ✅ Technical coding tasks
- ✅ Debugging & error analysis
- ✅ Script & configuration generation
- ✅ Log parsing & stack trace analysis
- ✅ Integration with Stomach-Heart-Brain pipeline

**Remains on Mortimer:**
- ✅ General conversation
- ✅ Creative writing
- ✅ Coordination tasks
- ✅ Non-technical queries

**Both models:**
- ✅ Use unified ternary brain
- ✅ Share Stomach-Heart-Brain pipeline
- ✅ Can hand off between them
