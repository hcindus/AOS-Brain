#!/bin/bash
# RS-79 POS System - Docker Deployment Script
# Usage: ./scripts/deploy-docker.sh [environment]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-production}
PROJECT_NAME="rs79"
BACKUP_DIR="/backup/rs79"

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    command -v docker >/dev/null 2>&1 || error "Docker is required but not installed"
    command -v docker-compose >/dev/null 2>&1 || error "Docker Compose is required but not installed"
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            warn ".env file not found. Copying from .env.example"
            cp .env.example .env
            warn "Please edit .env file with your actual values before continuing"
            exit 1
        else
            error ".env file not found and .env.example is missing"
        fi
    fi
    
    log "Prerequisites check passed"
}

# Create backup
create_backup() {
    log "Creating database backup..."
    
    mkdir -p "$BACKUP_DIR"
    BACKUP_FILE="$BACKUP_DIR/backup-$(date +%Y%m%d-%H%M%S).sql"
    
    # Backup PostgreSQL if running
    if docker-compose ps postgres | grep -q "Up"; then
        docker-compose exec -T postgres pg_dump -U rs79 rs79 > "$BACKUP_FILE" || warn "Backup failed, continuing..."
        log "Backup created: $BACKUP_FILE"
    else
        warn "PostgreSQL not running, skipping backup"
    fi
}

# Deploy application
deploy() {
    log "Starting deployment for environment: $ENVIRONMENT"
    
    # Pull latest changes if in git repo
    if [ -d ".git" ]; then
        log "Pulling latest changes..."
        git pull origin main || warn "Git pull failed, continuing with local files"
    fi
    
    # Build and start services
    log "Building Docker images..."
    docker-compose build --no-cache
    
    log "Starting services..."
    docker-compose up -d
    
    # Wait for database to be ready
    log "Waiting for database to be ready..."
    sleep 10
    
    # Run database migrations
    log "Running database migrations..."
    docker-compose exec -T app npx prisma migrate deploy || warn "Migration may have failed"
    
    # Health check
    log "Performing health check..."
    sleep 5
    
    if docker-compose ps app | grep -q "Up"; then
        log "Application is running successfully"
        
        # Show status
        docker-compose ps
        
        log "Deployment completed successfully!"
        log "Application should be available at: http://localhost:3000"
    else
        error "Application failed to start. Check logs with: docker-compose logs"
    fi
}

# Cleanup old backups and images
cleanup() {
    log "Cleaning up old resources..."
    
    # Remove old backups (keep last 7 days)
    find "$BACKUP_DIR" -name "backup-*.sql" -mtime +7 -delete 2>/dev/null || true
    
    # Remove unused Docker images
    docker image prune -f || true
    
    log "Cleanup completed"
}

# Main execution
main() {
    log "=== RS-79 POS System Docker Deployment ==="
    
    cd "$(dirname "$0")/.."
    
    check_prerequisites
    create_backup
    deploy
    cleanup
    
    log "Deployment finished successfully!"
}

# Run main function
main "$@"