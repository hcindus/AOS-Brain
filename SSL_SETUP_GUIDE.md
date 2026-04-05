# SSL Setup Guide for myl0nr0s.cloud

## Current Status
- **HTTP:** ✅ Working (Port 80)
- **HTTPS:** ❌ Not configured
- **Server:** Python SimpleHTTPServer

## Quick Fix Options

### Option 1: Let's Encrypt (Recommended for Production)
```bash
# Install certbot
apt-get update
apt-get install -y certbot

# Get certificate
certbot certonly --standalone -d myl0nr0s.cloud

# Certificates will be at:
# /etc/letsencrypt/live/myl0nr0s.cloud/fullchain.pem
# /etc/letsencrypt/live/myl0nr0s.cloud/privkey.pem
```

### Option 2: Cloudflare (Easiest)
1. Sign up at cloudflare.com
2. Add myl0nr0s.cloud as a site
3. Change nameservers to Cloudflare
4. Enable "Always Use HTTPS"
5. SSL/TLS encryption mode: Flexible or Full

### Option 3: Self-Signed (Testing Only)
```bash
mkdir -p /root/.openclaw/workspace/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /root/.openclaw/workspace/ssl/private.key \
    -out /root/.openclaw/workspace/ssl/certificate.crt \
    -subj "/CN=myl0nr0s.cloud"
```

## Encrypted Webhooks Issue

The "encrypted webhooks" mentioned may be:
1. **HTTPS requirement** - Modern browsers block mixed content
2. **Webhook endpoints** - Need HTTPS for Stripe/webhook receivers
3. **Certificate validation** - Self-signed certs show warnings

## Solution

### Immediate (Use Cloudflare):
1. Point domain to Cloudflare
2. Enable proxy (orange cloud)
3. Force HTTPS redirect
4. Free SSL certificate automatically provided

### Production (Let's Encrypt + Nginx):
```bash
# Install nginx
apt-get install -y nginx

# Configure nginx with SSL
server {
    listen 443 ssl;
    server_name myl0nr0s.cloud;
    
    ssl_certificate /etc/letsencrypt/live/myl0nr0s.cloud/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myl0nr0s.cloud/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8000;
    }
}
```

## Testing

After setup:
```bash
curl -I https://myl0nr0s.cloud
# Should return: HTTP/2 200
```

---

**Recommendation:** Use Cloudflare for immediate SSL. It's free, instant, and handles DDoS protection.
