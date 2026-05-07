import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

// POST /api/payments/giftcard/use - Apply gift card to order
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { code, amount, orderId } = body

    if (!code || typeof code !== 'string') {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Gift card code is required' } },
        { status: 400 }
      )
    }

    if (!amount || amount <= 0) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Amount must be greater than 0' } },
        { status: 400 }
      )
    }

    // Normalize the code
    const normalizedCode = code.toUpperCase().replace(/\s/g, '')

    // Verify the gift card first
    const verifyResponse = await fetch(`${process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'}/api/payments/giftcard/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code: normalizedCode }),
    })

    if (!verifyResponse.ok) {
      const error = await verifyResponse.json()
      return NextResponse.json(error, { status: verifyResponse.status })
    }

    const { data: giftCardInfo } = await verifyResponse.json()

    // Check if amount exceeds balance
    if (amount > giftCardInfo.balance) {
      return NextResponse.json(
        { 
          success: false, 
          error: { 
            code: 'INSUFFICIENT_BALANCE', 
            message: `Amount ($${amount.toFixed(2)}) exceeds available balance ($${giftCardInfo.balance.toFixed(2)})` 
          } 
        },
        { status: 400 }
      )
    }

    // Calculate remaining balance after use
    const newBalance = giftCardInfo.balance - amount

    // In a real implementation, update the gift card balance in database
    // For customer store credit, update loyalty points
    if (giftCardInfo.customerId) {
      const pointsToDeduct = Math.ceil(amount * 100) // Convert dollars back to points
      await prisma.customer.update({
        where: { id: giftCardInfo.customerId },
        data: {
          loyaltyPoints: { decrement: pointsToDeduct },
        },
      })
    }

    return NextResponse.json({
      success: true,
      data: {
        code: normalizedCode,
        amountApplied: amount,
        previousBalance: giftCardInfo.balance,
        newBalance,
        transactionId: `TXN-${Date.now()}`,
        timestamp: new Date().toISOString(),
      },
    })
  } catch (error) {
    console.error('Gift card use error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to apply gift card' } },
      { status: 500 }
    )
  }
}
