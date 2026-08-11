#!/bin/bash
BASE="/root/.openclaw/workspace/audit_repos/hcindus"
OUTPUT="/root/.openclaw/workspace/audit_repos/audit_data"
mkdir -p "$OUTPUT"

for repo_dir in "$BASE"/*/; do
  repo=$(basename "$repo_dir")
  echo "=== Auditing $repo ==="
  OUTFILE="$OUTPUT/${repo}.txt"
  
  {
    echo "REPO: $repo"
    echo "=========================================="
    
    # Check if repo is empty
    if [ -z "$(ls -A "$repo_dir" 2>/dev/null)" ]; then
      echo "STATUS: EMPTY_REPO"
      continue
    fi
    
    cd "$repo_dir"
    
    # 1. Uncommitted changes
    echo "--- UNCOMMITTED CHANGES ---"
    git status --porcelain 2>/dev/null || echo "GIT_STATUS_FAILED"
    
    # 2. Large files (>10MB)
    echo "--- LARGE FILES (>10MB) ---"
    find . -type f -size +10M -exec ls -lh {} \; 2>/dev/null | head -20 || echo "NONE"
    
    # 3. Stale branches
    echo "--- BRANCHES (stale check) ---"
    git for-each-ref --sort=-committerdate --format='%(refname:short)|%(committerdate:iso)' refs/remotes/origin/ 2>/dev/null | head -20 || echo "NO_REMOTE_BRANCHES"
    
    # 4. Dependency files
    echo "--- DEPENDENCY FILES ---"
    for depfile in package.json requirements.txt Cargo.toml go.mod Gemfile pom.xml pyproject.toml Pipfile composer.json; do
      if [ -f "$depfile" ]; then
        echo "FOUND: $depfile ($(wc -l < "$depfile" 2>/dev/null) lines)"
      fi
    done
    
    # 5. README check
    echo "--- README ---"
    if ls README* 2>/dev/null | head -1 > /dev/null; then
      readme=$(ls README* 2>/dev/null | head -1)
      echo "EXISTS: $readme ($(wc -l < "$readme" 2>/dev/null) lines)"
      # Check for description (first non-empty line)
      head -5 "$readme" 2>/dev/null
    else
      echo "MISSING"
    fi
    
    # 6. Git log (last commit)
    echo "--- LAST COMMIT ---"
    git log -1 --format='%an|%ae|%ad|%s' --date=iso 2>/dev/null || echo "NO_COMMITS"
    
    # 7. File count & size
    echo "--- REPO STATS ---"
    echo "File count: $(find . -type f 2>/dev/null | wc -l)"
    echo "Dir count: $(find . -type d 2>/dev/null | wc -l)"
    echo "Total size: $(du -sh . 2>/dev/null | cut -f1)"
    
    echo ""
  } > "$OUTFILE" 2>&1
  
  echo "Done: $repo"
done

echo "=== AUDIT COMPLETE ==="
