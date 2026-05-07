import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { ValidationError, NotFoundError, PaymentError } from '@/lib/errors'
import { splitOrder, processSplitPayment, getSplitChecks } from '@/services/split-check-service'
import { authenticateRequest } from '@/lib/auth'

// POST /api/split-check - Split an order into multiple checks
export async function POST(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await req.json()
    const { orderId, splitType, numChecks, itemAssignments } = body

    if (!orderId) {
      return NextResponse.json({ error: 'Order ID is required' }, { status: 400 })
    }

    const result = await splitOrder({
      orderId,
      splitType,
      numChecks,
      itemAssignments,
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
    console.error('Split check error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

// GET /api/split-check?orderId=xxx - Get split checks for an order
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

    const result = await getSplitChecks(orderId)

    return NextResponse.json({
      success: true,
      data: result,
    })
  } catch (error) {
    if (error instanceof NotFoundError) {
      return NextResponse.json({ error: error.message }, { status: 404 })
    }
    console.error('Get split checks error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

// PATCH /api/split-check - Process payment for a split check
export async function PATCH(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await req.json()
    const { orderId, checkId, type, amount, reference, giftCardCode } = body

    if (!orderId || !checkId || !type || !amount) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 })
    }

    const result = await processSplitPayment({
      orderId,
      checkId,
      type,
      amount,
      reference,
      giftCardCode,
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
    console.error('Process split payment error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
