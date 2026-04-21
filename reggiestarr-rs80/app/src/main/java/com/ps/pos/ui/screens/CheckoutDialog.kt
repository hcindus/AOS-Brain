package com.ps.pos.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import java.text.NumberFormat

@Composable
fun CheckoutDialog(
    cart: List<com.ps.pos.viewmodel.RegisterViewModel.CartItem>,
    onDismiss: () -> Unit,
    onComplete: (String, Double) -> Unit
) {
    val currencyFormat = NumberFormat.getCurrencyInstance()
    
    val subtotal = cart.sumOf { it.unitPrice * it.quantity }
    val tax = cart.sumOf { 
        val (_, taxAmt) = com.ps.pos.utils.TaxCalculator.calculateTax(
            it.unitPrice * it.quantity,
            it.product.taxRate,
            it.product.taxType
        )
        taxAmt
    }
    val total = subtotal + tax

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Checkout", style = MaterialTheme.typography.headlineSmall) },
        text = {
            Column {
                // Cart summary
                cart.forEach { item ->
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text("${item.product.name} (${item.quantity.toInt()})")
                        Text(currencyFormat.format(item.unitPrice * item.quantity))
                    }
                }
                
                Divider(modifier = Modifier.padding(vertical = 8.dp))
                
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("Subtotal:")
                    Text(currencyFormat.format(subtotal))
                }
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("Tax:")
                    Text(currencyFormat.format(tax))
                }
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        "Total:",
                        style = MaterialTheme.typography.titleMedium
                    )
                    Text(
                        currencyFormat.format(total),
                        style = MaterialTheme.typography.titleMedium,
                        color = MaterialTheme.colorScheme.primary
                    )
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                Text(
                    "Payment: Cash Only (MVP)",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.secondary
                )
            }
        },
        confirmButton = {
            Button(
                onClick = { onComplete("CASH", total) }
            ) {
                Text("Complete Sale")
            }
        },
        dismissButton = {
            OutlinedButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}

@Composable
fun TransactionHistoryScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            "Transaction History",
            style = MaterialTheme.typography.headlineMedium
        )
        Text(
            "(ViewModel integration pending)",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.secondary
        )
    }
}

@Composable
fun SettingsScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            "Settings",
            style = MaterialTheme.typography.headlineMedium
        )
        Text(
            "Tax rates, printer config, etc.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.secondary
        )
    }
}
