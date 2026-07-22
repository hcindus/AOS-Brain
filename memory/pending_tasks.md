# Pending Tasks - Miles

## ACM Technologies API Integration
**Created:** 2026-05-02 17:51 UTC  
**Updated:** 2026-05-16 05:06 UTC  
**Status:** SOAP Client Rebuilt - Testing Required

### Issue Fixed
❌ **Problem:** Automation sending REST/JSON → API expects SOAP/XML  
✅ **Solution:** Rebuilt client per Jon Scarpa's 2026-05-15 email with proper SOAP structure

### Next Step
Test connectivity with corrected SOAP client:
```
https://secure-send.acmtech.com/note/5U567H575R4G6Z5g5e6T487Y6Q5C6O4i815O626J5i4k636B6W6n7J7B7t7E6q5Q#b4399ab938c0b925ba12558c0b856163746afb4cb1de0308775521c56af136ff
```

### Credentials Status
✅ **Retrieved** - Stored in `/root/.openclaw/workspace/aocros/secrets/acm_api.env`

### Remaining Tasks
- [ ] Test connectivity (test mode)
- [ ] Verify endpoint URL with Jon if needed
- [ ] Test order submission flow
- [ ] Retrieve product catalog
- [ ] Validate with Jon Scarpa
- [ ] Request account activation

### Contacts
- **Jon Scarpa** (IT Manager): Jon.Scarpa@acmtech.com, (951) 738-9898 x222
- **Michael Harrison** (Account Executive): michael.harrison@acmtech.com

### Reference
- Customer #71152
- API Endpoint: https://api.acmtech.com
- Docs: https://api-help.acmtech.com

---

## DNS Records Setup - Hostinger
**Created:** 2026-06-14  
**Status:** PENDING CAPTAIN ACTION

### Subdomains for psdepot.com
| Type | Name | Target | TTL |
|------|------|--------|-----|
| CNAME | cream | psdepot.com | 14400 |
| CNAME | reggiestarr | psdepot.com | 14400 |
| CNAME | dashboard | psdepot.com | 14400 |
| CNAME | depotchaos | psdepot.com | 14400 |

### SendGrid Domain Authentication
| Type | Host | Value |
|------|------|-------|
| CNAME | em8873.psdepot.com | u109143135.wl136.sendgrid.net |
| CNAME | s1._domainkey.psdepot.com | s1.domainkey.u109143135.wl136.sendgrid.net |
| CNAME | s2._domainkey.psdepot.com | s2.domainkey.u109143135.wl136.sendgrid.net |
| TXT | _dmarc.psdepot.com | v=DMARC1; p=none |

**Action Required:** Add these records in Hostinger Dashboard → Domains → psdepot.com → DNS Zone Editor

---

**Daily Check:** Review inbox for credentials from Captain

---

## PS Depot Website Widget + Cal.com Integration
**Created:** 2026-07-22  
**Status:** DEPLOYED - Awaiting Captain Action

### What's Done
✅ Smart widget with brain-connected responses deployed to `/static/widget/psdepot-widget.js`
✅ Agent routing (Pulp/Jane/Clippy-42) based on intent
✅ Cal.com webhook endpoint at `/api/webhooks/calcom`
✅ Inline booking embed in widget chat
✅ Lead capture to `/var/www/psdepot.com/data/leads/`

### Action Required
| Task | Status |
|------|--------|
| Add widget embed code to psdepot.com | **PENDING** |
| Configure Cal.com webhook URL | **PENDING** |
| Set Cal.com booking URL in widget config | **PENDING** |

### Widget Embed Code
```html
<script>
  window.PSDEPOT_WIDGET_API = 'https://mc.myl0nr0s.cloud:8080';
  window.PSDEPOT_WIDGET_POSITION = 'bottom-right';
  window.PSDEPOT_WIDGET_GREETING = 'Hi! Need help with POS supplies?';
  window.PSDEPOT_CALCOM_URL = 'https://cal.com/psdepot/EVENT-URL';  // <-- UPDATE THIS
</script>
<script src="https://mc.myl0nr0s.cloud:8080/static/widget/psdepot-widget.js" async></script>
```

### Cal.com Webhook Setup
**URL:** `https://mc.myl0nr0s.cloud:8080/api/webhooks/calcom`
**Events:** `BOOKING_CREATED`, `BOOKING_CANCELLED`, `BOOKING_RESCHEDULED`

---

## PS Depot Sitemap Update
**Created:** 2026-07-22  
**Status:** ✅ COMPLETE

### Updated
- 302 URLs total
- Added all Capton products (7 pages)
- Added CAS/SAM4S cash registers (30+ pages)
- Added OrionStar Lucki robot page
- Added PF-230 Phenol-Free Thermal Paper page

### Files
- **Sitemap:** `/var/www/psdepot.com/sitemap.xml`
- **Robots:** `/var/www/psdepot.com/robots.txt`

### Next Step
Submit to Google Search Console and Bing Webmaster Tools for indexing

**Daily Check:** Review inbox for credentials from Captain
