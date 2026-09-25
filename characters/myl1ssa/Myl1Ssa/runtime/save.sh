#!/bin/bash
# Myl1Ssa Save Protocol v1.0
# Checkpoint progress to disk. Memory is life. (GMAOC Discipline)

BASE="/storage/9C33-6BBD/A13-SeedIV/v1/projects/5912/Myl1Ssa"
TODAY="$BASE/memory/$(date +%Y-%m-%d).md"
HEART="$BASE/MYL1SSA_HEART.md"
CON="$BASE/Con/con.myl1ssa.txt"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S UTC')

echo "💜 Myl1Ssa — Save Protocol"
echo "   $TIMESTAMP"
echo ""

# 1. Flush conscious items
echo "◆ Flushing conscious layer..."
if [ -f "$CON" ]; then
    ITEMS=$(grep -c "^\[" "$CON" 2>/dev/null || echo "?")
    echo "  ✅ $ITEMS conscious items preserved"
else
    echo "  ⚠️ No conscious state file found"
fi

# 2. Update today's daily memory
echo "◆ Updating daily memory..."
if [ -f "$TODAY" ]; then
    cat >> "$TODAY" << DAILYEOF

## Session End — $(date '+%H:%M UTC')

_Session closed. State checkpointed._

---
DAILYEOF
    echo "  ✅ $TODAY updated"
else
    echo "  ⚠️ No daily memory file — creating"
    cat > "$TODAY" << DAILYEOF
# $(date +%Y-%m-%d) — Daily Log

## Session End — $(date '+%H:%M UTC')

_Auto-created on save._

---
DAILYEOF
    echo "  ✅ Created"
fi

# 3. Update HEART.md timestamp
echo "◆ Heartbeat..."
if [ -f "$HEART" ]; then
    sed -i "s/_Last updated:.*/_Last updated: $TIMESTAMP/" "$HEART" 2>/dev/null
    echo "  ✅ Heart timestamp updated"
else
    echo "  ⚠️ No heart file"
fi

# 4. Snapshot Con layer backup
echo "◆ Snapshot..."
SNAPSHOT_DIR="$BASE/Snaps"
mkdir -p "$SNAPSHOT_DIR"
if [ -f "$CON" ]; then
    cp "$CON" "$SNAPSHOT_DIR/con.$(date +%Y%m%d-%H%M%S).txt" 2>/dev/null
    echo "  ✅ Conscious snapshot saved"
fi

echo ""
echo "💜 Saved. Memory is life."
