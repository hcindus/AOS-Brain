#!/bin/bash
# Midnight Git Push Script - June 18, 2026 00:00 UTC

REPOS=(
  "/root/.openclaw/workspace"
  "/root/.openclaw/workspace/wiki"
  "/root/.openclaw/workspace/reggiestarr-pos"
  "/root/.openclaw/workspace/rs79-source"
  "/root/.openclaw/workspace/psdepot"
  "/root/.openclaw/workspace/Dusty"
  "/root/.openclaw/workspace/AGI_COMPANies"
  "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/CREAM"
  "/root/.openclaw/workspace/MilkMan-Game"
  "/root/.openclaw/workspace/Cream"
  "/root/.openclaw/workspace/aocros/products/aurora_lite_v2"
  "/root/.openclaw/workspace/aocros/products/myl5n_ros"
  "/root/.openclaw/workspace/aocros/products/myl0n_ros"
  "/root/.openclaw/workspace/aocros/products/agentverse"
  "/root/.openclaw/workspace/aocros/products/patricia_ros"
  "/root/.openclaw/workspace/aocros/products/myl4n_ros"
  "/root/.openclaw/workspace/aocros/products/myl1n_ros"
  "/root/.openclaw/workspace/aocros/products/prometheus_ros"
  "/root/.openclaw/workspace/aocros/products/myl2n_ros"
  "/root/.openclaw/workspace/aocros/products/myl3n_ros"
  "/root/.openclaw/workspace/aocros/products/cobra_ros"
)

echo "=== MIDNIGHT GIT PUSH REPORT ==="
echo "Date: $(date -u '+%Y-%m-%d %H:%M UTC')"
echo "Window: 00:00-08:00 UTC work period"
echo "===================================="
echo ""

TOTAL_REPOS=0
REPOS_WITH_CHANGES=0
TOTAL_COMMITS=0
TOTAL_FILES=0
SKIPPED_REPOS=0
PUSH_ERRORS=0

for repo in "${REPOS[@]}"; do
  if [ -d "$repo/.git" ]; then
    TOTAL_REPOS=$((TOTAL_REPOS + 1))
    cd "$repo" || continue
    REPO_NAME=$(basename "$repo")
    
    # Check for uncommitted changes
    if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
      REPOS_WITH_CHANGES=$((REPOS_WITH_CHANGES + 1))
      
      echo "[$REPO_NAME] Uncommitted changes detected"
      
      # Get list of changed files
      CHANGED_FILES=$(git status --porcelain | wc -l)
      TOTAL_FILES=$((TOTAL_FILES + CHANGED_FILES))
      
      # Show summary
      git status --short | head -20
      if [ $CHANGED_FILES -gt 20 ]; then
        echo "  ... and $((CHANGED_FILES - 20)) more files"
      fi
      
      # Stage all changes
      git add -A
      
      # Create descriptive commit message
      COMMIT_MSG="Work period $(date -u '+%Y-%m-%d %H:%M UTC') - $CHANGED_FILES files changed"
      
      # Commit with the message
      if git commit -m "$COMMIT_MSG" --quiet; then
        TOTAL_COMMITS=$((TOTAL_COMMITS + 1))
        echo "  ✓ Committed: $COMMIT_MSG"
        
        # Push to origin
        if git push origin HEAD --quiet 2>/dev/null; then
          echo "  ✓ Pushed to origin"
        else
          echo "  ⚠ Push failed - may need manual intervention"
          PUSH_ERRORS=$((PUSH_ERRORS + 1))
        fi
      else
        echo "  ⚠ Commit failed"
        PUSH_ERRORS=$((PUSH_ERRORS + 1))
      fi
      echo ""
    else
      SKIPPED_REPOS=$((SKIPPED_REPOS + 1))
    fi
  fi
done

echo "===================================="
echo "SUMMARY:"
echo "  Repositories scanned: $TOTAL_REPOS"
echo "  Repositories with changes: $REPOS_WITH_CHANGES"
echo "  Repositories skipped (no changes): $SKIPPED_REPOS"
echo "  Total commits made: $TOTAL_COMMITS"
echo "  Total files pushed: $TOTAL_FILES"
echo "  Push errors: $PUSH_ERRORS"
echo "===================================="
