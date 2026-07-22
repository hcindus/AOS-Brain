#!/bin/bash
# Setup script for weekly knowledge base auto-crawl

echo "Setting up weekly auto-crawl for psdepot.com knowledge base..."

# Create log directory
sudo mkdir -p /var/log/psdepot
sudo chown root:root /var/log/psdepot

# Add cron job
CRON_JOB="0 2 * * 0 /usr/bin/python3 /root/.openclaw/workspace/scripts/auto_crawl_rag.py crawl >> /var/log/psdepot/crawl.log 2>&1"

# Check if already exists
if sudo crontab -l | grep -q "auto_crawl_rag.py"; then
    echo "Cron job already exists. Skipping..."
else
    # Add to crontab
    (sudo crontab -l 2>/dev/null; echo "$CRON_JOB") | sudo crontab -
    echo "Cron job added: Weekly crawl every Sunday at 2am"
fi

# Show current crontab
echo ""
echo "Current cron jobs:"
sudo crontab -l | grep psdepot || echo "No psdepot jobs found"

echo ""
echo "Setup complete!"
echo "Manual run: sudo python3 /root/.openclaw/workspace/scripts/auto_crawl_rag.py crawl"
echo "Logs: /var/log/psdepot/crawl.log"