import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

// GET /api/items - List/search items
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const query = searchParams.get('q')
    const category = searchParams.get('category')
    const active = searchParams.get('active')
    const limit = parseInt(searchParams.get('limit') ?? '50')
    const offset = parseInt(searchParams.get('offset') ?? '0')

    const where: any = {}
    if (query) {
      where.OR = [
        { name: { contains: query, mode: 'insensitive' } },
        { sku: { contains: query, mode: 'insensitive' } },
      ]
    }
    if (category) where.category = category
    if (active !== null) where.active = active === 'true'

    const [items, total] = await Promise.all([
      prisma.item.findMany({
        where,
        orderBy: { name: 'asc' },
        take: limit,
        skip: offset,
      }),
      prisma.item.count({ where }),
    ])

    return NextResponse.json({
      success: true,
      data: items,
      meta: { limit, offset, total },
    })
  } catch (error) {
    console.error('List items error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to list items' } },
      { status: 500 }
    )
  }
}

// POST /api/items - Create item (admin only)
export async function POST(request: NextRequest) {
  try {
    const role = request.headers.get('x-clerk-role')
    if (role !== 'Admin' && role !== 'Manager') {
      return NextResponse.json(
        { success: false, error: { code: 'FORBIDDEN', message: 'Admin or Manager access required' } },
        { status: 403 }
      )
    }

    const body = await request.json()
    const { sku, name, price, category, active = true } = body

    if (!sku || !name || price === undefined || !category) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'SKU, name, price, and category required' } },
        { status: 400 }
      )
    }

    const item = await prisma.item.create({
      data: {
        sku,
        name,
        price: parseFloat(price),
        category,
        active,
      },
    })

    return NextResponse.json({ success: true, data: item }, { status: 201 })
  } catch (error: any) {
    console.error('Create item error:', error)
    if (error.code === 'P2002') {
      return NextResponse.json(
        { success: false, error: { code: 'CONFLICT', message: 'SKU already exists' } },
        { status: 409 }
      )
    }
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create item' } },
      { status: 500 }
    )
  }
}
