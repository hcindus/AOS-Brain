import { NextRequest, NextResponse } from 'next/server'
import bcrypt from 'bcryptjs'
import { prisma } from '@/lib/prisma'
import { ClerkRole } from '@/types/clerk'

/**
 * GET /api/clerks/[id]
 * Get a specific clerk by ID (admin/manager only)
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const role = request.headers.get('x-clerk-role')
    if (role !== 'Admin' && role !== 'Manager') {
      return NextResponse.json(
        { success: false, error: { code: 'FORBIDDEN', message: 'Insufficient permissions' } },
        { status: 403 }
      )
    }

    const { id } = params

    const clerk = await prisma.clerk.findUnique({
      where: { id },
      select: {
        id: true,
        name: true,
        role: true,
        active: true,
        createdAt: true,
        _count: {
          select: {
            orders: true,
            payments: true,
          },
        },
      },
    })

    if (!clerk) {
      return NextResponse.json(
        { success: false, error: { code: 'NOT_FOUND', message: 'Clerk not found' } },
        { status: 404 }
      )
    }

    // Calculate stats
    const orders = await prisma.order.findMany({
      where: { clerkId: id },
      select: { total: true },
    })

    const totalOrders = orders.length
    const totalSales = orders.reduce((sum, order) => sum + order.total, 0)
    const averageOrderValue = totalOrders > 0 ? totalSales / totalOrders : 0

    return NextResponse.json({
      success: true,
      data: {
        ...clerk,
        totalOrders,
        totalSales,
        averageOrderValue,
      },
    })
  } catch (error) {
    console.error('Get clerk error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get clerk' } },
      { status: 500 }
    )
  }
}

/**
 * PATCH /api/clerks/[id]
 * Update a clerk (admin only)
 */
export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const role = request.headers.get('x-clerk-role')
    if (role !== 'Admin') {
      return NextResponse.json(
        { success: false, error: { code: 'FORBIDDEN', message: 'Admin access required' } },
        { status: 403 }
      )
    }

    const { id } = params
    const body = await request.json()
    const { name, role: clerkRole, pin, active } = body

    const updateData: any = {}

    if (name !== undefined) {
      if (!name || typeof name !== 'string' || name.trim().length === 0) {
        return NextResponse.json(
          { success: false, error: { code: 'VALIDATION_ERROR', message: 'Name is required' } },
          { status: 400 }
        )
      }
      updateData.name = name.trim()
    }

    if (clerkRole !== undefined) {
      const validRoles = Object.values(ClerkRole)
      if (!validRoles.includes(clerkRole)) {
        return NextResponse.json(
          { success: false, error: { code: 'VALIDATION_ERROR', message: 'Invalid role' } },
          { status: 400 }
        )
      }
      updateData.role = clerkRole
    }

    if (pin !== undefined) {
      if (typeof pin !== 'string' || pin.length !== 4 || !/^[0-9]{4}$/.test(pin)) {
        return NextResponse.json(
          { success: false, error: { code: 'VALIDATION_ERROR', message: 'PIN must be 4 digits' } },
          { status: 400 }
        )
      }
      updateData.pin = bcrypt.hashSync(pin, 10)
    }

    if (active !== undefined) {
      updateData.active = active
    }

    const clerk = await prisma.clerk.update({
      where: { id },
      data: updateData,
      select: {
        id: true,
        name: true,
        role: true,
        active: true,
        createdAt: true,
      },
    })

    return NextResponse.json({
      success: true,
      data: clerk,
    })
  } catch (error: any) {
    console.error('Update clerk error:', error)
    if (error.code === 'P2025') {
      return NextResponse.json(
        { success: false, error: { code: 'NOT_FOUND', message: 'Clerk not found' } },
        { status: 404 }
      )
    }
    if (error.code === 'P2002') {
      return NextResponse.json(
        { success: false, error: { code: 'CONFLICT', message: 'PIN already in use' } },
        { status: 409 }
      )
    }
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update clerk' } },
      { status: 500 }
    )
  }
}

/**
 * DELETE /api/clerks/[id]
 * Deactivate a clerk (soft delete - admin only)
 */
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const role = request.headers.get('x-clerk-role')
    if (role !== 'Admin') {
      return NextResponse.json(
        { success: false, error: { code: 'FORBIDDEN', message: 'Admin access required' } },
        { status: 403 }
      )
    }

    const { id } = params

    // Soft delete by deactivating
    const clerk = await prisma.clerk.update({
      where: { id },
      data: { active: false },
      select: {
        id: true,
        name: true,
        role: true,
        active: true,
        createdAt: true,
      },
    })

    return NextResponse.json({
      success: true,
      data: clerk,
    })
  } catch (error: any) {
    console.error('Delete clerk error:', error)
    if (error.code === 'P2025') {
      return NextResponse.json(
        { success: false, error: { code: 'NOT_FOUND', message: 'Clerk not found' } },
        { status: 404 }
      )
    }
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to delete clerk' } },
      { status: 500 }
    )
  }
}
