import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { getSession } from '@/lib/auth'

// GET /api/items - List all items
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const category = searchParams.get('category')
    const search = searchParams.get('search')
    const activeOnly = searchParams.get('active') !== 'false'

    const where: any = {}
    
    if (category) {
      where.category = category
    }
    
    if (search) {
      where.OR = [
        { name: { contains: search, mode: 'insensitive' } },
        { sku: { contains: search, mode: 'insensitive' } },
        { barcode: { contains: search, mode: 'insensitive' } },
      ]
    }
    
    if (activeOnly) {
      where.active = true
    }

    const items = await prisma.item.findMany({
      where,
      orderBy: { category: 'asc' },
    })

    // Get unique categories
    const categories = await prisma.item.findMany({
      where: activeOnly ? { active: true } : {},
      select: { category: true },
      distinct: ['category'],
    })

    return NextResponse.json({
      success: true,
      data: {
        items,
        categories: categories.map(c => c.category),
      },
    })
  } catch (error) {
    console.error('List items error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'An error occurred' } },
      { status: 500 }
    )
  }
}

// POST /api/items - Create new item (Admin/Manager only)
export async function POST(request: NextRequest) {
  try {
    const session = await getSession()
    
    if (!session) {
      return NextResponse.json(
        { success: false, error: { code: 'UNAUTHORIZED', message: 'Not authenticated' } },
        { status: 401 }
      )
    }

    if (session.role === 'Clerk') {
      return NextResponse.json(
        { success: false, error: { code: 'FORBIDDEN', message: 'Insufficient permissions' } },
        { status: 403 }
      )
    }

    const body = await request.json()
    const { sku, name, price, category, stockQty, description, barcode } = body

    if (!sku || !name || !price || !category) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Missing required fields' } },
        { status: 400 }
      )
    }

    const item = await prisma.item.create({
      data: {
        sku,
        name,
        price: parseFloat(price),
        category,
        stockQty: parseInt(stockQty) || 0,
        description,
        barcode,
        active: true,
      },
    })

    return NextResponse.json({ success: true, data: { item } })
  } catch (error) {
    console.error('Create item error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'An error occurred' } },
      { status: 500 }
    )
  }
}
