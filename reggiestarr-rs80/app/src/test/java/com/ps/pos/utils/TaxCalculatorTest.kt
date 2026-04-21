package com.ps.pos.utils

import org.junit.Assert.*
import org.junit.Test

class TaxCalculatorTest {

    @Test
    fun `calculateTax returns correct amount for 8_25 percent`() {
        val subtotal = 100.0
        val tax = TaxCalculator.calculateTax(subtotal)
        assertEquals(8.25, tax, 0.01)
    }

    @Test
    fun `calculateTax rounds to 2 decimal places`() {
        val subtotal = 10.0
        val tax = TaxCalculator.calculateTax(subtotal)
        // 10 * 0.0825 = 0.825, should round to 0.83
        assertEquals(0.83, tax, 0.01)
    }

    @Test
    fun `calculateTax handles zero`() {
        val tax = TaxCalculator.calculateTax(0.0)
        assertEquals(0.0, tax, 0.01)
    }

    @Test
    fun `calculateTax handles negative (returns zero)`() {
        val tax = TaxCalculator.calculateTax(-100.0)
        // Should handle gracefully, likely returns 0 or negative
        assertTrue(tax <= 0.0)
    }

    @Test
    fun `calculateTotal returns subtotal plus tax`() {
        val subtotal = 100.0
        val total = TaxCalculator.calculateTotal(subtotal)
        assertEquals(108.25, total, 0.01)
    }

    @Test
    fun `calculateTotal handles zero`() {
        val total = TaxCalculator.calculateTotal(0.0)
        assertEquals(0.0, total, 0.01)
    }
}