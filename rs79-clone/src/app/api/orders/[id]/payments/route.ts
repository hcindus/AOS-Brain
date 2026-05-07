import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { getSession } from '@/lib/auth'
import { processPayment, calculateChange } from '@/services/payment-service'

// GET /api/orders/[id]/payments - Get order payments
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const session = await getSession()
    if (!session) {
      return NextResponse.json(
        { success: false, error: { code: 'UNAUTHORIZED', message: 'Not authenticated' } },
        { status: 401 }
      )
    }

    const { id } = params

    const payments = await prisma.payment.findMany({
      where: { orderId: id },
      orderBy: { createdAt: 'asc' },
    })

    return NextResponse.json({ success: true, data: { payments } })
  } catch (error) {
    console.error('Get payments error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'An error occurred' } },
      { status: 500 }
    )
  }
}

// POST /api/orders/[id]/payments - Add payment to order
export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const session = await getSession()
    if (!session) {
      return NextResponse.json(
        { success: false, error: { code: 'UNAUTHORIZED', message: 'Not authenticated' } },
        { status: 401 }
      )
    }

    const { id } = params
    const body = await request.json()
    
    const {
      clerkId,
      type,
      amountUsd,
      currency = 'USD',
      currencyRate = 1,
      reference,
      giftCardCode,
      tendered,
    } = body

    // Validate payment type
    const validTypes = ['cash', 'card', 'crypto', 'storecredit', 'giftcard', 'check']
    if (!validTypes.includes(type)) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Invalid payment type' } },
        { status: 400 }
      )
    }

    // Get order
    const order = await prisma.order.findUnique({
      where: { id },
      include: { payments: true, customer: true },
    })

    if (!order) {
      return NextResponse.json(
        { success: false, error: { code: 'NOT_FOUND', message: 'Order not found' } },
        { status: 404 }
      )
    }

    if (order.status === 'voided') {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Cannot add payment to voided order' } },
        { status: 400 }
      )
    }

    // Calculate remaining balance
    const totalPaid = order.payments.reduce((sum, p) => sum + p.amountUsd, 0)
    const remainingBalance = order.total - totalPaid

    // For cash payments, handle tendered amount and change
    let paymentAmount = amountUsd
    let changeDue = 0
    
    if (type === 'cash' && tendered && tendered > paymentAmount) {
      const changeResult = calculateChange(tendered, paymentAmount)
      if (changeResult.isValid) {
        changeDue = changeResult.change
      }
    }

    // Don't allow overpayment beyond reasonable rounding
    if (paymentAmount > remainingBalance + 0.01) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Payment exceeds remaining balance' } },
        { status: 400 }
      )
    }

    // Process the payment
    const result = await processPayment({
      orderId: id,
      clerkId: clerkId || session.id,
      type: type as any,
      amountUsd: paymentAmount,
      currency,
      currencyRate,
      reference,
      giftCardCode,
      customerId: order.customerId || undefined,
    })

    // Log the payment
    await prisma.sessionLog.create({
      data: {
        clerkId: clerkId || session.id,
        action: `payment_${type}`,
        details: JSON.stringify({
          orderId: id,
          amount: paymentAmount,
          currency,
          changeDue,
          giftCardBalance: result.giftCardBalance,
          storeCreditBalance: result.storeCreditBalance,
        }),
      },
    })

    return NextResponse.json({
      success: true,
      data: {
        payment: result.payment,
        changeDue,
        remainingBalance: Math.max(0, remainingBalance - paymentAmount),
        giftCardBalance: result.giftCardBalance,
        storeCreditBalance: result.storeCreditBalance,
      },
    })
  } catch (error: any) {
    console.error('Create payment error:', error)
    
    if (error.code === 'P2025') {
      return NextResponse.json(
        { success: false, error: { code: 'NOT_FOUND', message: 'Order or related resource not found' } },
        { status: 404 }
      )
    }
    
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: error.message || 'An error occurred' } },
      { status: 500 }
    )
  }
}
