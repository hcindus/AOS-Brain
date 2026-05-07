'use client'

import { useState, useEffect } from 'react'
import { cn } from '@/lib/utils'
import { ShoppingCart, CreditCard, X, ChevronUp, ChevronDown, User, Trash2 } from 'lucide-react'
import type { CartItem, Customer } from '@/types'

interface CartPanelProps {
  items: CartItem[]
  onUpdateQty: (itemId: string, qty: number) => void
  onRemoveItem: (itemId: string) => void
  onClearCart: () => void
  onCheckout: () => void
  onHoldOrder?: () => void
  onAddCustomer?: () => void
  customer?: Customer | null
  clerkName: string
  subtotal: number
  tax: number
  total: number
  currency: string
  isCollapsed?: boolean
  onToggleCollapse?: () => void
}

export function CartPanel({
  items,
  onUpdateQty,
  onRemoveItem,
  onClearCart,
  onCheckout,
  onHoldOrder,
  onAddCustomer,
  customer,
  clerkName,
  subtotal,
  tax,
  total,
  currency,
  isCollapsed = false,
  onToggleCollapse,
}: CartPanelProps) {
  const itemCount = items.reduce((sum, item) => sum + item.qty, 0)

  if (isCollapsed) {
    return (
      <div className="w-16 bg-white border-l border-surface-tertiary flex flex-col items-center py-4">
        <button
          onClick={onToggleCollapse}
          className="p-2 rounded-lg bg-primary/10 text-primary hover:bg-primary/20 transition-colors"
        >
          <ShoppingCart size={20} />
          {itemCount > 0 && (
            <span className="absolute -top-1 -right-1 w-5 h-5 bg-accent-danger text-white text-xs font-bold rounded-full flex items-center justify-center">
              {itemCount}
            </span>
          )}
        </button>
      </div>
    )
  }

  return (
    <div className="w-full max-w-md bg-white border-l border-surface-tertiary flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-surface-tertiary">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-lg">
            <ShoppingCart size={20} className="text-primary" />
          </div>
          <div>
            <h3 className="font-bold text-text-primary">Cart</h3>
            <p className="text-xs text-text-secondary">{itemCount} items</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {onToggleCollapse && (
            <button
              onClick={onToggleCollapse}
              className="p-2 text-text-secondary hover:text-text-primary hover:bg-surface-secondary rounded-lg transition-colors"
            >
              <ChevronUp size={18} />
            </button>
          )}
          <button
            onClick={onClearCart}
            disabled={items.length === 0}
            className="p-2 text-text-secondary hover:text-accent-danger hover:bg-red-50 rounded-lg transition-colors disabled:opacity-40"
          >
            <Trash2 size={18} />
          </button>
        </div>
      </div>

      {/* Clerk Info */}
      <div className="px-4 py-2 bg-surface-secondary border-b border-surface-tertiary flex items-center gap-2 text-sm text-text-secondary">
        <User size={14} />
        <span>Clerk: <span className="font-medium text-text-primary">{clerkName}</span></span>
      </div>

      {/* Customer Section */}
      <div className="px-4 py-3 border-b border-surface-tertiary">
        {customer ? (
          <div className="flex items-center justify-between p-3 bg-surface-secondary rounded-lg">
            <div>
              <p className="font-medium text-text-primary">{customer.name}</p>
              <p className="text-xs text-text-secondary">
                {customer.loyaltyCardNo} • {customer.loyaltyPoints} pts
              </p>
            </div>
            <button
              onClick={() => {}}
              className="p-1.5 text-text-secondary hover:text-accent-danger"
            >
              <X size={16} />
            </button>
          </div>
        ) : (
          <button
            onClick={onAddCustomer}
            className="w-full py-2.5 px-4 border-2 border-dashed border-surface-tertiary rounded-lg text-text-secondary hover:border-primary hover:text-primary transition-colors text-sm font-medium"
          >
            + Add Customer
          </button>
        )}
      </div>

      {/* Cart Items */}
      <div className="flex-1 overflow-y-auto p-4">
        {items.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-text-muted">
            <ShoppingCart size={48} className="mb-4 opacity-30" />
            <p className="text-lg font-medium">Your cart is empty</p>
            <p className="text-sm">Scan or click items to add</p>
          </div>
        ) : (
          <div className="space-y-3">
            {items.map((item) => (
              <div key={item.itemId} className="cart-item group">
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-text-primary truncate">{item.name}</p>
                  <p className="text-sm text-text-secondary">
                    {currency} {item.price.toFixed(2)} × {item.qty}
                  </p>
                </div>
                
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => onUpdateQty(item.itemId, Math.max(0, item.qty - 1))}
                    className="w-7 h-7 flex items-center justify-center rounded-md bg-surface-secondary text-text-secondary hover:bg-surface-tertiary hover:text-text-primary transition-colors"
                  >
                    −
                  </button>
                  <span className="w-8 text-center font-semibold text-text-primary">{item.qty}</span>
                  <button
                    onClick={() => onUpdateQty(item.itemId, item.qty + 1)}
                    className="w-7 h-7 flex items-center justify-center rounded-md bg-surface-secondary text-text-secondary hover:bg-surface-tertiary hover:text-text-primary transition-colors"
                  >
                    +
                  </button>
                  <button
                    onClick={() => onRemoveItem(item.itemId)}
                    className="p-1.5 text-text-muted hover:text-accent-danger opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <X size={16} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Totals */}
      <div className="p-4 border-t border-surface-tertiary bg-surface-secondary">
        <div className="space-y-2 mb-4">
          <div className="flex justify-between text-text-secondary">
            <span>Subtotal</span>
            <span>{currency} {subtotal.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-text-secondary">
            <span>Tax (10%)</span>
            <span>{currency} {tax.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-xl font-bold text-text-primary pt-2 border-t border-surface-tertiary">
            <span>Total</span>
            <span>{currency} {total.toFixed(2)}</span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          {onHoldOrder && (
            <button
              onClick={onHoldOrder}
              disabled={items.length === 0}
              className="py-3 px-4 rounded-xl font-semibold bg-surface-tertiary text-text-primary hover:bg-surface-tertiary/80 disabled:opacity-40 transition-colors"
            >
              Hold Order
            </button>
          )}
          <button
            onClick={onCheckout}
            disabled={items.length === 0}
            className={cn(
              'py-3 px-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all duration-150',
              items.length > 0
                ? 'bg-accent-success text-white hover:bg-green-600 shadow-lg shadow-green-500/25 active:scale-[0.98]'
                : 'bg-surface-tertiary text-text-muted cursor-not-allowed'
            )}
          >
            <CreditCard size={18} />
            Pay
          </button>
        </div>
      </div>
    </div>
  )
}
