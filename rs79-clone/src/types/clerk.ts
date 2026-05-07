/**
 * Clerk Types for RS-79 POS System
 */

export enum ClerkRole {
  Admin = 'Admin',
  Manager = 'Manager',
  Clerk = 'Clerk',
}

export interface Clerk {
  id: string
  name: string
  role: ClerkRole
  active: boolean
  createdAt: string
  updatedAt?: string
}

export interface ClerkSession {
  id: string
  name: string
  role: ClerkRole
}

export interface ClerkWithStats extends Clerk {
  totalOrders: number
  totalSales: number
  averageOrderValue: number
}

export interface ClerkFormData {
  name: string
  role: ClerkRole
  pin: string
  active?: boolean
}

export interface LoginCredentials {
  pin: string
}

export interface LoginResponse {
  clerk: ClerkSession
}

export interface SessionResponse {
  session: ClerkSession | null
}

export interface SessionLog {
  id: string
  clerkId: string
  action: string
  details?: string
  ipAddress?: string
  createdAt: string
}
