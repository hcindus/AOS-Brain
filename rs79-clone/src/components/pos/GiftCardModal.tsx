'use client'

import { useState } from 'react'
import { cn } from '@/lib/utils'

interface GiftCard {
  id: string
  code: string
  balance: number
  originalAmount: number
  isActive: boolean
  expiresAt?: string
}

interface GiftCardModalProps {
  isOpen: boolean
  onClose: () => void
  onCreate: (data: { originalAmount: number; expiresAt?: string }) => Promise<GiftCard>
  onLookup: (code: string) => Promise<GiftCard | null>
  canCreate: boolean
}

export function GiftCardModal({ isOpen, onClose, onCreate, onLookup, canCreate }: GiftCardModalProps) {
  const [mode, setMode] = useState<'menu' | 'create' | 'lookup'>('menu')
  const [amount, setAmount] = useState('')
  const [expiryMonths, setExpiryMonths] = useState('12')
  const [lookupCode, setLookupCode] = useState('')
  const [giftCard, setGiftCard] = useState<GiftCard | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  if (!isOpen) return null

  const handleCreate = async () => {
    const numAmount = parseFloat(amount)
    if (!numAmount || numAmount <= 0) {
      setError('Please enter a valid amount')
      return
    }

    setIsLoading(true)
    setError('')
    try {
      const expiresAt = expiryMonths ? new Date(Date.now() + parseInt(expiryMonths) * 30 * 24 * 60 * 60 * 1000).toISOString() : undefined
      const result = await onCreate({ originalAmount: numAmount, expiresAt })
      setGiftCard(result)
      setMode('lookup')
    } catch (err) {
      setError('Failed to create gift card')
    } finally {
      setIsLoading(false)
    }
  }

  const handleLookup = async () => {
    if (!lookupCode.trim()) {
      setError('Please enter a gift card code')
      return
    }

    setIsLoading(true)
    setError('')
    try {
      const result = await onLookup(lookupCode.trim().toUpperCase())
      if (result) {
        setGiftCard(result)
      } else {
        setError('Gift card not found')
      }
    } catch (err) {
      setError('Failed to lookup gift card')
    } finally {
      setIsLoading(false)
    }
  }

  const reset = () => {
    setMode('menu')
    setAmount('')
    setExpiryMonths('12')
    setLookupCode('')
    setGiftCard(null)
    setError('')
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl">
        <div className="p-6 border-b">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-text-primary">Gift Cards</h2>
            <button onClick={() => { reset(); onClose(); }} className="text-text-secondary hover:text-text-primary">✕</button>
          </div>
        </div>

        <div className="p-6 space-y-6">
          {mode === 'menu' && (
            <div className="space-y-4">
              {canCreate && (
                <button
                  onClick={() => setMode('create')}
                  className="w-full p-6 bg-surface-secondary rounded-xl hover:bg-surface-tertiary transition-colors text-left"
                >
                  <div className="font-semibold text-text-primary mb-1">Create Gift Card</div>
                  <div className="text-sm text-text-secondary">Issue a new gift card to customer</div>
                </button>
              )}
              <button
                onClick={() => setMode('lookup')}
                className="w-full p-6 bg-surface-secondary rounded-xl hover:bg-surface-tertiary transition-colors text-left"
              >
                <div className="font-semibold text-text-primary mb-1">Check Balance</div>
                <div className="text-sm text-text-secondary">Lookup gift card balance and details</div>
              </button>
            </div>
          )}

          {mode === 'create' && canCreate && (
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-text-primary">Amount</label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary">$</span>
                  <input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="25.00"
                    className="w-full pl-8 pr-4 py-3 border border-surface-tertiary rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                  />
                </div>
                <div className="flex gap-2">
                  {[10, 25, 50, 100].map((amt) => (
                    <button
                      key={amt}
                      onClick={() => setAmount(amt.toString())}
                      className="px-3 py-1 text-sm bg-surface-secondary text-text-primary rounded-lg hover:bg-surface-tertiary transition-colors"
                    >
                      ${amt}
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-text-primary">Expiry (Months)</label>
                <select
                  value={expiryMonths}
                  onChange={(e) => setExpiryMonths(e.target.value)}
                  className="w-full px-4 py-3 border border-surface-tertiary rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                >
                  <option value="6">6 months</option>
                  <option value="12">12 months</option>
                  <option value="24">24 months</option>
                  <option value="">No expiry</option>
                </select>
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
                  onClick={handleCreate}
                  disabled={isLoading}
                  className={cn(
                    'flex-1 py-3 font-semibold rounded-xl transition-colors',
                    !isLoading ? 'bg-primary text-white hover:bg-primary-dark' : 'bg-surface-tertiary text-text-muted'
                  )}
                >
                  {isLoading ? 'Creating...' : 'Create'}
                </button>
              </div>
            </div>
          )}

          {mode === 'lookup' && (
            <div className="space-y-4">
              {!giftCard ? (
                <>
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-text-primary">Gift Card Code</label>
                    <input
                      type="text"
                      value={lookupCode}
                      onChange={(e) => setLookupCode(e.target.value.toUpperCase())}
                      placeholder="GIFT-XXXX-XXXX-XXXX"
                      className="w-full px-4 py-3 border border-surface-tertiary rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none uppercase"
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
                      {isLoading ? 'Looking up...' : 'Lookup'}
                    </button>
                  </div>
                </>
              ) : (
                <div className="space-y-4">
                  <div className="bg-surface-secondary rounded-xl p-6 text-center">
                    <div className="text-sm text-text-secondary mb-2">Current Balance</div>
                    <div className="text-4xl font-bold text-text-primary">${giftCard.balance.toFixed(2)}</div>
                  </div>

                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-text-secondary">Code:</span>
                      <span className="font-mono text-text-primary">{giftCard.code}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-text-secondary">Original Amount:</span>
                      <span className="text-text-primary">${giftCard.originalAmount.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-text-secondary">Status:</span>
                      <span className={cn(
                        'font-medium',
                        giftCard.isActive ? 'text-success' : 'text-accent-danger'
                      )}>
                        {giftCard.isActive ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                    {giftCard.expiresAt && (
                      <div className="flex justify-between">
                        <span className="text-text-secondary">Expires:</span>
                        <span className="text-text-primary">{new Date(giftCard.expiresAt).toLocaleDateString()}</span>
                      </div>
                    )}
                  </div>

                  <button
                    onClick={() => { setGiftCard(null); setLookupCode(''); }}
                    className="w-full py-3 border border-surface-tertiary text-text-primary font-semibold rounded-xl hover:bg-surface-secondary transition-colors"
                  >
                    Lookup Another
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
