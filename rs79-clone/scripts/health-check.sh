#!/bin/bash
# RS-79 POS System - Health Check Script
# Usage: ./scripts/health-check.sh

# Configuration
APP_URL="${NEXTAUTH_URL:-http://localhost:3000}"
HEALTH_ENDPOINT="/api/health"
LOG_FILE="/var/log/rs79/health-check.log"
ALERT_EMAIL="${ALERT_EMAIL:-admin@example.com}"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Health check function
check_app() {
    local url="$1"
    
    if command -v curl &> /dev/null; then
        response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
        if [ "$response" = "200" ]; then
            return 0
        fi
    elif command -v wget &> /dev/null; then
        if wget --spider --timeout=5 "$url" 2>/dev/null; then
            return 0
        fi
    fi
    
    return 1
}

check_database() {
    # Check if we can connect to PostgreSQL
    if command -v psql &> /dev/null; then
        if [ -n "$DATABASE_URL" ]; then
            # Extract connection info from DATABASE_URL
            psql "$DATABASE_URL" -c "SELECT 1" > /dev/null 2>&1 && return 0
        elif [ -f "/opt/rs79/.env" ]; then
            source /opt/rs79/.env 2>/dev/null
            psql "$DATABASE_URL" -c "SELECT 1" > /dev/null 2>&1 && return 0
        fi
    fi
    
    return 1
}

check_disk_space() {
    local threshold=90
    local usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    
    if [ "$usage" -lt "$threshold" ]; then
        return 0
    fi
    
    return 1
}

check_memory() {
    local threshold=90
    
    # Get memory usage percentage
    if command -v free &> /dev/null; then
        local total=$(free | grep Mem | awk '{print $2}')
        local used=$(free | grep Mem | awk '{print $3}')
        local usage=$((used * 100 / total))
        
        if [ "$usage" -lt "$threshold" ]; then
            return 0
        fi
    fi
    
    return 1
}

# Logging function
log() {
    local message="[$(date +'%Y-%m-%d %H:%M:%S')] $1"
    echo "$message"
    
    if [ -d "$(dirname "$LOG_FILE")" ]; then
        echo "$message" >> "$LOG_FILE"
    fi
}

# Alert function (customize as needed)
alert() {
    local subject="$1"
    local message="$2"
    
    log "ALERT: $subject - $message"
    
    # Send email if mail command available
    if command -v mail &> /dev/null; then
        echo "$message" | mail -s "$subject" "$ALERT_EMAIL" 2>/dev/null || true
    fi
    
    # Send to systemd journal if available
    if command -v systemd-cat &> /dev/null; then
        echo "$message" | systemd-cat -t rs79-health -p err 2>/dev/null || true
    fi
}

# Main health check
main() {
    local failed=0
    
    echo -e "${YELLOW}=== RS-79 Health Check ===${NC}"
    
    # Check application
    echo -n "Checking application... "
    if check_app "$APP_URL$HEALTH_ENDPOINT" || check_app "$APP_URL"; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${RED}FAILED${NC}"
        failed=1
        alert "RS-79 Application Down" "Application is not responding at $APP_URL"
    fi
    
    # Check database
    echo -n "Checking database... "
    if check_database; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${RED}FAILED${NC}"
        failed=1
        alert "RS-79 Database Issue" "Database connection failed"
    fi
    
    # Check disk space
    echo -n "Checking disk space... "
    if check_disk_space; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${RED}WARNING${NC}"
        alert "RS-79 Disk Space Warning" "Disk space usage is above 90%"
    fi
    
    # Check memory
    echo -n "Checking memory... "
    if check_memory; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${RED}WARNING${NC}"
        alert "RS-79 Memory Warning" "Memory usage is above 90%"
    fi
    
    echo
    if [ $failed -eq 0 ]; then
        echo -e "${GREEN}All checks passed!${NC}"
        exit 0
    else
        echo -e "${RED}Some checks failed!${NC}"
        exit 1
    fi
}

main "$@"