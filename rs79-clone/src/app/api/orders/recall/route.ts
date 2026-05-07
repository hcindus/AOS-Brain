import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

// GET /api/orders/recall - List held orders for recall
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
