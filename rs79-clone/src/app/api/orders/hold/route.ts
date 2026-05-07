import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

// GET /api/orders/hold - List held orders
export async function GET(request: NextRequest) {
  try {
    const heldOrders = await prisma.order.findMany({
      where: { status: 'pending' },
      include: {
        items: {
          select: {
            itemId: true,
            name: true,
            price: true,
            qty: true,
            lineTotal: true,
          }
        },
        customer: {
          select: {
            id: true,
            name: true,
          }
        }
      },
      orderBy: { createdAt: 'desc' },
    })

    const formattedOrders = heldOrders.map(order => ({
      id: order.id,
      holdName: order.holdName || 'Unnamed Order',
      items: order.items,
      subtotal: order.subtotal,
      tax: order.tax,
      total: order.total,
      customerId: order.customerId,
      customerName: order.customer?.name,
      createdAt: order.createdAt.toISOString(),
    }))

    return NextResponse.json({
      success: true,
      data: formattedOrders,
    })
  } catch (error) {
    console.error('List held orders error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to list held orders' } },
      { status: 500 }
    )
  }
}

// POST /api/orders/hold - Create a held order
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
    const { name, items, subtotal, tax, total, customerId } = body

    if (!name || !items || items.length === 0) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Name and items required' } },
        { status: 400 }
      )
    }

    // Get next transaction number
    const lastOrder = await prisma.order.findFirst({
      orderBy: { transactionNo: 'desc' },
      select: { transactionNo: true },
    })
    const transactionNo = (lastOrder?.transactionNo ?? 0) + 1

    // Create held order
    const order = await prisma.order.create({
      data: {
        clerkId,
        customerId: customerId || null,
        transactionNo,
        subtotal,
        tax,
        total,
        currency: 'USD',
        currencyRate: 1,
        paymentType: 'pending',
        tendered: 0,
        change: 0,
        amountPaid: 0,
        balanceDue: total,
        status: 'pending',
        kdsStatus: 'new',
        holdName: name,
        items: {
          create: items.map((item: any) => ({
            itemId: item.itemId,
            name: item.name,
            price: item.price,
            qty: item.qty,
            lineTotal: item.lineTotal,
          })),
        },
      },
      include: {
        items: true,
        customer: { select: { id: true, name: true } },
      },
    })

    return NextResponse.json({
      success: true,
      data: {
        id: order.id,
        holdName: order.holdName,
        createdAt: order.createdAt,
      },
    }, { status: 201 })
  } catch (error) {
    console.error('Create held order error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to hold order' } },
      { status: 500 }
    )
  }
}
