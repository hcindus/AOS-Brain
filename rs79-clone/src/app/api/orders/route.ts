import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { getSession } from '@/lib/auth'

// GET /api/orders - List orders
export async function GET(request: NextRequest) {
  try {
    const session = await getSession()
    
    if (!session) {
      return NextResponse.json(
        { success: false, error: { code: 'UNAUTHORIZED', message: 'Not authenticated' } },
        { status: 401 }
      )
    }

    const { searchParams } = new URL(request.url)
    const status = searchParams.get('status')
    const clerkId = searchParams.get('clerkId')
    const customerId = searchParams.get('customerId')
    const startDate = searchParams.get('startDate')
    const endDate = searchParams.get('endDate')
    const page = parseInt(searchParams.get('page') || '1')
    const limit = parseInt(searchParams.get('limit') || '20')

    const where: any = {}
    
    if (status) where.status = status
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
          payments: true,
        },
        orderBy: { createdAt: 'desc' },
        skip: (page - 1) * limit,
        take: limit,
      }),
      prisma.order.count({ where }),
    ])

    return NextResponse.json({
      success: true,
      data: { orders },
      meta: { page, limit, total },
    })
  } catch (error) {
    console.error('List orders error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'An error occurred' } },
      { status: 500 }
    )
  }
}

// POST /api/orders - Create new order
export async function POST(request: NextRequest) {
  try {
    const session = await getSession()
    
    if (!session) {
      return NextResponse.json(
        { success: false, error: { code: 'UNAUTHORIZED', message: 'Not authenticated' } },
        { status: 401 }
      )
    }

    const body = await request.json()
    const {
      items,
      customerId,
      currency = 'USD',
      currencyRate = 1,
      paymentType,
      payments,
      notes,
      holdName,
    } = body

    if (!items || !Array.isArray(items) || items.length === 0) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Order must have at least one item' } },
        { status: 400 }
      )
    }

    // Calculate totals
    const subtotal = items.reduce((sum: number, item: any) => sum + (item.lineTotal || item.price * item.qty), 0)
    const tax = subtotal * 0.08 // 8% tax
    const total = subtotal + tax

    // Get next transaction number
    const lastOrder = await prisma.order.findFirst({
      orderBy: { transactionNo: 'desc' },
    })
    const transactionNo = (lastOrder?.transactionNo || 1000) + 1

    // Create order
    const order = await prisma.order.create({
      data: {
        transactionNo,
        clerkId: session.id,
        customerId,
        subtotal,
        tax,
        total,
        currency,
        currencyRate,
        paymentType,
        status: 'completed',
        kdsStatus: 'new',
        notes,
        holdName,
        amountPaid: total,
        balanceDue: 0,
        items: {
          create: items.map((item: any) => ({
            itemId: item.itemId || item.id,
            name: item.name,
            price: item.price,
            qty: item.qty,
            lineTotal: item.lineTotal || item.price * item.qty,
          })),
        },
        payments: {
          create: payments?.map((payment: any) => ({
            clerkId: session.id,
            type: payment.type,
            amountUsd: payment.amount / currencyRate,
            amountNative: payment.amount,
            currency: payment.currency || currency,
            currencyRate: payment.currencyRate || currencyRate,
            reference: payment.reference,
          })) || [{
            clerkId: session.id,
            type: paymentType || 'cash',
            amountUsd: total / currencyRate,
            amountNative: total,
            currency,
            currencyRate,
          }],
        },
      },
      include: {
        items: true,
        payments: true,
        clerk: { select: { name: true } },
        customer: true,
      },
    })

    // Log the order creation
    await prisma.sessionLog.create({
      data: {
        clerkId: session.id,
        action: 'order_created',
        details: JSON.stringify({ orderId: order.id, transactionNo, total }),
      },
    })

    return NextResponse.json({ success: true, data: { order } })
  } catch (error) {
    console.error('Create order error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'An error occurred' } },
      { status: 500 }
    )
  }
}
