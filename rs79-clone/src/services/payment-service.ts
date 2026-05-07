import { prisma } from '@/lib/prisma'
import { ValidationError, PaymentError, NotFoundError } from '@/lib/errors'
import type { Payment, GiftCard, StoreCredit } from '@prisma/client'

export interface ProcessPaymentInput {
  orderId: string
  clerkId: string
  type: 'cash' | 'card' | 'crypto' | 'storecredit' | 'giftcard' | 'check'
  amountUsd: number
  currency?: string
  currencyRate?: number
  reference?: string
  meta?: Record<string, unknown>
  giftCardCode?: string
  customerId?: string
}

export interface PaymentResult {
  payment: Payment
  changeDue?: number
  giftCardBalance?: number
  storeCreditBalance?: number
}

/**
 * Process a payment for an order
 */
export async function processPayment(input: ProcessPaymentInput): Promise<PaymentResult> {
  // Validate required fields
  if (!input.orderId) {
    throw new ValidationError('Order ID is required')
  }
  if (!input.clerkId) {
    throw new ValidationError('Clerk ID is required')
  }
  if (!input.type) {
    throw new ValidationError('Payment type is required')
  }
  if (input.amountUsd <= 0) {
    throw new ValidationError('Payment amount must be greater than 0')
  }

  // Get the order
  const order = await prisma.order.findUnique({
    where: { id: input.orderId },
    include: { payments: true },
  })

  if (!order) {
    throw new NotFoundError(`Order ${input.orderId} not found`)
  }

  if (order.status === 'voided') {
    throw new ValidationError('Cannot process payment for a voided order')
  }

  // Calculate amount already paid
  const totalPaid = order.payments.reduce((sum, p) => sum + p.amountUsd, 0)
  const remainingBalance = order.total - totalPaid

  // Handle gift card payment
  let giftCard: GiftCard | null = null
  if (input.type === 'giftcard') {
    if (!input.giftCardCode) {
      throw new ValidationError('Gift card code is required for gift card payments')
    }
    
    giftCard = await validateGiftCard(input.giftCardCode)
    
    if (giftCard.balance < input.amountUsd) {
      throw new PaymentError(
        `Insufficient gift card balance. Available: $${giftCard.balance.toFixed(2)}, Requested: $${input.amountUsd.toFixed(2)}`
      )
    }

    // Deduct from gift card
    await deductGiftCardBalance(giftCard.id, input.amountUsd)
  }

  // Handle store credit payment
  let storeCredit: StoreCredit | null = null
  if (input.type === 'storecredit') {
    if (!order.customerId) {
      throw new PaymentError('Store credit payments require a customer')
    }
    
    storeCredit = await prisma.storeCredit.findUnique({
      where: { customerId: order.customerId },
    })

    if (!storeCredit) {
      throw new PaymentError('Customer has no store credit account')
    }

    if (storeCredit.balance < input.amountUsd) {
      throw new PaymentError(
        `Insufficient store credit balance. Available: $${storeCredit.balance.toFixed(2)}, Requested: $${input.amountUsd.toFixed(2)}`
      )
    }

    // Deduct from store credit
    await prisma.storeCredit.update({
      where: { id: storeCredit.id },
      data: {
        balance: { decrement: input.amountUsd },
        totalSpent: { increment: input.amountUsd },
      },
    })
  }

  // Calculate native amount based on currency
  const currency = input.currency ?? 'USD'
  const currencyRate = input.currencyRate ?? 1
  const amountNative = currency === 'USD' ? input.amountUsd : input.amountUsd * currencyRate

  // Create the payment record
  const payment = await prisma.payment.create({
    data: {
      orderId: input.orderId,
      clerkId: input.clerkId,
      type: input.type,
      amountUsd: input.amountUsd,
      amountNative,
      currency,
      currencyRate,
      reference: input.reference,
      meta: input.meta ? JSON.stringify(input.meta) : null,
    },
  })

  // Update order balance
  const newTotalPaid = totalPaid + input.amountUsd
  const balanceDue = order.total - newTotalPaid

  await prisma.order.update({
    where: { id: input.orderId },
    data: {
      amountPaid: newTotalPaid,
      balanceDue: balanceDue > 0 ? balanceDue : 0,
      status: balanceDue <= 0 ? 'completed' : 'pending',
    },
  })

  return {
    payment,
    changeDue: balanceDue < 0 ? Math.abs(balanceDue) : 0,
    giftCardBalance: giftCard ? giftCard.balance - input.amountUsd : undefined,
    storeCreditBalance: storeCredit ? storeCredit.balance - input.amountUsd : undefined,
  }
}

/**
 * Calculate change due for cash payments
 */
export function calculateChange(tendered: number, totalDue: number): {
  change: number
  isValid: boolean
  error?: string
} {
  if (tendered < 0) {
    return { change: 0, isValid: false, error: 'Tendered amount cannot be negative' }
  }

  if (totalDue < 0) {
    return { change: 0, isValid: false, error: 'Total due cannot be negative' }
  }

  const change = tendered - totalDue

  if (change < 0) {
    return { 
      change: Math.abs(change), 
      isValid: false, 
      error: `Insufficient payment. Additional $${Math.abs(change).toFixed(2)} required` 
    }
  }

  return { change, isValid: true }
}

/**
 * Validate a gift card by code
 */
export async function validateGiftCard(code: string): Promise<GiftCard> {
  if (!code || code.trim().length === 0) {
    throw new ValidationError('Gift card code is required')
  }

  const giftCard = await prisma.giftCard.findUnique({
    where: { code: code.trim().toUpperCase() },
  })

  if (!giftCard) {
    throw new NotFoundError(`Gift card ${code} not found`)
  }

  if (!giftCard.isActive) {
    throw new PaymentError('Gift card is inactive')
  }

  if (giftCard.expiresAt && new Date() > giftCard.expiresAt) {
    throw new PaymentError('Gift card has expired')
  }

  if (giftCard.balance <= 0) {
    throw new PaymentError('Gift card has no remaining balance')
  }

  return giftCard
}

/**
 * Get gift card balance
 */
export async function getGiftCardBalance(code: string): Promise<{
  code: string
  balance: number
  originalAmount: number
  isActive: boolean
  expiresAt: Date | null
}> {
  const giftCard = await prisma.giftCard.findUnique({
    where: { code: code.trim().toUpperCase() },
  })

  if (!giftCard) {
    throw new NotFoundError(`Gift card ${code} not found`)
  }

  return {
    code: giftCard.code,
    balance: giftCard.balance,
    originalAmount: giftCard.originalAmount,
    isActive: giftCard.isActive,
    expiresAt: giftCard.expiresAt,
  }
}

/**
 * Deduct balance from gift card
 */
export async function deductGiftCardBalance(
  giftCardId: string,
  amount: number
): Promise<GiftCard> {
  if (amount <= 0) {
    throw new ValidationError('Deduction amount must be greater than 0')
  }

  const giftCard = await prisma.giftCard.findUnique({
    where: { id: giftCardId },
  })

  if (!giftCard) {
    throw new NotFoundError('Gift card not found')
  }

  if (giftCard.balance < amount) {
    throw new PaymentError(
      `Insufficient balance. Available: $${giftCard.balance.toFixed(2)}, Requested: $${amount.toFixed(2)}`
    )
  }

  const updated = await prisma.giftCard.update({
    where: { id: giftCardId },
    data: {
      balance: { decrement: amount },
    },
  })

  return updated
}

/**
 * Apply store credit to a customer
 */
export async function applyStoreCredit(
  customerId: string,
  amount: number,
  reason: string
): Promise<StoreCredit> {
  if (amount <= 0) {
    throw new ValidationError('Store credit amount must be greater than 0')
  }

  if (!reason || reason.trim().length === 0) {
    throw new ValidationError('Reason for store credit is required')
  }

  const existingCredit = await prisma.storeCredit.findUnique({
    where: { customerId },
  })

  let storeCredit: StoreCredit

  if (existingCredit) {
    storeCredit = await prisma.storeCredit.update({
      where: { id: existingCredit.id },
      data: {
        balance: { increment: amount },
        totalEarned: { increment: amount },
      },
    })
  } else {
    storeCredit = await prisma.storeCredit.create({
      data: {
        customerId,
        balance: amount,
        totalEarned: amount,
        totalSpent: 0,
      },
    })
  }

  // Log the credit application
  await prisma.sessionLog.create({
    data: {
      clerkId: 'system',
      action: 'STORE_CREDIT_APPLIED',
      details: `Store credit of $${amount.toFixed(2)} applied to customer ${customerId}. Reason: ${reason}`,
    },
  })

  return storeCredit
}

/**
 * Refund a payment
 */
export async function refundPayment(
  paymentId: string,
  clerkId: string,
  reason: string
): Promise<Payment> {
  if (!reason || reason.trim().length === 0) {
    throw new ValidationError('Refund reason is required')
  }

  const payment = await prisma.payment.findUnique({
    where: { id: paymentId },
    include: { order: true },
  })

  if (!payment) {
    throw new NotFoundError(`Payment ${paymentId} not found`)
  }

  // For gift card payments, return to gift card
  if (payment.type === 'giftcard' && payment.meta) {
    const meta = JSON.parse(payment.meta) as { giftCardCode?: string }
    if (meta.giftCardCode) {
      const giftCard = await prisma.giftCard.findUnique({
        where: { code: meta.giftCardCode },
      })
      if (giftCard) {
        await prisma.giftCard.update({
          where: { id: giftCard.id },
          data: { balance: { increment: payment.amountUsd } },
        })
      }
    }
  }

  // For store credit payments, return to store credit
  if (payment.type === 'storecredit' && payment.order.customerId) {
    await prisma.storeCredit.update({
      where: { customerId: payment.order.customerId },
      data: {
        balance: { increment: payment.amountUsd },
        totalSpent: { decrement: payment.amountUsd },
      },
    })
  }

  // Create a refund payment record (negative amount)
  const refundPayment = await prisma.payment.create({
    data: {
      orderId: payment.orderId,
      clerkId,
      type: 'cash', // Refund as cash by default
      amountUsd: -payment.amountUsd,
      amountNative: -payment.amountNative,
      currency: payment.currency,
      currencyRate: payment.currencyRate,
      reference: `REFUND-${paymentId}`,
      meta: JSON.stringify({ originalPaymentId: paymentId, reason }),
    },
  })

  // Update order balance
  await prisma.order.update({
    where: { id: payment.orderId },
    data: {
      amountPaid: { decrement: payment.amountUsd },
      balanceDue: { increment: payment.amountUsd },
    },
  })

  // Log the refund
  await prisma.sessionLog.create({
    data: {
      clerkId,
      action: 'PAYMENT_REFUNDED',
      details: `Payment ${paymentId} refunded. Amount: $${payment.amountUsd.toFixed(2)}. Reason: ${reason}`,
    },
  })

  return refundPayment
}
