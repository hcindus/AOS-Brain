package com.ps.pos.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.ps.pos.POSRepository
import com.ps.pos.data.entities.Transaction
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import java.util.*

class TransactionViewModel(
    private val repository: POSRepository = POSRepository()
) : ViewModel() {

    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()

    private val _selectedDate = MutableStateFlow<String?>(null)
    val selectedDate: StateFlow<String?> = _selectedDate.asStateFlow()

    private val _transactions = MutableStateFlow<List<Transaction>>(emptyList())
    val transactions: StateFlow<List<Transaction>> = _transactions.asStateFlow()

    private val _todayTotal = MutableStateFlow(0.0)
    val todayTotal: StateFlow<Double> = _todayTotal.asStateFlow()

    init {
        viewModelScope.launch {
            loadTransactions()
        }
    }

    private suspend fun loadTransactions() {
        // Mock data for demonstration
        val mockTransactions = generateMockTransactions()
        _transactions.value = mockTransactions
        calculateTodayTotal(mockTransactions)
    }

    private fun generateMockTransactions(): List<Transaction> {
        val calendar = Calendar.getInstance()
        return listOf(
            Transaction(
                transactionNumber = "TXN-A1B2C3D4",
                timestamp = calendar.timeInMillis,
                subtotal = 15.47,
                tax = 1.28,
                total = 16.75,
                paymentType = "Cash",
                tendered = 20.00,
                change = 3.25,
                status = "COMPLETED"
            ),
            Transaction(
                transactionNumber = "TXN-E5F6G7H8",
                timestamp = calendar.apply { add(Calendar.HOUR, -2) }.timeInMillis,
                subtotal = 8.99,
                tax = 0.74,
                total = 9.73,
                paymentType = "Card",
                tendered = 9.73,
                change = 0.0,
                status = "COMPLETED"
            ),
            Transaction(
                transactionNumber = "TXN-I9J0K1L2",
                timestamp = calendar.apply { add(Calendar.HOUR, -3) }.timeInMillis,
                subtotal = 24.96,
                tax = 2.06,
                total = 27.02,
                paymentType = "Cash",
                tendered = 30.00,
                change = 2.98,
                status = "COMPLETED"
            ),
            Transaction(
                transactionNumber = "TXN-M3N4O5P6",
                timestamp = calendar.apply { add(Calendar.DAY_OF_YEAR, -1) }.timeInMillis,
                subtotal = 12.50,
                tax = 1.03,
                total = 13.53,
                paymentType = "Other",
                tendered = 13.53,
                change = 0.0,
                status = "COMPLETED"
            )
        )
    }

    private fun calculateTodayTotal(transactions: List<Transaction>) {
        val today = Calendar.getInstance().apply {
            set(Calendar.HOUR_OF_DAY, 0)
            set(Calendar.MINUTE, 0)
            set(Calendar.SECOND, 0)
            set(Calendar.MILLISECOND, 0)
        }.timeInMillis

        val todayTotal = transactions
            .filter { it.timestamp >= today && it.status == "COMPLETED" }
            .sumOf { it.total }

        _todayTotal.value = todayTotal
    }

    fun onSearchQueryChange(query: String) {
        _searchQuery.value = query
        viewModelScope.launch {
            if (query.isBlank()) {
                loadTransactions()
            } else {
                val allTransactions = generateMockTransactions()
                _transactions.value = allTransactions.filter {
                    it.transactionNumber.contains(query, ignoreCase = true) ||
                    it.paymentType.contains(query, ignoreCase = true)
                }
            }
        }
    }

    fun reprintReceipt(transaction: Transaction) {
        // Trigger printer service to reprint
        viewModelScope.launch {
            // In real implementation, call PrinterService
            println("Reprinting receipt for ${transaction.transactionNumber}")
        }
    }

    fun onDateSelected(date: String?) {
        _selectedDate.value = date
        viewModelScope.launch {
            // Filter transactions by date
            loadTransactions()
        }
    }
}