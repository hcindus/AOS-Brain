package com.ps.pos.utils

import com.ps.pos.data.entities.Product

object TaxCalculator {
    
    fun calculateTax(price: Double, taxRate: Double, taxType: String): Pair<Double, Double> {
        return when (taxType.uppercase()) {
            "INCLUSIVE" -> {
                // Price already includes tax
                val taxAmount = price - (price / (1 + taxRate))
                val basePrice = price - taxAmount
                Pair(basePrice, taxAmount)
            }
            "EXEMPT" -> {
                // No tax
                Pair(price, 0.0)
            }
            else -> {
                // EXCLUSIVE - add tax to price
                val taxAmount = price * taxRate
                Pair(price, taxAmount)
            }
        }
    }

    fun getDisplayPrice(product: Product): Double {
        return if (product.taxType == "INCLUSIVE") {
            // For inclusive, show the total (price already includes tax)
            product.price
        } else {
            product.price
        }
    }

    fun getPriceBeforeTax(product: Product): Double {
        return if (product.taxType == "INCLUSIVE") {
            val (base, _) = calculateTax(product.price, product.taxRate, product.taxType)
            base
        } else {
            product.price
        }
    }
}
