'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import type { Item, CartItem, CurrencyCode, Customer } from '@/types'
import { CURRENCIES } from '@/lib/currency'

export default function RegisterPage() {
  const [items, setItems] = useState<Item[]>([])
  const [categories, setCategories] = useState<string[]>([])
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [cart, setCart] = useState<CartItem[]>([])
  const [currency, setCurrency] = useState<CurrencyCode>('USD')
  const [customer, setCustomer] = useState<Customer | null>(null)
  const [showPayment, setShowPayment] = useState(false)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    // Check session
    fetch('/api/auth/session')
      .then(res => {
        if (!res.ok) {
          router.push('/login')
        } else {
          loadItems()
        }
      })
  }, [router])

  const loadItems = async () => {
    try {
      const res = await fetch('/api/items')
      const data = await res.json()
      if (data.success) {
        setItems(data.data.items)
        setCategories(data.data.categories)
        setSelectedCategory(data.data.categories[0] || null)
      }
    } finally {
      setLoading(false)
    }
  }

  const filteredItems = items.filter(item => {
    const matchesCategory = selectedCategory ? item.category === selectedCategory : true
    const matchesSearch = searchQuery
      ? item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.sku.toLowerCase().includes(searchQuery.toLowerCase())
      : true
    return matchesCategory && matchesSearch && item.active
  })

  const addToCart = (item: Item) => {
    setCart(prev => {
      const existing = prev.find(ci => ci.item.id === item.id)
      if (existing) {
        return prev.map(ci =>
          ci.item.id === item.id ? { ...ci, qty: ci.qty + 1 } : ci
        )
      }
      return [...prev, { item, qty: 1 }]
    })
  }

  const updateQty = (itemId: string, delta: number) => {
    setCart(prev => {
      return prev.map(ci => {
        if (ci.item.id === itemId) {
          const newQty = Math.max(0, ci.qty + delta)
          return { ...ci, qty: newQty }
        }
        return ci
      }).filter(ci => ci.qty > 0)
    })
  }

  const removeFromCart = (itemId: string) => {
    setCart(prev => prev.filter(ci => ci.item.id !== itemId))
  }

  const subtotal = cart.reduce((sum, ci) => sum + ci.item.price * ci.qty, 0)
  const tax = subtotal * 0.08
  const total = subtotal + tax

  const symbol = CURRENCIES[currency]?.symbol || '$'

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-900 flex">
      {/* Left Panel: Items */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="h-16 bg-gray-800 border-b border-gray-700 flex items-center px-4 justify-between">
          <div className="flex items-center gap-4">
            <select
              value={currency}
              onChange={(e) => setCurrency(e.target.value as CurrencyCode)}
              className="bg-gray-700 text-white px-3 py-2 rounded-lg border border-gray-600"
            >
              <option value="USD">USD ($)</option>
              <option value="EUR">EUR (€)</option>
              <option value="JPY">JPY (¥)</option>
              <option value="GBP">GBP (£)</option>
            </select>
            <input
              type="text"
              placeholder="Search items..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-gray-700 text-white px-4 py-2 rounded-lg border border-gray-600 w-64"
            />
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={() => setShowPayment(true)}
              disabled={cart.length === 0}
              className="bg-green-600 hover:bg-green-700 disabled:bg-gray-700 disabled:text-gray-500 text-white px-6 py-2 rounded-lg font-semibold transition-colors"
            >
              Pay {symbol}{total.toFixed(2)}
            </button>
          </div>
        </div>

        {/* Categories */}
        <div className="h-12 bg-gray-800 border-b border-gray-700 flex items-center px-4 gap-2 overflow-x-auto">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-4 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
                selectedCategory === cat
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {cat}
            </button>
          ))}
          <button
            onClick={() => setSelectedCategory(null)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
              selectedCategory === null
                ? 'bg-blue-600 text-white'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
          >
            All
          </button>
        </div>

        {/* Items Grid */}
        <div className="flex-1 p-4 overflow-auto">
          <div className="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3">
            {filteredItems.map((item) => (
              <button
                key={item.id}
                onClick={() => addToCart(item)}
                className="bg-gray-800 hover:bg-gray-700 border border-gray-700 rounded-xl p-4 text-left transition-colors group"
              >
                <p className="text-white font-medium truncate group-hover:text-blue-400">{item.name}</p>
                <p className="text-gray-400 text-sm mt-1">{item.sku}</p>
                <p className="text-green-400 font-semibold mt-2">
                  {symbol}{item.price.toFixed(2)}
                </p>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Right Panel: Cart */}
      <div className="w-96 bg-gray-800 border-l border-gray-700 flex flex-col">
        {/* Cart Header */}
        <div className="h-16 border-b border-gray-700 flex items-center px-4 justify-between">
          <h2 className="text-white font-semibold">Current Order</h2>
          <button
            onClick={() => setCart([])}
            disabled={cart.length === 0}
            className="text-red-400 hover:text-red-300 text-sm disabled:text-gray-600"
          >
            Clear
          </button>
        </div>

        {/* Cart Items */}
        <div className="flex-1 overflow-auto p-4">
          {cart.length === 0 ? (
            <div className="text-center text-gray-500 mt-8">
              <p>Cart is empty</p>
              <p className="text-sm mt-2">Click items to add</p>
            </div>
          ) : (
            <div className="space-y-3">
              {cart.map(({ item, qty }) => (
                <div key={item.id} className="bg-gray-700 rounded-lg p-3">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <p className="text-white font-medium">{item.name}</p>
                      <p className="text-gray-400 text-sm">{symbol}{item.price.toFixed(2)} each</p>
                    </div>
                    <button
                      onClick={() => removeFromCart(item.id)}
                      className="text-red-400 hover:text-red-300 px-2"
                    >
                      ×
                    </button>
                  </div>
                  <div className="flex items-center justify-between mt-2">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => updateQty(item.id, -1)}
                        className="w-8 h-8 bg-gray-600 hover:bg-gray-500 rounded text-white"
                      >-</button>
                      <span className="text-white w-8 text-center">{qty}</span>
                      <button
                        onClick={() => updateQty(item.id, 1)}
                        className="w-8 h-8 bg-gray-600 hover:bg-gray-500 rounded text-white"
                      >+</button>
                    </div>
                    <span className="text-green-400 font-semibold">
                      {symbol}{(item.price * qty).toFixed(2)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Cart Totals */}
        <div className="border-t border-gray-700 p-4">
          <div className="space-y-2 mb-4">
            <div className="flex justify-between text-gray-400">
              <span>Subtotal</span>
              <span>{symbol}{subtotal.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-gray-400">
              <span>Tax (8%)</span>
              <span>{symbol}{tax.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-white text-xl font-bold pt-2 border-t border-gray-600">
              <span>Total</span>
              <span>{symbol}{total.toFixed(2)}</span>
            </div>
          </div>

          <button
            onClick={() => setShowPayment(true)}
            disabled={cart.length === 0}
            className="w-full h-14 bg-green-600 hover:bg-green-700 disabled:bg-gray-700 disabled:text-gray-500 text-white text-lg font-semibold rounded-xl transition-colors"
          >
            Process Payment
          </button>
        </div>
      </div>
    </div>
  )
}