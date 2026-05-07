# RS-79 POS System - Implementation Tasks

> **Status Legend:** `[ ]` Not Started | `[-]` In Progress | `[x]` Complete

---

## Phase 1: Foundation & Database (Priority: Critical)

### 1.1 Database Schema Enhancement

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1.1.1 | Add `GiftCard` model to schema | `[ ]` | code, balance, originalAmount, isActive, expiresAt |
| 1.1.2 | Add `StoreCredit` model to schema | `[ ]` | customer FK, balance, totalEarned, totalSpent |
| 1.1.3 | Add `ExchangeRate` model to schema | `[ ]` | fromCurrency, toCurrency, rate, updatedAt |
| 1.1.4 | Add `SessionLog` model to schema | `[ ]` | clerk FK, action, details, ipAddress |
| 1.1.5 | Enhance `Item` model | `[ ]` | stockQty, lowStock, description, barcode |
| 1.1.6 | Enhance `Payment` model | `[ ]` | Add clerkId FK for audit |
| 1.1.7 | Add database indexes | `[ ]` | Performance optimization |
| 1.1.8 | Create Prisma migration | `[ ]` | `npx prisma migrate dev` |
| 1.1.9 | Update seed.ts with sample data | `[ ]` | Include all new models |

### 1.2 Core Utilities & Services

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1.2.1 | Create `/src/lib/prisma.ts` singleton | `[ ]` | Prisma client singleton pattern |
| 1.2.2 | Create `/src/lib/currency.ts` | `[ ]` | Currency conversion service |
| 1.2.3 | Create `/src/lib/payments.ts` | `[ ]` | Payment validation & processing |
| 1.2.4 | Create `/src/lib/validation.ts` | `[ ]` | Zod schemas for all inputs |
| 1.2.5 | Create `/src/lib/errors.ts` | `[ ]` | Custom error classes |
| 1.2.6 | Create `/src/services/order-service.ts` | `[ ]` | Order business logic |
| 1.2.7 | Create `/src/services/payment-service.ts` | `[ ]` | Payment processing logic |
| 1.2.8 | Create `/src/services/customer-service.ts` | `[ ]` | Customer operations |
| 1.2.9 | Create `/src/services/giftcard-service.ts` | `[ ]` | Gift card validation |
| 1.2.10 | Create `/src/services/session-log-service.ts` | `[ ]` | Audit logging |

### 1.3 Type Definitions

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1.3.1 | Create `/src/types/index.ts` | `[ ]` | Export all types |
| 1.3.2 | Create `/src/types/clerk.ts` | `[ ]` | ClerkSession, ClerkRole, etc |
| 1.3.3 | Create `/src/types/order.ts` | `[ ]` | Order, OrderItem, OrderStatus |
| 1.3.4 | Create `/src/types/payment.ts` | `[ ]` | Payment, PaymentType, PaymentInput |
| 1.3.5 | Create `/src/types/customer.ts` | `[ ]` | Customer, GiftCard, StoreCredit |
| 1.3.6 | Create `/src/types/currency.ts` | `[ ]` | Currency, ExchangeRate |
| 1.3.7 | Create `/src/types/kds.ts` | `[ ]` | KDSOrder, KDSStatus |
| 1.3.8 | Create `/src/types/api.ts` | `[ ]` | API request/response types |

---

## Phase 2: Authentication System (Priority: Critical)

### 2.1 Auth API Routes

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2.1.1 | Create `POST /api/auth/login` | `[ ]` | PIN verification, JWT creation |
| 2.1.2 | Create `POST /api/auth/logout` | `[ ]` | Clear session cookie |
| 2.1.3 | Create `GET /api/auth/session` | `[ ]` | Verify current session |
| 2.1.4 | Create auth middleware | `[ ]` | Route protection wrapper |

### 2.2 Auth UI

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2.2.1 | Create login page layout | `[ ]` | Full-screen PIN entry |
| 2.2.2 | Create Numpad component | `[ ]` | 0-9, clear, backspace |
| 2.2.3 | Create PIN display component | `[ ]` | Masked PIN dots |
| 2.2.4 | Create ClerkSelector component | `[ ]` | Select clerk before PIN |
| 2.2.5 | Add login error handling | `[ ]` | Invalid PIN feedback |
| 2.2.6 | Add session expiration handling | `[ ]` | Auto-redirect on expiry |

### 2.3 Session Management

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2.3.1 | Update `/src/lib/auth.ts` | `[ ]` | Enhance with cookie options |
| 2.3.2 | Create `useSession` hook | `[ ]` | React hook for session |
| 2.3.3 | Create AuthProvider context | `[ ]` | Global auth state |

---

## Phase 3: POS Register Interface (Priority: Critical)

### 3.1 Core Register Layout

| # | Task | Status | Notes |
|---|------|--------|-------|
| 3.1.1 | Create register page layout | `[ ]` | Split: items left, cart right |
| 3.1.2 | Create POS header component | `[ ]` | Clerk info, currency selector |
| 3.1.3 | Create responsive grid for items | `[ ]` | CSS Grid/Flexbox |
| 3.1.4 | Create cart panel layout | `[ ]` | Item list, totals, actions |

### 3.2 Item Display Components

| # | Task | Status | Notes |
|---|------|--------|-------|
| 3.2.1 | Create CategoryTabs component | `[ ]` | Filter items by category |
| 3.2.2 | Create ItemGrid component | `[ ]` | Responsive item grid |
| 3.2.3 | Create ItemCard component | `[ ]` | Display item: name, price |
| 3.2.4 | Create ItemSearch component | `[ ]` | Text search for items |
| 3.2.5 | Add item images support | `[ ]` | Optional placeholder |

### 3.3 Cart Components

| # | Task | Status | Notes |
|---|------|--------|-------|
| 3.3.1 | Create CartProvider context | `[ ]` | Global cart state |
| 3.3.2 | Create CartItem component | `[ ]` | Qty controls, remove |
| 3.3.3 | Create CartList component | `[ ]` | Scrollable cart items |
| 3.3.4 | Create CartTotals component | `[ ]` | Subtotal, tax, total |
| 3.3.5 | Create QuantityAdjuster component | `[ ]` | +/- buttons or input |
| 3.3.6 | Add "Hold Order" functionality | `[ ]` | Save with name |
| 3.3.7 | Add "Recall Order" functionality | `[ ]` | Load held order |
| 3.3.8 | Add order notes input | `[ ]` | Text area for notes |

### 3.4 Customer Management in Register

| # | Task | Status | Notes |
|---|------|--------|-------|
| 3.4.1 | Create CustomerSearch component | `[ ]` | Search by name/phone |
| 3.4.2 | Create CustomerQuickAdd component | `[ ]` | Fast customer creation |
| 3.4.3 | Display customer loyalty info | `[ ]` | Points, store credit |
| 3.4.4 | Create "No Customer" button | `[ ]` | Clear customer |

---

## Phase 4: Payment System (Priority: Critical)

### 4.1 Payment Modal UI

| # | Task | Status | Notes |
|---|------|--------|-------|
| 4.1.1 | Create PaymentModal component | `[ ]` | Overlay with payment options |
| 4.1.2 | Create PaymentTypeSelector | `[ ]` | Cash, card, crypto, etc |
| 4.1.3 | Create AmountInput component | `[ ]` | Keypad or typed input |
| 4.1.4 | Create PaymentSummary component | `[ ]` | Current payments, balance |
| 4.1.5 | Add "Complete Sale" button | `[ ]` | Finalize order |

### 4.2 Payment Handlers

| # | Task | Status | Notes |
|---|------|--------|-------|
| 4.2.1 | Implement Cash payment | `[ ]` | Calculate change |
| 4.2.2 | Implement Card payment | `[ ]` | Record auth code |
| 4.2.3 | Implement Crypto payment | `[ ]` | Record tx hash |
| 4.2.4 | Implement GiftCard payment | `[ ]` | Validate code, deduct |
| 4.2.5 | Implement StoreCredit payment | `[ ]` | Deduct from customer |
| 4.2.6 | Implement Check payment | `[ ]` | Record check number |
| 4.2.7 | Implement Split payment | `[ ]` | Multiple payments |
| 4.2.8 | Create GiftCardInput component | `[ ]` | Code entry, balance display |

### 4.3 Payment API Routes

| # | Task | Status | Notes |
|---|------|--------|-------|
| 4.3.1 | Create `POST /api/payments/split` | `[ ]` | Calculate split totals |
| 4.3.2 | Create `POST /api/payments/giftcard/verify` | `[ ]` | Check balance |
| 4.3.3 | Create `POST /api/payments/giftcard/use` | `[ ]` | Apply to order |
| 4.3.4 | Create `POST /api/orders/[id]/payments` | `[ ]` | Add payment to order |

### 4.4 Receipt Printing

| # | Task | Status | Notes |
|---|------|--------|-------|
| 4.4.1 | Create Receipt component | `[ ]` | Printable receipt layout |
| 4.4.2 | Add print trigger after sale | `[ ]` | Auto-print option |
| 4.4.3 | Create digital receipt modal | `[ ]` | View before print |

---

## Phase 5: Multi-Currency Support (Priority: High)

### 5.1 Currency System

| # | Task | Status | Notes |
|---|------|--------|-------|
| 5.1.1 | Seed ExchangeRate data | `[ ]` | USD, EUR, JPY, GBP |
| 5.2.2 | Create CurrencySelector component | `[ ]` | Dropdown for currency |
| 5.2.3 | Create useCurrency hook | `[ ]` | Current currency state |
| 5.2.4 | Add currency display throughout | `[ ]` | Format all amounts |
| 5.2.5 | Add currency conversion API | `[ ]` | `POST /api/currency/convert` |
| 5.2.6 | Store base (USD) in database | `[ ]` | All prices in USD |
| 5.2.7 | Display in selected currency | `[ ]` | Real-time conversion |
| 5.2.8 | Handle multi-currency payments | `[ ]` | Payment in any currency |

---

## Phase 6: Order Management (Priority: High)

### 6.1 Order API Routes

| # | Task | Status | Notes |
|---|------|--------|-------|
| 6.1.1 | Create `GET /api/orders` | `[ ]` | List with filters, pagination |
| 6.1.2 | Create `POST /api/orders` | `[ ]` | Create new order |
| 6.1.3 | Create `GET /api/orders/[id]` | `[ ]` | Get order details |
| 6.1.4 | Create `PATCH /api/orders/[id]` | `[ ]` | Update order status |
| 6.1.5 | Create `POST /api/orders/[id]/void` | `[ ]` | Void order (refund) |
| 6.1.6 | Create `GET /api/orders/recent` | `[ ]` | Quick recent orders |
| 6.1.7 | Create `GET /api/orders/[id]/receipt` | `[ ]` | Get receipt data |

### 6.2 Order History UI

| # | Task | Status | Notes |
|---|------|--------|-------|
| 6.2.1 | Create orders list page | `[ ]` | Table with filters |
| 6.2.2 | Create OrderFilters component | `[ ]` | Date range, status, clerk |
| 6.2.3 | Create OrderTable component | `[ ]` | Sortable, paginated |
| 6.2.4 | Create OrderDetailsModal | `[ ]` | View full order |
| 6.2.5 | Add receipt reprint functionality | `[ ]` | From order history |
| 6.2.6 | Add order void workflow | `[ ]` | Manager approval |

### 6.3 Held Orders

| # | Task | Status | Notes |
|---|------|--------|-------|
| 6.3.1 | Create held orders list | `[ ]` | View saved carts |
| 6.3.2 | Create HoldModal component | `[ ]` | Name the hold |
| 6.3.3 | Implement recall functionality | `[ ]` | Load held cart |
| 6.3.4 | Auto-expire held orders | `[ ]` | After X hours |

---

## Phase 7: Customer Management (Priority: High)

### 7.1 Customer API Routes

| # | Task | Status | Notes |
|---|------|--------|-------|
| 7.1.1 | Create `GET /api/customers` | `[ ]` | Search customers |
| 7.1.2 | Create `POST /api/customers` | `[ ]` | Create customer |
| 7.1.3 | Create `GET /api/customers/[id]` | `[ ]` | Get customer |
| 7.1.4 | Create `PATCH /api/customers/[id]` | `[ ]` | Update customer |
| 7.1.5 | Create `GET /api/customers/[id]/orders` | `[ ]` | Order history |
| 7.1.6 | Create `POST /api/customers/[id]/loyalty` | `[ ]` | Adjust points |
| 7.1.7 | Create `POST /api/customers/[id]/storecredit` | `[ ]` | Adjust credit |

### 7.2 Customer UI

| # | Task | Status | Notes |
|---|------|--------|-------|
| 7.2.1 | Create customers list page | `[ ]` | Searchable table |
| 7.2.2 | Create CustomerForm component | `[ ]` | Create/edit form |
| 7.2.3 | Create CustomerDetails page | `[ ]` | Full customer view |
| 7.2.4 | Create CustomerOrders component | `[ ]` | Order history |
| 7.2.5 | Add loyalty points display | `[ ]` | Points earned/redeemed |
| 7.2.6 | Add store credit display | `[ ]` | Current balance |
| 7.2.7 | Create loyalty card lookup | `[ ]` | Scan/enter card # |

### 7.3 Gift Card Management

| # | Task | Status | Notes |
|---|------|--------|-------|
| 7.3.1 | Create gift card API routes | `[ ]` | CRUD operations |
| 7.3.2 | Create GiftCardForm component | `[ ]` | Create/edit cards |
| 7.3.3 | Create gift card lookup | `[ ]` | Check balance |
| 7.3.4 | Add gift card creation | `[ ]` | Generate codes |
| 7.3.5 | Add balance adjustment | `[ ]` | Admin override |

---

## Phase 8: Kitchen Display System (KDS) (Priority: Medium)

### 8.1 KDS Backend

| # | Task | Status | Notes |
|---|------|--------|-------|
| 8.1.1 | Create `GET /api/kds/orders` (SSE) | `[ ]` | Server-sent events |
| 8.1.2 | Create `PATCH /api/kds/orders/[id]` | `[ ]` | Update status |
| 8.1.3 | Create `GET /api/kds/orders/polling` | `[ ]` | Fallback polling |
| 8.1.4 | Add KDS order filtering | `[ ]` | New/preparing/done |

### 8.2 KDS Frontend

| # | Task | Status | Notes |
|---|------|--------|-------|
| 8.2.1 | Create KDS layout | `[ ]` | Full-screen display |
| 8.2.2 | Create OrderTicket component | `[ ]` | Display order items |
| 8.2.3 | Create KDS status columns | `[ ]` | New, Preparing, Done |
| 8.2.4 | Add timer to tickets | `[ ]` | Time since order |
| 8.2.5 | Add status action buttons | `[ ]` | Start, Done, Recall |
| 8.2.6 | Create useKDS hook | `[ ]` | SSE connection |
| 8.2.7 | Add sound notifications | `[ ]` | New order sound |
| 8.2.8 | Add auto-refresh fallback | `[ ]` | Polling mode |
| 8.2.9 | Create KDS settings | `[ ]` | Config page |

---

## Phase 9: Clerk & Admin Management (Priority: Medium)

### 9.1 Clerk API Routes

| # | Task | Status | Notes |
|---|------|--------|-------|
| 9.1.1 | Create `GET /api/clerks` | `[ ]` | List all clerks |
| 9.1.2 | Create `POST /api/clerks` | `[ ]` | Create clerk |
| 9.1.3 | Create `GET /api/clerks/[id]` | `[ ]` | Get clerk details |
| 9.1.4 | Create `PATCH /api/clerks/[id]` | `[ ]` | Update clerk |
| 9.1.5 | Create `POST /api/clerks/[id]/reset-pin` | `[ ]` | Reset PIN |
| 9.1.6 | Create `DELETE /api/clerks/[id]` | `[ ]` | Deactivate |

### 9.2 Clerk Management UI

| # | Task | Status | Notes |
|---|------|--------|-------|
| 9.2.1 | Create clerks list page | `[ ]` | Admin only |
| 9.2.2 | Create ClerkForm component | `[ ]` | Create/edit clerk |
| 9.2.3 | Create role selector | `[ ]` | Admin/Manager/Clerk |
| 9.2.4 | Add PIN generation/reset | `[ ]` | Secure PIN handling |
| 9.2.5 | Create clerk activity log | `[ ]` | Session logs |

---

## Phase 10: Reporting & Analytics (Priority: Low)

### 10.1 Report API Routes

| # | Task | Status | Notes |
|---|------|--------|-------|
| 10.1.1 | Create `GET /api/reports/daily` | `[ ]` | Daily summary |
| 10.1.2 | Create `GET /api/reports/clerk` | `[ ]` | Clerk performance |
| 10.1.3 | Create `GET /api/reports/items` | `[ ]` | Item sales |
| 10.1.4 | Create `GET /api/reports/payments` | `[ ]` | Payment summary |
| 10.1.5 | Create `GET /api/reports/hourly` | `[ ]` | Hourly breakdown |
| 10.1.6 | Create `GET /api/reports/export` | `[ ]` | CSV export |

### 10.2 Report UI

| # | Task | Status | Notes |
|---|------|--------|-------|
| 10.2.1 | Create reports dashboard | `[ ]` | Summary cards |
| 10.2.2 | Create DailyReport component | `[ ]` | Today's summary |
| 10.2.3 | Create ClerkReport component | `[ ]` | Clerk performance |
| 10.2.4 | Create ItemReport component | `[ ]` | Top sellers |
| 10.2.5 | Create PaymentReport component | `[ ]` | Payment breakdown |
| 10.2.6 | Add date range selector | `[ ]` | Custom periods |
| 10.2.7 | Add CSV export button | `[ ]` | Download reports |

---

## Phase 11: Item/Inventory Management (Priority: Medium)

### 11.1 Item API Routes

| # | Task | Status | Notes |
|---|------|--------|-------|
| 11.1.1 | Create `GET /api/items` | `[ ]` | List/search items |
| 11.1.2 | Create `POST /api/items` | `[ ]` | Create item |
| 11.1.3 | Create `GET /api/items/[id]` | `[ ]` | Get item |
| 11.1.4 | Create `PATCH /api/items/[id]` | `[ ]` | Update item |
| 11.1.5 | Create `DELETE /api/items/[id]` | `[ ]` | Delete item |
| 11.1.6 | Create `GET /api/items/low-stock` | `[ ]` | Low stock alert |

### 11.2 Item Management UI

| # | Task | Status | Notes |
|---|------|--------|-------|
| 11.2.1 | Create items list page | `[ ]` | Admin only |
| 11.2.2 | Create ItemForm component | `[ ]` | Create/edit item |
| 11.2.3 | Add barcode input | `[ ]` | For scanning |
| 11.2.4 | Add category management | `[ ]` | Manage categories |
| 11.2.5 | Add stock level display | `[ ]` | Current stock |
| 11.2.6 | Add low stock warnings | `[ ]` | Visual indicator |

---

## Phase 12: UI Components & Design System (Priority: High)

### 12.1 UI Primitives

| # | Task | Status | Notes |
|---|------|--------|-------|
| 12.1.1 | Create Button component | `[ ]` | Variants: primary, secondary, danger |
| 12.1.2 | Create Input component | `[ ]` | Text, number, password |
| 12.1.3 | Create Modal component | `[ ]` | Reusable modal |
| 12.1.4 | Create Card component | `[ ]` | Content container |
| 12.1.5 | Create Badge component | `[ ]` | Status indicators |
| 12.1.6 | Create Table component | `[ ]` | Sortable, paginated |
| 12.1.7 | Create Select component | `[ ]` | Dropdown |
| 12.1.8 | Create Tabs component | `[ ]` | Category tabs |
| 12.1.9 | Create Toast component | `[ ]` | Notifications |
| 12.1.10 | Create Skeleton component | `[ ]` | Loading states |

### 12.2 Layout Components

| # | Task | Status | Notes |
|---|------|--------|-------|
| 12.2.1 | Create AppLayout | `[ ]` | Main app wrapper |
| 12.2.2 | Create Sidebar component | `[ ]` | Navigation |
| 12.2.3 | Create Header component | `[ ]` | Top bar |
| 12.2.4 | Create Loading states | `[ ]` | Page loading |
| 12.2.5 | Create Error boundaries | `[ ]` | Error handling |

---

## Phase 13: Testing & Quality Assurance (Priority: High)

### 13.1 Unit Tests

| # | Task | Status | Notes |
|---|------|--------|-------|
| 13.1.1 | Setup Jest configuration | `[ ]` | Test runner |
| 13.1.2 | Test currency conversion | `[ ]` | Math accuracy |
| 13.1.3 | Test payment calculation | `[ ]` | Split payments |
| 13.1.4 | Test order totals | `[ ]` | Tax calculation |
| 13.1.5 | Test auth functions | `[ ]` | JWT, PIN hash |

### 13.2 Integration Tests

| # | Task | Status | Notes |
|---|------|--------|-------|
| 13.2.1 | Test full order flow | `[ ]` | Create → Pay → Complete |
| 13.2.2 | Test split payments | `[ ]` | Multiple payments |
| 13.2.3 | Test gift cards | `[ ]` | Balance tracking |
| 13.2.4 | Test loyalty points | `[ ]` | Earn/redeem |
| 13.2.5 | Test multi-currency | `[ ]` | Conversions |

### 13.3 E2E Tests

| # | Task | Status | Notes |
|---|------|--------|-------|
| 13.3.1 | Setup Playwright | `[ ]` | E2E framework |
| 13.3.2 | Test login flow | `[ ]` | Happy path |
| 13.3.3 | Test complete sale | `[ ]` | Full purchase |
| 13.3.4 | Test void order | `[ ]` | Refund flow |
| 13.3.5 | Test KDS updates | `[ ]` | Real-time |

---

## Phase 14: Documentation & Deployment (Priority: Medium)

### 14.1 Documentation

| # | Task | Status | Notes |
|---|------|--------|-------|
| 14.1.1 | Create README.md | `[ ]` | Setup instructions |
| 14.1.2 | Create API documentation | `[ ]` | Endpoint reference |
| 14.1.3 | Create user manual | `[ ]` | POS operation |
| 14.1.4 | Create admin guide | `[ ]` | System configuration |
| 14.1.5 | Document deployment | `[ ]` | Abacus AI platform |

### 14.2 Deployment

| # | Task | Status | Notes |
|---|------|--------|-------|
| 14.2.1 | Create production build | `[ ]` | `next build` |
| 14.2.2 | Configure environment | `[ ]` | Production env vars |
| 14.2.3 | Setup database migrations | `[ ]` | Production DB |
| 14.2.4 | Configure logging | `[ ]` | Error tracking |
| 14.2.5 | Performance optimization | `[ ]` | Bundle analysis |

---

## Quick Reference: Critical Path

### Must Have (MVP)
1. ✅ Phase 1: Database schema (enhanced)
2. ✅ Phase 2: Authentication (PIN login)
3. ✅ Phase 3: POS Register (basic)
4. ✅ Phase 4: Payment System (cash + card)

### Should Have (v1.0)
5. ✅ Phase 5: Multi-currency
6. ✅ Phase 6: Order Management
7. ✅ Phase 7: Customer Management (basic)
8. ✅ Phase 8: KDS (basic)

### Nice to Have (v1.1+)
9. Phase 9: Clerk Management
10. Phase 10: Reporting
11. Phase 11: Inventory
12. Phase 12+: Polish

---

## Task Count Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1: Foundation | 19 | `[ ]` Not Started |
| Phase 2: Auth | 11 | `[ ]` Not Started |
| Phase 3: Register | 19 | `[ ]` Not Started |
| Phase 4: Payment | 15 | `[ ]` Not Started |
| Phase 5: Currency | 8 | `[ ]` Not Started |
| Phase 6: Orders | 14 | `[ ]` Not Started |
| Phase 7: Customers | 14 | `[ ]` Not Started |
| Phase 8: KDS | 10 | `[ ]` Not Started |
| Phase 9: Clerks | 9 | `[ ]` Not Started |
| Phase 10: Reports | 12 | `[ ]` Not Started |
| Phase 11: Items | 10 | `[ ]` Not Started |
| Phase 12: UI | 14 | `[ ]` Not Started |
| Phase 13: Testing | 14 | `[ ]` Not Started |
| Phase 14: Docs/Deploy | 9 | `[ ]` Not Started |
| **TOTAL** | **178** | **0% Complete** |

---

## Notes for Implementation

### Priority Guidelines
1. **Critical**: System won't function without these
2. **High**: Expected features for production use
3. **Medium**: Enhances usability
4. **Low**: Nice to have, can defer

### Development Order Recommendation
1. Complete Phase 1-4 for MVP
2. Add Phase 5 (Currency) early - affects data model
3. Add Phase 6-7 for full functionality
4. Add Phase 8 if kitchen display needed
5. Remaining phases can be iterative

### Database Considerations
- All currency values stored in USD
- Exchange rates updated periodically
- Gift cards expire (check expiration)
- Session logs for audit compliance
