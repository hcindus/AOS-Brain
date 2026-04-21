package com.ps.pos.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.ps.pos.POSRepository
import com.ps.pos.data.entities.LineItem
import com.ps.pos.data.entities.Product
import com.ps.pos.data.entities.Transaction
import com.ps.pos.utils.TaxCalculator
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import java.util.*

class RegisterViewModel(
    private val repository: POSRepository = POSRepository()
) : ViewModel() {

    private val _cartItems = MutableStateFlow<List<LineItem>>(emptyList())
    val cartItems: StateFlow<List<LineItem>> = _cartItems.asStateFlow()

    private val _subtotal = MutableStateFlow(0.0)
    val subtotal: StateFlow<Double> = _subtotal.asStateFlow()

    private val _tax = MutableStateFlow(0.0)
    val tax: StateFlow<Double> = _tax.asStateFlow()

    private val _total = MutableStateFlow(0.0)
    val total: StateFlow<Double> = _total.asStateFlow()

    private var currentProduct: Product? = null
    private var currentQuantity: Int = 1

    private val _transactions = MutableStateFlow<List<Transaction>>(emptyList())

    init {
        // Add sample products for testing
        viewModelScope.launch {
            addSampleProducts()
        }
    }

    private suspend fun addSampleProducts() {
        val sampleProducts = listOf(
            Product(plu = "1001", name = "Coca-Cola 20oz", price = 2.49, category = "Beverages"),
            Product(plu = "1002", name = "Doritos Nacho", price = 1.99, category = "Snacks"),
            Product(plu = "1003", name = "Marlboro Red", price = 8.99, category = "Tobacco"),
            Product(plu = "1004", name = "Red Bull 8.4oz", price = 2.99, category = "Beverages"),
            Product(plu = "1005", name = "Snickers Bar", price = 1.29, category = "Snacks"),
            Product(plu = "1006", name = "Bud Light 6pk", price = 8.49, category = "Alcohol"),
            Product(plu = "1007", name = "USB Cable", price = 5.99, category = "Electronics"),
            Product(plu = "1008", name = "Lighter", price = 1.49, category = "General")
        )
        sampleProducts.forEach { repository.insertProduct(it) }
    }

    fun lookupProduct(plu: String) {
        viewModelScope.launch {
            currentProduct = repository.getProductByPlu(plu)
        }
    }

    fun setQuantity(qty: Int) {
        currentQuantity = qty.coerceAtLeast(1)
    }

    fun addToCart() {
        currentProduct?.let { product ->
            val lineItem = LineItem(
                productId = product.id,
                productName = product.name,
                quantity = currentQuantity.toDouble(),
                unitPrice = product.price,
                totalPrice = product.price * currentQuantity
            )
            _cartItems.value = _cartItems.value + lineItem
            updateTotals()
            currentProduct = null
            currentQuantity = 1
        }
    }

    fun removeFromCart(item: LineItem) {
        _cartItems.value = _cartItems.value.filter { it != item }
        updateTotals()
    }

    fun clearCart() {
        _cartItems.value = emptyList()
        updateTotals()
    }

    private fun updateTotals() {
        val sub = _cartItems.value.sumOf { it.totalPrice }
        val taxAmt = TaxCalculator.calculateTax(sub)
        _subtotal.value = sub
        _tax.value = taxAmt
        _total.value = sub + taxAmt
    }

    fun completeTransaction(paymentType: String, tendered: Double) {
        viewModelScope.launch {
            val transaction = Transaction(
                transactionNumber = generateTransactionNumber(),
                timestamp = System.currentTimeMillis(),
                subtotal = _subtotal.value,
                tax = _tax.value,
                total = _total.value,
                paymentType = paymentType,
                tendered = tendered,
                change = tendered - _total.value,
                status = "COMPLETED"
            )
            repository.insertTransaction(transaction, _cartItems.value)
            clearCart()
        }
    }

    private fun generateTransactionNumber(): String {
        return "TXN-${UUID.randomUUID().toString().take(8).uppercase()}"
    }
}