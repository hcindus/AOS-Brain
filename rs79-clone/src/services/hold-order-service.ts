import { prisma } from '@/lib/prisma'
import { ValidationError, NotFoundError } from '@/lib/errors'
import type { Order, OrderItem } from '@prisma/client'

export interface HeldOrder {
  id: string
  holdName: string
  items: OrderItem[]
  subtotal: number
  tax: number
  total: number
  customerId?: string
  customerName?: string
  clerkId: string
  clerkName: string
  createdAt: Date
  expiresAt: Date
}

export interface HoldOrderInput {
  clerkId: string
  holdName: string
  items: Array<{
    itemId: string
    name: string
    price: number
    qty: number
  }>
  subtotal: number
  tax: number
  total: number
  customerId?: string
  notes?: string
}

export interface RecallOrderResult {
  heldOrder: HeldOrder
  ticketNumber: number
}

// In-memory storage for held orders (can be replaced with Redis or database)
const heldOrders = new Map<string, HeldOrder>()

// Default hold expiration time in hours
const DEFAULT_HOLD_EXPIRY_HOURS = 4

/**
 * Generate a unique ticket number for held orders
 */
function generateTicketNumber(): number {
  return Math.floor(10000 + Math.random() * 90000)
}

/**
 * Hold an order with a ticket number
 */
export async function holdOrder(input: HoldOrderInput): Promise<{
  ticketNumber: number
  heldOrderId: string
  expiresAt: Date
}> {
  if (!input.holdName || input.holdName.trim().length === 0) {
    throw new ValidationError('Hold name is required')
  }

  if (!input.items || input.items.length === 0) {
    throw new ValidationError('Cannot hold an empty order')
  }

  const clerk = await prisma.clerk.findUnique({
    where: { id: input.clerkId },
  })

  if (!clerk) {
    throw new NotFoundError(`Clerk ${input.clerkId} not found`)
  }

  // Get customer name if customerId is provided
  let customerName: string | undefined
  if (input.customerId) {
    const customer = await prisma.customer.findUnique({
      where: { id: input.customerId },
    })
    if (customer) {
      customerName = customer.name
    }
  }

  const ticketNumber = generateTicketNumber()
  const now = new Date()
  const expiresAt = new Date(now.getTime() + DEFAULT_HOLD_EXPIRY_HOURS * 60 * 60 * 1000)

  const heldOrder: HeldOrder = {
    id: `HOLD-${ticketNumber}`,
    holdName: input.holdName.trim(),
    items: input.items.map((item, index) => ({
      id: `temp-${index}`,
      orderId: '', // Will be assigned when recalled
      itemId: item.itemId,
      name: item.name,
      price: item.price,
      qty: item.qty,
      lineTotal: item.price * item.qty,
    })),
    subtotal: input.subtotal,
    tax: input.tax,
    total: input.total,
    customerId: input.customerId,
    customerName,
    clerkId: input.clerkId,
    clerkName: clerk.name,
    createdAt: now,
    expiresAt,
  }

  // Store in memory
  heldOrders.set(heldOrder.id, heldOrder)

  // Also create a pending order in database for persistence
  const order = await prisma.order.create({
    data: {
      transactionNo: ticketNumber,
      clerkId: input.clerkId,
      customerId: input.customerId,
      subtotal: input.subtotal,
      tax: input.tax,
      total: input.total,
      currency: 'USD',
      currencyRate: 1,
      paymentType: 'pending',
      status: 'pending',
      holdName: input.holdName.trim(),
      notes: input.notes,
      amountPaid: 0,
      balanceDue: input.total,
      items: {
        create: input.items.map((item) => ({
          itemId: item.itemId,
          name: item.name,
          price: item.price,
          qty: item.qty,
          lineTotal: item.price * item.qty,
        })),
      },
    },
  })

  // Log the hold action
  await prisma.sessionLog.create({
    data: {
      clerkId: input.clerkId,
      action: 'ORDER_HELD',
      details: `Order held as "${heldOrder.holdName}" (Ticket #${ticketNumber})`,
    },
  })

  return {
    ticketNumber,
    heldOrderId: heldOrder.id,
    expiresAt,
  }
}

/**
 * Recall a held order by ticket number
 */
export async function recallOrder(ticketNumber: number): Promise<RecallOrderResult> {
  // First try to find in database
  const order = await prisma.order.findFirst({
    where: {
      transactionNo: ticketNumber,
      status: 'pending',
      holdName: { not: null },
    },
    include: {
      items: true,
      clerk: true,
    },
  })

  if (!order) {
    throw new NotFoundError(`Held order with ticket #${ticketNumber} not found`)
  }

  // Check if expired
  const heldOrderId = `HOLD-${ticketNumber}`
  const heldOrder = heldOrders.get(heldOrderId)
  
  if (heldOrder && heldOrder.expiresAt < new Date()) {
    // Expired - remove from memory and database
    heldOrders.delete(heldOrderId)
    await prisma.order.update({
      where: { id: order.id },
      data: { status: 'cancelled' },
    })
    throw new ValidationError(`Held order #${ticketNumber} has expired`)
  }

  const result: RecallOrderResult = {
    heldOrder: {
      id: heldOrderId,
      holdName: order.holdName!,
      items: order.items,
      subtotal: order.subtotal,
      tax: order.tax,
      total: order.total,
      customerId: order.customerId || undefined,
      clerkId: order.clerkId,
      clerkName: order.clerk.name,
      createdAt: order.createdAt,
      expiresAt: heldOrder?.expiresAt || new Date(Date.now() + DEFAULT_HOLD_EXPIRY_HOURS * 60 * 60 * 1000),
    },
    ticketNumber,
  }

  // Remove from memory
  heldOrders.delete(heldOrderId)

  // Update order status to indicate it's been recalled
  await prisma.order.update({
    where: { id: order.id },
    data: { holdName: null },
  })

  // Log the recall
  await prisma.sessionLog.create({
    data: {
      clerkId: order.clerkId,
      action: 'ORDER_RECALLED',
      details: `Order "${result.heldOrder.holdName}" (Ticket #${ticketNumber}) recalled`,
    },
  })

  return result
}

/**
 * List all active held orders
 */
export async function listHeldOrders(options?: {
  clerkId?: string
  includeExpired?: boolean
}): Promise<HeldOrder[]> {
  const where: {
    status: 'pending'
    holdName: { not: null }
    clerkId?: string
  } = {
    status: 'pending',
    holdName: { not: null },
  }

  if (options?.clerkId) {
    where.clerkId = options.clerkId
  }

  const orders = await prisma.order.findMany({
    where,
    include: {
      items: true,
      clerk: true,
      customer: true,
    },
    orderBy: { createdAt: 'desc' },
  })

  const result: HeldOrder[] = []

  for (const order of orders) {
    const heldOrderId = `HOLD-${order.transactionNo}`
    const heldOrder = heldOrders.get(heldOrderId)
    const expiresAt = heldOrder?.expiresAt || new Date(order.createdAt.getTime() + DEFAULT_HOLD_EXPIRY_HOURS * 60 * 60 * 1000)
    
    const isExpired = expiresAt < new Date()

    // Skip expired unless requested
    if (isExpired && !options?.includeExpired) {
      continue
    }

    result.push({
      id: heldOrderId,
      holdName: order.holdName!,
      items: order.items,
      subtotal: order.subtotal,
      tax: order.tax,
      total: order.total,
      customerId: order.customerId || undefined,
      customerName: order.customer?.name,
      clerkId: order.clerkId,
      clerkName: order.clerk.name,
      createdAt: order.createdAt,
      expiresAt,
    })
  }

  return result
}

/**
 * Cancel a held order
 */
export async function cancelHeldOrder(
  ticketNumber: number,
  clerkId: string
): Promise<void> {
  const order = await prisma.order.findFirst({
    where: {
      transactionNo: ticketNumber,
      status: 'pending',
      holdName: { not: null },
    },
  })

  if (!order) {
    throw new NotFoundError(`Held order #${ticketNumber} not found`)
  }

  // Remove from memory
  heldOrders.delete(`HOLD-${ticketNumber}`)

  // Cancel in database
  await prisma.order.update({
    where: { id: order.id },
    data: {
      status: 'cancelled',
      holdName: null,
    },
  })

  // Log the cancellation
  await prisma.sessionLog.create({
    data: {
      clerkId,
      action: 'ORDER_HOLD_CANCELLED',
      details: `Held order #${ticketNumber} cancelled`,
    },
  })
}

/**
 * Extend hold expiration time
 */
export async function extendHoldExpiration(
  ticketNumber: number,
  additionalHours: number,
  clerkId: string
): Promise<{ newExpiresAt: Date }> {
  if (additionalHours < 1 || additionalHours > 24) {
    throw new ValidationError('Extension must be between 1 and 24 hours')
  }

  const order = await prisma.order.findFirst({
    where: {
      transactionNo: ticketNumber,
      status: 'pending',
      holdName: { not: null },
    },
  })

  if (!order) {
    throw new NotFoundError(`Held order #${ticketNumber} not found`)
  }

  const heldOrderId = `HOLD-${ticketNumber}`
  const heldOrder = heldOrders.get(heldOrderId)

  if (!heldOrder) {
    throw new NotFoundError(`Held order #${ticketNumber} not found in memory`)
  }

  const newExpiresAt = new Date(heldOrder.expiresAt.getTime() + additionalHours * 60 * 60 * 1000)
  heldOrder.expiresAt = newExpiresAt

  heldOrders.set(heldOrderId, heldOrder)

  // Log the extension
  await prisma.sessionLog.create({
    data: {
      clerkId,
      action: 'ORDER_HOLD_EXTENDED',
      details: `Held order #${ticketNumber} extended by ${additionalHours} hours. New expiry: ${newExpiresAt.toLocaleString()}`,
    },
  })

  return { newExpiresAt }
}

/**
 * Get hold expiry configuration
 */
export function getHoldExpiryConfig(): {
  defaultExpiryHours: number
  maxExpiryHours: number
  minExpiryHours: number
} {
  return {
    defaultExpiryHours: DEFAULT_HOLD_EXPIRY_HOURS,
    maxExpiryHours: 24,
    minExpiryHours: 1,
  }
}

/**
 * Clean up expired held orders
 */
export async function cleanupExpiredHolds(): Promise<number> {
  const now = new Date()
  let cleaned = 0

  for (const [id, heldOrder] of heldOrders.entries()) {
    if (heldOrder.expiresAt < now) {
      heldOrders.delete(id)
      
      // Update database status
      const order = await prisma.order.findFirst({
        where: {
          transactionNo: parseInt(id.replace('HOLD-', '')),
          status: 'pending',
        },
      })

      if (order) {
        await prisma.order.update({
          where: { id: order.id },
          data: { status: 'cancelled' },
        })
      }

      cleaned++
    }
  }

  return cleaned
}
