'use client'

import { useState, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import type { Item, CartItem, Customer, Clerk } from '@/types'
import { POSHeader } from '@/components/pos/POSHeader'
import { CategorySidebar } from '@/components/pos/CategorySidebar'
import { ItemGrid } from '@/components/pos/ItemGrid'
import { CartPanel } from '@/components/pos/CartPanel'
import { PaymentModal } from '@/components/pos/PaymentModal'
import { CustomerSearch } from '@/components/pos/CustomerSearch'
import { HoldOrderModal } from '@/components/pos/HoldOrderModal'
import { RecallOrderPanel } from '@/components/pos/RecallOrderPanel'

interface Category {
  id: string
  name: string
  icon?: string
}

export default function RegisterPage() {
  const router = useRouter()
  const [clerk, setClerk] = useState<Clerk | null>(null)
  const [items, setItems] = useState<Item[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [cart, setCart] = useState<CartItem[]>([])
  const [customer, setCustomer] = useState<Customer | null>(null)
  const [currency, setCurrency] = useState<string>('USD')
  const [showPayment, setShowPayment] = useState(false)
  const [showCustomerSearch, setShowCustomerSearch] = useState(false)
  const [showHoldModal, setShowHoldModal] = useState(false)
  const [showRecallPanel, setShowRecallPanel] = useState(false)
  const [currentOrderId, setCurrentOrderId] = useState<string | null>(null)
  const [amountPaid, setAmountPaid] = useState(0)
  const [cartCollapsed, setCartCollapsed] = useState(false)
  const [currentTime, setCurrentTime] = useState('')
  const [loading, setLoading] = useState(true)

  // Update time
  useEffect(() => {
    const updateTime = () => {
      setCurrentTime(new Date().toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
      }))
    }
    updateTime()
    const interval = setInterval(updateTime, 1000)
    return () => clearInterval(interval)
  }, [])

  // Check session and load initial data
  useEffect(() => {
    const init = async () => {
      try {
        const sessionRes = await fetch('/api/auth/session')
        const sessionData = await sessionRes.json()
        
        if (!sessionData.success) {
          router.push('/login')
          return
        }
        
        setClerk(sessionData.data.clerk)
        await loadItems()
        await loadCategories()
      } catch (error) {
        console.error('Initialization error:', error)
        router.push('/login')
      } finally {
        setLoading(false)
      }
    }
    init()
  }, [router])

  const loadItems = async () => {
    try {
      const res = await fetch('/api/items')
      const data = await res.json()
      if (data.success) {
        setItems(data.data.items)
      }
    } catch (error) {
      console.error('Failed to load items:', error)
    }
  }

  const loadCategories = async () => {
    try {
      const res = await fetch('/api/items')
      const data = await res.json()
      if (data.success) {
        const uniqueCats = Array.from(new Set(data.data.items.map((i: Item) => i.category))) as string[]
        setCategories(uniqueCats.map((name) => ({
          id: name,
          name: name,
          icon: getCategoryIcon(name)
        })))
      }
    } catch (error) {
      console.error('Failed to load categories:', error)
    }
  }

  const getCategoryIcon = (category: string): string => {
    const map: Record<string, string> = {
      'food': 'food',
      'drinks': 'drinks',
      'beverages': 'drinks',
      'bakery': 'bakery',
      'dessert': 'dessert',
      'retail': 'retail',
      'general': 'general',
      'alcohol': 'alcohol',
    }
    return map[category.toLowerCase()] || 'general'
  }

  const filteredItems = items.filter(item => {
    if (!selectedCategory) return item.active
    return item.category === selectedCategory && item.active
  })

  const addToCart = useCallback((item: Item) => {
    setCart(prev => {
      const existing = prev.find(ci => ci.itemId === item.id)
      if (existing) {
        return prev.map(ci =>
          ci.itemId === item.id 
            ? { ...ci, qty: ci.qty + 1, lineTotal: (ci.qty + 1) * ci.price }
            : ci
        )
      }
      return [...prev, {
        itemId: item.id,
        name: item.name,
        price: item.price,
        qty: 1,
        lineTotal: item.price
      }]
    })
  }, [])

  const updateQty = useCallback((itemId: string, qty: number) => {
    if (qty <= 0) {
      setCart(prev => prev.filter(ci => ci.itemId !== itemId))
    } else {
      setCart(prev => prev.map(ci =>
        ci.itemId === itemId 
          ? { ...ci, qty, lineTotal: qty * ci.price }
          : ci
      ))
    }
  }, [])

  const removeFromCart = useCallback((itemId: string) => {
    setCart(prev => prev.filter(ci => ci.itemId !== itemId))
  }, [])

  const clearCart = useCallback(() => {
    setCart([])
    setCustomer(null)
    setCurrentOrderId(null)
    setAmountPaid(0)
  }, [])

  const subtotal = cart.reduce((sum, ci) => sum + ci.lineTotal, 0)
  const tax = subtotal * 0.1 // 10% tax
  const total = subtotal + tax

  const handleCheckout = () => {
    setShowPayment(true)
  }

  const handlePayment = async (payment: {
    type: string
    amountUsd: number
    currency: string
    reference?: string
  }) => {
    if (!clerk) return

    try {
      let orderId = currentOrderId

      // Create order if doesn't exist
      if (!orderId) {
        const orderRes = await fetch('/api/orders', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            clerkId: clerk.id,
            customerId: customer?.id,
            items: cart,
            subtotal,
            tax,
            total,
            currency,
            currencyRate: 1,
          }),
        })
        const orderData = await orderRes.json()
        if (!orderData.success) throw new Error(orderData.error?.message)
        orderId = orderData.data.order.id
        setCurrentOrderId(orderId)
      }

      // Process payment
      const paymentRes = await fetch(`/api/orders/${orderId}/payments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          clerkId: clerk.id,
          type: payment.type,
          amountUsd: payment.amountUsd,
          currency: payment.currency,
          reference: payment.reference,
        }),
      })
      
      const paymentData = await paymentRes.json()
      if (!paymentData.success) throw new Error(paymentData.error?.message)

      setAmountPaid(prev => prev + payment.amountUsd)

      // Check if fully paid
      if (amountPaid + payment.amountUsd >= total) {
        // Complete order
        await fetch(`/api/orders/${orderId}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ status: 'completed' }),
        })
        
        // Print receipt and clear
        clearCart()
        setShowPayment(false)
      }
    } catch (error) {
      console.error('Payment error:', error)
      alert('Payment failed: ' + (error as Error).message)
    }
  }

  const handleHoldOrder = async (holdName: string) => {
    if (!clerk || cart.length === 0) return

    try {
      const res = await fetch('/api/orders/hold', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          clerkId: clerk.id,
          customerId: customer?.id,
          items: cart,
          subtotal,
          tax,
          total,
          holdName,
        }),
      })
      
      const data = await res.json()
      if (data.success) {
        clearCart()
        setShowHoldModal(false)
      }
    } catch (error) {
      console.error('Hold order error:', error)
    }
  }

  const handleRecallOrder = async (orderId: string) => {
    try {
      const res = await fetch(`/api/orders/recall/${orderId}`)
      const data = await res.json()
      
      if (data.success && data.data.order) {
        const order = data.data.order
        setCurrentOrderId(order.id)
        setCart(order.items.map((item: any) => ({
          itemId: item.itemId,
          name: item.name,
          price: item.price,
          qty: item.qty,
          lineTotal: item.lineTotal,
        })))
        if (order.customer) {
          setCustomer(order.customer)
        }
        setShowRecallPanel(false)
      }
    } catch (error) {
      console.error('Recall order error:', error)
    }
  }

  const handleLogout = async () => {
    await fetch('/api/auth/logout', { method: 'POST' })
    router.push('/login')
  }

  if (loading) {
    return (
      <div className="h-screen flex items-center justify-center bg-surface-secondary">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (!clerk) return null

  return (
    <div className="h-screen flex flex-col bg-surface-secondary">
      {/* Header */}
      <POSHeader
        clerk={clerk}
        onLogout={handleLogout}
        onOpenMenu={() => setShowRecallPanel(true)}
        currentTime={currentTime}
      />

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Category Sidebar */}
        <CategorySidebar
          categories={categories}
          activeCategory={selectedCategory}
          onSelectCategory={setSelectedCategory}
        />

        {/* Item Grid */}
        <div className="flex-1 flex flex-col min-w-0">
          <ItemGrid
            items={filteredItems}
            onAddToCart={addToCart}
            currency={currency}
          />
        </div>

        {/* Cart Panel */}
        <CartPanel
          items={cart}
          onUpdateQty={updateQty}
          onRemoveItem={removeFromCart}
          onClearCart={clearCart}
          onCheckout={handleCheckout}
          onHoldOrder={() => setShowHoldModal(true)}
          onAddCustomer={() => setShowCustomerSearch(true)}
          customer={customer}
          clerkName={clerk.name}
          subtotal={subtotal}
          tax={tax}
          total={total}
          currency={currency}
          isCollapsed={cartCollapsed}
          onToggleCollapse={() => setCartCollapsed(!cartCollapsed)}
        />
      </div>

      {/* Modals */}
      {showPayment && (
        <PaymentModal
          isOpen={showPayment}
          onClose={() => setShowPayment(false)}
          onSubmit={handlePayment}
          onCompleteOrder={() => {
            clearCart()
            setShowPayment(false)
          }}
          total={total}
          amountPaid={amountPaid}
          currency={currency}
        />
      )}

      {showCustomerSearch && (
        <CustomerSearch
          onSelect={setCustomer}
          onClose={() => setShowCustomerSearch(false)}
        />
      )}

      {showHoldModal && (
        <HoldOrderModal
          onHold={handleHoldOrder}
          onClose={() => setShowHoldModal(false)}
          itemCount={cart.reduce((sum, ci) => sum + ci.qty, 0)}
          total={total}
          currency={currency}
        />
      )}

      {showRecallPanel && (
        <RecallOrderPanel
          orders={[]}
          onRecall={handleRecallOrder}
          onClose={() => setShowRecallPanel(false)}
        />
      )}
    </div>
  )
}
