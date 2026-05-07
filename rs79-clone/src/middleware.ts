import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { verifySession } from './lib/auth'

const PUBLIC_PATHS = ['/login', '/api/auth/login', '/_next', '/favicon.ico']

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Allow public paths
  if (PUBLIC_PATHS.some((path) => pathname.startsWith(path))) {
    return NextResponse.next()
  }

  // Check for session token
  const token = request.cookies.get('rs79_session')?.value
  
  if (!token) {
    // API routes return 401
    if (pathname.startsWith('/api/')) {
      return NextResponse.json(
        { success: false, error: { code: 'AUTH_REQUIRED', message: 'Authentication required' } },
        { status: 401 }
      )
    }
    // Page routes redirect to login
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Verify token
  const session = verifySession(token)
  
  if (!session) {
    // Clear invalid cookie and redirect
    const response = pathname.startsWith('/api/')
      ? NextResponse.json(
          { success: false, error: { code: 'AUTH_INVALID', message: 'Invalid or expired session' } },
          { status: 401 }
        )
      : NextResponse.redirect(new URL('/login', request.url))
    
    response.cookies.delete('rs79_session')
    return response
  }

  // Add session to headers for API routes
  if (pathname.startsWith('/api/')) {
    const requestHeaders = new Headers(request.headers)
    requestHeaders.set('x-clerk-id', session.id)
    requestHeaders.set('x-clerk-role', session.role)
    
    return NextResponse.next({
      request: { headers: requestHeaders },
    })
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
}
