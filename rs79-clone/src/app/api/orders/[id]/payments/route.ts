import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { convertToUsd } from '@/lib/currency'

// POST /api/orders/[id]/payments - Add payment to existing order
export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params
    const clerkId = request.headers.get('x-clerk-id')
    
    if (!clerkId) {
      return NextResponse.json(
        { success: false, error: { code: 'AUTH_REQUIRED', message: 'Authentication required' } },
        { status: 401 }
      )
    }

    const body = await request.json()
    const {
      type,
      amount,
      currency = 'USD',
      currencyRate = 1,
      reference,
      meta,
      tendered,
    } = body

    // Validate required fields
    if (!type || !['cash', 'card', 'crypto', 'storecredit', 'giftcard', 'check'].includes(type)) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Valid payment type is required' } },
        { status: 400 }
      )
    }

    if (!amount || amount <= 0) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Amount must be greater than 0' } },
        { status: 400 }
      )
    }

    // Get the order
    const order = await prisma.order.findUnique({
      where: { id },
      include: {
        payments: true,
        customer: true,
      },
    })

    if (!order) {
      return NextResponse.json(
        { success: false, error: { code: 'NOT_FOUND', message: 'Order not found' } },
        { status: 404 }
      )
    }

    // Check if order is already complete
    if (order.status === 'completed' && order.balanceDue <= 0) {
      return NextResponse.json(
        { success: false, error: { code: 'ORDER_COMPLETE', message: 'Order is already fully paid' } },
        { status: 400 }
      )
    }

    // Calculate payment in USD
    const amountUsd = currency === 'USD' 
      ? amount 
      : convertToUsd(amount, currency as any)

    // Calculate totals
    const currentPaid = order.amountPaid || 0
    const newTotalPaid = currentPaid + amountUsd
    const newBalanceDue = Math.max(0, order.total - newTotalPaid)
    const change = tendered && tendered > amount 
      ? tendered - amount 
      : 0

    // Update payment type if split
    let newPaymentType = order.paymentType
    if (order.paymentType !== 'split' && order.payments.length > 0) {
      newPaymentType = 'split'
    }

    // Update order status if fully paid
    const newStatus = newBalanceDue <= 0.01 ? 'completed' : 'pending'

    // Create payment and update order in transaction
    const result = await prisma.$transaction(async (tx) => {
      // Create the payment
      const payment = await tx.payment.create({
        data: {
          orderId: id,
          type,
          amountUsd,
          amountNative: amount,
          currency,
          currencyRate,
          reference: reference || null,
          meta: meta ? JSON.stringify(meta) : null,
        },
      })

      // Update order
      const updatedOrder = await tx.order.update({
        where: { id },
        data: {
          paymentType: newPaymentType,
          amountPaid: newTotalPaid,
          balanceDue: newBalanceDue,
          status: newStatus,
          tendered: tendered ? (order.tendered || 0) + tendered : order.tendered,
          change: change > 0 ? (order.change || 0) + change : order.change,
        },
        include: {
          clerk: { select: { id: true, name: true } },
          customer: { select: { id: true, name: true, loyaltyCardNo: true } },
          items: true,
          payments: true,
        },
      })

      return { payment, order: updatedOrder }
    })

    return NextResponse.json({
      success: true,
      data: {
        payment: result.payment,
        order: result.order,
        summary: {
          previousPaid: currentPaid,
          newPaid: newTotalPaid,
          balanceDue: newBalanceDue,
          isComplete: newBalanceDue <= 0.01,
          change: change > 0 ? change : 0,
        },
      },
    })
  } catch (error) {
    console.error('Add payment error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to add payment' } },
      { status: 500 }
    )
  }
}

// GET /api/orders/[id]/payments - Get payments for an order
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params

    const payments = await prisma.payment.findMany({
      where: { orderId: id },
      orderBy: { createdAt: 'asc' },
    })

    return NextResponse.json({
      success: true,
      data: payments,
    })
  } catch (error) {
    console.error('Get payments error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get payments' } },
      { status: 500 }
    )
  }
}
