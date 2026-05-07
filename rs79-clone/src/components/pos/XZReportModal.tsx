'use client'

import { useState } from 'react'
import { cn } from '@/lib/utils'

interface XZReportModalProps {
  isOpen: boolean
  onClose: () => void
  onGenerateXReport: () => Promise<ReportData>
  onGenerateZReport: () => Promise<ReportData>
  onPrint: (report: ReportData) => void
}

interface ReportData {
  reportType: 'X' | 'Z'
  generatedAt: string
  grossSales: number
  netSales: number
  taxCollected: number
  discounts: number
  refunds: number
  voids: number
  orderCount: number
  itemCount: number
  averageOrderValue: number
  paymentSummary: Array<{ type: string; count: number; amount: number }>
  clerkSummary: Array<{
    clerkName: string
    role: string
    orderCount: number
    totalSales: number
  }>
  voidDetails: Array<{
    transactionNo: number
    clerkName: string
    amount: number
    reason: string
  }>
}

export function XZReportModal({
  isOpen,
  onClose,
  onGenerateXReport,
  onGenerateZReport,
  onPrint,
}: XZReportModalProps) {
  const [report, setReport] = useState<ReportData | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [activeTab, setActiveTab] = useState<'summary' | 'payments' | 'clerks' | 'voids'>('summary')

  if (!isOpen) return null

  const handleGenerateX = async () => {
    setIsLoading(true)
    try {
      const data = await onGenerateXReport()
      setReport(data)
    } finally {
      setIsLoading(false)
    }
  }

  const handleGenerateZ = async () => {
    if (!confirm('Generate Z-Report? This will reset shift counters.')) return
    setIsLoading(true)
    try {
      const data = await onGenerateZReport()
      setReport(data)
    } finally {
      setIsLoading(false)
    }
  }

  const formatCurrency = (amount: number) => `$${amount.toFixed(2)}`

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-4xl max-h-[90vh] overflow-auto bg-white rounded-2xl shadow-2xl">
        <div className="sticky top-0 bg-white border-b p-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-text-primary">X/Z Reports</h2>
            <button onClick={onClose} className="text-text-secondary hover:text-text-primary">✕</button>
          </div>

          {!report && (
            <div className="flex gap-3 mt-4">
              <button
                onClick={handleGenerateX}
                disabled={isLoading}
                className="flex-1 py-3 bg-primary text-white font-semibold rounded-xl hover:bg-primary-dark transition-colors"
              >
                Generate X-Report (Current Shift)
              </button>
              <button
                onClick={handleGenerateZ}
                disabled={isLoading}
                className="flex-1 py-3 bg-accent-danger text-white font-semibold rounded-xl hover:bg-accent-danger/90 transition-colors"
              >
                Generate Z-Report (End of Day)
              </button>
            </div>
          )}
        </div>

        {report && (
          <div className="p-6 space-y-6">
            {/* Report Header */}
            <div className="bg-surface-secondary rounded-xl p-4">
              <div className="flex items-center justify-between">
                <div>
                  <span
                    className={cn(
                      'inline-block px-3 py-1 rounded-full text-sm font-bold',
                      report.reportType === 'X'
                        ? 'bg-primary/10 text-primary'
                        : 'bg-accent-danger/10 text-accent-danger'
                    )}
                  >
                    {report.reportType}-REPORT
                  </span>
                  <p className="text-sm text-text-secondary mt-2">
                    Generated: {new Date(report.generatedAt).toLocaleString()}
                  </p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => onPrint(report)}
                    className="px-4 py-2 bg-surface-tertiary text-text-primary rounded-lg hover:bg-surface-secondary transition-colors"
                  >
                    Print
                  </button>
                  <button
                    onClick={() => setReport(null)}
                    className="px-4 py-2 border border-surface-tertiary text-text-primary rounded-lg hover:bg-surface-secondary transition-colors"
                  >
                    New Report
                  </button>
                </div>
              </div>
            </div>

            {/* Navigation Tabs */}
            <div className="flex border-b">
              {[
                { id: 'summary', label: 'Summary' },
                { id: 'payments', label: 'Payments' },
                { id: 'clerks', label: 'By Clerk' },
                { id: 'voids', label: 'Voids' },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as typeof activeTab)}
                  className={cn(
                    'px-6 py-3 font-medium transition-colors',
                    activeTab === tab.id
                      ? 'border-b-2 border-primary text-primary'
                      : 'text-text-secondary hover:text-text-primary'
                  )}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Summary Tab */}
            {activeTab === 'summary' && (
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-surface-secondary rounded-xl p-4">
                  <div className="text-sm text-text-secondary mb-1">Gross Sales</div>
                  <div className="text-2xl font-bold text-text-primary">{formatCurrency(report.grossSales)}</div>
                </div>
                <div className="bg-surface-secondary rounded-xl p-4">
                  <div className="text-sm text-text-secondary mb-1">Net Sales</div>
                  <div className="text-2xl font-bold text-success">{formatCurrency(report.netSales)}</div>
                </div>
                <div className="bg-surface-secondary rounded-xl p-4">
                  <div className="text-sm text-text-secondary mb-1">Tax Collected</div>
                  <div className="text-2xl font-bold text-text-primary">{formatCurrency(report.taxCollected)}</div>
                </div>
                <div className="bg-surface-secondary rounded-xl p-4">
                  <div className="text-sm text-text-secondary mb-1">Total Orders</div>
                  <div className="text-2xl font-bold text-text-primary">{report.orderCount}</div>
                </div>
                <div className="bg-surface-secondary rounded-xl p-4">
                  <div className="text-sm text-text-secondary mb-1">Items Sold</div>
                  <div className="text-2xl font-bold text-text-primary">{report.itemCount}</div>
                </div>
                <div className="bg-surface-secondary rounded-xl p-4">
                  <div className="text-sm text-text-secondary mb-1">Average Order</div>
                  <div className="text-2xl font-bold text-text-primary">{formatCurrency(report.averageOrderValue)}</div>
                </div>
                <div className="bg-accent-danger/5 rounded-xl p-4">
                  <div className="text-sm text-accent-danger mb-1">Discounts</div>
                  <div className="text-2xl font-bold text-accent-danger">{formatCurrency(report.discounts)}</div>
                </div>
                <div className="bg-accent-danger/5 rounded-xl p-4">
                  <div className="text-sm text-accent-danger mb-1">Voids</div>
                  <div className="text-2xl font-bold text-accent-danger">{formatCurrency(report.voids)}</div>
                </div>
              </div>
            )}

            {/* Payments Tab */}
            {activeTab === 'payments' && (
              <div className="space-y-2">
                {report.paymentSummary.length === 0 ? (
                  <p className="text-text-secondary text-center py-8">No payments recorded</p>
                ) : (
                  report.paymentSummary.map((payment) => (
                    <div
                      key={payment.type}
                      className="flex items-center justify-between p-4 bg-surface-secondary rounded-xl"
                    >
                      <div className="flex items-center gap-3">
                        <span className="font-medium text-text-primary capitalize">{payment.type}</span>
                        <span className="text-sm text-text-secondary">({payment.count} transactions)</span>
                      </div>
                      <div className="font-bold text-text-primary">{formatCurrency(payment.amount)}</div>
                    </div>
                  ))
                )}
              </div>
            )}

            {/* Clerks Tab */}
            {activeTab === 'clerks' && (
              <div className="space-y-2">
                {report.clerkSummary.length === 0 ? (
                  <p className="text-text-secondary text-center py-8">No clerk activity</p>
                ) : (
                  report.clerkSummary.map((clerk) => (
                    <div key={clerk.clerkName} className="p-4 bg-surface-secondary rounded-xl">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-semibold text-text-primary">{clerk.clerkName}</span>
                        <span className="text-sm text-text-secondary">{clerk.role}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-text-secondary">{clerk.orderCount} orders</span>
                        <span className="font-medium text-text-primary">{formatCurrency(clerk.totalSales)}</span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}

            {/* Voids Tab */}
            {activeTab === 'voids' && (
              <div className="space-y-2">
                {report.voidDetails.length === 0 ? (
                  <p className="text-text-secondary text-center py-8">No voids recorded</p>
                ) : (
                  report.voidDetails.map((voidItem) => (
                    <div key={voidItem.transactionNo} className="p-4 bg-accent-danger/5 rounded-xl">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-semibold text-text-primary">
                          Order #{voidItem.transactionNo}
                        </span>
                        <span className="font-bold text-accent-danger">{formatCurrency(voidItem.amount)}</span>
                      </div>
                      <div className="text-sm text-text-secondary mb-1">Clerk: {voidItem.clerkName}</div>
                      <div className="text-sm text-text-secondary">Reason: {voidItem.reason}</div>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
