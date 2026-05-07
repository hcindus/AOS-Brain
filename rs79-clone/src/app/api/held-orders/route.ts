import { NextRequest, NextResponse } from 'next/server'
import { ValidationError, NotFoundError } from '@/lib/errors'
import { 
  holdOrder, 
  recallOrder, 
  listHeldOrders, 
  cancelHeldOrder,
  extendHoldExpiration 
} from '@/services/hold-order-service'
import { authenticateRequest } from '@/lib/auth'

// POST /api/held-orders - Hold an order
export async function POST(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await req.json()
    const { holdName, items, subtotal, tax, total, customerId, notes } = body

    const result = await holdOrder({
      clerkId: clerk.id,
      holdName,
      items,
      subtotal,
      tax,
      total,
      customerId,
      notes,
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
    console.error('Hold order error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

// GET /api/held-orders - List held orders
export async function GET(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { searchParams } = new URL(req.url)
    const includeExpired = searchParams.get('includeExpired') === 'true'
    const clerkFilter = searchParams.get('clerkId')

    const result = await listHeldOrders({
      clerkId: clerkFilter || undefined,
      includeExpired,
    })

    return NextResponse.json({
      success: true,
      data: result,
    })
  } catch (error) {
    console.error('List held orders error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

// PATCH /api/held-orders - Recall or extend a held order
export async function PATCH(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await req.json()
    const { action, ticketNumber, additionalHours } = body

    if (!ticketNumber) {
      return NextResponse.json({ error: 'Ticket number is required' }, { status: 400 })
    }

    if (action === 'recall') {
      const result = await recallOrder(parseInt(ticketNumber))
      return NextResponse.json({
        success: true,
        data: result,
      })
    }

    if (action === 'extend') {
      if (!additionalHours) {
        return NextResponse.json({ error: 'Additional hours required' }, { status: 400 })
      }
      const result = await extendHoldExpiration(
        parseInt(ticketNumber),
        additionalHours,
        clerk.id
      )
      return NextResponse.json({
        success: true,
        data: result,
      })
    }

    return NextResponse.json({ error: 'Invalid action' }, { status: 400 })
  } catch (error) {
    if (error instanceof ValidationError) {
      return NextResponse.json({ error: error.message }, { status: 400 })
    }
    if (error instanceof NotFoundError) {
      return NextResponse.json({ error: error.message }, { status: 404 })
    }
    console.error('Held order action error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

// DELETE /api/held-orders - Cancel a held order
export async function DELETE(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { searchParams } = new URL(req.url)
    const ticketNumber = searchParams.get('ticketNumber')

    if (!ticketNumber) {
      return NextResponse.json({ error: 'Ticket number is required' }, { status: 400 })
    }

    await cancelHeldOrder(parseInt(ticketNumber), clerk.id)

    return NextResponse.json({
      success: true,
      message: 'Held order cancelled successfully',
    })
  } catch (error) {
    if (error instanceof ValidationError) {
      return NextResponse.json({ error: error.message }, { status: 400 })
    }
    if (error instanceof NotFoundError) {
      return NextResponse.json({ error: error.message }, { status: 404 })
    }
    console.error('Cancel held order error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
