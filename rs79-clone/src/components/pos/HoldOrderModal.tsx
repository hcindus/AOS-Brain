'use client'

import { useState } from 'react'
import { cn } from '@/lib/utils'

interface HoldOrderModalProps {
  isOpen: boolean
  onClose: () => void
  onHold: (data: { holdName: string; notes?: string }) => void
  defaultName?: string
}

export function HoldOrderModal({ isOpen, onClose, onHold, defaultName }: HoldOrderModalProps) {
  const [holdName, setHoldName] = useState(defaultName || '')
  const [notes, setNotes] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  if (!isOpen) return null

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!holdName.trim()) return

    setIsSubmitting(true)
    try {
      await onHold({ holdName: holdName.trim(), notes: notes.trim() || undefined })
      setHoldName('')
      setNotes('')
      onClose()
    } finally {
      setIsSubmitting(false)
    }
  }

  const quickNames = ['Bar', 'Table 1', 'Table 2', 'Table 3', 'Drive-Thru', 'Phone Order']

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl">
        <div className="p-6 border-b">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-text-primary">Hold Order</h2>
            <button onClick={onClose} className="text-text-secondary hover:text-text-primary">✕</button>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-text-primary">Hold Name / Ticket</label>
            <input
              type="text"
              value={holdName}
              onChange={(e) => setHoldName(e.target.value)}
              placeholder="e.g., Table 5, John, Bar"
              className="w-full px-4 py-3 border border-surface-tertiary rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
              autoFocus
            />
            <div className="flex flex-wrap gap-2">
              {quickNames.map((name) => (
                <button
                  key={name}
                  type="button"
                  onClick={() => setHoldName(name)}
                  className="px-3 py-1 text-sm bg-surface-secondary text-text-primary rounded-full hover:bg-surface-tertiary transition-colors"
                >
                  {name}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-text-primary">Notes (Optional)</label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Any special instructions..."
              rows={3}
              className="w-full px-4 py-3 border border-surface-tertiary rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none resize-none"
            />
          </div>

          <div className="flex gap-3">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 py-3 border border-surface-tertiary text-text-primary font-semibold rounded-xl hover:bg-surface-secondary transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!holdName.trim() || isSubmitting}
              className={cn(
                'flex-1 py-3 font-semibold rounded-xl transition-colors',
                holdName.trim() && !isSubmitting
                  ? 'bg-primary text-white hover:bg-primary-dark'
                  : 'bg-surface-tertiary text-text-muted cursor-not-allowed'
              )}
            >
              {isSubmitting ? 'Holding...' : 'Hold Order'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
