#!/bin/bash
# RS-79 POS System - VPS Bare Metal Deployment Script
# Usage: ./scripts/deploy-vps.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
INSTALL_DIR="/opt/rs79"
LOG_DIR="/var/log/rs79"
BACKUP_DIR="/backup/rs79"
USER="rs79"
NODE_VERSION="20"

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root or with sudo"
    fi
}

# Install system dependencies
install_dependencies() {
    log "Installing system dependencies..."
    
    apt-get update
    apt-get install -y \
        curl \
        wget \
        git \
        build-essential \
        nginx \
        postgresql \
        postgresql-contrib \
        postgresql-client \
        redis-server \
        certbot \
        python3-certbot-nginx \
        fail2ban \
        ufw \
        logrotate \
        htop \
        vim \
        unzip || error "Failed to install dependencies"
    
    log "System dependencies installed"
}

# Install Node.js
install_nodejs() {
    log "Installing Node.js $NODE_VERSION..."
    
    if command -v node &> /dev/null; then
        CURRENT_NODE=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
        if [ "$CURRENT_NODE" -ge "$NODE_VERSION" ]; then
            info "Node.js $CURRENT_NODE is already installed"
            return 0
        fi
    fi
    
    curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash -
    apt-get install -y nodejs || error "Failed to install Node.js"
    
    # Install PM2 globally
    npm install -g pm2 || error "Failed to install PM2"
    
    log "Node.js and PM2 installed"
}

# Setup PostgreSQL
setup_postgresql() {
    log "Setting up PostgreSQL..."
    
    # Start PostgreSQL
    systemctl enable postgresql
    systemctl start postgresql
    
    # Create database and user
    sudo -u postgres psql << EOF || error "Failed to setup PostgreSQL"
CREATE USER rs79 WITH PASSWORD 'changeme-strong-password';
CREATE DATABASE rs79 OWNER rs79;
GRANT ALL PRIVILEGES ON DATABASE rs79 TO rs79;
\c rs79
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOF
    
    log "PostgreSQL configured"
}

# Create system user
create_user() {
    log "Creating system user..."
    
    if ! id "$USER" &>/dev/null; then
        useradd -r -s /bin/false -d "$INSTALL_DIR" -m "$USER" || error "Failed to create user"
    fi
    
    # Add user to www-data group for nginx
    usermod -a -G www-data "$USER"
    
    log "System user created"
}

# Setup application directory
setup_app_directory() {
    log "Setting up application directory..."
    
    # Create directories
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$LOG_DIR"
    mkdir -p "$BACKUP_DIR"
    mkdir -p "/var/www/certbot"
    
    # Set ownership
    chown -R $USER:$USER "$INSTALL_DIR"
    chown -R $USER:$USER "$LOG_DIR"
    chown -R $USER:$USER "$BACKUP_DIR"
    
    log "Application directory configured"
}

# Setup firewall
setup_firewall() {
    log "Configuring firewall..."
    
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow OpenSSH
    ufw allow 'Nginx Full'
    ufw allow 3000/tcp  # Allow direct access for testing
    
    ufw --force enable
    
    log "Firewall configured"
}

# Setup fail2ban
setup_fail2ban() {
    log "Setting up fail2ban..."
    
    cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true

[nginx-badbots]
enabled = true

[nginx-noscript]
enabled = true

[nginx-limit-req]
enabled = true
EOF
    
    systemctl enable fail2ban
    systemctl restart fail2ban
    
    log "fail2ban configured"
}

# Deploy application
deploy_application() {
    log "Deploying application..."
    
    # Copy application files
    if [ -d "/root/.openclaw/workspace/rs79-clone" ]; then
        rsync -av --exclude='node_modules' --exclude='.next' --exclude='.git' \
            /root/.openclaw/workspace/rs79-clone/ "$INSTALL_DIR/" || error "Failed to copy application files"
    else
        warn "Source directory not found. Please clone the repository to $INSTALL_DIR"
        exit 1
    fi
    
    # Set ownership
    chown -R $USER:$USER "$INSTALL_DIR"
    
    # Install dependencies and build
    cd "$INSTALL_DIR"
    sudo -u $USER npm ci || error "Failed to install npm dependencies"
    sudo -u $USER npx prisma generate || error "Failed to generate Prisma client"
    sudo -u $USER npm run build || error "Failed to build application"
    
    # Setup environment file
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            warn ".env file created from template. Please configure it!"
        fi
    fi
    
    log "Application deployed"
}

# Setup Nginx
setup_nginx() {
    log "Configuring Nginx..."
    
    # Copy nginx configuration
    if [ -f "$INSTALL_DIR/nginx/rs79.conf" ]; then
        cp "$INSTALL_DIR/nginx/rs79.conf" /etc/nginx/sites-available/rs79
        cp "$INSTALL_DIR/nginx/proxy_params" /etc/nginx/proxy_params
        
        # Enable site
        ln -sf /etc/nginx/sites-available/rs79 /etc/nginx/sites-enabled/
        rm -f /etc/nginx/sites-enabled/default
        
        # Test configuration
        nginx -t || error "Nginx configuration test failed"
        
        # Reload nginx
        systemctl reload nginx
    fi
    
    log "Nginx configured"
}

# Setup SSL certificate (Let's Encrypt)
setup_ssl() {
    log "Setting up SSL certificate..."
    
    # This will fail if domain is not properly configured, which is expected
    # The user should run certbot manually after DNS is configured
    warn "To setup SSL, run: certbot --nginx -d yourdomain.com"
    
    log "SSL setup deferred (run certbot manually)"
}

# Setup systemd service
setup_systemd() {
    log "Setting up systemd service..."
    
    if [ -f "$INSTALL_DIR/systemd/rs79.service" ]; then
        cp "$INSTALL_DIR/systemd/rs79.service" /etc/systemd/system/
        systemctl daemon-reload
        systemctl enable rs79
        log "Systemd service configured"
    fi
}

# Setup log rotation
setup_logrotate() {
    log "Setting up log rotation..."
    
    cat > /etc/logrotate.d/rs79 << EOF
$LOG_DIR/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0644 $USER $USER
    sharedscripts
    postrotate
        /bin/kill -HUP \$(cat /var/run/rs79.pid 2>/dev/null) 2>/dev/null || true
    endscript
}
EOF
    
    log "Log rotation configured"
}

# Create management script
create_manage_script() {
    log "Creating management script..."
    
    cat > /usr/local/bin/rs79-manage << 'SCRIPT'
#!/bin/bash
# RS-79 Management Script

case "$1" in
    start)
        systemctl start rs79
        ;;
    stop)
        systemctl stop rs79
        ;;
    restart)
        systemctl restart rs79
        ;;
    status)
        systemctl status rs79
        ;;
    logs)
        tail -f /var/log/rs79/app.log
        ;;
    backup)
        /opt/rs79/scripts/backup.sh
        ;;
    update)
        cd /opt/rs79 && git pull && npm ci && npm run build && systemctl restart rs79
        ;;
    *)
        echo "Usage: rs79-manage {start|stop|restart|status|logs|backup|update}"
        exit 1
        ;;
esac
SCRIPT
    
    chmod +x /usr/local/bin/rs79-manage
    
    log "Management script created: rs79-manage"
}

# Main deployment
main() {
    log "=== RS-79 POS System VPS Deployment ==="
    
    check_root
    install_dependencies
    install_nodejs
    create_user
    setup_postgresql
    setup_app_directory
    setup_firewall
    setup_fail2ban
    deploy_application
    setup_nginx
    setup_systemd
    setup_logrotate
    create_manage_script
    
    log "=== Deployment Complete ==="
    log ""
    log "Next steps:"
    log "1. Configure your domain DNS to point to this server"
    log "2. Edit /opt/rs79/.env with your production values"
    log "3. Run: certbot --nginx -d yourdomain.com (for SSL)"
    log "4. Start the service: systemctl start rs79"
    log "5. Check status: rs79-manage status"
    log ""
    log "Management commands:"
    log "  - rs79-manage start|stop|restart|status"
    log "  - rs79-manage logs"
    log "  - rs79-manage backup"
    log "  - rs79-manage update"
}

main "$@"