import { prisma } from './prisma'
import type { CurrencyCode } from '@/types'

export const CURRENCIES: Record<CurrencyCode, { symbol: string; name: string }> = {
  USD: { symbol: '$', name: 'US Dollar' },
  EUR: { symbol: '€', name: 'Euro' },
  JPY: { symbol: '¥', name: 'Japanese Yen' },
  GBP: { symbol: '£', name: 'British Pound' },
}

export const BASE_CURRENCY: CurrencyCode = 'USD'

export async function getExchangeRate(from: CurrencyCode, to: CurrencyCode): Promise<number> {
  if (from === to) return 1
  
  const rate = await prisma.exchangeRate.findUnique({
    where: {
      fromCurrency_toCurrency: {
        fromCurrency: from,
        toCurrency: to,
      },
    },
  })
  
  return rate?.rate ?? 1
}

export function convertAmount(amount: number, from: CurrencyCode, to: CurrencyCode, rate: number): number {
  if (from === to) return amount
  return amount * rate
}

export function formatCurrency(amount: number, currency: CurrencyCode): string {
  const symbol = CURRENCIES[currency]?.symbol ?? '$'
  
  if (currency === 'JPY') {
    return `${symbol}${Math.round(amount).toLocaleString()}`
  }
  
  return `${symbol}${amount.toFixed(2)}`
}

export function formatCurrencyRaw(amount: number, currency: CurrencyCode): string {
  if (currency === 'JPY') {
    return Math.round(amount).toString()
  }
  return amount.toFixed(2)
}

export function parseCurrencyInput(input: string, currency: CurrencyCode): number {
  const value = parseFloat(input.replace(/[^0-9.]/g, ''))
  if (isNaN(value)) return 0
  
  if (currency === 'JPY') {
    return Math.round(value)
  }
  
  return Math.round(value * 100) / 100
}

export function getSupportedCurrencies(): CurrencyCode[] {
  return Object.keys(CURRENCIES) as CurrencyCode[]
}
