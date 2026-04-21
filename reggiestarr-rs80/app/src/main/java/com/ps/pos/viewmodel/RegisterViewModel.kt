package com.ps.pos.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.ps.pos.POSRepository
import com.ps.pos.data.entities.Product
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class RegisterViewModel(private val repository: POSRepository) : ViewModel() {
    
    val products: StateFlow<List<Product>> = repository.allProducts
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    
    private val _cart = MutableStateFlow<List<CartItem>>(emptyList())
    val cart: StateFlow<List<CartItem>> = _cart.asStateFlow()
    
    private val _currentInput = MutableStateFlow("")
    val currentInput: StateFlow<String> = _currentInput.asStateFlow()
    
    private val _showCheckout = MutableStateFlow(false)
    val showCheckout: StateFlow<Boolean> = _showCheckout.asStateFlow()
    
    private val _selectedProduct = MutableStateFlow<Product?>(null)
    val selectedProduct: StateFlow<Product?> = _selectedProduct.asStateFlow()
    
    private val _customPrice = MutableStateFlow(0.0)
    
    fun onDigitInput(digit: String) {
        _currentInput.value += digit
    }
    
    fun onClear() {
        _currentInput.value = ""
        _selectedProduct.value = null
        _customPrice.value = 0.0
    }
    
    fun onDelete() {
        if (_currentInput.value.isNotEmpty()) {
            _currentInput.value = _currentInput.value.dropLast(1)
        }
    }
    
    fun onEnter() {
        viewModelScope.launch {
            val input = _currentInput.value
            
            // Try to find product by PLU
            val product = repository.getProductByPlu(input.uppercase())
            
            if (product != null) {
                if (product.openPrice) {
                    // Open price item - need custom price
                    _selectedProduct.value = product
                    _customPrice.value = 0.0
                } else {
                    // Fixed price - add to cart
                    addToCart(product, 1.0, product.price)
                    onClear()
                }
            } else {
                // Could be quantity entry or custom price
                val numericValue = input.toDoubleOrNull()
                if (numericValue != null && numericValue > 0) {
                    _customPrice.value = numericValue
                }
            }
        }
    }
    
    fun onProductClick(product: Product) {
        if (product.openPrice) {
            _selectedProduct.value = product
            _currentInput.value = ""
        } else {
            addToCart(product, 1.0, product.price)
        }
    }
    
    fun addToCart(product: Product, quantity: Double, price: Double) {
        val currentCart = _cart.value.toMutableList()
        
        // Check if item already in cart
        val existingIndex = currentCart.indexOfFirst { 
            it.product.pluCode == product.pluCode && it.unitPrice == price 
        }
        
        if (existingIndex >= 0) {
            // Update quantity
            val existing = currentCart[existingIndex]
            currentCart[existingIndex] = existing.copy(quantity = existing.quantity + quantity)
        } else {
            // Add new item
            currentCart.add(CartItem(product, quantity, price))
        }
        
        _cart.value = currentCart
    }
    
    fun removeFromCart(index: Int) {
        val currentCart = _cart.value.toMutableList()
        if (index in currentCart.indices) {
            currentCart.removeAt(index)
            _cart.value = currentCart
        }
    }
    
    fun clearCart() {
        _cart.value = emptyList()
    }
    
    fun onCheckout() {
        if (_cart.value.isNotEmpty()) {
            _showCheckout.value = true
        }
    }
    
    fun dismissCheckout() {
        _showCheckout.value = false
    }
    
    fun completeCheckout(paymentType: String, tendered: Double) {
        viewModelScope.launch {
            val cartItems = _cart.value.map { 
                POSRepository.CartItem(it.product, it.quantity, it.unitPrice) 
            }
            
            repository.createTransaction(cartItems, paymentType, tendered)
            clearCart()
            dismissCheckout()
        }
    }
    
    data class CartItem(
        val product: Product,
        val quantity: Double,
        val unitPrice: Double
    )
}

class RegisterViewModelFactory(private val repository: POSRepository) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(RegisterViewModel::class.java)) {
            return RegisterViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
