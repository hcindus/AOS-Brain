import { prisma } from '@/lib/prisma'
import { ValidationError, NotFoundError, PaymentError } from '@/lib/errors'
import type { GiftCard } from '@prisma/client'

export interface CreateGiftCardInput {
  code?: string
  originalAmount: number
  expiresAt?: Date
}

export interface GiftCardTransaction {
  type: 'deduct' | 'add'
  amount: number
  timestamp: Date
  orderId?: string
}

/**
 * Generate a random gift card code
 */
function generateGiftCardCode(): string {
  // Format: GIFT-XXXX-XXXX-XXXX (12 alphanumeric characters)
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
  let code = 'GIFT-'
  for (let i = 0; i < 12; i++) {
    if (i > 0 && i % 4 === 0) code += '-'
    code += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return code
}

/**
 * Create a new gift card
 */
export async function createGiftCard(input: CreateGiftCardInput): Promise<GiftCard> {
  if (input.originalAmount <= 0) {
    throw new ValidationError('Gift card amount must be greater than 0')
  }

  let code = input.code?.trim().toUpperCase()
  
  // Generate code if not provided
  if (!code) {
    let attempts = 0
    do {
      code = generateGiftCardCode()
      attempts++
      // Check if code already exists
      const existing = await prisma.giftCard.findUnique({
        where: { code },
      })
      if (!existing) break
    } while (attempts < 10)
    
    if (attempts >= 10) {
      throw new Error('Failed to generate unique gift card code')
    }
  } else {
    // Validate custom code format
    if (!/^[A-Z0-9\-]+$/.test(code)) {
      throw new ValidationError('Gift card code must contain only letters, numbers, and hyphens')
    }
    
    // Check if code already exists
    const existing = await prisma.giftCard.findUnique({
      where: { code },
    })
    if (existing) {
      throw new ValidationError(`Gift card code ${code} already exists`)
    }
  }

  const giftCard = await prisma.giftCard.create({
    data: {
      code,
      balance: input.originalAmount,
      originalAmount: input.originalAmount,
      isActive: true,
      expiresAt: input.expiresAt ?? null,
    },
  })

  return giftCard
}

/**
 * Validate a gift card by code
 * Returns the gift card if valid, throws error otherwise
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
    throw new PaymentError(`Gift card expired on ${giftCard.expiresAt.toLocaleDateString()}`)
  }

  if (giftCard.balance <= 0) {
    throw new PaymentError('Gift card has no remaining balance')
  }

  return giftCard
}

/**
 * Get gift card details including balance
 */
export async function getGiftCardDetails(code: string): Promise<{
  code: string
  balance: number
  originalAmount: number
  isActive: boolean
  isExpired: boolean
  expiresAt: Date | null
  isValid: boolean
  error?: string
}> {
  const giftCard = await prisma.giftCard.findUnique({
    where: { code: code.trim().toUpperCase() },
  })

  if (!giftCard) {
    return {
      code: code.trim().toUpperCase(),
      balance: 0,
      originalAmount: 0,
      isActive: false,
      isExpired: false,
      expiresAt: null,
      isValid: false,
      error: 'Gift card not found',
    }
  }

  const now = new Date()
  const isExpired = giftCard.expiresAt ? now > giftCard.expiresAt : false
  let isValid = giftCard.isActive && !isExpired && giftCard.balance > 0
  let error: string | undefined

  if (!giftCard.isActive) {
    error = 'Gift card is inactive'
    isValid = false
  } else if (isExpired) {
    error = `Gift card expired on ${giftCard.expiresAt!.toLocaleDateString()}`
    isValid = false
  } else if (giftCard.balance <= 0) {
    error = 'Gift card has no remaining balance'
    isValid = false
  }

  return {
    code: giftCard.code,
    balance: giftCard.balance,
    originalAmount: giftCard.originalAmount,
    isActive: giftCard.isActive,
    isExpired,
    expiresAt: giftCard.expiresAt,
    isValid,
    error,
  }
}

/**
 * Get gift card balance
 */
export async function getBalance(code: string): Promise<number> {
  const giftCard = await prisma.giftCard.findUnique({
    where: { code: code.trim().toUpperCase() },
  })

  if (!giftCard) {
    throw new NotFoundError(`Gift card ${code} not found`)
  }

  return giftCard.balance
}

/**
 * Deduct balance from gift card
 */
export async function deductBalance(
  code: string,
  amount: number
): Promise<{ giftCard: GiftCard; remainingBalance: number }> {
  if (amount <= 0) {
    throw new ValidationError('Deduction amount must be greater than 0')
  }

  const giftCard = await validateGiftCard(code)

  if (giftCard.balance < amount) {
    throw new PaymentError(
      `Insufficient balance. Available: $${giftCard.balance.toFixed(2)}, Requested: $${amount.toFixed(2)}`
    )
  }

  const updated = await prisma.giftCard.update({
    where: { id: giftCard.id },
    data: {
      balance: { decrement: amount },
    },
  })

  return {
    giftCard: updated,
    remainingBalance: updated.balance,
  }
}

/**
 * Add balance to gift card (for reloads/refunds)
 */
export async function addBalance(
  code: string,
  amount: number,
  reason?: string
): Promise<{ giftCard: GiftCard; newBalance: number }> {
  if (amount <= 0) {
    throw new ValidationError('Amount to add must be greater than 0')
  }

  const giftCard = await prisma.giftCard.findUnique({
    where: { code: code.trim().toUpperCase() },
  })

  if (!giftCard) {
    throw new NotFoundError(`Gift card ${code} not found`)
  }

  if (!giftCard.isActive) {
    throw new PaymentError('Cannot add balance to inactive gift card')
  }

  const updated = await prisma.giftCard.update({
    where: { id: giftCard.id },
    data: {
      balance: { increment: amount },
    },
  })

  // Log the reload
  await prisma.sessionLog.create({
    data: {
      clerkId: 'system',
      action: 'GIFT_CARD_RELOADED',
      details: `Gift card ${code} reloaded with $${amount.toFixed(2)}. Reason: ${reason ?? 'N/A'}. New balance: $${updated.balance.toFixed(2)}`,
    },
  })

  return {
    giftCard: updated,
    newBalance: updated.balance,
  }
}

/**
 * Deactivate a gift card
 */
export async function deactivateGiftCard(
  code: string,
  reason?: string
): Promise<GiftCard> {
  const giftCard = await prisma.giftCard.findUnique({
    where: { code: code.trim().toUpperCase() },
  })

  if (!giftCard) {
    throw new NotFoundError(`Gift card ${code} not found`)
  }

  if (!giftCard.isActive) {
    throw new ValidationError('Gift card is already inactive')
  }

  const updated = await prisma.giftCard.update({
    where: { id: giftCard.id },
    data: { isActive: false },
  })

  // Log the deactivation
  await prisma.sessionLog.create({
    data: {
      clerkId: 'system',
      action: 'GIFT_CARD_DEACTIVATED',
      details: `Gift card ${code} deactivated. Reason: ${reason ?? 'N/A'}`,
    },
  })

  return updated
}

/**
 * Reactivate a gift card
 */
export async function reactivateGiftCard(
  code: string,
  reason?: string
): Promise<GiftCard> {
  const giftCard = await prisma.giftCard.findUnique({
    where: { code: code.trim().toUpperCase() },
  })

  if (!giftCard) {
    throw new NotFoundError(`Gift card ${code} not found`)
  }

  if (giftCard.isActive) {
    throw new ValidationError('Gift card is already active')
  }

  const updated = await prisma.giftCard.update({
    where: { id: giftCard.id },
    data: { isActive: true },
  })

  // Log the reactivation
  await prisma.sessionLog.create({
    data: {
      clerkId: 'system',
      action: 'GIFT_CARD_REACTIVATED',
      details: `Gift card ${code} reactivated. Reason: ${reason ?? 'N/A'}`,
    },
  })

  return updated
}

/**
 * List gift cards with filters
 */
export async function listGiftCards(options: {
  isActive?: boolean
  hasBalance?: boolean
  expiresBefore?: Date
  limit?: number
  offset?: number
}): Promise<{ giftCards: GiftCard[]; total: number }> {
  const where: {
    isActive?: boolean
    expiresAt?: { lt?: Date }
    balance?: { gt?: number }
  } = {}

  if (options.isActive !== undefined) where.isActive = options.isActive
  if (options.expiresBefore) where.expiresAt = { lt: options.expiresBefore }
  if (options.hasBalance) where.balance = { gt: 0 }

  const [giftCards, total] = await Promise.all([
    prisma.giftCard.findMany({
      where,
      orderBy: { createdAt: 'desc' },
      take: options.limit ?? 50,
      skip: options.offset ?? 0,
    }),
    prisma.giftCard.count({ where }),
  ])

  return { giftCards, total }
}

/**
 * Get gift card summary statistics
 */
export async function getGiftCardStats(): Promise<{
  totalCards: number
  activeCards: number
  totalBalance: number
  totalOriginalValue: number
  expiredCards: number
}> {
  const [
    totalCards,
    activeCards,
    expiredCards,
    balanceAgg,
  ] = await Promise.all([
    prisma.giftCard.count(),
    prisma.giftCard.count({ where: { isActive: true } }),
    prisma.giftCard.count({
      where: {
        expiresAt: { lt: new Date() },
        isActive: true,
      },
    }),
    prisma.giftCard.aggregate({
      _sum: { balance: true, originalAmount: true },
    }),
  ])

  return {
    totalCards,
    activeCards,
    totalBalance: balanceAgg._sum.balance ?? 0,
    totalOriginalValue: balanceAgg._sum.originalAmount ?? 0,
    expiredCards,
  }
}
