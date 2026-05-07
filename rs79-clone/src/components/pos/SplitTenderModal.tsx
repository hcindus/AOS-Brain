'use client'

import { useState } from 'react'
import { cn } from '@/lib/utils'

interface SplitTenderModalProps {
  isOpen: boolean
  onClose: () => void
  totalDue: number
  onPaymentComplete: (result: { payments: Payment[]; change: number }) => void
}

interface Payment {
  type: 'cash' | 'card' | 'crypto' | 'storecredit' | 'giftcard' | 'check'
  amount: number
  reference?: string
}

const paymentTypes = [
  { id: 'cash', name: 'Cash', icon: '💵' },
  { id: 'card', name: 'Card', icon: '💳' },
  { id: 'crypto', name: 'Crypto', icon: '₿' },
  { id: 'storecredit', name: 'Store Credit', icon: '💰' },
  { id: 'giftcard', name: 'Gift Card', icon: '🎁' },
  { id: 'check', name: 'Check', icon: '📝' },
]

export function SplitTenderModal({ isOpen, onClose, totalDue, onPaymentComplete }: SplitTenderModalProps) {
  const [payments, setPayments] = useState<Payment[]>([])
  const [selectedType, setSelectedType] = useState<Payment['type']>('cash')
  const [amount, setAmount] = useState('')
  const [reference, setReference] = useState('')
  const [giftCardCode, setGiftCardCode] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)

  if (!isOpen) return null

  const totalPaid = payments.reduce((sum, p) => sum + p.amount, 0)
  const remainingBalance = Math.max(0, totalDue - totalPaid)
  const changeDue = Math.max(0, totalPaid - totalDue)

  const handleAddPayment = () => {
    const paymentAmount = parseFloat(amount)
    if (isNaN(paymentAmount) || paymentAmount <= 0) return

    const newPayment: Payment = {
      type: selectedType,
      amount: paymentAmount,
      reference: selectedType === 'check' ? reference : selectedType === 'card' ? reference : undefined,
    }

    setPayments([...payments, newPayment])
    setAmount('')
    setReference('')
    setGiftCardCode('')
  }

  const handleRemovePayment = (index: number) => {
    setPayments(payments.filter((_, i) => i !== index))
  }

  const handleComplete = async () => {
    setIsProcessing(true)
    try {
      onPaymentComplete({ payments, change: changeDue })
      setPayments([])
      onClose()
    } finally {
      setIsProcessing(false)
    }
  }

  const quickAmounts = [5, 10, 20, 50, 100].filter(a => a <= remainingBalance * 2 || a <= 100)

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-lg bg-white rounded-2xl shadow-2xl">
        <div className="p-6 border-b">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-text-primary">Split Tender</h2>
            <button onClick={onClose} className="text-text-secondary hover:text-text-primary">✕</button>
          </div>
        </div>

        <div className="p-6 space-y-6">
          {/* Balance Display */}
          <div className="bg-surface-secondary rounded-xl p-4">
            <div className="flex justify-between items-center mb-2">
              <span className="text-text-secondary">Total Due:</span>
              <span className="text-xl font-bold text-text-primary">${totalDue.toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-text-secondary">Total Paid:</span>
              <span className="text-lg font-semibold text-primary">${totalPaid.toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center pt-2 border-t">
              <span className="font-medium text-text-primary">{remainingBalance > 0 ? 'Balance Due:' : 'Change Due:'}</span>
              <span className={`text-xl font-bold ${remainingBalance > 0 ? 'text-accent-danger' : 'text-success'}`}>
                ${(remainingBalance > 0 ? remainingBalance : changeDue).toFixed(2)}
              </span>
            </div>
          </div>

          {/* Existing Payments */}
          {payments.length > 0 && (
            <div className="space-y-2">
              <h3 className="font-semibold text-text-primary">Payments</h3>
              {payments.map((payment, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-surface-secondary rounded-lg">
                  <div className="flex items-center gap-2">
                    <span>{paymentTypes.find(t => t.id === payment.type)?.icon}</span>
                    <span className="font-medium text-text-primary capitalize">{payment.type}</span>
                    {payment.reference && <span className="text-sm text-text-secondary">({payment.reference})</span>}
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="font-semibold text-text-primary">${payment.amount.toFixed(2)}</span>
                    <button onClick={() => handleRemovePayment(index)} className="text-accent-danger hover:opacity-70">✕</button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Add Payment Form */}
          {remainingBalance > 0 && (
            <div className="space-y-4">
              <h3 className="font-semibold text-text-primary">Add Payment</h3>
              
              {/* Payment Type Selection */}
              <div className="grid grid-cols-3 gap-2">
                {paymentTypes.map((type) => (
                  <button
                    key={type.id}
                    onClick={() => setSelectedType(type.id as Payment['type'])}
                    className={cn(
                      'p-3 rounded-lg border-2 text-sm font-medium transition-all',
                      selectedType === type.id
                        ? 'border-primary bg-primary/5 text-primary'
                        : 'border-surface-tertiary text-text-secondary hover:border-primary/50'
                    )}
                  >
                    <span className="block text-lg mb-1">{type.icon}</span>
                    {type.name}
                  </button>
                ))}
              </div>

              {/* Amount Input */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-text-primary">Amount</label>
                <div className="flex gap-2">
                  <div className="relative flex-1">
                    <span className="absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary">$</span>
                    <input
                      type="number"
                      value={amount}
                      onChange={(e) => setAmount(e.target.value)}
                      placeholder={remainingBalance.toFixed(2)}
                      className="w-full pl-8 pr-4 py-3 border border-surface-tertiary rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                    />
                  </div>
                  <button
                    onClick={() => setAmount(remainingBalance.toFixed(2))}
                    className="px-4 py-2 bg-surface-secondary text-text-primary rounded-xl hover:bg-surface-tertiary transition-colors"
                  >
                    Balance
                  </button>
                </div>
                <div className="flex gap-2">
                  {quickAmounts.map((amt) => (
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

              {/* Reference Field for Check/Card */}
              {(selectedType === 'check' || selectedType === 'card') && (
                <div className="space-y-2">
                  <label className="text-sm font-medium text-text-primary">
                    {selectedType === 'check' ? 'Check Number' : 'Auth Code'}
                  </label>
                  <input
                    type="text"
                    value={reference}
                    onChange={(e) => setReference(e.target.value)}
                    className="w-full px-4 py-3 border border-surface-tertiary rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                  />
                </div>
              )}

              {/* Gift Card Code */}
              {selectedType === 'giftcard' && (
                <div className="space-y-2">
                  <label className="text-sm font-medium text-text-primary">Gift Card Code</label>
                  <input
                    type="text"
                    value={giftCardCode}
                    onChange={(e) => setGiftCardCode(e.target.value.toUpperCase())}
                    placeholder="GIFT-XXXX-XXXX-XXXX"
                    className="w-full px-4 py-3 border border-surface-tertiary rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none uppercase"
                  />
                </div>
              )}

              <button
                onClick={handleAddPayment}
                disabled={!amount || parseFloat(amount) <= 0}
                className={cn(
                  'w-full py-3 font-semibold rounded-xl transition-colors',
                  amount && parseFloat(amount) > 0
                    ? 'bg-primary text-white hover:bg-primary-dark'
                    : 'bg-surface-tertiary text-text-muted cursor-not-allowed'
                )}
              >
                Add Payment
              </button>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex gap-3">
            <button
              onClick={onClose}
              className="flex-1 py-3 border border-surface-tertiary text-text-primary font-semibold rounded-xl hover:bg-surface-secondary transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleComplete}
              disabled={payments.length === 0 || isProcessing}
              className={cn(
                'flex-1 py-3 font-semibold rounded-xl transition-colors',
                payments.length > 0 && !isProcessing
                  ? 'bg-success text-white hover:bg-success/90'
                  : 'bg-surface-tertiary text-text-muted cursor-not-allowed'
              )}
            >
              {isProcessing ? 'Processing...' : 'Complete'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
