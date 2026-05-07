# RS-79 Clone — Proof of Concept

Based on reverse-engineered rs79.abacusai.app architecture.

## Discovered Stack
- **Framework:** Next.js 14+ (App Router)
- **Auth:** JWT session cookies (rs79_session)
- **Database:** Prisma (PostgreSQL inferred from CUIDs)
- **Platform:** Abacus AI (abacusai.app)

## API Endpoints Mapped

### Auth
- `POST /api/auth/login` — {clerkId, pin} → {success, clerk, session}

### Data
- `GET /api/clerks` — List all clerks
- `GET /api/orders` — List all orders with items, payments, customers

## Entity Schema (Discovered)

### Clerk
- id: CUID (cmo...)
- name: string
- role: Admin | Manager | Clerk
- active: boolean
- createdAt: ISO8601

### Order
- id: CUID
- transactionNo: number (auto-increment)
- clerkId: CUID
- customerId: CUID | null
- subtotal, tax, total: number
- currency: USD | EUR | JPY | GBP
- currencyRate: number
- paymentType: cash | card | crypto | storecredit | giftcard | check | split
- tendered, change: number | null
- status: completed | pending | cancelled
- kdsStatus: new | done
- items: OrderItem[]
- payments: Payment[]
- clerk: Clerk
- customer: Customer | null

### OrderItem
- id: CUID
- orderId: CUID
- itemId: string (item-* patterns)
- name: string
- price: number
- qty: number
- lineTotal: number

### Payment
- id: CUID
- orderId: CUID
- type: cash | card | crypto | storecredit | giftcard | check
- amountUsd, amountNative: number
- currency: string
- currencyRate: number
- reference, meta: any

### Customer
- id: CUID
- name: string
- phone: string | null
- loyaltyCardNo: string
- loyaltyPoints: number

