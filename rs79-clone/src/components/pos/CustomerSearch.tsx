'use client'

import { useState, useCallback, useEffect } from 'react'
import { Customer } from '@/types'
import { Search, X, User, Phone, CreditCard } from 'lucide-react'
import { cn } from '@/lib/utils'

interface CustomerSearchProps {
  onSelect: (customer: Customer) => void
  onClose: () => void
}

export function CustomerSearch({ onSelect, onClose }: CustomerSearchProps) {
  const [query, setQuery] = useState('')
  const [customers, setCustomers] = useState<Customer[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const searchCustomers = useCallback(async (searchQuery: string) => {
    if (!searchQuery.trim()) {
      setCustomers([])
      return
    }
    
    setIsLoading(true)
    try {
      const response = await fetch(`/api/customers?q=${encodeURIComponent(searchQuery)}`)
      const data = await response.json()
      if (data.success) {
        setCustomers(data.data || [])
      }
    } catch (error) {
      console.error('Failed to search customers:', error)
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    const timeout = setTimeout(() => searchCustomers(query), 300)
    return () => clearTimeout(timeout)
  }, [query, searchCustomers])

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-md w-full shadow-2xl overflow-hidden">
        <div className="p-6 border-b border-surface-tertiary">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-text-primary">Add Customer</h2>
            <button
              onClick={onClose}
              className="p-2 text-text-secondary hover:text-text-primary hover:bg-surface-secondary rounded-lg transition-colors"
            >
              <X size={20} />
            </button>
          </div>
          
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" size={20} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by name or phone..."
              className="w-full pl-10 pr-4 py-3 border border-surface-tertiary rounded-xl text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              autoFocus
            />
          </div>
        </div>

        <div className="max-h-[400px] overflow-y-auto">
          {isLoading ? (
            <div className="p-8 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-2"></div>
              <p className="text-text-secondary">Searching...</p>
            </div>
          ) : query.trim() && customers.length === 0 ? (
            <div className="p-8 text-center text-text-muted">
              <User size={48} className="mx-auto mb-4 opacity-30" />
              <p>No customers found</p>
            </div>
          ) : customers.length > 0 ? (
            <div className="p-3 space-y-1">
              {customers.map((customer) => (
                <button
                  key={customer.id}
                  onClick={() => onSelect(customer)}
                  className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-surface-secondary transition-colors text-left"
                >
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <User size={20} className="text-primary" />
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-text-primary truncate">{customer.name}</p>
                    <div className="flex items-center gap-3 text-sm text-text-secondary">
                      {customer.phone && (
                        <span className="flex items-center gap-1">
                          <Phone size={12} />
                          {customer.phone}
                        </span>
                      )}
                      <span className="flex items-center gap-1">
                        <CreditCard size={12} />
                        {customer.loyaltyCardNo}
                      </span>
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <span className={cn(
                      "text-sm font-medium px-2 py-1 rounded-full",
                      customer.loyaltyPoints > 0 ? "bg-amber-100 text-amber-700" : "bg-surface-tertiary text-text-muted"
                    )}>
                      {customer.loyaltyPoints} pts
                    </span>
                  </div>
                </button>
              ))}
            </div>
          ) : (
            <div className="p-8 text-center text-text-muted">
              <Search size={48} className="mx-auto mb-4 opacity-30" />
              <p className="text-lg font-medium mb-1">Search for customers</p>
              <p className="text-sm">Enter a name or phone number</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
