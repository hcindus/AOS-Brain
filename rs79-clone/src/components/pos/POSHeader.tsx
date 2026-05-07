'use client'

import { cn } from '@/lib/utils'
import { User, LogOut, Clock, Settings, Bell, Menu } from 'lucide-react'
import type { Clerk } from '@/types'

interface POSHeaderProps {
  clerk: Clerk
  onLogout: () => void
  onOpenSettings?: () => void
  onOpenMenu?: () => void
  currentTime?: string
}

export function POSHeader({
  clerk,
  onLogout,
  onOpenSettings,
  onOpenMenu,
  currentTime,
}: POSHeaderProps) {
  const roleColors = {
    Admin: 'bg-accent-danger/10 text-accent-danger',
    Manager: 'bg-accent-warning/10 text-accent-warning',
    Clerk: 'bg-primary/10 text-primary',
  }

  return (
    <header className="h-16 bg-white border-b border-surface-tertiary flex items-center justify-between px-4 lg:px-6">
      <div className="flex items-center gap-4">
        {onOpenMenu && (
          <button
            onClick={onOpenMenu}
            className="lg:hidden p-2 -ml-2 text-text-secondary hover:text-text-primary hover:bg-surface-secondary rounded-lg transition-colors"
          >
            <Menu size={20} />
          </button>
        )}
        
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center shadow-md shadow-primary/20">
            <span className="text-white font-bold text-lg">RS</span>
          </div>
          <div className="hidden sm:block">
            <h1 className="font-bold text-text-primary leading-tight">RS-79</h1>
            <p className="text-xs text-text-secondary">POS System</p>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <{/* Time Display */}
        <div className="hidden md:flex items-center gap-2 text-text-secondary">
          <Clock size={16} />
          <span className="text-sm font-medium">{currentTime || '--:--'}</span>
        </div>

        <{/* Notifications */}
        <button
          onClick={() => {}}
          className="relative p-2 text-text-secondary hover:text-text-primary hover:bg-surface-secondary rounded-lg transition-colors"
        >
          <Bell size={20} />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-accent-danger rounded-full"></span>
        </button>

        <{/* Clerk Info */}
        <div className="flex items-center gap-3 pl-4 border-l border-surface-tertiary">
          <div className="hidden sm:block text-right">
            <p className="font-semibold text-text-primary text-sm">{clerk.name}</p>
            <span className={cn(
              'inline-block px-2 py-0.5 rounded-full text-xs font-medium',
              roleColors[clerk.role] || roleColors.Clerk
            )}>
              {clerk.role}
            </span>
          </div>
          
          <div className="w-9 h-9 bg-surface-secondary rounded-full flex items-center justify-center">
            <User size={18} className="text-text-secondary" />
          </div>

          <button
            onClick={onLogout}
            className="p-2 text-text-secondary hover:text-accent-danger hover:bg-red-50 rounded-lg transition-colors"
            title="Logout"
          >
            <LogOut size={18} />
          </button>

          {onOpenSettings && (
            <button
              onClick={onOpenSettings}
              className="hidden sm:block p-2 text-text-secondary hover:text-text-primary hover:bg-surface-secondary rounded-lg transition-colors"
              title="Settings"
            >
              <Settings size={18} />
            </button>
          )}
        </div>
      </div>
    </header>
  )
}
