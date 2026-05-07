import jwt from 'jsonwebtoken'
import { cookies } from 'next/headers'
import { NextRequest } from 'next/server'
import type { ClerkSession, ClerkRole } from '@/types/clerk'

const JWT_SECRET = process.env.JWT_SECRET || 'rs79-dev-secret-change-in-production'

export function createSession(clerk: ClerkSession): string {
  return jwt.sign(clerk, JWT_SECRET, { expiresIn: '12h' })
}

export function verifySession(token: string): ClerkSession | null {
  try {
    const payload = jwt.verify(token, JWT_SECRET) as {
      id: string
      name: string
      role: string
    }
    return {
      id: payload.id,
      name: payload.name,
      role: payload.role as ClerkRole,
    }
  } catch {
    return null
  }
}

export async function getSession(): Promise<ClerkSession | null> {
  const cookieStore = cookies()
  const token = cookieStore.get('rs79_session')?.value
  if (!token) return null
  return verifySession(token)
}

export async function authenticateRequest(req: NextRequest): Promise<ClerkSession | null> {
  const token = req.cookies.get('rs79_session')?.value
  if (!token) return null
  return verifySession(token)
}

export function hasPermission(session: ClerkSession | null, requiredRoles: ClerkRole[]): boolean {
  if (!session) return false
  return requiredRoles.includes(session.role)
}

// Helper for API routes - requires auth and returns response if not authenticated
export async function requireAuth(req: NextRequest, allowedRoles: ClerkRole[] = ['Admin', 'Manager']): Promise<{ success: boolean; response?: NextResponse; session?: ClerkSession }> {
  const session = await authenticateRequest(req)
  
  if (!session) {
    return {
      success: false,
      response: NextResponse.json(
        { success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } },
        { status: 401 }
      )
    }
  }
  
  if (!hasPermission(session, allowedRoles)) {
    return {
      success: false,
      response: NextResponse.json(
        { success: false, error: { code: 'FORBIDDEN', message: 'Insufficient permissions' } },
        { status: 403 }
      )
    }
  }
  
  return { success: true, session }
}
