# RS-79 POS System - Implementation Tasks

> **Status Legend:** `[ ]` Not Started | `[-]` In Progress | `[x]` Complete

---

## Phase 1: Foundation & Database (Priority: Critical) - COMPLETE ✅

### 1.1 Database Schema Enhancement

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1.1.1 | Add `GiftCard` model to schema | `[x]` | code, balance, originalAmount, isActive, expiresAt |
| 1.1.2 | Add `StoreCredit` model to schema | `[x]` | customer FK, balance, totalEarned, totalSpent |
| 1.1.3 | Add `ExchangeRate` model to schema | `[x]` | fromCurrency, toCurrency, rate, updatedAt |
| 1.1.4 | Add `SessionLog` model to schema | `[x]` | clerk FK, action, details, ipAddress |
| 1.1.5 | Enhance `Item` model | `[x]` | stockQty, lowStock, description, barcode |
| 1.1.6 | Enhance `Payment` model | `[x]` | Add clerkId FK for audit |
| 1.1.7 | Add database indexes | `[x]` | Performance optimization |
| 1.1.8 | Create Prisma migration | `[x]` | `npx prisma migrate dev` |
| 1.1.9 | Update seed.ts with sample data | `[x]` | Include all new models |
| 1.1.10 | Add `meta` field to Order | `[x]` | JSON for split checks |

### 1.2 Core Utilities & Services

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1.2.1 | Create `/src/lib/prisma.ts` singleton | `[x]` | Prisma client singleton pattern |
| 1.2.2 | Create `/src/lib/currency.ts` | `[x]` | Currency conversion service |
| 1.2.3 | Create `/src/lib/payments.ts` | `[x]` | Payment validation & processing |
| 1.2.4 | Create `/src/lib/validation.ts` | `[x]` | Zod schemas for all inputs |
| 1.2.5 | Create `/src/lib/errors.ts` | `[x]` | Custom error classes |
| 1.2.6 | Create `/src/services/order-service.ts` | `[x]` | Order business logic |
| 1.2.7 | Create `/src/services/payment-service.ts` | `[x]` | Payment processing logic |
| 1.2.8 | Create `/src/services/customer-service.ts` | `[x]` | Customer operations |
| 1.2.9 | Create `/src/services/giftcard-service.ts` | `[x]` | Gift card validation |
| 1.2.10 | Create `/src/services/session-log-service.ts` | `[x]` | Audit logging |

### 1.3 Type Definitions

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1.3.1 | Create `/src/types/index.ts` | `[x]` | Export all types |
| 1.3.2 | Create `/src/types/clerk.ts` | `[x]` | ClerkSession, ClerkRole, etc |
| 1.3.3 | Create `/src/types/order.ts` | `[x]` | Order, OrderItem, OrderStatus |
| 1.3.4 | Create `/src/types/payment.ts` | `[x]` | Payment, PaymentType, PaymentInput |
| 1.3.5 | Create `/src/types/customer.ts` | `[x]` | Customer, GiftCard, StoreCredit |
| 1.3.6 | Create `/src/types/currency.ts` | `[x]` | Currency, ExchangeRate |
| 1.3.7 | Create `/src/types/kds.ts` | `[x]` | KDSOrder, KDSStatus |
| 1.3.8 | Create `/src/types/api.ts` | `[x]` | API request/response types |

---

## Phase 2A: Advanced Features (Priority: Critical) - COMPLETE ✅

### 2A.1 Split Check System

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2A.1.1 | Create `split-check-service.ts` | `[x]` | Even and by-item split logic |
| 2A.1.2 | Create `POST /api/split-check` | `[x]` | Split order endpoint |
| 2A.1.3 | Create `GET /api/split-check` | `[x]` | Get split checks endpoint |
| 2A.1.4 | Create `PATCH /api/split-check` | `[x]` | Process split payment |
| 2A.1.5 | Create `SplitCheckModal` component | `[x]` | Even/by-item split UI |
| 2A.1.6 | Split receipt generation | `[x]` | Individual split receipts |

### 2A.2 Split Tender System

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2A.2.1 | Create `split-tender-service.ts` | `[x]` | Multiple payment methods logic |
| 2A.2.2 | Create `POST /api/split-tender` | `[x]` | Process multiple payments |
| 2A.2.3 | Create `GET /api/split-tender` | `[x]` | Get tender status |
| 2A.2.4 | Create `SplitTenderModal` component | `[x]` | Cash+Card combo UI |
| 2A.2.5 | Remaining balance display | `[x]` | Real-time balance tracking |

### 2A.3 Hold/Recall Transactions

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2A.3.1 | Create `hold-order-service.ts` | `[x]` | Hold/recall logic |
| 2A.3.2 | Create `POST /api/held-orders` | `[x]` | Hold order endpoint |
| 2A.3.3 | Create `GET /api/held-orders` | `[x]` | List held orders |
| 2A.3.4 | Create `PATCH /api/held-orders` | `[x]` | Recall/extend hold |
| 2A.3.5 | Create `DELETE /api/held-orders` | `[x]` | Cancel held order |
| 2A.3.6 | Create `HoldOrderModal` component | `[x]` | Hold with name input |
| 2A.3.7 | Create `RecallOrderPanel` component | `[x]` | Ticket number recall |
| 2A.3.8 | Auto-expire held orders | `[x]` | 4-hour default expiry |

### 2A.4 PIN-Based Clerk Authentication

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2A.4.1 | Enhance clerk auth with PIN | `[x]` | 4-6 digit PIN support |
| 2A.4.2 | Role-based permissions | `[x]` | Admin/Manager/Clerk roles |
| 2A.4.3 | Create `ClerkLoginModal` component | `[x]` | PIN pad UI |
| 2A.4.4 | Session tracking | `[x]` | Clerk session in API |
| 2A.4.5 | Permission middleware | `[x]` | Route protection |

### 2A.5 X/Z Report System

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2A.5.1 | Create `xz-report-service.ts` | `[x]` | Report generation logic |
| 2A.5.2 | Create `GET /api/reports/x` | `[x]` | X-Report endpoint |
| 2A.5.3 | Create `POST /api/reports/x` | `[x]` | Z-Report endpoint |
| 2A.5.4 | Create `XZReportModal` component | `[x]` | Report display UI |
| 2A.5.5 | Payment method breakdown | `[x]` | Sales by payment type |
| 2A.5.6 | Clerk performance breakdown | `[x]` | Sales by clerk |
| 2A.5.7 | Void/refund totals | `[x]` | Negative amounts |
| 2A.5.8 | Thermal printer format | `[x]` | formatThermalPrint function |

### 2A.6 Gift Card UI

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2A.6.1 | Create `POST /api/gift-cards` | `[x]` | Create gift card endpoint |
| 2A.6.2 | Create `GET /api/gift-cards` | `[x]` | Lookup/balance endpoint |
| 2A.6.3 | Create `PATCH /api/gift-cards` | `[x]` | Update gift card |
| 2A.6.4 | Create `GiftCardModal` component | `[x]` | Create/lookup UI |
| 2A.6.5 | Gift card creation | `[x]` | Generate unique codes |
| 2A.6.6 | Balance check | `[x]` | Code lookup UI |

### 2A.7 Store Credit UI

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2A.7.1 | Create `GET /api/store-credit` | `[x]` | Get store credit |
| 2A.7.2 | Create `POST /api/store-credit` | `[x]` | Add store credit |
| 2A.7.3 | Create `PATCH /api/store-credit` | `[x]` | Apply store credit |
| 2A.7.4 | Create `StoreCreditModal` component | `[x]` | Credit management UI |
| 2A.7.5 | Add credit workflow | `[x]` | Reason tracking |
| 2A.7.6 | Apply to order | `[x]` | Payment integration |

---

## Phase 2B: Additional Features (Priority: High)

### 2B.1 Kitchen Display System (KDS)

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2B.1.1 | Create KDS backend | `[-]` | SSE/polling endpoints |
| 2B.1.2 | Create KDS frontend | `[]` | Full-screen display |
| 2B.1.3 | Order ticket component | `[]` | Display order items |
| 2B.1.4 | Status management | `[]` | New/Preparing/Done |

### 2B.2 Customer Management

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2B.2.1 | Customer list page | `[]` | Searchable table |
| 2B.2.2 | Customer details | `[]` | Full customer view |
| 2B.2.3 | Order history | `[]` | Customer orders |
| 2B.2.4 | Loyalty management | `[]` | Points tracking |

### 2B.3 Item Management

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2B.3.1 | Item list page | `[]` | Admin only |
| 2B.3.2 | Item creation form | `[]` | Create/edit items |
| 2B.3.3 | Stock management | `[]` | Track quantities |
| 2B.3.4 | Barcode support | `[]` | Scan items |

---

## Task Count Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1: Foundation | 28 | `[x]` Complete |
| Phase 2A: Advanced Features | 38 | `[x]` Complete |
| Phase 2B: Additional Features | 11 | `[-]` In Progress |
| **TOTAL** | **77** | **85% Complete** |

---

## Phase 2A Deliverables Summary

### Services Created
1. ✅ `src/services/split-check-service.ts` - Split order logic
2. ✅ `src/services/split-tender-service.ts` - Multiple payment methods
3. ✅ `src/services/hold-order-service.ts` - Hold/recall transactions
4. ✅ `src/services/xz-report-service.ts` - X/Z report generation

### API Routes Created
1. ✅ `POST/GET/PATCH /api/split-check` - Split check operations
2. ✅ `POST/GET /api/split-tender` - Split tender operations
3. ✅ `POST/GET/PATCH/DELETE /api/held-orders` - Held order operations
4. ✅ `GET/POST /api/reports/x` - X/Z report generation
5. ✅ `POST/GET/PATCH /api/gift-cards` - Gift card management
6. ✅ `GET /api/gift-cards/stats` - Gift card statistics
7. ✅ `GET/POST/PATCH /api/store-credit` - Store credit operations

### React Components Created
1. ✅ `SplitCheckModal` - Even/by-item split UI
2. ✅ `SplitTenderModal` - Multiple payment methods UI
3. ✅ `HoldOrderModal` - Hold order with name input
4. ✅ `RecallOrderPanel` - Ticket number recall UI
5. ✅ `ClerkLoginModal` - PIN-based authentication
6. ✅ `XZReportModal` - X/Z report display
7. ✅ `GiftCardModal` - Create/lookup gift cards
8. ✅ `StoreCreditModal` - Credit management

### Database Updates
- ✅ Added `meta` JSON field to Order model for split checks

### Authentication Enhancements
- ✅ Updated `lib/auth.ts` with `authenticateRequest()` and `hasPermission()`
- ✅ Role-based access control (Admin/Manager/Clerk)
