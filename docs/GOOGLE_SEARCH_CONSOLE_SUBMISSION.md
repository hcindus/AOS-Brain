# Google Search Console Submission Guide
**Date:** 2026-08-04
**Sitemap:** https://psdepot.com/sitemap.xml (396 pages)
**Status:** ✅ Sitemap ready | ⏳ Awaiting Search Console verification

---

## Current Status
- ✅ sitemap.xml: LIVE (396 URLs, 70KB)
- ✅ robots.txt: LIVE (updated, references sitemap)
- ⏳ Google Search Console verification needed

---

## Option 1: HTML File Verification (Recommended)
1. Go to https://search.google.com/search-console
2. Add property: `psdepot.com` (URL prefix)
3. Choose "HTML file upload" verification
4. Google provides filename like: `googleXXXXXXX.html`
5. Place in: `/var/www/psdepot.com/`
6. Click "Verify"

## Option 2: DNS Verification
1. Go to https://search.google.com/search-console
2. Add property: `psdepot.com` (URL prefix)
3. Choose "DNS record" verification
4. Copy the TXT record value
5. Add to Hostinger DNS (ns1.dns-parking.com)
6. Verify

## Option 3: Meta Tag Verification
Add to `/var/www/psdepot.com/index.html` head section:
```html
<meta name="google-site-verification" content="YOUR_CODE" />
```

---

## After Verification
1. Go to Sitemaps section
2. Enter: `https://psdepot.com/sitemap.xml`
3. Click "Submit"
4. Monitor indexing in Coverage report

## Sitemap Breakdown
| Priority | Count | Page Types |
|----------|-------|------------|
| 1.0 (highest) | 1 | Homepage |
| 0.9 | 2 | POS, RS-80 |
| 0.8 | 73 | Products, ReggieStarr, CREAM |
| 0.7 | 17 | Categories, sales |
| 0.6 | 7 | Blog |
| 0.5 | 282 | Landing pages (states/cities) |
| 0.3 | 13 | Appointments, authenticated |
| 0.1 | 1 | 404 page | 404 page |
| **TOTAL** | **396** | |

---

## Quick Submit (If Already Verified)
```bash
curl -X POST "https://www.googleapis.com/webmasters/v3/sites/https%3A%2F%2Fpsdepot.com/sitemaps/https%3A%2F%2Fpsdepot.com%2Fsitemap.xml" \
  -H "Authorization: Bearer YOUR_OAUTH_TOKEN"
```
