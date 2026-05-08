#!/bin/bash
# 📦 Database Backup Script
# Backs up critical databases daily with timestamped archives
# Run via cron: 0 2 * * * /root/.openclaw/workspace/scripts/db_backup.sh

BACKUP_DIR="/root/.openclaw/workspace/backups/databases"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/var/log/db_backup.log"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Databases to backup
DBS=(
    "/root/.openclaw/workspace/datadepot/leads.db"
    "/root/.openclaw/workspace/data/factory/dark_factory.db"
    "/root/.openclaw/workspace/data/depot_chaos/unified.db"
    "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DATADEPOT_INTELLIGENCE/database/datadepot.db"
    "/root/.openclaw/workspace/aocros/desks/pipeline/shared/pipeline.db"
    "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
)

echo "[$TIMESTAMP] Starting database backup..." >> "$LOG_FILE"

for db in "${DBS[@]}"; do
    if [ -f "$db" ]; then
        db_name=$(basename "$db" .db)
        backup_file="$BACKUP_DIR/${db_name}_${TIMESTAMP}.db"
        
        # Use SQLite backup command for consistency
        sqlite3 "$db" ".backup '$backup_file'" 2>/dev/null
        
        if [ $? -eq 0 ]; then
            # Compress the backup
            gzip "$backup_file"
            echo "  ✓ Backed up: $db_name" >> "$LOG_FILE"
        else
            # Fallback to cp if sqlite3 backup fails
            cp "$db" "$backup_file" && gzip "$backup_file"
            echo "  ⚠ Copied (sqlite backup failed): $db_name" >> "$LOG_FILE"
        fi
    fi
done

# Cleanup old backups (keep last 14 days)
find "$BACKUP_DIR" -name "*.db.gz" -mtime +14 -delete 2>/dev/null

# Report
backup_count=$(ls -1 "$BACKUP_DIR"/*.db.gz 2>/dev/null | wc -l)
echo "[$TIMESTAMP] Backup complete. Total backups: $backup_count" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
