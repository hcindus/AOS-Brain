package com.ps.pos

import com.ps.pos.data.AppDatabase
import com.ps.pos.data.entities.LineItem
import com.ps.pos.data.entities.Product
import com.ps.pos.data.entities.Transaction
import com.ps.pos.utils.TaxCalculator
import kotlinx.coroutines.flow.Flow
import java.util.Date
import java.util.UUID

class POSRepository(private val database: AppDatabase) {
    
    val allProducts: Flow<List<Product>> = database.productDao().getAll()
    val allTransactions: Flow<List<Transaction>> = database.transactionDao().getAll()
    
    suspend fun getProductByPlu(pluCode: String): Product? {
        return database.productDao().getByPlu(pluCode)
    }
    
    suspend fun createTransaction(
        cartItems: List<CartItem>,
        paymentType: String,
        tendered: Double
    ): Transaction {
        var subtotal = 0.0
        var totalTax = 0.0
        
        // Calculate totals
        cartItems.forEach { item ->
            val (basePrice, tax) = TaxCalculator.calculateTax(
                item.unitPrice * item.quantity,
                item.product.taxRate,
                item.product.taxType
            )
            subtotal += basePrice
            totalTax += tax
        }
        
        val total = subtotal + totalTax
        val change = if (tendered > total) tendered - total else 0.0
        
        val transaction = Transaction(
            id = UUID.randomUUID().toString(),
            timestamp = Date().time,
            subtotal = subtotal,
            taxAmount = totalTax,
            total = total,
            paymentType = paymentType,
            tendered = tendered,
            change = change,
            status = "COMPLETED"
        )
        
        // Insert transaction
        database.transactionDao().insert(transaction)
        
        // Insert line items
        cartItems.forEach { item ->
            val (_, tax) = TaxCalculator.calculateTax(
                item.unitPrice * item.quantity,
                item.product.taxRate,
                item.product.taxType
            )
            
            val lineItem = LineItem(
                transactionId = transaction.id,
                pluCode = item.product.pluCode,
                name = item.product.name,
                quantity = item.quantity,
                unitPrice = item.unitPrice,
                taxAmount = tax,
                total = (item.unitPrice * item.quantity) + tax
            )
            database.lineItemDao().insert(lineItem)
            
            // Decrement stock if tracked
            if (item.product.trackInventory) {
                database.productDao().decrementStock(item.product.pluCode, item.quantity)
            }
        }
        
        return transaction
    }
    
    fun getLineItemsForTransaction(txId: String): Flow<List<LineItem>> {
        return database.lineItemDao().getForTransaction(txId)
    }
    
    data class CartItem(
        val product: Product,
        val quantity: Double,
        val unitPrice: Double
    )
}
