# Website Deployment Instructions
## Performance Supply Depot LLC

---

## 🚀 DEPLOY TO HOSTINGER

### Method 1: Hostinger Control Panel (Recommended)

1. **Log in:** https://www.hostinger.com
2. **Navigate:** Hosting → performancesupplydepot.com → File Manager
3. **Upload:**
   - Go to `public_html/`
   - Upload `index.html` (replace existing)
   - Upload all assets (CSS, JS, images)

### Method 2: FTP Upload

**FTP Credentials:**
- **Host:** ftp.performancesupplydepot.com
- **User:** [Get from Hostinger panel]
- **Pass:** [Get from Hostinger panel]
- **Port:** 21

**Files to Upload:**
```
/public_html/
├── index.html (main site)
├── css/
├── js/
├── images/
└── assets/
```

### Method 3: Git Deployment (Advanced)

If Git integration enabled:
```bash
git remote add hostinger [HOSTINGER_GIT_URL]
git push hostinger main
```

---

## 📁 DEPLOYMENT PACKAGE

**Location:** `/root/.openclaw/workspace/aocros/AGI_COMPANY_WEBSITES/performance-supply-depot/`

**Files Ready:**
- ✅ `index.html` - Main website (24KB)
- ✅ `deploy.sh` - Deployment script

**Status:** Ready for upload

---

## ⚡ QUICK DEPLOY

```bash
# From local machine:
scp -r /root/.openclaw/workspace/aocros/AGI_COMPANY_WEBSITES/performance-supply-depot/* \
  [USER]@ftp.performancesupplydepot.com:/public_html/
```

---

## ✅ POST-DEPLOY CHECKLIST

- [ ] Website loads at https://performancesupplydepot.com
- [ ] All pages render correctly
- [ ] Contact form works
- [ ] Mobile responsive
- [ ] SSL certificate active

---

**Last Updated:** 2026-03-16 06:45 UTC
**Ready for deployment:** YES
