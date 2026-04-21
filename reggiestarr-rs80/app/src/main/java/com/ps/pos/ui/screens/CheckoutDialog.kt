package com.ps.pos.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog

@Composable
fun CheckoutDialog(
    total: Double,
    onDismiss: () -> Unit,
    onComplete: (String, Double) -> Unit
) {
    var paymentType by remember { mutableStateOf("Cash") }
    var tendered by remember { mutableStateOf(total.toString()) }
    val change = tendered.toDoubleOrNull()?.minus(total) ?: 0.0

    Dialog(onDismissRequest = onDismiss) {
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
        ) {
            Column(
                modifier = Modifier.padding(20.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(
                    "Checkout",
                    style = MaterialTheme.typography.headlineSmall
                )

                Spacer(modifier = Modifier.height(16.dp))

                // Total
                Text(
                    "Total: $${String.format("%.2f", total)}",
                    style = MaterialTheme.typography.headlineMedium,
                    color = MaterialTheme.colorScheme.primary
                )

                Spacer(modifier = Modifier.height(16.dp))

                // Payment type
                Text("Payment Method", style = MaterialTheme.typography.bodyLarge)
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    PaymentButton("Cash", paymentType == "Cash") { paymentType = "Cash" }
                    PaymentButton("Card", paymentType == "Card") { paymentType = "Card" }
                    PaymentButton("Other", paymentType == "Other") { paymentType = "Other" }
                }

                Spacer(modifier = Modifier.height(16.dp))

                // Tendered amount
                OutlinedTextField(
                    value = tendered,
                    onValueChange = { tendered = it },
                    label = { Text("Amount Tendered") },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                    modifier = Modifier.fillMaxWidth()
                )

                Spacer(modifier = Modifier.height(16.dp))

                // Change
                if (change >= 0) {
                    Text(
                        "Change: $${String.format("%.2f", change)}",
                        style = MaterialTheme.typography.headlineSmall,
                        color = MaterialTheme.colorScheme.tertiary
                    )
                }

                Spacer(modifier = Modifier.height(24.dp))

                // Buttons
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    OutlinedButton(onClick = onDismiss) {
                        Text("Cancel")
                    }
                    Button(
                        onClick = {
                            tendered.toDoubleOrNull()?.let {
                                onComplete(paymentType, it)
                            }
                        },
                        enabled = tendered.toDoubleOrNull() != null && tendered.toDoubleOrNull()!! >= total
                    ) {
                        Text("Complete Sale")
                    }
                }
            }
        }
    }
}

@Composable
fun PaymentButton(text: String, selected: Boolean, onClick: () -> Unit) {
    Button(
        onClick = onClick,
        colors = ButtonDefaults.buttonColors(
            containerColor = if (selected) MaterialTheme.colorScheme.primary
            else MaterialTheme.colorScheme.surfaceVariant
        )
    ) {
        Text(text)
    }
}