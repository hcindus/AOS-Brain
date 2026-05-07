'use client'

import React, { createContext, useContext, useEffect, useState } from 'react'
import { ClerkSession } from '@/types/clerk'

interface AuthContextValue {
  session: ClerkSession | null
  isLoading: boolean
  isAuthenticated: boolean
  logout: () => Promise<void>
  refreshSession: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

/**
 * AuthProvider
 * 
 * Provides authentication context to the entire application.
 * Wraps the app to provide session data to all children.
 * 
 * Usage:
 * ```tsx
 * // In layout.tsx
 * <AuthProvider>
 *   {children}
 * </AuthProvider>
 * ```
 */
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<ClerkSession | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  /**
   * Fetch current session from API
   */
  const refreshSession = async () => {
    try {
      const response = await fetch('/api/auth/session', {
        credentials: 'include',
      })
      const data = await response.json()
      
      if (data.success && data.data.session) {
        setSession(data.data.session)
      } else {
        setSession(null)
      }
    } catch (error) {
      console.error('Failed to refresh session:', error)
      setSession(null)
    }
  }

  /**
   * Logout - clear session
   */
  const logout = async () => {
    try {
      await fetch('/api/auth/logout', { 
        method: 'POST',
        credentials: 'include',
      })
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      setSession(null)
      window.location.href = '/login'
    }
  }

  // Check for existing session on mount
  useEffect(() => {
    refreshSession().finally(() => setIsLoading(false))
  }, [])

  const value: AuthContextValue = {
    session,
    isLoading,
    isAuthenticated: !!session,
    logout,
    refreshSession,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

/**
 * useAuth Hook
 * 
 * Hook to access authentication context
 * Must be used within AuthProvider
 */
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
