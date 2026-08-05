# Brain v4 Port 8000 Diagnosis
**Priority:** HIGH  
**Assigned:** Forge  
**Date:** 2026-08-05

## Problem
- Brain processes running but port 8000 not responding
- Socket (/tmp/aos_brain.sock) works fine (tick 65K, 15 organs)
- Mission Control on port 8001 works
- Port 8000 may be optional or misconfigured

## Investigation Steps
1. [x] Kill zombie process (done 2026-08-04)
2. [ ] Check brain logs for port 8000 bind attempts
3. [ ] Verify no firewall blocking
4. [ ] Document if port 8000 is intentional (socket-only architecture)
5. [ ] If intentional, update monitoring to stop false alerts

## Logs
```bash
journalctl -u aos-brain-v4 --since "2026-08-04" | grep -i "port\|bind\|8000"
ss -tlnp | grep 8000
```

## Current Brain State
- Process: PID 970526 (clean, single process)
- Socket: /tmp/aos_brain.sock (responsive)
- Mission Control: Port 8001 (working)
- Port 8000: NOT LISTENING

## Success Criteria
- [ ] Root cause documented
- [ ] Fix applied or false-alert suppressed
