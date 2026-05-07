import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

// POST /api/payments/giftcard/verify - Check gift card balance by code
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { code } = body

    if (!code || typeof code !== 'string') {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Gift card code is required' } },
        { status: 400 }
      )
    }

    // Normalize the code (remove spaces, uppercase)
    const normalizedCode = code.toUpperCase().replace(/\s/g, '')

    // For this implementation, we'll check if the code exists in the database
    // In a real implementation, you'd have a GiftCard model
    // Here we'll use a mock implementation for demonstration
    
    // Check if this is a customer-specific store credit
    const customer = await prisma.customer.findFirst({
      where: {
        OR: [
          { loyaltyCardNo: normalizedCode },
          { phone: normalizedCode },
        ],
      },
    })

    if (customer) {
      // Return customer store credit info
      return NextResponse.json({
        success: true,
        data: {
          code: normalizedCode,
          type: 'storecredit',
          balance: customer.loyaltyPoints * 0.01, // Points converted to dollars
          customerId: customer.id,
          customerName: customer.name,
          isValid: true,
          expiresAt: null,
        },
      })
    }

    // Mock gift card validation for demo
    // In production, query a GiftCard table
    const mockGiftCards: Record<string, { balance: number; expiresAt: string | null }> = {
      'GIFT-1234': { balance: 50.00, expiresAt: null },
      'GIFT-5678': { balance: 100.00, expiresAt: null },
      'GIFT-9999': { balance: 25.00, expiresAt: '2025-12-31T23:59:59Z' },
    }

    const giftCard = mockGiftCards[normalizedCode]

    if (!giftCard) {
      return NextResponse.json(
        { success: false, error: { code: 'NOT_FOUND', message: 'Gift card not found or invalid' } },
        { status: 404 }
      )
    }

    // Check if expired
    if (giftCard.expiresAt && new Date(giftCard.expiresAt) < new Date()) {
      return NextResponse.json(
        { success: false, error: { code: 'EXPIRED', message: 'Gift card has expired' } },
        { status: 400 }
      )
    }

    // Check if balance is zero
    if (giftCard.balance <= 0) {
      return NextResponse.json(
        { success: false, error: { code: 'ZERO_BALANCE', message: 'Gift card has no remaining balance' } },
        { status: 400 }
      )
    }

    return NextResponse.json({
      success: true,
      data: {
        code: normalizedCode,
        type: 'giftcard',
        balance: giftCard.balance,
        customerId: null,
        customerName: null,
        isValid: true,
        expiresAt: giftCard.expiresAt,
      },
    })
  } catch (error) {
    console.error('Gift card verification error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to verify gift card' } },
      { status: 500 }
    )
  }
}
