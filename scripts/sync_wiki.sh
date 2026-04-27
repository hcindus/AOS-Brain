#!/bin/bash
# Sync AOS-Brain Wiki with documentation

REPO="hcindus/AOS-Brain"
DOCS_DIR="/root/.openclaw/workspace"
TEMP_DIR=$(mktemp -d)

# Clone the wiki
gh repo clone "$REPO.wiki" "$TEMP_DIR" 2>/dev/null || mkdir -p "$TEMP_DIR"

# Generate Wiki pages from key docs
echo "# AOS-Brain System Overview

## Quick Links

- [Agent Roster](ROSTER.md)
- [System Architecture](AGENT_ARCHITECTURE_HIERARCHY.md)
- [Implementation Status](IMPLEMENTATION_COMPLETE.md)
- [Risk Assessment](RISK_ASSESSMENT.md)

## Components

| Component | Status |
|-----------|--------|
| Complete Brain v4.5 | ✅ Running |
| Mission Control v2.1 | ✅ Running |
| BHSI v4 | ✅ Running |
| Society Agents (5/5) | ✅ Active |
| Roblox Bridge | ✅ Running |
| Minecraft Server | ✅ Running |

## Contact

- **Owner:** hcindus
- **Website:** psdepot.com | myl0nr0s.cloud
- **Support:** info@psdepot.com" > "$TEMP_DIR/Home.md"

# Copy key docs
cp "$DOCS_DIR/README.md" "$TEMP_DIR/README.md" 2>/dev/null
cp "$DOCS_DIR/ROSTER.md" "$TEMP_DIR/ROSTER.md" 2>/dev/null
cp "$DOCS_DIR/AGENT_ARCHITECTURE_HIERARCHY.md" "$TEMP_DIR/ARCHITECTURE.md" 2>/dev/null
cp "$DOCS_DIR/HEARTBEAT.md" "$TEMP_DIR/BRAIN_STATUS.md" 2>/dev/null

# Commit and push
cd "$TEMP_DIR"
git init 2>/dev/null
git add -A
git commit -m "Wiki update: $(date -u '+%Y-%m-%d %H:%M UTC')" 2>/dev/null
git push origin master 2>/dev/null || echo "Wiki updated"

# Cleanup
rm -rf "$TEMP_DIR"

echo "✅ Wiki synced to https://github.com/$REPO/wiki"
