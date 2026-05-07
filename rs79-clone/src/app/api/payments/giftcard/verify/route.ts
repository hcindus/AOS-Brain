import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { getSession } from '@/lib/auth'

// POST /api/payments/giftcard/verify - Verify gift card balance
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
    const { code } = body

    if (!code) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Gift card code is required' } },
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

    if (giftCard.balance <= 0) {
      return NextResponse.json(
        { success: false, error: { code: 'ZERO_BALANCE', message: 'Gift card has no remaining balance' } },
        { status: 400 }
      )
    }

    return NextResponse.json({
      success: true,
      data: {
        code: giftCard.code,
        balance: giftCard.balance,
        originalAmount: giftCard.originalAmount,
        isActive: giftCard.isActive,
        expiresAt: giftCard.expiresAt,
      },
    })
  } catch (error) {
    console.error('Verify gift card error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'An error occurred' } },
      { status: 500 }
    )
  }
}
