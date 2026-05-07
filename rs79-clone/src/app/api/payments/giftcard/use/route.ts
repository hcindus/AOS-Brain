import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { getSession } from '@/lib/auth'

// POST /api/payments/giftcard/use - Use gift card for payment
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
    const { code, amount, orderId } = body

    if (!code) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Gift card code is required' } },
        { status: 400 }
      )
    }

    if (!amount || amount <= 0) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Valid amount is required' } },
        { status: 400 }
      )
    }

    const giftCard = await prisma.giftCard.findUnique({
      where: { code: code.trim().toUpperCase() },
    })

    if (!giftCard) {
      return NextResponse.json(
        { success: false, error: { code: 'NOT_FOUND', message: 'Gift card not found' } },
        { status: 404 }
      )
    }

    if (!giftCard.isActive) {
      return NextResponse.json(
        { success: false, error: { code: 'INVALID_CARD', message: 'Gift card is inactive' } },
        { status: 400 }
      )
    }

    if (giftCard.expiresAt && new Date() > giftCard.expiresAt) {
      return NextResponse.json(
        { success: false, error: { code: 'EXPIRED', message: 'Gift card has expired' } },
        { status: 400 }
      )
    }

    if (giftCard.balance < amount) {
      return NextResponse.json(
        { 
          success: false, 
          error: { 
            code: 'INSUFFICIENT_FUNDS', 
            message: `Insufficient balance. Available: $${giftCard.balance.toFixed(2)}, Requested: $${amount.toFixed(2)}` 
          } 
        },
        { status: 400 }
      )
    }

    // Deduct from gift card
    const updatedCard = await prisma.giftCard.update({
      where: { id: giftCard.id },
      data: {
        balance: { decrement: amount },
      },
    })

    // Log the usage
    await prisma.sessionLog.create({
      data: {
        clerkId: session.id,
        action: 'giftcard_used',
        details: JSON.stringify({
          code: giftCard.code,
          amount,
          remainingBalance: updatedCard.balance,
          orderId,
        }),
      },
    })

    return NextResponse.json({
      success: true,
      data: {
        code: updatedCard.code,
        amountUsed: amount,
        remainingBalance: updatedCard.balance,
      },
    })
  } catch (error) {
    console.error('Use gift card error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'An error occurred' } },
      { status: 500 }
    )
  }
}
