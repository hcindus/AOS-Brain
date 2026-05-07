import { z } from 'zod'

// ==========================================
// Order Validation Schemas
// ==========================================

export const orderItemSchema = z.object({
  itemId: z.string().min(1, 'Item ID is required'),
  name: z.string().min(1, 'Item name is required'),
  price: z.number().min(0, 'Price cannot be negative'),
  qty: z.number().min(0.01, 'Quantity must be greater than 0'),
})

export const createOrderSchema = z.object({
  clerkId: z.string().min(1, 'Clerk ID is required'),
  customerId: z.string().optional(),
  items: z.array(orderItemSchema).min(1, 'Order must have at least one item'),
  subtotal: z.number().min(0, 'Subtotal cannot be negative'),
  tax: z.number().min(0, 'Tax cannot be negative'),
  total: z.number().min(0, 'Total cannot be negative'),
  currency: z.string().default('USD'),
  currencyRate: z.number().default(1),
  paymentType: z.enum(['cash', 'card', 'crypto', 'storecredit', 'giftcard', 'check', 'split']),
  tendered: z.number().min(0).optional(),
  change: z.number().min(0).optional(),
  holdName: z.string().optional(),
  notes: z.string().optional(),
  loyaltyRedeemed: z.number().min(0).default(0),
  discountUsd: z.number().min(0).default(0),
})

export const updateOrderStatusSchema = z.object({
  orderId: z.string().min(1, 'Order ID is required'),
  status: z.enum(['completed', 'pending', 'cancelled']),
})

export const voidOrderSchema = z.object({
  orderId: z.string().min(1, 'Order ID is required'),
  voidReason: z.string().min(1, 'Void reason is required'),
  clerkId: z.string().min(1, 'Clerk ID is required'),
})

export const updateKdsStatusSchema = z.object({
  orderId: z.string().min(1, 'Order ID is required'),
  kdsStatus: z.enum(['new', 'preparing', 'done']),
})

// ==========================================
// Payment Validation Schemas
// ==========================================

export const processPaymentSchema = z.object({
  orderId: z.string().min(1, 'Order ID is required'),
  clerkId: z.string().min(1, 'Clerk ID is required'),
  type: z.enum(['cash', 'card', 'crypto', 'storecredit', 'giftcard', 'check']),
  amountUsd: z.number().min(0.01, 'Payment amount must be greater than 0'),
  currency: z.string().default('USD'),
  currencyRate: z.number().default(1),
  reference: z.string().optional(),
  meta: z.record(z.unknown()).optional(),
  giftCardCode: z.string().optional(),
  customerId: z.string().optional(),
})

export const calculateChangeSchema = z.object({
  tendered: z.number().min(0, 'Tendered amount cannot be negative'),
  totalDue: z.number().min(0, 'Total due cannot be negative'),
})

export const refundPaymentSchema = z.object({
  paymentId: z.string().min(1, 'Payment ID is required'),
  clerkId: z.string().min(1, 'Clerk ID is required'),
  reason: z.string().min(1, 'Refund reason is required'),
})

// ==========================================
// Customer Validation Schemas
// ==========================================

export const createCustomerSchema = z.object({
  name: z.string().min(1, 'Customer name is required').max(100, 'Name too long'),
  phone: z.string().regex(/^\+?[\d\-\s\(\)]{10,}$/, 'Invalid phone number').optional(),
  loyaltyCardNo: z.string().optional(),
  loyaltyPoints: z.number().min(0).default(0),
})

export const updateCustomerSchema = z.object({
  customerId: z.string().min(1, 'Customer ID is required'),
  name: z.string().min(1).max(100).optional(),
  phone: z.string().regex(/^\+?[\d\-\s\(\)]{10,}$/, 'Invalid phone number').optional(),
})

export const updateLoyaltyPointsSchema = z.object({
  customerId: z.string().min(1, 'Customer ID is required'),
  pointsToAdd: z.number(),
})

export const redeemLoyaltyPointsSchema = z.object({
  customerId: z.string().min(1, 'Customer ID is required'),
  pointsToRedeem: z.number().min(1, 'Must redeem at least 1 point'),
})

export const addStoreCreditSchema = z.object({
  customerId: z.string().min(1, 'Customer ID is required'),
  amount: z.number().min(0.01, 'Amount must be greater than 0'),
  reason: z.string().min(1, 'Reason is required'),
})

// ==========================================
// Gift Card Validation Schemas
// ==========================================

export const createGiftCardSchema = z.object({
  code: z.string().optional(),
  originalAmount: z.number().min(0.01, 'Amount must be greater than 0'),
  expiresAt: z.date().optional(),
})

export const applyGiftCardSchema = z.object({
  code: z.string().min(1, 'Gift card code is required'),
  amount: z.number().min(0.01, 'Amount must be greater than 0').optional(),
})

export const validateGiftCardSchema = z.object({
  code: z.string().min(1, 'Gift card code is required'),
})

export const deductGiftCardSchema = z.object({
  code: z.string().min(1, 'Gift card code is required'),
  amount: z.number().min(0.01, 'Amount must be greater than 0'),
})

export const addGiftCardBalanceSchema = z.object({
  code: z.string().min(1, 'Gift card code is required'),
  amount: z.number().min(0.01, 'Amount must be greater than 0'),
  reason: z.string().optional(),
})

export const deactivateGiftCardSchema = z.object({
  code: z.string().min(1, 'Gift card code is required'),
  reason: z.string().optional(),
})

// ==========================================
// Clerk Validation Schemas
// ==========================================

export const createClerkSchema = z.object({
  name: z.string().min(1, 'Clerk name is required').max(100),
  role: z.enum(['Admin', 'Manager', 'Clerk']),
  pin: z.string().regex(/^\d{4}$/, 'PIN must be exactly 4 digits'),
  active: z.boolean().default(true),
})

export const authenticateClerkSchema = z.object({
  name: z.string().min(1, 'Clerk name is required'),
  pin: z.string().min(1, 'PIN is required'),
})

export const updateClerkPinSchema = z.object({
  clerkId: z.string().min(1, 'Clerk ID is required'),
  newPin: z.string().regex(/^\d{4}$/, 'PIN must be exactly 4 digits'),
})

// ==========================================
// Item Validation Schemas
// ==========================================

export const createItemSchema = z.object({
  sku: z.string().min(1, 'SKU is required').max(50),
  name: z.string().min(1, 'Item name is required').max(200),
  price: z.number().min(0, 'Price cannot be negative'),
  category: z.string().min(1, 'Category is required'),
  stockQty: z.number().int().min(0).default(0),
  lowStock: z.number().int().min(0).default(10),
  description: z.string().optional(),
  barcode: z.string().optional(),
  active: z.boolean().default(true),
})

export const updateItemSchema = z.object({
  itemId: z.string().min(1, 'Item ID is required'),
  sku: z.string().min(1).max(50).optional(),
  name: z.string().min(1).max(200).optional(),
  price: z.number().min(0).optional(),
  category: z.string().min(1).optional(),
  stockQty: z.number().int().min(0).optional(),
  lowStock: z.number().int().min(0).optional(),
  description: z.string().optional(),
  barcode: z.string().optional(),
  active: z.boolean().optional(),
})

export const updateStockSchema = z.object({
  itemId: z.string().min(1, 'Item ID is required'),
  quantity: z.number().int(),
  reason: z.string().optional(),
})

// ==========================================
// Session Log Validation Schemas
// ==========================================

export const createSessionLogSchema = z.object({
  clerkId: z.string().min(1, 'Clerk ID is required'),
  action: z.string().min(1, 'Action is required'),
  details: z.string().optional(),
  ipAddress: z.string().ip().optional(),
})

export const sessionLogQuerySchema = z.object({
  clerkId: z.string().optional(),
  action: z.string().optional(),
  startDate: z.date().optional(),
  endDate: z.date().optional(),
  limit: z.number().int().min(1).max(1000).default(50),
  offset: z.number().int().min(0).default(0),
})

// ==========================================
// Exchange Rate Validation Schemas
// ==========================================

export const createExchangeRateSchema = z.object({
  fromCurrency: z.string().min(3, 'Currency code must be 3 characters').max(3),
  toCurrency: z.string().min(3, 'Currency code must be 3 characters').max(3),
  rate: z.number().min(0.0001, 'Rate must be greater than 0'),
})

export const convertCurrencySchema = z.object({
  amount: z.number().min(0),
  fromCurrency: z.string().min(3).max(3),
  toCurrency: z.string().min(3).max(3),
})

// ==========================================
// Type Exports
// ==========================================

export type CreateOrderInput = z.infer<typeof createOrderSchema>
export type OrderItemInput = z.infer<typeof orderItemSchema>
export type UpdateOrderStatusInput = z.infer<typeof updateOrderStatusSchema>
export type VoidOrderInput = z.infer<typeof voidOrderSchema>
export type UpdateKdsStatusInput = z.infer<typeof updateKdsStatusSchema>

export type ProcessPaymentInput = z.infer<typeof processPaymentSchema>
export type CalculateChangeInput = z.infer<typeof calculateChangeSchema>
export type RefundPaymentInput = z.infer<typeof refundPaymentSchema>

export type CreateCustomerInput = z.infer<typeof createCustomerSchema>
export type UpdateCustomerInput = z.infer<typeof updateCustomerSchema>
export type UpdateLoyaltyPointsInput = z.infer<typeof updateLoyaltyPointsSchema>
export type RedeemLoyaltyPointsInput = z.infer<typeof redeemLoyaltyPointsSchema>
export type AddStoreCreditInput = z.infer<typeof addStoreCreditSchema>

export type CreateGiftCardInput = z.infer<typeof createGiftCardSchema>
export type ApplyGiftCardInput = z.infer<typeof applyGiftCardSchema>
export type ValidateGiftCardInput = z.infer<typeof validateGiftCardSchema>
export type DeductGiftCardInput = z.infer<typeof deductGiftCardSchema>
export type AddGiftCardBalanceInput = z.infer<typeof addGiftCardBalanceSchema>
export type DeactivateGiftCardInput = z.infer<typeof deactivateGiftCardSchema>

export type CreateClerkInput = z.infer<typeof createClerkSchema>
export type AuthenticateClerkInput = z.infer<typeof authenticateClerkSchema>
export type UpdateClerkPinInput = z.infer<typeof updateClerkPinSchema>

export type CreateItemInput = z.infer<typeof createItemSchema>
export type UpdateItemInput = z.infer<typeof updateItemSchema>
export type UpdateStockInput = z.infer<typeof updateStockSchema>

export type CreateSessionLogInput = z.infer<typeof createSessionLogSchema>
export type SessionLogQueryInput = z.infer<typeof sessionLogQuerySchema>

export type CreateExchangeRateInput = z.infer<typeof createExchangeRateSchema>
export type ConvertCurrencyInput = z.infer<typeof convertCurrencySchema>
