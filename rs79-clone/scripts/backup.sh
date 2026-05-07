#!/bin/bash
# RS-79 POS System - Backup Script
# Usage: ./scripts/backup.sh [retention_days]

set -e

# Configuration
BACKUP_DIR="/backup/rs79"
DB_NAME="rs79"
DB_USER="rs79"
RETENTION_DAYS=${1:-30}
DATE=$(date +%Y%m%d-%H%M%S)

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Database backup
backup_database() {
    log "Backing up database..."
    
    BACKUP_FILE="$BACKUP_DIR/db-backup-$DATE.sql"
    
    # Try PostgreSQL first
    if command -v pg_dump &> /dev/null; then
        pg_dump -U "$DB_USER" -d "$DB_NAME" > "$BACKUP_FILE" 2>/dev/null && \
            gzip "$BACKUP_FILE" && \
            log "Database backup created: ${BACKUP_FILE}.gz" || \
            warn "PostgreSQL backup failed"
    elif command -v sqlite3 &> /dev/null; then
        # SQLite fallback
        DB_PATH="${INSTALL_DIR:-/opt/rs79}/prisma/dev.db"
        if [ -f "$DB_PATH" ]; then
            sqlite3 "$DB_PATH" ".backup '$BACKUP_FILE'" && \
                gzip "$BACKUP_FILE" && \
                log "SQLite backup created: ${BACKUP_FILE}.gz" || \
                warn "SQLite backup failed"
        fi
    fi
}

# Application files backup
backup_files() {
    log "Backing up application files..."
    
    BACKUP_FILE="$BACKUP_DIR/files-backup-$DATE.tar.gz"
    
    tar -czf "$BACKUP_FILE" \
        -C "${INSTALL_DIR:-/opt/rs79}" \
        --exclude='node_modules' \
        --exclude='.next' \
        --exclude='logs' \
        --exclude='*.log' \
        . 2>/dev/null && \
        log "Files backup created: $BACKUP_FILE" || \
        warn "Files backup failed"
}

# Environment backup
backup_env() {
    log "Backing up environment configuration..."
    
    BACKUP_FILE="$BACKUP_DIR/env-backup-$DATE.tar.gz"
    
    tar -czf "$BACKUP_FILE" \
        -C "${INSTALL_DIR:-/opt/rs79}" \
        .env \
        nginx/ \
        systemd/ 2>/dev/null && \
        log "Environment backup created: $BACKUP_FILE" || \
        warn "Environment backup failed"
}

# Cleanup old backups
cleanup_old_backups() {
    log "Cleaning up backups older than $RETENTION_DAYS days..."
    
    find "$BACKUP_DIR" -name "*.gz" -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
    find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
    
    log "Old backups cleaned up"
}

# Main
main() {
    log "=== RS-79 Backup Starting ==="
    
    backup_database
    backup_files
    backup_env
    cleanup_old_backups
    
    # Show backup summary
    log "=== Backup Summary ==="
    ls -lh "$BACKUP_DIR" | tail -n +2
    
    log "=== Backup Complete ==="
}

main "$@"