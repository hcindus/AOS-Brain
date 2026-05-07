import { NextRequest, NextResponse } from 'next/server'
import { ValidationError, NotFoundError } from '@/lib/errors'
import { 
  createGiftCard,
  validateGiftCard,
  getGiftCardDetails,
  deductBalance,
  addBalance,
  deactivateGiftCard,
  listGiftCards,
  getGiftCardStats
} from '@/services/giftcard-service'
import { authenticateRequest, hasPermission } from '@/lib/auth'
import { ClerkRole } from '@/types/clerk'

// POST /api/gift-cards - Create a new gift card
export async function POST(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Only Admin and Manager can create gift cards
    if (!hasPermission(clerk, [ClerkRole.Admin, ClerkRole.Manager])) {
      return NextResponse.json({ error: 'Insufficient permissions' }, { status: 403 })
    }

    const body = await req.json()
    const { code, originalAmount, expiresAt } = body

    const giftCard = await createGiftCard({
      code,
      originalAmount,
      expiresAt: expiresAt ? new Date(expiresAt) : undefined,
    })

    return NextResponse.json({
      success: true,
      data: giftCard,
    })
  } catch (error) {
    if (error instanceof ValidationError) {
      return NextResponse.json({ error: error.message }, { status: 400 })
    }
    console.error('Create gift card error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

// GET /api/gift-cards - List or search gift cards
export async function GET(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { searchParams } = new URL(req.url)
    const code = searchParams.get('code')
    const action = searchParams.get('action')

    if (code) {
      // Get specific gift card details
      if (action === 'validate') {
        const giftCard = await validateGiftCard(code)
        return NextResponse.json({
          success: true,
          data: giftCard,
        })
      }
      
      const details = await getGiftCardDetails(code)
      return NextResponse.json({
        success: true,
        data: details,
      })
    }

    // List gift cards
    const isActive = searchParams.get('isActive')
    const hasBalance = searchParams.get('hasBalance')
    const limit = parseInt(searchParams.get('limit') || '50')
    const offset = parseInt(searchParams.get('offset') || '0')

    const result = await listGiftCards({
      isActive: isActive !== null ? isActive === 'true' : undefined,
      hasBalance: hasBalance !== null ? hasBalance === 'true' : undefined,
      limit,
      offset,
    })

    return NextResponse.json({
      success: true,
      data: result,
    })
  } catch (error) {
    if (error instanceof ValidationError) {
      return NextResponse.json({ error: error.message }, { status: 400 })
    }
    if (error instanceof NotFoundError) {
      return NextResponse.json({ error: error.message }, { status: 404 })
    }
    console.error('Get gift cards error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

// PATCH /api/gift-cards - Update gift card (add balance, deactivate, etc)
export async function PATCH(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await req.json()
    const { code, action, amount, reason } = body

    if (!code || !action) {
      return NextResponse.json(
        { error: 'Code and action are required' },
        { status: 400 }
      )
    }

    switch (action) {
      case 'addBalance': {
        // Only Admin and Manager can add balance
        if (!hasPermission(clerk, [ClerkRole.Admin, ClerkRole.Manager])) {
          return NextResponse.json({ error: 'Insufficient permissions' }, { status: 403 })
        }
        const result = await addBalance(code, amount, reason)
        return NextResponse.json({
          success: true,
          data: result,
        })
      }

      case 'deactivate': {
        // Only Admin and Manager can deactivate
        if (!hasPermission(clerk, [ClerkRole.Admin, ClerkRole.Manager])) {
          return NextResponse.json({ error: 'Insufficient permissions' }, { status: 403 })
        }
        const result = await deactivateGiftCard(code, reason)
        return NextResponse.json({
          success: true,
          data: result,
        })
      }

      default:
        return NextResponse.json({ error: 'Invalid action' }, { status: 400 })
    }
  } catch (error) {
    if (error instanceof ValidationError) {
      return NextResponse.json({ error: error.message }, { status: 400 })
    }
    if (error instanceof NotFoundError) {
      return NextResponse.json({ error: error.message }, { status: 404 })
    }
    console.error('Update gift card error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

// GET /api/gift-cards/stats - Get gift card statistics
export async function OPTIONS(req: NextRequest) {
  return NextResponse.json({ success: true })
}
