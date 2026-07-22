# URGENT: Build ReggieStarr RS-80 Android APK
**Priority:** 🔴 CRITICAL  
**Assigned:** Forge  
**Deadline:** 2026-07-25 (3 days)

## Task
Execute Android build for RS-80 MVP.

## Commands
```bash
cd /root/.openclaw/workspace/reggiestarr-rs80
./gradlew assembleRelease
```

## Success Criteria
- [ ] APK generated in `app/build/outputs/apk/release/`
- [ ] File size < 50MB
- [ ] Installable on Android 8.0+ (API 26+)

## Deliverable
Upload APK to `/factory_output/reggiestarr-rs80-2026-07-22.apk`

## Blockers
None - ready to build.
