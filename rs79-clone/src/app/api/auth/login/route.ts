import { NextRequest, NextResponse } from 'next/server'
import bcrypt from 'bcryptjs'
import { prisma } from '@/lib/prisma'
import { createSession } from '@/lib/auth'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { pin } = body

    if (!pin || typeof pin !== 'string' || pin.length !== 4) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'PIN must be 4 digits' } },
        { status: 400 }
      )
    }

    // Find clerk by PIN (we need to check all since PINs are hashed)
    const clerks = await prisma.clerk.findMany({
      where: { active: true },
    })

    const clerk = clerks.find((c) => bcrypt.compareSync(pin, c.pin))

    if (!clerk) {
      return NextResponse.json(
        { success: false, error: { code: 'AUTH_INVALID_PIN', message: 'Invalid PIN' } },
        { status: 401 }
      )
    }

    // Create session
    const session = { id: clerk.id, name: clerk.name, role: clerk.role }
    const token = createSession(session)

    // Set cookie
    const response = NextResponse.json({
      success: true,
      data: { clerk: { id: clerk.id, name: clerk.name, role: clerk.role } },
    })

    response.cookies.set('rs79_session', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 12 * 60 * 60, // 12 hours
      path: '/',
    })

    return response
  } catch (error) {
    console.error('Login error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Login failed' } },
      { status: 500 }
    )
  }
}
