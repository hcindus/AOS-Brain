import { NextRequest, NextResponse } from 'next/server'
import { NotFoundError } from '@/lib/errors'
import { generateXReport, generateZReport, formatThermalPrint, getShiftHistory } from '@/services/xz-report-service'
import { authenticateRequest, hasPermission } from '@/lib/auth'
import { ClerkRole } from '@/types/clerk'

// GET /api/reports/x - Generate X-Report (current shift totals)
export async function GET(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Only Admin and Manager can view reports
    if (!hasPermission(clerk, [ClerkRole.Admin, ClerkRole.Manager])) {
      return NextResponse.json({ error: 'Insufficient permissions' }, { status: 403 })
    }

    const { searchParams } = new URL(req.url)
    const type = searchParams.get('type') || 'X'
    const format = searchParams.get('format') || 'json'

    if (type === 'Z') {
      // Z-Report is generated via POST
      return NextResponse.json({ error: 'Use POST for Z-Report' }, { status: 400 })
    }

    const report = await generateXReport(clerk.id)

    if (format === 'print') {
      const printOutput = formatThermalPrint(report)
      return new NextResponse(printOutput, {
        headers: {
          'Content-Type': 'text/plain',
        },
      })
    }

    return NextResponse.json({
      success: true,
      data: report,
    })
  } catch (error) {
    if (error instanceof NotFoundError) {
      return NextResponse.json({ error: error.message }, { status: 404 })
    }
    console.error('Generate X-Report error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

// POST /api/reports/x - Generate Z-Report (end-of-day)
export async function POST(req: NextRequest) {
  try {
    const clerk = await authenticateRequest(req)
    if (!clerk) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Only Admin and Manager can generate Z-Reports
    if (!hasPermission(clerk, [ClerkRole.Admin, ClerkRole.Manager])) {
      return NextResponse.json({ error: 'Insufficient permissions' }, { status: 403 })
    }

    const body = await req.json()
    const { format = 'json' } = body

    const report = await generateZReport(clerk.id)

    if (format === 'print') {
      const printOutput = formatThermalPrint(report)
      return new NextResponse(printOutput, {
        headers: {
          'Content-Type': 'text/plain',
        },
      })
    }

    return NextResponse.json({
      success: true,
      data: report,
    })
  } catch (error) {
    if (error instanceof NotFoundError) {
      return NextResponse.json({ error: error.message }, { status: 404 })
    }
    console.error('Generate Z-Report error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
