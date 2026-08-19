# Performance Supply Depot — Mobile Ordering App (Android)

A lightweight native WebView wrapper that loads https://psdepot.com in a
full-screen shell, reusing the live store (catalog, cart, checkout).

## Build
```bash
export ANDROID_HOME=/opt/android-sdk
gradle assembleDebug
# → app/build/outputs/apk/debug/app-debug.apk
```

## Stack
- Java, plain `Activity` (no appcompat → ~15 KB APK)
- `WebView` with JS + DOM storage (localStorage cart works)
- Handles back-navigation, `tel:`/`mailto:`/external links in the browser

## Download (built)
`https://psdepot.com/downloads/Performance-Supply-Depot.apk`

## Notes
- `minSdk 23` (Android 6.0+), `targetSdk 34`
- Debug-signed for testing; release-sign + Play Store signing for production.
- Icon is the generic Android launcher icon — swap for the PSD brand logo.
