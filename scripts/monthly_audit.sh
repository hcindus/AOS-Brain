#!/bin/bash
# Monthly Audit Script for GitHub and VPS
# Runs on 1st of every month at 00:00 UTC

AUDIT_LOG="/root/.openclaw/workspace/memory/monthly_audit_$(date +%Y-%m).md"

echo "# Monthly Audit Report - $(date +%Y-%m-%d)" > "$AUDIT_LOG"
echo "" >> "$AUDIT_LOG"
echo "## GitHub Audit" >> "$AUDIT_LOG"
echo "" >> "$AUDIT_LOG"

cd /root/.openclaw/workspace

echo "### Repository Status" >> "$AUDIT_LOG"
echo "\`\`\`" >> "$AUDIT_LOG"
git status --short >> "$AUDIT_LOG" 2>&1
echo "\`\`\`" >> "$AUDIT_LOG"
echo "" >> "$AUDIT_LOG"

echo "### Commit Count (Last 30 Days)" >> "$AUDIT_LOG"
echo "- Total: $(git rev-list --count --since='30 days ago' HEAD) commits" >> "$AUDIT_LOG"
echo "" >> "$AUDIT_LOG"

echo "### Recent Commits" >> "$AUDIT_LOG"
echo "\`\`\`" >> "$AUDIT_LOG"
git log --oneline --since='30 days ago' | head -20 >> "$AUDIT_LOG"
echo "\`\`\`" >> "$AUDIT_LOG"
echo "" >> "$AUDIT_LOG"

echo "### File Sizes" >> "$AUDIT_LOG"
echo "\`\`\`" >> "$AUDIT_LOG"
find . -name "*.md" -type f -exec wc -l {} + 2>/dev/null | tail -10 >> "$AUDIT_LOG"
echo "\`\`\`" >> "$AUDIT_LOG"
echo "" >> "$AUDIT_LOG"

echo "## VPS Audit" >> "$AUDIT_LOG"
echo "" >> "$AUDIT_LOG"

echo "### System Resources" >> "$AUDIT_LOG"
echo "\`\`\`" >> "$AUDIT_LOG"
echo "Load: $(uptime | awk -F'load average:' '{print $2}')" >> "$AUDIT_LOG"
echo "Memory: $(free -h | grep '^Mem' | awk '{print $3 "/" $2}') used" >> "$AUDIT_LOG"
echo "Disk: $(df -h / | tail -1 | awk '{print $3 "/" $2 " (" $5 ")"}')" >> "$AUDIT_LOG"
echo "\`\`\`" >> "$AUDIT_LOG"
echo "" >> "$AUDIT_LOG"

echo "### Running Services" >> "$AUDIT_LOG"
echo "\`\`\`" >> "$AUDIT_LOG"
systemctl list-units --type=service --state=running | grep -E "(minecraft|ollama|roblox)" >> "$AUDIT_LOG"
echo "\`\`\`" >> "$AUDIT_LOG"
echo "" >> "$AUDIT_LOG"

echo "### Docker/Ollama Status" >> "$AUDIT_LOG"
echo "\`\`\`" >> "$AUDIT_LOG"
curl -s http://localhost:11434/api/tags 2>/dev/null | grep -o '"name":"[^"]*"' | head -5 >> "$AUDIT_LOG" || echo "Ollama check skipped" >> "$AUDIT_LOG"
echo "\`\`\`" >> "$AUDIT_LOG"
echo "" >> "$AUDIT_LOG"

echo "## Recommendations" >> "$AUDIT_LOG"
echo "" >> "$AUDIT_LOG"
echo "- [ ] Review large files for optimization" >> "$AUDIT_LOG"
echo "- [ ] Check for unused dependencies" >> "$AUDIT_LOG"
echo "- [ ] Verify backup integrity" >> "$AUDIT_LOG"
echo "- [ ] Review memory usage trends" >> "$AUDIT_LOG"
echo "" >> "$AUDIT_LOG"

echo "---" >> "$AUDIT_LOG"
echo "*Audit completed at $(date -Iseconds)*" >> "$AUDIT_LOG"

# Commit the audit report
cd /root/.openclaw/workspace
git add memory/monthly_audit_*.md
git commit -m "Monthly audit report: $(date +%Y-%m)" || true

# Push to GitHub
git push origin master || echo "Push failed, manual review needed"

echo "Monthly audit complete. Report: $AUDIT_LOG"
