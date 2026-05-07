import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

// GET /api/customers - Search customers
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const query = searchParams.get('q')
    const limit = parseInt(searchParams.get('limit') ?? '20')
    const offset = parseInt(searchParams.get('offset') ?? '0')

    const where: any = {}
    if (query) {
      where.OR = [
        { name: { contains: query, mode: 'insensitive' } },
        { phone: { contains: query } },
        { loyaltyCardNo: { contains: query, mode: 'insensitive' } },
      ]
    }

    const [customers, total] = await Promise.all([
      prisma.customer.findMany({
        where,
        orderBy: { name: 'asc' },
        take: limit,
        skip: offset,
      }),
      prisma.customer.count({ where }),
    ])

    return NextResponse.json({
      success: true,
      data: customers,
      meta: { limit, offset, total },
    })
  } catch (error) {
    console.error('List customers error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to list customers' } },
      { status: 500 }
    )
  }
}

// POST /api/customers - Create customer
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { name, phone, loyaltyCardNo } = body

    if (!name) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Name is required' } },
        { status: 400 }
      )
    }

    // Generate loyalty card number if not provided
    const cardNo = loyaltyCardNo || `LC${Date.now().toString(36).toUpperCase()}`

    const customer = await prisma.customer.create({
      data: {
        name,
        phone: phone || null,
        loyaltyCardNo: cardNo,
        loyaltyPoints: 0,
      },
    })

    return NextResponse.json({ success: true, data: customer }, { status: 201 })
  } catch (error: any) {
    console.error('Create customer error:', error)
    if (error.code === 'P2002') {
      return NextResponse.json(
        { success: false, error: { code: 'CONFLICT', message: 'Loyalty card number already exists' } },
        { status: 409 }
      )
    }
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create customer' } },
      { status: 500 }
    )
  }
}
