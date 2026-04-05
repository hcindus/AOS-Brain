#!/bin/bash
# SSL Setup Script for myl0nr0s.cloud

# Generate self-signed certificate for testing
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /root/.openclaw/workspace/ssl/private.key \
    -out /root/.openclaw/workspace/ssl/certificate.crt \
    -subj "/C=US/ST=California/L=Los Angeles/O=AGI Company/CN=myl0nr0s.cloud"

# Set permissions
chmod 600 /root/.openclaw/workspace/ssl/private.key
chmod 644 /root/.openclaw/workspace/ssl/certificate.crt

echo "Self-signed certificate created."
echo "Location: /root/.openclaw/workspace/ssl/"
echo ""
echo "To use in production, get certificate from:"
echo "  - Let's Encrypt (free)"
echo "  - Cloudflare (free with proxy)"
echo "  - Your domain registrar"
