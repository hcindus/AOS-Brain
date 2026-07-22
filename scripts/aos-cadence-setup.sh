#!/bin/bash
# AOS Brain Cadence Setup v1.0
# Ensures all Four C's run on schedule

echo "Setting up AOS Brain cadence..."

# Create cron file for AOS Brain
cat > /etc/cron.d/aos-brain-cadence << 'EOF'
# AOS Brain v4.5 - Automated Cadence
# Performance Supply Depot LLC

SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# =============================================================================
# BRAIN HEALTH CHECKS
# =============================================================================

# Every 10 minutes: Keepalive check (comprehensive)
*/10 * * * * root /root/.openclaw/workspace/scripts/agent_keepalive.sh --no-restart >/dev/null 2>&1

# Every 30 minutes: Ollama keepalive (Mortimer model resident)
*/30 * * * * root timeout 30 /root/.openclaw/workspace/scripts/ollama_keepalive.sh >/dev/null 2>&1 || true

# Every hour: Brain persistence checkpoint
0 * * * * root echo '{"cmd":"save"}' | nc -U /tmp/aos_brain.sock >/dev/null 2>&1 || true

# =============================================================================
# DAILY OPERATIONS
# =============================================================================

# Daily at 04:00 UTC: Full audit + report generation
0 4 * * * root /root/.openclaw/workspace/skills/audit/scripts/audit.sh >/dev/null 2>&1

# Daily at 04:30 UTC: Wiki regeneration
30 4 * * * root /usr/bin/python3 /root/.openclaw/workspace/wiki/update_wiki.py >/dev/null 2>&1

# Daily at 05:00 UTC: Memory consolidation
0 5 * * * root /usr/bin/python3 /root/.openclaw/workspace/scripts/memory_consolidation.py >/dev/null 2>&1 || true

# =============================================================================
# WEEKLY OPERATIONS
# =============================================================================

# Sunday at 03:00 UTC: Full system backup
0 3 * * 0 root /root/.openclaw/workspace/scripts/backup_brain.sh >/dev/null 2>&1 || true

# Sunday at 04:00 UTC: Cleanup old logs
0 4 * * 0 root find /var/log/aos -name "*.log" -mtime +7 -delete >/dev/null 2>&1

EOF

chmod 644 /etc/cron.d/aos-brain-cadence

echo "✅ AOS Brain cadence installed to /etc/cron.d/aos-brain-cadence"
echo ""
echo "Schedule:"
echo "  Every 10m: Agent keepalive"
echo "  Every 30m: Ollama keepalive"  
echo "  Every hour: Brain checkpoint"
echo "  Daily 04:00: Full audit"
echo "  Daily 04:30: Wiki regeneration"
echo "  Daily 05:00: Memory consolidation"
echo "  Weekly Sun: Backup + cleanup"
