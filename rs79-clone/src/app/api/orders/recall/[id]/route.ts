import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

// POST /api/orders/recall/[id] - Recall a held order
export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const clerkId = request.headers.get('x-clerk-id')
    if (!clerkId) {
      return NextResponse.json(
        { success: false, error: { code: 'AUTH_REQUIRED', message: 'Authentication required' } },
        { status: 401 }
      )
    }

    const { id } = params

    // Get the held order
    const order = await prisma.order.findFirst({
      where: { 
        id,
        status: 'pending',
      },
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
    })

    if (!order) {
      return NextResponse.json(
        { success: false, error: { code: 'ORDER_NOT_FOUND', message: 'Held order not found' } },
        { status: 404 }
      )
    }

    // Delete the held order after recalling
    await prisma.order.delete({
      where: { id },
    })

    return NextResponse.json({
      success: true,
      data: {
        id: order.id,
        items: order.items,
        subtotal: order.subtotal,
        tax: order.tax,
        total: order.total,
        customerId: order.customerId,
        customerName: order.customer?.name,
        holdName: order.holdName,
      },
    })
  } catch (error) {
    console.error('Recall order error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to recall order' } },
      { status: 500 }
    )
  }
}
