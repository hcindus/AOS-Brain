import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

// GET /api/kds/orders - Get orders for KDS (with SSE support)
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const status = searchParams.get('status') || 'new'
    
    // Support for Server-Sent Events
    const accept = request.headers.get('accept')
    const isSSE = accept?.includes('text/event-stream')

    if (isSSE) {
      // Return SSE stream (simplified - in production, implement proper SSE)
      const orders = await prisma.order.findMany({
        where: { kdsStatus: { in: ['new', 'preparing'] } },
        include: {
          clerk: { select: { name: true } },
          items: true,
        },
        orderBy: { createdAt: 'asc' },
      })

      const stream = new ReadableStream({
        start(controller) {
          const encoder = new TextEncoder()
          const data = `data: ${JSON.stringify({ orders })}

`
          controller.enqueue(encoder.encode(data))
          controller.close()
        },
      })

      return new Response(stream, {
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          Connection: 'keep-alive',
        },
      })
    }

    // Regular JSON response
    const orders = await prisma.order.findMany({
      where: { kdsStatus: status },
      include: {
        clerk: { select: { name: true } },
        items: { select: { name: true, qty: true } },
      },
      orderBy: { createdAt: 'asc' },
    })

    return NextResponse.json({ success: true, data: orders })
  } catch (error) {
    console.error('KDS orders error:', error)
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get KDS orders' } },
      { status: 500 }
    )
  }
}
