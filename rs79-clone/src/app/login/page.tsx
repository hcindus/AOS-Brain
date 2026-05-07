'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Loader2 } from 'lucide-react'
import type { Clerk } from '@/types'

export default function LoginPage() {
  const [clerks, setClerks] = useState<Clerk[]>([])
  const [selectedClerk, setSelectedClerk] = useState<string | null>(null)
  const [pin, setPin] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const router = useRouter()

  useEffect(() => {
    // Fetch active clerks
    fetch('/api/clerks')
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setClerks(data.data.clerks.filter((c: Clerk) => c.active))
        }
        setLoading(false)
      })
      .catch(() => {
        setError('Failed to load clerks')
        setLoading(false)
      })
  }, [])

  const handleClerkSelect = (clerkId: string) => {
    setSelectedClerk(clerkId)
    setError('')
    setPin('')
  }

  const handlePinDigit = (digit: string) => {
    if (pin.length < 4) {
      setPin(prev => prev + digit)
      setError('')
    }
  }

  const handleBackspace = () => {
    setPin(prev => prev.slice(0, -1))
    setError('')
  }

  const handleClear = () => {
    setPin('')
    setError('')
  }

  const handleLogin = async () => {
    if (!selectedClerk || pin.length !== 4) {
      setError('Please select a clerk and enter 4-digit PIN')
      return
    }

    setSubmitting(true)
    setError('')

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clerkId: selectedClerk, pin }),
      })

      const data = await res.json()

      if (res.ok) {
        router.push('/register')
      } else {
        setError(data.error?.message || 'Invalid PIN')
        setPin('')
      }
    } catch {
      setError('Login failed')
      setPin('')
    } finally {
      setSubmitting(false)
    }
  }

  // Auto-submit when PIN is 4 digits
  useEffect(() => {
    if (pin.length === 4 && selectedClerk) {
      handleLogin()
    }
  }, [pin, selectedClerk])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-white animate-spin" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo/Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">RS-79</h1>
          <p className="text-gray-400">Point of Sale System</p>
        </div>

        {/* Clerk Selection */}
        {!selectedClerk ? (
          <div className="bg-gray-800 rounded-2xl p-6">
            <h2 className="text-xl font-semibold text-white mb-4 text-center">Select Clerk</h2>
            <div className="space-y-2">
              {clerks.map((clerk) => (
                <button
                  key={clerk.id}
                  onClick={() => handleClerkSelect(clerk.id)}
                  className="w-full p-4 bg-gray-700 hover:bg-gray-600 rounded-xl text-white text-left transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-lg">{clerk.name}</p>
                      <p className="text-sm text-gray-400">{clerk.role}</p>
                    </div>
                    <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                      {clerk.name.charAt(0)}
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="bg-gray-800 rounded-2xl p-6">
            {/* Selected Clerk */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <p className="text-gray-400 text-sm">Logging in as</p>
                <p className="text-white font-medium text-lg">
                  {clerks.find(c => c.id === selectedClerk)?.name}
                </p>
              </div>
              <button
                onClick={() => {
                  setSelectedClerk(null)
                  setPin('')
                  setError('')
                }}
                className="text-blue-400 hover:text-blue-300 text-sm"
              >
                Change
              </button>
            </div>

            {/* PIN Display */}
            <div className="flex justify-center gap-3 mb-8">
              {[0, 1, 2, 3].map((i) => (
                <div
                  key={i}
                  className={`w-14 h-14 rounded-xl border-2 flex items-center justify-center transition-all ${
                    i < pin.length
                      ? 'bg-blue-600 border-blue-600'
                      : 'bg-gray-700 border-gray-600'
                  }`}
                >
                  {i < pin.length && (
                    <div className="w-4 h-4 bg-white rounded-full" />
                  )}
                </div>
              ))}
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-900/50 border border-red-500 rounded-lg p-3 mb-4">
                <p className="text-red-300 text-center text-sm">{error}</p>
              </div>
            )}

            {/* Numpad */}
            <div className="grid grid-cols-3 gap-3">
              {['1', '2', '3', '4', '5', '6', '7', '8', '9'].map((digit) => (
                <button
                  key={digit}
                  onClick={() => handlePinDigit(digit)}
                  disabled={submitting}
                  className="aspect-square bg-gray-700 hover:bg-gray-600 active:bg-gray-500 rounded-xl text-white text-2xl font-semibold transition-colors disabled:opacity-50"
                >
                  {digit}
                </button>
              ))}
              <button
                onClick={handleClear}
                disabled={submitting}
                className="aspect-square bg-yellow-600/20 hover:bg-yellow-600/40 rounded-xl text-yellow-400 text-lg font-medium transition-colors disabled:opacity-50"
              >
                C
              </button>
              <button
                onClick={() => handlePinDigit('0')}
                disabled={submitting}
                className="aspect-square bg-gray-700 hover:bg-gray-600 active:bg-gray-500 rounded-xl text-white text-2xl font-semibold transition-colors disabled:opacity-50"
              >
                0
              </button>
              <button
                onClick={handleBackspace}
                disabled={submitting || pin.length === 0}
                className="aspect-square bg-red-600/20 hover:bg-red-600/40 rounded-xl text-red-400 text-lg font-medium transition-colors disabled:opacity-50 flex items-center justify-center"
              >
                ⌫
              </button>
            </div>

            {/* Submit Button */}
            <button
              onClick={handleLogin}
              disabled={submitting || pin.length !== 4}
              className="w-full mt-6 h-14 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:text-gray-500 text-white text-lg font-semibold rounded-xl transition-colors flex items-center justify-center"
            >
              {submitting ? (
                <Loader2 className="w-6 h-6 animate-spin" />
              ) : (
                'Login'
              )}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}