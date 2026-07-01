#!/bin/bash
REPOS=(
  "." "AGI_COMPANY" "AGI_COMPANY/subsidiaries/CREAM" "Cream" "DepotChaos" "Dusty" "MetaClaw" "MilkMan-Game" 
  "aocros" "aocros/products/agentverse" "aocros/products/aurora_lite_v2" "aocros/products/aurora_lite_v3"
  "aocros/products/cobra_ros" "aocros/products/myl0n_ros" "aocros/products/myl1n_ros" "aocros/products/myl2n_ros"
  "aocros/products/myl3n_ros" "aocros/products/myl4n_ros" "aocros/products/myl5n_ros" "aocros/products/myl6n_ros"
  "aocros/products/patricia_ros" "aocros/products/prometheus_ros" "claw-code"
  "mobile_projects/amhud-supplies" "mobile_projects/cream" "mobile_projects/depotcrm" "mobile_projects/dusty-wallet"
  "mobile_projects/leche-game" "mobile_projects/milkman-game" "mobile_projects/psdepot-supplies" 
  "mobile_projects/reggiestarr-pos" "mobile_projects/secretarial-pool" "mobile_projects/tappylewis"
  "mobile_projects/uncleshield-av" "myl0nr0s.cloud" "psdepot" "psdepot-landing" "reggiestarr-pos"
  "rs79-source" "tappylewis.cloud" "wiki"
)

echo "=== GIT STATUS CHECK ==="
echo "Timestamp: $(date -u +"%Y-%m-%d %H:%M UTC")"
echo ""

for repo in "${REPOS[@]}"; do
  if [ -d "$repo/.git" ]; then
    cd "$repo" || continue
    changes=$(git status --porcelain 2>/dev/null | wc -l)
    ahead=$(git rev-list --left-right --count origin...HEAD 2>/dev/null | awk '{print $2}')
    if [ -z "$ahead" ]; then ahead=0; fi
    if [ "$changes" -gt 0 ] || [ "$ahead" -gt 0 ]; then
      echo "REPO: $repo (uncommitted: $changes, unpushed: $ahead)"
    fi
    cd - > /dev/null 2>&1
  fi
done
