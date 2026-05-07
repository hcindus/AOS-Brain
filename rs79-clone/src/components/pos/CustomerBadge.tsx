'use client'

import { Customer } from '@/types'
import { User, X, CreditCard, Gift } from 'lucide-react'
import { cn } from '@/lib/utils'

interface CustomerBadgeProps {
  customer: Customer
  onRemove: () => void
}

export function CustomerBadge({ customer, onRemove }: CustomerBadgeProps) {
  const hasPoints = customer.loyaltyPoints > 0
  const hasStoreCredit = customer.storeCredit && customer.storeCredit.balance > 0

  return (
    <div className="flex items-center gap-3 p-3 bg-primary/5 border border-primary/20 rounded-xl">
      <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
        <User size={20} className="text-primary" />
      </div>
      
      <div className="flex-1 min-w-0">
        <p className="font-medium text-text-primary truncate">{customer.name}</p>
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs text-text-secondary flex items-center gap-1">
            <CreditCard size={12} />
            {customer.loyaltyCardNo}
          </span>
          
          {hasPoints && (
            <span className={cn(
              "text-xs font-medium px-1.5 py-0.5 rounded-full",
              hasPoints ? "bg-amber-100 text-amber-700" : "bg-surface-tertiary text-text-muted"
            )}>
              {customer.loyaltyPoints} pts
            </span>
          )}
          
          {hasStoreCredit && (
            <span className="text-xs font-medium px-1.5 py-0.5 rounded-full bg-green-100 text-green-700 flex items-center gap-1">
              <Gift size={12} />
              ${customer.storeCredit!.balance.toFixed(2)} credit
            </span>
          )}
        </div>
      </div>
      
      <button
        onClick={onRemove}
        className="p-1.5 text-text-secondary hover:text-accent-danger hover:bg-red-50 rounded-lg transition-colors flex-shrink-0"
        title="Remove customer"
      >
        <X size={16} />
      </button>
    </div>
  )
}
