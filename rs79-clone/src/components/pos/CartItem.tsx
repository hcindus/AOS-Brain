'use client'

import { CartItem as CartItemType } from '@/types'
import { QuantityAdjuster } from './QuantityAdjuster'
import { X } from 'lucide-react'

interface CartItemProps {
  item: CartItemType
  onUpdateQty: (itemId: string, qty: number) => void
  onRemove: (itemId: string) => void
  currency: string
}

export function CartItem({ item, onUpdateQty, onRemove, currency }: CartItemProps) {
  return (
    <div className="group flex items-center gap-3 p-3 bg-white border border-surface-tertiary rounded-xl hover:border-primary/30 transition-colors">
      {/* Item Info */}
      <div className="flex-1 min-w-0">
        <p className="font-medium text-text-primary truncate">{item.name}</p>
        <p className="text-sm text-text-secondary">
          {currency}{item.price.toFixed(2)} × {item.qty}
        </p>
      </div>

      {/* Quantity */}
      <div className="flex-shrink-0">
        <QuantityAdjuster
          qty={item.qty}
          onIncrease={() => onUpdateQty(item.itemId, item.qty + 1)}
          onDecrease={() => onUpdateQty(item.itemId, item.qty - 1)}
          min={1}
        />
      </div>

      {/* Line Total */}
      <div className="flex-shrink-0 text-right min-w-[60px]">
        <p className="font-bold text-text-primary">
          {currency}{item.lineTotal.toFixed(2)}
        </p>
      </div>

      {/* Remove Button */}
      <button
        onClick={() => onRemove(item.itemId)}
        className="flex-shrink-0 p-1.5 text-text-muted hover:text-accent-danger opacity-0 group-hover:opacity-100 transition-opacity"
        title="Remove item"
      >
        <X size={16} />
      </button>
    </div>
  )
}
