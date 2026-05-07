import { prisma } from '@/lib/prisma'
import { ValidationError, NotFoundError } from '@/lib/errors'
import type { Payment, Order, Clerk } from '@prisma/client'

export type ReportType = 'X' | 'Z'

export interface PaymentSummary {
  type: string
  count: number
  amount: number
}

export interface ClerkSummary {
  clerkId: string
  clerkName: string
  role: string
  orderCount: number
  totalSales: number
  voidCount: number
  voidAmount: number
}

export interface XZReport {
  reportType: ReportType
  generatedAt: Date
  shiftStartTime?: Date
  shiftEndTime?: Date
  // Financial totals
  grossSales: number
  netSales: number
  taxCollected: number
  discounts: number
  refunds: number
  voids: number
  // Payment breakdown
  paymentSummary: PaymentSummary[]
  // Clerk breakdown
  clerkSummary: ClerkSummary[]
  // Order statistics
  orderCount: number
  itemCount: number
  averageOrderValue: number
  // Void/refund details
  voidDetails: Array<{
    transactionNo: number
    clerkName: string
    amount: number
    reason: string
    voidedAt: Date
  }>
  // Gift card activity
  giftCardSales: number
  giftCardRedemptions: number
  // Store credit activity
  storeCreditIssued: number
  storeCreditRedeemed: number
  // For Z-report: last Z-report info
  lastZReportTime?: Date
  // Shift totals (cumulative from last Z)
  shiftTotals?: {
    openingBalance: number
    closingBalance: number
    expectedBalance: number
    variance: number
  }
}

export interface GenerateReportInput {
  clerkId: string
  reportType: ReportType
  shiftStartTime?: Date
}

/**
 * Generate X-Report (current shift totals, read-only)
 */
export async function generateXReport(clerkId: string): Promise<XZReport> {
  // Get the last Z-report time to calculate shift totals
  const lastZReport = await prisma.sessionLog.findFirst({
    where: { action: 'Z_REPORT_GENERATED' },
    orderBy: { createdAt: 'desc' },
  })

  const shiftStartTime = lastZReport?.createdAt || new Date(Date.now() - 24 * 60 * 60 * 1000)
  const shiftEndTime = new Date()

  return generateReport('X', shiftStartTime, shiftEndTime, clerkId)
}

/**
 * Generate Z-Report (end-of-day with counter reset)
 */
export async function generateZReport(clerkId: string): Promise<XZReport> {
  // Get the last Z-report time
  const lastZReport = await prisma.sessionLog.findFirst({
    where: { action: 'Z_REPORT_GENERATED' },
    orderBy: { createdAt: 'desc' },
  })

  const shiftStartTime = lastZReport?.createdAt || new Date(Date.now() - 24 * 60 * 60 * 1000)
  const shiftEndTime = new Date()

  const report = await generateReport('Z', shiftStartTime, shiftEndTime, clerkId)

  // Log the Z-report generation
  await prisma.sessionLog.create({
    data: {
      clerkId,
      action: 'Z_REPORT_GENERATED',
      details: `Z-Report generated. Shift totals: Gross=$${report.grossSales.toFixed(2)}, Net=$${report.netSales.toFixed(2)}, Orders=${report.orderCount}`,
    },
  })

  return report
}

/**
 * Generate report data
 */
async function generateReport(
  reportType: ReportType,
  shiftStartTime: Date,
  shiftEndTime: Date,
  generatingClerkId: string
): Promise<XZReport> {
  // Get all completed orders in the shift period
  const orders = await prisma.order.findMany({
    where: {
      createdAt: {
        gte: shiftStartTime,
        lte: shiftEndTime,
      },
      status: {
        in: ['completed', 'voided'],
      },
    },
    include: {
      payments: true,
      clerk: true,
      items: true,
    },
  })

  const completedOrders = orders.filter((o) => o.status === 'completed')
  const voidedOrders = orders.filter((o) => o.status === 'voided')

  // Calculate financial totals
  const grossSales = completedOrders.reduce((sum, o) => sum + o.subtotal, 0)
  const taxCollected = completedOrders.reduce((sum, o) => sum + o.tax, 0)
  const netSales = completedOrders.reduce((sum, o) => sum + o.total, 0)
  const discounts = completedOrders.reduce((sum, o) => sum + o.discountUsd, 0)
  const voids = voidedOrders.reduce((sum, o) => sum + o.total, 0)

  // Get refunds from negative payments
  const payments = completedOrders.flatMap((o) => o.payments)
  const refunds = payments
    .filter((p) => p.amountUsd < 0)
    .reduce((sum, p) => sum + Math.abs(p.amountUsd), 0)

  // Calculate payment summary
  const paymentSummary = calculatePaymentSummary(payments)

  // Calculate clerk summary
  const clerkSummary = await calculateClerkSummary(orders)

  // Get void details
  const voidDetails = voidedOrders.map((o) => ({
    transactionNo: o.transactionNo,
    clerkName: o.clerk?.name || 'Unknown',
    amount: o.total,
    reason: o.voidReason || 'No reason provided',
    voidedAt: o.voidedAt || o.createdAt,
  }))

  // Calculate gift card activity
  const giftCardSales = await calculateGiftCardSales(shiftStartTime, shiftEndTime)
  const giftCardRedemptions = payments
    .filter((p) => p.type === 'giftcard' && p.amountUsd > 0)
    .reduce((sum, p) => sum + p.amountUsd, 0)

  // Calculate store credit activity
  const storeCreditIssued = await calculateStoreCreditIssued(shiftStartTime, shiftEndTime)
  const storeCreditRedeemed = payments
    .filter((p) => p.type === 'storecredit' && p.amountUsd > 0)
    .reduce((sum, p) => sum + p.amountUsd, 0)

  // Get last Z-report time
  const lastZReport = await prisma.sessionLog.findFirst({
    where: { action: 'Z_REPORT_GENERATED' },
    orderBy: { createdAt: 'desc' },
  })

  return {
    reportType,
    generatedAt: new Date(),
    shiftStartTime,
    shiftEndTime,
    grossSales,
    netSales,
    taxCollected,
    discounts,
    refunds,
    voids,
    paymentSummary,
    clerkSummary,
    orderCount: completedOrders.length,
    itemCount: completedOrders.reduce((sum, o) => sum + o.items.length, 0),
    averageOrderValue: completedOrders.length > 0 ? netSales / completedOrders.length : 0,
    voidDetails,
    giftCardSales,
    giftCardRedemptions,
    storeCreditIssued,
    storeCreditRedeemed,
    lastZReportTime: lastZReport?.createdAt,
  }
}

/**
 * Calculate payment summary
 */
function calculatePaymentSummary(payments: Payment[]): PaymentSummary[] {
  const summary: Record<string, { count: number; amount: number }> = {}

  for (const payment of payments) {
    if (payment.amountUsd > 0) {
      // Only count positive payments (not refunds)
      if (!summary[payment.type]) {
        summary[payment.type] = { count: 0, amount: 0 }
      }
      summary[payment.type].count++
      summary[payment.type].amount += payment.amountUsd
    }
  }

  return Object.entries(summary).map(([type, data]) => ({
    type,
    count: data.count,
    amount: data.amount,
  }))
}

/**
 * Calculate clerk summary
 */
async function calculateClerkSummary(orders: Order[]): Promise<ClerkSummary[]> {
  const clerkData: Record<
    string,
    {
      clerk: Clerk
      orderCount: number
      totalSales: number
      voidCount: number
      voidAmount: number
    }
  > = {}

  for (const order of orders) {
    if (!clerkData[order.clerkId]) {
      const clerk = await prisma.clerk.findUnique({
        where: { id: order.clerkId },
      })
      if (!clerk) continue

      clerkData[order.clerkId] = {
        clerk,
        orderCount: 0,
        totalSales: 0,
        voidCount: 0,
        voidAmount: 0,
      }
    }

    if (order.status === 'completed') {
      clerkData[order.clerkId].orderCount++
      clerkData[order.clerkId].totalSales += order.total
    } else if (order.status === 'voided') {
      clerkData[order.clerkId].voidCount++
      clerkData[order.clerkId].voidAmount += order.total
    }
  }

  return Object.values(clerkData).map((data) => ({
    clerkId: data.clerk.id,
    clerkName: data.clerk.name,
    role: data.clerk.role,
    orderCount: data.orderCount,
    totalSales: data.totalSales,
    voidCount: data.voidCount,
    voidAmount: data.voidAmount,
  }))
}

/**
 * Calculate gift card sales
 */
async function calculateGiftCardSales(startTime: Date, endTime: Date): Promise<number> {
  const logs = await prisma.sessionLog.findMany({
    where: {
      action: 'GIFT_CARD_CREATED',
      createdAt: {
        gte: startTime,
        lte: endTime,
      },
    },
  })

  // Parse amounts from log details
  let total = 0
  for (const log of logs) {
    const match = log.details?.match(/\$([\d.]+)/)
    if (match) {
      total += parseFloat(match[1])
    }
  }

  return total
}

/**
 * Calculate store credit issued
 */
async function calculateStoreCreditIssued(startTime: Date, endTime: Date): Promise<number> {
  const logs = await prisma.sessionLog.findMany({
    where: {
      action: { in: ['STORE_CREDIT_ADDED', 'STORE_CREDIT_APPLIED'] },
      createdAt: {
        gte: startTime,
        lte: endTime,
      },
    },
  })

  let total = 0
  for (const log of logs) {
    const match = log.details?.match(/\$([\d.]+)/)
    if (match) {
      total += parseFloat(match[1])
    }
  }

  return total
}

/**
 * Format report for thermal printer
 */
export function formatThermalPrint(report: XZReport): string {
  const lines: string[] = []
  const width = 42

  // Header
  lines.push('='.repeat(width))
  lines.push(centerText(`${report.reportType}-REPORT`, width))
  lines.push(centerText(`Generated: ${report.generatedAt.toLocaleString()}`, width))
  lines.push('='.repeat(width))

  // Shift info
  lines.push(`Shift: ${report.shiftStartTime?.toLocaleString()} -`)
  lines.push(`       ${report.shiftEndTime?.toLocaleString()}`)
  lines.push('')

  // Financial summary
  lines.push(leftRightText('GROSS SALES:', formatCurrency(report.grossSales), width))
  lines.push(leftRightText('TAX COLLECTED:', formatCurrency(report.taxCollected), width))
  lines.push(leftRightText('NET SALES:', formatCurrency(report.netSales), width))
  lines.push(leftRightText('DISCOUNTS:', `-${formatCurrency(report.discounts)}`, width))
  lines.push(leftRightText('REFUNDS:', `-${formatCurrency(report.refunds)}`, width))
  lines.push(leftRightText('VOIDS:', `-${formatCurrency(report.voids)}`, width))
  lines.push('-'.repeat(width))
  lines.push(leftRightText('TOTAL:', formatCurrency(report.netSales - report.refunds - report.voids), width))
  lines.push('')

  // Payment breakdown
  lines.push(centerText('PAYMENT METHODS', width))
  lines.push('-'.repeat(width))
  for (const payment of report.paymentSummary) {
    lines.push(leftRightText(`${payment.type.toUpperCase()}:`, formatCurrency(payment.amount), width))
  }
  lines.push('')

  // Clerk summary
  lines.push(centerText('CLERK PERFORMANCE', width))
  lines.push('-'.repeat(width))
  for (const clerk of report.clerkSummary) {
    lines.push(`${clerk.clerkName} (${clerk.role})`)
    lines.push(`  Orders: ${clerk.orderCount}  Sales: ${formatCurrency(clerk.totalSales)}`)
    if (clerk.voidCount > 0) {
      lines.push(`  Voids: ${clerk.voidCount} (${formatCurrency(clerk.voidAmount)})`)
    }
  }
  lines.push('')

  // Statistics
  lines.push(centerText('STATISTICS', width))
  lines.push('-'.repeat(width))
  lines.push(leftRightText('TOTAL ORDERS:', report.orderCount.toString(), width))
  lines.push(leftRightText('TOTAL ITEMS:', report.itemCount.toString(), width))
  lines.push(leftRightText('AVG ORDER:', formatCurrency(report.averageOrderValue), width))
  lines.push('')

  // Gift cards & store credit
  lines.push(centerText('GIFT CARD / STORE CREDIT', width))
  lines.push('-'.repeat(width))
  lines.push(leftRightText('GC Sales:', formatCurrency(report.giftCardSales), width))
  lines.push(leftRightText('GC Redemptions:', formatCurrency(report.giftCardRedemptions), width))
  lines.push(leftRightText('SC Issued:', formatCurrency(report.storeCreditIssued), width))
  lines.push(leftRightText('SC Redeemed:', formatCurrency(report.storeCreditRedeemed), width))
  lines.push('')

  // Footer
  lines.push('='.repeat(width))
  lines.push(centerText('*** END OF REPORT ***', width))
  lines.push('='.repeat(width))

  return lines.join('\n')
}

/**
 * Helper: Center text
 */
function centerText(text: string, width: number): string {
  const padding = Math.floor((width - text.length) / 2)
  return ' '.repeat(Math.max(0, padding)) + text
}

/**
 * Helper: Left-right aligned text
 */
function leftRightText(left: string, right: string, width: number): string {
  const spaceCount = width - left.length - right.length
  return left + ' '.repeat(Math.max(0, spaceCount)) + right
}

/**
 * Helper: Format currency
 */
function formatCurrency(amount: number): string {
  return `$${amount.toFixed(2)}`
}

/**
 * Get shift history
 */
export async function getShiftHistory(limit: number = 10): Promise<
  Array<{
    shiftStart: Date
    shiftEnd: Date
    grossSales: number
    orderCount: number
  }>
> {
  const zReports = await prisma.sessionLog.findMany({
    where: { action: 'Z_REPORT_GENERATED' },
    orderBy: { createdAt: 'desc' },
    take: limit,
  })

  const history: Array<{
    shiftStart: Date
    shiftEnd: Date
    grossSales: number
    orderCount: number
  }> = []

  for (let i = 0; i < zReports.length; i++) {
    const current = zReports[i]
    const previous = zReports[i + 1]

    const shiftStart = previous?.createdAt || new Date(current.createdAt.getTime() - 24 * 60 * 60 * 1000)
    const shiftEnd = current.createdAt

    // Get orders for this shift
    const orders = await prisma.order.findMany({
      where: {
        createdAt: {
          gte: shiftStart,
          lte: shiftEnd,
        },
        status: 'completed',
      },
    })

    history.push({
      shiftStart,
      shiftEnd,
      grossSales: orders.reduce((sum, o) => sum + o.total, 0),
      orderCount: orders.length,
    })
  }

  return history
}
