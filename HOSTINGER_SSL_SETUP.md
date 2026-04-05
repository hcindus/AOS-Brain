# Hostinger SSL Setup Guide

## Current Status
- **Site:** myl0nr0s.cloud
- **Current Server:** Python SimpleHTTPServer (HTTP only)
- **Issue:** No HTTPS/SSL certificate

## Solution: nginx + Let's Encrypt (Recommended)

### Step 1: Install nginx
```bash
sudo apt update
sudo apt install -y nginx
```

### Step 2: Configure nginx for myl0nr0s.cloud
```bash
sudo tee /etc/nginx/sites-available/myl0nr0s.cloud << 'EOF'
server {
    listen 80;
    server_name myl0nr0s.cloud www.myl0nr0s.cloud;
    
    root /root/.openclaw/workspace/aocros/AGI_COMPANY_WEBSITES/performance-supply-depot;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF
```

### Step 3: Enable site
```bash
sudo ln -sf /etc/nginx/sites-available/myl0nr0s.cloud /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 4: Install Certbot for Let's Encrypt
```bash
sudo apt install -y certbot python3-certbot-nginx
```

### Step 5: Obtain SSL Certificate
```bash
sudo certbot --nginx -d myl0nr0s.cloud -d www.myl0nr0s.cloud --agree-tos --non-interactive --email admin@myl0nr0s.cloud
```

### Step 6: Auto-renewal (automatic with certbot)
```bash
sudo systemctl status certbot.timer
```

### Step 7: Redirect HTTP to HTTPS
Certbot should add this automatically, but verify:
```bash
sudo tee /etc/nginx/sites-available/myl0nr0s.cloud << 'EOF'
server {
    listen 80;
    server_name myl0nr0s.cloud www.myl0nr0s.cloud;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name myl0nr0s.cloud www.myl0nr0s.cloud;
    
    ssl_certificate /etc/letsencrypt/live/myl0nr0s.cloud/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myl0nr0s.cloud/privkey.pem;
    
    root /root/.openclaw/workspace/aocros/AGI_COMPANY_WEBSITES/performance-supply-depot;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF
sudo nginx -t && sudo systemctl reload nginx
```

## Alternative: Hostinger hPanel (If using Hostinger shared hosting)

1. Log into Hostinger hPanel
2. Go to **Websites** → **myl0nr0s.cloud**
3. Click **SSL** in the left menu
4. Click **Install SSL Certificate**
5. Select **Let's Encrypt (Free)**
6. Click **Install**
7. Wait 5-10 minutes for propagation
8. Enable **Force HTTPS** redirect

## Verification

Test SSL after setup:
```bash
curl -I https://myl0nr0s.cloud
curl -I https://www.myl0nr0s.cloud
```

## Troubleshooting

### Port 80/443 already in use
```bash
sudo lsof -i :80
sudo lsof -i :443
sudo pkill -f "python.*SimpleHTTPServer"
sudo pkill -f "python.*http.server"
```

### Firewall blocks
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### Permission denied on root
```bash
# If nginx can't access /root/, move site:
sudo mkdir -p /var/www/myl0nr0s.cloud
sudo cp -r /root/.openclaw/workspace/aocros/AGI_COMPANY_WEBSITES/performance-supply-depot/* /var/www/myl0nr0s.cloud/
sudo chown -R www-data:www-data /var/www/myl0nr0s.cloud
```

## Post-SSL Checklist

- [ ] HTTPS working (https://myl0nr0s.cloud)
- [ ] HTTP redirects to HTTPS
- [ ] Stripe payment test successful
- [ ] Agent status page accessible
- [ ] SSL certificate auto-renewing

## Notes

- Let's Encrypt certificates expire every 90 days (auto-renewed by certbot)
- Webhooks will work after SSL is active
- Site flagged issue should resolve once HTTPS is enabled
