'use client'

import { useEffect } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { useAuth } from './AuthProvider'
import { ClerkRole } from '@/types/clerk'

interface ProtectedRouteProps {
  children: React.ReactNode
  allowedRoles?: ClerkRole[]
  fallback?: React.ReactNode
}

/**
 * ProtectedRoute
 * 
 * Wrapper component that protects routes requiring authentication.
 * Optionally restricts access to specific roles.
 * 
 * Usage:
 * ```tsx
 * // Protect any route
 * <ProtectedRoute>
 *   <DashboardPage />
 * </ProtectedRoute>
 * 
 * // Protect with role restriction
 * <ProtectedRoute allowedRoles={[ClerkRole.Admin, ClerkRole.Manager]}>
 *   <AdminPage />
 * </ProtectedRoute>
 * 
 * // With custom loading/fallback
 * <ProtectedRoute fallback={<CustomLoading />}>
 *   <DashboardPage />
 * </ProtectedRoute>
 * ```
 */
export function ProtectedRoute({
  children,
  allowedRoles,
  fallback,
}: ProtectedRouteProps) {
  const router = useRouter()
  const pathname = usePathname()
  const { session, isLoading, isAuthenticated } = useAuth()

  useEffect(() => {
    // Wait for auth check to complete
    if (isLoading) return

    // Not authenticated - redirect to login
    if (!isAuthenticated) {
      const loginUrl = new URL('/login', window.location.origin)
      loginUrl.searchParams.set('redirect', pathname)
      router.push(loginUrl.toString())
      return
    }

    // Check role restrictions
    if (allowedRoles && session) {
      const userRole = session.role as ClerkRole
      if (!allowedRoles.includes(userRole)) {
        // Redirect to unauthorized page or home
        router.push('/register')
      }
    }
  }, [isLoading, isAuthenticated, session, allowedRoles, pathname, router])

  // Show loading state while checking auth
  if (isLoading) {
    return (
      <>
        {fallback || (
          <div className="min-h-screen flex items-center justify-center bg-surface-secondary">
            <div className="flex flex-col items-center gap-4">
              <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin" />
              <p className="text-text-secondary">Loading...</p>
            </div>
          </div>
        )}
      </>
    )
  }

  // Not authenticated - don't render children (will redirect)
  if (!isAuthenticated) {
    return null
  }

  // Check role access
  if (allowedRoles && session) {
    const userRole = session.role as ClerkRole
    if (!allowedRoles.includes(userRole)) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-surface-secondary">
          <div className="text-center p-8 bg-white rounded-2xl shadow-soft max-w-md">
            <div className="w-16 h-16 bg-accent-danger/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-accent-danger" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h1 className="text-xl font-bold text-text-primary mb-2">Access Denied</h1>
            <p className="text-text-secondary mb-6">
              You don&apos;t have permission to access this page.
            </p>
            <button
              onClick={() => router.push('/register')}
              className="px-6 py-2 bg-primary text-white rounded-xl font-medium hover:bg-primary-dark transition-colors"
            >
              Go to Register
            </button>
          </div>
        </div>
      )
    }
  }

  // Authenticated and authorized - render children
  return <>{children}</>
}

/**
 * withProtection HOC
 * 
 * Higher-order component for protecting pages
 * 
 * Usage:
 * ```tsx
 * function AdminPage() { ... }
 * export default withProtection(AdminPage, { allowedRoles: [ClerkRole.Admin] })
 * ```
 */
export function withProtection<P extends object>(
  Component: React.ComponentType<P>,
  options?: { allowedRoles?: ClerkRole[] }
) {
  return function ProtectedComponent(props: P) {
    return (
      <ProtectedRoute allowedRoles={options?.allowedRoles}>
        <Component {...props} />
      </ProtectedRoute>
    )
  }
}
