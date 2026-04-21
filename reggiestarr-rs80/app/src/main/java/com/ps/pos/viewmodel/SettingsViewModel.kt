package com.ps.pos.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

data class SettingsState(
    val taxRate: String = "0.0825",
    val printerIp: String = "192.168.1.100",
    val printerPort: String = "9100",
    val autoPrint: Boolean = true,
    val storeName: String = "ReggieStarr RS-80",
    val storeAddress: String = "",
    val receiptFooter: String = "Thank you for your business!",
    val requireLogin: Boolean = false,
    val cashierPassword: String = "",
    val soundEffects: Boolean = true,
    val autoLockMinutes: Int = 5
)

class SettingsViewModel : ViewModel() {

    private val _settings = MutableStateFlow(SettingsState())
    val settings: StateFlow<SettingsState> = _settings.asStateFlow()

    private val _saveStatus = MutableStateFlow<String?>(null)
    val saveStatus: StateFlow<String?> = _saveStatus.asStateFlow()

    init {
        // Load saved settings (mock implementation)
        viewModelScope.launch {
            loadSettings()
        }
    }

    private suspend fun loadSettings() {
        // In real implementation, load from SharedPreferences or DataStore
        _settings.value = SettingsState()
    }

    fun onTaxRateChange(value: String) {
        _settings.value = _settings.value.copy(taxRate = value)
    }

    fun onPrinterIpChange(value: String) {
        _settings.value = _settings.value.copy(printerIp = value)
    }

    fun onPrinterPortChange(value: String) {
        _settings.value = _settings.value.copy(printerPort = value)
    }

    fun onAutoPrintChange(value: Boolean) {
        _settings.value = _settings.value.copy(autoPrint = value)
    }

    fun onStoreNameChange(value: String) {
        _settings.value = _settings.value.copy(storeName = value)
    }

    fun onStoreAddressChange(value: String) {
        _settings.value = _settings.value.copy(storeAddress = value)
    }

    fun onReceiptFooterChange(value: String) {
        _settings.value = _settings.value.copy(receiptFooter = value)
    }

    fun onRequireLoginChange(value: Boolean) {
        _settings.value = _settings.value.copy(requireLogin = value)
    }

    fun onCashierPasswordChange(value: String) {
        _settings.value = _settings.value.copy(cashierPassword = value)
    }

    fun onSoundEffectsChange(value: Boolean) {
        _settings.value = _settings.value.copy(soundEffects = value)
    }

    fun onAutoLockChange(minutes: Int) {
        _settings.value = _settings.value.copy(autoLockMinutes = minutes)
    }

    fun saveSettings() {
        viewModelScope.launch {
            // In real implementation, save to SharedPreferences or DataStore
            println("Saving settings: ${_settings.value}")
            _saveStatus.value = "Settings saved successfully!"

            // Clear status after delay
            kotlinx.coroutines.delay(2000)
            _saveStatus.value = null
        }
    }

    fun resetToDefaults() {
        _settings.value = SettingsState()
    }

    fun exportData() {
        viewModelScope.launch {
            // Export products and transactions to CSV/JSON
            println("Exporting data...")
            _saveStatus.value = "Data exported to Downloads/"
            kotlinx.coroutines.delay(2000)
            _saveStatus.value = null
        }
    }

    fun importData() {
        viewModelScope.launch {
            // Import products and transactions from backup
            println("Importing data...")
            _saveStatus.value = "Data imported successfully!"
            kotlinx.coroutines.delay(2000)
            _saveStatus.value = null
        }
    }
}