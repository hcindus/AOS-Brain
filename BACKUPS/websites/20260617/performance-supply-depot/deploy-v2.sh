#!/bin/bash
# Deploy PSDEPOT website to psdepot.com (Hostinger)
# Updated for automated deployment

set -e

API_KEY="ZshPCsKTXRYn92Fepo5olzkAsEjwP8gi27MIH5g1522689b1"
DOMAIN="psdepot.com"
WEBSITE_DIR="/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/website/performance-supply-depot"

echo "================================"
echo "🚀 PSDEPOT Deployment Script v2"
echo "================================"
echo "Domain: $DOMAIN"
echo "Source: $WEBSITE_DIR"
echo ""

# Check source exists
if [ ! -d "$WEBSITE_DIR" ]; then
    echo "❌ Error: Website directory not found at $WEBSITE_DIR"
    exit 1
fi

cd "$WEBSITE_DIR"

# Get latest git commit
COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
DATE=$(date '+%Y-%m-%d %H:%M UTC')

echo "📦 Preparing deployment..."
echo "   Git commit: $COMMIT"
echo "   Timestamp: $DATE"

# Create deployment archive
echo ""
echo "📦 Creating deployment archive..."
DEPLOY_FILE="/tmp/psdepot-deploy-$(date +%Y%m%d-%H%M%S).tar.gz"
tar -czf "$DEPLOY_FILE" \
    --exclude='.git' \
    --exclude='*.log' \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.env' \
    -C "$WEBSITE_DIR" .

echo "✅ Archive created: $DEPLOY_FILE"
echo "   Size: $(du -h "$DEPLOY_FILE" | cut -f1)"

echo ""
echo "📤 Upload Options:"
echo ""
echo "Option 1 - Hostinger File Manager (Recommended):"
echo "  1. Log in to: https://www.hostinger.com"
echo "  2. Go to Hosting → $DOMAIN → File Manager"
echo "  3. Navigate to: public_html/"
echo "  4. Upload: $DEPLOY_FILE"
echo "  5. Extract the archive"
echo ""
echo "Option 2 - FTP/SFTP:"
echo "  Server: $DOMAIN"
echo "  Port: 21 (FTP) or 22 (SFTP)"
echo "  User: Your Hostinger FTP username"
echo "  Pass: Your Hostinger FTP password"
echo "  Remote path: /public_html/"
echo ""
echo "Option 3 - SCP (requires SSH access):"
echo "  scp -r $WEBSITE_DIR/* user@$DOMAIN:/public_html/"
echo ""
echo "Option 4 - Git Push (if configured):"
echo "  cd $WEBSITE_DIR"
echo "  git push origin main"
echo ""

# Save deployment info
INFO_FILE="/tmp/psdepot-deploy-info.txt"
cat > "$INFO_FILE" << EOF
PSDEPOT Deployment Package
==========================
Date: $DATE
Git Commit: $COMMIT
Domain: $DOMAIN
Archive: $DEPLOY_FILE
Size: $(du -h "$DEPLOY_FILE" | cut -f1)
Files Included:
$(tar -tzf "$DEPLOY_FILE" | head -20)
...
EOF

echo ""
echo "📋 Deployment info saved to: $INFO_FILE"
echo ""
echo "🌐 Live URLs after deployment:"
echo "   https://$DOMAIN/"
echo "   https://$DOMAIN/cart.html"
echo "   https://$DOMAIN/products.html"
echo ""
echo "⚠️  IMPORTANT: Remember to start the payment server after deployment!"
echo "   systemctl start psdepot-payment"
echo ""
echo "✅ Deployment package ready!"
