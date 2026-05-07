'use client'

import { useState, useMemo, useEffect } from 'react'
import { cn } from '@/lib/utils'
import { X, DollarSign, CreditCard, Bitcoin, Gift, Building2, Wallet, Check, ChevronRight, ChevronLeft } from 'lucide-react'
import type { PaymentType, Payment } from '@/types'

interface PaymentModalProps {
  isOpen: boolean
  onClose: () => void
  onSubmit: (payment: Payment) => void
  onCompleteOrder: () => void
  total: number
  amountPaid: number
  currency: string
  availableCurrencies?: { code: string; name: string; rate: number }[]
}

const paymentMethods: { type: PaymentType; label: string; icon: React.ReactNode }[] = [
  { type: 'cash', label: 'Cash', icon: <DollarSign size={20} /> },
  { type: 'card', label: 'Card', icon: <CreditCard size={20} /> },
  { type: 'crypto', label: 'Crypto', icon: <Bitcoin size={20} /> },
  { type: 'storecredit', label: 'Store Credit', icon: <Wallet size={20} /> },
  { type: 'giftcard', label: 'Gift Card', icon: <Gift size={20} /> },
  { type: 'check', label: 'Check', icon: <Building2 size={20} /> },
]

export function PaymentModal({
  isOpen,
  onClose,
  onSubmit,
  onCompleteOrder,
  total,
  amountPaid,
  currency,
  availableCurrencies = [{ code: 'USD', name: 'US Dollar', rate: 1 }],
}: PaymentModalProps) {
  const [selectedMethod, setSelectedMethod] = useState<PaymentType>('cash')
  const [amount, setAmount] = useState('')
  const [selectedCurrency, setSelectedCurrency] = useState(currency)
  const [step, setStep] = useState<'method' | 'amount' | 'confirm'>('method')
  const [reference, setReference] = useState('')

  const balanceDue = useMemo(() => total - amountPaid, [total, amountPaid])
  const numericAmount = parseFloat(amount) || 0

  useEffect(() => {
    if (isOpen) {
      setAmount(balanceDue.toFixed(2))
      setSelectedCurrency(currency)
      setStep('method')
      setReference('')
    }
  }, [isOpen, balanceDue, currency])

  const currencyRate = availableCurrencies.find(c => c.code === selectedCurrency)?.rate || 1
  const amountInUsd = numericAmount / currencyRate

  const handleSubmit = () => {
    if (numericAmount <= 0) return

    const payment: Payment = {
      type: selectedMethod,
      amountUsd: amountInUsd,
      amountNative: numericAmount,
      currency: selectedCurrency,
      currencyRate,
      reference: reference || undefined,
    }

    onSubmit(payment)
    setAmount('')
    setReference('')
  }

  const handleComplete = () => {
    onCompleteOrder()
    onClose()
  }

  const handleQuickAmount = (value: number) => {
    setAmount(value.toFixed(2))
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div className="w-full max-w-lg bg-white rounded-2xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-surface-tertiary">
          <div className="flex items-center gap-3">
            {step !== 'method' && (
              <button
                onClick={() => setStep(step === 'confirm' ? 'amount' : 'method')}
                className="p-1 -ml-1 text-text-secondary hover:text-text-primary rounded-lg transition-colors"
              >
                <ChevronLeft size={20} />
              </button>
            )}
            <h2 className="text-lg font-bold text-text-primary">
              {step === 'method' && 'Select Payment Method'}
              {step === 'amount' && 'Enter Amount'}
              {step === 'confirm' && 'Confirm Payment'}
            </h2>
          </div>
          
          <button
            onClick={onClose}
            className="p-2 text-text-secondary hover:text-text-primary hover:bg-surface-secondary rounded-lg transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Balance Summary */}
        <div className="px-6 py-4 bg-surface-secondary border-b border-surface-tertiary">
          <div className="flex justify-between items-center">
            <span className="text-text-secondary">Total</span>
            <span className="text-lg font-semibold text-text-primary">{currency} {total.toFixed(2)}</span>
          </div>
          <div className="flex justify-between items-center mt-1">
            <span className="text-text-secondary">Paid</span>
            <span className="text-text-secondary">{currency} {amountPaid.toFixed(2)}</span>
          </div>
          <div className="flex justify-between items-center mt-2 pt-2 border-t border-surface-tertiary">
            <span className="font-medium text-text-primary">Balance Due</span>
            <span className="text-xl font-bold text-accent-success">{currency} {balanceDue.toFixed(2)}</span>
          </div>
        </div>

        {/* Step Content */}
        <div className="p-6">
          {step === 'method' && (
            <div className="grid grid-cols-2 gap-3">
              {paymentMethods.map((method) => (
                <button
                  key={method.type}
                  onClick={() => {
                    setSelectedMethod(method.type)
                    setStep('amount')
                  }}
                  className={cn(
                    'flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all duration-150',
                    selectedMethod === method.type
                      ? 'border-primary bg-primary/5 text-primary'
                      : 'border-surface-tertiary text-text-secondary hover:border-primary/50 hover:bg-surface-secondary'
                  )}
                >
                  {method.icon}
                  <span className="font-medium">{method.label}</span>
                </button>
              ))}
            </div>
          )}

          {step === 'amount' && (
            <div className="space-y-4">
              {/* Currency Selector */}
              <div className="flex gap-2">
                {availableCurrencies.map((curr) => (
                  <button
                    key={curr.code}
                    onClick={() => {
                      setSelectedCurrency(curr.code)
                      setAmount((parseFloat(amount) * (currencyRate / curr.rate) || 0).toFixed(2))
                    }}
                    className={cn(
                      'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                      selectedCurrency === curr.code
                        ? 'bg-primary text-white'
                        : 'bg-surface-tertiary text-text-secondary hover:bg-surface-tertiary/80'
                    )}
                  >
                    {curr.code}
                  </button>
                ))}
              </div>

              {/* Amount Input */}
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-2xl text-text-secondary">{selectedCurrency}</span>
                <input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  className="w-full pl-16 pr-4 py-4 text-right text-3xl font-bold bg-surface-secondary border border-surface-tertiary rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/30 text-text-primary"
                  placeholder="0.00"
                  step="0.01"
                  min="0"
                  max={balanceDue.toFixed(2)}
                />
              </div>

              {/* Quick Amounts */}
              <div className="grid grid-cols-4 gap-2">
                {[5, 10, 20, 50, 100, 'Exact'].map((val) => (
                  <button
                    key={val}
                    onClick={() => handleQuickAmount(val === 'Exact' ? balanceDue : val as number)}
                    className="py-2 px-3 bg-surface-tertiary text-text-secondary hover:bg-surface-tertiary/80 rounded-lg text-sm font-medium transition-colors"
                  >
                    {val === 'Exact' ? 'Exact' : `$${val}`}
                  </button>
                ))}
              </div>

              {/* Reference (for non-cash) */}
              {selectedMethod !== 'cash' && (
                <input
                  type="text"
                  value={reference}
                  onChange={(e) => setReference(e.target.value)}
                  placeholder={
                    selectedMethod === 'card' ? 'Last 4 digits or reference...' :
                    selectedMethod === 'check' ? 'Check number...' :
                    selectedMethod === 'giftcard' ? 'Gift card code...' :
                    'Reference...'
                  }
                  className="w-full px-4 py-3 bg-white border border-surface-tertiary rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/30 text-text-primary"
                />
              )}

              <button
                onClick={() => setStep('confirm')}
                disabled={numericAmount <= 0 || numericAmount > balanceDue}
                className={cn(
                  'w-full py-4 rounded-xl font-bold text-lg flex items-center justify-center gap-2 transition-all duration-150',
                  numericAmount > 0 && numericAmount <= balanceDue
                    ? 'bg-primary text-white hover:bg-primary-dark shadow-lg shadow-primary/25 active:scale-[0.98]'
                    : 'bg-surface-tertiary text-text-muted cursor-not-allowed'
                )}
              >
                Continue
                <ChevronRight size={20} />
              </button>
            </div>
          )}

          {step === 'confirm' && (
            <div className="space-y-4">
              <div className="bg-surface-secondary rounded-xl p-4 space-y-2">
                <div className="flex justify-between">
                  <span className="text-text-secondary">Method</span>
                  <span className="font-medium text-text-primary">
                    {paymentMethods.find(m => m.type === selectedMethod)?.label}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-secondary">Amount</span>
                  <span className="font-medium text-text-primary">
                    {selectedCurrency} {numericAmount.toFixed(2)}
                  </span>
                </div>
                {selectedCurrency !== 'USD' && (
                  <div className="flex justify-between text-sm">
                    <span className="text-text-muted">USD Equivalent</span>
                    <span className="text-text-secondary">${amountInUsd.toFixed(2)}</span>
                  </div>
                )}
                {reference && (
                  <div className="flex justify-between">
                    <span className="text-text-secondary">Reference</span>
                    <span className="font-medium text-text-primary">{reference}</span>
                  </div>
                )}
              </div>

              <button
                onClick={handleSubmit}
                className="w-full py-4 rounded-xl font-bold text-lg bg-accent-success text-white hover:bg-green-600 shadow-lg shadow-green-500/25 active:scale-[0.98] transition-all duration-150 flex items-center justify-center gap-2"
              >
                <Check size={20} />
                Confirm Payment
              </button>
            </div>
          )}
        </div>

        {/* Footer */}
        {amountPaid > 0 && balanceDue <= 0 && (
          <div className="px-6 py-4 border-t border-surface-tertiary bg-surface-secondary">
            <button
              onClick={handleComplete}
              className="w-full py-3 rounded-xl font-bold text-lg bg-accent-success text-white hover:bg-green-600 shadow-lg shadow-green-500/25 active:scale-[0.98] transition-all duration-150 flex items-center justify-center gap-2"
            >
              <Check size={20} />
              Complete Order
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
