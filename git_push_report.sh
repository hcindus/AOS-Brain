#!/bin/bash

REPORT_FILE="/tmp/git_push_report_$(date +%Y%m%d_%H%M%S).txt"
exec > >(tee "$REPORT_FILE") 2>&1

echo "======================================"
echo "GIT PUSH SCHEDULE EXECUTION REPORT"
echo "======================================"
echo "Execution Time: $(date -u '+%Y-%m-%d %H:%M UTC')"
echo ""

BASE_DIR="/root/.openclaw/workspace"
cd "$BASE_DIR"

MAIN_REPOS=(
    "."
    "wiki"
    "reggiestarr-pos"
    "psdepot"
    "Dusty"
    "AGI_COMPANY"
    "MilkMan-Game"
    "Cream"
    "aocros"
    "claw-code"
    "tappylewis.cloud"
    "MetaClaw"
    "DepotChaos"
)

TOTAL_COMMITS=0
TOTAL_FILES=0
REPOS_PUSHED=0
ISSUES=()

for repo_path in "${MAIN_REPOS[@]}"; do
    full_path="$BASE_DIR/$repo_path"
    if [ ! -d "$full_path/.git" ]; then
        echo "[!] $repo_path: No .git directory found"
        continue
    fi
    
    cd "$full_path" || continue
    repo_name=$(basename "$full_path")
    
    echo ""
    echo "--- Repository: $repo_name ---"
    
    # Check for changes
    changes=$(git status --porcelain 2>/dev/null | wc -l)
    if [ "$changes" -eq 0 ]; then
        echo "    No uncommitted changes"
        continue
    fi
    
    echo "    Found $changes modified/new files"
    
    # Get remote URL
    remote_url=$(git remote get-url origin 2>/dev/null || echo "No remote")
    echo "    Remote: $remote_url"
    
    # Check for large files (>10MB)
    large_files=$(git status --porcelain 2>/dev/null | awk '{print $2}' | while read f; do
        if [ -f "$f" ] && [ $(stat -c%s "$f" 2>/dev/null || echo 0) -gt 10485760 ]; then
            echo "$f"
        fi
    done)
    
    if [ -n "$large_files" ]; then
        echo "    [!] Large files detected (>10MB):"
        echo "$large_files" | sed 's/^/        /'
        ISSUES+=("$repo_name: Large files need separate handling")
    fi
    
    # Stage and commit in chunks
    chunk=1
    while IFS= read -r -d '' file; do
        git add "$file"
        
        # Commit every 50 files
        staged=$(git diff --cached --name-only 2>/dev/null | wc -l)
        if [ "$staged" -ge 50 ]; then
            commit_msg="$(date -u '+%Y-%m-%d %H:%M UTC') - Chunk $chunk - $staged files"
            git commit -m "$commit_msg" --quiet
            TOTAL_COMMITS=$((TOTAL_COMMITS + 1))
            TOTAL_FILES=$((TOTAL_FILES + staged))
            echo "    Committed chunk $chunk: $staged files"
            chunk=$((chunk + 1))
        fi
    done < <(git status --porcelain 2>/dev/null | awk '{print $2}' | tr '\n' '\0')
    
    # Commit remaining staged files
    staged=$(git diff --cached --name-only 2>/dev/null | wc -l)
    if [ "$staged" -gt 0 ]; then
        commit_msg="$(date -u '+%Y-%m-%d %H:%M UTC') - Chunk $chunk - $staged files (final)"
        if git commit -m "$commit_msg" --quiet; then
            TOTAL_COMMITS=$((TOTAL_COMMITS + 1))
            TOTAL_FILES=$((TOTAL_FILES + staged))
            echo "    Committed final chunk $chunk: $staged files"
        fi
    fi
    
    # Push to origin
    if git push origin HEAD 2>&1; then
        echo "    [✓] Pushed to origin"
        REPOS_PUSHED=$((REPOS_PUSHED + 1))
    else
        echo "    [!] Push failed"
        ISSUES+=("$repo_name: Push failed")
    fi
done

echo ""
echo "======================================"
echo "SUMMARY"
echo "======================================"
echo "Repositories with changes processed: $REPOS_PUSHED"
echo "Total commits made: $TOTAL_COMMITS"
echo "Total files pushed: $TOTAL_FILES"
echo ""

if [ ${#ISSUES[@]} -gt 0 ]; then
    echo "ISSUES ENCOUNTERED:"
    printf '  - %s\n' "${ISSUES[@]}"
else
    echo "No issues encountered."
fi

echo ""
echo "Report saved to: $REPORT_FILE"
