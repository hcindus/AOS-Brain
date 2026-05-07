import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

// PATCH /api/kds/orders/[id] - Update KDS status
export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = params
    const body = await request.json()
    const { kdsStatus } = body

    if (!kdsStatus || !['new', 'preparing', 'done'].includes(kdsStatus)) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Invalid KDS status' } },
        { status: 400 }
      )
    }

    const order = await prisma.order.update({
      where: { id },
      data: { kdsStatus },
      include: {
        clerk: { select: { name: true } },
        items: { select: { name: true, qty: true } },
      },
    })

    return NextResponse.json({ success: true, data: order })
  } catch (error: any) {
    console.error('Update KDS status error:', error)
    if (error.code === 'P2025') {
      return NextResponse.json(
        { success: false, error: { code: 'ORDER_NOT_FOUND', message: 'Order not found' } },
        { status: 404 }
      )
    }
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update order status' } },
      { status: 500 }
    )
  }
}
