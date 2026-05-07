import { NextRequest, NextResponse } from 'next/server'
import { ValidationError, NotFoundError, PaymentError } from '@/lib/errors'
import { processSplitTender, getSplitTenderStatus } from '@/services/split-tender-service'
import { authenticateRequest } from '@/lib/auth'

// POST /api/split-tender - Process multiple payments for single transaction
export async function POST(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await req.json()
    const { orderId, payments } = body

    if (!orderId || !payments || !Array.isArray(payments)) {
      return NextResponse.json(
        { error: 'Order ID and payments array are required' },
        { status: 400 }
      )
    }

    const result = await processSplitTender({
      orderId,
      clerkId: clerk.id,
      payments,
    })

    return NextResponse.json({
      success: true,
      data: result,
    })
  } catch (error) {
    if (error instanceof ValidationError) {
      return NextResponse.json({ error: error.message }, { status: 400 })
    }
    if (error instanceof NotFoundError) {
      return NextResponse.json({ error: error.message }, { status: 404 })
    }
    if (error instanceof PaymentError) {
      return NextResponse.json({ error: error.message }, { status: 400 })
    }
    console.error('Split tender error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

// GET /api/split-tender?orderId=xxx - Get split tender status
export async function GET(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { searchParams } = new URL(req.url)
    const orderId = searchParams.get('orderId')

    if (!orderId) {
      return NextResponse.json({ error: 'Order ID is required' }, { status: 400 })
    }

    const result = await getSplitTenderStatus(orderId)

    return NextResponse.json({
      success: true,
      data: result,
    })
  } catch (error) {
    if (error instanceof NotFoundError) {
      return NextResponse.json({ error: error.message }, { status: 404 })
    }
    console.error('Get split tender status error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
