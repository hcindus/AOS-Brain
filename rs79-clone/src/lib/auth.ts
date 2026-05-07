import jwt from 'jsonwebtoken'
import { cookies } from 'next/headers'
import { ClerkSession, ClerkRole } from '@/types/clerk'

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
