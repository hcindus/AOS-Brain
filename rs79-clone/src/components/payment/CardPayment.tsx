'use client'

import { useState } from 'react'
import { cn } from '@/lib/utils'
import { CreditCard, Terminal, Check, X } from 'lucide-react'
import { Button } from '@/components/ui/Button'

interface CardPaymentProps {
  balanceDue: number
  currency: string
  onSubmit: (data: { amount: number; reference: string; authCode: string; cardType?: string }) => void
  onCancel: () => void
  onTerminalRequest?: () => Promise<{ success: boolean; refNo?: string; authCode?: string; cardType?: string }>
}

const CARD_TYPES = [
  { code: 'visa', name: 'Visa', pattern: /^4/ },
  { code: 'mastercard', name: 'Mastercard', pattern: /^5[1-5]/ },
  { code: 'amex', name: 'American Express', pattern: /^3[47]/ },
  { code: 'discover', name: 'Discover', pattern: /^6/ },
]

export function CardPayment({ balanceDue, currency, onSubmit, onCancel, onTerminalRequest }: CardPaymentProps) {
  const [amount, setAmount] = useState<string>(balanceDue.toFixed(2))
  const [reference, setReference] = useState('')
  const [authCode, setAuthCode] = useState('')
  const [cardType, setCardType] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isTerminalMode, setIsTerminalMode] = useState(false)
  const [terminalStatus, setTerminalStatus] = useState<'idle' | 'processing' | 'success' | 'error'>('idle')

  const numericAmount = parseFloat(amount) || 0

  const detectCardType = (ref: string) => {
    const digits = ref.replace(/\D/g, '')
    for (const type of CARD_TYPES) {
      if (type.pattern.test(digits)) {
        return type.code
      }
    }
    return 'unknown'
  }

  const handleTerminalPayment = async () => {
    setIsTerminalMode(true)
    setTerminalStatus('processing')

    try {
      if (onTerminalRequest) {
        const result = await onTerminalRequest()
        if (result.success) {
          setReference(result.refNo || '')
          setAuthCode(result.authCode || '')
          setCardType(result.cardType || 'unknown')
          setTerminalStatus('success')
        } else {
          setTerminalStatus('error')
        }
      } else {
        // Simulate terminal processing
        await new Promise((resolve) => setTimeout(resolve, 2000))
        setReference(`TERM-${Date.now()}`)
        setAuthCode(`AUTH-${Math.floor(Math.random() * 1000000)}`)
        setCardType('visa')
        setTerminalStatus('success')
      }
    } catch {
      setTerminalStatus('error')
    }
  }

  const handleReferenceChange = (value: string) => {
    setReference(value)
    setCardType(detectCardType(value))
    setErrors((prev) => ({ ...prev, reference: '' }))
  }

  const handleSubmit = () => {
    const newErrors: Record<string, string> = {}

    if (numericAmount <= 0) {
      newErrors.amount = 'Amount must be greater than 0'
    } else if (numericAmount > balanceDue + 0.01) {
      newErrors.amount = `Amount cannot exceed balance due ($${balanceDue.toFixed(2)})`
    }

    if (!reference.trim()) {
      newErrors.reference = 'Reference number (last 4 digits) is required'
    }

    if (!authCode.trim()) {
      newErrors.authCode = 'Authorization code is required'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    onSubmit({
      amount: numericAmount,
      reference,
      authCode,
      cardType,
    })
  }

  if (isTerminalMode) {
    return (
      <div className="space-y-6">
        <div className="p-6 bg-surface-secondary rounded-xl text-center">
          {terminalStatus === 'processing' && (
            <>
              <div className="w-16 h-16 mx-auto mb-4 border-4 border-primary/30 border-t-primary rounded-full animate-spin" />
              <p className="text-lg font-medium text-text-primary">Processing card payment...\u003c/p>
              <p className="text-sm text-text-secondary mt-2">Please follow prompts on terminal</p>
            </>
          )}
          {terminalStatus === 'success' && (
            <>
              <div className="w-16 h-16 mx-auto mb-4 bg-accent-success rounded-full flex items-center justify-center">
                <Check className="text-white" size={32} />
              </div>
              <p className="text-lg font-medium text-accent-success">Payment Approved!</p>
              <p className="text-sm text-text-secondary mt-2">Auth Code: {authCode}</p>
              <div className="mt-6">
                <Button onClick={handleSubmit} className="w-full">
                  Add Payment to Order
                </Button>
              </div>
            </>
          )}
          {terminalStatus === 'error' && (
            <>
              <div className="w-16 h-16 mx-auto mb-4 bg-red-500 rounded-full flex items-center justify-center">
                <X className="text-white" size={32} />
              </div>
              <p className="text-lg font-medium text-red-500">Payment Failed</p>
              <p className="text-sm text-text-secondary mt-2">Please try again or use manual entry</p>
              <div className="mt-6 flex gap-3">
                <Button variant="outline" onClick={() => setIsTerminalMode(false)} className="flex-1">
                  Manual Entry
                </Button>
                <Button onClick={handleTerminalPayment} className="flex-1">
                  Retry
                </Button>
              </div>
            </>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Amount Section */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-text-secondary">Amount ({currency})</label>
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
        {errors.amount && <p className="text-sm text-red-500">{errors.amount}</p>}
      </div>

      {/* Terminal Integration */}
      <div className="p-4 border-2 border-dashed border-surface-tertiary rounded-xl">
        <div className="flex items-center gap-3 mb-3">
          <Terminal className="text-primary" size={24} />
          <div>
            <p className="font-medium text-text-primary">Terminal Integration</p>
            <p className="text-sm text-text-secondary">Connect to payment terminal</p>
          </div>
        </div>
        <Button variant="outline" className="w-full" onClick={handleTerminalPayment}>
          <CreditCard size={18} className="mr-2" />
          Process on Terminal
        </Button>
      </div>

      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-surface-tertiary" />
        </div>
        <div className="relative flex justify-center text-sm">
          <span className="px-2 bg-white text-text-secondary">Or Manual Entry</span>
        </div>
      </div>

      {/* Manual Entry Fields */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-text-secondary mb-1">
            Last 4 Digits or Reference
          </label>
          <input
            type="text"
            value={reference}
            onChange={(e) => handleReferenceChange(e.target.value)}
            maxLength={4}
            className={cn(
              'w-full px-4 py-3 bg-white border-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/30 text-text-primary transition-colors',
              errors.reference ? 'border-red-500' : 'border-surface-tertiary'
            )}
            placeholder="••••"
          />
          {cardType && cardType !== 'unknown' && (
            <p className="text-xs text-text-secondary mt-1 capitalize">Detected: {cardType}</p>
          )}
          {errors.reference && <p className="text-sm text-red-500">{errors.reference}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-text-secondary mb-1">
            Authorization Code
          </label>
          <input
            type="text"
            value={authCode}
            onChange={(e) => {
              setAuthCode(e.target.value)
              setErrors((prev) => ({ ...prev, authCode: '' }))
            }}
            className={cn(
              'w-full px-4 py-3 bg-white border-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/30 text-text-primary transition-colors',
              errors.authCode ? 'border-red-500' : 'border-surface-tertiary'
            )}
            placeholder="Enter auth code..."
          />
          {errors.authCode && <p className="text-sm text-red-500">{errors.authCode}</p>}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3 pt-4">
        <Button variant="outline" className="flex-1" onClick={onCancel}>
          Cancel
        </Button>
        <Button className="flex-1" onClick={handleSubmit}>
          <CreditCard size={18} />
          Add Card Payment
        </Button>
      </div>
    </div>
  )
}
