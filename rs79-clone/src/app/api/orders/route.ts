import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { convertToUsd } from '@/lib/currency'

// GET /api/orders - List orders
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const limit = parseInt(searchParams.get('limit') ?? '50')
    const offset = parseInt(searchParams.get('offset') ?? '0')
    const status = searchParams.get('status')
    const kdsStatus = searchParams.get('kdsStatus')
    const clerkId = searchParams.get('clerkId')
    const customerId = searchParams.get('customerId')
    const startDate = searchParams.get('startDate')
    const endDate = searchParams.get('endDate')

    const where: any = {}
    if (status) where.status = status
    if (kdsStatus) where.kdsStatus = kdsStatus
    if (clerkId) where.clerkId = clerkId
    if (customerId) where.customerId = customerId
    
    if (startDate || endDate) {
      where.createdAt = {}
      if (startDate) where.createdAt.gte = new Date(startDate)
      if (endDate) where.createdAt.lte = new Date(endDate)
    }

    const [orders, total] = await Promise.all([
      prisma.order.findMany({
        where,
        include: {
          clerk: { select: { id: true, name: true } },
          customer: { select: { id: true, name: true, loyaltyCardNo: true } },
          items: true,
          _count: { select: { items: true } },
        },
        orderBy: { createdAt: 'desc' },
        take: limit,
        skip: offset,
      }),
      prisma.order.count({ where }),
    ])

    return NextResponse.json({
      success: true,
      data: orders,
      meta: { limit, offset, total },
    })
  } catch (error) {
    console.error('List orders error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to list orders' } },
      { status: 500 }
    )
  }
}

// POST /api/orders - Create order
export async function POST(request: NextRequest) {
  try {
    const clerkId = request.headers.get('x-clerk-id')
    if (!clerkId) {
      return NextResponse.json(
        { success: false, error: { code: 'AUTH_REQUIRED', message: 'Authentication required' } },
        { status: 401 }
      )
    }

    const body = await request.json()
    const {
      customerId,
      items,
      currency = 'USD',
      currencyRate = 1,
      payments,
      holdName,
      notes,
      discountUsd = 0,
      loyaltyRedeemed = 0,
    } = body

    // Validation
    if (!items || !Array.isArray(items) || items.length === 0) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Order must have at least one item' } },
        { status: 400 }
      )
    }

    if (!payments || !Array.isArray(payments) || payments.length === 0) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Order must have at least one payment' } },
        { status: 400 }
      )
    }

    // Calculate totals
    let subtotal = 0
    const orderItems = []
    
    for (const item of items) {
      if (!item.itemId || !item.name || !item.price || !item.qty) {
        return NextResponse.json(
          { success: false, error: { code: 'VALIDATION_ERROR', message: 'Invalid item data' } },
          { status: 400 }
        )
      }
      
      const lineTotal = item.price * item.qty
      subtotal += lineTotal
      orderItems.push({
        itemId: item.itemId,
        name: item.name,
        price: item.price,
        qty: item.qty,
        lineTotal,
      })
    }

    const tax = subtotal * 0.08 // 8% tax rate
    const total = subtotal + tax - discountUsd - loyaltyRedeemed
    
    // Calculate payment totals
    let amountPaid = 0
    const orderPayments = []
    let tendered = 0
    let change = 0
    let paymentType = payments[0]?.type
    
    // Check if split payment
    if (payments.length > 1) {
      paymentType = 'split'
    }

    for (const payment of payments) {
      const amountUsd = payment.currency === 'USD' 
        ? payment.amount 
        : convertToUsd(payment.amount, payment.currency)
      
      amountPaid += amountUsd
      
      orderPayments.push({
        type: payment.type,
        amountUsd,
        amountNative: payment.amount,
        currency: payment.currency || 'USD',
        currencyRate: payment.currencyRate || 1,
        reference: payment.reference || null,
        meta: payment.meta ? JSON.stringify(payment.meta) : null,
      })

      if (payment.type === 'cash') {
        tendered += payment.tendered || payment.amount
      }
    }

    change = tendered > total ? tendered - total : 0
    const balanceDue = total - amountPaid

    // Validate payment covers total
    if (amountPaid < total - 0.01) {
      return NextResponse.json(
        { success: false, error: { code: 'PAYMENT_INSUFFICIENT', message: `Payment ($${amountPaid.toFixed(2)}) is less than total ($${total.toFixed(2)})` } },
        { status: 400 }
      )
    }

    // Calculate loyalty earned (1 point per dollar spent)
    const loyaltyEarned = Math.floor(total > 0 ? total : 0)

    // Create order with transaction
    const order = await prisma.$transaction(async (tx) => {
      // Update customer loyalty if applicable
      if (customerId) {
        const customer = await tx.customer.findUnique({ where: { id: customerId } })
        if (customer) {
          await tx.customer.update({
            where: { id: customerId },
            data: {
              loyaltyPoints: { increment: loyaltyEarned - loyaltyRedeemed },
            },
          })
        }
      }

      // Create the order
      const newOrder = await tx.order.create({
        data: {
          clerkId,
          customerId: customerId || null,
          subtotal,
          tax,
          total,
          currency,
          currencyRate,
          paymentType,
          tendered: tendered > 0 ? tendered : amountPaid,
          change: change > 0 ? change : 0,
          status: 'completed',
          kdsStatus: 'new',
          holdName: holdName || null,
          notes: notes || null,
          amountPaid,
          balanceDue: balanceDue > 0 ? balanceDue : 0,
          loyaltyEarned,
          loyaltyRedeemed,
          discountUsd,
          items: {
            create: orderItems,
          },
          payments: {
            create: orderPayments,
          },
        },
        include: {
          clerk: { select: { id: true, name: true } },
          customer: { select: { id: true, name: true } },
          items: true,
          payments: true,
        },
      })

      return newOrder
    })

    return NextResponse.json({ success: true, data: order }, { status: 201 })
  } catch (error) {
    console.error('Create order error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create order' } },
      { status: 500 }
    )
  }
}
