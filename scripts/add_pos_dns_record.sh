#!/bin/bash
# DNS Record Adder for psdepot.com
# Requires DNS provider API credentials

# For dns-parking.com, you typically need to:
# 1. Log into your domain registrar (where psdepot.com was purchased)
# 2. Find DNS Management / DNS Records section
# 3. Add an A record:
#    Name: pos
#    Type: A
#    Value: 31.97.6.40
#    TTL: 3600 (or default)

# Alternative: If you have Cloudflare or another DNS provider:
# export CF_API_TOKEN="your_token_here"
# export CF_ZONE_ID="your_zone_id"
# curl -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
#   -H "Authorization: Bearer $CF_API_TOKEN" \
#   -H "Content-Type: application/json" \
#   --data '{"type":"A","name":"pos.psdepot.com","content":"31.97.6.40","ttl":3600}'

echo "========================================"
echo "DNS RECORD NEEDED FOR pos.psdepot.com"
echo "========================================"
echo ""
echo "Record Type: A"
echo "Name: pos"
echo "Value: 31.97.6.40"
echo "TTL: 3600 (1 hour)"
echo ""
echo "Current nameservers: ns1.dns-parking.com, ns2.dns-parking.com"
echo ""
echo "To add this record:"
echo "1. Log into your domain registrar where psdepot.com was purchased"
echo "2. Navigate to DNS Management / DNS Zone Editor"
echo "3. Add the A record shown above"
echo "4. Wait 5-10 minutes for propagation"
echo "5. Run: sudo certbot --nginx -d pos.psdepot.com"
echo "========================================"
