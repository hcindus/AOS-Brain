package com.ps.pos

import com.ps.pos.data.entities.LineItem
import com.ps.pos.data.entities.Product
import com.ps.pos.data.entities.Transaction

class POSRepository {
    // Mock implementation - replace with actual database calls
    private val products = mutableListOf<Product>()
    private val transactions = mutableListOf<Transaction>()
    private val lineItems = mutableListOf<LineItem>()

    suspend fun getProductByPlu(plu: String): Product? {
        return products.find { it.plu == plu }
    }

    suspend fun insertProduct(product: Product) {
        products.add(product)
    }

    suspend fun insertTransaction(transaction: Transaction, items: List<LineItem>) {
        val txnId = transactions.size.toLong() + 1
        transactions.add(transaction.copy(id = txnId))
        items.forEach { item ->
            lineItems.add(item.copy(transactionId = txnId))
        }
    }
}