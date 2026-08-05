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

## 🟡 OPTIONAL — Subdomain A Records (3 records)

| Type | Host | Value |
|------|------|-------|
| A | depotchaos.psdepot.com | 31.97.6.40 |
| A | pos.psdepot.com | 31.97.6.40 |
| A | api.psdepot.com | 31.97.6.40 |

---

## ✅ ALREADY COMPLETE

| Item | Method |
|------|--------|
| Google Search Console verification | Meta tag (HTML file alternative available) |
| Sitemap submission | https://psdepot.com/sitemap.xml |

---

## TOTAL: 7 records (4 critical, 3 optional)
