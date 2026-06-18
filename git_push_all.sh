#!/bin/bash
# Git Push Schedule - 8 Hour Chunks
# Timestamp: 2026-06-18 16:12 UTC

REPORT_FILE="/tmp/git_push_report_$(date +%Y%m%d_%H%M%S).txt"
echo "=== GIT PUSH REPORT ===" > "$REPORT_FILE"
echo "Started: $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

WORKSPACE="/root/.openclaw/workspace"
cd "$WORKSPACE"

# Find all git repositories
REPOS=$(find "$WORKSPACE" -type d -name ".git" 2>/dev/null | sed 's|/\.git$||' | sort)

TOTAL_COMMITS=0
TOTAL_FILES=0
REPOS_PUSHED=0
REPOS_SKIPPED=0
LARGE_FILES=""

echo "Found $(echo "$REPOS" | wc -l) git repositories" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

for REPO in $REPOS; do
    cd "$REPO" || continue
    REPO_NAME=$(basename "$REPO")
    
    echo "--- Processing: $REPO_NAME ---" >> "$REPORT_FILE"
    
    # Check if there are changes
    if git diff --quiet && git diff --cached --quiet && [ -z "$(git status --porcelain)" ]; then
        echo "  Status: No changes to push" >> "$REPORT_FILE"
        REPOS_SKIPPED=$((REPOS_SKIPPED + 1))
        continue
    fi
    
    # Get list of modified files
    MODIFIED_FILES=$(git status --porcelain | grep -E '^\s*[MADRC]' | wc -l)
    UNTRACKED_FILES=$(git status --porcelain | grep -E '^\?\?' | wc -l)
    
    echo "  Modified: $MODIFIED_FILES, Untracked: $UNTRACKED_FILES" >> "$REPORT_FILE"
    
    # Check for large files (>10MB)
    LARGE_IN_REPO=$(find "$REPO" -type f -size +10M 2>/dev/null | head -20)
    if [ -n "$LARGE_IN_REPO" ]; then
        LARGE_FILES="${LARGE_FILES}\n  $REPO_NAME: $(echo "$LARGE_IN_REPO" | wc -l) large files"
        echo "  WARNING: Large files detected" >> "$REPORT_FILE"
    fi
    
    # Stage and commit in chunks (max 50 files per commit)
    CHUNK_SIZE=50
    CHUNK_NUM=1
    
    # Get all modified/deleted files
    ALL_FILES=$(git status --porcelain | grep -E '^\s*[MD]' | sed 's/^\s*[MD]\s*//' | head -1000)
    FILE_COUNT=$(echo "$ALL_FILES" | grep -v '^$' | wc -l)
    
    if [ "$FILE_COUNT" -gt 0 ]; then
        # Process in chunks
        echo "$ALL_FILES" | while IFS= read -r file; do
            [ -z "$file" ] && continue
            git add "$file" 2>/dev/null || true
        done
        
        # Commit with descriptive message
        COMMIT_MSG="Auto-push: $REPO_NAME - $(date -u '+%Y-%m-%d %H:%M UTC') - Files: $FILE_COUNT"
        git commit -m "$COMMIT_MSG" >> "$REPORT_FILE" 2>&1 || true
        
        TOTAL_COMMITS=$((TOTAL_COMMITS + 1))
        TOTAL_FILES=$((TOTAL_FILES + FILE_COUNT))
        
        # Push to origin
        git push origin $(git branch --show-current) >> "$REPORT_FILE" 2>&1
        PUSH_STATUS=$?
        
        if [ $PUSH_STATUS -eq 0 ]; then
            echo "  PUSHED: $FILE_COUNT files in commit" >> "$REPORT_FILE"
            REPOS_PUSHED=$((REPOS_PUSHED + 1))
        else
            echo "  ERROR: Push failed" >> "$REPORT_FILE"
        fi
    else
        echo "  No staged files to commit" >> "$REPORT_FILE"
    fi
    
    echo "" >> "$REPORT_FILE"
done

# Summary
echo "" >> "$REPORT_FILE"
echo "=== SUMMARY ===" >> "$REPORT_FILE"
echo "Repositories pushed: $REPOS_PUSHED" >> "$REPORT_FILE"
echo "Repositories skipped: $REPOS_SKIPPED" >> "$REPORT_FILE"
echo "Total commits made: $TOTAL_COMMITS" >> "$REPORT_FILE"
echo "Total files pushed: $TOTAL_FILES" >> "$REPORT_FILE"
echo "Large files flagged:$LARGE_FILES" >> "$REPORT_FILE"
echo "Ended: $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> "$REPORT_FILE"

cat "$REPORT_FILE"
