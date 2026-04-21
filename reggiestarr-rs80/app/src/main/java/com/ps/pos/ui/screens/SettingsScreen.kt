package com.ps.pos.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.ps.pos.viewmodel.SettingsViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    onBack: () -> Unit,
    viewModel: SettingsViewModel = viewModel()
) {
    val settings by viewModel.settings.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Settings") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Tax Settings
            SettingsSection(title = "Tax Settings") {
                OutlinedTextField(
                    value = settings.taxRate,
                    onValueChange = viewModel::onTaxRateChange,
                    label = { Text("Tax Rate (e.g., 0.0825 for 8.25%)") },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                    modifier = Modifier.fillMaxWidth()
                )
            }

            // Printer Settings
            SettingsSection(title = "Printer Settings") {
                OutlinedTextField(
                    value = settings.printerIp,
                    onValueChange = viewModel::onPrinterIpChange,
                    label = { Text("Printer IP Address") },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                    modifier = Modifier.fillMaxWidth()
                )

                OutlinedTextField(
                    value = settings.printerPort,
                    onValueChange = viewModel::onPrinterPortChange,
                    label = { Text("Printer Port (default: 9100)") },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                    modifier = Modifier.fillMaxWidth()
                )

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Auto-print receipts")
                    Switch(
                        checked = settings.autoPrint,
                        onCheckedChange = viewModel::onAutoPrintChange
                    )
                }
            }

            // Store Settings
            SettingsSection(title = "Store Settings") {
                OutlinedTextField(
                    value = settings.storeName,
                    onValueChange = viewModel::onStoreNameChange,
                    label = { Text("Store Name (appears on receipts)") },
                    modifier = Modifier.fillMaxWidth()
                )

                OutlinedTextField(
                    value = settings.storeAddress,
                    onValueChange = viewModel::onStoreAddressChange,
                    label = { Text("Store Address") },
                    maxLines = 3,
                    modifier = Modifier.fillMaxWidth()
                )

                OutlinedTextField(
                    value = settings.receiptFooter,
                    onValueChange = viewModel::onReceiptFooterChange,
                    label = { Text("Receipt Footer Text") },
                    modifier = Modifier.fillMaxWidth()
                )
            }

            // App Settings
            SettingsSection(title = "App Settings") {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Require login")
                    Switch(
                        checked = settings.requireLogin,
                        onCheckedChange = viewModel::onRequireLoginChange
                    )
                }

                if (settings.requireLogin) {
                    OutlinedTextField(
                        value = settings.cashierPassword,
                        onValueChange = viewModel::onCashierPasswordChange,
                        label = { Text("Cashier Password") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.NumberPassword),
                        modifier = Modifier.fillMaxWidth()
                    )
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Sound effects")
                    Switch(
                        checked = settings.soundEffects,
                        onCheckedChange = viewModel::onSoundEffectsChange
                    )
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Auto-lock screen (minutes)")
                    Text(settings.autoLockMinutes.toString())
                }
                Slider(
                    value = settings.autoLockMinutes.toFloat(),
                    onValueChange = { viewModel.onAutoLockChange(it.toInt()) },
                    valueRange = 0f..30f,
                    steps = 5
                )
            }

            Spacer(modifier = Modifier.height(32.dp))

            // Action Buttons
            Button(
                onClick = { viewModel.saveSettings() },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Save Settings")
            }

            OutlinedButton(
                onClick = { viewModel.resetToDefaults() },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Reset to Defaults")
            }

            OutlinedButton(
                onClick = { viewModel.exportData() },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Export Data (Backup)")
            }

            OutlinedButton(
                onClick = { viewModel.importData() },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Import Data (Restore)")
            }
        }
    }
}

@Composable
fun SettingsSection(
    title: String,
    content: @Composable ColumnScope.() -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text(
                text = title,
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary
            )
            Divider()
            content()
        }
    }
}