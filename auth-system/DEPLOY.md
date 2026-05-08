# Deployment Guide - Secure Auth System

## Quick Deploy Test

```bash
cd auth-system
npm install
npm run setup
npm run dev
```

Visit: http://localhost:3000

## Production Deployment

### 1. Environment Setup

Copy `.env.example` to `.env` and configure:

```bash
NODE_ENV=production
FRONTEND_URL=https://yourdomain.com
PORT=3000

# Use Redis for distributed rate limiting
REDIS_URL=redis://your-redis-host:6379

# Generate strong secrets
JWT_ACCESS_SECRET=$(openssl rand -hex 32)
JWT_REFRESH_SECRET=$(openssl rand -hex 32)
BCRYPT_PEPPER=$(openssl rand -hex 32)
```

### 2. SSL/TLS (Required)

Use reverse proxy (nginx) for HTTPS:

```nginx
server {
    listen 443 ssl http2;
    server_name auth.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. PM2 Process Manager

```bash
npm install -g pm2
pm2 start backend/server.js --name auth-api
pm2 save
pm2 startup
```

### 4. Database Backup

```bash
# Daily backup cron job
0 2 * * * sqlite3 /path/to/auth.db ".backup '/backups/auth-$(date +\%Y\%m\%d).db'"
```

## Testing Security

```bash
# Run security tests
npm test

# Manual test checklist:
# [ ] Registration with breached password → Rejected
# [ ] 6 failed logins → Account locked
# [ ] No CSRF token → Request rejected
# [ ] SQL injection in email → Sanitized
# [ ] Password reset token → Expires after 1 hour
# [ ] Refresh token reuse → All sessions revoked
```

## Integration with Existing Sites

Add to your existing site:

```html
<script src="https://auth.yourdomain.com/assets/auth.js"></script>
<script>
// Protected page check
if (!AuthAPI.isAuthenticated()) {
    window.location.href = 'https://auth.yourdomain.com/';
}
</script>
```

## Monitoring

Check logs:
```bash
tail -f logs/audit.log | grep FAILED
```

Alert on:
- Multiple failed logins from same IP
- Password reset abuse
- New device logins for existing users
