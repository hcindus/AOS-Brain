// Re-export all clerk types from clerk.ts
export * from './clerk'

// Payment Types
export type PaymentType = 'cash' | 'card' | 'crypto' | 'storecredit' | 'giftcard' | 'check'

export interface PaymentInput {
  type: PaymentType | 'split'
  amount: number
  reference?: string
  giftCardCode?: string
  currency?: string
  currencyRate?: number
  checkNumber?: string
  walletAddress?: string
  storeCreditAmount?: number
}

export interface Payment {
  id: string
  orderId: string
  clerkId: string
  type: PaymentType
  amountUsd: number
  amountNative: number
  currency: string
  currencyRate: number
  reference?: string
  meta?: string
  createdAt: Date
}

// Order Types
export type OrderStatus = 'completed' | 'pending' | 'cancelled' | 'voided'
export type KDSStatus = 'new' | 'preparing' | 'done'

export interface OrderItem {
  id: string
  orderId: string
  itemId: string
  name: string
  price: number
  qty: number
  lineTotal: number
}

export interface Order {
  id: string
  transactionNo: number
  clerkId: string
  customerId?: string
  subtotal: number
  tax: number
  total: number
  currency: string
  currencyRate: number
  paymentType: string
  tendered?: number
  change?: number
  status: OrderStatus
  kdsStatus: KDSStatus
  holdName?: string
  notes?: string
  amountPaid: number
  balanceDue: number
  loyaltyEarned: number
  loyaltyRedeemed: number
  discountUsd: number
  voidReason?: string
  voidedAt?: Date
  createdAt: Date
  updatedAt: Date
  items?: OrderItem[]
  payments?: Payment[]
  clerk?: ClerkInfo
  customer?: Customer
}

// Clerk Info (simplified reference)
export interface ClerkInfo {
  id: string
  name: string
  role: string
}

// Customer Types
export interface Customer {
  id: string
  name: string
  phone?: string
  loyaltyCardNo: string
  loyaltyPoints: number
  createdAt: Date
  storeCredit?: StoreCredit
}

export interface StoreCredit {
  id: string
  customerId: string
  balance: number
  totalEarned: number
  totalSpent: number
  createdAt: Date
}

// Gift Card Types
export interface GiftCard {
  id: string
  code: string
  balance: number
  originalAmount: number
  isActive: boolean
  expiresAt?: Date
  createdAt: Date
}

// Item Types
export interface Item {
  id: string
  sku: string
  name: string
  price: number
  category: string
  taxCategory?: string // standard, reduced, zero, exempt
  taxRate?: number     // Override rate
  description?: string
  barcode?: string
  stockQty: number
  lowStock: number
  active: boolean
  createdAt: Date
}

// Currency Types
export interface ExchangeRate {
  id: string
  fromCurrency: string
  toCurrency: string
  rate: number
  updatedAt: Date
}

export type CurrencyCode = 'USD' | 'EUR' | 'JPY' | 'GBP'

export interface Currency {
  code: CurrencyCode
  symbol: string
  name: string
}

// KDS Types
export interface KDSOrder {
  id: string
  transactionNo: number
  items: OrderItem[]
  notes?: string
  status: KDSStatus
  createdAt: Date
  elapsedMinutes: number
}

// Cart Types
export interface CartItem {
  itemId: string
  name: string
  price: number
  qty: number
  lineTotal: number
}

export interface Cart {
  items: CartItem[]
  customer?: Customer
  currency: CurrencyCode
  holdName?: string
  notes?: string
}

// Held Order Types
export interface HeldOrder {
  id: string
  holdName: string
  items: CartItem[]
  subtotal: number
  tax: number
  total: number
  customerId?: string
  customerName?: string
  createdAt: string
}

// API Response Types
export interface ApiResponse<T = unknown> {
  success: boolean
  data?: T
  error?: {
    code: string
    message: string
    details?: Record<string, unknown>
  }
  meta?: {
    page?: number
    limit?: number
    total?: number
  }
}
