'use client'

import { useState, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import type { Item, CartItem, Customer, Clerk, PaymentInput } from '@/types'
import { POSHeader } from '@/components/pos/POSHeader'
import { CategorySidebar } from '@/components/pos/CategorySidebar'
import { ItemGrid } from '@/components/pos/ItemGrid'
import { CartPanel } from '@/components/pos/CartPanel'
import { PaymentModal } from '@/components/pos/PaymentModal'
import { CustomerSearch } from '@/components/pos/CustomerSearch'
import { HoldOrderModal } from '@/components/pos/HoldOrderModal'
import { RecallOrderPanel } from '@/components/pos/RecallOrderPanel'
import { calculateCartTax, TaxConfig, TaxMode, CartTaxResult } from '@/lib/tax'

interface Category {
  id: string
  name: string
  icon?: string
}

interface StoreSettings {
  taxMode: TaxMode
  taxConfig: TaxConfig
  currency: string
}

interface CartItemWithCategory extends CartItem {
  category: string
}

export default function RegisterPage() {
  const router = useRouter()
  const [clerk, setClerk] = useState<Clerk | null>(null)
  const [items, setItems] = useState<Item[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [cart, setCart] = useState<CartItemWithCategory[]>([])
  const [customer, setCustomer] = useState<Customer | null>(null)
  const [settings, setSettings] = useState<StoreSettings | null>(null)
  const [cartTax, setCartTax] = useState<CartTaxResult>({
    subtotal: 0,
    tax: 0,
    total: 0,
    mode: 'exclusive',
    breakdown: []
  })
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
        const [sessionRes, settingsRes] = await Promise.all([
          fetch('/api/auth/session'),
          fetch('/api/settings')
        ])
        
        const sessionData = await sessionRes.json()
        const settingsData = await settingsRes.json()
        
        if (!sessionData.success) {
          router.push('/login')
          return
        }
        
        setClerk(sessionData.data.clerk)
        
        if (settingsData.success) {
          setSettings({
            taxMode: settingsData.data.taxMode || 'exclusive',
            taxConfig: settingsData.data.taxConfig || { mode: 'exclusive', rates: [{ name: 'Standard', rate: 0.10 }], defaultRate: 0.10, roundTo: 0.01 },
            currency: settingsData.data.currency || 'USD'
          })
        } else {
          // Fallback defaults
          setSettings({
            taxMode: 'exclusive',
            taxConfig: { mode: 'exclusive', rates: [{ name: 'Standard', rate: 0.10 }], defaultRate: 0.10, roundTo: 0.01 },
            currency: 'USD'
          })
        }
        
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

  // Recalculate tax whenever cart changes
  useEffect(() => {
    if (!settings) return
    
    const taxResult = calculateCartTax(
      cart.map(item => ({ price: item.price, qty: item.qty, category: item.category })),
      settings.taxConfig
    )
    setCartTax(taxResult)
  }, [cart, settings])

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
        lineTotal: item.price,
        category: item.category
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

  const handleCheckout = () => {
    setShowPayment(true)
  }

  const handlePayment = async (payment: PaymentInput) => {
    if (!clerk || !settings) return

    try {
      let orderId = currentOrderId
      const paymentAmountUsd = payment.amount

      // Create order if doesn't exist
      if (!orderId) {
        const orderRes = await fetch('/api/orders', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            clerkId: clerk.id,
            customerId: customer?.id,
            items: cart.map(item => ({
              itemId: item.itemId,
              name: item.name,
              price: item.price,
              qty: item.qty,
              lineTotal: item.lineTotal
            })),
            subtotal: cartTax.subtotal,
            tax: cartTax.tax,
            total: cartTax.total,
            currency: settings.currency,
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
          amountUsd: paymentAmountUsd,
          currency: payment.currency || 'USD',
          reference: payment.reference,
        }),
      })
      
      const paymentData = await paymentRes.json()
      if (!paymentData.success) throw new Error(paymentData.error?.message)

      setAmountPaid(prev => prev + paymentAmountUsd)

      // Check if fully paid
      if (amountPaid + paymentAmountUsd >= cartTax.total) {
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

  const handleHoldOrder = async (data: { holdName: string; notes?: string }) => {
    if (!clerk || cart.length === 0 || !settings) return

    try {
      const res = await fetch('/api/orders/hold', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          clerkId: clerk.id,
          customerId: customer?.id,
          items: cart,
          subtotal: cartTax.subtotal,
          tax: cartTax.tax,
          total: cartTax.total,
          holdName: data.holdName,
          notes: data.notes,
        }),
      })
      
      const resData = await res.json()
      if (resData.success) {
        clearCart()
        setShowHoldModal(false)
      }
    } catch (error) {
      console.error('Hold order error:', error)
    }
  }

  const handleRecallOrderByTicket = async (ticketNumber: number) => {
    try {
      const res = await fetch(`/api/held-orders`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'recall', ticketNumber }),
      })
      const data = await res.json()
      
      if (data.success && data.data.heldOrder) {
        const heldOrder = data.data.heldOrder
        // Note: held orders lose category info - we'll need to lookup items
        // For now, assign 'general' as fallback
        setCart(heldOrder.items.map((item: any) => ({
          itemId: item.itemId,
          name: item.name,
          price: item.price,
          qty: item.qty,
          lineTotal: item.lineTotal,
          category: 'general'
        })))
        if (heldOrder.customerId) {
          // Fetch customer details
          const custRes = await fetch(`/api/customers/${heldOrder.customerId}`)
          const custData = await custRes.json()
          if (custData.success) {
            setCustomer(custData.data.customer)
          }
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

  if (loading || !settings) {
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
            currency={settings.currency}
            taxMode={settings.taxMode}
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
          subtotal={cartTax.subtotal}
          tax={cartTax.tax}
          total={cartTax.total}
          currency={settings.currency}
          taxMode={settings.taxMode}
          taxBreakdown={cartTax.breakdown}
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
          total={cartTax.total}
          amountPaid={amountPaid}
          currency={settings.currency}
          taxMode={settings.taxMode}
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
          isOpen={showHoldModal}
          onHold={handleHoldOrder}
          onClose={() => setShowHoldModal(false)}
          defaultName={`Order ${new Date().toLocaleTimeString()}`}
        />
      )}

      {showRecallPanel && (
        <RecallOrderPanel
          isOpen={showRecallPanel}
          onRecall={async (ticketNumber: number) => {
            await handleRecallOrderByTicket(ticketNumber)
            return { id: `HOLD-${ticketNumber}`, holdName: '', items: [], subtotal: 0, total: 0, clerkName: '', createdAt: '', expiresAt: '', clerkId: '' }
          }}
          onCancel={async () => {}}
          heldOrders={[]}
          onRefresh={() => {}}
          onClose={() => setShowRecallPanel(false)}
        />
      )}
    </div>
  )
}
