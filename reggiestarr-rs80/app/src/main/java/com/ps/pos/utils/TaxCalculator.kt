package com.ps.pos.utils

object TaxCalculator {
    private const val TAX_RATE = 0.0825 // 8.25% - adjust for your jurisdiction

    fun calculateTax(subtotal: Double): Double {
        return (subtotal * TAX_RATE * 100).toInt() / 100.0 // Round to 2 decimals
    }

    fun calculateTotal(subtotal: Double): Double {
        return subtotal + calculateTax(subtotal)
    }
}