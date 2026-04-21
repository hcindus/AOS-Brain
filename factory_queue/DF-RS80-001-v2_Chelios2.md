# Factory Order: DF-RS80-001-v2
**Agent:** Chelios2  
**Priority:** URGENT  
**Status:** ASSIGNED  
**Created:** 2026-04-21 07:47 UTC
**Supervisor:** Miles

---

## Mission: RS-80 MVP — Android Native Offline-First POS

### Background  
RS-80 is the sovereignty-first successor to ReggieStarr. Zero subscriptions. Zero cloud dependency. Power-only operation anywhere on Earth.

Your mission: Build the MVP Android native application.

### Deliverables
1. **Android Studio Project** — Kotlin, Jetpack Compose, Room ORM
2. **Calculator Keypad** — 7-8-9 top, Clear/Enter top row, 00 by 0
3. **Tax System** — Exclusive/Inclusive/Exempt per-item
4. **Open Price** — Zero PLU triggers custom price entry
5. **Cash Payments** — MVP hardware support
6. **ESC/POS Printing** — Thermal receipt support
7. **SQLite Database** — Local, encrypted, offline-only

### Architecture
```
reggiestarr-rs80/
├── app/src/main/java/com/ps/pos/
│   ├── MainActivity.kt
│   ├── RegisterScreen.kt
│   ├── CheckoutScreen.kt
│   ├── SettingsScreen.kt
│   ├── data/
│   │   ├── AppDatabase.kt
│   │   ├── ProductDao.kt
│   │   ├── TransactionDao.kt
│   │   └── entities/
│   │       ├── Product.kt
│   │       ├── Transaction.kt
│   │       └── LineItem.kt
│   ├── ui/components/
│   │   ├── CalculatorKeypad.kt
│   │   ├── ProductGrid.kt
│   │   └── ReceiptView.kt
│   ├── utils/
│   │   ├── EscPosPrinter.kt
│   │   └── TaxCalculator.kt
│   └── viewmodel/
│       └── RegisterViewModel.kt
├── build.gradle.kts
└── README.md
```

### Target Hardware
- SUNMI V2 Pro or PAX A920
- Android 10+ (API 29+)
- 4GB RAM / 64GB storage minimum

### MVP Feature Checklist
| Feature | Required |
|---------|----------|
| PLU product grid | ✅ |
| Calculator keypad (7-8-9 top) | ✅ |
| Clear/Enter top row | ✅ |
| 00 button by 0 | ✅ |
| Tax: Exclusive/Inclusive/Exempt | ✅ |
| Open price (zero PLU) | ✅ |
| Cash payments only | ✅ |
| Thermal receipt ESC/POS | ✅ |
| SQLite offline encrypted | ✅ |
| Transaction history | ✅ |

### Customer
**amhudsupply.org** — waiting for deployment. Speed is critical.

### Check-in Protocol
- Daily progress reports to Miles
- Blockers: escalate immediately  
- Completion: notify Miles for APK handoff

---
**Authority:** Captain (root)  
**Supervisor:** Miles  
**Execution:** Chelios2
