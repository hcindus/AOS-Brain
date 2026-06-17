#!/bin/bash
# Deploy Performance Supply Depot website to Hostinger

API_KEY="ZshPCsKTXRYn92Fepo5olzkAsEjwP8gi27MIH5g1522689b1"
DOMAIN="performancesupplydepot.com"

# Upload via FTP/SFTP (Hostinger uses standard FTP)
# Using lftp for recursive upload

echo "Deploying to Hostinger..."
echo "Domain: $DOMAIN"

# Check if lftp is available
if ! command -v lftp &> /dev/null; then
    echo "Installing lftp..."
    apt-get update -qq && apt-get install -y -qq lftp
fi

# Note: In production, this would use Hostinger's API or FTP
# For now, creating deployment package
echo "Creating deployment package..."
tar -czf ../deploy_$(date +%Y%m%d_%H%M%S).tar.gz .

echo "Deployment package created."
echo "Manual upload required to Hostinger control panel:"
echo "1. Log in to https://www.hostinger.com"
echo "2. Go to File Manager"
echo "3. Upload to public_html/"
echo ""
echo "Or use FTP:"
echo "Host: ftp.performancesupplydepot.com"
echo "User: [FTP_USER]"
echo "Pass: [FTP_PASS]"
