'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { PinPad } from '@/components/ui/PinPad'

export default function LoginPage() {
  const router = useRouter()
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  // Fetch clerks on mount (for future use)
  useEffect(() => {
    // Pre-load clerks data
    fetch('/api/clerks')
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          console.log('Available clerks:', data.data.length)
        }
      })
      .catch((err) => console.error('Failed to fetch clerks:', err))
  }, [])

  const handleLogin = async (pin: string) => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pin }),
      })

      const data = await response.json()

      if (data.success) {
        console.log('Login successful:', data.data.clerk.name)
        // Redirect to register page on success
        router.push('/register')
      } else {
        setError(data.error?.message || 'Invalid PIN')
      }
    } catch (err) {
      console.error('Login error:', err)
      setError('Login failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-surface-secondary flex flex-col items-center justify-center p-4">
      {/* Logo / Brand */}
      <div className="mb-8 text-center">
        <div className="w-16 h-16 bg-primary rounded-2xl mx-auto mb-4 flex items-center justify-center shadow-lg shadow-primary/25">
          <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
        </div>
        <h1 className="text-2xl font-bold text-text-primary">RS-79 POS</h1>
        <p className="text-text-secondary mt-1">Enter your PIN to login</p>
      </div>

      {/* PIN Pad */}
      <PinPad
        onSubmit={handleLogin}
        title="Staff Login"
        error={error}
        isLoading={isLoading}
      />

      {/* Footer */}
      <p className="mt-8 text-sm text-text-muted">
        RS-79 Point of Sale System
      </p>
    </div>
  )
}
