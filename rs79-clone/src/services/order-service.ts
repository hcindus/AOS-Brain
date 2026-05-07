import { prisma } from '@/lib/prisma'
import { NotFoundError, ValidationError } from '@/lib/errors'
import type { Order, OrderItem, Prisma } from '@prisma/client'

export interface CreateOrderInput {
  clerkId: string
  customerId?: string
  items: Array<{
    itemId: string
    name: string
    price: number
    qty: number
  }>
  subtotal: number
  tax: number
  total: number
  currency?: string
  currencyRate?: number
  paymentType: string
  tendered?: number
  change?: number
  holdName?: string
  notes?: string
  loyaltyRedeemed?: number
  discountUsd?: number
}

export interface OrderWithRelations extends Order {
  items: OrderItem[]
  clerk: { name: string }
  customer?: { name: string; loyaltyCardNo: string } | null
}

/**
 * Create a new order with order items
 */
export async function createOrder(input: CreateOrderInput): Promise<OrderWithRelations> {
  // Validate required fields
  if (!input.clerkId) {
    throw new ValidationError('Clerk ID is required')
  }
  if (!input.items || input.items.length === 0) {
    throw new ValidationError('Order must have at least one item')
  }
  if (!input.paymentType) {
    throw new ValidationError('Payment type is required')
  }

  // Calculate line totals and validate items
  const orderItems = input.items.map(item => {
    if (item.qty <= 0) {
      throw new ValidationError(`Invalid quantity for item ${item.name}`)
    }
    return {
      itemId: item.itemId,
      name: item.name,
      price: item.price,
      qty: item.qty,
      lineTotal: item.price * item.qty,
    }
  })

  // Calculate loyalty points earned (1 point per dollar spent, rounded down)
  const loyaltyEarned = Math.floor(input.subtotal)

  // Get next transaction number
  const lastOrder = await prisma.order.findFirst({
    orderBy: { transactionNo: 'desc' },
  })
  const transactionNo = (lastOrder?.transactionNo ?? 0) + 1

  // Create the order
  const order = await prisma.order.create({
    data: {
      transactionNo,
      clerkId: input.clerkId,
      customerId: input.customerId,
      subtotal: input.subtotal,
      tax: input.tax,
      total: input.total,
      currency: input.currency ?? 'USD',
      currencyRate: input.currencyRate ?? 1,
      paymentType: input.paymentType,
      tendered: input.tendered,
      change: input.change,
      status: 'completed',
      kdsStatus: 'new',
      holdName: input.holdName,
      notes: input.notes,
      amountPaid: input.tendered ?? input.total,
      balanceDue: 0,
      loyaltyEarned,
      loyaltyRedeemed: input.loyaltyRedeemed ?? 0,
      discountUsd: input.discountUsd ?? 0,
      items: {
        create: orderItems,
      },
    },
    include: {
      items: true,
      clerk: {
        select: { name: true },
      },
      customer: {
        select: { name: true, loyaltyCardNo: true },
      },
    },
  })

  // Update customer loyalty points if applicable
  if (input.customerId) {
    await prisma.customer.update({
      where: { id: input.customerId },
      data: {
        loyaltyPoints: {
          increment: loyaltyEarned - (input.loyaltyRedeemed ?? 0),
        },
      },
    })
  }

  return order
}

/**
 * Update order status (e.g., pending, completed, cancelled)
 */
export async function updateOrderStatus(
  orderId: string,
  status: 'completed' | 'pending' | 'cancelled'
): Promise<Order> {
  const order = await prisma.order.findUnique({
    where: { id: orderId },
  })

  if (!order) {
    throw new NotFoundError(`Order ${orderId} not found`)
  }

  if (order.status === 'voided') {
    throw new ValidationError('Cannot update status of a voided order')
  }

  const updatedOrder = await prisma.order.update({
    where: { id: orderId },
    data: { status },
  })

  return updatedOrder
}

/**
 * Update KDS (Kitchen Display System) status
 */
export async function updateKdsStatus(
  orderId: string,
  kdsStatus: 'new' | 'preparing' | 'done'
): Promise<Order> {
  const order = await prisma.order.findUnique({
    where: { id: orderId },
  })

  if (!order) {
    throw new NotFoundError(`Order ${orderId} not found`)
  }

  const updatedOrder = await prisma.order.update({
    where: { id: orderId },
    data: { kdsStatus },
  })

  return updatedOrder
}

/**
 * Void an order (with reason)
 */
export async function voidOrder(
  orderId: string,
  voidReason: string,
  clerkId: string
): Promise<Order> {
  if (!voidReason || voidReason.trim().length === 0) {
    throw new ValidationError('Void reason is required')
  }

  const order = await prisma.order.findUnique({
    where: { id: orderId },
    include: { customer: true },
  })

  if (!order) {
    throw new NotFoundError(`Order ${orderId} not found`)
  }

  if (order.status === 'voided') {
    throw new ValidationError('Order is already voided')
  }

  // Reverse loyalty points if customer exists
  if (order.customerId && order.loyaltyEarned > 0) {
    await prisma.customer.update({
      where: { id: order.customerId },
      data: {
        loyaltyPoints: {
          decrement: order.loyaltyEarned,
        },
      },
    })
  }

  const voidedOrder = await prisma.order.update({
    where: { id: orderId },
    data: {
      status: 'voided',
      voidReason: voidReason.trim(),
      voidedAt: new Date(),
    },
  })

  // Log the void action
  await prisma.sessionLog.create({
    data: {
      clerkId,
      action: 'ORDER_VOIDED',
      details: `Order #${order.transactionNo} voided. Reason: ${voidReason}`,
    },
  })

  return voidedOrder
}

/**
 * Get order by ID with full relations
 */
export async function getOrderById(orderId: string): Promise<OrderWithRelations> {
  const order = await prisma.order.findUnique({
    where: { id: orderId },
    include: {
      items: true,
      clerk: {
        select: { name: true },
      },
      customer: {
        select: { name: true, loyaltyCardNo: true },
      },
      payments: {
        include: {
          clerk: {
            select: { name: true },
          },
        },
      },
    },
  })

  if (!order) {
    throw new NotFoundError(`Order ${orderId} not found`)
  }

  return order as OrderWithRelations
}

/**
 * Get order by transaction number
 */
export async function getOrderByTransactionNo(transactionNo: number): Promise<OrderWithRelations> {
  const order = await prisma.order.findUnique({
    where: { transactionNo },
    include: {
      items: true,
      clerk: {
        select: { name: true },
      },
      customer: {
        select: { name: true, loyaltyCardNo: true },
      },
      payments: {
        include: {
          clerk: {
            select: { name: true },
          },
        },
      },
    },
  })

  if (!order) {
    throw new NotFoundError(`Order with transaction #${transactionNo} not found`)
  }

  return order as OrderWithRelations
}

/**
 * List orders with pagination and filters
 */
export async function listOrders(options: {
  clerkId?: string
  customerId?: string
  status?: string
  kdsStatus?: string
  startDate?: Date
  endDate?: Date
  limit?: number
  offset?: number
}): Promise<{ orders: OrderWithRelations[]; total: number }> {
  const where: Prisma.OrderWhereInput = {}

  if (options.clerkId) where.clerkId = options.clerkId
  if (options.customerId) where.customerId = options.customerId
  if (options.status) where.status = options.status
  if (options.kdsStatus) where.kdsStatus = options.kdsStatus
  
  if (options.startDate || options.endDate) {
    where.createdAt = {}
    if (options.startDate) where.createdAt.gte = options.startDate
    if (options.endDate) where.createdAt.lte = options.endDate
  }

  const [orders, total] = await Promise.all([
    prisma.order.findMany({
      where,
      include: {
        items: true,
        clerk: {
          select: { name: true },
        },
        customer: {
          select: { name: true, loyaltyCardNo: true },
        },
      },
      orderBy: { createdAt: 'desc' },
      take: options.limit ?? 50,
      skip: options.offset ?? 0,
    }),
    prisma.order.count({ where }),
  ])

  return { orders: orders as OrderWithRelations[], total }
}
