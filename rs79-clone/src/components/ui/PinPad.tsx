'use client'

import { useState, useCallback } from 'react'
import { cn } from '@/lib/utils'

interface PinPadProps {
  onSubmit: (pin: string) => void
  onCancel?: () => void
  maxLength?: number
  title?: string
  error?: string | null
  isLoading?: boolean
}

export function PinPad({
  onSubmit,
  onCancel,
  maxLength = 4,
  title = 'Enter PIN',
  error,
  isLoading = false,
}: PinPadProps) {
  const [pin, setPin] = useState('')

  const handleNumber = useCallback((num: string) => {
    if (pin.length < maxLength && !isLoading) {
      setPin((prev) => prev + num)
    }
  }, [pin, maxLength, isLoading])

  const handleBackspace = useCallback(() => {
    if (!isLoading) {
      setPin((prev) => prev.slice(0, -1))
    }
  }, [isLoading])

  const handleClear = useCallback(() => {
    if (!isLoading) {
      setPin('')
    }
  }, [isLoading])

  const handleSubmit = useCallback(() => {
    if (pin.length >= 4 && !isLoading) {
      onSubmit(pin)
    }
  }, [pin, onSubmit, isLoading])

  const keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'C', '0', '←']

  return (
    <div className="w-full max-w-sm mx-auto p-6 bg-white rounded-2xl shadow-soft">
      <div className="text-center mb-6">
        <h2 className="text-xl font-bold text-text-primary mb-2">{title}</h2>
        <p className="text-sm text-text-secondary">Enter your 4-digit PIN</p>
      </div>

      {/* PIN Display */}
      <div className="mb-6">
        <div className="flex justify-center gap-3 mb-2">
          {Array.from({ length: maxLength }).map((_, i) => (
            <div
              key={i}
              className={cn(
                'w-12 h-14 rounded-xl border-2 flex items-center justify-center text-2xl font-bold transition-all',
                i < pin.length
                  ? 'border-primary bg-primary/5 text-primary'
                  : 'border-surface-tertiary bg-surface-secondary text-transparent'
              )}
            >
              {pin[i] || '•'}
            </div>
          ))}
        </div>
        {error && (
          <p className="text-center text-sm text-accent-danger mt-2">{error}</p>
        )}
      </div>

      {/* Keypad */}
      <div className="keypad-grid mb-4">
        {keys.map((key) => {
          const isAction = key === 'C' || key === '←'
          return (
            <button
              key={key}
              onClick={() => {
                if (key === 'C') handleClear()
                else if (key === '←') handleBackspace()
                else handleNumber(key)
              }}
              disabled={isLoading}
              className={cn(
                'h-16 text-xl font-semibold rounded-xl transition-all duration-150',
                isAction
                  ? 'bg-surface-tertiary text-text-secondary hover:bg-surface-tertiary/80'
                  : 'bg-white border border-surface-tertiary text-text-primary hover:bg-surface-secondary active:bg-surface-tertiary active:scale-95 shadow-sm',
                isLoading && 'opacity-50 cursor-not-allowed'
              )}
            >
              {key}
            </button>
          )
        })}
      </div>

      {/* Submit Button */}
      <button
        onClick={handleSubmit}
        disabled={pin.length < 4 || isLoading}
        className={cn(
          'w-full py-4 rounded-xl font-bold text-lg transition-all duration-150',
          pin.length >= 4 && !isLoading
            ? 'bg-primary text-white hover:bg-primary-dark shadow-lg shadow-primary/25 active:scale-[0.98]'
            : 'bg-surface-tertiary text-text-muted cursor-not-allowed'
        )}
      >
        {isLoading ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
            </svg>
            Verifying...
          </span>
        ) : (
          'Login'
        )}
      </button>

      {onCancel && (
        <button
          onClick={onCancel}
          disabled={isLoading}
          className="w-full mt-3 py-3 text-text-secondary hover:text-text-primary font-medium transition-colors"
        >
          Cancel
        </button>
      )}
    </div>
  )
}
