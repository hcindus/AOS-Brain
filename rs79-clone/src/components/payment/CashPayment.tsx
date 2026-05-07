'use client'

import { useState, useMemo } from 'react'
import { cn } from '@/lib/utils'
import { DollarSign, ArrowLeftRight } from 'lucide-react'
import { Button } from '@/components/ui/Button'

interface CashPaymentProps {
  balanceDue: number
  currency: string
  onSubmit: (data: { amount: number; tendered: number; change: number }) => void
  onCancel: () => void
}

const QUICK_AMOUNTS = [5, 10, 20, 50, 100]

export function CashPayment({ balanceDue, currency, onSubmit, onCancel }: CashPaymentProps) {
  const [amount, setAmount] = useState<string>(balanceDue.toFixed(2))
  const [tendered, setTendered] = useState<string>('')
  const [errors, setErrors] = useState<Record<string, string>>({})

  const numericAmount = parseFloat(amount) || 0
  const numericTendered = parseFloat(tendered) || 0

  const change = useMemo(() => {
    if (numericTendered > numericAmount) {
      return numericTendered - numericAmount
    }
    return 0
  }, [numericAmount, numericTendered])

  const isValid = numericAmount > 0 && numericAmount <= balanceDue + 0.01

  const handleQuickAmount = (value: number) => {
    setAmount(value.toFixed(2))
    // Auto-fill tendered as the higher of amount or value
    const tenderedValue = Math.max(value, numericAmount)
    setTendered(tenderedValue.toFixed(2))
    setErrors({})
  }

  const handleExactAmount = () => {
    setAmount(balanceDue.toFixed(2))
    setTendered(balanceDue.toFixed(2))
    setErrors({})
  }

  const handleSubmit = () => {
    const newErrors: Record<string, string> = {}

    if (numericAmount <= 0) {
      newErrors.amount = 'Amount must be greater than 0'
    } else if (numericAmount > balanceDue + 0.01) {
      newErrors.amount = `Amount cannot exceed balance due ($${balanceDue.toFixed(2)})`
    }

    if (numericTendered < numericAmount) {
      newErrors.tendered = 'Tendered amount must be at least the payment amount'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    onSubmit({
      amount: numericAmount,
      tendered: numericTendered,
      change,
    })
  }

  return (
    <div className="space-y-6">
      {/* Amount Section */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-text-secondary">
          Payment Amount ({currency})
        </label>
        <div className="relative">
          <span className="absolute left-4 top-1/2 -translate-y-1/2 text-xl text-text-secondary">
            {currency === 'USD' ? '$' : currency}
          </span>
          <input
            type="number"
            value={amount}
            onChange={(e) => {
              setAmount(e.target.value)
              setErrors((prev) => ({ ...prev, amount: '' }))
            }}
            className={cn(
              'w-full pl-12 pr-4 py-4 text-right text-3xl font-bold bg-surface-secondary border-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/30 text-text-primary transition-colors',
              errors.amount ? 'border-red-500' : 'border-surface-tertiary'
            )}
            placeholder="0.00"
            step="0.01"
            min="0.01"
            max={balanceDue}
          />
        </div>
        {errors.amount && (
          <p className="text-sm text-red-500">{errors.amount}</p>
        )}

        {/* Quick Amount Buttons */}
        <div className="grid grid-cols-3 gap-2">
          <button
            onClick={handleExactAmount}
            className="py-2 px-3 bg-surface-tertiary hover:bg-surface-tertiary/80 text-text-secondary hover:text-text-primary rounded-lg text-sm font-medium transition-colors"
          >
            Exact
          </button>
          {QUICK_AMOUNTS.map((value) => (
            <button
              key={value}
              onClick={() => handleQuickAmount(value)}
              className="py-2 px-3 bg-surface-tertiary hover:bg-surface-tertiary/80 text-text-secondary hover:text-text-primary rounded-lg text-sm font-medium transition-colors"
            >
              ${value}
            </button>
          ))}
        </div>
      </div>

      {/* Tendered Section */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-text-secondary">
          Tendered Amount ({currency})
        </label>
        <div className="relative">
          <span className="absolute left-4 top-1/2 -translate-y-1/2 text-xl text-text-secondary">
            {currency === 'USD' ? '$' : currency}
          </span>
          <input
            type="number"
            value={tendered}
            onChange={(e) => {
              setTendered(e.target.value)
              setErrors((prev) => ({ ...prev, tendered: '' }))
            }}
            className={cn(
              'w-full pl-12 pr-4 py-4 text-right text-3xl font-bold bg-surface-secondary border-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/30 text-text-primary transition-colors',
              errors.tendered ? 'border-red-500' : 'border-surface-tertiary'
            )}
            placeholder="0.00"
            step="0.01"
            min="0"
          />
        </div>
        {errors.tendered && (
          <p className="text-sm text-red-500">{errors.tendered}</p>
        )}

        {/* Quick Tendered Buttons */}
        <div className="flex flex-wrap gap-2">
          {numericAmount > 0 && [
            Math.ceil(numericAmount / 5) * 5,
            Math.ceil(numericAmount / 10) * 10,
            Math.ceil(numericAmount / 20) * 20,
          ].filter((v, i, a) => a.indexOf(v) === i && v >= numericAmount).map((value) => (
            <button
              key={value}
              onClick={() => setTendered(value.toFixed(2))}
              className="py-1.5 px-3 bg-surface-secondary hover:bg-primary/10 text-text-secondary hover:text-primary border border-surface-tertiary rounded-lg text-sm transition-colors"
            >
              ${value}
            </button>
          ))}
        </div>
      </div>

      {/* Change Display */}
      {change > 0 && (
        <div className="p-4 bg-accent-success/10 border border-accent-success/30 rounded-xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <ArrowLeftRight className="text-accent-success" size={20} />
              <span className="font-medium text-text-secondary">Change Due</span>
            </div>
            <span className="text-2xl font-bold text-accent-success">
              {currency === 'USD' ? '$' : currency}{change.toFixed(2)}
            </span>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex gap-3 pt-4">
        <Button variant="outline" className="flex-1" onClick={onCancel}>
          Cancel
        </Button>
        <Button
          className="flex-1"
          disabled={!isValid || numericTendered < numericAmount}
          onClick={handleSubmit}
        >
          <DollarSign size={18} />
          Add Cash Payment
        </Button>
      </div>
    </div>
  )
}
