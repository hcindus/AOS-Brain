# Master Task List — psdepot.com & AGI Company
**Updated:** 2026-08-05 15:11 UTC | **By:** Miles

---

## 🔴 HIGH PRIORITY — Needs Captain Action

### 1. Google Business Profile (+8 SEO points)
**Task:** Go to business.google.com → claim "Performance Supply Depot LLC"
**Add:** Phone (888) 881-6834, hours, photos, services, service area
**Why:** Single biggest SEO win remaining — Mortimer estimates +8 points

### 2. SendGrid API Key
**Task:** Set `SENDGRID_API_KEY` environment variable
**Where:** `systemctl edit depotchaos` → add `Environment=SENDGRID_API_KEY=SG.xxxxx`
**Files:** `/datadepot/web/sendgrid_sender.py` already built, just needs key
**Status:** 28 emails stuck in queue (as of Aug 3)

### 3. DNS Records — Hostinger
**Task:** Add these to Hostinger DNS Zone Editor for psdepot.com:

**Subdomains:**
| Type | Name | Target | TTL |
|------|------|--------|-----|
| CNAME | cream | psdepot.com | 14400 |
| CNAME | reggiestarr | psdepot.com | 14400 |
| CNAME | dashboard | psdepot.com | 14400 |
| CNAME | depotchaos | psdepot.com | 14400 |

**SendGrid Domain Auth:**
| Type | Host | Value |
|------|------|-------|
| CNAME | em8873.psdepot.com | u109143135.wl136.sendgrid.net |
| CNAME | s1._domainkey.psdepot.com | s1.domainkey.u109143135.wl136.sendgrid.net |
| CNAME | s2._domainkey.psdepot.com | s2.domainkey.u109143135.wl136.sendgrid.net |
| TXT | _dmarc.psdepot.com | v=DMARC1; p=none |

### 4. performancesupplydepot.com Domain
**Task:** Register domain, point DNS to 31.97.6.40
**Status:** Nginx redirect already configured — works immediately when DNS points

### 5. GitHub Access for Morty's SEO Files ✅ RESOLVED
**Status:** ✅ Files downloaded & deployed via API token
**Repo:** `hcindus/aios-sync` → `downloads/mortimer-v1/`
**Downloaded to:** `/root/psdepot-build/`
- ✅ 14 FAQ schemas deployed to product pages (BreadcrumbList + FAQPage schema)
- ✅ 3 OG image designs (v1-industrial, v2-clean, v3-premium)
- ✅ 4 docs (alt-text-audit, deployment-guide, seo-audit, social-media-strategy)

### 6. Widget Embed on psdepot.com
**Task:** Add the smart widget embed code to all psdepot.com pages
**Widget URL:** `https://mc.myl0nr0s.cloud:8080/static/widget/psdepot-widget.js`
**Also needed:** Set Cal.com booking URL, configure webhook

---

## 🟡 MEDIUM PRIORITY

### 7. Sitemap Submission
**Task:** Submit sitemap.xml to Google Search Console + Bing Webmaster Tools
**Status:** ✅ Sitemap generated (302 URLs), just needs submission

### 8. ACM Technologies API Testing
**Task:** Test SOAP connectivity, verify order submission
**Client rebuilt:** ✅ Just needs endpoint testing
**Contact:** Jon Scarpa (Jon.Scarpa@acmtech.com)

### 9. Local Citations Submission
**Info doc:** `/blog/DRAFTS/local-citations-info.md`
**Submit to:**
- [ ] Yelp for Business (biz.yelp.com)
- [ ] Better Business Bureau (bbb.org)
- [ ] YellowPages (yellowpages.com)
- [ ] Bing Places (bingplaces.com)
- [ ] Apple Maps Connect

### 10. Blog Content Pipeline
**Published today:** ✅ 2 new posts (printer cleaning + thermal vs bond)
**Future topics:** POS setup guides, printer troubleshooting, industry-specific checklists

---

## 🟢 COMPLETED (2026-08-05 SEO Blitz)

| # | Item | Status |
|---|------|--------|
| 1 | OG Image (1200×630) | ✅ Live on 193 pages |
| 2 | Social footer (TikTok/IG/YT/X) | ✅ 44 pages |
| 3 | Alt text audit | ✅ All good |
| 4 | www → non-www redirect | ✅ nginx 301 |
| 5 | CSS fixes (duplicate blocks, missing tags, stray keyframes) | ✅ 199 pages |
| 6 | Press kit colors (Deep Tech Blue, Performance Orange, Electric Cyan) | ✅ 199 pages |
| 7 | PSDepot → PerformanceSupplyDepot branding | ✅ All pages |
| 8 | Patriotic blink phone number (888) 881-6834 | ✅ All pages |
| 9 | Cart color → RED (#c53030) | ✅ All pages |
| 10 | Mobile optimizations (44px touch targets, responsive grids) | ✅ All pages |
| 11 | Clarion logo on thermal-paper.html | ✅ |
| 12 | performancesupplydepot.com nginx redirect | ✅ Configured |
| 13 | Blog posts (2 new SEO articles) | ✅ |
| 14 | Local citations info doc | ✅ Prepared |
| 15 | Full site backup | ✅ 51MB in .backups/ |

---

## 📊 Pending Count Summary

| Priority | Count |
|----------|-------|
| 🔴 Captain Action Required | 6 |
| 🟡 Medium Priority | 4 |
| 🟢 Completed Today | 15 |
| **Total Tracked** | **25** |
