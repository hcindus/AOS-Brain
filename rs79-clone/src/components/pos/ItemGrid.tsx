'use client'

import { cn } from '@/lib/utils'
import { Package, DollarSign, Eye } from 'lucide-react'
import type { Item } from '@/types'

interface ItemGridProps {
  items: Item[]
  onAddToCart: (item: Item) => void
  onItemClick?: (item: Item) => void
  currency: string
  taxMode?: 'exclusive' | 'inclusive'
}

export function ItemGrid({ items, onAddToCart, onItemClick, currency, taxMode = 'exclusive' }: ItemGridProps) {
  if (items.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-text-muted p-8">
        <Package size={64} className="mb-4 opacity-30" />
        <p className="text-xl font-medium mb-1">No items found</p>
        <p className="text-sm">Try selecting a different category</p>
      </div>
    )
  }

  return (
    <div className="flex-1 overflow-y-auto p-4">
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-3">
        {items.map((item) => (
          <div
            key={item.id}
            className={cn(
              'group relative flex flex-col',
              'bg-white border border-surface-tertiary rounded-xl',
              'transition-all duration-150',
              'hover:border-primary/40 hover:shadow-soft'
            )}
          >
            {/* Quick View Button */}
            {onItemClick && (
              <button
                onClick={() => onItemClick(item)}
                className="absolute top-2 right-2 p-2 bg-white/90 backdrop-blur-sm rounded-lg text-text-secondary opacity-0 group-hover:opacity-100 transition-opacity hover:text-primary shadow-sm z-10"
                title="Quick view"
              >
                <Eye size={16} />
              </button>
            )}

            {/* Item Image / Click Area */}
            <button
              onClick={() => onAddToCart(item)}
              className="flex-1 flex flex-col items-center p-4 active:scale-[0.98] transition-transform"
            >
              {/* Placeholder for item image */}
              <div className="w-full aspect-square mb-3 bg-surface-secondary rounded-lg flex items-center justify-center group-hover:bg-primary/5 transition-colors">
                <Package size={32} className="text-text-muted group-hover:text-primary/40" />
              </div>
              
              {/* Item details */}
              <div className="w-full text-center">
                <p className="font-semibold text-text-primary text-sm line-clamp-2 min-h-[2.5rem]">
                  {item.name}
                </p>
                <div className="flex items-center justify-center gap-1 mt-2">
                  <span className="font-bold text-accent-success">
                    {currency}{item.price.toFixed(2)}
                  </span>
                  {taxMode === 'inclusive' && (
                    <span className="text-xs text-text-muted">inc.</span>
                  )}
                </div>
                <p className="text-xs text-text-muted mt-1">{item.sku}</p>
              </div>
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
