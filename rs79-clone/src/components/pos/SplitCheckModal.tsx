'use client'

import { useState } from 'react'
import { cn } from '@/lib/utils'
import type { CartItem } from '@/types'

interface SplitCheckModalProps {
  isOpen: boolean
  onClose: () => void
  items: CartItem[]
  subtotal: number
  tax: number
  total: number
  onSplitComplete: (splits: { checks: SplitCheck[] }) => void
}

interface SplitCheck {
  id: number
  name: string
  items: CartItem[]
  subtotal: number
  tax: number
  total: number
}

export function SplitCheckModal({
  isOpen,
  onClose,
  items,
  subtotal,
  tax,
  total,
  onSplitComplete,
}: SplitCheckModalProps) {
  const [splitType, setSplitType] = useState<'even' | 'byItem'>('even')
  const [numChecks, setNumChecks] = useState(2)
  const [itemAssignments, setItemAssignments] = useState<Record<string, number[]>>({})
  const [step, setStep] = useState(1)

  if (!isOpen) return null

  const handleNumChecksChange = (value: number) => {
    if (value >= 2 && value <= 10) {
      setNumChecks(value)
    }
  }

  const handleItemCheckToggle = (itemId: string, checkId: number) => {
    setItemAssignments((prev) => {
      const currentChecks = prev[itemId] || []
      const newChecks = currentChecks.includes(checkId)
        ? currentChecks.filter((id) => id !== checkId)
        : [...currentChecks, checkId]
      return { ...prev, [itemId]: newChecks }
    })
  }

  const calculateEvenSplits = (): SplitCheck[] => {
    const splits: SplitCheck[] = []
    const itemsPerCheck = Math.ceil(items.length / numChecks)
    const taxPerCheck = tax / numChecks
    const totalPerCheck = subtotal / numChecks + taxPerCheck

    for (let i = 0; i < numChecks; i++) {
      const checkItems = items.slice(i * itemsPerCheck, (i + 1) * itemsPerCheck)
      const checkSubtotal = checkItems.reduce((sum, item) => sum + item.lineTotal, 0)

      splits.push({
        id: i + 1,
        name: `Check ${i + 1}`,
        items: checkItems,
        subtotal: checkSubtotal,
        tax: taxPerCheck,
        total: checkSubtotal + taxPerCheck,
      })
    }
    return splits
  }

  const calculateByItemSplits = (): SplitCheck[] => {
    const splits: SplitCheck[] = []

    for (let i = 1; i <= numChecks; i++) {
      const checkItems = items.filter((item) => itemAssignments[item.itemId]?.includes(i))
      const checkSubtotal = checkItems.reduce((sum, item) => sum + item.lineTotal, 0)
      const checkTax = subtotal > 0 ? (checkSubtotal / subtotal) * tax : 0

      splits.push({
        id: i,
        name: `Check ${i}`,
        items: checkItems,
        subtotal: checkSubtotal,
        tax: checkTax,
        total: checkSubtotal + checkTax,
      })
    }
    return splits
  }

  const handleConfirm = () => {
    const splits = splitType === 'even' ? calculateEvenSplits() : calculateByItemSplits()
    onSplitComplete({ checks: splits })
    onClose()
  }

  const canProceed =
    splitType === 'even' ||
    Object.values(itemAssignments).some((checks) => checks.length > 0)

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-2xl max-h-[90vh] overflow-auto bg-white rounded-2xl shadow-2xl">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b p-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-text-primary">Split Check</h2>
            <button
              onClick={onClose}
              className="text-text-secondary hover:text-text-primary transition-colors"
            >
              ✕
            </button>
          </div>
        </div>

        <div className="p-6 space-y-6">
          {/* Step 1: Choose split method */}
          {step === 1 && (
            <>
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-text-primary">Choose Split Method</h3>
                <div className="grid grid-cols-2 gap-4">
                  <button
                    onClick={() => setSplitType('even')}
                    className={cn(
                      'p-6 rounded-xl border-2 text-left transition-all',
                      splitType === 'even'
                        ? 'border-primary bg-primary/5'
                        : 'border-surface-tertiary hover:border-primary/50'
                    )}
                  >
                    <div className="font-semibold text-text-primary mb-2">Even Split</div>
                    <div className="text-sm text-text-secondary">
                      Divide all items equally among checks
                    </div>
                  </button>
                  <button
                    onClick={() => setSplitType('byItem')}
                    className={cn(
                      'p-6 rounded-xl border-2 text-left transition-all',
                      splitType === 'byItem'
                        ? 'border-primary bg-primary/5'
                        : 'border-surface-tertiary hover:border-primary/50'
                    )}
                  >
                    <div className="font-semibold text-text-primary mb-2">By Item</div>
                    <div className="text-sm text-text-secondary">
                      Assign specific items to each check
                    </div>
                  </button>
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-text-primary">Number of Checks</label>
                <div className="flex items-center gap-4">
                  <button
                    onClick={() => handleNumChecksChange(numChecks - 1)}
                    disabled={numChecks <= 2}
                    className="w-10 h-10 rounded-lg border border-surface-tertiary text-text-primary hover:bg-surface-secondary disabled:opacity-50"
                  >
                    -
                  </button>
                  <span className="text-2xl font-bold text-text-primary w-12 text-center">
                    {numChecks}
                  </span>
                  <button
                    onClick={() => handleNumChecksChange(numChecks + 1)}
                    disabled={numChecks >= 10}
                    className="w-10 h-10 rounded-lg border border-surface-tertiary text-text-primary hover:bg-surface-secondary disabled:opacity-50"
                  >
                    +
                  </button>
                </div>
              </div>

              <button
                onClick={() => setStep(2)}
                className="w-full py-3 bg-primary text-white font-semibold rounded-xl hover:bg-primary-dark transition-colors"
              >
                Continue
              </button>
            </>
          )}

          {/* Step 2: Assign items (if byItem) or confirm */}
          {step === 2 && (
            <>
              {splitType === 'byItem' ? (
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-text-primary">Assign Items to Checks</h3>
                  <div className="text-sm text-text-secondary mb-4">
                    Click check numbers to assign each item
                  </div>
                  <div className="space-y-2">
                    {items.map((item) => (
                      <div
                        key={item.itemId}
                        className="flex items-center justify-between p-4 bg-surface-secondary rounded-xl"
                      >
                        <div className="flex-1">
                          <div className="font-medium text-text-primary">{item.name}</div>
                          <div className="text-sm text-text-secondary">
                            Qty: {item.qty} × ${item.price.toFixed(2)} = ${item.lineTotal.toFixed(2)}
                          </div>
                        </div>
                        <div className="flex gap-2">
                          {Array.from({ length: numChecks }, (_, i) => i + 1).map((checkId) => (
                            <button
                              key={checkId}
                              onClick={() => handleItemCheckToggle(item.itemId, checkId)}
                              className={cn(
                                'w-8 h-8 rounded-lg text-sm font-semibold transition-all',
                                itemAssignments[item.itemId]?.includes(checkId)
                                  ? 'bg-primary text-white'
                                  : 'bg-white border border-surface-tertiary text-text-secondary hover:border-primary'
                              )}
                            >
                              {checkId}
                            </button>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-text-primary">Split Preview</h3>
                  <div className="grid gap-4">
                    {calculateEvenSplits().map((split) => (
                      <div key={split.id} className="p-4 bg-surface-secondary rounded-xl">
                        <div className="font-semibold text-text-primary mb-2">{split.name}</div>
                        <div className="text-sm text-text-secondary mb-2">
                          {split.items.length} items
                        </div>
                        <div className="space-y-1 text-sm">
                          <div className="flex justify-between">
                            <span>Subtotal:</span>
                            <span>${split.subtotal.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Tax:</span>
                            <span>${split.tax.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between font-semibold text-text-primary">
                            <span>Total:</span>
                            <span>${split.total.toFixed(2)}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="flex gap-3">
                <button
                  onClick={() => setStep(1)}
                  className="flex-1 py-3 border border-surface-tertiary text-text-primary font-semibold rounded-xl hover:bg-surface-secondary transition-colors"
                >
                  Back
                </button>
                <button
                  onClick={handleConfirm}
                  disabled={!canProceed}
                  className={cn(
                    'flex-1 py-3 font-semibold rounded-xl transition-colors',
                    canProceed
                      ? 'bg-primary text-white hover:bg-primary-dark'
                      : 'bg-surface-tertiary text-text-muted cursor-not-allowed'
                  )}
                >
                  Confirm Split
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
