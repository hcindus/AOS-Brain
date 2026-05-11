#!/bin/bash
# PSD/DepotChaos API Configuration Backup
# Date: 2026-05-11

# Service files
DEPOTCHAOS_SERVICE="/etc/systemd/system/depotchaos-api.service"
PSD_API_SERVICE="/etc/systemd/system/psd-api.service"
NGINX_CONFIG="/etc/nginx/sites-enabled/psdepot.com"

# Database files
UNIFIED_DB="/root/.openclaw/workspace/data/depot_chaos/unified.db"
DEPOTCHAOS_DB="/root/.openclaw/workspace/DepotChaos/depot_chaos.db"

# API files
PSD_API="/root/.openclaw/workspace/datadepot/web/psd_api.py"
DEPOTCHAOS_API="/root/.openclaw/workspace/datadepot/web/depotchaos_fastapi.py"

# Web files
PSD_PERFORMANCE="/root/.openclaw/workspace/datadepot/web/psd_performance.html"
PSD_DASHBOARD="/root/.openclaw/workspace/datadepot/web/psd_dashboard.html"

# Backup directory
BACKUP_DIR="/root/.openclaw/workspace/datadepot/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Copy service files
cp "$DEPOTCHAOS_SERVICE" "$BACKUP_DIR/" 2>/dev/null
cp "$PSD_API_SERVICE" "$BACKUP_DIR/" 2>/dev/null
cp "$NGINX_CONFIG" "$BACKUP_DIR/" 2>/dev/null

# Copy database backups (sqlite3 .backup command)
sqlite3 "$UNIFIED_DB" ".backup $BACKUP_DIR/unified.db.backup" 2>/dev/null
sqlite3 "$DEPOTCHAOS_DB" ".backup $BACKUP_DIR/depot_chaos.db.backup" 2>/dev/null

# Copy API files
cp "$PSD_API" "$BACKUP_DIR/"
cp "$DEPOTCHAOS_API" "$BACKUP_DIR/"
cp "$PSD_PERFORMANCE" "$BACKUP_DIR/"
cp "$PSD_DASHBOARD" "$BACKUP_DIR/"

echo "Backup completed: $BACKUP_DIR"
echo ""
echo "To restore services:"
echo "  systemctl restart depotchaos-api"
echo "  systemctl restart psd-api"
echo "  nginx -t && systemctl reload nginx"
