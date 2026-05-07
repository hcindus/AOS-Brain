export type CurrencyCode = 'USD' | 'EUR' | 'JPY' | 'GBP'

export interface Currency {
  code: CurrencyCode
  symbol: string
  name: string
  rateToUsd: number
}

export const CURRENCIES: Record<CurrencyCode, Currency> = {
  USD: { code: 'USD', symbol: '$', name: 'US Dollar', rateToUsd: 1.0 },
  EUR: { code: 'EUR', symbol: '€', name: 'Euro', rateToUsd: 0.92 },
  JPY: { code: 'JPY', symbol: '¥', name: 'Japanese Yen', rateToUsd: 151.47 },
  GBP: { code: 'GBP', symbol: '£', name: 'British Pound', rateToUsd: 0.79 },
}

export function getRate(from: CurrencyCode, to: CurrencyCode): number {
  if (from === to) return 1
  const fromRate = CURRENCIES[from]?.rateToUsd ?? 1
  const toRate = CURRENCIES[to]?.rateToUsd ?? 1
  return toRate / fromRate
}

export function convert(
  amount: number,
  from: CurrencyCode,
  to: CurrencyCode
): number {
  if (from === to) return amount
  const rate = getRate(from, to)
  return amount * rate
}

export function convertToUsd(amount: number, from: CurrencyCode): number {
  return convert(amount, from, 'USD')
}

export function convertFromUsd(amount: number, to: CurrencyCode): number {
  return convert(amount, 'USD', to)
}

export function formatAmount(amount: number, currency: CurrencyCode): string {
  const curr = CURRENCIES[currency]
  if (!curr) return `$${amount.toFixed(2)}`
  
  const formatted = amount.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
  return `${curr.symbol}${formatted}`
}

export function getSupportedCurrencies(): Currency[] {
  return Object.values(CURRENCIES)
}
