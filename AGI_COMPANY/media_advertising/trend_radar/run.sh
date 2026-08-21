#!/bin/bash
# Trend Radar daily runner
set -e
cd /root/.openclaw/workspace/AGI_COMPANY/media_advertising/trend_radar
exec ./.venv/bin/python trend_radar.py
