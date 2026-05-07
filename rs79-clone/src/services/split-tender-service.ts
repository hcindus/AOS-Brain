import { prisma } from '@/lib/prisma'
import { ValidationError, NotFoundError, PaymentError } from '@/lib/errors'
import type { Payment, Order } from '@prisma/client'

export interface SplitTenderInput {
  orderId: string
  clerkId: string
  payments: Array<{
    type: 'cash' | 'card' | 'crypto' | 'storecredit' | 'giftcard' | 'check'
    amount: number
    reference?: string
    giftCardCode?: string
  }>
}

export interface SplitTenderPayment {
  id: string
  type: string
  amount: number
  reference?: string
  timestamp: Date
}

export interface SplitTenderStatus {
  totalDue: number
  totalPaid: number
  remainingBalance: number
  payments: SplitTenderPayment[]
  isComplete: boolean
}

/**
 * Process multiple payments for a single transaction
 */
export async function processSplitTender(input: SplitTenderInput): Promise<{
  payments: Payment[]
  totalPaid: number
  remainingBalance: number
  changeDue: number
  isComplete: boolean
}> {
  const { orderId, clerkId, payments } = input

  if (!payments || payments.length === 0) {
    throw new ValidationError('At least one payment is required')
  }

  // Get the order
  const order = await prisma.order.findUnique({
    where: { id: orderId },
    include: { payments: true },
  })

  if (!order) {
    throw new NotFoundError(`Order ${orderId} not found`)
  }

  if (order.status === 'voided') {
    throw new PaymentError('Cannot process payments for a voided order')
  }

  // Calculate totals
  const totalDue = order.total
  const alreadyPaid = order.payments.reduce((sum, p) => sum + p.amountUsd, 0)
  const remainingBeforeThis = totalDue - alreadyPaid

  // Validate total payment amount doesn't exceed remaining balance by too much
  const totalPaymentAmount = payments.reduce((sum, p) => sum + p.amount, 0)

  const createdPayments: Payment[] = []
  let runningTotal = alreadyPaid
  let lastPaymentOverage = 0

  // Process each payment
  for (let i = 0; i < payments.length; i++) {
    const payment = payments[i]
    const isLastPayment = i === payments.length - 1

    // Validate payment type
    if (!['cash', 'card', 'crypto', 'storecredit', 'giftcard', 'check'].includes(payment.type)) {
      throw new ValidationError(`Invalid payment type: ${payment.type}`)
    }

    // Handle gift card payment
    if (payment.type === 'giftcard' && payment.giftCardCode) {
      const giftCard = await prisma.giftCard.findUnique({
        where: { code: payment.giftCardCode.toUpperCase() },
      })

      if (!giftCard || !giftCard.isActive) {
        throw new PaymentError(`Invalid gift card: ${payment.giftCardCode}`)
      }

      if (giftCard.expiresAt && new Date() > giftCard.expiresAt) {
        throw new PaymentError('Gift card has expired')
      }

      if (giftCard.balance < payment.amount) {
        throw new PaymentError(
          `Insufficient gift card balance. Available: $${giftCard.balance.toFixed(2)}`
        )
      }

      // Deduct from gift card
      await prisma.giftCard.update({
        where: { id: giftCard.id },
        data: { balance: { decrement: payment.amount } },
      })
    }

    // Handle store credit payment
    if (payment.type === 'storecredit' && order.customerId) {
      const storeCredit = await prisma.storeCredit.findUnique({
        where: { customerId: order.customerId },
      })

      if (!storeCredit) {
        throw new PaymentError('Customer has no store credit account')
      }

      if (storeCredit.balance < payment.amount) {
        throw new PaymentError(
          `Insufficient store credit. Available: $${storeCredit.balance.toFixed(2)}`
        )
      }

      // Deduct from store credit
      await prisma.storeCredit.update({
        where: { id: storeCredit.id },
        data: {
          balance: { decrement: payment.amount },
          totalSpent: { increment: payment.amount },
        },
      })
    }

    // Calculate actual amount (don't overpay except on last payment)
    let actualAmount = payment.amount
    if (!isLastPayment && runningTotal + payment.amount > totalDue) {
      actualAmount = totalDue - runningTotal
      if (actualAmount < 0) actualAmount = 0
    }

    // Create payment record
    const paymentRecord = await prisma.payment.create({
      data: {
        orderId,
        clerkId,
        type: payment.type,
        amountUsd: actualAmount,
        amountNative: actualAmount,
        currency: 'USD',
        currencyRate: 1,
        reference: payment.reference,
        meta: JSON.stringify({
          splitTender: true,
          giftCardCode: payment.giftCardCode,
          requestedAmount: payment.amount,
        }),
      },
    })

    createdPayments.push(paymentRecord)
    runningTotal += actualAmount

    // Track overage on last payment for change calculation
    if (isLastPayment) {
      lastPaymentOverage = payment.amount - actualAmount
    }
  }

  // Calculate final status
  const remainingBalance = Math.max(0, totalDue - runningTotal)
  const changeDue = remainingBalance === 0 ? lastPaymentOverage : 0
  const isComplete = remainingBalance === 0

  // Update order
  await prisma.order.update({
    where: { id: orderId },
    data: {
      amountPaid: runningTotal,
      balanceDue: remainingBalance,
      status: isComplete ? 'completed' : 'pending',
      paymentType: 'split',
      tendered: runningTotal,
      change: changeDue,
    },
  })

  return {
    payments: createdPayments,
    totalPaid: runningTotal,
    remainingBalance,
    changeDue,
    isComplete,
  }
}

/**
 * Get split tender status for an order
 */
export async function getSplitTenderStatus(orderId: string): Promise<SplitTenderStatus> {
  const order = await prisma.order.findUnique({
    where: { id: orderId },
    include: { payments: true },
  })

  if (!order) {
    throw new NotFoundError(`Order ${orderId} not found`)
  }

  const totalPaid = order.payments.reduce((sum, p) => sum + p.amountUsd, 0)
  const remainingBalance = Math.max(0, order.total - totalPaid)

  return {
    totalDue: order.total,
    totalPaid,
    remainingBalance,
    payments: order.payments.map((p) => ({
      id: p.id,
      type: p.type,
      amount: p.amountUsd,
      reference: p.reference || undefined,
      timestamp: p.createdAt,
    })),
    isComplete: remainingBalance === 0 && totalPaid >= order.total,
  }
}

/**
 * Add a payment to an existing order (for continued split tender)
 */
export async function addSplitTenderPayment(
  orderId: string,
  clerkId: string,
  payment: {
    type: 'cash' | 'card' | 'crypto' | 'storecredit' | 'giftcard' | 'check'
    amount: number
    reference?: string
    giftCardCode?: string
  }
): Promise<{
  payment: Payment
  status: SplitTenderStatus
}> {
  const result = await processSplitTender({
    orderId,
    clerkId,
    payments: [payment],
  })

  const status = await getSplitTenderStatus(orderId)

  return {
    payment: result.payments[0],
    status,
  }
}

/**
 * Calculate suggested payment amounts for split tender
 */
export function calculateSplitTenderSuggestions(
  totalDue: number,
  numPayments: number
): number[] {
  if (numPayments < 1) return [totalDue]
  
  const baseAmount = totalDue / numPayments
  const rounded = Math.round(baseAmount * 100) / 100
  
  const suggestions: number[] = []
  let runningTotal = 0

  for (let i = 0; i < numPayments - 1; i++) {
    suggestions.push(rounded)
    runningTotal += rounded
  }

  // Last payment gets remainder to ensure exact total
  suggestions.push(Math.round((totalDue - runningTotal) * 100) / 100)

  return suggestions
}

/**
 * Validate that a split tender combination is valid
 */
export function validateSplitTender(
  totalDue: number,
  payments: { amount: number }[]
): {
  isValid: boolean
  totalPayments: number
  difference: number
  error?: string
} {
  const totalPayments = payments.reduce((sum, p) => sum + p.amount, 0)
  const difference = totalPayments - totalDue

  if (totalPayments < totalDue) {
    return {
      isValid: false,
      totalPayments,
      difference,
      error: `Insufficient payment. Additional $${Math.abs(difference).toFixed(2)} required`,
    }
  }

  if (totalPayments > totalDue * 1.5) {
    return {
      isValid: false,
      totalPayments,
      difference,
      error: 'Payment exceeds reasonable overage amount',
    }
  }

  return {
    isValid: true,
    totalPayments,
    difference,
  }
}
