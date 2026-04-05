#!/bin/bash
# Monthly GitHub Audit Script - hcindus
# Date: 2026-04-01

REPOS=(
  "amhudsupply"
  "AOS-Brain"
  "hcindus"
  "Myl0n.R0s"
  "myl0n.r1s"
  "neon-courier"
  "performance-supply-depot"
  "performancesupplydepot"
  "tappylewis.cloud"
  "Warzone-2100-Maps"
  "website-template"
)

AUDIT_DIR="/tmp/github_audit_$(date +%Y%m%d)"
mkdir -p "$AUDIT_DIR"

echo "# GitHub Monthly Audit Report - hcindus"
echo "Date: $(date '+%Y-%m-%d %H:%M UTC')"
echo "Auditor: Miles (Autonomous Operations Engine)"
echo ""

for repo in "${REPOS[@]}"; do
  echo "========================================"
  echo "REPO: $repo"
  echo "========================================"
  
  REPO_URL="https://github.com/hcindus/${repo}.git"
  REPO_DIR="$AUDIT_DIR/$repo"
  
  # Clone or fetch
  if [ -d "$REPO_DIR/.git" ]; then
    cd "$REPO_DIR" && git fetch --all --quiet 2>/dev/null
  else
    git clone --depth 1 "$REPO_URL" "$REPO_DIR" 2>/dev/null
    cd "$REPO_DIR" 2>/dev/null || continue
  fi
  
  # Check if clone succeeded
  if [ ! -d ".git" ]; then
    echo "⚠️  FAILED TO CLONE: $repo"
    continue
  fi
  
  # 1. Check for uncommitted changes (if any local modifications)
  echo "---"
  echo "1. WORKING TREE STATUS:"
  if git status --porcelain | grep -q .; then
    echo "   ⚠️  UNCOMMITTED CHANGES DETECTED"
    git status --short
  else
    echo "   ✅ Clean working tree"
  fi
  
  # 2. Check for large files
  echo "---"
  echo "2. LARGE FILES (>1MB):"
  LARGE_FILES=$(git ls-tree -r -l --abbrev --full-name HEAD 2>/dev/null | awk '$4 > 1048576 {print $4, $5}' | sort -rn | head -10)
  if [ -n "$LARGE_FILES" ]; then
    echo "   ⚠️  Large files found (should review .gitignore):"
    echo "$LARGE_FILES" | while read size name; do
      SIZE_MB=$(echo "scale=2; $size/1048576" | bc 2>/dev/null || echo "$(($size/1048576))")
      echo "      - $name (${SIZE_MB}MB)"
    done
  else
    echo "   ✅ No files >1MB"
  fi
  
  # 3. Check for stale branches
  echo "---"
  echo "3. BRANCHES (local tracking):"
  git branch -a 2>/dev/null | head -20 | sed 's/^/   /'
  
  # Check for branches not updated in 90 days
  echo "   ---"
  echo "   Branches not updated in 90+ days:"
  git for-each-ref --sort=committerdate refs/remotes/origin --format='%(refname:short) %(committerdate:iso8601)' 2>/dev/null | while read branch date; do
    BRANCH_DATE=$(date -d "$date" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S%z" "$date" +%s 2>/dev/null)
    CURRENT=$(date +%s)
    DIFF=$(( (CURRENT - BRANCH_DATE) / 86400 ))
    if [ $DIFF -gt 90 ]; then
      echo "   ⚠️  $branch ($DIFF days old)"
    fi
  done
  
  # 4. Check for dependency files
  echo "---"
  echo "4. DEPENDENCY FILES:"
  for depfile in package.json requirements.txt Cargo.toml pom.xml build.gradle Gemfile; do
    if [ -f "$depfile" ]; then
      echo "   📦 $depfile"
    fi
  done
  
  # 5. Check README
  echo "---"
  echo "5. README STATUS:"
  if [ -f "README.md" ]; then
    LINES=$(wc -l < README.md)
    if [ $LINES -lt 10 ]; then
      echo "   ⚠️  README.md exists but is very short ($LINES lines)"
    else
      echo "   ✅ README.md present ($LINES lines)"
    fi
    # Check for badges
    if grep -q "badge" README.md 2>/dev/null; then
      echo "   ✅ Contains badges"
    else
      echo "   💡 Consider adding status badges"
    fi
  elif [ -f "README.rst" ]; then
    echo "   ℹ️  README.rst present"
  else
    echo "   ❌ No README found"
  fi
  
  # 6. Security files
  echo "---"
  echo "6. SECURITY FILES:"
  if [ -f ".gitignore" ]; then
    IGNORE_SIZE=$(wc -l < .gitignore)
    echo "   ✅ .gitignore ($IGNORE_SIZE lines)"
  else
    echo "   ❌ No .gitignore file"
  fi
  
  if [ -f "LICENSE" ] || [ -f "LICENSE.md" ]; then
    echo "   ✅ License file present"
  else
    echo "   ⚠️  No license file"
  fi
  
  echo ""
done

echo "========================================"
echo "AUDIT COMPLETE"
echo "========================================"
