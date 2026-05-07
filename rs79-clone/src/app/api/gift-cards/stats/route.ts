import { NextRequest, NextResponse } from 'next/server'
import { NotFoundError } from '@/lib/errors'
import { getGiftCardStats } from '@/services/giftcard-service'
import { authenticateRequest, hasPermission } from '@/lib/auth'
import { ClerkRole } from '@/types/clerk'

// GET /api/gift-cards/stats - Get gift card statistics
export async function GET(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Only Admin and Manager can view stats
    if (!hasPermission(clerk, [ClerkRole.Admin, ClerkRole.Manager])) {
      return NextResponse.json({ error: 'Insufficient permissions' }, { status: 403 })
    }

    const stats = await getGiftCardStats()

    return NextResponse.json({
      success: true,
      data: stats,
    })
  } catch (error) {
    console.error('Get gift card stats error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
