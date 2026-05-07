'use client'

import { cn } from '@/lib/utils'
import {
  LayoutGrid,
  UtensilsCrossed,
  Coffee,
  ShoppingBag,
  Cake,
  Beer,
  IceCream,
  Package,
  Grid3X3,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react'

interface Category {
  id: string
  name: string
  icon?: string
}

interface CategorySidebarProps {
  categories: Category[]
  activeCategory: string | null
  onSelectCategory: (categoryId: string | null) => void
  isCollapsed?: boolean
  onToggleCollapse?: () => void
}

const iconMap: Record<string, React.ComponentType<{ size?: number }>> = {
  'all': LayoutGrid,
  'food': UtensilsCrossed,
  'drinks': Coffee,
  'bakery': Cake,
  'alcohol': Beer,
  'dessert': IceCream,
  'merch': ShoppingBag,
  'retail': ShoppingBag,
  'general': Package,
}

function getIcon(iconName?: string): React.ComponentType<{ size?: number }> {
  return iconName && iconMap[iconName] ? iconMap[iconName] : Grid3X3
}

export function CategorySidebar({
  categories,
  activeCategory,
  onSelectCategory,
  isCollapsed = false,
  onToggleCollapse,
}: CategorySidebarProps) {
  const allCategories = [
    { id: null, name: 'All Items', icon: 'all' },
    ...categories
  ]

  if (isCollapsed) {
    return (
      <div className="w-16 bg-white border-r border-surface-tertiary flex flex-col h-full">
        <div className="flex-1 overflow-y-auto py-2 space-y-1 px-2">
          {allCategories.map((cat) => {
            const Icon = getIcon(cat.icon)
            const isActive = activeCategory === cat.id
            return (
              <button
                key={cat.id ?? 'all'}
                onClick={() => onSelectCategory(cat.id)}
                className={cn(
                  'w-full p-3 rounded-xl transition-all duration-150 flex justify-center',
                  isActive
                    ? 'bg-primary text-white shadow-md'
                    : 'text-text-secondary hover:bg-surface-secondary'
                )}
                title={cat.name}
              >
                <Icon size={20} />
              </button>
            )
          })}
        </div>
        
        {onToggleCollapse && (
          <div className="p-3 border-t border-surface-tertiary">
            <button
              onClick={onToggleCollapse}
              className="w-full p-2 text-text-secondary hover:text-text-primary hover:bg-surface-secondary rounded-lg transition-colors"
              title="Expand sidebar"
            >
              <ChevronRight size={20} />
            </button>
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="w-56 bg-white border-r border-surface-tertiary flex flex-col h-full">
      <div className="p-4 border-b border-surface-tertiary">
        <h2 className="font-bold text-text-primary">Categories</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto p-3 space-y-1">
        {allCategories.map((cat) => {
          const Icon = getIcon(cat.icon)
          const isActive = activeCategory === cat.id
          return (
            <button
              key={cat.id ?? 'all'}
              onClick={() => onSelectCategory(cat.id)}
              className={cn(
                'w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all duration-150',
                isActive
                  ? 'bg-primary text-white shadow-md'
                  : 'text-text-secondary hover:bg-surface-secondary'
              )}
            >
              <Icon size={20} />
              <span className="truncate">{cat.name}</span>
            </button>
          )
        })}
      </div>
      
      {onToggleCollapse && (
        <div className="p-3 border-t border-surface-tertiary">
          <button
            onClick={onToggleCollapse}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 text-text-secondary hover:text-text-primary hover:bg-surface-secondary rounded-xl transition-colors text-sm"
          >
            <ChevronLeft size={16} />
            Collapse
          </button>
        </div>
      )}
    </div>
  )
}
