import { NextRequest, NextResponse } from 'next/server'
import bcrypt from 'bcryptjs'
import { prisma } from '@/lib/prisma'

// GET /api/clerks - List clerks (admin/manager only)
export async function GET(request: NextRequest) {
  try {
    const role = request.headers.get('x-clerk-role')
    if (role !== 'Admin' && role !== 'Manager') {
      return NextResponse.json(
        { success: false, error: { code: 'FORBIDDEN', message: 'Insufficient permissions' } },
        { status: 403 }
      )
    }

    const { searchParams } = new URL(request.url)
    const active = searchParams.get('active')
    
    const where: any = {}
    if (active !== null) {
      where.active = active === 'true'
    }

    const clerks = await prisma.clerk.findMany({
      where,
      orderBy: { name: 'asc' },
      select: {
        id: true,
        name: true,
        role: true,
        active: true,
        createdAt: true,
      },
    })

    return NextResponse.json({ success: true, data: clerks })
  } catch (error) {
    console.error('List clerks error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to list clerks' } },
      { status: 500 }
    )
  }
}

// POST /api/clerks - Create clerk (admin only)
export async function POST(request: NextRequest) {
  try {
    const role = request.headers.get('x-clerk-role')
    if (role !== 'Admin') {
      return NextResponse.json(
        { success: false, error: { code: 'FORBIDDEN', message: 'Admin access required' } },
        { status: 403 }
      )
    }

    const body = await request.json()
    const { name, role: clerkRole, pin } = body

    if (!name || !clerkRole || !pin) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Name, role, and PIN required' } },
        { status: 400 }
      )
    }

    if (typeof pin !== 'string' || pin.length !== 4 || !/^[0-9]{4}$/.test(pin)) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'PIN must be 4 digits' } },
        { status: 400 }
      )
    }

    const validRoles = ['Admin', 'Manager', 'Clerk']
    if (!validRoles.includes(clerkRole)) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Invalid role' } },
        { status: 400 }
      )
    }

    const hashedPin = bcrypt.hashSync(pin, 10)

    const clerk = await prisma.clerk.create({
      data: {
        name,
        role: clerkRole,
        pin: hashedPin,
        active: true,
      },
      select: {
        id: true,
        name: true,
        role: true,
        active: true,
        createdAt: true,
      },
    })

    return NextResponse.json({ success: true, data: clerk }, { status: 201 })
  } catch (error: any) {
    console.error('Create clerk error:', error)
    if (error.code === 'P2002') {
      return NextResponse.json(
        { success: false, error: { code: 'CONFLICT', message: 'PIN already in use' } },
        { status: 409 }
      )
    }
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create clerk' } },
      { status: 500 }
    )
  }
}
