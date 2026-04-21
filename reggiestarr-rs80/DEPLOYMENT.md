# ReggieStarr RS-80 Deployment Checklist

## System Overview
- **Name:** ReggieStarr RS-80 POS System
- **Version:** 1.0.0
- **Platform:** Android 7.0+ (API 23+)
- **Target:** SUNMI V2 Pro, PAX A920, PAX A80

## Current Status: ✅ BUILD READY

### Core Features Implemented
- ✅ Calculator-style keypad (0-9, 00, C, +/-, decimal)
- ✅ Three modes: QTY, PLU, PRICE
- ✅ Product database with Room
- ✅ Cart management with real-time totals
- ✅ Tax calculation (8.25% configurable)
- ✅ Checkout dialog with payment types
- ✅ ESC/POS thermal printer integration
- ✅ Sample product seeding

### Architecture
```
app/src/main/java/com/ps/pos/
├── MainActivity.kt           # Entry point
├── RS80Application.kt        # App initialization
├── POSRepository.kt          # Data repository
├── data/
│   ├── AppDatabase.kt        # Room database
│   ├── entities/             # Product, Transaction, LineItem
│   └── dao/                  # Data access objects
├── ui/
│   ├── screens/
│   │   ├── RegisterScreen.kt    # Main register UI
│   │   └── CheckoutDialog.kt    # Payment dialog
│   ├── components/
│   │   └── CalculatorKeypad.kt # Calculator layout
│   └── theme/
│       ├── Color.kt, Theme.kt, Type.kt
├── viewmodel/
│   └── RegisterViewModel.kt   # Business logic
├── utils/
│   └── TaxCalculator.kt       # Tax utilities
└── services/
    └── PrinterService.kt      # ESC/POS printing
```

## Build Instructions

### Prerequisites
```bash
# Install Android SDK
sdkmanager "platforms;android-34"
sdkmanager "build-tools;34.0.0"

# Or use Gradle wrapper
./gradlew --version
```

### Debug Build
```bash
cd /root/.openclaw/workspace/reggiestarr-rs80
./gradlew assembleDebug
```
**Output:** `app/build/outputs/apk/debug/app-debug.apk`

### Release Build
```bash
# Create keystore (first time only)
keytool -genkey -v -keystore reggiestarr.keystore -alias rs80 -keyalg RSA -keysize 2048 -validity 10000

# Build release
./gradlew assembleRelease
```
**Output:** `app/build/outputs/apk/release/app-release-unsigned.apk`

### Sign Release APK
```bash
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
  -keystore reggiestarr.keystore \
  app/build/outputs/apk/release/app-release-unsigned.apk rs80

zipalign -v 4 \
  app/build/outputs/apk/release/app-release-unsigned.apk \
  ReggieStarr-RS80-v1.0.0.apk
```

## Customer: amhudsupply.org

### Delivery Package
```
ReggieStarr-RS80-v1.0.0/
├── ReggieStarr-RS80-v1.0.0.apk
├── INSTALL.md
├── USER_GUIDE.md
└── SAMPLE_PRODUCTS.csv
```

### Installation Steps
1. Enable "Unknown Sources" in Android Settings
2. Transfer APK to device (USB, cloud, ADB)
3. Tap APK to install
4. Grant requested permissions (Bluetooth, USB)

### Configuration
- Printer IP: Edit `PrinterService.kt` → `PRINTER_IP`
- Tax Rate: Edit `TaxCalculator.kt` → `TAX_RATE`
- Products: Use PLU lookup or import CSV

## Quick Start Guide
1. Launch ReggieStarr RS-80
2. Tap calculator keys to enter quantity
3. Press QTY/PLU/PRICE mode
4. Enter product PLU or price
5. Press ENTER
6. Tap ADD TO CART
7. Repeat for more items
8. Press CHECKOUT
9. Select payment type, enter tendered
10. Press COMPLETE SALE

## Next Version Features (v1.1)
- [ ] Barcode scanner integration
- [ ] Cloud sync for multi-terminal
- [ ] Split tender (cash + card)
- [ ] Kitchen display system (KDS)
- [ ] Receipt printer auto-detect
- [ ] Offline mode with sync
- [ ] Manager reports dashboard

## Support
- **Contact:** Captain (root) via Miles
- **Repository:** https://github.com/hcindus/AOS-Brain/tree/master/reggiestarr-rs80
- **Issues:** Submit via GitHub or contact directly

## License
Performance Supply Depot LLC - Internal Use Only
