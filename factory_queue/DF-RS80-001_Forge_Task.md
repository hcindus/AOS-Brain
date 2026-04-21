# Factory Order: DF-RS80-001
**Agent:** Forge  
**Priority:** URGENT  
**Status:** ASSIGNED  
**Created:** 2026-04-21 07:47 UTC

---

## Mission: RS-80 MVP — Android Native Offline-First POS

### Background
RS-80 is the sovereignty-first successor to ReggieStarr. Zero subscriptions, zero cloud dependency, power-only operation.

### Deliverables
1. **Android Studio Project** — Kotlin, Jetpack Compose, Room ORM
2. **Calculator Keypad** — 7-8-9 top, Clear/Enter top, 00 by 0
3. **Tax System** — Exclusive/Inclusive/Exempt per-item
4. **Open Price** — Zero PLU triggers custom price entry
5. **Cash Payments** — MVP hardware support
6. **ESC/POS Printing** — Thermal receipt support
7. **SQLite Database** — Local, encrypted, offline-only

### Architecture
```
reggiestarr-rs80/
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── java/
│   │       │   └── com/performancesupply/reggiestarr/
│   │       │       ├── MainActivity.kt
│   │       │       ├── RegisterScreen.kt
│   │       │       ├── CheckoutScreen.kt
│   │       │       ├── SettingsScreen.kt
│   │       │       ├── data/
│   │       │       │   ├── AppDatabase.kt
│   │       │       │   ├── ProductDao.kt
│   │       │       │   ├── TransactionDao.kt
│   │       │       │   └── entities/
│   │       │       ├── ui/
│   │       │       │   ├── components/
│   │       │       │   │   ├── CalculatorKeypad.kt
│   │       │       │   │   ├── ProductGrid.kt
│   │       │       │   │   └── ReceiptPrinter.kt
│   │       │       │   └── theme/
│   │       │       └── utils/
│   │       │           ├── EscPosPrinter.kt
│   │       │           └── TaxCalculator.kt
│   │       └── res/
│   └── build.gradle.kts
├── gradle/
└── README.md
```

### Target Hardware
- SUNMI V2 Pro or PAX A920
- Android 10+ (API 29+)
- Built-in thermal printer
- Minimum 4GB RAM / 64GB storage

### Key Features (MVP)
| Feature | Status |
|---------|--------|
| PLU product grid | Required |
| Calculator keypad (7-8-9) | Required |
| Tax: Exclusive/Inclusive/Exempt | Required |
| Open price (zero PLU) | Required |
| Cash payment only | Required |
| Thermal receipt print | Required |
| Transaction history | Required |
| SQLite offline storage | Required |

### Check-in
Daily updates to Captain via sessions.

---
**Assigned by:** Miles  
**Approved by:** Captain
