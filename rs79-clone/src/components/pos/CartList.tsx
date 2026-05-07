'use client'

import { CartItem } from '@/types'
import { CartItem as CartItemComponent } from './CartItem'
import { ShoppingCart } from 'lucide-react'

interface CartListProps {
  items: CartItem[]
  onUpdateQty: (itemId: string, qty: number) => void
  onRemoveItem: (itemId: string) => void
  currency: string
}

export function CartList({ items, onUpdateQty, onRemoveItem, currency }: CartListProps) {
  if (items.length === 0) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-text-muted p-8">
        <ShoppingCart size={64} className="mb-4 opacity-30" />
        <p className="text-lg font-medium mb-1">Your cart is empty</p>
        <p className="text-sm">Scan or click items to add</p>
      </div>
    )
  }

  return (
    <div className="h-full overflow-y-auto p-4">
      <div className="space-y-3">
        {items.map((item) => (
          <CartItemComponent
            key={item.itemId}
            item={item}
            onUpdateQty={onUpdateQty}
            onRemove={onRemoveItem}
            currency={currency}
          />
        ))}
      </div>
    </div>
  )
}
