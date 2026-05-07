import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = params

    const order = await prisma.order.findUnique({
      where: { id },
      include: {
        clerk: { select: { id: true, name: true, role: true } },
        customer: { select: { id: true, name: true, phone: true, loyaltyCardNo: true, loyaltyPoints: true } },
        items: true,
        payments: true,
      },
    })

    if (!order) {
      return NextResponse.json(
        { success: false, error: { code: 'ORDER_NOT_FOUND', message: 'Order not found' } },
        { status: 404 }
      )
    }

    return NextResponse.json({ success: true, data: order })
  } catch (error) {
    console.error('Get order error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get order' } },
      { status: 500 }
    )
  }
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = params
    const body = await request.json()
    const { status, kdsStatus, notes } = body

    const updateData: any = {}
    if (status) updateData.status = status
    if (kdsStatus) updateData.kdsStatus = kdsStatus
    if (notes !== undefined) updateData.notes = notes

    const order = await prisma.order.update({
      where: { id },
      data: updateData,
      include: {
        clerk: { select: { id: true, name: true } },
        customer: { select: { id: true, name: true } },
        items: true,
        payments: true,
      },
    })

    return NextResponse.json({ success: true, data: order })
  } catch (error: any) {
    console.error('Update order error:', error)
    if (error.code === 'P2025') {
      return NextResponse.json(
        { success: false, error: { code: 'ORDER_NOT_FOUND', message: 'Order not found' } },
        { status: 404 }
      )
    }
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update order' } },
      { status: 500 }
    )
  }
}
