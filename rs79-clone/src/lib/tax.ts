// Tax calculation utilities for POS
// Supports: tax-exclusive (US), tax-inclusive (EU/VAT), multi-rate, category-based

export type TaxMode = 'exclusive' | 'inclusive'

export interface TaxRate {
  name: string
  rate: number // 0.10 = 10%
  category?: string // Optional: apply to specific categories
  region?: string // Optional: apply to specific regions
}

export interface TaxConfig {
  mode: TaxMode
  rates: TaxRate[]
  defaultRate: number
  roundTo: number // 0.01 = cents
}

// Default config - can be overridden per-store
export const DEFAULT_TAX_CONFIG: TaxConfig = {
  mode: 'exclusive', // US-style: add tax at end
  rates: [
    { name: 'Standard', rate: 0.10 }, // 10% default
    { name: 'Reduced', rate: 0.05 },   // 5% for some categories
    { name: 'Zero', rate: 0 },         // 0% exempt
  ],
  defaultRate: 0.10,
  roundTo: 0.01,
}

// Get tax rate for an item (by category)
export function getTaxRate(
  category: string,
  config: TaxConfig = DEFAULT_TAX_CONFIG
): number {
  const categoryRate = config.rates.find(r => 
    r.category?.toLowerCase() === category.toLowerCase()
  )
  return categoryRate?.rate ?? config.defaultRate
}

// Calculate tax for a line item
export interface LineTaxResult {
  netPrice: number      // Price without tax
  grossPrice: number    // Price with tax included
  taxPerUnit: number     // Tax amount per unit
  lineTax: number       // Total tax for qty
  lineTotal: number     // Total with tax
  rate: number          // Applied rate
}

export function calculateLineTax(
  price: number,
  qty: number,
  rate: number,
  mode: TaxMode
): LineTaxResult {
  if (mode === 'inclusive') {
    // EU/VAT style: price includes tax
    // $110 inclusive @ 10% = $100 net + $10 tax
    const netPrice = price / (1 + rate)
    const taxPerUnit = price - netPrice
    const lineTax = round(taxPerUnit * qty, 0.01)
    const lineTotal = round(price * qty, 0.01)
    
    return {
      netPrice: round(netPrice, 0.01),
      grossPrice: price,
      taxPerUnit: round(taxPerUnit, 0.01),
      lineTax,
      lineTotal,
      rate
    }
  } else {
    // US style: add tax at end
    // $100 + 10% = $110 total
    const taxPerUnit = price * rate
    const lineTax = round(taxPerUnit * qty, 0.01)
    const lineTotal = round((price * qty) + lineTax, 0.01)
    
    return {
      netPrice: price,
      grossPrice: round(price * (1 + rate), 0.01),
      taxPerUnit: round(taxPerUnit, 0.01),
      lineTax,
      lineTotal,
      rate
    }
  }
}

// Calculate totals for a cart
export interface CartTaxResult {
  subtotal: number      // Net amount (before tax)
  tax: number           // Total tax
  total: number         // Final amount
  mode: TaxMode
  breakdown: {
    rate: number
    name: string
    amount: number
  }[]
}

export interface CartItemWithTax {
  itemId: string
  name: string
  price: number // Original price (net for exclusive, gross for inclusive)
  qty: number
  category: string
  lineTax: LineTaxResult
}

export function calculateCartTax(
  items: { price: number; qty: number; category: string }[],
  config: TaxConfig = DEFAULT_TAX_CONFIG
): CartTaxResult {
  const breakdown = new Map<number, number>()
  let subtotal = 0
  let totalTax = 0
  
  for (const item of items) {
    const rate = getTaxRate(item.category, config)
    const lineResult = calculateLineTax(item.price, item.qty, rate, config.mode)
    
    subtotal += config.mode === 'inclusive' 
      ? lineResult.netPrice * item.qty 
      : item.price * item.qty
    totalTax += lineResult.lineTax
    
    // Track by rate
    const current = breakdown.get(rate) ?? 0
    breakdown.set(rate, current + lineResult.lineTax)
  }
  
  const total = config.mode === 'inclusive'
    ? items.reduce((sum, item) => sum + (item.price * item.qty), 0)
    : round(subtotal + totalTax, 0.01)
  
  return {
    subtotal: round(subtotal, 0.01),
    tax: round(totalTax, 0.01),
    total: round(total, 0.01),
    mode: config.mode,
    breakdown: Array.from(breakdown.entries()).map(([rate, amount]) => ({
      rate,
      name: `${(rate * 100).toFixed(0)}%`,
      amount: round(amount, 0.01)
    }))
  }
}

// Helper: Round to nearest increment
function round(value: number, precision: number): number {
  return Math.round(value / precision) * precision
}

// Get display label for tax mode
export function getTaxModeLabel(mode: TaxMode): string {
  return mode === 'inclusive' ? 'incl. tax' : '+ tax'
}

// Format price with tax indicator
export function formatPriceWithTax(
  price: number, 
  mode: TaxMode, 
  currency: string = '$'
): string {
  const suffix = mode === 'inclusive' ? ' (incl. tax)' : ''
  return `${currency}${price.toFixed(2)}${suffix}`
}

// Parse tax config from environment or JSON
export function parseTaxConfig(envConfig?: string): TaxConfig {
  if (!envConfig) return DEFAULT_TAX_CONFIG
  
  try {
    const parsed = JSON.parse(envConfig)
    return {
      ...DEFAULT_TAX_CONFIG,
      ...parsed
    }
  } catch {
    return DEFAULT_TAX_CONFIG
  }
}

// Common tax configurations
export const TAX_CONFIGS = {
  us: DEFAULT_TAX_CONFIG,
  uk: {
    mode: 'inclusive' as TaxMode,
    rates: [
      { name: 'Standard', rate: 0.20 },
      { name: 'Reduced', rate: 0.05, category: 'energy' },
      { name: 'Zero', rate: 0, category: 'food' },
    ],
    defaultRate: 0.20,
    roundTo: 0.01,
  },
  eu: {
    mode: 'inclusive' as TaxMode,
    rates: [
      { name: 'Standard', rate: 0.21 },
      { name: 'Reduced', rate: 0.09 },
      { name: 'Zero', rate: 0 },
    ],
    defaultRate: 0.21,
    roundTo: 0.01,
  },
}