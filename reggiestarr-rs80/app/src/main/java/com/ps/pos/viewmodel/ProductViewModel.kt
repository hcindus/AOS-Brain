package com.ps.pos.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.ps.pos.POSRepository
import com.ps.pos.data.entities.Product
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class ProductViewModel(
    private val repository: POSRepository = POSRepository()
) : ViewModel() {

    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()

    private val _products = MutableStateFlow<List<Product>>(emptyList())
    val products: StateFlow<List<Product>> = _products.asStateFlow()

    init {
        // Load all products initially
        viewModelScope.launch {
            loadProducts()
        }

        // Filter products based on search query
        viewModelScope.launch {
            searchQuery.collect { query ->
                if (query.isBlank()) {
                    loadProducts()
                } else {
                    searchProducts(query)
                }
            }
        }
    }

    private suspend fun loadProducts() {
        // In a real implementation, this would fetch from database
        // For now, using mock data
        _products.value = getMockProducts()
    }

    private suspend fun searchProducts(query: String) {
        val allProducts = getMockProducts()
        _products.value = allProducts.filter {
            it.name.contains(query, ignoreCase = true) ||
            it.plu.contains(query, ignoreCase = true) ||
            it.barcode?.contains(query, ignoreCase = true) == true
        }
    }

    private fun getMockProducts(): List<Product> {
        return listOf(
            Product(plu = "1001", name = "Coca-Cola 20oz", price = 2.49, category = "Beverages"),
            Product(plu = "1002", name = "Doritos Nacho", price = 1.99, category = "Snacks"),
            Product(plu = "1003", name = "Marlboro Red", price = 8.99, category = "Tobacco"),
            Product(plu = "1004", name = "Red Bull 8.4oz", price = 2.99, category = "Beverages"),
            Product(plu = "1005", name = "Snickers Bar", price = 1.29, category = "Snacks"),
            Product(plu = "1006", name = "Bud Light 6pk", price = 8.49, category = "Alcohol"),
            Product(plu = "1007", name = "USB Cable", price = 5.99, category = "Electronics"),
            Product(plu = "1008", name = "Lighter", price = 1.49, category = "General")
        )
    }

    fun onSearchQueryChange(query: String) {
        _searchQuery.value = query
    }

    fun addProduct(product: Product) {
        viewModelScope.launch {
            repository.insertProduct(product)
            loadProducts()
        }
    }

    fun updateProduct(product: Product) {
        viewModelScope.launch {
            // In real implementation, call repository.updateProduct(product)
            loadProducts()
        }
    }

    fun deleteProduct(product: Product) {
        viewModelScope.launch {
            // In real implementation, call repository.deleteProduct(product)
            loadProducts()
        }
    }
}