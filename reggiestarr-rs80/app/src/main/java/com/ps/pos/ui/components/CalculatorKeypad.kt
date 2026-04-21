package com.ps.pos.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun CalculatorKeypad(
    onProductLookup: (String) -> Unit,
    onQuantity: (Int) -> Unit,
    onAddToCart: () -> Unit,
    modifier: Modifier = Modifier
) {
    var display by remember { mutableStateOf("") }
    var mode by remember { mutableStateOf(KeypadMode.QUANTITY) }

    Column(
        modifier = modifier
            .fillMaxHeight()
            .background(Color(0xFF2C2C2C))
            .padding(8.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // Display
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(80.dp)
                .background(Color(0xFF1A1A1A), RoundedCornerShape(8.dp))
                .padding(16.dp),
            contentAlignment = Alignment.CenterEnd
        ) {
            Text(
                text = display.ifEmpty { "0" },
                fontSize = 48.sp,
                fontWeight = FontWeight.Bold,
                color = Color.White,
                textAlign = TextAlign.End
            )
        }

        Spacer(modifier = Modifier.height(8.dp))

        // Mode indicator
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            ModeButton("QTY", mode == KeypadMode.QUANTITY) { mode = KeypadMode.QUANTITY }
            ModeButton("PLU", mode == KeypadMode.PLU) { mode = KeypadMode.PLU }
            ModeButton("PRICE", mode == KeypadMode.PRICE) { mode = KeypadMode.PRICE }
        }

        Spacer(modifier = Modifier.height(8.dp))

        // Keypad grid
        Column(
            modifier = Modifier.weight(1f),
            verticalArrangement = Arrangement.SpaceEvenly
        ) {
            // Row 7 8 9
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                CalcButton("7") { display += "7" }
                CalcButton("8") { display += "8" }
                CalcButton("9") { display += "9" }
            }
            // Row 4 5 6
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                CalcButton("4") { display += "4" }
                CalcButton("5") { display += "5" }
                CalcButton("6") { display += "6" }
            }
            // Row 1 2 3
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                CalcButton("1") { display += "1" }
                CalcButton("2") { display += "2" }
                CalcButton("3") { display += "3" }
            }
            // Row C 0 00
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                CalcButton("C", Color(0xFFE53935)) {
                    display = ""
                }
                CalcButton("0") { display += "0" }
                CalcButton("00") { display += "00" }
            }
            // Row . +/- Enter
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                CalcButton(".", Color(0xFF757575)) { if (!display.contains(".")) display += "." }
                CalcButton("+/-", Color(0xFF757575)) {
                    display = if (display.startsWith("-")) display.drop(1) else "-$display"
                }
                ActionButton("ENTER", Color(0xFF43A047)) {
                    when (mode) {
                        KeypadMode.QUANTITY -> display.toIntOrNull()?.let { onQuantity(it) }
                        KeypadMode.PLU -> if (display.isNotEmpty()) onProductLookup(display)
                        KeypadMode.PRICE -> {}
                    }
                    display = ""
                }
            }
        }

        Spacer(modifier = Modifier.height(8.dp))

        // Add to cart
        Button(
            onClick = onAddToCart,
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF1976D2))
        ) {
            Text("ADD TO CART", fontSize = 20.sp, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun CalcButton(
    text: String,
    color: Color = Color(0xFF424242),
    onClick: () -> Unit
) {
    Button(
        onClick = onClick,
        modifier = Modifier.size(72.dp),
        shape = CircleShape,
        colors = ButtonDefaults.buttonColors(containerColor = color)
    ) {
        Text(text, fontSize = 24.sp, fontWeight = FontWeight.Bold)
    }
}

@Composable
fun ActionButton(
    text: String,
    color: Color = Color(0xFF43A047),
    onClick: () -> Unit
) {
    Button(
        onClick = onClick,
        modifier = Modifier.size(width = 144.dp, height = 72.dp),
        shape = RoundedCornerShape(36.dp),
        colors = ButtonDefaults.buttonColors(containerColor = color)
    ) {
        Text(text, fontSize = 16.sp, fontWeight = FontWeight.Bold)
    }
}

@Composable
fun ModeButton(text: String, selected: Boolean, onClick: () -> Unit) {
    Button(
        onClick = onClick,
        modifier = Modifier.size(width = 80.dp, height = 36.dp),
        colors = ButtonDefaults.buttonColors(
            containerColor = if (selected) Color(0xFF1976D2) else Color(0xFF616161)
        )
    ) {
        Text(text, fontSize = 12.sp)
    }
}

enum class KeypadMode {
    QUANTITY, PLU, PRICE
}