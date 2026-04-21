package com.ps.pos.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.QrCodeScanner
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ps.pos.data.entities.LineItem
import com.ps.pos.ui.components.CalculatorKeypad
import com.ps.pos.viewmodel.RegisterViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RegisterScreen(
    viewModel: RegisterViewModel,
    onNavigateToProducts: () -> Unit = {},
    onNavigateToTransactions: () -> Unit = {},
    onNavigateToSettings: () -> Unit = {}
) {
    val cartItems by viewModel.cartItems.collectAsState()
    val subtotal by viewModel.subtotal.collectAsState()
    val tax by viewModel.tax.collectAsState()
    val total by viewModel.total.collectAsState()
    var showCheckout by remember { mutableStateOf(false) }
    var showMenu by remember { mutableStateOf(false) }
    var showBarcodeInput by remember { mutableStateOf(false) }
    var barcodeText by remember { mutableStateOf("") }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("ReggieStarr RS-80") },
                actions = {
                    IconButton(onClick = { showMenu = true }) {
                        Icon(Icons.Default.Menu, "Menu")
                    }
                    IconButton(onClick = { showBarcodeInput = true }) {
                        Icon(Icons.Default.QrCodeScanner, "Scan Barcode")
                    }
                    DropdownMenu(
                        expanded = showMenu,
                        onDismissRequest = { showMenu = false }
                    ) {
                        DropdownMenuItem(
                            text = { Text("Products") },
                            onClick = {
                                showMenu = false
                                onNavigateToProducts()
                            }
                        )
                        DropdownMenuItem(
                            text = { Text("Transactions") },
                            onClick = {
                                showMenu = false
                                onNavigateToTransactions()
                            }
                        )
                        DropdownMenuItem(
                            text = { Text("Settings") },
                            onClick = {
                                showMenu = false
                                onNavigateToSettings()
                            }
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        }
    ) { padding ->
        Row(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            // Left side - Cart
            Column(
                modifier = Modifier
                    .weight(0.6f)
                    .fillMaxHeight()
                    .padding(16.dp)
            ) {
                // Cart header
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        "Cart (${cartItems.size})",
                        style = MaterialTheme.typography.headlineSmall
                    )
                    IconButton(onClick = { viewModel.clearCart() }) {
                        Icon(Icons.Default.Delete, "Clear cart")
                    }
                }

                // Cart items
                LazyColumn(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxWidth()
                ) {
                    items(cartItems) { item ->
                        CartItemRow(
                            item = item,
                            onRemove = { viewModel.removeFromCart(item) }
                        )
                    }
                }

                Divider(modifier = Modifier.padding(vertical = 8.dp))

                // Totals
                TotalRow("Subtotal:", subtotal)
                TotalRow("Tax (8.25%):", tax)
                TotalRow("Total:", total, isTotal = true)

                Spacer(modifier = Modifier.height(8.dp))

                // Checkout button
                Button(
                    onClick = { showCheckout = true },
                    modifier = Modifier.fillMaxWidth(),
                    enabled = cartItems.isNotEmpty()
                ) {
                    Icon(Icons.Default.ShoppingCart, null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("CHECKOUT")
                }
            }

            // Right side - Calculator Keypad
            CalculatorKeypad(
                onProductLookup = { plu -> viewModel.lookupProduct(plu) },
                onQuantity = { qty -> viewModel.setQuantity(qty) },
                onAddToCart = { viewModel.addToCart() },
                modifier = Modifier.weight(0.4f)
            )
        }
    }

    if (showCheckout) {
        CheckoutDialog(
            total = total,
            onDismiss = { showCheckout = false },
            onComplete = { paymentType, tendered ->
                viewModel.completeTransaction(paymentType, tendered)
                showCheckout = false
            }
        )
    }
}

@Composable
fun CartItemRow(item: LineItem, onRemove: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = item.productName,
                    style = MaterialTheme.typography.bodyLarge
                )
                Text(
                    text = "${item.quantity} x $${String.format("%.2f", item.unitPrice)}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            Text(
                text = "$${String.format("%.2f", item.totalPrice)}",
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.primary
            )
        }
    }
}

@Composable
fun TotalRow(label: String, amount: Double, isTotal: Boolean = false) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(
            text = label,
            style = if (isTotal) MaterialTheme.typography.headlineSmall
            else MaterialTheme.typography.bodyLarge
        )
        Text(
            text = "$${String.format("%.2f", amount)}",
            style = if (isTotal) MaterialTheme.typography.headlineSmall
            else MaterialTheme.typography.bodyLarge,
            color = if (isTotal) MaterialTheme.colorScheme.primary
            else MaterialTheme.colorScheme.onSurface
        )
    }
}