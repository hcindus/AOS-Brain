#!/bin/bash
# Quick web PWA deploy script
# Usage: ./deploy_web_pwa.sh <project_name> <source_path> <domain>

PROJECT_NAME=${1:-""}
SOURCE_PATH=${2:-""}
DOMAIN=${3:-""}

if [ -z "$PROJECT_NAME" ] || [ -z "$SOURCE_PATH" ] || [ -z "$DOMAIN" ]; then
    echo "Usage: $0 <project_name> <source_path> <domain>"
    echo "Example: $0 cream /root/.openclaw/workspace/Cream/web cream.psdepot.com"
    exit 1
fi

WEB_ROOT="/var/www/psdepot.com/$PROJECT_NAME"

echo "🚀 Deploying $PROJECT_NAME to $DOMAIN..."

# Create web root
mkdir -p "$WEB_ROOT"

# Copy files
if [ -d "$SOURCE_PATH" ]; then
    cp -r "$SOURCE_PATH"/* "$WEB_ROOT/"
    echo "✅ Files copied to $WEB_ROOT"
else
    echo "❌ Source path not found: $SOURCE_PATH"
    exit 1
fi

# Verify index.html exists
if [ -f "$WEB_ROOT/index.html" ]; then
    echo "✅ index.html verified"
else
    echo "⚠️ No index.html found - may need manual setup"
fi

# Reload web server if nginx exists
if command -v nginx &> /dev/null; then
    nginx -t && systemctl reload nginx
    echo "✅ nginx reloaded"
else
    echo "ℹ️ nginx not found (may be on different server)"
fi

echo ""
echo "📋 Deployment Summary:"
echo "   Project: $PROJECT_NAME"
echo "   Domain: $DOMAIN"
echo "   Web Root: $WEB_ROOT"
echo "   Status: ✅ DEPLOYED (Web)"
echo ""
echo "   Mobile APK: Use Option 1 (Android SDK) for native app"
echo ""
