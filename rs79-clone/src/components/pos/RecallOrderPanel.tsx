'use client'

import { useState, useEffect } from 'react'
import { cn } from '@/lib/utils'

interface HeldOrder {
  id: string
  holdName: string
  items: Array<{
    name: string
    qty: number
    lineTotal: number
  }>
  subtotal: number
  total: number
  customerName?: string
  clerkName: string
  createdAt: string
  expiresAt: string
}

interface RecallOrderPanelProps {
  isOpen: boolean
  onClose: () => void
  onRecall: (ticketNumber: number) => Promise<HeldOrder>
  onCancel: (ticketNumber: number) => Promise<void>
  heldOrders: HeldOrder[]
  onRefresh: () => void
}

export function RecallOrderPanel({
  isOpen,
  onClose,
  onRecall,
  onCancel,
  heldOrders,
  onRefresh,
}: RecallOrderPanelProps) {
  const [ticketNumber, setTicketNumber] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [selectedOrder, setSelectedOrder] = useState<HeldOrder | null>(null)

  useEffect(() => {
    if (isOpen) {
      onRefresh()
    }
  }, [isOpen])

  if (!isOpen) return null

  const handleRecallByTicket = async () => {
    if (!ticketNumber.trim()) {
      setError('Please enter a ticket number')
      return
    }

    setIsLoading(true)
    setError('')
    try {
      await onRecall(parseInt(ticketNumber))
      onClose()
    } catch (err) {
      setError('Order not found or already expired')
    } finally {
      setIsLoading(false)
    }
  }

  const handleRecallOrder = async (order: HeldOrder) => {
    const ticketNum = parseInt(order.id.replace('HOLD-', ''))
    setIsLoading(true)
    try {
      await onRecall(ticketNum)
      onClose()
    } catch (err) {
      setError('Failed to recall order')
    } finally {
      setIsLoading(false)
    }
  }

  const handleCancelOrder = async (order: HeldOrder, e: React.MouseEvent) => {
    e.stopPropagation()
    if (!confirm(`Cancel held order "${order.holdName}"?`)) return

    const ticketNum = parseInt(order.id.replace('HOLD-', ''))
    setIsLoading(true)
    try {
      await onCancel(ticketNum)
      onRefresh()
    } catch (err) {
      setError('Failed to cancel order')
    } finally {
      setIsLoading(false)
    }
  }

  const formatTimeRemaining = (expiresAt: string) => {
    const diff = new Date(expiresAt).getTime() - Date.now()
    if (diff <= 0) return 'Expired'
    const hours = Math.floor(diff / (1000 * 60 * 60))
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
    return `${hours}h ${minutes}m remaining`
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-2xl max-h-[90vh] overflow-auto bg-white rounded-2xl shadow-2xl">
        <div className="sticky top-0 bg-white border-b p-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-text-primary">Recall Order</h2>
            <button onClick={onClose} className="text-text-secondary hover:text-text-primary">✕</button>
          </div>
        </div>

        <div className="p-6 space-y-6">
          {/* Ticket Number Input */}
          <div className="bg-surface-secondary rounded-xl p-4">
            <label className="block text-sm font-medium text-text-primary mb-2">Enter Ticket Number</label>
            <div className="flex gap-2">
              <input
                type="number"
                value={ticketNumber}
                onChange={(e) => setTicketNumber(e.target.value)}
                placeholder="Ticket #"
                className="flex-1 px-4 py-3 border border-surface-tertiary rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
              />
              <button
                onClick={handleRecallByTicket}
                disabled={isLoading}
                className={cn(
                  'px-6 py-3 font-semibold rounded-xl transition-colors',
                  !isLoading ? 'bg-primary text-white hover:bg-primary-dark' : 'bg-surface-tertiary text-text-muted'
                )}
              >
                Recall
              </button>
            </div>
            {error && <p className="text-accent-danger text-sm mt-2">{error}</p>}
          </div>

          {/* Held Orders List */}
          <div>
            <h3 className="font-semibold text-text-primary mb-3">Active Held Orders</h3>
            
            {heldOrders.length === 0 ? (
              <p className="text-text-secondary text-center py-8">No active held orders</p>
            ) : (
              <div className="space-y-3">
                {heldOrders.map((order) => (
                  <div
                    key={order.id}
                    onClick={() => handleRecallOrder(order)}
                    className="p-4 bg-surface-secondary rounded-xl hover:bg-surface-tertiary cursor-pointer transition-colors"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-3">
                        <span className="text-lg font-bold text-primary">#{order.id.replace('HOLD-', '')}</span>
                        <span className="font-semibold text-text-primary">{order.holdName}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm text-text-secondary">
                          {formatTimeRemaining(order.expiresAt)}
                        </span>
                        <button
                          onClick={(e) => handleCancelOrder(order, e)}
                          className="px-3 py-1 text-sm text-accent-danger hover:bg-accent-danger/10 rounded-lg transition-colors"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                    
                    <div className="text-sm text-text-secondary mb-2">
                      {order.items.length} items • {order.customerName || 'No customer'} • Held by {order.clerkName}
                    </div>
                    
                    <div className="flex justify-between items-center">
                      <div className="text-sm text-text-secondary">
                        {new Date(order.createdAt).toLocaleString()}
                      </div>
                      <div className="font-bold text-text-primary">${order.total.toFixed(2)}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
