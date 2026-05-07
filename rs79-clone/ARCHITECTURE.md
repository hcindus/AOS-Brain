# RS-79 POS System Architecture

## System Overview

**RS-79 Clone** is a Next.js 14+ Point of Sale (POS) system built with modern web technologies. The system supports multi-currency transactions, multiple payment methods, and kitchen display integration for restaurant operations.

### Technology Stack

| Layer | Technology |
|-------|------------|
| Framework | Next.js 14+ (App Router) |
| Language | TypeScript |
| Database | SQLite (Prisma ORM) |
| Styling | Tailwind CSS |
| UI Components | React 18 |
| Auth | JWT (rs79_session cookie) |
| Icons | Lucide React |

---

## Architecture Patterns

### 1. Clean Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Routes     │  │   Pages      │  │  Components  │      │
│  │  (Next.js)   │  │  (Client)    │  │   (React)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├─────────────────────────────────────────────────────────────┤
│                     API LAYER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Route      │  │   Handler    │  │   Schema     │      │
│  │  (Next API)  │  │   (Logic)    │  │  (Zod/TS)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├─────────────────────────────────────────────────────────────┤
│                     BUSINESS LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Services   │  │   Utils      │  │    Types     │      │
│  │   (Core)     │  │   (Helpers)  │  │   (Domain)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├─────────────────────────────────────────────────────────────┤
│                     DATA LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Prisma     │  │   Schema     │  │   Database   │      │
│  │   Client     │  │   (Models)   │  │   (SQLite)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 2. Directory Structure

```
rs79-clone/
├── prisma/
│   ├── schema.prisma      # Database schema
│   ├── seed.ts            # Seed data
│   └── migrations/          # Database migrations
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── (auth)/          # Auth route group
│   │   │   ├── login/
│   │   │   └── logout/
│   │   ├── (pos)/           # POS route group
│   │   │   ├── dashboard/
│   │   │   ├── register/
│   │   │   ├── orders/
│   │   │   ├── customers/
│   │   │   └── reports/
│   │   ├── api/             # API routes
│   │   │   ├── auth/
│   │   │   ├── orders/
│   │   │   ├── customers/
│   │   │   ├── items/
│   │   │   └── reports/
│   │   ├── kds/             # Kitchen Display
│   │   ├── globals.css
│   │   └── layout.tsx
│   ├── components/          # React components
│   │   ├── pos/             # POS components
│   │   ├── ui/              # UI primitives
│   │   ├── kds/             # KDS components
│   │   └── shared/          # Shared components
│   ├── hooks/               # Custom React hooks
│   ├── lib/                 # Utilities
│   │   ├── auth.ts          # JWT auth
│   │   ├── prisma.ts        # Prisma client
│   │   ├── currency.ts      # Currency conversion
│   │   ├── payments.ts      # Payment handlers
│   │   └── utils.ts         # Utilities
│   ├── types/               # TypeScript types
│   │   ├── index.ts
│   │   ├── clerk.ts
│   │   ├── order.ts
│   │   └── payment.ts
│   └── services/            # Business logic
│       ├── order-service.ts
│       ├── payment-service.ts
│       └── customer-service.ts
├── public/                  # Static assets
├── next.config.js
├── tailwind.config.ts
└── package.json
```

---

## Database Schema (Enhanced)

### Entity Relationship Diagram

```
┌────────────────┐         ┌──────────────────┐         ┌────────────────┐
│    Clerk       │         │      Order       │         │   Customer     │
├────────────────┤         ├──────────────────┤         ├────────────────┤
│ id (PK)        │1      * │ id (PK)          │*      1 │ id (PK)        │
│ name           │◄────────┤ clerkId (FK)     │────────►│ name           │
│ role           │         │ customerId (FK)  │         │ phone          │
│ pin            │         │ transactionNo    │         │ loyaltyCardNo  │
│ active         │         │ subtotal         │         │ loyaltyPoints  │
│ createdAt      │         │ tax              │         │ createdAt      │
└────────────────┘         │ total            │         └────────────────┘
                         │ currency         │
                         │ currencyRate     │         ┌────────────────┐
                         │ paymentType      │         │   GiftCard     │
                         │ tendered         │         ├────────────────┤
                         │ change           │         │ id (PK)        │
                         │ status           │         │ code           │
                         │ kdsStatus        │         │ balance        │
                         │ holdName         │         │ originalAmount │
                         │ notes            │         │ isActive       │
                         │ amountPaid       │         │ expiresAt      │
                         │ balanceDue       │         │ createdAt      │
                         │ loyaltyEarned    │         └────────────────┘
                         │ loyaltyRedeemed  │
                         │ discountUsd      │
                         └────────┬─────────┘
                                  │
                         ┌────────┴─────────┐
                         │                  │
              ┌──────────▼──────────┐   ┌───▼───────────────┐
              │     OrderItem       │   │     Payment       │
              ├─────────────────────┤   ├───────────────────┤
              │ id (PK)             │   │ id (PK)           │
              │ orderId (FK)        │   │ orderId (FK)      │
              │ itemId              │   │ type              │
              │ name                │   │ amountUsd         │
              │ price               │   │ amountNative      │
              │ qty                 │   │ currency          │
              │ lineTotal           │   │ currencyRate      │
              └─────────────────────┘   │ reference         │
                                        │ meta              │
                                        │ clerkId (FK)      │
                                        │ createdAt         │
                                        └───────────────────┘

┌────────────────┐         ┌──────────────────┐         ┌────────────────┐
│     Item       │         │  ExchangeRate    │         │ StoreCredit   │
├────────────────┤         ├──────────────────┤         ├────────────────┤
│ id (PK)        │         │ id (PK)          │         │ id (PK)       │
│ sku (UK)       │         │ fromCurrency     │         │ customerId FK │
│ name           │         │ toCurrency       │         │ balance       │
│ price          │         │ rate             │         │ totalEarned   │
│ category       │         │ updatedAt        │         │ totalSpent    │
│ active         │         └──────────────────┘         │ createdAt     │
│ stockQty       │                                         └────────────────┘
│ lowStock       │
│ description    │         ┌──────────────────┐
│ barcode        │         │   SessionLog     │
│ createdAt      │         ├──────────────────┤
└────────────────┘         │ id (PK)          │
                           │ clerkId (FK)     │
                           │ action           │
                           │ details          │
                           │ ipAddress        │
                           │ createdAt        │
                           └──────────────────┘
```

### Schema Enhancements from Base

1. **GiftCard** - Track gift cards with codes, balances, expiration
2. **StoreCredit** - Customer store credit balances (separate from loyalty)
3. **ExchangeRate** - Real-time currency conversion rates
4. **SessionLog** - Audit trail for clerk actions
5. **Item Enhancements** - Stock tracking, barcodes, descriptions, low stock alerts
6. **Payment Enhancements** - Link to clerk, full metadata support

---

## Authentication Flow

```
┌─────────┐     ┌─────────────┐     ┌──────────────┐     ┌────────────┐
│  Clerk  │     │  Login Page │     │   API Auth   │     │  JWT Token │
└────┬────┘     └──────┬──────┘     └──────┬───────┘     └─────┬──────┘
     │                 │                   │                   │
     │ Enter PIN       │                   │                   │
     │────────────────►│                   │                   │
     │                 │ POST /api/auth    │                   │
     │                 │──────────────────►│                   │
     │                 │                   │ Verify PIN        │
     │                 │                   │ Create Session    │
     │                 │                   ├──────────────────►│
     │                 │                   │                   │
     │                 │  200 OK + Cookie  │                   │
     │                 │◄──────────────────│                   │
     │                 │                   │                   │
     │    Redirect     │                   │                   │
     │◄────────────────│                   │                   │
     │                 │                   │                   │
     │                 │                   │                   │
     │ ════════════════ Authenticated Actions ═══════════════ │
     │                 │                   │                   │
     │ Request + Cookie│                   │                   │
     │─────────────────►│                  │                   │
     │                   │  Verify Token    │                   │
     │                   │──────────────────┤                   │
     │                   │                  │                   │
     │                   │  Session Data    │                   │
     │◄──────────────────│                  │                   │
```

### Session Cookie
- Name: `rs79_session`
- HttpOnly: true
- Secure: production only
- SameSite: strict
- MaxAge: 12 hours

---

## API Route Structure

### RESTful Endpoints

```
/api
├── auth
│   ├── POST /login              # PIN-based login
│   └── POST /logout             # Clear session
├── clerks
│   ├── GET    /                 # List clerks (admin only)
│   ├── POST   /                 # Create clerk
│   ├── GET    /[id]             # Get clerk
│   ├── PATCH  /[id]             # Update clerk
│   └── DELETE /[id]             # Deactivate clerk
├── orders
│   ├── GET    /                 # List orders (with filters)
│   ├── POST   /                 # Create order
│   ├── GET    /[id]             # Get order details
│   ├── PATCH  /[id]             # Update order status
│   ├── POST   /[id]/payments    # Add payment to order
│   └── POST   /[id]/void        # Void order
├── customers
│   ├── GET    /                 # Search customers
│   ├── POST   /                 # Create customer
│   ├── GET    /[id]             # Get customer
│   ├── PATCH  /[id]             # Update customer
│   └── GET    /[id]/orders      # Customer order history
├── items
│   ├── GET    /                 # List/search items
│   ├── POST   /                 # Create item (admin)
│   ├── GET    /[id]             # Get item
│   ├── PATCH  /[id]             # Update item
│   └── DELETE /[id]             # Delete item
├── payments
│   ├── POST   /split            # Calculate split payment
│   ├── POST   /giftcard/verify  # Verify gift card
│   └── POST   /giftcard/use     # Apply gift card
├── reports
│   ├── GET    /daily            # Daily summary
│   ├── GET    /clerk            # Clerk performance
│   ├── GET    /items            # Item sales
│   └── GET    /payments         # Payment methods
└── kds
    ├── GET    /orders           # Orders for kitchen (SSE)
    └── PATCH  /orders/[id]      # Mark order done
```

### Response Format

```typescript
// Success
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}

// Error
{
  "success": false,
  "error": {
    "code": "INVALID_PIN",
    "message": "Invalid PIN code"
  }
}
```

---

## Component Architecture

### Component Hierarchy

```
Layout
├── Header
│   ├── ClerkInfo
│   ├── CurrencySelector
│   └── QuickActions
├── Sidebar (conditional)
└── Main Content
    ├── POS Register
    │   ├── ItemGrid
    │   │   ├── CategoryTabs
    │   │   └── ItemCard
    │   ├── CartPanel
    │   │   ├── CartItem
    │   │   ├── CartTotals
    │   │   └── PaymentButtons
    │   └── PaymentModal
    │       ├── PaymentTypeSelector
    │       ├── AmountInput
    │       ├── SplitPaymentPanel
    │       └── GiftCardInput
    ├── OrderHistory
    │   ├── OrderFilters
    │   ├── OrderTable
    │   └── OrderDetailsModal
    ├── CustomerManager
    │   ├── CustomerSearch
    │   ├── CustomerList
    │   └── CustomerForm
    └── KDS Display
        ├── OrderTicket (new)
        └── OrderTicket (done)
```

### Component Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| **UI Primitives** | Base components | Button, Input, Card, Modal, Badge |
| **POS Components** | Register-specific | Numpad, CartItem, ItemGrid, PaymentPad |
| **KDS Components** | Kitchen display | OrderTicket, Timer, StatusButton |
| **Shared Components** | Cross-feature | DataTable, SearchBar, DatePicker |

---

## State Management

### Client-Side State

```typescript
// Cart State (Zustand/Context)
interface CartState {
  items: CartItem[]
  currency: Currency
  clerk: ClerkSession | null
  customer: Customer | null
  payments: PaymentInput[]
  holdName: string | null
  notes: string | null
  
  // Actions
  addItem: (item: Item) => void
  removeItem: (itemId: string) => void
  updateQuantity: (itemId: string, qty: number) => void
  setCustomer: (customer: Customer | null) => void
  addPayment: (payment: PaymentInput) => void
  removePayment: (index: number) => void
  clearCart: () => void
  calculateTotals: () => Totals
}

// POS UI State
interface UIState {
  activeCategory: string | null
  searchQuery: string
  showPaymentModal: boolean
  showCustomerModal: boolean
  showHoldModal: boolean
}
```

### Server-Side State
- Database via Prisma
- Session cookies for auth
- No server-side session store (stateless JWT)

---

## Multi-Currency System

### Supported Currencies

| Code | Symbol | Rate (to USD) |
|------|--------|---------------|
| USD | $ | 1.0 (base) |
| EUR | € | 0.92 |
| JPY | ¥ | 151.47 |
| GBP | £ | 0.79 |

### Conversion Flow

```
1. All prices stored in USD (base currency)
2. Display: Convert USD → Selected currency
3. Payment: Accept in selected currency
4. Storage: Convert to USD for reports
5. Reporting: All values in USD for consistency
```

### Currency Service

```typescript
interface CurrencyService {
  getRate(from: Currency, to: Currency): number
  convert(amount: number, from: Currency, to: Currency): number
  format(amount: number, currency: Currency): string
  getSupportedCurrencies(): Currency[]
}
```

---

## Payment Processing

### Payment Types

| Type | Flow | Reference Required |
|------|------|-------------------|
| **Cash** | Enter amount tendered, calculate change | No |
| **Card** | External terminal, record reference | Yes (auth code) |
| **Crypto** | External processor, record tx hash | Yes (tx hash) |
| **StoreCredit** | Deduct from customer balance | No |
| **GiftCard** | Validate code, deduct balance | Yes (card code) |
| **Check** | Record check number | Yes (check #) |
| **Split** | Multiple payment types | Per payment |

### Payment Flow

```
┌─────────────┐
│  Order Cart │
└──────┬──────┘
       │ Calculate Total
       ▼
┌─────────────┐     ┌─────────────┐
│  Payment    │────►│  Cash?      │
│  Selection  │     │  Calc Change│
└─────────────┘     └─────────────┘
       │
       ├─────────────► Card → Record Auth Code
       │
       ├─────────────► Crypto → Record TX Hash
       │
       ├─────────────► GiftCard → Validate → Deduct
       │
       ├─────────────► StoreCredit → Check Balance → Deduct
       │
       └─────────────► Split → Multiple Payments
```

---

## Kitchen Display System (KDS)

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                   KDS Display                      │
│  ┌──────────────┐      ┌──────────────┐          │
│  │   Orders     │      │   Orders     │          │
│  │   (New)      │      │   (Done)     │          │
│  │              │      │              │          │
│  │  ┌────────┐  │      │  ┌────────┐  │          │
│  │  │Ticket 1│  │      │  │Ticket X│  │          │
│  │  │ 2m ago │  │      │  │ 5m ago │  │          │
│  │  │[Done]  │  │      │  │[Recall]│  │          │
│  │  └────────┘  │      │  └────────┘  │          │
│  │  ┌────────┐  │      │              │          │
│  │  │Ticket 2│  │      │              │          │
│  │  │ 5m ago │  │      │              │          │
│  │  └────────┘  │      │              │          │
│  └──────────────┘      └──────────────┘          │
└─────────────────────────────────────────────────────┘
                         ▲
                         │ SSE / Polling
                         ▼
               ┌──────────────────┐
               │   Server State   │
               │   order.kdsStatus│
               └──────────────────┘
```

### KDS States

| Status | Meaning | Actions |
|--------|---------|---------|
| `new` | Order received, not started | View, Start, Done |
| `preparing` | Kitchen is working on it | Done |
| `done` | Order complete | Recall |

### Real-time Updates
- **Primary**: Server-Sent Events (SSE) on `/api/kds/orders`
- **Fallback**: Polling every 5 seconds
- **Update Trigger**: Order status changes, new orders

---

## Security Model

### Role-Based Access Control (RBAC)

| Feature | Admin | Manager | Clerk |
|---------|-------|---------|-------|
| View Orders | ✅ | ✅ | ✅ |
| Create Order | ✅ | ✅ | ✅ |
| Void Order | ✅ | ✅ | ✅ |
| Manage Items | ✅ | ✅ | ❌ |
| Manage Clerks | ✅ | ❌ | ❌ |
| View Reports | ✅ | ✅ | ❌ |
| Configure System | ✅ | ❌ | ❌ |
| Access KDS | ✅ | ✅ | ✅ |

### Security Measures

1. **PIN Authentication** - 4-digit clerk PINs (hashed with bcrypt)
2. **JWT Sessions** - Short-lived tokens (12h), HttpOnly cookies
3. **Input Validation** - Zod schemas for all API inputs
4. **SQL Injection Prevention** - Prisma ORM parameterized queries
5. **XSS Protection** - React escaping, CSP headers
6. **CSRF Protection** - SameSite cookies

---

## Performance Considerations

### Optimizations

| Area | Strategy |
|------|----------|
| Database | Indexed lookups on transactionNo, clerkId, customerId |
| Images | Next.js Image optimization for item photos |
| API | Response caching for static data (items) |
| Real-time | SSE for KDS instead of WebSocket for simplicity |
| Bundle | Code splitting by route |

### Database Indexes

```prisma
// Primary lookups
@@index([clerkId])
@@index([customerId])
@@index([transactionNo])
@@index([createdAt])
@@index([status])
@@index([kdsStatus])

// Search
@@index([name])
@@index([sku])
@@index([loyaltyCardNo])
```

---

## Error Handling Strategy

### Error Types

```typescript
type ErrorCode = 
  | 'AUTH_INVALID_PIN'
  | 'AUTH_SESSION_EXPIRED'
  | 'ORDER_NOT_FOUND'
  | 'ORDER_ALREADY_COMPLETED'
  | 'PAYMENT_INSUFFICIENT'
  | 'GIFT_CARD_INVALID'
  | 'GIFT_CARD_EXPIRED'
  | 'GIFT_CARD_INSUFFICIENT'
  | 'STORE_CREDIT_INSUFFICIENT'
  | 'ITEM_NOT_FOUND'
  | 'ITEM_INACTIVE'
  | 'CUSTOMER_NOT_FOUND'
  | 'VALIDATION_ERROR'
  | 'INTERNAL_ERROR'
```

### Error Response Pattern

```typescript
// API errors return 200 with error object
// or appropriate HTTP status codes
{
  "success": false,
  "error": {
    "code": "GIFT_CARD_INSUFFICIENT",
    "message": "Gift card balance ($15.00) is less than payment amount ($25.00)",
    "details": {
      "cardBalance": 15.00,
      "requestedAmount": 25.00
    }
  }
}
```

---

## Testing Strategy

### Test Layers

| Layer | Framework | Coverage |
|-------|-----------|----------|
| Unit | Jest | Services, utilities |
| Component | Testing Library | React components |
| Integration | Playwright | User flows |
| API | Jest + Supertest | API endpoints |
| E2E | Playwright | Critical paths |

### Critical Test Paths

1. Login → Create Order → Process Payment → Complete
2. Login → Load Cart → Apply Gift Card → Complete
3. Login → Create Order → KDS Update → Complete
4. Multi-currency conversion accuracy
5. Split payment calculation

---

## Deployment Architecture

### Target Environment: Abacus AI Platform

```
┌─────────────────────────────────────────────────────┐
│              Abacus AI Platform                    │
│  ┌───────────────────────────────────────────────┐ │
│  │              Next.js Application               │ │
│  │  ┌─────────────┐  ┌─────────────────────────┐ │ │
│  │  │   App       │  │   API Routes             │ │ │
│  │  │   (Static)  │  │   (Serverless Functions) │ │ │
│  │  └─────────────┘  └─────────────────────────┘ │ │
│  └───────────────────────────────────────────────┘ │
│                        │                           │
│                        ▼                           │
│  ┌───────────────────────────────────────────────┐ │
│  │              SQLite Database                  │ │
│  │         (Persistent Volume)                   │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

### Environment Variables

```
# Required
DATABASE_URL="file:./dev.db"
JWT_SECRET="your-production-secret-here"

# Optional
NEXT_PUBLIC_DEFAULT_CURRENCY="USD"
NEXT_PUBLIC_KDS_ENABLED="true"
```

---

## Future Considerations

### Potential Enhancements

1. **Offline Support** - Service workers for offline cart persistence
2. **Multi-store** - Support for multiple locations
3. **Receipt Printing** - ESC/POS thermal printer integration
4. **Barcode Scanning** - USB scanner integration
5. **Inventory Management** - Stock alerts, reorder points
6. **Mobile App** - React Native companion
7. **Analytics Dashboard** - Charts and trends
8. **Loyalty Programs** - Tier-based rewards

---

## Appendix: Type Definitions

See `/src/types/index.ts` for complete type definitions including:
- ClerkSession, ClerkRole
- Order, OrderItem, OrderStatus
- Payment, PaymentType
- Customer, GiftCard
- Currency, ExchangeRate
- KDSOrder, KDSStatus
