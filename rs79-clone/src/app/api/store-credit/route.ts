import { NextRequest, NextResponse } from 'next/server'
import { ValidationError, NotFoundError } from '@/lib/errors'
import { 
  getStoreCredit,
  addStoreCredit,
  useStoreCredit,
  getCustomerById
} from '@/services/customer-service'
import { authenticateRequest, hasPermission } from '@/lib/auth'
import { ClerkRole } from '@/types/clerk'

// GET /api/store-credit?customerId=xxx - Get store credit for customer
export async function GET(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { searchParams } = new URL(req.url)
    const customerId = searchParams.get('customerId')

    if (!customerId) {
      return NextResponse.json({ error: 'Customer ID is required' }, { status: 400 })
    }

    const storeCredit = await getStoreCredit(customerId)

    return NextResponse.json({
      success: true,
      data: storeCredit,
    })
  } catch (error) {
    if (error instanceof NotFoundError) {
      return NextResponse.json({ error: error.message }, { status: 404 })
    }
    console.error('Get store credit error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

// POST /api/store-credit - Add store credit to customer
export async function POST(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Only Admin and Manager can add store credit
    if (!hasPermission(clerk, [ClerkRole.Admin, ClerkRole.Manager])) {
      return NextResponse.json({ error: 'Insufficient permissions' }, { status: 403 })
    }

    const body = await req.json()
    const { customerId, amount, reason } = body

    if (!customerId || !amount || !reason) {
      return NextResponse.json(
        { error: 'Customer ID, amount, and reason are required' },
        { status: 400 }
      )
    }

    const storeCredit = await addStoreCredit(customerId, amount, reason)

    return NextResponse.json({
      success: true,
      data: storeCredit,
    })
  } catch (error) {
    if (error instanceof ValidationError) {
      return NextResponse.json({ error: error.message }, { status: 400 })
    }
    if (error instanceof NotFoundError) {
      return NextResponse.json({ error: error.message }, { status: 404 })
    }
    console.error('Add store credit error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

// PATCH /api/store-credit - Use/apply store credit
export async function PATCH(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await req.json()
    const { customerId, amount } = body

    if (!customerId || !amount) {
      return NextResponse.json(
        { error: 'Customer ID and amount are required' },
        { status: 400 }
      )
    }

    const storeCredit = await useStoreCredit(customerId, amount)

    return NextResponse.json({
      success: true,
      data: storeCredit,
    })
  } catch (error) {
    if (error instanceof ValidationError) {
      return NextResponse.json({ error: error.message }, { status: 400 })
    }
    if (error instanceof NotFoundError) {
      return NextResponse.json({ error: error.message }, { status: 404 })
    }
    console.error('Use store credit error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
