'use client'

import { useState, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { CategorySidebar } from '@/components/pos/CategorySidebar'
import { ItemGrid } from '@/components/pos/ItemGrid'
import { CartPanel } from '@/components/pos/CartPanel'
import type { Item, CartItem } from '@/types'

interface Clerk {
  id: string
  name: string
  role: string
}

export default function RegisterPage() {
  const router = useRouter()
  const [items, setItems] = useState<Item[]>([])
  const [cart, setCart] = useState<CartItem[]>([])
  const [categories, setCategories] = useState<{ id: string; name: string; icon: string }[]>([])
  const [activeCategory, setActiveCategory] = useState<string | null>(null)
  const [clerk, setClerk] = useState<Clerk | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Calculate totals
  const subtotal = cart.reduce((sum, item) => sum + item.lineTotal, 0)
  const tax = subtotal * 0.10 // 10% tax
  const total = subtotal + tax

  // Fetch items and verify session
  useEffect(() => {
    const loadData = async () => {
      try {
        // Get items
        const itemsRes = await fetch('/api/items?limit=100')
        const itemsData = await itemsRes.json()

        if (itemsData.success) {
          setItems(itemsData.data)
          
          // Extract unique categories
          const categoryMap = new Map<string, { id: string; name: string; icon: string }>()
          itemsData.data.forEach((item: Item) => {
            if (!categoryMap.has(item.category)) {
              categoryMap.set(item.category, {
                id: item.category,
                name: item.category.charAt(0).toUpperCase() + item.category.slice(1),
                icon: getCategoryIcon(item.category),
              })
            }
          })
          setCategories(Array.from(categoryMap.values()))
        }

        // Get session clerk info from cookie
        const sessionResponse = await fetch('/api/clerks')
        const sessionData = await sessionResponse.json()
        
        // For MVP, default to first active clerk or Admin
        setClerk({ id: 'admin', name: 'Admin', role: 'Admin' })
      } catch (error) {
        console.error('Failed to load data:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadData()
  }, [])

  const getCategoryIcon = (category: string): string => {
    const iconMap: Record<string, string> = {
      drinks: 'Coffee',
      bakery: 'Cake',
      food: 'Utensils',
      dessert: 'IceCream',
      retail: 'ShoppingBag',
      alcohol: 'Beer',
      general: 'Package',
    }
    return iconMap[category] || 'Grid3X3'
  }

  const filteredItems = activeCategory
    ? items.filter((item) => item.category === activeCategory)
    : items

  const handleAddToCart = useCallback((item: Item) => {
    setCart((prev) => {
      const existing = prev.find((i) => i.itemId === item.id)
      if (existing) {
        return prev.map((i) =>
          i.itemId === item.id
            ? { ...i, qty: i.qty + 1, lineTotal: i.price * (i.qty + 1) }
            : i
        )
      }
      return [
        ...prev,
        {
          itemId: item.id,
          name: item.name,
          price: item.price,
          qty: 1,
          lineTotal: item.price,
        },
      ]
    })
  }, [])

  const handleUpdateQty = useCallback((itemId: string, qty: number) => {
    if (qty <= 0) {
      setCart((prev) => prev.filter((i) => i.itemId !== itemId))
    } else {
      setCart((prev) =>
        prev.map((i) =>
          i.itemId === itemId
            ? { ...i, qty, lineTotal: i.price * qty }
            : i
        )
      )
    }
  }, [])

  const handleRemoveItem = useCallback((itemId: string) => {
    setCart((prev) => prev.filter((i) => i.itemId !== itemId))
  }, [])

  const handleClearCart = useCallback(() => {
    setCart([])
  }, [])

  const handleCheckout = useCallback(() => {
    if (cart.length === 0) return
    
    // For MVP, just create a simple order
    const orderData = {
      items: cart.map((item) => ({
        itemId: item.itemId,
        name: item.name,
        price: item.price,
        qty: item.qty,
      })),
      payments: [
        {
          type: 'cash',
          amount: total,
          tendered: total,
        },
      ],
    }

    fetch('/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(orderData),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          alert(`Order #${data.data.transactionNo} created successfully!`)
          handleClearCart()
        } else {
          alert('Failed to create order: ' + data.error?.message)
        }
      })
      .catch((err) => {
        console.error('Checkout error:', err)
        alert('Checkout failed')
      })
  }, [cart, total])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-surface-secondary flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-text-secondary">Loading POS...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-screen flex overflow-hidden bg-surface-secondary">
      {/* Left Section: Categories + Items */}
      <div className="flex flex-1 min-w-0">
        <CategorySidebar
          categories={categories}
          activeCategory={activeCategory}
          onSelectCategory={setActiveCategory}
        />
        <div className="flex-1 flex flex-col">
          {/* Header */}
          <div className="h-16 bg-white border-b border-surface-tertiary flex items-center justify-between px-6">
            <h1 className="text-xl font-bold text-text-primary">RS-79 Register</h1>
            <div className="flex items-center gap-4">
              <span className="text-sm text-text-secondary">
                Clerk: <span className="font-medium text-text-primary">{clerk?.name || 'Unknown'}</span>
              </span>
              <button
                onClick={() => router.push('/login')}
                className="text-sm text-primary hover:text-primary-dark font-medium"
              >
                Logout
              </button>
            </div>
          </div>
          {/* Items Grid */}
          <ItemGrid
            items={filteredItems}
            onAddToCart={handleAddToCart}
            currency="USD"
          />
        </div>
      </div>

      {/* Right Section: Cart */}
      <div className="w-[420px] flex-shrink-0">
        <CartPanel
          items={cart}
          onUpdateQty={handleUpdateQty}
          onRemoveItem={handleRemoveItem}
          onClearCart={handleClearCart}
          onCheckout={handleCheckout}
          clerkName={clerk?.name || 'Unknown'}
          subtotal={subtotal}
          tax={tax}
          total={total}
          currency="USD"
        />
      </div>
    </div>
  )
}
