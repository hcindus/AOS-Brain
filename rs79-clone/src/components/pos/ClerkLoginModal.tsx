'use client'

import { useState, useEffect } from 'react'
import { cn } from '@/lib/utils'

interface Clerk {
  id: string
  name: string
  role: 'Admin' | 'Manager' | 'Clerk'
  active: boolean
}

interface ClerkLoginModalProps {
  isOpen: boolean
  onClose: () => void
  onLogin: (clerkId: string, pin: string) => Promise<{ success: boolean; error?: string }>
  clerks: Clerk[]
}

export function ClerkLoginModal({ isOpen, onClose, onLogin, clerks }: ClerkLoginModalProps) {
  const [selectedClerk, setSelectedClerk] = useState<Clerk | null>(null)
  const [pin, setPin] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    if (isOpen) {
      setSelectedClerk(null)
      setPin('')
      setError('')
    }
  }, [isOpen])

  if (!isOpen) return null

  const activeClerks = clerks.filter((c) => c.active)

  const handleNumber = (num: string) => {
    if (pin.length < 6) {
      setPin((prev) => prev + num)
      setError('')
    }
  }

  const handleBackspace = () => {
    setPin((prev) => prev.slice(0, -1))
    setError('')
  }

  const handleClear = () => {
    setPin('')
    setError('')
  }

  const handleSubmit = async () => {
    if (!selectedClerk || pin.length < 4) return

    setIsLoading(true)
    setError('')

    try {
      const result = await onLogin(selectedClerk.id, pin)
      if (!result.success) {
        setError(result.error || 'Login failed')
        setPin('')
      }
    } catch {
      setError('An error occurred')
      setPin('')
    } finally {
      setIsLoading(false)
    }
  }

  const keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'C', '0', '←']

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl">
        <div className="p-6 border-b">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-text-primary">{selectedClerk ? 'Enter PIN' : 'Select Clerk'}</h2>
            <button onClick={onClose} className="text-text-secondary hover:text-text-primary">✕</button>
          </div>
        </div>

        <div className="p-6">
          {!selectedClerk ? (
            <div className="grid grid-cols-2 gap-3">
              {activeClerks.map((clerk) => (
                <button
                  key={clerk.id}
                  onClick={() => setSelectedClerk(clerk)}
                  className="p-4 bg-surface-secondary rounded-xl hover:bg-surface-tertiary transition-colors text-left"
                >
                  <div className="font-semibold text-text-primary">{clerk.name}</div>
                  <div className="text-sm text-text-secondary">{clerk.role}</div>
                </button>
              ))}
            </div>
          ) : (
            <div className="space-y-6">
              <div className="text-center">
                <div className="text-lg font-medium text-text-primary">{selectedClerk.name}</div>
                <div className="text-sm text-text-secondary">Enter your 4-6 digit PIN</div>
                <button
                  onClick={() => {
                    setSelectedClerk(null)
                    setPin('')
                    setError('')
                  }}
                  className="text-sm text-primary hover:underline mt-2"
                >
                  Change Clerk
                </button>
              </div>

              <div className="flex justify-center gap-3">
                {Array.from({ length: 6 }).map((_, i) => (
                  <div
                    key={i}
                    className={cn(
                      'w-10 h-12 rounded-xl border-2 flex items-center justify-center text-lg font-bold transition-all',
                      i < pin.length
                        ? 'border-primary bg-primary/5 text-primary'
                        : 'border-surface-tertiary bg-surface-secondary text-transparent'
                    )}
                  >
                    •
                  </div>
                ))}
              </div>

              {error && <p className="text-center text-accent-danger text-sm">{error}</p>}

              <div className="grid grid-cols-3 gap-2">
                {keys.map((key) => (
                  <button
                    key={key}
                    onClick={() => {
                      if (key === 'C') handleClear()
                      else if (key === '←') handleBackspace()
                      else handleNumber(key)
                    }}
                    disabled={isLoading}
                    className={cn(
                      'h-14 text-xl font-semibold rounded-xl transition-all',
                      key === 'C' || key === '←'
                        ? 'bg-surface-tertiary text-text-secondary'
                        : 'bg-surface-secondary text-text-primary hover:bg-surface-tertiary'
                    )}
                  >
                    {key}
                  </button>
                ))}
              </div>

              <button
                onClick={handleSubmit}
                disabled={pin.length < 4 || isLoading}
                className={cn(
                  'w-full py-4 rounded-xl font-bold text-lg transition-colors',
                  pin.length >= 4 && !isLoading
                    ? 'bg-primary text-white hover:bg-primary-dark'
                    : 'bg-surface-tertiary text-text-muted cursor-not-allowed'
                )}
              >
                {isLoading ? 'Verifying...' : 'Login'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
