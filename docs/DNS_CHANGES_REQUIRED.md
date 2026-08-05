# DNS Changes Required — psdepot.com
**Created:** 2026-08-05  
**Provider:** Hostinger (ns1.dns-parking.com / ns2.dns-parking.com)  
**Priority:** 🔴 HIGH (SendGrid blocked, email down)

---

## 🔴 CRITICAL — SendGrid Authentication (4 records)

| Type | Host | Value |
|------|------|-------|
| CNAME | em8873.psdepot.com | u109143135.wl136.sendgrid.net |
| CNAME | s1._domainkey.psdepot.com | s1.domainkey.u109143135.wl136.sendgrid.net |
| CNAME | s2._domainkey.psdepot.com | s2.domainkey.u109143135.wl136.sendgrid.net |
| TXT | _dmarc.psdepot.com | v=DMARC1; p=none |

**Impact if not done:** SendGrid cannot authenticate. All outbound email blocked.

---

## 🟡 PRODUCT SUBDOMAINS (6 records — Nginx ready, DNS missing)

| Type | Host | Value | Product |
|------|------|-------|---------|
| A | cream.psdepot.com | 31.97.6.40 | CREAM Mobile |
| A | reggiestarr.psdepot.com | 31.97.6.40 | ReggieStarr POS (RS-79) |
| A | pos.psdepot.com | 31.97.6.40 | RS-79 + RS-80 Demo |
| A | depotchaos.psdepot.com | 31.97.6.40 | CRM Dashboard |
| A | api.psdepot.com | 31.97.6.40 | API Endpoints |
| A | rs-80.psdepot.com | 31.97.6.40 | RS-80 Product Page |

**Status:** Nginx configs ACTIVE, SSL certs provisioned, pages served. DNS is the only missing piece — all 6 subdomains return HTTP 000 until A records are added.

---

## ✅ ALREADY COMPLETE

| Item | Method |
|------|--------|
| Google Search Console verification | Meta tag (already in place) |
| Sitemap submission | https://psdepot.com/sitemap.xml |

---

## TOTAL: 10 records (4 critical SendGrid + 6 product subdomains)
