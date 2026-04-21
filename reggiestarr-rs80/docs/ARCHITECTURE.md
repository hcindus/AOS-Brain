# ReggieStarr RS-80 Architecture Document

**Version:** 1.0.0  
**Date:** 2026-04-21  
**Status:** Draft for Review  
**Customer:** amhudsupply.org (pending deployment)  

---

## Executive Summary

ReggieStarr RS-80 is an **offline-first, subscription-free Android POS system** designed for food trucks, bars, restaurants, cafes, pop-up kitchens, and retail operations that require **true sovereignty** over their commerce infrastructure.

**Core Philosophy:** Power-only operation. No cloud dependency. No monthly fees. Own your data.

---

## Product Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | Operate 100% offline (no internet required) | MUST |
| FR-002 | Multi-terminal sync over local WiFi mesh | MUST |
| FR-003 | Android terminal support (compact, built-in printer) | MUST |
| FR-004 | Android tablet support (kitchen display, customer-facing) | MUST |
| FR-005 | Configurable tax rates (0% - custom %) | MUST |
| FR-006 | Tax-inclusive pricing option | MUST |
| FR-007 | Tax-exempt transaction capability | MUST |
| FR-008 | Offline card payment storage (encrypted vault) | MUST |
| FR-009 | Cash payment with drawer integration | MUST |
| FR-010 | Batch payment processing when online | MUST |
| FR-011 | Zero subscription/licensing fees | MUST |
| FR-012 | End-to-end encryption for all sensitive data | MUST |

### Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-001 | Cold start to operational | < 5 seconds |
| NFR-002 | Transaction latency | < 100ms |
| NFR-003 | Battery life (terminal) | > 8 hours active |
| NFR-004 | Local sync speed (100 transactions) | < 2 seconds |
| NFR-005 | Data retention | Unlimited |
| NFR-006 | Hardware failure recovery | < 10 minutes |

---

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    REGGIESTARR RS-80                        │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐   │
│  │  Terminal   │◄──►│  Local Mesh │◄──►│     Tablet      │   │
│  │  (Primary)  │    │   Network   │    │  (Kitchen/Disp) │   │
│  └──────┬──────┘    └─────────────┘    └─────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              LOCAL DATABASE (SQLite + CRDT)               ││
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   ││
│  │  │ Products │ │  Orders  │ │Payments  │ │  Audit   │   ││
│  │  │  (SKU)   │ │(History) │ │ (Vault)  │ │  (Log)   │   ││
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘   ││
│  └─────────────────────────────────────────────────────────┘│
│         │                                                   │
│         ▼ (Optional: Batch when online)                     │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              PAYMENT PROCESSOR (When Online)          ││
│  │         Stripe / Square / Offline fallback            ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Form Factor Specifications

#### A. Android Terminal (Primary POS)

**Target Hardware:**
- SUNMI V2 Pro or PAX A920
- 5.5" - 6" touchscreen
- Built-in 58mm thermal printer
- Integrated NFC/Chip reader
- 4GB RAM / 64GB storage minimum
- Android 10+ (API 29+)

**UI Characteristics:**
- Fast-tap optimized (large buttons)
- Portrait orientation
- Minimal navigation (single screen flow)
- Hardware button integration (scan, print)

#### B. Android Tablet (Kitchen Display / Customer-Facing)

**Target Hardware:**
- Samsung Galaxy Tab A8 or equivalent
- 10" screen minimum
- WiFi only (no cellular required)
- Rugged case optional
- Android 10+ (API 29+)

**UI Characteristics:**
- Kitchen display: Order queue, timing, status
- Customer-facing: Cart review, tipping, signature
- Landscape orientation
- Real-time sync with terminal

---

## Data Architecture

### Database Schema

```sql
-- Core tables
products (id, sku, name, price, category, tax_exempt, created_at)
tax_rates (id, name, rate_percent, location_id, is_default)
orders (id, terminal_id, items_json, subtotal, tax, total, 
        payment_type, status, created_at, synced_at)
payments (id, order_id, type, amount, card_token_encrypted, 
          batch_id, status, processed_at)
terminals (id, name, type, last_seen, sync_checkpoint)
audit_log (id, table_name, record_id, action, diff_json, created_at)
```

### Conflict-Free Replicated Data Type (CRDT)

For multi-terminal sync without a central server:

```javascript
// CRDT Operation Log
{
  "op_id": "uuid",
  "terminal_id": "terminal-001",
  "timestamp": "2026-04-21T07:26:00Z",
  "vector_clock": {"terminal-001": 45, "terminal-002": 42},
  "operation": "INSERT",
  "table": "orders",
  "data": {...},
  "checksum": "sha256:..."
}
```

**Merge Strategy:** Last-write-wins with vector clock precedence.

---

## Tax System Architecture

### Tax Configuration

```kotlin
data class TaxConfig(
    val id: String,
    val name: String,           // "California State", "SF County"
    val ratePercent: BigDecimal, // 8.5, 10.0, 0.0
    val appliesTo: List<String>, // Product categories
    val isCompound: Boolean      // Applied after other taxes
)
```

### Tax Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **Exclusive** (default) | Price shows pre-tax, tax added at checkout | Standard retail |
| **Inclusive** | Price includes tax, reverse-calculated | Bar menu pricing |
| **Exempt** | No tax applied to transaction | Non-profit, resale |
| **Mixed** | Per-item tax status | Complex operations |

### Calculation Examples

```kotlin
// Exclusive: $10.00 + 8.5% = $10.85
// Inclusive: $10.00 = $9.22 + $0.78 tax
// Exempt: $10.00 = $10.00

fun calculateTax(subtotal: BigDecimal, config: TaxConfig): TaxResult {
    return when (config.mode) {
        EXCLUSIVE -> subtotal * config.ratePercent
        INCLUSIVE -> subtotal - (subtotal / (1 + config.ratePercent))
        EXEMPT -> BigDecimal.ZERO
    }
}
```

---

## Payment Architecture

### Offline Payment Vault

**Encryption:** AES-256-GCM with hardware-backed keystore (Android Keystore System)

```kotlin
// Card token storage (offline)
data class OfflinePayment(
    val tokenId: String,          // UUID
    val encryptedPan: String,     // AES-256 encrypted
    val lastFour: String,         // Plaintext for receipt
    val expiryMonth: Int,
    val expiryYear: Int,
    val amount: BigDecimal,
    val capturedAt: DateTime,
    val batchId: String?          // Null until batched
)
```

**Security:**
- Keys never leave hardware keystore
- Tokens auto-expire after 7 days unbatched
- Tamper detection wipes vault

### Batch Processing

```kotlin
// When connectivity detected
fun processBatch(payments: List<OfflinePayment>) {
    payments.chunked(100).forEach { batch ->
        val results = paymentGateway.processBatch(batch)
        results.forEach { updateStatus(it) }
    }
}
```

---

## Network Architecture

### Local Mesh Discovery

```kotlin
// mDNS/Bonjour for zero-config peer discovery
val nsdManager = context.getSystemService(Context.NSD_SERVICE) as NsdManager
val serviceInfo = NsdServiceInfo().apply {
    serviceName = "ReggieStarr-${terminalId}"
    serviceType = "_reggiestarr._tcp"
    port = 9876
}
nsdManager.registerService(serviceInfo, NsdProtocol.DNS_SD, registrationListener)
```

### Sync Protocol

1. **Discovery:** Terminal broadcasts on local network
2. **Handshake:** Peers exchange vector clocks
3. **Diff:** Each side sends operations since last sync checkpoint
4. **Merge:** CRDT merge, conflicts resolved by timestamp
5. **Ack:** Confirm receipt, update checkpoint

**Transport:** WebSocket over local WiFi (no internet required)

---

## Hardware Integration

### Peripherals Supported

| Peripheral | Interface | Libraries |
|------------|-----------|-----------|
| Thermal Printer | USB/Bluetooth | ESC/POS command set |
| Cash Drawer | USB trigger | Standard pulse |
| Barcode Scanner | USB HID | Built-in Android |
| NFC Reader | Built-in / USB | Android NFC API |
| Chip Card Reader | USB | CCID protocol |
| Customer Display | USB/Bluetooth | Serial protocol |

### Printer Integration

```kotlin
// ESC/POS commands for SUNMI/PAX printers
fun printReceipt(order: Order) {
    val commands = mutableListOf<ByteArray>()
    commands.add(ESC_CENTER)           // Center align
    commands.add("ReggieStarr".toByteArray())
    commands.add(LINE_FEED)
    commands.add(ESC_LEFT)             // Left align
    commands.add(order.toText())
    commands.add(ESC_CUT)              // Cut paper
    printerPort.write(commands.flatten())
}
```

---

## Deployment Architecture

### Single Terminal Mode

- Standalone operation
- No network configuration required
- Full functionality independent

### Multi-Terminal Mesh Mode

```
┌────────────────────────────────────┐
│         Local WiFi Network         │
│    (No internet required)          │
│                                    │
│  ┌──────────┐    ┌──────────┐     │
│  │Terminal 1│◄──►│Terminal 2│     │
│  │ (Master) │    │ (Slave)  │     │
│  └────┬─────┘    └────┬─────┘     │
│       │               │            │
│       └───────────────┘            │
│              │                     │
│         ┌────┴────┐                │
│         │ Tablet  │                │
│         │(Kitchen)│                │
│         └─────────┘                │
└────────────────────────────────────┘
```

**Master Election:** First terminal online becomes sync coordinator. Automatic failover.

---

## Development Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Language** | Kotlin (Android) | Native performance, null-safety |
| **UI Framework** | Jetpack Compose | Modern, reactive, fast |
| **Database** | SQLite + Room | Proven, offline-first |
| **Sync** | CRDT custom impl | No server dependency |
| **Crypto** | Android Keystore + Tink | Hardware-backed security |
| **Build** | Gradle | Standard Android toolchain |

---

## Security Architecture

### Threat Model

| Threat | Mitigation |
|--------|------------|
| Device theft | Encrypted database, remote wipe (if online) |
| Network sniffing | TLS 1.3 for sync, local network only |
| Tampering | Keystore-backed keys, integrity checks |
| Data loss | Automated local backup, peer sync |
| Card data exposure | Tokenization, encrypted vault, PCI-DSS aligned |

### Encryption Standards

- **At Rest:** SQLCipher (AES-256)
- **In Transit:** TLS 1.3 (local network)
- **Card Tokens:** AES-256-GCM + hardware key
- **Backup:** GPG encrypted

---

## MVP Scope (Phase 1)

**Goal:** Deploy to amhudsupply.org for validation

### In Scope

- [ ] Terminal app (SUNMI/PAX target)
- [ ] Product catalog management
- [ ] Order creation and checkout
- [ ] Tax exclusive/inclusive/exempt
- [ ] Cash payments
- [ ] Offline card vault
- [ ] Thermal printer integration
- [ ] Basic reporting (daily totals)

### Out of Scope (Phase 2)

- [ ] Kitchen display (tablet)
- [ ] Multi-terminal mesh
- [ ] Advanced analytics
- [ ] Inventory management
- [ ] Customer loyalty

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Time to first transaction | < 5 minutes from unboxing |
| Transaction success rate | > 99.9% |
| Offline operation duration | Unlimited |
| Customer satisfaction | NPS > 50 |
| Cost vs Square | Break-even at 4 months |

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Hardware incompatibility | Medium | High | Test matrix of 3+ devices |
| Payment processor rejection | Low | Critical | Stripe + Square + backup |
| Sync conflicts | Medium | Medium | CRDT + manual override |
| Customer training | High | Medium | Video tutorials, simple UX |

---

## Open Questions

1. **Payment Processor:** Stripe vs. Square vs. Braintree for batch processing?
2. **Hardware Partnership:** Direct SUNMI/PAX relationship or reseller?
3. **Open Source:** AGPL license for core, proprietary for hardware drivers?
4. **Update Mechanism:** Sideload APK or F-Droid repository?

---

**Next Steps:**
1. Review and approve architecture
2. Select MVP hardware target
3. Set up development environment
4. Begin terminal app development

**Document Owner:** Miles  
**Reviewers:** Captain (root)  
**Approval:** Pending
