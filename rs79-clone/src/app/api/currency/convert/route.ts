import { NextRequest, NextResponse } from 'next/server'
import { convertAmount, getExchangeRate, CURRENCIES } from '@/lib/currency'
import { prisma } from '@/lib/prisma'
import type { CurrencyCode } from '@/types'

// GET /api/currency/convert?from=USD&to=EUR&amount=100 - Real-time conversion
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const from = (searchParams.get('from') || 'USD') as CurrencyCode
    const to = (searchParams.get('to') || 'EUR') as CurrencyCode
    const amount = parseFloat(searchParams.get('amount') || '0')

    if (!amount || amount <= 0) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Amount must be greater than 0' } },
        { status: 400 }
      )
    }

    if (!CURRENCIES[from]) {
      return NextResponse.json(
        { success: false, error: { code: 'INVALID_CURRENCY', message: `Currency '${from}' not supported` } },
        { status: 400 }
      )
    }

    if (!CURRENCIES[to]) {
      return NextResponse.json(
        { success: false, error: { code: 'INVALID_CURRENCY', message: `Currency '${to}' not supported` } },
        { status: 400 }
      )
    }

    // Get exchange rate from database
    const rateRecord = await prisma.exchangeRate.findUnique({
      where: {
        fromCurrency_toCurrency: {
          fromCurrency: from,
          toCurrency: to,
        },
      },
    })

    const rate = rateRecord?.rate ?? 1
    const convertedAmount = convertAmount(amount, from, to, rate)

    return NextResponse.json({
      success: true,
      data: {
        from,
        to,
        amount,
        convertedAmount,
        rate,
        timestamp: new Date().toISOString(),
        formatted: {
          from: `${CURRENCIES[from].symbol}${amount.toFixed(2)}`,
          to: `${CURRENCIES[to].symbol}${convertedAmount.toFixed(2)}`,
        },
      },
    })
  } catch (error) {
    console.error('Currency conversion error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to convert currency' } },
      { status: 500 }
    )
  }
}

// POST /api/currency/convert - Convert multiple amounts
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { amounts, from, to } = body

    if (!Array.isArray(amounts) || amounts.length === 0) {
      return NextResponse.json(
        { success: false, error: { code: 'VALIDATION_ERROR', message: 'Amounts array is required' } },
        { status: 400 }
      )
    }

    if (!CURRENCIES[from as CurrencyCode]) {
      return NextResponse.json(
        { success: false, error: { code: 'INVALID_CURRENCY', message: `Currency '${from}' not supported` } },
        { status: 400 }
      )
    }

    if (!CURRENCIES[to as CurrencyCode]) {
      return NextResponse.json(
        { success: false, error: { code: 'INVALID_CURRENCY', message: `Currency '${to}' not supported` } },
        { status: 400 }
      )
    }

    // Get exchange rate
    const rateRecord = await prisma.exchangeRate.findUnique({
      where: {
        fromCurrency_toCurrency: {
          fromCurrency: from,
          toCurrency: to,
        },
      },
    })

    const rate = rateRecord?.rate ?? 1

    const results = amounts.map(amount => {
      const convertedAmount = convertAmount(amount, from as CurrencyCode, to as CurrencyCode, rate)
      return {
        original: amount,
        converted: convertedAmount,
        formatted: {
          original: `${CURRENCIES[from as CurrencyCode].symbol}${amount.toFixed(2)}`,
          converted: `${CURRENCIES[to as CurrencyCode].symbol}${convertedAmount.toFixed(2)}`,
        },
      }
    })

    return NextResponse.json({
      success: true,
      data: {
        from,
        to,
        results,
        rate,
        timestamp: new Date().toISOString(),
      },
    })
  } catch (error) {
    console.error('Currency conversion error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to convert currency' } },
      { status: 500 }
    )
  }
}