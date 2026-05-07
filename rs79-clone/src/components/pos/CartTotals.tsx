'use client'

interface CartTotalsProps {
  subtotal: number
  tax: number
  total: number
  currency: string
}

export function CartTotals({ subtotal, tax, total, currency }: CartTotalsProps) {
  return (
    <div className="p-4 bg-surface-secondary">
      <div className="space-y-2">
        <div className="flex justify-between text-sm text-text-secondary">
          <span>Subtotal</span>
          <span>{currency}{subtotal.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-sm text-text-secondary">
          <span>Tax (10%)</span>
          <span>{currency}{tax.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-lg font-bold text-text-primary pt-2 border-t border-surface-tertiary">
          <span>Total</span>
          <span className="text-accent-success">{currency}{total.toFixed(2)}</span>
        </div>
      </div>
    </div>
  )
}
