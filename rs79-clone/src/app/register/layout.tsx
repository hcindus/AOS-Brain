'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

export default function RegisterLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null)

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await fetch('/api/health')
        if (response.status === 401) {
          setIsAuthenticated(false)
          router.push('/login')
        } else {
          setIsAuthenticated(true)
        }
      } catch {
        setIsAuthenticated(false)
      }
    }
    checkAuth()
  }, [router])

  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen bg-surface-secondary flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-text-secondary">Authenticating...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="h-screen overflow-hidden bg-surface-secondary">
      {children}
    </div>
  )
}
