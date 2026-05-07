import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

const SALT_ROUNDS = 10

// Hash PIN function
async function hashPin(pin: string): Promise<string> {
  return bcrypt.hash(pin, SALT_ROUNDS)
}

async function main() {
  console.log('🌱 Starting database seed...')

  // Clear existing data
  await prisma.payment.deleteMany()
  await prisma.orderItem.deleteMany()
  await prisma.order.deleteMany()
  await prisma.storeCredit.deleteMany()
  await prisma.giftCard.deleteMany()
  await prisma.exchangeRate.deleteMany()
  await prisma.sessionLog.deleteMany()
  await prisma.item.deleteMany()
  await prisma.customer.deleteMany()
  await prisma.clerk.deleteMany()

  console.log('🗑️  Cleared existing data')

  // Create Clerks with PINs
  const adminClerk = await prisma.clerk.create({
    data: {
      name: 'Admin User',
      role: 'Admin',
      pin: await hashPin('1234'),
      active: true,
    },
  })

  const managerClerk = await prisma.clerk.create({
    data: {
      name: 'Manager One',
      role: 'Manager',
      pin: await hashPin('5678'),
      active: true,
    },
  })

  const clerk1 = await prisma.clerk.create({
    data: {
      name: 'John Doe',
      role: 'Clerk',
      pin: await hashPin('0000'),
      active: true,
    },
  })

  const clerk2 = await prisma.clerk.create({
    data: {
      name: 'Jane Smith',
      role: 'Clerk',
      pin: await hashPin('1111'),
      active: true,
    },
  })

  console.log('👥 Created clerks:', { admin: adminClerk.name, manager: managerClerk.name, clerks: [clerk1.name, clerk2.name] })

  // Create Exchange Rates (USD base)
  const exchangeRates = [
    { fromCurrency: 'USD', toCurrency: 'USD', rate: 1.0 },
    { fromCurrency: 'USD', toCurrency: 'EUR', rate: 0.92 },
    { fromCurrency: 'USD', toCurrency: 'JPY', rate: 151.47 },
    { fromCurrency: 'USD', toCurrency: 'GBP', rate: 0.79 },
    { fromCurrency: 'EUR', toCurrency: 'USD', rate: 1.09 },
    { fromCurrency: 'JPY', toCurrency: 'USD', rate: 0.0066 },
    { fromCurrency: 'GBP', toCurrency: 'USD', rate: 1.27 },
  ]

  for (const rate of exchangeRates) {
    await prisma.exchangeRate.create({ data: rate })
  }
  console.log('💱 Created exchange rates')

  // Create Categories and Items
  const categories = [
    {
      name: 'Beverages',
      items: [
        { sku: 'BEV001', name: 'Espresso', price: 3.50, stockQty: 100 },
        { sku: 'BEV002', name: 'Cappuccino', price: 4.50, stockQty: 100 },
        { sku: 'BEV003', name: 'Latte', price: 4.75, stockQty: 100 },
        { sku: 'BEV004', name: 'Americano', price: 3.75, stockQty: 100 },
        { sku: 'BEV005', name: 'Mocha', price: 5.00, stockQty: 100 },
        { sku: 'BEV006', name: 'Tea', price: 2.50, stockQty: 100 },
        { sku: 'BEV007', name: 'Hot Chocolate', price: 4.00, stockQty: 100 },
        { sku: 'BEV008', name: 'Iced Coffee', price: 4.25, stockQty: 100 },
        { sku: 'BEV009', name: 'Smoothie', price: 6.00, stockQty: 50 },
        { sku: 'BEV010', name: 'Soda', price: 2.00, stockQty: 200 },
      ],
    },
    {
      name: 'Food',
      items: [
        { sku: 'FOOD001', name: 'Croissant', price: 3.00, stockQty: 30 },
        { sku: 'FOOD002', name: 'Muffin', price: 2.75, stockQty: 25 },
        { sku: 'FOOD003', name: 'Bagel', price: 2.50, stockQty: 40 },
        { sku: 'FOOD004', name: 'Sandwich', price: 8.50, stockQty: 20 },
        { sku: 'FOOD005', name: 'Salad', price: 9.00, stockQty: 15 },
        { sku: 'FOOD006', name: 'Soup', price: 6.00, stockQty: 25 },
        { sku: 'FOOD007', name: 'Pastry', price: 3.50, stockQty: 20 },
        { sku: 'FOOD008', name: 'Breakfast Burrito', price: 8.00, stockQty: 15 },
        { sku: 'FOOD009', name: 'Quiche', price: 7.50, stockQty: 12 },
        { sku: 'FOOD010', name: 'Pizza Slice', price: 4.50, stockQty: 20 },
      ],
    },
    {
      name: 'Retail',
      items: [
        { sku: 'RTL001', name: 'Coffee Beans (1lb)', price: 14.99, stockQty: 50 },
        { sku: 'RTL002', name: 'Travel Mug', price: 24.99, stockQty: 20 },
        { sku: 'RTL003', name: 'T-Shirt', price: 19.99, stockQty: 30 },
        { sku: 'RTL004', name: 'Gift Card $25', price: 25.00, stockQty: 100 },
        { sku: 'RTL005', name: 'Gift Card $50', price: 50.00, stockQty: 100 },
        { sku: 'RTL006', name: 'Gift Card $100', price: 100.00, stockQty: 100 },
      ],
    },
    {
      name: 'Merchandise',
      items: [
        { sku: 'MERCH001', name: 'Branded Hat', price: 22.00, stockQty: 15 },
        { sku: 'MERCH002', name: 'Sticker Pack', price: 5.00, stockQty: 100 },
        { sku: 'MERCH003', name: 'Notebook', price: 8.00, stockQty: 40 },
        { sku: 'MERCH004', name: 'Pen Set', price: 12.00, stockQty: 35 },
      ],
    },
  ]

  for (const category of categories) {
    for (const item of category.items) {
      await prisma.item.create({
        data: {
          ...item,
          category: category.name,
          active: true,
          lowStock: 10,
        },
      })
    }
  }
  console.log('🍔 Created items in', categories.length, 'categories')

  // Create Customers with Loyalty Cards
  const customers = [
    { name: 'Alice Johnson', phone: '555-0101', loyaltyCardNo: 'LOYAL001', loyaltyPoints: 250 },
    { name: 'Bob Williams', phone: '555-0102', loyaltyCardNo: 'LOYAL002', loyaltyPoints: 100 },
    { name: 'Carol Davis', phone: '555-0103', loyaltyCardNo: 'LOYAL003', loyaltyPoints: 500 },
    { name: 'David Brown', phone: '555-0104', loyaltyCardNo: 'LOYAL004', loyaltyPoints: 75 },
    { name: 'Emma Wilson', phone: '555-0105', loyaltyCardNo: 'LOYAL005', loyaltyPoints: 1000 },
    { name: 'Frank Miller', phone: '555-0106', loyaltyCardNo: 'LOYAL006', loyaltyPoints: 0 },
    { name: 'Grace Lee', phone: '555-0107', loyaltyCardNo: 'LOYAL007', loyaltyPoints: 350 },
    { name: 'Henry Taylor', phone: '555-0108', loyaltyCardNo: 'LOYAL008', loyaltyPoints: 200 },
    { name: 'Iris Chen', phone: '555-0109', loyaltyCardNo: 'LOYAL009', loyaltyPoints: 600 },
    { name: 'Jack Anderson', phone: '555-0110', loyaltyCardNo: 'LOYAL010', loyaltyPoints: 150 },
  ]

  for (const customerData of customers) {
    const customer = await prisma.customer.create({
      data: customerData,
    })
    
    // Add store credit for some customers
    if (['Carol Davis', 'Emma Wilson', 'Iris Chen'].includes(customer.name)) {
      await prisma.storeCredit.create({
        data: {
          customerId: customer.id,
          balance: customer.name === 'Emma Wilson' ? 50.00 : 25.00,
          totalEarned: customer.name === 'Emma Wilson' ? 100.00 : 50.00,
          totalSpent: customer.name === 'Emma Wilson' ? 50.00 : 25.00,
        },
      })
    }
  }
  console.log('👤 Created', customers.length, 'customers with loyalty cards')

  // Create Gift Cards
  const giftCards = [
    { code: 'GIFT001', balance: 25.00, originalAmount: 25.00 },
    { code: 'GIFT002', balance: 50.00, originalAmount: 50.00 },
    { code: 'GIFT003', balance: 100.00, originalAmount: 100.00 },
    { code: 'GIFT004', balance: 10.00, originalAmount: 25.00 }, // Partially used
    { code: 'GIFT005', balance: 75.00, originalAmount: 100.00 }, // Partially used
    { code: 'GIFT006', balance: 0.00, originalAmount: 50.00, isActive: false }, // Used up
  ]

  for (const card of giftCards) {
    await prisma.giftCard.create({
      data: {
        ...card,
        isActive: card.isActive !== false,
        expiresAt: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000), // 1 year expiry
      },
    })
  }
  console.log('🎁 Created', giftCards.length, 'gift cards')

  // Create Sample Orders (matching real transaction patterns)
  const sampleOrders = [
    { clerkId: clerk1.id, total: 12.50, paymentType: 'cash', currency: 'USD' },
    { clerkId: clerk2.id, total: 24.99, paymentType: 'card', currency: 'USD' },
    { clerkId: clerk1.id, total: 45.00, paymentType: 'split', currency: 'USD' },
    { clerkId: clerk2.id, total: 8.50, paymentType: 'crypto', currency: 'USD' },
    { clerkId: clerk1.id, total: 15.00, paymentType: 'giftcard', currency: 'USD' },
    { clerkId: clerk2.id, total: 32.25, paymentType: 'storecredit', currency: 'USD' },
    { clerkId: adminClerk.id, total: 18.75, paymentType: 'check', currency: 'USD' },
    { clerkId: clerk1.id, total: 11.20, paymentType: 'cash', currency: 'EUR' },
    { clerkId: clerk2.id, total: 2500, paymentType: 'card', currency: 'JPY' },
    { clerkId: managerClerk.id, total: 28.50, paymentType: 'cash', currency: 'GBP' },
  ]

  let transactionCounter = 1000
  for (const orderData of sampleOrders) {
    const tax = orderData.total * 0.08 // 8% tax
    const subtotal = orderData.total
    const total = subtotal + tax

    await prisma.order.create({
      data: {
        transactionNo: transactionCounter++,
        clerkId: orderData.clerkId,
        customerId: null,
        subtotal: subtotal,
        tax: tax,
        total: total,
        currency: orderData.currency,
        currencyRate: orderData.currency === 'EUR' ? 0.92 : orderData.currency === 'JPY' ? 151.47 : orderData.currency === 'GBP' ? 0.79 : 1.0,
        paymentType: orderData.paymentType,
        tendered: total,
        change: 0,
        status: 'completed',
        kdsStatus: 'done',
        amountPaid: total,
        balanceDue: 0,
        items: {
          create: [
            {
              itemId: 'sample-item-1',
              name: 'Sample Item',
              price: subtotal,
              qty: 1,
              lineTotal: subtotal,
            },
          ],
        },
        payments: {
          create: [
            {
              clerkId: orderData.clerkId,
              type: orderData.paymentType,
              amountUsd: total / (orderData.currency === 'EUR' ? 0.92 : orderData.currency === 'JPY' ? 151.47 : orderData.currency === 'GBP' ? 0.79 : 1.0),
              amountNative: total,
              currency: orderData.currency,
              currencyRate: orderData.currency === 'EUR' ? 0.92 : orderData.currency === 'JPY' ? 151.47 : orderData.currency === 'GBP' ? 0.79 : 1.0,
            },
          ],
        },
      },
    })
  }
  console.log('📝 Created', sampleOrders.length, 'sample orders')

  console.log('✅ Database seed completed successfully!')
}

main()
  .catch((e) => {
    console.error('❌ Seed failed:', e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
