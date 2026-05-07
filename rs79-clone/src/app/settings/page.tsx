'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { ArrowLeft, Save, RefreshCw, Percent, DollarSign, Receipt } from 'lucide-react'
import { TAX_CONFIGS } from '@/lib/tax'

interface TaxRate {
  name: string
  rate: number
  category?: string
}

interface StoreSettings {
  taxMode: 'exclusive' | 'inclusive'
  taxConfig: {
    mode: 'exclusive' | 'inclusive'
    rates: TaxRate[]
    defaultRate: number
    roundTo: number
  }
  currency: string
  receiptHeader?: string
  receiptFooter?: string
}

export default function SettingsPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  
  const [settings, setSettings] = useState<StoreSettings>({
    taxMode: 'exclusive',
    taxConfig: {
      mode: 'exclusive',
      rates: [{ name: 'Standard', rate: 0.10 }],
      defaultRate: 0.10,
      roundTo: 0.01,
    },
    currency: 'USD',
    receiptHeader: '',
    receiptFooter: '',
  })

  // Load settings on mount
  useEffect(() => {
    loadSettings()
  }, [])

  const loadSettings = async () => {
    try {
      const res = await fetch('/api/settings')
      const data = await res.json()
      if (data.success) {
        setSettings(data.data)
      }
    } catch (error) {
      setError('Failed to load settings')
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    setSaving(true)
    setError('')
    setSuccess('')

    try {
      const res = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings),
      })

      const data = await res.json()
      if (data.success) {
        setSuccess('Settings saved successfully')
      } else {
        setError(data.error?.message || 'Failed to save settings')
      }
    } catch (error) {
      setError('Failed to save settings')
    } finally {
      setSaving(false)
    }
  }

  const applyPreset = (preset: keyof typeof TAX_CONFIGS) => {
    const config = TAX_CONFIGS[preset]
    setSettings(prev => ({
      ...prev,
      taxMode: config.mode,
      taxConfig: config,
    }))
  }

  const addTaxRate = () => {
    setSettings(prev => ({
      ...prev,
      taxConfig: {
        ...prev.taxConfig,
        rates: [...prev.taxConfig.rates, { name: 'New Rate', rate: 0 }],
      },
    }))
  }

  const updateTaxRate = (index: number, field: keyof TaxRate, value: string | number) => {
    setSettings(prev => ({
      ...prev,
      taxConfig: {
        ...prev.taxConfig,
        rates: prev.taxConfig.rates.map((r, i) =>
          i === index ? { ...r, [field]: value } : r
        ),
      },
    }))
  }

  const removeTaxRate = (index: number) => {
    setSettings(prev => ({
      ...prev,
      taxConfig: {
        ...prev.taxConfig,
        rates: prev.taxConfig.rates.filter((_, i) => i !== index),
      },
    }))
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-surface-secondary">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-surface-secondary">
      {/* Header */}
      <div className="bg-white border-b border-surface-tertiary px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push('/register')}
              className="p-2 hover:bg-surface-secondary rounded-lg transition-colors"
            >
              <ArrowLeft size={20} />
            </button>
            <h1 className="text-xl font-bold">Store Settings</h1>
          </div>
          
          <button
            onClick={handleSave}
            disabled={saving}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 disabled:opacity-50 transition-colors"
          >
            <Save size={18} />
            {saving ? 'Saving...' : 'Save Settings'}
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto p-6 space-y-6">
        {/* Success/Error Messages */}
        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">
            {error}
          </div>
        )}
        {success && (
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg text-green-600">
            {success}
          </div>
        )}

        {/* Tax Settings */}
        <div className="bg-white rounded-xl border border-surface-tertiary overflow-hidden">
          <div className="px-6 py-4 border-b border-surface-tertiary bg-surface-secondary">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <Percent size={20} className="text-primary" />
              </div>
              <div>
                <h2 className="font-semibold">Tax Settings</h2>
                <p className="text-sm text-text-secondary">Configure how taxes are calculated</p>
              </div>
            </div>
          </div>

          <div className="p-6 space-y-6">
            {/* Tax Mode */}
            <div>
              <label className="block text-sm font-medium mb-3">Tax Calculation Mode</label>
              <div className="grid grid-cols-2 gap-4">
                <label
                  className={`p-4 border-2 rounded-xl cursor-pointer transition-all ${
                    settings.taxMode === 'exclusive'
                      ? 'border-primary bg-primary/5'
                      : 'border-surface-tertiary hover:border-primary/50'
                  }`}
                >
                  <input
                    type="radio"
                    name="taxMode"
                    value="exclusive"
                    checked={settings.taxMode === 'exclusive'}
                    onChange={(e) => setSettings(prev => ({ ...prev, taxMode: e.target.value as 'exclusive' | 'inclusive' }))}
                    className="sr-only"
                  />
                  <div className="font-medium">Tax Exclusive (US Style)</div>
                  <p className="text-sm text-text-secondary mt-1">
                    Prices shown without tax. Tax added at checkout.
                    <br />
                    <span className="text-xs">Example: $100 + 10% = $110 total</span>
                  </p>
                </label>

                <label
                  className={`p-4 border-2 rounded-xl cursor-pointer transition-all ${
                    settings.taxMode === 'inclusive'
                      ? 'border-primary bg-primary/5'
                      : 'border-surface-tertiary hover:border-primary/50'
                  }`}
                >
                  <input
                    type="radio"
                    name="taxMode"
                    value="inclusive"
                    checked={settings.taxMode === 'inclusive'}
                    onChange={(e) => setSettings(prev => ({ ...prev, taxMode: e.target.value as 'exclusive' | 'inclusive' }))}
                    className="sr-only"
                  />
                  <div className="font-medium">Tax Inclusive (EU/VAT Style)</div>
                  <p className="text-sm text-text-secondary mt-1">
                    Prices include tax. Tax extracted from total.
                    <br />
                    <span className="text-xs">Example: $110 (incl. $10 tax) = $100 net</span>
                  </p>
                </label>
              </div>
            </div>

            {/* Quick Presets */}
            <div>
              <label className="block text-sm font-medium mb-3">Quick Presets</label>
              <div className="flex flex-wrap gap-3">
                <button
                  type="button"
                  onClick={() => applyPreset('us')}
                  className="px-4 py-2 bg-surface-secondary rounded-lg hover:bg-surface-tertiary transition-colors text-sm"
                >
                  🇺🇸 US (10% exclusive)
                </button>
                <button
                  type="button"
                  onClick={() => applyPreset('uk')}
                  className="px-4 py-2 bg-surface-secondary rounded-lg hover:bg-surface-tertiary transition-colors text-sm"
                >
                  🇬🇧 UK (20% inclusive)
                </button>
                <button
                  type="button"
                  onClick={() => applyPreset('eu')}
                  className="px-4 py-2 bg-surface-secondary rounded-lg hover:bg-surface-tertiary transition-colors text-sm"
                >
                  🇪🇺 EU (21% inclusive)
                </button>
              </div>
            </div>

            {/* Tax Rates */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <label className="block text-sm font-medium">Tax Rates</label>
                <button
                  type="button"
                  onClick={addTaxRate}
                  className="text-sm text-primary hover:text-primary/80"
                >
                  + Add Rate
                </button>
              </div>

              <div className="space-y-3">
                {settings.taxConfig.rates.map((rate, index) => (
                  <div key={index} className="flex items-center gap-3 p-3 bg-surface-secondary rounded-lg">
                    <input
                      type="text"
                      value={rate.name}
                      onChange={(e) => updateTaxRate(index, 'name', e.target.value)}
                      placeholder="Rate name"
                      className="flex-1 px-3 py-2 rounded-lg border border-surface-tertiary focus:border-primary focus:outline-none"
                    />
                    <div className="flex items-center gap-2">
                      <input
                        type="number"
                        value={(rate.rate * 100).toFixed(2)}
                        onChange={(e) => updateTaxRate(index, 'rate', parseFloat(e.target.value) / 100)}
                        step="0.01"
                        min="0"
                        max="100"
                        className="w-20 px-3 py-2 rounded-lg border border-surface-tertiary focus:border-primary focus:outline-none text-right"
                      />
                      <span className="text-text-secondary">%</span>
                    </div>

                    <input
                      type="text"
                      value={rate.category || ''}
                      onChange={(e) => updateTaxRate(index, 'category', e.target.value)}
                      placeholder="Category (optional)"
                      className="w-40 px-3 py-2 rounded-lg border border-surface-tertiary focus:border-primary focus:outline-none"
                    />

                    {settings.taxConfig.rates.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeTaxRate(index)}
                        className="p-2 text-accent-danger hover:bg-red-50 rounded-lg transition-colors"
                      >
                        &times;
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Currency Settings */}
        <div className="bg-white rounded-xl border border-surface-tertiary overflow-hidden">
          <div className="px-6 py-4 border-b border-surface-tertiary bg-surface-secondary">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <DollarSign size={20} className="text-primary" />
              </div>
              <div>
                <h2 className="font-semibold">Currency</h2>
                <p className="text-sm text-text-secondary">Set your default currency</p>
              </div>
            </div>
          </div>

          <div className="p-6">
            <select
              value={settings.currency}
              onChange={(e) => setSettings(prev => ({ ...prev, currency: e.target.value }))}
              className="w-full px-3 py-2 rounded-lg border border-surface-tertiary focus:border-primary focus:outline-none"
            >
              <option value="USD">USD - US Dollar ($)</option>
              <option value="EUR">EUR - Euro (€)</option>
              <option value="GBP">GBP - British Pound (£)</option>
              <option value="JPY">JPY - Japanese Yen (¥)</option>
              <option value="CAD">CAD - Canadian Dollar (C$)</option>
              <option value="AUD">AUD - Australian Dollar (A$)</option>
            </select>
          </div>
        </div>

        {/* Receipt Settings */}
        <div className="bg-white rounded-xl border border-surface-tertiary overflow-hidden">
          <div className="px-6 py-4 border-b border-surface-tertiary bg-surface-secondary">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <Receipt size={20} className="text-primary" />
              </div>
              <div>
                <h2 className="font-semibold">Receipt</h2>
                <p className="text-sm text-text-secondary">Customize receipt header and footer</p>
              </div>
            </div>
          </div>

          <div className="p-6 space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Header</label>
              <textarea
                value={settings.receiptHeader || ''}
                onChange={(e) => setSettings(prev => ({ ...prev, receiptHeader: e.target.value }))}
                placeholder="e.g., Thank you for shopping with us!"
                rows={2}
                className="w-full px-3 py-2 rounded-lg border border-surface-tertiary focus:border-primary focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Footer</label>
              <textarea
                value={settings.receiptFooter || ''}
                onChange={(e) => setSettings(prev => ({ ...prev, receiptFooter: e.target.value }))}
                placeholder="e.g., Returns accepted within 30 days"
                rows={2}
                className="w-full px-3 py-2 rounded-lg border border-surface-tertiary focus:border-primary focus:outline-none"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}