import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { getSession } from '@/lib/auth'

// GET /api/clerks - List all clerks (Admin/Manager only)
export async function GET(request: NextRequest) {
  try {
    const session = await getSession()
    
    if (!session) {
      return NextResponse.json(
        { success: false, error: { code: 'UNAUTHORIZED', message: 'Not authenticated' } },
        { status: 401 }
      )
    }

    // Only Admin and Manager can list all clerks
    if (session.role === 'Clerk') {
      // Clerks can only see themselves
      const clerk = await prisma.clerk.findUnique({
        where: { id: session.id },
        select: { id: true, name: true, role: true, active: true },
      })
      return NextResponse.json({ success: true, data: { clerks: clerk ? [clerk] : [] } })
    }

    const clerks = await prisma.clerk.findMany({
      select: { id: true, name: true, role: true, active: true, createdAt: true },
      orderBy: { name: 'asc' },
    })

    return NextResponse.json({ success: true, data: { clerks } })
  } catch (error) {
    console.error('List clerks error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'An error occurred' } },
      { status: 500 }
    )
  }
}
