'use client'

import { Minus, Plus } from 'lucide-react'

interface QuantityAdjusterProps {
  qty: number
  onIncrease: () => void
  onDecrease: () => void
  min?: number
  max?: number
}

export function QuantityAdjuster({
  qty,
  onIncrease,
  onDecrease,
  min = 0,
  max = 99,
}: QuantityAdjusterProps) {
  const canDecrease = qty > min
  const canIncrease = qty < max

  return (
    <div className="flex items-center gap-1">
      <button
        onClick={onDecrease}
        disabled={!canDecrease}
        className="w-7 h-7 flex items-center justify-center rounded-md bg-surface-secondary text-text-secondary hover:bg-surface-tertiary hover:text-text-primary disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        aria-label="Decrease quantity"
      >
        <Minus size={14} />
      </button>
      
      <span className="w-8 text-center font-semibold text-text-primary">{qty}</span>
      
      <button
        onClick={onIncrease}
        disabled={!canIncrease}
        className="w-7 h-7 flex items-center justify-center rounded-md bg-surface-secondary text-text-secondary hover:bg-surface-tertiary hover:text-text-primary disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        aria-label="Increase quantity"
      >
        <Plus size={14} />
      </button>
    </div>
  )
}
