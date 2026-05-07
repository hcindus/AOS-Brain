import { prisma } from '@/lib/prisma'
import { ValidationError, NotFoundError } from '@/lib/errors'
import type { OrderItem } from '@prisma/client'

export interface SplitCheck {
  id: number
  name: string
  items: OrderItem[]
  subtotal: number
  tax: number
  total: number
  amountPaid: number
  balanceDue: number
  isPaid: boolean
}

export interface SplitCheckInput {
  orderId: string
  splitType: 'even' | 'byItem'
  numChecks?: number
  itemAssignments?: Record<string, number[]> // itemId -> checkIds array
}

export interface ProcessSplitPaymentInput {
  orderId: string
  checkId: number
  type: 'cash' | 'card' | 'crypto' | 'storecredit' | 'giftcard' | 'check'
  amount: number
  reference?: string
  giftCardCode?: string
}

/**
 * Split an order into multiple checks
 */
export async function splitOrder(input: SplitCheckInput): Promise<{
  originalOrderId: string
  splits: SplitCheck[]
}> {
  const { orderId, splitType, numChecks, itemAssignments } = input

  // Get the original order
  const order = await prisma.order.findUnique({
    where: { id: orderId },
    include: { items: true, payments: true },
  })

  if (!order) {
    throw new NotFoundError(`Order ${orderId} not found`)
  }

  if (order.status !== 'pending' && order.status !== 'completed') {
    throw new ValidationError('Cannot split an order that is not pending or completed')
  }

  let splits: SplitCheck[] = []

  if (splitType === 'even' && numChecks) {
    // Even split
    splits = splitEvenly(order.items, numChecks, order.tax)
  } else if (splitType === 'byItem' && itemAssignments) {
    // Split by item selection
    splits = splitByItems(order.items, itemAssignments, order.tax)
  } else {
    throw new ValidationError('Invalid split configuration')
  }

  // Store split configuration in order meta
  await prisma.order.update({
    where: { id: orderId },
    data: {
      meta: JSON.stringify({
        isSplit: true,
        splitType,
        numChecks,
        splits,
      }),
    },
  })

  return {
    originalOrderId: orderId,
    splits,
  }
}

/**
 * Split items evenly among checks
 */
function splitEvenly(
  items: OrderItem[],
  numChecks: number,
  totalTax: number
): SplitCheck[] {
  if (numChecks < 2 || numChecks > 10) {
    throw new ValidationError('Number of checks must be between 2 and 10')
  }

  const subtotal = items.reduce((sum, item) => sum + item.lineTotal, 0)
  const taxPerCheck = totalTax / numChecks
  const totalPerCheck = (subtotal / numChecks) + taxPerCheck

  const splits: SplitCheck[] = []
  const itemsPerCheck = Math.ceil(items.length / numChecks)

  for (let i = 0; i < numChecks; i++) {
    const checkItems = items.slice(i * itemsPerCheck, (i + 1) * itemsPerCheck)
    const checkSubtotal = checkItems.reduce((sum, item) => sum + item.lineTotal, 0)
    
    splits.push({
      id: i + 1,
      name: `Check ${i + 1}`,
      items: checkItems,
      subtotal: checkSubtotal,
      tax: taxPerCheck,
      total: totalPerCheck,
      amountPaid: 0,
      balanceDue: totalPerCheck,
      isPaid: false,
    })
  }

  return splits
}

/**
 * Split items by assignment
 */
function splitByItems(
  items: OrderItem[],
  itemAssignments: Record<string, number[]>,
  totalTax: number
): SplitCheck[] {
  const checkIds = new Set<number>()
  
  // Find all unique check IDs
  Object.values(itemAssignments).forEach((checkIdList) => {
    checkIdList.forEach((id) => checkIds.add(id))
  })

  if (checkIds.size < 2) {
    throw new ValidationError('At least 2 checks required for split')
  }

  const sortedCheckIds = Array.from(checkIds).sort((a, b) => a - b)
  const splits: SplitCheck[] = []

  for (const checkId of sortedCheckIds) {
    const checkItems: OrderItem[] = []
    let checkSubtotal = 0

    // Find items assigned to this check
    for (const item of items) {
      if (itemAssignments[item.id]?.includes(checkId)) {
        checkItems.push(item)
        checkSubtotal += item.lineTotal
      }
    }

    if (checkItems.length === 0) {
      throw new ValidationError(`Check ${checkId} has no items assigned`)
    }

    // Calculate proportional tax
    const totalSubtotal = items.reduce((sum, item) => sum + item.lineTotal, 0)
    const checkTax = totalSubtotal > 0 ? (checkSubtotal / totalSubtotal) * totalTax : 0

    splits.push({
      id: checkId,
      name: `Check ${checkId}`,
      items: checkItems,
      subtotal: checkSubtotal,
      tax: checkTax,
      total: checkSubtotal + checkTax,
      amountPaid: 0,
      balanceDue: checkSubtotal + checkTax,
      isPaid: false,
    })
  }

  return splits
}

/**
 * Process payment for a specific split check
 */
export async function processSplitPayment(
  input: ProcessSplitPaymentInput
): Promise<{
  split: SplitCheck
  changeDue: number
  remainingBalance: number
}> {
  const { orderId, checkId, type, amount, giftCardCode } = input

  // Get order and split info
  const order = await prisma.order.findUnique({
    where: { id: orderId },
  })

  if (!order) {
    throw new NotFoundError(`Order ${orderId} not found`)
  }

  if (!order.meta) {
    throw new ValidationError('Order is not a split check')
  }

  const meta = JSON.parse(order.meta as string)
  if (!meta.isSplit) {
    throw new ValidationError('Order is not a split check')
  }

  // Find the split
  const split = meta.splits.find((s: SplitCheck) => s.id === checkId)
  if (!split) {
    throw new NotFoundError(`Check ${checkId} not found`)
  }

  if (split.isPaid) {
    throw new ValidationError(`Check ${checkId} is already paid`)
  }

  // Handle gift card payment
  if (type === 'giftcard' && giftCardCode) {
    const giftCard = await prisma.giftCard.findUnique({
      where: { code: giftCardCode.toUpperCase() },
    })

    if (!giftCard || !giftCard.isActive) {
      throw new ValidationError('Invalid gift card')
    }

    if (giftCard.expiresAt && new Date() > giftCard.expiresAt) {
      throw new ValidationError('Gift card has expired')
    }

    if (giftCard.balance < amount) {
      throw new ValidationError(
        `Insufficient gift card balance. Available: $${giftCard.balance.toFixed(2)}`
      )
    }

    // Deduct from gift card
    await prisma.giftCard.update({
      where: { id: giftCard.id },
      data: { balance: { decrement: amount } },
    })
  }

  // Calculate change
  const changeDue = amount > split.balanceDue ? amount - split.balanceDue : 0
  const actualPayment = Math.min(amount, split.balanceDue)

  // Update split
  split.amountPaid += actualPayment
  split.balanceDue = Math.max(0, split.total - split.amountPaid)
  split.isPaid = split.balanceDue === 0

  // Update meta
  meta.splits = meta.splits.map((s: SplitCheck) =>
    s.id === checkId ? split : s
  )

  // Update order
  const allPaid = meta.splits.every((s: SplitCheck) => s.isPaid)
  
  await prisma.order.update({
    where: { id: orderId },
    data: {
      meta: JSON.stringify(meta),
      status: allPaid ? 'completed' : 'pending',
      amountPaid: meta.splits.reduce((sum: number, s: SplitCheck) => sum + s.amountPaid, 0),
      balanceDue: meta.splits.reduce((sum: number, s: SplitCheck) => sum + s.balanceDue, 0),
    },
  })

  // Create payment record for this split
  await prisma.payment.create({
    data: {
      orderId,
      clerkId: order.clerkId,
      type,
      amountUsd: actualPayment,
      amountNative: actualPayment,
      currency: 'USD',
      currencyRate: 1,
      reference: input.reference || `SPLIT-CHECK-${checkId}`,
      meta: JSON.stringify({ splitCheckId: checkId, splitPayment: true }),
    },
  })

  return {
    split,
    changeDue,
    remainingBalance: meta.splits.reduce((sum: number, s: SplitCheck) => sum + s.balanceDue, 0),
  }
}

/**
 * Get split checks for an order
 */
export async function getSplitChecks(orderId: string): Promise<{
  isSplit: boolean
  splits: SplitCheck[]
}> {
  const order = await prisma.order.findUnique({
    where: { id: orderId },
  })

  if (!order) {
    throw new NotFoundError(`Order ${orderId} not found`)
  }

  if (!order.meta) {
    return { isSplit: false, splits: [] }
  }

  const meta = JSON.parse(order.meta as string)
  return {
    isSplit: meta.isSplit || false,
    splits: meta.splits || [],
  }
}

/**
 * Generate receipt for a specific split check
 */
export async function generateSplitReceipt(
  orderId: string,
  checkId: number
): Promise<{
  check: SplitCheck
  transactionNo: number
  createdAt: Date
}> {
  const order = await prisma.order.findUnique({
    where: { id: orderId },
    include: { clerk: true },
  })

  if (!order) {
    throw new NotFoundError(`Order ${orderId} not found`)
  }

  if (!order.meta) {
    throw new ValidationError('Order is not a split check')
  }

  const meta = JSON.parse(order.meta as string)
  const split = meta.splits?.find((s: SplitCheck) => s.id === checkId)

  if (!split) {
    throw new NotFoundError(`Check ${checkId} not found`)
  }

  return {
    check: split,
    transactionNo: order.transactionNo,
    createdAt: order.createdAt,
  }
}
