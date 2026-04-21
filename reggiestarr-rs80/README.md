# ReggieStarr RS-80

## Offline-First Android POS System

**Version:** 1.0.0-MVP  
**Platform:** Android 10+ (API 29+)  
**Target Hardware:** SUNMI V2 Pro, PAX A920

---

## Features (MVP)

- ✅ **Offline Operation** — SQLite database, no internet required
- ✅ **Calculator Keypad** — 7-8-9 top, Clear/Enter top row, 00 by 0
- ✅ **Tax Modes** — Exclusive, Inclusive, Exempt per-item
- ✅ **Open Price** — Zero PLU triggers custom price entry
- ✅ **Cash Payments** — MVP hardware support
- ✅ **Sample Data** — Pre-loaded products for testing

---

## Project Structure

```
app/src/main/java/com/ps/pos/
├── MainActivity.kt              # Entry point
├── RS80Application.kt           # Application class with seed data
├── POSRepository.kt             # Data repository
├── data/
│   ├── AppDatabase.kt          # Room database
│   ├── dao/                     # Data Access Objects
│   └── entities/                # Room entities
├── ui/
│   ├── components/              # Reusable UI components
│   │   └── CalculatorKeypad.kt # Calculator-style keypad
│   ├── screens/                 # Screen composables
│   │   ├── RegisterScreen.kt   # Main POS screen
│   │   ├── CheckoutDialog.kt  # Checkout flow
│   │   └── ...
│   └── theme/                   # Material3 theme
└── utils/
    └── TaxCalculator.kt        # Tax calculation logic
```

---

## Build Instructions

### Prerequisites
- Android Studio Hedgehog (2023.1.1) or newer
- JDK 17
- Android SDK 34

### Build Steps

1. **Open in Android Studio**
   ```bash
   cd reggiestarr-rs80
   studio .
   ```

2. **Sync Gradle**
   - Click "Sync Now" in Android Studio
   - Or run: `./gradlew sync`

3. **Build APK**
   ```bash
   ./gradlew assembleDebug
   ```

4. **Install on Device**
   ```bash
   adb install app/build/outputs/apk/debug/app-debug.apk
   ```

---

## Configuration

### Sample Products
The app seeds sample data on first launch:
- `BURGER` — Cheeseburger ($8.99, tax exclusive)
- `FRIES` — French Fries ($3.99, tax exclusive)
- `SODA` — Soda ($2.50, tax exclusive)
- `OPEN` — Open Price Item (custom price)
- `TAXINC` — Tax Inclusive Item ($10.00)
- `TAXEX` — Tax Exempt Item ($5.00)

### Tax Rates
Default tax rate: 8.75%  
Configurable per product via `taxRate` field.

---

## Next Steps

1. **Hardware Integration**
   - ESC/POS thermal printer support
   - Barcode scanner (USB-HID)
   - Cash drawer trigger

2. **Network Sync**
   - Local WiFi mesh
   - CRDT conflict resolution
   - Multi-terminal support

3. **Advanced Features**
   - Split tender payments
   - Layaway/held orders
   - Loyalty program
   - Kitchen display system

---

## License

AGI Company — All rights reserved

## Support

Contact: Captain (root)
