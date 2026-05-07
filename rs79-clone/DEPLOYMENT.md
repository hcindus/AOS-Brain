# RS-79 POS System - Deployment Guide

Complete deployment instructions for running RS-79 POS System in-house on VPS/Docker infrastructure.

---

## Quick Start

Choose your deployment method:

| Method | Use Case | Complexity |
|--------|----------|------------|
| **Docker Compose** | Single server, quick setup | Low |
| **VPS Bare Metal** | Production, maximum control | Medium |
| **Docker + SystemD** | Hybrid, auto-restart | Medium |

---

## Prerequisites

### Minimum System Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 2 GB | 4+ GB |
| Disk | 20 GB SSD | 50+ GB SSD |
| OS | Ubuntu 22.04 LTS | Ubuntu 24.04 LTS |
| Network | Static IP | Domain + SSL |

### Required Software

- **Node.js** 20+ (for bare metal)
- **PostgreSQL** 14+ (database)
- **Nginx** (reverse proxy)
- **Docker** + **Docker Compose** (for containerized)
- **Git** (for deployment)

---

## Method 1: Docker Compose (Recommended for Quick Start)

### 1. Clone the Repository

```bash
cd /opt
git clone https://github.com/agi-company/rs79-clone.git
cd rs79-clone
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your values
nano .env
```

**Required variables:**
```env
POSTGRES_PASSWORD=your-secure-password
NEXTAUTH_SECRET=$(openssl rand -base64 32)
JWT_SECRET=$(openssl rand -base64 32)
NEXTAUTH_URL=https://pos.yourdomain.com
```

### 3. Deploy

```bash
# Make script executable
chmod +x scripts/deploy-docker.sh

# Run deployment
./scripts/deploy-docker.sh
```

### 4. Verify

```bash
docker-compose ps
docker-compose logs -f app
```

---

## Method 2: VPS Bare Metal

### 1. Run Automated Setup

```bash
# From project root
chmod +x scripts/deploy-vps.sh
sudo ./scripts/deploy-vps.sh
```

This script will:
- Install all dependencies (Node.js, PostgreSQL, Nginx, Redis)
- Create system user `rs79`
- Setup PostgreSQL database
- Configure firewall (UFW) and fail2ban
- Deploy the application
- Setup Nginx reverse proxy
- Configure systemd service
- Setup log rotation

### 2. Configure Environment

```bash
sudo nano /opt/rs79/.env
```

Set your production values:
```env
DATABASE_URL=postgresql://rs79:your-password@localhost:5432/rs79?schema=public
NEXTAUTH_SECRET=your-super-secret-key
JWT_SECRET=your-jwt-secret
NEXTAUTH_URL=https://pos.yourdomain.com
```

### 3. Configure Domain & SSL

```bash
# Edit nginx config with your domain
sudo nano /etc/nginx/sites-available/rs79

# Get SSL certificate
sudo certbot --nginx -d pos.yourdomain.com

# Reload nginx
sudo systemctl reload nginx
```

### 4. Start Service

```bash
sudo systemctl start rs79
sudo systemctl enable rs79
```

### 5. Verify

```bash
rs79-manage status
rs79-manage logs
```

---

## Method 3: Hybrid (Docker + SystemD)

For automatic Docker restart and management:

```bash
# Create systemd service for Docker Compose
sudo tee /etc/systemd/system/rs79-docker.service > /dev/null <<EOF
[Unit]
Description=RS-79 POS System (Docker)
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/rs79
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
ExecReload=/usr/bin/docker-compose up -d

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable rs79-docker
sudo systemctl start rs79-docker
```

---

## Post-Deployment

### Create Initial Admin User

```bash
# For Docker
sudo docker-compose exec app npx prisma studio

# For VPS bare metal
cd /opt/rs79
sudo -u rs79 npx prisma studio
```

Access Prisma Studio at `http://your-server:5555` to add your first clerk/admin.

### Health Monitoring

```bash
# Run health check
./scripts/health-check.sh

# Setup cron for automated health checks
sudo tee /etc/cron.d/rs79-health > /dev/null <<EOF
*/5 * * * * root /opt/rs79/scripts/health-check.sh >/dev/null 2>&1
EOF
```

### Backup Strategy

```bash
# Manual backup
rs79-manage backup

# Automated daily backups
sudo tee /etc/cron.d/rs79-backup > /dev/null <<EOF
0 2 * * * rs79 /opt/rs79/scripts/backup.sh 7 >> /var/log/rs79/backup.log 2>&1
EOF
```

---

## Management Commands

### Docker Method

```bash
cd /opt/rs79

# View status
docker-compose ps

# View logs
docker-compose logs -f app
docker-compose logs -f postgres

# Restart
docker-compose restart

# Update
docker-compose pull
docker-compose up -d

# Database migrations
docker-compose exec app npx prisma migrate deploy
```

### VPS Method

```bash
# Using management script
rs79-manage start
rs79-manage stop
rs79-manage restart
rs79-manage status
rs79-manage logs
rs79-manage backup
rs79-manage update

# Using systemctl
sudo systemctl start rs79
sudo systemctl stop rs79
sudo systemctl restart rs79
sudo systemctl status rs79
sudo journalctl -u rs79 -f
```

---

## Security Checklist

- [ ] Change default passwords
- [ ] Enable firewall (UFW)
- [ ] Configure fail2ban
- [ ] Setup SSL/TLS certificates
- [ ] Restrict SSH access (key-only, non-standard port)
- [ ] Disable root login
- [ ] Setup automated security updates
- [ ] Configure backups
- [ ] Setup monitoring/alerting
- [ ] Enable audit logging

---

## Troubleshooting

### Application Won't Start

```bash
# Check logs
sudo journalctl -u rs79 -n 100 --no-pager

# For Docker
docker-compose logs app

# Check database connection
sudo -u rs79 psql $DATABASE_URL -c "SELECT 1"
```

### Database Connection Issues

```bash
# Verify PostgreSQL is running
sudo systemctl status postgresql

# Check connection
sudo -u postgres psql -c "\du"

# Reset password if needed
sudo -u postgres psql -c "ALTER USER rs79 WITH PASSWORD 'newpassword';"
```

### Nginx Issues

```bash
# Test configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log

# Verify upstream is accessible
curl http://localhost:3000/api/health
```

### Permission Issues

```bash
# Fix ownership
sudo chown -R rs79:rs79 /opt/rs79
sudo chmod 750 /opt/rs79

# Fix log permissions
sudo chown -R rs79:rs79 /var/log/rs79
```

---

## Migration from Abacus AI

### Data Export

1. Export data from current Abacus AI instance:
   - Clerks
   - Customers
   - Orders
   - Items

2. Convert to Prisma-compatible format

3. Import using Prisma:
```bash
npx prisma db seed
# or custom import script
```

### Parallel Running

Recommended approach:
1. Deploy RS-79 in parallel
2. Run both systems for 1-2 weeks
3. Gradually migrate users
4. Switch DNS when confident

---

## Files Reference

| File | Purpose | Location |
|------|---------|----------|
| `Dockerfile` | Container definition | Project root |
| `docker-compose.yml` | Multi-service stack | Project root |
| `systemd/rs79.service` | SystemD service unit | `/etc/systemd/system/` |
| `nginx/rs79.conf` | Nginx site config | `/etc/nginx/sites-available/` |
| `scripts/deploy-docker.sh` | Docker deployment | Run manually |
| `scripts/deploy-vps.sh` | VPS deployment | Run manually |
| `scripts/backup.sh` | Backup automation | Run manually or via cron |
| `scripts/health-check.sh` | Health monitoring | Run manually or via cron |

---

## Support

- **Documentation**: See `README.md` and source code comments
- **Issues**: GitHub Issues (if public repo)
- **Captain's Contact**: For AGI Company internal deployments

---

*Last Updated: 2026-05-07*
*Version: 1.0*
