import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = params

    const customer = await prisma.customer.findUnique({
      where: { id },
    })

    if (!customer) {
      return NextResponse.json(
        { success: false, error: { code: 'CUSTOMER_NOT_FOUND', message: 'Customer not found' } },
        { status: 404 }
      )
    }

    return NextResponse.json({ success: true, data: customer })
  } catch (error) {
    console.error('Get customer error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get customer' } },
      { status: 500 }
    )
  }
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = params
    const body = await request.json()
    const { name, phone, loyaltyPoints } = body

    const updateData: any = {}
    if (name !== undefined) updateData.name = name
    if (phone !== undefined) updateData.phone = phone
    if (loyaltyPoints !== undefined) updateData.loyaltyPoints = loyaltyPoints

    const customer = await prisma.customer.update({
      where: { id },
      data: updateData,
    })

    return NextResponse.json({ success: true, data: customer })
  } catch (error: any) {
    console.error('Update customer error:', error)
    if (error.code === 'P2025') {
      return NextResponse.json(
        { success: false, error: { code: 'CUSTOMER_NOT_FOUND', message: 'Customer not found' } },
        { status: 404 }
      )
    }
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update customer' } },
      { status: 500 }
    )
  }
}
