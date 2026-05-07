'use client'

import { useState } from 'react'
import { cn } from '@/lib/utils'

interface StoreCreditModalProps {
  isOpen: boolean
  onClose: () => void
  onAddCredit: (data: { customerId: string; amount: number; reason: string }) => Promise<void>
  onLookup: (customerId: string) => Promise<{ balance: number; totalEarned: number; totalSpent: number } | null>
  onApplyToOrder: (amount: number) => void
  currentOrderTotal?: number
}

export function StoreCreditModal({
  isOpen,
  onClose,
  onAddCredit,
  onLookup,
  onApplyToOrder,
  currentOrderTotal,
}: StoreCreditModalProps) {
  const [mode, setMode] = useState<'menu' | 'lookup' | 'add' | 'apply'>('menu')
  const [customerId, setCustomerId] = useState('')
  const [amount, setAmount] = useState('')
  const [reason, setReason] = useState('')
  const [creditInfo, setCreditInfo] = useState<{
    balance: number
    totalEarned: number
    totalSpent: number
  } | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  if (!isOpen) return null

  const handleLookup = async () => {
    if (!customerId.trim()) {
      setError('Please enter a customer ID')
      return
    }

    setIsLoading(true)
    setError('')
    try {
      const result = await onLookup(customerId.trim())
      if (result) {
        setCreditInfo(result)
        setMode('lookup')
      } else {
        setError('Customer not found or has no store credit')
      }
    } catch {
      setError('Failed to lookup store credit')
    } finally {
      setIsLoading(false)
    }
  }

  const handleAddCredit = async () => {
    const numAmount = parseFloat(amount)
    if (!numAmount || numAmount <= 0) {
      setError('Please enter a valid amount')
      return
    }
    if (!reason.trim()) {
      setError('Please enter a reason')
      return
    }

    setIsLoading(true)
    setError('')
    try {
      await onAddCredit({ customerId, amount: numAmount, reason: reason.trim() })
      setMode('lookup')
      setAmount('')
      setReason('')
    } catch {
      setError('Failed to add store credit')
    } finally {
      setIsLoading(false)
    }
  }

  const handleApply = () => {
    const applyAmount = parseFloat(amount)
    if (!applyAmount || applyAmount <= 0) {
      setError('Please enter a valid amount')
      return
    }
    if (creditInfo && applyAmount > creditInfo.balance) {
      setError('Amount exceeds available credit')
      return
    }
    onApplyToOrder(applyAmount)
    onClose()
  }

  const reset = () => {
    setMode('menu')
    setCustomerId('')
    setAmount('')
    setReason('')
    setCreditInfo(null)
    setError('')
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl">
        <div className="p-6 border-b">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-text-primary">Store Credit</h2>
            <button onClick={() => { reset(); onClose(); }} className="text-text-secondary hover:text-text-primary">✕</button>
          </div>
        </div>

        <div className="p-6 space-y-6">
          {mode === 'menu' && (
            <div className="space-y-4">
              <button
                onClick={() => setMode('lookup')}
                className="w-full p-6 bg-surface-secondary rounded-xl hover:bg-surface-tertiary transition-colors text-left"
              >
                <div className="font-semibold text-text-primary mb-1">Check Balance</div>
                <div className="text-sm text-text-secondary">View customer store credit balance</div>
              </button>
              <button
                onClick={() => setMode('add')}
                className="w-full p-6 bg-surface-secondary rounded-xl hover:bg-surface-tertiary transition-colors text-left"
              >
                <div className="font-semibold text-text-primary mb-1">Add Store Credit</div>
                <div className="text-sm text-text-secondary">Add credit to customer account</div>
              </button>
              {currentOrderTotal && currentOrderTotal > 0 && (
                <button
                  onClick={() => setMode('apply')}
                  className="w-full p-6 bg-surface-secondary rounded-xl hover:bg-surface-tertiary transition-colors text-left"
                >
                  <div className="font-semibold text-text-primary mb-1">Apply to Order</div>
                  <div className="text-sm text-text-secondary">Use store credit for current order</div>
                </button>
              )}
            </div>
          )}

          {(mode === 'lookup' || mode === 'add' || mode === 'apply') && !creditInfo && (
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-text-primary">Customer ID</label>
                <input
                  type="text"
                  value={customerId}
                  onChange={(e) => setCustomerId(e.target.value)}
                  placeholder="Enter customer ID"
                  className="w-full px-4 py-3 border border-surface-tertiary rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                />
              </div>

              {error && <p className="text-accent-danger text-sm">{error}</p>}

              <div className="flex gap-3">
                <button
                  onClick={() => setMode('menu')}
                  className="flex-1 py-3 border border-surface-tertiary text-text-primary font-semibold rounded-xl hover:bg-surface-secondary transition-colors"
                >
                  Back
                </button>
                <button
                  onClick={handleLookup}
                  disabled={isLoading}
                  className={cn(
                    'flex-1 py-3 font-semibold rounded-xl transition-colors',
                    !isLoading ? 'bg-primary text-white hover:bg-primary-dark' : 'bg-surface-tertiary text-text-muted'
                  )}
                >
                  {isLoading ? 'Loading...' : 'Lookup'}
                </button>
              </div>
            </div>
          )}

          {mode === 'add' && creditInfo && (
            <div className="space-y-4">
              <div className="bg-surface-secondary rounded-xl p-4">
                <div className="text-sm text-text-secondary mb-1">Current Balance</div>
                <div className="text-2xl font-bold text-text-primary">${creditInfo.balance.toFixed(2)}</div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-text-primary">Amount to Add</label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary">$</span>
                  <input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="0.00"
                    className="w-full pl-8 pr-4 py-3 border border-surface-tertiary rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-text-primary">Reason</label>
                <select
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  className="w-full px-4 py-3 border border-surface-tertiary rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                >
                  <option value="">Select reason...</option>
                  <option value="Refund">Refund</option>
                  <option value="Return">Return</option>
                  <option value="Compensation">Compensation</option>
                  <option value="Promotional">Promotional</option>
                </select>
              </div>

              {error && <p className="text-accent-danger text-sm">{error}</p>}

              <div className="flex gap-3">
                <button
                  onClick={() => setCreditInfo(null)}
                  className="flex-1 py-3 border border-surface-tertiary text-text-primary font-semibold rounded-xl hover:bg-surface-secondary transition-colors"
                >
                  Back
                </button>
                <button
                  onClick={handleAddCredit}
                  disabled={isLoading}
                  className={cn(
                    'flex-1 py-3 font-semibold rounded-xl transition-colors',
                    !isLoading ? 'bg-primary text-white hover:bg-primary-dark' : 'bg-surface-tertiary text-text-muted'
                  )}
                >
                  {isLoading ? 'Adding...' : 'Add Credit'}
                </button>
              </div>
            </div>
          )}

          {(mode === 'lookup' || mode === 'apply') && creditInfo && (
            <div className="space-y-4">
              <div className="bg-surface-secondary rounded-xl p-6 text-center">
                <div className="text-sm text-text-secondary mb-2">Available Credit</div>
                <div className="text-4xl font-bold text-text-primary">${creditInfo.balance.toFixed(2)}</div>
              </div>

              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-text-secondary">Total Earned:</span>
                  <span className="text-text-primary">${creditInfo.totalEarned.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-secondary">Total Spent:</span>
                  <span className="text-text-primary">${creditInfo.totalSpent.toFixed(2)}</span>
                </div>
              </div>

              {mode === 'apply' && (
                <div className="space-y-2">
                  <label className="text-sm font-medium text-text-primary">Amount to Apply</label>
                  <div className="relative">
                    <span className="absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary">$</span>
                    <input
                      type="number"
                      value={amount}
                      onChange={(e) => setAmount(e.target.value)}
                      placeholder={Math.min(creditInfo.balance, currentOrderTotal || 0).toFixed(2)}
                      max={creditInfo.balance}
                      className="w-full pl-8 pr-4 py-3 border border-surface-tertiary rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                    />
                  </div>
                  {error && <p className="text-accent-danger text-sm">{error}</p>}

                  <button
                    onClick={handleApply}
                    className="w-full py-3 bg-primary text-white font-semibold rounded-xl hover:bg-primary-dark transition-colors"
                  >
                    Apply to Order
                  </button>
                </div>
              )}

              <button
                onClick={() => { setCreditInfo(null); setCustomerId(''); }}
                className="w-full py-3 border border-surface-tertiary text-text-primary font-semibold rounded-xl hover:bg-surface-secondary transition-colors"
              >
                Lookup Another
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
