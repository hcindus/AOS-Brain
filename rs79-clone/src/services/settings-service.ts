import { prisma } from '@/lib/db'
import { TaxConfig, parseTaxConfig, DEFAULT_TAX_CONFIG } from '@/lib/tax'
import { Prisma } from '@prisma/client'

export interface StoreSettings {
  taxMode: 'exclusive' | 'inclusive'
  taxConfig: TaxConfig
  currency: string
  receiptHeader?: string
  receiptFooter?: string
}

const DEFAULT_SETTINGS: StoreSettings = {
  taxMode: 'exclusive',
  taxConfig: DEFAULT_TAX_CONFIG,
  currency: 'USD',
}

export async function getStoreSettings(): Promise<StoreSettings> {
  try {
    const settings = await prisma.storeSettings.findFirst()
    
    if (!settings) {
      // Create default settings without receipt fields initially
      const createData: Prisma.StoreSettingsCreateInput = {
        taxMode: DEFAULT_SETTINGS.taxMode,
        taxConfig: JSON.stringify(DEFAULT_SETTINGS.taxConfig),
        currency: DEFAULT_SETTINGS.currency,
      }
      await prisma.storeSettings.create({ data: createData })
      return DEFAULT_SETTINGS
    }
    
    return {
      taxMode: settings.taxMode as 'exclusive' | 'inclusive',
      taxConfig: parseTaxConfig(settings.taxConfig ?? undefined),
      currency: settings.currency,
      receiptHeader: settings.receiptHeader ?? undefined,
      receiptFooter: settings.receiptFooter ?? undefined,
    }
  } catch (error) {
    console.error('Failed to get store settings:', error)
    return DEFAULT_SETTINGS
  }
}

export async function updateStoreSettings(
  settings: Partial<StoreSettings>
): Promise<{ success: boolean; error?: string }> {
  try {
    const existing = await prisma.storeSettings.findFirst()
    
    if (existing) {
      // Update existing - build partial update
      const updateData: Prisma.StoreSettingsUpdateInput = {
        updatedAt: new Date(),
      }
      
      if (settings.taxMode) updateData.taxMode = settings.taxMode
      if (settings.taxConfig) updateData.taxConfig = JSON.stringify(settings.taxConfig)
      if (settings.currency) updateData.currency = settings.currency
      if (settings.receiptHeader !== undefined) {
        updateData.receiptHeader = settings.receiptHeader || undefined
      }
      if (settings.receiptFooter !== undefined) {
        updateData.receiptFooter = settings.receiptFooter || undefined
      }
      
      await prisma.storeSettings.update({
        where: { id: existing.id },
        data: updateData,
      })
    } else {
      // Create new
      const createData: Prisma.StoreSettingsCreateInput = {
        taxMode: settings.taxMode ?? DEFAULT_SETTINGS.taxMode,
        taxConfig: settings.taxConfig 
          ? JSON.stringify(settings.taxConfig) 
          : JSON.stringify(DEFAULT_SETTINGS.taxConfig),
        currency: settings.currency ?? DEFAULT_SETTINGS.currency,
      }
      
      if (settings.receiptHeader !== undefined) {
        createData.receiptHeader = settings.receiptHeader || undefined
      }
      if (settings.receiptFooter !== undefined) {
        createData.receiptFooter = settings.receiptFooter || undefined
      }
      
      await prisma.storeSettings.create({ data: createData })
    }
    
    return { success: true }
  } catch (error) {
    console.error('Failed to update store settings:', error)
    return { success: false, error: (error as Error).message }
  }
}

// Helper to get current tax config
export async function getTaxConfig(): Promise<TaxConfig> {
  const settings = await getStoreSettings()
  return settings.taxConfig
}

// Helper to get tax mode
export async function getTaxMode(): Promise<'exclusive' | 'inclusive'> {
  const settings = await getStoreSettings()
  return settings.taxMode
}