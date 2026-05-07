import { NextRequest, NextResponse } from 'next/server'
import { getSession } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

export async function POST(request: NextRequest) {
  try {
    const session = await getSession()

    if (session) {
      // Log the logout
      await prisma.sessionLog.create({
        data: {
          clerkId: session.id,
          action: 'logout',
          details: JSON.stringify({ ipAddress: request.ip ?? 'unknown' }),
        },
      })
    }

    const response = NextResponse.json({
      success: true,
      data: { message: 'Logged out successfully' },
    })

    response.cookies.delete('rs79_session')

    return response
  } catch (error) {
    console.error('Logout error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'An error occurred during logout' } },
      { status: 500 }
    )
  }
}
