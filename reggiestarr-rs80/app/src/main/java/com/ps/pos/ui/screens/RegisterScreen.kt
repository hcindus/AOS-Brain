package com.ps.pos.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.ps.pos.data.entities.Product
import com.ps.pos.ui.components.CalculatorKeypad
import com.ps.pos.viewmodel.RegisterViewModel
import java.text.NumberFormat

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RegisterScreen(viewModel: RegisterViewModel) {
    val products by viewModel.products.collectAsState()
    val cart by viewModel.cart.collectAsState()
    val currentInput by viewModel.currentInput.collectAsState()
    val showCheckout by viewModel.showCheckout.collectAsState()
    
    val currencyFormat = NumberFormat.getCurrencyInstance()
    
    Column(modifier = Modifier.fillMaxSize()) {
        // Product Grid (top half)
        LazyVerticalGrid(
            columns = GridCells.Fixed(3),
            modifier = Modifier.weight(1f),
            contentPadding = PaddingValues(8.dp)
        ) {
            items(products) { product ->
                ProductButton(
                    product = product,
                    onClick = { viewModel.onProductClick(product) }
                )
            }
        }
        
        // Cart and Input Section
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f),
            elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
        ) {
            Row(modifier = Modifier.fillMaxSize()) {
                // Cart Display
                Column(
                    modifier = Modifier
                        .weight(1f)
                        .padding(8.dp)
                ) {
                    Text(
                        "Cart",
                        style = MaterialTheme.typography.titleMedium
                    )
                    
                    LazyColumn(
                        modifier = Modifier.weight(1f)
                    ) {
                        items(cart) { item ->
                            CartItemRow(
                                item = item,
                                onRemove = { viewModel.removeFromCart(cart.indexOf(item)) }
                            )
                        }
                    }
                    
                    // Totals
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
                    
                    Divider(modifier = Modifier.padding(vertical = 4.dp))
                    Text("Subtotal: ${currencyFormat.format(subtotal)}")
                    Text("Tax: ${currencyFormat.format(tax)}")
                    Text(
                        "Total: ${currencyFormat.format(total)}",
                        style = MaterialTheme.typography.titleLarge,
                        color = MaterialTheme.colorScheme.primary
                    )
                    
                    // Checkout Button
                    Button(
                        onClick = { viewModel.onCheckout() },
                        modifier = Modifier.fillMaxWidth(),
                        enabled = cart.isNotEmpty()
                    ) {
                        Icon(Icons.Default.ShoppingCart, contentDescription = null)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Checkout")
                    }
                }
                
                // Calculator and Input
                Column(
                    modifier = Modifier
                        .weight(1f)
                        .padding(8.dp)
                ) {
                    // Current input display
                    OutlinedTextField(
                        value = currentInput,
                        onValueChange = { },
                        readOnly = true,
                        label = { Text("PLU / Price") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    // Calculator Keypad (7-8-9 top, Clear/Enter top row)
                    CalculatorKeypad(
                        onDigit = { viewModel.onDigitInput(it) },
                        onClear = { viewModel.onClear() },
                        onDelete = { viewModel.onDelete() },
                        onEnter = { viewModel.onEnter() },
                        modifier = Modifier.fillMaxSize()
                    )
                }
            }
        }
    }
    
    // Checkout Dialog
    if (showCheckout) {
        CheckoutDialog(
            cart = cart,
            onDismiss = { viewModel.dismissCheckout() },
            onComplete = { paymentType, tendered ->
                viewModel.completeCheckout(paymentType, tendered)
            }
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun ProductButton(
    product: Product,
    onClick: () -> Unit
) {
    val displayPrice = if (product.openPrice) "OPEN" else
        NumberFormat.getCurrencyInstance().format(product.price)
    
    Card(
        onClick = onClick,
        modifier = Modifier
            .padding(4.dp)
            .aspectRatio(1f),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(8.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text(
                text = product.name,
                style = MaterialTheme.typography.bodyMedium,
                textAlign = TextAlign.Center,
                maxLines = 2
            )
            Text(
                text = displayPrice,
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary
            )
            if (product.taxType != "EXCLUSIVE") {
                Text(
                    text = product.taxType,
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.secondary
                )
            }
        }
    }
}

@Composable
private fun CartItemRow(
    item: RegisterViewModel.CartItem,
    onRemove: () -> Unit
) {
    val currencyFormat = NumberFormat.getCurrencyInstance()
    
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(
                item.product.name,
                style = MaterialTheme.typography.bodyMedium
            )
            Text(
                "${item.quantity.toInt()} × ${currencyFormat.format(item.unitPrice)}",
                style = MaterialTheme.typography.bodySmall
            )
        }
        Text(
            currencyFormat.format(item.unitPrice * item.quantity),
            style = MaterialTheme.typography.bodyMedium
        )
        IconButton(onClick = onRemove) {
            Icon(Icons.Default.Delete, contentDescription = "Remove")
        }
    }
}
