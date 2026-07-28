#!/bin/bash
# Check git status for all repositories

WORKSPACE="/root/.openclaw/workspace"
OUTPUT_FILE="/tmp/git_status_report.txt"

> "$OUTPUT_FILE"

echo "=== GIT STATUS REPORT ===" >> "$OUTPUT_FILE"
echo "Generated: $(date -u '+%Y-%m-%d %H:%M UTC')" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Find all git repos
find "$WORKSPACE" -type d -name ".git" 2>/dev/null | sort | while read -r gitdir; do
    repo_dir=$(dirname "$gitdir")
    repo_name=$(basename "$repo_dir")
    rel_path=$(realpath --relative-to="$WORKSPACE" "$repo_dir")

    cd "$repo_dir"

    # Check for uncommitted changes
    status=$(git status --porcelain 2>/dev/null)
    if [ -n "$status" ]; then
        echo "REPO: $rel_path" >> "$OUTPUT_FILE"
        echo "  Files changed:" >> "$OUTPUT_FILE"
        echo "$status" | while read -r line; do
            echo "    $line" >> "$OUTPUT_FILE"
        done
        echo "" >> "$OUTPUT_FILE"
    fi

done

echo "=== END REPORT ===" >> "$OUTPUT_FILE"
cat "$OUTPUT_FILE"