import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = params

    const item = await prisma.item.findUnique({
      where: { id },
    })

    if (!item) {
      return NextResponse.json(
        { success: false, error: { code: 'ITEM_NOT_FOUND', message: 'Item not found' } },
        { status: 404 }
      )
    }

    return NextResponse.json({ success: true, data: item })
  } catch (error) {
    console.error('Get item error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get item' } },
      { status: 500 }
    )
  }
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const role = request.headers.get('x-clerk-role')
    if (role !== 'Admin' && role !== 'Manager') {
      return NextResponse.json(
        { success: false, error: { code: 'FORBIDDEN', message: 'Admin or Manager access required' } },
        { status: 403 }
      )
    }

    const { id } = params
    const body = await request.json()
    const { sku, name, price, category, active } = body

    const updateData: any = {}
    if (sku !== undefined) updateData.sku = sku
    if (name !== undefined) updateData.name = name
    if (price !== undefined) updateData.price = parseFloat(price)
    if (category !== undefined) updateData.category = category
    if (active !== undefined) updateData.active = active

    const item = await prisma.item.update({
      where: { id },
      data: updateData,
    })

    return NextResponse.json({ success: true, data: item })
  } catch (error: any) {
    console.error('Update item error:', error)
    if (error.code === 'P2025') {
      return NextResponse.json(
        { success: false, error: { code: 'ITEM_NOT_FOUND', message: 'Item not found' } },
        { status: 404 }
      )
    }
    if (error.code === 'P2002') {
      return NextResponse.json(
        { success: false, error: { code: 'CONFLICT', message: 'SKU already exists' } },
        { status: 409 }
      )
    }
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update item' } },
      { status: 500 }
    )
  }
}

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

    await prisma.item.delete({
      where: { id },
    })

    return NextResponse.json({ success: true, data: { message: 'Item deleted' } })
  } catch (error: any) {
    console.error('Delete item error:', error)
    if (error.code === 'P2025') {
      return NextResponse.json(
        { success: false, error: { code: 'ITEM_NOT_FOUND', message: 'Item not found' } },
        { status: 404 }
      )
    }
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to delete item' } },
      { status: 500 }
    )
  }
}
