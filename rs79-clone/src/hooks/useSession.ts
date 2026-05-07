'use client'

import { useState, useEffect, useCallback } from 'react'
import type { ClerkSession } from '@/types'

export function useSession() {
  const [session, setSession] = useState<ClerkSession | null>(null)
  const [loading, setLoading] = useState(true)

  const checkSession = useCallback(async () => {
    try {
      const res = await fetch('/api/auth/session')
      if (res.ok) {
        const data = await res.json()
        setSession(data.data?.clerk || null)
      } else {
        setSession(null)
      }
    } catch (error) {
      setSession(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    checkSession()
  }, [checkSession])

  const login = async (clerkId: string, pin: string) => {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ clerkId, pin }),
    })
    
    const data = await res.json()
    
    if (res.ok) {
      setSession(data.data.clerk)
      return { success: true }
    }
    
    return { success: false, error: data.error }
  }

  const logout = async () => {
    await fetch('/api/auth/logout', { method: 'POST' })
    setSession(null)
  }

  return { session, loading, login, logout, checkSession }
}
