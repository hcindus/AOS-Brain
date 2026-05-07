import { prisma } from '@/lib/prisma'
import { ValidationError, NotFoundError } from '@/lib/errors'
import type { Customer, StoreCredit } from '@prisma/client'

export interface CreateCustomerInput {
  name: string
  phone?: string
  loyaltyCardNo?: string
  loyaltyPoints?: number
}

export interface CustomerWithStoreCredit extends Customer {
  storeCredit: StoreCredit | null
}

/**
 * Find existing customer or create a new one
 */
export async function findOrCreateCustomer(input: CreateCustomerInput): Promise<Customer> {
  // Validate required fields
  if (!input.name || input.name.trim().length === 0) {
    throw new ValidationError('Customer name is required')
  }

  // Try to find by loyalty card number first
  if (input.loyaltyCardNo) {
    const existingByCard = await prisma.customer.findUnique({
      where: { loyaltyCardNo: input.loyaltyCardNo.trim().toUpperCase() },
    })
    if (existingByCard) {
      // Update phone if provided
      if (input.phone && input.phone !== existingByCard.phone) {
        return await prisma.customer.update({
          where: { id: existingByCard.id },
          data: { phone: input.phone },
        })
      }
      return existingByCard
    }
  }

  // Try to find by phone number
  if (input.phone) {
    const existingByPhone = await prisma.customer.findFirst({
      where: { phone: input.phone.trim() },
    })
    if (existingByPhone) {
      return existingByPhone
    }
  }

  // Generate loyalty card number if not provided
  let loyaltyCardNo = input.loyaltyCardNo?.trim().toUpperCase()
  if (!loyaltyCardNo) {
    // Generate unique loyalty card number (LOYAL + timestamp + random)
    const timestamp = Date.now().toString(36).toUpperCase()
    const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0')
    loyaltyCardNo = `LOYAL${timestamp}${random}`
  }

  // Check if loyalty card number already exists
  const existingCard = await prisma.customer.findUnique({
    where: { loyaltyCardNo },
  })
  if (existingCard) {
    throw new ValidationError(`Loyalty card number ${loyaltyCardNo} already exists`)
  }

  // Create new customer
  const customer = await prisma.customer.create({
    data: {
      name: input.name.trim(),
      phone: input.phone?.trim() || null,
      loyaltyCardNo,
      loyaltyPoints: input.loyaltyPoints ?? 0,
    },
  })

  // Create empty store credit record for the customer
  await prisma.storeCredit.create({
    data: {
      customerId: customer.id,
      balance: 0,
      totalEarned: 0,
      totalSpent: 0,
    },
  })

  return customer
}

/**
 * Get customer by ID with store credit
 */
export async function getCustomerById(customerId: string): Promise<CustomerWithStoreCredit> {
  const customer = await prisma.customer.findUnique({
    where: { id: customerId },
    include: { storeCredit: true },
  })

  if (!customer) {
    throw new NotFoundError(`Customer ${customerId} not found`)
  }

  return customer as CustomerWithStoreCredit
}

/**
 * Get customer by loyalty card number
 */
export async function getCustomerByLoyaltyCard(cardNo: string): Promise<CustomerWithStoreCredit> {
  const customer = await prisma.customer.findUnique({
    where: { loyaltyCardNo: cardNo.trim().toUpperCase() },
    include: { storeCredit: true },
  })

  if (!customer) {
    throw new NotFoundError(`Customer with card ${cardNo} not found`)
  }

  return customer as CustomerWithStoreCredit
}

/**
 * Update customer loyalty points
 */
export async function updateLoyaltyPoints(
  customerId: string,
  pointsToAdd: number
): Promise<Customer> {
  if (!customerId) {
    throw new ValidationError('Customer ID is required')
  }

  const customer = await prisma.customer.findUnique({
    where: { id: customerId },
  })

  if (!customer) {
    throw new NotFoundError(`Customer ${customerId} not found`)
  }

  // Calculate new points (don't go below 0)
  const newPoints = Math.max(0, customer.loyaltyPoints + pointsToAdd)

  const updated = await prisma.customer.update({
    where: { id: customerId },
    data: { loyaltyPoints: newPoints },
  })

  // Log the points update
  await prisma.sessionLog.create({
    data: {
      clerkId: 'system',
      action: 'LOYALTY_POINTS_UPDATED',
      details: `Customer ${customer.name} (${customerId}): ${pointsToAdd > 0 ? '+' : ''}${pointsToAdd} points. New total: ${newPoints}`,
    },
  })

  return updated
}

/**
 * Redeem loyalty points (convert points to discount)
 * Returns the discount amount in USD
 */
export async function redeemLoyaltyPoints(
  customerId: string,
  pointsToRedeem: number
): Promise<{ customer: Customer; discountUsd: number }> {
  if (pointsToRedeem <= 0) {
    throw new ValidationError('Points to redeem must be greater than 0')
  }

  const customer = await prisma.customer.findUnique({
    where: { id: customerId },
  })

  if (!customer) {
    throw new NotFoundError(`Customer ${customerId} not found`)
  }

  if (customer.loyaltyPoints < pointsToRedeem) {
    throw new ValidationError(
      `Insufficient points. Available: ${customer.loyaltyPoints}, Requested: ${pointsToRedeem}`
    )
  }

  // Calculate discount: 100 points = $1.00
  const discountUsd = pointsToRedeem / 100

  const updated = await prisma.customer.update({
    where: { id: customerId },
    data: { loyaltyPoints: { decrement: pointsToRedeem } },
  })

  // Log the redemption
  await prisma.sessionLog.create({
    data: {
      clerkId: 'system',
      action: 'LOYALTY_POINTS_REDEEMED',
      details: `Customer ${customer.name} redeemed ${pointsToRedeem} points for $${discountUsd.toFixed(2)} discount. Remaining: ${updated.loyaltyPoints}`,
    },
  })

  return { customer: updated, discountUsd }
}

/**
 * Get store credit for a customer
 */
export async function getStoreCredit(customerId: string): Promise<StoreCredit> {
  const storeCredit = await prisma.storeCredit.findUnique({
    where: { customerId },
  })

  if (!storeCredit) {
    throw new NotFoundError(`No store credit found for customer ${customerId}`)
  }

  return storeCredit
}

/**
 * Add store credit to a customer
 */
export async function addStoreCredit(
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

  const customer = await prisma.customer.findUnique({
    where: { id: customerId },
  })

  if (!customer) {
    throw new NotFoundError(`Customer ${customerId} not found`)
  }

  let storeCredit = await prisma.storeCredit.findUnique({
    where: { customerId },
  })

  if (storeCredit) {
    storeCredit = await prisma.storeCredit.update({
      where: { id: storeCredit.id },
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

  // Log the credit addition
  await prisma.sessionLog.create({
    data: {
      clerkId: 'system',
      action: 'STORE_CREDIT_ADDED',
      details: `Store credit of $${amount.toFixed(2)} added to customer ${customer.name}. Reason: ${reason}. New balance: $${storeCredit.balance.toFixed(2)}`,
    },
  })

  return storeCredit
}

/**
 * Use store credit (deduct from balance)
 */
export async function useStoreCredit(
  customerId: string,
  amount: number
): Promise<StoreCredit> {
  if (amount <= 0) {
    throw new ValidationError('Amount to use must be greater than 0')
  }

  const storeCredit = await prisma.storeCredit.findUnique({
    where: { customerId },
  })

  if (!storeCredit) {
    throw new NotFoundError(`No store credit found for customer ${customerId}`)
  }

  if (storeCredit.balance < amount) {
    throw new ValidationError(
      `Insufficient store credit. Available: $${storeCredit.balance.toFixed(2)}, Requested: $${amount.toFixed(2)}`
    )
  }

  const updated = await prisma.storeCredit.update({
    where: { id: storeCredit.id },
    data: {
      balance: { decrement: amount },
      totalSpent: { increment: amount },
    },
  })

  return updated
}

/**
 * List customers with pagination and search
 */
export async function listCustomers(options: {
  search?: string
  limit?: number
  offset?: number
}): Promise<{ customers: CustomerWithStoreCredit[]; total: number }> {
  const where: { name?: { contains: string }; phone?: { contains: string } } = {}

  if (options.search) {
    const search = options.search.trim()
    where.name = { contains: search }
    // If search looks like a phone number, also search by phone
    if (/^[\d\-\+\(\)\s]+$/.test(search)) {
      where.phone = { contains: search }
    }
  }

  const [customers, total] = await Promise.all([
    prisma.customer.findMany({
      where,
      include: { storeCredit: true },
      orderBy: { name: 'asc' },
      take: options.limit ?? 50,
      skip: options.offset ?? 0,
    }),
    prisma.customer.count({ where }),
  ])

  return { customers: customers as CustomerWithStoreCredit[], total }
}

/**
 * Update customer information
 */
export async function updateCustomer(
  customerId: string,
  updates: Partial<Pick<Customer, 'name' | 'phone'>>
): Promise<Customer> {
  const customer = await prisma.customer.findUnique({
    where: { id: customerId },
  })

  if (!customer) {
    throw new NotFoundError(`Customer ${customerId} not found`)
  }

  const data: { name?: string; phone?: string | null } = {}
  if (updates.name !== undefined) data.name = updates.name.trim()
  if (updates.phone !== undefined) data.phone = updates.phone?.trim() || null

  const updated = await prisma.customer.update({
    where: { id: customerId },
    data,
  })

  return updated
}
