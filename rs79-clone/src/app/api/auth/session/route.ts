import { NextResponse } from 'next/server'
import { getSession } from '@/lib/auth'

/**
 * GET /api/auth/session
 * Returns current session data
 * Used by AuthProvider to check auth status
 */
export async function GET() {
  try {
    const session = await getSession()
    
    if (!session) {
      return NextResponse.json({
        success: true,
        data: { session: null },
      })
    }

    return NextResponse.json({
      success: true,
      data: { session },
    })
  } catch (error) {
    console.error('Session error:', error)
    return NextResponse.json(
      { 
        success: false, 
        error: { code: 'INTERNAL_ERROR', message: 'Failed to get session' } 
      },
      { status: 500 }
    )
  }
}
