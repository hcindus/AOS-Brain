#!/bin/bash
# AOS Brain GitHub Sync v1.0
# Multi-device synchronization for laptop/phone/VPS

REPO_NAME="aos-brain-sync"
WORKSPACE="/root/.openclaw/workspace"
SYNC_DIR="$WORKSPACE/.sync"
GITHUB_USER="${GITHUB_USER:-hcindus}"
BRANCH="${BRANCH:-main}"

# Files to sync (lightweight, no secrets)
SYNC_FILES=(
    "MEMORY.md"
    "HEARTBEAT.md"
    "SOUL.md"
    "IDENTITY.md"
    "USER.md"
    "AGENTS.md"
    "wiki/"
    "skills/"
    "reports/"
    "visual-graph/"
)

# Files to NEVER sync (secrets)
IGNORE_PATTERNS=(
    "*.env"
    "secrets/"
    "*.key"
    "*.pem"
    "*.pkl"
    ".env*"
    "*/secrets/*"
)

echo "🔄 AOS Brain GitHub Sync"
echo "========================"

init_repo() {
    echo "📦 Initializing sync repository..."
    
    mkdir -p "$SYNC_DIR"
    cd "$SYNC_DIR"
    
    # Initialize git if not exists
    if [ ! -d ".git" ]; then
        git init
        git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git" 2>/dev/null || true
    fi
    
    # Create .gitignore
    cat > .gitignore << 'GITIGNORE'
# Secrets - NEVER SYNC
*.env
.env*
secrets/
*.key
*.pem
*.pkl
*.password
*.secret

# Large files
*.log
*.db
node_modules/
__pycache__/
*.pyc

# Local state
.sync/
tmp/
cache/
GITIGNORE

    echo "✅ Repository initialized"
}

sync_to_github() {
    echo "⬆️  Syncing TO GitHub..."
    
    # Copy files to sync dir
    for item in "${SYNC_FILES[@]}"; do
        src="$WORKSPACE/$item"
        if [ -e "$src" ]; then
            mkdir -p "$(dirname "$item")"
            cp -r "$src" "$item" 2>/dev/null || true
        fi
    done
    
    # Add all
    git add -A
    
    # Commit with timestamp
    git commit -m "Sync: $(date -u '+%Y-%m-%d %H:%M:%S UTC')" || {
        echo "ℹ️  No changes to sync"
        return 0
    }
    
    # Push
    git push origin "$BRANCH" || {
        echo "❌ Push failed. Trying to set upstream..."
        git push -u origin "$BRANCH"
    }
    
    echo "✅ Synced to GitHub"
}

sync_from_github() {
    echo "⬇️  Syncing FROM GitHub..."
    
    git fetch origin
    git pull origin "$BRANCH"
    
    # Copy back to workspace (preserve local files)
    for item in "${SYNC_FILES[@]}"; do
        if [ -e "$item" ]; then
            mkdir -p "$(dirname "$WORKSPACE/$item")"
            cp -r "$item" "$WORKSPACE/" 2>/dev/null || true
        fi
    done
    
    echo "✅ Synced from GitHub"
}

setup_auto_sync() {
    echo "⚙️  Setting up auto-sync..."
    
    # Add to existing cadence
    cat >> /etc/cron.d/aos-brain-cadence << 'CRON'

# Auto-sync to GitHub every 6 hours
0 */6 * * * root /root/.openclaw/workspace/scripts/github-sync.sh push >/dev/null 2>&1
CRON

    echo "✅ Auto-sync configured (every 6 hours)"
}

case "${1:-sync}" in
    init)
        init_repo
        ;;
    push|sync)
        cd "$SYNC_DIR" || init_repo
        sync_to_github
        ;;
    pull|update)
        cd "$SYNC_DIR" || { echo "❌ Sync directory not found. Run init first."; exit 1; }
        sync_from_github
        ;;
    auto)
        setup_auto_sync
        ;;
    status)
        cd "$SYNC_DIR" || { echo "❌ Not initialized"; exit 1; }
        git status --short
        ;;
    *)
        echo "Usage: $0 {init|push|pull|auto|status}"
        exit 1
        ;;
esac
