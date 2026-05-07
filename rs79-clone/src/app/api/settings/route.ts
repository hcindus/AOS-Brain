import { NextRequest, NextResponse } from 'next/server'
import { getStoreSettings, updateStoreSettings } from '@/services/settings-service'
import { prisma } from '@/lib/db'
import { requireAuth } from '@/lib/auth'

// GET /api/settings - Get store settings
export async function GET(req: NextRequest) {
  try {
    const settings = await getStoreSettings()
    return NextResponse.json({ success: true, data: settings })
  } catch (error) {
    console.error('Failed to get settings:', error)
    return NextResponse.json(
      { success: false, error: { code: 'SETTINGS_ERROR', message: 'Failed to get settings' } },
      { status: 500 }
    )
  }
}

// POST /api/settings - Update store settings
export async function POST(req: NextRequest) {
  const auth = await requireAuth(req)
  if (!auth.success) return auth.response

  try {
    const body = await req.json()
    const { taxMode, taxConfig, currency, receiptHeader, receiptFooter } = body

    // Validate taxMode
    if (taxMode && !['exclusive', 'inclusive'].includes(taxMode)) {
      return NextResponse.json(
        { success: false, error: { code: 'INVALID_TAX_MODE', message: 'Tax mode must be exclusive or inclusive' } },
        { status: 400 }
      )
    }

    // Update settings
    const result = await updateStoreSettings({
      taxMode,
      taxConfig,
      currency,
      receiptHeader,
      receiptFooter,
    })

    if (!result.success) {
      return NextResponse.json(
        { success: false, error: { code: 'UPDATE_FAILED', message: result.error } },
        { status: 500 }
      )
    }

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Failed to update settings:', error)
    return NextResponse.json(
      { success: false, error: { code: 'UPDATE_ERROR', message: 'Failed to update settings' } },
      { status: 500 }
    )
  }
}