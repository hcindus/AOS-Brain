import { NextRequest, NextResponse } from 'next/server'

export interface SplitPaymentEntry {
  type: 'cash' | 'card' | 'crypto' | 'storecredit' | 'giftcard' | 'check'
  amount: number
  currency: string
  currencyRate: number
  reference?: string
  tendered?: number
  giftCardCode?: string
}

export interface SplitPaymentRequest {
  total: number
  entries: SplitPaymentEntry[]
}

export interface SplitPaymentResponse {
  total: number
  totalPaid: number
  remainingBalance: number
  isComplete: boolean
  entries: Array<{
    type: string
    amountNative: number
    amountUsd: number
    currency: string
    change?: number
    reference?: string
  }>
}

// POST /api/payments/split - Calculate split payment amounts
export async function POST(request: NextRequest) {
  try {
    const body: SplitPaymentRequest = await request.json()
    const { total, entries } = body

    if (!total || total <= 0) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Total must be greater than 0' } },
        { status: 400 }
      )
    }

    if (!entries || !Array.isArray(entries) || entries.length === 0) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'At least one payment entry required' } },
        { status: 400 }
      )
    }

    // Calculate each entry
    let totalPaid = 0
    const calculatedEntries = []
    const usedCurrencies = new Set<string>()

    for (const entry of entries) {
      const { type, amount, currency, currencyRate, reference, tendered } = entry
      
      // Convert to USD
      const amountUsd = currency === 'USD' 
        ? amount 
        : amount / currencyRate
      
      totalPaid += amountUsd
      usedCurrencies.add(currency)

      const calculatedEntry: any = {
        type,
        amountNative: amount,
        amountUsd,
        currency,
        reference,
      }

      // Calculate change for cash payments
      if (type === 'cash' && tendered && tendered > amount) {
        const tenderedUsd = currency === 'USD'
          ? tendered
          : tendered / currencyRate
        calculatedEntry.change = tenderedUsd - amountUsd
      }

      calculatedEntries.push(calculatedEntry)
    }

    const remainingBalance = Math.max(0, total - totalPaid)
    const isComplete = remainingBalance <= 0.01 // Allow for small rounding errors

    // Calculate change for entire order if overpaid
    let totalChange = 0
    if (totalPaid > total) {
      totalChange = totalPaid - total
    }

    const response: SplitPaymentResponse = {
      total,
      totalPaid,
      remainingBalance,
      isComplete,
      entries: calculatedEntries,
    }

    return NextResponse.json({ success: true, data: response })
  } catch (error) {
    console.error('Split payment calculation error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to calculate split payment' } },
      { status: 500 }
    )
  }
}
