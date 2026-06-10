#!/bin/bash
# CA SOS Scraper V3 - Daily Cron Runner
# Runs at 6:00 AM UTC daily

/usr/bin/python3 /root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/enrichment/ca_sos_scraper_v3.py >> /var/log/aos/ca_sos_scraper_v3.log 2>&1
