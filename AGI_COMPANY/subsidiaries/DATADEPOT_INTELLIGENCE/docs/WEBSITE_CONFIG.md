# DataDepot Intelligence — Website Configuration

## Subdomain Setup

### Nginx Configuration Required

File: `/etc/nginx/sites-available/data.psdepot.com`

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name data.psdepot.com;
    
    root /var/www/data.psdepot.com;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    # API endpoint for data (future)
    location /api {
        proxy_pass http://localhost:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Deployment Steps

1. Create directory:
```bash
mkdir -p /var/www/data.psdepot.com
```

2. Copy web files:
```bash
cp /root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DATADEPOT_INTELLIGENCE/web/index.html /var/www/data.psdepot.com/
```

3. Enable site:
```bash
ln -s /etc/nginx/sites-available/data.psdepot.com /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

4. SSL Certificate:
```bash
certbot --nginx -d data.psdepot.com
```

### DNS Configuration

Add A record:
- `data.psdepot.com` → `5.161.41.79` (Miles.cloud VPS IP)

### Current Status
- ✅ HTML files created
- ⏳ Nginx config (requires elevated permissions)
- ⏳ DNS record (requires DNS access)
- ⏳ SSL certificate (requires DNS to propagate)

### Alternative: Deploy to Existing Domain
If subdomain setup is delayed, can deploy to:
- `psdepot.com/datadepot/` (subdirectory)
- `myl0nr0s.cloud/datadepot/` (alternate domain)

---
*Config v1.0 — 2026-04-29*
