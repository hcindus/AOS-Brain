#!/bin/bash
# Initialize git repos and push all 11 projects to GitHub

set -e

cd /root/.openclaw/workspace/mobile_projects

echo "========================================="
echo "INITIALIZING GIT REPOSITORIES"
echo "========================================="

PROJECTS=(
    "dusty-wallet"
    "uncleshield-av"
    "reggiestarr-pos"
    "cream"
    "milkman-game"
    "leche-game"
    "amhud-supplies"
    "tappylewis"
    "secretarial-pool"
    "psdepot-supplies"
    "depotcrm"
)

for project in "${PROJECTS[@]}"; do
    echo ""
    echo "Processing: $project"
    echo "-----------------------------------------"
    
    cd "$project"
    
    # Initialize git if not exists
    if [ ! -d .git ]; then
        git init
        git add .
        git commit -m "Initial commit: Android project v1.0"
        echo "✅ Git initialized"
    else
        echo "✅ Git already initialized"
    fi
    
    # Create remote repo on GitHub
    if ! git remote get-url origin > /dev/null 2>&1; then
        echo "Creating GitHub repo hcindus/$project..."
        if gh repo create "hcindus/$project" --private --source=. --remote=origin --push 2>/dev/null; then
            echo "✅ GitHub repo created and pushed"
        else
            echo "⚠️  Repo may already exist, trying to push..."
            git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null || echo "⚠️  Push failed, may need manual setup"
        fi
    else
        echo "✅ Remote already configured"
        git push origin main 2>/dev/null || git push origin master 2>/dev/null || echo "⚠️  Push failed"
    fi
    
    cd ..
done

echo ""
echo "========================================="
echo "ALL PROJECTS PROCESSED!"
echo "========================================="
echo ""
echo "GitHub Repositories:"
for project in "${PROJECTS[@]}"; do
    echo "- https://github.com/hcindus/$project"
done
echo ""
echo "Next steps:"
echo "1. Build APKs with Android Studio"
echo "2. Create releases on GitHub"
echo "3. Upload APK files to releases"
