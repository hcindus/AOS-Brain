#!/bin/bash
cd /root/.openclaw/workspace
echo "=== GIT STATUS ==="
git status --short 2>/dev/null | wc -l
echo ""
echo "=== LAST 5 COMMITS ==="
git log --oneline -5
echo ""
echo "=== FIRST 50 FILES IN STATUS ==="
git status --short 2>/dev/null | head -50
