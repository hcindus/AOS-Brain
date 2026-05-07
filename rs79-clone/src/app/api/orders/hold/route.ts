import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { getSession } from '@/lib/auth'

// POST /api/orders/hold - Hold an order for later
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
      holdName,
      notes,
    } = body

    if (!items || !Array.isArray(items) || items.length === 0) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Order must have at least one item' } },
        { status: 400 }
      )
    }

    // Calculate totals
    const subtotal = items.reduce((sum: number, item: any) => sum + (item.lineTotal || item.price * item.qty), 0)
    const tax = subtotal * 0.1 // 10% tax
    const total = subtotal + tax

    // Get next transaction number
    const lastOrder = await prisma.order.findFirst({
      orderBy: { transactionNo: 'desc' },
    })
    const transactionNo = (lastOrder?.transactionNo || 1000) + 1

    // Create held order
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
        paymentType: 'pending',
        status: 'pending',
        kdsStatus: 'new',
        holdName: holdName || `Hold #${transactionNo}`,
        notes,
        amountPaid: 0,
        balanceDue: total,
        items: {
          create: items.map((item: any) => ({
            itemId: item.itemId || item.id,
            name: item.name,
            price: item.price,
            qty: item.qty,
            lineTotal: item.lineTotal || item.price * item.qty,
          })),
        },
      },
      include: {
        items: true,
        clerk: { select: { name: true } },
        customer: true,
      },
    })

    // Log the hold
    await prisma.sessionLog.create({
      data: {
        clerkId: session.id,
        action: 'order_held',
        details: JSON.stringify({ orderId: order.id, holdName, total }),
      },
    })

    return NextResponse.json({ success: true, data: { order } })
  } catch (error) {
    console.error('Hold order error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'An error occurred' } },
      { status: 500 }
    )
  }
}

// GET /api/orders/hold - List held orders
export async function GET(request: NextRequest) {
  try {
    const session = await getSession()
    if (!session) {
      return NextResponse.json(
        { success: false, error: { code: 'UNAUTHORIZED', message: 'Not authenticated' } },
        { status: 401 }
      )
    }

    const heldOrders = await prisma.order.findMany({
      where: {
        status: 'pending',
        holdName: { not: null },
      },
      include: {
        items: true,
        clerk: { select: { id: true, name: true } },
        customer: { select: { id: true, name: true, loyaltyCardNo: true } },
      },
      orderBy: { createdAt: 'desc' },
    })

    return NextResponse.json({ success: true, data: { orders: heldOrders } })
  } catch (error) {
    console.error('List held orders error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'An error occurred' } },
      { status: 500 }
    )
  }
}
