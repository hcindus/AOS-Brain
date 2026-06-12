#!/bin/bash
# Dual SMTP Configuration Script
# Routes emails based on priority:
#   - SendGrid: Critical (leads, alerts, sales)
#   - Hostinger: Bulk (cron notifications)

SENDGRID_API_KEY="${1:-YOUR_SENDGRID_API_KEY}"
SENDGRID_USER="apikey"

if [ "$SENDGRID_API_KEY" = "YOUR_SENDGRID_API_KEY" ]; then
    echo "Usage: $0 <sendgrid_api_key>"
    echo "Please provide your SendGrid API key"
    exit 1
fi

echo "Configuring dual SMTP system..."

# Create SendGrid password map
cat > /etc/postfix/sasl_passwd.sendgrid << EOF
[smtp.sendgrid.net]:587 $SENDGRID_USER:$SENDGRID_API_KEY
EOF

# Create sender-based transport map
cat > /etc/postfix/sender_transport << EOF
# Critical emails → SendGrid
/^miles@myl0nr0s\.cloud$/   sendgrid:
/^captain@.*$/               sendgrid:
/^alerts@.*$/                sendgrid:
/^sales@.*$/                 sendgrid:
/^leads@.*$/                 sendgrid:

# Default → Hostinger (bulk/low-priority)
EOF

# Postfix master.cf - Add sendgrid transport
cat >> /etc/postfix/master.cf << 'EOF'

# SendGrid transport
sendgrid unix -       -       n       -       -       smtp
    -o syslog_name=postfix-sendgrid
    -o smtp_host_lookup=dns
    -o smtp_tls_wrappermode=no
    -o smtp_tls_security_level=encrypt
    -o smtp_sasl_auth_enable=yes
    -o smtp_sasl_password_maps=hash:/etc/postfix/sasl_passwd.sendgrid
    -o smtp_sasl_security_options=noanonymous
    -o smtp_sender_dependent_authentication=yes
EOF

# Update main.cf for sender-based routing
cat >> /etc/postfix/main.cf << 'EOF'

# Dual SMTP Configuration
sender_dependent_relayhost_maps = hash:/etc/postfix/sender_transport
smtp_sender_dependent_authentication = yes
transport_maps = hash:/etc/postfix/transport

# SendGrid-specific settings (for sendgrid transport)
sendgrid_destination_rate_delay = 5s
sendgrid_destination_concurrency_limit = 5
EOF

# Create transport map
cat > /etc/postfix/transport << EOF
sendgrid    smtp:[smtp.sendgrid.net]:587
*           smtp:[smtp.hostinger.com]:587
EOF

# Hash the maps
postmap /etc/postfix/sasl_passwd.sendgrid
postmap /etc/postfix/sender_transport
postmap /etc/postfix/transport

echo "✅ Dual SMTP configuration complete!"
echo ""
echo "Email routing:"
echo "  - SendGrid: miles@myl0nr0s.cloud, alerts, sales, leads"
echo "  - Hostinger: All other (cron notifications, bulk)"
echo ""
echo "Reloading Postfix..."
/usr/sbin/postfix reload

echo "✅ Done! Test with:"
echo "  echo 'Test' | mail -s 'Critical Alert' miles@myl0nr0s.cloud"
