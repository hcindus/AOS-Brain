import { NextRequest, NextResponse } from 'next/server'
import bcrypt from 'bcryptjs'
import { prisma } from '@/lib/prisma'
import { createSession } from '@/lib/auth'

export async function POST(request: NextRequest) {
  try {
    const { clerkId, pin } = await request.json()

    if (!clerkId || !pin) {
      return NextResponse.json(
        { success: false, error: { code: 'MISSING_CREDENTIALS', message: 'Clerk ID and PIN are required' } },
        { status: 400 }
      )
    }

    const clerk = await prisma.clerk.findUnique({
      where: { id: clerkId },
    })

    if (!clerk) {
      return NextResponse.json(
        { success: false, error: { code: 'INVALID_CREDENTIALS', message: 'Invalid clerk ID or PIN' } },
        { status: 401 }
      )
    }

    if (!clerk.active) {
      return NextResponse.json(
        { success: false, error: { code: 'ACCOUNT_INACTIVE', message: 'Account is inactive' } },
        { status: 403 }
      )
    }

    const isPinValid = await bcrypt.compare(pin, clerk.pin)

    if (!isPinValid) {
      return NextResponse.json(
        { success: false, error: { code: 'INVALID_CREDENTIALS', message: 'Invalid clerk ID or PIN' } },
        { status: 401 }
      )
    }

    // Create session
    const session = {
      id: clerk.id,
      name: clerk.name,
      role: clerk.role as 'Admin' | 'Manager' | 'Clerk',
    }

    const token = createSession(session)

    // Log the login
    await prisma.sessionLog.create({
      data: {
        clerkId: clerk.id,
        action: 'login',
        details: JSON.stringify({ ipAddress: request.ip ?? 'unknown' }),
      },
    })

    // Set cookie
    const response = NextResponse.json({
      success: true,
      data: { clerk: session },
    })

    response.cookies.set('rs79_session', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 60 * 60 * 12, // 12 hours
    })

    return response
  } catch (error) {
    console.error('Login error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'An error occurred during login' } },
      { status: 500 }
    )
  }
}
