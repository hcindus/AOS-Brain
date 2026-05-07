'use client'

import { useState } from 'react'
import { cn } from '@/lib/utils'
import { Bitcoin, QrCode, Copy, Check, ExternalLink } from 'lucide-react'
import { Button } from '@/components/ui/Button'

interface CryptoPaymentProps {
  balanceDue: number
  currency: string
  onSubmit: (data: { amount: number; txHash: string; network: string; walletAddress: string }) => void
  onCancel: () => void
}

const SUPPORTED_NETWORKS = [
  { code: 'btc', name: 'Bitcoin', symbol: 'BTC', color: '#F7931A' },
  { code: 'eth', name: 'Ethereum', symbol: 'ETH', color: '#627EEA' },
  { code: 'usdc', name: 'USDC (ERC-20)', symbol: 'USDC', color: '#2775CA' },
  { code: 'usdt', name: 'USDT (ERC-20)', symbol: 'USDT', color: '#26A17B' },
]

// Mock wallet addresses for demo
const WALLET_ADDRESSES: Record<string, string> = {
  btc: 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
  eth: '0x71C7656EC7ab88b098defB751B7401B5f6d8976F',
  usdc: '0x71C7656EC7ab88b098defB751B7401B5f6d8976F',
  usdt: '0x71C7656EC7ab88b098defB751B7401B5f6d8976F',
}

export function CryptoPayment({ balanceDue, currency, onSubmit, onCancel }: CryptoPaymentProps) {
  const [amount, setAmount] = useState<string>(balanceDue.toFixed(2))
  const [txHash, setTxHash] = useState('')
  const [selectedNetwork, setSelectedNetwork] = useState('btc')
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [copied, setCopied] = useState(false)
  const [verifying, setVerifying] = useState(false)
  const [verificationStatus, setVerificationStatus] = useState<'idle' | 'pending' | 'verified' | 'failed'>('idle')

  const numericAmount = parseFloat(amount) || 0
  const walletAddress = WALLET_ADDRESSES[selectedNetwork]

  const handleCopyAddress = () => {
    navigator.clipboard.writeText(walletAddress)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleVerifyTransaction = async () => {
    if (!txHash.trim()) {
      setErrors({ txHash: 'Transaction hash is required' })
      return
    }

    setVerifying(true)
    setVerificationStatus('pending')

    // Simulate verification
    await new Promise((resolve) => setTimeout(resolve, 2000))

    // Mock verification - in production this would check blockchain
    const isValid = txHash.length >= 10
    setVerificationStatus(isValid ? 'verified' : 'failed')
    setVerifying(false)
  }

  const handleSubmit = () => {
    const newErrors: Record<string, string> = {}

    if (numericAmount <= 0) {
      newErrors.amount = 'Amount must be greater than 0'
    }

    if (!txHash.trim()) {
      newErrors.txHash = 'Transaction hash is required'
    }

    if (verificationStatus !== 'verified') {
      newErrors.verification = 'Please verify the transaction first'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    onSubmit({
      amount: numericAmount,
      txHash,
      network: selectedNetwork,
      walletAddress,
    })
  }

  const network = SUPPORTED_NETWORKS.find((n) => n.code === selectedNetwork)

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
          />
        </div>
        {errors.amount && <p className="text-sm text-red-500">{errors.amount}</p>}
      </div>

      {/* Network Selection */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-text-secondary">Select Network</label>
        <div className="grid grid-cols-2 gap-2">
          {SUPPORTED_NETWORKS.map((net) => (
            <button
              key={net.code}
              onClick={() => {
                setSelectedNetwork(net.code)
                setVerificationStatus('idle')
              }}
              className={cn(
                'flex items-center gap-2 p-3 rounded-xl border-2 transition-all duration-150',
                selectedNetwork === net.code
                  ? 'border-primary bg-primary/5 text-primary'
                  : 'border-surface-tertiary text-text-secondary hover:border-primary/50 hover:bg-surface-secondary'
              )}
            >
              <div
                className="w-4 h-4 rounded-full"
                style={{ backgroundColor: net.color }}
              />
              <span className="font-medium">{net.name}</span>
            </button>
          ))}
        </div>
      </div>

      {/* QR Code Placeholder */}
      <div className="p-4 bg-surface-secondary rounded-xl">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <QrCode className="text-primary" size={20} />
            <span className="font-medium text-text-primary">Payment Address</span>
          </div>
          <button
            onClick={handleCopyAddress}
            className="flex items-center gap-1 px-2 py-1 text-sm text-primary hover:bg-primary/10 rounded-lg transition-colors"
          >
            {copied ? <Check size={14} /> : <Copy size={14} />}
            {copied ? 'Copied!' : 'Copy'}
          </button>
        </div>

        <div className="flex flex-col items-center gap-4">
          {/* QR Code Placeholder */}
          <div className="w-40 h-40 bg-white rounded-xl flex items-center justify-center border-2 border-surface-tertiary">
            <div className="text-center">
              <QrCode className="mx-auto mb-2 text-text-secondary" size={48} />
              <p className="text-xs text-text-secondary">Scan to pay</p>
            </div>
          </div>

          {/* Wallet Address */}
          <div className="w-full">
            <p className="text-xs text-text-secondary mb-1">Wallet Address ({network?.symbol})</p>
            <div className="flex items-center gap-2 p-2 bg-white border border-surface-tertiary rounded-lg">
              <code className="flex-1 text-xs text-text-primary break-all font-mono">{walletAddress}</code>
              <a
                href={`https://${selectedNetwork === 'btc' ? 'mempool.space' : 'etherscan.io'}/address/${walletAddress}`}
                target="_blank"
                rel="noopener noreferrer"
                className="p-1 text-text-secondary hover:text-primary transition-colors"
              >
                <ExternalLink size={14} />
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Transaction Hash Input */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-text-secondary">Transaction Hash</label>
        <div className="flex gap-2">
          <input
            type="text"
            value={txHash}
            onChange={(e) => {
              setTxHash(e.target.value)
              setErrors((prev) => ({ ...prev, txHash: '', verification: '' }))
              setVerificationStatus('idle')
            }}
            placeholder={`Enter ${selectedNetwork} transaction hash...`}
            className={cn(
              'flex-1 px-4 py-3 bg-white border-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/30 text-text-primary transition-colors',
              errors.txHash ? 'border-red-500' : 'border-surface-tertiary'
            )}
          />
          <Button
            variant="outline"
            onClick={handleVerifyTransaction}
            disabled={!txHash.trim() || verifying}
            className="whitespace-nowrap"
          >
            {verifying ? 'Verifying...' : 'Verify'}
          </Button>
        </div>
        {errors.txHash && <p className="text-sm text-red-500">{errors.txHash}</p>}

        {/* Verification Status */}
        {verificationStatus === 'pending' && (
          <div className="flex items-center gap-2 text-sm text-amber-600">
            <div className="w-4 h-4 border-2 border-amber-600 border-t-transparent rounded-full animate-spin" />
            Verifying transaction on {network?.name}...
          </div>
        )}
        {verificationStatus === 'verified' && (
          <div className="flex items-center gap-2 text-sm text-accent-success"
          >
            <Check size={16} />
            Transaction verified successfully!
          </div>
        )}
        {verificationStatus === 'failed' && (
          <div className="text-sm text-red-500">
            Verification failed. Please check the transaction hash and try again.
          </div>
        )}
        {errors.verification && <p className="text-sm text-red-500">{errors.verification}</p>}
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3 pt-4">
        <Button variant="outline" className="flex-1" onClick={onCancel}>
          Cancel
        </Button>
        <Button
          className="flex-1"
          onClick={handleSubmit}
          disabled={verificationStatus !== 'verified'}
        >
          <Bitcoin size={18} />
          Add Crypto Payment
        </Button>
      </div>
    </div>
  )
}
