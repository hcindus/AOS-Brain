'use client'

import { useState } from 'react'
import { X, Save } from 'lucide-react'

interface HoldOrderModalProps {
  onHold: (name: string) => void
  onClose: () => void
  itemCount: number
  total: number
  currency: string
}

export function HoldOrderModal({ onHold, onClose, itemCount, total, currency }: HoldOrderModalProps) {
  const [name, setName] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim()) return
    
    setIsSubmitting(true)
    try {
      await onHold(name.trim())
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-bold text-text-primary">Hold Order</h2>
            <p className="text-sm text-text-secondary">Save this cart for later</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-text-secondary hover:text-text-primary hover:bg-surface-secondary rounded-lg transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        <div className="mb-6 p-4 bg-surface-secondary rounded-xl">
          <div className="flex justify-between text-sm mb-2">
            <span className="text-text-secondary">Items:</span>
            <span className="font-medium text-text-primary">{itemCount}</span>
          </div>
          <div className="flex justify-between text-lg font-bold">
            <span className="text-text-primary">Total:</span>
            <span className="text-accent-success">{currency}{total.toFixed(2)}</span>
          </div>
        </div>

        <form onSubmit={handleSubmit}>
          <label className="block text-sm font-medium text-text-primary mb-2">
            Order Name (e.g., "Table 5", "John's Order")
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter order name..."
            className="w-full px-4 py-3 border border-surface-tertiary rounded-xl text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent mb-6"
            autoFocus
          />

          <div className="flex gap-3">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 py-3 px-4 rounded-xl font-medium bg-surface-secondary text-text-primary hover:bg-surface-tertiary transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!name.trim() || isSubmitting}
              className="flex-1 py-3 px-4 rounded-xl font-bold bg-primary text-white hover:bg-primary-dark disabled:opacity-40 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
            >
              <Save size={18} />
              {isSubmitting ? 'Saving...' : 'Hold Order'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
