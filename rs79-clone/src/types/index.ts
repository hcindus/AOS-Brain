export interface Clerk {
  id: string
  name: string
  role: 'Admin' | 'Manager' | 'Clerk'
  active: boolean
}

export interface Item {
  id: string
  sku: string
  name: string
  price: number
  category: string
  active: boolean
}

export interface CartItem {
  itemId: string
  name: string
  price: number
  qty: number
  lineTotal: number
}

export interface Customer {
  id: string
  name: string
  phone?: string
  loyaltyCardNo: string
  loyaltyPoints: number
}

export type PaymentType = 'cash' | 'card' | 'crypto' | 'storecredit' | 'giftcard' | 'check' | 'split'

export interface Payment {
  type: PaymentType
  amountUsd: number
  amountNative: number
  currency: string
  currencyRate: number
  reference?: string
}

export interface Order {
  id?: string
  transactionNo?: number
  clerkId: string
  customerId?: string
  items: CartItem[]
  subtotal: number
  tax: number
  total: number
  discountUsd: number
  currency: string
  currencyRate: number
  payments: Payment[]
  tendered: number
  change: number
  amountPaid: number
  balanceDue: number
  notes?: string
  holdName?: string
}

export interface Category {
  id: string
  name: string
  icon?: string
  color?: string
}
