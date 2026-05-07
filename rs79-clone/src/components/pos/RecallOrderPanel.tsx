'use client'

import { HeldOrder } from '@/types'
import { X, RotateCcw, Clock, User } from 'lucide-react'

interface RecallOrderPanelProps {
  orders: HeldOrder[]
  onRecall: (orderId: string) => void
  onClose: () => void
}

function formatElapsedTime(createdAt: string): string {
  const created = new Date(createdAt)
  const now = new Date()
  const diff = Math.floor((now.getTime() - created.getTime()) / 1000 / 60)
  
  if (diff < 1) return 'Just now'
  if (diff < 60) return `${diff} min ago`
  const hours = Math.floor(diff / 60)
  if (hours < 24) return `${hours} hr ago`
  return `${Math.floor(hours / 24)} days ago`
}

export function RecallOrderPanel({ orders, onRecall, onClose }: RecallOrderPanelProps) {
  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-lg w-full max-h-[80vh] flex flex-col shadow-2xl">
        <div className="flex items-center justify-between p-6 border-b border-surface-tertiary">
          <div>
            <h2 className="text-xl font-bold text-text-primary">Recall Held Order</h2>
            <p className="text-sm text-text-secondary">Select an order to resume</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-text-secondary hover:text-text-primary hover:bg-surface-secondary rounded-lg transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6">
          {orders.length === 0 ? (
            <div className="text-center py-12 text-text-muted">
              <RotateCcw size={48} className="mx-auto mb-4 opacity-30" />
              <p className="text-lg font-medium mb-1">No held orders</p>
              <p className="text-sm">There are no orders currently on hold</p>
            </div>
          ) : (
            <div className="space-y-3">
              {orders.map((order) => (
                <button
                  key={order.id}
                  onClick={() => onRecall(order.id)}
                  className="w-full p-4 border border-surface-tertiary rounded-xl hover:border-primary hover:shadow-soft transition-all text-left group"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-text-primary">{order.holdName}</span>
                    </div>
                    <div className="flex items-center gap-1 text-xs text-text-secondary">
                      <Clock size={12} />
                      {formatElapsedTime(order.createdAt)}
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-4">
                      <span className="text-text-secondary">
                        {order.items.length} items
                      </span>
                      {order.customerName && (
                        <span className="flex items-center gap-1 text-text-secondary">
                          <User size={12} />
                          {order.customerName}
                        </span>
                      )}
                    </div>
                    <span className="font-bold text-accent-success">
                      ${order.total.toFixed(2)}
                    </span>
                  </div>

                  <div className="mt-3 pt-3 border-t border-surface-tertiary">
                    <div className="flex items-center justify-between text-xs text-text-muted">
                      <span>Click to recall order</span>
                      <RotateCcw size={14} className="text-primary opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
