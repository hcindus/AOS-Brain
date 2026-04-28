#!/bin/bash
# Load wiki content into memory for Miles

WIKI_DIR="/root/.openclaw/workspace/wiki"

echo "Loading wiki into context..."

# Ensure wiki exists
if [ ! -d "$WIKI_DIR" ]; then
    echo "Cloning wiki..."
    mkdir -p "$WIKI_DIR"
    cd "$WIKI_DIR"
    git init
    git remote add origin https://github.com/hcindus/AOS-Brain.wiki.git
    git pull origin master 2>/dev/null || echo "Wiki cloned"
fi

# Sync latest
cd "$WIKI_DIR"
git pull origin master 2>/dev/null || true

echo "Wiki loaded:"
echo "  - Home.md"
echo "  - ROSTER.md (Agent directory)"
echo "  - ARCHITECTURE.md (System design)"
echo "  - BRAIN_STATUS.md (Live health)"
echo "  - IMPLEMENTATION_COMPLETE.md"
echo "  - RISK_ASSESSMENT.md"
echo "  - README.md"
