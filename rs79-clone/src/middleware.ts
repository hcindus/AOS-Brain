import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { verifySession } from './lib/auth'

// Paths that don't require authentication
const PUBLIC_PATHS = [
  '/login',
  '/api/auth/login',
  '/api/auth/session',
  '/_next',
  '/favicon.ico',
  '/api/health',
]

// Protected route patterns that require authentication
const PROTECTED_PATTERNS = [
  '/register',
  '/api/orders',
  '/api/customers',
  '/api/items',
  '/api/payments',
  '/api/kds',
]

/**
 * Check if path matches any protected pattern
 */
function isProtectedPath(pathname: string): boolean {
  return PROTECTED_PATTERNS.some(pattern => 
    pathname.startsWith(pattern)
  )
}

/**
 * Check if path is public
 */
function isPublicPath(pathname: string): boolean {
  return PUBLIC_PATHS.some(path => pathname.startsWith(path))
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Allow public paths
  if (isPublicPath(pathname)) {
    return NextResponse.next()
  }

  // Check for session token
  const token = request.cookies.get('rs79_session')?.value
  
  // No token - not authenticated
  if (!token) {
    // API routes return 401
    if (pathname.startsWith('/api/')) {
      return NextResponse.json(
        { success: false, error: { code: 'AUTH_REQUIRED', message: 'Authentication required' } },
        { status: 401 }
      )
    }
    
    // Page routes redirect to login
    if (isProtectedPath(pathname)) {
      const loginUrl = new URL('/login', request.url)
      loginUrl.searchParams.set('redirect', pathname)
      return NextResponse.redirect(loginUrl)
    }
    
    return NextResponse.next()
  }

  // Verify token
  const session = verifySession(token)
  
  // Invalid or expired token
  if (!session) {
    // Clear invalid cookie
    const response = pathname.startsWith('/api/')
      ? NextResponse.json(
          { success: false, error: { code: 'AUTH_INVALID', message: 'Invalid or expired session' } },
          { status: 401 }
        )
      : NextResponse.redirect(new URL('/login', request.url))
    
    response.cookies.delete('rs79_session')
    return response
  }

  // Add session data to request headers for API routes
  if (pathname.startsWith('/api/')) {
    const requestHeaders = new Headers(request.headers)
    requestHeaders.set('x-clerk-id', session.id)
    requestHeaders.set('x-clerk-name', session.name)
    requestHeaders.set('x-clerk-role', session.role)
    
    return NextResponse.next({
      request: { headers: requestHeaders },
    })
  }

  // User is authenticated, allow access
  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|.*\\.png$|.*\\.jpg$|.*\\.svg$).*)'],
}
