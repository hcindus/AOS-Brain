'use client'

import { cn } from '@/lib/utils'
import { LayoutGrid, Coffee, ShoppingBag, Utensils, Cake, Beer, IceCream, Package, Grid3X3 } from 'lucide-react'

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

const iconMap: Record<string, React.ReactNode> = {
  'all': <LayoutGrid size={20} />,
  'food': <Utensils size={20} />,
  'drinks': <Coffee size={20} />,
  'bakery': <Cake size={20} />,
  'alcohol': <Beer size={20} />,
  'dessert': <IceCream size={20} />,
  'retail': <ShoppingBag size={20} />,
  'general': <Package size={20} />,
}

function getIcon(iconName?: string) {
  return iconName && iconMap[iconName] ? iconMap[iconName] : <Grid3X3 size={20} />
}

export function CategorySidebar({
  categories,
  activeCategory,
  onSelectCategory,
  isCollapsed = false,
  onToggleCollapse,
}: CategorySidebarProps) {
  if (isCollapsed) {
    return (
      <div className="w-16 bg-white border-r border-surface-tertiary flex flex-col">
        <button
          onClick={() => onSelectCategory(null)}
          className={cn(
            'p-3 m-2 rounded-xl transition-all duration-150',
            activeCategory === null
              ? 'bg-primary text-white shadow-md'
              : 'text-text-secondary hover:bg-surface-secondary'
          )}
        >
          {getIcon('all')}
        </button>
        <div className="flex-1 overflow-y-auto py-2 space-y-1 px-2">
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => onSelectCategory(cat.id)}
              className={cn(
                'w-full p-3 rounded-xl transition-all duration-150 flex justify-center',
                activeCategory === cat.id
                  ? 'bg-primary text-white shadow-md'
                  : 'text-text-secondary hover:bg-surface-secondary'
              )}
              title={cat.name}
            >
              {getIcon(cat.icon)}
            </button>
          ))}
        </div>
        
        {onToggleCollapse && (
          <button
            onClick={onToggleCollapse}
            className="p-3 m-2 text-text-secondary hover:text-text-primary hover:bg-surface-secondary rounded-xl transition-colors"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M9 18l6-6-6-6" />
            </svg>
          </button>
        )}
      </div>
    )
  }

  return (
    <div className="w-56 bg-white border-r border-surface-tertiary flex flex-col">
      <div className="p-4 border-b border-surface-tertiary">
        <h2 className="font-bold text-text-primary">Categories</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto p-3 space-y-1">
        <button
          onClick={() => onSelectCategory(null)}
          className={cn(
            'w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all duration-150',
            activeCategory === null
              ? 'bg-primary text-white shadow-md'
              : 'text-text-secondary hover:bg-surface-secondary'
          )}
        >
          {getIcon('all')}
          <span>All Items</span>
        </button>
        
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => onSelectCategory(cat.id)}
            className={cn(
              'w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all duration-150',
              activeCategory === cat.id
                ? 'bg-primary text-white shadow-md'
                : 'text-text-secondary hover:bg-surface-secondary'
            )}
          >
            {getIcon(cat.icon)}
            <span className="truncate">{cat.name}</span>
          </button>
        ))}
      </div>
      
      {onToggleCollapse && (
        <div className="p-3 border-t border-surface-tertiary">
          <button
            onClick={onToggleCollapse}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 text-text-secondary hover:text-text-primary hover:bg-surface-secondary rounded-xl transition-colors text-sm"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M11 17l-5-5 5-5M18 17l-5-5 5-5" />
            </svg>
            Collapse
          </button>
        </div>
      )}
    </div>
  )
}
