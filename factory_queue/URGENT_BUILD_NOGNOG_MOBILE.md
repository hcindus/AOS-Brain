# URGENT: Build N'og nog v3 Mobile
**Priority:** 🟡 HIGH  
**Assigned:** Forge  
**Deadline:** 2026-08-05 (14 days)

## Task
Wrap existing web app for mobile using Capacitor.

## Commands
```bash
cd /root/.openclaw/workspace/nognog
npm install @capacitor/core @capacitor/cli
npx cap add android
npx cap add ios
npx cap sync
npx cap open android  # Build APK
npx cap open ios      # Build IPA
```

## Prerequisites
- [ ] Node.js dependencies installed
- [ ] Capacitor configured
- [ ] Web app builds successfully

## Success Criteria
- [ ] APK generated
- [ ] IPA generated
- [ ] Web-to-native bridge functional
