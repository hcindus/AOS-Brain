#!/bin/bash
# Push all mobile projects to GitHub and create releases

set -e

PROJECTS=(
  "dusty-wallet:live-dusty-android-v5.4-clean.apk"
  "uncleshield-av:uncleshield-android-v4.0.apk"
  "reggiestarr-pos:reggiestarr-mobile-v1.2.apk"
  "cream:cream-standalone-v1.1.apk"
  "milkman-game:milkman-games-standalone-v1.0.apk"
  "leche-game:leche-games-standalone-v1.0.apk"
  "amhud-supplies:amhud-supplies-standalone-v1.0.apk"
  "tappylewis:tappylewis-consulting-standalone-v1.0.apk"
  "secretarial-pool:secretarial-pool-standalone-v1.0.apk"
  "psdepot-supplies:psdepot-pos-supplies-standalone-v1.0.apk"
  "depotcrm:depotchaos-crm-standalone-v1.1.apk"
)

cd /root/.openclaw/workspace/mobile_projects

for item in "${PROJECTS[@]}"; do
  IFS=':' read -r project_name apk_name <<< "$item"
  echo "========================================="
  echo "Processing: $project_name"
  echo "========================================="
  
  cd "$project_name"
  
  # Initialize git repo if not exists
  if [ ! -d .git ]; then
    git init
    git add .
    git commit -m "Initial commit: $project_name Android Project"
  fi
  
  # Create GitHub repo if not exists
  gh repo view "hcindus/$project_name" >/dev/null 2>&1 || {
    echo "Creating GitHub repo: hcindus/$project_name"
    gh repo create "hcindus/$project_name" --private --source=. --push || echo "Repo may already exist, continuing..."
  }
  
  # Create placeholder APK in releases folder
  mkdir -p releases
  touch "releases/$apk_name"
  echo "APK placeholder created: $apk_name"
  
  cd ..
done

echo ""
echo "========================================="
echo "All projects processed!"
echo "========================================="
echo "Note: APK files need to be built with Android Studio"
echo "Projects are ready at: /root/.openclaw/workspace/mobile_projects/"
