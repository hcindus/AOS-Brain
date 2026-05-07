import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

// GET /api/customers - Search customers
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const search = searchParams.get('q') || searchParams.get('search')
    const page = parseInt(searchParams.get('page') || '1')
    const limit = parseInt(searchParams.get('limit') || '20')

    const where: any = {}
    
    if (search) {
      where.OR = [
        { name: { contains: search, mode: 'insensitive' } },
        { phone: { contains: search, mode: 'insensitive' } },
        { loyaltyCardNo: { contains: search, mode: 'insensitive' } },
      ]
    }

    const [customers, total] = await Promise.all([
      prisma.customer.findMany({
        where,
        include: {
          storeCredit: true,
        },
        orderBy: { name: 'asc' },
        skip: (page - 1) * limit,
        take: limit,
      }),
      prisma.customer.count({ where }),
    ])

    return NextResponse.json({
      success: true,
      data: customers,
      meta: { page, limit, total },
    })
  } catch (error) {
    console.error('List customers error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'An error occurred' } },
      { status: 500 }
    )
  }
}

// POST /api/customers - Create new customer
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
    const cardNo = loyaltyCardNo || `LOYAL${Date.now().toString(36).toUpperCase()}`

    const customer = await prisma.customer.create({
      data: {
        name,
        phone,
        loyaltyCardNo: cardNo,
      },
      include: {
        storeCredit: true,
      },
    })

    return NextResponse.json({ success: true, data: customer })
  } catch (error: any) {
    if (error.code === 'P2002') {
      return NextResponse.json(
        { success: false, error: { code: 'DUPLICATE_ERROR', message: 'Loyalty card number already exists' } },
        { status: 400 }
      )
    }
    console.error('Create customer error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'An error occurred' } },
      { status: 500 }
    )
  }
}
