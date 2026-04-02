#!/bin/bash
# VERSION: 1.0.0
# UPDATED: 2026-04-02 04:08 UTC
# CHANGELOG: Initial auto-versioning script
#
# Auto Version Bump Script
# Updates VERSION_INDEX.md when files change

WORKSPACE="/root/.openclaw/workspace"
VERSION_FILE="$WORKSPACE/VERSION_INDEX.md"
LOG_FILE="$WORKSPACE/logs/version_bump.log"

mkdir -p $(dirname $LOG_FILE)

# Get current date/time for build
DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H%M')
BUILD="${DATE}.${TIME}"
DATETIME=$(date '+%Y-%m-%d %H:%M UTC')

# Check if VERSION_INDEX.md exists
if [ ! -f "$VERSION_FILE" ]; then
    echo "[$(date)] ERROR: VERSION_INDEX.md not found" >> "$LOG_FILE"
    exit 1
fi

# Update the global version in VERSION_INDEX.md
sed -i "s/Current: [0-9]\{4\}\.[0-9]\{2\}\.[0-9]\{2\}\.[0-9]\{4\}/Current: $BUILD/" "$VERSION_FILE"
sed -i "s/\(build \)[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\} [0-9]\{2\}:[0-9]\{2\} UTC/\1$DATETIME/" "$VERSION_FILE"

# Check if there are uncommitted changes
cd "$WORKSPACE"
if git status --porcelain | grep -q "^"; then
    # There are changes - version bump
    echo "[$(date)] Changes detected, build $BUILD" >> "$LOG_FILE"
    echo "$BUILD"
else
    echo "[$(date)] No changes" >> "$LOG_FILE"
    echo "no_change"
fi
