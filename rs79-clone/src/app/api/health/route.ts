import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET() {
  try {
    // Check database connection
    await prisma.$queryRaw`SELECT 1`

    return NextResponse.json({
      success: true,
      data: {
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        version: process.env.npm_package_version || '0.1.0',
      },
    })
  } catch (error) {
    console.error('Health check error:', error)
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'HEALTH_CHECK_FAILED',
          message: 'Database connection failed',
        },
      },
      { status: 503 }
    )
  }
}
