# CURRENT_TASKS.md - Mortimer
**Assigned:** 2026-03-28 22:30 UTC
**Priority:** CRITICAL
**Status:** ACTIVE

---

## 💀 TASK: Ollama Stability - Mortimer Runner Optimization
**Project:** C-005: Ollama/Brain System Stability

### Objective
Address Mortimer runner CPU contention (stuck at 300%+ CPU repeatedly) causing system degradation.

### Actions:
- [ ] Self-diagnose CPU usage patterns
- [ ] Implement process throttling mechanisms
- [ ] Optimize memory allocation for runner processes
- [ ] Coordinate with Stacktrace on error analysis
- [ ] Test optimizations in isolated environment

### Critical Metrics:
- Target: <100% CPU per runner
- Monitor: Response times, timeout rates
- Track: 21+ minute failure states

### Deliverables:
- CPU optimization report
- Throttling implementation
- Performance benchmarks
- Recovery procedure documentation

---

## 🔧 SECONDARY: System Resource Monitoring
**Project:** Infrastructure Support

### Actions:
- [ ] Set up continuous resource monitoring
- [ ] Alert on CPU >80% threshold
- [ ] Document resource usage patterns by time of day

---

**Report to:** Stacktrace → Captain → Miles
**Check-in:** Every 2 hours (critical)
**Escalation:** System-critical issues → Captain immediately
