package com.ps.pos.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import java.util.*

// Data classes for reports
data class TopProduct(
    val name: String,
    val quantity: Int,
    val revenue: Double
)

data class CategorySales(
    val name: String,
    val amount: Double,
    val percentage: Float
)

class ReportsViewModel : ViewModel() {

    enum class TimePeriod {
        TODAY, WEEK, MONTH, YEAR
    }

    private val _selectedPeriod = MutableStateFlow(TimePeriod.TODAY)
    val selectedPeriod: StateFlow<TimePeriod> = _selectedPeriod.asStateFlow()

    private val _dailySales = MutableStateFlow(0.0)
    val dailySales: StateFlow<Double> = _dailySales.asStateFlow()

    private val _weeklySales = MutableStateFlow(0.0)
    val weeklySales: StateFlow<Double> = _weeklySales.asStateFlow()

    private val _monthlySales = MutableStateFlow(0.0)
    val monthlySales: StateFlow<Double> = _monthlySales.asStateFlow()

    private val _topProducts = MutableStateFlow<List<TopProduct>>(emptyList())
    val topProducts: StateFlow<List<TopProduct>> = _topProducts.asStateFlow()

    private val _salesByCategory = MutableStateFlow<List<CategorySales>>(emptyList())
    val salesByCategory: StateFlow<List<CategorySales>> = _salesByCategory.asStateFlow()

    init {
        loadReports()
    }

    private fun loadReports() {
        viewModelScope.launch {
            // Generate mock data for demonstration
            generateMockData()
        }
    }

    private fun generateMockData() {
        // Daily sales (today)
        _dailySales.value = 1250.75

        // Weekly sales
        _weeklySales.value = 8750.50

        // Monthly sales
        _monthlySales.value = 32500.00

        // Top products
        _topProducts.value = listOf(
            TopProduct("Coca-Cola 20oz", 45, 112.05),
            TopProduct("Marlboro Red", 32, 287.68),
            TopProduct("Doritos Nacho", 28, 55.72),
            TopProduct("Red Bull 8.4oz", 25, 74.75),
            TopProduct("Snickers Bar", 22, 28.38)
        )

        // Sales by category
        val total = _dailySales.value
        _salesByCategory.value = listOf(
            CategorySales("Beverages", 425.50, (425.50 / total * 100).toFloat()),
            CategorySales("Tobacco", 380.25, (380.25 / total * 100).toFloat()),
            CategorySales("Snacks", 285.00, (285.00 / total * 100).toFloat()),
            CategorySales("Electronics", 95.00, (95.00 / total * 100).toFloat()),
            CategorySales("General", 65.00, (65.00 / total * 100).toFloat())
        )
    }

    fun onPeriodSelected(period: TimePeriod) {
        _selectedPeriod.value = period
        // In real implementation, reload data for selected period
        viewModelScope.launch {
            generateMockData() // Refresh with new period data
        }
    }

    fun exportReport() {
        viewModelScope.launch {
            // Export to CSV or PDF
            println("Exporting report for period: ${_selectedPeriod.value}")
            // Would generate CSV with:
            // - Period summary (daily/weekly/monthly totals)
            // - Top products list
            // - Category breakdown
            // - Transaction count
        }
    }

    // Calculate trend compared to previous period
    fun getSalesTrend(): Float {
        // Mock: 5% increase
        return 5.2f
    }

    // Get average transaction value
    fun getAverageTransaction(): Double {
        return _dailySales.value / 45 // Mock: 45 transactions
    }

    // Get total transaction count
    fun getTransactionCount(): Int {
        return 45 // Mock
    }
}